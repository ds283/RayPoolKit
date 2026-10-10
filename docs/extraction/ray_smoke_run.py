#!/usr/bin/env python3
"""
Drive ``RayWorkPool`` under a real, local Ray instance (extraction prompt 07 §2.2; decision U13).

The test suite never starts Ray: it drives the pool through an in-process stand-in for
``ray.wait`` and ``ray.get`` (decision U6). This script is the one place where the pool runs
against Ray itself. It is not a test: the suite does not collect it, and it does not run in CI.

**How it is run.** From a checkout or an export, with the package importable and its tests in the
tree (the script imports the three printed-line patterns from
``raypoolkit.tests.test_printed_lines``, so an installed wheel, which carries no tests, will not
do), with no Ray running:

    env -u PYTHONPATH ./venv/bin/python docs/extraction/ray_smoke_run.py

It imports only the standard library, ``ray`` and ``raypoolkit``. Its objects (``Item``, the
remote functions, the ``Store`` actor and ``StorePool``) are defined here, so Ray pickles them by
value; it uses no stand-in and imports no client.

**No usage report.** Ray reports usage statistics to its servers when ``~/.ray/config.json`` (or
its own default) enables them, and the reporter runs even with ``include_dashboard=False``. The
environment variable ``RAY_USAGE_STATS_ENABLED=0`` takes priority over the file, so the script sets
it, by assignment, before it imports ``ray`` or ``raypoolkit``. It changes no file of Ray's.

**What it does.**

1. It prints Python's, Ray's and ``raypoolkit``'s versions (the last from ``importlib.metadata``),
   ``raypoolkit.__file__``, the module of ``ray.wait`` and ``ray.get``, and checks that the pool
   module's ``ray`` is the ``ray`` imported here and that neither function is a ``unittest.mock``
   object.
2. **It refuses to run**, exiting 2 before it starts anything, if ``ray.is_initialized()`` is
   already true or ``pgrep -lf 'gcs_server|raylet|ray::'`` finds a process. It prints each
   process's id and the first word of its command line, no more: a ``ray::`` process rewrites its
   title, and on macOS the rest can be its environment.
3. It starts Ray with ``ray.init(num_cpus=4, include_dashboard=False, log_to_driver=False)``, which
   starts a local instance and connects to none, and calls ``ray.shutdown()`` in a ``finally``.
4. It runs five steps, each isolated: an exception in a step is that step's ``FAIL``, with its type
   and message, and the next step runs. Each prints ``PASS`` or ``FAIL`` with what it saw, and the
   pool's printed lines are captured, not passed through.

   1. **lookup-only**: ``compute_handler=None``, a generator ``task_list`` of 20 items,
      ``store_results=True``, ``create_batch_size=3``, ``process_batch_size=4``,
      ``max_task_queue=5``; ``results`` holds the 20 objects, in order.
   2. **the compute path**: 12 items, each built as ``{"ref": ..., "compute_payload": 1}``, with a
      label builder and a validation handler, ``store_results=True``, ``process_batch_size=3``,
      ``max_task_queue=4``, titled; every result is the persisted object (``store_id`` 1-12 over
      the 12, ``stored``, ``available``, the label and payload its compute was given, the value
      its compute task returned), and the completion line counts 12 lookup, compute, store and
      validation.
   3. **a persist with no validation, then a post handler**: 5 items; the post handler is given
      each object with its ``store_id`` set, and is given the object ``results`` holds.
   4. **the availability path**: ``compute_handler=None``, an availability handler and a post
      handler, and a task builder that returns ``None`` for one item and a list of two lookups for
      each of the other five; the availability handler is called on each of the 10 objects looked
      up, and the post handler on each once its task completes.
   5. **the printed lines in real time**: a titled lookup-only pool of 30 remote tasks of 0.05 s,
      notifying on every pass (``notify_min_time_interval=0``, ``notify_time_interval=0``,
      ``notify_batch_size=1``), ``process_batch_size=2``, stdout captured: one banner, one
      progress line per pass of ``run()`` (the count is derived from the step's own sizes, below)
      and one completion line match the three patterns; no stamp carries a UTC offset; and
      ``total_time`` is set. The lines it matched are printed.

5. After ``ray.shutdown()`` it polls ``pgrep`` for up to 10 s and prints how many Ray processes
   are left. That count is reported, not judged.

Every value a step asserts is the script's own: counts and orders it built, never a figure read
from a log.

**Exit status.** 0 if every step passes, 1 if any fails, 2 if it refused to run.
"""

