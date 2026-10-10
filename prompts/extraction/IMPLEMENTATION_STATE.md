# extraction campaign — implementation state

**Last updated:** 2026-10-10 · **Status: IN PROGRESS — 2 of 7 prompts written (01, 02), 01 landed
(`49f3ddf`) and reviewed.** G1 holds at SGK `b510bc9`, the import commit. The user took U1–U3 at set-up and
U4–U5 for 01 and U6 and U9 for 02, all on 2026-10-10 and as recommended (README §6.2; U9 as
amended at 02's writing). The package `raypoolkit` exists;
`compare_with_source.py` exits 0; the suite is 3 tests. The U5 freeze is in force.

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
| **U4** module name | keep `RayWorkPool.py`; re-export the class from the root | **taken** 2026-10-10 |
| **U5** freeze | no client edits its `RayTools/` until it adopts | **taken** 2026-10-10; in force from 01's commit |
| **U6** Ray stand-in | real `ObjectRef(bytes)`; `ray.wait` / `ray.get` replaced in-process | **taken** 2026-10-10 |
| **U7** versions | Python ≥3.12, Ray ≥2.43; tested 3.12.15/2.43.0 and 3.13.16/2.55.1 | open, for 03 |
| **U8** handler checks | defaults apply only with a compute handler (option b) | open, for 04 |
| **U9** printed lines | pinned, wording and layout, against a scripted clock; the three consumer patterns checked | **taken** 2026-10-10, as amended |
| **U10** CPBH shim | none | open, for 06 |

## 1. Prompts

| # | Prompt | Status | Commit | Suite |
|---|---|---|---|---|
| 01 | [`01-import-the-pool.md`](01-import-the-pool.md) | **landed** 2026-10-10 ([log](logs/01-import-the-pool.md)), reviewed | `49f3ddf` | 0 → 3 |
| 02 | [`02-the-test-suite.md`](02-the-test-suite.md) | **written** 2026-10-10 | — | 3 → N |
| 03 | `03-supported-versions-and-ci.md` | not written | — | — |
| 04 | `04-fix-the-inherited-faults.md` | not written | — | — |
| 05 | `05-release-v0.2.0.md` | not written | — | — |
| 06 | `06-the-adoption-checklists.md` | not written | — | — |
| 07 | `07-verification-and-close-out.md` | not written | — | — |

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`310db6e`),
used for 01.

**Orchestrator review of prompt 01 (2026-10-10).** Dispatched from `310db6e` to one Opus
subagent, with the note's §0 facts, its one addition (breakage (h)) and its two recommendations.
Reviewed against its commit `49f3ddf`, with nothing landed after it. **Every check of the note's
§3 passed**, and acceptance 1–3 are met. No stop condition fired.

*At dispatch.* The note's gate held at `310db6e`. The tree was clean, the only worktree was this
checkout, and `raypoolkit` was not installed in `venv/`. SGK's `HEAD` was `b510bc9`, with
`RayTools/RayWorkPool.py` at blob `b4666fa`. No Ray process was up.

*The checks.*
1. **Scope.** `49f3ddf` touches 13 files: the prompt's §6 list (`pyproject.toml`, the six files
   under `raypoolkit/`, `compare_with_source.py`, `PROVENANCE.md`), the log, this board,
   `prompts/INDEX.md` and the index. No `venv/`, `*.egg-info` or scratch file.
2. **E1, the files.** `git ls-files raypoolkit` gives exactly `__init__.py`, `RayWorkPool.py`,
   `_timing.py`, `contract.py`, `tests/__init__.py` and `tests/test_package_imports.py`.
   `__init__.py` binds the two names and `__all__`, and nothing else. `contract.py` imports only
   `typing` and `ray`, is not `runtime_checkable`, and names no client or `datastorekit` class.
3. **E2, by running.** The check exits 0: 572 identical lines, 2 D-imp and 1 D-pool in
   `RayWorkPool.py`; 4 D-int definitions and the byte-for-byte span in `_timing.py`; 4 declared
   files; 0 undeclared. The counts equal the log's.
4. **E2, by reading.** The script was read in full. The blob is checked first. D-imp is an exact
   two-entry `ast` map of whole `ImportFrom` statements, with no alias. D-pool is the one
   identifier on a line that parses as a lone annotated parameter with no default. There is no
   D-fmt rule and no line number in any rule. Only equal-length `replace` runs are classified, so
   additions and deletions never are. D-int compares `ast` segments, the body's names in order, the
   span byte for byte, and only blank lines between docstring and span.
5. **E3, the check bites.** (a)–(h) were replayed from the log in `bash`. Each exits 1 and names
   the line or file, as logged. The orchestrator's own: SGK's `WallclockTimer` (`utilities.py:6-17`,
   with its two imports) appended to `_timing.py` fails on BODY and SPAN. `git status` was clean
   after each.
6. **E4, the guard.** `Ran 3 tests … OK`. Test 1 uses `ast.walk` over every module under
   `raypoolkit/`, tests included, resolves relative imports, and names file, line and module. Tests
   2 and 3 run `sys.executable -I` from a `tempfile` directory, with a 300 s timeout. Test 3's
   docstring states the patching rule.
7. **E5, isolation.** From the scratchpad, with `env -u PYTHONPATH` and `-I`, the prompt's §3.1
   import succeeds and leaves `ray.is_initialized()` false; `import RayTools` and
   `import datastorekit` each fail with `ModuleNotFoundError`.
8. **E6, the pins.** The `numpy` diff fails test 1 alone; the re-export removal fails tests 2 and
   3; the class-only variant fails test 3 alone. The `datastorekit` diff in `contract.py` stops
   discovery at load (`ERROR: raypoolkit.tests`), since the package imports `contract`. Run as a
   script, the module fails all three, test 1 naming `raypoolkit/contract.py:9`. That is the log's
   account (deviation 6, STRUCTURALLY REQUIRED). The suite is 3 again after each.
