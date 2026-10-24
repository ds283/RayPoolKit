# rehearsal-lock campaign — implementation state

**Last updated:** 2026-10-24 · **Status: ACTIVE — 4 prompts written (01, 02, 03, and the fix 03a), of 6; 01 landed
(`6733447`), reviewed, and CI green at both ends: `raypoolkit/rehearsal_lock.py`, the lock at
`~/.raypoolkit/rehearsal-lock` with the old-location refusal, the owner file, the five commands
and the process rule by temp dir, standard library only; its 103 tests and two guard tests. 02
landed (`722466a`), reviewed, and CI green at both ends: `docs/rehearsal-lock/ray_proof.py`, run
under real Ray holding the real shared lock, exits 0 at 3.12.15 / Ray 2.43.0 and 3.13.16 / Ray
2.55.1 (`ray[default]` scratch venvs, the user's choice of 2026-10-24), 31 checks each, for the
agent and again for the orchestrator; its offline replay fails under M10 and M12 at both ends;
nothing under `raypoolkit/` changed. 03 landed (`89d6875`), reviewed: `pyproject.toml` at `0.3.0`,
the contract `docs/rehearsal-lock.md` (98 statements, each checked), and `README.md`,
`PROVENANCE.md` and `CLAUDE.md` true of `v0.3.0`; the suite 226 → 226 at both ends; the release
check passes with and without the stale manifest (10 entries, none under `raypoolkit/tests/`).
03a landed (`67a75b9`), reviewed: `docs/rehearsal-lock.md` §4 (a leading `//` passes the `ray_temp_dir`
check) and §6 item 4 (pid 1 is not kept out of the listing) corrected to what the module does,
each with its caller advice and a probe; nothing under `raypoolkit/` or `pyproject.toml` changed;
the suite 226 → 226. **`v0.3.0` is tagged** (2026-10-24, annotated, on `67a75b9`) after CI
passed at both ends there, and a client's install from the tag is checked (below).** G1 holds at SGK `216e44d`, CPBH
`807f175` and SI `8b4f615` (SI's `HEAD` is now `7071bb8`, its `ray_cluster.sh` still blob
`6c8eada`). The user took D1–D4 (README §6.1) and U1–U6 (README §6.2), all on 2026-10-23 and
U1–U6 as recommended. The package is at `0.3.0`, tagged `v0.3.0` on `67a75b9`; the suite is 226 tests (121 before
01), at 3.12.15 / Ray 2.43.0 and 3.13.16 / Ray 2.55.1. No issue is open: the one the review of 03
found, two edge statements of the contract not true of the module, was closed by 03a (§4).

**Campaign:** [`README.md`](README.md) ·
**Sources:** SecondaryGWKit's `tools/rehearsal_lock.py`, blob `ea14336`; ChamPBH's and
StochasticInstantons' `ray_cluster.sh`, blobs `eaae1e7` and `6c8eada` (G1) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.2

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Made by the user (README §6.1):**

| Decision | Decided |
|---|---|
| **D1** | Extract the shared rehearsal lock into RayPoolKit (2026-10-23) |
| **D2** | The lock moves to `~/.raypoolkit/rehearsal-lock` (2026-10-23) |
| **D3** | The three clients switch together, on one day; no transitional release (2026-10-23) |
| **D4** | Phase 1 only: the lock and the process check, not cluster start and stop (2026-10-23) |

**Put to the user (README §6.2):**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** module | `raypoolkit/rehearsal_lock.py`, run as `python -m raypoolkit.rehearsal_lock`; no console script | **taken** 2026-10-23, for 01 |
| **U2** process rule | the temp-dir rule alone; SGK starts its in-process instances with `_temp_dir` | **taken** 2026-10-23, for 01 |
| **U3** lazy import | no: keep the eager root import (0.3 s gained; U4 of `extraction` broken) | **taken** 2026-10-23, for 01 |
| **U4** old location | `acquire` refuses while `~/ScienceData/.rehearsal-lock` exists, in `0.3.x` | **taken** 2026-10-23, for 01 |
| **U5** override | no environment variable; `lock_dir` keyword for tests and 02 only | **taken** 2026-10-23, for 01 |
| **U6** release | `v0.3.0` | **taken** 2026-10-23, for 03 |

## 1. Prompts

| # | Prompt | Status | Commit | Suite |
|---|---|---|---|---|
| 01 | [`01-the-lock-module.md`](01-the-lock-module.md) | **landed** 2026-10-23 ([log](logs/01-the-lock-module.md)), reviewed | `6733447` | 121 → 226 |
| 02 | [`02-prove-it-under-real-ray.md`](02-prove-it-under-real-ray.md) | **landed** 2026-10-24 ([log](logs/02-prove-it-under-real-ray.md)), reviewed; CI green | `722466a` | 226 → 226 |
| 03 | [`03-release-v0.3.0.md`](03-release-v0.3.0.md) | **landed** 2026-10-24 ([log](logs/03-release-v0.3.0.md)), reviewed; released in `v0.3.0` with 03a | `89d6875` | 226 → 226 |
| 03a | [`03a-correct-two-clauses-of-the-contract.md`](03a-correct-two-clauses-of-the-contract.md) | **landed** 2026-10-24 ([log](logs/03a-correct-two-clauses-of-the-contract.md)); reviewed; CI green; **tagged `v0.3.0`** | `67a75b9` | 226 → 226 |
| 04 | `04-the-switch-over-checklists.md` | not written | — | — |
| 05 | `05-verification-and-close-out.md` | not written | — | — |

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`10be4d5`),
used for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`ae1e064`), used for 02;
[`orchestrator/prompt-03.md`](orchestrator/prompt-03.md) (`8c0dfff`), used for 03. 03a has no note of
its own: the prompt carries the orchestrator's measurements.

