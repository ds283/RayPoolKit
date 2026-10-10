# Log — extraction prompt 01: import the pool

**Subject:** Import SGK's RayWorkPool as the raypoolkit package · **Commit:** `49f3ddf` ·
**Date:** 2026-10-10 · **Agent:** Claude Opus 5.5

**Result: landed.** The package `raypoolkit` exists, its `RayWorkPool` module is SGK's at `b510bc9`
changed by two D-imp lines and one D-pool line, and `_timing.py` holds SGK's four definitions byte
for byte. `compare_with_source.py` exits 0; the suite goes from **0 to 3** tests, all passing;
`black --check raypoolkit docs` is clean. All eight breakages of the check and the three of the
guard fail as recorded below. One issue is opened (§6), so the index goes from 5 to **6**.

**Gate, re-checked at start.** SGK `HEAD` is `b510bc90b66985532d28996ab4e5b13b0ff71709`;
`git -C SecondaryGWKit rev-parse b510bc9:RayTools/RayWorkPool.py` is
`b4666fa89abb26829fd585b881947d7ef5172cea`; it was last changed by `0ee16a8` (2026-09-04);
`RayTools/__init__.py` is 0 bytes. This repository was at `310db6e`, clean. No Ray process was
running, and none was started.

## 1. What shipped

