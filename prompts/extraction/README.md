# Campaign — extraction

**Written:** 2026-10-10 by Claude Opus 5.5, at the user's request, from a read-only comparison of
the three client projects' `RayWorkPool` copies made the same day (§0.2). The user took U1–U3 at
set-up (§6.2), and U4 and U5 on 2026-10-10, each as recommended; **prompt 01 is written**
(2026-10-10), with G1 re-checked. Each prompt is written after the one before it has landed and
been reviewed, against the tree it left.

## 0. Why this campaign exists

Three projects run the same `RayWorkPool` work queue, each from its own copy of
`RayTools/RayWorkPool.py`:

- **SecondaryGWKit (SGK)** carries the developed copy. Since 2026-09-04 it has had:
  - a task builder that may return `None` for "nothing to enqueue" (`e81b145`, backported from
    SI);
  - the correct "available" progress rate (`e81b145`);
  - the compute step split into a local `store_handler` and a `persist_handler` that makes the
    datastore round-trip (`0ee16a8`).
- **StochasticInstantons (SI)** has the split and the `None` return, but still reports the
  "available" rate from the store count. Its messages say "handler" where SGK's say "maker", and
  it carries the Apache licence header that SGK's file lacks.
- **ChamPBH (CPBH)** has the `None` return only. Its `store_handler` is what the others call the
  persist handler: it is handed `(obj, pool)` and returns the `ObjectRef` of the datastore write,
  and `obj.store()` is called unconditionally before it.

The same fixes have to be made three times, and have not been: the rate fix reached one copy.
DatastoreKit is moving the datastore layer out of the same three projects (its README §8.1 records
`RayWorkPool` as the later unit of work this campaign is). This campaign does the same for the
pool.

### 0.1 What "extraction" means here

The pool moves into a package, `raypoolkit`, in this repository. Each client then deletes its
`RayTools/` and imports the package at a tagged release, in an adoption campaign of its own. The
package is imported from SGK's copy, unchanged in behaviour (U2), and released as `v0.1.0` once a
test suite pins that behaviour. The faults inherited from the source are then fixed and released
as `v0.2.0`, the release the clients adopt.

### 0.2 Measurements taken by the planner (2026-10-10, read-only)

**The source.** SGK's `RayTools/RayWorkPool.py`, 575 lines, blob `b4666fa`, last changed by
`0ee16a8` (2026-09-04) and unchanged through SGK `b510bc9` (HEAD, tree clean).
`RayTools/__init__.py` is empty in all three.

**The client copies, at the clients' HEADs (all clean):**

| Client | HEAD | Blob | Last change | Lines | Changed lines against SGK (`diff`) |
|---|---|---|---|---|---|
| SGK | `b510bc9` | `b4666fa` | `0ee16a8`, 2026-09-04 | 575 | — |
| SI | `7bb3efd` | `92be5b2` | `7cf4123`, 2026-06-16 | 590 | 39 (15 of them the licence header) |
| CPBH | `52142d7` | `aaa6dc9` | `79fb527`, 2026-01-25 | 580 | 40 (15 of them the licence header) |

What differs, in full:

| | CPBH | SGK | SI |
|---|---|---|---|
| Store / persist split | no | yes | yes |
| `None` from a task builder | yes, tested after the sequence case | yes, tested first | as CPBH |
| `_last_num_available_complete` assigned from | `_num_store_complete` | `_num_available_complete` | `_num_store_complete` |
| Constructor messages say | "maker" | "maker" | "handler" |
| Licence header | yes | no | yes |

The `None` orderings are the same behaviour; only the message under `store_results=True` differs.

**Client dependencies of the source.** Two imports, at `RayWorkPool.py:8-9` in SGK:
- `Datastore.SQL.ShardedPool.ShardedPool`, used **only as the type hint** of the constructor's
  `pool` argument. The pool is otherwise passed through to the store and persist handlers, and the
  default persist handler calls `pool.object_store(obj)`. Nothing else is called on it.
- `utilities.format_time`, used in the progress and completion lines. It and the three
  `SECONDS_PER_*` constants it uses are identical in all three clients' `utilities.py` (by
  AST-segment hash) and in DatastoreKit's `datastorekit/_timing.py`.

