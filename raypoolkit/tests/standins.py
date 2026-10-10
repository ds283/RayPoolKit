"""
In-process stand-ins that let the suite drive ``RayWorkPool`` with no Ray cluster (decision U6).

The pool module reaches Ray through two calls, ``ray.wait`` and ``ray.get``, and through
``ObjectRef`` for one ``isinstance`` test. Work items here are **real** ``ray.ObjectRef``
instances, built from 28 bytes (which needs no cluster), and the module's name ``ray`` is replaced,
for each test, by a namespace that has ``wait`` and ``get`` and nothing else, so that any other use
of ``ray`` in the module fails loudly with ``AttributeError``.

The entry points, which later prompts build on:

- ``StandinRay``: a table from ref to value. ``ref(value)`` mints a ref; ``wait`` applies Ray's
  contract (read from ``ray/_private/worker.py`` at 2.43.0, and the same at 2.53.0 and 2.55.1) and
  then returns the refs in the order ``order`` gives; ``get`` returns a copy of the value, as Ray
  does. ``namespace()`` is what replaces the module's ``ray``.
- ``ScriptedClock``: stands in for the module's ``time`` (``time_namespace()``) and ``datetime``
  (``datetime_namespace()``).
- ``Work``, ``Blob`` and ``StandinDatastorePool``: work objects and a datastore pool, at module
  level so that they pickle. They reach the active ``StandinRay`` through ``active_ray()``, which
  ``PoolTestCase`` sets, never by holding it.
- ``PoolTestCase``: installs all of the above by string target, refuses ``ray.init``, and runs a
  pool with stdout captured.

**Patching.** ``raypoolkit.RayWorkPool``, the package attribute, is the class, not the module
(decision U4; see ``test_package_imports``' third test). Every patch here names its target as a
string, ``"raypoolkit.RayWorkPool.ray"`` and so on, which reaches the module.

**Ray's auto-init.** Ray's ``wait`` and ``get`` call ``ray.init()`` through the module attribute
unless ``RAY_ENABLE_AUTO_CONNECT=0`` was set before ``ray`` was imported, which the suite cannot
arrange: importing any test module imports ``raypoolkit``, which imports ``ray``. So every
``PoolTestCase`` patches ``"ray.init"`` with a function that raises ``RayInitCalled``, and its
tear-down asserts that ``ray.is_initialized()`` is false. A test that reaches real Ray fails at
once, and no cluster starts.
"""

import contextlib
import io
import pickle
import types
import unittest
from datetime import datetime, timedelta
from typing import NamedTuple
from unittest import mock

import ray
from ray import ObjectRef

from raypoolkit.RayWorkPool import RayWorkPool

# the string targets every PoolTestCase patches (decision U4: never the package attribute)
POOL_MODULE = "raypoolkit.RayWorkPool"
RAY_TARGET = POOL_MODULE + ".ray"
TIME_TARGET = POOL_MODULE + ".time"
DATETIME_TARGET = POOL_MODULE + ".datetime"
RAY_INIT_TARGET = "ray.init"

# the most calls StandinRay.wait accepts before it decides the pool is not making progress. The
# largest test in the suite needs well under a tenth of this (the log of prompt 02 records it)
DEFAULT_MAX_WAIT_CALLS = 1000

# the naive base the ScriptedClock's datetime adds its reading to
DEFAULT_CLOCK_BASE = datetime(2026, 10, 10, 12, 0, 0)

REF_LENGTH = 28


class RayInitCalled(RuntimeError):
    """Raised by the patched ``ray.init``: a test reached real Ray."""


def refuse_ray_init(*args, **kwargs):
    raise RayInitCalled(
        "ray.init was called: a test reached real Ray (the suite must need no cluster)"
    )


# --- the active stand-in --------------------------------------------------------------------------

_active_ray = None


