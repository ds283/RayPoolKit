# Log — extraction prompt 02: the test suite

**Subject:** Pin RayWorkPool's behaviour with an in-process Ray stand-in · **Commit:** this commit ·
**Date:** 2026-10-10 · **Agent:** Claude Opus 5.5

**Result: landed.** Eight new files under `raypoolkit/tests/`: the stand-ins (`standins.py`) and
seven test modules. The suite goes from **3 to 116** tests, all passing, with no Ray process before
or after and `ray.init` never reached in a passing run. Every reachable row of §2.4's inventory,
and each row this log adds, has a named test, and **every one of the 89 mutations of
`raypoolkit/RayWorkPool.py` fails the suite and fails the test named for its row**; none hangs.
(m1) fails the fault-1 test and nothing else. (s1) and (s2) each fail tests, so no issue is opened
and the index stays at **6**. `raypoolkit/RayWorkPool.py` is byte for byte `49f3ddf`'s;
`compare_with_source.py` exits 0 with 01's counts and 12 declared files; `black --check
raypoolkit docs` is clean.

**Gate, re-checked at start.** `HEAD` was `319099a`, the tree clean. `Ran 3 tests … OK`. The check
exited 0 (572 identical, 2 D-imp, 1 D-pool, 4 D-int, 4 declared, 0 undeclared). SGK `HEAD` is
`b510bc90b66985532d28996ab4e5b13b0ff71709`, `RayTools/RayWorkPool.py` blob
`b4666fa89abb26829fd585b881947d7ef5172cea`. `pgrep -lf 'gcs_server|raylet|ray::'` was empty. The
venv: Python 3.12.15, `ray` 2.43.0, `black` 25.1.0. No SGK code was run; SGK was read only through
`git rev-parse` for this gate and `compare_with_source.py`'s `git show`.

## 1. What shipped

| File | Lines | What |
|---|---|---|
| `raypoolkit/tests/standins.py` | 425 | `StandinRay`, `ScriptedClock`, `Work`, `Blob`, `StandinDatastorePool`, `PoolTestCase` (§1.1) |
| `raypoolkit/tests/test_standins.py` | 247 | 30 tests: Ray's `wait` contract clause by clause, the spin cap, `get` by value, `fresh_refs`, the clock, the work objects and datastore, the `ray.init` guard |
| `raypoolkit/tests/test_construction.py` | 110 | 12 tests: C1–C4, the three default handlers (D1–D3), `results` and `total_time` only when asked for, the messages ("maker", fault 5) |
| `raypoolkit/tests/test_task_builder.py` | 292 | 20 tests: R1–R9 |
| `raypoolkit/tests/test_run_paths.py` | 420 | 22 tests: L1–L6, A1, K1, S1–S4, V1–V2, P1, P0 and X1 |
| `raypoolkit/tests/test_scheduling.py` | 134 | 7 tests: the three sizes, read from `wait_calls` and the builder's calls; `results` order under reversed completion |
| `raypoolkit/tests/test_printed_lines.py` | 473 | 17 tests: U9, every line word for word against the scripted clock; N1–N5, F1–F2, Q1–Q2, T1–T2; `format_time`'s edges; the three consumer patterns |
| `raypoolkit/tests/test_inherited_faults.py` | 135 | 5 tests, `TestInheritedFaults`, under §2.6's names |
| `docs/extraction/compare_with_source.py` | +8 | eight `NO_SOURCE` entries, each naming "02 §2.x"; no other change |
| this log, the board, `prompts/INDEX.md` | | the records |

`docs/OPEN_ISSUES.md` is unchanged: nothing is opened, closed or narrowed (§6).

### 1.1 The stand-ins' entry points (for 03 and 04)

All in `raypoolkit/tests/standins.py`. The prompt's names are kept; the additions are marked *(+)*.

**`StandinRay(*, max_wait_calls: int = DEFAULT_MAX_WAIT_CALLS)`**, `DEFAULT_MAX_WAIT_CALLS = 1000`.
- `ref(value) -> ObjectRef`: a fresh ref from a counter (starting at 1), `counter.to_bytes(28,
  "big")`; records `value` keyed on the ref's bytes.
- `wait(refs, *, num_returns=1, timeout=None, fetch_local=True) -> (ready, remaining)`. First it
  records `(len(refs), num_returns)` in `wait_calls` and `("wait", len, num_returns)` in `log`, and
  raises `RuntimeError("StandinRay.wait has been called N times, past its cap of C: …")` once the
  calls exceed `max_wait_calls` (the spin cap, clarification 1). Then Ray's checks, in Ray 2.43.0's
  order (`ray/_private/worker.py:2950-2997`) and with its types: a single `ObjectRef` →
  `TypeError`; not a `list` → `TypeError`; `timeout < 0` → `ValueError`; an element not an
  `ObjectRef` → `TypeError`; **an empty list → `([], [])`, before `num_returns` is checked**;
  duplicates (`len(refs) != len(set(refs))`) → `ValueError`; `num_returns <= 0` → `ValueError`;
  `num_returns > len(refs)` → `ValueError`. Then `order(list(refs))` (checked to be a
  permutation), the first `num_returns` as `ready`. Every ref is ready at once.
- `order`: settable callable, default the identity. `fresh_refs`: when true, `wait` returns
  `ObjectRef(r.binary())` for each, equal but distinct.
- `get(ref, *, timeout=None)`: `pickle.loads(pickle.dumps(value))`. A `list` or `tuple` →
  `TypeError`; a non-ref → `TypeError`; a ref it did not mint → `KeyError` naming `ref.hex()`. A
  ref built from a minted ref's bytes resolves. Each ref is appended to `get_calls` *(+)*.
- `namespace()` *(+)*: `types.SimpleNamespace(wait=…, get=…)`, which replaces the module's `ray`.
- `value_of(ref)` *(+)*: the recorded value itself (for the stand-in's own tests).
- `wait_calls`, `get_calls` *(+)*, `log` *(+)*: a shared event list, appended to by `wait`, the
  work objects, the datastore and the tests' handlers, so that interleavings can be read.

**`ScriptedClock(*, step: int = 1, base: datetime = datetime(2026, 10, 10, 12, 0, 0))`**.
- `perf_counter()`: `reading += step`, returns the new `reading`; the reading starts at 0.
  `perf_counter_calls` *(+)* counts calls.
- `advance(seconds)`: `reading += seconds`, no call counted.
- `now()`: the naive `base + timedelta(seconds=reading)`; it **reads** and does not advance.
- `time_namespace()` *(+)* → `SimpleNamespace(perf_counter=…)`; `datetime_namespace()` *(+)* →
  `SimpleNamespace(now=…)`. The prompt's "companion that stands in for the module's `datetime`" is
  this namespace, not a separate class. `stamp(reading)` *(+)* formats a stamp.

**Work objects and the datastore** (module level, so they pickle):
- `Work(name, available=False)`: attributes `name`, `available`, `store_id=None`,
  `compute_kwargs=None`, `stored=False`. `compute(**kwargs)` records the arguments on the object
  and as `("compute", name, kwargs)` in the active stand-in's `log`, and returns
  `active_ray().ref(("computed", name))`. `store()` sets `stored` and logs `("store", name)`.
- `Blob(name)` *(+)*: no `available` attribute.
- `StandinDatastorePool(*, available_after_store=True, first_store_id=1001)`:
  `object_store(obj)` appends `obj` to `calls`, logs `("object_store", name)`, and returns
  `active_ray().ref(copy)`, where `copy` is a pickled copy of `obj` with `store_id` set (1001,
  1002, …) and `available = available_after_store`.
- `active_ray()`, `set_active_ray(standin)` *(+)*: the module-level accessor. Objects never hold
  the stand-in.

**`PoolTestCase(unittest.TestCase)`**, with no `test_` method (clarification 7).
- `setUp`: `self.ray`, `self.clock`, `self.datastore`; `set_active_ray(self.ray)`; patches, by
  string target only, `"raypoolkit.RayWorkPool.ray"` → `self.ray.namespace()`,
  `"raypoolkit.RayWorkPool.time"` → `self.clock.time_namespace()`,
  `"raypoolkit.RayWorkPool.datetime"` → `self.clock.datetime_namespace()`, and `"ray.init"` →
  `refuse_ray_init`, which raises `RayInitCalled(RuntimeError)`.
- `tearDown`: `assertFalse(ray.is_initialized())`.
- `make_pool(task_list, task_builder, **kwargs) -> PoolRun(pool, lines)`: constructs with stdout
  captured (the banner is printed at construction); `pool=` defaults to `self.datastore`.
  `run_existing(pool) -> lines` runs a built pool. `run_pool(task_list, task_builder, **kwargs) ->
  PoolRun(pool, lines)` does both; the lines are construction's then the run's, by
  `str.splitlines()`. If either raises, the lines printed so far are in `self.lines`.
- Helpers *(+)*: `work_builder(available=False, make=None)`, `recording_handler(name,
  returns=None)`, `ref_returning_handler(name, value=True)`, `logged(name)`.

### 1.2 The white-box seams used (§2.2)

| Test | Seam |
|---|---|
| `test_printed_lines.TestPureFunctions.test_readable_rate_units` | `_readable_rate`, called directly |
| `test_printed_lines.TestPureFunctions.test_format_rates` | `_format_rates`, called directly (including both times `None` → `''`) |
| `test_printed_lines.TestStatusMessages` (3 tests) | `_build_queued_status_message()` and `_build_completed_status_message(…)`, called directly on constructed pools |
| `test_run_paths.TestUnexpectedItemType.test_an_unexpected_item_type_raises` | `_inflight` and `_data` seeded before `run()` |

`test_printed_lines.TestPureFunctions.test_format_time_at_its_edges` calls `raypoolkit._timing.format_time`,
a module function, not part of `RayWorkPool.py`. No other test reads or writes anything private.

## 2. Deviations from the prompt

The orchestrator's brief added seven clarifications (1–7 below). Each is an **IMPLEMENTATION
CHOICE at the orchestrator's direction**.

1. **A spin cap in `StandinRay.wait`, and a timeout on every mutation run** (clarification 1).
   The cap is **1,000 calls** per `StandinRay`; the most any test makes is **16**
   (`test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`,
   four subtests of four `wait`s each), measured by wrapping `PoolTestCase.tearDown` from a scratch
   runner. `test_standins.TestWaitContract.test_wait_raises_past_its_call_cap` tests it. Each
   mutation run is the whole suite under `subprocess.run(…, timeout=300)`. **No mutation timed
   out.** X1's mutation is the one that would otherwise spin: with the `raise` gone, the seeded
   item is never popped, and the cap ends the run with its own `RuntimeError`, whose message the
   X1 test rejects (measured: X1 is the only mutation whose output mentions the cap). No test builds a pool with a size below 1.
2. **(m1) is all 26 `.hex` keys, each `.hex` → `.hex()`, as one diff** (clarification 2), on
   `ref`, `available_task`, `compute_task`, `store_task` and `validation_task` alike. The driver
   asserts that it changes exactly 26 lines.
3. **(m5) has a test built for it** (clarification 3):
   `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`, a
   lookup-only pool with an availability handler and every object available, notifying on every
   pass. (m5) fails it, and nothing else.
4. **Rows added to the inventory** (clarification 4, and §2.4's "a branch the agent finds"): P0,
   the absent post handler at each of the five exits, with five mutations; Z1, `_format_rates`'
   `assert` (`:42`), unreachable; Z2, the five `max(…, 0)` clamps, never active (E1 survives).
   (These added unreachable rows are named Z, so as not to collide with the decisions U1–U10;
   the prompt's own U1 keeps its name.) **Beyond the brief**, as the prompt's §2.4 asks: D1–D3,
   the three default handlers, which §2.3 asks `test_construction.py` to reach but §2.4 gives no
   row; Z3 (`:262`'s `and allow_store`) and
   Z4 (`:250`'s `and len(self._todo) > 0`), both redundant (E2, E3 survive); and Z5 (`:403`'s
   `_compute_data.pop`), unobservable (E4 survives). The survivors are recorded in §5.3.
   **IMPLEMENTATION CHOICE** for the additions beyond the brief.
5. **The clock** (clarification 5). `step` is a whole number of seconds (1 by default), so
   `format_time` prints `1s`, `3s`, and the lines stay exact. `perf_counter()` advances, then
   returns the new reading; `now()` reads the same reading without advancing, so a stamp is the
   reading of the `:523` call before it.
6. **`wait` enforces Ray's two further checks** (clarification 6): a single `ObjectRef` is a
   `TypeError` before the list check, and a negative `timeout` a `ValueError`. Each has a test.
7. **`PoolTestCase` has no `test_` method** (clarification 7), nor do the modules' intermediate
   bases (`BuilderTestCase`, `RunPathTestCase`, `SchedulingTestCase`), so importing them adds
   nothing to a module's count.

Choices of this prompt's agent:

8. **Entry points beyond the prompt's**, all marked *(+)* in §1.1: `namespace()`, `value_of()`,
   `get_calls`, `log`, `max_wait_calls`, `time_namespace()`, `datetime_namespace()`, `stamp()`,
   `perf_counter_calls`, `Blob`, `active_ray()`/`set_active_ray()`, `PoolRun`, `make_pool()`,
   `run_existing()` and four builder/handler helpers. The prompt's "companion" for `datetime` is
   `ScriptedClock.datetime_namespace()`. **IMPLEMENTATION CHOICE.**
9. **`get`'s errors**: `KeyError` naming the hex for a ref it did not mint, `TypeError` for a list
   or a non-ref. **IMPLEMENTATION CHOICE.**
10. **More than one mutation for some rows.** The prompt asks for one per row. Of the 44
    reachable rows, 28 have one and 16 have several, every one failing: R4, R7, R8, L4, V1, N1,
    N2, F2, Q1, Q2 and T2 have sub-mutations (`R4b`, …); P1 has ten (at each exit, a `None` return
    replacing the entry, and a replacement without `store_results`) and P0 five; and C3, S4 and N5
    also carry (m3), (m2) and (m5). **IMPLEMENTATION CHOICE.**
11. **The fault tests pin the raising line's text, not its number.** "`KeyError` from `:322`" is
    asserted as the last frame in `RayWorkPool.py` having the source text
    `item_type, payload = self._data[ref.hex]`; faults 3 and 4b likewise. `assertRaises` clears
    the traceback, so a helper, `raised_by`, catches the exception itself. Line numbers move when
    04 edits the module; the text identifies the line. **IMPLEMENTATION CHOICE.**
12. **X1's seed is keyed both ways.** `_data` is seeded under `ref.hex` and `ref.hex()`, so that
    the test pins the branch, not the keying, and (m1) does not fail it. Both are writes to
    `_data`, within §2.2's seam. **IMPLEMENTATION CHOICE.**
13. **The defaults' N1 test does not catch N1b.** With the defaults, a short run is silent because
    of the 300 s interval and the 500-item batch as well as the 60 s minimum, so removing the
    minimum (N1b) is caught by `test_the_minimum_interval_is_a_strict_bound` instead, which pins
    the minimum alone and its strictness. The defaults test says so in its docstring.
    **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT. The spacing of the printed lines was taken from `:545`, `:550-551`, `:567`,
`:570` and `:574`; the prompt's paraphrase in §2.5 agrees with it, character for character.

## 3. Verification performed

### 3.1 The suite (prompt §3.1)

**Before: 3** (`Ran 3 tests in 0.863s … OK`, at `319099a`). **After: 116.**
`./venv/bin/python -m unittest discover -s raypoolkit/tests -t .`, from the repository root, output
to a scratch file:

```
....................................................................................................................
----------------------------------------------------------------------
Ran 116 tests in 3.571s

