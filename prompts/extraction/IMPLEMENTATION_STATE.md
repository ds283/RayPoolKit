# extraction campaign — implementation state

**Last updated:** 2026-10-10 · **Status: IN PROGRESS — 6 of 7 prompts written (01–06), 01 landed
(`49f3ddf`) and reviewed, 02 landed (`b9f6dec`) and reviewed, 03 landed (`4e90a8a`) and
reviewed; `v0.1.0` tagged; 04 landed (`0b6ffd2`) and reviewed, CI green; 05 landed (`eaef0ce`)
and reviewed, CI green; `v0.2.0` tagged; 06 written.** G1 holds at SGK `b510bc9`, the import commit. The user took U1–U3 at set-up and U4–U5
for 01, U6 and U9 for 02, U7 for 03, U8 and U11 for 04 and U10 and U12 for 06, all on 2026-10-10 and as recommended
(README §6.2; U9 as amended at 02's writing; U8 with two amendments); U8 and U11 are applied by 04.
The package `raypoolkit` is at `0.2.0`, declaring Python `>=3.12` and `ray>=2.43`, with its test
package excluded from the wheel and package data off, so that a stale `egg-info` manifest cannot
put the tests in a wheel (05). Since 04, faults 1–5 are fixed on `main`, with the constructor's
sizes checked, each fix guarded by a test that `v0.1.0`'s module fails; `README.md` and
`PROVENANCE.md` describe `v0.2.0` (05). `compare_with_source.py` is retired at `v0.1.0`. The suite is 121 tests, with no Ray cluster, passing at 3.12.15 / 2.43.0 and
3.13.16 / 2.55.1 (in CI on `0b6ffd2`, `914070c` and `eaef0ce`). No issue is open. The U5 freeze is in force.

**`v0.1.0` is released**: an annotated tag on 03's commit, `4e90a8a`, made at the user's
instruction on 2026-10-10 after CI passed there at both ends (run `38054782562`), and pushed with
`main` (README §5 rule 10). See *Release of `v0.1.0`*, below.

**`v0.2.0` is released**: an annotated tag on 05's commit, `eaef0ce`, made by the user on
2026-10-10 after CI passed there at both ends (run `38075908457`), and pushed (README §5 rule
10). It is the release the clients adopt. See *Release of `v0.2.0`*, below.

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
| **U5** freeze | no client edits its `RayTools/` until it adopts | **taken** 2026-10-10; in force from 01's commit; amended by U12 |
| **U6** Ray stand-in | real `ObjectRef(bytes)`; `ray.wait` / `ray.get` replaced in-process | **taken** 2026-10-10 |
| **U7** versions | Python ≥3.12, Ray ≥2.43; tested 3.12.15/2.43.0 and 3.13.16/2.55.1 | **taken** 2026-10-10 |
| **U8** handler checks | defaults apply only with a compute handler (option b); `ValueError`; all four compute-path arguments checked | **taken** 2026-10-10, amended; **applied** by 04 (`0b6ffd2`) |
| **U9** printed lines | pinned, wording and layout, against a scripted clock; the three consumer patterns checked | **taken** 2026-10-10, as amended |
| **U10** CPBH shim | none | **taken** 2026-10-10, for 06; no CPBH site at `52142d7` affected |
| **U11** licence header | CPBH's and SI's header, on `RayWorkPool.py` only | **taken** 2026-10-10: on all four package modules; **applied** by 04 (`0b6ffd2`) |
| **U12** order with DatastoreKit | U5 amended: a DatastoreKit-first adoption may rewrite the one `ShardedPool` import in `RayTools/RayWorkPool.py` | **taken** 2026-10-10, for 06 |

## 1. Prompts

| # | Prompt | Status | Commit | Suite |
|---|---|---|---|---|
| 01 | [`01-import-the-pool.md`](01-import-the-pool.md) | **landed** 2026-10-10 ([log](logs/01-import-the-pool.md)), reviewed | `49f3ddf` | 0 → 3 |
| 02 | [`02-the-test-suite.md`](02-the-test-suite.md) | **landed** 2026-10-10 ([log](logs/02-the-test-suite.md)), reviewed | `b9f6dec` | 3 → 116 |
| 03 | [`03-supported-versions-and-ci.md`](03-supported-versions-and-ci.md) | **landed** 2026-10-10 ([log](logs/03-supported-versions-and-ci.md)), reviewed; tagged `v0.1.0` | `4e90a8a` | 116 → 116 |
| 04 | [`04-fix-the-inherited-faults.md`](04-fix-the-inherited-faults.md) | **landed** 2026-10-10 ([log](logs/04-fix-the-inherited-faults.md)), reviewed | `0b6ffd2` | 116 → 121 |
| 05 | [`05-release-v0.2.0.md`](05-release-v0.2.0.md) | **landed** 2026-10-10 ([log](logs/05-release-v0.2.0.md)), reviewed; CI green; tagged `v0.2.0` | `eaef0ce` | 121 → 121 |
| 06 | [`06-the-adoption-checklists.md`](06-the-adoption-checklists.md) | **written** 2026-10-10 | — | 121 → 121 |
| 07 | `07-verification-and-close-out.md` | not written | — | — |

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`310db6e`),
used for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`319099a`), used for 02;
[`orchestrator/prompt-03.md`](orchestrator/prompt-03.md) (`e136eee`), used for 03;
[`orchestrator/prompt-04.md`](orchestrator/prompt-04.md) (`a7d9252`), used for 04;
[`orchestrator/prompt-05.md`](orchestrator/prompt-05.md) (`1868b6e`), used for 05.

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

