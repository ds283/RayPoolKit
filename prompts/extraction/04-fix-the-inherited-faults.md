# Prompt 04 — fix the inherited faults

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 03 landed (`4e90a8a`), its review is recorded (`9db0619`), and **`v0.1.0` is tagged on
  `4e90a8a`** after green CI at both ends (`6b1ddfe`).
- U8 and U11 are taken (README §6.2, 2026-10-10).
- `git status` is clean in this repository, and the suite gives `Ran 116 tests … OK`.

**Closes:** `[00-in-flight-work-is-keyed-on-a-bound-method]`,
`[00-a-post-handler-after-persist-gets-the-unpersisted-object]`,
`[00-store-results-sizes-from-len-of-the-task-list]`,
`[00-the-constructor-checks-its-handlers-unevenly]`,
`[00-messages-say-maker-and-the-module-has-no-licence-header]`,
`[01-a-kept-comment-names-the-datastore-service]` and
`[02-the-constructor-does-not-check-its-sizes]`. **Narrows:** nothing. **Opens:** only what the
work finds.

**Recommended model:** **Opus.**
- The code is small: about 100 changed lines in one module, most of them the 26 `.hex` keys and
  a rewritten constructor check.
- Its weight is in the tests. 02 pinned every fault as it behaves; 04 turns each pin into a guard
  of the fix, and each guard must be shown to fail on the unfixed code. A guard that passes for the
  wrong reason looks exactly like one that works.

**Read first:**

1. [`README.md`](README.md): §0.2 (faults 1–5 and the call-site table), §2 (rows 04–06), §4,
   §5 (rules 6–10) and §6.2 (U8, U11).
2. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`.
3. The board: §3, all seven issues this prompt closes, each with its **Package** lines and its
   **Pinned (02)** line; and the reviews of 02 and 03.
4. [`logs/02-the-test-suite.md`](logs/02-the-test-suite.md) §1.1 (the stand-ins' entry points),
   §1.2 (the white-box seams), §5.2 ((m1)–(m3), the fixes as mutations) and §8.
5. The package as `v0.1.0` left it: `raypoolkit/RayWorkPool.py` in full, `contract.py`,
   `_timing.py`, `__init__.py`; and the tests this prompt changes: `test_inherited_faults.py`,
   `test_construction.py`, `test_run_paths.py` (S4, X1), `test_printed_lines.py`
   (`TestStatusMessages`) and `test_standins.py:108-118`.
6. `docs/extraction/compare_with_source.py`'s docstring, and, for the precedent only,
   DatastoreKit's retirement of its own check: `git -C /Users/ds283/Documents/Code/DatastoreKit
   show HEAD:docs/extraction/compare_with_source.py | head -8`.

Facts below are at `6b1ddfe` (the package and suite as at `v0.1.0`), measured on 2026-10-10.
Line numbers are `v0.1.0`'s; the fixes move them, and the log gives the new ones.

---

## 1. What is wanted

04 fixes the five faults the package inherited, and two issues found since, so that `v0.2.0` (05)
is the release the clients adopt. After it:

- in-flight work is keyed on the ref's value, so the pool works when `ray.wait` returns equal but
  distinct refs (fault 1);
- the post handler after a persist with no validation step is given the persisted object
  (fault 2);
- `store_results=True` accepts any iterable `task_list` (fault 3);
- the constructor checks its handlers evenly, as U8 decides (fault 4), and refuses a size below 1
  (`[02-the-constructor-does-not-check-its-sizes]`), each with `ValueError`;
- its messages say "handler", and every package module carries the licence header U11 decides
  (fault 5);
- the comment that names the client's datastore service is reworded
  (`[01-a-kept-comment-names-the-datastore-service]`).

**Each fix has a test the unfixed code fails**, and 02's pinning tests are inverted into guards.
**The printed lines do not change** (README §5 rule 7): no line a pool prints today changes in
wording or layout.

**README §5 rule 8 has lifted**: this is the first prompt that changes the module. The equivalence
check is retired at `v0.1.0` (§2.8). **04 makes no tag and pushes nothing**, and changes neither
`pyproject.toml` (still `0.1.0`) nor the repository's `README.md` or `PROVENANCE.md`: 05 does all
three and makes `v0.2.0`. The README's "as of `v0.1.0`" wording stays true of `v0.1.0`.

---

## 2. What to change

### 2.1 Fault 1: key in-flight work on `ref.hex()`

Every one of the 26 keys the board lists (`RayWorkPool.py:260, 263, 266, 277, 322, 337, 338, 351,
352, 379, 381, 389, 390, 403, 409, 410, 434, 435, 444, 445, 467, 468, 479, 480, 505, 506`), on
`ref`, `available_task`, `compute_task`, `store_task` and `validation_task` alike, changes from
`.hex` to `.hex()`. Nothing else in those lines.

- **Why `.hex()` and not the ref itself:** it is the one-token change 02's (m1) measured (log 02
  §5.2: it fails the fault-1 pin and nothing else), and `.hex()` strings compare by value. An
  `ObjectRef` key would work too (refs hash and compare by their bytes) but rewrites more.
- **Measured** by the planner on a scratch copy with every fix of §2 applied, with the stand-in's
  `fresh_refs` on: a lookup-only pool, a pool with an availability handler, compute → store →
  persist → validate, compute → store → persist with no validation, and a pool of `Blob`s each
  run to completion with the right `results`.

### 2.2 Fault 2: the post handler after a persist gets the persisted object

`:490`, `self._post_handler(obj)` → `self._post_handler(replacement_obj)`, in the `"store"` branch
with no validation handler (`:487-492`). Every exit then passes the object the pool holds for the
item. 02's (m2) is this change.

### 2.3 Fault 3: size `results` from the items already counted

`:138`, `range(len(task_list))` → `range(self._num_total_items)`. 02's (m3) is this change.

### 2.4 Fault 4: the constructor's handler checks (U8)

U8, taken 2026-10-10 as recommended (option (b)), with two amendments the user took the same day:
every argument check raises **`ValueError`**, and the check for an argument with no compute handler
covers **all four compute-path arguments**.

Replace the two checks at `:94-102` with:

- **No compute handler** (`compute_handler is None`):
  - a `store_handler` or `persist_handler` **left at its default** resolves to `None`. "Left at
    its default" is tested by identity: `store_handler is _default_store_handler`,
    `persist_handler is _default_persist_handler`. The defaults in the signature do not change, so
    `inspect.signature(RayWorkPool)` is as it was. (A caller who passes the private default
    function explicitly is treated as having left it out; that is harmless and is not tested.)
  - then each of `store_handler`, `persist_handler`, `validation_handler` and `label_builder`, in
    that order, that is not `None` raises `ValueError` with the message
    `f"No compute handler was supplied, so {name} would never be called; leave it out, or pass None"`.
- **A compute handler** (anything else, the default included): each of `store_handler` and
  `persist_handler`, in that order, that is `None` raises `ValueError` with the message
  `f"A compute handler was supplied, so {name} must not be None; leave it out to use the default"`.

Write the checks as the planner did, with a loop over `(name, value)` pairs, so that each message
is one f-string; `black` leaves each message on one line. The resolved values are what the
constructor stores in `self._store_handler` and `self._persist_handler`.

**Why the resolution matters for the printed lines.** The store segment of the queued and completed
messages is gated on `self._persist_handler is not None` (`:173`, `:210`). Because the default
resolves to `None` without a compute handler, a lookup-only pool prints exactly the same lines
whether it passes `persist_handler=None` (SGK, SI), `store_handler=None` alone (CPBH), or neither.
Measured: the three spellings print identical lines in a titled run. If the default were kept
instead, CPBH's spelling would print a `0 store` segment.

**What this does to the clients** (measured read-only through `git` and `ast` at SGK `b510bc9`,
CPBH `52142d7`, SI `7bb3efd`, outside each client's `RayTools/`, tests, `docs/` and `prompts/`):
every one of the 87 call sites constructs under the new checks. The 70 lookup-only sites pass
`compute_handler=None`, with `store_handler` and `persist_handler` each `None` or left out, and
`validation_handler` and `label_builder` each `None` or left out. The 17 compute sites pass no
`None` for either handler. No client catches `RuntimeError` or `RuntimeWarning` around a pool. So
**no client must change anything**, and 04 is not split (README §2, row 04's note).

**What becomes unconstructible:** a pool with a validation handler, a label builder, or an explicit
store or persist handler, but no compute handler. Each was silently ignored before. No client
builds one. `test_printed_lines.TestStatusMessages`' "validation only" case is such a pool (§3.4).

### 2.5 The sizes

After the handler checks, each of `create_batch_size`, `process_batch_size` and `max_task_queue`,
in that order, that is below 1 raises `ValueError` with the message
`f"{name} must be at least 1, not {value!r}"`. Nothing checks their type, and the three
notification settings are not checked.

- **Why:** with `max_task_queue=0` or `create_batch_size=0`, `run()` never ends; with
  `process_batch_size=0` and work in flight, `ray.wait` raises (the board's issue).
- **The clients:** every literal size at the 87 sites is at least 1. SI passes `max_task_queue` by
  name at three sites, and both batch sizes by a call at one; this prompt cannot read their values
  and does not need to.

### 2.6 Fault 5: the messages and the licence header (U11)

- **The messages** are §2.4's and §2.5's. None says "maker". The two old messages go.
- **The header** (U11, taken 2026-10-10): CPBH's and SI's copies of the module carry the same
  14-line Apache 2.0 header, byte for byte (`git -C …/StochasticInstantons show
  7bb3efd:RayTools/RayWorkPool.py | head -14`; CPBH `52142d7` is identical; SHA-256 of the 14
  lines with their newlines `e73e9334…e1ab9`). It begins `# (c) University of Sussex 2026` and
  `# Created by David Seery`. It goes, byte for byte, then one blank line, at the top of **all four
  package modules**: `RayWorkPool.py`, `_timing.py`, `contract.py` and `__init__.py`. Not on the
  tests. Copy it from SI's file through `git show`; do not retype it. `black` leaves the four files
  unchanged with it (measured).