| File | What |
|---|---|
| `pyproject.toml` | setuptools build (`setuptools>=64`, `setuptools.build_meta`); `raypoolkit` `0.1.0.dev0`; `requires-python = ">=3.12"`; the one dependency `ray`, unbounded (03 sets it, U7); `packages.find` `include = ["raypoolkit*"]`, the tests included |
| `raypoolkit/__init__.py` | the two re-exports and `__all__`, nothing else (U4) |
| `raypoolkit/RayWorkPool.py` | SGK's `RayTools/RayWorkPool.py` at `b510bc9`, with `:8`, `:9` (D-imp) and `:75` (D-pool) rewritten. 575 lines, every line where it was in SGK |
| `raypoolkit/_timing.py` | a module docstring naming the source, then SGK `utilities.py:20-61` byte for byte (the three `SECONDS_PER_*`, the two blank lines, `format_time`); no import |
| `raypoolkit/contract.py` | `DatastorePool(Protocol)` with `object_store(self, objects) -> ObjectRef`; imports `typing.Protocol` and `ray.ObjectRef` only; not `runtime_checkable` |
| `raypoolkit/tests/__init__.py` | empty |
| `raypoolkit/tests/test_package_imports.py` | the guard, three tests (§2.7) |
| `docs/extraction/compare_with_source.py` | the equivalence check (§2.5) |
| `PROVENANCE.md` | source, import commit, blob, the file map, the classes, how to re-run the check, the U5 freeze |
| this log, the board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md` | the records |

**The check's rules** (its docstring states them in full). A differing line pair is classified only
inside a `difflib` `replace` run of equal length on both sides, and only when exactly one rule's
image of the source line equals the package line, indentation included. Added or deleted lines are
never classified.
- **D-imp** is an exact two-entry map of whole statements: the source line must parse, alone, as
  one level-0 `ImportFrom` with one alias and no `as`, be spelled exactly as `ast.unparse` spells
  it, and have `(module, name)` in the map; its image is the mapped statement, unparsed, at the
  same indentation.
- **D-pool** is the one identifier: the source line, less its trailing comma, must parse as the only
  parameter of a function, with no default and the bare annotation `ShardedPool`, with
  `ShardedPool` occurring on it once; its image replaces that identifier with `DatastorePool`.
- **No D-fmt rule** (the orchestrator's recommendation, followed). `black` 25.1.0 changes no line
  of the package module (§3.5), so none is needed.
- **D-int** (for `_timing.py`): the package module is its docstring (which must name
  `utilities.py` and `b510bc9`) and then exactly the four definitions, found in the source by name,
  in source order, each with a source segment equal to SGK's; and, beyond the prompt, its text
  from the first definition to the end is SGK's text over the same span byte for byte, with only
  blank lines between the docstring and that span (§2, deviation 4).
- **Files:** every `.py` under `raypoolkit/` (outside `__pycache__`) must be in `FILES` or
  `NO_SOURCE`; a declared file that is missing fails too.
- Exit status: 0 when all holds, 1 when not, 2 when it cannot run (`git` fails, or the blob is not
  `b4666fa`).

## 2. Deviations from the prompt

1. **Breakage (h), an alias that keeps the old name** — added to §2.5's (a)–(g) at the
   orchestrator's direction. **IMPLEMENTATION CHOICE.** Result in §4.
2. **Each rule is a substitution applied to the source line, and there is no D-fmt rule** — the
   orchestrator's two recommendations, followed. **IMPLEMENTATION CHOICE.** The prompt's §2.4 lists
   D-fmt as an allowed class; the check has no rule for it because `black` changes nothing, so a
   line `black` had changed would fail the check (which the prompt's §5 makes a stop anyway).
3. **`DatastorePool` models only the scalar use of `object_store`.** DatastoreKit `v0.2.0`'s
   `ShardedPool.object_store(self, objects)` (`datastorekit/SQL/ShardedPool.py:3339`, read through
   `git show`) is unannotated, and returns one `ObjectRef` for one object or a list of them for a
   list or tuple. The pool only ever passes one object (`_default_persist_handler`, `:68-69`), so
   the protocol is `object_store(self, objects) -> ObjectRef`, and its docstring says that the pool
   never passes a list. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
4. **The D-int check is stricter than §2.5 asks.** Besides the `ast` segment comparison, it requires
   the package text from the first definition to the end to equal SGK's span byte for byte, and only
   blank lines between the docstring and that span, because `ast` does not see a comment placed
   between definitions. **IMPLEMENTATION CHOICE.**
5. **Test 3 pins two facts beyond §2.7's list**, both stated in §2.2 as consequences of U4:
   `import raypoolkit.RayWorkPool as m` gives the class, and `mock.patch("raypoolkit.RayWorkPool.ray",
   …)` patches the module. **IMPLEMENTATION CHOICE**: the docstring tells later prompts to patch
   through a string target, so the test proves that this works.
6. **The `datastorekit` breakage cannot reach test 1 through the suite's command.** Discovery
   imports the package `raypoolkit.tests`, which imports `raypoolkit/__init__.py`, which imports
   `contract.py`, which raises `ModuleNotFoundError` before any test is collected: the suite fails
   with one loader error and no test runs. To show test 1's own failure, the guard module was also
   run as a script (`./venv/bin/python raypoolkit/tests/test_package_imports.py`), which does not
   import the package in-process: test 1 then fails naming `raypoolkit/contract.py:9`, and tests 2
   and 3 fail in their children. **STRUCTURALLY REQUIRED**: the tests live inside the package
   (§2.2), so a package that cannot import cannot have its tests loaded.
7. **"The re-export removed"** is taken to be both re-export lines and `__all__`, leaving
   `__init__.py` empty; it fails tests 2 and 3, as the prompt expects. A supplementary variant
   that removes only the class's line fails test 3 alone: test 2 passes, because
   `from raypoolkit import RayWorkPool` then falls back to importing the submodule. Both recorded in
   §4. **IMPLEMENTATION CHOICE.**
8. **§3.1 was run from the session scratchpad, not `/tmp`**, in a shell started with `env -i` (no
   `PYTHONPATH`), per the orchestrator's conventions; the directory holds no `raypoolkit/`.
   **IMPLEMENTATION CHOICE.**
9. **The check prints the lines it classified as well as those it could not**, and `pyproject.toml`
   carries a one-line `description`; neither is asked for. **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT.

## 3. Verification performed

### 3.1 The venv and `pip freeze`

`venv/` from set-up, not recreated: Python 3.12.15, `ray==2.43.0`, `black==25.1.0`.
`./venv/bin/python -m pip install -e .` built `raypoolkit-0.1.0.dev0` (editable) in an isolated
build environment and installed it. `pip freeze` afterwards, as printed:

```
aiosignal==1.4.0
attrs==26.1.0
black==25.1.0
certifi==2026.7.22
charset-normalizer==3.5.2
click==8.5.0
filelock==4.1.0
frozenlist==1.8.0
idna==3.20
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
msgpack==1.2.3
mypy_extensions==1.1.0
packaging==26.3
pathspec==1.1.1
platformdirs==4.12.4
protobuf==7.36.2
PyYAML==6.0.3
ray==2.43.0
-e git+https://github.com/ds283/RayPoolKit.git@310db6ea723a07e42533367299103e318edc6cd9#egg=raypoolkit
referencing==0.37.0
requests==2.34.2
rpds-py==2026.9.1
typing_extensions==4.16.0
urllib3==2.8.0
```

### 3.2 No client is reachable (prompt §3.1)

From `…/scratchpad/agent01/work/fresh` (outside this repository), under
`env -i HOME=… PATH=/usr/bin:/bin /bin/bash --noprofile --norc`:

```
PYTHONPATH=<unset> cwd=/private/tmp/claude-35086/-Users-ds283-Documents-Code-RayPoolKit/34edbf4f-d5c2-4b38-87d1-4da2f31a5ec4/scratchpad/agent01/work/fresh
import raypoolkit ...: exit 0
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'RayTools'
import RayTools: exit 1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'datastorekit'
import datastorekit: exit 1
```

### 3.3 The suite (prompt §3.2)

**Before: 0** (no test file exists at `310db6e`; `git ls-tree -r HEAD` lists none). **After: 3.**
`./venv/bin/python -m unittest discover -s raypoolkit/tests -t .`, output to a scratch file:

```
...
----------------------------------------------------------------------
Ran 3 tests in 3.267s