**Release of `v0.1.0` (2026-10-10).** Put to the user after the review of 03, and done at the
user's instruction, in the order the review recommended, so that CI ran on 03's commit itself:
1. **Push.** `git push origin 4e90a8a:main` moved `origin/main` from `97f9ff0` to `4e90a8a`.
2. **CI.** The workflow's first run, `38054782562` on `4e90a8a`, passed both jobs, the suite's
   first run on Linux: `suite (low)`, Python 3.12.15 / Ray 2.43.0 (GCC 13.3.0 build),
   `Ran 116 tests … OK` and `black` "15 files would be left unchanged."; `suite (high)`,
   Python 3.13.16 / Ray 2.55.1, `Ran 116 tests … OK`.
3. **The tag.** `v0.1.0`, annotated (tag object `0a9cdb2`), on `4e90a8a`, pushed; then `main`
   (`9db0619`, the review) pushed, and its CI run, `38055129804`, passed both jobs.
4. **A client's install, checked.** `uv pip install "raypoolkit @
   git+https://github.com/ds283/RayPoolKit@v0.1.0" "ray==2.55.1"` into a fresh 3.13.16 venv, with
   `uv`'s cache bypassed: `direct_url.json` records `requested_revision` `v0.1.0` and `commit_id`
   `4e90a8a…`; the installed package is the four modules and no `tests/`; from an empty directory
   with `-I`, the two public names import, `version` is `0.1.0`, `requires` is `['ray>=2.43']`,
   `ray.is_initialized()` is false, and `import raypoolkit.tests` raises `ModuleNotFoundError`.

**Orchestrator review of prompt 04 (2026-10-10).** Dispatched from `a7d9252` to one Opus
subagent, with the note's §0 facts and its eight clarifications, and one addendum: another
session's short-lived Ray clusters, from DatastoreKit's scratchpad, were to be attributed and left
alone. Reviewed against its commit `0b6ffd2`, with nothing landed after it. **Every check of the
note's §3 passed**, and acceptance 1–5 are met. No stop condition fired.

*At dispatch.* The note's gate held at `a7d9252`. The tree was clean, the only worktree was this
checkout, `git diff v0.1.0 -- raypoolkit` was empty, `git tag` was `v0.1.0` alone and `origin/main`
was `6b1ddfe`. The suite gave 116 and the check exited 0. A DatastoreKit session's local Ray
(`gcs_server`, `raylet`) was up for a few seconds and gone before dispatch; none was this
repository's.

*The checks.*
1. **E1, scope.** `0b6ffd2` touches 14 files: the four package modules, the four test modules the
   prompt names and `test_standins.py` (its one comment), `compare_with_source.py`, the log, this
   board, `prompts/INDEX.md` and the index. `git diff c207238 0b6ffd2` over `pyproject.toml`,
   `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore`, `.github`, `standins.py`,
   the three other test modules and the campaign README is empty. `git ls-files raypoolkit` equals
   `v0.1.0`'s. No tag was made and `origin` is unchanged.