**Orchestrator review of prompt 01 (2026-10-23).** Dispatched from `10be4d5` to one Opus
subagent, with the note's §0: eleven clarifications and the measured facts. Reviewed against its
commit `6733447`, with nothing landed after it. **Every check of the note's §3 passed**, and the
prompt's acceptance 1–3 are met. No stop condition fired.

*At dispatch.* The note's gate held at `10be4d5`: the tree clean, this checkout the only worktree,
G1 holding at SGK `216e44d`, `Ran 121 tests … OK`, neither lock location present under the real
`HOME`, no Ray process.

*The checks.*
1. **Scope.** `6733447` touches six files: `raypoolkit/rehearsal_lock.py` and
   `raypoolkit/tests/test_rehearsal_lock.py` (new), `raypoolkit/tests/test_package_imports.py`
   (two tests and the helper `_run_child_args`; the three tests and `_run_child` unchanged), the
   log, this board and `prompts/INDEX.md`. `__init__.py`, `RayWorkPool.py`, `contract.py`,
   `_timing.py`, every other test, `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md` and
   `.github/` are unchanged from `50d91c7`. No tag; `origin/main` still `7ba95fc`.
2. **E2, the module, by reading.** Read whole. It is README §4 and the prompt's §2.2–§2.3 with the
   note's clarifications: the header byte for byte; both locations computed per call from
   `Path.home()`; every argument checked before anything is touched; `acquire`'s old-location check
   before any `mkdir`, then one `os.mkdir`; `set_pid` and `release` refusing as listed, both sides
   of a mismatch printed; argparse with no `--force`, `--wait`, `--retry` or `--lock-dir`. The rule
   strips `/private` only as a leading component, ends a match at `/`, a space, `=` or the end,
   seeds the client server only for `host:port` with `( |$)`, and lets ancestors seed the walk
   without being listed. The provenance note is the only place a client is named, in the module or
   its tests.
3. **E3, the suite, by running.** `venv/` (3.12.15 / 2.43.0): `Ran 226 tests … OK`. The
   orchestrator's own venv (3.13.16 / 2.55.1, editable): `Ran 226 tests … OK`. 121 + 2 + 103. No
   Ray process before or after.
