# Log — extraction prompt 03: supported versions and CI

**Subject:** Declare the supported versions and add CI, ready for v0.1.0 · **Commit:** this
commit · **Date:** 2026-10-10 · **Agent:** Claude Opus 5.5

**Result: landed.** `pyproject.toml` declares `0.1.0`, `ray>=2.43` (no ceiling) and the exclusion
of `raypoolkit.tests`; `.github/workflows/tests.yml` runs the suite at both ends of U7's range;
`README.md` is rewritten for a client. The suite is **116 → 116**, passing in `venv/` (3.12.15 /
2.43.0), in a fresh low-end venv (3.12.15 / 2.43.0) and in a fresh high-end venv (3.13.16 /
2.55.1), with no Ray process before or after any run. A wheel built from a fresh `git archive`
export passes the release check: `raypoolkit-0.1.0-py3-none-any.whl`, 12,016 bytes, 9 entries,
nothing under `raypoolkit/tests/`. (a)–(f) each fail as the prompt expects. No file under
`raypoolkit/` or `docs/extraction/` changed; `compare_with_source.py` exits 0 with 02's counts.
**One issue is opened** (§6, `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`), so the
index goes from 7 to **8**. **No tag was made and nothing was pushed**: `v0.1.0` is ready to be
tagged on this commit once CI passes there.

**Gate, re-checked at start.** `HEAD` was `e136eee` (the prompt written at `c73fc91`; `e136eee`
adds only an orchestrator note), the tree clean, the only worktree this checkout, no tag,
`origin/main` at `97f9ff0`. `venv/`: `Ran 116 tests … OK`, by module 3, 30, 12, 20, 22, 7, 17, 5.
The check exited 0 (572 identical, 2 D-imp, 1 D-pool, 4 D-int, 12 declared files, 0 undeclared).
`black --check raypoolkit docs`: 15 files unchanged. `pgrep -lf 'gcs_server|raylet|ray::'` was
empty (exit 1). Toolchain: `uv` 0.12.20 (`/opt/local/bin/uv`), `/opt/local/bin/python3.12` 3.12.15,
`/opt/local/bin/python3.13` 3.13.16. Every venv, export, wheel and driver script of this log is
under the agent's scratch directory (`…/scratchpad/agent03/`), written `$S` below.

## 1. What shipped

| File | What |
|---|---|
| `pyproject.toml` | `version = "0.1.0"` (from `0.1.0.dev0`); `dependencies = ["ray>=2.43"]` (from `"ray"`); `exclude = ["raypoolkit.tests", "raypoolkit.tests.*"]` under `[tool.setuptools.packages.find]`. Nothing else (§2.1) |
| `.github/workflows/tests.yml` | new: one job, `suite`, on `ubuntu-24.04`, matrix `low` (3.12.15 / 2.43.0) and `high` (3.13.16 / 2.55.1), `fail-fast: false`; checkout, setup-python, editable install with the pin, versions, the suite, and `black --check` on `low` only; `permissions: contents: read` (§2.5) |
| `README.md` | rewritten: Status, Supported versions, Installing, Using it, Developing; the opening paragraph, the DatastoreKit paragraph and the licence kept (§2.6) |
| this log, the board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md` | the records; the index gains one row (§6) |

The diff to `pyproject.toml`, as committed:

```diff
@@ -4,12 +4,13 @@ build-backend = "setuptools.build_meta"
 
 [project]
 name = "raypoolkit"
-version = "0.1.0.dev0"
+version = "0.1.0"
 description = "A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks"
 requires-python = ">=3.12"
 dependencies = [
-    "ray",
+    "ray>=2.43",
 ]
 
 [tool.setuptools.packages.find]
 include = ["raypoolkit*"]