### 2.7 The text the fixes make untrue

Each of these becomes false when the fixes land. Reword it, and change nothing else in it:

- `RayWorkPool.py:423-424`, the comment kept from SGK: "…submit a store request to the Datastore
  service." → "…submit a store request to the datastore."
  (`[01-a-kept-comment-names-the-datastore-service]`).
- `contract.py`'s docstring: "or who passes `persist_handler=None`" → a pool with no compute
  handler, which uses neither default (§2.4).
- `test_standins.py:116`, the comment "the bound method the pool keys on differs": the pool no
  longer keys on it. The assertion stays; it is a fact about Ray.
- The docstrings of every test §3 changes, and the two modules' docstrings
  (`test_inherited_faults.py`, `test_construction.py`), which say the tests pin the faults "as
  they behave" and that 04 inverts them.

The comment at `:440` ("a compute handler was supplied, so a persist handler must have been also")
stays: it is now enforced.

### 2.8 The equivalence check is retired at `v0.1.0`

As DatastoreKit retired its own when its fixes began (its U27; README §5 rule 8 here ends at 03):

- **Run it once, before any change**: `./venv/bin/python docs/extraction/compare_with_source.py`
  exits 0 with 572 identical, 2 D-imp, 1 D-pool, 4 D-int, 12 declared files, 0 undeclared. Its
  whole output goes in the log. **This is its last run.** It is not run after the change, when it
  fails by design.
- `docs/extraction/compare_with_source.py` gains one paragraph at the top of its docstring: it
  checks the package as tagged `v0.1.0`, the last tree that equals its source up to the classes
  below; it was retired there (README §5 rule 8; prompt 04 §2.8), since 04 changes the module in
  its own right; if it is run again, run it on that tag, for example from a `git worktree` of
  `v0.1.0`. Nothing else in the script changes.

---

## 3. The tests

The suite is **116** before. It rises by the five new tests below to **121**; the log gives it by
module. A count that falls is a stop. Every test that changes keeps its class.

### 3.1 `test_inherited_faults.py`: the pins become guards

The module docstring says each test now guards the fix of the board's fault, and names the board's
§4. Each test is renamed and inverted; its docstring names its (now resolved) issue and says what
the unfixed code did.

| Old name (02) | New name | What it asserts |
|---|---|---|
| `test_fault_in_flight_work_is_keyed_on_a_bound_method` | `test_fresh_refs_from_wait_complete_every_path` | with `fresh_refs`, one `subTest` per path of §2.1 (lookup-only; availability handler; compute with validation; compute without; `Blob`s), each running to completion with the expected `results` |
| `test_fault_post_handler_after_persist_gets_the_unpersisted_object` | `test_the_post_handler_after_persist_gets_the_persisted_object` | at exit 4 the post handler is given an object whose `store_id` is 1001, and it **is** `results[0]` |
| `test_fault_store_results_sizes_from_len_of_the_task_list` | `test_store_results_accepts_a_generator_task_list` | a generator with `store_results=True` constructs, runs, and fills `results` in order |
| `test_fault_persist_handler_without_compute_raises_runtime_warning` | `test_a_lookup_only_pool_needs_no_persist_handler` | `compute_handler=None` alone constructs and runs, and its queued message is `0 lookup` (no store segment) |
| `test_fault_store_handler_none_with_compute_fails_at_first_compute` | `test_store_handler_none_with_compute_is_refused_at_construction` | `ValueError` at construction, with §2.4's message; no `wait` call, no datastore call |

The stand-in is shared across a test's `subTest`s: assert on each run's own `results` and lines,
not on cumulative logs.

