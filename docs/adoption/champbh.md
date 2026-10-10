# Adoption checklist: ChamPBH (CPBH)

- **Client:** ChamPBH, `/Users/ds283/Documents/Code/ChamPBH`, at **`52142d7`**
  (`52142d75aebe00855804e2daff4f63aee50ffc3e`, branch `main`, 2026-10-07, "Store each shard key
  under its own serial").
- **Tree:** **23 uncommitted changes, not read.** `git status --porcelain` lists 23 paths, every
  one untracked (`??`): two run scripts (`full_run_2026.6.0.sh`, `full_run_2026.6.0-refresh.sh`),
  seventeen pilot datastores (`pilot-2026.6.0.db` and `pilot-2026.6.0-shard0000.db` …
  `-shard0015.db`), two logs (`pilot-main.log`, `pilot-plot.log`), `pilot-out/` and
  `prompts/jordan-normalization/`. No tracked file is modified, and none is under `RayTools/`. The
  datastores were not opened. This checklist describes `52142d7`; no stash.
- **Package:** `raypoolkit` at **`v0.2.0`** (`eaef0ce`).
- **How it was measured:** read-only, by RayPoolKit's extraction prompt 06 on 2026-10-10, through
  `git show`, `git grep`, `git ls-tree` and `git log` only, and by
  [`measure_client_pools.py`](measure_client_pools.py) (the appendix). Nothing of CPBH was imported,
  run or opened, and no store was opened. **CPBH's adoption campaign measures again before acting,
  and its numbers govern.**
- **This is data, not instructions.** It describes CPBH at `52142d7`. CPBH's campaign decides what
  to do, under CPBH's `CLAUDE.md`. A recommendation is marked **Advice:**; a choice that is CPBH's
  is named as CPBH's.

Unless another commit is named, a `path:line` is CPBH's at `52142d7`, and one under `raypoolkit/`
is the package's at `v0.2.0`.

**In one paragraph.** CPBH's copy predates the store/persist split: its `store_handler` is what the
package calls the persist handler, and it calls `obj.store()` itself before it. No CPBH site passes
a callable `store_handler`, so under `v0.2.0` every one of its 17 constructions constructs as it
stands and does what CPBH's copy does: the 14 lookup-only sites pass `store_handler=None`, which
the package accepts, and the 3 compute sites use the defaults, which are the same two steps. So the
adoption is: delete `RayTools/`, rewrite three imports. The "available" rate's fix reaches CPBH,
but no CPBH site prints that rate (item 5).

---

## 1. The client and its versions

- **Python 3.13.16** (`venv/pyvenv.cfg`, read as text: `version = 3.13.16`, MacPorts' 3.13
  framework); **`ray==2.53.0`** (`requirements.txt:78`). Inside the declared
  `requires-python = ">=3.12"` and `ray>=2.43`: Python equals the tested high end, and Ray lies
  between the tested ends (2.43.0, 2.55.1), above Python 3.13's effective floor of 2.45.0. Ray
  2.53.0 is not itself tested.
- **The pin it adds** to `requirements.txt`:
  ```text
  raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
  ```
  CPBH keeps its own `ray==2.53.0`. An editable install of `raypoolkit` is never for CPBH's
  production runs ([`README.md`](README.md) §1).
- CPBH's tests run as `CLAUDE.md:63-67` gives them: `unittest` discovery of
  `CosmologyModels/tests`, `ComputeTargets/tests` and `Datastore/tests` (`:64-66`).

## 2. What it deletes

| File | Blob | Lines | Last changed |
|---|---|---|---|
| `RayTools/RayWorkPool.py` | `aaa6dc9218658e1389fe3eeee5d184dcd8dc0d26` | 580 | `79fb527`, 2026-01-25, "Add beta summary plot driver" |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` (empty) | 0 | — |

With them go the copy's two client imports, `RayTools/RayWorkPool.py:23` (`from
Datastore.SQL.ShardedPool import ShardedPool`, the type hint of `pool` at `:86`) and `:24` (`from
utilities import format_time`). CPBH's `utilities.format_time` stays CPBH's. Nothing else is under
`RayTools/`.

## 3. Which imports it rewrites

**Three**, every one `from RayTools.RayWorkPool import RayWorkPool` at module level, each becoming
`from raypoolkit import RayWorkPool`:

| File:line | Today | After |
|---|---|---|
| `main.py:50` | `from RayTools.RayWorkPool import RayWorkPool` | `from raypoolkit import RayWorkPool` |
| `plot_ScalarModel.py:44` | likewise | likewise |
| `plot_by_beta.py:38` | likewise | likewise |

No import is nested, none names a private name, and no string literal, `import_module` or
`__import__` call names `RayTools` (appendix).

## 4. Its call sites

**17** `RayWorkPool(...)` calls, each with two positional arguments, no `**kwargs`, and a `title`
keyword (5 a title, 12 `title=None`):

| | Calls | Spelled |
|---|---|---|
| No compute handler (`compute_handler=None`) | 14 | every one with `store_handler=None` and no `persist_handler`; with `available_handler`, `validation_handler` and `label_builder` `None`, and `post_handler` `None` (1, `plot_ScalarModel.py:1556`) or left out (13) |
| Compute handler given | 3 | `main.py:276`, `:533`, `:820`: a compute handler, a validation handler and a label builder; no `store_handler` |
| `store_results=True` | 13 | |

**Every one constructs under `v0.2.0`**, by the package's own constructor (the appendix's verdict
column). Every size is a literal of at least 1.

**Sites that must change: none at `52142d7`.**

**What CPBH's `store_handler` means, and decision U10.**
- In CPBH's copy, `store_handler` is the persist step: its default is
  `pool.object_store(obj)` (`RayTools/RayWorkPool.py:79-80`, `:90`), and on a completed compute the
  copy calls `obj.store()` unconditionally (`:436`) and then `self._store_handler(obj, self._pool)`
  (`:446`). Its constructor refuses a compute handler with `store_handler=None` (`RuntimeError`,
  `:104-107`) and a `store_handler` with no compute handler (`RuntimeWarning`, raised, `:109-112`),
  which is why CPBH's 14 lookup-only sites pass `store_handler=None`.
- In `v0.2.0`, `store_handler` is the local step, default `obj.store()` (`raypoolkit/RayWorkPool.py:79-80`),
  and `persist_handler` the datastore round-trip, default `pool.object_store(obj)` (`:83-84`).
- **At the 3 compute sites** neither is passed, so `v0.2.0` calls `obj.store()` and then
  `pool.object_store(obj)`: what CPBH's copy does.
- **At the 14 lookup-only sites** `store_handler=None` is accepted, and with no compute handler the
  default persist handler does not apply (`raypoolkit/RayWorkPool.py:109-113`). They construct and
  run as today.
- **Decision U10 (2026-10-10): the package carries no shim** for CPBH's old meaning. It changes no
  CPBH site at `52142d7`, since none passes a callable `store_handler`. **A callable `store_handler`
  added to CPBH before it adopts must become `persist_handler` on adoption** (taking `(obj, pool)`
  and returning the `ObjectRef` of the datastore write); a step that replaces `obj.store()` is the
  new `store_handler`.
- The 14 lookup-only sites may keep `store_handler=None` or drop it: under `v0.2.0` a pool with no
  compute handler needs only `compute_handler=None` ([Which handlers a pool needs](../../README.md#which-handlers-a-pool-needs)).
  The choice is CPBH's. **Advice:** keep them in the adoption commit, so that its diff is the
  imports alone.

## 5. What changes in behaviour

The board's issues are in [`IMPLEMENTATION_STATE.md`](../../prompts/extraction/IMPLEMENTATION_STATE.md)
§4; the package's own account is [Changes in `v0.2.0`](../../README.md#changes-in-v020), written
for a copy that is `v0.1.0`'s pool, which CPBH's is not, so this item says where CPBH differs.

| Change | At CPBH | Issue | What CPBH should check |
|---|---|---|---|
| Constructor checks raise `ValueError` (decision U8) | no site affected: all 17 construct. No tracked `.py` file outside `RayTools/` and `prompts/` has an `except` clause for `RuntimeError` or `RuntimeWarning` | `[00-the-constructor-checks-its-handlers-unevenly]`, `[02-the-constructor-does-not-check-its-sizes]` | nothing, if every site still constructs (item 8) |
| A pool with no compute handler needs only `compute_handler=None` | the 14 lookup-only sites, optionally (item 4) | `[00-the-constructor-checks-its-handlers-unevenly]` | nothing |
| CPBH's `store_handler` meaning "persist" (decision U10) | its 14 `store_handler=None` keep their effect; there is no callable to rename (item 4) | — | that no callable `store_handler` has been added since `52142d7` |
| The post handler after a persist, with no validation handler, gets the persisted object | no site: every compute site has a validation handler, and none has a post handler | `[00-a-post-handler-after-persist-gets-the-unpersisted-object]` | nothing |
| `store_results=True` accepts a generator | accepted | `[00-store-results-sizes-from-len-of-the-task-list]` | nothing |
| In-flight work keyed on each ref's value | every site (CPBH's copy keys on `ref.hex`, e.g. `:439-440`, `:449-450`); no visible change while `ray.wait` returns the refs it was given | `[00-in-flight-work-is-keyed-on-a-bound-method]` | nothing |
| **The "available" rate computed from the available count** | changes the rate's numbers, not the line's layout: CPBH's copy sets `_last_num_available_complete` from the store count (`:565`), the package from the available count (`raypoolkit/RayWorkPool.py:600`). The available segment is printed only by a pool with an availability handler (copy `:185`, `:230`; package `:216`, `:261`), and **no CPBH site gives one** (appendix), so no line CPBH prints at `52142d7` changes | — (README §0.2, fault 6) | the progress lines of any pool given an `available_handler` after `52142d7` |
| A task builder's `None` under `store_results=True` | still a `RuntimeError`, now "a task builder returned None, which is not compatible with store_results=True" (`raypoolkit/RayWorkPool.py:329-333`), where CPBH's copy says "store_results=True is not compatible with returning None values from a task builder" (`:311-315`) | — | nothing, unless CPBH matches the text |
| The constructor's messages say "handler" | exception text only (CPBH's copy says "maker", `:106`, `:111`); no CPBH site raises one | `[00-messages-say-maker-and-the-module-has-no-licence-header]` | nothing |

**The printed lines.** CPBH's copy's seven `print()` calls are the package's, by `ast`, and so are
its `_readable_rate` and `_format_rates`. Its two message builders differ in one condition each:
the "store" segment is printed when `self._store_handler is not None` (`:182`, `:219`), where the
package prints it when `self._persist_handler is not None` (`raypoolkit/RayWorkPool.py:213`,
`:250`). At every CPBH site the two agree: a lookup-only site has neither (CPBH's `store_handler=None`;
the package's persist handler resolves to `None`), and a compute site has both (the defaults). So
the banner, progress and completion lines CPBH's sites print are unchanged in wording and layout.

## 6. Its tests

**No CPBH test module names `RayWorkPool` or `RayTools`** (appendix), and no tracked `.py` file
outside `prompts/` imports `main`. CPBH's suites (item 1) need no change for the adoption.

## 7. The order with DatastoreKit

- **The import.** `RayTools/RayWorkPool.py:23`, `from Datastore.SQL.ShardedPool import ShardedPool`,
  is used only as the type hint of `pool` (`:86`). DatastoreKit's CPBH checklist at `v0.2.1` lists it
  among the `ShardedPool` imports to rewrite (`champbh.md:93`, "a type hint", and its appendix,
  `:602`).
- **Decision U12** (2026-10-10): if CPBH adopts DatastoreKit first, it may rewrite that one line to
  `from datastorekit.SQL.ShardedPool import ShardedPool`, and nothing else in `RayTools/`; the
  `raypoolkit` adoption then deletes the file. If CPBH adopts `raypoolkit` first, the file is gone
  and DatastoreKit's rewrite list has one import fewer. Adopting both in one campaign is possible but
  not required ([`README.md`](README.md) §5). CPBH has no test that counts `RayTools/`, so no order
  needs a test edit.
- DatastoreKit's checklist for CPBH: <https://github.com/ds283/DatastoreKit/blob/v0.2.1/docs/adoption/champbh.md>.

## 8. Its acceptance

G3 holds when CPBH has adopted `v0.2.0` in a campaign of its own, and:
1. `RayTools/` is gone: `git ls-tree <commit> RayTools` is empty.
2. **No import of `RayTools`:** `measure_client_pools.py cpbh --commit <commit>` reports 0 imports,
   0 string literals and 0 `import_module` / `__import__` calls naming it.
3. `requirements.txt` holds the pin of item 1, and CPBH's venv is installed from it.
4. **CPBH's suites pass**, the three of item 1.
5. **Every site constructs**: the script at the new commit gives every call the verdict
   "constructs", and finds as many calls as CPBH expects (17 at `52142d7`).
6. The gate is recorded on this repository's extraction board, §2, row G3.

## 9. What goes stale in it

- **`.documents/architecture-summary.md`**, 21 lines naming the pool (the appendix lists each with
  its text):
  - `:35-36`, the repository layout's `RayTools/` and `RayWorkPool.py`;
  - `:153`, the section "`RayWorkPool` (`RayTools/RayWorkPool.py`)", whose constructor table
    (from `:157`) gives `store_handler` as "`Callable(obj, pool) → ObjectRef` | `pool.object_store(obj)`
    | Persists result" (`:165`), the old meaning (U10), and has no `persist_handler` row;
  - `:585`, "The `RayWorkPool` handles steps 3–4 automatically via its default `compute_handler` and
    `store_handler`", which under `v0.2.0` is three defaults (compute, store, persist);
  - `:648`, "`RayWorkPool` will later call `store()` and then `pool.object_store()`", which stays
    true of the defaults;
  - `:920-925` and `:1086-1094`, two examples of a construction, each still constructing under
    `v0.2.0`; `:999`, "`RayWorkPool` (entire file)" among components reusable with no change; and
    `:155`, `:244`, `:355`, `:829`, `:855`, `:856`, `:862`, `:868`, `:969`, `:1056`, `:1108`,
    `:1110`, `:1116`, which describe what the pool does and stay true.
- **`.documents/integrator-audit-2026-09-30/README.md:69`**: "`RayTools/RayWorkPool.py` calls
  `obj.store()` on a completed compute task with no `try`", a dated audit; the package's default
  store handler does the same.

  **Advice:** update `architecture-summary.md`'s `:35-36`, `:153`, the table from `:157` and
  `:585`, which describe the code; leave the dated audit as it is. CPBH's own rules for its
  documents govern.
- **Campaign records**: `prompts/`, 21 lines in 11 files. They are history, and are not rewritten.

---

## Appendix: the script's output

`./venv/bin/python docs/adoption/measure_client_pools.py cpbh`, from this repository's root at
extraction prompt 06's commit, with `raypoolkit` `0.2.0`; as printed.

# `RayWorkPool` in ChamPBH (CPBH) at `52142d7`

- **Repository:** `/Users/ds283/Documents/Code/ChamPBH`, read through `git` only.
- **Commit:** `52142d75aebe00855804e2daff4f63aee50ffc3e`.
- **Verdicts by:** `raypoolkit 0.2.0`, its own constructor.
- **Files:** 478 tracked; 203 `.py` files outside `RayTools/` parsed; 0 did not parse; 4 binary, not searched; 0 datastores, not read.
- **`ray.is_initialized()` after the verdicts:** False.

## `RayTools/` at the commit

| File | Blob |
|---|---|
| `RayTools/RayWorkPool.py` | `aaa6dc9218658e1389fe3eeee5d184dcd8dc0d26` |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |

## Totals

| Measure | Count |
|---|---|
| Imports of a `RayTools` module | 3 (module level 3, nested 0) |
| … naming a private name | 0 |
| String literals naming `RayTools` | 0 |
| `import_module` / `__import__` calls naming `RayTools` | 0 |
| `RayWorkPool(...)` calls | 17 |
| … no compute handler (`compute_handler=None`) | 14 |
| … compute handler given | 3 |
| … compute handler left at its default | 0 |
| … `store_results=True` | 13 |
| … with a `title` keyword | 17 (`title=None` 12, set 5) |
| … positional arguments | 2 at 17 |
| … with `*args` / `**kwargs` | 0 / 0 |
| Verdicts | `constructs` 17 |
| Calls with a flag / flags | 0 / 0 |
| Lines of non-`.py` files naming `RayTools` or `RayWorkPool` | 43 |
| Test modules naming `RayTools` or `RayWorkPool` | 0 |

## The handler keywords, by spelling

Each handler keyword as absent (—), `None` or set; a row per spelling, with its calls.

| `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` | Calls |
|---|---|---|---|---|---|---|---|
| None | None | — | None | None | None | None | 1 |
| None | None | — | None | None | — | None | 13 |
| set | — | — | — | set | — | set | 3 |

## Imports of a `RayTools` module (3)

| File:line | Scope | Statement | Private names |
|---|---|---|---|
| `main.py:50` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `plot_ScalarModel.py:44` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `plot_by_beta.py:38` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |

## String literals naming `RayTools` (0)

None.

## `import_module` / `__import__` calls naming `RayTools` (0)

None.

## `RayWorkPool(...)` calls (17)

Each call at the line of its name. Handlers: absent (—), `None` or set. Sizes: the source text of each size keyword given. `results`: `store_results`. Verdict: `v0.2.0`'s constructor, given the classes.

| File:line | Scope | Pos. | `**` | compute | store | persist | available | validation | post | label | Sizes | `results` | Title | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `main.py:193` | `run_pipeline.build_solver_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:276` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=3`, `max_task_queue=24` | False | set | `constructs` |
| `main.py:355` | `run_pipeline.build_adiabatic_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:405` | `run_pipeline.build_adiabatic_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:473` | `run_pipeline.build_adiabatic_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:533` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=3`, `max_task_queue=24` | False | set | `constructs` |
| `main.py:611` | `run_pipeline.build_bbn_data_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:663` | `run_pipeline.build_bbn_data_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:736` | `run_pipeline.build_bbn_data_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:820` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=3`, `max_task_queue=24` | False | set | `constructs` |
| `plot_ScalarModel.py:1556` | `run_pipeline` | 2 | — | None | None | — | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `plot_by_beta.py:715` | `run_pipeline.report_dropped_bbn_models` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:803` | `run_pipeline.report_dropped_scalar_models` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:865` | `run_pipeline.build_plot_work` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:899` | `run_pipeline.build_plot_work` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:926` | `run_pipeline.build_plot_work` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:959` | `run_pipeline` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=10`, `max_task_queue=10` | True | set | `constructs` |

## Calls with a compute path: the handlers given (3)

The source text of each handler keyword given, at each call whose compute handler is given or left at its default.

| File:line | `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` |
|---|---|---|---|---|---|---|---|
| `main.py:276` | `compute_solver_batch` | — | — | — | `validate_solver_batch` | — | `build_solver_batch_label` |
| `main.py:533` | `compute_adiabatic_batch` | — | — | — | `validate_adiabatic_batch` | — | `build_adiabatic_batch_label` |
| `main.py:820` | `compute_bbn_data_batch` | — | — | — | `validate_bbn_data_batch` | — | `build_bbn_data_batch_label` |

## Flags (0, on 0 calls)

None.

## Notification keywords, by source text (5 calls; never passed)

| File:line | Keywords |
|---|---|
| `main.py:276` | `notify_batch_size=2`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:533` | `notify_batch_size=2`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:820` | `notify_batch_size=2`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `plot_ScalarModel.py:1556` | `notify_batch_size=50`, `notify_time_interval=120` |
| `plot_by_beta.py:959` | `notify_batch_size=10`, `notify_min_time_interval=120` |

## Non-`.py` files naming `RayTools` or `RayWorkPool` (43 lines)

| Top directory | Lines | Files |
|---|---|---|
| `.documents/` | 22 | 2 |
| `prompts/` | 21 | 11 |

Each line outside the campaign records (`prompts/`, `.prompts/`), 22:

```text
.documents/architecture-summary.md:35: ├── RayTools/
.documents/architecture-summary.md:36: │   └── RayWorkPool.py               # Generic distributed work queue
.documents/architecture-summary.md:153: ### 3.2 `RayWorkPool` (`RayTools/RayWorkPool.py`)
.documents/architecture-summary.md:155: `RayWorkPool` is the single generic orchestrator for all computation phases. It is instantiated with a list of work items and a set of handler callables, and its `run()` method drives a state machine until every item has been processed.
.documents/architecture-summary.md:244: The `available` property is the sentinel used by `RayWorkPool` to distinguish "already in database" from "needs computation".
.documents/architecture-summary.md:355: 2. For missing items only, call `object_get(...)` without `_do_not_populate`. This creates skeleton rows and returns objects ready for `RayWorkPool` to compute and store.
.documents/architecture-summary.md:585: The `RayWorkPool` handles steps 3–4 automatically via its default `compute_handler` and `store_handler`.
.documents/architecture-summary.md:648: 5. Store sampled `SampleValues` in memory; `RayWorkPool` will later call `store()` and then `pool.object_store()`.
.documents/architecture-summary.md:829: - `store_tag`: groups related computations; used by `RayWorkPool` to tag outputs (e.g. `SamplesPerLog10Z_250`)
.documents/architecture-summary.md:855: → RayWorkPool with compute_handler = ScalarModel.compute()
.documents/architecture-summary.md:856: → RayWorkPool with validation_handler = pool.object_validate()
.documents/architecture-summary.md:862: → RayWorkPool with compute_handler = AdiabaticHistory.compute()
.documents/architecture-summary.md:868: → RayWorkPool with compute_handler = BBNData.compute(payload={"small_network": True})
.documents/architecture-summary.md:920: query_queue = RayWorkPool(
.documents/architecture-summary.md:969: **`RayWorkPool` resilience:** The work pool does not bail out if individual tasks fail — it continues processing remaining items. The `_do_not_populate` two-pass pattern means failed objects are skipped in downstream stages (checked via `obj.failure`).
.documents/architecture-summary.md:999: - `RayWorkPool` (entire file)
.documents/architecture-summary.md:1056: # Copies computation result into self (called by RayWorkPool after compute)
.documents/architecture-summary.md:1086: work_pool = RayWorkPool(
.documents/architecture-summary.md:1108: 4. **`compute()` must return an `ObjectRef`.** `RayWorkPool` expects a Ray future from `compute_handler`. If the computation is CPU-bound and cannot be a Ray task (rare), wrap it in `ray.remote`.
.documents/architecture-summary.md:1110: 5. **`store()` is called on the driver side, not in Ray.** After `ray.get(compute_ref)` completes, `RayWorkPool` calls `obj.store()` on the Python object in the driver process. This should copy data from the compute result into the object's fields. Then `pool.object_store(obj)` is called to serialize to the database.
.documents/architecture-summary.md:1116: 8. **`store_results=True` in `RayWorkPool` is only for query-only passes.** When `task_builder` returns lists of refs (the vectorized case), the indices break. Use `store_results=True` only with scalar-returning `task_builder`s.
.documents/integrator-audit-2026-09-30/README.md:69: short). Only `ComputationFailureError` is caught (`:823`). `RayTools/RayWorkPool.py` calls
```

## Test modules naming `RayTools` or `RayWorkPool` (0)

None.

## Files that do not parse (0)

None.