+exclude = ["raypoolkit.tests", "raypoolkit.tests.*"]
```

## 2. Deviations from the prompt

The orchestrator's brief added eight clarifications (1–8 below). Each is an **IMPLEMENTATION
CHOICE at the orchestrator's direction**.

1. **The editable installs from the repository root rewrote the gitignored
   `raypoolkit.egg-info/`** (clarification 1): `venv/`'s reinstall and the low and high venvs'
   installs left it at 13:13, saying `Version: 0.1.0` and `Requires-Dist: ray>=2.43`. It is never
   staged, and `git status` shows it only under `--ignored`. No wheel was built in the tree. (Its
   `SOURCES.txt` is another matter: §6.1.)
2. **`venv/`'s metadata was checked with `importlib.metadata`** (clarification 2), before and after
   the reinstall: `0.1.0.dev0 ['ray']` → `0.1.0 ['ray>=2.43']`. Both `pip freeze` outputs are
   recorded (§3.2); they are identical.
3. **`uv`'s cache at `~/.cache/uv` was used** (clarification 3), neither bypassed nor cleaned.
   Every resolve of §3 finished in under 25 ms.
4. **The matrix** (clarification 4) is `strategy.matrix.include`, two entries keyed `end: low|high`,
   every version a quoted string; the job is named `suite (${{ matrix.end }})`; step 6 runs under
   `if: matrix.end == 'low'`.
5. **The actions are referenced as `actions/checkout@v7` and `actions/setup-python@v7`**
   (clarification 5), not pinned to a SHA.
6. **The README gives the three default handlers by what they do** ("calls `obj.compute(**kwargs)`",
   "calls `obj.store()`", "calls `pool.object_store(obj)`") and the sizes as values, never by the
   private names `_default_*_handler` or `DEFAULT_*` (clarification 6). §4 records each default
   with the body it was read from.
7. **The README's printed-line examples are copied from one pinned whole-run test**
   (clarification 7):
   `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`.
   They were taken from the lines that test compares, captured by running the test itself (§4.2),
   not composed. The README says the stamps, counts, times and rates are illustrative.
8. **The breakage diffs to `pyproject.toml` are written against this commit's `pyproject.toml`**
   and applied with `git apply` inside fresh exports (clarification 8); the repository's
   `pyproject.toml` was touched only by §2.1's edit. (b) and (c) are `uv pip install --dry-run`
   into a throwaway 3.12 venv.

Choices of this prompt's agent:

9. **Step 6's install is a no-op locally.** §2.3 installs `black==25.1.0` in the same resolve as
   the package; the workflow installs it in step 6 instead, on `low` only. The replay ran step 6's
   install anyway (`Checked 1 package`), then `black --check`. **STRUCTURALLY REQUIRED**: §2.3 and
   §2.5 install `black` at different points.
10. **Workflow steps with no local counterpart**: step 1 (`actions/checkout@v7`; the replay ran on
    the working tree, which equals this commit's for every file the suite reads); step 2
    (`actions/setup-python@v7`; stood in for by `uv venv --python /opt/local/bin/python3.1x`,
    MacPorts' builds, not the Actions builds); and step 3's `python -m pip install --upgrade pip`
    (a `uv` venv has no `pip`). **STRUCTURALLY REQUIRED**: GitHub cannot run here.
11. **(a) and (b) are recorded as diffs to `.github/workflows/tests.yml`**, the file this commit
    adds, each checked with `git apply --check` against it. What ran for (a) was the install
    command with `-e .` removed; for (b), the install command with the pin `ray==2.42.1`.
    **IMPLEMENTATION CHOICE**, so that each is replayable from this commit.
12. **(c)'s dry-run carries the low end's pin**, `-e <export> "ray==2.43.0"`, i.e. the low end's
    step 3 with (c) applied. **IMPLEMENTATION CHOICE.**
13. **The release check is a script** (`$S/scripts/release_check.py`, not committed, reproduced in
    §3.6) that makes every check of §2.4 and prints PASS or FAIL for each. It checks the wheel's
    file list exactly (the four modules; `LICENSE`, `METADATA`, `WHEEL`, `top_level.txt` and
    `RECORD` under `dist-info`). It was reused unchanged for (d)–(f). **IMPLEMENTATION CHOICE.**
14. **The README says a little more than §2.6 lists**, each item checked (§4): that `task_list` is
    consumed at construction and should be a sequence with `store_results=True`; that an object
    whose `available` is false, in a pool with no compute handler, is left as it is and the post
    handler is not called (pinned by `test_run_paths.TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing`);
    that a compute handler with `persist_handler=None` raises `RuntimeError`; that the persisted
    object must have `available` true; and that the suite's test base refuses `ray.init`. No fault
    is listed: the board is pointed at, and the one fault the prompt asks to be stated
    (`persist_handler=None`) is. **IMPLEMENTATION CHOICE.**
15. **Measurements beyond the prompt**, all in scratch: `uv pip compile --only-binary ray` for
    Ray 2.43.0, 2.44.0, 2.44.1 and 2.45.0 on Python 3.13 (macOS arm64 and manylinux x86_64), and
    unpinned `ray>=2.43` on 3.13 and 3.14, to check the README's statements (§3.8); and two wheel
    builds, export-g and export-h, behind the issue of §6.1. **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT.

## 3. Verification performed

### 3.1 The suite, by venv (prompt §3.1)

Every run from the repository root, `<python> -m unittest discover -s raypoolkit/tests -t .`
(with `-v` for the per-module count), in the foreground, its output written to a file in `$S` and
the verdict grepped from it. `pgrep -lf 'gcs_server|raylet|ray::'` was empty (exit 1) before and
after every run.

| Venv | `sys.version` | `ray.__version__` | `raypoolkit` | Verdict |
|---|---|---|---|---|
| `venv/`, before any change | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | `0.1.0.dev0`, editable | `Ran 116 tests in 2.331s` `OK` |
| `venv/`, after §2.1/§2.4 and the reinstall | as above | 2.43.0 | `0.1.0`, editable | `Ran 116 tests in 1.690s` `OK` |
| `$S/venv-low` (fresh) | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | `0.1.0`, editable | `Ran 116 tests in 3.455s` `OK` |
| `$S/venv-high` (fresh) | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | `0.1.0`, editable | `Ran 116 tests in 3.605s` `OK` |
| `venv/`, after every change (final) | as above | 2.43.0 | `0.1.0`, editable | `Ran 116 tests in 0.874s` `OK` |
| `$S/venv-low`, final | as above | 2.43.0 | `0.1.0`, editable | `Ran 116 tests in 0.810s` `OK` |
| `$S/venv-high`, final | as above | 2.55.1 | `0.1.0`, editable | `Ran 116 tests in 0.828s` `OK` |

By module, in every run: `test_package_imports` 3, `test_standins` 30, `test_construction` 12,
`test_task_builder` 20, `test_run_paths` 22, `test_scheduling` 7, `test_printed_lines` 17,
`test_inherited_faults` 5. **Before: 116. After: 116.** No warning was printed at either end: the
only lines matching "warning" in any output are test names.

In every venv, `raypoolkit.__file__` is `/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py`
(the editable install), and `importlib.metadata` gives `0.1.0 ['ray>=2.43']`.

### 3.2 `venv/`'s reinstall (prompt §2.3)

```
$ ./venv/bin/python -m pip install --no-deps -e .
Obtaining file:///Users/ds283/Documents/Code/RayPoolKit
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Checking if build backend supports build_editable: started
  Checking if build backend supports build_editable: finished with status 'done'
  Getting requirements to build editable: started
  Getting requirements to build editable: finished with status 'done'
  Preparing editable metadata (pyproject.toml): started
  Preparing editable metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: raypoolkit
  Building editable for raypoolkit (pyproject.toml): started
  Building editable for raypoolkit (pyproject.toml): finished with status 'done'
  Created wheel for raypoolkit: filename=raypoolkit-0.1.0-0.editable-py3-none-any.whl size=6981 sha256=7d6f5d700e280bab1e90de3c256a55a64b74a1d2b4892e6529f734425495788f
  Stored in directory: /private/var/folders/tm/y9rd_z8x1ks3m09yhkjc0h7800128f/T/pip-ephem-wheel-cache-uq5erktr/wheels/ae/ed/ff/e9451c3e44c61597c01d5d3317ab13f852c264ea133ef6e862
Successfully built raypoolkit
Installing collected packages: raypoolkit
  Attempting uninstall: raypoolkit
    Found existing installation: raypoolkit 0.1.0.dev0
    Uninstalling raypoolkit-0.1.0.dev0:
      Successfully uninstalled raypoolkit-0.1.0.dev0
Successfully installed raypoolkit-0.1.0
```

`pip` 26.2.1. `importlib.metadata.version("raypoolkit")`, `requires("raypoolkit")`: before
`0.1.0.dev0 ['ray']`, after `0.1.0 ['ray>=2.43']`. `pip freeze`, before and after, identical, as
printed:

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
-e git+https://github.com/ds283/RayPoolKit.git@e136eee06d490fd9050977ceb5aac9a86102e106#egg=raypoolkit
referencing==0.37.0
requests==2.34.2
rpds-py==2026.9.1
typing_extensions==4.16.0
urllib3==2.8.0
```

### 3.3 The fresh venvs, and the workflow replayed (prompt §2.3, §2.5)

Each command as run, with the workflow step it stands for. `R` is the repository root, the working
directory of every command.