4. **E4, the breakage, by replaying.** M1–M14, extracted from the log's text, each `git apply
   --check`ed and replayed in `bash` on `6733447`: each failed exactly the log's count (6, 6, 3,
   3, 6, 4, 3, 3, 2, 11, 2, 6, 103, 2). The orchestrator's own: (o1) the seeds skipping the safe
   set fails `test_an_ancestor_naming_the_temp_dir_seeds_its_other_children`; (o2) `/private`
   stripped by `removeprefix` fails `test_private_is_stripped_only_as_a_whole_component`; (o3) the
   client-server match without `( |$)` fails the `127.0.0.1:64000` subtest; (o4) the parent's
   `mkdir` before the old-location check fails the three old-location refusals. The tree was clean
   after each.
5. **E5, isolation, by running.** The high-end suite ran with `HOME` an empty scratch directory,
   which stayed empty; so did the breakage replays' `HOME`. The real `~/.raypoolkit` and
   `~/ScienceData/.rehearsal-lock` are absent, before and after. Every test patches `_ps_output` or
   passes `ps_text`.
6. **The command line, by running.** The orchestrator's own transcript, from a script against a
   scratch `HOME`: `acquire` 0, `status` 0, `set-pid` 0, another project's `acquire` 3 and
   `release` 1 (both sides printed), `release` 1 (pid alive), then 0 once the pid was gone;
   `status` 0, `ray-processes` 0; a relative temp dir and `--force` each 2; the old location made by
   hand, `acquire` 3 and `status` reporting it. Then one run against the real `ps`, starting no
   Ray: a shell whose command names a scratch temp dir, and its child, both listed under the `/tmp`
   and the `/private/tmp` spellings, nothing for a longer name, and nothing once both were gone.
7. **The tests, by reading.** Each refusal leaves one reason standing; `status` is pinned line by
   line; the fixtures are neutral and the reconstructed trees say so; every class derives from the
   `HOME`-patching base.
8. **`black`.** `black --check raypoolkit docs`: 19 files unchanged.
9. **E6, the records.** The log has every section of README §5.1 and the prompt's §4.3 additions;
   the index counts 0, matching its header.

*The agent's own choices, accepted.* Deviations 12–21 of the log. Three were looked at closely:
- **The `setUp` guard (18)** stops every test of the module unless both locations are under the
  patched `HOME`, so M13 fails all 103 tests in `setUp` rather than its named test alone. Accepted:
  failing every test is still M13 caught, and the guard is what keeps a location bug from reaching
  a real lock through the suite.
- **M9's named test cannot fail (21).** "Contains" with no leading boundary matches
  `/private/tmp/ray-a` for `/tmp/ray-a` however `/private` is handled; the reverse direction
  catches M9. Accepted as STRUCTURALLY REQUIRED.
- **`status`'s address (13).** With a temp dir given, the listing uses the address given, never the
  owner's; with none, the owner's pair; an address alone is a usage error. Accepted: it is README
  §4's synopsis, `status [--ray-temp-dir D [--ray-address A]]`.

*Observed, not opened.* `acquire` creates the lock's parent outside its `try`, so if
`~/.raypoolkit` is a plain file the command ends in a traceback (exit 1) with nothing created.
That is the safe side, and it can only happen to a file made by hand. 03's contract document may
say so. The log's §5 lists the rest.

*CI on 01's commit (2026-10-23).* The user pushed `6733447` alone, then `2e561e2`. The `tests`
workflow passed on both, at both ends: run 40031056598 on `6733447` (`suite (low)` and `suite
(high)` green, 34 s), and run 40031383762 on `2e561e2` (24 s). It is the first CI run over
`raypoolkit/rehearsal_lock.py` and its tests, and over the guard's two new tests on Ubuntu.

*Residue fixed in the review's own commit:* "this commit" → `6733447` on this board, in the log
and in `prompts/INDEX.md`; README's header and §2 status for 01; this notes line.

**Orchestrator review of prompt 02 (2026-10-24).** Dispatched from `ae1e064` to one Opus
subagent, with the note's §0: thirteen clarifications and the measured facts. Reviewed against its
commit `722466a`, with nothing landed after it. **Every check of the note's §3 passed**, and the
prompt's acceptance 1–4 are met. No stop condition fired.

*Before dispatch, a decision for the user.* The prompt's §2.1 could not pass as written: `venv/`
carries the minimal `ray`, with no `grpc`, and Ray 2.43.0 and 2.55.1 both refuse a client-server
port without it (`RayParams` raises `ValueError`), so part (b)'s `ray start` would have failed at
both ends. The clients pin the `ray[default]` set. **The user chose on 2026-10-24** to run the
proof in two `ray[default]` scratch venvs, 3.12.15 / 2.43.0 and 3.13.16 / 2.55.1, with `venv/`
keeping the suite and `black` (the note's clarification 1; the log's deviation 1, STRUCTURALLY
REQUIRED).

*At dispatch.* The note's gate held at `ae1e064`: the tree clean, this checkout the only worktree,
`Ran 226 tests … OK`, `black` 19 files, no Ray process, ports 6420, 6421, 8270 and 52370 free,
neither lock location under the real `HOME`, no `RAY_*` variable.

*The checks.*
1. **Scope.** `722466a` touches four files: `docs/rehearsal-lock/ray_proof.py` (new), the log,
   this board and `prompts/INDEX.md`. `raypoolkit/`, `pyproject.toml`, `README.md`,
   `PROVENANCE.md`, `CLAUDE.md`, `.github/` and the campaign README are unchanged from `3f1620e`.
   No tag; `origin/main` still `2e561e2`.
2. **The machine after the agent.** No Ray process; the four ports free; neither lock location;
   `/tmp/ray-rpk02a` and `…b` hold Ray's session directories, `…c` was never made.
3. **The script, by reading.** Read whole against the prompt's §2.2–§2.3 and the note's
   clarifications. `RAY_USAGE_STATS_ENABLED=0` is set and the `RAY_*` refusal list taken before
   `raypoolkit` is imported. Every lock call is a fresh `-I` interpreter from an empty directory,
   `lock_dir=old_lock_dir()` but for (c)'s default-location acquire. Neither the script's argv nor
   the driver's names a temp dir. The witness uses the venv's `ray` directory,
   `ray.util.client.server` and `ray::` alone, less the script and its children. There is one
   `os.kill` in the file, reached only through `signal_if_same`, which guards pid ≤ 1, the script
   and its ancestors and then compares the command with the one recorded. No `ray stop`, `killpg`
   or `pkill`. Any exception, and SIGTERM or SIGHUP, goes to the cleanup, which on a failure before
   b3 signals only what both the listing and the witness name. It names no client.
4. **The proof, by running.** In the orchestrator's own `ray[default]` venvs (editable installs of
   this checkout), from a command naming no temp dir, in the background: **exit 0 at both ends, 31
   checks of 31**, 60.2 s at 3.12.15 / 2.43.0 and 65.7 s at 3.13.16 / 2.55.1. Every role matched
   the log: the reaper in the witness and in neither listing at a1, and gone after
   `ray.shutdown()`; the client server listed with the address only, naming no temp dir; a stop
   list of 8 processes at the low end and 18 at the high end (four dashboard children gone by
   their turn and sent nothing); `gcs_server` and `monitor.py` outliving SIGTERM and killed after
   the grace, at both ends. Before and after each run: no Ray process, the lock free,
   `~/.raypoolkit` absent, the four ports (and 8265) free.
5. **The breakage, by replaying.** The agent's extracted M8–M12 (SHA-256 as its log's §4), each
   applied, replayed and reverted, over the orchestrator's records and the agent's, with `HOME` an
   empty scratch directory that stayed empty. Unmutated, all four replays exit 0. **M10** fails a1
   and b2 at 2.43.0, and a1, b1, b2 and b3 at 2.55.1; **M12** fails b1, b2 and b3 at both ends; M8,
   M9 and M11 pass, for the reasons the log gives. The module and `git status` were restored after
   each.
6. **The witness, from the record** (the orchestrator's, 2.55.1). At a1 every one of the 11
   witness processes names the venv's `ray` directory or is a `ray::` process; at b1, 8 of 18 do
   and the other 10 (the dashboard's children) are descendants of one; none is unexplained. The
   listings equal the witness, less the reaper at a1.
7. **The suite and `black`.** `venv/`: `Ran 226 tests … OK`. `black --check raypoolkit docs`: 20
   files unchanged.
8. **The fixtures against the real lines** (the log's §3.9). Every role a test of 01 relies on
   holds in the real trees. `TREE_243` labels two seed scripts wrongly (`default_worker.py` for
   `dashboard.py`, and the order of `log_monitor.py`), and `TREE_255`'s `dashboard.py --minimal`
   is not what `ray[default]` runs; neither changes what a test proves, so nothing is opened.
9. **The records.** The log has every section of README §5.1 and the prompt's §4.4 additions:
   both runs' whole output, their durations and readings, both venvs' freezes, §3.6's replay,
   §3.9's comparison, the breakage record. The index counts 0, matching its header.

*The agent's own choices, accepted.* Deviations 14–24 of the log. Two were looked at closely:
- **`self_pid=-1` for the offline listing (14).** On macOS `launchd` is pid 1 with ppid 0
  (measured by the orchestrator too), so `self_pid=0`'s "own descendants" are the whole table and
  every offline listing would be empty: a1 could never pass. `-1` is in no row. Accepted as
  STRUCTURALLY REQUIRED; the prompt's text was wrong, the module is right.
- **The settling rule (15).** A checkpoint passes only when two consecutive readings agree and
  the expectation holds on them, which is never weaker than the prompt's and gives a2 its bound.

*Observed, not opened.* The replay can catch a mutation that under-lists, never one that
over-lists: the record keeps only the rows of processes in the witness or a listing (the prompt's
§2.2), so a process a mutation would wrongly add is never in it. That is why M8 cannot bite, and
01's fixed-table tests stay the guard for over-listing. `KeyboardInterrupt` is not among the
exceptions the parts catch, so a Ctrl-C at a terminal would end the script without its cleanup;
it is run in the background, where nothing sends one. The log's §5 lists the rest: the
in-process dashboard on port 8265 under `ray[default]` (for 04's SGK checklist), `self_pid` as a
test seam (for 03's contract document), and `ray[default]` venvs for 05.

*Residue fixed in the review's own commit:* "this commit" → `722466a` on this board, in the log
and in `prompts/INDEX.md`; README's header and §2 status for 02; this notes line.

*CI on 02's work (2026-10-24).* The user pushed `main` from `2e561e2` to `cc5f2d6`, carrying
`3f1620e`, `ae1e064`, `722466a` and `cc5f2d6` in one push, so the `tests` workflow ran once, on
`cc5f2d6`: run 40086680695 passed both jobs (`suite (high)` 24 s, `suite (low)` 26 s). `722466a`
has no run of its own; the run on `cc5f2d6` covers its tree, since `cc5f2d6` touches only
`prompts/`. It is the first CI run of `black --check` over `docs/rehearsal-lock/ray_proof.py`. The
proof itself does not run in CI.

**Orchestrator review of prompt 03 (2026-10-24).** Dispatched from `8c0dfff` to one Opus
subagent, with the note's §0: twelve clarifications and the measured facts. Reviewed against its
commit `89d6875`, with nothing landed after it. **Every check of the note's §3 passed but one
part of check 6**: two statements of the contract are not true of the module at an edge, and are
opened as `[03-the-contract-overstates-two-edges-of-the-module]` (§3). No stop condition fired.

*Before dispatch.* Read against the module, the prompt's account of the lock was short of it in
six places (the note's clarifications 1–6). The Python API's fifth command function is
`ray_processes_command`, and a bad argument raises `ValueError`, not 2 (clarification 1,
STRUCTURALLY REQUIRED). A Ray driver calling the Python API sees nothing of its own in-process
instance, since every process of it descends from the driver (clarification 2, from 02's records
at both ends and a probe). The others give the exit conditions README §4 leaves out, the match's
missing leading boundary, identity by spelling, and where each line goes.

*At dispatch.* The note's gate held at `8c0dfff`: the tree clean, this checkout the only worktree,
`Ran 226 tests … OK`, `black` 20 files, no Ray process, neither lock location under the real
`HOME`, no `RAY_*` variable.

*The checks.*
1. **Scope.** `89d6875` touches eight files: `pyproject.toml`, `docs/rehearsal-lock.md` (new),
   `README.md`, `PROVENANCE.md`, `CLAUDE.md`, the log, this board and `prompts/INDEX.md`.
   `raypoolkit/`, `docs/rehearsal-lock/`, `docs/adoption/`, `docs/extraction/`, `.github/`,
   `LICENSE`, `.gitignore` and the campaign README are unchanged from `6e0ba38`. No tag;
   `origin/main` still `cc5f2d6`; no `build/` or `dist/`. No Ray process; neither lock location.
2. **`pyproject.toml`.** The version and the description, and nothing else.
3. **The suite.** `venv/`: `Ran 226 tests … OK`, reporting `0.3.0` and `['ray>=2.43']`. The
   orchestrator's own fresh 3.13.16 / 2.55.1 venv (editable): `Ran 226 tests … OK`.
4. **The distribution, re-built** from fresh exports of `89d6875`, without `-q`: (R1') and (R2')
   (the manifest then `Version: 0.3.0`, 10 files under `tests/`) are each 21,368 bytes, 10
   entries, none under `raypoolkit/tests/`, 0 "absent from"; the five modules byte-equal to the
   commit's. (R2') in a fresh 3.13.16 / `ray==2.55.1` venv passed the prompt's §3.3 from an empty
   directory with `-I`: the imports from `site-packages`, `0.3.0` and `['ray>=2.43']`, Ray not
   initialized, `raypoolkit.tests` absent, `--help`, `status` and `ray-processes` (from a script
   file), the scratch `HOME` left empty.
5. **The breakage, by replaying.** (a) and (b) extracted from the log's text (SHA-256 as the log
   gives them) and applied in fresh exports: (a) gives a `0.2.0` wheel; (b) 63,134 bytes, 21
   entries, 11 under `raypoolkit/tests/`, and `raypoolkit.tests.test_rehearsal_lock` imports from
   a throwaway venv's `site-packages`. The orchestrator's (o1), `include-package-data = true` with
   the manifest: 51,047 bytes, 20 entries, 10 under `raypoolkit/tests/`, 2 "absent from", so the
   setting still guards a stale manifest. `git status` clean throughout.
6. **The contract, read against the module.** Read whole with `rehearsal_lock.py` beside it. Its
   eleven sections are §2.2's, in order, and carry clarifications 1–6: the API, every exit
   condition, the rule exactly (no leading boundary; the client server's two parts), identity by
   spelling, the driver paragraph, every `status` line and its condition, the streams. The log's
   eleven probe-only statements (S4, S5, S8, S16, S18, S30, S40, S46, S66, S74, S90) agree with
   the orchestrator's own probes of the note's §0. **Two statements are not true at an edge**,
   each found by a probe against a fixed table and a scratch `HOME`:
   - §4 says a `ray_temp_dir` in normal form has no `//`. POSIX's `os.path.normpath` keeps a
     leading `//`, so `//tmp/ray-a` passes the check (`/tmp//ray-a` and `///tmp/ray-a` do not).
   - §6 item 4 says this process's ancestors are never listed. The ancestor walk stops before pid
     1 (`rehearsal_lock.py:376`), so pid 1 is listed when its command names the temp dir: with
     `1 0 /init --temp-dir=/tmp/ray-a` an ancestor of the reading process, `ray_processes` returns
     `[1]`. 01's log §5 records the module's behaviour; the contract does not.
   Each over-states what the module promises in a case no project meets today, and each is a
   one-clause correction of the document; nothing under `raypoolkit/` need change.
