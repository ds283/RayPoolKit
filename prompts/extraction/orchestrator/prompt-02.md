# Orchestrator — prompt 02, the test suite

Read [`../README.md`](../README.md) first: §0.2 (with its note at 02's writing), §1, §2 (rows
02–04), §4, §5 and §6.2 (U6, U9). Then read [`prompt-01.md`](prompt-01.md) §0's last list,
"Conventions", which this note keeps unless it says otherwise, and the board's *Orchestrator
review of prompt 01*.

**You do not write code.** You may:
- run the suite, the equivalence check and the tests the log names;
- replay the log's mutation and stand-in diffs with `git apply`, and revert them;
- run an in-process check or a probe from the session scratchpad, never committing one;
- read SGK through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show b510bc9:<path>`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`02-the-test-suite.md`](../02-the-test-suite.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** none expected; one possible, from (s2) ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- 01 landed (`49f3ddf`) and its review is recorded (`53477ff`). 02 is written (`d9adb9b`), and U6
  and U9 are taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the first prompt whose output is judged by what it would catch, not by what it is.** 01
moved a file and proved the move. 02 writes perhaps a hundred tests over a module it must not
touch, and a test that passes without reaching its branch looks exactly like one that does. The
acceptance is therefore mutation: each reachable row of the inventory has a named test and a
named mutation that fails it. The review has three halves:
- **the stand-ins are faithful**: `wait` refuses what Ray refuses, with Ray's exception types;
  `get` copies, as Ray does; no test can reach real Ray, and none can hang;
- **the suite bites**: every mutation in the log fails the tests it names when replayed, and the
  orchestrator's own (§3 check 6) fail too;
- **the module is untouched**: `raypoolkit/RayWorkPool.py` is byte for byte `49f3ddf`'s, and the
  check still exits 0 with 01's counts.

**What moves on purpose:** eight new files under `raypoolkit/tests/` (`standins.py` and the seven
modules of the prompt's §2.3); eight `NO_SOURCE` entries in `compare_with_source.py`; the records.
Nothing under `raypoolkit/` outside `tests/`, and not `test_package_imports.py`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-10 at `d9adb9b` (package
files as at `49f3ddf`). Pass them on. Each is an IMPLEMENTATION CHOICE at the orchestrator's
direction unless it says otherwise, and the log says so.

1. **A spin guard in the stand-in, and a timeout on every mutation run.** Some mutations stop
   `run()` from making progress, and then it loops for ever. Measured on a scratch stand-in:
   `max_task_queue=0` or `create_batch_size=0` leaves `_todo` full and `_inflight` empty, so every
   pass calls `ray.wait([], num_returns=0)`, which returns `([], [])`, and the loop at `:246` never
   ends. Mutating `:250` or `:252` to `if False:` / `while False:` does the same. So:
   - `StandinRay.wait` counts its calls and raises a `RuntimeError` naming the count past a cap
     (the orchestrator's probe used 1,000; any cap far above the largest test's need will do).
     `test_standins.py` tests the cap. The log gives its value.
   - The mutation driver runs each suite with a timeout (Python's `subprocess.run(…, timeout=…)`;
     GNU `timeout` is also at `/opt/local/libexec/gnubin/timeout`). A mutation that times out has
     **not** been caught: the log records it as a hang and the agent strengthens the guard, not the
     record.
   - No test constructs a pool with `max_task_queue`, `create_batch_size` or `process_batch_size`
     below 1. That such a pool never ends (or, for `process_batch_size=0`, raises Ray's
     `ValueError`) is an observation for the log, not a branch to pin.
2. **(m1) means all 26 `.hex` keys**, the board's list (`:260 … :506`), on `ref`,
   `available_task`, `compute_task`, `store_task` and `validation_task` alike, each `.hex` →
   `.hex()`. Applied as one diff. It must fail the fault-1 test; the log lists everything else that
   fails (the orchestrator expects nothing else to).
3. **(m5) needs a test built for it.** The mutation sets `_last_num_available_complete` from
   `_num_store_complete`. It is seen only in a *second* progress pair, as the available segment's
   interval rate, and only when the two counts differed at the first pair. A lookup-only pool with
   an availability handler and every object available does it (its store count stays 0). Without
   such a test (m5) survives.
4. **Inventory rows the prompt does not list.** Add each to the log's table with a test and a
   mutation, or as unreachable with the reason, as the prompt's §2.4 asks for a found branch:
   - **the absent post handler at each of the five exits**: the false arm of `:361`, `:398`,
     `:417`, `:489` and `:513`. P1 pins the handler's return; nothing pins that no handler means no
     call. Mutating one guard to `if True:` calls `None` and must fail;
   - **`_format_rates`' `assert current_value is not None`** (`:42`): unreachable, since every
     caller passes an `int` count. A row beside U1, no test;
   - **the five `max(…, 0)` clamps** (`:340`, `:412`, `:437`, `:470`, `:508`): never active, since
     each decrement follows the increment for the same task, so removing one is an equivalent
     mutation. One row, unreachable, no test. 04 may want to know.
5. **The clock.** `ScriptedClock`'s step is an integer number of seconds (the default 1 s is fine):
   `format_time` prints `{interval:.3g}s`, so integral readings print as `4s`, `2m 5s`, and the
   pinned lines stay exact. The `datetime` companion's `now()` **reads** the clock and does not
   advance it, so that the stamp is the reading of the `:523` call before it. The log states both.
6. **Ray's `wait` has two checks the prompt does not list** (read at 2.43.0,
   `ray/_private/worker.py:2950-2997`): a single `ObjectRef` is refused before the list check (both
   `TypeError`), and a negative `timeout` is a `ValueError`. The pool passes neither. The stand-in
   may enforce them; the log says whether it does.
7. **`PoolTestCase` has no `test_` method.** Each test module imports it, and `unittest`'s loader
   collects every `TestCase` subclass in a module's namespace. A `test_` method on it would run
   once per importing module and inflate the count.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's measurements hold** at Ray 2.43.0, by a probe from the scratchpad with
  `env -u PYTHONPATH … -I`:
  - `ObjectRef(bytes(28))` constructs; 20 and 4 bytes raise `ValueError` ("ID string needs to have
    length 28"). Two refs from the same bytes are `==`, hash equal, and make a one-member set;
    their `.hex` methods are not equal, and their `.hex()` strings are. One ref's `.hex`, read
    twice, is equal to itself and hashes equal, so a ref the builder returns twice collapses to one
    key.
  - `pickle` and `copy.deepcopy` give an equal, distinct ref.
  - **The `wait` contract**, `ray/_private/worker.py:2950-2997`, is the prompt's clauses 1–6 in that
    order, after the two checks of clarification 6. The empty-list return (`:2987-2988`) precedes
    the duplicate and `num_returns` checks.
  - **The auto-init hook.** `enable_auto_connect` is a module constant, read from the environment
    when `ray/_private/auto_init_hook.py` is imported (`:7`), so it cannot be set after `import
    ray`. `auto_init_ray` calls `ray.init()` through the module attribute, inside
    `with auto_init_lock:`. With `"ray.init"` patched to raise, real `ray.get` and `ray.wait` on a
    constructed ref each raise the patch's exception, a second `ray.get` raises it again (the lock
    is released; no deadlock), `ray.is_initialized()` stays false, and no Ray process appears.
  - **The string target.** `mock.patch("raypoolkit.RayWorkPool.ray", ns)` replaces the module's
    `ray` (`sys.modules["raypoolkit.RayWorkPool"].ray is ns`), leaves the class without a `ray`
    attribute, and restores the module's on exit.
  - **With `fresh_refs`**, the first completed lookup raises `KeyError` at `:322`.
  - `format_time`, `_readable_rate` and `_format_rates` give exactly the prompt's §2.5 values, all
    fourteen. A naive `datetime` formats with `%z` as `2026-10-10 12:00:00`, no offset.
- **The module's calls, as the prompt says:** `ray.wait` at `:316`, `ray.get` at `:331`, `:455` and
  `:499`; `isinstance(…, ObjectRef)` at `:281`; `time.perf_counter` at `:161`, `:523`, `:555` and
  `:564`; `datetime.now()` at `:544`. `format_time` (`_timing.py:16-52`) uses no clock.
- **The consumer patterns** are SGK's at `b510bc9`,
  `docs/gktk-remedial/scoped_pipeline_run.py:120-124` (`_STAGE_BANNER`, `_QUEUE_PROGRESS`,
  `_QUEUE_COMPLETE`), character for character the prompt's §2.5. The test copies them from the prompt, not from SGK, and names no client.
- **What the progress line counts.** `{n}/{total}` and the percentage come from `len(self._todo)`,
  the items whose task has **not yet been built**, not those not yet complete. A pool whose items
  are all built in the first batch therefore prints `0/T … = 100.00% complete` with the N4 suffix
  on its first progress line, while every task is still in flight. That is the behaviour to pin.
- **The banner's first captured line is empty** (`"\n** {title}"`).
- **The fault tests behave as the prompt's §2.6 says**, by reading: fault 3's `TypeError` is
  `len()` of the consumed generator at `:138`; fault 4b's is calling `None` at `:431`. Fault 2's
  results entry holds the persisted object only if the post handler returns `None` (P1).
- **The toolchain.** `venv/` as 01 left it: Python 3.12.15, `ray==2.43.0`, `black==25.1.0`,
  `raypoolkit` installed editable. It needs no change.
- **Expected counts.** The suite is **3** before (`Ran 3 tests … OK`, re-run by the orchestrator at
  `d9adb9b`, 0.8 s) and N after, N > 3. `compare_with_source.py` exits 0 before (572 identical, 2
  D-imp, 1 D-pool, 4 D-int, 4 declared files, 0 undeclared) and with the same counts and **12**
  declared files after. The index is **6** now, and 6 after, or 7 if (s2) opens an issue.
- **SGK.** `HEAD` is still `b510bc9`, its tree clean, `RayTools/RayWorkPool.py` blob `b4666fa`.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) The stand-ins.** `standins.py` gives the prompt's entry points; `wait` enforces the
  contract with Ray's types, and the spin cap; `get` copies; `PoolTestCase` patches by string only,
  including `"ray.init"`, and checks `ray.is_initialized()` at tear-down.
- **(E2) The suite runs**, `Ran N tests … OK`, with no Ray process before or after.
- **(E3) The inventory is covered.** One log row per §2.4 ID and per addition, each with a test that
  exists and reaches its branch.
- **(E4) The suite bites.** Every mutation in the log fails what it says, replayed, and the
  orchestrator's own mutations fail too.
- **(E5) The faults and the lines.** The five fault tests under the prompt's names, each failed by
  its mutation; the printed lines pinned whole, and matching the orchestrator's rendering (§3).
- **(E6) The module is untouched**; the check exits 0 with 01's counts; the guard passes; `black` is
  clean.
- **(E7) The records.** The log with the prompt's §4.3 additions; the board, the index and
  `prompts/INDEX.md`.

**Conventions.** Prompt 01's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each mutation and stand-in diff with `git apply --check` and `-R --check`, replay it in
  `bash`, and check that `git status` is clean after it;
- read SGK only through `git show b510bc9:<path>`, and never run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, and put **no scratch `.py` under
  `raypoolkit/`**, even for a moment: the guard and the check scan it, and a mutation run would
  collect it;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

Two additions:
- **A mutation driver lives in the scratchpad**, and applies each diff with `git apply` from the
  repository root, so that what it ran is exactly what the log records. Each run is the whole
  suite, by `CLAUDE.md`'s command, under a timeout (clarification 1).
- **The pinned lines are read from the module, not from the prompt.** The prompt paraphrases
  `:545` and `:550-551`; the tests take their spacing from the source. Where the two differ, the
  source is right and the log says so; a difference in *behaviour* from the prompt is a stop
  (prompt §5).

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone.
2. **The baseline.** The suite gives `Ran 3 tests … OK`, and `compare_with_source.py` exits 0.
   `git diff 49f3ddf -- raypoolkit/RayWorkPool.py` is empty.
3. **SGK.** `git -C SecondaryGWKit rev-parse b510bc9:RayTools/RayWorkPool.py` is `b4666fa…`.
   Record SGK's `HEAD`.
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
5. **The index.** 6 now; 6 after, or 7 with (s2)'s issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md` and log 01;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's seven clarifications and additions. Clarification 1 is
the one that matters: without the spin guard, the mutation pass hangs.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02-the-test-suite.md`, in README §5.1's form, with
  the prompt's §4.3 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else.** In particular it
  must not touch any file under `raypoolkit/` outside `tests/`, nor `test_package_imports.py`,
  `pyproject.toml`, `PROVENANCE.md`, `README.md`, `CLAUDE.md`, the campaign README, or anything
  under `orchestrator/`.
- **The package module is not edited**, except by a mutation that is reverted at once.
- **It edits no client repository and not DatastoreKit, and runs none of their code.**
- **It runs no build and no `pip`, and starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list and the records: the
   eight new files under `raypoolkit/tests/`, `compare_with_source.py`, the log, the board,
   `prompts/INDEX.md` and, if needed, the index. No `venv/`, `*.egg-info`, `__pycache__` or scratch
   file. `git diff 49f3ddf <commit> -- raypoolkit/RayWorkPool.py raypoolkit/_timing.py
   raypoolkit/contract.py raypoolkit/__init__.py raypoolkit/tests/test_package_imports.py` is
   empty.
2. **E1, the stand-ins, by reading.** Read `standins.py` in full, against the prompt's §2.1 and
   §0's clarifications:
   - `wait` checks, in Ray's order, list (`TypeError`), elements (`TypeError`), empty → `([], [])`,
     duplicates by equality (`ValueError`), `num_returns <= 0` and `> len` (`ValueError`); records
     `(len(refs), num_returns)`; returns `order(refs)` split at `num_returns`; with `fresh_refs`,
     rebuilds the ready refs from their bytes; raises past the spin cap;
   - `get` returns `pickle.loads(pickle.dumps(value))` and refuses an unminted ref, naming it;
   - the work objects and the datastore pool are at module level and carry no stand-in;
   - the clock advances on every `perf_counter`, and `now()` does not advance it;
   - `PoolTestCase.setUp` patches the four string targets and nothing through the package
     attribute; `tearDown` asserts `ray.is_initialized()` is false; it has no `test_` method.
3. **E2, by running.** In a fresh shell, `./venv/bin/python -m unittest discover -s
   raypoolkit/tests -t .` gives `Ran N tests … OK`, with N and the per-module counts equal to the
   log's. `pgrep -lf 'gcs_server|raylet|ray::'` is empty before and after. Run it twice; the counts
   and verdict agree.
4. **E3, the inventory, by reading.** The log's table has one row per §2.4 ID and per §0
   clarification 4 addition, plus any the agent found. Every named test exists (`grep -n "def
   <name>"`). Read six tests in full and check that each reaches its row: **L5** (no task, no post
   handler, `results` keeps the unavailable object), **S4** with **P1**, **R9** (the all-`None`
   batch and `wait_calls` holding `(0, 0)`), **N3/N4** (100.00% with the suffix on the first pair),
   **N5** (a second pair with interval rates), **X1** (seeded through `_inflight` and `_data` only).
   The white-box seams: `grep -nE "\._[a-z]" raypoolkit/tests/test_*.py` finds only the prompt's
   §2.2 helpers, `_inflight` and `_data` in X1's test, and the log lists each test that uses one.