**The interface, as the clients use it.** The constructor (`pool`, `task_list`, `task_builder`
and twelve keyword handlers and sizes); `run()`; the public attributes `results` (with
`store_results=True`) and `total_time` (with a `title`); and the lines printed to stdout. Call
sites of `RayWorkPool(...)` outside each client's `RayTools/`, tests, `docs/` and `prompts/`, by
`ast` over `git ls-files` at HEAD:

| Client | Sites | Lookup-only (`compute_handler=None`) | Compute | `store_results=True` |
|---|---|---|---|---|
| SGK | 54 | 44, each passing `store_handler=None` and `persist_handler=None` | 10 | 39 |
| SI | 16 | 12, each passing `store_handler=None` and `persist_handler=None` | 4 | 11 |
| CPBH | 17 | 14, each passing `store_handler=None` (its persist handler) | 3 | 13 |

Two consequences for adoption:
- **CPBH's 14 lookup-only sites** pass no `persist_handler`. Under the package they would get the
  default one, and the constructor raises when a persist handler is set without a compute handler
  (`RayWorkPool.py:99-102`), so each must change. Its 3 compute sites use the default store
  handler, which in the package is the default persist handler, so they keep their behaviour.
- **SGK's tests depend on the pool's surface.** `RunRegistry/tests/test_pipeline_adoption.py`
  pins six lines the pool prints (banner, two progress notifications, completion pair), parsed by
  SGK's `StageTracker`. Three `ComputeTargets/tests/` modules find pool constructions by
  `ast.Call` with `func.id == "RayWorkPool"`, and two more execute pieces of `main.py` with a
  stand-in bound to the name `RayWorkPool`, so the call must stay spelled `RayWorkPool(...)`.