2. **E2, the module.** `git diff v0.1.0 0b6ffd2 -- raypoolkit/RayWorkPool.py` was read whole: the
   header; §2.4's checks with the resolution by identity and §2.5's sizes;
   `range(self._num_total_items)`; the comment; 26 lines `.hex` → `.hex()`, nothing else on them, and no
   bare `.hex` left; `:530`'s argument. It equals the orchestrator's own scratch application of the
   prompt but for two blank lines. The signature is unchanged (18 parameters, names, kinds,
   defaults by qualified name and annotations equal to `v0.1.0`'s). The other three modules differ
   by the header, and `contract.py` also by §2.7's sentence; the header's 15 lines hash alike in all
   four, and its 14 to SI's `e73e9334…e1ab9`.
3. **E3, the suite.** `venv/`: `Ran 121 tests … OK`. The orchestrator's own fresh `uv` venv at
   3.13.16 / 2.55.1, the repository editable in one resolve: 121, OK. By module: construction 15,
   inherited faults 6, package imports 3, printed lines 18, run paths 22, scheduling 7, stand-ins
   30, task builder 20. No Ray process before or after.
4. **E4, the breakage.** (r1)–(r10) were extracted from the log's text and replayed from the clean
   tree at `0b6ffd2`, each with the whole suite under a 300 s timeout. Each gave the log's verdict
   line exactly, and failed the log's tests, entry counts included ((r4): 51 tests, 80 entries);
   `git status` was clean after each. The orchestrator's own: (o1) `value < 1` → `value <= 1`
   fails C7 at 1 (and 124 entries in all, since `process_batch_size` defaults to 1); (o2)
   `store_handler` dropped from the no-compute tuple fails C2's `store_handler` subtest alone.
5. **E4, the guards on `v0.1.0`.** In a fresh export of `0b6ffd2` with `v0.1.0`'s
   `RayWorkPool.py` copied over it: `Ran 121 tests … FAILED (failures=11, errors=23)`, the 17 tests
   and 34 entries of log §4.11, entry for entry; every test 04 did not change passes there.
6. **E5, the lines.** `test_printed_lines.py` changes only `HANDLER_SETS` ("validation only" gone,
   the two lookup-only spellings added) and adds the spelling test, which resets the clock before
   each of its three runs and expects the nine lines of
   `test_a_lookup_only_run_notifying_on_every_pass`. No expected line of an existing test changed.
7. **E6, the tests.** `test_inherited_faults.py`, `test_construction.py` and `test_run_paths.py`
   were read: §3's names, docstrings naming each resolved issue and the old behaviour, messages
   compared whole with `type(...) is ValueError`, S4's identity with `results[0]`, X1 seeded under
   `ref.hex()` only, the header test finding the modules from `raypoolkit.__file__`. The only new
   use of a private name in the tests is `_build_queued_status_message`, 02 §2.2's seam.
8. **The check, retired.** Its diff is the one docstring paragraph. From a `git worktree` of
   `v0.1.0` (removed after), it exits 0 with 572 identical, 2 D-imp, 1 D-pool, 4 D-int, 12 declared
   files, 0 undeclared; log §3.3 holds the agent's last run before the change.
9. **`black --check raypoolkit docs`** (25.1.0): 15 files unchanged.
10. **E7, the records.** The log has every section of README §5.1 and the prompt's §5.5 additions,
    with §0's clarifications as deviations 1–8. This board had 04's row, U8 and U11 applied, one
    issue in §3 and the seven in §4, each with a dated **Resolved (04)** line whose line numbers
    match the module. The index counts 1 row, matching its header; `prompts/INDEX.md`'s line says
    04 landed.

*Findings.*
- **None opened.** The agent's observations are kept as observations: `README.md:147-152` and
  `PROVENANCE.md:40` describe `v0.1.0`, as they say, and 05 rewrites both (README §2, row 05);
  `compare_with_source.py`'s `NO_SOURCE` text is true of `v0.1.0`, where the retired check runs; a
  size that does not compare with 1 now raises `TypeError` at construction rather than in `run()`.
  06's checklists should note that a pool with no compute handler still takes an
  `available_handler` and a `post_handler`.
- **A correction to the note.** Its clarification 3 said (r4) "fails 71 of the 116" on the
  unchanged suite. That counted failing entries, subtests separately, not tests; the agent's 51
  tests (80 entries) are on the new suite. The two do not disagree.

*Residue fixed in the follow-up commit.* "this commit" → `0b6ffd2` on this board, in the log and
in `prompts/INDEX.md`; README §2's status and header for 04; this review and the notes line.

**CI on 04's commit (2026-10-10).** Put to the user after the review, and done by the user, in the
order the review recommended: `git push origin 0b6ffd2:main` moved `origin/main` from `6b1ddfe` to
`0b6ffd2`, and the workflow's run `38071307103` on it passed both jobs: `suite (low)`, Python 3.12
/ Ray 2.43.0, `Ran 121 tests … OK` and `black` "15 files would be left unchanged."; `suite
(high)`, Python 3.13 / Ray 2.55.1, `Ran 121 tests … OK`. Then `main` (`914070c`, the review) was
pushed, and its run, `38071490036`, passed both jobs. No tag was made: `v0.2.0` is 05's.

**Orchestrator review of prompt 05 (2026-10-10).** Dispatched from `1868b6e` to one Opus
subagent, with the note's §0 facts and its eight clarifications. Reviewed against its commit
`eaef0ce`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–4 are met. No stop condition fired.

*At dispatch.* The note's gate held at `1868b6e`. The tree was clean, the only worktree was this
checkout, `git diff 0b6ffd2 -- raypoolkit pyproject.toml README.md PROVENANCE.md` was empty,
`git tag` was `v0.1.0` alone and `origin/main` was `914070c`. The suite gave 121 at `f839209`. The
repository's `raypoolkit.egg-info/SOURCES.txt` listed the ten test files. A DatastoreKit session's
local Ray, up while the note was written, was gone before dispatch; none was this repository's.

*The checks.*
1. **E1, scope.** `eaef0ce` touches 7 files: `pyproject.toml`, `README.md`, `PROVENANCE.md`, the
   log, this board, `prompts/INDEX.md` and the index. `git diff f839209 eaef0ce` over
   `raypoolkit`, `docs/extraction`, `.github`, `CLAUDE.md`, `LICENSE`, `.gitignore` and the
   campaign README is empty. No tag was made, `origin` is unchanged, there is no `build/` or
   `dist/`, and the only worktree is this checkout.
2. **E2, `pyproject.toml`.** Two changes: `version = "0.2.0"`, and `[tool.setuptools]`
   `include-package-data = false` before `[tool.setuptools.packages.find]`, whose `exclude` stays.
3. **E3, the suite.** `venv/`: `Ran 121 tests … OK`, by module construction 15, inherited faults
   6, package imports 3, printed lines 18, run paths 22, scheduling 7, stand-ins 30, task builder
   20; `importlib.metadata` gives `0.2.0` and `['ray>=2.43']`. The orchestrator's own fresh `uv`
   venv at 3.13.16 / 2.55.1, the repository editable in one resolve: 121, OK. No Ray process
   before or after.
4. **E4, the distribution, re-built from `eaef0ce`.** Two fresh `git archive eaef0ce` exports,
   built with `uv build --wheel` and no `-q`: (R1') as exported, and (R2') with the repository's
   `raypoolkit.egg-info/` copied in (`Version: 0.2.0`, its `SOURCES.txt` still listing the ten test
   files). Each gives `raypoolkit-0.2.0-py3-none-any.whl`, 13,565 bytes, the 9 entries of the log,
   none under `raypoolkit/tests/`, and no "absent from" line; the four modules in each are
   byte-equal to the commit's. (R2') installed into a fresh 3.13.16 / 2.55.1 venv and run from an
   empty directory with `-I`: the package imports from `site-packages`, `version` is `0.2.0`,
   `requires` is `['ray>=2.43']`, `ray.is_initialized()` is false, and `import raypoolkit.tests`
   raises `ModuleNotFoundError`.