5. **E4, the log's mutations, by replaying.** Replay every mutation diff of the log, one at a time,
   from a clean tree, with a bash driver in the scratchpad and a timeout. Each must apply cleanly,
   fail the suite, and fail the tests the log names (compare the sets of failing test ids). (m1)–(m5)
   are among them; (m4) is nine diffs, one per literal. `git status` is clean after each.
6. **E4, the orchestrator's own mutations**, not in the prompt. Each must fail the suite:
   - (o1) `:482` `(idx, replacement_obj)` → `(idx, obj)`: V2's post handler then gets the
     pre-persist object, and V1's warning prints `store_id=None`;
   - (o2) `:419` drop `and self._store_results`: with an availability handler, a post handler that
     returns non-`None` and no `store_results`, the pool raises `AttributeError` (no `results`);
   - (o3) `:555` `self._last_notify_time = time.perf_counter()` → `= now_time`: the next pair's
     interval is one clock step longer, so its interval rates change;
   - (o4) `:286` drop `contents={str(ref_data)}` from the message: R6's test pins the message whole.
     If it passes, that is not a failure of the suite, but the log's R6 row must then say the
     message is not pinned; record which.
   (o1)–(o3) failing nothing is a finding, opened on the board's §3.
7. **E5, the faults.** `test_inherited_faults.py` has `TestInheritedFaults` with the prompt's five
   names, each docstring naming its board issue and saying it pins the fault. Replay (m1), (m2) and
   (m3) and see the fault tests fail. Fault 5's "maker" assertions are in `test_construction.py`.
   The board's §3 has a dated line on each of faults 1–5 naming its test.
