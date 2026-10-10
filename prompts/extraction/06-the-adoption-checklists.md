# Prompt 06 — the adoption checklists

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 05 landed (`eaef0ce`), its review is recorded (`9a00f80`), and **`v0.2.0`** is tagged on
  `eaef0ce` after green CI (run `38075908457`); the release is recorded (`b2b6ab4`), whose CI run
  `38076190172` also passed.
- `git status` is clean in this repository, and the suite gives `Ran 121 tests … OK`.
- U10 and U12 are taken (README §6.2).

**Closes:** nothing. **Narrows:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The code is one measuring script. The weight is in three documents that another repository's
  campaign will act on, each fact of which has to be true of a client at a named commit and of the
  package at `v0.2.0`, cited by `path:line`, and measured, not inferred.
- Two of the facts below change what a client must do and were found only by reading its code
  (SI's private import, SI's batch sizes from `len()`); the agent has to look for more of the same.

**Read first:**

1. [`README.md`](README.md): §0.2 (the clients, the call sites, the inherited faults), §1, §2
   (rows 05–07), §3, §4, §5 (rules 5, 6, 9) and §6.2 (U5, U8, U10, U12), and §7 (G2–G4).
2. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`, above all "What this repository is" and
   "A client's change is not made here".
3. The board: §1's review of 05 and *Release of `v0.2.0`*; §4 (every resolved issue, since each
   fault's fix is a behaviour a client meets on adoption).
4. The package as tagged: `README.md` ("Changes in `v0.2.0`", "Which handlers a pool needs", "The
   printed lines are part of the interface"), `PROVENANCE.md`, and `raypoolkit/RayWorkPool.py`
   (the constructor, `:88-215`).
5. The precedent, DatastoreKit's checklists, read **only** through
   `git -C /Users/ds283/Documents/Code/DatastoreKit show v0.2.1:<path>`: `docs/adoption/README.md`
   and `docs/adoption/secondarygwkit.md` for the form; and the `RayTools/` rows of all three
   checklists, which U12 answers. Do not copy their content; their client facts are about the
   datastore layer, not the pool.

Facts below are at this repository's `b2b6ab4` and at the client commits named in §0, measured
read-only on 2026-10-10.

---

## 0. The clients, as measured

Each client was read through `git ls-tree` and `git show` at its commit, never from its working
tree, by a planner's script that parsed each tracked `.py` file with `ast`. None was imported,
run or edited.

| Client | Repository | Commit (branch) | Tree | `RayTools/RayWorkPool.py` | Python (`venv/pyvenv.cfg`) | Ray (`requirements.txt`) |
|---|---|---|---|---|---|---|
| SGK | `SecondaryGWKit/` | `b510bc9` (`handover-remedial`) | clean | blob `b4666fa`, last changed `0ee16a8` | 3.12.15 | `ray==2.43.0` |
| CPBH | `ChamPBH/` | `52142d7` (`main`) | **23 uncommitted changes**, not read | blob `aaa6dc9`, last changed `79fb527` | 3.13.16 | `ray==2.53.0` |
| SI | `StochasticInstantons/` | `7bb3efd` (`main`) | clean | blob `92be5b2`, last changed `7cf4123` | `version_info = 3.13.13` (the version at creation; its interpreter is MacPorts' 3.13) | `ray==2.55.1` |

Each commit is each client's `HEAD`, unchanged since the plan was written (README §0.2), and is
the commit DatastoreKit's checklists were measured at. All three are inside the declared range
(`>=3.12`, `ray>=2.43`); SGK equals the low tested end, SI the high; CPBH's Ray lies between the
ends.

### 0.1 Imports of `RayTools`

Outside `RayTools/` itself, every import is `from RayTools.RayWorkPool import …`, at module level:

| Client | Sites |
|---|---|
| SGK (7) | `main.py:63`; `extract_GkSource_data.py:37`, `extract_GkWKB_data.py:35`, `extract_Gk_data.py:32`, `extract_QuadSourceIntegral_data.py:42`, `extract_TkWKB_data.py:30`, `extract_tensor_source_data.py:31` |
| CPBH (3) | `main.py:50`, `plot_ScalarModel.py:44`, `plot_by_beta.py:38` |
| SI (3) | `main.py:45` (`RayWorkPool, _default_store_handler`), `plot_GradientCoupledSolutions.py:100`, `plot_InstantonSolutions.py:72` |

String literals naming `RayTools` in `.py` files: **SGK 8** (six in
`Datastore/tests/test_layer_is_generic.py`, one in `docs/tolerance-convergence/inventory.py:382`,
one in an archived measurement script under `prompts/`); CPBH 0; SI 0.

### 0.2 The call sites, under `v0.2.0`

Every `RayWorkPool(...)` call (`ast.Call` whose function is the name or attribute `RayWorkPool`),
with each handler keyword classed as absent, the literal `None`, or set:

| | SGK | CPBH | SI |
|---|---|---|---|
| Sites | 54 | 17 | 16 |
| No compute handler (`compute_handler=None`) | 44 | 14 | 12 |
| … spelled | `store_handler=None, persist_handler=None` (44) | `store_handler=None` only (14) | `store_handler=None, persist_handler=None` (12) |
| Compute handler given | 6 | 3 | 4 |
| Compute handler left at its default | 4 (`main.py:1042`, `:1057`, `:1940`, `:4146`) | 0 | 0 |
| `store_results=True` | 39 | 13 | 11 |
| Titled | 54 | 17 | 16 |
| Positional arguments | 2 at every site | 2 | 2 |
| `**kwargs` | none | none | none |

- **Every site constructs under `v0.2.0`**, as 04 measured (README §6.2, U8): no site with no
  compute handler gives a store handler, persist handler, validation handler or label builder that
  is not `None`, and no site with one gives `store_handler=None` or `persist_handler=None`.
- **Sizes.** Every literal size is at least 1. SI has three that are not literals:
  `max_task_queue=MAX_INFLIGHT_PIPELINE_UNIFIED` (`main.py:396`; `MAX_INFLIGHT_PIPELINE // 3`,
  `:79`, so 16), `max_task_queue=MAX_INFLIGHT_PIPELINE` (`:505`, `:1107`; 50, `:61`), and
  **`create_batch_size=len(traj_payloads)`, `process_batch_size=len(traj_payloads)`**
  (`main.py:729-730`), where `traj_payloads` has one entry per model in `model_list` (`:705-716`).
  With an empty `model_list`, SI's copy constructs and `run()` returns at once (its loop,
  `RayTools/RayWorkPool.py:261`, runs while anything is in flight or to do); **`v0.2.0` raises
  `ValueError` at construction** ("create_batch_size must be at least 1, not 0").
