# extraction campaign — implementation state

**Last updated:** 2026-10-10 · **Status: IN PROGRESS — 3 of 7 prompts written (01–03), 01 landed
(`49f3ddf`) and reviewed, 02 landed (`b9f6dec`) and reviewed, 03 landed (`4e90a8a`) and
reviewed.** G1 holds at SGK `b510bc9`, the import commit. The user took U1–U3 at set-up and U4–U5
for 01, U6 and U9 for 02 and U7 for 03, all on 2026-10-10 and as recommended (README §6.2; U9 as
amended at 02's writing). The package `raypoolkit` is at `0.1.0`, declaring Python `>=3.12` and
`ray>=2.43`, with its test package excluded from the wheel; `compare_with_source.py` exits 0; the
suite is 116 tests, with no Ray cluster, passing at 3.12.15 / 2.43.0 and 3.13.16 / 2.55.1, and
faults 1–5 are each pinned as they behave. 8 issues are open. The U5 freeze is in force.

**`v0.1.0` is ready to be tagged on 03's commit, `4e90a8a`, once CI (`.github/workflows/tests.yml`)
passes there at both ends. No tag has been made, and nothing has been pushed** (README §5 rule
10). The push, the CI run and the tag are put to the user (the review of 03, below).

**Campaign:** [`README.md`](README.md) ·
**Source:** SecondaryGWKit's `RayTools/RayWorkPool.py`, blob `b4666fa` (G1) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.1

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Made by the user (README §6.1):**

| Decision | Decided |
|---|---|
| **D1** | Extract `RayWorkPool` as a separate, reusable component (2026-10-10) |
| **D2** | DatastoreKit's: the datastore layer first; the pool is this separate unit of work (2026-10-07) |

**Put to the user (README §6.2):**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** name | RayPoolKit / `raypoolkit`, public `ds283/RayPoolKit` | **taken** 2026-10-10 |
| **U2** source | SGK's copy, imported faithfully | **taken** 2026-10-10 |
| **U3** dependency | none on `datastorekit`; the pool typed by a `Protocol` | **taken** 2026-10-10 |
| **U4** module name | keep `RayWorkPool.py`; re-export the class from the root | **taken** 2026-10-10 |
| **U5** freeze | no client edits its `RayTools/` until it adopts | **taken** 2026-10-10; in force from 01's commit |
| **U6** Ray stand-in | real `ObjectRef(bytes)`; `ray.wait` / `ray.get` replaced in-process | **taken** 2026-10-10 |
| **U7** versions | Python ≥3.12, Ray ≥2.43; tested 3.12.15/2.43.0 and 3.13.16/2.55.1 | **taken** 2026-10-10 |
| **U8** handler checks | defaults apply only with a compute handler (option b) | open, for 04 |
| **U9** printed lines | pinned, wording and layout, against a scripted clock; the three consumer patterns checked | **taken** 2026-10-10, as amended |
| **U10** CPBH shim | none | open, for 06 |

## 1. Prompts

| # | Prompt | Status | Commit | Suite |
|---|---|---|---|---|
| 01 | [`01-import-the-pool.md`](01-import-the-pool.md) | **landed** 2026-10-10 ([log](logs/01-import-the-pool.md)), reviewed | `49f3ddf` | 0 → 3 |
| 02 | [`02-the-test-suite.md`](02-the-test-suite.md) | **landed** 2026-10-10 ([log](logs/02-the-test-suite.md)), reviewed | `b9f6dec` | 3 → 116 |
| 03 | [`03-supported-versions-and-ci.md`](03-supported-versions-and-ci.md) | **landed** 2026-10-10 ([log](logs/03-supported-versions-and-ci.md)), reviewed | `4e90a8a` | 116 → 116 |
| 04 | `04-fix-the-inherited-faults.md` | not written | — | — |
| 05 | `05-release-v0.2.0.md` | not written | — | — |
| 06 | `06-the-adoption-checklists.md` | not written | — | — |
| 07 | `07-verification-and-close-out.md` | not written | — | — |

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`310db6e`),
used for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`319099a`), used for 02;
[`orchestrator/prompt-03.md`](orchestrator/prompt-03.md) (`e136eee`), used for 03.

