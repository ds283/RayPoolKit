# Log — extraction prompt 04: fix the inherited faults

**Subject:** Fix the five inherited faults and check the constructor's sizes · **Commit:** this
commit · **Date:** 2026-10-10 · **Agent:** Claude Opus 5.5

**Result: landed.** Faults 1–5 are fixed in `raypoolkit/RayWorkPool.py`, with the size checks of
`[02-the-constructor-does-not-check-its-sizes]` and the comment of
`[01-a-kept-comment-names-the-datastore-service]`. All four package modules carry U11's licence
header, byte for byte from SI's copy. 02's five fault pins are inverted into guards, and five
tests are added. The suite goes from **116 to 121**, passing at 3.12.15 / 2.43.0 (`venv/`) and
3.13.16 / 2.55.1 (a fresh `uv` venv), with no Ray process of this repository's before or after
any run. Every printed-line test of 02 passes unchanged, except for §3.4's `HANDLER_SETS` edit.
(r1)–(r10) each fail at least the planner's tests. On `v0.1.0`'s module, every one of the 17 new
or changed tests fails. `compare_with_source.py` was run once, before any change (exit 0, 02's
counts), and then retired. **Seven issues are closed and none opened**, so the index goes from 8
to **1**. No tag was made, nothing was pushed, and `pyproject.toml`, `README.md` and
`PROVENANCE.md` are unchanged.

**Gate, re-checked at start.** `HEAD` was `a7d9252` (the orchestration note; the prompt was
written at `c207238`), the tree clean, the only worktree this checkout, `git tag` only `v0.1.0`,
`origin/main` at `6b1ddfe`. `git diff v0.1.0 -- raypoolkit` was empty. `venv/`: Python 3.12.15,
`ray` 2.43.0, `black` 25.1.0, `raypoolkit` `0.1.0` editable. `Ran 116 tests … OK`. The check
exited 0 (§3.3). `black --check raypoolkit docs`: 15 files unchanged. Every scratch file, driver,
diff, output and venv of this log is under the agent's scratch directory
(`…/scratchpad/agent04/`), written `$S` below.

## 1. What shipped