def set_active_ray(standin):
    """Make ``standin`` the ``StandinRay`` that work objects and the datastore pool mint refs from."""
    global _active_ray
    _active_ray = standin


def active_ray() -> "StandinRay":
    if _active_ray is None:
        raise RuntimeError("no StandinRay is active (is the test a PoolTestCase?)")
    return _active_ray


# --- Ray ------------------------------------------------------------------------------------------


class StandinRay:
    """
    ``ray.wait`` and ``ray.get`` over real ``ObjectRef``s, resolved from a table.

    Every ref is ready at once; the order in which ``wait`` returns them is the only thing a test
    controls, through ``order``.
    """

    def __init__(self, *, max_wait_calls: int = DEFAULT_MAX_WAIT_CALLS):
        self._next = 1
        self._table = {}
        # a callable from the list wait was given to the same refs in the order to return them
        self.order = lambda refs: refs
        # when true, wait returns equal but distinct refs, built from the same bytes
        self.fresh_refs = False
        self.max_wait_calls = max_wait_calls
        # (len(refs), num_returns) for every call of wait, in order
        self.wait_calls = []
        # every ref passed to get, in order
        self.get_calls = []
        # a shared event log: wait appends ("wait", len(refs), num_returns); work objects, the
        # datastore pool and tests append their own events, so that the order can be read
        self.log = []

    # minting

    def ref(self, value) -> ObjectRef:
        """A fresh 28-byte ``ObjectRef`` whose value is ``value``."""
        binary = self._next.to_bytes(REF_LENGTH, "big")
        self._next += 1
        ref = ObjectRef(binary)
        self._table[binary] = value
        return ref

    def value_of(self, ref: ObjectRef):
        """The value recorded for ``ref`` itself, not a copy (for tests of the stand-in)."""
        return self._table[ref.binary()]

    # ray.wait

    def wait(self, refs, *, num_returns=1, timeout=None, fetch_local=True):
        n = len(refs) if isinstance(refs, list) else None
        self.wait_calls.append((n, num_returns))
        self.log.append(("wait", n, num_returns))
        if len(self.wait_calls) > self.max_wait_calls:
            raise RuntimeError(
                f"StandinRay.wait has been called {len(self.wait_calls)} times, past its cap of "
                f"{self.max_wait_calls}: the pool is not making progress"
            )

        # Ray's checks, in Ray's order and with Ray's exception types
        if isinstance(refs, ObjectRef):
            raise TypeError(
                "wait() expected a list of ray.ObjectRef, got a single ray.ObjectRef"
            )
        if not isinstance(refs, list):
            raise TypeError(
                f"wait() expected a list of ray.ObjectRef, got {type(refs)}"
            )
        if timeout is not None and timeout < 0:
            raise ValueError(
                f"The 'timeout' argument must be nonnegative. Received {timeout}"
            )
        for ref in refs:
            if not isinstance(ref, ObjectRef):
                raise TypeError(
                    f"wait() expected a list of ray.ObjectRef, got list containing {type(ref)}"
                )
        if len(refs) == 0:
            return [], []
        if len(refs) != len(set(refs)):
            raise ValueError("Wait requires a list of unique ray_waitables.")
        if num_returns <= 0:
            raise ValueError("Invalid number of objects to return %d." % num_returns)
        if num_returns > len(refs):
            raise ValueError(
                "num_returns cannot be greater than the number of ray_waitables provided to "
                "ray.wait."
            )

        ordered = list(self.order(list(refs)))
        if sorted(r.binary() for r in ordered) != sorted(r.binary() for r in refs):
            raise AssertionError(
                "StandinRay.order must return the refs it was given, reordered"
            )
        if self.fresh_refs:
            ordered = [ObjectRef(r.binary()) for r in ordered]
        return ordered[:num_returns], ordered[num_returns:]

    # ray.get

    def get(self, ref, *, timeout=None):
        if isinstance(ref, (list, tuple)):
            raise TypeError(
                "StandinRay.get takes a single ObjectRef: the pool never passes a list"
            )
        if not isinstance(ref, ObjectRef):
            raise TypeError(f"StandinRay.get expected an ObjectRef, got {type(ref)}")
        self.get_calls.append(ref)
        binary = ref.binary()
        if binary not in self._table:
            raise KeyError(
                f"StandinRay.get: ref {ref.hex()} was not minted by this stand-in"
            )
        # by value, as Ray returns a deserialized copy
        return pickle.loads(pickle.dumps(self._table[binary]))

    def namespace(self):
        """What replaces the pool module's ``ray``: ``wait`` and ``get``, and nothing else."""
        return types.SimpleNamespace(wait=self.wait, get=self.get)