7. **No client.** The grep finds nothing in `docs/rehearsal-lock.md` or in the README's added lines.
8. **The README.** Status describes `v0.3.0` and keeps `v0.2.0`, `v0.1.0` and DatastoreKit;
   "Changes in `v0.3.0`" precedes "Changes in `v0.2.0`" and says nothing of when a project moves
   its pin; the pin is `@v0.3.0`; "The rehearsal lock" sits between "Using it" and "Developing",
   its table matching the module and not copying the contract; Licence says five. Every relative
   link in the four documents resolves to a file tracked at `89d6875`.
9. **`PROVENANCE.md` and `CLAUDE.md`.** As §2.4 and §2.5, every blob and commit as the note's facts
   have them; the exceptions of "What this repository is" unchanged (clarification 10).
10. **`black`.** 20 files unchanged.
11. **The records.** The log has every section of README §5.1 and the prompt's §4.5 additions,
    with clarification 1 recorded as STRUCTURALLY REQUIRED and no UNINTENDED DRIFT.

*The agent's own choices, accepted.* Deviations 13–20 of the log. Two were looked at closely:
- **The import cost (13)**, "0.3–0.6 s at Ray 2.43.0" in place of "about 0.3 s": measured on the
  day, and 01's log §5 had 0.62 s. Accepted.