**Orchestrator review of prompt 01 (2026-10-10).** Dispatched from `310db6e` to one Opus
subagent, with the note's §0 facts, its one addition (breakage (h)) and its two recommendations.
Reviewed against its commit `49f3ddf`, with nothing landed after it. **Every check of the note's
§3 passed**, and acceptance 1–3 are met. No stop condition fired.

*At dispatch.* The note's gate held at `310db6e`. The tree was clean, the only worktree was this
checkout, and `raypoolkit` was not installed in `venv/`. SGK's `HEAD` was `b510bc9`, with
`RayTools/RayWorkPool.py` at blob `b4666fa`. No Ray process was up.

*The checks.*
1. **Scope.** `49f3ddf` touches 13 files: the prompt's §6 list (`pyproject.toml`, the six files
   under `raypoolkit/`, `compare_with_source.py`, `PROVENANCE.md`), the log, this board,
   `prompts/INDEX.md` and the index. No `venv/`, `*.egg-info` or scratch file.
2. **E1, the files.** `git ls-files raypoolkit` gives exactly `__init__.py`, `RayWorkPool.py`,
   `_timing.py`, `contract.py`, `tests/__init__.py` and `tests/test_package_imports.py`.
   `__init__.py` binds the two names and `__all__`, and nothing else. `contract.py` imports only
   `typing` and `ray`, is not `runtime_checkable`, and names no client or `datastorekit` class.
3. **E2, by running.** The check exits 0: 572 identical lines, 2 D-imp and 1 D-pool in
   `RayWorkPool.py`; 4 D-int definitions and the byte-for-byte span in `_timing.py`; 4 declared
   files; 0 undeclared. The counts equal the log's.
4. **E2, by reading.** The script was read in full. The blob is checked first. D-imp is an exact
   two-entry `ast` map of whole `ImportFrom` statements, with no alias. D-pool is the one
   identifier on a line that parses as a lone annotated parameter with no default. There is no
   D-fmt rule and no line number in any rule. Only equal-length `replace` runs are classified, so
   additions and deletions never are. D-int compares `ast` segments, the body's names in order, the
   span byte for byte, and only blank lines between docstring and span.
5. **E3, the check bites.** (a)–(h) were replayed from the log in `bash`. Each exits 1 and names
   the line or file, as logged. The orchestrator's own: SGK's `WallclockTimer` (`utilities.py:6-17`,
   with its two imports) appended to `_timing.py` fails on BODY and SPAN. `git status` was clean
   after each.
6. **E4, the guard.** `Ran 3 tests … OK`. Test 1 uses `ast.walk` over every module under
   `raypoolkit/`, tests included, resolves relative imports, and names file, line and module. Tests
   2 and 3 run `sys.executable -I` from a `tempfile` directory, with a 300 s timeout. Test 3's
   docstring states the patching rule.
7. **E5, isolation.** From the scratchpad, with `env -u PYTHONPATH` and `-I`, the prompt's §3.1
   import succeeds and leaves `ray.is_initialized()` false; `import RayTools` and
   `import datastorekit` each fail with `ModuleNotFoundError`.
8. **E6, the pins.** The `numpy` diff fails test 1 alone; the re-export removal fails tests 2 and
   3; the class-only variant fails test 3 alone. The `datastorekit` diff in `contract.py` stops
   discovery at load (`ERROR: raypoolkit.tests`), since the package imports `contract`. Run as a
   script, the module fails all three, test 1 naming `raypoolkit/contract.py:9`. That is the log's
   account (deviation 6, STRUCTURALLY REQUIRED). The suite is 3 again after each.
9. **E7, the records.** The log has every section of README §5.1, `pip freeze` (Python 3.12.15,
   `ray==2.43.0`, `black==25.1.0`, the editable `raypoolkit`), the check's whole output, the counts
   0 → 3, and the five faults' package lines. `PROVENANCE.md` has the six items of the prompt's
   §2.8, with both subject lines right. The index counts 6 rows, matching its header.
   `black --check raypoolkit docs` (25.1.0) is clean.