**One new test**, for fault 5's header: `test_every_package_module_carries_the_licence_header`. It
reads the first 15 lines of each of the four package modules (found from `raypoolkit.__file__`'s
directory, not hard-coded paths) and compares them with the header and its blank line, held in the
test as a constant.

### 3.2 `test_construction.py`

The module docstring loses its "maker" paragraph. `COMPUTE_WITHOUT_PERSIST` and
`PERSIST_WITHOUT_COMPUTE` are replaced by the two message templates of §2.4 and the one of §2.5.

| Test | Change |
|---|---|
| C1 `test_compute_handler_without_persist_handler_raises_runtime_error` | becomes `test_a_compute_handler_with_persist_handler_none_raises_value_error`: `type(...) is ValueError`, the message whole |
| C2 `test_persist_handler_without_compute_handler_raises_runtime_warning` | becomes `test_an_explicit_compute_path_argument_without_a_compute_handler_raises_value_error`: one `subTest` for each of the four arguments, given a callable with `compute_handler=None`, the message whole |
| *new* C5 | `test_a_compute_handler_with_store_handler_none_raises_value_error` |
| *new* C6 | `test_a_pool_without_a_compute_handler_constructs_however_it_is_spelled`: four `subTest`s, `compute_handler=None` with nothing else, with `persist_handler=None`, with `store_handler=None`, with both; each constructs and its queued message is `0 lookup` |
| *new* C7 | `test_a_size_below_one_raises_value_error`: each of the three sizes at 0 and at -1, the message whole; and each at 1 constructs |
| `test_neither_handler_constructs`, `test_both_handlers_construct` | unchanged |

The queued message is `_build_queued_status_message()`, a seam 02 §2.2 already allows. No new
white-box seam: no test reads `_store_handler` or `_persist_handler`.

### 3.3 `test_run_paths.py`

- **S4**, `test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`: the
  post handler's object **is** the persisted object (`results[0]`, `store_id` 1001), not the one
  the compute ran on. The name stays; the docstring drops "the board's fault 2" for "fault 2,
  fixed".
- **X1**, `test_an_unexpected_item_type_raises`: seeds `_inflight` and `_data` under `ref.hex()`
  only; the bound-method key and the docstring's sentence about it go.

### 3.4 `test_printed_lines.py`

- `TestStatusMessages.HANDLER_SETS` loses "validation only", which no longer constructs (§2.4),
  and gains "lookup only, nothing passed" (`{"compute_handler": None}`, `["lookup"]`) and "lookup
  only, store_handler=None" (`["lookup"]`). The "compute" and "every handler" cases still show the
  validation segment absent and present. Subtests do not change the count.
- **One new test**, `TestProgressAndCompletion.test_a_lookup_only_pool_prints_the_same_lines_however_its_handlers_are_spelled`:
  the run of `test_a_lookup_only_run_notifying_on_every_pass`, built three ways (§2.4's three
  spellings), prints the same nine lines, which equal that test's.
- **Every other test in the module passes unchanged.** That is the check that no printed line
  moved (README §5 rule 7). If one fails, stop.

### 3.5 The planner's measurement of what flips

With every change of §2 applied to a scratch copy and the suite unchanged, 11 of the 116 fail:
the five fault pins; C1 and C2; S4; and the three `TestStatusMessages` tests, each in its
"validation only" subtest only. X1 passes (it seeds both keys). Nothing else fails. If the agent's
first run of the unchanged suite on the fixed module fails anything outside these, stop.

---

## 4. Verification

