# RayPoolKit

A driver-side work queue for [Ray](https://www.ray.io/). `RayWorkPool` takes a list of work
items, builds a lookup task for each, and carries every object it gets back through a fixed
cycle: if the object is already available it is finished (optionally after an availability
task), and if not it is computed, stored locally, persisted, and optionally validated, with a
post-processing hook at each exit. It caps the number of tasks in flight, so a long queue never
floods Ray's object store, and reports progress and rates as it drains.

## Status

**`v0.2.0`** is the release the client projects adopt. It is `v0.1.0` with the faults inherited
from SecondaryGWKit's copy fixed, and the constructor's arguments checked. Each fault's fix is
guarded by a test that `v0.1.0`'s module fails, in a test suite that needs no Ray cluster. What
changed for a caller is listed under [Changes in `v0.2.0`](#changes-in-v020), below; the issues,
with where each sat and how it was fixed, are in §4 (Resolved issues) of the campaign's status
board, [`prompts/extraction/IMPLEMENTATION_STATE.md`](prompts/extraction/IMPLEMENTATION_STATE.md).
The plan for the package, and for its client projects to depend on one copy of the pool, is
[`prompts/extraction/README.md`](prompts/extraction/README.md).

**`v0.1.0`** is the `RayTools/RayWorkPool.py` of
[SecondaryGWKit](https://github.com/ds283/SecondaryGWKit) at its commit `b510bc9`, moved here with
its behaviour unchanged ([`PROVENANCE.md`](PROVENANCE.md)).

RayPoolKit does not depend on [DatastoreKit](https://github.com/ds283/DatastoreKit), the
datastore layer extracted from the same projects. A `RayWorkPool` is handed any pool object its
handlers understand; the default persist handler calls only its `object_store` method.

## Changes in `v0.2.0`

For a client moving its pin from `v0.1.0`:

- **The constructor checks its arguments, and raises `ValueError` for any it refuses**, naming the
  argument: with no compute handler, a store handler, persist handler, validation handler or label
  builder given explicitly; with one, `store_handler=None` or `persist_handler=None`; and a size
  below 1 (see [Which handlers a pool needs](#which-handlers-a-pool-needs)). Two of these were
  refused by `v0.1.0` with other types: an explicit persist handler with no compute handler raised
  `RuntimeWarning` (as an exception), and a compute handler with `persist_handler=None` raised
  `RuntimeError`.
- **A pool with no compute handler needs only `compute_handler=None`.** The default store and
  persist handlers apply only with a compute handler, so `persist_handler=None` is no longer
  needed. `store_handler=None` and `persist_handler=None` are still accepted, and the pool prints
  the same lines either way.
- **Newly refused at construction:** a store handler, validation handler or label builder given
  with no compute handler (`v0.1.0` accepted it and never called it); a compute handler with
  `store_handler=None` (`v0.1.0` constructed, and `run()` raised `TypeError` at the first completed
  compute); and a `create_batch_size`, `process_batch_size` or `max_task_queue` below 1 (`v0.1.0`
  constructed, and `run()` then never returned, or raised from `ray.wait`).
- **The post handler after a persist is given the persisted object**, when there is no validation
  handler: the object in `results`, with its `store_id`. `v0.1.0` gave it the local copy from
  before the persist.
- **`store_results=True` accepts any iterable `task_list`**, a generator included; `v0.1.0` raised
  `TypeError` for one without `len()`.
- **In-flight work is keyed on each ref's value**, so the pool no longer depends on `ray.wait`
  returning the very objects it was given.
- **The printed lines are unchanged**, in wording and layout.

## Supported versions

| | Declared (`pyproject.toml`) | Tested: low end | Tested: high end |
|---|---|---|---|
| Python | `>=3.12` | 3.12.15 | 3.13.16 |
| Ray | `>=2.43` | 2.43.0 | 2.55.1 |

- The suite runs at both tested ends, in CI on Ubuntu 24.04
  ([`.github/workflows/tests.yml`](.github/workflows/tests.yml)), and on macOS where it is
  developed.
- On Python 3.13 the Ray floor is in effect **2.45.0**, the first Ray release with wheels for
  3.13 (2.43.0, 2.44.0 and 2.44.1 have none).
- Ray has no ceiling, so that a client can move Ray without a release here. Newer releases inside
  the declared range (Python 3.14, and Ray up to 2.59.0 today) are allowed but not tested.
- **A client pins its own Ray**, in its own `requirements.txt`.

## Installing

A client depends on a tagged release, pinned in its `requirements.txt`:

```text
raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
```

An editable install (`pip install -e`) is for developing this package, never for a client's
production runs: a production run must be reproducible from its pin.

## Using it

```python
from raypoolkit import RayWorkPool
```

A pool is built with `RayWorkPool(pool, task_list, task_builder, ...)`, the rest by keyword, and
drained with `run()`.

### The constructor

**The datastore pool.** `pool` is typed as `raypoolkit.DatastorePool`, a `typing.Protocol` with
one method, `object_store(obj)`, which returns the `ObjectRef` of a datastore write. `RayWorkPool`
keeps the pool and passes it through, as the second argument, to the store handler and the persist
handler; only the default persist handler calls anything on it. The protocol is a type hint and
is not checked at run time, so a pool whose handlers need nothing of it may be given any object.

**The work.**
- `task_list`: the work items, in order, as any iterable. It is consumed into a list at
  construction.
- `task_builder(item)`: called once for each item, and returns one of:
  1. an `ObjectRef`, the item's lookup task;
  2. a dict `{"ref": <ObjectRef>, "compute_payload": <anything>}`, where `"compute_payload"` is
     optional and, when present, is passed to the compute handler as `payload=`;
  3. a list, tuple or set of either of those, several lookups for one item (not allowed with
     `store_results=True`);
  4. `None`, nothing to enqueue for this item (not allowed with `store_results=True`).

  Anything else raises `RuntimeError`. When a lookup task completes, its value is fetched with
  `ray.get`; that value is "the object" below.

**The handlers.** Each is a keyword argument.

| Argument | Default | Given | Returns |
|---|---|---|---|
| `compute_handler` | calls `obj.compute(**kwargs)` | the object, with `label=` and `payload=` as keywords when there are any | the `ObjectRef` of the compute task |
| `store_handler` | calls `obj.store()` | `(obj, pool)`, on the driver, when the compute task has completed | nothing (its return is ignored) |
| `persist_handler` | calls `pool.object_store(obj)` | `(obj, pool)`, straight after the store handler | an `ObjectRef` whose value is the persisted object, which replaces the local copy |
| `available_handler` | `None` | the object, when its `available` is true | an `ObjectRef`; the pool waits for it but does not read its value |
| `validation_handler` | `None` | the persisted object | an `ObjectRef` whose value is `True`; any other value prints a `!! WARNING` line, and the pool carries on |
| `post_handler` | `None` | the object, at each point where it is finished | `None`, or a replacement, which with `store_results=True` replaces the item's entry in `results` |

`label_builder` (default `None`) is called with the object before its compute task is built; a
label that is not `None` is passed to the compute handler as `label=`.

**The sizes**, with their defaults; each must be at least 1:
- `create_batch_size=5`: how many work items have their tasks built in one pass, when there is
  room;
- `process_batch_size=1`: how many completed tasks one pass asks `ray.wait` for and handles;
- `max_task_queue=200`: new work items are taken only while fewer than this many tasks are in
  flight.

**The notifications**, printed only when the pool has a `title`, with their defaults:
- `notify_min_time_interval=60`: no progress lines until more than this many seconds have passed
  since the last;
- `notify_time_interval=300`: after that, progress lines when more than this many seconds have
  passed since the last;
- `notify_batch_size=500`: or when more than this many completed tasks have been handled since the
  last.

**The rest:**
- `title=None`: when given, the pool prints a banner at construction, progress lines as it runs and
  completion lines at the end, and sets `total_time`. Without one it prints nothing but the
  validation warning.
- `store_results=False`: when true, the pool keeps `results`, one entry per work item, in the order
  of `task_list`.

### The objects a lookup returns

- An object with an **`available` attribute** takes part in the cycle:
  - if `available` is true, it takes the **available path**: with an availability handler the pool
    runs the task that handler returns and then finishes the object; without one, the object is
    finished at once;
  - if it is false, and the pool has a compute handler, it takes the **compute path**: compute,
    store, persist, then validation if there is a validation handler, then finished. If the pool
    has no compute handler, nothing more is done with it, and the post handler is not called.
- An object **without an `available` attribute** (the result of a vectorised lookup, say) is
  finished as it is.
- An object on the compute path has `compute(**kwargs)`, returning an `ObjectRef`, and `store()`:
  the default compute and store handlers call them.
- The persisted object, the value of the persist handler's `ObjectRef`, must have `available` true,
  or the pool raises `RuntimeError`; and it has `store_id`, which the validation warning prints.

"Finished" means the post handler, if there is one, is called with the object.

### Running it

`run()` drains the queue and returns when every task has completed. Afterwards:
- `results` (with `store_results=True`) holds, for each work item, the object it ended with: the
  lookup's object, replaced by the persisted object on the compute path, and by the post handler's
  replacement if it returned one;
- `total_time` (with a `title`) is the run's duration in seconds.

### Which handlers a pool needs

The constructor checks the handlers against whether the pool has a compute handler, and checks the
sizes. It raises `ValueError` for any argument it refuses, naming the argument.

- **With a compute handler** (the default, or the caller's own), the store and persist handlers
  default to the ones in the table above. Either may be replaced, but neither may be `None`:
  `store_handler=None` or `persist_handler=None` raises `ValueError`, whose message says to leave
  the argument out to use the default.
- **Without one** (`compute_handler=None`), the pool has no compute path, and neither default
  applies. The four arguments used only on that path, `store_handler`, `persist_handler`,
  `validation_handler` and `label_builder`, must be left out or `None`; anything else raises
  `ValueError`, whose message says the argument would never be called. So a lookup-only pool
  passes `compute_handler=None` and needs nothing more; `store_handler=None` and
  `persist_handler=None` are accepted and change nothing. `available_handler` and `post_handler`
  are used on the lookup path, and may be given either way.
- **The sizes:** a `create_batch_size`, `process_batch_size` or `max_task_queue` below 1 raises
  `ValueError`, whose message gives the value.

### The printed lines are part of the interface

A client may parse what the pool prints. The banner, progress and completion lines look like this,
copied from a run the suite pins (`raypoolkit/tests/test_printed_lines.py`); the stamps, counts,
times and rates in them are illustrative.

The banner, printed at construction after an empty line:

```text
** Stage one
```

A progress pair:

```text
   -- 2026-10-10 12:00:02 (1s running): 0/2 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
      inflight: 1 lookup | completed: 1 lookup (avg 60/min)
```

The completion lines (the third only when no compute task completed):

```text
   -- ALL WORK ITEMS COMPLETE in time 5s
      Queue summary: 2 lookup (avg 24/min)
      (no compute items were evaluated - all assets read from datastore)
```

A change to their wording or layout is a change to the package's interface, and is released as a
new minor version.

### A worked example

[`raypoolkit/tests/standins.py`](raypoolkit/tests/standins.py), in this repository, is the worked
example of the objects and handlers a pool drives: `Work` (an object with `available`, `compute()`
and `store()`), `Blob` (an object without `available`) and `StandinDatastorePool` (an
`object_store` that returns the persisted object with its `store_id`). It is part of the test
suite and is not installed with the package.

## Developing

From the repository root, with Python 3.12 or later:

```bash
python3 -m venv venv
./venv/bin/pip install -e . "ray==2.43.0" "black==25.1.0"
./venv/bin/python -m unittest discover -s raypoolkit/tests -t .
```

The suite needs no Ray cluster. Its work items are real `ray.ObjectRef`s built from bytes, and the
pool's `ray.wait` and `ray.get` are replaced in-process by the stand-ins in
`raypoolkit/tests/standins.py`, whose test base refuses `ray.init`. The import guard runs the
package in a child interpreter, so the package must be installed (editable) in the venv that runs
the suite. CI runs the suite at both tested ends, and `black --check raypoolkit docs`.

The equivalence check, [`docs/extraction/compare_with_source.py`](docs/extraction/compare_with_source.py),
compares the package with its source in SecondaryGWKit's repository, which it reads through `git`
at a local path. It was retired at `v0.1.0`: it describes that tag, and fails by design on a later
tree. It runs locally only, not in CI, from a `git worktree` of `v0.1.0`;
[`PROVENANCE.md`](PROVENANCE.md) gives the commands.

## Licence

Apache License 2.0; see [`LICENSE`](LICENSE). The four package modules carry the Apache 2.0
header.
