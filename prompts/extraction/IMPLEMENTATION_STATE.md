# extraction campaign — implementation state

**Last updated:** 2026-10-10 · **Status: PLANNED — 0 of 7 prompts written.** G1 holds at SGK
`b510bc9`. The user took U1–U3 at set-up on 2026-10-10 (README §6.2).

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
| **U4** module name | keep `RayWorkPool.py`; re-export the class from the root | open, for 01 |
| **U5** freeze | no client edits its `RayTools/` until it adopts | open, for 01 |
| **U6** Ray stand-in | real `ObjectRef(bytes)`; `ray.wait` / `ray.get` replaced in-process | open, for 02 |
| **U7** versions | Python ≥3.12, Ray ≥2.43; tested 3.12.15/2.43.0 and 3.13.16/2.55.1 | open, for 03 |
| **U8** handler checks | defaults apply only with a compute handler (option b) | open, for 04 |
| **U9** printed lines | pinned, wording and layout, against a frozen clock | open, for 02 |
| **U10** CPBH shim | none | open, for 06 |

## 1. Prompts

| # | Prompt | Status | Commit | Suite |
|---|---|---|---|---|
| 01 | `01-import-the-pool.md` | not written | — | — |
| 02 | `02-the-test-suite.md` | not written | — | — |
| 03 | `03-supported-versions-and-ci.md` | not written | — | — |
| 04 | `04-fix-the-inherited-faults.md` | not written | — | — |
| 05 | `05-release-v0.2.0.md` | not written | — | — |
| 06 | `06-the-adoption-checklists.md` | not written | — | — |
| 07 | `07-verification-and-close-out.md` | not written | — | — |

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1** | **holds** 2026-10-10: SGK `RayTools/RayWorkPool.py` is blob `b4666fa` at `b510bc9` |
| **G2** | not yet (SGK adopts `v0.2.0`) |
| **G3** | not yet (CPBH adopts `v0.2.0`) |
| **G4** | not yet (SI adopts `v0.2.0`) |

## 3. Active and unresolved issues

All five are inherited from the source and were opened at planning (README §0.2, faults 1–5).
Each is pinned as it behaves by 02 and fixed by 04 (README §2).

### `[00-in-flight-work-is-keyed-on-a-bound-method]`

**Opened:** 2026-10-10, at planning. **Owner:** 04.

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

### `[00-a-post-handler-after-persist-gets-the-unpersisted-object]`

**Opened:** 2026-10-10, at planning. **Owner:** 04.

In the `"store"` branch with no validation handler (SGK `RayWorkPool.py:488-491`), the post
handler is called with `obj`, the driver's copy from before the persist, not with
`replacement_obj`, the object the datastore returned with its `store_id` set. Every other exit
passes the current object.

*Impact.* Reachable at one client site, SGK `main.py:3247` (`postprocess_GkSourcePolicy`). That
handler reads only `policy`, `type` and `quality`, which `store()` sets locally, so it is correct
today. A post handler there that read `store_id` would see `None`.

*Next step.* 04 passes `replacement_obj`, with a test that a post handler after a persist sees the
replacement. 06's checklists re-measure the sites.

### `[00-store-results-sizes-from-len-of-the-task-list]`

**Opened:** 2026-10-10, at planning. **Owner:** 04.

With `store_results=True` the constructor sizes `results` from `len(task_list)` (SGK `:138`),
though it has already consumed `task_list` into `self._todo` and counted it. A generator or other
iterable without `len()` raises `TypeError`.

*Impact.* None known at a client: no client run is known to have raised it, but the planner did
not trace every `task_list` argument to its type (06 does). The constructor otherwise accepts any
iterable.

*Next step.* 04 sizes from `self._num_total_items`, with a test that passes a generator.

### `[00-the-constructor-checks-its-handlers-unevenly]`

**Opened:** 2026-10-10, at planning. **Owner:** 04, under U8.

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

### `[00-messages-say-maker-and-the-module-has-no-licence-header]`

**Opened:** 2026-10-10, at planning. **Owner:** 04.

The constructor's two messages say "compute maker" and "persist maker" for the handlers, and SGK's
module carries no licence header (CPBH's and SI's copies carry the Apache 2.0 header, and SI's
messages say "handler").

*Impact.* Cosmetic. The messages are not part of the printed-lines interface (`CLAUDE.md`); they
are exception text.

*Next step.* 04 rewrites the two messages and adds the header the repository's licence calls for.

## 4. Resolved issues

None.