OK
```

| Module | Before | After |
|---|---|---|
| `test_package_imports` | 3 | 3 |
| `test_standins` | — | 30 |
| `test_construction` | — | 12 |
| `test_task_builder` | — | 20 |
| `test_run_paths` | — | 22 |
| `test_scheduling` | — | 7 |
| `test_printed_lines` | — | 17 |
| `test_inherited_faults` | — | 5 |
| **Total** | **3** | **116** |

Counted from the verbose run's `(raypoolkit.tests.<module>.…)` lines. Several tests use
`subTest` (the five exits, the three sequence kinds, the handler sets, the value cases); a subtest
is not counted.

**Checking the expected lines.** Every expected line in `test_printed_lines.py` was derived by
hand from the clock's readings before the test was first run, and is commented with them. One
derivation was wrong: in the compute-and-validation run, `1/7` and `1/9` per second were written as
`8.571/min` and `6.667/min`, but `_readable_rate` moves to the next unit while the value is below
10, so the pool prints `514.3/hr` and `400/hr`. The error was the derivation's, not the module's;
the test was corrected to the module's output. Every other line matched at the first run.

### 3.2 No Ray (prompt §3.2)

`pgrep -lf 'gcs_server|raylet|ray::'` was empty (exit 1) at the start, before and after the first
full suite run, after all the mutation runs, and before and after the final suite run. `ray.is_initialized()` is asserted false in every
`PoolTestCase`'s tear-down. The guard fires only where a test makes it fire:
`test_standins.TestRayInitGuard.test_real_get_and_wait_reach_the_refused_ray_init` calls the real
`ray.get` and `ray.wait` on a minted ref, and each raises `RayInitCalled`; a second `ray.get`
raises it again (the auto-init lock is released).

### 3.3 The equivalence check (prompt §3.5)

`./venv/bin/python docs/extraction/compare_with_source.py`, exit **0**, whole output:

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 572
  D-imp: 2
  D-pool: 1
  unclassified: 0
    D-imp   source :8 / package :8
        - from Datastore.SQL.ShardedPool import ShardedPool
        + from raypoolkit.contract import DatastorePool
    D-imp   source :9 / package :9
        - from utilities import format_time
        + from raypoolkit._timing import format_time
    D-pool  source :75 / package :75
        -         pool: ShardedPool,
        +         pool: DatastorePool,

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 4
  unclassified: 0
    D-int   SECONDS_PER_MINUTE: package :11-11 equals source :20-20
    D-int   SECONDS_PER_HOUR: package :12-12 equals source :21-21
    D-int   SECONDS_PER_DAY: package :13-13 equals source :22-22
    D-int   format_time: package :16-52 equals source :25-61
    D-int   span: package :11-end equals source :20-61 byte for byte

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)
  raypoolkit/tests/standins.py: present (02 §2.1: the Ray, clock, work-object and pool stand-ins)
  raypoolkit/tests/test_standins.py: present (02 §2.1: the stand-ins' own tests)
  raypoolkit/tests/test_construction.py: present (02 §2.3: the constructor)
  raypoolkit/tests/test_task_builder.py: present (02 §2.3: the task builder's outcomes)
  raypoolkit/tests/test_run_paths.py: present (02 §2.3: the paths through the dispatch loop)
  raypoolkit/tests/test_scheduling.py: present (02 §2.3: the queue and batch sizes)
  raypoolkit/tests/test_printed_lines.py: present (02 §2.3: the printed lines (U9))
  raypoolkit/tests/test_inherited_faults.py: present (02 §2.3: faults 1-4, pinned as they behave)

Undeclared files under raypoolkit/: 0

RESULT: OK
```

01's counts: `RayWorkPool.py` 572 identical, 2 D-imp, 1 D-pool, 0 unclassified; `_timing.py` 4
D-int and the span; **12** declared files, all present; 0 undeclared. `git diff 49f3ddf --
raypoolkit/RayWorkPool.py` is empty.

### 3.4 The guard (prompt §3.6)

`test_package_imports.TestPackageImports.test_every_import_is_stdlib_ray_or_the_package` passes
over the eight new modules, which import only `contextlib`, `io`, `pickle`, `re`, `sys`,
`traceback`, `types`, `unittest`, `datetime`, `typing`, `ray` and `raypoolkit`.

### 3.5 `black` (prompt §3.7)

`./venv/bin/black --check raypoolkit docs`: "15 files would be left unchanged." `black` reformatted four of the new test
files when first run; no file outside `raypoolkit/tests/` and `compare_with_source.py` was passed to
it.

### 3.6 The format edges (prompt §2.5), re-measured

From the scratchpad, by calling the package's functions (not copied from the prompt): `format_time`
`0.00499` → `0.00499s`, `60` → `60s`, `61` → `1m 1s`, `3600` → `60m 0s`, `86400` → `24h 0s`,
`90061.25` → `1d 1h 1m 1.25s`; `_readable_rate` `0` → `0/day`, `0.01` → `36/hr`, `0.2` →
`12/min`, `10` → `10/sec`, `12345.6` → `1.235e+04/sec`; `_format_rates(10.0, 20.0, 5, 2)` →
`18/min, avg 15/min`, `(None, 2.0, 6, None)` → `avg 180/min`, `(None, None, 3, None)` → `''`. All
fourteen equal the prompt's. `ObjectRef(bytes(n))` constructs at 28 and raises `ValueError` ("ID
string needs to have length 28, got n") at 20 and 4; refs from equal bytes are `==`, hash equal
and make a one-member set, their `.hex` methods are unequal and their `.hex()` strings equal;
`pickle` and `copy.deepcopy` give an equal, distinct ref; a naive `datetime` formats with `%z` as
`2026-10-10 12:00:02`.

## 4. The inventory

One row per §2.4 ID, and the rows this prompt adds (*added*). Test names are
`<Class>.<test>`, in the modules of §1. Mutation IDs refer to §5, which gives each diff, every test it fails,
and the one test named for it, which the driver checked it fails (all 89 do). "Failed" counts
the distinct tests each mutation fails.

| ID | Lines | Branch | Test(s) | Mutation(s) (§5) | Failed |
|---|---|---|---|---|---|
| C1 | `:94-97` | compute without persist → `RuntimeError` | `TestHandlerChecks.test_compute_handler_without_persist_handler_raises_runtime_error` | C1 | C1: 1 test |
| C2 | `:99-102` | persist without compute → `RuntimeWarning` (fault 4) | `TestHandlerChecks.test_persist_handler_without_compute_handler_raises_runtime_warning`<br>`TestInheritedFaults.test_fault_persist_handler_without_compute_raises_runtime_warning` | C2 | C2: 2 tests |
| C3 | `:137-139` | `store_results` → `results` of `None`s | `TestResultsAndTitle.test_store_results_sizes_results_and_fills_it_with_none`<br>`TestResultsAndTitle.test_results_is_not_set_without_store_results`<br>`TestInheritedFaults.test_fault_store_results_sizes_from_len_of_the_task_list` | C3, m3 | C3: 21 tests; m3: 1 test |
| C4 | `:165-166` | `title` → the banner | `TestResultsAndTitle.test_a_title_prints_the_banner_at_construction`<br>`TestResultsAndTitle.test_no_title_prints_nothing` | C4 | C4: 11 tests |
| D1 *(added)* | `:60-61` | the default compute handler | `TestDefaultHandlers.test_the_default_compute_handler_calls_compute_with_the_arguments` | D1 | D1: 2 tests |
| D2 *(added)* | `:64-65` | the default store handler | `TestDefaultHandlers.test_the_default_store_handler_calls_store` | D2 | D2: 4 tests |
| D3 *(added)* | `:68-69` | the default persist handler | `TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool` | D3 | D3: 26 tests |
| R1 | `:250` | a batch only while the queue has room | `TestBatchCreation.test_a_batch_is_created_only_while_the_queue_has_room`<br>`TestSizes.test_max_task_queue_holds_back_the_next_batch_until_the_queue_drains_below_it` | R1 | R1: 2 tests |
| R2 | `:252` | at most `create_batch_size` calls | `TestBatchCreation.test_a_batch_makes_at_most_create_batch_size_builder_calls`<br>`TestSizes.test_the_default_sizes_build_five_at_a_time_and_process_one_at_a_time` | R2 | R2: 6 tests |
| R3 | `:262-266` | result index only with `store_results` and a single return | `TestSingleReturns.test_store_results_takes_a_result_index_per_single_return_in_task_order`<br>`TestSingleReturns.test_without_store_results_a_single_return_takes_no_index` | R3 | R3: 19 tests |
| R4 | `:271-279` | a dict with `"ref"`, ± `"compute_payload"` | `TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`<br>`TestSingleReturns.test_a_dict_without_a_compute_payload_passes_no_payload` | R4, R4b | R4: 6 tests; R4b: 3 tests |
| R5 | `:281-282` | a bare `ObjectRef` | `TestSingleReturns.test_a_bare_object_ref_is_enqueued` | R5 | R5: 58 tests |
| R6 | `:284-287` | anything else → `RuntimeError` | `TestRefusedReturns.test_an_int_is_refused`<br>… `_a_string_`, `_a_dict_without_ref_`, `_a_nested_list_`, `_a_refused_element_of_a_sequence_` | R6 | R6: 5 tests |
| R7 | `:289-294` | `None`; with `store_results` → `RuntimeError` | `TestNoneReturns.test_none_from_every_builder_enqueues_nothing_and_waits_on_nothing`<br>`TestNoneReturns.test_none_for_some_items_enqueues_the_others`<br>`TestNoneReturns.test_none_with_store_results_raises` | R7, R7b | R7: 3 tests; R7b: 1 test |
| R8 | `:296-307` | a list, tuple or set; with `store_results` → `RuntimeError` | `TestSequenceReturns.test_a_list_a_tuple_and_a_set_are_each_enqueued_element_by_element`<br>`TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`<br>`TestSequenceReturns.test_an_empty_sequence_enqueues_nothing`<br>`TestSequenceReturns.test_a_sequence_with_store_results_raises` | R8, R8b | R8: 6 tests; R8b: 1 test |
| R9 | `:315` | `num_returns = min(…)`, 0 with nothing in flight | `TestBatchCreation.test_num_returns_is_the_smaller_of_process_batch_size_and_the_work_in_flight`<br>`TestSizes.test_process_batch_size_sets_how_many_tasks_each_wait_returns` | R9 | R9: 7 tests |
| L1 | `:324-341` | a lookup completes; its object in `results` | `TestLookup.test_a_completed_lookup_puts_its_object_in_results`<br>`TestLookup.test_results_hold_what_get_returned_not_what_the_builder_minted` | L1 | L1: 10 tests |
| L2 | `:345-357` | available, with an availability handler | `TestAvailable.test_available_with_an_availability_handler_runs_an_available_task` | L2 | L2: 2 tests |
| L3 | `:361-364` | available, no availability handler → exit 1 | `TestAvailable.test_available_without_an_availability_handler_exits_to_the_post_handler` | L3 | L3: 10 tests |
| L4 | `:366-392` | not available, compute handler; `label`, `payload` | `TestNotAvailable.test_not_available_with_a_compute_handler_runs_a_compute_task`<br>`TestNotAvailable.test_a_label_from_the_label_builder_is_passed_as_label`<br>`TestNotAvailable.test_a_label_builder_returning_none_passes_no_label`<br>`TestNotAvailable.test_a_label_and_a_payload_are_passed_together` | L4, L4b, L4c, L4d | L4: 26 tests; L4b: 5 tests; L4c: 3 tests; L4d: 3 tests |
| L5 | `:366-368` | not available, no compute handler → nothing | `TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing` | L5 | L5: 1 test |
| L6 | `:396-401` | no `available` attribute → exit 2 | `TestBlob.test_an_object_without_available_exits_to_the_post_handler` | L6 | L6: 5 tests |
| A1 | `:405-420` | an availability task completes → exit 3 | `TestAvailable.test_available_with_an_availability_handler_runs_an_available_task` | A1 | A1: 4 tests |
| K1 | `:422-447` | a compute completes → store, persist, a store task | `TestComputeStoreValidate.test_a_completed_compute_runs_the_store_handler_then_the_persist_handler`<br>`TestInheritedFaults.test_fault_store_handler_none_with_compute_fails_at_first_compute` | K1 | K1: 6 tests |
| S1 | `:455-461` | a store's object not available → `RuntimeError` | `TestComputeStoreValidate.test_a_store_whose_object_is_not_available_raises` | S1 | S1: 1 test |
| S2 | `:463-471` | the persisted object replaces the entry | `TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object` | S2 | S2: 7 tests |
| S3 | `:474-485` | a validation handler → a `"validate"` task | `TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object` | S3 | S3: 4 tests |
| S4 | `:489-492` | no validation handler → exit 4 (fault 2) | `TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`<br>`TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object` | S4, m2 | S4: 5 tests; m2: 2 tests |
| V1 | `:499-503` | a validation not `True` → the warning | `TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`<br>`TestComputeStoreValidate.test_a_validation_that_is_true_prints_nothing`<br>`TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines` | V1, V1b | V1: 2 tests; V1b: 1 test |
| V2 | `:513-516` | a validation completes → exit 5 | `TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object` | V2 | V2: 5 tests |
| P1 | `:363`, `:400`, `:419`, `:491`, `:515` | a non-`None` return replaces only with `store_results` | `TestExits.test_a_returned_replacement_replaces_the_results_entry`<br>`TestExits.test_a_returned_none_leaves_the_results_entry`<br>`TestExits.test_a_returned_replacement_without_store_results_is_dropped` | P1-1, P1-1b, P1-2, P1-2b, P1-3, P1-3b, P1-4, P1-4b, P1-5, P1-5b | P1-1: 3 tests; P1-1b: 1 test; P1-2: 2 tests; P1-2b: 1 test; P1-3: 2 tests; P1-3b: 1 test; P1-4: 3 tests; P1-4b: 1 test; P1-5: 2 tests; P1-5b: 1 test |
| P0 *(added)* | `:361`, `:398`, `:417`, `:489`, `:513` | no post handler at an exit → no call | `TestExits.test_each_exit_without_a_post_handler_calls_nothing` | P0-1, P0-2, P0-3, P0-4, P0-5 | P0-1: 21 tests; P0-2: 1 test; P0-3: 2 tests; P0-4: 15 tests; P0-5: 4 tests |
| X1 | `:518-519` | an unexpected item type → `RuntimeError` (seeded) | `TestUnexpectedItemType.test_an_unexpected_item_type_raises` | X1 | X1: 1 test |
| N1 | `:526-529` | no progress without a title or before the minimum | `TestProgressAndCompletion.test_no_progress_lines_without_a_title`<br>`TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`<br>`TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound` | N1a, N1b | N1a: 1 test; N1b: 1 test |
| N2 | `:530-533` | a pair by time or by count | `TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`<br>`TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed` | N2a, N2b | N2a: 7 tests; N2b: 1 test |
| N3 | `:535-542` | the percentage | `TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built` | N3 | N3: 2 tests |
| N4 | `:546-547` | the suffix above 99.99% | `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`<br>`TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built` | N4 | N4: 7 tests |
| N5 | `:557-561` | the last counts move on | `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`<br>`TestProgressAndCompletion.test_the_available_rate_is_per_interval` | N5, m5 | N5: 5 tests; m5: 1 test |
| F1 | `:563-571` | with a title: `total_time` and the completion pair | `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`<br>`TestResultsAndTitle.test_total_time_is_set_only_with_a_title` | F1 | F1: 11 tests |
| F2 | `:572-575` | the no-compute line | `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`<br>`TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass` | F2, F2b | F2: 7 tests; F2b: 2 tests |
| Q1 | `:168-182` | the queued message's segments | `TestStatusMessages.test_the_queued_message_has_a_segment_per_handler`<br>`TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass` | Q1a, Q1b, Q1c, Q1d | Q1a: 2 tests; Q1b: 2 tests; Q1c: 2 tests; Q1d: 2 tests |
| Q2 | `:184-243` | the completed message's segments, ± rates | `TestStatusMessages.test_the_completed_message_without_rates`<br>`TestStatusMessages.test_the_completed_message_with_rates` | Q2a, Q2b, Q2c, Q2d, Q2e | Q2a: 4 tests; Q2b: 4 tests; Q2c: 3 tests; Q2d: 4 tests; Q2e: 1 test |
| T1 | `:20-33` | `_readable_rate`'s units | `TestPureFunctions.test_readable_rate_units` | T1 | T1: 12 tests |
| T2 | `:36-57` | `_format_rates` | `TestPureFunctions.test_format_rates` | T2a, T2b, T2c | T2a: 6 tests; T2b: 11 tests; T2c: 10 tests |
| U1 | `:33` | `_readable_rate`'s `raise NotImplementedError` | none: unreachable: the `"day"` entry's multiplier is `None`, so the loop always returns there | — | — |
| Z1 *(added)* | `:42` | `_format_rates`' `assert current_value is not None` | none: unreachable: every caller passes one of the pool's `int` counts | — | — |
| Z2 *(added)* | `:340`, `:412`, `:437`, `:470`, `:508` | the five `max(… - 1, 0)` clamps | none: never active: each decrement follows the increment for the same task. Removing all five (E1) is an equivalent mutation and survives | — | — |
| Z3 *(added)* | `:262` | R3's `and allow_store` | none: redundant: `allow_store=False` comes only from the sequence branch, which raises first under `store_results`. Removing it (E2) survives | — | — |
| Z4 *(added)* | `:250` | R1's `and len(self._todo) > 0` | none: redundant: the inner `while` at `:252` checks it again. Removing it (E3) survives | — | — |
| Z5 *(added)* | `:403` | `self._compute_data.pop(ref.hex, None)` | none: unobservable: without it an entry stays in `_compute_data`, which nothing public reads. Removing it (E4) survives | — | — |