- **CPBH and U10.** No CPBH site passes a callable `store_handler`: 14 pass `None`, 3 leave it out.
  CPBH's copy calls `obj.store()` unconditionally and then its `store_handler(obj, pool)`, whose
  default is `pool.object_store(obj)`; `v0.2.0`'s defaults are `obj.store()` (store) then
  `pool.object_store(obj)` (persist). So at its 3 compute sites (`main.py:276`, `:533`, `:820`)
  the package does what CPBH's copy does, and at its 14 lookup-only sites `store_handler=None` is
  accepted and the default persist handler does not apply. U10 (no shim) changes no CPBH site at
  `52142d7`.
- **SI and `_default_store_handler`.** SI imports the private name (`main.py:45`) and passes it
  as `store_handler` four times: to its helper `_run_instanton_queue` (`:401`) at `main.py:664`,
  `:824` and `:848`, which forwards it to the call at `:492` (`store_handler=store_handler`,
  `:497`), and directly to the call at `:1092` (`:1097`). SI's `_default_store_handler` is
  `obj.store()` (`RayTools/RayWorkPool.py:79-80`), as is the package's. Under `v0.2.0` the name
  still imports as `from raypoolkit.RayWorkPool import _default_store_handler` (U4's note: the
  submodule stays reachable by a `from` import), but it is private; passing it is the same as
  leaving `store_handler` out.