**Inherited faults** (all three copies, unless noted; line numbers are SGK's):
1. **In-flight work is keyed on a bound method.** Every dictionary is keyed on `ref.hex`, the
   method, not `ref.hex()`. Two equal `ObjectRef`s that are distinct objects give unequal keys
   (measured: `ObjectRef(b) == ObjectRef(b)` and their hashes agree, but their `.hex` methods do
   not compare equal, at Ray 2.43.0, 2.53.0 and 2.55.1). The pool works only because `ray.wait`
   returns the very objects it was given.
2. **After a persist with no validation step, the post handler gets the unpersisted object**
   (`:488-491`): it is handed the local copy from before the persist, not the replacement the
   datastore returned, so it sees no `store_id`. Reachable at one site, SGK `main.py:3247`
   (`postprocess_GkSourcePolicy`), harmless there today because that handler reads only fields
   `store()` sets locally.
3. **`results` is sized from `len(task_list)`** (`:138`), not from the list the constructor has
   already built, so a generator `task_list` with `store_results=True` raises `TypeError`.
4. **The constructor checks its handlers unevenly.** It *raises* `RuntimeWarning` (an exception)
   when a persist handler is set without a compute handler (`:99-102`), which is why every
   lookup-only site must pass `persist_handler=None` explicitly; and it does not check that a
   compute handler comes with a store handler, so `store_handler=None` with a compute handler
   fails with `TypeError` at the first completed compute.
5. **Cosmetic:** the constructor's messages say "maker" for "handler", and the module has no
   licence header.
6. *(CPBH and SI only)* The "available" rate is computed from the store count. Fixed in the
   source; it reaches CPBH and SI on adoption.

**No copy has a unit test of the pool.** Every behaviour the package keeps has to be pinned by a
new suite (02).

**Ray without a cluster.** `ray.ObjectRef(bytes(28))` constructs with `ray.is_initialized()` false
at Ray 2.43.0, 2.53.0 and 2.55.1, and such refs hash and compare by their bytes. So the suite can
drive the pool with real refs and an in-process stand-in for `ray.wait` and `ray.get` (U6).

**Runtime versions** of the clients' `venv`s:

| Client | Python | Ray |
|---|---|---|
| SGK | 3.12.15 | 2.43.0 |
| CPBH | 3.13.16 | 2.53.0 |
| SI | 3.13.16 | 2.55.1 |

## 1. Scope

**In scope:**
- the package `raypoolkit`: SGK's `RayWorkPool.py`, with its two client imports replaced (§4);
- `pyproject.toml`; the internalised `format_time`; `PROVENANCE.md`;
- a test suite that pins the pool's behaviour with no Ray cluster, and a guard test;
- the supported-version statement and CI; the releases `v0.1.0` (03) and `v0.2.0` (05);
- the fixes of the inherited faults 1–5 (04);
- the per-client adoption checklists, measured against `v0.2.0` (06).

**Out of scope:**
- **any edit to SGK, CPBH or SI.** Each adopts in its own campaign (§7);
- **any change to the pool's behaviour or output before 04** (§5 rule 8). A fault found by an
  earlier prompt is recorded, not fixed;
- **compatibility shims for a client.** CPBH's `store_handler` meaning "persist" is not kept under
  any name; CPBH rewrites its call sites when it adopts (U10);
- **the clients' task builders and handlers**, which are where the shard-key payloads are built.
  They call DatastoreKit's API, not the pool's, and adopt with DatastoreKit;
- **DatastoreKit.** No prompt here edits it. Its README's note that `RayWorkPool` is not part of
  that package is DatastoreKit's to update;
- **new features**: cancellation, retries, signal handling, structured progress reporting. They are
  for later campaigns, once the clients share one copy.

## 2. Prompts

| # | Prompt | Covers | Status |
|---|---|---|---|
| 01 | [`01-import-the-pool.md`](01-import-the-pool.md) | The package skeleton (`pyproject.toml`, `raypoolkit/`), SGK's `RayWorkPool.py` (blob `b4666fa`) under §4's names. The `ShardedPool` import is replaced by a `typing.Protocol` the hint names (U3); `format_time` and the `SECONDS_PER_*` constants are internalised byte for byte in `raypoolkit/_timing.py`. `PROVENANCE.md` records the source commit, the file map and the differences allowed. A guard test checks that the package imports only the standard library, `ray` and itself. **Acceptance:** <br>• `import raypoolkit` and `from raypoolkit import RayWorkPool` work in a fresh venv with no client on `sys.path`; <br>• a script, kept in `docs/extraction/`, compares the module with its SGK source and finds no difference beyond the allowed classes; its output is in the log. *(At writing: the import commit is SGK `b510bc9`; the protocol is `raypoolkit.contract.DatastorePool`; the guard has three tests, the third pinning U4's re-export, which shadows the submodule of the same name.)* | **written** 2026-10-10 |
| 02 | `02-the-test-suite.md` | An in-process stand-in for `ray.wait` / `ray.get` over real `ObjectRef`s (U6), and stand-in work objects and pool. Tests that pin every path through `run()`: lookup-only; available with and without an availability handler; compute → store → persist → validate; the post handler at each of its five exits; `store_results` ordering and replacement; a task builder returning one ref, a `{"ref", "compute_payload"}` dict, a sequence, or `None`; `label_builder`; the constructor's checks and every error raised; the in-flight cap and batch sizes. The printed lines are pinned against a frozen clock (U9). Faults 1–4 are each pinned *as they behave*, by a test named for the fault, which 04 inverts. **Acceptance:** each branch of `run()` and each constructor check is reached by a test that a named mutation fails. | not written |
| 03 | `03-supported-versions-and-ci.md` | Dependency ranges in `pyproject.toml` (U7). The suite runs at both ends locally, in fresh scratch venvs, and from an installed wheel that carries no test package. A GitHub Actions workflow runs it at both ends. `README.md` gains usage. 03 makes no tag and pushes nothing; **`v0.1.0`** is tagged on its commit once CI passes there. | not written |
| 04 | `04-fix-the-inherited-faults.md` | Faults 1–5 of §0.2, each with a test the unfixed code fails, and 02's pinning tests inverted. The constructor's handler checks follow U8. The printed lines do not change. *(May be split into 04a and 04b when written, if fault 4's resolution changes what a client must pass.)* | not written |
| 05 | `05-release-v0.2.0.md` | `pyproject.toml` at `0.2.0`, `PROVENANCE.md` and `README.md`; both ends locally and in CI; **`v0.2.0`** tagged on its commit after green CI. | not written |
| 06 | `06-the-adoption-checklists.md` | `docs/adoption/`, one checklist per client, measured read-only at a named client commit and against `v0.2.0`: what it deletes (`RayTools/`); which imports it rewrites; its call sites, and what each must change (CPBH: the store/persist rename and its 14 lookup-only sites; any site U8 affects); its tests that depend on the pool's surface (SGK: §0.2); its documents that go stale (SI: `CLAUDE.md`'s protected list names `RayTools/`); its acceptance. Each says that adopting with DatastoreKit in one campaign is possible but not required. A script counts every client's imports and sites through `git` and `ast`. | not written |
| 07 | `07-verification-and-close-out.md` | A verification document from the package at `v0.2.0` and the records of 01–06; the campaign closed. | not written |

**Order.** 01 → 02 → 03 → 04 → 05 → 06 → 07. 03 follows 02 so that `v0.1.0` is a release whose
behaviour a suite pins: it is SGK's pool, unchanged. 04 follows 03 so that every fix is a
difference from a tagged, tested baseline. 06 is measured against `v0.2.0`, the release the
clients adopt, so that the checklists need no addenda.

## 3. Datastores

**No prompt opens a store of any client**, and the suite opens none at all: the pool is driven by
stand-ins. A measurement that needs a client's code (06's checklists) **reads source files through
`git`**; it does not import a client or run a client's tests.

## 4. The interfaces between prompts

**Fixed by this plan:**

- **The package** is `raypoolkit`, distributed as `raypoolkit` from this repository.
- **The module map.** SGK's module name is kept (U4), and the class is re-exported from the
  package root:

  | SGK | `raypoolkit` |
  |---|---|
  | `RayTools.RayWorkPool` | `raypoolkit.RayWorkPool`; `RayWorkPool` also from `raypoolkit` |
  | `utilities.format_time` (and `SECONDS_PER_*`) | `raypoolkit._timing.<same>` |
  | `Datastore.SQL.ShardedPool.ShardedPool` (the type hint) | a `typing.Protocol` in `raypoolkit`, named by 01 |

- **After 01:** `PROVENANCE.md`; `docs/extraction/compare_with_source.py`; the import guard
  `raypoolkit/tests/test_package_imports.py`.
- **After 02:** the stand-ins under `raypoolkit/tests/` (02 names their entry points); the
  pinning tests of faults 1–4, which 04 inverts.
- **After 03:** `pyproject.toml` at `0.1.0` with U7's range; `.github/workflows/tests.yml`; the
  README's usage. After its CI passes, the tag `v0.1.0`.
- **After 04:** the fixes and their tests. 04 names any change to what a caller must pass.
- **After 05:** `pyproject.toml` at `0.2.0`; the tag `v0.2.0`.
- **After 06:** `docs/adoption/` and its measuring script, which 07 cites.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus
   `docs/OPEN_ISSUES.md`.
4. **Do not fix things the prompt did not ask for.** A defect found in the inherited behaviour is
   recorded, with a §3 issue, not fixed (rule 8).
5. **No prompt edits a client repository, or DatastoreKit.** Reading one is allowed. Running a
   client's code or tests is not.
6. **No test needs a Ray cluster, imports a client, or imports `datastorekit`.** The suite count is
   recorded before and after each prompt; a count that falls is a stop.
7. **The printed lines are an interface** (`CLAUDE.md`). No prompt changes them unless it says so;
   none in this plan does.
8. **Equivalence with the source, through 03.** The package module equals SGK's at blob `b4666fa`,
   modulo §4's map, the internalisation and black. `compare_with_source.py` checks this, and each
   prompt through 03 runs it. Any other difference is a stop.
9. **Deliberate breakage.** Each prompt names mutations its tests must catch. The log records each
   as a diff, exactly as applied, so the orchestrator can replay it with `git apply`. Mutations are
   never committed.
10. **No tag except where a prompt says so** (03: `v0.1.0`; 05: `v0.2.0`), each made on the prompt's
    commit once CI passes there, and none is moved or deleted.

### 5.1 The log template

- the subject, commit and result;
- **What shipped**;
- **Deviations from the prompt**, each classified;
- **Verification performed**: suite count before and after, and (through 03) the output of
  `compare_with_source.py`;
- **The deliberate-breakage record**;
- **Observations not acted on**;
- **State handed to the next prompt**.

## 6. Decisions

### 6.1 Made by the user, and not reopened here

- **D1** (2026-10-10): **extract `RayWorkPool` as a separate, reusable component**, as DatastoreKit
  did for the datastore layer, rather than reconcile the three copies in place.
- **D2** (DatastoreKit, 2026-10-07): the datastore layer went first; the pool is this separate
  unit of work.

### 6.2 Decisions this campaign needs

Each is put with a recommendation. **U1–U3 were taken by the user at set-up on 2026-10-10, and
U4 and U5 the same day for 01, each as recommended**; the recommendation below is the decision.
The others are put when the prompt that needs them is written.

- **U1: the name and the repository.** *Taken:* RayPoolKit, package `raypoolkit`, a public GitHub
  repository `ds283/RayPoolKit` (as DatastoreKit's D3), checked out at
  `/Users/ds283/Documents/Code/RayPoolKit`.
- **U2: the source.** *Taken:* SGK's copy, imported faithfully. It is the superset of the three:
  the others' only extras are wording and a licence header (fault 5), fixed in 04.
- **U3: no dependency on `datastorekit`.** *Taken:* the pool is duck-typed, described by a small
  `typing.Protocol` (`object_store`), and `format_time` is internalised. The two packages version
  independently, and a client may adopt either first.
- **U4: the module name** *(for 01)*. *Taken 2026-10-10:* keep `RayWorkPool.py` as the module name, as
  DatastoreKit kept its modules' names (its U5), and re-export the class from the package root so
  that clients write `from raypoolkit import RayWorkPool`. SGK's AST tests (§0.2) need only that
  the call is spelled `RayWorkPool(...)`. *(At 01's writing: the re-export makes the package
  attribute `raypoolkit.RayWorkPool` the class, shadowing the submodule; the module stays reachable
  through `sys.modules`, `importlib.import_module`, `from raypoolkit.RayWorkPool import …` and
  string targets to `mock.patch`, measured at Python 3.12.15 and 3.13.16. 01 pins this.)*
- **U5: freeze the clients' copies** *(for 01)*. *Taken 2026-10-10:* from 01's writing until each client
  adopts, no client edits its `RayTools/`; a fix wanted in a client is made here and reaches it on
  adoption. G1 (§7) is SGK's half of this.
- **U6: the suite's Ray stand-in** *(for 02)*. *Recommended:* work items are real
  `ray.ObjectRef(bytes)` instances, and the pool module's `ray.wait` and `ray.get` are replaced by
  an in-process stand-in that resolves them from a table, in a controllable order. Alternatives
  rejected: a local Ray cluster (the suite would need one, against `CLAUDE.md`); `local_mode`
  (deprecated and absent at the high end); fake ref classes (the pool tests `isinstance(…,
  ObjectRef)`).
- **U7: the supported versions** *(for 03)*. *Recommended:* `requires-python = ">=3.12"`,
  `ray>=2.43`, tested at Python 3.12.15 / Ray 2.43.0 and Python 3.13.16 / Ray 2.55.1, as
  DatastoreKit's.
- **U8: the constructor's handler checks** *(for 04)*. Options: (a) keep raising when a persist
  handler is set without a compute handler, but as `ValueError`, and add the missing store-handler
  check; (b) make the default persist and store handlers apply only when a compute handler is
  given, so a lookup-only pool needs neither `store_handler=None` nor `persist_handler=None`, and
  raise only on an explicit, unusable combination. *Recommended:* (b). Every existing call site
  keeps working (SGK's and SI's explicit `None`s are still accepted), and CPBH's 14 lookup-only
  sites then need no change on adoption.
- **U9: pin the printed lines** *(for 02)*. *Recommended:* yes, every line's wording and layout,
  against a frozen clock and timer, including SGK's six pinned lines as a case.
- **U10: no shim for CPBH** *(for 06)*. *Recommended:* CPBH renames its 3 compute sites'
  store-handler use on adoption if it overrides it (at HEAD it does not), and the package carries
  no client's old meaning of `store_handler`.

## 7. Gates outside this repository

| Gate | Holds when | Needed by |
|---|---|---|
| **G1** | SGK's `RayTools/RayWorkPool.py` is still blob `b4666fa` when 01 is written. If it has changed, the plan is re-measured before 01. **Holds (2026-10-10)** at SGK `b510bc9`. | 01 |
| **G2** | SGK has adopted `v0.2.0` in a campaign of its own: `RayTools/` deleted, the package imported at a pinned tag, its suites pass, including the six pinned lines. | — |
| **G3** | CPBH has adopted `v0.2.0` in a campaign of its own (06's checklist). | — |
| **G4** | SI has adopted `v0.2.0`, when it is next active (06's checklist). | — |

The campaign closes at 07. G2–G4 are recorded on this board as they hold, but this campaign does
not wait for them.

## 8. Later units of work

None is in this campaign's scope, and none is planned yet. Candidates, once the clients share one
copy: cancellation and clean shutdown on a signal (SGK has probed SIGTERM handling,
`docs/a3-v2-readiness/sigterm_handler_probe.py`); retry of a failed compute; and progress reported
as structured data, which SGK's `StageTracker` now recovers by parsing the printed lines.