8. **E5, the printed lines.** Read `test_printed_lines.py`. The three patterns are the prompt's,
   character for character, and its docstring names no client: `grep -nE
   "SecondaryGWKit|SGK|StageTracker|RunRegistry|ChamPBH|StochasticInstantons|Datastore\b"
   raypoolkit/tests/*.py` finds nothing but board issue names. Then compare one of the agent's
   whole-run tests with the orchestrator's rendering, below. It was made on a scratch stand-in:
   the clock advancing 1 s per call, its first reading 1 s; `now()` = 2026-10-10 12:00:00 plus
   the reading; four items built in one batch; the datastore stand-in setting
   `store_id = 100 + item`; a validation handler failing item 2; `notify_min_time_interval=2`,
   `notify_time_interval=3`. If the agent's set-up differs, rebuild the rendering to match it
   rather than expecting the same text:

   ```

   ** demo
      -- 2026-10-10 12:00:05 (4s running): 0/4 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         inflight: 0 lookup, 4 compute, 0 store, 0 validation | completed: 4 lookup (avg 60/min), 0 compute (avg 0/day), 0 store (avg 0/day), 0 validation (avg 0/day)
      -- 2026-10-10 12:00:10 (9s running): 0/4 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         inflight: 0 lookup, 0 compute, 4 store, 0 validation | completed: 4 lookup (0/day, avg 26.67/min), 4 compute (60/min, avg 26.67/min), 0 store (0/day, avg 0/day), 0 validation (0/day, avg 0/day)
   …
   !! WARNING: W object with store_id=102 did not validate after being emplaced in the datastore
   …
      -- ALL WORK ITEMS COMPLETE in time 21s
         Queue summary: 4 lookup (avg 11.43/min), 4 compute (avg 11.43/min), 4 store (avg 11.43/min), 4 validation (avg 11.43/min)
   ```