import os

# Before ``ray`` or ``raypoolkit`` is imported (see the docstring).
os.environ["RAY_USAGE_STATS_ENABLED"] = "0"

import contextlib
import importlib.metadata
import io
import re
import subprocess
import sys
import time
import traceback
import unittest.mock

import ray

import raypoolkit
from raypoolkit import RayWorkPool
from raypoolkit.tests.test_printed_lines import (
    BANNER_PATTERN,
    COMPLETE_PATTERN,
    PROGRESS_PATTERN,
)

RAY_PATTERN = "gcs_server|raylet|ray::"
INIT_ARGUMENTS = {"num_cpus": 4, "include_dashboard": False, "log_to_driver": False}

# A progress line's stamp, followed directly by the running time: no UTC offset between them.
STAMP_WITHOUT_OFFSET = re.compile(r"^   -- \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \(")


class StepFailure(Exception):
    pass


def check(condition, message):
    if not condition:
        raise StepFailure(message)


# --- The objects the pool drives --------------------------------------------------------------


class Item:
    """A work object: ``available``, ``compute(label=None, payload=None)`` and ``store()``."""

    def __init__(self, n, available):
        self.n = n
        self.available = available
        self.store_id = None
        self.stored = False
        self.compute_kwargs = None
        self.value = None
        self._compute_ref = None

    def compute(self, label=None, payload=None):
        self.compute_kwargs = {"label": label, "payload": payload}
        self._compute_ref = compute_value.remote(self.n, payload)
        return self._compute_ref

    def store(self):
        # Called by the default store handler on the driver, once the compute task has completed.
        self.value = ray.get(self._compute_ref)
        self._compute_ref = None
        self.stored = True


@ray.remote
def lookup(n, available):
    return Item(n, available)


@ray.remote
def slow_lookup(n):
    time.sleep(0.05)
    return Item(n, True)


@ray.remote
def compute_value(n, payload):
    return 1000 * n + (payload if payload is not None else 0)


@ray.remote
def acknowledge(n):
    return n


@ray.remote
class Store:
    def __init__(self):
        self._next_store_id = 1

    def object_store(self, obj):
        obj.store_id = self._next_store_id
        self._next_store_id += 1
        obj.available = True
        return obj

    def validate(self, obj):
        return True


class StorePool:
    """The datastore pool: its ``object_store`` calls the ``Store`` actor."""

    def __init__(self):
        self.actor = Store.remote()

    def object_store(self, obj):
        return self.actor.object_store.remote(obj)


