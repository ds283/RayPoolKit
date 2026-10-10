# The extraction campaign: verification

**Campaign:** [`prompts/extraction/README.md`](../prompts/extraction/README.md) ·
**Board:** [`prompts/extraction/IMPLEMENTATION_STATE.md`](../prompts/extraction/IMPLEMENTATION_STATE.md) ·
**Written by:** [extraction prompt 07](../prompts/extraction/07-verification-and-close-out.md),
log [`07-verification-and-close-out.md`](../prompts/extraction/logs/07-verification-and-close-out.md) ·
**Date:** 2026-10-10 · **Verifies:** the package as tagged **`v0.2.0`**, commit `eaef0ce` (tag object
`4e7eb15`), and the records of prompts 01–06. `git diff eaef0ce -- raypoolkit pyproject.toml` is
empty at the commit that adds this document.

*This document is additive from the day it is committed (`CLAUDE.md` rule 6): a later measurement is
added as a new dated subsection, and what is here is not rewritten.*

Every fact below carries a commit, a `path:line` at a named tree, or a command and its output. A
statement of a log is cited by log and section ("log 05 §3.3" is
`prompts/extraction/logs/05-release-v0.2.0.md` §3.3); "the board" is the campaign's
`IMPLEMENTATION_STATE.md`, and "README" without a path is the campaign's plan. Where this document
and a log disagree, it says which is right and why; it does not rewrite the log. `<scratch>` stands
for the scratch directory of prompt 07's run (`<session scratchpad>/agent07`), outside the
repository; `$S` is the same directory in the commands of §11.

---

## 1. What this document is