5. **E5, the breakage.** (a)–(c) were extracted from the log's text and replayed in fresh exports
   of `eaef0ce`, each passing `git apply --check` and, once applied, `-R --check`: (a) with the
   stale manifest gives 42,737 bytes, 19 entries, 10 under `raypoolkit/tests/` and 2 "absent from"
   lines; (b) gives 19 entries, 10 tests, and its wheel's `raypoolkit.tests` imports from
   `site-packages` in a throwaway venv; (c) gives `raypoolkit-0.1.0-py3-none-any.whl`. The
   orchestrator's own (o1), `include-package-data = true` with the stale manifest, fails as (a)
   does (19 entries, 10 tests, 2 "absent from" lines), so it is the setting's value, not the
   table's presence, that closes the issue. The repository's `git status` stayed clean.
6. **E6, the README.** Read whole. "Changes in `v0.2.0`" does not repeat the prompt's "silently
   ignored" bullet (clarification 1): it says that `v0.1.0` already refused an explicit persist
   handler with no compute handler (`RuntimeWarning`) and a compute handler with
   `persist_handler=None` (`RuntimeError`). The orchestrator's own probe constructed each case
   against `v0.1.0`'s module and `eaef0ce`'s, and every "was" and "now" in the section matches. On
   `v0.1.0`: the default or an explicit persist handler with no compute handler raises
   `RuntimeWarning`; an explicit store handler, validation handler or label builder with no
   compute handler constructs, as do `store_handler=None` with a compute handler and
   `create_batch_size=0`; a compute handler with `persist_handler=None` raises `RuntimeError`; a
   generator with `store_results=True` raises `TypeError`. On `eaef0ce`: every refusal is
   `ValueError`, and the lookup-only default and the generator construct. "Which handlers a pool
   needs" replaces the old section, gives types and the gist of each message, and names no issue.
   The pin is `@v0.2.0`, "pass a sequence" is gone, the sizes are "at least 1", and Developing and
   Licence are as §2.2 asks. The printed-line examples are unchanged. Every relative link in both
   files resolves in the commit, and both in-page anchors match their headings.