- **The added behaviours (16)**, among them the order of `release`'s checks and a failed `rmdir`
  leaving a lock with no owner file: each was read against the module and is right.

*Observed, not opened.* `CLAUDE.md`'s first exception reads "imported from", and the lock module was
modelled on its sources, not imported; the exceptions are the user's, and the wording is put to
them. `docs/rehearsal-lock/ray_proof.py` takes the lock at `old_lock_dir()`, so a re-run after the
switch-over holds a lock no project looks at (for 04 and 05). The log's §5 lists the rest.

*Residue fixed in the review's own commit:* "this commit" → `89d6875` on this board, in the log
and in `prompts/INDEX.md`; README's header and §2 status for 03; this notes line.

**Orchestrator review of prompt 03a (2026-10-24).** The user chose a fix prompt over an
orchestrator edit. Written (`b2ee2b3`) with the orchestrator's measurements in the prompt itself,
and dispatched from it to one Opus subagent; reviewed against its commit `67a75b9`, with nothing
landed after it. **Every check passed**, and the prompt's acceptance 1–3 are met. No stop
condition fired.

*The checks.*
1. **Scope.** `67a75b9` touches five files: `docs/rehearsal-lock.md`, the log, this board,
   `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`. `raypoolkit/`, `pyproject.toml`, `README.md`,
   `PROVENANCE.md`, `CLAUDE.md`, `.github/`, 03's log, the prompt and the campaign README are
   unchanged from `b2ee2b3`, and `git diff 89d6875 67a75b9 -- raypoolkit pyproject.toml` is empty,
   so the wheel is 03's. No tag; `origin/main` still `cc5f2d6`.