### 0.3 What changes in behaviour on adoption

From the board's §4 and the diff of each copy against `v0.2.0`, the printing and message lines
only: every client's copy prints the same banner, progress and completion lines as `v0.2.0`, in
wording and layout. What a client meets:

| Change | SGK | CPBH | SI |
|---|---|---|---|
| Constructor checks raise `ValueError` (U8) | yes; no site affected | yes; no site affected | yes; `main.py:729-730` with an empty `model_list` |
| A pool with no compute handler needs only `compute_handler=None` | yes | yes | yes |
| Post handler after a persist with no validation gets the persisted object (fault 2) | `main.py:3247` (compute handler, `validation_handler=None`, a post handler) | no site (every compute site has a validation handler) | no site (likewise) |
| `store_results=True` with a generator (fault 3) | accepted | accepted | accepted |
| In-flight work keyed on the ref's value (fault 1) | yes | yes | yes |
| The "available" rate computed from the available count, not the store count (README §0.2, fault 6) | already so | **changes**: the rate's numbers, not the line's layout | **changes**, likewise |
| CPBH's `store_handler` meaning "persist" (U10) | — | its 14 `store_handler=None` keep their effect; no callable to rename | — |

No client but SGK parses what the pool prints (`git grep` for "ALL WORK ITEMS COMPLETE", "work
items remaining" and "Queue summary" outside `RayTools/` finds nothing in CPBH or SI).

### 0.4 Tests that depend on the pool

- **SGK.**
  - `RunRegistry/tests/test_pipeline_adoption.py`: six lines "in the vocabulary `RayWorkPool`
    prints" (`:32-44`), parsed by SGK's `StageTracker` through three patterns (README §0.2's
    note). The lines are unchanged in `v0.2.0` (U9; 04 and 05 changed no printed line). Its
    comment cites `RayTools/RayWorkPool.py` line numbers (`:166`, `:548`, `:566`), which go stale.
  - Three `ComputeTargets/tests/` modules find pool constructions by `ast.Call` with
    `func.id == "RayWorkPool"` (`test_main_plumbing.py:449`, `:736`;
    `test_quadsource_policy_main.py:145`; `test_wkb_numeric_parent_main.py:86`, `:120`), and two
    compile one function of `main.py` and bind the name `RayWorkPool` to a stand-in
    (`test_gksource_parent_set_main.py:262-290`, `test_quadsource_integral_parent_main.py:790`).
    None executes `main.py`'s import line. Each needs only that the call stays spelled
    `RayWorkPool(...)`, which `from raypoolkit import RayWorkPool` keeps.
  - **`Datastore/tests/test_layer_is_generic.py` counts `RayTools/` as part of the datastore
    layer**: `layer_files()` globs `RayTools/*.py` (`:70-71`); `AUDIT_LIST` names
    `RayTools/RayWorkPool.py` (`:88`) and `test_the_derived_files_hold_the_audits_list` (`:303-304`)
    asserts every listed file exists; `_NOT_PROJECT_PACKAGES` (`:120`), `import_allowed`
    (`:192-193`) and `test_the_allow_list` (`:357`) name `RayTools`. Deleting `RayTools/` fails at
    least `:303-304`. DatastoreKit's SGK checklist retires this module when SGK adopts DatastoreKit,
    so whether SGK edits it depends on the order (U12).
- **CPBH, SI.** No test names `RayWorkPool` or `RayTools`.

### 0.5 What goes stale

Tracked files other than `.py` that name `RayTools` or `RayWorkPool` (lines):

