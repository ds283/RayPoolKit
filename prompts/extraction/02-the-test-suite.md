# Prompt 02 — the test suite

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 01 landed (`49f3ddf`) and its review is recorded (`53477ff`).
- U6 and U9 are taken (README §6.2, 2026-10-10, both as recommended; U9 as amended at this
  prompt's writing).
- `git status` is clean in this repository, and the suite gives `Ran 3 tests … OK`.

**Closes:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus**. The suite is what makes `v0.1.0` a release whose behaviour is
pinned (README §2, order), and what 04 inverts fault by fault. A test that passes without
reaching the branch it names is worse than none: it will be cited as coverage. The acceptance is
therefore mutation, not reading.

**Read first:**

1. [`README.md`](README.md): §0.2 (with its note at this prompt's writing), §1, §2 (rows 02–04),
   §4, §5 (all of it, rules 6, 8 and 9 especially) and §6.2 (U6, U9).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §3, the five `[00-…]` faults with their
   **Package** lines, and `[01-a-kept-comment-names-the-datastore-service]`; §1's *Orchestrator
   review of prompt 01*.
3. [`logs/01-import-the-pool.md`](logs/01-import-the-pool.md) §3.6 and §7.
4. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`, in particular "What this repository is"
   (with its two exceptions, taken 2026-10-10) and "Repository mechanics".
5. The package, in full: `raypoolkit/RayWorkPool.py` (575 lines), `_timing.py`, `contract.py`,
   `__init__.py`. Then `raypoolkit/tests/test_package_imports.py`: test 3's docstring states how a
   test must patch the module (U4). Then `docs/extraction/compare_with_source.py`'s `NO_SOURCE`.

Line numbers below are the package's at `53477ff`, which equal SGK's at `b510bc9`.

---

## 1. What is wanted

A suite that pins what `RayWorkPool` does today, every path through `run()` and every check in
the constructor, with no Ray cluster. Each branch of §2.4's inventory is reached by a named test,
and a named mutation of that branch fails it. Faults 1–4 of the board's §3 are pinned **as they
behave**, by tests named for them, which 04 inverts. Every line the pool prints is pinned, word
for word, against a scripted clock (U9).

**No behaviour changes.** The package module is not edited (README §5 rule 8). A test that cannot
pass against the module as it is records a finding; it does not change the module.

---

## 2. What to change

### 2.1 The Ray stand-in (U6)

The pool module reaches Ray through exactly two calls, `ray.wait` (`:316`) and `ray.get` (`:331`,
`:455`, `:499`), and through `ObjectRef` for one `isinstance` test (`:281`), imported by name
(`from ray import ObjectRef`, `:6`). Work items are **real `ray.ObjectRef` instances**, and the
module's name `ray` is replaced, for each test, by a stand-in that has `wait` and `get` and
nothing else, so that any other use of `ray` in the module fails loudly.

**Measured by the planner (2026-10-10), and to be relied on:**
- `ray.ObjectRef(b)` constructs with no cluster when `b` is **exactly 28 bytes**; 20 or 4 bytes
  raise `ValueError`. Refs from equal bytes are equal and hash equal, but their `.hex` bound
  methods are not equal (fault 1). A set of two such refs has one member.
- `pickle` and `copy.deepcopy` of an `ObjectRef` work with no cluster, and give an equal but
  distinct ref.
- **Ray's `wait` contract**, read from `ray/_private/worker.py` at 2.43.0 (this venv), and found
  the same in ChamPBH's venv (2.53.0) and StochasticInstantons' (2.55.1), read only:
  1. the argument must be a `list` (an `ObjectRef` or other type is a `TypeError`);
  2. every element must be an `ObjectRef` (else `TypeError`);
  3. **an empty list returns `([], [])`, before `num_returns` is checked**;
  4. refs that are equal count as duplicates: `len(refs) != len(set(refs))` is a `ValueError`;
  5. `num_returns <= 0` is a `ValueError`, and so is `num_returns > len(refs)`;
  6. it returns `(ready, remaining)`.

  The stand-in's `wait` enforces 1–5 with the same exception types, so that the suite fails where
  Ray would. Clause 3 matters: when every task builder in a batch returns `None`, the pool calls
  `ray.wait([], num_returns=0)` (`:315-318`), and Ray accepts that.
- `ray.wait` and `ray.get` are wrapped by Ray's auto-init hook, which calls `ray.init()` through
  the module attribute (`ray/_private/auto_init_hook.py`) unless `RAY_ENABLE_AUTO_CONNECT=0` was
  set **before `ray` was imported**. The suite cannot set it in time: importing any test module
  imports `raypoolkit`, which imports `ray`. **So every test patches `ray.init`** (the string
  target `"ray.init"`) with a function that raises, and asserts `ray.is_initialized()` is false at
  tear-down. A test that reaches real Ray then fails at once, and no cluster starts. (Measured: with
  `ray.init` so patched, real `ray.get` and `ray.wait` on a constructed ref raise the patch's
  exception, and no Ray process appears.)

**The stand-in, `raypoolkit/tests/standins.py`.** Its entry points are this prompt's interface to
03 and 04. Names may differ only if the log gives the mapping.
- **`StandinRay`**, a table from ref to value.
  - `ref(value) -> ObjectRef` mints a fresh 28-byte ref from a counter and records `value`.
  - `wait(refs, *, num_returns=1, timeout=None, fetch_local=True)` applies the contract above. It
    then returns the first `num_returns` refs of `order(refs)` as `ready` and the rest as
    `remaining`. `order` is a settable callable, by default the identity (input order).
    - **Every ref is ready at once.** Order is the only thing a test controls.
    - Each call is recorded as `(len(refs), num_returns)` in `wait_calls`.
    - A flag, `fresh_refs`, makes `wait` return equal but **distinct** refs, built from the same
      bytes (for fault 1).
  - `get(ref)` returns the recorded value **by value**, as `pickle.loads(pickle.dumps(value))`,
    as Ray does. A ref it did not mint is an error naming the ref. The module only ever calls
    `get` on one ref, so a list argument may be refused.
- **`ScriptedClock`**, standing in for the module's `time`.
  - `perf_counter()` advances by a set step on every call (by default 1 s); `advance(seconds)`
    jumps.
  - A companion stands in for the module's `datetime`. Its `now()` returns a **naive** `datetime`
    equal to a fixed base plus the clock's current reading.
  - The module calls `perf_counter` at `:161` (construction), `:523` (every pass of the loop),
    `:555` (after a notification) and `:564` (completion), and `datetime.now()` only at `:544`.
  - **The clock must advance.** At completion, `_format_rates` divides by the total time (`:50`).
    A clock that returns one value raises `ZeroDivisionError` there, which perf_counter never
    does.
- **Work objects and a datastore pool**, defined at module level so that they pickle.
  - A work object has an `available` attribute; a "blob" kind has none. Its `compute(**kwargs)`
    records its keyword arguments and returns a ref minted by the active stand-in. Its `store()`
    records that it ran. Its `store_id` is `None` until a persist sets it.
  - The stand-in datastore pool's `object_store(obj)` records the call. It returns a ref whose
    value is a copy of `obj` with `store_id` set and `available` true, or, when the test asks,
    with `available` false (for `:458`).
  - Objects are copied whenever they pass through `get`. They therefore must not carry the
    stand-in itself; they reach the active `StandinRay` through a module-level accessor that the
    test case sets.
- **`PoolTestCase(unittest.TestCase)`**. Its `setUp` installs, **by string target only** (U4,
  guard test 3's docstring):
  - `"raypoolkit.RayWorkPool.ray"` → the stand-in's `wait`/`get` namespace;
  - `"raypoolkit.RayWorkPool.time"` and `"raypoolkit.RayWorkPool.datetime"` → the clock;
  - `"ray.init"` → a function that raises.

  It gives a helper that runs a pool with stdout captured and returns the lines. Its `tearDown`
  asserts `ray.is_initialized()` is false. A test that patches through the package attribute
  `raypoolkit.RayWorkPool` patches the class, not the module, and is wrong.

`standins.py` gets its own tests (`test_standins.py`): each clause of the `wait` contract with its
exception type; `get` by value; `fresh_refs`; the clock; and the `ray.init` guard firing on a real
`ray.get`.

### 2.2 White-box seams, and no others

The suite drives the pool through its constructor, `run()`, `results`, `total_time` and stdout.
Two seams below that are allowed, and the log lists every test that uses one:
- **The private helpers** `_readable_rate`, `_format_rates` (module functions) and
  `_build_queued_status_message`, `_build_completed_status_message` (methods), called directly.
  For example, `_format_rates` with both times `None` returns `''`, which `run()` never reaches.
- **Seeding `_inflight` and `_data`** before `run()`, only for the unexpected-item-type branch
  (`:518-519`), which no public input reaches.

Nothing else private is read or written.

### 2.3 The test modules

All under `raypoolkit/tests/`. Each module's tests use `PoolTestCase`, except where a module
tests only pure functions.
- `test_standins.py`: §2.1.
- `test_construction.py`: the checks at `:94-102` and their exceptions and messages, exactly as
  they are (including "maker", for fault 5, which 04 rewords); the three default handlers
  (`:60-69`), each reached through a pool built with its default; `results` only with
  `store_results=True`, sized and filled with `None`; the banner only with a `title`; neither
  `results` nor `total_time` set when not asked for.
- `test_task_builder.py`: the builder's six outcomes (`:257-310`), §2.4 R1–R9.
- `test_run_paths.py`: every path through the dispatch loop (`:320-521`), §2.4 L, A, K, S, V
  and X, including the five exits to the post handler and what each puts in `results`.
- `test_scheduling.py`: `max_task_queue`, `create_batch_size` and `process_batch_size`, read from
  `wait_calls` and from the builder's call count. `results` keeps the task list's order whatever
  order tasks complete in (the stand-in's `order` reversed).
- `test_printed_lines.py`: U9, §2.5.
- `test_inherited_faults.py`: faults 1–4, §2.6.

### 2.4 The branch inventory

Every row is reached by at least one named test, and has one named mutation that fails it (§3.3),
except U1, which is unreachable. The log reports it as such, with the reason, and it gets no
test. IDs are this prompt's, for the log's table.

**Constructor**
| ID | Lines | Branch |
|---|---|---|
| C1 | `:94-97` | compute handler without persist handler → `RuntimeError` |
| C2 | `:99-102` | persist handler without compute handler → `RuntimeWarning`, raised (fault 4) |
| C3 | `:137-139` | `store_results` → `results` sized from `len(task_list)` (fault 3), `_current_idx = 0` |
| C4 | `:165-166` | `title` → the banner |

**The task builder** (one pass of `:252-312`)
| ID | Lines | Branch |
|---|---|---|
| R1 | `:250` | a batch is created only while `len(_inflight) < max_task_queue` and items remain |
| R2 | `:252` | at most `create_batch_size` builder calls per batch |
| R3 | `:262-266` | the result index is taken only with `store_results` and a single return; else `None` |
| R4 | `:271-279` | a dict with `"ref"`, with and without `"compute_payload"` |
| R5 | `:281-282` | a bare `ObjectRef` |
| R6 | `:284-287` | anything else (including a dict without `"ref"`, or a nested list) → `RuntimeError` |
| R7 | `:289-294` | `None`: nothing enqueued; with `store_results` → `RuntimeError` |
| R8 | `:296-307` | a list, tuple or set; with `store_results` → `RuntimeError`; each element through R4–R6 with no result index |
| R9 | `:315` | `num_returns = min(process_batch_size, len(_inflight))`, which is 0 with nothing in flight |

**The dispatch loop**
| ID | Lines | Branch |
|---|---|---|
| L1 | `:324-341` | a lookup completes; with `store_results`, its object goes in `results` |
| L2 | `:345-357` | available, with an availability handler → an `"available"` task |
| L3 | `:361-364` | available, no availability handler → **post-handler exit 1** |
| L4 | `:366-392` | not available, with a compute handler → a compute task, with `label` from `label_builder` when it returns non-`None`, and `payload` from `"compute_payload"` |
| L5 | `:366-368` | not available, **no compute handler** → nothing: no task, no post handler, `results` keeps the unavailable object. Pinned as it behaves; the planner does not classify it as a fault |
| L6 | `:396-401` | no `available` attribute (a "blob") → **post-handler exit 2** |
| A1 | `:405-420` | an availability task completes → **post-handler exit 3**, given the lookup's object |
| K1 | `:422-447` | a compute completes → the store handler, then the persist handler, → a `"store"` task |
| S1 | `:455-461` | a store completes and its object is not available → `RuntimeError` |
| S2 | `:463-471` | a store completes; with `store_results`, the persisted object replaces the entry |
| S3 | `:474-485` | with a validation handler → a `"validate"` task on the persisted object |
| S4 | `:489-492` | no validation handler → **post-handler exit 4**, given the *pre-persist* object (fault 2) |
| V1 | `:499-503` | a validation returns anything but `True` → the warning line |
| V2 | `:513-516` | a validation completes → **post-handler exit 5**, given the persisted object |
| P1 | `:363`, `:400`, `:419`, `:491`, `:515` | at each exit, a non-`None` return replaces the `results` entry only with `store_results`; `None` leaves it |
| X1 | `:518-519` | an unexpected item type → `RuntimeError` (seeded, §2.2) |

**Notification and completion**
| ID | Lines | Branch |
|---|---|---|
| N1 | `:526-529` | no progress lines without a `title`, nor before `notify_min_time_interval` has passed |
| N2 | `:530-533` | a progress pair when `notify_time_interval` has passed, or when more than `notify_batch_size` items were processed since the last |
| N3 | `:535-542` | the percentage: 100.0 with nothing left to create, else the fraction |
| N4 | `:546-547` | the "(may be waiting …)" suffix above 99.99% |
| N5 | `:557-561` | the "last" counts move on, so the next pair's rates are per interval |
| F1 | `:563-571` | with a `title`: `total_time`, and the completion pair |
| F2 | `:572-575` | the "(no compute items …)" line when no compute completed |
| Q1 | `:168-182` | each optional segment of the queued message, per handler set |
| Q2 | `:184-243` | each optional segment of the completed message, per handler set, with and without rates |
| T1 | `:20-33` | `_readable_rate`'s units: `/sec`, `/min`, `/hr`, `/day` |
| T2 | `:36-57` | `_format_rates`: interval rate only with both a delta and a last value; avg only with a total |
| U1 | `:33` | `_readable_rate`'s `raise NotImplementedError`: **unreachable** (the `"day"` entry always returns) |

A branch the agent finds that is not in this inventory is added to the log's table, with a test
and a mutation, and the log says so.

### 2.5 The printed lines (U9)

**Pinned word for word.** Each test captures stdout and asserts whole lines. The clock is
scripted, and the stamp comes from the stand-in's naive `now()`. The lines:
- the banner, `"\n** {title}"` (a blank line, then the title);
- the progress pair: `"   -- {stamp} ({format_time} running): {n}/{total} work items remaining =
  {pct:.2f}% complete"`, with the N4 suffix where it applies, then `"      inflight: … | completed:
  …"`. Take the exact spacing from `:545` and `:550-551`, not from this paraphrase;
- the completion pair, `"   -- ALL WORK ITEMS COMPLETE in time {format_time}"` and
  `"      Queue summary: …"`, and F2's line;
- V1's warning, which is printed with or without a `title`.

With a naive stamp, `%z` prints nothing: the stamp is `YYYY-MM-DD HH:MM:SS`, with no offset.

**`format_time` and the rates are pinned at their edges**, measured by the planner and to be
re-measured, not copied:
- `format_time`: `0.00499` → `0.00499s`; `60` → `60s`; `61` → `1m 1s`; `3600` → `60m 0s`;
  `86400` → `24h 0s`; `90061.25` → `1d 1h 1m 1.25s`. The comparisons are strict (`>`), and a unit
  is skipped when what remains is below it, which is why `86400` has no minutes;
- `_readable_rate`: `0` → `0/day`; `0.01` → `36/hr`; `0.2` → `12/min`; `10` → `10/sec`;
  `12345.6` → `1.235e+04/sec`;
- `_format_rates(10.0, 20.0, 5, 2)` → `18/min, avg 15/min`; `(None, 2.0, 6, None)` →
  `avg 180/min`; `(None, None, 3, None)` → `''`.

**The consumer patterns.** A consumer of this output is known to parse it with three patterns,
which the suite checks against the pool's **actual** lines:
- banner: `^\s*(?:\*\*|>>)\s+(\S.*?)\s*$`, whose group is the title;
- progress: `(\d+)/(\d+)\s+work items remaining\s*=\s*([\d.]+)%\s+complete`, with its three
  groups equal to the pool's numbers;
- completion: `ALL WORK ITEMS COMPLETE`.

The patterns are copied into the test as they are. Its docstring says that a consumer parses the
output with them, and that changing a line they match changes the pool's interface (`CLAUDE.md`,
"Releases"). It names no client.

### 2.6 The inherited faults, pinned as they behave

In `test_inherited_faults.py`, class `TestInheritedFaults`, under these names, which 04 inverts
and renames. Each docstring names its board issue and says that the test pins the fault, not the
intended behaviour.

| Test | Board issue | Pins |
|---|---|---|
| `test_fault_in_flight_work_is_keyed_on_a_bound_method` | `[00-in-flight-work-is-keyed-on-a-bound-method]` | with `fresh_refs`, the first completed lookup raises `KeyError` from `:322` |
| `test_fault_post_handler_after_persist_gets_the_unpersisted_object` | `[00-a-post-handler-after-persist-gets-the-unpersisted-object]` | at exit 4 the handler is given an object whose `store_id` is `None`, while `results` (S2) holds the persisted one |
| `test_fault_store_results_sizes_from_len_of_the_task_list` | `[00-store-results-sizes-from-len-of-the-task-list]` | a generator `task_list` with `store_results=True` raises `TypeError` at construction; without `store_results` it runs |
| `test_fault_persist_handler_without_compute_raises_runtime_warning` | `[00-the-constructor-checks-its-handlers-unevenly]` | `compute_handler=None` with the default persist handler raises `RuntimeWarning` |
| `test_fault_store_handler_none_with_compute_fails_at_first_compute` | the same | `store_handler=None` with a compute handler constructs, then raises `TypeError` when the first compute completes |

Fault 5 is pinned by `test_construction.py`'s message assertions, and has no test of its own here.

### 2.7 The equivalence check

`compare_with_source.py` gains one entry in `NO_SOURCE` per new file of §2.1 and §2.3, each
naming "02 §2.x", and **no other change**: no rule, constant or behaviour. It still exits 0 with
01's counts (572 identical, 2 D-imp, 1 D-pool, 4 D-int). A new file under `raypoolkit/` that is
not declared is a failure, as 01 designed.

---

## 3. Verification

1. **The suite.** `./venv/bin/python -m unittest discover -s raypoolkit/tests -t .` gives
   `Ran N tests … OK`, with N > 3. The count before is 3. Record N, and the count per module.
2. **No Ray.** `pgrep -lf 'gcs_server|raylet|ray::'` is empty before and after the suite. The
   `ray.init` guard never fires in a passing run (a test asserts it can fire, in
   `test_standins.py`).
3. **Mutation.** For each row of §2.4 except U1, one mutation of
   `raypoolkit/RayWorkPool.py`, applied alone to a clean tree, makes the suite fail. Record each
   as a diff, as README §5 rule 9 asks, with the tests that fail. A mutation inverts, removes or
   short-circuits the branch (for example `if self._store_results:` → `if False:`). It is not an
   edit elsewhere that happens to break a test. Add these, which pin things §2.4 does not name:
   - (m1) every `ref.hex` key → `ref.hex()`. It **must fail** the fault-1 test, and the log
     records whatever else fails. 04 makes this change, so the record tells 04's author what
     moves;
   - (m2) `:490` `self._post_handler(obj)` → `self._post_handler(replacement_obj)`: the fault-2
     test fails;
   - (m3) `:138` `len(task_list)` → `self._num_total_items`: the fault-3 test fails;
   - (m4) one character of each printed literal (`:166`, `:545`, `:547`, `:550`, `:551`, `:567`,
     `:570`, `:574`, `:502`): a §2.5 test fails for each;
   - (m5) `:560` back to CPBH/SI's `self._num_store_complete`: a rate test fails. (01's (c) showed
     the equivalence check catches it; this shows the suite does too.)

   Drive the mutations with a script in the scratchpad if that helps. The log still records every
   diff exactly as applied, and `git status` is clean after each.