1. **The suite**, from the repository root: in `venv/` (3.12.15 / 2.43.0) and in a fresh scratch
   venv at the high end (3.13.16 / 2.55.1, made with `uv` as 03 made its, the package installed
   editable in one resolve with the pins). Each gives `Ran 121 tests … OK` (or the log's count,
   if the agent's differs and says why). No Ray process before or after.
2. **The check, once, before any change** (§2.8), its whole output in the log.
3. `./venv/bin/black --check raypoolkit docs` (25.1.0) is clean.
4. **The deliberate-breakage record.** Each item is a diff against this prompt's final tree,
   exactly as applied, with the tests it fails; checked with `git apply --check` and `-R --check`,
   replayed in `bash`, run with the whole suite under a timeout (02's driver pattern; the spin cap
   still applies), never committed, `git status` clean after each. Expected failures are the
   planner's; the log lists what actually fails.
   - **(r1)** the 26 keys back to `.hex`: fails `test_fresh_refs_from_wait_complete_every_path`,
     and X1 (now a `KeyError`);
   - **(r2)** fault 2's call back to `obj`: fails the fault-2 guard and S4;
   - **(r3)** `len(task_list)` restored: fails the fault-3 guard;
   - **(r4)** the two default resolutions removed: fails C6, the fault-4a guard and the
     printed-lines spelling test;
   - **(r5)** the store default resolved but not the persist default: as (r4), from the persist
     side;
   - **(r6)** the compute-branch `None` check removed: fails C1, C5 and the fault-4b guard;
   - **(r7)** `validation_handler` and `label_builder` dropped from the no-compute check: fails
     C2's two subtests for them;
   - **(r8)** `value < 1` → `value < 0`: fails C7's zero cases;
   - **(r9)** one message says "maker" for "handler": fails its message test;
   - **(r10)** `_timing.py`'s header removed: fails the header test.
   Each must fail at least one test. One that fails none is a stop.
5. **The guards fail on `v0.1.0`.** Check out `v0.1.0`'s `raypoolkit/RayWorkPool.py` over the
   fixed one (`git show v0.1.0:raypoolkit/RayWorkPool.py > raypoolkit/RayWorkPool.py`), run the
   whole new suite, record every failing test, and restore. Every guard of §3.1 and every new or
   changed test of §3.2–§3.4 fails (the header test too, for `RayWorkPool.py` alone, since the
   other three keep theirs), except any the log explains. `git status` is clean after.

---

## 5. Acceptance

1. §2's changes, and nothing else, in the package; §3's in the tests; §2.8's paragraph in the
   check.
2. The suite passes at both ends, at 121 or the log's count.
3. Every printed-line test of 02 passes unchanged, but for §3.4's `HANDLER_SETS` edit.
4. (r1)–(r10) each fail what the log says; §4.5's run on `v0.1.0`'s module fails the guards.
5. **The records**, in the same commit:
   - the log, `logs/04-fix-the-inherited-faults.md`, per README §5.1. It also has:
     - the check's last output (§2.8);
     - the diff of `raypoolkit/RayWorkPool.py` against `v0.1.0`, whole;
     - each closed issue with the lines that fix it, in the new module, and the test that guards
       it;
     - the counts by module, before and after;
     - (r1)–(r10) and §4.5's run;
     - every venv's versions and verdict;
   - the board: the header; §1's row for 04 (landed, "this commit", 116 → 121); the seven
     issues moved from §3 to §4, each with a dated **Resolved (04)** line naming its fix and its
     guard; and U8 and U11 shown as applied;
   - `docs/OPEN_ISSUES.md`: the seven rows deleted, **8 → 1** open (the one left is
     `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`, proposed for 05);
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The first run of the unchanged suite on the fixed module fails anything outside §3.5's eleven.
- A printed-line test other than §3.4's `HANDLER_SETS` subtests fails, or passing one would need
  a line the pool prints to change.
- A breakage of §4.4 fails no test, or the suite count falls.
- Passing anything would need a change to a file not in §7, a new file under `raypoolkit/`, or a
  white-box seam beyond 02 §2.2's.
- The header in SI's and CPBH's copies is not as §2.6 says.
- Anything would push, tag, change `pyproject.toml`, `README.md` or `PROVENANCE.md`, start Ray, or
  edit, run or import SecondaryGWKit, ChamPBH, StochasticInstantons or DatastoreKit (reading SI's
  header and DatastoreKit's docstring through `git show` is allowed).

---

## 7. What this prompt does not do

- **Files it changes:**
  - `raypoolkit/RayWorkPool.py`, `raypoolkit/_timing.py`, `raypoolkit/contract.py`,
    `raypoolkit/__init__.py`;
  - `raypoolkit/tests/test_inherited_faults.py`, `test_construction.py`, `test_run_paths.py`,
    `test_printed_lines.py`, and the one comment in `test_standins.py`;
  - `docs/extraction/compare_with_source.py`, its docstring only;
  - the log, the board, `prompts/INDEX.md` and `docs/OPEN_ISSUES.md`.
- It adds no file under `raypoolkit/`, and changes no other test, nor `standins.py`.
- It does not change `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `LICENSE`,
  `.gitignore`, the workflow or the campaign README.
- It fixes nothing else, including `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`
  (05).
- It makes no tag and pushes nothing. After its review, pushing its commit is put to the user, and
  CI runs there; `v0.2.0` is 05's.
- It writes no orchestration note.

---

## 8. The log and the board

`logs/04-fix-the-inherited-faults.md`, using README §5.1, with the additions of §5.5. The check's
output has its place for the last time (§2.8).

`IMPLEMENTATION_STATE.md`: the header, §1's row for 04 (landed, commit, log, suite), and §3/§4 for
the seven issues.