| Client | Total | By top directory | Of note |
|---|---|---|---|
| SGK | 196 | `prompts/` 156, `docs/` 39, `CLAUDE.md` 1 | **`CLAUDE.md:70-73`** says "The `RayTools/` files are not frozen either", which U5 contradicts; SGK was never told of U5 (`PROVENANCE.md`, "The freeze": "Prompt 01 does not edit any client to announce it") |
| CPBH | 43 | `.documents/` 22, `prompts/` 21 | `.documents/architecture-summary.md` describes `RayTools/` (`:35-36`, `:153`) and the old `store_handler` (`:585`, `:648`) |
| SI | 89 | `.documents/` 44, `.prompts/` 27, `.claude/` 17, `CLAUDE.md` 1 | **`CLAUDE.md:89-95`**, "Protected infrastructure", lists `RayTools/`; `.claude/rules/datastore-factories.md:23` and `.claude/rules/ray-dispatch.md:101` describe the handler slots and `RayTools/RayWorkPool.py` |

Campaign records (`prompts/`, `.prompts/`) and dated verification documents are history: a
checklist lists them by count, and says they are not rewritten.

### 0.6 The order with DatastoreKit (U12)

DatastoreKit's checklists (at `v0.2.1`) list each copy's `from Datastore.SQL.ShardedPool import
ShardedPool` as an import to rewrite: SGK `RayTools/RayWorkPool.py:8`, CPBH and SI `:23`. It is
used only as the type hint of the constructor's `pool` (SGK `:75`, CPBH `:86`, SI `:90`). U5
freezes `RayTools/` until a client adopts `raypoolkit`. **U12, taken 2026-10-10:** a client that
adopts DatastoreKit before `raypoolkit` may rewrite that one import to
`from datastorekit.SQL.ShardedPool import ShardedPool`, and nothing else in `RayTools/`; the
change is a type hint's and alters no behaviour. So any order is possible:

| Order | What `RayTools/` sees | SGK's `test_layer_is_generic.py` |
|---|---|---|
| `raypoolkit` first | deleted; DatastoreKit's later rewrite list has one import fewer | edited by the `raypoolkit` adoption to drop its `RayTools` entries (§0.4), then retired by DatastoreKit's |
| DatastoreKit first | the one import rewritten (U12), then deleted by the `raypoolkit` adoption | retired by DatastoreKit's adoption; nothing for `raypoolkit`'s |
| Both in one campaign | deleted; the import never rewritten | retired |

---

## 1. What is wanted

06 writes **`docs/adoption/`**: one checklist per client, a README holding what the three share,
and the script that measures them. After it, each client's own adoption campaign, in its own
repository, can be planned from its checklist (README §7, G2–G4) without reading this campaign.

- **A checklist is data, not instructions.** It describes the client at one commit; the client's
  campaign measures again before acting, and its numbers govern. A choice that is the client's is
  named with what each option touches, and not made; a recommendation is marked **Advice:**.
- **Every fact carries a `path:line`** at the client's commit (named once at the head of the
  checklist), or at `v0.2.0` (`eaef0ce`) for a line under `raypoolkit/`, or comes from the
  script, whose Markdown output is each checklist's appendix.
- **No behaviour of the package changes.** No file under `raypoolkit/` is touched; the suite stays
  at **121**.
- **No client is edited, imported or run**, and DatastoreKit is read only through `git show
  v0.2.1:<path>` (README §5 rule 5; `CLAUDE.md`).

---

## 2. What to write

### 2.1 `docs/adoption/measure_client_pools.py`

```bash
./venv/bin/python docs/adoption/measure_client_pools.py sgk  [--commit SHA] [--json]
./venv/bin/python docs/adoption/measure_client_pools.py cpbh [--commit SHA] [--json]
./venv/bin/python docs/adoption/measure_client_pools.py si   [--commit SHA] [--json]
```

- **Reads** the client at `/Users/ds283/Documents/Code/<repository>` through `git ls-tree -r` and
  `git show <commit>:<path>` only, never its working tree; the default commit is §0's. Parses each
  tracked `.py` file outside `RayTools/` with `ast`.
