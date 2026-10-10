# Adoption checklist: StochasticInstantons (SI)

- **Client:** StochasticInstantons, `/Users/ds283/Documents/Code/StochasticInstantons`, at
  **`7bb3efd`** (`7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7`, branch `main`, 2026-10-09, "Record the
  R1 calculation review and open its issues board").
- **Tree:** clean at the start and at the end of the measurement (`git status --porcelain` empty,
  no stash).
- **Package:** `raypoolkit` at **`v0.2.0`** (`eaef0ce`).
- **How it was measured:** read-only, by RayPoolKit's extraction prompt 06 on 2026-10-10, through
  `git show`, `git grep`, `git ls-tree` and `git log` only, and by
  [`measure_client_pools.py`](measure_client_pools.py) (the appendix). Nothing of SI was imported,
  run or opened, and no store was opened. **SI's adoption campaign measures again before acting,
  and its numbers govern.**
- **This is data, not instructions.** It describes SI at `7bb3efd`. SI's campaign decides what to
  do, under SI's `CLAUDE.md`. A recommendation is marked **Advice:**; a choice that is SI's is named
  as SI's.

Unless another commit is named, a `path:line` is SI's at `7bb3efd`, and one under `raypoolkit/` is
the package's at `v0.2.0`.

**In one paragraph.** SI's copy has the store/persist split, as the package does. Every one of its
16 constructions constructs under `v0.2.0` as it stands. Two things are SI's own: `main.py`
imports the copy's private `_default_store_handler` and passes it four times, which is the same as
leaving `store_handler` out (item 3); and one construction sizes its batches by `len()`, which
`v0.2.0` refuses at 0, though by reading SI never builds an empty model list (item 4). `RayTools/`
is on SI's protected list (item 9).

---

## 1. The client and its versions

- **Python:** `venv/pyvenv.cfg` (read as text) records `version = 3.13.13`, the version when the
  venv was made, and names MacPorts' 3.13 framework as its `base-executable`; that interpreter is
  3.13.16 today. SI's venv was not run. Either version is inside the declared
  `requires-python = ">=3.12"`; 3.13.16 is the tested high end.
- **`ray==2.55.1`** (`requirements.txt:57`): the tested high end, inside `ray>=2.43`.
- **The pin it adds** to `requirements.txt`:
  ```text
  raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
  ```
  SI keeps its own `ray==2.55.1`. An editable install of `raypoolkit` is never for SI's production
  runs ([`README.md`](README.md) §1).
- SI's default test run is `pytest -m "not integration and not slow"` (`CLAUDE.md:21`).

## 2. What it deletes

| File | Blob | Lines | Last changed |
|---|---|---|---|
| `RayTools/RayWorkPool.py` | `92be5b2c9e4c2c65695078bd1b8f97db2f56c7b0` | 590 | `7cf4123`, 2026-06-16, "Refactor imports, reformat code for improved readability, and clean up argument parser in `main.py` and supporting modules." |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` (empty) | 0 | — |

With them go the copy's two client imports, `RayTools/RayWorkPool.py:23` (`from
Datastore.SQL.ShardedPool import ShardedPool`, the type hint of `pool` at `:90`) and `:24` (`from
utilities import format_time`). SI's `utilities.format_time` stays SI's. Nothing else is under
`RayTools/`.

## 3. Which imports it rewrites

**Three**, at module level:

| File:line | Today | After |
|---|---|---|
| `main.py:45` | `from RayTools.RayWorkPool import RayWorkPool, _default_store_handler` | `from raypoolkit import RayWorkPool`, and one of the options below |
| `plot_GradientCoupledSolutions.py:100` | `from RayTools.RayWorkPool import RayWorkPool` | `from raypoolkit import RayWorkPool` |
| `plot_InstantonSolutions.py:72` | `from RayTools.RayWorkPool import RayWorkPool` | `from raypoolkit import RayWorkPool` |

No import is nested, and no string literal, `import_module` or `__import__` call names `RayTools`
(appendix).

**`_default_store_handler`, a private name.** `main.py:45` imports it, and `main.py` passes it as
`store_handler` four times:
- three to the helper `_run_instanton_queue` (`:401`, whose parameter `store_handler` has no
  default, `:410`), at `:664`, `:824` and `:848`; the helper forwards it to its construction at
  `:492` (`store_handler=store_handler`, `:497`);
- one directly, to the construction at `:1092` (`:1097`).

SI's `_default_store_handler` is `obj.store()` (`RayTools/RayWorkPool.py:79-80`), and so is the
package's (`raypoolkit/RayWorkPool.py:79-80`), which is the default of `store_handler`
(`:94`). Both constructions it reaches have a compute handler, so passing it is the same as leaving
`store_handler` out. Two options, SI's to choose:
- **(a) Drop it.** `main.py:45` imports `RayWorkPool` alone; `:1097` is deleted; `_run_instanton_queue`
  stops taking `store_handler` (`:410`) and passing it (`:497`), and its three callers stop passing
  it (`:664`, `:824`, `:848`). Seven lines, and the default does the same thing.
- **(b) Keep it**, imported as `from raypoolkit.RayWorkPool import _default_store_handler`, which
  works at `v0.2.0` (the module stays reachable for a `from` import; [`README.md`](README.md) §2).
  It is private: a later release may rename or remove it without notice.

**Advice:** (a). The name is private, and what SI passes is the default.

## 4. Its call sites

**16** `RayWorkPool(...)` calls, each with two positional arguments, no `**kwargs`, and a `title`
keyword (6 a title, 10 `title=None`):

| | Calls | Spelled |
|---|---|---|
| No compute handler (`compute_handler=None`) | 12 | every one with `store_handler=None, persist_handler=None`; 10 with `validation_handler=None` as well, 2 (`plot_GradientCoupledSolutions.py:938`, `plot_InstantonSolutions.py:1171`) with every handler `None` |
| Compute handler given | 4 | `main.py:383`, `:492`, `:718`, `:1092`: each sets the compute, store, persist and validation handlers and a label builder |
| `store_results=True` | 11 | |

**Every one constructs under `v0.2.0`**, by the package's own constructor (the appendix's verdict
column). Three size expressions are not literals, at five keywords on four calls; the script
replaced each by 1 and flagged it:

| Call | Keyword | Value |
|---|---|---|
| `main.py:383` | `max_task_queue=MAX_INFLIGHT_PIPELINE_UNIFIED` (`:396`) | `MAX_INFLIGHT_PIPELINE // 3` (`:79`), so 16 |
| `main.py:492` | `max_task_queue=MAX_INFLIGHT_PIPELINE` (`:505`) | 50 (`:61`) |
| `main.py:1092` | `max_task_queue=MAX_INFLIGHT_PIPELINE` (`:1107`) | 50 |
| `main.py:718` | `create_batch_size=len(traj_payloads)`, `process_batch_size=len(traj_payloads)` (`:729-730`) | the number of models (below) |

**`main.py:729-730`.** `traj_payloads` has one entry per model in `model_list` (`:705-716`).
`v0.2.0` refuses a size below 1 at construction, so with an empty `model_list` the construction at
`:718` would raise `ValueError: create_batch_size must be at least 1, not 0`, where SI's copy
constructs and `run()` returns at once (its loop, `RayTools/RayWorkPool.py:261`, runs only while
work is in flight or to do). **By reading, SI never builds an empty `model_list` at `7bb3efd`:**
`run_all_pipelines` (`main.py:670`) is called only at `:1211`, with `inputs["model_list"]`
(`:1153`) from `build_pipeline_inputs` (`config/pipeline_setup.py:114`), whose
`build_model_list` (`config/model_list.py:5`) makes one model per sampled value, and samples at
least one: the values given, when there are any (`:20-21`, `:67-68`), or otherwise
`n = max(1, …)` values (`:23-30`, `:70-77`); any other potential type raises `ValueError`
(`:112-113`).

**Sites that must change: none at `7bb3efd`.** `main.py:729-730` must change only if SI comes to
support an empty model list. Then, SI's choice:
- `max(1, len(traj_payloads))` for both sizes: the pool constructs, and `run()` returns at once
  with nothing to do, as today (two lines);
- or refuse an empty model list before the pool, in `build_model_list` or `run_all_pipelines`.

The 12 lookup-only sites may keep `store_handler=None, persist_handler=None`, or drop both: under
`v0.2.0` a pool with no compute handler needs only `compute_handler=None`
([Which handlers a pool needs](../../README.md#which-handlers-a-pool-needs)). The choice is SI's.
**Advice:** keep them in the adoption commit, so that its diff is the imports and item 3.

## 5. What changes in behaviour

The board's issues are in [`IMPLEMENTATION_STATE.md`](../../prompts/extraction/IMPLEMENTATION_STATE.md)
§4; the package's own account is [Changes in `v0.2.0`](../../README.md#changes-in-v020), written
for a copy that is `v0.1.0`'s pool, which SI's nearly is (it differs in the rows marked here).

| Change | At SI | Issue | What SI should check |
|---|---|---|---|
| Constructor checks raise `ValueError` (decision U8) | no site affected at `7bb3efd`: all 16 construct; `main.py:729-730` with an empty `model_list` (item 4). SI's copy refused a compute handler with `persist_handler=None` (`RuntimeError`) and a persist handler with no compute handler (`RuntimeWarning`, raised) (`RayTools/RayWorkPool.py:109-117`); no tracked `.py` file outside `RayTools/` and `.prompts/` has an `except` clause for either | `[00-the-constructor-checks-its-handlers-unevenly]`, `[02-the-constructor-does-not-check-its-sizes]` | that `model_list` is still never empty (item 4) |
| A pool with no compute handler needs only `compute_handler=None` | the 12 lookup-only sites, optionally (item 4) | `[00-the-constructor-checks-its-handlers-unevenly]` | nothing |
| The post handler after a persist, with no validation handler, gets the persisted object | no site: every compute site has a validation handler, and none has a post handler | `[00-a-post-handler-after-persist-gets-the-unpersisted-object]` | nothing |
| `store_results=True` accepts a generator | accepted | `[00-store-results-sizes-from-len-of-the-task-list]` | nothing |
| In-flight work keyed on each ref's value | every site; no visible change while `ray.wait` returns the refs it was given | `[00-in-flight-work-is-keyed-on-a-bound-method]` | nothing |
| **The "available" rate computed from the available count** | changes the rate's numbers, not the line's layout: SI's copy sets `_last_num_available_complete` from the store count (`:575`), the package from the available count (`raypoolkit/RayWorkPool.py:600`). The available segment is printed only by a pool with an availability handler (copy `:191`, `:236`; package `:216`, `:261`), and **no SI site gives one** (appendix), so no line SI prints at `7bb3efd` changes | — (README §0.2, fault 6) | the progress lines of any pool given an `available_handler` after `7bb3efd` |
| A task builder's `None` under `store_results=True` | still a `RuntimeError`, now "a task builder returned None, which is not compatible with store_results=True" (`raypoolkit/RayWorkPool.py:329-333`), where SI's copy says "store_results=True is not compatible with returning None values from a task builder" (`:317-321`) | — | nothing, unless SI matches the text |
| The constructor's messages | exception text only; SI's copy already says "handler"; no SI site raises one | `[00-messages-say-maker-and-the-module-has-no-licence-header]` | nothing |

**The printed lines.** SI's copy's seven `print()` calls and its four message helpers are the
package's, by `ast`: the banner, progress and completion lines are unchanged in wording and
layout. No SI code parses them (`git grep` for "ALL WORK ITEMS COMPLETE", "work items remaining"
and "Queue summary" outside `RayTools/` finds nothing).

## 6. Its tests

**No SI test module names `RayWorkPool` or `RayTools`** (appendix), and no tracked `.py` file
outside `.prompts/` imports `main`. SI's suite (item 1) needs no change for the adoption.

## 7. The order with DatastoreKit

- **The import.** `RayTools/RayWorkPool.py:23`, `from Datastore.SQL.ShardedPool import ShardedPool`,
  is used only as the type hint of `pool` (`:90`). DatastoreKit's SI checklist at `v0.2.1` lists it
  among the imports to rewrite (`stochasticinstantons.md:105`, "a type hint", and its appendix,
  `:578`), and names `RayTools/` among SI's protected files (`:47`).
- **Decision U12** (2026-10-10): if SI adopts DatastoreKit first, it may rewrite that one line to
  `from datastorekit.SQL.ShardedPool import ShardedPool`, and nothing else in `RayTools/`; the
  `raypoolkit` adoption then deletes the file. If SI adopts `raypoolkit` first, the file is gone and
  DatastoreKit's rewrite list has one import fewer. Adopting both in one campaign is possible but not
  required ([`README.md`](README.md) §5). SI has no test that counts `RayTools/`, so no order needs
  a test edit. Either way the edit is to a file on SI's protected list, which SI's `CLAUDE.md:91-92`
  allows only when a prompt names it and says exactly what to change (item 9).
- DatastoreKit's checklist for SI: <https://github.com/ds283/DatastoreKit/blob/v0.2.1/docs/adoption/stochasticinstantons.md>.

## 8. Its acceptance

G4 holds when SI has adopted `v0.2.0`, when it is next active, in a campaign of its own, and:
1. `RayTools/` is gone: `git ls-tree <commit> RayTools` is empty.
2. **No import of `RayTools`:** `measure_client_pools.py si --commit <commit>` reports 0 imports,
   0 string literals and 0 `import_module` / `__import__` calls naming it; and no import of
   `_default_store_handler` if SI took option (a) of item 3.
3. `requirements.txt` holds the pin of item 1, and SI's venv is installed from it.
4. **SI's suite passes** (item 1).
5. **Every site constructs**: the script at the new commit gives every call the verdict
   "constructs", and finds as many calls as SI expects (16 at `7bb3efd`). Its flags on non-literal
   sizes remain; each is checked by hand, as item 4 does.
6. The gate is recorded on this repository's extraction board, §2, row G4.

## 9. What goes stale in it

- **`CLAUDE.md:89-109`, "Protected infrastructure"**, whose list names `RayTools/` (`:95`): "Never
  modify these files unless a prompt explicitly names them and describes exactly what to change"
  (`:91-92`). SI's adoption prompt must name `RayTools/` to delete it; afterwards the entry names a
  directory that is gone. Whether the list then names anything of the pool's is SI's choice.
- **`.claude/rules/`**, 17 lines in 3 files (the appendix lists each with its text):
  - `ray-dispatch.md:99-106`, "Why `RayWorkPool` requires plain classes", reads
    "`RayTools/RayWorkPool.py` accesses compute targets as plain Python objects" (`:101`) and cites
    the copy's lines 354, 436 and 393 (`:103-105`), which go with the file;
  - `datastore-factories.md:23-27`, the handler slots: `store_handler` calls `obj.store()`, then
    `persist_handler` calls `pool.object_store(obj)`, which stays true of the package's defaults;
  - the rest (`compute-targets.md:105`; `datastore-factories.md:13`, `:42`, `:113`, `:223`;
    `ray-dispatch.md:58`, `:65`, `:116`, `:214`, `:229`, `:236`, `:237`, `:245`) describe what the
    pool does with a compute target, and stay true.
- **`.documents/`**, 44 lines in 8 files:
  - `FILE_MAP.md:31`, `:287`: `RayTools/RayWorkPool.py` in the file map;
  - `INFRASTRUCTURE.md:351-373`, "`RayWorkPool` — the distributed work-queue", whose `:353` names
    `RayTools/RayWorkPool.py`; the constructor it sketches (`:357-373`) has `v0.2.0`'s keywords; and `:1`, `:4`, `:46`,
    `:128`, `:286`, `:289`, `:346`, `:411`, `:412`, `:418`, `:452`, `:478`, which stay true;
  - `architecture-summary.md:27-28` (the layout's `RayTools/`), `:319-344` (the section, `:321`
    naming the file; the constructor it sketches has `v0.2.0`'s keywords), and `:172`, `:188`, `:245`, `:349`, `:419`,
    `:482`, `:518`, `:556`, which stay true;
  - dated records: `gradient-coupled-instanton/24-prerequisite-wallclock-safeguard.md:75`, `:78`,
    `:86` (`:75`: "`RayTools/RayWorkPool.py` is protected"); `gradient-coupled-plotting/DESIGN_gradient_coupled_plotting.md:65`,
    `:336`; `gradient-coupled-plotting/PROMPT_AUTHORING_BRIEF.md:209`;
    `handoff-notes/2026-10-08/summary-E-june-pipeline.md:4`, `:20`, `:22`, `:32`, `:42`, `:48`,
    `:54`; `handoff-notes/2026-10-08/summary-F-june-science.md:15`.

  **Advice:** update `CLAUDE.md:95`, `ray-dispatch.md:99-106`, `FILE_MAP.md:31`, `:287`,
  `INFRASTRUCTURE.md:353` and `architecture-summary.md:27-28`, `:321`, which describe the code;
  leave the dated records as they are. SI's own rules for its documents govern.
- **Campaign records**: `.prompts/`, 27 lines in 8 files. They are history, and are not rewritten.

---

## Appendix: the script's output

`./venv/bin/python docs/adoption/measure_client_pools.py si`, from this repository's root at
extraction prompt 06's commit, with `raypoolkit` `0.2.0`; as printed.

# `RayWorkPool` in StochasticInstantons (SI) at `7bb3efd`

- **Repository:** `/Users/ds283/Documents/Code/StochasticInstantons`, read through `git` only.
- **Commit:** `7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7`.
- **Verdicts by:** `raypoolkit 0.2.0`, its own constructor.
- **Files:** 363 tracked; 193 `.py` files outside `RayTools/` parsed; 0 did not parse; 1 binary, not searched; 0 datastores, not read.
- **`ray.is_initialized()` after the verdicts:** False.

## `RayTools/` at the commit

| File | Blob |
|---|---|
| `RayTools/RayWorkPool.py` | `92be5b2c9e4c2c65695078bd1b8f97db2f56c7b0` |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |

## Totals

| Measure | Count |
|---|---|
| Imports of a `RayTools` module | 3 (module level 3, nested 0) |
| … naming a private name | 1 |
| String literals naming `RayTools` | 0 |
| `import_module` / `__import__` calls naming `RayTools` | 0 |
| `RayWorkPool(...)` calls | 16 |
| … no compute handler (`compute_handler=None`) | 12 |
| … compute handler given | 4 |
| … compute handler left at its default | 0 |
| … `store_results=True` | 11 |
| … with a `title` keyword | 16 (`title=None` 10, set 6) |
| … positional arguments | 2 at 16 |
| … with `*args` / `**kwargs` | 0 / 0 |
| Verdicts | `constructs` 16 |
| Calls with a flag / flags | 4 / 5 |
| Lines of non-`.py` files naming `RayTools` or `RayWorkPool` | 89 |
| Test modules naming `RayTools` or `RayWorkPool` | 0 |

## The handler keywords, by spelling

Each handler keyword as absent (—), `None` or set; a row per spelling, with its calls.

| `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` | Calls |
|---|---|---|---|---|---|---|---|
| None | None | None | None | None | None | None | 2 |
| None | None | None | — | None | — | — | 10 |
| set | set | set | — | set | — | set | 4 |

## Imports of a `RayTools` module (3)

| File:line | Scope | Statement | Private names |
|---|---|---|---|
| `main.py:45` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool, _default_store_handler` | `_default_store_handler` |
| `plot_GradientCoupledSolutions.py:100` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `plot_InstantonSolutions.py:72` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |

## String literals naming `RayTools` (0)

None.

## `import_module` / `__import__` calls naming `RayTools` (0)

None.

## `RayWorkPool(...)` calls (16)

Each call at the line of its name. Handlers: absent (—), `None` or set. Sizes: the source text of each size keyword given. `results`: `store_results`. Verdict: `v0.2.0`'s constructor, given the classes.

| File:line | Scope | Pos. | `**` | compute | store | persist | available | validation | post | label | Sizes | `results` | Title | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `main.py:221` | `_run_pipeline_queue` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:249` | `_run_pipeline_queue` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:316` | `_run_pipeline_queue` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:383` | `_run_pipeline_queue` | 2 | — | set | set | set | — | set | — | set | `create_batch_size=5`, `process_batch_size=3`, `max_task_queue=MAX_INFLIGHT_PIPELINE_UNIFIED` **flagged** | False | set | `constructs` |
| `main.py:445` | `_run_instanton_queue` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:492` | `_run_instanton_queue` | 2 | — | set | set | set | — | set | — | set | `create_batch_size=5`, `process_batch_size=3`, `max_task_queue=MAX_INFLIGHT_PIPELINE` **flagged** | False | set | `constructs` |
| `main.py:589` | `_run_gradient_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:718` | `run_all_pipelines` | 2 | — | set | set | set | — | set | — | set | `create_batch_size=len(traj_payloads)` **flagged**, `process_batch_size=len(traj_payloads)` **flagged** | True | set | `constructs` |
| `main.py:871` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:900` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:964` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1015` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1041` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1092` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | set | set | set | — | set | — | set | `create_batch_size=5`, `process_batch_size=3`, `max_task_queue=MAX_INFLIGHT_PIPELINE` **flagged** | False | set | `constructs` |
| `plot_GradientCoupledSolutions.py:938` | `run_plots` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `plot_InstantonSolutions.py:1171` | `run_plots` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |

## Calls with a compute path: the handlers given (4)

The source text of each handler keyword given, at each call whose compute handler is given or left at its default.

| File:line | `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` |
|---|---|---|---|---|---|---|---|
| `main.py:383` | `lambda obj, **kw: obj.compute(**kw)` | `pipeline_store_handler` | `pipeline_persist_handler` | — | `lambda obj: pool.object_validate(obj)` | — | `lambda obj: f"Pipeline(dNstar={float(obj.delta_Nstar):.4g})"` |
| `main.py:492` | `lambda obj, **kwargs: obj.compute(**kwargs)` | `store_handler` | `persist_handler` | — | `lambda obj: pool.object_validate(obj)` | — | `label_builder` |
| `main.py:718` | `lambda obj, **kwargs: obj.compute(**kwargs)` | `inflaton_trajectory_store_handler` | `lambda obj, pool: pool.object_store(obj)` | — | `lambda obj: pool.object_validate(obj)` | — | `lambda obj: "InflatonTrajectory"` |
| `main.py:1092` | `lambda obj, **kwargs: obj.compute(**kwargs)` | `_default_store_handler` | `lambda obj, pool: pool.object_store(obj)` | — | `lambda obj: pool.object_validate(obj)` | — | `lambda obj: ( f"CompactionFunction(dNstar={float(obj.delta_Nstar):.4g})" )` |

## Flags (5, on 4 calls)

| Call | Keyword line | Flag |
|---|---|---|
| `main.py:383` | `:396` | `max_task_queue=MAX_INFLIGHT_PIPELINE_UNIFIED is not a literal; replaced by 1` |
| `main.py:492` | `:505` | `max_task_queue=MAX_INFLIGHT_PIPELINE is not a literal; replaced by 1` |
| `main.py:718` | `:729` | `create_batch_size=len(traj_payloads) is not a literal; replaced by 1` |
| `main.py:718` | `:730` | `process_batch_size=len(traj_payloads) is not a literal; replaced by 1` |
| `main.py:1092` | `:1107` | `max_task_queue=MAX_INFLIGHT_PIPELINE is not a literal; replaced by 1` |

## Notification keywords, by source text (2 calls; never passed)

| File:line | Keywords |
|---|---|
| `plot_GradientCoupledSolutions.py:938` | `notify_batch_size=50`, `notify_time_interval=120` |
| `plot_InstantonSolutions.py:1171` | `notify_batch_size=50`, `notify_time_interval=120` |

## Non-`.py` files naming `RayTools` or `RayWorkPool` (89 lines)

| Top directory | Lines | Files |
|---|---|---|
| `.claude/` | 17 | 3 |
| `.documents/` | 44 | 8 |
| `.prompts/` | 27 | 8 |
| `CLAUDE.md` | 1 | 1 |

Each line outside the campaign records (`prompts/`, `.prompts/`), 62:

```text
.claude/rules/compute-targets.md:105: logging. `RayWorkPool` supplies it via `label_builder` if one is configured.
.claude/rules/datastore-factories.md:13: This is the most important rule in this file. Violating it causes `RayWorkPool`
.claude/rules/datastore-factories.md:23: Note: `RayWorkPool` has three distinct handler slots — `store_handler` (calls
.claude/rules/datastore-factories.md:42: # Not found — return UNPOPULATED object; RayWorkPool will call compute()
.claude/rules/datastore-factories.md:113: guaranteed by the `store_handler` step in `RayWorkPool`, which runs before
.claude/rules/datastore-factories.md:223: and `validated = True`. This flag is used by `RayWorkPool` for the initial
.claude/rules/ray-dispatch.md:58: """Must return an ObjectRef. RayWorkPool waits on this."""
.claude/rules/ray-dispatch.md:65: """Called on the DRIVER by RayWorkPool after compute() resolves.
.claude/rules/ray-dispatch.md:99: ## Why `RayWorkPool` requires plain classes
.claude/rules/ray-dispatch.md:101: `RayTools/RayWorkPool.py` accesses compute targets as plain Python objects:
.claude/rules/ray-dispatch.md:106: return an `ObjectRef`; `RayWorkPool` never calls `.remote()` on it
.claude/rules/ray-dispatch.md:116: class Foo(DatastoreObject):          # NEVER — breaks RayWorkPool
.claude/rules/ray-dispatch.md:214: The custom handler must be wired in explicitly at the `RayWorkPool` call site
.claude/rules/ray-dispatch.md:229: O(grid_size). Run this inside a `RayWorkPool` with large batch sizes
.claude/rules/ray-dispatch.md:236: Feed only the missing items into a second `RayWorkPool` with a conservative
.claude/rules/ray-dispatch.md:237: `max_task_queue` (e.g. 20). `RayWorkPool`'s main loop guards task creation
.claude/rules/ray-dispatch.md:245: `RayWorkPool`. This overlaps queries with compute, but has two drawbacks that
.documents/FILE_MAP.md:31: | `RayTools_RayWorkPool.py` | `RayTools/RayWorkPool.py` | `RayWorkPool` class: the core distributed work-queue abstraction; manages the **lookup → compute → store → persist → validate** state machine over a list of compute targets using `ray.wait()`; provides `create_batch_size`, `process_batch_size`, `max_task_queue` controls |
.documents/FILE_MAP.md:287: | `RayTools/` (other files)                               | Only `RayWorkPool.py` is directly relevant                                  |
.documents/INFRASTRUCTURE.md:1: # INFRASTRUCTURE — how `Datastore`, `ShardedPool`, and `RayWorkPool` work
.documents/INFRASTRUCTURE.md:4: (`Datastore`) and distributed dispatch (`RayWorkPool`). It does not cover the
.documents/INFRASTRUCTURE.md:46: `RayWorkPool` uses to decide whether a grid point needs computing at all.
.documents/INFRASTRUCTURE.md:128: is exactly the signal `RayWorkPool` needs to decide computation is required.
.documents/INFRASTRUCTURE.md:286: **Why `Foo` must stay a plain class:** `RayWorkPool` accesses compute targets
.documents/INFRASTRUCTURE.md:289: *return* an `ObjectRef` rather than `RayWorkPool` calling `.remote()` on
.documents/INFRASTRUCTURE.md:346: handler is wired explicitly at the `RayWorkPool` call site — never hidden
.documents/INFRASTRUCTURE.md:351: ## 9. `RayWorkPool` — the distributed work-queue
.documents/INFRASTRUCTURE.md:353: `RayTools/RayWorkPool.py` drives every compute stage through five states:
.documents/INFRASTRUCTURE.md:357: RayWorkPool(
.documents/INFRASTRUCTURE.md:411: `RayWorkPool`, with a conservative `max_task_queue` (e.g. 20). Because
.documents/INFRASTRUCTURE.md:412: `RayWorkPool`'s own loop already caps in-flight tasks, no separate manual
.documents/INFRASTRUCTURE.md:418: `RayWorkPool`. That approach overlaps queries with compute but has two
.documents/INFRASTRUCTURE.md:452: MISS path, inside RayWorkPool:
.documents/INFRASTRUCTURE.md:478: RayWorkPool over compute_list:
.documents/architecture-summary.md:27: RayTools/
.documents/architecture-summary.md:28: RayWorkPool.py               — distributed work-queue abstraction
.documents/architecture-summary.md:172: persisted. `RayWorkPool` reads this property directly.
.documents/architecture-summary.md:188: which signals to `RayWorkPool` that computation is needed.
.documents/architecture-summary.md:245: **Why `Foo` must be a plain class:** `RayWorkPool` accesses compute targets as
.documents/architecture-summary.md:319: ## RayWorkPool
.documents/architecture-summary.md:321: `RayTools/RayWorkPool.py` provides the main distributed work-queue abstraction.
.documents/architecture-summary.md:328: RayWorkPool(
.documents/architecture-summary.md:349: `RayWorkPool.run()` drives a state machine over all in-flight `ObjectRef`s:
.documents/architecture-summary.md:419: One `RayWorkPool` runs over all `(model, phi0, pi0, potential)` combinations.
.documents/architecture-summary.md:482: RayWorkPool(
.documents/architecture-summary.md:518: MISS path in RayWorkPool:
.documents/architecture-summary.md:556: RayWorkPool:
.documents/gradient-coupled-instanton/24-prerequisite-wallclock-safeguard.md:75: the Ray dispatch layer, and `RayTools/RayWorkPool.py` is protected
.documents/gradient-coupled-instanton/24-prerequisite-wallclock-safeguard.md:78: through the *real* `main.py`/`RayWorkPool` pipeline (per the prompt's own
.documents/gradient-coupled-instanton/24-prerequisite-wallclock-safeguard.md:86: driver that bypasses `RayWorkPool` and dispatches
.documents/gradient-coupled-plotting/DESIGN_gradient_coupled_plotting.md:65: dispatch.py          # RayWorkPool wiring, generic _render_item wrapper,
.documents/gradient-coupled-plotting/DESIGN_gradient_coupled_plotting.md:336: the terminal `RayWorkPool(..., store_results=False)` drain stay exactly as they
.documents/gradient-coupled-plotting/PROMPT_AUTHORING_BRIEF.md:209: `RayWorkPool(..., store_results=False)` drain must be preserved exactly.
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:4: `2026-06-14_Codebase-evaluation-and-refactoring-strategy.md`, `2026-06-16_Inflaton-trajectory-sampling-and-database-storage-strategy.md`, `2026-06-16_InflatonTrajectory-validation-failure-diagnosis.md`, `2026-06-16_Refactoring-plotting-scripts-for-RayWorkPool-integration.md`, `2026-06-16_Converting-instanton-trajectories-to-primordial-black-hole-d.md`, `2026-06-21_Enhancing-instanton-solution-plot-styling-and-metadata.md`, `2026-06-21_Radial-density-profile-and-compaction-function-analysis.md`, `2026-06-22_Ray-failure-mode-identification.md`, `2026-06-22_DOE-meaning-in-project-context.md`.
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:20: **14 Jun 20:46.** David's brief (reproduced verbatim as `.prompts/base-implementation/01-initial.md`): reuse ChamPBH's three layers — `RayWorkPool`, `Datastore`/`ShardedPool`, the lookup–compute–store "unit of work"; single-field scope but "build the code in such a way that the extensions of multiple field models is considered from the beginning"; no slow-roll approximation, state `(φ, π=dφ/dN)` doubled by MSR response fields `P₁, P₂`; the compaction-function pipeline sketch (end-of-inflation surface fixes `k_end`; at each step "only the core region continues on the instanton; the outer region detaches"). **Recorded** (01-initial.md).
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:22: **14 Jun 20:47 — Claude's keep/drop evaluation.** Keep: `RayWorkPool`, `ShardedPool`/`Datastore`/`SerialPoolBroker`, `DatastoreObject`, Dimensionless/Dimensionful quantities and factories, `tolerance`/`version`/`store_tag`, `IntegrationSupervisor`/`RHS_timer`, `phi_value`/`pi_value`. Drop: `ConformalCouplings/`, `QCD_Cosmology`, chameleon `StateVector`/`ODEPolicy`, `ScalarModel*`, `AdiabaticHistory`, `BBNData`, `redshift`/`temperature` as time coordinate (replaced by `efold_value`/`efold_array`). Also flagged: `main.py` bug `allowed_drop_actions` undefined (neutralised by hollowing out `main.py`). **Recorded** only at the level of the resulting layout (architecture-summary "Repository layout", CLAUDE.md protected list); the keep/drop *reasoning* and the ChamPBH→instanton correspondence table (e.g. `CompactionFunction` "analogous to `AdiabaticHistory`", `PBHMassFunction` "analogous to `BBNData`") are **NOT recorded**.
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:32: **15 Jun 11:26–12:25 — the `@ray.remote`-on-classes incident.** Claude Code had decorated `InflatonTrajectory` as a Ray actor and used `Foo.__ray_actor_class__(...)` in the factory; David asked why, since `ScalarModel` in ChamPBH was never an actor. Diagnosis: `RayWorkPool` reads `obj.available`, calls `obj.store()` on the driver, and expects `compute()` to return an `ObjectRef`; corrective Prompt 3.5. **Recorded** fully (ray-dispatch.md, datastore-factories.md, CLAUDE.md rule 1).
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:42: ### 16 June — sampling strategy, `RayWorkPool` handlers, time convention
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:48: **16 Jun 10:15–10:29 — backpressure.** Claude's draft left `main.py` driving Ray manually; David: `RayWorkPool` "is supposed to be the abstraction for work queue management. We don't want to submit all tasks to Ray simultaneously otherwise it gets overwhelmed"; a lookup queue then a work queue, as in ChamPBH. David also refused to defer the custom store handler ("The whole point of this refactoring is that `InflatonTrajectory` needs to mint the `efold_value` objects"). **Recorded** (two-pass dispatch in ray-dispatch.md and INFRASTRUCTURE §10, with the grouper-batch comparison).
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:54: **16 Jun 11:39–11:58 — plotting refactor.** `plot_InstantonSolutions.py` must go through `RayWorkPool` "to prevent the machine on which the plotting code is running from being overwhelmed"; `read_table` on sharded tables is forbidden (reads one shard); fetch per-item via `object_get` keyed by `delta_Nstar`; `read_table_config` extended by David to `delta_Nstar`, `efold_value`, `inflaton_mass`, `quartic_coupling`, `phi_value`, `pi_value`. **Recorded** (pool-read-apis.md).
.documents/handoff-notes/2026-10-08/summary-F-june-science.md:15: *Design decisions (all recorded).* Step-1 N_final-decoupling test; Sobol/LHC in (δN★, ΔN) with coarse N_final; GP regressor on the signed distance C̄_max − 0.4 rather than a classifier; scalars-only storage; Sobol indices on the surrogate. David rejected weighting-down extrapolated points: the extrapolation "is done using an exact analytic formula and should be reliable". David proposed the unified single-`RayWorkPool` pipeline (prompts 6–8) after noticing the two-pass architecture made `set_store_full_values(False)` unsafe. David set the integrity rule: a recompute whose scalars disagree with a stored row "is an integrity failure and shouldn't happen ... we would raise an exception" (`PIPELINE_SCALAR_INTEGRITY_RTOL = 1e-4`). Footer provenance `[summary-only]` added after David could not tell the two smoke-test runs apart. Output: prompts 01–10 and `handoff-sparse-sampling.md`.
CLAUDE.md:95: RayTools/                          Datastore/SQL/ShardedPool.py
```

## Test modules naming `RayTools` or `RayWorkPool` (0)

None.

## Files that do not parse (0)

None.