*Findings.*
- **One issue opened by the agent, and kept:** `[01-a-kept-comment-names-the-datastore-service]`
  (`RayWorkPool.py:424`). The note expected none; the agent's reading of `CLAUDE.md` is right, and
  the comment is SGK's text, which rule 8 keeps until 04.
- **A correction to the note.** Its §0 put fault 2's post-handler call at `:489`; that is the
  `elif`, and the call is at `:490` (the log, and §3 below, are right). README §0.2's and §3's
  "SGK `:488-491`" is the same span read one line short; the board's **Package** line, `:487-492`,
  supersedes it.
- **Put to the user, not acted on:** `CLAUDE.md` says the package names no client module "in code,
  strings, docstrings or comments", but two mentions inside `raypoolkit/` are required by the
  prompt: `_timing.py`'s docstring names SGK's `utilities.py` (D-int), and the guard's
  `FORBIDDEN_ROOTS` names `Datastore`, `RayTools` and `utilities` (§2.7 test 2). Whether
  `CLAUDE.md` excepts provenance and guard text, or 04 rewords them, is the user's decision.
  **Taken 2026-10-10, at 02's writing:** `CLAUDE.md` excepts both; nothing is opened.

*Residue fixed in the follow-up commit.* "this commit" → `49f3ddf` on this board, in the log and
in `prompts/INDEX.md`; README §2's status and header for 01; this review and the notes line.

**Orchestrator review of prompt 02 (2026-10-10).** Dispatched from `319099a` to one Opus
subagent, with the note's §0 facts and its seven clarifications and additions. Reviewed against its
commit `b9f6dec`, with nothing landed after it. **Every check of the note's §3 passed**, and
acceptance 1–3 are met. No stop condition fired.

*At dispatch.* The note's gate held at `319099a`. The tree was clean, the only worktree was this
checkout, and `git diff 49f3ddf -- raypoolkit/RayWorkPool.py` was empty. SGK's `HEAD` was
`b510bc9`, with `RayTools/RayWorkPool.py` at blob `b4666fa`. No Ray process was up.

*The checks.*
1. **Scope.** `b9f6dec` touches 12 files: the eight new files under `raypoolkit/tests/`,
   `compare_with_source.py`, the log, this board and `prompts/INDEX.md`. `git diff 49f3ddf b9f6dec`
   over `RayWorkPool.py`, `_timing.py`, `contract.py`, `__init__.py` and `test_package_imports.py`
   is empty.
2. **E1, the stand-ins, by reading.** `standins.py` was read in full. `wait` applies Ray 2.43.0's
   checks in Ray's order with Ray's types (single ref, list, negative `timeout`, elements, empty →
   `([], [])`, duplicates, `num_returns`), records each call, honours `order` and `fresh_refs`, and
   raises past a cap of 1,000 calls. `get` returns a pickle copy and names an unminted ref. The work
   objects and the datastore pool are at module level and reach the stand-in through `active_ray()`.
   `now()` reads the clock without advancing it. `PoolTestCase` patches the four string targets and
   nothing else, asserts `ray.is_initialized()` false at tear-down, and has no `test_` method.
3. **E2, by running.** Twice, in a fresh shell: `Ran 116 tests … OK`. Per module, by the loader:
   3, 30, 12, 20, 22, 7, 17, 5, as logged. No Ray process before or after.
4. **E3, the inventory, by reading.** The log's table has a row for each of §2.4's 41 IDs, and for
   D1–D3, P0 and Z1–Z5. Six tests were read in full and reach their rows: L5, S4 with P1 (and P0),
   R9 (`wait_calls == [(0, 0)]`), N3/N4, N5 (`test_the_available_rate_is_per_interval`) and X1.
   The white-box seams are only §2.2's; X1 seeds `_data` under both `ref.hex` and `ref.hex()`
   (deviation 12), which is within the seam.