2. **The document, read against the module.** §4's `ray_temp_dir` rule now admits a leading `//`
   and names the four measured spellings; §6 item 4 now exempts the reader's ancestors other than
   pid 1, and says that pid 1 naming `D` lists every descendant of pid 1 outside that set; "What
   it asks of a caller" gains "never start the temp dir with `//`" and "never use a temp dir that
   pid 1's command names". Each is true of `rehearsal_lock.py:126-135`, `:307-312` and
   `:374-379`. The opening links 03a's log too. Nothing else changed.
3. **The probes, re-run.** The agent's P-a, P-b and its own P-c, run again by the orchestrator
   with `venv/`'s interpreter, `-I`, from a directory outside the repository: each exits 0 with
   output byte-equal to the agent's, and each matches the prompt's measurements and the
   orchestrator's own of 2026-10-24.
4. **The suite and `black`.** `venv/`: `Ran 226 tests … OK`; `black --check raypoolkit docs`: 20
   files unchanged. No Ray process; neither lock location under the real `HOME`.
5. **Links and names.** The document's six relative links resolve to tracked files; the client
   grep finds nothing.
6. **The records.** The log has every section of README §5.1; the issue is in §4 with its
   **Resolved (03a)** line; the index counts 0, matching its header.

*The agent's own choices, accepted.* Deviations 1–8 of the log. **Deviation 1** (STRUCTURALLY
REQUIRED) replaces the prompt's "every process outside that set" with "every descendant of pid 1
outside that set, which is almost every process": on Linux, `kthreadd` (pid 2) has ppid 0, so the
kernel threads are not pid 1's descendants (its P-c). The prompt's text was wrong; the agent's is
the module's.