## 5. The deliberate-breakage record

Every diff is exactly as applied, by `git apply` from the repository root, by a driver in the
session scratchpad (never under `raypoolkit/`). For each: `git apply --check`; `git apply`; the
whole suite by `CLAUDE.md`'s command under a 300 s timeout; `git apply -R --check`; `git apply -R`;
then the file's SHA-256 and `git status --porcelain --untracked-files=all` compared with their
values before ("tree restored"). All 96 diffs were then replayed again by a `bash` loop (`--check`,
apply, `-R --check`, `-R`, status unchanged after each: 96 replayed, 0 bad), and (m1) was re-run
through the suite from `bash`, with the same result. None is committed. They were run on the final
tree of this commit. "Failed" lists each failing test once (a test with several failing subtests
is listed once).

**Summary.** 89 mutations of `raypoolkit/RayWorkPool.py`: **89 caught, 0 hangs, 0 trees not
restored**, and each fails the test named for it. 4 equivalent mutations survive (§5.3). The
stand-in diffs (s1) and (s2) each fail tests; (s3) was not run (§5.4).

*A slip in the driver, corrected.* This filesystem is case-insensitive, so the stand-in diffs, first
named `s1`–`s3`, overwrote the diff and output files of the mutations `S1`–`S3`. The results had
been recorded from the right diffs before the overwrite, but the files were not. The stand-in diffs
were renamed `st-s1`–`st-s3`, and `S1`–`S3`, (s1) and (s2) were run again, with the same results;
what follows is from those runs.

### 5.1 The inventory's mutations

**C1** — compute without persist check removed. Suite: `Ran 116 tests in 1.643s / FAILED (failures=1)`; tree restored: yes. Named test: `TestHandlerChecks.test_compute_handler_without_persist_handler_raises_runtime_error`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -91,7 +91,7 @@
         title: str = None,
         store_results: bool = False,
     ):
-        if compute_handler is not None and persist_handler is None:
+        if False:
             raise RuntimeError(
                 "If a compute maker is supplied, a persist maker must also be supplied to serialize the result of the computation"
             )
```

Failed:
- `test_construction.TestHandlerChecks.test_compute_handler_without_persist_handler_raises_runtime_error`

**C2** — persist without compute check removed. Suite: `Ran 116 tests in 1.733s / FAILED (failures=2)`; tree restored: yes. Named test: `TestHandlerChecks.test_persist_handler_without_compute_handler_raises_runtime_warning`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -96,7 +96,7 @@
                 "If a compute maker is supplied, a persist maker must also be supplied to serialize the result of the computation"
             )
 
-        if compute_handler is None and persist_handler is not None:
+        if False:
             raise RuntimeWarning(
                 "No compute maker was supplied, but a persist maker was provided. This will have no effect because there will be no compute results to store"
             )
```

Failed:
- `test_construction.TestHandlerChecks.test_persist_handler_without_compute_handler_raises_runtime_warning`
- `test_inherited_faults.TestInheritedFaults.test_fault_persist_handler_without_compute_raises_runtime_warning`

**C3** — store_results branch at construction removed. Suite: `Ran 116 tests in 1.495s / FAILED (failures=1, errors=32)`; tree restored: yes. Named test: `TestResultsAndTitle.test_store_results_sizes_results_and_fills_it_with_none`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -134,7 +134,7 @@
         self._compute_data = {}
 
         self._store_results = store_results
-        if store_results:
+        if False:
             self.results = [None for _ in range(len(task_list))]
             self._current_idx = 0
 
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`
- `test_construction.TestResultsAndTitle.test_no_title_prints_nothing`
- `test_construction.TestResultsAndTitle.test_store_results_sizes_results_and_fills_it_with_none`
- `test_inherited_faults.TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`
- `test_inherited_faults.TestInheritedFaults.test_fault_store_results_sizes_from_len_of_the_task_list`
- `test_run_paths.TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`
- `test_run_paths.TestAvailable.test_available_without_an_availability_handler_exits_to_the_post_handler`
- `test_run_paths.TestBlob.test_an_object_without_available_exits_to_the_post_handler`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`
- `test_run_paths.TestLookup.test_a_completed_lookup_puts_its_object_in_results`
- `test_run_paths.TestLookup.test_results_hold_what_get_returned_not_what_the_builder_minted`
- `test_run_paths.TestNotAvailable.test_not_available_with_a_compute_handler_runs_a_compute_task`
- `test_run_paths.TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_through_compute_and_store`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_when_lookups_complete_in_reverse`
- `test_task_builder.TestSingleReturns.test_store_results_takes_a_result_index_per_single_return_in_task_order`

**C4** — banner branch removed. Suite: `Ran 116 tests in 1.594s / FAILED (failures=11)`; tree restored: yes. Named test: `TestResultsAndTitle.test_a_title_prints_the_banner_at_construction`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -162,7 +162,7 @@
         self._last_notify_time = self._start_time
 
         self._title = title
-        if title is not None:
+        if False:
             print(f"\n** {title}")
 
     def _build_queued_status_message(self):
```

Failed:
- `test_construction.TestResultsAndTitle.test_a_title_prints_the_banner_at_construction`
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`

**D1** — default compute handler drops its keyword arguments. Suite: `Ran 116 tests in 1.137s / FAILED (failures=2)`; tree restored: yes. Named test: `TestDefaultHandlers.test_the_default_compute_handler_calls_compute_with_the_arguments`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -58,7 +58,7 @@
 
 
 def _default_compute_handler(obj, **kwargs) -> ObjectRef:
-    return obj.compute(**kwargs)
+    return obj.compute()
 
 
 def _default_store_handler(obj, pool) -> None:
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_compute_handler_calls_compute_with_the_arguments`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`

**D2** — default store handler does not call store(). Suite: `Ran 116 tests in 0.996s / FAILED (failures=4)`; tree restored: yes. Named test: `TestDefaultHandlers.test_the_default_store_handler_calls_store`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -62,7 +62,7 @@
 
 
 def _default_store_handler(obj, pool) -> None:
-    obj.store()
+    pass
 
 
 def _default_persist_handler(obj, pool) -> ObjectRef:
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`
- `test_construction.TestDefaultHandlers.test_the_default_store_handler_calls_store`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`

**D3** — default persist handler does not call object_store. Suite: `Ran 116 tests in 0.902s / FAILED (errors=33)`; tree restored: yes. Named test: `TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -66,7 +66,7 @@
 
 
 def _default_persist_handler(obj, pool) -> ObjectRef:
-    return pool.object_store(obj)
+    return None
 
 
 class RayWorkPool:
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_compute_handler_calls_compute_with_the_arguments`
- `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`
- `test_construction.TestDefaultHandlers.test_the_default_store_handler_calls_store`
- `test_construction.TestResultsAndTitle.test_no_title_prints_nothing`
- `test_inherited_faults.TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_store_whose_object_is_not_available_raises`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_true_prints_nothing`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`
- `test_run_paths.TestNotAvailable.test_a_label_and_a_payload_are_passed_together`
- `test_run_paths.TestNotAvailable.test_a_label_builder_returning_none_passes_no_label`
- `test_run_paths.TestNotAvailable.test_a_label_from_the_label_builder_is_passed_as_label`
- `test_run_paths.TestNotAvailable.test_not_available_with_a_compute_handler_runs_a_compute_task`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_through_compute_and_store`
- `test_scheduling.TestSizes.test_process_batch_size_applies_to_every_stage`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`
- `test_task_builder.TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`
- `test_task_builder.TestSingleReturns.test_a_dict_without_a_compute_payload_passes_no_payload`

**R1** — the max_task_queue gate removed. Suite: `Ran 116 tests in 1.145s / FAILED (failures=2)`; tree restored: yes. Named test: `TestBatchCreation.test_a_batch_is_created_only_while_the_queue_has_room`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -247,7 +247,7 @@
             # if there is space in the task queue, and there are items remaining to queue,
             # then initiate new work
             # either we create a fixed batch size, or we enqueue work until the task queue is exhasuted
-            if len(self._inflight) < self._max_task_queue and len(self._todo) > 0:
+            if len(self._todo) > 0:
                 count = 0
                 while count < self._create_batch_size and len(self._todo) > 0:
                     # consume more tasks from the task queue and schedule their work
```

Failed:
- `test_scheduling.TestSizes.test_max_task_queue_holds_back_the_next_batch_until_the_queue_drains_below_it`
- `test_task_builder.TestBatchCreation.test_a_batch_is_created_only_while_the_queue_has_room`

**R2** — the create_batch_size bound removed. Suite: `Ran 116 tests in 1.265s / FAILED (failures=6)`; tree restored: yes. Named test: `TestBatchCreation.test_a_batch_makes_at_most_create_batch_size_builder_calls`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -249,7 +249,7 @@
             # either we create a fixed batch size, or we enqueue work until the task queue is exhasuted
             if len(self._inflight) < self._max_task_queue and len(self._todo) > 0:
                 count = 0
-                while count < self._create_batch_size and len(self._todo) > 0:
+                while len(self._todo) > 0:
                     # consume more tasks from the task queue and schedule their work
 
                     # pop gets the item from the end of the list
```

Failed:
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_scheduling.TestSizes.test_max_task_queue_holds_back_the_next_batch_until_the_queue_drains_below_it`
- `test_scheduling.TestSizes.test_the_default_sizes_build_five_at_a_time_and_process_one_at_a_time`
- `test_task_builder.TestBatchCreation.test_a_batch_is_created_only_while_the_queue_has_room`
- `test_task_builder.TestBatchCreation.test_a_batch_makes_at_most_create_batch_size_builder_calls`

**R3** — no result index is ever taken. Suite: `Ran 116 tests in 1.065s / FAILED (errors=31)`; tree restored: yes. Named test: `TestSingleReturns.test_store_results_takes_a_result_index_per_single_return_in_task_order`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -259,7 +259,7 @@
                     def store_single_ref(ref, allow_store=True):
                         self._inflight[ref.hex] = ref
 