| Workflow step | Low end, as run | High end, as run |
|---|---|---|
| 1. `actions/checkout@v7` | none (the working tree; deviation 10) | none |
| 2. `actions/setup-python@v7`, `python-version: ${{ matrix.python }}` | `uv venv --python /opt/local/bin/python3.12 $S/venv-low` | `uv venv --python /opt/local/bin/python3.13 $S/venv-high` |
| 3. `python -m pip install --upgrade pip` | none (deviation 10) | none |
| 3. `python -m pip install -e . "ray==${{ matrix.ray }}"` | `uv pip install --python $S/venv-low/bin/python -e . "ray==2.43.0" "black==25.1.0"` | `uv pip install --python $S/venv-high/bin/python -e . "ray==2.55.1" "black==25.1.0"` |
| 4. versions | `$S/venv-low/bin/python -c "import sys, ray; print('python', sys.version); print('ray', ray.__version__)"` | the same with `venv-high` |
| 5. the suite | `$S/venv-low/bin/python -m unittest discover -s raypoolkit/tests -t . -v` | the same with `venv-high` |
| 6. `python -m pip install black==25.1.0` (low only) | `uv pip install --python $S/venv-low/bin/python "black==25.1.0"` → `Checked 1 package in 23ms` | not run (`if: matrix.end == 'low'`) |
| 6. `black --check raypoolkit docs` (low only) | `$S/venv-low/bin/black --check raypoolkit docs` → `15 files would be left unchanged.`, exit 0 | not run |

Step 3's output, low end (one resolve; the pins satisfy `ray>=2.43`):

```
Using Python 3.12.15 environment at: $S/venv-low
Resolved 25 packages in 22ms
   Building raypoolkit @ file:///Users/ds283/Documents/Code/RayPoolKit
      Built raypoolkit @ file:///Users/ds283/Documents/Code/RayPoolKit
Prepared 1 package in 1.89s
Installed 25 packages in 205ms
 + aiosignal==1.4.0
 + attrs==26.1.0
 + black==25.1.0
 + certifi==2026.7.22
 + charset-normalizer==3.5.2
 + click==8.5.0
 + filelock==4.1.0
 + frozenlist==1.8.0
 + idna==3.20
 + jsonschema==4.26.0
 + jsonschema-specifications==2025.9.1
 + msgpack==1.2.3
 + mypy-extensions==1.1.0
 + packaging==26.3
 + pathspec==1.1.1
 + platformdirs==4.12.4
 + protobuf==7.36.2
 + pyyaml==6.0.3
 + ray==2.43.0
 + raypoolkit==0.1.0 (from file:///Users/ds283/Documents/Code/RayPoolKit)
 + referencing==0.37.0
 + requests==2.34.2
 + rpds-py==2026.9.1
 + typing-extensions==4.16.0
 + urllib3==2.8.0
```

High end:

```
Using Python 3.13.16 environment at: $S/venv-high
Resolved 22 packages in 14ms
   Building raypoolkit @ file:///Users/ds283/Documents/Code/RayPoolKit
      Built raypoolkit @ file:///Users/ds283/Documents/Code/RayPoolKit
Prepared 1 package in 2.03s
Installed 22 packages in 201ms
 + attrs==26.1.0
 + black==25.1.0
 + certifi==2026.7.22
 + charset-normalizer==3.5.2
 + click==8.5.0
 + filelock==4.1.0
 + idna==3.20
 + jsonschema==4.26.0
 + jsonschema-specifications==2025.9.1
 + msgpack==1.2.3
 + mypy-extensions==1.1.0
 + packaging==26.3
 + pathspec==1.1.1
 + platformdirs==4.12.4
 + protobuf==7.36.2
 + pyyaml==6.0.3
 + ray==2.55.1
 + raypoolkit==0.1.0 (from file:///Users/ds283/Documents/Code/RayPoolKit)
 + referencing==0.37.0
 + requests==2.34.2
 + rpds-py==2026.9.1
 + urllib3==2.8.0
```

Step 4's output: `python 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)]`
/ `ray 2.43.0`; and `python 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0
(clang-2100.3.34.2)]` / `ray 2.55.1`. Step 5's verdicts are §3.1's.

### 3.4 The workflow parses, and its matrix is §2.3's (prompt §3.4)

`$S/venv-high/bin/python -c "import yaml, sys; print(yaml.safe_load(open(sys.argv[1])))" .github/workflows/tests.yml`
(PyYAML 6.0.3):

```
{'name': 'tests', True: {'push': {'branches': ['main']}, 'pull_request': None, 'workflow_dispatch': None}, 'permissions': {'contents': 'read'}, 'jobs': {'suite': {'name': 'suite (${{ matrix.end }})', 'runs-on': 'ubuntu-24.04', 'strategy': {'fail-fast': False, 'matrix': {'include': [{'end': 'low', 'python': '3.12.15', 'ray': '2.43.0'}, {'end': 'high', 'python': '3.13.16', 'ray': '2.55.1'}]}}, 'steps': [{'uses': 'actions/checkout@v7'}, {'uses': 'actions/setup-python@v7', 'with': {'python-version': '${{ matrix.python }}'}}, {'name': 'Install the package, editable, with the pin', 'run': 'python -m pip install --upgrade pip\npython -m pip install -e . "ray==${{ matrix.ray }}"\n'}, {'name': 'Versions', 'run': 'python -c "import sys, ray; print(\'python\', sys.version); print(\'ray\', ray.__version__)"\n'}, {'name': 'The suite', 'run': 'python -m unittest discover -s raypoolkit/tests -t .'}, {'name': 'black', 'if': "matrix.end == 'low'", 'run': 'python -m pip install black==25.1.0\nblack --check raypoolkit docs\n'}]}}}
```

(`on` loads as `True`, YAML 1.1.) Checked from the loaded data: `include ==
[{'end': 'low', 'python': '3.12.15', 'ray': '2.43.0'}, {'end': 'high', 'python': '3.13.16',
'ray': '2.55.1'}]` is `True`, and every value is a `str`; the triggers are `push` to `main`,
`pull_request` and `workflow_dispatch`; `permissions` is `{'contents': 'read'}`; `fail-fast` is
`False`; one job, `suite`, on `ubuntu-24.04`; the only actions are `actions/checkout@v7` and
`actions/setup-python@v7`. No secret, cache, artefact or other action; nothing that reads a client.

### 3.5 The equivalence check (prompt §3.2)

`./venv/bin/python docs/extraction/compare_with_source.py`, exit **0**, before and after; the two
outputs are byte for byte identical. Whole output (after):

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

02's counts: 572 identical, 2 D-imp, 1 D-pool, 4 D-int, 12 declared files, 0 undeclared.

### 3.6 The release check (prompt §2.4, §3.3)

**The build.** One fresh export, one build, never in the repository tree (hazard 2):

