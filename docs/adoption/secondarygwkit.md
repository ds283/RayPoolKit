# Adoption checklist: SecondaryGWKit (SGK)

- **Client:** SecondaryGWKit, `/Users/ds283/Documents/Code/SecondaryGWKit`, at **`b510bc9`**
  (`b510bc90b66985532d28996ab4e5b13b0ff71709`, branch `handover-remedial`, 2026-10-07, "Freeze the
  datastore layer while it moves to DatastoreKit").
- **Tree:** clean at the start and at the end of the measurement (`git status --porcelain` empty,
  no stash).
- **Package:** `raypoolkit` at **`v0.2.0`** (`eaef0ce`).
- **How it was measured:** read-only, by RayPoolKit's extraction prompt 06 on 2026-10-10, through
  `git show`, `git grep`, `git ls-tree` and `git log` only, and by
  [`measure_client_pools.py`](measure_client_pools.py) (the appendix). Nothing of SGK was imported,
  run or opened, and no store was opened. **SGK's adoption campaign measures again before acting,
  and its numbers govern.**
- **This is data, not instructions.** It describes SGK at `b510bc9`. SGK's campaign decides what to
  do, under SGK's `CLAUDE.md`. A recommendation is marked **Advice:**; a choice that is SGK's is
  named as SGK's.

Unless another commit is named, a `path:line` is SGK's at `b510bc9`, and one under `raypoolkit/`
is the package's at `v0.2.0`.

**In one paragraph.** SGK's `RayTools/RayWorkPool.py` is the source of the package: `v0.1.0` is
that file under a new name, and `v0.2.0` is `v0.1.0` with the inherited faults fixed. Every one of
SGK's 54 pool constructions constructs under `v0.2.0` as it stands, and its printed lines are the
package's. So the adoption is mechanical: delete `RayTools/`, rewrite seven imports, and edit one
test module if `raypoolkit` comes before DatastoreKit (item 6). One construction meets a change in
behaviour, `main.py:3247`, and by reading it records the same statistics (item 5).

---

## 1. The client and its versions

- **Python 3.12.15** (`venv/pyvenv.cfg`, read as text: `version = 3.12.15`, MacPorts' 3.12
  framework); **`ray==2.43.0`** (`requirements.txt:74`). Both are exactly the package's tested low
  end, inside the declared `requires-python = ">=3.12"` and `ray>=2.43`.
- **The pin it adds** to `requirements.txt`:
  ```text
  raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
  ```
  SGK keeps its own `ray==2.43.0`. An editable install of `raypoolkit` is never for SGK's production
  runs ([`README.md`](README.md) §1).
- SGK's test command is `CLAUDE.md:106-109` (`PYTHONPATH=. ./venv/bin/python -m unittest discover
  -s ComputeTargets/tests -t .`, at `:108`). Six test roots are tracked: `AdaptiveLevin/tests`,
  `ComputeTargets/tests`, `CosmologyModels/tests`, `Datastore/tests`, `LiouvilleGreen/tests`,
  `RunRegistry/tests`.

## 2. What it deletes

| File | Blob | Lines | Last changed |
|---|---|---|---|
| `RayTools/RayWorkPool.py` | `b4666fa89abb26829fd585b881947d7ef5172cea` | 575 | `0ee16a8`, 2026-09-04, "Split RayWorkPool store_handler into store and persist handlers" |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` (empty) | 0 | — |

With them go the copy's two client imports, `RayTools/RayWorkPool.py:8` (`from
Datastore.SQL.ShardedPool import ShardedPool`, the type hint of `pool` at `:75`) and `:9` (`from
utilities import format_time`). SGK's `utilities.format_time` stays SGK's: the package carries its
own (`raypoolkit/_timing.py`). Nothing else is under `RayTools/`.

## 3. Which imports it rewrites

**Seven**, every one `from RayTools.RayWorkPool import RayWorkPool` at module level, each becoming
`from raypoolkit import RayWorkPool`:

| File:line | Today | After |
|---|---|---|
| `main.py:63` | `from RayTools.RayWorkPool import RayWorkPool` | `from raypoolkit import RayWorkPool` |
| `extract_GkSource_data.py:37` | likewise | likewise |
| `extract_GkWKB_data.py:35` | likewise | likewise |
| `extract_Gk_data.py:32` | likewise | likewise |
| `extract_QuadSourceIntegral_data.py:42` | likewise | likewise |
| `extract_TkWKB_data.py:30` | likewise | likewise |
| `extract_tensor_source_data.py:31` | likewise | likewise |

- No import is nested, none names a private name, and no `import_module` or `__import__` call
  names `RayTools` (appendix).
- **Keep the bare name.** `from raypoolkit import RayWorkPool` keeps every call spelled
  `RayWorkPool(...)`, which five test modules need (item 6). A spelling `raypoolkit.RayWorkPool(...)`
  would be an attribute call, and their `ast` matches would miss it.
- **String literals naming `RayTools`: 8.** Six are in `Datastore/tests/test_layer_is_generic.py`
  (`:1`, `:70`, `:88`, `:120`, `:192`, `:357`; item 6). One is
  `docs/tolerance-convergence/inventory.py:382`, `"RayTools"` in `PRODUCTION_TREES` (item 9). One
  is in an archived campaign script, `prompts/datastore-generic/orchestrator/measure-09/scripts/m3_make_mutations.py:33`,
  a record, not rewritten.

## 4. Its call sites

**54** `RayWorkPool(...)` calls, each with two positional arguments (`pool`, `task_list`), no
`**kwargs`, and a `title` keyword (26 a title, 28 `title=None`, which prints nothing):

| | Calls | Spelled |
|---|---|---|
| No compute handler (`compute_handler=None`) | 44 | every one with `store_handler=None, persist_handler=None`; 6 also pass every other handler as `None`, 27 all but `post_handler`, 1 sets `post_handler` (`main.py:2974`), 10 pass only the three `None`s (appendix, "by spelling") |
| Compute handler given | 6 | `main.py:1420`, `:1634`, `:2115`, `:2428`, `:3229`, `:3247`; none passes `store_handler` or `persist_handler` |
| Compute handler left at its default | 4 | `main.py:1042` and `:1057` pass no handler; `:1940` passes a validation handler and a label builder; `:4146` passes `validation_handler=None` and a label builder |
| `store_results=True` | 39 | |

**Every one constructs under `v0.2.0`**, by the package's own constructor (the appendix's verdict
column). Every size is a literal of at least 1; no size is flagged.

**Sites that must change: none at `b510bc9`.**

- The ten compute pools get the package's default store and persist handlers
  (`raypoolkit/RayWorkPool.py:79-84`: `obj.store()`, then `pool.object_store(obj)`), as they get
  SGK's today (`RayTools/RayWorkPool.py:64-69`, the same two).
- The 44 lookup-only pools may keep `store_handler=None, persist_handler=None`, or drop both:
  under `v0.2.0` a pool with no compute handler needs only `compute_handler=None`, and the two
  `None`s are accepted and change nothing, the printed lines included
  ([Which handlers a pool needs](../../README.md#which-handlers-a-pool-needs)). The choice is SGK's.
  **Advice:** keep them in the adoption commit, so that its diff is the imports alone.
- `main.py:2974` gives a post handler to a pool with no compute handler. `v0.2.0` accepts that:
  `available_handler` and `post_handler` are used on the lookup path (same section).

## 5. What changes in behaviour

The board's issues are in [`IMPLEMENTATION_STATE.md`](../../prompts/extraction/IMPLEMENTATION_STATE.md)
§4; the package's own account is [Changes in `v0.2.0`](../../README.md#changes-in-v020).

| Change | At SGK | Issue | What SGK should check |
|---|---|---|---|
| Constructor checks raise `ValueError` (decision U8) | no site affected: all 54 construct. SGK's copy refused a persist handler with no compute handler (`RuntimeWarning`) and a compute handler with `persist_handler=None` (`RuntimeError`); no SGK `except` clause wraps a pool construction (the three in `main.py` are at `:297`, `:505` and `:520`, none around a `RayWorkPool(...)`) | `[00-the-constructor-checks-its-handlers-unevenly]`, `[02-the-constructor-does-not-check-its-sizes]` | nothing, if every site still constructs (item 8) |
| A pool with no compute handler needs only `compute_handler=None` | the 44 lookup-only sites, optionally (item 4) | `[00-the-constructor-checks-its-handlers-unevenly]` | nothing |
| **The post handler after a persist, with no validation handler, gets the persisted object** | **`main.py:3247`** (below) | `[00-a-post-handler-after-persist-gets-the-unpersisted-object]` | the statistics `main.py:3265-` prints, if SGK wants a measurement (below) |
| `store_results=True` accepts a generator | accepted; no SGK site needs it | `[00-store-results-sizes-from-len-of-the-task-list]` | nothing |
| In-flight work keyed on each ref's value | every site; no visible change while `ray.wait` returns the refs it was given | `[00-in-flight-work-is-keyed-on-a-bound-method]` | nothing |
| The "available" rate computed from the available count | already so in SGK's copy (`e81b145`) | — (README §0.2, fault 6) | nothing |
| The constructor's messages say "handler" | exception text only; no SGK site raises one | `[00-messages-say-maker-and-the-module-has-no-licence-header]` | nothing |

**`main.py:3247`** is the `GkSourcePolicy_queue` (`APPLY GKSOURCE POLICIES`): a compute handler
(`compute_GkSourcePolicy_work`), `validation_handler=None`, and `post_handler=postprocess_GkSourcePolicy`.
SGK's copy calls the post handler with its local object, from before the persist; `v0.2.0` calls it
with the object the persist returned (`raypoolkit/RayWorkPool.py:529-530`).

- **What the handler reads.** `postprocess_GkSourcePolicy` (`main.py:2871`) reads `obj.policy`
  (`:2874`), `policy.label` (`:2875`), `policy.store_id` only when the label is `None` (`:2876`; the
  policy's, not `obj`'s), `obj.type` (`:2882`) and `obj.quality` (`:2883`), and counts them into
  `GkSourcePolicy_statistics`. It keeps no reference to `obj` and returns `None`.
- **What the persisted object is.** `pool.object_store(obj)` is `ShardedPool.object_store`
  (`Datastore/SQL/ShardedPool.py:3328`). `GkSourcePolicyData` is sharded on `k`
  (`config/sharding.py:32`), so the object goes to one shard's `Datastore` actor,
  `self._shards[shard_id].object_store.remote(item)` (`Datastore/SQL/ShardedPool.py:3418`), whose
  `object_store` (`Datastore/SQL/Datastore.py:598`) returns what the factory's `store` returns
  (`:648`, `:658`, `:670`). `sqla_GkSourcePolicyData_factory.store`
  (`Datastore/SQL/ObjectFactories/GkSourcePolicyData.py:150-174`) inserts the row, sets
  `obj._my_id` (`:172`) and returns `obj` (`:174`). So the persisted object is the local object as
  Ray carried it to the actor and back, with `store_id` set. `policy`, `type` and `quality` read
  `_policy`, `_type` and `_quality` (`ComputeTargets/GkSourcePolicyData.py:584-600`), set at
  construction (`_policy`, `:519`) and by `store()` before the persist (`_type` and `_quality`,
  `:574-575`), and they travel with the object: neither
  `GkSourcePolicyData` nor `GkSourcePolicy` nor `DatastoreObject` (`Datastore/object.py`) defines
  `__getstate__`, `__setstate__` or `__reduce__` (`git grep` finds them only in
  `Datastore/SQL/schema.py` and `Datastore/replication.py`).
- **So, by reading, nothing the handler records changes**: the same key, type and quality, now
  from a copy whose `store_id` is set. This was not run. **Advice:** if SGK's campaign wants it
  measured, compare the "GkSourcePolicyData SUMMARY STATISTICS" `main.py` prints after the queue
  (`:3265`) in a scoped run before and after adoption, through the driver `CLAUDE.md:114-118` names.

The post handlers at `main.py:1420` and `:2115` (`record_unresolved_osc`) follow a validation
handler, so they are given the validated object, as today. `:3229` passes `post_handler=None`.

**The printed lines.** SGK's copy's seven `print()` calls and its four message helpers
(`_readable_rate`, `_format_rates`, `_build_queued_status_message`, `_build_completed_status_message`)
are the package's, by `ast`. What SGK's `StageTracker` parses does not change (item 6), nor do the
lines two dated measurement scripts parse: the completion line
(`docs/datastore-integrity-verification/qsi_resolution_cost.py:29`) and the `Queue summary` line
(`docs/datastore-integrity-verification/stage_counts.py:18`).

## 6. Its tests

Seven test modules name `RayWorkPool` or `RayTools` (appendix).

**`RunRegistry/tests/test_pipeline_adoption.py`** pins what the run registry reads of the pool's
output. `A3_OUTPUT` (`:38-44`) holds five lines: the banner `** CALCULATE QUADRATIC SOURCE
INTEGRALS` (`:39`) and two progress notifications of two lines each (`:40-43`), stamped `+0100`.
The comment above it (`:32-37`) speaks of six lines, "the banner from its constructor (:166), two
progress notifications (:548) and the completion pair (:566)"; the completion pair is not in the
block (another test feeds one completion line, `:125`), and the pool prints no UTC offset
(`datetime.now()` is naive; `raypoolkit/RayWorkPool.py:584-585`). The test feeds the block to `StageTracker`, whose three patterns are in its driver
(`docs/gktk-remedial/scoped_pipeline_run.py:120-124`, named at `:30`): the banner, the progress
line's "`n/m work items remaining = p% complete`", and "`ALL WORK ITEMS COMPLETE`". The package's
banner, progress and completion lines are unchanged (decision U9), so the test needs no change.
It names `RayWorkPool` once, in that comment (`:32`), and `RayTools` nowhere; the comment's line
numbers are those of SGK's copy (`:166` the banner `print`, `:548` a progress `print(msg)`, `:566`
the completion `print(`), which at `v0.2.0` are `raypoolkit/RayWorkPool.py:206`, `:588` and `:606`
(item 9).

**Five `ComputeTargets/tests/` modules** need only that the call stays spelled `RayWorkPool(...)`:
- three find pool constructions by `ast.Call` whose `func` is an `ast.Name` with `id ==
  "RayWorkPool"`: `test_main_plumbing.py:445-450` and `:733-737`; `test_quadsource_policy_main.py:142-146`;
  `test_wkb_numeric_parent_main.py:83-87` and `:117-121`;
- two compile one function of `main.py` and bind the name `RayWorkPool` to a stand-in:
  `test_gksource_parent_set_main.py:262-290` (`"RayWorkPool": _WorkPool` at `:270`) and
  `test_quadsource_integral_parent_main.py:782-` (at `:790`). Neither executes `main.py`'s import
  line.

`from raypoolkit import RayWorkPool` keeps all five passing.

**`Datastore/tests/test_layer_is_generic.py` counts `RayTools/` as part of the datastore layer.**
- `layer_files()` adds `RayTools/*.py` (`:70-71`); `AUDIT_LIST` names `RayTools/RayWorkPool.py`
  (`:88`), and `test_the_derived_files_hold_the_audits_list` asserts that every listed file is found
  (`:303-304`). `_NOT_PROJECT_PACKAGES` names `RayTools` (`:120`), `import_allowed` allows any
  `RayTools` module (`:192-193`), and `test_the_allow_list` asserts it allows `RayTools.RayWorkPool`
  (`:357`). The docstring (`:5-7`) and a comment (`:182`) name it too.
- **What it needs, in each order** (item 7):
  - **`raypoolkit` first:** with `RayTools/` deleted, the glob at `:70-71` finds nothing and
    `:303-304` **fails**, since `:88` lists a file that is gone. The least edit is `:88`.
    `:120`, `:192-193` and `:357` keep passing (`:357` only because `:192-193` stays; removing one
    without the other fails `:357`). **Advice:** remove the `RayTools` entries together (`:7`,
    `:70-71`, `:88`, `:120`, `:182`, `:192-193`, `:357`), so that the module says what the layer is.
  - **DatastoreKit first:** DatastoreKit's SGK checklist deletes this module when SGK adopts
    DatastoreKit ([its item 7](https://github.com/ds283/DatastoreKit/blob/v0.2.1/docs/adoption/secondarygwkit.md),
    `secondarygwkit.md:230-232` at `v0.2.1`); nothing is left for `raypoolkit`'s adoption.
  - **Both in one campaign:** retired with the datastore layer; no edit for `RayTools`.

No other SGK test names the pool.

## 7. The order with DatastoreKit

- **The import.** `RayTools/RayWorkPool.py:8`, `from Datastore.SQL.ShardedPool import ShardedPool`,
  is used only as the type hint of `pool` (`:75`). DatastoreKit's SGK checklist at `v0.2.1` lists
  it among the imports to rewrite (`secondarygwkit.md:92`, and its appendix, `:704`), and notes
  that `test_layer_is_generic.py`'s `layer_files()` "would find only `RayTools/` once the layer is
  gone" (`:230-232`).
- **Decision U12** (2026-10-10): if SGK adopts DatastoreKit first, it may rewrite that one line to
  `from datastorekit.SQL.ShardedPool import ShardedPool`, and nothing else in `RayTools/`; the
  `raypoolkit` adoption then deletes the file. If SGK adopts `raypoolkit` first, the file is gone
  and DatastoreKit's rewrite list has one import fewer. Adopting both in one campaign is possible but
  not required. The orders and what each does to `test_layer_is_generic.py` are item 6 and
  [`README.md`](README.md) §5.
- **SGK's `CLAUDE.md:69-73`** says "The `RayTools/` files are not frozen either: they are not part
  of this extraction" (`:70-71`). Of DatastoreKit's extraction that is so; this repository's
  decision U5 freezes them until SGK adopts `raypoolkit`, U12 excepting the one import (item 9).
- DatastoreKit's checklist for SGK: <https://github.com/ds283/DatastoreKit/blob/v0.2.1/docs/adoption/secondarygwkit.md>.

## 8. Its acceptance

G2 holds when SGK has adopted `v0.2.0` in a campaign of its own, and:
1. `RayTools/` is gone: `git ls-tree <commit> RayTools` is empty.
2. **No import of `RayTools`:** `measure_client_pools.py sgk --commit <commit>` reports 0 imports
   and 0 `import_module` / `__import__` calls naming it. A string literal may remain only where SGK
   chose to keep it (item 9) or in a campaign record.
3. `requirements.txt` holds the pin of item 1, and SGK's venv is installed from it.
4. **SGK's suites pass**: `ComputeTargets/tests` (the five modules of item 6 among them),
   `RunRegistry/tests` (`test_pipeline_adoption.py` among them) and `Datastore/tests`
   (`test_layer_is_generic.py` as item 6 leaves it), and the other three roots. The campaign plan's
   wording of G2 says "the six pinned lines"; what the test pins is the five-line `A3_OUTPUT` block
   of item 6.
5. **Every site constructs**: the script at the new commit gives every call the verdict
   "constructs", and finds as many calls as SGK expects (54 at `b510bc9`).
6. The gate is recorded on this repository's extraction board, §2, row G2.

## 9. What goes stale in it

- **`CLAUDE.md:69-73`**, the paragraph whose `:70-71` says the `RayTools/` files are not frozen
  (item 7). After adoption there is no `RayTools/`.
- **`RunRegistry/tests/test_pipeline_adoption.py:32-33`**, the comment's `:166`, `:548` and `:566`,
  line numbers of the deleted copy (item 6).
- **`Datastore/tests/test_layer_is_generic.py`**, as item 6 says.
- **`docs/tolerance-convergence/inventory.py:382`**, `"RayTools"` in `PRODUCTION_TREES`
  (`:373-386`). `production_files()` skips a tree that does not exist (`:418-421`), so the script
  still runs; but it lists the trees in its report (`:1350`), so a regenerated
  `docs/tolerance-convergence/TOLERANCE-INVENTORY.md` would still name `RayTools` as `:563` does.
- **Prose in `docs/`**, 39 lines in 10 files (the appendix lists each with its text). Each is a
  dated audit or verification document, or planning prose, and describes the copy as it was:
  - `docs/a3-v2-readiness-audit.md:88`, `:90`, `:232`, `:583`, `:584`: the copy's lookup branch and
    its `ray.wait` with no timeout, read in `RayTools/RayWorkPool.py`;
  - `docs/a3-v2-readiness-verification.md:536` and `docs/a3-v2-readiness/rehearsal/reader_rows.txt:10`:
    a recorded traceback through `RayTools/RayWorkPool.py`, line 331;
  - `docs/backport-modules-audit.md:16`, `:48`, `:78`, `:81`, `:220`, `:222`, `:256`, `:258`, `:284`,
    `:429`, `:430`, `:456`, `:459`: the audit that compared the three copies (line counts, the
    `None` return, the store/persist split, the available-rate slip), by the copies' line numbers;
  - `docs/backport-modules-verification.md:40`, `:44`, `:75`, `:110`, `:112`, `:140`, `:141`, `:179`,
    `:183`, `:215`, `:285`: its verification (commits `e81b145` and `0ee16a8`, 45 constructions, a
    byte-compile and import of `RayTools/*.py`);
  - `docs/datastore-generic-audit.md:242`, `:244`: `RayTools/RayWorkPool.py` counted in the
    datastore layer, as `test_layer_is_generic.py` counts it;
  - `docs/gktk-remedial-verification.md:562`, `:704` and `docs/source-remediation-verification.md:31`:
    runs through a real `RayWorkPool`;
  - `docs/one-loop-planning/resonance-scaffolding-v1/sigw-resonance-reconciliation.md:199`, `:287`:
    work items "through `RayWorkPool`", which stays true;
  - `docs/tolerance-convergence/TOLERANCE-INVENTORY.md:563`: `RayTools` among the production trees
    (above).

  **Advice:** do not rewrite them. Each records the copy at its date; SGK's own rules for its
  documents govern.
- **Campaign records**: `prompts/`, 156 lines in 44 files. They are history, and are not rewritten.

---

## Appendix: the script's output

`./venv/bin/python docs/adoption/measure_client_pools.py sgk`, from this repository's root at
extraction prompt 06's commit, with `raypoolkit` `0.2.0`; as printed.

# `RayWorkPool` in SecondaryGWKit (SGK) at `b510bc9`

- **Repository:** `/Users/ds283/Documents/Code/SecondaryGWKit`, read through `git` only.
- **Commit:** `b510bc90b66985532d28996ab4e5b13b0ff71709`.
- **Verdicts by:** `raypoolkit 0.2.0`, its own constructor.
- **Files:** 1432 tracked; 460 `.py` files outside `RayTools/` parsed; 0 did not parse; 0 binary, not searched; 0 datastores, not read.
- **`ray.is_initialized()` after the verdicts:** False.

## `RayTools/` at the commit

| File | Blob |
|---|---|
| `RayTools/RayWorkPool.py` | `b4666fa89abb26829fd585b881947d7ef5172cea` |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |

## Totals

| Measure | Count |
|---|---|
| Imports of a `RayTools` module | 7 (module level 7, nested 0) |
| … naming a private name | 0 |
| String literals naming `RayTools` | 8 |
| `import_module` / `__import__` calls naming `RayTools` | 0 |
| `RayWorkPool(...)` calls | 54 |
| … no compute handler (`compute_handler=None`) | 44 |
| … compute handler given | 6 |
| … compute handler left at its default | 4 |
| … `store_results=True` | 39 |
| … with a `title` keyword | 54 (`title=None` 28, set 26) |
| … positional arguments | 2 at 54 |
| … with `*args` / `**kwargs` | 0 / 0 |
| Verdicts | `constructs` 54 |
| Calls with a flag / flags | 0 / 0 |
| Lines of non-`.py` files naming `RayTools` or `RayWorkPool` | 196 |
| Test modules naming `RayTools` or `RayWorkPool` | 7 |

## The handler keywords, by spelling

Each handler keyword as absent (—), `None` or set; a row per spelling, with its calls.

| `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` | Calls |
|---|---|---|---|---|---|---|---|
| None | None | None | None | None | None | None | 6 |
| None | None | None | None | None | — | None | 27 |
| None | None | None | None | None | set | None | 1 |
| None | None | None | — | — | — | — | 10 |
| — | — | — | — | None | — | set | 1 |
| — | — | — | — | — | — | — | 2 |
| — | — | — | — | set | — | set | 1 |
| set | — | — | — | None | set | None | 1 |
| set | — | — | — | set | None | set | 1 |
| set | — | — | — | set | — | set | 2 |
| set | — | — | — | set | set | set | 2 |

## Imports of a `RayTools` module (7)

| File:line | Scope | Statement | Private names |
|---|---|---|---|
| `extract_GkSource_data.py:37` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_GkWKB_data.py:35` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_Gk_data.py:32` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_QuadSourceIntegral_data.py:42` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_TkWKB_data.py:30` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_tensor_source_data.py:31` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `main.py:63` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |

## String literals naming `RayTools` (8)

```text
Datastore/tests/test_layer_is_generic.py:1 [(module)] "\nThe generic layer names nothing of the project, and imports nothing of it but two generic\nmodules (prompts/datastore-generic, prompt 09; README \u00a75 rule
Datastore/tests/test_layer_is_generic.py:70 [layer_files] "RayTools"
Datastore/tests/test_layer_is_generic.py:88 [(module)] "RayTools/RayWorkPool.py"
Datastore/tests/test_layer_is_generic.py:120 [(module)] "RayTools"
Datastore/tests/test_layer_is_generic.py:192 [import_allowed] "RayTools"
Datastore/tests/test_layer_is_generic.py:357 [TestTheLayerImportsNoProjectPackage.test_the_allow_list] "RayTools.RayWorkPool"
docs/tolerance-convergence/inventory.py:382 [(module)] "RayTools"
prompts/datastore-generic/orchestrator/measure-09/scripts/m3_make_mutations.py:33 [(module)] "    for path in (REPO_ROOT / \"RayTools\").glob(\"*.py\"):\n        found.add(path.relative_to(REPO_ROOT).as_posix())\n"
```

## `import_module` / `__import__` calls naming `RayTools` (0)

None.

## `RayWorkPool(...)` calls (54)

Each call at the line of its name. Handlers: absent (—), `None` or set. Sizes: the source text of each size keyword given. `results`: `store_results`. Verdict: `v0.2.0`'s constructor, given the classes.

| File:line | Scope | Pos. | `**` | compute | store | persist | available | validation | post | label | Sizes | `results` | Title | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `extract_GkSource_data.py:812` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_GkSource_data.py:825` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_GkSource_data.py:910` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_GkWKB_data.py:403` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_GkWKB_data.py:416` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_GkWKB_data.py:483` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_Gk_data.py:359` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_Gk_data.py:372` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_Gk_data.py:432` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_QuadSourceIntegral_data.py:1105` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_QuadSourceIntegral_data.py:1118` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_QuadSourceIntegral_data.py:1272` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_TkWKB_data.py:422` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_TkWKB_data.py:472` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_tensor_source_data.py:355` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_tensor_source_data.py:399` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `main.py:1042` | `run_pipeline` | 2 | — | — | — | — | — | — | — | — | `create_batch_size=10`, `process_batch_size=10`, `max_task_queue=30` | True | set | `constructs` |
| `main.py:1057` | `run_pipeline` | 2 | — | — | — | — | — | — | — | — | `create_batch_size=10`, `process_batch_size=10`, `max_task_queue=30` | True | set | `constructs` |
| `main.py:1319` | `run_pipeline.build_Tk_numeric_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1420` | `run_pipeline` | 2 | — | set | — | — | — | set | set | set | `create_batch_size=2`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:1483` | `run_pipeline.build_Tk_WKB_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1550` | `run_pipeline.build_Tk_WKB_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1634` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:1701` | `run_pipeline.build_tensor_source_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1767` | `run_pipeline.build_tensor_source_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1824` | `run_pipeline.build_tensor_source_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1940` | `run_pipeline` | 2 | — | — | — | — | — | set | — | set | `create_batch_size=1`, `process_batch_size=20`, `max_task_queue=300` | False | set | `constructs` |
| `main.py:1993` | `run_pipeline.build_Gk_numeric_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2115` | `run_pipeline` | 2 | — | set | — | — | — | set | set | set | `create_batch_size=2`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:2188` | `run_pipeline.build_Gk_WKB_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2265` | `run_pipeline.build_Gk_WKB_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2428` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:2502` | `run_pipeline.resolve_GkSource_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=5`, `process_batch_size=10` | True | None | `constructs` |
| `main.py:2584` | `run_pipeline.build_GkSource_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2659` | `run_pipeline.build_missing_GkSource` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=5`, `process_batch_size=10` | True | None | `constructs` |
| `main.py:2926` | `run_pipeline.build_incomplete_GkSourcePolicy` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2974` | `run_pipeline.build_incomplete_GkSourcePolicy` | 2 | — | None | None | None | None | None | set | None | `create_batch_size=20`, `process_batch_size=20` | False | None | `constructs` |
| `main.py:3034` | `run_pipeline.build_GkSourcePolicy_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3074` | `run_pipeline.build_GkSourcePolicy_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3163` | `run_pipeline.build_missing_GkSourcePolicy` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3229` | `run_pipeline` | 2 | — | set | — | — | — | set | None | set | `create_batch_size=1`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:3247` | `run_pipeline` | 2 | — | set | — | — | — | None | set | None | `create_batch_size=1`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:3350` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3398` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3460` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3515` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3557` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3686` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3783` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3824` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3886` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3958` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3997` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:4146` | `run_pipeline` | 2 | — | — | — | — | — | None | — | set | `create_batch_size=1`, `process_batch_size=100`, `max_task_queue=1000` | False | set | `constructs` |

## Calls with a compute path: the handlers given (10)

The source text of each handler keyword given, at each call whose compute handler is given or left at its default.

| File:line | `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` |
|---|---|---|---|---|---|---|---|
| `main.py:1042` | — | — | — | — | — | — | — |
| `main.py:1057` | — | — | — | — | — | — | — |
| `main.py:1420` | `compute_Tk_numeric_work` | — | — | — | `validate_Tk_numeric_work` | `lambda obj: record_unresolved_osc(Tk_unresolved_osc, obj)` | `build_Tk_numeric_work_label` |
| `main.py:1634` | `compute_Tk_numeric_work` | — | — | — | `validate_Tk_numeric_work` | — | `build_Tk_numeric_work_label` |
| `main.py:1940` | — | — | — | — | `validate_tensor_source_work` | — | `build_tensor_source_work_label` |
| `main.py:2115` | `compute_Gk_numeric_work` | — | — | — | `validate_Gk_numeric_work` | `lambda obj: record_unresolved_osc(Gk_unresolved_osc, obj)` | `build_Gk_numeric_work_label` |
| `main.py:2428` | `compute_Gk_WKB_work` | — | — | — | `validate_Gk_WKB_work` | — | `build_Gk_WKB_work_label` |
| `main.py:3229` | `compute_GkSource_work` | — | — | — | `validate_GkSource_work` | `None` | `build_GkSource_work_label` |
| `main.py:3247` | `compute_GkSourcePolicy_work` | — | — | — | `None` | `postprocess_GkSourcePolicy` | `None` |
| `main.py:4146` | — | — | — | — | `None` | — | `build_QuadSourceIntegral_label` |

## Flags (0, on 0 calls)

None.

## Notification keywords, by source text (16 calls; never passed)

| File:line | Keywords |
|---|---|
| `extract_GkSource_data.py:910` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_GkWKB_data.py:483` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_Gk_data.py:432` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_QuadSourceIntegral_data.py:1272` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_TkWKB_data.py:472` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_tensor_source_data.py:399` | `notify_batch_size=50`, `notify_time_interval=120` |
| `main.py:1042` | `notify_batch_size=10`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:1057` | `notify_batch_size=10`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:1420` | `notify_batch_size=500`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:1634` | `notify_batch_size=500`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:1940` | `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:2115` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:2428` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:3229` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:3247` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:4146` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |

## Non-`.py` files naming `RayTools` or `RayWorkPool` (196 lines)

| Top directory | Lines | Files |
|---|---|---|
| `CLAUDE.md` | 1 | 1 |
| `docs/` | 39 | 10 |
| `prompts/` | 156 | 44 |

Each line outside the campaign records (`prompts/`, `.prompts/`), 40:

```text
CLAUDE.md:71: `RayTools/` files are not frozen either: they are not part of this extraction. SecondaryGWKit's
docs/a3-v2-readiness-audit.md:88: - **Helpers that make no `pool.` call** [read]: `RayWorkPool` with `compute_handler`,
docs/a3-v2-readiness-audit.md:90: only its `task_builder` and never stores (`RayTools/RayWorkPool.py`, the `lookup` branch);
docs/a3-v2-readiness-audit.md:232: measured. `RayWorkPool`'s `ray.wait` has no timeout (read: `RayTools/RayWorkPool.py`, the main
docs/a3-v2-readiness-audit.md:583: `KeyboardInterrupt` keeps its type; anything else is held until the wait ends, and `RayWorkPool`'s
docs/a3-v2-readiness-audit.md:584: wait has no timeout (S1, measured; RayWorkPool read). **So the handler must record the signal
docs/a3-v2-readiness-verification.md:536: File ".../RayTools/RayWorkPool.py", line 331, in run
docs/a3-v2-readiness/rehearsal/reader_rows.txt:10: File "/Users/ds283/Documents/Code/SecondaryGWKit/RayTools/RayWorkPool.py", line 331, in run
docs/backport-modules-audit.md:16: | `RayTools/RayWorkPool.py` | 558 lines | 580 | 590 |
docs/backport-modules-audit.md:48: - `RayWorkPool.py`: differs by exactly one change, present **only in `SI`** (item **E1**).
docs/backport-modules-audit.md:78: | **B4** | `RayWorkPool` task builder returning `None` | CPBH→SI | **Backport** | XS |
docs/backport-modules-audit.md:81: | **E1** | `store_handler` / `persist_handler` split in `RayWorkPool` | SI | **Backport with care** | M (35 call sites) |
docs/backport-modules-audit.md:220: ### B4. `RayWorkPool` does not tolerate a task builder returning `None`
docs/backport-modules-audit.md:222: - **SGWK location:** `RayTools/RayWorkPool.py:283-297` (the `list`/`tuple`/`set` vs. scalar dispatch)
docs/backport-modules-audit.md:256: ### E1. `RayWorkPool`: `store_handler` / `persist_handler` split
docs/backport-modules-audit.md:258: - **SGWK locations:** `RayTools/RayWorkPool.py:64-65` (`_default_store_handler`), `89-97`
docs/backport-modules-audit.md:284: `extract_TkWKB_data.py`, `extract_tensor_source_data.py`; 45 `RayWorkPool(...)` constructions in
docs/backport-modules-audit.md:429: - **D4.** `RayWorkPool` notification bookkeeping: `self._last_num_available_complete = self._num_store_complete`
docs/backport-modules-audit.md:430: (`SGWK/RayWorkPool.py:543`, `SI:575`) — copy-paste; should be `self._num_available_complete`.
docs/backport-modules-audit.md:456: `RayWorkPool` + `ClientPool`.
docs/backport-modules-audit.md:459: 5. **Commit 5 — `persist_handler` split (E1), if wanted.** `RayWorkPool` + all 35 `store_handler=None`
docs/backport-modules-verification.md:40: e81b145 Tidy up latent faults in ShardedPool, RayWorkPool and ClientPool (prompt 03)
docs/backport-modules-verification.md:44: 0ee16a8 Split RayWorkPool store_handler into store and persist handlers (prompt 05)
docs/backport-modules-verification.md:75: | `RayWorkPool(` | 45 | **45** |
docs/backport-modules-verification.md:110: | Byte-compile | `./venv/bin/python3 -m py_compile main.py extract_*.py Datastore/SQL/*.py Datastore/SQL/ObjectFactories/*.py RayTools/*.py config/sharding.py tools/*.py` | exit 0 |
docs/backport-modules-verification.md:112: | Import, for real | `import Datastore.SQL.ShardedPool`, `Datastore.SQL.Datastore`, `RayTools.RayWorkPool`, `config.sharding` | all import clean, **no `sys.modules` stub needed** — confirms `d6f4a43` generalises |
docs/backport-modules-verification.md:140: | 6 | Task builder returning `None` completes under `store_results=False`, raises under `store_results=True` | **RUN — PASS** | Against a real `RayWorkPool(pool, ...)` built from the live pool (prompt 03's own verification used a dummy `pool` stand-in): both branches behave exactly as B4 requires. |
docs/backport-modules-verification.md:141: | 7 | Default handlers still store a result correctly | **NOT RUN** | Needs a real compute-target object (`.available`/`.compute()`/`.store()` contract) carried through `RayWorkPool`'s compute→store→persist cycle. See §5. |
docs/backport-modules-verification.md:179: - **Check 7 (default handlers store a real compute result end-to-end).** `RayWorkPool`'s
docs/backport-modules-verification.md:183: for real needs one genuine compute-target object carried through a live `RayWorkPool`, which means
docs/backport-modules-verification.md:215: `Datastore`/`ShardedPool`/`RayWorkPool` test suite is future work, not something to bolt on here.
docs/backport-modules-verification.md:285: - `[01-shard-key-persistence]` and the `read_table`/`RayWorkPool`-negative-case half of
docs/datastore-generic-audit.md:242: `Datastore/shard_paths.py` and `RayTools/RayWorkPool.py`. The factories under OF are the client.
docs/datastore-generic-audit.md:244: infrastructure contract), `RayWorkPool.py` and `ProfileAgent.py` hold no project knowledge.
docs/gktk-remedial-verification.md:562: 16's wiring survives a real `RayWorkPool` with `store_results=False`.
docs/gktk-remedial-verification.md:704: 4. Prompt 16's per-$k$ unresolved-oscillation summary works in a real `RayWorkPool`: **16 printed
docs/one-loop-planning/resonance-scaffolding-v1/sigw-resonance-reconciliation.md:199: for every response `k`. It is looped, not vectorised over grid points (the `RayWorkPool` batches
docs/one-loop-planning/resonance-scaffolding-v1/sigw-resonance-reconciliation.md:287: **Vectorised or looped?** Looped over `(z_response, k, q, r)` work items through `RayWorkPool`, with
docs/source-remediation-verification.md:31: the oracle is valid.** A real `ShardedPool`/`RayWorkPool` run on a locally bootstrapped Ray
docs/tolerance-convergence/TOLERANCE-INVENTORY.md:563: Every keyword argument named `amplitude_rtol`, `atol`, `deriv_rtol`, `epsabs`, `epsrel`, `phase_atol`, `rtol`, `xtol` whose value is a numeric literal, in the production trees `AdaptiveLevin`, `ComputeTargets`, `CosmologyConcepts`, `CosmologyModels`, `Datastore`, `LiouvilleGreen`, `MetadataConcepts`, `Quadrature`, `RayTools`, `Units`, `config`, `utilities`, in `main.py` and in the `extract_*.py` readers. Test trees, `docs/` and `prompts/` are excluded: they measure the pipeline, they are not it.
```

## Test modules naming `RayTools` or `RayWorkPool` (7)

```text
ComputeTargets/tests/test_gksource_parent_set_main.py:218: """Stands in for RayWorkPool: runs the task builder over the items, in order, and keeps the
ComputeTargets/tests/test_gksource_parent_set_main.py:270: "RayWorkPool": _WorkPool,
ComputeTargets/tests/test_main_plumbing.py:432: """Both numeric RayWorkPool constructions pass a post_handler, and both are followed by a
ComputeTargets/tests/test_main_plumbing.py:449: and call.func.id == "RayWorkPool"
ComputeTargets/tests/test_main_plumbing.py:700: of the batch the enclosing `RayWorkPool` dispatches over. `unclassified` holds any site whose
ComputeTargets/tests/test_main_plumbing.py:730: # calls reached through a RayWorkPool task_builder: the tolerance is in the batch
ComputeTargets/tests/test_main_plumbing.py:736: and node.func.id == "RayWorkPool"
ComputeTargets/tests/test_main_plumbing.py:764: label = f"{scope_label}: RayWorkPool({batch_name}) line {call.lineno}"
ComputeTargets/tests/test_quadsource_integral_parent_main.py:615: """Stands in for RayWorkPool: runs the task builder over the items, in order, and keeps the
ComputeTargets/tests/test_quadsource_integral_parent_main.py:790: "RayWorkPool": _WorkPool,
ComputeTargets/tests/test_quadsource_policy_main.py:136: the ``key`` entry or keyword). "query" is a RayWorkPool dispatch over a batch of payload
ComputeTargets/tests/test_quadsource_policy_main.py:145: and node.func.id == "RayWorkPool"
ComputeTargets/tests/test_wkb_numeric_parent_main.py:77: RayWorkPool dispatch over a batch (an existence query or a stage lookup) and "construction" for
ComputeTargets/tests/test_wkb_numeric_parent_main.py:86: and node.func.id == "RayWorkPool"
ComputeTargets/tests/test_wkb_numeric_parent_main.py:114: """The RayWorkPool lines of `scope` dispatching a lookup of `cls`."""
ComputeTargets/tests/test_wkb_numeric_parent_main.py:120: and node.func.id == "RayWorkPool"
Datastore/tests/test_layer_is_generic.py:7: module of ``RayTools/``. ``layer_files()`` derives the set from the filesystem, not from
Datastore/tests/test_layer_is_generic.py:70: for path in (REPO_ROOT / "RayTools").glob("*.py"):
Datastore/tests/test_layer_is_generic.py:88: "RayTools/RayWorkPool.py",
Datastore/tests/test_layer_is_generic.py:120: _NOT_PROJECT_PACKAGES = {"Datastore", "RayTools", "config"}
Datastore/tests/test_layer_is_generic.py:182: # WallclockTimer and format_time (Datastore, ProfileAgent, RayWorkPool): a shared helper that
Datastore/tests/test_layer_is_generic.py:192: if root == "RayTools":
Datastore/tests/test_layer_is_generic.py:357: "RayTools.RayWorkPool",
RunRegistry/tests/test_pipeline_adoption.py:32: # Six lines in the vocabulary `RayWorkPool` prints, in the order it prints them: the banner from
```

## Files that do not parse (0)

None.
