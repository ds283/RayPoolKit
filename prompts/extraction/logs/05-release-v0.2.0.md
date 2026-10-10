# Log — extraction prompt 05: release `v0.2.0`

**Subject:** Prepare v0.2.0 and keep a stale manifest out of the wheel · **Commit:** `eaef0ce` ·
**Date:** 2026-10-10 · **Agent:** Claude Opus 5.5

**Result: landed.** `pyproject.toml` says `0.2.0` and gains `[tool.setuptools]`
`include-package-data = false`, and nothing else. `README.md` is rewritten where it described
`v0.1.0` (Status, a new "Changes in `v0.2.0`", the pin, the work, the sizes, a new "Which handlers
a pool needs", Developing, Licence); `PROVENANCE.md` makes three statements "of `v0.1.0`", gives
the retired check's commands from a `git worktree` of the tag, and gains "Since `v0.1.0`". No file
under `raypoolkit/` changed. The suite is **121 → 121**, passing in `venv/` (3.12.15 / 2.43.0,
`raypoolkit` `0.1.0` → `0.2.0`), in a fresh low-end venv (3.12.15 / 2.43.0) and in a fresh
high-end venv (3.13.16 / 2.55.1), with no Ray process before or after any run. The release check
passes twice: (R1) a fresh export, and (R2) a fresh export with the repository's stale
`raypoolkit.egg-info/` copied in; each wheel has **9 entries, none under `raypoolkit/tests/`**, and
each build log has **0** "absent from" lines. (a)–(c) each fail as the prompt says. **One issue is
closed and none opened**, so the index goes from 1 to **0**. **No tag was made and nothing was
pushed**: `v0.2.0` is ready to be tagged on `eaef0ce` once CI passes there at both ends.

**Gate, re-checked at start.** `HEAD` was `1868b6e` (the orchestration note, touching only
`prompts/extraction/orchestrator/`; the prompt was written at `f839209`, 04's review at `914070c`).
The tree was clean, the only worktree this checkout, `git tag` only `v0.1.0`. `venv/`: Python
3.12.15, `ray` 2.43.0, `black` 25.1.0, pip 26.2.1, `raypoolkit` editable, `importlib.metadata`
`0.1.0` `['ray>=2.43']`; `Ran 121 tests in 1.358s` `OK`, by module construction 15,
inherited_faults 6, package_imports 3, printed_lines 18, run_paths 22, scheduling 7, standins 30,
task_builder 20. `black --check raypoolkit docs`: 15 files unchanged. No `build/` or `dist/`. The
repository's gitignored `raypoolkit.egg-info/` was there (18:14), its `PKG-INFO` `Version: 0.1.0`,
its `SOURCES.txt` listing 10 files under `raypoolkit/tests/`. No Ray process. Toolchain: `uv`
0.12.20, `/opt/local/bin/python3.12` 3.12.15, `/opt/local/bin/python3.13` 3.13.16. Every venv,
export, wheel, probe and driver of this log is under the agent's scratch directory
(`…/scratchpad/agent05/`), written `$S` below.

## 1. What shipped

| File | What |
|---|---|
| `pyproject.toml` | `version = "0.2.0"` (from `"0.1.0"`); a `[tool.setuptools]` table, before `[tool.setuptools.packages.find]`, holding `include-package-data = false`. Nothing else (§2.1) |
| `README.md` | Status for `v0.2.0`, with `v0.1.0` in one sentence; "Changes in `v0.2.0`"; the pin at `v0.2.0`; `task_list` as any iterable; the sizes at least 1; "A pool with no compute handler must pass `persist_handler=None`" replaced by "Which handlers a pool needs"; the retired check in Developing; the header in Licence (§2.2). Everything else as it was, the printed-line examples included |
| `PROVENANCE.md` | "At `v0.1.0`, …" on the differences allowed and on SGK's comments; "Re-running the check" from a `git worktree` of `v0.1.0`; a section "Since `v0.1.0`" before "The freeze" (§2.3). The file map, the classes and the freeze unchanged |
| this log, the board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md` | the records; the index loses its one row |

The diff to `pyproject.toml`, as committed:

```diff
@@ -4,13 +4,16 @@ build-backend = "setuptools.build_meta"
 
 [project]
 name = "raypoolkit"
-version = "0.1.0"
+version = "0.2.0"
 description = "A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks"
 requires-python = ">=3.12"
 dependencies = [
     "ray>=2.43",
 ]
 
+[tool.setuptools]
+include-package-data = false
+
 [tool.setuptools.packages.find]
 include = ["raypoolkit*"]
 exclude = ["raypoolkit.tests", "raypoolkit.tests.*"]
```

`raypoolkit.egg-info/` (gitignored) was rewritten by the editable installs of §3.2 and §3.3 and is
not staged.

## 2. Deviations from the prompt

The orchestrator's brief added eight clarifications and additions (1–8 below). Each is an
**IMPLEMENTATION CHOICE at the orchestrator's direction**, except 1, which is **STRUCTURALLY
REQUIRED**.

1. **The README does not repeat the prompt's "now refused … (each was silently ignored)" bullet**
   (clarification 1). It is untrue of `v0.1.0`, read from `git show v0.1.0:raypoolkit/RayWorkPool.py`
   (`:94-102`) and measured by the probe of §3.6: an explicit persist handler with no compute
   handler was already refused, with `RuntimeWarning` raised as an exception; a compute handler
   with `persist_handler=None` was already refused, with `RuntimeError`; and a compute handler with
   `store_handler=None` constructed and then failed in `run()` with `TypeError`, so it was neither
   refused nor ignored. The README's "Changes" therefore says: the checks raise `ValueError`, and
   two of them were refused by `v0.1.0` with `RuntimeWarning` and `RuntimeError` (bullet 1); and
   **newly refused**: a store handler, validation handler or label builder with no compute handler
   (`v0.1.0` accepted it and never called it), a compute handler with `store_handler=None` (`v0.1.0`
   failed in `run()`), and a size below 1 (bullet 3). **STRUCTURALLY REQUIRED**: the prompt's §5
   makes a statement untrue of the module a stop, and this is the correction.
2. **Every wheel was built without `-q`**, stdout and stderr captured to `$S/out/build-<label>.log`,
   and `grep -c "absent from"` recorded (clarification 2): (R1) 0, (R2) 0, (a) **2**, (b) 0, (c) 0.
   Every build printed the two "byte-compiling is disabled, skipping" lines and no other warning,
   except (a).
3. **(R2)'s manifest was recorded before each build that copied it in** (clarification 3). Both
   such builds, (R2) and (a), ran before `venv/`'s reinstall, so the copy said `Version: 0.1.0`,
   with `grep -c tests/ SOURCES.txt` **10**. After every editable install of this log the
   repository's copy says `Version: 0.2.0`, and its `SOURCES.txt` still lists the **10**, as the
   clarification measured.
4. **The printed-line examples were checked by rendering** (clarification 4): §3.8.
5. **`PROVENANCE.md`'s commands were run as written**, with `<scratch>` as `$S`, from a `bash`
   script (`$S/scripts/retired_check.sh`); the worktree was removed after, and `git worktree list`
   showed this checkout alone (clarification 5; §3.9). The file writes the scratch directory as a
   placeholder, `<scratch>`, and the repository as `REPO=$(pwd)`, not as this session's paths. The
   check's `RESULT: FAIL` on a later tree is the orchestrator's measurement, cited and not re-run:
   the brief allows the check's read of SGK only from a worktree of `v0.1.0`.
6. **"New here, with no source" in `PROVENANCE.md` is left as it is** (clarification 6): §6,
   observation 1.
7. **Each breakage diff is against `eaef0ce`'s `pyproject.toml`**, applied with `git apply` run
   inside its own fresh export (`$S` is not inside a repository), each checked with `git apply
   --check` before and `git apply -R --check` after (clarification 7). The repository's
   `pyproject.toml` was touched only by §2.1's edit.
8. **No Ray process was up at any point** (clarification 8). The DatastoreKit cluster the note
   describes was gone before this log's first check. Each check filtered out shells whose own
   command lines carry the pattern (`$S/scripts/raycheck.sh`), and an unfiltered `pgrep -lf
   'gcs_server|raylet'` at the start was empty.

Choices of this prompt's agent:

9. **"Each fault's fix is guarded by a test that `v0.1.0`'s module fails"**, where the prompt's §2.2
   says "Each fix is guarded by a test". 04 also reworded a comment
   (`[01-a-kept-comment-names-the-datastore-service]`), which no test guards (board §4), so "each
   fix" would be untrue of one fix. **STRUCTURALLY REQUIRED** (§5: a statement the README makes must
   be true of the module).
10. **The release check is a script**, `$S/scripts/release_check.py`, taking the wheel and the
    version (`0.2.0`); it makes each check of 03 §2.4 in turn, as 03's did, and prints PASS or FAIL
    for each. It was reused unchanged for (a)–(c). `$S/scripts/wheelinfo.py` prints each wheel's
    name, size, SHA-256, entries and `METADATA`. **IMPLEMENTATION CHOICE.**
11. **(R1)'s wheel was installed and checked too**, in its own fresh venv (`$S/venv-wheel-R1`, the
    high end's pins), beside the prompt's (R2) install (`$S/venv-wheel`). **IMPLEMENTATION CHOICE.**
12. **(R1), (R2) and (a)–(c) were built before `venv/`'s reinstall and the fresh venvs**, straight
    after §2.1's edit. The order changes nothing: each build reads only its export.
    **IMPLEMENTATION CHOICE.**
13. **(c)'s check expects `0.2.0`**, so its version check fails, and so does the `dist-info` file
    list, whose directory is `raypoolkit-0.1.0.dist-info/`. **IMPLEMENTATION CHOICE.**
14. **The "was" of each "Changes" statement was measured on `v0.1.0`'s module by a probe**
    (`$S/probes/probe_changes.py`, a `PoolTestCase` that prints each outcome and asserts nothing),
    run in a `git archive v0.1.0` export with a throwaway venv, and again on the working tree
    (§3.6). **IMPLEMENTATION CHOICE.**
15. **"The printed lines are unchanged" was also checked by `ast`**: the module's seven `print()`
    calls, its four message builders and `_timing.py` are equal at `v0.1.0` and in the tree (§3.7).
    **IMPLEMENTATION CHOICE.**
16. **The README says a little more than §2.2 lists**, each checked (§4): in "Which handlers a pool
    needs", that `available_handler` and `post_handler` are used on the lookup path and may be given
    either way (log 04 §5, observation 5); and in-page links from Status and "Changes" to the two
    new sections. The board's §4 is named in text ("§4 (Resolved issues)"), without an anchor.
    **IMPLEMENTATION CHOICE.**
17. **Status folds two `v0.1.0` sentences into the `v0.2.0` paragraph**: "pinned by a test suite
    that needs no Ray cluster" moves there, and "`PROVENANCE.md` gives the file map and the only
    differences allowed" becomes the link after `v0.1.0`'s one sentence. **IMPLEMENTATION CHOICE.**
18. **`ray`'s newest release was re-measured**: `uv pip compile` of `ray>=2.43` resolves to
    `ray==2.59.0` at Python 3.13 and 3.14, so the README's "Ray up to 2.59.0 today" holds.
    **IMPLEMENTATION CHOICE.**

Two slips, both corrected:
- **The wrapper that ran (R1)'s and (R2)'s builds stopped after (R1)**: it was a `zsh` command line
  with an `echo ===` between the two, and `zsh` expands a word beginning with `=`. The build
  script itself is `bash` (`$S/scripts/build.sh`, by its shebang) and had finished (R1); (R2) was
  then built by a second call. Every later build was run as `bash $S/scripts/build.sh`.
  **UNINTENDED DRIFT**, corrected; no result depends on it.
- **The probe's first version shared one stand-in across its three size cases**, so the wait-call
  cap was reached early and `process_batch_size=0` showed the cap's error instead of Ray's
  `ValueError`. Each size case was made its own test method, with its own stand-in, and the probe
  re-run; §3.6 is the re-run. **UNINTENDED DRIFT**, corrected.

## 3. Verification performed

### 3.1 The suite, by venv (prompt §3.1)

Every run from the repository root, `<python> -m unittest discover -s raypoolkit/tests -t .`, in the
foreground, its output written to `$S/out/suite-<venv>-<when>.txt` and the verdict grepped from
it. Counts by module are by the loader (`$S/scripts/count_by_module.py`). `$S/scripts/raycheck.sh`
found no Ray process before or after every run.

| Venv | `sys.version` | `ray` | `raypoolkit` | When | Verdict |
|---|---|---|---|---|---|
| `venv/` | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | `0.1.0`, editable | before any change | `Ran 121 tests in 1.358s` `OK` |
| `venv/` | as above | 2.43.0 | `0.2.0`, editable | after §2.1 and the reinstall | `Ran 121 tests in 2.476s` `OK` |
| `$S/venv-low` (fresh) | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | `0.2.0`, editable | after §2.1 | `Ran 121 tests in 3.410s` `OK` |
| `$S/venv-high` (fresh) | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | `0.2.0`, editable | after §2.1 | `Ran 121 tests in 4.601s` `OK` |
| `venv/` | as above | 2.43.0 | `0.2.0`, editable | final tree | `Ran 121 tests in 6.108s` `OK` |
| `$S/venv-low` | as above | 2.43.0 | `0.2.0`, editable | final tree | `Ran 121 tests in 6.520s` `OK` |
| `$S/venv-high` | as above | 2.55.1 | `0.2.0`, editable | final tree | `Ran 121 tests in 8.766s` `OK` |

By module, in every run: `test_construction` 15, `test_inherited_faults` 6,
`test_package_imports` 3, `test_printed_lines` 18, `test_run_paths` 22, `test_scheduling` 7,
`test_standins` 30, `test_task_builder` 20. **Before: 121. After: 121.** In every venv
`raypoolkit.__file__` is `/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py` and
`importlib.metadata` gives `0.2.0` `['ray>=2.43']` after §2.1.

The fresh venvs, made as 03 §2.3 made them, each with one resolve:

```
$ uv venv --python /opt/local/bin/python3.12 $S/venv-low
Using CPython 3.12.15 interpreter at: /opt/local/bin/python3.12
$ uv pip install --python $S/venv-low/bin/python -e . "ray==2.43.0" "black==25.1.0"
Using Python 3.12.15 environment at: $S/venv-low
Resolved 25 packages in 305ms
   Building raypoolkit @ file:///Users/ds283/Documents/Code/RayPoolKit
      Built raypoolkit @ file:///Users/ds283/Documents/Code/RayPoolKit
Prepared 1 package in 2.03s
Installed 25 packages in 273ms
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
 + raypoolkit==0.2.0 (from file:///Users/ds283/Documents/Code/RayPoolKit)
 + referencing==0.37.0
 + requests==2.34.2
 + rpds-py==2026.9.1
 + typing-extensions==4.16.0
 + urllib3==2.8.0

$ uv venv --python /opt/local/bin/python3.13 $S/venv-high
Using CPython 3.13.16 interpreter at: /opt/local/bin/python3.13
$ uv pip install --python $S/venv-high/bin/python -e . "ray==2.55.1" "black==25.1.0"
Using Python 3.13.16 environment at: $S/venv-high
Resolved 22 packages in 13ms
   Building raypoolkit @ file:///Users/ds283/Documents/Code/RayPoolKit
      Built raypoolkit @ file:///Users/ds283/Documents/Code/RayPoolKit
Prepared 1 package in 14.97s
Installed 22 packages in 221ms
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
 + raypoolkit==0.2.0 (from file:///Users/ds283/Documents/Code/RayPoolKit)
 + referencing==0.37.0
 + requests==2.34.2
 + rpds-py==2026.9.1
 + urllib3==2.8.0
```

`uv`'s cache at `~/.cache/uv` was used, neither bypassed nor cleaned.

### 3.2 `venv/`'s metadata (prompt §3.2)

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
  Created wheel for raypoolkit: filename=raypoolkit-0.2.0-0.editable-py3-none-any.whl size=6981 sha256=3c5c4f64666b569b1a0e3126100c72df8702115a12090b0cea3eba0c604af4c6
  Stored in directory: /private/var/folders/tm/y9rd_z8x1ks3m09yhkjc0h7800128f/T/pip-ephem-wheel-cache-0m09rxfr/wheels/ae/ed/ff/e9451c3e44c61597c01d5d3317ab13f852c264ea133ef6e862
Successfully built raypoolkit
Installing collected packages: raypoolkit
  Attempting uninstall: raypoolkit
    Found existing installation: raypoolkit 0.1.0
    Uninstalling raypoolkit-0.1.0:
      Successfully uninstalled raypoolkit-0.1.0
Successfully installed raypoolkit-0.2.0
```

| | `importlib.metadata.version("raypoolkit")` | `requires("raypoolkit")` |
|---|---|---|
| before | `0.1.0` | `['ray>=2.43']` |
| after | `0.2.0` | `['ray>=2.43']` |

`pip freeze` before and after is identical (it does not show an editable version): `black==25.1.0`,
`ray==2.43.0`, `-e git+https://github.com/ds283/RayPoolKit.git@1868b6eec3da89b5e1b60c7882456a0f9531ba27#egg=raypoolkit`
(the `HEAD` at the freeze), and the 22 other packages of log 03 §3.2, at the same versions.

### 3.3 The release check (prompt §3.3)

**The builds.** `$S/scripts/build.sh <label> <manifest> [diff]`, in `bash`, one fresh export per
build, never in the repository tree:

```bash
mkdir $S/export-<label>                              # must not exist
git -C $R archive HEAD | tar -x -C $S/export-<label>
cp $R/pyproject.toml $S/export-<label>/pyproject.toml   # the working tree's, §2.1
cp -R $R/raypoolkit.egg-info $S/export-<label>/      # (R2) and (a) only
(cd $S/export-<label> && git apply --check <diff> && git apply <diff> && git apply -R --check <diff>)   # (a)-(c) only
uv build --wheel --out-dir $S/dist-<label> $S/export-<label> > $S/out/build-<label>.log 2>&1
```

`$R` is the repository root. Each export held `.github`, `.gitignore`, `CLAUDE.md`, `docs`,
`LICENSE`, `prompts`, `PROVENANCE.md`, `pyproject.toml`, `raypoolkit`, `README.md`, and no
`build/`, `dist/` or `*.egg-info` (until (R2)'s and (a)'s copy). `pyproject.toml` is the only file
05 changes that the build reads (it has no `readme` key). Before (R2)'s build the copy said
`Version: 0.1.0`, and `grep -c tests/ raypoolkit.egg-info/SOURCES.txt` gave **10**.

**(R2)'s build log, whole** (`$S/out/build-R2.log`, 54 lines; "absent from": **0**):

```
Building wheel...
running egg_info
writing raypoolkit.egg-info/PKG-INFO
writing dependency_links to raypoolkit.egg-info/dependency_links.txt
writing requirements to raypoolkit.egg-info/requires.txt
writing top-level names to raypoolkit.egg-info/top_level.txt
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
running egg_info
writing raypoolkit.egg-info/PKG-INFO
writing dependency_links to raypoolkit.egg-info/dependency_links.txt
writing requirements to raypoolkit.egg-info/requires.txt
writing top-level names to raypoolkit.egg-info/top_level.txt
reading manifest file 'raypoolkit.egg-info/SOURCES.txt'
adding license file 'LICENSE'
writing manifest file 'raypoolkit.egg-info/SOURCES.txt'
Copying raypoolkit.egg-info to build/bdist.macosx-27.0-arm64/wheel/./raypoolkit-0.2.0-py3.14.egg-info
running install_scripts
creating build/bdist.macosx-27.0-arm64/wheel/raypoolkit-0.2.0.dist-info/WHEEL
creating '$S/dist-R2/.tmp-0ap8_vtr/raypoolkit-0.2.0-py3-none-any.whl' and adding 'build/bdist.macosx-27.0-arm64/wheel' to it
adding 'raypoolkit/RayWorkPool.py'
adding 'raypoolkit/__init__.py'
adding 'raypoolkit/_timing.py'
adding 'raypoolkit/contract.py'
adding 'raypoolkit-0.2.0.dist-info/licenses/LICENSE'
adding 'raypoolkit-0.2.0.dist-info/METADATA'
adding 'raypoolkit-0.2.0.dist-info/WHEEL'
adding 'raypoolkit-0.2.0.dist-info/top_level.txt'
adding 'raypoolkit-0.2.0.dist-info/RECORD'
removing build/bdist.macosx-27.0-arm64/wheel
Successfully built $S/dist-R2/raypoolkit-0.2.0-py3-none-any.whl
```

**(R1)'s build log** (`$S/out/build-R1.log`, 56 lines; "absent from": **0**) is the same but for
two lines (`creating raypoolkit.egg-info`, and a first `writing manifest file` before the read, since
the export has no manifest) and the scratch paths. Its only warnings are the two
"byte-compiling" lines.

**The wheels.**

| | (R1) | (R2) |
|---|---|---|
| Name | `raypoolkit-0.2.0-py3-none-any.whl` | `raypoolkit-0.2.0-py3-none-any.whl` |
| Size (`os.path.getsize`) | **13,565 bytes** | **13,565 bytes** |
| Entries | **9** | **9** |
| Under `raypoolkit/tests/` | **0** | **0** |
| SHA-256 | `059e7c32e08120232b15bf7f1ed6711aa9c31cd7ee3a9804851f50e8dc57d014` | `e3d4648404bc072dccdd5b03fdd6e6f0fefe20d53d1b8b08ed39634ee0018b45` |
| "absent from" in the build log | 0 | 0 |

The SHA-256s differ by the zip timestamps; the file lists and contents are the same. Both file
lists, entry by entry:

| Entry | Size (bytes) |
|---|---|
| `raypoolkit/RayWorkPool.py` | 26,152 |
| `raypoolkit/__init__.py` | 740 |
| `raypoolkit/_timing.py` | 2,373 |
| `raypoolkit/contract.py` | 1,886 |
| `raypoolkit-0.2.0.dist-info/licenses/LICENSE` | 11,357 |
| `raypoolkit-0.2.0.dist-info/METADATA` | 243 |
| `raypoolkit-0.2.0.dist-info/WHEEL` | 91 |
| `raypoolkit-0.2.0.dist-info/top_level.txt` | 11 |
| `raypoolkit-0.2.0.dist-info/RECORD` | 728 |

Extracted from each wheel, the four modules equal the tree's byte for byte (`cmp`). `METADATA`, in
both:

```
Metadata-Version: 2.4
Name: raypoolkit
Version: 0.2.0
Summary: A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks
Requires-Python: >=3.12
License-File: LICENSE
Requires-Dist: ray>=2.43
Dynamic: license-file
```

After (R2)'s build, the export's `raypoolkit.egg-info/SOURCES.txt` still lists the 10 test files
(§6, observation 3): setuptools still merges the stale manifest; the setting keeps the files out
of the wheel.

**The installs**, each into a fresh venv at the high end's pins, not editable:

```
$ uv venv --python /opt/local/bin/python3.13 $S/venv-wheel
$ uv pip install --python $S/venv-wheel/bin/python $S/dist-R2/raypoolkit-0.2.0-py3-none-any.whl "ray==2.55.1"
Using Python 3.13.16 environment at: venv-wheel
Resolved 18 packages in 658ms
Prepared 1 package in 33ms
Installed 18 packages in 314ms
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
 + raypoolkit==0.2.0 (from file://$S/dist-R2/raypoolkit-0.2.0-py3-none-any.whl)
 + referencing==0.37.0
 + requests==2.34.2
 + rpds-py==2026.9.1
 + urllib3==2.8.0
$ uv venv --python /opt/local/bin/python3.13 $S/venv-wheel-R1
$ uv pip install --python $S/venv-wheel-R1/bin/python $S/dist-R1/raypoolkit-0.2.0-py3-none-any.whl "ray==2.55.1"
Resolved 18 packages in 31ms
# … the same 18 packages, with raypoolkit==0.2.0 from $S/dist-R1/raypoolkit-0.2.0-py3-none-any.whl
```

**The check of (R2)**, from an empty directory outside the repository, `PYTHONPATH` unset, `-I`
(exit 0):

```
$ cd $S/empty && env -u PYTHONPATH $S/venv-wheel/bin/python -I $S/scripts/release_check.py $S/dist-R2/raypoolkit-0.2.0-py3-none-any.whl 0.2.0
cwd: $S/empty | PYTHONPATH: None | -I: 1
python: 3.13.16 | sys.path[0]: '/opt/local/Library/Frameworks/Python.framework/Versions/3.13/lib/python313.zip'
wheel: 9 entries, 0 under raypoolkit/tests/
PASS  file list: the four modules  [['raypoolkit/RayWorkPool.py', 'raypoolkit/__init__.py', 'raypoolkit/_timing.py', 'raypoolkit/contract.py']]
PASS  file list: LICENSE and the dist-info files  [['raypoolkit-0.2.0.dist-info/METADATA', 'raypoolkit-0.2.0.dist-info/RECORD', 'raypoolkit-0.2.0.dist-info/WHEEL', 'raypoolkit-0.2.0.dist-info/licenses/LICENSE', 'raypoolkit-0.2.0.dist-info/top_level.txt']]
PASS  file list: nothing under raypoolkit/tests/  [0]
PASS  import raypoolkit
PASS  from raypoolkit import RayWorkPool, DatastorePool
PASS  import_module('raypoolkit.RayWorkPool')  [$S/venv-wheel/lib/python3.13/site-packages/raypoolkit/RayWorkPool.py]
PASS  import_module('raypoolkit._timing')  [$S/venv-wheel/lib/python3.13/site-packages/raypoolkit/_timing.py]
PASS  import_module('raypoolkit.contract')  [$S/venv-wheel/lib/python3.13/site-packages/raypoolkit/contract.py]
PASS  raypoolkit.__file__ under the venv's site-packages  [$S/venv-wheel/lib/python3.13/site-packages/raypoolkit/__init__.py]
PASS  ray.is_initialized() is False  [ray 2.55.1]
PASS  import raypoolkit.tests raises ModuleNotFoundError  [No module named 'raypoolkit.tests']
PASS  version("raypoolkit") == "0.2.0"  [0.2.0]
PASS  requires("raypoolkit") == ["ray>=2.43"]  [['ray>=2.43']]
RESULT: OK (13 pass, 0 fail)
```

**The check of (R1)**, the same command with `$S/venv-wheel-R1` and (R1)'s wheel: the same 13
lines, each PASS, paths under `$S/venv-wheel-R1`; `RESULT: OK (13 pass, 0 fail)`, exit 0.

No Ray process before or after. `$S/empty` was still empty after. The wheels are not committed;
`git status` shows no `build/`, `dist/` or `*.egg-info`, and `--ignored` shows only
`raypoolkit.egg-info/`, `raypoolkit/__pycache__/` and `venv/`, as before.

### 3.4 `black` (prompt §3.4)

`./venv/bin/black --check raypoolkit docs` (25.1.0): "15 files would be left unchanged.", before
and after, exit 0. No Python file was changed; `black` was not run on the README, `PROVENANCE.md`
or `pyproject.toml`.

### 3.5 The links (prompt §3.5)

`$S/scripts/links.py`: every relative link in `README.md` (11) and `PROVENANCE.md` (3) resolves to
a file in `git ls-files`, and the README's two in-page anchors (`#changes-in-v020`,
`#which-handlers-a-pool-needs`) are the slugs of its headings. `RESULT: OK`.

### 3.6 The "Changes" statements on `v0.1.0`'s module and on the tree (clarification 1)

`$S/probes/probe_changes.py`, a `PoolTestCase` with eight tests that print one `PROBE` line per case
and assert nothing. Run once from a `git archive v0.1.0` export (`$S/export-v010`; its
`raypoolkit.__file__` the export's), and once from the repository root (the working tree's), each
with the throwaway `$S/venv-break-c` and `PYTHONPATH=$S/probes`; both `Ran 8 tests … OK`. Each run
case uses a fresh stand-in with a cap of 50 `wait` calls (more means `run()` makes no progress).

| Case | `v0.1.0` | the tree |
|---|---|---|
| no compute handler, nothing else | `RuntimeWarning` ("No compute maker was supplied, but a persist maker was provided…") | constructs |
| no compute handler, `persist_handler=None` | constructs | constructs |
| no compute handler, `store_handler=None`, `persist_handler=None` | constructs | constructs |
| no compute handler, `persist_handler=None`, explicit store handler | constructs (never called) | `ValueError` (`store_handler` would never be called) |
| no compute handler, `persist_handler=None`, validation handler | constructs | `ValueError` (`validation_handler`) |
| no compute handler, `persist_handler=None`, label builder | constructs | `ValueError` (`label_builder`) |
| no compute handler, explicit persist handler | `RuntimeWarning` | `ValueError` (`persist_handler`) |
| compute handler, `persist_handler=None` | `RuntimeError` ("If a compute maker is supplied, a persist maker must also be supplied…") | `ValueError` (`persist_handler` must not be None) |
| compute handler, `store_handler=None` | constructs; `run()` raises `TypeError: 'NoneType' object is not callable` | `ValueError` at construction (`store_handler` must not be None) |
| `create_batch_size=0`, lookup-only | constructs; `run()` past the wait cap (never ends) | `ValueError` ("create_batch_size must be at least 1, not 0") |
| `process_batch_size=0`, lookup-only | constructs; `run()` raises `ValueError: Invalid number of objects to return 0.` from `ray.wait` | `ValueError` ("process_batch_size must be at least 1, not 0") |
| `max_task_queue=0`, lookup-only | constructs; `run()` past the wait cap (never ends) | `ValueError` ("max_task_queue must be at least 1, not 0") |
| generator `task_list`, `store_results=True` | `TypeError: object of type 'generator' has no len()` | constructs |
| post handler after a persist, no validation handler | given `store_id=None`, not `results[0]` | given `store_id=1001`, `results[0]` |
| `fresh_refs` from `wait`, lookup-only | `KeyError: <bound method ObjectRef.hex of ObjectRef(…01)>` | completes |

Each "was" and "now" of README "Changes in `v0.2.0`" is a row of this table, and each "now" is also
asserted by a test of the suite (§4).

### 3.7 What prints, compared with `v0.1.0` (deviation 15)

`$S/scripts/printed_unchanged.py`: the module's `print()` calls, 7 at `v0.1.0` and 7 in the tree,
are equal by `ast.dump`; `_build_completed_status_message`, `_build_queued_status_message`,
`_format_rates` and `_readable_rate` are equal; `_timing.py` is equal by `ast.dump` (it differs by
the header comment only). The functions that differ are `store_ref` and `store_single_ref`, nested
in `run()`, by fault 1's `.hex()`.

### 3.8 The printed-line examples (clarification 4)

`$S/scripts/render_lines.py` ran
`test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass` with
`unittest.TestCase.assertEqual` wrapped to record the first list it compares. The test passed, the
actual lines equalled the expected, and they were:

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

Each of the README's six example lines (run on the final README) is one of these nine, leading
spaces included. Five are also literal in the test module; the progress line is not (the test
builds it with `progress(...)` and `SUFFIX`), as the clarification says.

### 3.9 The retired check, from a worktree of `v0.1.0` (clarification 5)

`$S/scripts/retired_check.sh`, `PROVENANCE.md`'s commands with `<scratch>` as `$S`:

```bash
cd /Users/ds283/Documents/Code/RayPoolKit
REPO=$(pwd)
git worktree add --detach $S/raypoolkit-v0.1.0 v0.1.0
cd $S/raypoolkit-v0.1.0
"$REPO"/venv/bin/python docs/extraction/compare_with_source.py
cd "$REPO"
git worktree remove $S/raypoolkit-v0.1.0
git worktree list
```

`Preparing worktree (detached HEAD 4e90a8a)`; the check printed 572 identical, 2 D-imp, 1 D-pool
and 0 unclassified in `RayWorkPool.py`, 4 D-int and the byte-for-byte span in `_timing.py`, 12
declared files present, 0 undeclared, `RESULT: OK`, **exit 0**, the counts of log 04 §3.3. The
worktree was removed, and `git worktree list` printed this checkout alone
(`/Users/ds283/Documents/Code/RayPoolKit 1868b6e [main]`).

## 4. The README's names, and how each was checked (prompt §2.2, §3.5)

`$S/scripts/readme_names.py`, run with `venv/`'s interpreter from the repository root on the final
README: **108 pass, 0 fail**, exit 0. It extracts every inline code span of the README outside
fenced blocks (84 distinct) and fails unless each is checked.

| README name | How checked | Found |
|---|---|---|
| `RayWorkPool`; `RayWorkPool(pool, task_list, task_builder, ...)` | `from raypoolkit import RayWorkPool`; `inspect.signature` | a class; 18 parameters, these three first, required, positional-or-keyword |
| `raypoolkit.DatastorePool`, `typing.Protocol` | imported; `_is_protocol`; `_is_runtime_protocol`; MRO | the protocol, not `runtime_checkable` |
| `object_store`, `object_store(obj)` | `vars(DatastorePool)`; `inspect.signature` | its one public member, `(self, objects) -> ObjectRef`, called with one object |
| `ObjectRef`, `ray.ObjectRef`, `ray.wait`, `ray.get`, `ray.init` | imported; `ray.wait(` and `ray.get(` in the module | present |
| `pool`, `task_list`, `compute_handler`, `store_handler`, `persist_handler`, `available_handler`, `validation_handler`, `post_handler`, `label_builder`, `create_batch_size`, `process_batch_size`, `max_task_queue`, `title` | each in `inspect.signature(RayWorkPool).parameters` | present; `pool` annotated `DatastorePool` |
| `task_builder(item)` | the parameter; `self._task_builder(item)` in the module | present |
| `create_batch_size=5`, `process_batch_size=1`, `max_task_queue=200`, `notify_min_time_interval=60`, `notify_time_interval=300`, `notify_batch_size=500`, `title=None`, `store_results=False` | signature default, value and type | as stated |
| `available_handler`, `validation_handler`, `post_handler`, `label_builder` defaults | signature default | `None` |
| `obj.compute(**kwargs)`, `compute(**kwargs)`; `obj.store()`, `store()`; `pool.object_store(obj)` | the source of each default handler | `_default_compute_handler` returns `obj.compute(**kwargs)`; `_default_store_handler` calls `obj.store()`; `_default_persist_handler` returns `pool.object_store(obj)` |
| `(obj, pool)` | the module | `self._store_handler(obj, self._pool)`, `self._persist_handler(obj, self._pool)` |
| `payload=`, `label=`, `"compute_payload"`, `{"ref": <ObjectRef>, "compute_payload": <anything>}` | the module | the compute arguments and the builder's dict, as stated |
| `run()` | `inspect.signature(RayWorkPool.run)` | `(self)` |
| `results`, `total_time`, `available`, `store_id`, `True`, `!! WARNING`, `None` | the module's source | `results` sized from `self._num_total_items`; `self.total_time`; `hasattr(obj, "available")`; `store_id={obj.store_id}`; `is not True`; the warning; `is not None` |
| `task_list` (any iterable, consumed) | `self._todo = [x for x in task_list]`; the generator guard (below) | as stated |
| `len()` | `range(len(task_list))` in `v0.1.0`'s module, absent from the tree's | as stated |
| `ValueError` | three `raise ValueError(` in the constructor; tests below | as stated |
| `RuntimeError` | raised by the module (5 sites), none in the constructor; in `v0.1.0`'s constructor (§3.6) | as stated |
| `RuntimeWarning` | `raise RuntimeWarning(` in `v0.1.0`'s module, absent from the tree's; §3.6 | as stated |
| `TypeError` | §3.6 (`v0.1.0`'s `run()` with `store_handler=None`; its `len(task_list)`) | as stated |
| `compute_handler=None`, `store_handler=None`, `persist_handler=None`, `store_results=True` | the parameters exist; their meaning by the tests below and §3.6 | as stated |
| `Work`, `compute()`, `Blob`, `StandinDatastorePool` | imported from `raypoolkit.tests.standins`; instances inspected | `Work` has `available`, `compute`, `store`; `Blob` has no `available`; `object_store` callable |
| files: `PROVENANCE.md`, `LICENSE`, `pyproject.toml`, `.github/workflows/tests.yml`, `raypoolkit/tests/standins.py`, `raypoolkit/tests/test_printed_lines.py`, `docs/extraction/compare_with_source.py`, `prompts/extraction/README.md`, `prompts/extraction/IMPLEMENTATION_STATE.md` | `git ls-files` | all tracked |
| `v0.2.0`, `v0.1.0`, `>=3.12`, `>=2.43` | `pyproject.toml` (by `tomllib`); `git rev-parse refs/tags/v0.1.0` | `0.2.0`; the tag exists; as declared |
| `RayTools/RayWorkPool.py`, `b510bc9` | `PROVENANCE.md` | as stated |
| `requirements.txt`, `pip install -e`, `black --check raypoolkit docs`, `git`, `git worktree` | not Python names | — |

**The statements of "Changes in `v0.2.0`" and "Which handlers a pool needs"**, each by a test that
asserts it (each exists, by the loader, and passed in every run of §3.1), and by §3.6 for the
`v0.1.0` side:

| Statement | Test |
|---|---|
| no compute handler: an explicit store, persist, validation handler or label builder raises `ValueError`, naming it ("would never be called") | `test_construction.TestHandlerChecks.test_an_explicit_compute_path_argument_without_a_compute_handler_raises_value_error` (message whole) |
| a compute handler with `store_handler=None` raises `ValueError` at construction ("leave it out to use the default") | `test_construction.TestHandlerChecks.test_a_compute_handler_with_store_handler_none_raises_value_error`; `test_inherited_faults.TestInheritedFaults.test_store_handler_none_with_compute_is_refused_at_construction` |
| a compute handler with `persist_handler=None` raises `ValueError` | `test_construction.TestHandlerChecks.test_a_compute_handler_with_persist_handler_none_raises_value_error` |
| a size below 1 raises `ValueError`, giving the value | `test_construction.TestSizeChecks.test_a_size_below_one_raises_value_error` |
| a pool with no compute handler needs only `compute_handler=None`; `store_handler=None` and `persist_handler=None` accepted | `test_construction.TestHandlerChecks.test_a_pool_without_a_compute_handler_constructs_however_it_is_spelled`; `test_inherited_faults.TestInheritedFaults.test_a_lookup_only_pool_needs_no_persist_handler` |
| the same lines however it is spelled | `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_pool_prints_the_same_lines_however_its_handlers_are_spelled` |
| with a compute handler, the default persist handler applies | `test_construction.TestDefaultHandlers.test_the_default_persist_handler_calls_object_store_on_the_pool` |
| the post handler after a persist gets the persisted object, `results[0]`, with its `store_id` | `test_inherited_faults.TestInheritedFaults.test_the_post_handler_after_persist_gets_the_persisted_object`; `test_run_paths.TestComputeStoreValidate.test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler` |
| `store_results=True` accepts a generator `task_list` | `test_inherited_faults.TestInheritedFaults.test_store_results_accepts_a_generator_task_list` |
| in-flight work keyed on each ref's value; `wait` may return fresh refs | `test_inherited_faults.TestInheritedFaults.test_fresh_refs_from_wait_complete_every_path` |
| `available_handler` and `post_handler` on a pool with no compute handler | `test_run_paths.TestAvailable.test_available_with_an_availability_handler_runs_an_available_task` |
| the printed lines are unchanged | the README's examples are this test's lines (§3.8); §3.7 |
| the four package modules carry the header (Licence) | `test_inherited_faults.TestInheritedFaults.test_every_package_module_carries_the_licence_header` |

## 5. The deliberate-breakage record (prompt §3.6)

Each diff is against `eaef0ce`'s `pyproject.toml`, exactly as applied, made with `diff -u` from
edited copies in `$S/mk/` and saved in `$S/diffs/`. Each was applied with `git apply` run in its
own fresh export (`bash $S/scripts/build.sh <label> <manifest> $S/diffs/<label>.diff`, §3.3), after
`git apply --check` there ("ok"), and `git apply -R --check` passed after. Each wheel was installed,
with `ray==2.55.1`, into its own throwaway 3.13.16 venv (`$S/venv-break-<label>`), and the release
check run as in §3.3, expecting `0.2.0`. The low, high and wheel venvs were not touched.

**Summary.** (a) fails: 19 entries, 10 under `raypoolkit/tests/`, the warning printed (2 lines).
(b) fails: 19 entries, and `import raypoolkit.tests` succeeds from the wheel. (c) fails the
version check. **3 items, 3 fail as the prompt says.**

### (a) The issue, back

The `[tool.setuptools]` table removed, and the repository's `raypoolkit.egg-info/` copied in
(`Version: 0.1.0`, `grep -c tests/ SOURCES.txt` **10**).

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -11,9 +11,6 @@
     "ray>=2.43",
 ]
 
-[tool.setuptools]
-include-package-data = false
-
 [tool.setuptools.packages.find]
 include = ["raypoolkit*"]
 exclude = ["raypoolkit.tests", "raypoolkit.tests.*"]
```

Build log `$S/out/build-a.log`, 127 lines; `grep -c "absent from"`: **2**, at lines 26 and 34:

```
/Users/ds283/.cache/uv/builds-v0/.tmp2AucrS/lib/python3.14/site-packages/setuptools/command/build_py.py:215: _Warning: Package 'raypoolkit.tests' is absent from the `packages` configuration.
        but it is absent from setuptools' `packages` configuration.
```

The wheel: `raypoolkit-0.2.0-py3-none-any.whl`, **42,737 bytes**, SHA-256
`565c2d1aaadee950209d87a2bbca1254a12c528d9116b96d915e601adc304267`, **19 entries, 10 under
`raypoolkit/tests/`** (`__init__.py`, `standins.py` and the eight `test_*.py`; `RECORD` 1,650
bytes). The check, exit 1:

```
wheel: 19 entries, 10 under raypoolkit/tests/
FAIL  file list: the four modules  [[... the four modules and the ten raypoolkit/tests/ files ...]]
PASS  file list: LICENSE and the dist-info files  [...]
FAIL  file list: nothing under raypoolkit/tests/  [10]
PASS  import raypoolkit
PASS  from raypoolkit import RayWorkPool, DatastorePool
PASS  import_module('raypoolkit.RayWorkPool')  [$S/venv-break-a/lib/python3.13/site-packages/raypoolkit/RayWorkPool.py]
PASS  import_module('raypoolkit._timing')  [...]
PASS  import_module('raypoolkit.contract')  [...]
PASS  raypoolkit.__file__ under the venv's site-packages  [...]
PASS  ray.is_initialized() is False  [ray 2.55.1]
FAIL  import raypoolkit.tests raises ModuleNotFoundError  [it imported]
PASS  version("raypoolkit") == "0.2.0"  [0.2.0]
PASS  requires("raypoolkit") == ["ray>=2.43"]  [['ray>=2.43']]
RESULT: FAILED (10 pass, 3 fail)
```

### (b) The setting alone

The table kept, the `exclude` removed, no manifest copied.

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -16,4 +16,3 @@
 
 [tool.setuptools.packages.find]
 include = ["raypoolkit*"]
-exclude = ["raypoolkit.tests", "raypoolkit.tests.*"]
```

Build log `$S/out/build-b.log`, 88 lines; "absent from": 0 (the tests are a found package, so
`build_py` copies `raypoolkit/tests/` as one, from line 20). The wheel:
`raypoolkit-0.2.0-py3-none-any.whl`, **42,737 bytes**, SHA-256
`6737d9b2efcf32c607f118408b21404f58115fef4452e211d09830fbcc916e16`, **19 entries, 10 under
`raypoolkit/tests/`**. The check, exit 1: the same three FAILs as (a), among them
`FAIL  import raypoolkit.tests raises ModuleNotFoundError  [it imported]`;
`RESULT: FAILED (10 pass, 3 fail)`. So the setting alone does not keep the tests out: the exclusion
is needed too.

### (c) The version not moved

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "raypoolkit"
-version = "0.2.0"
+version = "0.1.0"
 description = "A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks"
 requires-python = ">=3.12"
 dependencies = [
```

Build log `$S/out/build-c.log`, 56 lines; "absent from": 0. The wheel:
`raypoolkit-0.1.0-py3-none-any.whl`, **13,564 bytes**, SHA-256
`72aec363ec47d59bb30998b2c0565ee5df921be53716b8fd51d945d89a75ff18`, 9 entries, 0 under
`raypoolkit/tests/`. The check, exit 1:

```
wheel: 9 entries, 0 under raypoolkit/tests/
PASS  file list: the four modules  [...]
FAIL  file list: LICENSE and the dist-info files  [['raypoolkit-0.1.0.dist-info/METADATA', 'raypoolkit-0.1.0.dist-info/RECORD', 'raypoolkit-0.1.0.dist-info/WHEEL', 'raypoolkit-0.1.0.dist-info/licenses/LICENSE', 'raypoolkit-0.1.0.dist-info/top_level.txt']]
PASS  file list: nothing under raypoolkit/tests/  [0]
PASS  import raypoolkit
PASS  from raypoolkit import RayWorkPool, DatastorePool
PASS  import_module('raypoolkit.RayWorkPool')  [...]
PASS  import_module('raypoolkit._timing')  [...]
PASS  import_module('raypoolkit.contract')  [...]
PASS  raypoolkit.__file__ under the venv's site-packages  [...]
PASS  ray.is_initialized() is False  [ray 2.55.1]
PASS  import raypoolkit.tests raises ModuleNotFoundError  [No module named 'raypoolkit.tests']
FAIL  version("raypoolkit") == "0.2.0"  [0.1.0]
PASS  requires("raypoolkit") == ["ray>=2.43"]  [['ray>=2.43']]
RESULT: FAILED (11 pass, 2 fail)
```

## 6. Observations not acted on

1. **`PROVENANCE.md`'s "New here, with no source" lists only 01's new files** (`__init__.py`,
   `contract.py`, `tests/__init__.py`, the guard), though `v0.1.0` declared 12 files with no
   source (02 added the suite). It records the import made by 01, and §2.3 changes nothing else in
   the file. No issue (clarification 6).
2. **`PROVENANCE.md`'s D-fmt bullet says "the package module's line numbers are SGK's"**: true at
   `v0.1.0`, not of `v0.2.0`, whose header moves every line. The section now opens "At `v0.1.0`,
   …", so it reads as of the tag. No issue.
3. **The stale manifest persists, and no longer matters.** After (R2)'s build the export's
   `SOURCES.txt` still lists the 10 test files, and so does the repository's after every editable
   install of this log (`PKG-INFO` now `Version: 0.2.0`). setuptools still merges it; with the
   setting, none of its files reaches the wheel. The prompt's §6 leaves the directory alone. No
   issue.
4. **`uv build` ran setuptools under Python 3.14** (`raypoolkit-0.2.0-py3.14.egg-info` in each build
   log), as log 03 §6.2 found; the wheel is `py3-none-any`. No issue.
5. **Tool-internal temporary directories outside the scratch directory**: `venv/`'s reinstall built
   in `pip`'s system temporary directory, and `uv build` under `~/.cache/uv/builds-v0/`, as in 03.
   Neither is in the repository.

## 7. Issues

**Opened:** none. **Closed** (board §3 → §4, with a dated **Resolved (05)** line):
`[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`. **Narrowed:** none.
`docs/OPEN_ISSUES.md` goes from 1 to **0** open.

## 8. State handed to the next prompt

- `HEAD` is `eaef0ce`. `raypoolkit/` is unchanged since `0b6ffd2`.
- **`pyproject.toml`**: `raypoolkit` `0.2.0`, `requires-python = ">=3.12"`, `ray>=2.43`, the test
  package excluded from the packages and package data off. `venv/` holds `0.2.0`, editable.
- **Suite: 121 tests**, passing at 3.12.15 / 2.43.0 and 3.13.16 / 2.55.1 on macOS. CI has not run on
  `eaef0ce`; it runs when the commit is pushed.
- **`v0.2.0` is ready to be tagged on `eaef0ce` once CI passes there at both ends.** No tag was
  made and nothing was pushed (README §5 rule 10). If CI fails, no tag: a fix prompt lands first.
  Local `main` is ahead of `origin/main` (`914070c`) by `f839209`, `1868b6e` and `eaef0ce`.
- `README.md` describes `v0.2.0`, with the pin `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0`,
  written as of the tag; 06's checklists are measured against it.
- The drivers, probes and wheels (`$S/`) are not committed; every diff they applied is in §5,
  exactly as applied.