- **Reports:**
  1. every import of a `RayTools` module, at module level or nested (with the enclosing function
     or class), with file, line and names; any name imported that begins with `_`, flagged;
  2. string literals that name `RayTools`, and `importlib.import_module` / `__import__` calls that
     do;
  3. every `RayWorkPool(...)` call: file and line; positional count; `**kwargs`; each of the seven
     handler keywords (`compute_handler`, `store_handler`, `persist_handler`, `available_handler`,
     `validation_handler`, `post_handler`, `label_builder`) as absent, `None` or set; each size
     keyword's source text; `store_results`; `title`;
  4. **for each call, `v0.2.0`'s verdict, from the package's own constructor**, not from a
     restatement of its rule: build the call's keywords with `None` for `None`, a distinct
     callable for "set", left out for absent, each literal size evaluated with
     `ast.literal_eval` and a non-literal one replaced by 1 and flagged; construct
     `raypoolkit.RayWorkPool` with a stand-in pool, an empty `task_list` and a trivial
     `task_builder` (construction calls no Ray); record "constructs" or the exception's type and
     message. The verdict is only as good as the classes: say so in the docstring;
  5. tracked files other than `.py` naming `RayTools` or `RayWorkPool`, counted by top directory,
     with each line outside the campaign-record directories (`prompts/`, `.prompts/`) listed;
  6. the client's test modules (`test_*.py`, `*_test.py`, or under a `tests/` directory) that name
     `RayWorkPool` or `RayTools`, with the lines.
- **Output:** Markdown by default (the checklists' appendices), JSON with `--json`. Sorted, so two
  runs at one commit give the same bytes. Exits 0 on success and 2 when it cannot read the client
  or the commit.
- **Imports** only the standard library and `raypoolkit`. It names the clients, as
  `docs/extraction/compare_with_source.py` names SGK; nothing under `raypoolkit/` does (`CLAUDE.md`).
  It is not a test, is not collected by the suite, and does not run in CI. `black` clean (CI checks
  `docs/`).

**Its figures must equal §0's**, or the log says which differs and why: imports SGK 7, CPBH 3,
SI 3; sites 54, 17, 16 with §0.2's splits; every verdict "constructs", with SI's three non-literal
sizes flagged; text mentions 196, 43, 89. A difference in the agent's favour (a site the planner
missed) is recorded and the checklists use the script's figure; a site that does **not** construct
is a stop (§5).

### 2.2 `docs/adoption/README.md`

What the three share, in DatastoreKit's form but not its content:
- **Head:** written by extraction prompt 06, against `v0.2.0` (`eaef0ce`); the clients read through
  `git` only, at the commits named; a checklist is data, not instructions.