```
mkdir $S/export-1 && git archive HEAD | tar -x -C $S/export-1
cp pyproject.toml $S/export-1/pyproject.toml        # the working tree's, §2.1 and §2.4
uv build --wheel --out-dir $S/dist-1 $S/export-1
```

The export held `.gitignore`, `CLAUDE.md`, `docs`, `LICENSE`, `prompts`, `PROVENANCE.md`,
`pyproject.toml`, `raypoolkit`, `README.md`, and no `build/`, `dist/` or `*.egg-info`.
`pyproject.toml` is the only file 03 changes that the build reads. The build's output:

```
Building wheel...
running egg_info
creating raypoolkit.egg-info
writing raypoolkit.egg-info/PKG-INFO
writing dependency_links to raypoolkit.egg-info/dependency_links.txt
writing requirements to raypoolkit.egg-info/requires.txt
writing top-level names to raypoolkit.egg-info/top_level.txt
writing manifest file 'raypoolkit.egg-info/SOURCES.txt'
reading manifest file 'raypoolkit.egg-info/SOURCES.txt'
adding license file 'LICENSE'
writing manifest file 'raypoolkit.egg-info/SOURCES.txt'
running bdist_wheel
running build
running build_py
creating build/lib/raypoolkit
copying raypoolkit/RayWorkPool.py -> build/lib/raypoolkit
copying raypoolkit/__init__.py -> build/lib/raypoolkit
copying raypoolkit/_timing.py -> build/lib/raypoolkit
copying raypoolkit/contract.py -> build/lib/raypoolkit
running egg_info
writing raypoolkit.egg-info/PKG-INFO
writing dependency_links to raypoolkit.egg-info/dependency_links.txt
writing requirements to raypoolkit.egg-info/requires.txt
writing top-level names to raypoolkit.egg-info/top_level.txt
reading manifest file 'raypoolkit.egg-info/SOURCES.txt'
adding license file 'LICENSE'
writing manifest file 'raypoolkit.egg-info/SOURCES.txt'
warning: build_py: byte-compiling is disabled, skipping.

installing to build/bdist.macosx-27.0-arm64/wheel
running install
running install_lib
creating build/bdist.macosx-27.0-arm64/wheel
creating build/bdist.macosx-27.0-arm64/wheel/raypoolkit
copying build/lib/raypoolkit/RayWorkPool.py -> build/bdist.macosx-27.0-arm64/wheel/./raypoolkit
copying build/lib/raypoolkit/__init__.py -> build/bdist.macosx-27.0-arm64/wheel/./raypoolkit
copying build/lib/raypoolkit/_timing.py -> build/bdist.macosx-27.0-arm64/wheel/./raypoolkit
copying build/lib/raypoolkit/contract.py -> build/bdist.macosx-27.0-arm64/wheel/./raypoolkit
warning: install_lib: byte-compiling is disabled, skipping.

running install_egg_info
Copying raypoolkit.egg-info to build/bdist.macosx-27.0-arm64/wheel/./raypoolkit-0.1.0-py3.14.egg-info
running install_scripts
creating build/bdist.macosx-27.0-arm64/wheel/raypoolkit-0.1.0.dist-info/WHEEL
creating '$S/dist-1/.tmp-_smo1ab2/raypoolkit-0.1.0-py3-none-any.whl' and adding 'build/bdist.macosx-27.0-arm64/wheel' to it
adding 'raypoolkit/RayWorkPool.py'
adding 'raypoolkit/__init__.py'
adding 'raypoolkit/_timing.py'
adding 'raypoolkit/contract.py'
adding 'raypoolkit-0.1.0.dist-info/licenses/LICENSE'
adding 'raypoolkit-0.1.0.dist-info/METADATA'
adding 'raypoolkit-0.1.0.dist-info/WHEEL'
adding 'raypoolkit-0.1.0.dist-info/top_level.txt'
adding 'raypoolkit-0.1.0.dist-info/RECORD'
removing build/bdist.macosx-27.0-arm64/wheel
Successfully built $S/dist-1/raypoolkit-0.1.0-py3-none-any.whl
```

**The wheel.**
- Name: `raypoolkit-0.1.0-py3-none-any.whl`
- Size: **12,016 bytes** (`wc -c`)
- Entries: **9**
- SHA-256: `875fe534d3a7b9dfb3c6d7caf8f20d0e46c0f08f7d06046cf729fe922869806d`
  (zip timestamps make it differ from build to build; the file list and contents are what
  reproduce)

| Entry | Size (bytes) |
|---|---|
| `raypoolkit/RayWorkPool.py` | 24,614 |
| `raypoolkit/__init__.py` | 137 |
| `raypoolkit/_timing.py` | 1,770 |
| `raypoolkit/contract.py` | 1,252 |
| `raypoolkit-0.1.0.dist-info/licenses/LICENSE` | 11,357 |
| `raypoolkit-0.1.0.dist-info/METADATA` | 243 |
| `raypoolkit-0.1.0.dist-info/WHEEL` | 91 |
| `raypoolkit-0.1.0.dist-info/top_level.txt` | 11 |
| `raypoolkit-0.1.0.dist-info/RECORD` | 728 |

Nothing under `raypoolkit/tests/`. `METADATA`:

```
Metadata-Version: 2.4
Name: raypoolkit
Version: 0.1.0
Summary: A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks
Requires-Python: >=3.12
License-File: LICENSE
Requires-Dist: ray>=2.43
Dynamic: license-file
```

**The install**, into a third fresh venv at the high end's pins, not editable:

```
$ uv venv --python /opt/local/bin/python3.13 $S/venv-wheel
$ uv pip install --python $S/venv-wheel/bin/python $S/dist-1/raypoolkit-0.1.0-py3-none-any.whl "ray==2.55.1"
Using Python 3.13.16 environment at: $S/venv-wheel
Resolved 18 packages in 18ms
Prepared 1 package in 11ms
Installed 18 packages in 199ms
 + attrs==26.1.0
 + certifi==2026.7.22
 + charset-normalizer==3.5.2
 + click==8.5.0
 + filelock==4.1.0
 + idna==3.20
 + jsonschema==4.26.0
 + jsonschema-specifications==2025.9.1
 + msgpack==1.2.3
 + packaging==26.3
 + protobuf==7.36.2
 + pyyaml==6.0.3
 + ray==2.55.1
 + raypoolkit==0.1.0 (from file://$S/dist-1/raypoolkit-0.1.0-py3-none-any.whl)
 + referencing==0.37.0
 + requests==2.34.2
 + rpds-py==2026.9.1
 + urllib3==2.8.0
```

**The check**, from an empty directory outside the repository, `PYTHONPATH` unset, `-I`:

```
$ cd $S/empty && env -u PYTHONPATH $S/venv-wheel/bin/python -I $S/scripts/release_check.py $S/dist-1/raypoolkit-0.1.0-py3-none-any.whl
cwd: $S/empty | PYTHONPATH: None | -I: 1
python: 3.13.16 | sys.path[0]: '/opt/local/Library/Frameworks/Python.framework/Versions/3.13/lib/python313.zip'
wheel: 9 entries, 0 under raypoolkit/tests/
PASS  file list: the four modules  [['raypoolkit/RayWorkPool.py', 'raypoolkit/__init__.py', 'raypoolkit/_timing.py', 'raypoolkit/contract.py']]
PASS  file list: LICENSE and the dist-info files  [['raypoolkit-0.1.0.dist-info/METADATA', 'raypoolkit-0.1.0.dist-info/RECORD', 'raypoolkit-0.1.0.dist-info/WHEEL', 'raypoolkit-0.1.0.dist-info/licenses/LICENSE', 'raypoolkit-0.1.0.dist-info/top_level.txt']]
PASS  file list: nothing under raypoolkit/tests/  [0]
PASS  import raypoolkit
PASS  from raypoolkit import RayWorkPool, DatastorePool
PASS  import_module('raypoolkit.RayWorkPool')  [$S/venv-wheel/lib/python3.13/site-packages/raypoolkit/RayWorkPool.py]
PASS  import_module('raypoolkit._timing')  [$S/venv-wheel/lib/python3.13/site-packages/raypoolkit/_timing.py]
PASS  import_module('raypoolkit.contract')  [$S/venv-wheel/lib/python3.13/site-packages/raypoolkit/contract.py]
PASS  raypoolkit.__file__ under the venv's site-packages  [$S/venv-wheel/lib/python3.13/site-packages/raypoolkit/__init__.py]
PASS  ray.is_initialized() is False  [ray 2.55.1]
PASS  import raypoolkit.tests raises ModuleNotFoundError  [No module named 'raypoolkit.tests']
PASS  version("raypoolkit") == "0.1.0"  [0.1.0]
PASS  requires("raypoolkit") == ["ray>=2.43"]  [['ray>=2.43']]
RESULT: OK (13 pass, 0 fail)
```

(Paths under the scratch directory are written `$S` here.) `pgrep` was empty afterwards. The wheel
is not committed; `git status` shows no `build/`, `dist/` or `*.egg-info`, and `--ignored` shows
only `raypoolkit.egg-info/`, `raypoolkit/__pycache__/` and `venv/`, as before.

The driver, `$S/scripts/release_check.py`, makes each check of §2.4 in turn: it lists the wheel
with `zipfile` and compares the four modules and the five `dist-info` entries exactly, and counts
entries under `raypoolkit/tests/`; it imports `raypoolkit`, the two names, and the three modules by
`importlib.import_module`; it compares `os.path.realpath(raypoolkit.__file__)` with the venv's
`sysconfig` `purelib`; it imports `ray` and asserts `ray.is_initialized() is False`; it expects
`ModuleNotFoundError` from `import raypoolkit.tests`; and it compares
`importlib.metadata.version` and `requires` with `0.1.0` and `['ray>=2.43']`. It exits 1 if any
fails.

### 3.7 `black` (prompt §3.5)

`./venv/bin/black --check raypoolkit docs` (25.1.0): "15 files would be left unchanged.", before
and after. No Python file was changed; `black` was not run on the workflow or the README.

### 3.8 The README's version statements, measured

`uv pip compile --only-binary ray --python-version 3.13`, with `--python-platform
aarch64-apple-darwin` and `x86_64-manylinux_2_28`: `ray==2.43.0`, `2.44.0` and `2.44.1` each give
"No solution found … has no wheels with a matching Python ABI tag (e.g., `cp313`)" on both;
`ray==2.45.0` resolves on both. Unpinned `ray>=2.43` resolves to `ray==2.59.0` on 3.13, on 3.14
(this machine's platform) and on 3.14 manylinux. So the README's "in effect 2.45.0 on 3.13", "2.43.0,
2.44.0 and 2.44.1 have none" and "Ray up to 2.59.0 today, Python 3.14" hold.

### 3.9 The hazards (prompt §2.2)

1. **The guard needs the package installed.** Confirmed by (a): with Ray but no `raypoolkit`, and
   `PYTHONPATH=.`, exactly tests 2 and 3 of `test_package_imports` fail, each child raising
   `ModuleNotFoundError: No module named 'raypoolkit'`; 114 pass. Every venv the suite ran in has
   the package installed editable (§3.1), and the workflow's step 3 installs it with `-e .`.
2. **A stale `build/` leaks the tests into the wheel.** Confirmed by (f): the second build in the
   same export, with the exclusion restored, shipped all ten test files from the first build's
   `build/lib/raypoolkit/tests/`. Every build of this log ran in its own fresh export, except (f),
   whose reuse is the point; none ran in the tree. **A second route was found**: a stale
   `raypoolkit.egg-info/SOURCES.txt` ships the tests too, as package data, whatever `build/`
   holds. The repository's own `raypoolkit.egg-info/` is such a manifest (§6.1, opened as an
   issue).
3. **Linux is not measured.** Nothing here stands in for it. The workflow is the first Linux run;
   the tag waits for it to pass at both ends.
4. **The newest versions are not tested.** Python 3.14 and Ray 2.59.0 are inside the declared range
   (§3.8). The README states the two tested ends, that newer releases are allowed but untested, and
   that a client pins its own Ray. No third CI job was added.
5. **The check cannot run in CI.** The workflow runs the suite and `black --check`, and nothing
   else (§3.4); its comment says the equivalence check runs locally only. The check ran here (§3.5).

## 4. The README's names, arguments and defaults

Every name the README gives was checked against the package by `$S/scripts/readme_names.py`, run
with `venv/`'s interpreter from the repository root (exit 0, **77 pass, 0 fail**), and the
signature was also dumped from the installed wheel in `$S/venv-wheel`, with `-I` from `$S/empty`
(18 parameters, no `self`; the same names and defaults).

### 4.1 How each was checked