5. **E4, the log's mutations, by replaying.** All 96 diffs were extracted from the log's text and
   replayed, one at a time, from a clean tree, each with the whole suite under a 300 s timeout. Each
   of the 89 mutations and the stand-in diffs (s1) and (s2) failed **exactly** the set of tests the
   log lists for it. E1–E4 passed, as logged. (s3) was applied and reverted without a run. No
   timeout; the tree was clean after each; no Ray process afterwards.
6. **E4, the orchestrator's own mutations.** (o1) `:482` `(idx, replacement_obj)` → `(idx, obj)`
   fails 3 tests; (o2) `:419` without `and self._store_results` fails 1; (o3) `:555` `= now_time`
   fails 8; (o4) `:286` without `contents=…` fails the 5 R6 tests, so R6's message is pinned whole.
7. **E5, the faults.** `TestInheritedFaults` has the prompt's five names, each docstring naming its
   board issue and saying it pins the fault. (m1) fails the fault-1 test alone, (m2) the fault-2
   test and S4's identity test, (m3) the fault-3 test alone. §3 below has a dated "Pinned (02)" line
   on each of faults 1–5.
8. **E5, the printed lines.** The three patterns are the prompt's, character for character, and no
   new test file names a client. The orchestrator re-rendered three of the agent's whole-run tests
   (the compute-with-validation run, the per-interval available rate, the percentage run) on its own
   scratch stand-in: each matches the agent's expected lines exactly, including `514.3/hr` and
   `400/hr`, which the agent first derived wrongly by hand and corrected to the module (log §3.1).
9. **E1 and E5, the stand-ins bite.** (s1) fails five tests, the all-`None` one with Ray's
   `ValueError`; (s2) fails two, so no issue arises. (s3)'s account was checked by reading: only
   `TestRayInitGuard` calls the real `ray.get` or `ray.wait`.
10. **E6 and E7.** The check exits 0: 572 identical, 2 D-imp, 1 D-pool, 4 D-int, 12 declared files,
    0 undeclared; its diff is the eight `NO_SOURCE` lines. The guard passes over the new modules.
    `black --check raypoolkit docs` (25.1.0) is clean. The log has every section of README §5.1 and
    the prompt's §4.3 additions.

*Findings.*
- **One issue opened by the review:** `[02-the-constructor-does-not-check-its-sizes]` (§3 below).
  The agent recorded it as an observation only (log 02 §6.1), following the note's clarification 1,
  which said "an observation for the log, not a branch to pin". The note did not mean "no issue",
  and `CLAUDE.md`'s rule 4 asks for one; the wording was the orchestrator's.
- **Not opened:** the four equivalent mutations (log 02 §5.3) are redundant or unobservable code,
  not defects; the log records them for 04.

*Residue fixed in the follow-up commit.* "this commit" → `b9f6dec` on this board, in the log and
in `prompts/INDEX.md`; README §2's status and header for 02; this review and the notes line.

**Orchestrator review of prompt 03 (2026-10-10).** Dispatched from `e136eee` to one Opus
subagent, with the note's §0 facts and its eight clarifications. Reviewed against its commit
`4e90a8a`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–5 are met. No stop condition fired.

*At dispatch.* The note's gate held at `e136eee`. The tree was clean, the only worktree was this
checkout, there was no tag, and `origin/main` was `97f9ff0`. The suite gave 116 and the check
exited 0 at `c73fc91`, and `e136eee` touched only `prompts/`. No Ray process was up.

*The checks.*
1. **E1, scope.** `4e90a8a` touches 7 files: `pyproject.toml`, `.github/workflows/tests.yml`,
   `README.md`, the log, this board, `prompts/INDEX.md` and the index. `git diff c73fc91 4e90a8a`
   over `raypoolkit`, `docs/extraction`, `PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore` and
   the campaign README is empty. No tag; `git ls-remote origin` shows `main` at `97f9ff0` and no
   tag; no `build/` or `dist/` in the repository.