9. **E1 and E5, the stand-ins bite.** Replay (s1) and (s2) and check the log's account. If (s2)
   failed nothing, its §3 issue is open and indexed. Read (s3)'s account and check, by reading
   only, that the test it names would reach real `ray.get` or `ray.wait`. Do not run it.
10. **E6 and E7, the check, the guard and the records.**
    - `./venv/bin/python docs/extraction/compare_with_source.py` exits 0: 572 identical, 2 D-imp,
      1 D-pool, 4 D-int, 12 declared files, 0 undeclared; the `git diff` of the script is eight
      `NO_SOURCE` lines, each naming "02 §2.x". The guard's test 1 passes over the new modules.
      `./venv/bin/black --check raypoolkit docs` (25.1.0) is clean.
    - The log has every section of README §5.1 and each of the prompt's §4.3 additions: the
      inventory table; the entry points with signatures; the seams, test by test; the counts
      3 → N by module; the check's whole output; every mutation diff; §0's clarifications recorded
      as deviations.
    - Board: the header, 02's row (landed, suite 3 → N), the fault lines in §3, any new issue.
      Index: count it, and check the header matches. `prompts/INDEX.md`: the campaign's line.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02* paragraph, in the form of
  01's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 02, and its header;
  - the notes line, with this note added and marked "used for 02".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - what landed, and the count N, by module;
  - the stand-ins' entry points, and the spin cap;
  - the inventory: rows covered, rows unreachable, rows added;
  - the mutations: how many, all caught; (m1)'s full effect, for 04; the orchestrator's (o1)–(o4);
  - anything opened;
  - that 03 can now be written, against the tree 02 left, with U7 to put to the user.