| File | What |
|---|---|
| `raypoolkit/RayWorkPool.py` | the header; the rewritten constructor checks and the size checks (U8, §2.4–§2.5); `range(self._num_total_items)` (fault 3); the 26 keys on `.hex()` (fault 1); `self._post_handler(replacement_obj)` (fault 2); "the datastore" in the kept comment. The whole diff against `v0.1.0` is §1.2 |
| `raypoolkit/_timing.py`, `raypoolkit/__init__.py` | the header and one blank line, prepended; nothing else |
| `raypoolkit/contract.py` | the header; the docstring's "or who passes ``persist_handler=None``" → "or whose pool has no compute handler, and so uses neither default" (§2.7) |
| `raypoolkit/tests/test_inherited_faults.py` | the five pins renamed and inverted (§3.1), and the header test; the module docstring |
| `raypoolkit/tests/test_construction.py` | C1 and C2 renamed and inverted; C5, C6 and C7 added; the message templates; the module docstring (§3.2) |
| `raypoolkit/tests/test_run_paths.py` | S4 and X1 (§3.3) |
| `raypoolkit/tests/test_printed_lines.py` | `HANDLER_SETS` loses "validation only" and gains two lookup-only spellings; the spelling test (§3.4) |
| `raypoolkit/tests/test_standins.py` | the one comment at `:116` (§2.7); the assertion stays |
| `docs/extraction/compare_with_source.py` | one paragraph at the top of the docstring (§2.8); nothing else |
| this log, the board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md` | the records |

No file was added under `raypoolkit/`. `raypoolkit.egg-info/` (gitignored) was rewritten by the
high-end editable install at 18:04 and is not staged.

### 1.1 The closed issues, the lines that fix them, and their guards

Line numbers are the new module's (the header moves every line by 15, the checks by 25 more).

| Issue | Fixed at | Guarded by |
|---|---|---|
| `[00-in-flight-work-is-keyed-on-a-bound-method]` | the 26 keys, `RayWorkPool.py:300, 303, 306, 317, 362, 377, 378, 391, 392, 419, 421, 429, 430, 443, 449, 450, 474, 475, 484, 485, 507, 508, 519, 520, 545, 546`, each `.hex()` | `test_inherited_faults.TestInheritedFaults.test_fresh_refs_from_wait_complete_every_path`; also X1 (`test_run_paths.TestUnexpectedItemType.test_an_unexpected_item_type_raises`), now seeded under `ref.hex()` only |
| `[00-a-post-handler-after-persist-gets-the-unpersisted-object]` | `:530`, `replacement_obj = self._post_handler(replacement_obj)` | `test_the_post_handler_after_persist_gets_the_persisted_object`; S4 (`test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`) |
| `[00-store-results-sizes-from-len-of-the-task-list]` | `:178`, `range(self._num_total_items)` | `test_store_results_accepts_a_generator_task_list` |
| `[00-the-constructor-checks-its-handlers-unevenly]` | `:109-134`: the two resolutions by identity (`:110-113`), the no-compute loop over four arguments (`:115-124`), the compute branch's loop over two (`:126-134`) | `test_a_lookup_only_pool_needs_no_persist_handler`, `test_store_handler_none_with_compute_is_refused_at_construction`; C1, C2, C5, C6 (`test_construction.TestHandlerChecks`); `test_printed_lines`' spelling test and `HANDLER_SETS`' two new cases |
| `[00-messages-say-maker-and-the-module-has-no-licence-header]` | the three messages at `:123`, `:133` and `:142`, none saying "maker"; the header at `:1-15` of `RayWorkPool.py`, `_timing.py`, `contract.py` and `__init__.py` | the message assertions of C1, C2, C5, C7 and the fault-4b guard; `test_every_package_module_carries_the_licence_header` |
| `[01-a-kept-comment-names-the-datastore-service]` | `:464`, "…submit a store request to the datastore." | none (a comment); `git grep -n "Datastore service" raypoolkit` is empty |
| `[02-the-constructor-does-not-check-its-sizes]` | `:136-142`, each size below 1 raises `ValueError` | C7 (`test_construction.TestSizeChecks.test_a_size_below_one_raises_value_error`) |

The comment at `:480` ("a compute handler was supplied, so a persist handler must have been also")
is unchanged, and now enforced (§2.7).

`inspect.signature(RayWorkPool)` is unchanged: the parameters' names, kinds, annotations and
defaults (the three default handlers by name) equal `v0.1.0`'s, compared in scratch with
`v0.1.0`'s module loaded from `git show`.

### 1.2 The diff of `raypoolkit/RayWorkPool.py` against `v0.1.0`, whole

`git diff v0.1.0 -- raypoolkit/RayWorkPool.py` (78 insertions, 38 deletions):

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
index e949de6..d5e1669 100644
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -1,3 +1,18 @@
+# (c) University of Sussex 2026
+# Created by David Seery
+#
+# Licensed under the Apache License, Version 2.0 (the "License");
+# you may not use this file except in compliance with the License.
+# You may obtain a copy of the License at
+#
+#    http://www.apache.org/licenses/LICENSE-2.0
+#
+# Unless required by applicable law or agreed to in writing, software
+# distributed under the License is distributed on an "AS IS" BASIS,
+# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+# See the License for the specific language governing permissions and
+# limitations under the License.
+
 import time
 from datetime import datetime
 from typing import Optional
@@ -91,15 +106,40 @@ class RayWorkPool:
         title: str = None,
         store_results: bool = False,
     ):
-        if compute_handler is not None and persist_handler is None:
-            raise RuntimeError(
-                "If a compute maker is supplied, a persist maker must also be supplied to serialize the result of the computation"
-            )
-
-        if compute_handler is None and persist_handler is not None:
-            raise RuntimeWarning(
-                "No compute maker was supplied, but a persist maker was provided. This will have no effect because there will be no compute results to store"
-            )
+        if compute_handler is None:
+            if store_handler is _default_store_handler:
+                store_handler = None
+            if persist_handler is _default_persist_handler:
+                persist_handler = None
+
+            for name, value in (
+                ("store_handler", store_handler),
+                ("persist_handler", persist_handler),
+                ("validation_handler", validation_handler),
+                ("label_builder", label_builder),
+            ):
+                if value is not None:
+                    raise ValueError(
+                        f"No compute handler was supplied, so {name} would never be called; leave it out, or pass None"
+                    )
+
+        else:
+            for name, value in (
+                ("store_handler", store_handler),
+                ("persist_handler", persist_handler),
+            ):
+                if value is None:
+                    raise ValueError(
+                        f"A compute handler was supplied, so {name} must not be None; leave it out to use the default"
+                    )
+
+        for name, value in (
+            ("create_batch_size", create_batch_size),
+            ("process_batch_size", process_batch_size),
+            ("max_task_queue", max_task_queue),
+        ):
+            if value < 1:
+                raise ValueError(f"{name} must be at least 1, not {value!r}")
 
         self._pool = pool
 
@@ -135,7 +175,7 @@ class RayWorkPool:
 
         self._store_results = store_results
         if store_results:
-            self.results = [None for _ in range(len(task_list))]
+            self.results = [None for _ in range(self._num_total_items)]
             self._current_idx = 0
 
         self._num_lookup_queue = 0
@@ -257,13 +297,13 @@ class RayWorkPool:
                     ref_data = self._task_builder(item)
 
                     def store_single_ref(ref, allow_store=True):
-                        self._inflight[ref.hex] = ref
+                        self._inflight[ref.hex()] = ref
 
                         if self._store_results and allow_store:
-                            self._data[ref.hex] = ("lookup", self._current_idx)
+                            self._data[ref.hex()] = ("lookup", self._current_idx)
                             self._current_idx += 1
                         else:
-                            self._data[ref.hex] = ("lookup", None)
+                            self._data[ref.hex()] = ("lookup", None)
 
                         self._num_lookup_queue += 1
 
@@ -274,7 +314,7 @@ class RayWorkPool:
                             store_single_ref(ref, allow_store=allow_store)
 
                             if "compute_payload" in ref_data:
-                                self._compute_data[ref.hex] = ref_data[
+                                self._compute_data[ref.hex()] = ref_data[
                                     "compute_payload"
                                 ]
 
@@ -319,7 +359,7 @@ class RayWorkPool:
 
             for ref in done_refs:
                 ref: ObjectRef
-                item_type, payload = self._data[ref.hex]
+                item_type, payload = self._data[ref.hex()]
 
                 if item_type == "lookup":
                     # payload is an index into the result set
@@ -334,8 +374,8 @@ class RayWorkPool:
                         self.results[idx] = obj
 
                     # remove the original 'lookup' task from the work queue
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_lookup_queue = max(self._num_lookup_queue - 1, 0)
                     self._num_lookup_complete += 1
@@ -348,8 +388,8 @@ class RayWorkPool:
                                 available_task: ObjectRef = self._available_handler(obj)
 
                                 # add this task to the work queue
-                                self._inflight[available_task.hex] = available_task
-                                self._data[available_task.hex] = (
+                                self._inflight[available_task.hex()] = available_task
+                                self._data[available_task.hex()] = (
                                     "available",
                                     (idx, obj),
                                 )
@@ -376,9 +416,9 @@ class RayWorkPool:
                                     {"label": label} if label is not None else {}
                                 )
 
-                                if ref.hex in self._compute_data:
+                                if ref.hex() in self._compute_data:
                                     compute_args.update(
-                                        {"payload": self._compute_data[ref.hex]}
+                                        {"payload": self._compute_data[ref.hex()]}
                                     )
 
                                 compute_task: ObjectRef = self._compute_handler(
@@ -386,8 +426,8 @@ class RayWorkPool:
                                 )
 
                                 # add this compute task to the work queue
-                                self._inflight[compute_task.hex] = compute_task
-                                self._data[compute_task.hex] = ("compute", (idx, obj))
+                                self._inflight[compute_task.hex()] = compute_task
+                                self._data[compute_task.hex()] = ("compute", (idx, obj))
 
                                 self._num_compute_queue += 1
 
@@ -400,14 +440,14 @@ class RayWorkPool:
                             if replacement_obj is not None and self._store_results:
                                 self.results[idx] = replacement_obj
 
-                    self._compute_data.pop(ref.hex, None)
+                    self._compute_data.pop(ref.hex(), None)
 
                 elif item_type == "available":
                     # payload is a pair of the target index and the constructed object
                     idx, obj = payload
 
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_available_queue = max(self._num_available_queue - 1, 0)
                     self._num_available_complete += 1
@@ -421,7 +461,7 @@ class RayWorkPool:
 
                 elif item_type == "compute":
                     # payload contains an index into the result set and (our local copy of) the object that has finished computation;
-                    # we want it to store the result of the computation internally, and then submit a store request to the Datastore service.
+                    # we want it to store the result of the computation internally, and then submit a store request to the datastore.
                     # the results will then be serialized into the database
                     idx, obj = payload
 
@@ -431,8 +471,8 @@ class RayWorkPool:
                     self._store_handler(obj, self._pool)
 
                     # remove the original 'compute' task from the work queue
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_compute_queue = max(self._num_compute_queue - 1, 0)
                     self._num_compute_complete += 1
@@ -441,8 +481,8 @@ class RayWorkPool:
                     store_task: ObjectRef = self._persist_handler(obj, self._pool)
 
                     # add this store task to the work queue
-                    self._inflight[store_task.hex] = store_task
-                    self._data[store_task.hex] = ("store", payload)
+                    self._inflight[store_task.hex()] = store_task
+                    self._data[store_task.hex()] = ("store", payload)
 
                     self._num_store_queue += 1
 
@@ -464,8 +504,8 @@ class RayWorkPool:
                         self.results[idx] = replacement_obj
 
                     # remove the original 'store' task from the work queue
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_store_queue = max(self._num_store_queue - 1, 0)
                     self._num_store_complete += 1
@@ -476,8 +516,8 @@ class RayWorkPool:
                             replacement_obj
                         )
 
-                        self._inflight[validation_task.hex] = validation_task
-                        self._data[validation_task.hex] = (
+                        self._inflight[validation_task.hex()] = validation_task
+                        self._data[validation_task.hex()] = (
                             "validate",
                             (idx, replacement_obj),
                         )
@@ -487,7 +527,7 @@ class RayWorkPool:
                     # otherwise, this is the exit point for driver flow associated with this task, so apply the
                     # postprocessing task, if one was supplied
                     elif self._post_handler is not None:
-                        replacement_obj = self._post_handler(obj)
+                        replacement_obj = self._post_handler(replacement_obj)
                         if replacement_obj is not None and self._store_results:
                             self.results[idx] = replacement_obj
 
@@ -502,8 +542,8 @@ class RayWorkPool:
                             f"!! WARNING: {type(obj).__name__} object with store_id={obj.store_id} did not validate after being emplaced in the datastore"
                         )
 
-                    self._inflight.pop(ref.hex, None)
-                    self._data.pop(ref.hex, None)
+                    self._inflight.pop(ref.hex(), None)
+                    self._data.pop(ref.hex(), None)
 
                     self._num_validation_queue = max(self._num_validation_queue - 1, 0)
                     self._num_validation_complete += 1
```

