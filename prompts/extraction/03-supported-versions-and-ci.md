# Prompt 03 — supported versions and CI, ready for `v0.1.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 02 landed (`b9f6dec`) and its review is recorded (`307ed96`).
- U7 is taken (README §6.2, 2026-10-10, as recommended).
- `git status` is clean in this repository, and the suite gives `Ran 116 tests … OK`.

**Closes:** nothing. **Narrows:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The code is small: `pyproject.toml`, one workflow file and the README.
- Its weight is in running the suite in four places it has never run: a fresh venv at each end of
  U7's range, a venv with the package installed from a wheel, and (after the push) Linux. Each
  fails in its own way if it is set up wrongly, and two of those ways look like the package's
  fault when they are not (§2.2, hazards 1 and 2).

**Read first:**

1. [`README.md`](README.md): §0.2 (the runtime versions), §1, §2 (rows 03–05), §4, §5 (rules 6–10)
   and §6.2 (U7).
2. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`, above all "Releases" and "Repository
   mechanics".
3. The board, with the review of 02. Then [`logs/02-the-test-suite.md`](logs/02-the-test-suite.md)
   §1.1 and §8, and [`logs/01-import-the-pool.md`](logs/01-import-the-pool.md) §3.1, on how
   `venv/` was built.
4. The repository as 02 left it: `pyproject.toml`, `README.md`, `PROVENANCE.md`, `.gitignore`;
   `raypoolkit/__init__.py`, `contract.py` and `RayWorkPool.py`'s constructor (`:72-166`);
   `raypoolkit/tests/test_package_imports.py`, whose tests 2 and 3 run a child interpreter; and
   `raypoolkit/tests/standins.py`, the worked example of the objects a pool drives.
5. For comparison only: DatastoreKit's `prompts/extraction/05-supported-versions-and-ci.md` and its
   `.github/workflows/tests.yml`, read with `git -C /Users/ds283/Documents/Code/DatastoreKit show
   HEAD:<path>`. That package's prompt solved the same problem, with a database this one does not
   have. Nothing is copied from it without checking it here.

Facts below are at `307ed96` (the package unchanged since `49f3ddf`, the suite since `b9f6dec`),
measured on 2026-10-10.

---

## 1. What is wanted

03 makes the package ready to be released as `v0.1.0`: SGK's pool, unchanged in behaviour, with a
suite that pins it. After it:

- `pyproject.toml` declares U7's range and the version `0.1.0`;
- the distribution holds the package and not its test package (§2.4);
- a GitHub Actions workflow runs the 116 at both ends of U7's range;
- the repository's `README.md` says what the package is, what it supports, how a client installs
  it, and how a client uses it;
- **the suite has run, and passed, in a fresh venv at each end, and the package imports from an
  installed wheel**, all on this machine, before anything reaches GitHub.

**03 makes no tag and pushes nothing** (README §2, row 03; §5 rule 10). After its review, pushing
`main` is put to the user. CI must then pass at both ends on 03's commit, and only then is `v0.1.0`
made, annotated, on that commit, and pushed. If CI fails, a fix prompt lands first: no tag is ever
made on a commit whose CI is red, since rule 10 forbids moving one. The tag is not this prompt's
work.

**No behaviour of the package changes.** No file under `raypoolkit/` is touched (README §5 rule 8),
so `compare_with_source.py` gives 02's result. The suite stays at **116**: 03 adds no test.

---

## 2. What to change

### 2.1 `pyproject.toml` (U7)

- `version = "0.1.0"` (from `"0.1.0.dev0"`).
- `requires-python = ">=3.12"`, unchanged.
- `dependencies = ["ray>=2.43"]` (from an unbounded `"ray"`). **No Ray ceiling**, so that a client
  can move Ray without a release here. The two ends are what CI tests; the README says so.
- The package list, per §2.4.
- Nothing else. No classifiers, URLs or licence field: `setuptools>=64`'s licence handling differs
  across versions, and the `LICENSE` file is already in the wheel (measured, §2.2).

### 2.2 What the planner measured

On this machine (macOS 27, arm64), from the session scratchpad, with nothing in the repository
written:

- **The low end is `venv/`:** Python 3.12.15, `ray` 2.43.0, `black` 25.1.0, the package installed
  editable (01). `Ran 116 tests … OK`.
- **Fresh venvs at both ends**, made with `uv` 0.12.20 from MacPorts' `/opt/local/bin/python3.12`
  (3.12.15) and `/opt/local/bin/python3.13` (3.13.16), each with
  `uv pip install -e . "ray==<pin>" "black==25.1.0"`: **`Ran 116 tests … OK` at both**, with no
  warning printed and no Ray process before or after.
- **The stand-ins at the high end.** The suite depends on three things inside Ray (log 02 §8):
  `ObjectRef` built from 28 bytes, `ray.wait`'s argument checks, and the auto-init hook's lookup of
  `ray.init`. At 2.55.1, `ray/_private/auto_init_hook.py` differs from 2.43.0's only in the order of
  its imports, and `wait`'s checks, from the single-ref test to the `num_returns` bound, are
  identical line for line. The suite passing at 2.55.1 is the end-to-end check.
- **Wheels.** `uv pip compile --only-binary ray`, per Python and platform:

  | Python | `ray==2.43.0` | `ray==2.44.1` | `ray==2.45.0` | `ray==2.55.1` |
  |---|---|---|---|---|
  | 3.12, Linux x86_64 and macOS arm64 | resolves | — | — | — |
  | 3.13, Linux x86_64 and macOS arm64 | **no solution** | **no solution** | resolves | resolves |

  So **on Python 3.13 Ray's floor is in effect 2.45.0**: no earlier release has a 3.13 wheel.
- **The newest releases today:** `ray` 2.59.0, with wheels for Python 3.14 on Linux and macOS.
  `requires-python = ">=3.12"` therefore admits Python 3.14, and an unpinned install resolves to
  Ray 2.59.0. Neither is tested (hazard 4).
- **The wheel.** Built with `uv build --wheel` from a fresh `git archive` export of the tree, with
  §2.1's and §2.4's `pyproject.toml`: `raypoolkit-0.1.0-py3-none-any.whl`, 9 entries (the four
  package modules, `LICENSE` under `dist-info/licenses/`, `METADATA`, `WHEEL`, `top_level.txt`,
  `RECORD`), 12,016 bytes. Without §2.4's exclusion it has 19 entries, ten of them under
  `raypoolkit/tests/`. Installed into a fresh venv at the high end's pins, from outside the
  repository with `-I`: `raypoolkit`, its three modules and its two public names import,
  `ray.is_initialized()` stays false, and `import raypoolkit.tests` raises `ModuleNotFoundError`.
- **The editable install, with the exclusion**, in a fresh venv at the high end: `Ran 116 tests …
  OK` from the repository root. The editable finder still maps the whole `raypoolkit/` directory,
  so `raypoolkit.tests` stays importable there. That is what the suite needs; the wheel is what a
  client gets.
- **The resolver refuses outside the range**, with §2.1's `pyproject.toml`, by `uv pip install
  --dry-run` into a throwaway 3.12 venv: `ray==2.42.1` ("raypoolkit==0.1.0 depends on ray>=2.43
  … unsatisfiable"), and `requires-python = ">=3.13"` at the low end ("the current Python version
  (3.12.15) does not satisfy Python>=3.13").
- **CI.** `ds283/RayPoolKit` is public, its default branch `main`, Actions enabled with all actions
  allowed, and it has never run a workflow. `actions/python-versions`' manifest has
  `python-3.12.15-linux-24.04-x64` and `python-3.13.16-linux-24.04-x64`. The latest releases
  (`gh api repos/actions/<name>/releases/latest`) are `actions/checkout` `v7.0.1` and
  `actions/setup-python` `v7.0.0`. `origin/main` is at `97f9ff0`, behind local `main`.
- **PyYAML** is a dependency of Ray (`Requires-Dist: pyyaml`), so any scratch venv can parse the
  workflow.

**Hazards.** Check each, and say in the log what you found.

1. **The guard needs the package installed.** `test_package_imports`' tests 2 and 3 run
   `sys.executable -I` from an empty temporary directory, so they find `raypoolkit` only through an
   installation. Measured: in a venv with Ray but no `raypoolkit`, run with `PYTHONPATH=.`, those
   two fail and the other 114 pass. Every venv you run the suite in has the package installed,
   editable, and so does CI.
2. **A stale `build/` leaks the tests into the wheel.** Measured: after a first `uv build` in an
   export, a second build in the same directory, with the exclusion added, still shipped all ten
   test files, from the first build's `build/lib/`. A wheel built that way would pass a release
   check that looks only at imports and fail one that lists the wheel. **Build every wheel from a
   fresh `git archive HEAD` export in the scratchpad, one export per build.** Never build in the
   repository tree. `.gitignore` covers `build/`, `dist/` and `*.egg-info/`, but a build there
   would leave a `build/` that the next one reuses.
3. **Linux is not measured.** The suite was written and has only run on macOS. CI is the first
   Linux run. Nothing here can stand in for it, which is why the tag waits for it.
4. **The newest versions are not tested.** Python 3.14 and Ray 2.59.0 are inside the declared range
   (§2.2). The README states the two tested ends, and says that a client pins its own Ray. A third
   CI job for "the newest allowed" is not asked for (U7), and is not added.
5. **The check cannot run in CI.** `compare_with_source.py` reads SGK through `git`. It runs here,
   as every prompt through 03 runs it. The workflow runs the suite and `black --check`, and nothing
   that needs a client.

### 2.3 The fresh venvs, at both ends

Make two venvs **in the session scratchpad**, never under the repository, with `uv`:

| End | Interpreter | Pins |
|---|---|---|
| low | `/opt/local/bin/python3.12` | `ray==2.43.0`, `black==25.1.0` |
| high | `/opt/local/bin/python3.13` | `ray==2.55.1`, `black==25.1.0` |

- In each, install the package **editable, together with its pins, in one resolve**:
  `uv pip install --python <venv>/bin/python -e . "ray==…" "black==25.1.0"`. This is the
  workflow's install step (§2.5). One resolve also checks that the pins satisfy `pyproject.toml`'s
  declared range.
- Run the suite from the repository root with each venv's interpreter. Both must give `Ran 116
  tests … OK`. Record each venv's `sys.version` and `ray.__version__`, and `pgrep -lf
  'gcs_server|raylet|ray::'` before and after.
- **Downloads.** Packages from PyPI into the scratchpad, for these venvs and §2.4's build, and
  nothing else. 01's `pip install -e .` already fetched `setuptools` the same way.
- **The project's `venv/` is not rebuilt.** After §2.1 and §2.4, reinstall the package in it
  editable with `--no-deps` (`./venv/bin/python -m pip install --no-deps -e .`), so that its
  metadata says `0.1.0`, and run the suite there too. Record `pip freeze` before and after.

### 2.4 The distribution

`[tool.setuptools.packages.find]` keeps `include = ["raypoolkit*"]` and gains
`exclude = ["raypoolkit.tests", "raypoolkit.tests.*"]`.
- **Why:** the test package is not a client's to import. It is this repository's, and it would put
  a second `PoolTestCase` and a patched `ray.init` within reach of any client's code.
- **Check it does not break the editable installs.** Run the whole suite in all three venvs after
  the change.

**The release check.** Build the wheel from a fresh export (hazard 2). §2.1's change is not yet
committed when the check runs, so: `git archive HEAD | tar -x -C <scratch>/export-<n>` into a new,
empty directory; copy the working tree's `pyproject.toml` over the export's (the only file 03
changes that the build reads); then `uv build --wheel --out-dir <scratch>/dist-<n>
<scratch>/export-<n>`. The log says so. Install the wheel, not
editable, into a third fresh scratch venv, at the high end's pins. Then, from a directory outside
the repository, with `PYTHONPATH` unset and `-I`:
- `import raypoolkit`; `from raypoolkit import RayWorkPool, DatastorePool`; and the three modules
  `raypoolkit.RayWorkPool`, `raypoolkit._timing` and `raypoolkit.contract` by
  `importlib.import_module`;
- `raypoolkit.__file__` is under the venv's `site-packages`, not this repository;
- `ray.is_initialized()` is false afterwards;
- `import raypoolkit.tests` raises `ModuleNotFoundError`;
- the wheel's file list is the four modules, `LICENSE` and the `dist-info` files, and nothing under
  `raypoolkit/tests/`;
- `importlib.metadata.version("raypoolkit")` is `0.1.0`, and `requires("raypoolkit")` is
  `["ray>=2.43"]`.

Record the wheel's name, size, entry count and SHA-256, its file list, and each command's output.
The wheel is not committed, and no `build/`, `dist/` or `*.egg-info` appears in `git status`.

### 2.5 The workflow

`.github/workflows/tests.yml`:
- A comment at the top: the suite at both ends of the supported range (README "Supported
  versions"); the equivalence check under `docs/extraction/` reads the source repository and runs
  locally only.
- **Triggers:** `push` to `main`, `pull_request`, and `workflow_dispatch`.
- **One job, `suite`, on `ubuntu-24.04`**, with a matrix of exactly two entries, named `low` and
  `high`, holding §2.3's Python and Ray versions. `fail-fast: false`, so that one end's failure
  does not hide the other's.
- **Steps:**
  1. `actions/checkout@v7`;
  2. `actions/setup-python@v7`, with the matrix's Python;
  3. `python -m pip install --upgrade pip`, then
     `python -m pip install -e . "ray==${{ matrix.ray }}"`;
  4. print `sys.version` and `ray.__version__`;
  5. `python -m unittest discover -s raypoolkit/tests -t .`;
  6. on `low` only: `python -m pip install black==25.1.0` and `black --check raypoolkit docs`.
- **Permissions:** `contents: read`. No secrets, no cache, no artefact upload, no other action.
- It runs nothing of hazard 5.

**Replay it here.** GitHub cannot run it from this machine, so run steps 3–6 by hand, with `uv` in
place of `pip`, in §2.3's venvs. The log records the commands as run, and which step of the
workflow each stands for. A workflow step with no local counterpart is named in the log.

Validate the file as YAML, with PyYAML from one of the scratch venvs:
`<venv>/bin/python -c "import yaml, sys; print(yaml.safe_load(open(sys.argv[1])))" <file>`.
(PyYAML reads the key `on` as `True`; that is YAML 1.1, and GitHub reads it correctly.) Check that
the matrix's values equal §2.3's table.

### 2.6 The README

The repository's `README.md` is rewritten from its "being extracted" state. It keeps the opening
paragraph's description of what the pool does, the DatastoreKit paragraph and the licence. It gains:

- **Status.** `v0.1.0` is SecondaryGWKit's `RayWorkPool` at `b510bc9`, moved here with its
  behaviour unchanged (`PROVENANCE.md`), and pinned by a suite that needs no Ray cluster. The
  faults inherited with it are listed on the board and are pinned as they behave; `v0.2.0` fixes
  them. Point at the campaign README and its board. Do not list the faults in the README: the board
  is where they are kept.
- **Supported versions.** A table with the declared range (§2.1) and the two tested ends (§2.3).
  Say that on Python 3.13 Ray's floor is in effect 2.45.0 (§2.2), that newer releases inside the
  range (Python 3.14, Ray up to 2.59.0 today) are allowed but not tested, and that a client pins its
  own Ray.
- **Installing.** The pinned form `CLAUDE.md` gives, `raypoolkit @
  git+https://github.com/ds283/RayPoolKit@v0.1.0`, in a client's `requirements.txt`. Add one
  sentence: an editable install is for developing this package, never for a client's production
  runs. Write it as of the tag: the README is committed before the tag exists, and is true once it
  does.