2. **E2, `pyproject.toml`.** Three changes: `version = "0.1.0"`, `"ray>=2.43"`, the `exclude` line.
3. **E2, the suite.** `venv/`: `Ran 116 tests … OK`, `importlib.metadata` `0.1.0`,
   `['ray>=2.43']`. In the orchestrator's own fresh `uv` venvs, the repository installed editable
   in one resolve with the pins: 116, OK, at 3.12.15 / 2.43.0 and at 3.13.16 / 2.55.1. No Ray
   process before or after.
4. **E3, the distribution, rebuilt from the commit.** A `git archive 4e90a8a` export with no file
   copied in builds `raypoolkit-0.1.0-py3-none-any.whl`, 12,016 bytes, the log's 9 entries; its
   four modules are byte for byte the commit's, and its `METADATA` says `0.1.0`, `>=3.12`,
   `ray>=2.43`. Its SHA-256 (`5bc9885…`) differs from the agent's (`875fe53…`), as the note
   expected: the export's file times are the commit's. Installed into a fresh 3.13.16 / 2.55.1
   venv and run from an empty directory with `-I`: every import of the prompt's §2.4 succeeds from
   `site-packages`, `ray.is_initialized()` is false, and `import raypoolkit.tests` raises
   `ModuleNotFoundError`.
5. **E4, the workflow.** The comment, the three triggers, one job `suite` on `ubuntu-24.04`,
   `fail-fast: false`, a matrix of two entries keyed `end` whose six values load as strings equal
   to §2.3, the six steps with `@v7` for both actions, `black` on `low` only, `permissions:
   contents: read`; nothing else. `yaml.safe_load` parses it.
6. **E4, the replay.** Log §3.3 gives a command for each of steps 3–6 at both ends, and names the
   steps with no local counterpart (deviation 10).
7. **E5, the breakage.** The five diffs were extracted from the log's text, and each applies with
   `git apply --check` at `4e90a8a`. Replayed in throwaway venvs and fresh exports of the commit:
   (a) fails the guard's tests 2 and 3 and only those; (b) and (c) refuse, naming `ray>=2.43` and
   `Python>=3.13`; (d) gives 5 entries and no module, and `import raypoolkit` fails; (e) ships 10
   test files and `raypoolkit.tests` imports; (f)'s second wheel has 19 entries, 10 of them tests.
   The orchestrator's own, `"ray>=2.56"` in an export, refuses `ray==2.55.1` at the high end. The
   repository's `git status` was clean throughout.
8. **E6, the README.** The constructor's 18 parameters, the defaults (the three handler defaults
   by what their bodies do) and the handlers' arguments agree with the module; the claims spot-read
   against it (the task builder's four returns, the available task's value unread, the persisted
   object's `available` check, the validation warning on `is not True`, the strict `>`
   notifications, `total_time`) hold. It states `persist_handler=None` for a lookup-only pool, the
   pinned install line and the editable-install warning, the range with Ray's effective 2.45.0 on
   3.13, and that newer releases are untested. The printed-line examples are lines of
   `test_a_lookup_only_run_notifying_on_every_pass`, the progress line through that test's own
   `progress(...)` helper. No fault is listed. Every relative link resolves to a tracked file.
9. **The check and the formatter.** The check exits 0: 572 identical, 2 D-imp, 1 D-pool, 4 D-int,
   12 declared files, 0 undeclared. `black --check raypoolkit docs` (25.1.0): 15 files unchanged.
10. **E7, the records.** The log has every section of README §5.1 and each of the prompt's §4.5
    additions, with §0's clarifications recorded as deviations 1–8. This board had the header, the
    "ready to be tagged" line, 03's row and the new §3 issue; the index counts 8 rows, matching its
    header; `prompts/INDEX.md`'s line says 03 landed.

*Findings.*
- **One issue opened by the agent, and kept:**
  `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` (§3 below). The orchestrator
  reproduced it: the repository's `raypoolkit.egg-info/` (its `SOURCES.txt` listing 10 test
  files) copied into a fresh export of `4e90a8a` gives a wheel of 19 entries, 10 of them tests, with
  setuptools' "absent from the `packages` configuration" warning; `include-package-data = false`
  gives 9. A client's `git+…@v0.1.0` install builds from a fresh clone, so `v0.1.0` does not wait
  for it.