## 2. Deviations from the prompt

The orchestrator's brief added eight clarifications and additions (1–8 below). Each is an
**IMPLEMENTATION CHOICE at the orchestrator's direction**.

1. **"Tree restored" is measured, not `git status` clean** (clarification 1). Before each breakage
   item and the §4.5 run, the driver recorded the SHA-256 of the ten files this work changes and
   `git status --porcelain --untracked-files=all`; after the revert both were compared, byte for
   byte, with what they were. Each item below says "tree restored: yes".
2. **§4.5 restored the fixed module from a scratch copy, never through git** (clarification 2).
   The fixed `RayWorkPool.py` (SHA-256 `8f4c1d7d…8ce919`) was copied to `$S/v010-run2/`,
   `v0.1.0`'s was written over it with `git show`, the suite ran, and the copy was put back with
   `cp -p`; its SHA-256 and the whole snapshot were then compared (§4.11). The breakage diffs were
   reverted with `git apply -R` only. No `git checkout`, `git restore` or `git stash` was run.
3. **The planner's expected failures are a floor** (clarification 3). §4 lists what actually
   failed. (r4) fails 51 tests (80 failing entries, counting subtests); (r1) and (r5) also fail
   more than the planner listed, each explained there. No item failed nothing.
4. **The spelling test sets `self.clock.reading = 0` before each run** (clarification 4), one
   `subTest` per spelling, so that all three print the nine lines of
   `test_a_lookup_only_run_notifying_on_every_pass` exactly. The stand-in's public attribute is set;
   `standins.py` is unchanged and no seam of the pool is added.
5. **The flips, as re-measured** (clarification 5): this agent's first run of the unchanged suite
   on the fixed module gave the same eleven (§3.2). The checks are one loop over `(name, value)`
   pairs per branch, then the sizes' loop, as the prompt and the clarification word them.
6. **The "before" count at the high end is from an export** (clarification 6): a `git archive
   v0.1.0` export at `$S/export-v010`, run with the high venv from that directory, so that its
   `raypoolkit` is the export's (checked: `raypoolkit.__file__` is the export's). Every other run
   is from the repository root and tests the working tree.
7. **The high end was made as 03 made it** (clarification 7): `uv venv -p
   /opt/local/bin/python3.13 $S/venv-high`, then `uv pip install --python $S/venv-high/bin/python -e
   /Users/ds283/Documents/Code/RayPoolKit "ray==2.55.1"`, one resolve (18 packages), with `uv`'s
   cache. It rewrote the gitignored `raypoolkit.egg-info/`; nothing is staged from it, and no wheel
   was built. `venv/` was not reinstalled.
8. **The header was taken through `git show` and prepended by a script** (clarification 8): `git
   -C …/StochasticInstantons show 7bb3efd:RayTools/RayWorkPool.py | head -14`, compared with
   CPBH's (`git -C …/ChamPBH show 52142d7:…`) by `cmp` (identical, lines 1–15 alike, line 15
   blank in both); SHA-256 of the 14 lines `e73e93340148903e1dc2ffdba80b9870faeee548ea4275ab89f488d9c42e1ab9`,
   as the prompt says. The script prepended those bytes and one `"\n"` to each module, after
   asserting none already began with `# (c)`. `_timing.py` and `contract.py` keep their
   docstrings as their module docstrings (checked through `__doc__`). The test's constant is the 15
   lines; it equals SI's lines 1–15 byte for byte, its first 14 lines hash to `e73e9334…e1ab9`, and
   the 15 lines to `c638d0ef051a50a9fa3c048d4e72d904328a8aed86094d3b3253b08e2b4f2000`.

Choices of this prompt's agent:

9. **C7 is in a new class, `TestSizeChecks`**; C5 and C6 are in `TestHandlerChecks`, beside C1 and
   C2. The prompt places the new tests in the module, not in a class. **IMPLEMENTATION CHOICE.**
10. **The fresh-refs guard runs two items on each path**, so that every dictionary holds more than
    one key when a lookup is made, and gives each `subTest` a fresh `StandinDatastorePool`, so that
    the compute paths' `store_id`s are 1001 and 1002 in each. It asserts each run's own `results`
    (name, `available`, `store_id`) and its printed lines (none, untitled), never the shared log.
    The `Blob` path is a fifth `subTest`, outside the loop, since its `results` have no
    `available`. **IMPLEMENTATION CHOICE.**
11. **The fault-3 guard passes `persist_handler=None` explicitly**, as 02's pin did, so that on
    `v0.1.0`'s module it fails for fault 3 (`TypeError` from `len(task_list)`), not for fault 4.
    It uses three items. **IMPLEMENTATION CHOICE.**
12. **The fault-4a guard reads the queued message after construction, then runs the pool** and
    checks its one `wait` call: "constructs and runs", as the prompt asks. **IMPLEMENTATION
    CHOICE.**
13. **`raised_by` is gone from `test_inherited_faults.py`**, with the unused `Work` import: no
    guard needs the raising line. The fault-4b guard uses `assertRaises` and checks
    `type(...) is ValueError` and the message whole. **IMPLEMENTATION CHOICE.**
14. **The header test is a method of `TestInheritedFaults`**, with one `subTest` per module, and
    reads each module's first 15 lines with `readline()` from the directory of
    `raypoolkit.__file__`. **IMPLEMENTATION CHOICE.**
15. **S4 also asserts that the post handler's object is not the one the compute ran on**, beside
    "is `results[0]`" and `store_id` 1001. **IMPLEMENTATION CHOICE.**