4. **The stand-ins bite.** Each with a diff and the tests that fail:
   - (s1) `wait` without the empty-list clause: the all-`None` builder test fails with Ray's
     `ValueError`;
   - (s2) `get` returning the stored object itself, not a copy: a test that depends on by-value
     semantics fails, or the log says that none does, and opens a §3 issue for it;
   - (s3) `PoolTestCase` not patching `ray.init`: show, **by reading, without running it**, which
     test would then start Ray. Do not run it.
5. **The check.** `./venv/bin/python docs/extraction/compare_with_source.py` exits 0 with 01's
   counts, and every new file declared. Its whole output goes in the log.
6. **The guard.** `test_package_imports.py`'s test 1 passes over the new modules: they import
   only the standard library, `ray` and `raypoolkit`.
7. `./venv/bin/black --check raypoolkit docs` is clean.

---

## 4. Acceptance

1. §2.1's and §2.3's files exist under their names, or under names the log maps.
2. §3.1–§3.7 hold. In particular, every reachable row of §2.4 has a test and a failing mutation.
3. **The records**, in the same commit:
   - the log, `logs/02-the-test-suite.md`, per README §5.1. It also holds:
     - the inventory table, one row per §2.4 ID plus any added: ID, test(s), mutation (diff),
       what failed;
     - the stand-ins' entry points with their signatures, for 03 and 04;
     - the white-box seams used, test by test;
     - the counts 3 → N, by module;
     - the check's whole output;
   - this board: the header, §1's row for 02 (landed, "this commit", suite), and in §3 a dated
     line on each fault saying which test pins it;
   - `prompts/INDEX.md`: the campaign's line;
   - `docs/OPEN_ISSUES.md`, if the work opens or changes anything.

