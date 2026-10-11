# Campaign index

One line per campaign under `prompts/`. It is an index: the campaign's `README.md` holds the plan
and its `IMPLEMENTATION_STATE.md` the status; if this file and a board disagree, the board is
right.

**Last updated:** 2026-10-12 · 1 campaign: 1 closed.

| Campaign | Status | Opened → last board update | Owns | Open issues |
|---|---|---|---|---|
| [`extraction`](extraction/IMPLEMENTATION_STATE.md) | **closed** 2026-10-10 by 07: 7 of 7 landed, 01 landed (`49f3ddf`: the package imported, suite 3) and reviewed, 02 landed (`b9f6dec`: the test suite with no Ray cluster, suite 116, faults 1–5 pinned) and reviewed, 03 landed (`4e90a8a`: `0.1.0`, Python `>=3.12`, `ray>=2.43`, CI workflow, README; suite 116 at both ends; CI green at both ends) and reviewed, tagged **`v0.1.0`**; 04 landed (`0b6ffd2`: faults 1–5 fixed and guarded, U8 and U11 applied, the sizes checked, the equivalence check retired at `v0.1.0`; suite 116 → 121 at both ends; seven issues closed) and reviewed, CI green at both ends; 05 landed (`eaef0ce`: `0.2.0`, `include-package-data = false`, README and `PROVENANCE.md` for `v0.2.0`; suite 121 → 121 at both ends; the release check passes with and without a stale manifest; one issue closed) and reviewed, CI green at both ends, tagged **`v0.2.0`**; 06 landed (`67f3f7e`: `docs/adoption/`, three checklists and `measure_client_pools.py`, against `v0.2.0`; all 87 client call sites construct; suite 121 → 121; no issue opened) and reviewed; 07 landed (`1ae1a49`: `docs/extraction-verification.md`; `docs/extraction/ray_smoke_run.py` passes under a local Ray at both ends; the `v0.2.0` wheel rebuilt offline; no issue opened; suite 121 → 121) and reviewed, and the campaign closed with G2–G4 open; G2 holds since 2026-10-12 (SGK adopted `v0.2.0`, `RayTools/` deleted at SGK `643c3b2`), G3–G4 open; G1 holds (import commit SGK `b510bc9`, blob `b4666fa`); U1–U14 taken 2026-10-10 (U5 amended by U12); U5 freeze in force | 2026-10-10 → 2026-10-12 | moving SGK's `RayWorkPool` into `raypoolkit`; a test suite with no Ray cluster; fixing the inherited faults; releases `v0.1.0` and `v0.2.0`; the clients' adoption checklists | §1.1; 0 |