- **Using it.** In prose and short lists, not a worked program:
  - `from raypoolkit import RayWorkPool`; the constructor's arguments, grouped: the datastore pool
    (`DatastorePool`, what it must provide, and that it is passed through to the store and persist
    handlers); `task_list` and `task_builder`, with the four things a task builder may return; the
    six handlers and what each is given and returns; `label_builder`; the three sizes and three
    notification settings with their defaults; `title`; `store_results`;
  - the objects a lookup returns: an `available` attribute decides whether one takes the
    available or the compute path, and an object without one is finished as it is; a compute
    handler's object has `compute(**kwargs)` returning an `ObjectRef`, and `store()`; a persisted
    object has `store_id`;
  - `run()`, then `results` (with `store_results=True`) and `total_time` (with a `title`);
  - **as of `v0.1.0`, a pool with no compute handler must pass `persist_handler=None`**, or the
    constructor raises (`[00-the-constructor-checks-its-handlers-unevenly]`); say so plainly, since
    every client meets it;
  - **the printed lines are part of the interface** (`CLAUDE.md`, "Releases"): what the banner,
    progress and completion lines look like, in one example each, taken from the suite's pinned
    lines (`test_printed_lines.py`), and that a change to them is released as a new minor version.
  - Every name the README mentions is checked against the package: each importable name by
    importing it, each argument by `inspect.signature(RayWorkPool)`, each default by reading it
    from that signature. List them in the log with how each was checked.
  - Do not write a client in the README. Point at `raypoolkit/tests/standins.py` in this repository
    as the worked example of the objects and handlers a pool drives, and say that it is not
    installed with the package.