-                        if self._store_results and allow_store:
+                        if False:
                             self._data[ref.hex] = ("lookup", self._current_idx)
                             self._current_idx += 1
                         else:
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`
- `test_construction.TestResultsAndTitle.test_no_title_prints_nothing`
- `test_inherited_faults.TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`
- `test_run_paths.TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`
- `test_run_paths.TestAvailable.test_available_without_an_availability_handler_exits_to_the_post_handler`
- `test_run_paths.TestBlob.test_an_object_without_available_exits_to_the_post_handler`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`
- `test_run_paths.TestLookup.test_a_completed_lookup_puts_its_object_in_results`
- `test_run_paths.TestLookup.test_results_hold_what_get_returned_not_what_the_builder_minted`
- `test_run_paths.TestNotAvailable.test_not_available_with_a_compute_handler_runs_a_compute_task`
- `test_run_paths.TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_through_compute_and_store`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_when_lookups_complete_in_reverse`
- `test_task_builder.TestSingleReturns.test_store_results_takes_a_result_index_per_single_return_in_task_order`

**R4** — a dict with ref is not recognised. Suite: `Ran 116 tests in 1.053s / FAILED (errors=7)`; tree restored: yes. Named test: `TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -268,7 +268,7 @@
                         self._num_lookup_queue += 1
 
                     def store_ref(ref_data, allow_store=True):
-                        if isinstance(ref_data, dict) and "ref" in ref_data:
+                        if False:
                             # interpret as a dict containing the ObjectRef, and possibly also a compute payload
                             ref = ref_data["ref"]
                             store_single_ref(ref, allow_store=allow_store)
```

Failed:
- `test_run_paths.TestNotAvailable.test_a_label_and_a_payload_are_passed_together`
- `test_task_builder.TestSequenceReturns.test_a_list_a_tuple_and_a_set_are_each_enqueued_element_by_element`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`
- `test_task_builder.TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`
- `test_task_builder.TestSingleReturns.test_a_dict_without_a_compute_payload_passes_no_payload`
- `test_task_builder.TestSingleReturns.test_store_results_takes_a_result_index_per_single_return_in_task_order`

**R4b** — compute_payload is not recorded. Suite: `Ran 116 tests in 1.226s / FAILED (failures=3)`; tree restored: yes. Named test: `TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -273,7 +273,7 @@
                             ref = ref_data["ref"]
                             store_single_ref(ref, allow_store=allow_store)
 
-                            if "compute_payload" in ref_data:
+                            if False:
                                 self._compute_data[ref.hex] = ref_data[
                                     "compute_payload"
                                 ]
```

Failed:
- `test_run_paths.TestNotAvailable.test_a_label_and_a_payload_are_passed_together`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`
- `test_task_builder.TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`

**R5** — a bare ObjectRef is not recognised. Suite: `Ran 116 tests in 1.141s / FAILED (failures=2, errors=77)`; tree restored: yes. Named test: `TestSingleReturns.test_a_bare_object_ref_is_enqueued`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -278,7 +278,7 @@
                                     "compute_payload"
                                 ]
 
-                        elif isinstance(ref_data, ObjectRef):
+                        elif False:
                             store_single_ref(ref_data, allow_store=allow_store)
 
                         else:
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_compute_handler_calls_compute_with_the_arguments`
- `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`
- `test_construction.TestDefaultHandlers.test_the_default_store_handler_calls_store`
- `test_construction.TestResultsAndTitle.test_no_title_prints_nothing`
- `test_construction.TestResultsAndTitle.test_results_is_not_set_without_store_results`
- `test_construction.TestResultsAndTitle.test_total_time_is_set_only_with_a_title`
- `test_inherited_faults.TestInheritedFaults.test_fault_in_flight_work_is_keyed_on_a_bound_method`
- `test_inherited_faults.TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`
- `test_inherited_faults.TestInheritedFaults.test_fault_store_handler_none_with_compute_fails_at_first_compute`
- `test_inherited_faults.TestInheritedFaults.test_fault_store_results_sizes_from_len_of_the_task_list`
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_without_a_title`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_run_paths.TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`
- `test_run_paths.TestAvailable.test_available_without_an_availability_handler_exits_to_the_post_handler`
- `test_run_paths.TestBlob.test_an_object_without_available_exits_to_the_post_handler`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_compute_runs_the_store_handler_then_the_persist_handler`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_store_whose_object_is_not_available_raises`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_true_prints_nothing`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`
- `test_run_paths.TestLookup.test_a_completed_lookup_puts_its_object_in_results`
- `test_run_paths.TestLookup.test_results_hold_what_get_returned_not_what_the_builder_minted`
- `test_run_paths.TestNotAvailable.test_a_label_builder_returning_none_passes_no_label`
- `test_run_paths.TestNotAvailable.test_a_label_from_the_label_builder_is_passed_as_label`
- `test_run_paths.TestNotAvailable.test_not_available_with_a_compute_handler_runs_a_compute_task`
- `test_run_paths.TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_through_compute_and_store`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_when_lookups_complete_in_reverse`
- `test_scheduling.TestSizes.test_max_task_queue_holds_back_the_next_batch_until_the_queue_drains_below_it`
- `test_scheduling.TestSizes.test_one_builder_call_per_item`
- `test_scheduling.TestSizes.test_process_batch_size_applies_to_every_stage`
- `test_scheduling.TestSizes.test_process_batch_size_sets_how_many_tasks_each_wait_returns`
- `test_scheduling.TestSizes.test_the_default_sizes_build_five_at_a_time_and_process_one_at_a_time`
- `test_task_builder.TestBatchCreation.test_a_batch_is_created_only_while_the_queue_has_room`
- `test_task_builder.TestBatchCreation.test_a_batch_makes_at_most_create_batch_size_builder_calls`
- `test_task_builder.TestBatchCreation.test_num_returns_is_the_smaller_of_process_batch_size_and_the_work_in_flight`
- `test_task_builder.TestNoneReturns.test_none_for_some_items_enqueues_the_others`
- `test_task_builder.TestRefusedReturns.test_a_refused_element_of_a_sequence_is_refused`
- `test_task_builder.TestSequenceReturns.test_a_list_a_tuple_and_a_set_are_each_enqueued_element_by_element`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`
- `test_task_builder.TestSingleReturns.test_a_bare_object_ref_is_enqueued`
- `test_task_builder.TestSingleReturns.test_store_results_takes_a_result_index_per_single_return_in_task_order`
- `test_task_builder.TestSingleReturns.test_without_store_results_a_single_return_takes_no_index`

**R6** — an uninterpretable return is ignored, not refused. Suite: `Ran 116 tests in 0.831s / FAILED (failures=5)`; tree restored: yes. Named test: `TestRefusedReturns.test_an_int_is_refused`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -282,9 +282,7 @@
                             store_single_ref(ref_data, allow_store=allow_store)
 
                         else:
-                            raise RuntimeError(
-                                f'could not interpret output from task builder (object type="{type(ref_data).__name__}", contents={str(ref_data)})'
-                            )
+                            pass
 
                     if ref_data is None:
                         if self._store_results:
```

Failed:
- `test_task_builder.TestRefusedReturns.test_a_dict_without_ref_is_refused`
- `test_task_builder.TestRefusedReturns.test_a_nested_list_is_refused`
- `test_task_builder.TestRefusedReturns.test_a_refused_element_of_a_sequence_is_refused`
- `test_task_builder.TestRefusedReturns.test_a_string_is_refused`
- `test_task_builder.TestRefusedReturns.test_an_int_is_refused`

**R7** — None is not recognised. Suite: `Ran 116 tests in 0.899s / FAILED (failures=1, errors=2)`; tree restored: yes. Named test: `TestNoneReturns.test_none_from_every_builder_enqueues_nothing_and_waits_on_nothing`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -286,7 +286,7 @@
                                 f'could not interpret output from task builder (object type="{type(ref_data).__name__}", contents={str(ref_data)})'
                             )
 
-                    if ref_data is None:
+                    if False:
                         if self._store_results:
                             raise RuntimeError(
                                 "a task builder returned None, which is not compatible with store_results=True"
```

Failed:
- `test_task_builder.TestNoneReturns.test_none_for_some_items_enqueues_the_others`
- `test_task_builder.TestNoneReturns.test_none_from_every_builder_enqueues_nothing_and_waits_on_nothing`
- `test_task_builder.TestNoneReturns.test_none_with_store_results_raises`

**R7b** — None with store_results is not refused. Suite: `Ran 116 tests in 0.937s / FAILED (failures=1)`; tree restored: yes. Named test: `TestNoneReturns.test_none_with_store_results_raises`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -287,7 +287,7 @@
                             )
 
                     if ref_data is None:
-                        if self._store_results:
+                        if False:
                             raise RuntimeError(
                                 "a task builder returned None, which is not compatible with store_results=True"
                             )
```

Failed:
- `test_task_builder.TestNoneReturns.test_none_with_store_results_raises`

**R8** — a sequence is not recognised. Suite: `Ran 116 tests in 0.772s / FAILED (failures=5, errors=5)`; tree restored: yes. Named test: `TestSequenceReturns.test_a_list_a_tuple_and_a_set_are_each_enqueued_element_by_element`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -293,11 +293,7 @@
                             )
                         # nothing to enqueue for this item
 
-                    elif (
-                        isinstance(ref_data, list)
-                        or isinstance(ref_data, tuple)
-                        or isinstance(ref_data, set)
-                    ):
+                    elif False:
                         if self._store_results:
                             raise RuntimeError(
                                 "store_results=True is not compatible with returning multiple work items from a task builder"
```

Failed:
- `test_task_builder.TestRefusedReturns.test_a_nested_list_is_refused`
- `test_task_builder.TestRefusedReturns.test_a_refused_element_of_a_sequence_is_refused`
- `test_task_builder.TestSequenceReturns.test_a_list_a_tuple_and_a_set_are_each_enqueued_element_by_element`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`
- `test_task_builder.TestSequenceReturns.test_a_sequence_with_store_results_raises`
- `test_task_builder.TestSequenceReturns.test_an_empty_sequence_enqueues_nothing`

**R8b** — a sequence with store_results is not refused. Suite: `Ran 116 tests in 1.102s / FAILED (errors=3)`; tree restored: yes. Named test: `TestSequenceReturns.test_a_sequence_with_store_results_raises`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -298,7 +298,7 @@
                         or isinstance(ref_data, tuple)
                         or isinstance(ref_data, set)
                     ):
-                        if self._store_results:
+                        if False:
                             raise RuntimeError(
                                 "store_results=True is not compatible with returning multiple work items from a task builder"
                             )
```

Failed:
- `test_task_builder.TestSequenceReturns.test_a_sequence_with_store_results_raises`

**R9** — num_returns not capped by the work in flight. Suite: `Ran 116 tests in 0.990s / FAILED (failures=2, errors=5)`; tree restored: yes. Named test: `TestBatchCreation.test_num_returns_is_the_smaller_of_process_batch_size_and_the_work_in_flight`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -312,7 +312,7 @@
                     count += 1
 
             # wait for some work to complete
-            num_returns = min(self._process_batch_size, len(self._inflight))
+            num_returns = self._process_batch_size
             done_refs, _ = ray.wait(
                 list(self._inflight.values()), num_returns=num_returns
             )
```

Failed:
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_through_compute_and_store`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_when_lookups_complete_in_reverse`
- `test_scheduling.TestSizes.test_process_batch_size_sets_how_many_tasks_each_wait_returns`
- `test_task_builder.TestBatchCreation.test_a_batch_makes_at_most_create_batch_size_builder_calls`
- `test_task_builder.TestBatchCreation.test_num_returns_is_the_smaller_of_process_batch_size_and_the_work_in_flight`
- `test_task_builder.TestNoneReturns.test_none_from_every_builder_enqueues_nothing_and_waits_on_nothing`
- `test_task_builder.TestSequenceReturns.test_an_empty_sequence_enqueues_nothing`

**L1** — a completed lookup's object not put in results. Suite: `Ran 116 tests in 0.872s / FAILED (failures=5, errors=9)`; tree restored: yes. Named test: `TestLookup.test_a_completed_lookup_puts_its_object_in_results`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -330,7 +330,7 @@
                     # result of the lookup should be a computable/storable object
                     obj = ray.get(ref)
 
-                    if self._store_results:
+                    if False:
                         self.results[idx] = obj
 
                     # remove the original 'lookup' task from the work queue
```

Failed:
- `test_run_paths.TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`
- `test_run_paths.TestAvailable.test_available_without_an_availability_handler_exits_to_the_post_handler`
- `test_run_paths.TestBlob.test_an_object_without_available_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`
- `test_run_paths.TestLookup.test_a_completed_lookup_puts_its_object_in_results`
- `test_run_paths.TestLookup.test_results_hold_what_get_returned_not_what_the_builder_minted`
- `test_run_paths.TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_when_lookups_complete_in_reverse`
- `test_task_builder.TestSingleReturns.test_store_results_takes_a_result_index_per_single_return_in_task_order`

**L2** — the availability handler is never used. Suite: `Ran 116 tests in 0.803s / FAILED (failures=2)`; tree restored: yes. Named test: `TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -344,7 +344,7 @@
                     if hasattr(obj, "available"):
                         if obj.available:
                             # check whether an availability handler exists
-                            if self._available_handler is not None:
+                            if False:
                                 available_task: ObjectRef = self._available_handler(obj)
 
                                 # add this task to the work queue
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_run_paths.TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`

**L3** — exit 1 never taken. Suite: `Ran 116 tests in 1.246s / FAILED (failures=12)`; tree restored: yes. Named test: `TestAvailable.test_available_without_an_availability_handler_exits_to_the_post_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -358,7 +358,7 @@
 
                             # otherwise, this is the exit point for driver flow associated with this task, so apply the
                             # postprocessing task, if one was supplied
-                            elif self._post_handler is not None:
+                            elif False:
                                 replacement_obj = self._post_handler(obj)
                                 if replacement_obj is not None and self._store_results:
                                     self.results[idx] = replacement_obj
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_fault_store_results_sizes_from_len_of_the_task_list`
- `test_run_paths.TestAvailable.test_available_without_an_availability_handler_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_when_lookups_complete_in_reverse`
- `test_task_builder.TestNoneReturns.test_none_for_some_items_enqueues_the_others`
- `test_task_builder.TestSequenceReturns.test_a_list_a_tuple_and_a_set_are_each_enqueued_element_by_element`
- `test_task_builder.TestSingleReturns.test_a_bare_object_ref_is_enqueued`
- `test_task_builder.TestSingleReturns.test_without_store_results_a_single_return_takes_no_index`

**L4** — no compute task is ever scheduled. Suite: `Ran 116 tests in 1.241s / FAILED (failures=29, errors=4)`; tree restored: yes. Named test: `TestNotAvailable.test_not_available_with_a_compute_handler_runs_a_compute_task`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -365,7 +365,7 @@
 
                         else:
                             # check whether a compute handler exists
