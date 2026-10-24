# rehearsal-lock campaign — implementation state

**Last updated:** 2026-10-24 · **Status: ACTIVE — 2 of 5 prompts written (01, 02); 01 landed
(`6733447`), reviewed, and CI green at both ends: `raypoolkit/rehearsal_lock.py`, the lock at
`~/.raypoolkit/rehearsal-lock` with the old-location refusal, the owner file, the five commands
and the process rule by temp dir, standard library only; its 103 tests and two guard tests. 02
landed (this commit): `docs/rehearsal-lock/ray_proof.py`, run under real Ray holding the real
shared lock, exits 0 at 3.12.15 / Ray 2.43.0 and 3.13.16 / Ray 2.55.1 (`ray[default]` scratch
venvs, the user's choice of 2026-10-24), 31 checks each; its offline replay fails under M10 and
M12 at both ends; nothing under `raypoolkit/` changed.** G1 holds at SGK `216e44d`, CPBH `807f175` and
SI `8b4f615`. The user took D1–D4 (README §6.1) and U1–U6 (README §6.2), all on 2026-10-23 and
U1–U6 as recommended. The package is at `0.2.0`; the suite is 226 tests (121 before 01), at
3.12.15 / Ray 2.43.0 and 3.13.16 / Ray 2.55.1. No issue is open.

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
| 02 | [`02-prove-it-under-real-ray.md`](02-prove-it-under-real-ray.md) | **landed** 2026-10-24 ([log](logs/02-prove-it-under-real-ray.md)) | this commit | 226 → 226 |
| 03 | `03-release-v0.3.0.md` | not written | — | — |
| 04 | `04-the-switch-over-checklists.md` | not written | — | — |
| 05 | `05-verification-and-close-out.md` | not written | — | — |

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`10be4d5`),
used for 01.

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

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1** | **holds** 2026-10-23: SGK `tools/rehearsal_lock.py` is blob `ea14336` and `tools/tests/test_rehearsal_lock.py` blob `cdeecd6` at `216e44d`; CPBH's `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` is blob `eaae1e7` at `807f175`; SI's is blob `6c8eada` at `8b4f615` (the tip of its unmerged branch `dk-and-rpk-migration`) |
| **G2** | not yet (the switch-over: all three on `v0.3.0`, on one day) |

## 3. Active and unresolved issues

None.

## 4. Resolved issues

None.