- **Two corrections to the note, from the log:** `pip freeze`'s editable line names the `HEAD` at
  the time of the freeze, not of the install (log 03 §6.3); and `uv build` runs setuptools under
  `uv`'s default Python, 3.14 here, which does not change a pure-Python wheel (§6.2).
- **Not opened:** the README gives the protocol's method as `object_store(obj)`, as `contract.py`'s
  docstring does, while its signature names the parameter `objects` (DatastoreKit's name). The pool
  calls it positionally with one object, so nothing behaves differently.

*Residue fixed in the follow-up commit.* "this commit" → `4e90a8a` on this board, in the log and
in `prompts/INDEX.md`; README §2's status and header for 03; this review and the notes line.

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1** | **holds** 2026-10-10, re-checked at 01's writing and again at its start: SGK `RayTools/RayWorkPool.py` is blob `b4666fa` at `b510bc9`, the import commit |
| **G2** | not yet (SGK adopts `v0.2.0`) |
| **G3** | not yet (CPBH adopts `v0.2.0`) |
| **G4** | not yet (SI adopts `v0.2.0`) |

## 3. Active and unresolved issues

The five `[00-…]` entries are inherited from the source and were opened at planning (README
§0.2, faults 1–5). Each is pinned as it behaves by 02 and fixed by 04 (README §2). Since 01, each
gives the **Package** lines where its fault sits in `raypoolkit/RayWorkPool.py`, read from the
package (log 01 §3.6); they equal SGK's at `b510bc9`, because 01 replaced lines one for one.

### `[00-in-flight-work-is-keyed-on-a-bound-method]`

**Opened:** 2026-10-10, at planning. **Owner:** 04.

**Package (01):** 26 lines keyed on `.hex`, `raypoolkit/RayWorkPool.py:260, 263, 266, 277, 322,
337, 338, 351, 352, 379, 381, 389, 390, 403, 409, 410, 434, 435, 444, 445, 467, 468, 479, 480, 505,
506`.

`RayWorkPool.run()` keys `_inflight`, `_data` and `_compute_data` on `ref.hex`, the bound method,
not on `ref.hex()` or the ref itself. Bound methods compare by the identity of `__self__`, so two
equal `ObjectRef`s that are distinct Python objects give unequal keys. Measured at Ray 2.43.0,
2.53.0 and 2.55.1: `ObjectRef(b) == ObjectRef(b)` and their hashes agree, but their `.hex` methods
do not compare equal.

*Impact.* None today: `ray.wait` returns the objects it was given, so every lookup finds its key.
A Ray release that returns fresh refs from `ray.wait`, or a stand-in that does, makes every
completed task a `KeyError`.

*Next step.* 04 keys the dictionaries on the ref itself (or `ref.hex()`), with a test whose
stand-in `ray.wait` returns equal but distinct refs.

**Pinned (02, 2026-10-10):** `raypoolkit/tests/test_inherited_faults.py`,
`TestInheritedFaults.test_fault_in_flight_work_is_keyed_on_a_bound_method`, as it behaves: with the
stand-in's `fresh_refs`, the first completed lookup raises `KeyError` from `self._data[ref.hex]`.
Changing all 26 keys to `.hex()` fails this test and no other (log 02 §5.2). 04 inverts it.

### `[00-a-post-handler-after-persist-gets-the-unpersisted-object]`

**Opened:** 2026-10-10, at planning. **Owner:** 04.

**Package (01):** `raypoolkit/RayWorkPool.py:487-492`: the `elif self._post_handler is not None:`
at `:489`, the call `self._post_handler(obj)` at `:490`.

In the `"store"` branch with no validation handler (SGK `RayWorkPool.py:488-491`), the post
handler is called with `obj`, the driver's copy from before the persist, not with
`replacement_obj`, the object the datastore returned with its `store_id` set. Every other exit
passes the current object.

*Impact.* Reachable at one client site, SGK `main.py:3247` (`postprocess_GkSourcePolicy`). That
handler reads only `policy`, `type` and `quality`, which `store()` sets locally, so it is correct
today. A post handler there that read `store_id` would see `None`.

*Next step.* 04 passes `replacement_obj`, with a test that a post handler after a persist sees the
replacement. 06's checklists re-measure the sites.

**Pinned (02, 2026-10-10):** `TestInheritedFaults.test_fault_post_handler_after_persist_gets_the_unpersisted_object`:
at exit 4 the post handler is given an object whose `store_id` is `None`, while `results` holds the
persisted one. Passing `replacement_obj` at `:490` fails it and S4's identity test,
`test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`.
04 inverts both.

### `[00-store-results-sizes-from-len-of-the-task-list]`

**Opened:** 2026-10-10, at planning. **Owner:** 04.

**Package (01):** `raypoolkit/RayWorkPool.py:138`.

With `store_results=True` the constructor sizes `results` from `len(task_list)` (SGK `:138`),
though it has already consumed `task_list` into `self._todo` and counted it. A generator or other
iterable without `len()` raises `TypeError`.

*Impact.* None known at a client: no client run is known to have raised it, but the planner did
not trace every `task_list` argument to its type (06 does). The constructor otherwise accepts any
iterable.

*Next step.* 04 sizes from `self._num_total_items`, with a test that passes a generator.

**Pinned (02, 2026-10-10):** `TestInheritedFaults.test_fault_store_results_sizes_from_len_of_the_task_list`: a
generator `task_list` with `store_results=True` raises `TypeError` at `:138`; without it, it runs.
Sizing from `self._num_total_items` fails this test alone. 04 inverts it.

### `[00-the-constructor-checks-its-handlers-unevenly]`

**Opened:** 2026-10-10, at planning. **Owner:** 04, under U8.

**Package (01):** the `RuntimeWarning` check at `raypoolkit/RayWorkPool.py:99-102` (raised at
`:100`); the store handler, never checked, is called at `:431`.

The constructor raises `RuntimeWarning`, an exception class, when a persist handler is set without
a compute handler (SGK `:99-102`). Since the default persist handler is not `None`, every
lookup-only pool must pass `persist_handler=None`. It does not check the converse for the store
handler: `store_handler=None` with a compute handler fails with `TypeError` at the first completed
compute, not at construction.

*Impact.* Every lookup-only site in SGK (44) and SI (12) carries `persist_handler=None` for this
reason. CPBH's 14 lookup-only sites do not, so under the package as imported each raises at
construction until CPBH changes it.

*Next step.* U8 is put when 04 is written; the recommendation (option b) makes the defaults apply
only with a compute handler, so no existing site has to change.

**Pinned (02, 2026-10-10):** `TestInheritedFaults.test_fault_persist_handler_without_compute_raises_runtime_warning`
(also `test_construction.TestHandlerChecks.test_persist_handler_without_compute_handler_raises_runtime_warning`,
with the message) and `TestInheritedFaults.test_fault_store_handler_none_with_compute_fails_at_first_compute`
(`TypeError` from `self._store_handler(obj, self._pool)` once the first compute completes). 04
inverts them under U8.

### `[00-messages-say-maker-and-the-module-has-no-licence-header]`

**Opened:** 2026-10-10, at planning. **Owner:** 04.

**Package (01):** "maker" at `raypoolkit/RayWorkPool.py:96` and `:101`; no licence header (`:1` is
`import time`).

The constructor's two messages say "compute maker" and "persist maker" for the handlers, and SGK's
module carries no licence header (CPBH's and SI's copies carry the Apache 2.0 header, and SI's
messages say "handler").

*Impact.* Cosmetic. The messages are not part of the printed-lines interface (`CLAUDE.md`); they
are exception text.

*Next step.* 04 rewrites the two messages and adds the header the repository's licence calls for.

**Pinned (02, 2026-10-10):** by `raypoolkit/tests/test_construction.py`'s message assertions,
`TestHandlerChecks.test_compute_handler_without_persist_handler_raises_runtime_error` and
`…_persist_handler_without_compute_handler_raises_runtime_warning`, which compare each message
whole (`COMPUTE_WITHOUT_PERSIST`, `PERSIST_WITHOUT_COMPUTE`). No test pins the absent header. 04
changes the two constants.

### `[01-a-kept-comment-names-the-datastore-service]`

**Opened:** 2026-10-10, by 01 (log 01 §5.1). **Owner:** 04.

**Package (01):** `raypoolkit/RayWorkPool.py:424`, a comment kept from SGK as it is (01 §2.4):
"…and then submit a store request to the Datastore service". `Datastore` is the name of SGK's
datastore package and class. `CLAUDE.md` says the package names no client class, module or package
in its comments. The module's other mentions (`:430`, `:451`, `:502`, `:574`) say "datastore" in
lower case, generically.

*Impact.* None on behaviour: it is a comment. It breaks a stated invariant of the package's text.

*Next step.* 04, which rewrites the module's wording for
`[00-messages-say-maker-and-the-module-has-no-licence-header]`, rewords the comment generically
("the datastore"). The printed lines are not affected.

### `[02-the-constructor-does-not-check-its-sizes]`

**Opened:** 2026-10-10, by the orchestrator's review of 02 (log 02 §6.1). **Owner:** 04, with
U8's handler checks.

**Package:** `raypoolkit/RayWorkPool.py:85-87` (the three sizes, unchecked); the loop at `:246`,
the batch guard at `:250`, the inner loop at `:252`, and `num_returns` at `:315`.

The constructor accepts any `create_batch_size`, `process_batch_size` and `max_task_queue`.
Measured by the orchestrator on a scratch stand-in at 02's dispatch: with `max_task_queue=0` or
`create_batch_size=0`, no task is ever built, so every pass calls `ray.wait([], num_returns=0)`,
which returns `([], [])`, and `run()` never ends. With `process_batch_size=0` and work in flight,
`num_returns` is 0 and `ray.wait` raises `ValueError`.

*Impact.* None known at a client: the defaults are 5, 1 and 200. A caller who passes 0 hangs a
driver with no message.

*Next step.* 04 raises `ValueError` at construction for a size below 1, with a test for each, as
part of the constructor checks U8 settles. No test pins the hang today (02 builds no such pool).

### `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`

**Opened:** 2026-10-10, by 03 (log 03 §6.1). **Owner:** not assigned; proposed for 05, the next
prompt that changes `pyproject.toml`.

**Where:** `pyproject.toml`'s `[tool.setuptools.packages.find]`, whose `exclude` keeps
`raypoolkit.tests` out of the packages but not out of the package data; and the gitignored
`raypoolkit.egg-info/` at the repository root, which every editable install rewrites.

setuptools reads an existing `raypoolkit.egg-info/SOURCES.txt` and merges it into the new one. The
repository's copy still lists the ten files under `raypoolkit/tests/`, carried from the manifests
written before 03's exclusion; a fresh export's lists none. Measured by 03 in scratch, never in the
tree: a fresh `git archive` export with 03's `pyproject.toml` and the repository's
`raypoolkit.egg-info/` copied in builds a wheel of 19 entries, 10 under `raypoolkit/tests/`,
shipped as package data of `raypoolkit` (`include-package-data` defaults to on), with setuptools
warning "Package 'raypoolkit.tests' is absent from the `packages` configuration". The exclusion
does not prevent it.

*Impact.* None on a client: a `git+…@v0.1.0` install builds from a fresh clone, which has no
`egg-info` (it is gitignored), as 03's release check did (9 entries). It is a second route for
03's hazard 2: a wheel built in a working tree, which `CLAUDE.md` and 03 already forbid, ships the
test package, with its patched `ray.init` and second `PoolTestCase`.

*Next step.* Set `[tool.setuptools]` `include-package-data = false` (the package has no data files;
`LICENSE` reaches the wheel's `dist-info/licenses/` either way). Measured by 03 in a scratch export
with the stale manifest: 9 entries and no warning. It changes `pyproject.toml`, so a prompt that
says so makes it, with the release check re-run; 03 could not (its §2.1: "Nothing else").

## 4. Resolved issues

None.