-                            if self._compute_handler is not None:
+                            if False:
                                 # otherwise, schedule a compute task
                                 label: str = (
                                     self._label_builder(obj)
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_compute_handler_calls_compute_with_the_arguments`
- `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`
- `test_construction.TestDefaultHandlers.test_the_default_store_handler_calls_store`
- `test_inherited_faults.TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`
- `test_inherited_faults.TestInheritedFaults.test_fault_store_handler_none_with_compute_fails_at_first_compute`
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_compute_runs_the_store_handler_then_the_persist_handler`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_store_whose_object_is_not_available_raises`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`
- `test_run_paths.TestNotAvailable.test_a_label_and_a_payload_are_passed_together`
- `test_run_paths.TestNotAvailable.test_a_label_builder_returning_none_passes_no_label`
- `test_run_paths.TestNotAvailable.test_a_label_from_the_label_builder_is_passed_as_label`
- `test_run_paths.TestNotAvailable.test_not_available_with_a_compute_handler_runs_a_compute_task`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_through_compute_and_store`
- `test_scheduling.TestSizes.test_process_batch_size_applies_to_every_stage`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`
- `test_task_builder.TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`
- `test_task_builder.TestSingleReturns.test_a_dict_without_a_compute_payload_passes_no_payload`

**L4b** — label passed even when the label builder returns None. Suite: `Ran 116 tests in 0.965s / FAILED (failures=5)`; tree restored: yes. Named test: `TestNotAvailable.test_a_label_builder_returning_none_passes_no_label`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -373,7 +373,7 @@
                                     else None
                                 )
                                 compute_args = (
-                                    {"label": label} if label is not None else {}
+                                    {"label": label}
                                 )
 
                                 if ref.hex in self._compute_data:
```

Failed:
- `test_run_paths.TestNotAvailable.test_a_label_builder_returning_none_passes_no_label`
- `test_run_paths.TestNotAvailable.test_not_available_with_a_compute_handler_runs_a_compute_task`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`
- `test_task_builder.TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`
- `test_task_builder.TestSingleReturns.test_a_dict_without_a_compute_payload_passes_no_payload`