16. **C2 gives each argument `lambda *args, **kwargs: None`**, and C6 also asserts that
    construction prints nothing. **IMPLEMENTATION CHOICE.**
17. **`black` joined `test_construction.py`'s three message templates onto one line each**
    (each was first written in parentheses). The templates are `str.format` strings, so the tests
    compare with the module's messages whole. **IMPLEMENTATION CHOICE** (formatting).
18. **The retirement paragraph** follows DatastoreKit's (`HEAD`, lines 1–8) in form, naming
    `v0.1.0`, README §5 rule 8 and prompt 04 §2.8. **IMPLEMENTATION CHOICE.**

One slip, corrected: **the first §4.5 run's snapshot hashed nothing.** It was run from `zsh`,
which does not split an unquoted variable, so `shasum` was given the file list as one name and
failed; the comparison then covered `git status` and the module's own SHA-256 only (both equal).
It was run again from a `bash` script (`$S/scripts/run_on_v010.sh`), whose snapshot hashes all ten
files: tree restored, and the same failing set, entry for entry (§4.11). **UNINTENDED DRIFT**,
corrected; every other driver of this log is `bash`.

## 3. Verification performed

### 3.1 The suite, by venv and by module (prompt §4.1)

Every run is `<python> -m unittest discover -s raypoolkit/tests -t .`, in the foreground, its output
written to a file in `$S` and the verdict grepped from it. Counts by module are by the loader
(`$S/scripts/count_by_module.py`, which walks `unittest.defaultTestLoader.discover`).

| Venv | `sys.version` | `ray` | Tree | Verdict |
|---|---|---|---|---|
| `venv/`, before any change | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | the repository at `a7d9252` | `Ran 116 tests in 3.767s` `OK` |
| `$S/venv-high`, before | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | `git archive v0.1.0` export (deviation 6) | `Ran 116 tests in 1.488s` `OK` |
| `venv/`, after | as above | 2.43.0 | the final tree | `Ran 121 tests in 2.838s` `OK` |
| `$S/venv-high`, after | as above | 2.55.1 | the final tree | `Ran 121 tests in 4.753s` `OK` |

`venv/`: `black==25.1.0`, `ray==2.43.0`, `-e git+…RayPoolKit.git@a7d9252…#egg=raypoolkit`
(`pip freeze`; the `HEAD` at the freeze). `$S/venv-high`: `ray==2.55.1`, `-e
file:///Users/ds283/Documents/Code/RayPoolKit` (`uv pip freeze`). In both, `importlib.metadata`
gives `raypoolkit` `0.1.0`, and from the repository root `raypoolkit.__file__` is
`/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py`.

| Module | Before (both ends) | After (both ends) |
|---|---|---|
| `test_construction` | 12 | **15** (C5, C6, C7) |
| `test_inherited_faults` | 5 | **6** (the header test) |
| `test_package_imports` | 3 | 3 |
| `test_printed_lines` | 17 | **18** (the spelling test) |
| `test_run_paths` | 22 | 22 |
| `test_scheduling` | 7 | 7 |
| `test_standins` | 30 | 30 |
| `test_task_builder` | 20 | 20 |
| **Total** | **116** | **121** |

### 3.2 The unchanged suite on the fixed module (prompt §3.5)

With every change of §2 made to the package and no test yet changed:
`Ran 116 tests … FAILED (failures=6, errors=5)`, exactly §3.5's eleven.

- Errors (`ValueError` at construction): `test_construction.TestHandlerChecks.test_compute_handler_without_persist_handler_raises_runtime_error`;
  `test_inherited_faults.TestInheritedFaults.test_fault_store_handler_none_with_compute_fails_at_first_compute`;
  `test_printed_lines.TestStatusMessages`' three tests, each in its "validation only" subtest
  only.
- Failures: `test_construction.TestHandlerChecks.test_persist_handler_without_compute_handler_raises_runtime_warning`;
  the fault-1, fault-2, fault-3 and fault-4a pins; S4.

X1 passed (it seeded both keys). Nothing else failed, so no stop.

### 3.3 The check's last run (prompt §2.8)