def run_captured(build):
    """Construct a pool with ``build()`` and run it, capturing stdout; return (pool, lines)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        pool = build()
        pool.run()
    return pool, buffer.getvalue().splitlines()


def expected_passes(num_items, create_batch_size, process_batch_size, max_task_queue):
    """
    The number of passes of ``run()``'s loop for a lookup-only pool in which every work item is
    one lookup task and no lookup starts another task: the loop's own counting
    (``raypoolkit/RayWorkPool.py:286-358`` at ``v0.2.0``), with the tasks as counts. Each pass
    builds up to ``create_batch_size`` items when fewer than ``max_task_queue`` tasks are in
    flight, then waits for ``min(process_batch_size, in flight)`` of them, so with both notify
    intervals 0 each pass prints one progress notification (``:563-595``).
    """
    todo, inflight, passes = num_items, 0, 0
    while inflight > 0 or todo > 0:
        if inflight < max_task_queue and todo > 0:
            built = min(create_batch_size, todo)
            todo -= built
            inflight += built
        inflight -= min(process_batch_size, inflight)
        passes += 1
    return passes


# --- The steps ---------------------------------------------------------------------------------


def step_1_lookup_only():
    count = 20
    pool, lines = run_captured(
        lambda: RayWorkPool(
            None,
            (n for n in range(count)),
            lambda n: lookup.remote(n, True),
            compute_handler=None,
            store_results=True,
            create_batch_size=3,
            process_batch_size=4,
            max_task_queue=5,
        )
    )
    seen = [getattr(obj, "n", obj) for obj in pool.results]
    check(
        seen == list(range(count)), f"results hold {seen}, not 0..{count - 1} in order"
    )
    check(lines == [], f"an untitled pool printed {lines!r}")
    return f"results hold the {count} objects in order ({seen[0]}..{seen[-1]}); nothing printed"


def step_2_compute_path():
    count = 12
    store = StorePool()
    title = "Smoke run, step 2"
    try:
        pool, lines = run_captured(
            lambda: RayWorkPool(
                store,
                list(range(count)),
                lambda n: {"ref": lookup.remote(n, False), "compute_payload": 1},
                validation_handler=lambda obj: store.actor.validate.remote(obj),
                label_builder=lambda obj: f"item-{obj.n}",
                store_results=True,
                process_batch_size=3,
                max_task_queue=4,
                title=title,
            )
        )
    finally:
        ray.kill(store.actor)

    results = pool.results
    check(
        [obj.n for obj in results] == list(range(count)),
        f"results hold {[obj.n for obj in results]}",
    )
    store_ids = sorted(obj.store_id for obj in results)
    check(store_ids == list(range(1, count + 1)), f"store_ids are {store_ids}")
    check(all(obj.stored for obj in results), "an object was not stored")
    check(all(obj.available for obj in results), "an object is not available")
    kwargs = [obj.compute_kwargs for obj in results]
    check(
        kwargs == [{"label": f"item-{n}", "payload": 1} for n in range(count)],
        f"the compute arguments were {kwargs}",
    )
    values = [obj.value for obj in results]
    check(
        values == [1000 * n + 1 for n in range(count)],
        f"the computed values were {values}",
    )
    check(
        not any("WARNING" in line for line in lines), f"a warning was printed: {lines}"
    )
    summary = [line for line in lines if "Queue summary:" in line]
    check(len(summary) == 1, f"{len(summary)} 'Queue summary' lines")
    counted = dict(
        (kind, int(number))
        for number, kind in re.findall(
            r"(\d+) (lookup|compute|store|available|validation)", summary[0]
        )
    )
    wanted = {"lookup": count, "compute": count, "store": count, "validation": count}
    check(counted == wanted, f"the completion line counts {counted}")
    check(
        sum(1 for line in lines if COMPLETE_PATTERN.search(line)) == 1,
        "not one completion line",
    )
    return (
        f"{count} results persisted, in order; store_ids {store_ids[0]}-{store_ids[-1]}; "
        f"stored and available; labels item-0..item-{count - 1}, payload 1; values from the "
        f"compute tasks; completion line: {summary[0].strip()}"
    )


def step_3_persist_then_post():
    count = 5
    store = StorePool()
    seen = []

    def post_handler(obj):
        seen.append(obj)
        return None

    try:
        pool, lines = run_captured(
            lambda: RayWorkPool(
                store,
                list(range(count)),
                lambda n: lookup.remote(n, False),
                post_handler=post_handler,
                store_results=True,
            )
        )
    finally:
        ray.kill(store.actor)

    check(len(seen) == count, f"the post handler was called {len(seen)} times")
    unset = sorted(obj.n for obj in seen if obj.store_id is None)
    check(
        not unset,
        f"the post handler was given store_id None for items {unset} "
        f"(store_ids it saw: {[obj.store_id for obj in seen]})",
    )
    by_n = {obj.n: obj for obj in seen}
    check(
        all(by_n[obj.n] is obj for obj in pool.results),
        "the post handler was not given the objects results holds",
    )
    return (
        f"the post handler saw {count} objects, store_ids "
        f"{sorted(obj.store_id for obj in seen)}, each the object results holds"
    )


def step_4_availability_path():
    items = list(range(6))
    available_seen = []
    post_seen = []

    def task_builder(n):
        if n == 0:
            return None
        return [lookup.remote(n, True), lookup.remote(100 + n, True)]

    def available_handler(obj):
        available_seen.append(obj.n)
        return acknowledge.remote(obj.n)

    def post_handler(obj):
        post_seen.append(obj.n)
        return None

    pool, lines = run_captured(
        lambda: RayWorkPool(
            None,
            items,
            task_builder,
            compute_handler=None,
            available_handler=available_handler,
            post_handler=post_handler,
        )
    )
    expected = sorted([n for n in items[1:]] + [100 + n for n in items[1:]])
    check(
        sorted(available_seen) == expected,
        f"the availability handler was called on {sorted(available_seen)}",
    )
    check(
        sorted(post_seen) == expected,
        f"the post handler was called on {sorted(post_seen)}",
    )
    check(lines == [], f"an untitled pool printed {lines!r}")
    return (
        f"the availability handler was called on the {len(expected)} objects looked up "
        f"({expected}), and the post handler on each; the item whose builder returned None "
        f"was not looked up"
    )


def step_5_printed_lines():
    count = 30
    title = "Smoke run, step 5"
    create_batch_size, process_batch_size, max_task_queue = 5, 2, 200
    pool, lines = run_captured(
        lambda: RayWorkPool(
            None,
            list(range(count)),
            lambda n: slow_lookup.remote(n),
            compute_handler=None,
            create_batch_size=create_batch_size,
            process_batch_size=process_batch_size,
            max_task_queue=max_task_queue,
            notify_min_time_interval=0,
            notify_time_interval=0,
            notify_batch_size=1,
            title=title,
        )
    )
    banners = [line for line in lines if BANNER_PATTERN.match(line)]
    progress = [line for line in lines if PROGRESS_PATTERN.search(line)]
    completes = [line for line in lines if COMPLETE_PATTERN.search(line)]
    passes = expected_passes(
        count, create_batch_size, process_batch_size, max_task_queue
    )

    print("    matched by BANNER_PATTERN:")
    for line in banners:
        print(f"      {line}")
    print("    matched by PROGRESS_PATTERN:")
    for line in progress:
        print(f"      {line}")
    print("    matched by COMPLETE_PATTERN:")
    for line in completes:
        print(f"      {line}")

    check(len(banners) == 1, f"{len(banners)} banner lines")
    check(
        BANNER_PATTERN.match(banners[0]).group(1) == title,
        f"the banner's title is {BANNER_PATTERN.match(banners[0]).group(1)!r}",
    )
    check(
        len(progress) == passes,
        f"{len(progress)} progress lines, where the step's sizes give {passes} passes",
    )
    totals = {int(PROGRESS_PATTERN.search(line).group(2)) for line in progress}
    check(totals == {count}, f"the progress lines' totals are {totals}")
    with_offset = [line for line in progress if not STAMP_WITHOUT_OFFSET.match(line)]
    check(
        not with_offset, f"stamps with a UTC offset, or not as expected: {with_offset}"
    )
    check(len(completes) == 1, f"{len(completes)} completion lines")
    total_time = getattr(pool, "total_time", None)
    check(
        isinstance(total_time, float) and total_time > 0,
        f"total_time is {total_time!r}",
    )
    return (
        f"{len(lines)} lines captured: 1 banner, {len(progress)} progress lines "
        f"(= {passes} passes for {count} tasks at create_batch_size={create_batch_size}, "
        f"process_batch_size={process_batch_size}), 1 completion line; no stamp has a UTC "
        f"offset; total_time {total_time:.3f} s"
    )


STEPS = [
    ("1", "lookup-only, a generator task_list", step_1_lookup_only),
    ("2", "the compute path", step_2_compute_path),
    (
        "3",
        "a persist with no validation, then a post handler",
        step_3_persist_then_post,
    ),
    ("4", "the availability path", step_4_availability_path),
    ("5", "the printed lines in real time", step_5_printed_lines),
]


# --- The run -----------------------------------------------------------------------------------


def ray_processes():
    """Return (returncode, output) of ``pgrep -lf`` for Ray's processes."""
    result = subprocess.run(
        ["pgrep", "-lf", RAY_PATTERN], capture_output=True, text=True, check=False
    )
    return result.returncode, result.stdout.strip()