7. **E6, `PROVENANCE.md`.** The diff makes `:40-42` and `:57` statements of `v0.1.0`, rewrites
   "Re-running the check" for a worktree of the tag, and adds "Since `v0.1.0`" before "The freeze".
   The file map, the classes, "New here" and the freeze are unchanged. Its commands were run as
   written, with the worktree in the scratchpad: exit 0, with 572 identical lines, 2 D-imp, 1
   D-pool and 4 D-int; the worktree was removed after.
8. **No behaviour moved.** `git diff 0b6ffd2 eaef0ce -- raypoolkit` is empty.
9. **`black --check raypoolkit docs`** (25.1.0): 15 files unchanged.
10. **E7, the records.** The log has every section of README §5.1 and the prompt's §4.4 additions,
    with §0's clarifications as deviations 1–8 (1 STRUCTURALLY REQUIRED). This board had the header
    with the "ready to be tagged" line, 05's row, §3 empty and the issue in §4 with a dated
    **Resolved (05)** line. The index counts 0 rows, matching its header; `prompts/INDEX.md`'s line
    says 05 landed.

*Findings.*
- **None opened.** The agent's observations are kept as observations: "New here" in
  `PROVENANCE.md` lists only 01's files, and the D-fmt bullet's "line numbers are SGK's" now reads
  as of `v0.1.0`; both are records of the import. The stale manifest is still merged by setuptools
  but no longer reaches a wheel.
- **The agent's deviation 9**, "each fault's fix is guarded" in place of "each fix is guarded", is
  accepted as STRUCTURALLY REQUIRED: 04's reworded comment has no test.

*Residue fixed in the follow-up commit.* "this commit" → `eaef0ce` on this board, in the log and
in `prompts/INDEX.md`; README §2's status and header for 05; this review and the notes line.