`./venv/bin/python docs/extraction/compare_with_source.py`, before any change: **exit 0**. Its
whole output:

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 572
  D-imp: 2
  D-pool: 1
  unclassified: 0
    D-imp   source :8 / package :8
        - from Datastore.SQL.ShardedPool import ShardedPool
        + from raypoolkit.contract import DatastorePool
    D-imp   source :9 / package :9
        - from utilities import format_time
        + from raypoolkit._timing import format_time
    D-pool  source :75 / package :75
        -         pool: ShardedPool,
        +         pool: DatastorePool,

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 4
  unclassified: 0
    D-int   SECONDS_PER_MINUTE: package :11-11 equals source :20-20
    D-int   SECONDS_PER_HOUR: package :12-12 equals source :21-21
    D-int   SECONDS_PER_DAY: package :13-13 equals source :22-22
    D-int   format_time: package :16-52 equals source :25-61
    D-int   span: package :11-end equals source :20-61 byte for byte

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)
  raypoolkit/tests/standins.py: present (02 §2.1: the Ray, clock, work-object and pool stand-ins)
  raypoolkit/tests/test_standins.py: present (02 §2.1: the stand-ins' own tests)
  raypoolkit/tests/test_construction.py: present (02 §2.3: the constructor)
  raypoolkit/tests/test_task_builder.py: present (02 §2.3: the task builder's outcomes)
  raypoolkit/tests/test_run_paths.py: present (02 §2.3: the paths through the dispatch loop)
  raypoolkit/tests/test_scheduling.py: present (02 §2.3: the queue and batch sizes)
  raypoolkit/tests/test_printed_lines.py: present (02 §2.3: the printed lines (U9))
  raypoolkit/tests/test_inherited_faults.py: present (02 §2.3: faults 1-4, pinned as they behave)

Undeclared files under raypoolkit/: 0

RESULT: OK
```

It was not run again; on this commit's tree it fails by design.

### 3.4 `black` (prompt §4.3)

`./venv/bin/black --check raypoolkit docs` (25.1.0): `15 files would be left unchanged.` `black`
left the four package modules unchanged with the header and the new checks (each message one
f-string on one line); it reformatted only `test_construction.py`'s templates (deviation 17).

### 3.5 No Ray

`pgrep -lf 'gcs_server|raylet|ray::'` matched no Ray process at any point. Once, at the start, it
matched three `zsh` processes of another session (`…-Users-ds283-Documents-Code-DatastoreKit/…/orch11`),
whose own command lines contain the same pattern while they ran DatastoreKit's suite; they are not
this repository's and not Ray, and were left alone. From then on the check filtered out shells
(`grep -v -E '^[0-9]+ (/bin/)?(zsh|bash|sh) '`) and found nothing, before and after every suite
run; an unfiltered `pgrep -lf 'gcs_server|raylet'` after the last run was empty. No test reached
`ray.init` (every passing run tears down with `ray.is_initialized()` false).

### 3.6 The printed lines (README §5 rule 7)

`git diff -- raypoolkit/tests/test_printed_lines.py` is `HANDLER_SETS`' edit and the one new test;
no other line of the module changed, and every one of its other tests passes. The spelling test
prints the same nine lines for all three spellings, equal to
`test_a_lookup_only_run_notifying_on_every_pass`'s. `TestStatusMessages`' "compute" and "every
handler" cases still show the validation segment absent and present.

## 4. The deliberate-breakage record (prompt §4.4, §4.5)

Each diff is exactly as applied, against the final tree before the commit, made by
`$S/scripts/make_diffs.py` and replayed by `$S/scripts/replay.sh` (`bash`): `git apply --check`;
`git apply`; the whole suite under `gtimeout 300`; `git apply -R --check`; `git apply -R`; the
snapshot of deviation 1 compared. None timed out; none is committed. "Failed" lists each failing
test, with its failing subtests.

**Summary.** (r1)–(r10): **10 items, each fails at least the planner's tests; 0 fail nothing; 0
timeouts; 10 trees restored.**

### (r1) the 26 keys back to `.hex`

`Ran 121 tests … FAILED (errors=6)`; tree restored: yes. Planner: the fresh-refs guard and X1.

```diff
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -297,13 +297,13 @@
                     ref_data = self._task_builder(item)
 
                     def store_single_ref(ref, allow_store=True):
-                        self._inflight[ref.hex()] = ref
+                        self._inflight[ref.hex] = ref
 
                         if self._store_results and allow_store:
-                            self._data[ref.hex()] = ("lookup", self._current_idx)
+                            self._data[ref.hex] = ("lookup", self._current_idx)
                             self._current_idx += 1
                         else:
-                            self._data[ref.hex()] = ("lookup", None)
+                            self._data[ref.hex] = ("lookup", None)
 
                         self._num_lookup_queue += 1
 
@@ -314,7 +314,7 @@
                             store_single_ref(ref, allow_store=allow_store)
 
                             if "compute_payload" in ref_data:
-                                self._compute_data[ref.hex()] = ref_data[
+                                self._compute_data[ref.hex] = ref_data[
                                     "compute_payload"
                                 ]
 
@@ -359,7 +359,7 @@
 
             for ref in done_refs:
                 ref: ObjectRef
-                item_type, payload = self._data[ref.hex()]
+                item_type, payload = self._data[ref.hex]
 
                 if item_type == "lookup":
                     # payload is an index into the result set
@@ -374,8 +374,8 @@
                         self.results[idx] = obj
 
                     # remove the original 'lookup' task from the work queue
-                    self._inflight.pop(ref.hex(), None)
-                    self._data.pop(ref.hex(), None)
+                    self._inflight.pop(ref.hex, None)
+                    self._data.pop(ref.hex, None)
 
                     self._num_lookup_queue = max(self._num_lookup_queue - 1, 0)
                     self._num_lookup_complete += 1
@@ -388,8 +388,8 @@
                                 available_task: ObjectRef = self._available_handler(obj)
 
                                 # add this task to the work queue
-                                self._inflight[available_task.hex()] = available_task
-                                self._data[available_task.hex()] = (
+                                self._inflight[available_task.hex] = available_task
+                                self._data[available_task.hex] = (
                                     "available",
                                     (idx, obj),
                                 )
@@ -416,9 +416,9 @@
                                     {"label": label} if label is not None else {}
                                 )
 
-                                if ref.hex() in self._compute_data:
+                                if ref.hex in self._compute_data:
                                     compute_args.update(
-                                        {"payload": self._compute_data[ref.hex()]}
+                                        {"payload": self._compute_data[ref.hex]}
                                     )
 
                                 compute_task: ObjectRef = self._compute_handler(
@@ -426,8 +426,8 @@
                                 )
 
                                 # add this compute task to the work queue
-                                self._inflight[compute_task.hex()] = compute_task
-                                self._data[compute_task.hex()] = ("compute", (idx, obj))
+                                self._inflight[compute_task.hex] = compute_task
+                                self._data[compute_task.hex] = ("compute", (idx, obj))
 
                                 self._num_compute_queue += 1
 
@@ -440,14 +440,14 @@
                             if replacement_obj is not None and self._store_results:
                                 self.results[idx] = replacement_obj
 
-                    self._compute_data.pop(ref.hex(), None)
+                    self._compute_data.pop(ref.hex, None)
 
                 elif item_type == "available":
                     # payload is a pair of the target index and the constructed object
                     idx, obj = payload
 
-                    self._inflight.pop(ref.hex(), None)
-                    self._data.pop(ref.hex(), None)
+                    self._inflight.pop(ref.hex, None)
+                    self._data.pop(ref.hex, None)
 
                     self._num_available_queue = max(self._num_available_queue - 1, 0)
                     self._num_available_complete += 1
@@ -471,8 +471,8 @@
                     self._store_handler(obj, self._pool)
 
                     # remove the original 'compute' task from the work queue
-                    self._inflight.pop(ref.hex(), None)
-                    self._data.pop(ref.hex(), None)
+                    self._inflight.pop(ref.hex, None)
+                    self._data.pop(ref.hex, None)
 
                     self._num_compute_queue = max(self._num_compute_queue - 1, 0)
                     self._num_compute_complete += 1
@@ -481,8 +481,8 @@
                     store_task: ObjectRef = self._persist_handler(obj, self._pool)
 
                     # add this store task to the work queue
-                    self._inflight[store_task.hex()] = store_task
-                    self._data[store_task.hex()] = ("store", payload)
+                    self._inflight[store_task.hex] = store_task
+                    self._data[store_task.hex] = ("store", payload)
 
                     self._num_store_queue += 1
 
@@ -504,8 +504,8 @@
                         self.results[idx] = replacement_obj
 
                     # remove the original 'store' task from the work queue
-                    self._inflight.pop(ref.hex(), None)
-                    self._data.pop(ref.hex(), None)
+                    self._inflight.pop(ref.hex, None)
+                    self._data.pop(ref.hex, None)
 
                     self._num_store_queue = max(self._num_store_queue - 1, 0)
                     self._num_store_complete += 1
@@ -516,8 +516,8 @@
                             replacement_obj
                         )
 
-                        self._inflight[validation_task.hex()] = validation_task
-                        self._data[validation_task.hex()] = (
+                        self._inflight[validation_task.hex] = validation_task
+                        self._data[validation_task.hex] = (
                             "validate",
                             (idx, replacement_obj),
                         )
@@ -542,8 +542,8 @@
                             f"!! WARNING: {type(obj).__name__} object with store_id={obj.store_id} did not validate after being emplaced in the datastore"
                         )
 
-                    self._inflight.pop(ref.hex(), None)
-                    self._data.pop(ref.hex(), None)
+                    self._inflight.pop(ref.hex, None)
+                    self._data.pop(ref.hex, None)
 
                     self._num_validation_queue = max(self._num_validation_queue - 1, 0)
                     self._num_validation_complete += 1
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_fresh_refs_from_wait_complete_every_path`, all
  five subtests (`lookup only`, `availability handler`, `compute with validation`, `compute without
  validation`, `blobs`), each `KeyError`
- `test_run_paths.TestUnexpectedItemType.test_an_unexpected_item_type_raises` (`KeyError`: the pool
  looks up `ref.hex`, the seed is under `ref.hex()`)

### (r2) fault 2's call back to `obj`

`Ran 121 tests … FAILED (failures=2)`; tree restored: yes. Planner: the fault-2 guard and S4.

```diff
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -527,7 +527,7 @@
                     # otherwise, this is the exit point for driver flow associated with this task, so apply the
                     # postprocessing task, if one was supplied
                     elif self._post_handler is not None:
-                        replacement_obj = self._post_handler(replacement_obj)
+                        replacement_obj = self._post_handler(obj)
                         if replacement_obj is not None and self._store_results:
                             self.results[idx] = replacement_obj
 
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_the_post_handler_after_persist_gets_the_persisted_object`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler`

### (r3) `len(task_list)` restored

`Ran 121 tests … FAILED (errors=1)`; tree restored: yes. Planner: the fault-3 guard.

```diff
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -175,7 +175,7 @@
 
         self._store_results = store_results
         if store_results:
-            self.results = [None for _ in range(self._num_total_items)]
+            self.results = [None for _ in range(len(task_list))]
             self._current_idx = 0
 
         self._num_lookup_queue = 0
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_store_results_accepts_a_generator_task_list`
  (`TypeError`)

### (r4) the two default resolutions removed

`Ran 121 tests … FAILED (failures=3, errors=77)`; tree restored: yes. Planner: C6, the fault-4a
guard and the spelling test. As clarification 3 says, it is wide: every lookup-only test spelled
`LOOKUP_ONLY` leaves the store handler at its default, which now raises at construction naming
`store_handler`. 51 tests fail (80 entries, subtests counted), the planner's three among them.

```diff
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -107,11 +107,6 @@
         store_results: bool = False,
     ):
         if compute_handler is None:
-            if store_handler is _default_store_handler:
-                store_handler = None
-            if persist_handler is _default_persist_handler:
-                persist_handler = None
-
             for name, value in (
                 ("store_handler", store_handler),
                 ("persist_handler", persist_handler),
```

Failed (test, with the number of failing entries where a test fails in more than one subtest):
- `test_construction.TestHandlerChecks.test_a_pool_without_a_compute_handler_constructs_however_it_is_spelled` (3 entries)
- `test_construction.TestHandlerChecks.test_an_explicit_compute_path_argument_without_a_compute_handler_raises_value_error` (3 entries)
- `test_construction.TestHandlerChecks.test_neither_handler_constructs`
- `test_inherited_faults.TestInheritedFaults.test_a_lookup_only_pool_needs_no_persist_handler`
- `test_inherited_faults.TestInheritedFaults.test_fresh_refs_from_wait_complete_every_path` (3 entries)
- `test_inherited_faults.TestInheritedFaults.test_store_results_accepts_a_generator_task_list`
- `test_printed_lines.TestConsumerPatterns.test_the_patterns_match_the_pool_s_lines`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_pool_prints_the_same_lines_however_its_handlers_are_spelled` (3 entries)
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_more_than_notify_batch_size_items_were_processed`
- `test_printed_lines.TestProgressAndCompletion.test_a_pair_when_the_notify_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_before_the_minimum_interval_has_passed`
- `test_printed_lines.TestProgressAndCompletion.test_no_progress_lines_without_a_title`
- `test_printed_lines.TestProgressAndCompletion.test_the_available_rate_is_per_interval`
- `test_printed_lines.TestProgressAndCompletion.test_the_minimum_interval_is_a_strict_bound`
- `test_printed_lines.TestProgressAndCompletion.test_the_percentage_counts_items_whose_task_is_not_yet_built`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_with_rates` (4 entries)
- `test_printed_lines.TestStatusMessages.test_the_completed_message_without_rates` (4 entries)
- `test_printed_lines.TestStatusMessages.test_the_queued_message_has_a_segment_per_handler` (4 entries)
- `test_run_paths.TestAvailable.test_available_with_an_availability_handler_runs_an_available_task`
- `test_run_paths.TestAvailable.test_available_without_an_availability_handler_exits_to_the_post_handler`
- `test_run_paths.TestExits.test_a_returned_none_leaves_the_results_entry` (3 entries)
- `test_run_paths.TestExits.test_a_returned_replacement_replaces_the_results_entry` (3 entries)
- `test_run_paths.TestExits.test_a_returned_replacement_without_store_results_is_dropped` (3 entries)
- `test_run_paths.TestExits.test_each_exit_without_a_post_handler_calls_nothing` (3 entries)
- `test_run_paths.TestLookup.test_a_completed_lookup_puts_its_object_in_results`
- `test_run_paths.TestLookup.test_results_hold_what_get_returned_not_what_the_builder_minted`
- `test_run_paths.TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing`
- `test_run_paths.TestUnexpectedItemType.test_an_unexpected_item_type_raises`
- `test_scheduling.TestResultsOrder.test_results_keep_task_order_when_lookups_complete_in_reverse`
- `test_scheduling.TestSizes.test_max_task_queue_holds_back_the_next_batch_until_the_queue_drains_below_it`
- `test_scheduling.TestSizes.test_one_builder_call_per_item`
- `test_scheduling.TestSizes.test_process_batch_size_sets_how_many_tasks_each_wait_returns`
- `test_scheduling.TestSizes.test_the_default_sizes_build_five_at_a_time_and_process_one_at_a_time`
- `test_task_builder.TestBatchCreation.test_a_batch_is_created_only_while_the_queue_has_room`
- `test_task_builder.TestBatchCreation.test_a_batch_makes_at_most_create_batch_size_builder_calls`
- `test_task_builder.TestBatchCreation.test_num_returns_is_the_smaller_of_process_batch_size_and_the_work_in_flight`
- `test_task_builder.TestNoneReturns.test_none_for_some_items_enqueues_the_others`
- `test_task_builder.TestNoneReturns.test_none_from_every_builder_enqueues_nothing_and_waits_on_nothing`
- `test_task_builder.TestNoneReturns.test_none_with_store_results_raises`
- `test_task_builder.TestRefusedReturns.test_a_dict_without_ref_is_refused`
- `test_task_builder.TestRefusedReturns.test_a_nested_list_is_refused`
- `test_task_builder.TestRefusedReturns.test_a_refused_element_of_a_sequence_is_refused`
- `test_task_builder.TestRefusedReturns.test_a_string_is_refused`
- `test_task_builder.TestRefusedReturns.test_an_int_is_refused`
- `test_task_builder.TestSequenceReturns.test_a_list_a_tuple_and_a_set_are_each_enqueued_element_by_element` (3 entries)
- `test_task_builder.TestSequenceReturns.test_a_sequence_with_store_results_raises` (3 entries)
- `test_task_builder.TestSequenceReturns.test_an_empty_sequence_enqueues_nothing`
- `test_task_builder.TestSingleReturns.test_a_bare_object_ref_is_enqueued`
- `test_task_builder.TestSingleReturns.test_store_results_takes_a_result_index_per_single_return_in_task_order`
- `test_task_builder.TestSingleReturns.test_without_store_results_a_single_return_takes_no_index`
### (r5) the store default resolved, but not the persist default

`Ran 121 tests … FAILED (failures=2, errors=11)`; tree restored: yes. Planner: as (r4), from the
persist side: C6, the fault-4a guard and the spelling test. It is narrow, since `LOOKUP_ONLY`
passes `persist_handler=None`. The two C2 subtests beyond the planner's fail because the
unresolved default persist handler is refused first, with the `persist_handler` message, before
the loop reaches `validation_handler` or `label_builder`.

```diff
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -109,8 +109,6 @@
         if compute_handler is None:
             if store_handler is _default_store_handler:
                 store_handler = None
-            if persist_handler is _default_persist_handler:
-                persist_handler = None
 
             for name, value in (
                 ("store_handler", store_handler),
```

Failed:
- `test_construction.TestHandlerChecks.test_a_pool_without_a_compute_handler_constructs_however_it_is_spelled`
  (`nothing else`, `store_handler=None`)
- `test_construction.TestHandlerChecks.test_an_explicit_compute_path_argument_without_a_compute_handler_raises_value_error`
  (`validation_handler`, `label_builder`)
- `test_inherited_faults.TestInheritedFaults.test_a_lookup_only_pool_needs_no_persist_handler`
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_pool_prints_the_same_lines_however_its_handlers_are_spelled`
  (`nothing passed`, `store_handler=None`)
- `test_printed_lines.TestStatusMessages`' three tests, each in `lookup only, nothing passed` and
  `lookup only, store_handler=None`

### (r6) the compute branch's `None` check removed

`Ran 121 tests … FAILED (failures=3)`; tree restored: yes. Planner: C1, C5 and the fault-4b guard.

```diff
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -123,16 +123,6 @@
                         f"No compute handler was supplied, so {name} would never be called; leave it out, or pass None"
                     )
 
-        else:
-            for name, value in (
-                ("store_handler", store_handler),
-                ("persist_handler", persist_handler),
-            ):
-                if value is None:
-                    raise ValueError(
-                        f"A compute handler was supplied, so {name} must not be None; leave it out to use the default"
-                    )
-
         for name, value in (
             ("create_batch_size", create_batch_size),
             ("process_batch_size", process_batch_size),
```

Failed:
- `test_construction.TestHandlerChecks.test_a_compute_handler_with_persist_handler_none_raises_value_error`
- `test_construction.TestHandlerChecks.test_a_compute_handler_with_store_handler_none_raises_value_error`
- `test_inherited_faults.TestInheritedFaults.test_store_handler_none_with_compute_is_refused_at_construction`

### (r7) `validation_handler` and `label_builder` dropped from the no-compute check

`Ran 121 tests … FAILED (failures=2)`; tree restored: yes. Planner: C2's two subtests for them.

```diff
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -115,8 +115,6 @@
             for name, value in (
                 ("store_handler", store_handler),
                 ("persist_handler", persist_handler),
-                ("validation_handler", validation_handler),
-                ("label_builder", label_builder),
             ):
                 if value is not None:
                     raise ValueError(
```

Failed:
- `test_construction.TestHandlerChecks.test_an_explicit_compute_path_argument_without_a_compute_handler_raises_value_error`
  (`validation_handler`, `label_builder`)

### (r8) `value < 1` → `value < 0`

`Ran 121 tests … FAILED (failures=3)`; tree restored: yes. Planner: C7's zero cases.

```diff
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -138,7 +138,7 @@
             ("process_batch_size", process_batch_size),
             ("max_task_queue", max_task_queue),
         ):
-            if value < 1:
+            if value < 0:
                 raise ValueError(f"{name} must be at least 1, not {value!r}")
 
         self._pool = pool
```

Failed:
- `test_construction.TestSizeChecks.test_a_size_below_one_raises_value_error`, in its three
  `value=0` subtests (`create_batch_size`, `process_batch_size`, `max_task_queue`)

### (r9) one message says "maker"

The no-compute message, "No compute handler was supplied" → "No compute maker was supplied".
`Ran 121 tests … FAILED (failures=4)`; tree restored: yes. Planner: its message test.

```diff
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -120,7 +120,7 @@
             ):
                 if value is not None:
                     raise ValueError(
-                        f"No compute handler was supplied, so {name} would never be called; leave it out, or pass None"
+                        f"No compute maker was supplied, so {name} would never be called; leave it out, or pass None"
                     )
 
         else:
```

Failed:
- `test_construction.TestHandlerChecks.test_an_explicit_compute_path_argument_without_a_compute_handler_raises_value_error`,
  all four subtests

### (r10) `_timing.py`'s header removed

`Ran 121 tests … FAILED (failures=1)`; tree restored: yes. Planner: the header test.

```diff
--- a/raypoolkit/_timing.py
+++ b/raypoolkit/_timing.py
@@ -1,18 +1,3 @@
-# (c) University of Sussex 2026
-# Created by David Seery
-#
-# Licensed under the Apache License, Version 2.0 (the "License");
-# you may not use this file except in compliance with the License.
-# You may obtain a copy of the License at
-#
-#    http://www.apache.org/licenses/LICENSE-2.0
-#
-# Unless required by applicable law or agreed to in writing, software
-# distributed under the License is distributed on an "AS IS" BASIS,
-# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-# See the License for the specific language governing permissions and
-# limitations under the License.
-
 """
 The timing helpers the pool's progress and completion lines use.
 
```

Failed:
- `test_inherited_faults.TestInheritedFaults.test_every_package_module_carries_the_licence_header`
  (`module='_timing.py'`)

### 4.11 The new suite on `v0.1.0`'s module (prompt §4.5)

`$S/scripts/run_on_v010.sh` (deviation 2): the fixed module copied to scratch; `git show
v0.1.0:raypoolkit/RayWorkPool.py > raypoolkit/RayWorkPool.py` (then `git diff --quiet v0.1.0 --
raypoolkit/RayWorkPool.py` true); the whole suite under `gtimeout 300`; the copy put back. **`Ran
121 tests … FAILED (failures=11, errors=23)`**; tree restored: yes (all ten SHA-256s and `git
status` equal; `RayWorkPool.py` is `8f4c1d7d…8ce919` again). 17 tests fail, and they are exactly
§3.1's six guards and §3.2–§3.4's eleven new or changed tests:

- `test_construction.TestHandlerChecks.test_a_compute_handler_with_persist_handler_none_raises_value_error` (ERROR)
- `test_construction.TestHandlerChecks.test_a_compute_handler_with_store_handler_none_raises_value_error` (FAIL)
- `test_construction.TestHandlerChecks.test_a_pool_without_a_compute_handler_constructs_however_it_is_spelled` (ERROR): `(spelling='nothing else')`; `(spelling='store_handler=None')`
- `test_construction.TestHandlerChecks.test_an_explicit_compute_path_argument_without_a_compute_handler_raises_value_error` (ERROR): `(argument='store_handler')`; `(argument='persist_handler')`; `(argument='validation_handler')`; `(argument='label_builder')`
- `test_construction.TestSizeChecks.test_a_size_below_one_raises_value_error` (FAIL): `(size='create_batch_size', value=0)`; `(size='create_batch_size', value=-1)`; `(size='process_batch_size', value=0)`; `(size='process_batch_size', value=-1)`; `(size='max_task_queue', value=0)`; `(size='max_task_queue', value=-1)`
- `test_inherited_faults.TestInheritedFaults.test_a_lookup_only_pool_needs_no_persist_handler` (ERROR)
- `test_inherited_faults.TestInheritedFaults.test_every_package_module_carries_the_licence_header` (FAIL): `(module='RayWorkPool.py')`
- `test_inherited_faults.TestInheritedFaults.test_fresh_refs_from_wait_complete_every_path` (ERROR): `(path='lookup only')`; `(path='availability handler')`; `(path='compute with validation')`; `(path='compute without validation')`; `(path='blobs')`
- `test_inherited_faults.TestInheritedFaults.test_store_handler_none_with_compute_is_refused_at_construction` (FAIL)
- `test_inherited_faults.TestInheritedFaults.test_store_results_accepts_a_generator_task_list` (ERROR)
- `test_inherited_faults.TestInheritedFaults.test_the_post_handler_after_persist_gets_the_persisted_object` (FAIL)
- `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_pool_prints_the_same_lines_however_its_handlers_are_spelled` (ERROR): `(spelling='nothing passed')`; `(spelling='store_handler=None')`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_with_rates` (ERROR): `(handlers='lookup only, nothing passed')`; `(handlers='lookup only, store_handler=None')`
- `test_printed_lines.TestStatusMessages.test_the_completed_message_without_rates` (ERROR): `(handlers='lookup only, nothing passed')`; `(handlers='lookup only, store_handler=None')`
- `test_printed_lines.TestStatusMessages.test_the_queued_message_has_a_segment_per_handler` (ERROR): `(handlers='lookup only, nothing passed')`; `(handlers='lookup only, store_handler=None')`
- `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler` (FAIL)
- `test_run_paths.TestUnexpectedItemType.test_an_unexpected_item_type_raises` (ERROR)
Nothing else fails. Each subtest that passes there is one `v0.1.0` accepts too: C6's
`persist_handler=None` and `both None`, C7's `value=1`, the spelling test's `persist_handler=None`,
`HANDLER_SETS`' unchanged cases, and the header test's three modules other than `RayWorkPool.py`,
which keep their header (§4.5 replaces only `RayWorkPool.py`). The guard's tests 2 and 3 run in a
subprocess from a temporary directory and import the same working tree, so they ran against
`v0.1.0`'s module too, and passed.

## 5. Observations not acted on

1. **`README.md` still describes `v0.1.0`'s constructor.** Its section "A pool with no compute
   handler must pass `persist_handler=None`" (`README.md:147-152`) says the constructor raises
   `RuntimeWarning`, and that a compute handler with `persist_handler=None` raises `RuntimeError`;
   on this commit's tree both are `ValueError`, and a lookup-only pool needs neither `None`. It
   says "As of `v0.1.0`", which stays true of `v0.1.0`; the prompt (§1, §7) leaves the README to
   05. No issue: 05's plan already rewrites it (README §2, row 05).
2. **`PROVENANCE.md:40`** says `raypoolkit/RayWorkPool.py` equals its source except for the listed
   classes. True of `v0.1.0`, not of this commit's tree. Left to 05, as the prompt says; no issue.
3. **`compare_with_source.py`'s `NO_SOURCE` entry for `test_inherited_faults.py`** still reads
   "faults 1-4, pinned as they behave". §2.8 limits the change to the docstring's paragraph, and the
   retired script describes `v0.1.0`, where it is true. No issue.
4. **A size that does not compare with `1` now raises `TypeError` at construction**, from the check's
   `value < 1` (measured: `None` and `"5"` give `'<' not supported between …`; `0.5` gives the
   `ValueError` message; `1.5` constructs). Before, the same values failed in `run()`. The prompt
   says nothing checks the sizes' type, and nothing does; this is the comparison's own error. No
   client passes a non-integer literal (prompt §2.5). No issue.
5. **A pool with no compute handler may still be given an `available_handler` or a
   `post_handler`**: both are used on the lookup path, and U8 checks only the four compute-path
   arguments. As intended; noted for 06's checklists.
6. **02's four equivalent mutations** (log 02 §5.3) were not re-measured; 04 changed none of the
   lines they touch except by the key spelling.

## 6. Issues

**Opened:** none. **Closed** (board §3 → §4, each with a dated **Resolved (04)** line):
`[00-in-flight-work-is-keyed-on-a-bound-method]`,
`[00-a-post-handler-after-persist-gets-the-unpersisted-object]`,
`[00-store-results-sizes-from-len-of-the-task-list]`,
`[00-the-constructor-checks-its-handlers-unevenly]`,
`[00-messages-say-maker-and-the-module-has-no-licence-header]`,
`[01-a-kept-comment-names-the-datastore-service]` and
`[02-the-constructor-does-not-check-its-sizes]`. **Narrowed:** none. `docs/OPEN_ISSUES.md` goes
from 8 to **1** open: `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`, still proposed
for 05.

## 7. State handed to the next prompt

- `HEAD` is this commit. `pyproject.toml` still says `0.1.0`; `README.md` and `PROVENANCE.md` are
  as `v0.1.0` left them (§5.1–§5.2). No tag was made and nothing pushed; local `main` is ahead of
  `origin/main` (`6b1ddfe`) by `c207238`, `a7d9252` and this commit.
- **Suite: 121 tests**, passing at 3.12.15 / 2.43.0 and 3.13.16 / 2.55.1 on macOS. CI has not run
  on this commit; it runs when the commit is pushed.
- **What a caller must pass, after 04** (README §4, "04 names any change"): nothing new. A
  lookup-only pool needs only `compute_handler=None`; `store_handler=None` and
  `persist_handler=None` are still accepted. Newly refused, each with `ValueError` at
  construction: a pool with no compute handler but a `store_handler`, `persist_handler`,
  `validation_handler` or `label_builder` that is not `None` (a store or persist handler left at
  its default excepted); a compute handler with `store_handler=None` or `persist_handler=None`;
  and a size below 1. The two old exception types (`RuntimeError`, `RuntimeWarning`) are no longer
  raised by the constructor. The printed lines are unchanged.
- `compare_with_source.py` is retired at `v0.1.0` (its docstring says how to run it there).
- The drivers (`$S/scripts/`) are not committed; every diff they applied is in §4, exactly as
  applied.