- **Developing.** How to make a venv, install editable, and run the suite (`CLAUDE.md`'s command);
  that the suite needs no Ray cluster and why (the stand-ins); that CI runs it at both ends; and
  that the check under `docs/extraction/` needs SecondaryGWKit's repository, so it runs locally
  only.

No other prose file changes. `PROVENANCE.md` and `CLAUDE.md` stay as they are.

---

## 3. Verification

1. **The suite, four times:** in `venv/` (after the editable reinstall), in the low and high
   scratch venvs, and again in `venv/` after every change. Each gives `Ran 116 tests … OK`. The log
   records each venv's versions. No Ray process before or after any run.
2. `./venv/bin/python docs/extraction/compare_with_source.py` exits 0, with 02's counts (572
   identical, 2 D-imp, 1 D-pool, 4 D-int, 12 declared files, 0 undeclared). Its whole output goes
   in the log.
3. **The release check** of §2.4 passes, with its record.
4. **The workflow**, replayed as §2.5 says, at both ends; the file parses as YAML; the matrix equals
   §2.3.
5. `./venv/bin/black --check raypoolkit docs` (25.1.0) is clean. `black` is not run on the
   workflow or the README.
6. **The breakage record.** Each item is a change exactly as applied, with what failed. None is
   committed, and `git status` is clean after each. A diff to a tracked file is recorded with its
   trailing context lines and checked with `git apply --check` as recorded. Use throwaway venvs and
   exports for these; never change the venvs you verify with.
   - **(a) The workflow's install without the package:** step 3 with `-e .` removed (the pin
     installed alone), in a throwaway venv at the high end, the suite run with `PYTHONPATH=.`.
     Expect the guard's tests 2 and 3 to fail, and only those (hazard 1).
   - **(b) The Ray floor:** step 3 with `ray==2.42.1`. The resolver refuses, naming `ray>=2.43`.
   - **(c) The Python floor:** `requires-python = ">=3.13"` in `pyproject.toml`. The low end's
     install refuses.
   - **(d) An exclusion too broad:** `exclude` gains `"raypoolkit"`. The release check fails: the
     wheel holds no module, and `import raypoolkit` fails.
   - **(e) The test package shipped:** the `exclude` removed. The release check fails:
     `import raypoolkit.tests` succeeds, and the wheel lists files under `raypoolkit/tests/`.
   - **(f) A stale build:** build the wheel of (e), then, in the same export with the exclusion
     restored, build again. The release check's file list fails (hazard 2). Record both wheels'
     entry counts.