OK
```

### 3.4 The equivalence check (prompt §3.3)

`./venv/bin/python docs/extraction/compare_with_source.py`, exit 0, whole output:

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

Undeclared files under raypoolkit/: 0

RESULT: OK
```

Per class: `RayWorkPool.py` 572 identical, **2 D-imp, 1 D-pool**, 0 unclassified; `_timing.py`
**4 D-int** definitions and the byte-for-byte span, 0 unclassified; 4 declared new files present;
0 undeclared.

### 3.5 `black` (prompt §3.5)

`./venv/bin/black --check raypoolkit docs`: "7 files would be left unchanged." `black` changed no
package file at any point: before formatting, `--check --diff` reported all six package files
unchanged and reformatted only `docs/extraction/compare_with_source.py`, which is new here. **No
line of `RayWorkPool.py` was changed by `black`.**

### 3.6 Where the five faults of the board's §3 now sit

Read from `raypoolkit/RayWorkPool.py` (by `grep -n` and `sed -n`), not carried over from the
board. They equal SGK's numbers, since D-imp and D-pool replace one line by one and `black` changes
nothing.

| Issue | Package lines |
|---|---|
| `[00-in-flight-work-is-keyed-on-a-bound-method]` | 26 lines keyed on `.hex`: `:260, 263, 266, 277, 322, 337, 338, 351, 352, 379, 381, 389, 390, 403, 409, 410, 434, 435, 444, 445, 467, 468, 479, 480, 505, 506` |
| `[00-a-post-handler-after-persist-gets-the-unpersisted-object]` | the `"store"` branch's exit with no validation handler, `:487-492`: `elif self._post_handler is not None:` at `:489`, the call `self._post_handler(obj)` at **`:490`** |
| `[00-store-results-sizes-from-len-of-the-task-list]` | `:138`, `self.results = [None for _ in range(len(task_list))]` |
| `[00-the-constructor-checks-its-handlers-unevenly]` | the `RuntimeWarning` check `:99-102` (raised at `:100`); the unchecked store handler is called at `:431` |
| `[00-messages-say-maker-and-the-module-has-no-licence-header]` | "maker" at `:96` and `:101`; no header (`:1` is `import time`) |