*Observed, not opened.* The module's docstrings (`rehearsal_lock.py:63-64`, `:345-347`) and
`PROVENANCE.md:102` still say ancestors are never listed, without the pid 1 exception; the
docstrings are under `raypoolkit/` and change only in a later release. A temp dir of
`//private/tmp/…` is matched only as spelled, not in its `/tmp/…` spelling (P-c); §4's "the process
rule then matches the leading `//` as spelled" and the new `//` advice cover it. No test pins
either corrected edge; both rest on the probes. The log's §5 lists the rest.

*Residue fixed in the review's own commit:* "this commit" → `67a75b9` on this board, in the log
and in `prompts/INDEX.md`; README's header and §2 status for 03 and 03a.

**Release of `v0.3.0` (2026-10-24).** Put to the user after the review of 03a, and done on the
user's instruction, in the order the review recommended, so that CI ran on the tagged commit
itself:
1. **Push.** `git push origin 67a75b9:main` moved `origin/main` from `cc5f2d6` to `67a75b9`,
   carrying `6e0ba38`, `8c0dfff`, `89d6875`, `b4edd2c`, `b2ee2b3` and `67a75b9` in one push.
2. **CI on `67a75b9`.** The `tests` workflow's run 40121254667 passed both jobs: `suite (low)`,
   Python 3.12.15 / Ray 2.43.0 (25 s), and `suite (high)`, Python 3.13.16 / Ray 2.55.1 (39 s). It
   is the first CI run over `pyproject.toml` at `0.3.0`, `docs/rehearsal-lock.md` and 03's
   documents. `89d6875` has no run of its own; `67a75b9`'s tree differs from it only in `docs/` and
   `prompts/`.
3. **The review's follow-up.** `git push origin c1164a5:main`, once run 40121254667 had passed:
   run 40121340908 on `c1164a5` passed both jobs (`suite (low)` 19 s, `suite (high)` 23 s).