**L4c** — the label builder is never called. Suite: `Ran 116 tests in 1.594s / FAILED (failures=3)`; tree restored: yes. Named test: `TestNotAvailable.test_a_label_from_the_label_builder_is_passed_as_label`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -369,7 +369,7 @@
                                 # otherwise, schedule a compute task
                                 label: str = (
                                     self._label_builder(obj)
-                                    if self._label_builder is not None
+                                    if False
                                     else None
                                 )
                                 compute_args = (
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_compute_handler_calls_compute_with_the_arguments`
- `test_run_paths.TestNotAvailable.test_a_label_and_a_payload_are_passed_together`
- `test_run_paths.TestNotAvailable.test_a_label_from_the_label_builder_is_passed_as_label`

**L4d** — the compute payload is never passed. Suite: `Ran 116 tests in 2.789s / FAILED (failures=3)`; tree restored: yes. Named test: `TestNotAvailable.test_a_label_and_a_payload_are_passed_together`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -376,7 +376,7 @@
                                     {"label": label} if label is not None else {}
                                 )
 
-                                if ref.hex in self._compute_data:
+                                if False:
                                     compute_args.update(
                                         {"payload": self._compute_data[ref.hex]}
                                     )
```

Failed:
- `test_run_paths.TestNotAvailable.test_a_label_and_a_payload_are_passed_together`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`
- `test_task_builder.TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`

**L5** — the absent compute handler is called. Suite: `Ran 116 tests in 1.967s / FAILED (errors=1)`; tree restored: yes. Named test: `TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -365,7 +365,7 @@
 
                         else:
                             # check whether a compute handler exists
-                            if self._compute_handler is not None:
+                            if True:
                                 # otherwise, schedule a compute task
                                 label: str = (
                                     self._label_builder(obj)
```

Failed:
- `test_run_paths.TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing`

**L6** — every object treated as having available. Suite: `Ran 116 tests in 1.385s / FAILED (errors=5)`; tree restored: yes. Named test: `TestBlob.test_an_object_without_available_exits_to_the_post_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -341,7 +341,7 @@
                     self._num_lookup_complete += 1
 
                     # if the object has an 'available' attribute, we regard it as participating in the available/compute/store cycle
-                    if hasattr(obj, "available"):
+                    if True:
                         if obj.available:
                             # check whether an availability handler exists
                             if self._available_handler is not None:
```

Failed:
- `test_run_paths.TestBlob.test_an_object_without_available_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`

**A1** — exit 3 never taken. Suite: `Ran 116 tests in 1.667s / FAILED (failures=4)`; tree restored: yes. Named test: `TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -414,7 +414,7 @@
 
                     # this is the exit point for driver flow associated with this task, so apply the
                     # postprocessing task, if one was supplied
-                    if self._post_handler is not None:
+                    if False:
                         replacement_obj = self._post_handler(obj)
                         if replacement_obj is not None and self._store_results:
                             self.results[idx] = replacement_obj
```

Failed:
- `test_run_paths.TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`

**K1** — the store handler is not called. Suite: `Ran 116 tests in 1.621s / FAILED (failures=6)`; tree restored: yes. Named test: `TestComputeStoreValidate.test_a_completed_compute_runs_the_store_handler_then_the_persist_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -428,7 +428,7 @@
                     # call the store handler to resolve the Ray future and populate the object;
                     # the default simply calls obj.store(), but this can be overridden (e.g. to
                     # mint associated datastore objects before the persist step)
-                    self._store_handler(obj, self._pool)
+                    pass
 
                     # remove the original 'compute' task from the work queue
                     self._inflight.pop(ref.hex, None)
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`
- `test_construction.TestDefaultHandlers.test_the_default_store_handler_calls_store`
- `test_inherited_faults.TestInheritedFaults.test_fault_store_handler_none_with_compute_fails_at_first_compute`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_compute_runs_the_store_handler_then_the_persist_handler`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`

**S1** — an unavailable persisted object is not refused. Suite: `Ran 116 tests in 1.335s / FAILED (failures=1)`; tree restored: yes. Named test: `TestComputeStoreValidate.test_a_store_whose_object_is_not_available_raises`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -455,7 +455,7 @@
                     replacement_obj = ray.get(ref)
 
                     # replacement object should now satisfy the available attribute
-                    if not replacement_obj.available:
+                    if False:
                         raise RuntimeError(
                             "Object returned from store service does not satisfy the available property"
                         )
```

Failed:
- `test_run_paths.TestComputeStoreValidate.test_a_store_whose_object_is_not_available_raises`

**S2** — the persisted object does not replace the results entry. Suite: `Ran 116 tests in 1.243s / FAILED (failures=8, errors=1)`; tree restored: yes. Named test: `TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -460,7 +460,7 @@
                             "Object returned from store service does not satisfy the available property"
                         )
 
-                    if self._store_results:
+                    if False:
                         self.results[idx] = replacement_obj
 
                     # remove the original 'store' task from the work queue
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`
- `test_inherited_faults.TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_through_compute_and_store`

**S3** — the validation handler is never used. Suite: `Ran 116 tests in 1.098s / FAILED (failures=6, errors=1)`; tree restored: yes. Named test: `TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -471,7 +471,7 @@
                     self._num_store_complete += 1
 
                     # determine whether this work queue has a validation step
-                    if self._validation_handler is not None:
+                    if False:
                         validation_task: ObjectRef = self._validation_handler(
                             replacement_obj
                         )
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`

**S4** — exit 4 never taken. Suite: `Ran 116 tests in 1.934s / FAILED (failures=4, errors=1)`; tree restored: yes. Named test: `TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -486,7 +486,7 @@
 
                     # otherwise, this is the exit point for driver flow associated with this task, so apply the
                     # postprocessing task, if one was supplied
-                    elif self._post_handler is not None:
+                    elif False:
                         replacement_obj = self._post_handler(obj)
                         if replacement_obj is not None and self._store_results:
                             self.results[idx] = replacement_obj
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`

**V1** — the validation warning never printed. Suite: `Ran 116 tests in 1.582s / FAILED (failures=5)`; tree restored: yes. Named test: `TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -497,7 +497,7 @@
                     idx, obj = payload
 
                     result = ray.get(ref)
-                    if result is not True:
+                    if False:
                         print(
                             f"!! WARNING: {type(obj).__name__} object with store_id={obj.store_id} did not validate after being emplaced in the datastore"
                         )
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`

**V1b** — the validation warning on falsy results only. Suite: `Ran 116 tests in 1.829s / FAILED (failures=2)`; tree restored: yes. Named test: `TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -497,7 +497,7 @@
                     idx, obj = payload
 
                     result = ray.get(ref)
-                    if result is not True:
+                    if not result:
                         print(
                             f"!! WARNING: {type(obj).__name__} object with store_id={obj.store_id} did not validate after being emplaced in the datastore"
                         )
```

Failed:
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`

**V2** — exit 5 never taken. Suite: `Ran 116 tests in 1.570s / FAILED (failures=3, errors=5)`; tree restored: yes. Named test: `TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -510,7 +510,7 @@
 
                     # this is the exit point for driver flow associated with this task, so apply the
                     # postprocessing task, if one was supplied
-                    if self._post_handler is not None:
+                    if False:
                         replacement_obj = self._post_handler(obj)
                         if replacement_obj is not None and self._store_results:
                             self.results[idx] = replacement_obj
```

Failed:
- `test_run_paths.TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry`
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`

**P1-1** — exit 1: a None return replaces the entry. Suite: `Ran 116 tests in 3.182s / FAILED (failures=1, errors=2)`; tree restored: yes. Named test: `TestExits.test_a_returned_none_leaves_the_results_entry`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -360,7 +360,7 @@
                             # postprocessing task, if one was supplied
                             elif self._post_handler is not None:
                                 replacement_obj = self._post_handler(obj)
-                                if replacement_obj is not None and self._store_results:
+                                if self._store_results:
                                     self.results[idx] = replacement_obj
 
                         else:
```

Failed:
- `test_run_paths.TestAvailable.test_available_without_an_availability_handler_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_when_lookups_complete_in_reverse`

**P1-1b** — exit 1: a return replaces without store_results. Suite: `Ran 116 tests in 2.450s / FAILED (errors=1)`; tree restored: yes. Named test: `TestExits.test_a_returned_replacement_without_store_results_is_dropped`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -360,7 +360,7 @@
                             # postprocessing task, if one was supplied
                             elif self._post_handler is not None:
                                 replacement_obj = self._post_handler(obj)
-                                if replacement_obj is not None and self._store_results:
+                                if replacement_obj is not None:
                                     self.results[idx] = replacement_obj
 
                         else:
```

Failed:
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`

**P1-2** — exit 2: a None return replaces the entry. Suite: `Ran 116 tests in 1.788s / FAILED (failures=2)`; tree restored: yes. Named test: `TestExits.test_a_returned_none_leaves_the_results_entry`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -397,7 +397,7 @@
                         # this is the exit point, so apply the postprocessing task, if one was provided
                         if self._post_handler is not None:
                             replacement_obj = self._post_handler(obj)
-                            if replacement_obj is not None and self._store_results:
+                            if self._store_results:
                                 self.results[idx] = replacement_obj
 
                     self._compute_data.pop(ref.hex, None)
```

Failed:
- `test_run_paths.TestBlob.test_an_object_without_available_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`

**P1-2b** — exit 2: a return replaces without store_results. Suite: `Ran 116 tests in 1.616s / FAILED (errors=1)`; tree restored: yes. Named test: `TestExits.test_a_returned_replacement_without_store_results_is_dropped`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -397,7 +397,7 @@
                         # this is the exit point, so apply the postprocessing task, if one was provided
                         if self._post_handler is not None:
                             replacement_obj = self._post_handler(obj)
-                            if replacement_obj is not None and self._store_results:
+                            if replacement_obj is not None:
                                 self.results[idx] = replacement_obj
 
                     self._compute_data.pop(ref.hex, None)
```

Failed:
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`

**P1-3** — exit 3: a None return replaces the entry. Suite: `Ran 116 tests in 1.692s / FAILED (failures=1, errors=1)`; tree restored: yes. Named test: `TestExits.test_a_returned_none_leaves_the_results_entry`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -416,7 +416,7 @@
                     # postprocessing task, if one was supplied
                     if self._post_handler is not None:
                         replacement_obj = self._post_handler(obj)
-                        if replacement_obj is not None and self._store_results:
+                        if self._store_results:
                             self.results[idx] = replacement_obj
 
                 elif item_type == "compute":
```

Failed:
- `test_run_paths.TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`

**P1-3b** — exit 3: a return replaces without store_results. Suite: `Ran 116 tests in 1.304s / FAILED (errors=1)`; tree restored: yes. Named test: `TestExits.test_a_returned_replacement_without_store_results_is_dropped`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -416,7 +416,7 @@
                     # postprocessing task, if one was supplied
                     if self._post_handler is not None:
                         replacement_obj = self._post_handler(obj)
-                        if replacement_obj is not None and self._store_results:
+                        if replacement_obj is not None:
                             self.results[idx] = replacement_obj
 
                 elif item_type == "compute":
```

Failed:
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`

**P1-4** — exit 4: a None return replaces the entry. Suite: `Ran 116 tests in 2.018s / FAILED (errors=3)`; tree restored: yes. Named test: `TestExits.test_a_returned_none_leaves_the_results_entry`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -488,7 +488,7 @@
                     # postprocessing task, if one was supplied
                     elif self._post_handler is not None:
                         replacement_obj = self._post_handler(obj)
-                        if replacement_obj is not None and self._store_results:
+                        if self._store_results:
                             self.results[idx] = replacement_obj
 
                 elif item_type == "validate":
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_through_compute_and_store`

**P1-4b** — exit 4: a return replaces without store_results. Suite: `Ran 116 tests in 1.549s / FAILED (errors=1)`; tree restored: yes. Named test: `TestExits.test_a_returned_replacement_without_store_results_is_dropped`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -488,7 +488,7 @@
                     # postprocessing task, if one was supplied
                     elif self._post_handler is not None:
                         replacement_obj = self._post_handler(obj)
-                        if replacement_obj is not None and self._store_results:
+                        if replacement_obj is not None:
                             self.results[idx] = replacement_obj
 
                 elif item_type == "validate":
```

Failed:
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`

**P1-5** — exit 5: a None return replaces the entry. Suite: `Ran 116 tests in 1.685s / FAILED (failures=1, errors=1)`; tree restored: yes. Named test: `TestExits.test_a_returned_none_leaves_the_results_entry`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -512,7 +512,7 @@
                     # postprocessing task, if one was supplied
                     if self._post_handler is not None:
                         replacement_obj = self._post_handler(obj)
-                        if replacement_obj is not None and self._store_results:
+                        if self._store_results:
                             self.results[idx] = replacement_obj
 
                 else:
```

Failed:
- `test_run_paths.TestComputeStoreValidate.test_a_validation_handler_runs_a_validate_task_on_the_persisted_object`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry`

**P1-5b** — exit 5: a return replaces without store_results. Suite: `Ran 116 tests in 1.491s / FAILED (errors=1)`; tree restored: yes. Named test: `TestExits.test_a_returned_replacement_without_store_results_is_dropped`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -512,7 +512,7 @@
                     # postprocessing task, if one was supplied
                     if self._post_handler is not None:
                         replacement_obj = self._post_handler(obj)
-                        if replacement_obj is not None and self._store_results:
+                        if replacement_obj is not None:
                             self.results[idx] = replacement_obj
 
                 else:
```

Failed:
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped`

**P0-1** — exit 1 calls the absent post handler. Suite: `Ran 116 tests in 1.738s / FAILED (errors=21)`; tree restored: yes. Named test: `TestExits.test_each_exit_without_a_post_handler_calls_nothing`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -358,7 +358,7 @@
 
                             # otherwise, this is the exit point for driver flow associated with this task, so apply the
                             # postprocessing task, if one was supplied
-                            elif self._post_handler is not None:
+                            elif True:
                                 replacement_obj = self._post_handler(obj)
                                 if replacement_obj is not None and self._store_results:
                                     self.results[idx] = replacement_obj
```

Failed:
- `test_construction.TestResultsAndTitle.test_results_is_not_set_without_store_results`
- `test_construction.TestResultsAndTitle.test_total_time_is_set_only_with_a_title`
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_without_a_title`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`
- `test_run_paths.TestLookup.test_a_completed_lookup_puts_its_object_in_results`
- `test_run_paths.TestLookup.test_results_hold_what_get_returned_not_what_the_builder_minted`
- `test_scheduling.TestSizes.test_max_task_queue_holds_back_the_next_batch_until_the_queue_drains_below_it`
- `test_scheduling.TestSizes.test_one_builder_call_per_item`
- `test_scheduling.TestSizes.test_process_batch_size_sets_how_many_tasks_each_wait_returns`
- `test_scheduling.TestSizes.test_the_default_sizes_build_five_at_a_time_and_process_one_at_a_time`
- `test_task_builder.TestBatchCreation.test_a_batch_is_created_only_while_the_queue_has_room`
- `test_task_builder.TestBatchCreation.test_a_batch_makes_at_most_create_batch_size_builder_calls`
- `test_task_builder.TestBatchCreation.test_num_returns_is_the_smaller_of_process_batch_size_and_the_work_in_flight`
- `test_task_builder.TestSingleReturns.test_store_results_takes_a_result_index_per_single_return_in_task_order`

**P0-2** — exit 2 calls the absent post handler. Suite: `Ran 116 tests in 1.554s / FAILED (errors=1)`; tree restored: yes. Named test: `TestExits.test_each_exit_without_a_post_handler_calls_nothing`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -395,7 +395,7 @@
                     # and should be finalized
                     else:
                         # this is the exit point, so apply the postprocessing task, if one was provided
-                        if self._post_handler is not None:
+                        if True:
                             replacement_obj = self._post_handler(obj)
                             if replacement_obj is not None and self._store_results:
                                 self.results[idx] = replacement_obj
```

Failed:
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`

**P0-3** — exit 3 calls the absent post handler. Suite: `Ran 116 tests in 2.038s / FAILED (errors=2)`; tree restored: yes. Named test: `TestExits.test_each_exit_without_a_post_handler_calls_nothing`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -414,7 +414,7 @@
 
                     # this is the exit point for driver flow associated with this task, so apply the
                     # postprocessing task, if one was supplied
-                    if self._post_handler is not None:
+                    if True:
                         replacement_obj = self._post_handler(obj)
                         if replacement_obj is not None and self._store_results:
                             self.results[idx] = replacement_obj
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`

**P0-4** — exit 4 calls the absent post handler. Suite: `Ran 116 tests in 1.313s / FAILED (errors=15)`; tree restored: yes. Named test: `TestExits.test_each_exit_without_a_post_handler_calls_nothing`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -486,7 +486,7 @@
 
                     # otherwise, this is the exit point for driver flow associated with this task, so apply the
                     # postprocessing task, if one was supplied
-                    elif self._post_handler is not None:
+                    elif True:
                         replacement_obj = self._post_handler(obj)
                         if replacement_obj is not None and self._store_results:
                             self.results[idx] = replacement_obj
```

Failed:
- `test_construction.TestDefaultHandlers.test_the_default_compute_handler_calls_compute_with_the_arguments`
- `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool`
- `test_construction.TestDefaultHandlers.test_the_default_store_handler_calls_store`
- `test_construction.TestResultsAndTitle.test_no_title_prints_nothing`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_compute_runs_the_store_handler_then_the_persist_handler`
- `test_run_paths.TestComputeStoreValidate.test_a_completed_store_replaces_the_results_entry_with_the_persisted_object`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`
- `test_run_paths.TestNotAvailable.test_a_label_and_a_payload_are_passed_together`
- `test_run_paths.TestNotAvailable.test_a_label_builder_returning_none_passes_no_label`
- `test_run_paths.TestNotAvailable.test_a_label_from_the_label_builder_is_passed_as_label`
- `test_run_paths.TestNotAvailable.test_not_available_with_a_compute_handler_runs_a_compute_task`
- `test_scheduling.TestSizes.test_process_batch_size_applies_to_every_stage`
- `test_task_builder.TestSequenceReturns.test_a_sequence_element_carries_its_compute_payload`
- `test_task_builder.TestSingleReturns.test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler`
- `test_task_builder.TestSingleReturns.test_a_dict_without_a_compute_payload_passes_no_payload`

**P0-5** — exit 5 calls the absent post handler. Suite: `Ran 116 tests in 0.933s / FAILED (errors=4)`; tree restored: yes. Named test: `TestExits.test_each_exit_without_a_post_handler_calls_nothing`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -510,7 +510,7 @@
 
                     # this is the exit point for driver flow associated with this task, so apply the
                     # postprocessing task, if one was supplied
-                    if self._post_handler is not None:
+                    if True:
                         replacement_obj = self._post_handler(obj)
                         if replacement_obj is not None and self._store_results:
                             self.results[idx] = replacement_obj
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_true_prints_nothing`
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing`

**X1** — an unexpected item type is not refused. Suite: `Ran 116 tests in 1.377s / FAILED (failures=1)`; tree restored: yes. Named test: `TestUnexpectedItemType.test_an_unexpected_item_type_raises`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -516,7 +516,7 @@
                             self.results[idx] = replacement_obj
 
                 else:
-                    raise RuntimeError(f'Unexpected work queue item type "{item_type}"')
+                    pass
 
                 self._batch += 1
 
```

Failed:
- `test_run_paths.TestUnexpectedItemType.test_an_unexpected_item_type_raises`

**N1a** — progress printed without a title. Suite: `Ran 116 tests in 1.438s / FAILED (failures=1)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_no_progress_lines_without_a_title`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -524,7 +524,7 @@
             elapsed_since_last_notify = now_time - self._last_notify_time
             elapsed_since_start = now_time - self._start_time
             if (
-                self._title is not None
+                True
                 and elapsed_since_last_notify > self._notify_min_time_interval
             ):
                 if (
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_without_a_title`

**N1b** — the minimum interval ignored. Suite: `Ran 116 tests in 1.088s / FAILED (failures=1)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -525,7 +525,7 @@
             elapsed_since_start = now_time - self._start_time
             if (
                 self._title is not None
-                and elapsed_since_last_notify > self._notify_min_time_interval
+                and True
             ):
                 if (
                     elapsed_since_last_notify > self._notify_time_interval
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`

**N2a** — the notify time interval never triggers. Suite: `Ran 116 tests in 3.303s / FAILED (failures=7)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -528,7 +528,7 @@
                 and elapsed_since_last_notify > self._notify_min_time_interval
             ):
                 if (
-                    elapsed_since_last_notify > self._notify_time_interval
+                    False
                     or self._batch > self._notify_batch_size
                 ):
                     num_items_remain = len(self._todo)
```

Failed:
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**N2b** — the notify batch size never triggers. Suite: `Ran 116 tests in 1.810s / FAILED (failures=1)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -529,7 +529,7 @@
             ):
                 if (
                     elapsed_since_last_notify > self._notify_time_interval
-                    or self._batch > self._notify_batch_size
+                    or False
                 ):
                     num_items_remain = len(self._todo)
                     if num_items_remain == 0:
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`

**N3** — the percentage always 100. Suite: `Ran 116 tests in 1.816s / FAILED (failures=2)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -532,7 +532,7 @@
                     or self._batch > self._notify_batch_size
                 ):
                     num_items_remain = len(self._todo)
-                    if num_items_remain == 0:
+                    if True:
                         percent_complete = 100.0
                     else:
                         percent_complete = (
```

Failed:
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**N4** — the suffix never printed. Suite: `Ran 116 tests in 1.660s / FAILED (failures=7)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -543,7 +543,7 @@
 
                     now = datetime.now()
                     msg = f"   -- {now:%Y-%m-%d %H:%M:%S%z} ({format_time(elapsed_since_start)} running): {len(self._todo)}/{self._num_total_items} work items remaining = {percent_complete:.2f}% complete"
-                    if percent_complete > 99.99:
+                    if False:
                         msg += " (may be waiting for compute/store/validate tasks to finish)"
                     print(msg)
 
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**N5** — the last lookup count never moves on. Suite: `Ran 116 tests in 1.680s / FAILED (failures=5)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -554,7 +554,7 @@
                     self._batch = 0
                     self._last_notify_time = time.perf_counter()
 
-                    self._last_num_lookup_complete = self._num_lookup_complete
+                    pass
                     self._last_num_compute_complete = self._num_compute_complete
                     self._last_num_store_complete = self._num_store_complete
                     self._last_num_available_complete = self._num_available_complete
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**F1** — no completion lines or total_time. Suite: `Ran 116 tests in 2.020s / FAILED (failures=11)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -560,7 +560,7 @@
                     self._last_num_available_complete = self._num_available_complete
                     self._last_num_validation_complete = self._num_validation_complete
 
-        if self._title is not None:
+        if False:
             final_time = time.perf_counter()
             self.total_time = final_time - self._start_time
             print(
```

Failed:
- `test_construction.TestResultsAndTitle.test_total_time_is_set_only_with_a_title`
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`

**F2** — the no-compute line never printed. Suite: `Ran 116 tests in 1.942s / FAILED (failures=7)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -569,7 +569,7 @@
             print(
                 f"      Queue summary: {self._build_completed_status_message(total_time_in_seconds=self.total_time)}"
             )
-            if self._num_compute_complete == 0:
+            if False:
                 print(
                     "      (no compute items were evaluated - all assets read from datastore)"
                 )
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**F2b** — the no-compute line always printed. Suite: `Ran 116 tests in 1.524s / FAILED (failures=2)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -569,7 +569,7 @@
             print(
                 f"      Queue summary: {self._build_completed_status_message(total_time_in_seconds=self.total_time)}"
             )
-            if self._num_compute_complete == 0:
+            if True:
                 print(
                     "      (no compute items were evaluated - all assets read from datastore)"
                 )
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`

**Q1a** — queued: no compute segment. Suite: `Ran 116 tests in 1.325s / FAILED (failures=3)`; tree restored: yes. Named test: `TestStatusMessages.test_the_queued_message_has_a_segment_per_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -167,7 +167,7 @@
 
     def _build_queued_status_message(self):
         msg = f"{self._num_lookup_queue} lookup"
-        if self._compute_handler is not None:
+        if False:
             msg += f", {self._num_compute_queue} compute"
 
         if self._persist_handler is not None:
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestStatusMessages.test_the_queued_message_has_a_segment_per_handler`

**Q1b** — queued: no store segment. Suite: `Ran 116 tests in 1.688s / FAILED (failures=3)`; tree restored: yes. Named test: `TestStatusMessages.test_the_queued_message_has_a_segment_per_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -170,7 +170,7 @@
         if self._compute_handler is not None:
             msg += f", {self._num_compute_queue} compute"
 
-        if self._persist_handler is not None:
+        if False:
             msg += f", {self._num_store_queue} store"
 
         if self._available_handler is not None:
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestStatusMessages.test_the_queued_message_has_a_segment_per_handler`

**Q1c** — queued: no available segment. Suite: `Ran 116 tests in 1.592s / FAILED (failures=3)`; tree restored: yes. Named test: `TestStatusMessages.test_the_queued_message_has_a_segment_per_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -173,7 +173,7 @@
         if self._persist_handler is not None:
             msg += f", {self._num_store_queue} store"
 
-        if self._available_handler is not None:
+        if False:
             msg += f", {self._num_available_queue} available"
 
         if self._validation_handler is not None:
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestStatusMessages.test_the_queued_message_has_a_segment_per_handler`

**Q1d** — queued: no validation segment. Suite: `Ran 116 tests in 2.513s / FAILED (failures=3)`; tree restored: yes. Named test: `TestStatusMessages.test_the_queued_message_has_a_segment_per_handler`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -176,7 +176,7 @@
         if self._available_handler is not None:
             msg += f", {self._num_available_queue} available"
 
-        if self._validation_handler is not None:
+        if False:
             msg += f", {self._num_validation_queue} validation"
 
         return msg
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestStatusMessages.test_the_queued_message_has_a_segment_per_handler`

**Q2a** — completed: no compute segment. Suite: `Ran 116 tests in 2.015s / FAILED (failures=6)`; tree restored: yes. Named test: `TestStatusMessages.test_the_completed_message_without_rates`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -196,7 +196,7 @@
         if len(submsg) > 0:
             msg += f" ({submsg})"
 
-        if self._compute_handler is not None:
+        if False:
             msg += f", {self._num_compute_complete} compute"
             submsg = _format_rates(
                 since_last_notify_in_seconds,
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_with_rates`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_without_rates`

**Q2b** — completed: no store segment. Suite: `Ran 116 tests in 2.196s / FAILED (failures=6)`; tree restored: yes. Named test: `TestStatusMessages.test_the_completed_message_without_rates`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -207,7 +207,7 @@
             if len(submsg) > 0:
                 msg += f" ({submsg})"
 
-        if self._persist_handler is not None:
+        if False:
             msg += f", {self._num_store_complete} store"
             submsg = _format_rates(
                 since_last_notify_in_seconds,
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_with_rates`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_without_rates`

**Q2c** — completed: no available segment. Suite: `Ran 116 tests in 1.997s / FAILED (failures=5)`; tree restored: yes. Named test: `TestStatusMessages.test_the_completed_message_without_rates`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -218,7 +218,7 @@
             if len(submsg) > 0:
                 msg += f" ({submsg})"
 
-        if self._available_handler is not None:
+        if False:
             msg += f", {self._num_available_complete} available"
             submsg = _format_rates(
                 since_last_notify_in_seconds,
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_with_rates`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_without_rates`

**Q2d** — completed: no validation segment. Suite: `Ran 116 tests in 2.857s / FAILED (failures=6)`; tree restored: yes. Named test: `TestStatusMessages.test_the_completed_message_without_rates`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -229,7 +229,7 @@
             if len(submsg) > 0:
                 msg += f" ({submsg})"
 
-        if self._validation_handler is not None:
+        if False:
             msg += f", {self._num_validation_complete} validation"
             submsg = _format_rates(
                 since_last_notify_in_seconds,
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_with_rates`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_without_rates`

**Q2e** — completed: parentheses even with no rates. Suite: `Ran 116 tests in 1.929s / FAILED (failures=5)`; tree restored: yes. Named test: `TestStatusMessages.test_the_completed_message_without_rates`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -193,7 +193,7 @@
             self._num_lookup_complete,
             self._last_num_lookup_complete,
         )
-        if len(submsg) > 0:
+        if True:
             msg += f" ({submsg})"
 
         if self._compute_handler is not None:
```

Failed:
- `test_printed_lines.TestStatusMessages.test_the_completed_message_without_rates`

**T1** — _readable_rate always /sec. Suite: `Ran 116 tests in 1.708s / FAILED (failures=19)`; tree restored: yes. Named test: `TestPureFunctions.test_readable_rate_units`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -25,7 +25,7 @@
         ("hr", 24),
         ("day", None),
     ]:
-        if current_rate >= 10 or multiplier is None:
+        if True:
             return f"{current_rate:.4g}/{unit}"
 
         current_rate = current_rate * multiplier
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_printed_lines.TestPureFunctions.test_format_rates`
- `test_printed_lines.TestPureFunctions.test_readable_rate_units`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_with_rates`

**T2a** — _format_rates never gives the interval rate. Suite: `Ran 116 tests in 2.229s / FAILED (failures=6)`; tree restored: yes. Named test: `TestPureFunctions.test_format_rates`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -42,7 +42,7 @@
     assert current_value is not None
 
     msg = ""
-    if time_delta_in_seconds is not None and last_value is not None:
+    if False:
         current_rate_per_second = (current_value - last_value) / time_delta_in_seconds
         msg += _readable_rate(current_rate_per_second)
 
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestPureFunctions.test_format_rates`

**T2b** — _format_rates never gives the average. Suite: `Ran 116 tests in 2.123s / FAILED (failures=15)`; tree restored: yes. Named test: `TestPureFunctions.test_format_rates`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -46,7 +46,7 @@
         current_rate_per_second = (current_value - last_value) / time_delta_in_seconds
         msg += _readable_rate(current_rate_per_second)
 
-    if total_time_in_seconds is not None:
+    if False:
         avg_rate_per_second = current_value / total_time_in_seconds
         msg += (
             (", " if len(msg) > 0 else "")
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_printed_lines.TestPureFunctions.test_format_rates`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_with_rates`

**T2c** — _format_rates' interval rate without a last value. Suite: `Ran 116 tests in 2.051s / FAILED (errors=14)`; tree restored: yes. Named test: `TestPureFunctions.test_format_rates`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -42,7 +42,7 @@
     assert current_value is not None
 
     msg = ""
-    if time_delta_in_seconds is not None and last_value is not None:
+    if time_delta_in_seconds is not None:
         current_rate_per_second = (current_value - last_value) / time_delta_in_seconds
         msg += _readable_rate(current_rate_per_second)
 
```

Failed:
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestPureFunctions.test_format_rates`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_with_rates`


### 5.2 (m1)–(m5)

- **(m1)** fails `test_fault_in_flight_work_is_keyed_on_a_bound_method` **and nothing else**. With
  `.hex()` the keys are strings, so `fresh_refs`' equal-but-distinct refs find their entries and
  the run completes. (X1's seed is keyed both ways, deviation 12, so it does not move.)
- **(m2)** fails the fault-2 test and S4's identity test (§6.6).
- **(m3)** fails the fault-3 test alone.
- **(m4)**: each of the nine literals fails `test_a_lookup_only_run_notifying_on_every_pass`
  (`:166`, `:545`, `:547`, `:550`, `:551`, `:567`, `:570`, `:574`) or
  `test_the_validation_warning_among_the_titled_lines` (`:502`), and the other whole-line tests
  that print it.
- **(m5)** fails `test_the_available_rate_is_per_interval` alone.


**m1** — every .hex key -> .hex(). Suite: `Ran 116 tests in 3.310s / FAILED (failures=1)`; tree restored: yes. Named test: `TestInheritedFaults.test_fault_in_flight_work_is_keyed_on_a_bound_method`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -257,13 +257,13 @@
                     ref_data = self._task_builder(item)
 
                     def store_single_ref(ref, allow_store=True):
-                        self._inflight[ref.hex] = ref
+                        self._inflight[ref.hex()] = ref
 
                         if self._store_results and allow_store:
-                            self._data[ref.hex] = ("lookup", self._current_idx)
+                            self._data[ref.hex()] = ("lookup", self._current_idx)
                             self._current_idx += 1
                         else:
-                            self._data[ref.hex] = ("lookup", None)
+                            self._data[ref.hex()] = ("lookup", None)
 
                         self._num_lookup_queue += 1
 
@@ -274,7 +274,7 @@
                             store_single_ref(ref, allow_store=allow_store)
 
                             if "compute_payload" in ref_data:
-                                self._compute_data[ref.hex] = ref_data[
+                                self._compute_data[ref.hex()] = ref_data[
                                     "compute_payload"
                                 ]
 
@@ -319,7 +319,7 @@
 
             for ref in done_refs:
                 ref: ObjectRef
-                item_type, payload = self._data[ref.hex]
+                item_type, payload = self._data[ref.hex()]
 
                 if item_type == "lookup":
                     # payload is an index into the result set
@@ -334,8 +334,8 @@
                         self.results[idx] = obj
 
                     # remove the original 'lookup' task from the work queue
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_lookup_queue = max(self._num_lookup_queue - 1, 0)
                     self._num_lookup_complete += 1
@@ -348,8 +348,8 @@
                                 available_task: ObjectRef = self._available_handler(obj)
 
                                 # add this task to the work queue
-                                self._inflight[available_task.hex] = available_task
-                                self._data[available_task.hex] = (
+                                self._inflight[available_task.hex()] = available_task
+                                self._data[available_task.hex()] = (
                                     "available",
                                     (idx, obj),
                                 )
@@ -376,9 +376,9 @@
                                     {"label": label} if label is not None else {}
                                 )
 
-                                if ref.hex in self._compute_data:
+                                if ref.hex() in self._compute_data:
                                     compute_args.update(
-                                        {"payload": self._compute_data[ref.hex]}
+                                        {"payload": self._compute_data[ref.hex()]}
                                     )
 
                                 compute_task: ObjectRef = self._compute_handler(
@@ -386,8 +386,8 @@
                                 )
 
                                 # add this compute task to the work queue
-                                self._inflight[compute_task.hex] = compute_task
-                                self._data[compute_task.hex] = ("compute", (idx, obj))
+                                self._inflight[compute_task.hex()] = compute_task
+                                self._data[compute_task.hex()] = ("compute", (idx, obj))
 
                                 self._num_compute_queue += 1
 
@@ -400,14 +400,14 @@
                             if replacement_obj is not None and self._store_results:
                                 self.results[idx] = replacement_obj
 
-                    self._compute_data.pop(ref.hex, None)
+                    self._compute_data.pop(ref.hex(), None)
 
                 elif item_type == "available":
                     # payload is a pair of the target index and the constructed object
                     idx, obj = payload
 
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_available_queue = max(self._num_available_queue - 1, 0)
                     self._num_available_complete += 1
@@ -431,8 +431,8 @@
                     self._store_handler(obj, self._pool)
 
                     # remove the original 'compute' task from the work queue
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_compute_queue = max(self._num_compute_queue - 1, 0)
                     self._num_compute_complete += 1
@@ -441,8 +441,8 @@
                     store_task: ObjectRef = self._persist_handler(obj, self._pool)
 
                     # add this store task to the work queue
-                    self._inflight[store_task.hex] = store_task
-                    self._data[store_task.hex] = ("store", payload)
+                    self._inflight[store_task.hex()] = store_task
+                    self._data[store_task.hex()] = ("store", payload)
 
                     self._num_store_queue += 1
 
@@ -464,8 +464,8 @@
                         self.results[idx] = replacement_obj
 
                     # remove the original 'store' task from the work queue
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_store_queue = max(self._num_store_queue - 1, 0)
                     self._num_store_complete += 1
@@ -476,8 +476,8 @@
                             replacement_obj
                         )
 
-                        self._inflight[validation_task.hex] = validation_task
-                        self._data[validation_task.hex] = (
+                        self._inflight[validation_task.hex()] = validation_task
+                        self._data[validation_task.hex()] = (
                             "validate",
                             (idx, replacement_obj),
                         )
@@ -502,8 +502,8 @@
                             f"!! WARNING: {type(obj).__name__} object with store_id={obj.store_id} did not validate after being emplaced in the datastore"
                         )
 
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_validation_queue = max(self._num_validation_queue - 1, 0)
                     self._num_validation_complete += 1
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_fault_in_flight_work_is_keyed_on_a_bound_method`

**m2** — exit 4 given the persisted object. Suite: `Ran 116 tests in 1.850s / FAILED (failures=2)`; tree restored: yes. Named test: `TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -487,7 +487,7 @@
                     # otherwise, this is the exit point for driver flow associated with this task, so apply the
                     # postprocessing task, if one was supplied
                     elif self._post_handler is not None:
-                        replacement_obj = self._post_handler(obj)
+                        replacement_obj = self._post_handler(replacement_obj)
                         if replacement_obj is not None and self._store_results:
                             self.results[idx] = replacement_obj
 
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`

**m3** — results sized from the counted list. Suite: `Ran 116 tests in 1.854s / FAILED (failures=1)`; tree restored: yes. Named test: `TestInheritedFaults.test_fault_store_results_sizes_from_len_of_the_task_list`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -135,7 +135,7 @@
 
         self._store_results = store_results
         if store_results:
-            self.results = [None for _ in range(len(task_list))]
+            self.results = [None for _ in range(self._num_total_items)]
             self._current_idx = 0
 
         self._num_lookup_queue = 0
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_fault_store_results_sizes_from_len_of_the_task_list`

**m4-166** — banner literal. Suite: `Ran 116 tests in 2.000s / FAILED (failures=11)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -163,7 +163,7 @@
 
         self._title = title
         if title is not None:
-            print(f"\n** {title}")
+            print(f"\n*- {title}")
 
     def _build_queued_status_message(self):
         msg = f"{self._num_lookup_queue} lookup"
```

Failed:
- `test_construction.TestResultsAndTitle.test_a_title_prints_the_banner_at_construction`
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`

**m4-545** — progress literal. Suite: `Ran 116 tests in 1.873s / FAILED (failures=7)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -542,7 +542,7 @@
                         )
 
                     now = datetime.now()
-                    msg = f"   -- {now:%Y-%m-%d %H:%M:%S%z} ({format_time(elapsed_since_start)} running): {len(self._todo)}/{self._num_total_items} work items remaining = {percent_complete:.2f}% complete"
+                    msg = f"   -- {now:%Y-%m-%d %H:%M:%S%z} ({format_time(elapsed_since_start)} runninG): {len(self._todo)}/{self._num_total_items} work items remaining = {percent_complete:.2f}% complete"
                     if percent_complete > 99.99:
                         msg += " (may be waiting for compute/store/validate tasks to finish)"
                     print(msg)
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**m4-547** — suffix literal. Suite: `Ran 116 tests in 2.038s / FAILED (failures=7)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -544,7 +544,7 @@
                     now = datetime.now()
                     msg = f"   -- {now:%Y-%m-%d %H:%M:%S%z} ({format_time(elapsed_since_start)} running): {len(self._todo)}/{self._num_total_items} work items remaining = {percent_complete:.2f}% complete"
                     if percent_complete > 99.99:
-                        msg += " (may be waiting for compute/store/validate tasks to finish)"
+                        msg += " (may be waitinG for compute/store/validate tasks to finish)"
                     print(msg)
 
                     msg = f"      inflight: {self._build_queued_status_message()}"
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**m4-550** — inflight literal. Suite: `Ran 116 tests in 1.750s / FAILED (failures=7)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -547,7 +547,7 @@
                         msg += " (may be waiting for compute/store/validate tasks to finish)"
                     print(msg)
 
-                    msg = f"      inflight: {self._build_queued_status_message()}"
+                    msg = f"      inflighT: {self._build_queued_status_message()}"
                     msg += f" | completed: {self._build_completed_status_message(total_time_in_seconds=elapsed_since_start, since_last_notify_in_seconds=elapsed_since_last_notify)}"
                     print(msg)
 
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**m4-551** — completed literal. Suite: `Ran 116 tests in 2.184s / FAILED (failures=7)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -548,7 +548,7 @@
                     print(msg)
 
                     msg = f"      inflight: {self._build_queued_status_message()}"
-                    msg += f" | completed: {self._build_completed_status_message(total_time_in_seconds=elapsed_since_start, since_last_notify_in_seconds=elapsed_since_last_notify)}"
+                    msg += f" | completeD: {self._build_completed_status_message(total_time_in_seconds=elapsed_since_start, since_last_notify_in_seconds=elapsed_since_last_notify)}"
                     print(msg)
 
                     self._batch = 0
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**m4-567** — completion literal. Suite: `Ran 116 tests in 1.464s / FAILED (failures=10)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -564,7 +564,7 @@
             final_time = time.perf_counter()
             self.total_time = final_time - self._start_time
             print(
-                f"   -- ALL WORK ITEMS COMPLETE in time {format_time(self.total_time)}"
+                f"   -- ALL WORK ITEMS COMPLETE in tima {format_time(self.total_time)}"
             )
             print(
                 f"      Queue summary: {self._build_completed_status_message(total_time_in_seconds=self.total_time)}"
```

Failed:
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`

**m4-570** — summary literal. Suite: `Ran 116 tests in 2.445s / FAILED (failures=9)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -567,7 +567,7 @@
                 f"   -- ALL WORK ITEMS COMPLETE in time {format_time(self.total_time)}"
             )
             print(
-                f"      Queue summary: {self._build_completed_status_message(total_time_in_seconds=self.total_time)}"
+                f"      Queue summarY: {self._build_completed_status_message(total_time_in_seconds=self.total_time)}"
             )
             if self._num_compute_complete == 0:
                 print(
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`

**m4-574** — no-compute literal. Suite: `Ran 116 tests in 1.352s / FAILED (failures=7)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -571,5 +571,5 @@
             )
             if self._num_compute_complete == 0:
                 print(
-                    "      (no compute items were evaluated - all assets read from datastore)"
+                    "      (No compute items were evaluated - all assets read from datastore)"
                 )
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`

**m4-502** — warning literal. Suite: `Ran 116 tests in 2.114s / FAILED (failures=5)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -499,7 +499,7 @@
                     result = ray.get(ref)
                     if result is not True:
                         print(
-                            f"!! WARNING: {type(obj).__name__} object with store_id={obj.store_id} did not validate after being emplaced in the datastore"
+                            f"!! WARNINg: {type(obj).__name__} object with store_id={obj.store_id} did not validate after being emplaced in the datastore"
                         )
 
                     self._inflight.pop(ref.hex, None)
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_the_validation_warning_among_the_titled_lines`
- `test_run_paths.TestComputeStoreValidate.test_a_validation_that_is_not_true_prints_the_warning`

**m5** — available rate from the store count (CPBH/SI). Suite: `Ran 116 tests in 3.474s / FAILED (failures=1)`; tree restored: yes. Named test: `TestProgressAndCompletion.test_the_available_rate_is_per_interval`, failed.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -557,7 +557,7 @@
                     self._last_num_lookup_complete = self._num_lookup_complete
                     self._last_num_compute_complete = self._num_compute_complete
                     self._last_num_store_complete = self._num_store_complete
-                    self._last_num_available_complete = self._num_available_complete
+                    self._last_num_available_complete = self._num_store_complete
                     self._last_num_validation_complete = self._num_validation_complete
 
         if self._title is not None:
```

Failed:
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`


### 5.3 Equivalent mutations, which survive

Recorded so that 04's author knows what no test pins (§4's Z2–Z5). Each suite run is `OK`.


**E1** — the five max(..., 0) clamps removed. Suite: `Ran 116 tests in 2.048s / OK`; tree restored: yes.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -337,7 +337,7 @@
                     self._inflight.pop(ref.hex, None)
                     self._data.pop(ref.hex, None)
 
-                    self._num_lookup_queue = max(self._num_lookup_queue - 1, 0)
+                    self._num_lookup_queue = self._num_lookup_queue - 1
                     self._num_lookup_complete += 1
 
                     # if the object has an 'available' attribute, we regard it as participating in the available/compute/store cycle
@@ -409,7 +409,7 @@
                     self._inflight.pop(ref.hex, None)
                     self._data.pop(ref.hex, None)
 
-                    self._num_available_queue = max(self._num_available_queue - 1, 0)
+                    self._num_available_queue = self._num_available_queue - 1
                     self._num_available_complete += 1
 
                     # this is the exit point for driver flow associated with this task, so apply the
@@ -434,7 +434,7 @@
                     self._inflight.pop(ref.hex, None)
                     self._data.pop(ref.hex, None)
 
-                    self._num_compute_queue = max(self._num_compute_queue - 1, 0)
+                    self._num_compute_queue = self._num_compute_queue - 1
                     self._num_compute_complete += 1
 
                     # a compute handler was supplied, so a persist handler must have been also
@@ -467,7 +467,7 @@
                     self._inflight.pop(ref.hex, None)
                     self._data.pop(ref.hex, None)
 
-                    self._num_store_queue = max(self._num_store_queue - 1, 0)
+                    self._num_store_queue = self._num_store_queue - 1
                     self._num_store_complete += 1
 
                     # determine whether this work queue has a validation step
@@ -505,7 +505,7 @@
                     self._inflight.pop(ref.hex, None)
                     self._data.pop(ref.hex, None)
 
-                    self._num_validation_queue = max(self._num_validation_queue - 1, 0)
+                    self._num_validation_queue = self._num_validation_queue - 1
                     self._num_validation_complete += 1
 
                     # this is the exit point for driver flow associated with this task, so apply the
```

Failed: nothing (survives).

**E2** — 'and allow_store' removed. Suite: `Ran 116 tests in 1.561s / OK`; tree restored: yes.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -259,7 +259,7 @@
                     def store_single_ref(ref, allow_store=True):
                         self._inflight[ref.hex] = ref
 
-                        if self._store_results and allow_store:
+                        if self._store_results:
                             self._data[ref.hex] = ("lookup", self._current_idx)
                             self._current_idx += 1
                         else:
```

Failed: nothing (survives).

**E3** — ':250 and len(self._todo) > 0' removed. Suite: `Ran 116 tests in 2.371s / OK`; tree restored: yes.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -247,7 +247,7 @@
             # if there is space in the task queue, and there are items remaining to queue,
             # then initiate new work
             # either we create a fixed batch size, or we enqueue work until the task queue is exhasuted
-            if len(self._inflight) < self._max_task_queue and len(self._todo) > 0:
+            if len(self._inflight) < self._max_task_queue:
                 count = 0
                 while count < self._create_batch_size and len(self._todo) > 0:
                     # consume more tasks from the task queue and schedule their work
```

Failed: nothing (survives).

**E4** — the compute payload is not popped. Suite: `Ran 116 tests in 1.407s / OK`; tree restored: yes.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -400,7 +400,7 @@
                             if replacement_obj is not None and self._store_results:
                                 self.results[idx] = replacement_obj
 
-                    self._compute_data.pop(ref.hex, None)
+                    pass
 
                 elif item_type == "available":
                     # payload is a pair of the target index and the constructed object
```

Failed: nothing (survives).


### 5.4 The stand-ins bite: (s1)–(s3)


**st-s1** — wait without the empty-list clause. Suite: `Ran 116 tests in 2.745s / FAILED (errors=5)`; tree restored: yes.

```diff
diff --git a/raypoolkit/tests/standins.py b/raypoolkit/tests/standins.py
--- a/raypoolkit/tests/standins.py
+++ b/raypoolkit/tests/standins.py
@@ -162,8 +162,6 @@
                 raise TypeError(
                     f"wait() expected a list of ray.ObjectRef, got list containing {type(ref)}"
                 )
-        if len(refs) == 0:
-            return [], []
         if len(refs) != len(set(refs)):
             raise ValueError("Wait requires a list of unique ray_waitables.")
         if num_returns <= 0:
```

Failed:
- `test_standins.TestWaitContract.test_an_empty_list_returns_two_empty_lists_before_num_returns_is_checked`
- `test_standins.TestWaitContract.test_each_call_is_recorded`
- `test_standins.TestWaitContract.test_wait_raises_past_its_call_cap`
- `test_task_builder.TestNoneReturns.test_none_from_every_builder_enqueues_nothing_and_waits_on_nothing`
- `test_task_builder.TestSequenceReturns.test_an_empty_sequence_enqueues_nothing`

**st-s2** — get returns the stored object itself. Suite: `Ran 116 tests in 2.527s / FAILED (failures=2)`; tree restored: yes.

```diff
diff --git a/raypoolkit/tests/standins.py b/raypoolkit/tests/standins.py
--- a/raypoolkit/tests/standins.py
+++ b/raypoolkit/tests/standins.py
@@ -199,7 +199,7 @@
                 f"StandinRay.get: ref {ref.hex()} was not minted by this stand-in"
             )
         # by value, as Ray returns a deserialized copy
-        return pickle.loads(pickle.dumps(self._table[binary]))
+        return self._table[binary]
 
     def namespace(self):
         """What replaces the pool module's ``ray``: ``wait`` and ``get``, and nothing else."""
```

Failed:
- `test_run_paths.TestLookup.test_results_hold_what_get_returned_not_what_the_builder_minted`
- `test_standins.TestGet.test_get_returns_the_value_by_value`

(s1) fails the all-`None` builder test,
`test_none_from_every_builder_enqueues_nothing_and_waits_on_nothing`, with Ray's
`ValueError: Invalid number of objects to return 0.`, as the prompt expects. (s2) fails the
stand-in's own by-value test and a pool test that depends on by-value semantics
(`test_results_hold_what_get_returned_not_what_the_builder_minted`), so no §3 issue is opened.

**st-s3** — `PoolTestCase` not patching `ray.init`. **Not run** (prompt §3.4). `git apply --check`
passes; applied with no suite run, `git apply -R --check` passes, and it was reverted at once.

```diff
diff --git a/raypoolkit/tests/standins.py b/raypoolkit/tests/standins.py
--- a/raypoolkit/tests/standins.py
+++ b/raypoolkit/tests/standins.py
@@ -351,7 +351,6 @@
             (RAY_TARGET, self.ray.namespace()),
             (TIME_TARGET, self.clock.time_namespace()),
             (DATETIME_TARGET, self.clock.datetime_namespace()),
-            (RAY_INIT_TARGET, refuse_ray_init),
         ):
             patcher = mock.patch(target, replacement)
             patcher.start()
```

**By reading, the test that would start Ray** is
`test_standins.TestRayInitGuard.test_real_get_and_wait_reach_the_refused_ray_init`, at its first
`ray.get(ref)`. It is the only test that calls the real `ray.get` or `ray.wait`: a search of
`raypoolkit/tests/` for `ray.<name>(` outside `self.ray.` finds only its three calls and
`ray.is_initialized()`, which Ray does not wrap. Ray wraps `get` and `wait` (its `AUTO_INIT_APIS`,
`ray/__init__.py:211-220`) with `auto_init_ray`, which calls `ray.init()` through the module
attribute (`ray/_private/auto_init_hook.py:10-14`). Without the patch that is the real
`ray.init()`, which starts a local cluster; the `ray.get` would then wait on a ref no worker
produced, so the test would hang as well, and the tear-down would find `ray.is_initialized()`
true. No other test reaches real Ray even without the patch: the pool module's `ray` is still the
stand-in's namespace, and the other `ray` names the tests use (`ray.ObjectRef`,
`ray.is_initialized`) do not initialise Ray.

## 6. Observations not acted on

1. **A pool with a size below 1 never finishes, or raises Ray's error.** `max_task_queue=0` or
   `create_batch_size=0` leaves `_todo` full and `_inflight` empty, so every pass calls
   `ray.wait([], num_returns=0)` and the loop at `:246` never ends (the orchestrator's
   measurement; the spin cap would end it in the suite, and no test builds such a pool).
   `process_batch_size=0` makes `num_returns` 0 with work in flight, which Ray refuses with
   `ValueError`. The constructor checks none of the three. Recorded at the orchestrator's
   direction as an observation, not pinned; **no issue opened**. Whether it deserves one (04, with
   U8's constructor checks) is the orchestrator's call.
2. **Four equivalent mutations survive** (§5.3): the five `max(…, 0)` clamps (Z2), `:262`'s
   `and allow_store` (Z3), `:250`'s `and len(self._todo) > 0` (Z4) and `:403`'s
   `_compute_data.pop` (Z5). Each is redundant or unobservable through the public interface, not a
   defect; no issue opened. 04 may simplify them, and no test will notice.
3. **The progress line counts items whose task has not been built**, not items not yet complete:
   a pool whose items are all built in the first batch prints `0/T … = 100.00% complete` with the
   "(may be waiting …)" suffix while every task is still in flight. Pinned as it behaves (N3, N4);
   the suffix is the module's own account of it. Not a fault; no issue.
4. **The no-compute line says "all assets read from datastore"** whenever no compute completed,
   including for a pool with no compute handler, or one whose objects were all blobs. It is a
   printed line, pinned word for word (F2); its wording is part of the interface. No issue.
5. **(m1) moves nothing but the fault-1 test** (§5.2). 04's change of the keys will fail
   `test_fault_in_flight_work_is_keyed_on_a_bound_method` alone, which 04 inverts. X1's seed is
   keyed both ways (deviation 12), so 04 need not touch it unless it keys on the ref itself, in
   which case X1's seed needs a third key.
6. **(m2) moves two tests**: the fault-2 test and
   `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`,
   which pins that exit 4 is given the object the compute ran on. 04 inverts both. (m3) moves the
   fault-3 test alone.
7. **`ScriptedClock.stamp()`** is used only by the stand-in's own test; the printed-line tests
   build their stamps from the reading directly, so that each expected line is readable as
   written.

## 7. Issues

**Opened:** none. **Closed:** none. **Changed:** each of the five `[00-…]` entries on the board
gains a dated line saying which test pins it (fault 5: `test_construction.py`'s message
assertions). (s2) fails two tests, so the §3 issue the prompt provides for does not arise. The
index stays at **6** open; `docs/OPEN_ISSUES.md` is unchanged.

## 8. State handed to the next prompt

- `HEAD` is this commit. `raypoolkit/RayWorkPool.py` is unchanged since `49f3ddf`.
- **Suite: 116 tests**, all passing, in about 2–5 s at Python 3.12.15 / Ray 2.43.0, with no Ray
  cluster. 03 runs it at both ends of U7's range. The stand-ins import only `ray`, `raypoolkit` and
  the standard library, and use `ray.ObjectRef(bytes)`, `ray.is_initialized()` and the auto-init
  hook's `ray.init` lookup, each measured at 2.43.0 only here (the planner read the `wait`
  contract at 2.53.0 and 2.55.1 too).
- **The stand-ins' entry points** are §1.1's. A test that runs a pool subclasses `PoolTestCase`.
- **For 04**: the five fault tests are `test_inherited_faults.TestInheritedFaults.test_fault_*`;
  fault 5 is `test_construction.py`'s `COMPUTE_WITHOUT_PERSIST` and `PERSIST_WITHOUT_COMPUTE`. What
  each of 04's changes moves is in §5.2 ((m1), (m2), (m3)) and §6. The printed lines are pinned in
  `test_printed_lines.py`; 04 changes none of them (README §5 rule 7).
- The mutation driver is not committed. Every diff it applied is in §5, exactly as applied.
- `./venv/bin/python docs/extraction/compare_with_source.py` exits 0 with 12 declared files. A
  prompt that adds a file under `raypoolkit/` declares it in `NO_SOURCE`.

