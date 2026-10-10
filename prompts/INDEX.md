# Campaign index

One line per campaign under `prompts/`. It is an index: the campaign's `README.md` holds the plan
and its `IMPLEMENTATION_STATE.md` the status; if this file and a board disagree, the board is
right.

**Last updated:** 2026-10-10 · 1 campaign: 1 in progress.

| Campaign | Status | Opened → last board update | Owns | Open issues |
|---|---|---|---|---|
| [`extraction`](extraction/IMPLEMENTATION_STATE.md) | **in progress**: 3 of 7 written (01–03), 01 landed (`49f3ddf`: the package imported, suite 3) and reviewed, 02 landed (`b9f6dec`: the test suite with no Ray cluster, suite 116, faults 1–5 pinned) and reviewed, 03 landed (`4e90a8a`: `0.1.0`, Python `>=3.12`, `ray>=2.43`, CI workflow, README; suite 116 at both ends; `v0.1.0` ready to tag once CI passes, no tag made) and reviewed; G1 holds (import commit SGK `b510bc9`, blob `b4666fa`); U1–U7 and U9 taken 2026-10-10; U5 freeze in force | 2026-10-10 → 2026-10-10 | moving SGK's `RayWorkPool` into `raypoolkit`; a test suite with no Ray cluster; fixing the inherited faults; releases `v0.1.0` and `v0.2.0`; the clients' adoption checklists | §1.1; 8 |