4. **The tag.** `v0.3.0`, annotated (tag object `caf0076`, message "raypoolkit 0.3.0", as
   `v0.2.0`'s), on `67a75b9`, made and pushed on the user's instruction. `git ls-remote origin`
   shows it, peeling to `67a75b9`.
5. **A client's install, checked.** `uv pip install --no-cache "raypoolkit @
   git+https://github.com/ds283/RayPoolKit@v0.3.0" "ray==2.55.1"` into a fresh 3.13.16 venv in
   the scratchpad:
   - `direct_url.json` records `requested_revision` `v0.3.0` and `commit_id` `67a75b9…`;
   - the installed package is the five modules, each byte-equal to the tag's, with no `tests/`;
   - from an empty directory with `-I`, `version` is `0.3.0`, `requires` is `['ray>=2.43']`, the
     two public names import from `site-packages`, `ray.is_initialized()` is false, and `import
     raypoolkit.tests` raises `ModuleNotFoundError`;
   - `python -I -m raypoolkit.rehearsal_lock status`, with `HOME` an empty scratch directory,
     prints `lock: free (…)` and `Ray processes: no temp dir given`, exits 0, and leaves `HOME`
     empty.

This record is a commit of its own, made after the tag and not yet pushed when written. 04, the
switch-over checklists, is measured against `v0.3.0` and can now be written.

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1** | **holds** 2026-10-23: SGK `tools/rehearsal_lock.py` is blob `ea14336` and `tools/tests/test_rehearsal_lock.py` blob `cdeecd6` at `216e44d`; CPBH's `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` is blob `eaae1e7` at `807f175`; SI's is blob `6c8eada` at `8b4f615` (the tip of its unmerged branch `dk-and-rpk-migration`) |
| **G2** | not yet (the switch-over: all three on `v0.3.0`, on one day) |

## 3. Active and unresolved issues

None.

## 4. Resolved issues

### `[03-the-contract-overstates-two-edges-of-the-module]`

**Opened:** 2026-10-24, by the orchestrator's review of 03. **Owner:** 03a, before the tag.

**Where:** `docs/rehearsal-lock.md` at `89d6875`, §4 ("The argument rules", the `ray_temp_dir`
bullet) and §6 item 4.

Two statements of the contract say more than the module does:
- §4: "in normal form (`os.path.normpath` leaves it as it is, so no trailing `/`, `.`, `..` or
  `//`)". POSIX's `normpath` keeps a leading `//`, so `//tmp/ray-a` passes
  `_check_ray_temp_dir` (`raypoolkit/rehearsal_lock.py:126-135`).
- §6 item 4: "This process is never listed: the process reading the table, its ancestors, and its
  own descendants." The ancestor walk stops before pid 1 (`rehearsal_lock.py:376`, `pid > 1`), so
  pid 1 is listed when its command names the temp dir. Probe: a fixed table in which pid 1's
  command is `/init --temp-dir=/tmp/ray-a`, an ancestor of the reading process, gives `[1]`. 01's
  log §5 records this behaviour.

*Impact.* None on any project today: no caller passes a temp dir starting `//`, and pid 1 is
`launchd` on macOS. But the document is the contract three projects keep, and the tag `v0.3.0`
cannot be moved once made, so a statement untrue of the module is not released in it.

**Assigned (2026-10-24):** to prompt 03a, [`03a-correct-two-clauses-of-the-contract.md`](03a-correct-two-clauses-of-the-contract.md),
at the user's choice of a fix prompt; `v0.3.0` is then tagged on 03a's commit.

*Next step.* Correct the two clauses in `docs/rehearsal-lock.md`, saying what the module does (a
leading `//` is kept; pid 1 is not exempt), each with its probe recorded, and change nothing under
`raypoolkit/`. Then CI on that commit, then the tag.

**Resolved (03a, 2026-10-24):** in `67a75b9`. `docs/rehearsal-lock.md` §4 now says that normal
form is what `os.path.normpath` leaves unchanged, with no doubled `/` except a leading `//`, which
POSIX keeps and the check accepts (`//tmp/ray-a` passes; `/tmp//ray-a`, `///tmp/ray-a` and
`/tmp/ray-a/` do not). §6 item 4 now says that never listed are the reader, its ancestors other
than pid 1, and its own descendants; pid 1 is listed if its command names `D`, and then so is every
descendant of pid 1 outside that set, which over-lists (`acquire` 4, `release` 1). "What it asks of
a caller" gains: never start the temp dir with `//`, and never use one that pid 1's command names.
Probes against fixed tables, in [the log](logs/03a-correct-two-clauses-of-the-contract.md) §3.3:
**P-a**, the four spellings (one accepted, three refused) and, over one table, `[41]` for
`//tmp/ray-a` against `[40, 41]` for `/tmp/ray-a`; **P-b**, `[1, 30, 31]` with pid 1 naming `D`
(the old clause predicted `[30, 31]`) and `[]` with pid 1 naming another directory. Nothing under
`raypoolkit/` changed; the module's docstrings and `PROVENANCE.md:102`, which make the same pid 1
claim, are recorded in the log's §5.