**Release of `v0.2.0` (2026-10-10).** Put to the user after the review of 05, and done by the
user, in the order the review recommended, so that CI ran on 05's commit itself:
1. **Push.** `git push origin eaef0ce:main` moved `origin/main` from `914070c` to `eaef0ce`.
2. **CI.** The workflow's run `38075908457` on `eaef0ce` passed both jobs: `suite (low)`, Python
   3.12.15 / Ray 2.43.0, `raypoolkit` installed at `0.2.0`, `Ran 121 tests … OK` and `black` "15
   files would be left unchanged."; `suite (high)`, Python 3.13.16 / Ray 2.55.1, `Ran 121 tests …
   OK`.
3. **The tag.** `v0.2.0`, annotated (tag object `4e7eb15`, message "raypoolkit 0.2.0"), on
   `eaef0ce`, made by the user and pushed. The review's follow-up (`9a00f80`) and this record had
   not been pushed when this was written.
4. **A client's install, checked.** `uv pip install --no-cache "raypoolkit @
   git+https://github.com/ds283/RayPoolKit@v0.2.0" "ray==2.55.1"` into a fresh 3.13.16 venv:
   `direct_url.json` records `requested_revision` `v0.2.0` and `commit_id` `eaef0ce…`; the
   installed package is the four modules and no `tests/`; from an empty directory with `-I`, the
   two public names import, `version` is `0.2.0`, `requires` is `['ray>=2.43']`,
   `ray.is_initialized()` is false, and `import raypoolkit.tests` raises `ModuleNotFoundError`.
5. **`main` pushed.** The user then pushed `main` (`9a00f80`, the review, and `b2b6ab4`, this
   record), and its run, `38076190172` on `b2b6ab4`, passed both jobs. Recorded with 06's
   writing.

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1** | **holds** 2026-10-10, re-checked at 01's writing and again at its start: SGK `RayTools/RayWorkPool.py` is blob `b4666fa` at `b510bc9`, the import commit |
| **G2** | not yet (SGK adopts `v0.2.0`) |
| **G3** | not yet (CPBH adopts `v0.2.0`) |
| **G4** | not yet (SI adopts `v0.2.0`) |

## 3. Active and unresolved issues

None. The five `[00-…]` entries inherited from the source,
`[01-a-kept-comment-names-the-datastore-service]` and
`[02-the-constructor-does-not-check-its-sizes]` were closed by 04, and
`[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` by 05; all are in §4.

## 4. Resolved issues

The five `[00-…]` entries were inherited from the source and opened at planning (README §0.2,
faults 1–5); each was pinned as it behaved by 02 and fixed by 04. Their **Package** lines are
`v0.1.0`'s (log 01 §3.6); each **Resolved** line gives the line in the module as 04 left it.

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

**Resolved (04, 2026-10-10):** the 26 keys are `.hex()`, at `raypoolkit/RayWorkPool.py:300, 303, 306,
317, 362, 377, 378, 391, 392, 419, 421, 429, 430, 443, 449, 450, 474, 475, 484, 485, 507, 508, 519,
520, 545, 546`. Guarded by `test_inherited_faults.TestInheritedFaults.test_fresh_refs_from_wait_complete_every_path`
(with `fresh_refs`, a lookup-only pool, one with an availability handler, compute with and without
validation, and `Blob`s each run to completion with the right `results`) and by X1, now seeded under
`ref.hex()` only. (r1) fails both, and so does `v0.1.0`'s module (log 04 §4).

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