## 4. The deliberate-breakage record

Each diff is exactly as applied, with `git apply` from the repository root; each passed
`git apply --check` before and `git apply -R --check` after, was replayed by a `bash` script, and
was reverted with `git apply -R`. After each, a hash of every file under `raypoolkit`, `docs`,
`pyproject.toml`, `prompts` and `PROVENANCE.md`, together with `git status --short
--untracked-files=all`, equalled the hash before it ("tree restored: yes" for all eleven and the two
supplementary runs). None is committed. They were run on the working tree that `49f3ddf` records
(the package files were final when they ran).

### 4.1 The equivalence check: (a)–(h)

Each exits **1** with `RESULT: FAIL`. Its output is shown with the detail lines of the *classified*
lines (the D-imp, D-pool and D-int pairs of §3.4) left out; every count and every unclassified line
is as printed.

**(a)** `DEFAULT_MAX_TASK_QUEUE = 201`

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -11,7 +11,7 @@
 DEFAULT_CREATE_BATCH_SIZE = 5
 DEFAULT_PROCESS_BATCH_SIZE = 1
 
-DEFAULT_MAX_TASK_QUEUE = 200
+DEFAULT_MAX_TASK_QUEUE = 201
 DEFAULT_NOTIFY_BATCH_SIZE = 500
 DEFAULT_NOTIFY_TIME_INTERVAL = 5 * 60
 DEFAULT_NOTIFY_MIN_INTERVAL = 60
```

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 571
  D-imp: 2
  D-pool: 1
  unclassified: 1
  !! CHANGED (no rule maps it) source :14 / package :14
      - DEFAULT_MAX_TASK_QUEUE = 200
      + DEFAULT_MAX_TASK_QUEUE = 201

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 4
  unclassified: 0

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)

Undeclared files under raypoolkit/: 0

RESULT: FAIL
```

**(b)** an extra `import os`

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -1,4 +1,5 @@
 import time
+import os
 from datetime import datetime
 from typing import Optional
 
```

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 572
  D-imp: 2
  D-pool: 1
  unclassified: 1
  !! ADDED   package :2
      + import os

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 4
  unclassified: 0

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)

Undeclared files under raypoolkit/: 0

RESULT: FAIL
```

**(c)** the "available" rate regressed to the CPBH/SI form

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -557,7 +557,7 @@
                     self._last_num_lookup_complete = self._num_lookup_complete
                     self._last_num_compute_complete = self._num_compute_complete
                     self._last_num_store_complete = self._num_store_complete
-                    self._last_num_available_complete = self._num_available_complete
+                    self._last_num_available_complete = self._num_store_complete
                     self._last_num_validation_complete = self._num_validation_complete
 
         if self._title is not None:
```

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 571
  D-imp: 2
  D-pool: 1
  unclassified: 1
  !! CHANGED (no rule maps it) source :560 / package :560
      -                     self._last_num_available_complete = self._num_available_complete
      +                     self._last_num_available_complete = self._num_store_complete

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 4
  unclassified: 0

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)

Undeclared files under raypoolkit/: 0

RESULT: FAIL
```

**(d)** one deleted line

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -338,7 +338,6 @@
                     self._data.pop(ref.hex, None)
 
                     self._num_lookup_queue = max(self._num_lookup_queue - 1, 0)
-                    self._num_lookup_complete += 1
 
                     # if the object has an 'available' attribute, we regard it as participating in the available/compute/store cycle
                     if hasattr(obj, "available"):
```

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 571
  D-imp: 2
  D-pool: 1
  unclassified: 1
  !! DELETED source :341
      -                     self._num_lookup_complete += 1

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 4
  unclassified: 0

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)

Undeclared files under raypoolkit/: 0

RESULT: FAIL
```