**What the campaign set out to do** (README §0, §0.1, §1, §6.1). Three client projects,
SecondaryGWKit (SGK), ChamPBH (CPBH) and StochasticInstantons (SI), each ran its own copy of
`RayTools/RayWorkPool.py`, and a fix had to be made three times and had not been: the "available"
rate fix had reached one copy (README §0). The user decided on 2026-10-10 (**D1**) to extract the
pool as a separate, reusable component, as DatastoreKit had extracted the datastore layer (**D2**,
DatastoreKit's, 2026-10-07: the datastore layer first, the pool a separate unit of work). The
campaign was to import SGK's copy unchanged in behaviour (U2), pin that behaviour with a suite that
needs no Ray cluster, release it as `v0.1.0`, fix the faults inherited from the source and release
`v0.2.0`, the release the clients adopt, and hand each client an adoption checklist (README §0.1,
§1).

**What it delivered.**
- The package `raypoolkit`: SGK's `RayTools/RayWorkPool.py` at `b510bc9` (blob `b4666fa`), with
  its two client imports replaced, `format_time` internalised in `_timing.py`, and the pool typed by
  a `typing.Protocol`, `DatastorePool` (`PROVENANCE.md`; U3, U4).
- A suite of **121** tests that drives the pool with real `ObjectRef`s and an in-process stand-in
  for `ray.wait` and `ray.get` (U6), with no Ray cluster (§3).
- The fixes of the five faults inherited from the source, each guarded by a test that `v0.1.0`'s
  module fails, with the constructor's checks of U8, and of three issues found on the way (§6).
- A CI workflow at both tested ends, and two releases, each tagged on its prompt's commit after CI
  passed there (§2.3): **`v0.1.0`** (`4e90a8a`, SGK's behaviour) and **`v0.2.0`** (`eaef0ce`).
- `docs/adoption/`: a checklist per client, measured read-only against `v0.2.0`, and the script
  that measures them.
- With this prompt: this document, and `docs/extraction/ray_smoke_run.py`, the pool's first run
  under real Ray (U13).

**The headline, at `v0.2.0`.**
- **The suite** gives `Ran 121 tests … OK` in `venv/` (Python 3.12.15 / Ray 2.43.0) and at the high
  end (3.13.16 / 2.55.1), with the same count by module (§3.1).
- **Under real Ray** (U13), for the first time: the smoke script's five steps pass at both ends,
  Ray is left with no process by either check of §4.1, and each run's Ray says "Usage reporting is
  disabled." (§4). With fault 2's or fault 3's fix reverted, a step fails; with fault 1's fix
  reverted, **every step passes**, so fault 1 is guarded by the stand-in only (§4.5); with Ray
  already up, the script refuses and exits 2 (§4.4).
- **The release** (U14): the pin was installed from GitHub by the release record of `v0.2.0` and is
  cited, not fetched again; the wheel rebuilt offline from `git archive v0.2.0` is
  `raypoolkit-0.2.0-py3-none-any.whl`, 13,565 bytes, 9 entries, and its four modules are
  `eaef0ce`'s byte for byte (§5).
- **The checklists**: `measure_client_pools.py`, re-run here, prints each checklist's appendix byte
  for byte; all 87 client call sites construct under `v0.2.0` (§3).
- **Issues**: eight were opened and resolved on the board; **none is open**, and this prompt opens
  none (§6).
- **What remains** (§10): G2–G4, each client's adoption in a campaign of its own; a multi-node
  cluster, the clients' own suites, Python 3.14 and Ray above 2.55.1, unverified; fault 1 guarded
  by the stand-in only; and DatastoreKit's README, which is DatastoreKit's to change.

---

## 2. Reconciliation

### 2.1 The prompts

Each prompt landed as one commit, was dispatched from an orchestration note and reviewed in a
commit of its own (the board's notes line and its §1 reviews). The suite count is each log's
"after", re-read from its header and its suite section; the closed and opened issues are the
board's §3 and §4.

| Prompt | Commit | Note | Review | Suite after | Closed | Opened |
|---|---|---|---|---|---|---|
| 01 | `49f3ddf` | `310db6e` | `53477ff` | 3 | — | `[01-a-kept-comment-names-the-datastore-service]` |
| 02 | `b9f6dec` | `319099a` | `307ed96` | 116 | — | the review, `[02-the-constructor-does-not-check-its-sizes]` |
| 03 | `4e90a8a` | `e136eee` | `9db0619` | 116 | — | `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` |
| 04 | `0b6ffd2` | `a7d9252` | `914070c` | 121 | the five `[00-…]`, `[01-a-kept-comment-names-the-datastore-service]`, `[02-the-constructor-does-not-check-its-sizes]` | — |
| 05 | `eaef0ce` | `1868b6e` | `9a00f80` | 121 | `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` | — |
| 06 | `67f3f7e` | `deffdc2` | `71f0d66` | 121 | — | — |
| 07 | the commit that adds this document | `ff265ee` | — | 121 | the campaign | — |

The suite went 0 → 3 (01) → 116 (02) → 116 (03) → 121 (04) → 121 (05) → 121 (06) → 121 (07). The
five `[00-…]` issues were opened at planning, `4cb493f` (`git show 4cb493f:docs/OPEN_ISSUES.md`:
"**5 open**"). The open count went 5 → 6 (01) → 7 (02's review) → 8 (03) → 1 (04) → 0 (05), and
stayed 0 (logs 01 §6, 03 §7, 04 §6, 05 §7; the board's review of 02).

### 2.2 Every other commit

`git log --reverse --format='%h %s' ff265ee` lists **30** commits, from `3f1dfd4` (the repository
started) to `ff265ee`, the commit before 07's. Six are the prompts of §2.1. The other 24, by class:

| Class | Count | Commits |
|---|---|---|
| repository started | 1 | `3f1dfd4` "Start the RayPoolKit repository" |
| plan | 1 | `4cb493f` (U1–U3 taken; the five `[00-…]` issues opened) |
| prompt written | 7 | `97f9ff0` (01, U4–U5), `d9adb9b` (02, U6, U9), `c73fc91` (03, U7), `c207238` (04, U8, U11), `f839209` (05, and 04's CI recorded), `a1d64ea` (06, U10, U12), `787507a` (07, U13, U14) |
| note | 7 | `310db6e`, `319099a`, `e136eee`, `a7d9252`, `1868b6e`, `deffdc2`, `ff265ee` |
| review | 6 | `53477ff`, `307ed96`, `9db0619`, `914070c`, `9a00f80`, `71f0d66` |
| release record | 2 | `6b1ddfe` (`v0.1.0`), `b2b6ab4` (`v0.2.0`) |

6 prompts and 1 + 1 + 7 + 7 + 6 + 2 others: 30. Prompt 07's §1.3 counted 28, to `71f0d66`; `787507a` and `ff265ee`
landed after it was written, so 30 is the count at 07's commit (log 07 §2, deviation 2). The prompt's
classes have no place for `3f1dfd4`, which is a class of its own here.

### 2.3 Tags and CI

`git for-each-ref refs/tags --format='%(refname:short) %(objectname:short) %(*objectname:short)'`:

```text
v0.1.0 0a9cdb2 4e90a8a
v0.2.0 4e7eb15 eaef0ce
```

Both tags are annotated, made on their prompt's commit after the workflow passed there at both
ends, and pushed (the board, *Release of `v0.1.0`* and *Release of `v0.2.0`*). Neither has moved.

Every run of the workflow, `.github/workflows/tests.yml` (03's, unchanged since:
`git diff 4e90a8a eaef0ce -- .github` is empty), read with `gh run list` and `gh run view --log` on
2026-10-10: each **completed / success**, both jobs, `suite (low)` (Ray 2.43.0) and `suite (high)`
(Ray 2.55.1), successful, each suite's verdict `OK`, and `black` run on the low end only.

| Run | Commit | What it ran on | Suite, low / high | `black` |
|---|---|---|---|---|
| [38054782562](https://github.com/ds283/RayPoolKit/actions/runs/38054782562) | `4e90a8a` (03) | the workflow's first run; then `v0.1.0` was tagged | 116 / 116 | 15 files unchanged |
| [38055129804](https://github.com/ds283/RayPoolKit/actions/runs/38055129804) | `9db0619` | the review of 03 | 116 / 116 | 15 |
| [38055185065](https://github.com/ds283/RayPoolKit/actions/runs/38055185065) | `6b1ddfe` | the release record of `v0.1.0`; no record named this run before this document | 116 / 116 | 15 |
| [38071307103](https://github.com/ds283/RayPoolKit/actions/runs/38071307103) | `0b6ffd2` (04) | the board's *CI on 04's commit* | 121 / 121 | 15 |
| [38071490036](https://github.com/ds283/RayPoolKit/actions/runs/38071490036) | `914070c` | the review of 04 | 121 / 121 | 15 |
| [38075908457](https://github.com/ds283/RayPoolKit/actions/runs/38075908457) | `eaef0ce` (05) | then `v0.2.0` was tagged | 121 / 121 | 15 |
| [38076190172](https://github.com/ds283/RayPoolKit/actions/runs/38076190172) | `b2b6ab4` | the release record of `v0.2.0` | 121 / 121 | 15 |
| [38086076394](https://github.com/ds283/RayPoolKit/actions/runs/38086076394) | `787507a` | the gate's run: `71f0d66`, 06's records, was pushed with `787507a` and has no run of its own; `787507a` touches only `prompts/` | 121 / 121 | 16 |

The board records the first, fourth, sixth and seventh runs' verdicts (*Release of `v0.1.0`*, *CI on
04's commit*, *Release of `v0.2.0`*), and these agree. This prompt pushes nothing, makes no tag and
starts no run.

### 2.4 The environment

Every measurement of §3–§5 was made on 2026-10-10, 22:20–22:46 BST, on one machine: macOS 27.0.1
(build 26A434), arm64, `git` 2.56.0, `uv` 0.12.20. Every venv but `venv/` was made by
`uv venv --offline`, with its packages installed `--offline` from `uv`'s cache. No network was used
but `gh run list` and `gh run view`, which read GitHub's record of the runs above.

| Venv | Python | Ray | `raypoolkit` | Used for |
|---|---|---|---|---|
| `venv/` (the repository's) | 3.12.15 | 2.43.0 | 0.2.0, editable from the checkout | the suite (low end), `black` 25.1.0, the equivalence check at `v0.1.0`, `measure_client_pools.py` |
| `<scratch>/base-hi/venv` | 3.13.16 | 2.55.1 | 0.2.0, editable from `git archive HEAD` | the suite at the high end |
| `<scratch>/smoke-lo/venv` | 3.12.15 | 2.43.0 | 0.2.0, editable from `git archive HEAD` | §4, low end |
| `<scratch>/smoke-hi/venv` | 3.13.16 | 2.55.1 | as above | §4, high end, and (d) |
| `<scratch>/break-a/venv`, `break-b/venv`, `break-c/venv` | 3.13.16 | 2.55.1 | as above, each its own export, with a breakage applied | §4.4 (a)–(c) |

The low-end interpreter is `/opt/local/bin/python3.12`, the high-end `/opt/local/bin/python3.13`.
Each export is `git archive HEAD` at `ff265ee`, whose `raypoolkit/` is `eaef0ce`'s; the smoke
script, uncommitted at the time, was run from the repository root, so that `sys.path[0]` is
`docs/extraction/` and `raypoolkit` comes from the export (each run prints `raypoolkit.__file__`,
under its export). Ray's sessions are written to Ray's default, `/tmp/ray`, shared with other
sessions on this machine; this prompt passed no `_temp_dir` and deleted nothing there.

The clients, at the start and at the end of 07's work (`git -C <repo> rev-parse HEAD`,
`git status --porcelain | shasum`, first twelve characters, and `git stash list | wc -l`), equal:

| Client | `HEAD` | Porcelain lines (hash) | Stash | `RayTools/RayWorkPool.py` |
|---|---|---|---|---|
| SGK | `b510bc90b66985532d28996ab4e5b13b0ff71709` | 0 (`da39a3ee5e6b`) | 0 | `b4666fa89abb` |
| CPBH | `52142d75aebe00855804e2daff4f63aee50ffc3e` | 23 (`a772db72b9bc`) | 0 | `aaa6dc921865` |
| SI | `7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7` | 0 (`da39a3ee5e6b`) | 0 | `92be5b2c9e4c` |

They are the commits the checklists were measured at, so 06's figures still describe them.

---

## 3. Each prompt's acceptance, at `v0.2.0`

The acceptance is README §2's and the prompt's own; the review is the board's §1 paragraph for it,
every one of which found "every check of the note's §3 passed". The last column says what holds at
`v0.2.0` and how it was re-measured here, or why it was not.

| Prompt | Acceptance, in brief | What its review found | At `v0.2.0` |
|---|---|---|---|
| 01 | `import raypoolkit` and `from raypoolkit import RayWorkPool` in a fresh venv with no client; `compare_with_source.py` finds no difference beyond the allowed classes; the import guard | the check exits 0 (572 identical, 2 D-imp, 1 D-pool, 4 D-int) and bites, (a)–(h); the guard bites; the agent's issue `[01-a-kept-comment-names-the-datastore-service]` kept | **Re-measured.** The check, retired at `v0.1.0` (04), exits 0 from a worktree of the tag with the same counts and 12 declared files (§3.1). The guard's 3 tests pass in the 121 at both ends. Each smoke run imports the package from a fresh venv with no client on the path (§4). |
| 02 | the stand-ins; a test for every path through `run()` and every constructor check, each failing a named mutation; faults 1–4 pinned as they behave; the printed lines pinned (U9) | all 96 diffs replayed, each failing exactly the logged tests; opened `[02-the-constructor-does-not-check-its-sizes]` | **Re-measured in the suite**: 02's tests, as 04 left them (the fault pins and C1, C2 inverted, S4, X1 and `HANDLER_SETS` changed, five tests added; log 04 §1), pass in the 121 at both ends. The mutations were not re-run: the module changed at 04, which ran (r1)–(r10). **Under real Ray**, steps 1–4 take the lookup, available, compute–store–persist–validate and post-handler paths, and the four task-builder returns (§4.4). |
| 03 | `ray>=2.43`, `>=3.12`, the test package excluded; the suite at both ends in fresh venvs and in `venv/`; the release check; the workflow; `v0.1.0` after CI | the wheel rebuilt, 12,016 bytes, 9 entries; the workflow as specified; opened `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` | **Re-measured:** both ends (§3.1). `git diff 4e90a8a eaef0ce -- .github pyproject.toml` changes only `pyproject.toml`'s version and adds 05's `[tool.setuptools]` table, so the range and the workflow are 03's. `v0.1.0`'s wheel was not rebuilt here; `v0.2.0`'s was (§5). CI was not re-run; the gate's run is `38086076394`. |
| 04 | faults 1–5 fixed, each with a test the unfixed code fails; U8's checks; 02's pins inverted; the printed lines unchanged; (r1)–(r10) | every (r) replayed with the logged failures; the new suite on `v0.1.0`'s module fails 17 tests (34 entries); the module's diff read whole | **Re-measured:** the 121 at both ends. `RayWorkPool.py:530`, `:178`, `:109-142` and the 26 `.hex()` lines are where log 04 §1.1 says, read at `eaef0ce`. Under real Ray, (a) and (b) fail steps 3 and 1, and (c) fails nothing (§4.4, §4.5). The (r) diffs were not re-run. |
| 05 | `0.2.0` and `include-package-data = false`; `README.md` and `PROVENANCE.md` for `v0.2.0`; (R1) and (R2) 9 entries; `v0.2.0` after CI | (R1') and (R2') rebuilt: 13,565 bytes, 9 entries, no "absent from"; every "was" and "now" of the README checked against both modules | **Re-measured:** the wheel rebuilt offline from `git archive v0.2.0` has 13,565 bytes, the 9 entries, no "absent from" line, and `eaef0ce`'s four modules (§5). `PROVENANCE.md`'s "Re-running the check" was run as written (§3.1). The pin from GitHub was not installed again (U14); its record is cited (§5.1). |
| 06 | `docs/adoption/`: the README, three checklists and the script; the figures equal; every site constructs; every `path:line` read | the figures equal the orchestrator's; 40 links resolve; one citation corrected (`raypoolkit/__init__.py:16-19`) | **Re-measured:** `measure_client_pools.py sgk`, `cpbh` and `si` each exit 0 with nothing on stderr, and each output is byte-equal to its checklist's appendix (from `secondarygwkit.md:293`, `champbh.md:206`, `stochasticinstantons.md:232`), the clients being at the measured commits (§2.4). The `path:line`s of the checklists were not re-read. |

### 3.1 What was re-measured here

| Check | Command (from the repository root unless said) | Result |
|---|---|---|
| The suite, low end | `./venv/bin/python -m unittest discover -s raypoolkit/tests -t .` | `Ran 121 tests in 0.790s` / `OK` before any change; `Ran 121 tests in 0.881s` / `OK` at the end |
| The suite, high end | the same, from `<scratch>/base-hi/tree` with its venv | `Ran 121 tests in 1.464s` / `OK` |
| By module, every run | the verbose run's `(raypoolkit.tests.<module>.…)` lines | `test_construction` 15, `test_inherited_faults` 6, `test_package_imports` 3, `test_printed_lines` 18, `test_run_paths` 22, `test_scheduling` 7, `test_standins` 30, `test_task_builder` 20 |
| The import guard | in the suite: `test_package_imports`, 3 tests | pass at both ends |
| `black` | `./venv/bin/black --check raypoolkit docs` (25.1.0) | 16 files unchanged before; 17 after, with the smoke script |
| The equivalence check at `v0.1.0` | `PROVENANCE.md`'s "Re-running the check", with the worktree at `<scratch>/raypoolkit-v0.1.0` | exit 0: `RayWorkPool.py` 572 identical, 2 D-imp, 1 D-pool, 0 unclassified; `_timing.py` 4 D-int and the byte-for-byte span; 12 declared files present; 0 undeclared; `RESULT: OK`. The worktree was removed and `git worktree list` showed this checkout alone. It read SGK only through `git show` at `b510bc9` |
| The adoption script | `./venv/bin/python docs/adoption/measure_client_pools.py <client>` | each exit 0; byte-equal to the appendices (§3) |
| The package | `git diff eaef0ce -- raypoolkit pyproject.toml` | empty |

The suite was run with no Ray process up by either pattern of §4.1, before and after.

---

## 4. The package under Ray (U13)

### 4.1 The script and the runs

[`docs/extraction/ray_smoke_run.py`](extraction/ray_smoke_run.py) is a script, not a test; the
suite never collects it. Its docstring says what it is, how it is run and what it prints. In
brief:
- it sets `RAY_USAGE_STATS_ENABLED=0` before it imports `ray` or `raypoolkit` (§4.6);
- it imports the standard library, `ray`, `raypoolkit` and the three printed-line patterns of
  `raypoolkit/tests/test_printed_lines.py:35-39`; its objects (`Item`, four remote functions, the
  `Store` actor and `StorePool`) are its own, pickled by value. The patterns' import brings in
  `raypoolkit.tests.standins` (`test_printed_lines.py:25`), which patches nothing: the script checks
  that the pool module's `ray` is the `ray` it imported and that neither `ray.wait` nor `ray.get` is
  a `unittest.mock` object, and prints their module, `ray._private.worker`;
- it prints the versions and `raypoolkit.__file__`, then refuses, exiting 2 before it starts
  anything, if `ray.is_initialized()` is true or `pgrep -lf 'gcs_server|raylet|ray::'` finds a
  process;
- it starts Ray with `ray.init(num_cpus=4, include_dashboard=False, log_to_driver=False)`, and
  calls `ray.shutdown()` in a `finally`;
- it runs five steps, each isolated (an exception is that step's `FAIL`, and the next step runs),
  and exits 0 only if all pass, 1 if one fails.

Each end ran from a fresh offline venv with a fresh export installed editable (§2.4), from the
repository root, with `PYTHONPATH` unset:

```bash
env -u PYTHONPATH <scratch>/smoke-<end>/venv/bin/python docs/extraction/ray_smoke_run.py
```

The script run is the committed one (SHA-256 `6e631106abb181c0e155453b4eb0424c69981ea700713cd734eb901aee3804aa`). Its first draft, and what it showed,
are in log 07 §2 and §3.6.

Ray's processes were recorded before and after every run with two patterns, each process
attributed by its path: the script's own, `pgrep -lf 'gcs_server|raylet|ray::'`, and
`pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler'`, which also finds the Python processes a
local Ray starts (its dashboard, log monitor, monitor and process reaper). Both were empty before
and after each run of the table.

| | Low end | High end |
|---|---|---|
| Python / Ray | 3.12.15 / 2.43.0 | 3.13.16 / 2.55.1 |
| Started (BST) | 22:28:22 | 22:28:33 |
| `ray.init` | 4.4 s | 6.5 s |
| The script, in all (its own count) | 8.1 s | 10.7 s |
| `time -p`, real | printed as `real 10.:0` (sic); a second run at 22:30:20 gave 3.3 s, 7.2 s and `real 8.52` | 13.65 s |
| Exit code | 0 | 0 |
| Ray's session directory | `/tmp/ray/session_2026-10-10_22-28-25_349932_50472` | `/tmp/ray/session_2026-10-10_22-28-36_890588_50884` |
| Ray processes before and after, both patterns | 0 and 0 | 0 and 0 |

Steps 1–4 with Ray's start took about 6.2 s at the low end and 8.8 s at the high end (`ray.init`
plus the steps' own times), against the planner's 6.0 s and 9.0 s (prompt 07 §1.1). The script
asserts no time. At 2.55.1, `ray.init` writes a `FutureWarning` about
`RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO` to stderr; it is Ray's. Ray's "Started a local Ray instance."
line goes to stderr, and appears first in the captures below because stdout is buffered.

### 4.2 The output, low end

```text
2026-10-10 22:28:28,513	INFO worker.py:1841 -- Started a local Ray instance.
python: 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)]
ray: 2.43.0 (<scratch>/smoke-lo/venv/lib/python3.12/site-packages/ray/__init__.py)
raypoolkit: 0.2.0
raypoolkit.__file__: <scratch>/smoke-lo/tree/raypoolkit/__init__.py
RAY_USAGE_STATS_ENABLED: 0
ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
pgrep -lf 'gcs_server|raylet|ray::': no process
ray.init({'num_cpus': 4, 'include_dashboard': False, 'log_to_driver': False}): 4.4 s
session directory: /tmp/ray/session_2026-10-10_22-28-25_349932_50472
step 1, lookup-only, a generator task_list:
  PASS (0.0 s): results hold the 20 objects in order (0..19); nothing printed
step 2, the compute path:
  PASS (0.9 s): 12 results persisted, in order; store_ids 1-12; stored and available; labels item-0..item-11, payload 1; values from the compute tasks; completion line: Queue summary: 12 lookup (avg 14.03/sec), 12 compute (avg 14.03/sec), 12 store (avg 14.03/sec), 12 validation (avg 14.03/sec)
step 3, a persist with no validation, then a post handler:
  PASS (0.9 s): the post handler saw 5 objects, store_ids [1, 2, 3, 4, 5], each the object results holds
step 4, the availability path:
  PASS (0.0 s): the availability handler was called on the 10 objects looked up ([1, 2, 3, 4, 5, 101, 102, 103, 104, 105]), and the post handler on each; the item whose builder returned None was not looked up
step 5, the printed lines in real time:
    matched by BANNER_PATTERN:
      ** Smoke run, step 5
    matched by PROGRESS_PATTERN:
         -- 2026-10-10 22:28:31 (0.0565s running): 25/30 work items remaining = 16.67% complete
         -- 2026-10-10 22:28:31 (0.06s running): 20/30 work items remaining = 33.33% complete
         -- 2026-10-10 22:28:31 (0.11s running): 15/30 work items remaining = 50.00% complete
         -- 2026-10-10 22:28:31 (0.116s running): 10/30 work items remaining = 66.67% complete
         -- 2026-10-10 22:28:31 (0.166s running): 5/30 work items remaining = 83.33% complete
         -- 2026-10-10 22:28:31 (0.172s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.219s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.225s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.275s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.28s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.331s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.336s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.383s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.392s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.437s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
    matched by COMPLETE_PATTERN:
         -- ALL WORK ITEMS COMPLETE in time 0.437s
  PASS (0.4 s): 35 lines captured: 1 banner, 15 progress lines (= 15 passes for 30 tasks at create_batch_size=5, process_batch_size=2), 1 completion line; no stamp has a UTC offset; total_time 0.437 s
ray.shutdown(): ray.is_initialized() is False
Ray processes left after shutdown: 0 (after 0.0 s)
Summary: 5 of 5 steps passed; 8.1 s in all
```

### 4.3 The output, high end

```text
2026-10-10 22:28:42,220	INFO worker.py:2012 -- Started a local Ray instance.
<scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
  warnings.warn(
python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
ray: 2.55.1 (<scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/__init__.py)
raypoolkit: 0.2.0
raypoolkit.__file__: <scratch>/smoke-hi/tree/raypoolkit/__init__.py
RAY_USAGE_STATS_ENABLED: 0
ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
pgrep -lf 'gcs_server|raylet|ray::': no process
ray.init({'num_cpus': 4, 'include_dashboard': False, 'log_to_driver': False}): 6.5 s
session directory: /tmp/ray/session_2026-10-10_22-28-36_890588_50884
step 1, lookup-only, a generator task_list:
  PASS (0.1 s): results hold the 20 objects in order (0..19); nothing printed
step 2, the compute path:
  PASS (1.1 s): 12 results persisted, in order; store_ids 1-12; stored and available; labels item-0..item-11, payload 1; values from the compute tasks; completion line: Queue summary: 12 lookup (avg 10.9/sec), 12 compute (avg 10.9/sec), 12 store (avg 10.9/sec), 12 validation (avg 10.9/sec)
step 3, a persist with no validation, then a post handler:
  PASS (1.0 s): the post handler saw 5 objects, store_ids [1, 2, 3, 4, 5], each the object results holds
step 4, the availability path:
  PASS (0.1 s): the availability handler was called on the 10 objects looked up ([1, 2, 3, 4, 5, 101, 102, 103, 104, 105]), and the post handler on each; the item whose builder returned None was not looked up
step 5, the printed lines in real time:
    matched by BANNER_PATTERN:
      ** Smoke run, step 5
    matched by PROGRESS_PATTERN:
         -- 2026-10-10 22:28:45 (0.0678s running): 25/30 work items remaining = 16.67% complete
         -- 2026-10-10 22:28:45 (0.0689s running): 20/30 work items remaining = 33.33% complete
         -- 2026-10-10 22:28:45 (0.13s running): 15/30 work items remaining = 50.00% complete
         -- 2026-10-10 22:28:45 (0.133s running): 10/30 work items remaining = 66.67% complete
         -- 2026-10-10 22:28:45 (0.187s running): 5/30 work items remaining = 83.33% complete
         -- 2026-10-10 22:28:45 (0.19s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.246s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.249s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.301s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.304s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.358s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.36s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:46 (0.41s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:46 (0.414s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:46 (0.466s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
    matched by COMPLETE_PATTERN:
         -- ALL WORK ITEMS COMPLETE in time 0.466s
  PASS (0.5 s): 35 lines captured: 1 banner, 15 progress lines (= 15 passes for 30 tasks at create_batch_size=5, process_batch_size=2), 1 completion line; no stamp has a UTC offset; total_time 0.466 s
ray.shutdown(): ray.is_initialized() is False
Ray processes left after shutdown: 0 (after 0.0 s)
Summary: 5 of 5 steps passed; 10.7 s in all
```

### 4.4 The steps, and what each shows

| Step | What it asserts | Low end | High end |
|---|---|---|---|
| 1 | lookup-only (`compute_handler=None`, no `persist_handler=None`): a **generator** `task_list` of 20, `store_results=True`, `create_batch_size=3`, `process_batch_size=4`, `max_task_queue=5`; `results` holds the 20 objects in order; nothing printed | PASS | PASS |
| 2 | the compute path: 12 items built as `{"ref": …, "compute_payload": 1}`, a label builder and a validation handler, `store_results=True`, `process_batch_size=3`, `max_task_queue=4`, titled: every result is the persisted object, in order, `store_id`s 1–12, `stored` and `available`, compute given `label="item-<n>"` and `payload=1`, the value its compute task returned; no warning; the completion line counts 12 lookup, compute, store and validation | PASS | PASS |
| 3 | a persist with no validation, then a post handler, 5 items: the post handler is given each object with its `store_id` set, and the very object `results` holds (fault 2's fix) | PASS | PASS |
| 4 | the availability path: `compute_handler=None`, an availability handler and a post handler; the task builder returns `None` for one item and a list of two lookups for each of five others: the availability handler is called on the 10 objects looked up, and the post handler on each | PASS | PASS |
| 5 | the printed lines in real time: a titled lookup-only pool of 30 remote tasks of 0.05 s, `process_batch_size=2`, notifying on every pass: 1 line matches `BANNER_PATTERN` (its title the script's), 15 match `PROGRESS_PATTERN` (each of total 30), 1 matches `COMPLETE_PATTERN`; no stamp carries a UTC offset; `total_time` is set | PASS | PASS |

**Step 5's count is the script's own.** With both notify intervals 0, every pass of `run()` that
waits prints one notification (`raypoolkit/RayWorkPool.py:563-595` at `eaef0ce`), and each pass
waits for `min(process_batch_size, in flight)` refs (`:355-358`). The script's
`expected_passes(30, 5, 2, 200)` counts the passes from the loop's own rule and gives 15; at the
default `process_batch_size=1` it would give 30. The step asserts the count its own spelling
implies. Every run of step 5 gave 15: eleven runs at the two ends, the first draft's five included
(log 07 §3.6). The 35 lines captured are the empty line before the banner, the banner, 15 two-line notifications and
the three completion lines, the third "(no compute items were evaluated - all assets read from
datastore)" (log 02 §6.4).

**Three breakages and a refusal**, each at the high end; (a)–(c) are diffs to
`raypoolkit/RayWorkPool.py`, each applied to its own fresh export (`<scratch>/break-<x>/tree`, with
its own venv), never to the repository. Each passed `git apply --check`, and once applied
`git apply -R --check`; each was reverted with `git apply -R`, and the module's SHA-256 was then
`8f4c1d7d…8ce919`, as before (log 07 §4 gives the diffs). The repository's `git status` showed only
the new script throughout.

- **(a) fault 2's fix reverted**, `:530` `self._post_handler(replacement_obj)` →
  `self._post_handler(obj)`: step 3 fails, naming the `None` `store_id`s; the other four pass.

  ```text
  step 3, a persist with no validation, then a post handler:
    FAIL (1.1 s): __main__.StepFailure: the post handler was given store_id None for items [0, 1, 2, 3, 4] (store_ids it saw: [None, None, None, None, None]) [ray_smoke_run.py:328]
  ```
- **(b) fault 3's fix reverted**, `:178` `range(self._num_total_items)` → `range(len(task_list))`:
  step 1 fails at construction, and steps 2–5 run and pass (the steps' isolation).

  ```text
  step 1, lookup-only, a generator task_list:
    FAIL (0.0 s): builtins.TypeError: object of type 'generator' has no len() [RayWorkPool.py:178]
  ```
- **(c) fault 1's fix reverted**, the 26 `.hex()` → `.hex` (`:300` … `:546`): **every step
  passes**, exit 0 (§4.5).
- **(d) Ray already up.** A Python process of this prompt's own (`<scratch>/scripts/ray_holder.py`,
  in the background, with `RAY_USAGE_STATS_ENABLED=0`) called the same `ray.init(...)`, wrote a
  ready file and waited for a stop file, for at most 180 s, with `ray.shutdown()` in a `finally`.
  Its session was `/tmp/ray/session_2026-10-10_22-30-02_371190_52353`. The script, run while it was
  up, printed its versions and refused, exit 2, in 1.09 s, and made no session directory:

  ```text
  python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
  ray: 2.55.1 (<scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/__init__.py)
  raypoolkit: 0.2.0
  raypoolkit.__file__: <scratch>/smoke-hi/tree/raypoolkit/__init__.py
  RAY_USAGE_STATS_ENABLED: 0
  ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
  REFUSED: pgrep -lf 'gcs_server|raylet|ray::' exited 0:
    52372 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server
    52400 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet
    52402 ray::DashboardAgent
    52403 ray::RuntimeEnvAgent
    52431 ray::IDLE
    52432 ray::IDLE
    52433 ray::IDLE
    52434 ray::IDLE
  ```

  Then the stop file was written; the holder printed `ray.shutdown(); ray.is_initialized() is
  False` and exited 0, and both patterns were empty at 22:30:12.

Every (a)–(d) run left no Ray process by either pattern; (a)–(c) each made one session directory
(`session_2026-10-10_22-29-03_386918_51164`, `…_22-29-22_848341_51457`, `…_22-29-39_766865_51710`).

### 4.5 Fault 1 under real Ray

`[00-in-flight-work-is-keyed-on-a-bound-method]` keyed `_inflight`, `_data` and `_compute_data` on
the bound method `ref.hex`, which compares by the identity of the ref (the board's §4). 04 keyed
them on `ref.hex()`. **Under real Ray the fix is not observable**: with (c) applied, every step
passes at 2.55.1, because `ray.wait` returns the very `ObjectRef` objects it was given, so the bound
methods still find their keys. This is what README §0.2 said of fault 1 ("The pool works only
because `ray.wait` returns the very objects it was given"), now measured under a running Ray.

So fault 1's fix is guarded **by the stand-in only**:
`raypoolkit/tests/test_inherited_faults.py:44`,
`test_fresh_refs_from_wait_complete_every_path`, whose stand-in `ray.wait` returns equal but
distinct refs when `fresh_refs` is set (`raypoolkit/tests/standins.py:111`, `:182`), and X1
(`test_run_paths.py:405`), seeded under `ref.hex()` only. A Ray release whose `ray.wait` returned
fresh refs would make the fix matter; nothing here shows that any does. It is a finding, not a
breakage, and not an issue: the package is right, and the test that guards it exists (§10).

### 4.6 No usage report

This machine's `~/.ray/config.json` enables Ray's usage statistics, and the reporter, the API
server's `UsageStatsHead`, runs even with `include_dashboard=False`. The environment variable
`RAY_USAGE_STATS_ENABLED=0` takes priority over the file, so the script sets it (by assignment)
before it imports `ray`, and (d)'s holder did too; the file was not edited. In each of this
prompt's thirteen Ray sessions (§4.1's two, the second low-end run, (a)–(c), (d)'s holder, and
the six of the script's first draft, log 07 §3.6), `dashboard.log` says, at 2.43.0 and 2.55.1
respectively:

```text
INFO usage_stats_head.py:197 -- Usage reporting is disabled.
INFO usage_stats_head.py:200 -- Usage reporting is disabled.
```

`grep -ril usage` over each session's `logs/` names `dashboard.log`, `debug_state.txt`,
`gcs_server.out`, `raylet.out`, and `debug_state_gcs.txt` (2.43.0) or `monitor.log` (2.55.1). In
`dashboard.log` the matches are the `UsageStatsHead` module's loading and the line above; in the
others they are Ray's resource and object-store accounting ("Resource usage", "Current usage",
"GetAllResourceUsage", "Total Usage"). None of the seven sessions of the committed script's runs and its holder holds a file whose name
contains `usage_stats`.

---

## 5. The release (U14)

### 5.1 The pin, installed by the release record

U14 (README §6.2) decided that the pin is cited, not fetched again. The board's *Release of
`v0.2.0`* records, step by step, what the user did on 2026-10-10:
1. `git push origin eaef0ce:main` moved `origin/main` from `914070c` to `eaef0ce`;
2. run `38075908457` on `eaef0ce` passed both jobs: `suite (low)`, 3.12.15 / 2.43.0, `raypoolkit`
   at `0.2.0`, `Ran 121 tests … OK`, `black` "15 files would be left unchanged."; `suite (high)`,
   3.13.16 / 2.55.1, `Ran 121 tests … OK`;
3. `v0.2.0`, annotated (tag object `4e7eb15`, message "raypoolkit 0.2.0"), on `eaef0ce`, made by the
   user and pushed;
4. a client's install: `uv pip install --no-cache "raypoolkit @
   git+https://github.com/ds283/RayPoolKit@v0.2.0" "ray==2.55.1"` into a fresh 3.13.16 venv, whose
   `direct_url.json` records `requested_revision` `v0.2.0` and `commit_id` `eaef0ce…`; the four
   modules and no `tests/`; from an empty directory with `-I`, the two public names import,
   `version` is `0.2.0`, `requires` is `['ray>=2.43']`, `ray.is_initialized()` is false, and
   `import raypoolkit.tests` raises `ModuleNotFoundError`;
5. `main` pushed (`9a00f80`, `b2b6ab4`), and run `38076190172` on `b2b6ab4` passed both jobs.

The tag still peels to `eaef0ce` (§2.3).

### 5.2 The wheel, rebuilt offline

```bash
git archive v0.2.0 | tar -x -C <scratch>/export-v020
uv build --wheel --offline --out-dir <scratch>/wheel <scratch>/export-v020
```

The export held `.github`, `.gitignore`, `CLAUDE.md`, `docs`, `LICENSE`, `prompts`,
`PROVENANCE.md`, `pyproject.toml`, `raypoolkit`, `README.md`, and no `build/`, `dist/` or
`*.egg-info`. The build exited 0; its log (56 lines) has **0** "absent from" lines, and its only
warnings are setuptools' two "byte-compiling is disabled, skipping." `uv` ran setuptools under
Python 3.14 (`raypoolkit-0.2.0-py3.14.egg-info` in the log), as logs 03 §6.2 and 05 §6.4 found; the
wheel is `py3-none-any` (`WHEEL`: `Generator: setuptools (84.0.0)`, `Tag: py3-none-any`).

`raypoolkit-0.2.0-py3-none-any.whl`, **13,565 bytes**, **9 entries**:

| Entry | Bytes |
|---|---|
| `raypoolkit/RayWorkPool.py` | 26,152 |
| `raypoolkit/__init__.py` | 740 |
| `raypoolkit/_timing.py` | 2,373 |
| `raypoolkit/contract.py` | 1,886 |
| `raypoolkit-0.2.0.dist-info/licenses/LICENSE` | 11,357 |
| `raypoolkit-0.2.0.dist-info/METADATA` | 243 |
| `raypoolkit-0.2.0.dist-info/WHEEL` | 91 |
| `raypoolkit-0.2.0.dist-info/top_level.txt` | 11 |
| `raypoolkit-0.2.0.dist-info/RECORD` | 728 |

None is under `raypoolkit/tests/`. Each of the four modules equals `git show
eaef0ce:raypoolkit/<module>` byte for byte (SHA-256 prefixes `8f4c1d7d5aa2b133`,
`e7af5b53f61577ca`, `9ad06d7ddd1b0568`, `ddb1dcc8d528fc10`). `METADATA` gives `Version: 0.2.0`,
`Requires-Python: >=3.12` and `Requires-Dist: ray>=2.43`. The size and entries are log 05 §3.3's
and the board's (05's review); the wheel's SHA-256 is not compared, since an export's file times
are its commit's and a wheel's bytes follow them (03's review). Nothing of it is committed.

---

## 6. Issues

### 6.1 Resolved on the board (§4), eight

| Issue | Opened by | Closed by | Guarded by (at `eaef0ce`) |
|---|---|---|---|
| `[00-in-flight-work-is-keyed-on-a-bound-method]` | planning, `4cb493f` (fault 1) | 04, `0b6ffd2` | `test_inherited_faults.py:44` `test_fresh_refs_from_wait_complete_every_path`; X1 (`test_run_paths.py:405`). The stand-in only (§4.5) |
| `[00-a-post-handler-after-persist-gets-the-unpersisted-object]` | planning (fault 2) | 04, `0b6ffd2` | `test_inherited_faults.py:103` `test_the_post_handler_after_persist_gets_the_persisted_object`; S4 (`test_run_paths.py:277`). Under Ray: step 3, which (a) fails |
| `[00-store-results-sizes-from-len-of-the-task-list]` | planning (fault 3) | 04, `0b6ffd2` | `test_inherited_faults.py:124` `test_store_results_accepts_a_generator_task_list`. Under Ray: step 1, which (b) fails |
| `[00-the-constructor-checks-its-handlers-unevenly]` | planning (fault 4) | 04, `0b6ffd2` (U8) | `test_inherited_faults.py:141`, `:158`; C1, C2, C5, C6 in `test_construction.TestHandlerChecks`; `test_printed_lines`' spelling test. Under Ray: steps 1, 4 and 5 construct lookup-only pools with no `persist_handler=None` |
| `[00-messages-say-maker-and-the-module-has-no-licence-header]` | planning (fault 5) | 04, `0b6ffd2` (U11) | the message assertions of C1, C2, C5, C7; `test_inherited_faults.py:177` `test_every_package_module_carries_the_licence_header` |
| `[01-a-kept-comment-names-the-datastore-service]` | 01, `49f3ddf` (log 01 §5.1) | 04, `0b6ffd2` (`RayWorkPool.py:464`) | no test (a comment); `git grep -n "Datastore service" eaef0ce -- raypoolkit` is empty |
| `[02-the-constructor-does-not-check-its-sizes]` | the review of 02, `307ed96` (log 02 §6.1) | 04, `0b6ffd2` (`:136-142`) | C7, `test_construction.py:96` `test_a_size_below_one_raises_value_error` |
| `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` | 03, `4e90a8a` (log 03 §6.1) | 05, `eaef0ce` (`include-package-data = false`) | no test; 05's release check (R2) and its breakage (a) (log 05 §3.3, §5); here, the offline wheel's 9 entries (§5.2) |

### 6.2 None open

`docs/OPEN_ISSUES.md` counts **0** open before and after this prompt. This prompt opens none: what
it found (§4.5, fault 1 observable under the stand-in only) is not a defect of the package, and is
recorded as a gap (§10).

### 6.3 Fault 6, never an issue here

README §0.2's fault 6: CPBH's and SI's copies assign `_last_num_available_complete` from
`_num_store_complete`, so their "available" rate is computed from the store count. SGK's copy, the
source, already had the fix (`e81b145`, README §0), so the package never carried the fault and no
issue was opened for it. 02 pinned the right behaviour,
`test_printed_lines.py:371` `test_the_available_rate_is_per_interval`, which (m5) fails (log 02 §2,
deviation 3). The fix reaches CPBH and SI on adoption; at their measured commits no site gives an
`available_handler`, so no line they print changes (log 06 §2, deviation 17).

---

## 7. Decisions

**Made by the user** (README §6.1): **D1** (2026-10-10), extract `RayWorkPool` as a separate,
reusable component; **D2** (DatastoreKit's, 2026-10-07), the datastore layer first, the pool a
separate unit of work.

**Put to the user** (README §6.2), every one taken as recommended, U8 and U9 with amendments, U5
amended by U12. "Recorded" is the commit that recorded it as taken in the plan (README §6.2, and the
commit's subject); "applied" is where it took effect.

| Decision | What was decided | Taken, for | Recorded | Applied |
|---|---|---|---|---|
| **U1** | RayPoolKit, package `raypoolkit`, public `ds283/RayPoolKit` | 2026-10-10, at set-up | `4cb493f` | `49f3ddf` (`pyproject.toml`'s name) |
| **U2** | SGK's copy, imported faithfully | at set-up | `4cb493f` | `49f3ddf` (`PROVENANCE.md`) |
| **U3** | no dependency on `datastorekit`; the pool typed by a `Protocol`; `format_time` internalised | at set-up | `4cb493f` | `49f3ddf` (`contract.py`, `_timing.py`) |
| **U4** | keep `RayWorkPool.py`; re-export the class from the root | 2026-10-10, for 01 | `97f9ff0` | `49f3ddf`; pinned by the guard's test 3 |
| **U5** | no client edits its `RayTools/` until it adopts | 2026-10-10, for 01 | `97f9ff0` | in force from `49f3ddf` (`PROVENANCE.md`, "The freeze"); amended by U12 |
| **U6** | real `ObjectRef(bytes)`; `ray.wait` and `ray.get` replaced in-process | 2026-10-10, for 02 | `d9adb9b` | `b9f6dec` (`raypoolkit/tests/standins.py`) |
| **U7** | Python `>=3.12`, Ray `>=2.43`; tested 3.12.15 / 2.43.0 and 3.13.16 / 2.55.1 | 2026-10-10, for 03 | `c73fc91` | `4e90a8a` (`pyproject.toml`, the workflow) |
| **U8** | the default store and persist handlers apply only with a compute handler (option b); every argument check `ValueError`; the four compute-path arguments checked | 2026-10-10, for 04, with two amendments | `c207238` | `0b6ffd2` (`RayWorkPool.py:109-142`) |
| **U9** | the printed lines pinned against a scripted clock; the three consumer patterns checked | 2026-10-10, for 02, as amended at 02's writing | `d9adb9b` | `b9f6dec` (`test_printed_lines.py`) |
| **U10** | no shim for CPBH's `store_handler` | 2026-10-10, for 06 | `a1d64ea` | not applicable to the package; recorded in `docs/adoption/champbh.md` (`67f3f7e`): no CPBH site affected |
| **U11** | SI's licence header, byte for byte, on all four package modules | 2026-10-10, for 04 | `c207238` | `0b6ffd2` (lines 1–15 of each module) |
| **U12** | U5 amended: a DatastoreKit-first adoption may rewrite the one `ShardedPool` import | 2026-10-10, for 06 | `a1d64ea` | `67f3f7e` (`docs/adoption/README.md` §5) |
| **U13** | a smoke run under real Ray: a script in `docs/extraction/`, not a test | 2026-10-10, for 07 | `787507a` | the commit that adds this document (§4) |
| **U14** | cite the release record; rebuild the wheel offline; no network | 2026-10-10, for 07 | `787507a` | the commit that adds this document (§5) |

---

## 8. Deviations across the campaign

**How they were counted.** An entry is a top-level numbered item of a log's §2, "Deviations from
the prompt", or a slip that §2 records in a paragraph or bullet of its own (log 04 has one such
paragraph, log 05 two bullets). Its class is the label in its text; where the label is not in the
item, the class is the one the section's opening sentence gives it ("Each is an IMPLEMENTATION
CHOICE at the orchestrator's direction", which covers the orchestrator's clarifications in logs 02
to 06, "except 1" or "except 1 and 6" in logs 05 and 06, which are STRUCTURALLY REQUIRED). A
sentence saying there was none ("No UNINTENDED DRIFT.", logs 01, 02 and 03) is not an entry. A
scratch parser listed each entry with the labels in its text, and every entry without one was read
(log 07 §3.9).

| Log | Entries | STRUCTURALLY REQUIRED | IMPLEMENTATION CHOICE | UNINTENDED DRIFT |
|---|---|---|---|---|
| 01 | 9 | 1 | 8 | 0 |
| 02 | 13 | 0 | 13 | 0 |
| 03 | 15 | 2 | 13 | 0 |
| 04 | 19 | 0 | 18 | 1 |
| 05 | 20 | 2 | 16 | 2 |
| 06 | 26 | 3 | 21 | 2 |
| **All** | **102** | **8** | **89** | **5** |

Prompt 07's §1.3 gave 1 / 8 / 1, 0 / 7 / 1, 2 / 5 / 1, 0 / 10 / 1, 2 / 10 / 2 and 4 / 9 / 2 for
the six logs. Those are counts of the labels' words, line by line, as it warned, and the parser
reproduces them exactly. They are not counts of entries, for three reasons: one sentence classes
all of a log's orchestrator clarifications (7, 8, 8, 8 and 14 entries in logs 02 to 06), so that one
word stands for several entries, or none where the sentence's label is wrapped across two lines; a
label wrapped inside an entry is not seen by a line-by-line count; and a sentence saying there was
none ("No UNINTENDED DRIFT.", logs 01, 02 and 03) is a word but not an entry. So the entries above
were counted from the items, and each class read from the item or from the sentence that classes
it.

**Every UNINTENDED DRIFT entry**, each corrected before it affected a result:
- **log 04 §2, the paragraph after item 18**: the first run of the new suite on `v0.1.0`'s module
  was driven from `zsh`, which did not split the file list, so its snapshot hashed nothing; it was
  re-run from `bash`, with the same failing set.
- **log 05 §2, first slip**: a `zsh` wrapper stopped after (R1)'s build, since `zsh` expands a word
  beginning `=`; (R2) was built by a second call, and every later build by `bash`.
- **log 05 §2, second slip**: the "Changes" probe's first version shared one stand-in across three
  size cases, so the call cap fired first; each case got its own stand-in and the probe was re-run.
- **log 06 §2 item 25**: four read-only commands outside the brief's list for other repositories
  (`git branch --show-current`, `git remote -v`, `git remote get-url`, and an `ls -l` of a symlink
  in SI's working tree); nothing was written, and no checklist fact rests on them.
- **log 06 §2 item 26**: the script's first runs preceded a one-line comment fix; the later output
  is byte-equal.

**Every STRUCTURALLY REQUIRED entry that changed what a prompt delivered.** The other three
(log 01 item 6, log 03 items 9 and 10) changed a procedure, not a delivered file: the guard run as a
script to show its test 1, and two workflow steps with no local counterpart.

| Log, item | What it changed |
|---|---|
| 05 §2 item 1 | `README.md`'s "Changes in `v0.2.0`" does not say the old checks were "silently ignored": `v0.1.0` refused two of them, with `RuntimeWarning` and `RuntimeError` |
| 05 §2 item 9 | `README.md` says "each fault's fix is guarded", not "each fix", since 04's reworded comment has no test |
| 06 §2 item 1 | the checklists cite the constructor as `RayWorkPool.py:88-206` and its checks as `:109-142`, not the prompt's `:88-215` |
| 06 §2 item 6 | SGK's checklist quotes `A3_OUTPUT` as the five lines it holds, not "six" |
| 06 §2 item 15 | the script and the checklists split the "titled" sites into `title=None` (28, 12, 10) and set (26, 5, 6) |

---

## 9. Observations not acted on

Every item of every log's "Observations not acted on" section, **38** in all (01 §5: 7, 02 §6: 7,
03 §6: 6, 04 §5: 6, 05 §6: 5, 06 §9: 7; counted as the numbered items of each section). The
disposition at `v0.2.0` is decided from the later logs, the board and a read of `eaef0ce`, and
changes nothing.

| Log, item | Observation | At `v0.2.0` |
|---|---|---|
| 01 §5.1 | a kept comment names SGK's `Datastore` service | **addressed**: `[01-a-kept-comment-names-the-datastore-service]`, closed by 04 (`RayWorkPool.py:464`) |
| 01 §5.2 | `_timing.py`'s docstring and the guard's list name client modules | **addressed** by the user's decision at 02's writing: `CLAUDE.md` excepts both (the board's review of 01) |
| 01 §5.3 | the guard cannot run test 1 when the package does not import | **still an observation**, by design (log 01 deviation 6) |
| 01 §5.4 | test 2 does not check what `from raypoolkit import RayWorkPool` binds | **still an observation**; test 3 catches it (`test_package_imports.py` is unchanged since `49f3ddf`) |
| 01 §5.5 | the board's line for fault 2 said `:489` | **addressed** by 01's review (the board's Package line, `:487-492`); at `v0.2.0` the call is `:530` |
| 01 §5.6 | `pip freeze` records the editable install against the `HEAD` at install | **no longer true as stated**: log 03 §6.3 corrects it, the line names the `HEAD` at the freeze; here `venv/`'s freeze names `ff265ee`, a commit made after its install |
| 01 §5.7 | `raypoolkit.egg-info/` left at the root, gitignored | **still so** (`git status --ignored`) |
| 02 §6.1 | a size below 1 hangs or raises Ray's error | **addressed**: opened by 02's review as `[02-the-constructor-does-not-check-its-sizes]`, closed by 04 (`:136-142`) |
| 02 §6.2 | four equivalent mutations survive (Z2–Z5) | **still an observation**: the clamps at `:380`, `:452`, `:477`, `:510`, `:548`, `and allow_store` at `:302`, `and len(self._todo) > 0` at `:290`, `_compute_data.pop` at `:443`; not re-measured since 02 (log 04 §5.6) |
| 02 §6.3 | the progress line counts items not yet built, not items not complete | **still so**, pinned; under Ray, step 5's last ten progress lines say `0/30 … 100.00% complete` with the suffix while tasks are in flight (§4.2) |
| 02 §6.4 | "all assets read from datastore" for any pool with no completed compute | **still so** (`:612-615`), a printed line; step 5 prints it (§4.4) |
| 02 §6.5 | (m1) moves only the fault-1 test; X1 is seeded both ways | **addressed** by 04: X1 seeded under `ref.hex()` only (the board's §4) |
| 02 §6.6 | (m2) moves the fault-2 test and S4 | **addressed** by 04: both inverted |
| 02 §6.7 | `ScriptedClock.stamp()` is used only by the stand-in's own test | **still so** (`standins.py:243`; used at `test_standins.py:187` alone) |
| 03 §6.1 | a stale `egg-info` manifest ships the tests in a wheel | **addressed**: `[03-…]`, closed by 05 |
| 03 §6.2 | `uv build` runs setuptools under Python 3.14 | **still so** (§5.2); the wheel is `py3-none-any` |
| 03 §6.3 | `pip freeze`'s editable line names the `HEAD` at the freeze | **still so**, and it corrects log 01 §5.6 |
| 03 §6.4 | tool-internal temporary directories outside the scratch directory | **still so**; a record, not in the repository |
| 03 §6.5 | the release check's `raypoolkit.tests` check passes vacuously with no parent package | **still an observation** of 03's release check; the other checks catch that case |
| 03 §6.6 | a lookup-only pool may also pass `store_handler=None`; the constructor checks neither | **no longer true**: since 04 (U8) the constructor checks `store_handler` against the compute handler (`:109-134`) |
| 04 §5.1 | `README.md` describes `v0.1.0`'s constructor | **addressed** by 05 ("Which handlers a pool needs") |
| 04 §5.2 | `PROVENANCE.md:40` describes `v0.1.0` | **addressed** by 05 ("At `v0.1.0`, …") |
| 04 §5.3 | the check's `NO_SOURCE` text for `test_inherited_faults.py` | **still so** (`compare_with_source.py:121`), true of `v0.1.0`, where the retired check runs (04's review) |
| 04 §5.4 | a size that does not compare with 1 raises `TypeError` at construction | **still so** (`:141`) |
| 04 §5.5 | a pool with no compute handler may still take `available_handler` and `post_handler` | **addressed**: 05's README says so, and 06's checklists; step 4 runs such a pool under Ray |
| 04 §5.6 | 02's equivalent mutations not re-measured | **still so** |
| 05 §6.1 | `PROVENANCE.md`'s "New here" lists only 01's files | **still so**, a record of the import (05's review) |
| 05 §6.2 | the D-fmt bullet's "line numbers are SGK's" | **still so**, read as of `v0.1.0` |
| 05 §6.3 | the stale manifest persists, and no longer reaches a wheel | **still so**: the repository's `raypoolkit.egg-info/SOURCES.txt` lists 10 test files; the wheel of §5.2 has none |
| 05 §6.4 | `uv build` under Python 3.14 | **still so** (as 03 §6.2) |
| 05 §6.5 | tool-internal temporary directories | **still so**; a record |
| 06 §9.1 | the plan's G2 says "six pinned lines" | **addressed** by 06's review: README §7 corrected in place, with a dated note |
| 06 §9.2 | §0.2's "Titled" counts the keyword | **addressed** in 06 itself (deviation 15), accepted by its review |
| 06 §9.3 | SGK's `test_layer_is_generic.py:357` would test an allowance for a package that is gone | **still an observation**, SGK's; its checklist advises |
| 06 §9.4 | SI's `.claude/rules/ray-dispatch.md:103-105` cite the copy's lines, unchecked | **still unverified**, SI's |
| 06 §9.5 | the script reads one blob per `git show`, about 40 s on SGK | **still so** |
| 06 §9.6 | CPBH's remote is named `github` | **still so**; nothing depends on it |
| 06 §9.7 | SGK's `main.py:3247` settled by reading | **still so**, SGK's to measure; fault 2's fix itself is shown under Ray by step 3 and (a) |

Tally, by the last column's first words: **12 addressed** (by a prompt, a review or a decision),
**2 no longer true**, and **24 still so, still observations or still unverified**. Each of the 24
was left as an observation by its log, and no later log or review opened it as an issue; neither
does this prompt.

---

## 10. Known gaps

- **G2–G4.** No client has adopted the package. G2 (SGK), G3 (CPBH) and G4 (SI) are each that
  client's campaign, in its own repository, planned from its checklist in `docs/adoption/`
  (README §7). The checklists are measured at SGK `b510bc9`, CPBH `52142d7` and SI `7bb3efd`,
  commits that will move; each client re-measures before acting (`docs/adoption/README.md` §6).
  After the close, a gate is recorded on the board when it holds, in a records commit of its own.
- **What remains unverified.**
  - **A multi-node Ray cluster.** The smoke run is one local instance on one machine (§4). Nothing
    here has run the pool on a cluster, on several nodes or with remote workers.
  - **A client's own suites under the package.** No client's code or tests were run against any
    release (README §5 rule 5).
  - **Python 3.14 and Ray above 2.55.1**, inside the declared range (`>=3.12`, `ray>=2.43`) and
    untested (U7; `README.md`, "Supported versions").
- **Fault 1 is guarded by the stand-in only** (§4.5). Under real Ray at 2.55.1 the pool keyed on
  bound methods runs every step; only the stand-in's `fresh_refs` shows the fix.
- **DatastoreKit's README**, by the plan's account (README §0: its §8.1 records `RayWorkPool` as
  the later unit of work this campaign is), says that `RayWorkPool` is not part of that package.
  Updating it is DatastoreKit's (README §1, "Out of scope"); no prompt here edits DatastoreKit, and
  it was not read for this.

---

## 11. Reproduction

From a clean checkout of the commit that adds this document, at the repository root, with no Ray
process up (`pgrep -lf 'gcs_server|raylet|ray::'` and
`pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler'` both empty). `S` is an empty scratch
directory outside the repository; every `uv` command is offline; run the commands in `bash`.

### 11.1 The suite and the checks (§3.1)

```bash
./venv/bin/python -m unittest discover -s raypoolkit/tests -t . -v
./venv/bin/black --check raypoolkit docs
git diff eaef0ce -- raypoolkit pyproject.toml

REPO=$(pwd)
git worktree add --detach $S/raypoolkit-v0.1.0 v0.1.0
(cd $S/raypoolkit-v0.1.0 && "$REPO"/venv/bin/python docs/extraction/compare_with_source.py)
git worktree remove $S/raypoolkit-v0.1.0

mkdir -p $S/base-hi/tree && git archive HEAD | tar -x -C $S/base-hi/tree
uv venv --offline -p /opt/local/bin/python3.13 $S/base-hi/venv
uv pip install --offline --python $S/base-hi/venv/bin/python -e $S/base-hi/tree "ray==2.55.1"
(cd $S/base-hi/tree && env -u PYTHONPATH $S/base-hi/venv/bin/python -m unittest discover -s raypoolkit/tests -t . -v)

for c in sgk:secondarygwkit cpbh:champbh si:stochasticinstantons; do
  IFS=: read k f <<< "$c"
  ./venv/bin/python docs/adoption/measure_client_pools.py $k > $S/measure-$k.md
  n=$(grep -n '^# `RayWorkPool` in ' docs/adoption/$f.md | cut -d: -f1)
  tail -n +$n docs/adoption/$f.md | cmp - $S/measure-$k.md && echo "$k: equal"
done
```

### 11.2 The smoke run (§4.1–§4.3)

```bash
for end in lo:3.12:2.43.0 hi:3.13:2.55.1; do
  IFS=: read e py ray <<< "$end"
  mkdir -p $S/smoke-$e/tree && git archive HEAD | tar -x -C $S/smoke-$e/tree
  uv venv --offline -p /opt/local/bin/python$py $S/smoke-$e/venv
  uv pip install --offline --python $S/smoke-$e/venv/bin/python -e $S/smoke-$e/tree "ray==$ray"
  time -p env -u PYTHONPATH $S/smoke-$e/venv/bin/python docs/extraction/ray_smoke_run.py
  echo "exit=$?"
done
```

Run the ends one after the other: the script refuses to start while another instance's processes
are up. The script run is the checkout's, from the repository root, so that `sys.path[0]` is
`docs/extraction/` and `raypoolkit` comes from the export, whose path the run prints.

### 11.3 The breakages (§4.4)

Each diff is log 07 §4's, saved as `$S/a.diff`, `$S/b.diff` or `$S/c.diff`; each is applied to its
own export, at the high end:

```bash
for x in a b c; do
  mkdir -p $S/break-$x/tree && git archive HEAD | tar -x -C $S/break-$x/tree
  uv venv --offline -p /opt/local/bin/python3.13 $S/break-$x/venv
  uv pip install --offline --python $S/break-$x/venv/bin/python -e $S/break-$x/tree "ray==2.55.1"
  (cd $S/break-$x/tree && git apply --check $S/$x.diff && git apply $S/$x.diff && git apply -R --check $S/$x.diff)
  env -u PYTHONPATH $S/break-$x/venv/bin/python docs/extraction/ray_smoke_run.py; echo "exit=$?"
  (cd $S/break-$x/tree && git apply -R $S/$x.diff && shasum -a 256 raypoolkit/RayWorkPool.py)
done
```

(a) and (b) exit 1, (c) exits 0, and each module's SHA-256 after the revert is `8f4c1d7d…8ce919`.
For (d), log 07 §4 gives the holder, `ray_holder.py`: start it in the background with the
high-end venv and two file paths, wait for the first, run the script (exit 2), then create the
second, and check that both patterns are empty.

### 11.4 The release (§5)

```bash
mkdir -p $S/export-v020 $S/wheel
git archive v0.2.0 | tar -x -C $S/export-v020
uv build --wheel --offline --out-dir $S/wheel $S/export-v020 > $S/build.log 2>&1; echo "exit=$?"
grep -c "absent from" $S/build.log
ls -l $S/wheel
unzip -l $S/wheel/raypoolkit-0.2.0-py3-none-any.whl
for m in RayWorkPool.py __init__.py _timing.py contract.py; do
  unzip -p $S/wheel/raypoolkit-0.2.0-py3-none-any.whl raypoolkit/$m | cmp - <(git show eaef0ce:raypoolkit/$m) && echo "$m equal"
done
```

### 11.5 The records (§2)

```bash
git log --reverse --format='%h %s' ff265ee
git for-each-ref refs/tags --format='%(refname:short) %(objectname:short) %(*objectname:short)'
gh run list --limit 20
git show eaef0ce:raypoolkit/RayWorkPool.py | sed -n '178p;355,358p;530p;563,595p'
git show eaef0ce:raypoolkit/RayWorkPool.py | grep -c '\.hex()'
git show eaef0ce:raypoolkit/tests/test_printed_lines.py | sed -n '25p;35,39p'
```

---

## 12. Summary for the board

- The campaign delivered `raypoolkit` from SGK's `RayWorkPool.py` (`b510bc9`, blob `b4666fa`), a
  suite of 121 tests with no Ray cluster, the five inherited faults fixed, three adoption
  checklists, and two releases tagged after green CI: `v0.1.0` (`4e90a8a`), `v0.2.0` (`eaef0ce`).
- At `v0.2.0` the suite passes at both ends (121), `black` is clean over 17 files, the equivalence
  check at `v0.1.0` exits 0, and the adoption script reproduces each checklist's appendix.
- Under real Ray, at both ends, the smoke script's five steps pass, Ray leaves no process, and no
  usage is reported; it fails with fault 2's or fault 3's fix reverted, and refuses when Ray is up.
- With fault 1's fix reverted every step still passes: `ray.wait` returns the refs it was given, so
  fault 1 is guarded by the stand-in only.
- The wheel rebuilt offline from `v0.2.0` has 13,565 bytes, 9 entries and `eaef0ce`'s modules; the
  pin's install from GitHub is cited from the release record (U14).
- Eight issues opened and resolved; none open; none opened by 07.
- 102 deviations over six logs (8 STRUCTURALLY REQUIRED, 89 IMPLEMENTATION CHOICE, 5 UNINTENDED
  DRIFT), and 38 observations, each with its disposition.
- Gaps: G2–G4; a multi-node cluster; the clients' suites; Python 3.14 and Ray above 2.55.1; fault 1
  under real Ray; DatastoreKit's README.