**Resolved (04, 2026-10-10):** `raypoolkit/RayWorkPool.py:530` passes `replacement_obj`. Guarded by
`TestInheritedFaults.test_the_post_handler_after_persist_gets_the_persisted_object` (the post
handler's object has `store_id` 1001 and is `results[0]`) and by S4, inverted. (r2) fails both, and
so does `v0.1.0`'s module (log 04 §4).

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

**Resolved (04, 2026-10-10):** `raypoolkit/RayWorkPool.py:178` sizes `results` from
`self._num_total_items`. Guarded by `TestInheritedFaults.test_store_results_accepts_a_generator_task_list`.
(r3) fails it, and so does `v0.1.0`'s module (log 04 §4).

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

**Decided (2026-10-10):** U8 taken, option (b), with every argument check raising `ValueError`
and the check covering `store_handler`, `persist_handler`, `validation_handler` and
`label_builder`. 04 applies it (prompt 04 §2.4); all 87 client call sites construct under it.

**Pinned (02, 2026-10-10):** `TestInheritedFaults.test_fault_persist_handler_without_compute_raises_runtime_warning`
(also `test_construction.TestHandlerChecks.test_persist_handler_without_compute_handler_raises_runtime_warning`,
with the message) and `TestInheritedFaults.test_fault_store_handler_none_with_compute_fails_at_first_compute`
(`TypeError` from `self._store_handler(obj, self._pool)` once the first compute completes). 04
inverts them under U8.

**Resolved (04, 2026-10-10):** under U8, `raypoolkit/RayWorkPool.py:109-134`: with no compute
handler, a store or persist handler left at its default (by identity) resolves to `None`, and any
of the four compute-path arguments not `None` raises `ValueError`; with one, `store_handler=None`
or `persist_handler=None` raises `ValueError`. The signature is unchanged; no client call site must
change (prompt 04 §2.4). Guarded by `TestInheritedFaults.test_a_lookup_only_pool_needs_no_persist_handler`
and `…test_store_handler_none_with_compute_is_refused_at_construction`; by C1, C2, C5 and C6 in
`test_construction.TestHandlerChecks`; and by `test_printed_lines`' spelling test, which shows the
three lookup-only spellings print the same lines. (r4)–(r7) each fail them, and so does `v0.1.0`'s
module (log 04 §4).

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

**Decided (2026-10-10):** U11 taken: CPBH's and SI's 14-line header, byte for byte, on all four
package modules (`RayWorkPool.py`, `_timing.py`, `contract.py`, `__init__.py`), not the tests. 04
adds it with a test that reads it (prompt 04 §2.6, §3.1).

**Resolved (04, 2026-10-10):** the constructor's messages (`raypoolkit/RayWorkPool.py:123`, `:133`,
`:142`) say "handler", and U11's header is at lines 1–15 of all four package modules. Guarded by
the message assertions of `test_construction.py` (C1, C2, C5, C7) and the fault-4b guard, and by
`TestInheritedFaults.test_every_package_module_carries_the_licence_header`. (r9) and (r10) fail
them; `v0.1.0`'s module fails the header test for `RayWorkPool.py` (log 04 §4).

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

**Resolved (04, 2026-10-10):** the comment at `raypoolkit/RayWorkPool.py:464` says "…submit a
store request to the datastore." No test guards a comment; `git grep -n "Datastore service"
raypoolkit` is empty.

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

**Resolved (04, 2026-10-10):** `raypoolkit/RayWorkPool.py:136-142`: each of `create_batch_size`,
`process_batch_size` and `max_task_queue` below 1 raises `ValueError` ("<name> must be at least 1,
not <value>"). Guarded by C7, `test_construction.TestSizeChecks.test_a_size_below_one_raises_value_error`.
(r8) fails it, and so does `v0.1.0`'s module (log 04 §4).

### `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`

**Opened:** 2026-10-10, by 03 (log 03 §6.1). **Owner:** 05.

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

**Assigned (2026-10-10):** to 05, at the user's instruction when 05 was written: it is the next
prompt that changes `pyproject.toml`, and the release `v0.2.0` should not stand on a setting a
stale manifest defeats. Re-measured at 05's writing, at `914070c`: the repository's
`raypoolkit.egg-info/SOURCES.txt` still lists the ten test files; a fresh export at `0.2.0` with it
copied in builds 19 entries, 10 of them tests, without the setting, and 9 with it, with no
"absent from" warning (prompt 05 §2.1).

**Resolved (05, 2026-10-10):** `pyproject.toml` gains `[tool.setuptools]`
`include-package-data = false`, before `[tool.setuptools.packages.find]`, whose `exclude` stays.
Measured by 05's release check (log 05 §3.3), each wheel built with `uv build --wheel` (no `-q`)
from a fresh `git archive` export with 05's `pyproject.toml`: (R1), the export as it is, and (R2),
the export with the repository's `raypoolkit.egg-info/` copied in (its `SOURCES.txt` listing the
10 test files), each give `raypoolkit-0.2.0-py3-none-any.whl`, 13,565 bytes, **9 entries, none
under `raypoolkit/tests/`**, and no "absent from" line in the build log; (R2)'s wheel, installed
into a fresh 3.13.16 / 2.55.1 venv, passes every check of 03 §2.4 at `0.2.0`, and
`import raypoolkit.tests` raises `ModuleNotFoundError`. Breakage (a), the table removed with the
stale manifest, gives 19 entries, 10 of them tests, and the warning (2 "absent from" lines); (b),
the table kept and the `exclude` removed, ships the tests as packages (log 05 §5). The stale
manifest itself is left alone: setuptools still merges it, and none of its files reaches the wheel.