| README name | How checked | Found |
|---|---|---|
| `from raypoolkit import RayWorkPool` | imported | a class |
| `raypoolkit.DatastorePool` | imported from the package root; `_is_protocol`; `_is_runtime_protocol` | the `typing.Protocol` of `contract.py`, not `runtime_checkable` |
| `object_store(obj)` returning an `ObjectRef` | `vars(DatastorePool)`; `inspect.signature(DatastorePool.object_store)` | its one public member, `(self, objects) -> ray._raylet.ObjectRef` |
| `ObjectRef` | `ray.ObjectRef` imported | a class |
| `run()` | `inspect.signature(RayWorkPool.run)` | `(self)` |
| `RayWorkPool(pool, task_list, task_builder, ...)` | `inspect.signature(RayWorkPool)` | 18 parameters, these three first, required, positional-or-keyword; `pool` annotated `DatastorePool` |
| `compute_handler`, default "calls `obj.compute(**kwargs)`" | signature default; its source | `_default_compute_handler`, `RayWorkPool.py:60-61`, `return obj.compute(**kwargs)` |
| `store_handler`, default "calls `obj.store()`" | signature default; its source | `_default_store_handler`, `:64-65`, `obj.store()` |
| `persist_handler`, default "calls `pool.object_store(obj)`" | signature default; its source | `_default_persist_handler`, `:68-69`, `return pool.object_store(obj)` |
| `available_handler`, `validation_handler`, `post_handler`, `label_builder`, each `None` | signature defaults | `None` |
| `create_batch_size=5`, `process_batch_size=1`, `max_task_queue=200` | signature defaults (value and type) | 5, 1, 200 (`int`) |
| `notify_min_time_interval=60`, `notify_time_interval=300`, `notify_batch_size=500` | signature defaults | 60, 300, 500 (`int`) |
| `title=None`, `store_results=False` | signature defaults | `None`, `False` |
| no private name in the README | text search for `_default_` and `DEFAULT_` | none |
| every parameter named; no argument-like name that is not one | text search against `sig.parameters` | all 18 named; none extra |
| what each handler is given | read from `RayWorkPool.py` | compute `(obj, **compute_args)` at `:384-386`, `label=` from `:375-377`, `payload=` from `:379-382`; store `(obj, self._pool)` at `:431`; persist `(obj, self._pool)` at `:441`; available `(obj)` at `:348`; validation `(replacement_obj)` at `:475`; post `(obj)` at `:362`, `:399`, `:418`, `:490`, `:514`; `label_builder(obj)` at `:370-374` |
| what each returns, and what the pool does with it | read | compute, persist, available and validation each return a ref the pool puts in flight; the store handler's return is not read (`:431`); the available task's value is not fetched (the `"available"` branch has no `ray.get`); the persisted object is fetched (`:455`), must satisfy `available` (`:458-461`) and replaces the `results` entry (`:463-464`); a validation value `is not True` prints the warning (`:500-503`); a post handler's non-`None` return replaces the `results` entry only with `store_results` (e.g. `:363-364`) |
| the four task-builder returns, and `RuntimeError` otherwise | read | `ObjectRef` (`:281-282`); dict with `"ref"` and optional `"compute_payload"` (`:271-279`); list, tuple or set (`:296-307`); `None` (`:289-294`); else `RuntimeError` (`:284-287`); the two `store_results` refusals at `:290-293` and `:301-304` |
| the paths of an object | read; and the pinning tests | `hasattr(obj, "available")` at `:344`; available true at `:345`; false with a compute handler at `:366-368`; false without one, nothing (`test_run_paths.TestNotAvailable.test_not_available_without_a_compute_handler_does_nothing`); no attribute at `:394-401` |
| `results` only with `store_results=True`; `total_time` only with a `title` | constructor and `run()` source | `:137-139`; `:563-565` |
| "the sizes" and "the notifications" | read | `:250` (`max_task_queue`), `:252` (`create_batch_size`), `:315` (`process_batch_size`); `:526-533` (the strict `>` comparisons of the three notification settings at `:528`, `:531`, `:532`; `_batch` counting completed tasks at `:521`) |
| "Without one it prints nothing but the validation warning" | read: every `print` in the module | `:166` (banner), `:548`, `:552` (progress pair), `:566-575` (completion), all under `title`; `:501` (the warning), unconditional |
| `RuntimeWarning` for a persist handler without a compute handler; `RuntimeError` for the converse | constructor source | `:94-102` |
| `[00-the-constructor-checks-its-handlers-unevenly]` | text search of the board | present |
| `Work`, `Blob`, `StandinDatastorePool` in `raypoolkit/tests/standins.py` | imported; instances inspected | `Work` has `available`, `compute`, `store`; `Blob` has no `available`; `StandinDatastorePool().object_store` callable |
| files named: `PROVENANCE.md`, `LICENSE`, `.github/workflows/tests.yml`, `raypoolkit/tests/standins.py`, `raypoolkit/tests/test_printed_lines.py`, `docs/extraction/compare_with_source.py`, `prompts/extraction/README.md`, `prompts/extraction/IMPLEMENTATION_STATE.md` | `os.path.exists` | all exist |
| "not installed with the package" | the release check | `import raypoolkit.tests` raises `ModuleNotFoundError` from the wheel |
| the supported versions | §3.1, §3.8 | as stated |

### 4.2 The printed-line examples

Copied from
`test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`.
`$S/scripts/render_lines.py` ran that test with `unittest.TestCase.assertEqual` wrapped to record
the first list it compares, and printed it: the test passed, the actual lines equalled the
expected, and they were:

```
''
'** Stage one'
'   -- 2026-10-10 12:00:02 (1s running): 0/2 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)'
'      inflight: 1 lookup | completed: 1 lookup (avg 60/min)'
'   -- 2026-10-10 12:00:04 (3s running): 0/2 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)'
'      inflight: 0 lookup | completed: 2 lookup (60/min, avg 40/min)'
'   -- ALL WORK ITEMS COMPLETE in time 5s'
'      Queue summary: 2 lookup (avg 24/min)'
'      (no compute items were evaluated - all assets read from datastore)'
```