---

## 5. Stop conditions — stop and ask the user

- A reachable row of §2.4 cannot be reached through the public interface or §2.2's two seams.
- A test can pass only if the package module, or a rule of `compare_with_source.py`, changes.
- A behaviour differs from this prompt's description in a way that is not a misreading, for
  example a printed line whose layout is not `:545`'s. The module is SGK's, so a difference means
  that this prompt or the module is wrong, and the user decides which.
- The suite needs a Ray cluster, `ray.is_initialized()` becomes true, or a Ray process appears.
- The test count would fall below 3.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons or DatastoreKit.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `raypoolkit/tests/standins.py` and the seven test modules of §2.3;
  - `docs/extraction/compare_with_source.py`, its `NO_SOURCE` only;
  - the log, this board and `prompts/INDEX.md`;
  - `docs/OPEN_ISSUES.md`, if needed.
- It changes nothing in `raypoolkit/` outside `tests/`, and does not touch `test_package_imports.py`,
  `pyproject.toml`, `PROVENANCE.md`, `README.md`, `CLAUDE.md` or the campaign README.
- It fixes no fault (04), and sets no dependency range, adds no CI and makes no tag (03).
- It runs the suite at this venv's Python 3.12.15 / Ray 2.43.0 only. 03 runs it at both ends.

---

## 7. The log and the board

`logs/02-the-test-suite.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 02 (landed, commit, log, suite), and §3's
pinning lines.