# --- the clock ------------------------------------------------------------------------------------


class ScriptedClock:
    """
    The pool module's ``time`` and ``datetime``.

    ``perf_counter()`` advances the reading by ``step`` and returns the new reading, so the reading
    after a call is what that call returned. The reading starts at 0. ``step`` is a whole number of
    seconds (``format_time`` prints ``{interval:.3g}s``, so whole readings print exactly).
    ``advance(seconds)`` jumps without a call.

    ``now()`` returns the naive ``datetime`` ``base`` plus the current reading, and does **not**
    advance the clock: the stamp on a progress line is the reading the ``perf_counter()`` call
    before it returned.
    """

    def __init__(self, *, step: int = 1, base: datetime = DEFAULT_CLOCK_BASE):
        self.step = step
        self.base = base
        self.reading = 0
        self.perf_counter_calls = 0

    def perf_counter(self):
        self.perf_counter_calls += 1
        self.reading += self.step
        return self.reading

    def advance(self, seconds):
        self.reading += seconds

    def now(self):
        return self.base + timedelta(seconds=self.reading)

    def stamp(self, reading) -> str:
        """The stamp a progress line prints when ``now()`` is called at ``reading``."""
        return f"{self.base + timedelta(seconds=reading):%Y-%m-%d %H:%M:%S}"

    def time_namespace(self):
        return types.SimpleNamespace(perf_counter=self.perf_counter)

    def datetime_namespace(self):
        return types.SimpleNamespace(now=self.now)


# --- work objects and the datastore pool ----------------------------------------------------------


class Work:
    """
    A work object: it has ``available``, ``compute(**kwargs)``, ``store()`` and ``store_id``.

    ``compute`` and ``store`` record themselves on the object and in the active stand-in's log.
    Objects are copied whenever they pass through ``get``, so a test reads what happened to the
    copies through the log, or through what the pool hands back.
    """

    def __init__(self, name, available: bool = False):
        self.name = name
        self.available = available
        self.store_id = None
        self.compute_kwargs = None
        self.stored = False

    def compute(self, **kwargs) -> ObjectRef:
        self.compute_kwargs = dict(kwargs)
        active_ray().log.append(("compute", self.name, dict(kwargs)))
        return active_ray().ref(("computed", self.name))

    def store(self):
        self.stored = True
        active_ray().log.append(("store", self.name))

    def __repr__(self):
        return (
            f"Work({self.name!r}, available={self.available!r}, "
            f"store_id={self.store_id!r})"
        )