**(e)** `pool: ShardedPool` → `pool: object`

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -72,7 +72,7 @@
 class RayWorkPool:
     def __init__(
         self,
-        pool: DatastorePool,
+        pool: object,
         task_list,
         task_builder,
         compute_handler=_default_compute_handler,
```

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 572
  D-imp: 2
  D-pool: 0
  unclassified: 1
  !! CHANGED (no rule maps it) source :75 / package :75
      -         pool: ShardedPool,
      +         pool: object,

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 4
  unclassified: 0

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)

Undeclared files under raypoolkit/: 0

RESULT: FAIL
```

**(f)** one changed literal in `_timing.format_time`

```diff
diff --git a/raypoolkit/_timing.py b/raypoolkit/_timing.py
--- a/raypoolkit/_timing.py
+++ b/raypoolkit/_timing.py
@@ -24,7 +24,7 @@
         if len(str) > 0:
             str = str + f" {days}d"
         else:
-            str = f"{days}d"
+            str = f"{days}D"
 
     if int_interval > SECONDS_PER_HOUR:
         hours = int_interval // SECONDS_PER_HOUR
```

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 572
  D-imp: 2
  D-pool: 1
  unclassified: 0

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 3
  unclassified: 2
  !! CHANGED definition format_time
      --- source
      +++ package
      @@ -12 +12 @@
      -            str = f"{days}d"
      +            str = f"{days}D"
  !! SPAN: package :11-end is not source :20-61 byte for byte

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)

Undeclared files under raypoolkit/: 0

RESULT: FAIL
```

**(g)** an undeclared `raypoolkit/extra.py` (a new-file diff; `git apply -R` deletes it)

```diff
diff --git a/raypoolkit/extra.py b/raypoolkit/extra.py
new file mode 100644
--- /dev/null
+++ b/raypoolkit/extra.py
@@ -0,0 +1 @@
+"""A module no prompt declared."""
```

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 572
  D-imp: 2
  D-pool: 1
  unclassified: 0

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 4
  unclassified: 0

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)

Undeclared files under raypoolkit/: 1
  !! NOT DECLARED: raypoolkit/extra.py

RESULT: FAIL
```

**(h)** an alias that keeps the old name, `:75` back to SGK's `pool: ShardedPool,`

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -5,7 +5,7 @@
 import ray
 from ray import ObjectRef
 
-from raypoolkit.contract import DatastorePool
+from raypoolkit.contract import DatastorePool as ShardedPool
 from raypoolkit._timing import format_time
 
 DEFAULT_CREATE_BATCH_SIZE = 5
