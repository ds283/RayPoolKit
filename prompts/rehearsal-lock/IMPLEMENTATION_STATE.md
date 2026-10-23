# rehearsal-lock campaign — implementation state

**Last updated:** 2026-10-23 · **Status: PLANNED — 0 of 5 prompts written.** G1 holds at SGK
`216e44d`, CPBH `807f175` and SI `8b4f615`. The user took D1–D4 on 2026-10-23 (README §6.1);
U1–U6 are put (README §6.2), U1–U5 needed before 01 is written. The package is at `0.2.0`; the
suite is 121 tests.

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
| **U1** module | `raypoolkit/rehearsal_lock.py`, run as `python -m raypoolkit.rehearsal_lock`; no console script | open, for 01 |
| **U2** process rule | the temp-dir rule alone; SGK starts its in-process instances with `_temp_dir` | open, for 01 |
| **U3** lazy import | no: keep the eager root import (0.3 s gained; U4 of `extraction` broken) | open, for 01 |
| **U4** old location | `acquire` refuses while `~/ScienceData/.rehearsal-lock` exists, in `0.3.x` | open, for 01 |
| **U5** override | no environment variable; `lock_dir` keyword for tests and 02 only | open, for 01 |
| **U6** release | `v0.3.0` | open, for 03 |

## 1. Prompts

| # | Prompt | Status | Commit | Suite |
|---|---|---|---|---|
| 01 | `01-the-lock-module.md` | not written | — | — |
| 02 | `02-prove-it-under-real-ray.md` | not written | — | — |
| 03 | `03-release-v0.3.0.md` | not written | — | — |
| 04 | `04-the-switch-over-checklists.md` | not written | — | — |
| 05 | `05-verification-and-close-out.md` | not written | — | — |

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1** | **holds** 2026-10-23: SGK `tools/rehearsal_lock.py` is blob `ea14336` and `tools/tests/test_rehearsal_lock.py` blob `cdeecd6` at `216e44d`; CPBH's `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` is blob `eaae1e7` at `807f175`; SI's is blob `6c8eada` at `8b4f615` (the tip of its unmerged branch `dk-and-rpk-migration`) |
| **G2** | not yet (the switch-over: all three on `v0.3.0`, on one day) |

## 3. Active and unresolved issues

None.

## 4. Resolved issues

None.