def describe_environment():
    pool_module = sys.modules["raypoolkit.RayWorkPool"]
    print(f"python: {sys.version}")
    print(f"ray: {ray.__version__} ({ray.__file__})")
    print(f"raypoolkit: {importlib.metadata.version('raypoolkit')}")
    print(f"raypoolkit.__file__: {raypoolkit.__file__}")
    print(f"RAY_USAGE_STATS_ENABLED: {os.environ.get('RAY_USAGE_STATS_ENABLED')}")
    print(
        f"ray.wait: {ray.wait.__module__}; ray.get: {ray.get.__module__}; "
        f"the pool module's ray is this ray: {pool_module.ray is ray}"
    )
    problems = []
    if pool_module.ray is not ray:
        problems.append("the pool module's ray is not the ray imported here")
    for name in ("wait", "get"):
        if isinstance(getattr(ray, name), unittest.mock.NonCallableMock):
            problems.append(f"ray.{name} is a unittest.mock object")
    return problems


def main():
    started = time.perf_counter()
    problems = describe_environment()
    if problems:
        for problem in problems:
            print(f"REFUSED: {problem}")
        return 2

    if ray.is_initialized():
        print("REFUSED: ray.is_initialized() is already true")
        return 2
    returncode, output = ray_processes()
    if returncode != 1:
        print(f"REFUSED: pgrep -lf '{RAY_PATTERN}' exited {returncode}:")
        # Each process's id and the first word of its command line only: a ``ray::`` process
        # rewrites its title, and on macOS what follows can be its environment.
        for line in output.splitlines():
            print("  " + " ".join(line.split()[:2]))
        if not output:
            print("  (no output)")
        return 2
    print(f"pgrep -lf '{RAY_PATTERN}': no process")

    failures = 0
    try:
        before = time.perf_counter()
        ray.init(**INIT_ARGUMENTS)
        print(f"ray.init({INIT_ARGUMENTS}): {time.perf_counter() - before:.1f} s")
        try:
            node = ray._private.worker._global_node
            print(f"session directory: {node.get_session_dir_path()}")
        except Exception as error:  # informational only
            print(f"session directory: not read ({type(error).__name__}: {error})")

        for number, name, step in STEPS:
            print(f"step {number}, {name}:")
            before = time.perf_counter()
            try:
                seen = step()
            except Exception as error:
                failures += 1
                # The deepest frame that is not ``check``'s own.
                frames = traceback.extract_tb(error.__traceback__)
                where = [frame for frame in frames if frame.name != "check"][-1]
                print(
                    f"  FAIL ({time.perf_counter() - before:.1f} s): "
                    f"{type(error).__module__}.{type(error).__name__}: {error} "
                    f"[{os.path.basename(where.filename)}:{where.lineno}]"
                )
            else:
                print(f"  PASS ({time.perf_counter() - before:.1f} s): {seen}")
    finally:
        ray.shutdown()
        print(f"ray.shutdown(): ray.is_initialized() is {ray.is_initialized()}")

    waited = 0.0
    returncode, output = ray_processes()
    while returncode == 0 and waited < 10:
        time.sleep(0.5)
        waited += 0.5
        returncode, output = ray_processes()
    left = len(output.splitlines()) if returncode == 0 else 0
    print(f"Ray processes left after shutdown: {left} (after {waited:.1f} s)")

    print(
        f"Summary: {len(STEPS) - failures} of {len(STEPS)} steps passed; "
        f"{time.perf_counter() - started:.1f} s in all"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