---

## 4. Acceptance

1. `pyproject.toml` declares §2.1's range and version, and §2.4's exclusion.
2. The suite passes at both ends in fresh venvs, and in `venv/`. The release check passes.
3. The workflow is §2.5's and parses. Its steps were replayed at both ends.
4. §3.1–§3.6 hold.
5. **The records**, in the same commit:
   - the log, `logs/03-supported-versions-and-ci.md`, per README §5.1. It also has:
     - the versions of every venv, and each suite's verdict line;
     - every install command as run, and the workflow step each stands for;
     - the release check: the wheel's name, size, entry count and SHA-256, its file list, and
       each command's output;
     - every name the README mentions, with how it was checked;
     - the five hazards;
     - the check's whole output;
     - (a)–(f);
     - the test count before and after (116, 116);
   - the board: the header, §1's row for 03 (landed, "this commit", 116 → 116), and a line in its
     header saying that `v0.1.0` is ready to be tagged once CI passes on 03's commit, with no tag
     made;
   - `docs/OPEN_ISSUES.md`, if the work opens anything (7 open now);
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 116, in any venv. A failure at the high end is not
  "fixed" in the package or the tests: record what fails, and ask.
- Passing anything would need a change under `raypoolkit/`, to `compare_with_source.py`, or to any
  file not in §6.
- A pin of §2.3 does not resolve, or §2.1's range cannot be satisfied by both ends.
- The release check fails in a way (d)–(f) do not explain.
- Anything would push to GitHub, make or move a tag, change the repository's settings, or start
  Ray; or would edit, run or import SecondaryGWKit, ChamPBH, StochasticInstantons or DatastoreKit.
- A download other than PyPI packages into the scratchpad would be needed.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `pyproject.toml`;
  - `.github/workflows/tests.yml` (new);
  - `README.md`;
  - the log, this board, `prompts/INDEX.md`, and `docs/OPEN_ISSUES.md` if needed.
- It changes nothing else:
  - no file under `raypoolkit/`, in the package or its tests;
  - nothing under `docs/` but `OPEN_ISSUES.md`;
  - none of `PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore` or the campaign README.
- It makes no tag, and pushes nothing.
- It fixes nothing in the package, including the inherited faults and
  `[02-the-constructor-does-not-check-its-sizes]` (04).
- It writes no orchestration note.

---

## 7. The log and the board

`logs/03-supported-versions-and-ci.md`, using README §5.1, with the additions of §4.5.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 03 (landed, commit, log, suite).