@@ -72,7 +72,7 @@
 class RayWorkPool:
     def __init__(
         self,
-        pool: DatastorePool,
+        pool: ShardedPool,
         task_list,
         task_builder,
         compute_handler=_default_compute_handler,
```

```
Equivalence check: raypoolkit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at b510bc90b66985532d28996ab4e5b13b0ff71709
source blob of RayTools/RayWorkPool.py: b4666fa89abb26829fd585b881947d7ef5172cea (as expected)

raypoolkit/RayWorkPool.py  <-  RayTools/RayWorkPool.py  [module]
  identical: 573
  D-imp: 1
  D-pool: 0
  unclassified: 1
  !! CHANGED (no rule maps it) source :8 / package :8
      - from Datastore.SQL.ShardedPool import ShardedPool
      + from raypoolkit.contract import DatastorePool as ShardedPool

raypoolkit/_timing.py  <-  utilities.py  [internalised]
  D-int: 4
  unclassified: 0

Files with no source (declared):
  raypoolkit/__init__.py: present (01 §2.2: the re-export of RayWorkPool and DatastorePool)
  raypoolkit/contract.py: present (01 §2.3: the DatastorePool protocol)
  raypoolkit/tests/__init__.py: present (01 §2.2: empty)
  raypoolkit/tests/test_package_imports.py: present (01 §2.7: the import guard)

Undeclared files under raypoolkit/: 0

RESULT: FAIL
```

The D-imp rule refuses line 8 (it has an `as`), and line 75, now equal to SGK's, needs no class.

### 4.2 The guard

**`import numpy` inside a function of `RayWorkPool.py`** — suite exit 1, test 1 fails, tests 2 and
3 pass.

```diff
diff --git a/raypoolkit/RayWorkPool.py b/raypoolkit/RayWorkPool.py
--- a/raypoolkit/RayWorkPool.py
+++ b/raypoolkit/RayWorkPool.py
@@ -18,6 +18,8 @@
 
 
 def _readable_rate(rate_per_second: float):
+    import numpy
+
     current_rate = rate_per_second
     for unit, multiplier in [
         ("sec", 60),
```

```
F..
======================================================================
FAIL: test_every_import_is_stdlib_ray_or_the_package (raypoolkit.tests.test_package_imports.TestPackageImports.test_every_import_is_stdlib_ray_or_the_package)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/tests/test_package_imports.py", line 95, in test_every_import_is_stdlib_ray_or_the_package
    self.assertEqual(offending, [], "\n".join(offending))
AssertionError: Lists differ: ['raypoolkit/RayWorkPool.py:21: imports numpy'] != []

First list contains 1 additional elements.
First extra element 0:
'raypoolkit/RayWorkPool.py:21: imports numpy'

- ['raypoolkit/RayWorkPool.py:21: imports numpy']
+ [] : raypoolkit/RayWorkPool.py:21: imports numpy

----------------------------------------------------------------------
Ran 3 tests in 3.349s

FAILED (failures=1)
```

**`from datastorekit.SQL.ShardedPool import ShardedPool` added to `contract.py`** — suite exit 1,
with one loader error and no test run (deviation 6):

```diff
diff --git a/raypoolkit/contract.py b/raypoolkit/contract.py
--- a/raypoolkit/contract.py
+++ b/raypoolkit/contract.py
@@ -6,7 +6,9 @@
 
 from ray import ObjectRef
 
+from datastorekit.SQL.ShardedPool import ShardedPool
 
+
 class DatastorePool(Protocol):
     """
     The datastore pool a ``RayWorkPool`` is handed, described by the one method the pool calls.
```

```
E
======================================================================
ERROR: raypoolkit.tests (unittest.loader._FailedTest.raypoolkit.tests)
----------------------------------------------------------------------
ImportError: Failed to import test module: raypoolkit.tests
Traceback (most recent call last):
  File "/opt/local/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/unittest/loader.py", line 429, in _find_test_path
    package = self._get_module_from_name(name)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/local/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/unittest/loader.py", line 339, in _get_module_from_name
    __import__(name)
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py", line 1, in <module>
    from raypoolkit.RayWorkPool import RayWorkPool
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/RayWorkPool.py", line 8, in <module>
    from raypoolkit.contract import DatastorePool
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/contract.py", line 9, in <module>
    from datastorekit.SQL.ShardedPool import ShardedPool
ModuleNotFoundError: No module named 'datastorekit'


----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
```

The same diff, with the guard module run as a script (`./venv/bin/python
raypoolkit/tests/test_package_imports.py`), exit 1, **all three fail**. Test 1 names the file, line
and module; tests 2 and 3 fail because their child interpreters cannot import the package
(`datastorekit` is not installed in this venv, so test 2 fails on the import rather than on its
`sys.modules` check):

```
FFF
======================================================================
FAIL: test_every_import_is_stdlib_ray_or_the_package (__main__.TestPackageImports.test_every_import_is_stdlib_ray_or_the_package)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/tests/test_package_imports.py", line 95, in test_every_import_is_stdlib_ray_or_the_package
    self.assertEqual(offending, [], "\n".join(offending))
AssertionError: Lists differ: ['raypoolkit/contract.py:9: imports datastorekit.SQL.ShardedPool'] != []

First list contains 1 additional elements.
First extra element 0:
'raypoolkit/contract.py:9: imports datastorekit.SQL.ShardedPool'

- ['raypoolkit/contract.py:9: imports datastorekit.SQL.ShardedPool']
+ [] : raypoolkit/contract.py:9: imports datastorekit.SQL.ShardedPool

======================================================================
FAIL: test_the_class_is_re_exported_and_shadows_its_module (__main__.TestPackageImports.test_the_class_is_re_exported_and_shadows_its_module)
Decision U4: the module keeps its source's name, ``RayWorkPool``, and the class of the same
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/tests/test_package_imports.py", line 155, in test_the_class_is_re_exported_and_shadows_its_module
    self.assertEqual(result.returncode, 0, result.stderr)
AssertionError: 1 != 0 : Traceback (most recent call last):
  File "<string>", line 5, in <module>
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py", line 1, in <module>
    from raypoolkit.RayWorkPool import RayWorkPool
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/RayWorkPool.py", line 8, in <module>
    from raypoolkit.contract import DatastorePool
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/contract.py", line 9, in <module>
    from datastorekit.SQL.ShardedPool import ShardedPool
ModuleNotFoundError: No module named 'datastorekit'


======================================================================
FAIL: test_the_package_imports_with_no_client (__main__.TestPackageImports.test_the_package_imports_with_no_client)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/tests/test_package_imports.py", line 107, in test_the_package_imports_with_no_client
    self.assertEqual(result.returncode, 0, result.stderr)
AssertionError: 1 != 0 : Traceback (most recent call last):
  File "<string>", line 2, in <module>
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py", line 1, in <module>
    from raypoolkit.RayWorkPool import RayWorkPool
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/RayWorkPool.py", line 8, in <module>
    from raypoolkit.contract import DatastorePool
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/contract.py", line 9, in <module>
    from datastorekit.SQL.ShardedPool import ShardedPool
ModuleNotFoundError: No module named 'datastorekit'


----------------------------------------------------------------------
Ran 3 tests in 2.916s

FAILED (failures=3)
```

**The re-export removed from `raypoolkit/__init__.py`** — suite exit 1, tests 2 and 3 fail, test 1
passes:

```diff
diff --git a/raypoolkit/__init__.py b/raypoolkit/__init__.py
--- a/raypoolkit/__init__.py
+++ b/raypoolkit/__init__.py
@@ -1,4 +0,0 @@
-from raypoolkit.RayWorkPool import RayWorkPool
-from raypoolkit.contract import DatastorePool
-
-__all__ = ["RayWorkPool", "DatastorePool"]
```

```
.FF
======================================================================
FAIL: test_the_class_is_re_exported_and_shadows_its_module (raypoolkit.tests.test_package_imports.TestPackageImports.test_the_class_is_re_exported_and_shadows_its_module)
Decision U4: the module keeps its source's name, ``RayWorkPool``, and the class of the same
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/tests/test_package_imports.py", line 155, in test_the_class_is_re_exported_and_shadows_its_module
    self.assertEqual(result.returncode, 0, result.stderr)
AssertionError: 1 != 0 : Traceback (most recent call last):
  File "<string>", line 22, in <module>
AttributeError: module 'raypoolkit' has no attribute 'DatastorePool'


======================================================================
FAIL: test_the_package_imports_with_no_client (raypoolkit.tests.test_package_imports.TestPackageImports.test_the_package_imports_with_no_client)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/tests/test_package_imports.py", line 107, in test_the_package_imports_with_no_client
    self.assertEqual(result.returncode, 0, result.stderr)
AssertionError: 1 != 0 : Traceback (most recent call last):
  File "<string>", line 3, in <module>
ImportError: cannot import name 'DatastorePool' from 'raypoolkit' (/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py)


----------------------------------------------------------------------
Ran 3 tests in 1.972s

FAILED (failures=2)
```

*Supplementary:* only the class's re-export removed — suite exit 1, **test 3 alone** fails, on the
facts `module's class is the package's`, `package attribute is a class` and `package attribute is
named RayWorkPool`; test 2 passes (deviation 7):

```diff
diff --git a/raypoolkit/__init__.py b/raypoolkit/__init__.py
--- a/raypoolkit/__init__.py
+++ b/raypoolkit/__init__.py
@@ -1,4 +1,3 @@
-from raypoolkit.RayWorkPool import RayWorkPool
 from raypoolkit.contract import DatastorePool
 
 __all__ = ["RayWorkPool", "DatastorePool"]
```

## 5. Observations not acted on

1. **A kept comment names the client's `Datastore` service.** `raypoolkit/RayWorkPool.py:424`, an
   SGK comment kept as it is (prompt §2.4), says "submit a store request to the Datastore service".
   `CLAUDE.md` says the package names no client class, module or package in comments. Opened as
   `[01-a-kept-comment-names-the-datastore-service]`, for 04, which rewrites the module's wording
   anyway. The other mentions of "datastore" in the module (`:430`, `:451`, `:502`'s "emplaced in
   the datastore", `:574`) are lower-case and generic.
2. **Two mentions of client modules are required by the prompt**, and so are not opened as issues:
   `_timing.py`'s docstring names SGK's `utilities.py` at `b510bc9` (D-int requires it), and the
   guard's test 2 names `Datastore`, `RayTools` and `utilities` as modules that must not be loaded
   (§2.7). Both are inside `raypoolkit/`. If `CLAUDE.md`'s "names no client" is meant to except
   provenance and the guard's list, it may want to say so; that is not this prompt's to change.
3. **The guard cannot run its first test when the package itself does not import** (deviation 6).
   The suite still fails, with the import error naming the module. Not a defect; no issue opened.
4. **Test 2 does not check what `from raypoolkit import RayWorkPool` binds.** With only the class's
   re-export removed it passes, because the import falls back to the submodule; test 3 catches that
   case. Not acted on; no issue opened.
5. **The board's line for fault 2.** It cites SGK `:488-491`; the orchestrator's brief says "the
   call at `:489`". At `b510bc9` (and in the package), `:489` is the `elif`, and the call
   `self._post_handler(obj)` is at `:490`; the branch runs `:487-492`, comments included. The board's
   §3 now gives the package's lines (§3.6).
6. **`pip freeze` records the editable install against `310db6e`**, the `HEAD` when it was
   installed (`-e git+https://github.com/ds283/RayPoolKit.git@310db6e…#egg=raypoolkit`). The
   install points at the checkout, so it follows the tree; the hash in the line is informational.
7. `pip install -e .` left `raypoolkit.egg-info/` at the repository root; it is gitignored and not
   staged.

## 6. Issues

**Opened:** `[01-a-kept-comment-names-the-datastore-service]` (board §3; owner 04). **Closed:**
none. **Changed:** the five `[00-…]` entries each gain a **Package:** line giving where the fault
sits in `raypoolkit/RayWorkPool.py` (§3.6). The index goes from 5 to **6** open.

## 7. State handed to the next prompt

- `HEAD` is `49f3ddf`. The package `raypoolkit` `0.1.0.dev0` is installed editable in `venv/`.
- **Suite: 3 tests**, all passing (`test_package_imports`).
- `./venv/bin/python docs/extraction/compare_with_source.py` exits 0; 02 and 03 run it (README §5
  rule 8). A prompt that adds a `.py` file under `raypoolkit/` must declare it in the check's
  `NO_SOURCE` (02's stand-ins and tests among them), or the check fails.
- **U4's consequence:** `raypoolkit.RayWorkPool` is the class. Patch the module through a string
  target (`"raypoolkit.RayWorkPool.ray"`) or `sys.modules["raypoolkit.RayWorkPool"]`, never through
  the package attribute (test 3's docstring).
- Package line numbers equal SGK's at `b510bc9`; the five faults are where §3.6 says.
- The U5 freeze is in force from `49f3ddf` (`PROVENANCE.md`).
- No tag; `ray` is unbounded in `pyproject.toml` until 03.