- **The table** of the three checklists, each with its client commit and its gate (README §7).
- **§1 The release and the pin**: `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0`;
  the editable-install warning; the declared range, the two tested ends, and each client's Python
  and Ray against them (§0's table); each client keeps its own Ray pin.
- **§2 The module map**: `RayTools.RayWorkPool` → `raypoolkit` (`from raypoolkit import
  RayWorkPool`); the module stays reachable as `raypoolkit.RayWorkPool` for a `from` import of a
  module-level name (U4's note), and every name in it other than `RayWorkPool` and
  `DatastorePool` is private; `RayTools/__init__.py` has no counterpart. The pool's type hint is
  `raypoolkit.DatastorePool`, a `Protocol` a client's `ShardedPool` satisfies by having
  `object_store`; `raypoolkit` does not depend on `datastorekit` (U3).
- **§3 What changes for a caller**: point at the package README's "Changes in `v0.2.0`" and "Which
  handlers a pool needs"; do not restate them beyond one line each.
- **§4 What does not change**: the printed lines (U9), with the package README's section linked.
- **§5 The order with DatastoreKit**: §0.6's table, and U12 in one sentence with its date; that
  adopting both in one campaign is possible but not required; DatastoreKit's checklists are at its
  `v0.2.1`, linked by URL on GitHub, not by path.
- **§6 How a checklist is used**: measured at the named commit and re-measured by the client;
  a client's adoption is one campaign in its own repository; the pin moves in a commit of its own;
  the U5 freeze ends for a client when its adoption lands; a defect the client finds in the package
  is reported and fixed here, in a release.
- **§7 Re-measuring**: the script's commands, what it reports, and its figures at the checklists'
  commits.
- The checklist items, by number and name (§2.3).

### 2.3 The three checklists

`docs/adoption/secondarygwkit.md`, `docs/adoption/champbh.md`, `docs/adoption/stochasticinstantons.md`.
Each opens with the client, its repository path, its commit (full SHA, branch, date and subject),
and the state of its tree (CPBH: the 23 uncommitted changes were not read; the checklist describes
`52142d7`). Each then has the **same nine items, in the same order and under the same names**:

1. **The client and its versions**: Python and Ray against `v0.2.0`'s range and tested ends;
   the pin line it adds to `requirements.txt`.
2. **What it deletes**: `RayTools/RayWorkPool.py` and `RayTools/__init__.py`, with their blobs.
3. **Which imports it rewrites**: every import of §0.1, each with its replacement. SI's
   `_default_store_handler`: the two options (drop the import and the four keywords, since they
   pass the default; or import the private name from `raypoolkit.RayWorkPool`), with **Advice:**
   to drop it.
4. **Its call sites**: the count and split of §0.2; each site's verdict from the script; a list of
   the sites that must change, with why (for CPBH and SGK, none at the commit; for SI,
   `main.py:729-730` if an empty `model_list` is a run SI supports, with the options:
   `max(1, len(traj_payloads))`, or refusing an empty model list before the pool). Say what U10
   means for CPBH: no shim, and a callable `store_handler` added before adoption must become
   `persist_handler`.
5. **What changes in behaviour**: the client's column of §0.3, each row with its site and its
   board issue (the board's §4), and what the client should check. For SGK, `main.py:3247`
   (`postprocess_GkSourcePolicy`, README §0.2's fault 2): the handler now receives the persisted
   object; the checklist says what the handler reads (read it at the commit) and whether that
   changes anything. For CPBH and SI, the "available" rate's numbers.
6. **Its tests**: §0.4 for the client; for SGK, what `test_layer_is_generic.py` needs in each
   order of §0.6, by line.
7. **The order with DatastoreKit**: §0.6 for the client, with the `RayTools/` import's line, and a
   link to that client's DatastoreKit checklist at `v0.2.1` (by GitHub URL).
8. **Its acceptance**: what shows the adoption landed: `RayTools/` gone; no import of `RayTools`
   (the script at the client's new commit reports 0); the pin in `requirements.txt`; the client's
   own suites pass (SGK: including `test_pipeline_adoption.py` and the `ComputeTargets/tests`
   modules of §0.4); every site constructs; the gate of README §7 recorded on this board.
9. **What goes stale in it**: §0.5 for the client, each line outside its campaign records listed
   by `path:line` with what it says; the campaign records by count, not rewritten. For SGK,
   `CLAUDE.md:70-73` and the `RayTools` line numbers in `test_pipeline_adoption.py`'s comment.

Then the appendix: the script's Markdown output for that client, as printed.

**Check every statement.** Each `path:line` is read at the client's commit and quoted in the log
with what it says; each statement about the package is checked against `v0.2.0` (its README, a
test, or the module); each "constructs" is the script's.

---

## 3. Verification

1. **The suite**, from the repository root in `venv/`: `Ran 121 tests … OK`, before and after.
2. **The script**: each client run twice at its commit, the outputs byte-identical (`cmp`); exit 0;
   `--commit 0000000` (or any SHA the client lacks) exits 2; `--json` parses with `json.loads`.
3. **A fixture repository**, made in the scratchpad with `git init` and one commit, holding: a
   module-level and a nested `from RayTools.RayWorkPool import RayWorkPool, _private`; an
   `import_module("RayTools.RayWorkPool")`; a lookup-only call with both `None`s; a call with
   `compute_handler=None, label_builder=f`; a call with a compute handler and
   `store_handler=None`; a call with `create_batch_size=0`; a call with `max_task_queue=N`; a test
   module naming `RayWorkPool`; a Markdown file naming `RayTools`. The script, pointed at it by a
   path override used only for this check, must report each, with the verdicts `constructs`,
   `ValueError` (label builder), `ValueError` (store handler), `ValueError` (size) and
   `constructs` (flagged). How the override works is the agent's choice; the log says.
4. **The clients are untouched.** Before and after, for each client: `git -C <client> rev-parse
   HEAD`, `git -C <client> status --porcelain | shasum`, and `git -C <client> stash list | wc -l`;
   each equal. No client's `venv/` is used.
5. `./venv/bin/black --check raypoolkit docs` (25.1.0) is clean.
6. **Links**: every relative link in `docs/adoption/` resolves to a tracked file; every external
   link is to `github.com/ds283/…` at a named tag.
7. **The breakage record.** Each item is a diff against the committed script, exactly as applied,
   with what failed; none committed; the tree restored after each (02's driver pattern: the
   SHA-256 of each changed file and `git status --porcelain`):
   - **(a)** the verdict computed by a restated rule that forgets `label_builder`: the fixture's
     label-builder call reports "constructs";
   - **(b)** nested imports not walked (module level only): the fixture's nested import is
     missed;
   - **(c)** the working tree read in place of `git show`: an uncommitted edit in the fixture
     changes the output (make one, then remove it);
   - **(d)** the sort removed: two runs at one commit may differ, or the output changes order
     against the committed run (show which).

---

## 4. Acceptance

1. `docs/adoption/` holds the README, the three checklists and the script, as §2 says, and nothing
   else.
2. The script's figures equal §0's, or each difference is explained in the log; every site
   constructs.
3. Every `path:line` in the checklists was read at its commit, and every package statement checked
   against `v0.2.0`.
4. §3 passes; (a)–(d) fail as §3.7 says.
5. **The records**, in the same commit:
   - the log, `logs/06-the-adoption-checklists.md`, per README §5.1. It also has:
     - each client's commit, tree state and the untouched-check of §3.4, before and after;
     - the script's output for each client, whole, and its two-run `cmp`;
     - the fixture's output;
     - every `path:line` the checklists cite, with the text read there;
     - every statement about the package, with how it was checked;
     - (a)–(d);
     - the test count before and after (121, 121);
   - the board: the header; §1's row for 06 (landed, "this commit", 121 → 121); and §2's gates
     G2–G4 each pointing at its checklist;
   - `docs/OPEN_ISSUES.md`, only if an issue is opened;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- A site that does **not** construct under `v0.2.0` by the script's verdict (§0.2 and 04 say all
  87 do).
- A client's `RayTools/RayWorkPool.py` at its commit is not §0's blob, or a client's `HEAD` has
  moved and the agent cannot tell whether to measure the old commit or the new.
- A statement a checklist must make is not true of `v0.2.0`, or could be made true only by
  changing a file under `raypoolkit/`.
- The suite fails, or its count differs from 121.
- Anything would edit, run, import or open a store of SecondaryGWKit, ChamPBH, StochasticInstantons
  or DatastoreKit, or read one other than through `git`; use a client's `venv/` other than to read
  `pyvenv.cfg` as text; or touch a client's working tree, index or stash.
- Anything would push, tag, or write to GitHub.
- Passing anything would need a change to a file not in §6.

---

## 6. What this prompt does not do

- **Files it adds or changes:**
  - `docs/adoption/README.md`, `secondarygwkit.md`, `champbh.md`, `stochasticinstantons.md`,
    `measure_client_pools.py` (new);
  - the log, this board, `prompts/INDEX.md`, and `docs/OPEN_ISSUES.md` if an issue is opened.
- It changes nothing else: no file under `raypoolkit/`, `docs/extraction/` or `.github/`; not
  `README.md`, `PROVENANCE.md`, `pyproject.toml`, `CLAUDE.md`, `LICENSE`, `.gitignore` or the
  campaign README.
- It edits no client and no DatastoreKit file, and does not tell a client of U5 or U12: the
  checklists carry both, and each client learns of them when it plans its adoption.
- It makes no tag and pushes nothing.
- It writes no orchestration note.

---

## 7. The log and the board

`logs/06-the-adoption-checklists.md`, using README §5.1, with the additions of §4.5.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 06 (landed, commit, log, suite), §2's gates.