The README shows the banner (line 2, after the empty line 1), the first progress pair (lines 3–4)
and the completion lines (7–9), each as printed, leading spaces included. `readme_names.py`
confirms each is a line of the README and of the test module (the progress line through the
test's own `progress(...)` helper, as rendered above).

## 5. The deliberate-breakage record (prompt §3.6)

Each change exactly as applied. None is committed. `git status` was the same after each (the three
intended changes, ` M README.md`, ` M pyproject.toml`, `?? .github/`, and nothing else). Every
diff was checked with `git apply --check` in the repository; those applied in an export were also
checked there with `git apply --check` before and `git apply -R --check` after. Throwaway venvs and
exports were used throughout; the low, high and wheel venvs were not touched.

### (a) The workflow's install without the package

The diff (workflow step 3, `-e .` removed):

```diff
diff --git a/.github/workflows/tests.yml b/.github/workflows/tests.yml
--- a/.github/workflows/tests.yml
+++ b/.github/workflows/tests.yml
@@ -36,7 +36,7 @@ jobs:
       - name: Install the package, editable, with the pin
         run: |
           python -m pip install --upgrade pip
-          python -m pip install -e . "ray==${{ matrix.ray }}"
+          python -m pip install "ray==${{ matrix.ray }}"
 
       - name: Versions
         run: |
```

As run, at the high end:

```
uv venv --python /opt/local/bin/python3.13 $S/venv-break-a
uv pip install --python $S/venv-break-a/bin/python "ray==2.55.1"     # 17 packages, no raypoolkit
PYTHONPATH=. $S/venv-break-a/bin/python -m unittest discover -s raypoolkit/tests -t .
```

`find_spec('raypoolkit')` under `-I` was `None`. Result: **`Ran 116 tests` `FAILED (failures=2)`**,
exactly:
- `test_package_imports.TestPackageImports.test_the_class_is_re_exported_and_shadows_its_module`
- `test_package_imports.TestPackageImports.test_the_package_imports_with_no_client`

each with `AssertionError: 1 != 0` over a child traceback ending
`ModuleNotFoundError: No module named 'raypoolkit'`. The other 114 pass (hazard 1). No Ray process
before or after.

### (b) The Ray floor

The diff (workflow step 3 with `ray==2.42.1`):

```diff
diff --git a/.github/workflows/tests.yml b/.github/workflows/tests.yml
--- a/.github/workflows/tests.yml
+++ b/.github/workflows/tests.yml
@@ -36,7 +36,7 @@ jobs:
       - name: Install the package, editable, with the pin
         run: |
           python -m pip install --upgrade pip
-          python -m pip install -e . "ray==${{ matrix.ray }}"
+          python -m pip install -e . "ray==2.42.1"
 
       - name: Versions
         run: |
```

As run: `uv venv --python /opt/local/bin/python3.12 $S/venv-break-bc`, then
`uv pip install --dry-run --python $S/venv-break-bc/bin/python -e . "ray==2.42.1"`. Exit 1:

```
Using Python 3.12.15 environment at: $S/venv-break-bc
error: No solution found when resolving dependencies
  cause: Because only raypoolkit==0.1.0 is available and raypoolkit==0.1.0 depends on ray>=2.43, we can conclude that all versions of raypoolkit depend on ray>=2.43.
         And because you require ray==2.42.1 and raypoolkit, we can conclude that your requirements are unsatisfiable.
```

Control: `ray==2.42.1` alone resolves in the same venv (`Would install 20 packages`, `+ ray==2.42.1`),
so the refusal is the package's `ray>=2.43`.

### (c) The Python floor

The diff, against this commit's `pyproject.toml`:

```diff
diff --git a/pyproject.toml b/pyproject.toml
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -6,7 +6,7 @@ build-backend = "setuptools.build_meta"
 name = "raypoolkit"
 version = "0.1.0"
 description = "A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks"
-requires-python = ">=3.12"
+requires-python = ">=3.13"
 dependencies = [
     "ray>=2.43",
 ]
```

As run:

```
mkdir $S/export-c && git archive HEAD | tar -x -C $S/export-c && cp pyproject.toml $S/export-c/pyproject.toml
(cd $S/export-c && git apply --check $S/diffs/c.diff && git apply $S/diffs/c.diff && git apply -R --check $S/diffs/c.diff)
uv pip install --dry-run --python $S/venv-break-bc/bin/python -e $S/export-c "ray==2.43.0"
```

Exit 1:

```
Using Python 3.12.15 environment at: $S/venv-break-bc
error: No solution found when resolving dependencies
  cause: Because the current Python version (3.12.15) does not satisfy Python>=3.13 and raypoolkit==0.1.0 depends on Python>=3.13, we can conclude that raypoolkit==0.1.0 cannot be used.
         And because only raypoolkit==0.1.0 is available and you require raypoolkit, we can conclude that your requirements are unsatisfiable.
```

### (d) An exclusion too broad

```diff
diff --git a/pyproject.toml b/pyproject.toml
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -13,4 +13,4 @@ dependencies = [
 
 [tool.setuptools.packages.find]
 include = ["raypoolkit*"]
-exclude = ["raypoolkit.tests", "raypoolkit.tests.*"]
+exclude = ["raypoolkit", "raypoolkit.tests", "raypoolkit.tests.*"]
```

As run: a fresh `$S/export-d` (archive, `pyproject.toml` copied, the diff applied there as in (c));
`uv build --wheel --out-dir $S/dist-d $S/export-d`; a throwaway `$S/venv-break-d` (3.13.16) with
the wheel and `ray==2.55.1`; the release check as in §3.6. The wheel:
`raypoolkit-0.1.0-py3-none-any.whl`, 5,258 bytes, SHA-256
`ded7c5ff84967eadfa93ed2772ad2f8665c37b4d6f4e3fe3e178dd5489f5af44`, **5 entries, all under
`dist-info/`**. The check, exit 1:

```
wheel: 5 entries, 0 under raypoolkit/tests/
FAIL  file list: the four modules  [[]]
PASS  file list: LICENSE and the dist-info files  [...]
PASS  file list: nothing under raypoolkit/tests/  [0]
FAIL  import raypoolkit  [ModuleNotFoundError("No module named 'raypoolkit'")]
FAIL  from raypoolkit import RayWorkPool, DatastorePool  [ModuleNotFoundError("No module named 'raypoolkit'")]
FAIL  import_module('raypoolkit.RayWorkPool')  [ModuleNotFoundError("No module named 'raypoolkit'")]
FAIL  import_module('raypoolkit._timing')  [ModuleNotFoundError("No module named 'raypoolkit'")]
FAIL  import_module('raypoolkit.contract')  [ModuleNotFoundError("No module named 'raypoolkit'")]
FAIL  raypoolkit.__file__ under the venv's site-packages  [not imported]
PASS  ray.is_initialized() is False  [ray 2.55.1]
PASS  import raypoolkit.tests raises ModuleNotFoundError  [No module named 'raypoolkit']
PASS  version("raypoolkit") == "0.1.0"  [0.1.0]
PASS  requires("raypoolkit") == ["ray>=2.43"]  [['ray>=2.43']]
RESULT: FAILED (6 pass, 7 fail)
```

(The `raypoolkit.tests` check passes here only because its parent is missing; the import checks
are what fail.)

### (e) The test package shipped

```diff
diff --git a/pyproject.toml b/pyproject.toml
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -13,4 +13,3 @@ dependencies = [
 
 [tool.setuptools.packages.find]
 include = ["raypoolkit*"]
-exclude = ["raypoolkit.tests", "raypoolkit.tests.*"]
```

As run: a fresh `$S/export-e`, the diff applied there; `uv build --wheel --out-dir $S/dist-e
$S/export-e`; a throwaway `$S/venv-break-e`; the release check. The wheel: 39,350 bytes, SHA-256
`fa537bc631cf78047b37d46ee58e1b7969f40dd7a6b02b6cb537523d32294fc3`, **19 entries, 10 under
`raypoolkit/tests/`** (`__init__.py`, `standins.py` and the eight `test_*.py`). The check, exit 1:

```
wheel: 19 entries, 10 under raypoolkit/tests/
FAIL  file list: the four modules  [[... the four modules and the ten raypoolkit/tests/ files ...]]
PASS  file list: LICENSE and the dist-info files  [...]
FAIL  file list: nothing under raypoolkit/tests/  [10]
PASS  import raypoolkit
PASS  from raypoolkit import RayWorkPool, DatastorePool
PASS  import_module('raypoolkit.RayWorkPool')  [...]
PASS  import_module('raypoolkit._timing')  [...]
PASS  import_module('raypoolkit.contract')  [...]
PASS  raypoolkit.__file__ under the venv's site-packages  [...]
PASS  ray.is_initialized() is False  [ray 2.55.1]
FAIL  import raypoolkit.tests raises ModuleNotFoundError  [it imported]
PASS  version("raypoolkit") == "0.1.0"  [0.1.0]
PASS  requires("raypoolkit") == ["ray>=2.43"]  [['ray>=2.43']]
RESULT: FAILED (10 pass, 3 fail)
```

### (f) A stale build

In `$S/export-e`, after (e)'s build had left `build/` and `raypoolkit.egg-info/` there:
`git apply -R --check $S/diffs/e.diff && git apply -R $S/diffs/e.diff` (the exclusion restored;
the export's `pyproject.toml` then equals this commit's, by `diff`); `build/lib/raypoolkit/tests/`
still held the ten files; `uv build --wheel --out-dir $S/dist-f $S/export-e`. The build added
`raypoolkit/tests/__init__.py` and the nine other test files to the wheel. The wheel: 39,350 bytes,
SHA-256 `a65837356de9c099c86fa2bea73343f926d7eafbc040357ab294cfc72f9a052a`, **19 entries, 10 under
`raypoolkit/tests/`**, the same as (e)'s 19. Installed into a throwaway `$S/venv-break-f`, the check
exits 1:

```
wheel: 19 entries, 10 under raypoolkit/tests/
FAIL  file list: the four modules  [...]
FAIL  file list: nothing under raypoolkit/tests/  [10]
FAIL  import raypoolkit.tests raises ModuleNotFoundError  [it imported]
RESULT: FAILED (10 pass, 3 fail)
```

**Entry counts: (e) 19, (f) 19.** The file list fails (hazard 2), and so does the
`raypoolkit.tests` import, since the stale files are installed.

## 6. Observations not acted on

1. **A stale `egg-info` manifest ships the tests in a wheel, despite the exclusion.** setuptools
   reads an existing `raypoolkit.egg-info/SOURCES.txt` and merges it into the new one ("reading
   manifest file"). The repository's gitignored `raypoolkit.egg-info/`, rewritten by this prompt's
   editable installs (clarification 1), still lists the ten files under `raypoolkit/tests/`,
   carried from the manifests written before the exclusion; a fresh export's lists none
   (`$S/export-1/raypoolkit.egg-info/SOURCES.txt`). Measured in scratch, never in the tree: a fresh
   export of `HEAD`, with this commit's `pyproject.toml` and the repository's
   `raypoolkit.egg-info/` copied in (`$S/export-g`), builds a wheel of **19 entries, 10 under
   `raypoolkit/tests/`**, shipped as package data of `raypoolkit`, with setuptools warning
   "Package 'raypoolkit.tests' is absent from the `packages` configuration". The same export with
   `[tool.setuptools]` `include-package-data = false` appended (`$S/export-h`) builds 9 entries and
   no warning. A client is not affected: a `git+…@v0.1.0` install builds from a fresh clone, which
   has no `egg-info`, as the release check's export did. It is a second route for hazard 2, open to
   anyone who builds a wheel in a working tree. Not fixed: §2.1 says `pyproject.toml` changes in
   nothing else. **Opened** as `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`.
2. **`uv build` ran setuptools under Python 3.14** in its isolated build environment
   (`raypoolkit-0.1.0-py3.14.egg-info` in the build output; `…/builds-v0/…/lib/python3.14/…` in
   export-g's warning), `uv`'s default interpreter here. The wheel is `py3-none-any` and its
   contents do not depend on it. No issue.
3. **`pip freeze`'s editable line names the `HEAD` at the time of the freeze**, not of the
   install: `venv/`'s editable install predates `e136eee`, yet both freezes print `@e136eee…`.
   Clarification 2's "the `HEAD` at the time of install" (and log 01 §5.6's) is so only when the
   two coincide. No issue.
4. **Tool-internal temporary directories outside the scratch directory**: `venv/`'s reinstall
   (the prompt's command) built in `pip`'s system temporary directory (`/private/var/folders/…`),
   and `uv build` builds its isolated environments under `~/.cache/uv/builds-v0/`. Neither is a
   file this prompt wrote, and neither is in the repository.
5. **(d)'s `raypoolkit.tests` check passes vacuously** when the parent package is missing. The
   other checks catch (d); the release check is right as a whole. No issue.
6. **A lookup-only pool may also pass `store_handler=None`**, as SGK's and SI's sites do; the
   constructor does not check it either way. The README asks only for `persist_handler=None`, as
   the prompt does.

## 7. Issues

**Opened:** `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` (board §3; not assigned,
proposed for 05). **Closed:** none. **Changed:** none. The index goes from 7 to **8** open.

## 8. State handed to the next prompt

- `HEAD` is this commit. `raypoolkit/` is unchanged since `b9f6dec` (the package since `49f3ddf`).
- **`pyproject.toml`**: `raypoolkit` `0.1.0`, `requires-python = ">=3.12"`, `ray>=2.43`, the test
  package excluded from the distribution. `venv/` holds `0.1.0`, editable.
- **Suite: 116 tests**, passing at 3.12.15 / 2.43.0 and 3.13.16 / 2.55.1 on macOS.
- **CI**: `.github/workflows/tests.yml`, never run. It runs on the first push of `main`.
- **`v0.1.0` is ready to be tagged on this commit once CI passes there at both ends.** No tag was
  made and nothing was pushed (README §5 rule 10). If CI fails, a fix prompt lands first.
- `compare_with_source.py` exits 0 with 02's counts; 04 is the first prompt that may change the
  module, and README §5 rule 8 ends with 03.
- The wheel is built from a fresh `git archive` export, never from a tree with a `build/` or an
  `egg-info/` (§6.1).