class Blob:
    """A "blob": a lookup result with no ``available`` attribute."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Blob({self.name!r})"


class StandinDatastorePool:
    """
    The datastore pool. ``object_store(obj)`` records the call and returns a ref whose value is a
    copy of ``obj`` with ``store_id`` set and ``available`` true, or, with
    ``available_after_store=False``, false.
    """

    def __init__(self, *, available_after_store: bool = True, first_store_id=1001):
        self.available_after_store = available_after_store
        self._next_store_id = first_store_id
        # every object handed to object_store, as handed (not a copy)
        self.calls = []

    def object_store(self, obj) -> ObjectRef:
        self.calls.append(obj)
        persisted = pickle.loads(pickle.dumps(obj))
        persisted.store_id = self._next_store_id
        self._next_store_id += 1
        persisted.available = self.available_after_store
        active_ray().log.append(("object_store", getattr(obj, "name", None)))
        return active_ray().ref(persisted)


# --- the test case --------------------------------------------------------------------------------


class PoolRun(NamedTuple):
    pool: RayWorkPool
    lines: list


class PoolTestCase(unittest.TestCase):
    """
    The base of every test that runs a pool. It has no ``test_`` method of its own, so that
    importing it into a module adds nothing to that module's count.

    ``setUp`` makes a ``StandinRay`` (``self.ray``), a ``ScriptedClock`` (``self.clock``) and a
    ``StandinDatastorePool`` (``self.datastore``), and patches, by string target only:
    ``"raypoolkit.RayWorkPool.ray"``, ``"raypoolkit.RayWorkPool.time"``,
    ``"raypoolkit.RayWorkPool.datetime"`` and ``"ray.init"``. ``tearDown`` asserts that Ray was not
    initialised.
    """

    def setUp(self):
        super().setUp()
        self.ray = StandinRay()
        self.clock = ScriptedClock()
        self.datastore = StandinDatastorePool()
        self.lines = []
        set_active_ray(self.ray)
        self.addCleanup(set_active_ray, None)
        for target, replacement in (
            (RAY_TARGET, self.ray.namespace()),
            (TIME_TARGET, self.clock.time_namespace()),
            (DATETIME_TARGET, self.clock.datetime_namespace()),
            (RAY_INIT_TARGET, refuse_ray_init),
        ):
            patcher = mock.patch(target, replacement)
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self):
        self.assertFalse(
            ray.is_initialized(), "Ray was initialised: a test reached real Ray"
        )
        super().tearDown()

    def make_pool(self, task_list, task_builder, **kwargs) -> PoolRun:
        """Construct a pool with stdout captured. ``pool`` defaults to ``self.datastore``."""
        kwargs.setdefault("pool", self.datastore)
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                pool = RayWorkPool(
                    task_list=task_list, task_builder=task_builder, **kwargs
                )
        finally:
            self.lines = out.getvalue().splitlines()
        return PoolRun(pool, list(self.lines))

    def run_existing(self, pool) -> list:
        """Run a constructed pool with stdout captured, and return the lines it printed."""
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                pool.run()
        finally:
            self.lines = out.getvalue().splitlines()
        return list(self.lines)

    def run_pool(self, task_list, task_builder, **kwargs) -> PoolRun:
        """
        Construct and run a pool with stdout captured, and return it with every line it printed,
        construction's included. If either step raises, the lines printed so far are in
        ``self.lines``.
        """
        pool, construction_lines = self.make_pool(task_list, task_builder, **kwargs)
        try:
            run_lines = self.run_existing(pool)
        finally:
            self.lines = construction_lines + self.lines
        return PoolRun(pool, construction_lines + run_lines)

    # builders and handlers the tests share

    def work_builder(self, available: bool = False, make=None):
        """A task builder that mints one ref per item, its value ``Work(item, available)``."""
        if make is None:
            make = lambda item: Work(item, available=available)
        return lambda item: self.ray.ref(make(item))

    def recording_handler(self, name, returns=None):
        """A handler that appends ``(name, obj)`` to ``self.ray.log`` and returns ``returns(obj)``."""

        def handler(obj, *args, **kwargs):
            self.ray.log.append((name, obj))
            return returns(obj) if returns is not None else None

        return handler

    def ref_returning_handler(self, name, value=True):
        """An availability or validation handler: logs ``(name, obj)``, returns a ref to ``value``."""
        return self.recording_handler(name, returns=lambda obj: self.ray.ref(value))

    def logged(self, name):
        """The objects logged under ``name``, in order."""
        return [entry[1] for entry in self.ray.log if entry[0] == name]
