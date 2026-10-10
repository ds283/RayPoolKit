# Prompt 01 — import the pool

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- G1 holds. SGK's `RayTools/RayWorkPool.py` is blob **`b4666fa`** at SGK **`b510bc9`**, which is
  the **import commit** (re-checked 2026-10-10 at this prompt's writing).
- U1–U5 are taken (README §6.2).
- `git status` is clean in this repository.

**Closes:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus**. The work is small and mechanical, but every later prompt and every
client's adoption stands on it, and the equivalence check (§2.5) has to be written so that it would
catch a real difference, not only pass on this one.

**Read first:**

1. [`README.md`](README.md): §0.2, §1, §4 (the module map), §5 (all of it, rule 8 especially) and
   §6.2 (U2–U5).
2. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`, in particular "What this repository is"
   and "Repository mechanics".
3. In SGK at `b510bc9`, **read with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   b510bc9:<path>`**, never from SGK's working tree, which may have moved on:
   - `RayTools/RayWorkPool.py` (575 lines) and `RayTools/__init__.py` (empty);
   - `utilities.py`, lines 20–22 (`SECONDS_PER_MINUTE`, `SECONDS_PER_HOUR`, `SECONDS_PER_DAY`)
     and 25–61 (`format_time`).
4. For the protocol of §2.3 only: `datastorekit/SQL/ShardedPool.py`'s `object_store(self, objects)`,
   read with `git -C /Users/ds283/Documents/Code/DatastoreKit show v0.2.0:<path>` (`:3339` at the
   tag; DatastoreKit's working tree moves). Read it; do not import it.

Line numbers below are SGK's at `b510bc9`.

---

## 1. What is wanted

The package `raypoolkit` exists in this repository. Its `RayWorkPool` module is SGK's at
`b510bc9`, changed only in the ways §2.4 lists. A script proves that, line by line. The package
imports in a venv that can see no client and no `datastorekit`, and a guard test keeps it that way.

**No behaviour changes.** The five inherited faults the board's §3 holds are imported as they are:
04 fixes them. A further defect noticed in SGK's code is recorded, not fixed (README §5 rules 4
and 8).

---

## 2. What to change

### 2.1 The venv

`venv/` exists from set-up (Python 3.12.15 from `/opt/local/bin/python3.12`, `ray==2.43.0`,
`black==25.1.0`; gitignored). Do not recreate it. Install the package into it editable
(`./venv/bin/python -m pip install -e .`), so the tests import the package the way a client will.
Record `pip freeze` in the log.

### 2.2 The package skeleton

- `pyproject.toml`: a setuptools build (as DatastoreKit's: `setuptools>=64`,
  `setuptools.build_meta`); name `raypoolkit`; version `0.1.0.dev0`; `requires-python = ">=3.12"`;
  the single dependency `ray`, with no bounds yet, since 03 sets the range (U7). Packages are found
  by `include = ["raypoolkit*"]`; the test package is included for now (03 decides whether the
  wheel carries it).
- `raypoolkit/__init__.py`, new: re-exports `RayWorkPool` and `DatastorePool` (U4) and lists them
  in `__all__`. Nothing else.
- `raypoolkit/tests/__init__.py`, new and empty.

**U4's consequence, stated here so that no later prompt trips on it.** Once `__init__.py` binds
the class, the package attribute `raypoolkit.RayWorkPool` is the **class**, and shadows the
submodule of the same name: `import raypoolkit.RayWorkPool as m` also gives the class. The module
stays reachable as `sys.modules["raypoolkit.RayWorkPool"]`, by
`importlib.import_module("raypoolkit.RayWorkPool")`, by `from raypoolkit.RayWorkPool import …`,
and through a string target to `unittest.mock.patch` such as `"raypoolkit.RayWorkPool.ray"`
(each measured at Python 3.12.15 and 3.13.16 on a two-file package of the same shape, 2026-10-10).
§2.7's third test pins this.

### 2.3 The files, under README §4's names

| SGK at `b510bc9` | Here |
|---|---|
| `RayTools/RayWorkPool.py` | `raypoolkit/RayWorkPool.py` |
| `utilities.py`'s `SECONDS_PER_*` and `format_time` (lines 20–22, 25–61) | `raypoolkit/_timing.py` (those, nothing else) |
| `RayTools/__init__.py` (empty) | no counterpart: `raypoolkit/__init__.py` is new (§2.2) |
| — | `raypoolkit/contract.py`, new |

**`raypoolkit/contract.py`** holds one class, `DatastorePool`, a `typing.Protocol` describing the
pool a `RayWorkPool` is handed: the one method the default persist handler calls,
`object_store(self, objects) -> ObjectRef`, with the signature of DatastoreKit's
`ShardedPool.object_store`. Its docstring says, in this package's own terms:
- the pool is passed through to the store and persist handlers, and is otherwise unused;
- the protocol states what `_default_persist_handler` needs, and a caller whose handlers need
  more (or who passes `persist_handler=None`) may pass any object;
- it is not `runtime_checkable`, and nothing checks it at run time.

It imports only `typing` and `ray`. It names no client and no `datastorekit` class: the docstring
may say "a datastore pool", not which one.

### 2.4 The differences allowed, and no others

Each class below is allowed in the files it names. A difference that fits none of them is a stop
(§5).

- **D-imp — the import rewrite**, in `RayWorkPool.py`, exactly two lines:
  - `:8` `from Datastore.SQL.ShardedPool import ShardedPool` →
    `from raypoolkit.contract import DatastorePool`;
  - `:9` `from utilities import format_time` → `from raypoolkit._timing import format_time`.
- **D-pool — the type hint**, in `RayWorkPool.py`, exactly one line: `:75` `pool: ShardedPool,` →
  `pool: DatastorePool,`. `ShardedPool` appears nowhere else in the source (lines 8 and 75 only).
- **D-int — the internalised definitions.** `_timing.py` holds SGK's lines 20–22 and 25–61 **byte
  for byte**, after a module docstring naming their source (SGK `utilities.py` at `b510bc9`) and
  saying they are internalised so that the package needs no client. `format_time` uses no import,
  so `_timing.py` has none.
- **D-fmt — formatting.** `black` 25.1.0 on every package file. SGK's `RayWorkPool.py` is
  black-clean under 25.1.0 (checked at this prompt's writing), and the rewritten lines are no
  longer, so this should change nothing. Any line `black` changes is reported in the log.

**Not allowed here, though they are wanted later:** the licence header and the "maker" wording
(`[00-messages-say-maker-and-the-module-has-no-licence-header]`), and every other fix of the
board's §3. All are 04's. The module keeps SGK's comments and docstrings as they are.

### 2.5 The equivalence check

`docs/extraction/compare_with_source.py`, kept in the repository, run from the root as
`./venv/bin/python docs/extraction/compare_with_source.py`. The SGK path, the import commit and
the expected blob of `RayTools/RayWorkPool.py` (`b4666fa89abb26829fd585b881947d7ef5172cea`) are
constants at its top.

- It checks the blob with `git -C <SGK> rev-parse <commit>:RayTools/RayWorkPool.py`, and exits
  non-zero if it differs.
- For `RayWorkPool.py`, it reads the source with `git -C <SGK> show <commit>:<path>`, diffs the
  two line by line, and puts **every** differing line pair in exactly one class of §2.4, **by
  rule, not by a list of line numbers**. A D-imp rule matches only an import statement whose only
  change is the mapped module path and imported name of §2.4; the D-pool rule matches only a
  parameter line whose only change is `ShardedPool` → `DatastorePool`. An added or deleted line
  is never classified.
- For `_timing.py`, it parses both files with `ast` and requires each of the four definitions to
  have a source segment equal to SGK's, and the module to hold nothing else but its docstring.
- It walks `raypoolkit/` and requires every `.py` file to be either a §2.3 file with a source or
  one of the declared new files (`__init__.py`, `contract.py`, `tests/__init__.py` and the guard
  of §2.7). An undeclared file fails the check, so a later prompt that adds one must declare it.
- It prints, for each file, the count per class and **every line it could not classify**, and
  exits non-zero if any line is unclassified or any file is missing or undeclared.

**Show that the check bites.** With the tree otherwise correct, introduce each of these changes
separately, show that the script exits non-zero and names what is wrong, then revert:
- (a) `DEFAULT_MAX_TASK_QUEUE = 201` in `RayWorkPool.py`;
- (b) an extra `import os` in `RayWorkPool.py`;
- (c) the "available" rate regressed to the CPBH/SI form,
  `self._last_num_available_complete = self._num_store_complete`;
- (d) one deleted line in `RayWorkPool.py`;
- (e) `pool: ShardedPool` → `pool: object` (a hint change D-pool does not cover);
- (f) one changed literal in `_timing.format_time`;
- (g) an undeclared `raypoolkit/extra.py`.

### 2.6 Tests ported

None: no client has a test of the pool (README §0.2). The suite before this prompt is empty, and
02 writes the behavioural suite.

### 2.7 The package's import guard

New `raypoolkit/tests/test_package_imports.py`, three tests:

1. **Only allowed imports.** It parses every module under `raypoolkit/` with `ast` (tests
   included), collects every imported module, including imports inside functions and relative
   imports resolved against the package, and asserts that each one's root is in
   `sys.stdlib_module_names`, is `ray`, or is `raypoolkit`. `datastorekit` is therefore refused
   with any client package, and the failure message names the file, line and module.
2. **The package imports with no client.** In a fresh interpreter (`sys.executable -I`, run from
   a `tempfile` directory), `import raypoolkit; from raypoolkit import RayWorkPool, DatastorePool`
   succeeds, and afterwards none of `datastorekit`, `Datastore`, `RayTools` or `utilities` is in
   `sys.modules`.
3. **U4's re-export, pinned.** In a fresh interpreter: `raypoolkit.RayWorkPool` is the class;
   `sys.modules["raypoolkit.RayWorkPool"]` and `importlib.import_module("raypoolkit.RayWorkPool")`
   are the module; the module's `RayWorkPool` is the same object as the package's; and
   `raypoolkit.DatastorePool is raypoolkit.contract.DatastorePool`. The test's docstring states
   §2.2's consequence for later prompts: patch the module through a string target or
   `sys.modules`, never through the package attribute.

### 2.8 `PROVENANCE.md`

At the repository root, after DatastoreKit's `PROVENANCE.md` in form:
- the source repository, its URL and local checkout, the import commit `b510bc9` (full hash
  `b510bc90b66985532d28996ab4e5b13b0ff71709`) with its subject line, and the blob `b4666fa` of
  `RayTools/RayWorkPool.py`, last changed by `0ee16a8` ("Split RayWorkPool store_handler into
  store and persist handlers", 2026-09-04);
- that this is a fresh import (U2): SGK's history is not carried here;
- §2.3's table, and the new files with no source;
- §2.4's classes;
- how to re-run §2.5;
- **the U5 freeze:** from this prompt's commit until each client adopts (G2–G4), no client edits
  its `RayTools/`; a fix wanted in a client is made here and reaches it on adoption. The freeze is
  recorded here; this prompt does not edit any client to announce it.

---

## 3. Verification

1. In a **fresh shell with no `PYTHONPATH`**, from `/tmp`:
   ```bash
   /Users/ds283/Documents/Code/RayPoolKit/venv/bin/python -I -c "import raypoolkit; from raypoolkit import RayWorkPool, DatastorePool; from raypoolkit.RayWorkPool import RayWorkPool as R; assert R is RayWorkPool"
   ```
   succeeds. With `-c "import RayTools"`, and again with `-c "import datastorekit"`, it fails with
   `ModuleNotFoundError`, which shows that neither a client nor DatastoreKit is on the path.
2. `./venv/bin/python -m unittest discover -s raypoolkit/tests -t .` gives **`Ran 3 tests … OK`**:
   §2.7's three. The count before is 0 (there is no suite).
3. `compare_with_source.py` exits 0. Its whole output goes in the log; it should report two D-imp
   lines and one D-pool line in `RayWorkPool.py`, four matching definitions in `_timing.py`, and
   the declared new files.
4. **The breakage record.** Each item is a diff exactly as applied, with what failed. None is
   committed.
   - §2.5's (a)–(g), each failing the equivalence check;
   - an `import numpy` added inside a function of `RayWorkPool.py`, failing §2.7 test 1;
   - `from datastorekit.SQL.ShardedPool import ShardedPool` added to `contract.py`, failing §2.7
     test 1 (and test 2, if `datastorekit` happens to be importable; it is not in this venv, so
     record what test 2 does);
   - the re-export removed from `raypoolkit/__init__.py`, failing §2.7 tests 2 and 3.
5. `./venv/bin/black --check raypoolkit docs` is clean.

---

## 4. Acceptance

1. §2.2's and §2.3's files exist under their names, with `pyproject.toml` and `PROVENANCE.md`.
2. §3.1–§3.5 hold.
3. **The records**, in the same commit:
   - the log, `logs/01-import-the-pool.md`, per README §5.1. It also has `pip freeze`, the
     equivalence output and the test count before (0) and after (3);
   - this board: the header, §1's row for 01 (landed, commit, suite 3), and §3: for each of the
     five issues, the line in `raypoolkit/RayWorkPool.py` where the fault now sits, so 04 is
     pointed at the package rather than at SGK;
   - `prompts/INDEX.md`: the campaign's line;
   - `docs/OPEN_ISSUES.md`, if the work opens or changes anything.

---

## 5. Stop conditions — stop and ask the user

- G1 no longer holds: the blob of `RayTools/RayWorkPool.py` at `b510bc9` is not `b4666fa` (it
  cannot change for a fixed commit; if it reads differently, something is wrong with the checkout).
- The package module differs from its source in a way none of §2.4's classes covers, and making it
  fit would mean changing behaviour.
- The source imports, or the package needs, a module that is not the standard library, `ray`, or
  the package itself, beyond the two of §2.4.
- `black` 25.1.0 would reformat lines of `RayWorkPool.py` other than those §2.4 changes.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons or DatastoreKit.
  Reading SGK files, and DatastoreKit's one method at `v0.2.0`, through `git show` is
  the only access this prompt has.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `pyproject.toml`;
  - `raypoolkit/`, as §2.2, §2.3 and §2.7 list;
  - `docs/extraction/compare_with_source.py`;
  - `PROVENANCE.md`;
  - the log, this board and `prompts/INDEX.md`;
  - `docs/OPEN_ISSUES.md`, if needed.

  `.gitignore` already excludes `venv/` and `*.egg-info/`.
- It writes no behavioural test and no Ray stand-in (02).
- It sets no dependency range, adds no CI and makes no tag (03).
- It does not touch the repository's `README.md` or `CLAUDE.md`. Usage text is 03's.
- It fixes nothing in SGK's code, including the five faults of the board's §3, the licence header
  and the wording (04).

---

## 7. The log and the board

`logs/01-import-the-pool.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 01 (landed, commit, log, suite), and §3's
package line numbers.