9. **E7, the records.** The log has every section of README §5.1, `pip freeze` (Python 3.12.15,
   `ray==2.43.0`, `black==25.1.0`, the editable `raypoolkit`), the check's whole output, the counts
   0 → 3, and the five faults' package lines. `PROVENANCE.md` has the six items of the prompt's
   §2.8, with both subject lines right. The index counts 6 rows, matching its header.
   `black --check raypoolkit docs` (25.1.0) is clean.

*Findings.*
- **One issue opened by the agent, and kept:** `[01-a-kept-comment-names-the-datastore-service]`
  (`RayWorkPool.py:424`). The note expected none; the agent's reading of `CLAUDE.md` is right, and
  the comment is SGK's text, which rule 8 keeps until 04.
- **A correction to the note.** Its §0 put fault 2's post-handler call at `:489`; that is the
  `elif`, and the call is at `:490` (the log, and §3 below, are right). README §0.2's and §3's
  "SGK `:488-491`" is the same span read one line short; the board's **Package** line, `:487-492`,
  supersedes it.
- **Put to the user, not acted on:** `CLAUDE.md` says the package names no client module "in code,
  strings, docstrings or comments", but two mentions inside `raypoolkit/` are required by the
  prompt: `_timing.py`'s docstring names SGK's `utilities.py` (D-int), and the guard's
  `FORBIDDEN_ROOTS` names `Datastore`, `RayTools` and `utilities` (§2.7 test 2). Whether
  `CLAUDE.md` excepts provenance and guard text, or 04 rewords them, is the user's decision.
  **Taken 2026-10-10, at 02's writing:** `CLAUDE.md` excepts both; nothing is opened.

*Residue fixed in the follow-up commit.* "this commit" → `49f3ddf` on this board, in the log and
in `prompts/INDEX.md`; README §2's status and header for 01; this review and the notes line.

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1** | **holds** 2026-10-10, re-checked at 01's writing and again at its start: SGK `RayTools/RayWorkPool.py` is blob `b4666fa` at `b510bc9`, the import commit |
| **G2** | not yet (SGK adopts `v0.2.0`) |
| **G3** | not yet (CPBH adopts `v0.2.0`) |
| **G4** | not yet (SI adopts `v0.2.0`) |

## 3. Active and unresolved issues

The five `[00-…]` entries are inherited from the source and were opened at planning (README
§0.2, faults 1–5). Each is pinned as it behaves by 02 and fixed by 04 (README §2). Since 01, each
gives the **Package** lines where its fault sits in `raypoolkit/RayWorkPool.py`, read from the
package (log 01 §3.6); they equal SGK's at `b510bc9`, because 01 replaced lines one for one.

### `[00-in-flight-work-is-keyed-on-a-bound-method]`

**Opened:** 2026-10-10, at planning. **Owner:** 04.

**Package (01):** 26 lines keyed on `.hex`, `raypoolkit/RayWorkPool.py:260, 263, 266, 277, 322,
337, 338, 351, 352, 379, 381, 389, 390, 403, 409, 410, 434, 435, 444, 445, 467, 468, 479, 480, 505,
506`.

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

**Package (01):** `raypoolkit/RayWorkPool.py:487-492`: the `elif self._post_handler is not None:`
at `:489`, the call `self._post_handler(obj)` at `:490`.

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

**Package (01):** `raypoolkit/RayWorkPool.py:138`.

With `store_results=True` the constructor sizes `results` from `len(task_list)` (SGK `:138`),
though it has already consumed `task_list` into `self._todo` and counted it. A generator or other
iterable without `len()` raises `TypeError`.

*Impact.* None known at a client: no client run is known to have raised it, but the planner did
not trace every `task_list` argument to its type (06 does). The constructor otherwise accepts any
iterable.

*Next step.* 04 sizes from `self._num_total_items`, with a test that passes a generator.

### `[00-the-constructor-checks-its-handlers-unevenly]`

**Opened:** 2026-10-10, at planning. **Owner:** 04, under U8.

**Package (01):** the `RuntimeWarning` check at `raypoolkit/RayWorkPool.py:99-102` (raised at
`:100`); the store handler, never checked, is called at `:431`.

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

**Package (01):** "maker" at `raypoolkit/RayWorkPool.py:96` and `:101`; no licence header (`:1` is
`import time`).

The constructor's two messages say "compute maker" and "persist maker" for the handlers, and SGK's
module carries no licence header (CPBH's and SI's copies carry the Apache 2.0 header, and SI's
messages say "handler").

*Impact.* Cosmetic. The messages are not part of the printed-lines interface (`CLAUDE.md`); they
are exception text.

*Next step.* 04 rewrites the two messages and adds the header the repository's licence calls for.

### `[01-a-kept-comment-names-the-datastore-service]`

**Opened:** 2026-10-10, by 01 (log 01 §5.1). **Owner:** 04.

**Package (01):** `raypoolkit/RayWorkPool.py:424`, a comment kept from SGK as it is (01 §2.4):
"…and then submit a store request to the Datastore service". `Datastore` is the name of SGK's
datastore package and class. `CLAUDE.md` says the package names no client class, module or package
in its comments. The module's other mentions (`:430`, `:451`, `:502`, `:574`) say "datastore" in
lower case, generically.

*Impact.* None on behaviour: it is a comment. It breaks a stated invariant of the package's text.

*Next step.* 04, which rewrites the module's wording for
`[00-messages-say-maker-and-the-module-has-no-licence-header]`, rewords the comment generically
("the datastore"). The printed lines are not affected.

## 4. Resolved issues

None.
