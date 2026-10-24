# Log — rehearsal-lock prompt 03: release `v0.3.0`

**Subject:** Make the release v0.3.0 with the rehearsal lock's contract · **Commit:** this commit ·
**Date:** 2026-10-24 · **Agent:** Claude Opus 5.5

**Result: landed; `v0.3.0` is ready to be tagged once CI passes on this commit. No tag was made,
and nothing was pushed.**
- `pyproject.toml` says `0.3.0`, with the new description: two lines, nothing else.
- `docs/rehearsal-lock.md` is new: the contract of the lock, in the prompt's eleven sections, naming
  no client. Its **98 statements** are numbered in §3.5 below, and each is checked by a test, a
  probe or 02's log. **11 rest on a probe alone**, and in 22 more a probe checks a part that no
  test asserts (§3.5's last paragraph). None needed a change under `raypoolkit/`.
- `README.md`, `PROVENANCE.md` and `CLAUDE.md` are true of `v0.3.0`.
- The suite is **226 → 226**, `OK` in `venv/` (now reporting `0.3.0`) and in fresh venvs at both
  tested ends.
- The release check passes with and without the repository's manifest copied in: 10 entries, none
  under `raypoolkit/tests/`, 21,368 bytes. Breakage (a) and (b) fail as the prompt says.
- **No issue is opened**; the index stays at 0.
- Nothing under `raypoolkit/`, `docs/rehearsal-lock/`, `docs/adoption/`, `docs/extraction/` or
  `.github/` changed. No Ray was started. Neither lock location under the real `HOME` was touched.
  No client was edited or run.

**Gate, re-checked at start (12:01).**
- `HEAD` was `8c0dfff` (the orchestration note), on `6e0ba38`. The tree was clean, and this
  checkout was the only worktree. Tags `v0.1.0` and `v0.2.0`.
- `venv/`: `Ran 226 tests in 2.653s` `OK`. `importlib.metadata` gave `0.2.0` and `['ray>=2.43']`.
  `./venv/bin/black --check raypoolkit docs`: "20 files would be left unchanged."
- No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` exit 1), and no `RAY_*` variable.
- `~/ScienceData` is a directory; `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` did not exist.
- The repository's `raypoolkit.egg-info/PKG-INFO` said `Version: 0.2.0`, and its `SOURCES.txt`
  listed 10 files under `raypoolkit/tests/` (not `test_rehearsal_lock.py`).
- The clients, read only through `git`: SGK `216e44d` (`handover-remedial`), CPBH `807f175`
  (`jordan-normalization`) and SI `7071bb8` (`rrk-adoption`). Each pins `raypoolkit @
  git+https://github.com/ds283/RayPoolKit@v0.2.0` in `requirements.txt` and has no `RayTools/`.
  SGK's `tools/rehearsal_lock.py` and its tests are blobs `ea14336` and `cdeecd6`; CPBH's
  `ray_cluster.sh` is `eaae1e7`; SI's is `6c8eada` at both `8b4f615` and `7071bb8`; the brief is
  `d86ad43` at `8b4f615`.

Every scratch file of this log (venvs, exports, wheels, `HOME`s, scripts, diffs, outputs) is under
the agent's scratch directory, `…/scratchpad/agent03/`, written `$S` below.

## 1. What shipped

| File | What |
|---|---|
| `pyproject.toml` | `version = "0.3.0"`; the description of §2.1 |
| `docs/rehearsal-lock.md` (new) | the contract: §1–§11 of the prompt's §2.2, with clarifications 1–6 |
| `README.md` | the opening paragraph; Status; "Changes in `v0.3.0`"; one Supported-versions item; the pin; "The rehearsal lock"; one Developing paragraph; "five" modules |
| `PROVENANCE.md` | the opening's subject; the end of "Since `v0.1.0`"; "Since `v0.2.0`" (new); one sentence closing the freeze |
| `CLAUDE.md` | "What this repository is": the first sentence and the table; "Releases": the lock as an interface; "Repository mechanics": one bullet |
| this log, the board, `prompts/INDEX.md` | the records |

`docs/OPEN_ISSUES.md` is unchanged: nothing was opened.

`pyproject.toml`, as committed against `8c0dfff`:

```diff
@@ -4,8 +4,8 @@ build-backend = "setuptools.build_meta"
 
 [project]
 name = "raypoolkit"
-version = "0.2.0"
-description = "A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks"
+version = "0.3.0"
+description = "A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks, and a shared rehearsal lock for Ray runs"
 requires-python = ">=3.12"
 dependencies = [
     "ray>=2.43",
```

`git diff v0.2.0 HEAD -- raypoolkit` at `8c0dfff` holds only `rehearsal_lock.py`, its tests and the
guard's (`test_package_imports.py`). `RayWorkPool.py`, `contract.py`, `_timing.py` and
`__init__.py` are `v0.2.0`'s (`git diff --stat` empty), which the README's "unchanged" rests on.

## 2. Deviations from the prompt

The orchestrator's clarifications (twelve), each applied:

1. **The Python API as the module has it** (clarification 1): the five command functions are
   `acquire`, `set_pid`, `release`, `status` and `ray_processes_command`; `ray_processes` is the rule
   and returns tuples; a bad argument raises `ValueError` and no function returns 2; `lock_dir` is a
   keyword of the first four only; `ps_text` and `self_pid` are test seams. The prompt's §2.2
   item 2 ("the five functions are a Python API with the same exit codes") would have been untrue
   of `ray_processes`. Contract §2. **STRUCTURALLY REQUIRED.**
2. **A Ray driver cannot see its own instance through the API** (clarification 2). Contract §2 and
   §6, and the README's lock section. Checked by probe P2 on the a1 rows of 02's log (§3.9).
   IMPLEMENTATION CHOICE at the orchestrator's direction.
3. **Every exit code as the module has it** (clarification 3), in contract §7: `acquire` 4 for the
   client server too, and its "could not release the lock again"; `set-pid`'s and `release`'s
   further 1s; `ray-processes` 1 for an unreadable table; `status` 0 always; the unhandled
   `OSError` with exit 1 and no traceback as interface. Not a deviation (the clarification says so).
4. **The match, identity and argument checks stated exactly** (clarification 4): no leading
   boundary ("contains … followed by"); the client-server seed's two parts; identity by the strings
   as given; `/`; the split at the last colon, with no range check; the hostname fallback; the
   three cases of `owner pid: -`. Not deviations (the clarification says so).
5. **The lock is a directory** (clarification 5): contract §3, §7 and §8 state each condition as
   "not a directory", quoting `lock: free (<path> does not exist)`. Observation 1 of §5.
   IMPLEMENTATION CHOICE at the orchestrator's direction.
6. **What goes where, and how a process is printed** (clarification 6): contract §7's last list,
   and §8 pinned line by line to tests. IMPLEMENTATION CHOICE at the orchestrator's direction.
7. **The release check as `extraction` 05 ran it** (clarification 7): no `-q`; `grep -c "absent
   from"` recorded; the manifest's `Version:` and test count recorded before (R2); one fresh export
   per build; each diff `git apply --check`ed, applied and `-R --check`ed in the export.
   IMPLEMENTATION CHOICE at the orchestrator's direction.
8. **The `ray-processes` check from a script file** (clarification 8), with `/tmp/ray-rpk03-none` in
   a variable inside `$S/scripts/release_check.py`, named in no argv. IMPLEMENTATION CHOICE at the
   orchestrator's direction.
9. **The README's statements of the outside world** (clarification 9): "Ray up to 2.59.0 today" is
   kept, on the orchestrator's reading of PyPI of 2026-10-24 (not re-read here: this agent made no
   download beyond the venvs' packages). "Changes in `v0.3.0`" says nothing of when a project moves
   its pin. IMPLEMENTATION CHOICE at the orchestrator's direction.
10. **`CLAUDE.md`'s exceptions are not reworded** (clarification 10). Observation 2 of §5.
    IMPLEMENTATION CHOICE at the orchestrator's direction.
11. **`venv/` is not rebuilt**: its reinstall is `--no-deps`; every other venv is a fresh `uv` venv
    in `$S` (clarification 11). IMPLEMENTATION CHOICE at the orchestrator's direction.
12. **The board's header and 03's row, and `prompts/INDEX.md`**, are updated here; README §2's
    status for 03 is left to the review (clarification 12). IMPLEMENTATION CHOICE at the
    orchestrator's direction.

This agent's own:

13. **The import cost is "a few tenths of a second a call (0.3–0.6 s measured at Ray 2.43.0)"**,
    where the prompt's §2.2 item 2 says "about 0.3 s". Measured today in `venv/` (five runs, `import
    ray` timed with `perf_counter` in `-I`): 0.625, 0.465, 0.472, 0.409, 0.372 s; README §0.3 has
    0.28–0.30 s at 2.43.0 on 2026-10-23. "About 0.3 s" would understate today's figures.
    IMPLEMENTATION CHOICE.
14. **The README's `v0.2.0` paragraph keeps its client-naming line unchanged.** §2.3 asks for
    `v0.2.0`'s description "with the faults inherited from SGK's copy fixed"; §3.7 asks that the
    README's new and changed text name no client. The paragraph's first line was cut to
    "**`v0.2.0`** is `v0.1.0` with the faults inherited", and its next line, naming
    SecondaryGWKit, is the original line, unchanged in the diff. So both hold: the grep over the
    README's added lines finds nothing (§3.7). IMPLEMENTATION CHOICE.
15. **`CLAUDE.md` gains one sentence under the table**: "Each client's `RayTools/` copy of the pool
    is gone." The old column was about the copies; the new one is about the pins and the locks, so
    the fact the old one held is kept in a line of its own. IMPLEMENTATION CHOICE.
16. **The contract says a little more than §2.2 lists**, each probed: a non-directory at the lock's
    path (P10); an empty owner file's line in `status` (P9); `release`'s order of checks (P27), and
    that a failed `rmdir` leaves the lock without its owner file (P13); `acquire` and `status` not
    checking identity (P24); `set-pid`, `release` and `ray-processes` ignoring the old location
    (P18); a process the caller may not signal counting as live (P22). Each is something a caller
    can meet, and each is true of the module. IMPLEMENTATION CHOICE.
17. **The contract's opening points at this log** for the statement-by-statement checks, and
    qualifies its claim to "every statement about the module": two of its statements are guidance
    from outside the module (S45, the socket-path limit; S92, what the old-location refusal cannot
    catch). IMPLEMENTATION CHOICE.
18. **The release check also installs and checks (R1)**, in a venv of its own, and runs the
    command-line items in the same script as the imports. IMPLEMENTATION CHOICE: more than the
    prompt asks, and nothing less.
19. **PROVENANCE's list of what came from SGK's module follows the module's docstring**, which also
    names `_short_hostname`, `_ps_output` and the messages; the prompt's list is a subset ("as its
    docstring names them"). IMPLEMENTATION CHOICE.
20. **The README's caller sequence names the two ways to start Ray** (`ray.init(address="local",
    _temp_dir=D)`, `ray start --head --temp-dir D …`) and whose pid `set-pid` records, and closes
    with clarification 2's rule. IMPLEMENTATION CHOICE.

No UNINTENDED DRIFT was found.

## 3. Verification performed

### 3.1 The suite (prompt §3.1)

Every run is `<python> -m unittest discover -s raypoolkit/tests -t .` from the repository root, in
the foreground, its output written to `$S/out/suite-*.txt` and the verdict read from it. No Ray
process before or after any run (`pgrep` exit 1 each time).

| Venv | `sys.version` | `ray` | `raypoolkit` | Verdict |
|---|---|---|---|---|
| `venv/`, before | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | 0.2.0 | `Ran 226 tests in 2.653s` `OK` |
| `venv/`, after §3.2 | as above | 2.43.0 | 0.3.0 | `Ran 226 tests in 2.707s` `OK` |
| `$S/venv312` (fresh) | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | 0.3.0 | `Ran 226 tests in 3.100s` `OK` |
| `$S/venv313` (fresh) | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | 0.3.0 | `Ran 226 tests in 3.280s` `OK` |

By module (the loader's count, `venv/`, after): `test_construction` 15, `test_inherited_faults` 6,
`test_package_imports` 5, `test_printed_lines` 18, `test_rehearsal_lock` 103, `test_run_paths` 22,
`test_scheduling` 7, `test_standins` 30, `test_task_builder` 20; **226**. The count before and after
is **226, 226**.

**The installs, as run:**

```text
$ uv venv -p /opt/local/bin/python3.12 $S/venv312
Using CPython 3.12.15 interpreter at: /opt/local/bin/python3.12
$ uv pip install --python $S/venv312/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray==2.43.0" "black==25.1.0"
Resolved 25 packages in 256ms
Installed 25 packages in 110ms        (exit 0)
$ uv venv -p /opt/local/bin/python3.13 $S/venv313
Using CPython 3.13.16 interpreter at: /opt/local/bin/python3.13
$ uv pip install --python $S/venv313/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray==2.55.1" "black==25.1.0"
Resolved 22 packages in 6ms
Installed 22 packages in 118ms        (exit 0)
```

`uv` 0.12.20. **`uv pip freeze`**:
- `$S/venv312`: aiosignal==1.4.0 attrs==26.1.0 black==25.1.0 certifi==2026.10.23
  charset-normalizer==3.5.2 click==8.5.0 filelock==4.2.4 frozenlist==1.8.0 idna==3.20
  jsonschema==4.26.0 jsonschema-specifications==2025.9.1 msgpack==1.2.3 mypy-extensions==1.1.0
  packaging==26.3 pathspec==1.1.1 platformdirs==4.13.5 protobuf==7.36.2 pyyaml==6.0.3 ray==2.43.0
  `-e file:///Users/ds283/Documents/Code/RayPoolKit` referencing==0.37.0 requests==2.34.2
  rpds-py==2026.9.1 typing-extensions==4.16.0 urllib3==2.8.0
- `$S/venv313`: the same less aiosignal, frozenlist and typing-extensions, with ray==2.55.1.
- `venv/` (`pip freeze`, after): aiosignal==1.4.0 attrs==26.1.0 black==25.1.0 certifi==2026.7.22
  charset-normalizer==3.5.2 click==8.5.0 filelock==4.1.0 frozenlist==1.8.0 idna==3.20
  jsonschema==4.26.0 jsonschema-specifications==2025.9.1 msgpack==1.2.3 mypy_extensions==1.1.0
  packaging==26.3 pathspec==1.1.1 platformdirs==4.12.4 protobuf==7.36.2 PyYAML==6.0.3 ray==2.43.0
  `-e git+https://github.com/ds283/RayPoolKit.git@8c0dfff…#egg=raypoolkit` referencing==0.37.0
  requests==2.34.2 rpds-py==2026.9.1 typing_extensions==4.16.0 urllib3==2.8.0: as 01 recorded it,
  but for the editable line.

### 3.2 `venv/`'s metadata (prompt §3.2)

```text
$ ./venv/bin/python -m pip install --no-deps -e .
…
Successfully built raypoolkit
  Attempting uninstall: raypoolkit
    Found existing installation: raypoolkit 0.2.0
    Uninstalling raypoolkit-0.2.0:
      Successfully uninstalled raypoolkit-0.2.0
Successfully installed raypoolkit-0.3.0        (exit 0)
```

| | `importlib.metadata.version` | `requires` |
|---|---|---|
| before | `0.2.0` | `['ray>=2.43']` |
| after | `0.3.0` | `['ray>=2.43']` |

The reinstall rewrote `raypoolkit.egg-info/` (allowed): `PKG-INFO` now says `Version: 0.3.0`, and
`SOURCES.txt` still lists **10** files under `raypoolkit/tests/`, as before (observation 3).

### 3.3 The release check (prompt §3.3)

**The builds.** `$S/scripts/build.sh <label> <manifest> [diff]`, in `bash`, one fresh export per
build, never in the repository tree:

```bash
test ! -e $S/export-<label> && mkdir $S/export-<label>
git -C $R archive HEAD | tar -x -C $S/export-<label>
cp $R/pyproject.toml $S/export-<label>/pyproject.toml     # the working tree's, §2.1
cp -R $R/raypoolkit.egg-info $S/export-<label>/          # (R2) only
(cd $S/export-<label> && git apply --check <diff> && git apply <diff> && git apply -R --check <diff>)   # (a), (b) only
uv build --wheel --out-dir $S/dist-<label> $S/export-<label> > $S/out/build-<label>.log 2>&1
```

`$R` is the repository root and `HEAD` was `8c0dfff`. Each export held `.github`, `.gitignore`,
`CLAUDE.md`, `docs`, `LICENSE`, `prompts`, `PROVENANCE.md`, `pyproject.toml`, `raypoolkit` and
`README.md`, and (R2)'s also `raypoolkit.egg-info`. `pyproject.toml` is the only file 03 changes
that the build reads (it has no `readme` key). Before (R2)'s copy, the repository's manifest said
`Version: 0.3.0` (rewritten by §3.1's and §3.2's editable installs) and `grep -c tests/
raypoolkit.egg-info/SOURCES.txt` gave **10**.

**(R2)'s build log, whole** (`$S/out/build-R2.log`, 57 lines; `grep -c "absent from"`: **0**):

```text
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
copying raypoolkit/rehearsal_lock.py -> build/lib/raypoolkit
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
copying build/lib/raypoolkit/rehearsal_lock.py -> build/bdist.macosx-27.0-arm64/wheel/./raypoolkit
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
Copying raypoolkit.egg-info to build/bdist.macosx-27.0-arm64/wheel/./raypoolkit-0.3.0-py3.14.egg-info
running install_scripts
creating build/bdist.macosx-27.0-arm64/wheel/raypoolkit-0.3.0.dist-info/WHEEL
creating '$S/dist-R2/.tmp-bq23uddy/raypoolkit-0.3.0-py3-none-any.whl' and adding 'build/bdist.macosx-27.0-arm64/wheel' to it
adding 'raypoolkit/RayWorkPool.py'
adding 'raypoolkit/__init__.py'
adding 'raypoolkit/_timing.py'
adding 'raypoolkit/contract.py'
adding 'raypoolkit/rehearsal_lock.py'
adding 'raypoolkit-0.3.0.dist-info/licenses/LICENSE'
adding 'raypoolkit-0.3.0.dist-info/METADATA'
adding 'raypoolkit-0.3.0.dist-info/WHEEL'
adding 'raypoolkit-0.3.0.dist-info/top_level.txt'
adding 'raypoolkit-0.3.0.dist-info/RECORD'
removing build/bdist.macosx-27.0-arm64/wheel
Successfully built $S/dist-R2/raypoolkit-0.3.0-py3-none-any.whl
```

**(R1)'s build log** (`$S/out/build-R1.log`, 59 lines; "absent from": **0**) differs only by two
lines (`creating raypoolkit.egg-info`, and a first `writing manifest file` before the read, since
the export has no manifest) and its scratch paths. Each log's only warnings are the two
"byte-compiling is disabled" lines. After (R2)'s build, the export's `SOURCES.txt` still lists the
10 test files: setuptools merges the stale manifest, and `include-package-data = false` keeps the
files out.

**The wheels.**

| | (R1) | (R2) |
|---|---|---|
| Name | `raypoolkit-0.3.0-py3-none-any.whl` | `raypoolkit-0.3.0-py3-none-any.whl` |
| Size | **21,368 bytes** | **21,368 bytes** |
| Entries | **10** | **10** |
| Under `raypoolkit/tests/` | **0** | **0** |
| SHA-256 | `739054029da8451fb21da0520d34e0bbf456b9b5dc6aaad897f8552d7fc6be10` | `3274c2af94f56aa36690379f86691a49356f2db2dc7b8075e656ff276a347d34` |
| "absent from" | 0 | 0 |

The SHA-256s differ by the zip timestamps. The file lists are the same, entry by entry:

| Entry | Size (bytes) |
|---|---|
| `raypoolkit/RayWorkPool.py` | 26,152 |
| `raypoolkit/__init__.py` | 740 |
| `raypoolkit/_timing.py` | 2,373 |
| `raypoolkit/contract.py` | 1,886 |
| `raypoolkit/rehearsal_lock.py` | 27,043 |
| `raypoolkit-0.3.0.dist-info/licenses/LICENSE` | 11,357 |
| `raypoolkit-0.3.0.dist-info/METADATA` | 285 |
| `raypoolkit-0.3.0.dist-info/WHEEL` | 91 |
| `raypoolkit-0.3.0.dist-info/top_level.txt` | 11 |
| `raypoolkit-0.3.0.dist-info/RECORD` | 814 |

Unzipped, the five modules of each wheel equal the tree's byte for byte (`cmp`). `METADATA`, in
both:

```text
Metadata-Version: 2.4
Name: raypoolkit
Version: 0.3.0
Summary: A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks, and a shared rehearsal lock for Ray runs
Requires-Python: >=3.12
License-File: LICENSE
Requires-Dist: ray>=2.43
Dynamic: license-file
```

**The installs**, each into a fresh venv at the high end's pins, not editable:

```text
$ uv venv -p /opt/local/bin/python3.13 $S/venv-wheel-R2
$ uv pip install --python $S/venv-wheel-R2/bin/python $S/dist-R2/raypoolkit-0.3.0-py3-none-any.whl "ray==2.55.1"
Resolved 18 packages in 8ms
Installed 18 packages in 121ms
 + raypoolkit==0.3.0 (from file://$S/dist-R2/raypoolkit-0.3.0-py3-none-any.whl)        (exit 0)
$ uv venv -p /opt/local/bin/python3.13 $S/venv-wheel-R1
$ uv pip install --python $S/venv-wheel-R1/bin/python $S/dist-R1/raypoolkit-0.3.0-py3-none-any.whl "ray==2.55.1"
Resolved 18 packages in 4ms
Installed 18 packages in 63ms        (exit 0)
```

`$S/venv-wheel-R2`'s freeze: attrs, certifi, charset-normalizer, click, filelock, idna, jsonschema,
jsonschema-specifications, msgpack, packaging, protobuf, pyyaml, `ray==2.55.1`, `raypoolkit @
file://…/dist-R2/…whl`, referencing, requests, rpds-py, urllib3.

**The check of (R2)**, `$S/scripts/release_check.py`, from an empty directory, `PYTHONPATH` unset,
`-I`; its command-line items run the venv's interpreter with `HOME` set to the empty
`$S/home-rc-R2` (exit 0):

```text
$ cd $S/empty-R2 && env -u PYTHONPATH $S/venv-wheel-R2/bin/python -I $S/scripts/release_check.py $S/dist-R2/raypoolkit-0.3.0-py3-none-any.whl 0.3.0 $S/home-rc-R2
cwd: $S/empty-R2 | PYTHONPATH: None | -I: 1
python: 3.13.16 | sys.path[0]: '/opt/local/Library/Frameworks/Python.framework/Versions/3.13/lib/python313.zip'
wheel: 10 entries, 0 under raypoolkit/tests/
PASS  file list: the five modules  [['raypoolkit/RayWorkPool.py', 'raypoolkit/__init__.py', 'raypoolkit/_timing.py', 'raypoolkit/contract.py', 'raypoolkit/rehearsal_lock.py']]
PASS  file list: LICENSE and the dist-info files  [['raypoolkit-0.3.0.dist-info/METADATA', 'raypoolkit-0.3.0.dist-info/RECORD', 'raypoolkit-0.3.0.dist-info/WHEEL', 'raypoolkit-0.3.0.dist-info/licenses/LICENSE', 'raypoolkit-0.3.0.dist-info/top_level.txt']]
PASS  file list: 10 entries, nothing under raypoolkit/tests/  [10]
PASS  import raypoolkit
PASS  from raypoolkit import RayWorkPool, DatastorePool
PASS  import_module('raypoolkit.RayWorkPool') from site-packages  [$S/venv-wheel-R2/lib/python3.13/site-packages/raypoolkit/RayWorkPool.py]
PASS  import_module('raypoolkit._timing') from site-packages  [$S/venv-wheel-R2/lib/python3.13/site-packages/raypoolkit/_timing.py]
PASS  import_module('raypoolkit.contract') from site-packages  [$S/venv-wheel-R2/lib/python3.13/site-packages/raypoolkit/contract.py]
PASS  import_module('raypoolkit.rehearsal_lock') from site-packages  [$S/venv-wheel-R2/lib/python3.13/site-packages/raypoolkit/rehearsal_lock.py]
PASS  raypoolkit.__file__ under the venv's site-packages  [$S/venv-wheel-R2/lib/python3.13/site-packages/raypoolkit/__init__.py]
PASS  ray.is_initialized() is False  [ray 2.55.1]
PASS  import raypoolkit.tests raises ModuleNotFoundError  [No module named 'raypoolkit.tests']
PASS  version("raypoolkit") == "0.3.0"  [0.3.0]
PASS  requires("raypoolkit") == ["ray>=2.43"]  [['ray>=2.43']]
PASS  --help exits 0, its first line `usage: python -m raypoolkit.rehearsal_lock`  [usage: python -m raypoolkit.rehearsal_lock [-h]]
PASS  HOME is empty before  [$S/home-rc-R2]
  status stdout: lock: free ($HOME/.raypoolkit/rehearsal-lock does not exist) | Ray processes: no temp dir given
PASS  status exits 0 and prints `lock: free (…)`  [0]
PASS  no process names the probe's temp dir  [[]]
PASS  ray-processes for the probe's temp dir exits 0 and prints nothing  [(0, '', '')]
PASS  HOME is still empty afterwards  [[]]
RESULT: OK (0 fail)
```

The script reads the process table itself before the `ray-processes` item, and finds no process
naming `/tmp/ray-rpk03-none`, which is in a variable inside it (clarification 8). **The check of
(R1)**, the same command with `$S/venv-wheel-R1` and (R1)'s wheel: the same 21 lines, each PASS,
paths under `$S/venv-wheel-R1`; `RESULT: OK (0 fail)`, exit 0. `$S/empty-R1`, `$S/empty-R2`,
`$S/home-rc-R1` and `$S/home-rc-R2` were empty afterwards. No Ray process before or after.

### 3.4 `black` (prompt §3.4)

`./venv/bin/black --check raypoolkit docs` (25.1.0): "20 files would be left unchanged.", before
and after, exit 0. No Python file was changed, and `black` was not run on Markdown or
`pyproject.toml`.

### 3.5 The contract's statements (prompt §3.5)

Each statement of `docs/rehearsal-lock.md` that a test could falsify, numbered by section, with
what checks it. Tests are in `raypoolkit/tests/test_rehearsal_lock.py` unless named otherwise.
"P*n*" is a probe of §3.9, run with `HOME` a scratch directory, `lock_dir` explicit, and the
process table fixed text unless it says otherwise. "02" is
[02's log](02-prove-it-under-real-ray.md).

**§1–§2**

| # | Statement | Checked by |
|---|---|---|
| S1 | nothing waits for, queues, retries or breaks a lock | `test_there_is_no_option_to_break_wait_retry_or_move_the_lock`; every held-lock test returns 3 at once (`TestAcquire.held_case`) |
| S2 | `--help`'s first line starts `usage: python -m raypoolkit.rehearsal_lock` | `test_package_imports.test_the_lock_command_runs_with_no_client`; the release check (§3.3); `probe_cli.sh` |
| S3 | the module imports only the standard library | `test_package_imports.test_the_lock_module_imports_only_the_standard_library` |
| S4 | the command imports `ray` through the package root, 0.3–0.6 s | `probe_cli.sh` (`ray in sys.modules: True` after `import raypoolkit.rehearsal_lock`); the timing probe (deviation 13); README §0.3 |
| S5 | the five functions and their signatures | P1 (signatures printed) |
| S6 | each prints what its command prints and returns its exit code | the same codes asserted through the functions (`TestAcquire`, `TestSetPid`, `TestRelease`) and through `main` (`test_commands_and_exit_statuses`) |
| S7 | a bad argument raises `ValueError`; no function returns 2; `status(ray_address=…)` alone raises | `TestArguments` (every `assertRefusedByFunction`); `test_status_takes_an_address_only_with_a_temp_dir`; P15 |
| S8 | `lock_dir` is a keyword of the first four only | P1 |
| S9 | `ray_processes` returns `(pid, ppid, command)` sorted by pid, each command whole | `test_returns_pid_ppid_and_the_whole_command`; P17 |
| S10 | it raises `ValueError` for a bad argument, `RuntimeError` or `OSError` for an unreadable table | `test_bad_arguments_raise_value_error`; `test_a_failing_ps_raises_runtime_error`; P14 |
| S11 | `default_lock_dir()`, `old_lock_dir()` | `test_both_locations_follow_home_changed_after_import` |
| S12 | a driver cannot see its own in-process instance through the API | P2; `test_this_process_its_ancestors_and_its_children_are_never_listed`; 02 §3.4, the a1 rows (ppids) |

**§3**

| # | Statement | Checked by |
|---|---|---|
| S13 | the lock is `~/.raypoolkit/rehearsal-lock`, computed from `HOME` at each call | `test_both_locations_follow_home_changed_after_import`; `test_commands_without_lock_dir_use_the_patched_home` |
| S14 | `acquire` makes `~/.raypoolkit`, then the lock with one `os.mkdir`, never `exist_ok` | `test_parent_is_created_and_the_lock_by_one_os_mkdir`; the held tests (3 from `FileExistsError`) |
| S15 | no environment variable or option moves it | `test_no_environment_variable_moves_the_lock`; `test_there_is_no_option_to_break_wait_retry_or_move_the_lock` |
| S16 | a non-directory at the path: `status` free, `release` 0, `set-pid` 1, `acquire` 3 | P10 |

**§4**

| # | Statement | Checked by |
|---|---|---|
| S17 | UTF-8, seven lines in order, each ending in a newline | `test_free_lock_is_created_with_the_seven_keys`; P7 (non-ASCII values) |
| S18 | written as `owner.tmp` and renamed, by `acquire` and by `set-pid` | P7; P25 |
| S19 | the four values are the caller's arguments | `test_free_lock_is_created_with_the_seven_keys`; `test_an_in_process_caller_is_recorded_with_its_temp_dir` |
| S20 | `acquired`: ISO 8601, local, with offset, to the second | `test_free_lock_is_created_with_the_seven_keys` (offset); P7 (the pattern) |
| S21 | `host`: `hostname -s`, else `gethostname()` cut at the first dot | P6; `test_free_lock_is_created_with_the_seven_keys` (no dot) |
| S22 | `pid` is `-` until `set-pid`, which rewrites that line alone, every other byte kept | `test_free_lock_is_created_with_the_seven_keys`; `test_live_pid_changes_pid_and_only_pid` |
| S23 | every argument is checked before anything is touched; exit 2 or `ValueError` | `TestArguments` (`assertUntouched` on both paths) |
| S24 | one line, not empty or blank, no line break of any kind | `test_project_and_purpose_must_be_one_non_empty_line` |
| S25 | `ray_temp_dir`: absolute, normal form, not `in-process` | `test_ray_temp_dir_must_be_absolute_normal_and_not_in_process` |
| S26 | `ray_address`: split at the last colon; no range check; `[::1]:6379`, `h:99999` pass; `local`, `auto` do not | `test_ray_address_must_be_in_process_or_host_port`; `test_good_addresses_are_accepted`; P5 |
| S27 | a pid is a positive integer; on the command line, digits only | `test_pid_must_be_a_positive_integer` |
| S28 | a line splits at its first `": "` | `test_value_is_everything_after_the_first_colon_space`; `test_round_trips_its_own_file` |

**§5**

| # | Statement | Checked by |
|---|---|---|
| S29 | the caller's when `project` and `ray_temp_dir` equal the caller's | `test_the_identity_check_judges_each_shape`; `TestSetPid` and `TestRelease`: `test_the_same_project_with_another_temp_dir_is_refused`, `test_another_project_with_the_callers_temp_dir_is_refused` |
| S30 | the strings as given: `/private/tmp/ray-q` and `/tmp/ray-q` one temp dir to the rule, two callers | P4 (`acquire` with the first, `release` with the second 1, with the first 0; the rule lists the same for both) |
| S31 | an `in-process` owner is no caller's | `TestSetPid.test_an_in_process_owner_is_never_the_callers`; `TestRelease.test_an_in_process_owner_is_never_the_callers`; `test_the_identity_check_judges_each_shape` |
| S32 | `set-pid` and `release` touch no other's lock: 1, both sides printed | `test_another_project_is_refused_and_both_sides_printed`; `test_the_same_project_with_another_temp_dir_is_refused` (the caller's line); `TestSetPid.test_another_projects_lock_is_refused` (untouched); `probe_cli.sh` (`set-pid`'s two sides) |
| S33 | `acquire` and `status` do not check identity; the caller's own held lock is 3 | `test_held_by_the_caller_returns_3_and_prints_the_owner`; P24; `test_status_held_with_no_pid` (no caller given) |

**§6**

| # | Statement | Checked by |
|---|---|---|
| S34 | `acquire`, `release`, `status` and `ray-processes` use the rule | `test_processes_of_the_temp_dir_return_4_and_leave_no_lock`; `test_a_process_of_the_temp_dir_is_refused_with_pid_dash`; `test_status_with_processes_of_the_owners_temp_dir_and_address`; `test_commands_and_exit_statuses` |
| S35 | one reading of `ps -axww -o pid= -o ppid= -o command=` | `test_a_failing_ps_raises_runtime_error` (`PS_COMMAND`); `test_reads_the_process_table_through_one_function` (called once) |
| S36 | a line not beginning with a pid and a ppid is skipped | `test_lines_that_do_not_parse_are_skipped`; P29 (a pid and ppid with no command is kept) |
| S37 | both spellings, with and without a leading `/private` component | `test_the_private_spelling_is_matched_both_ways`; `test_a_private_spelling_command_alone_is_listed`; `test_a_tmp_spelling_command_alone_is_listed_for_the_private_spelling`; `test_private_is_stripped_only_as_a_whole_component` |
| S38 | followed by `/`, a space, `=` or the end | `test_the_match_ends_at_a_slash_a_space_an_equals_or_the_end` |
| S39 | matched literally; its end a whole component | `test_the_directory_is_matched_literally`; `test_the_match_is_a_whole_path_component` |
| S40 | no leading boundary: `/var/tmp/ray-a/x` for `/tmp/ray-a` | P3 |
| S41 | the client-server seed: only for `host:port`; both parts, anywhere; the address then a space or the end | `test_the_client_server_of_the_address_is_listed`; `test_the_client_server_must_name_the_whole_address`; `test_the_client_server_address_may_end_the_line`; `test_an_address_alone_is_not_a_client_server`; `test_no_client_server_seed_in_process_or_with_no_address` |
| S42 | every descendant of a seed is added | `test_a_descendant_of_a_seed_is_listed_though_it_names_nothing`; `test_the_tree_at_ray_2_43`; `test_the_tree_at_ray_2_55` |
| S43 | this process, its ancestors and its descendants never listed; they seed the walk | `test_this_process_its_ancestors_and_its_children_are_never_listed`; `test_an_ancestor_naming_the_temp_dir_seeds_its_other_children`; `test_the_default_self_pid_is_this_process` |
| S44 | `ray.init(address="local", _temp_dir=<dir>)`; `ray start --temp-dir <dir>` | §3.6's names probe (`ray.init`'s `address`, and `kwargs.pop("_temp_dir", None)` in its body at 2.43.0 and 2.55.1; `ray start`'s `--head` and `--temp-dir`); 02 (both forms run) |
| S45 | the socket path's limit, about 104 bytes on macOS | not a statement of the module: the brief's §3 and README U2 (contract, deviation 17) |
| S46 | `/` passes the checks, and every command with `//`, `/ `, `/=` or a trailing `/` is a seed | P19; P3 |
| S47 | `release` refuses while the recorded pid is alive | `test_a_live_pid_is_refused` |
| S48 | the reaper: a child of the driver, naming no temp dir, not listed; it exits at `ray.shutdown()` | `test_the_reaper_and_the_driver_are_not_listed`; 02 §3.4 (a1 rows `W--`; a2 "the reaper after ray.shutdown(): gone", at both ends) |
| S49 | every process of an in-process instance descends from the driver; the five named are its children; the command line lists them all bar the reaper | 02 §3.4, the a1 rows (2.43.0 `:437-447`, 2.55.1 `:810-820`: every seed's ppid the driver's, the workers the raylet's; the live listing the witness less the reaper); P2 |
| S50 | any command naming the temp dir is listed; an ancestor's other descendants too | `test_any_command_naming_the_temp_dir_is_listed`; `test_an_ancestor_naming_the_temp_dir_seeds_its_other_children` |

**§7**

| # | Statement | Checked by |
|---|---|---|
| S51 | `acquire`'s order: arguments, the old location, the parent, the lock, the owner file, the processes | `TestArguments` (untouched); `TestOldLocation.refused` (parent absent); `test_parent_is_created_and_the_lock_by_one_os_mkdir`; P26 (the owner file, `pid: -`, there when the table is read) |
| S52 | `acquire` 0 | `test_free_lock_is_created_with_the_seven_keys` |
| S53 | `acquire` 3: the old location, nothing created; held, nothing touched; the owner file printed, or `(no owner file)`; stop and ask | `TestOldLocation` (three refusals); `test_held_by_the_caller_returns_3_and_prints_the_owner`; `test_held_by_another_project_returns_3_and_prints_the_owner`; `test_held_in_process_by_another_project_returns_3`; `test_held_with_no_owner_file_returns_3_and_says_so` |
| S54 | `acquire` 4: processes of `D` or `A`'s client server, or unreadable; released again; a failed removal says so, still 4 | `test_processes_of_the_temp_dir_return_4_and_leave_no_lock`; `test_the_client_server_of_the_address_returns_4`; `test_an_unreadable_table_returns_4_and_leaves_no_lock`; P12 |
| S55 | `acquire` 1: the owner file not written; the lock removed | `test_an_owner_file_that_cannot_be_written_returns_1_and_leaves_no_lock` |
| S56 | `set-pid` 0 | `test_live_pid_changes_pid_and_only_pid`; `test_a_recorded_pid_is_replaced` |
| S57 | `set-pid` 1: `PID` not live, checked first; `os.kill(PID, 0)`; not signallable is live | `test_a_dead_pid_is_refused`; P11; P22; `test_pid_alive` |
| S58 | `set-pid` 1: no lock (not a directory) | `TestSetPid.test_no_lock_is_refused`; P10 |
| S59 | `set-pid` 1: no owner file | `TestSetPid.test_no_owner_file_is_refused` |
| S60 | `set-pid` 1: not the caller's | `TestSetPid.test_another_projects_lock_is_refused`, `…test_the_same_project_with_another_temp_dir_is_refused`, `…test_another_project_with_the_callers_temp_dir_is_refused` |
| S61 | `set-pid` 1: no `pid:` line or more than one; nothing changed in every refusal | `test_an_owner_file_with_no_pid_line_is_refused`; `test_an_owner_file_with_two_pid_lines_is_refused`; `TestSetPid.refused` (`assertUntouched`) |
| S62 | `release` removes `owner`, any `owner.tmp`, then the directory | `test_pid_dash_with_no_processes_releases` (with an `owner.tmp`); P23 |
| S63 | `release` takes the address from the owner file | `test_the_owners_client_server_alone_is_refused` |
| S64 | `release` 0: released, or no lock (not a directory) | `test_pid_dash_with_no_processes_releases`; `test_no_lock_returns_0`; P10 |
| S65 | `release` 1, in order: no owner file; not the caller's; the pid alive (`-` or not a number unchecked); the address unusable; processes; unreadable; nothing removed | `TestRelease.test_no_owner_file_is_refused`; `test_another_project_is_refused_and_both_sides_printed`; `test_a_live_pid_is_refused`; `test_an_owner_address_that_is_not_usable_is_refused`; `test_a_process_of_the_temp_dir_is_refused_with_pid_dash`; `test_the_owners_client_server_alone_is_refused`; `test_an_unreadable_table_is_refused`; `TestRelease.refused` (`assertUntouched`); P27 (the order; a pid `abc` released) |
| S66 | `release` 1 when the directory cannot be removed; the owner file already gone | P13 |
| S67 | `status` 0 always, an unreadable table included; it changes nothing | `test_status_with_an_unreadable_table`; every `status_lines` test (`rc == 0`); P30 (the tree before and after, four states) |
| S68 | `status` with `D`: `D`, and `A`'s client server if `host:port`, never the owner's; with no `D`, the owner's pair | `test_status_with_a_temp_dir_given_uses_it_not_the_owners`; `test_status_with_processes_of_the_owners_temp_dir_and_address`; P28 |
| S69 | `ray-processes` 0 none; 1 some; 1 unreadable | `test_commands_and_exit_statuses`; `test_the_client_server_option_of_ray_processes` |
| S70 | usage errors exit 2; no option to force, wait, retry, break or move | `test_usage_errors_exit_2`; `TestArguments` (`assertRefusedByCommandLine`); `test_there_is_no_option_to_break_wait_retry_or_move_the_lock` |
| S71 | `status --ray-address` only with `--ray-temp-dir` | `test_status_takes_an_address_only_with_a_temp_dir`; `probe_cli.sh` |
| S72 | refusals and errors to stderr; success lines, "no lock to release", `status`, the listing to stdout | `status_lines` (`err == ""`); `test_no_lock_returns_0` (stdout); `test_free_lock_is_created_with_the_seven_keys`, `test_live_pid_changes_pid_and_only_pid`, `test_pid_dash_with_no_processes_releases` (stdout); the refusal tests (stderr); `test_commands_and_exit_statuses` (listing on stdout, unreadable on stderr); `probe_cli.sh`; P14 |
| S73 | a listed process: `<pid> <ppid> <command[:150]>`; indented four in `status` and refusals, not by `ray-processes` | `test_a_listed_command_is_cut_to_150_characters`; `test_status_with_processes_of_the_owners_temp_dir_and_address`; `test_processes_of_the_temp_dir_return_4_and_leave_no_lock`; P31 (the cut in `status` and in a refusal) |
| S74 | an unhandled `OSError`: a traceback and exit 1; `~/.raypoolkit` a plain file: `acquire` creates nothing | `probe_cli.sh` (`FileExistsError` from `d.parent.mkdir`, exit 1, `HOME` holding only the file) |

**§8** (every line of `status`, in order)

| # | Line, and when | Checked by |
|---|---|---|
| S75 | `lock: HELD (<lock>)`: a directory | `test_status_held_with_no_pid` |
| S76 | `lock: free (<lock> does not exist)`: not a directory | `test_status_free`; P10 |
| S77 | the owner file's lines indented four; an empty file one empty line | `test_status_held_with_no_pid`; P9 |
| S78 | `    (no owner file)` | `test_status_held_with_no_owner_file_and_the_old_location_present` |
| S79 | `owner pid: - (no pid recorded yet)`: `-`, missing, not a number | `test_status_held_with_no_pid`; P8 |
| S80 | `owner pid <pid>: alive` / `owner pid <pid>: NOT alive` | `test_status_held_with_a_live_and_a_dead_pid` |
| S81 | `old location: PRESENT (<old>)`: anything there | `test_status_free_with_the_old_location_present`; `test_status_held_with_no_owner_file_and_the_old_location_present`; P16 (a plain file) |
| S82 | `Ray processes: no temp dir given` | `test_status_free`; `test_status_held_with_no_owner_file_and_the_old_location_present` |
| S83 | `Ray processes: the owner's ray_temp_dir or ray_address is not usable` | `test_status_with_owner_values_that_are_not_usable` (three shapes); P9 |
| S84 | `Ray processes of <D>: cannot read the process table (<reason>)` | `test_status_with_an_unreadable_table` |
| S85 | `Ray processes of <D>: none` | `test_status_free`; `test_status_held_with_no_pid`; `test_status_through_main_uses_the_default_location` |
| S86 | `Ray processes of <D>: <n>`, then the lines | `test_status_with_processes_of_the_owners_temp_dir_and_address`; `test_status_with_a_temp_dir_given_uses_it_not_the_owners` |
| S87 | the lines' order | the whole-output assertions of `test_status_held_with_no_pid`, `test_status_held_with_no_owner_file_and_the_old_location_present` and `test_status_free_with_the_old_location_present` |

**§9–§11**

| # | Statement | Checked by |
|---|---|---|
| S88 | while anything is at the old path, `acquire` 3 before creating anything; its owner file or `(no owner file)`; "the old location" | `TestOldLocation`: `test_the_old_location_with_an_owner_file_returns_3_and_prints_it`, `test_the_old_location_without_an_owner_file_returns_3`, `test_the_old_location_refuses_the_default_location_too`; P16 |
| S89 | `status` prints its `old location: PRESENT` line | as S81 |
| S90 | `set-pid`, `release` and `ray-processes` do not look at it | P18 |
| S91 | only the old location's parent present: `acquire` succeeds | `test_with_only_its_parent_present_acquire_succeeds` (the contract's "while anything exists at that path") |
| S92 | the refusal cannot catch a project acquiring at the old location after the move | not a statement of the module: about other implementations (U4) |
| S93 | it starts and stops no Ray, and signals no process | P20 (no `import ray`, no `"ray"` command, `os.kill` only as `os.kill(pid, 0)`, no `signal`, no `killpg`); S3 |
| S94 | it checks no port; the in-process dashboard on 8265 under `ray[default]` | P32 (`socket` used only for `gethostname`); 02 §3.9 and §5 (both ends) |
| S95 | a process naming neither, descended from none that does, is not listed | `test_a_descendant_of_a_seed_is_listed_though_it_names_nothing` (102 not listed); `test_another_projects_processes_are_not_listed` |
| S96 | proven on macOS only; the suite reads no real `ps` | 02 (the header; macOS); `LockTestCase.setUp` replaces `_ps_output` in every test |
| S97 | 103 tests, no Ray, `HOME` patched, no real `HOME` or `ps` | the loader's count (§3.1); `LockTestCase.setUp` (the patched `HOME` and its guard); 01's review (E5) |
| S98 | the proof: both ends; the real lock at the old location; (a), (b), (c); how it is run | 02, header and §3.4–§3.5; `ray_proof.py`'s docstring |

**98 statements.** Two (S45, S92) are not statements of the module and are marked so. Seven rest
on 02's log, alone or with a test or probe (S12, S44, S48, S49, S94, S96, S98). **Eleven rest on a
probe alone**, no test asserting them: S4, S5, S8, S16, S18, S30, S40, S46, S66, S74 and S90. **In
22 more, a probe checks a part that no test asserts** (the part the table credits to the probe):
S12, S17, S20, S21, S26, S36, S51, S54, S57, S58, S64, S65, S67, S68, S73, S76, S77, S79, S81, S88,
S93 and S94. None is untrue of the module; none needed a change under `raypoolkit/`. Each test name
in these tables was checked to exist in the suite (§3.10).

### 3.6 The README's names, and the links (prompt §3.6)

**Every code span in the README's new and changed text** (`git diff -U0 README.md`, the added lines),
with how it was checked. `$S/scripts/readme_names.py` ran in `venv/` (Ray 2.43.0) and `$S/venv313`
(Ray 2.55.1) with `HOME` an empty scratch directory: `RESULT: OK` in both, and `HOME` empty after.

| Name | Kind | Checked by |
|---|---|---|
| `raypoolkit.rehearsal_lock` | module | imported in both venvs |
| `RayWorkPool` | class | `from raypoolkit import RayWorkPool` in both venvs |
| `raypoolkit/rehearsal_lock.py`, `docs/rehearsal-lock.md`, `docs/rehearsal-lock/ray_proof.py`, `prompts/rehearsal-lock/README.md`, `prompts/rehearsal-lock/IMPLEMENTATION_STATE.md`, `LICENSE` | paths | each a tracked file (`git ls-files`, after staging) |
| `./venv/bin/python -m raypoolkit.rehearsal_lock <command> [options]`, `python -m raypoolkit.rehearsal_lock` | command | `probe_cli.sh`; the release check |
| `acquire`, `set-pid`, `release`, `status`, `ray-processes` | commands | `build_parser()`'s subcommands are exactly these five |
| `--project`, `--purpose`, `--ray-temp-dir`, `--ray-address`, `PID` | options | `build_parser()`: `acquire` all four required; `set-pid` `--project` and `--ray-temp-dir` required and the positional `pid`; `release` the two required; `status` `--ray-temp-dir` and `--ray-address` optional; `ray-processes` `--ray-temp-dir` required, `--ray-address` optional |
| `acquire` 0, 3 (held; the old location), 4 (processes, the client server, unreadable; released again), 1 | exit codes | S52–S55's tests |
| `set-pid` 0, 1 | exit codes | S56–S61's tests |
| `release` 0 (released; no lock), 1 | exit codes | S64–S65's tests |
| `status` 0 | exit code | S67's tests |
| `ray-processes` 0, 1 (some; unreadable) | exit codes | S69's tests |
| usage error 2 | exit code | `test_usage_errors_exit_2` |
| `in-process`, `host:port` | values | `rl.IN_PROCESS == "in-process"`; S26's tests |
| `~/.raypoolkit/rehearsal-lock`, `~/ScienceData/.rehearsal-lock` | paths | `default_lock_dir()` and `old_lock_dir()` under the scratch `HOME`; `test_both_locations_follow_home_changed_after_import` |
| `ray.init(address="local", _temp_dir=D)` | Ray call | `ray.init`'s `address`, and `kwargs.pop("_temp_dir", None)` in `ray._private.worker.init`, at 2.43.0 and 2.55.1 |
| `ray start --head --temp-dir D …` | Ray command | `ray.scripts.scripts.start`'s options include `--head` and `--temp-dir` (read from the click command; nothing run) |
| `gcs_server` | process | 02 §3.4 (the cluster's `gcs_server`) |
| `ps` | command | `PS_COMMAND` (S35) |
| `ray[default]` | extra | 02 (its venvs) |
| `D`, `A`, `P` | placeholders | the README's own |
| `v0.1.0`, `v0.2.0`, `v0.3.0` | tags | `git tag` (`v0.3.0` is written as of the tag, as 05 of `extraction` wrote `v0.2.0`'s) |

**The links.** Every relative link target in `README.md`, `PROVENANCE.md`, `CLAUDE.md` and
`docs/rehearsal-lock.md`, resolved from the file's own directory, is a tracked file (`git ls-files`
after staging, which includes this log): §3.10.

**The test names.** Every `test_…` name in §3.5 and here exists in `raypoolkit/tests/`: §3.10.

### 3.7 No client named (prompt §3.7)

```text
$ grep -n -i -E 'secondary|sgk|champbh|cpbh|stochastic|instanton' docs/rehearsal-lock.md
(nothing; exit 1)
$ git diff -U0 README.md | grep '^+' | grep -v '^+++' | grep -n -i -E 'secondary|sgk|champbh|cpbh|stochastic|instanton'
(nothing; exit 1)
```

The README's unchanged lines still name SecondaryGWKit twice (the `v0.2.0` and `v0.1.0`
paragraphs; deviation 14). `PROVENANCE.md` and `CLAUDE.md` name the clients by design.

### 3.8 The real `HOME` and Ray (prompt §3.9)

| | Before (12:01) | After (before the commit) |
|---|---|---|
| `~/ScienceData` | a directory (`drwxr-xr-x … Oct 24 11:31`) | the same |
| `~/ScienceData/.rehearsal-lock` | does not exist | does not exist |
| `~/.raypoolkit` | does not exist | does not exist |
| `pgrep -lf 'gcs_server|raylet|ray::'` | exit 1, nothing | exit 1, nothing |

Every probe, the release check and the names check ran with `HOME` a scratch directory; each was
empty afterwards, or held only what the probe made inside it. No `/tmp/ray*` path was touched.

### 3.9 The probes

Each ran in `venv/` (3.12.15 / 2.43.0), from the empty `$S/empty`, with `-I` and `PYTHONPATH`
unset, `HOME` a fresh scratch directory, `lock_dir` explicit in every lock call, and
`rehearsal_lock._ps_output` replaced by fixed text unless the line says otherwise. Each exits 0,
every line PASS; the outputs are `$S/out/probe_api*.txt` and `$S/out/probe_cli.txt`.

| Probe | Script | What it showed |
|---|---|---|
| P1 | `probe_api.py` | the signatures; `lock_dir` keyword-only in `acquire`, `set_pid`, `release`, `status` alone; `ps_text`, `self_pid` keyword-only |
| P2 | `probe_api.py` | 02's a1 rows at 2.43.0 (`:437-447`, as recorded there, cut at 150), with a parent shell 90000 for the driver 90522 and a lock command 90600 below the driver: `self_pid` the driver → `[]`; `self_pid` 90600 → `[90524, 90528, 90529, 90536, 90537, 90538, 90539, 90540, 90541, 90543]`, every row but the driver, the reaper and the shell; `self_pid` in no row → the same |
| P3 | `probe_api.py` | `/var/tmp/ray-a/x` listed for `/tmp/ray-a`, `/tmp/ray-ab/x` not; `/` lists `x //y` |
| P4 | `probe_api.py` | `acquire` with `/private/tmp/ray-q` 0; `release` with `/tmp/ray-q` 1, printing `'/private/tmp/ray-q', not '/tmp/ray-q'` and the caller's line; with `/private/tmp/ray-q` 0; the rule lists the same two processes for both spellings |
| P5 | `probe_api.py` | `h:99999`, `[::1]:6379`, `a:b:1`, `127.0.0.1:0` accepted |
| P6 | `probe_api.py` | `subprocess.run` raising `OSError` and `gethostname()` `box.example.org` → `box`; unpatched, `hostname -s` (`mps026088`) |
| P7 | `probe_api.py` | `acquire` calls `os.replace('owner.tmp', 'owner')` once, `owner.tmp` existing; only `owner` left; the file UTF-8 (`Ünï`, `café ☕`), seven keys in order, the purpose `purpose: café ☕` read back whole; `acquired` `2026-10-24T12:03:18+01:00` |
| P8 | `probe_api.py` | `owner pid: - (no pid recorded yet)` for `pid: -`, no pid line, `pid: abc`, `pid: 12a` |
| P9 | `probe_api.py` | an empty owner file: `lock: HELD (…)`, an empty line, `owner pid: - (no pid recorded yet)`, `Ray processes: the owner's ray_temp_dir or ray_address is not usable`; 0, nothing on stderr |
| P10 | `probe_api.py` | a plain file at the lock path: `status` 0, `lock: free (<path> does not exist)`; `release` 0, `no lock to release (<path>)` on stdout; `acquire` 3, held, `(no owner file)`; `set-pid` 1, "there is no lock"; the file unchanged |
| P11 | `probe_api.py` | `set-pid` with a dead pid and no lock: 1, `set-pid: <pid> is not a live process; nothing changed` |
| P12 | `probe_api.py` | a process of the temp dir alive and `_remove_lock` raising `OSError('busy')`: `acquire` 4, `could not release the lock again (busy)` on stderr, nothing on stdout |
| P13 | `probe_api.py` | a file `extra` in the lock directory: `release` 1, `release: could not remove <lock> ([Errno 66] Directory not empty: …)`; the directory still there, `owner` gone; `status` then prints `    (no owner file)` |
| P14 | `probe_api.py` | `subprocess.run` raising `FileNotFoundError`: `ray_processes` raises it; `_ps_output` raising `RuntimeError`: `ray_processes_command` 1, nothing on stdout, `cannot read the process table …` on stderr; `status` 0, its line on stdout, nothing on stderr |
| P15 | `probe_api.py` | `ValueError` from `acquire` (relative temp dir), `set_pid` (pid 0), `release` (two-line project), `status(None, address)`, `ray_processes_command` (`local`), `ray_processes` (trailing `/`) |
| P16 | `probe_api.py` | a plain file at the old location: `acquire` 3, "the old location of the rehearsal lock exists"; `status` prints `old location: PRESENT (<old>)`; the lock not made |
| P17 | `probe_api.py` | sorted by pid (7, 30); the 300-character command returned whole |
| P18 | `probe_api2.py` | the old location a directory: `set_pid` 0, `release` 0, `ray_processes_command` 0 on the new lock |
| P19 | `probe_api2.py` | `/`: `a //b`, `a / b`, `a /=b`, `a b/` listed; `a /usr/bin/python` not |
| P20 | `probe_api2.py` | the module's source: `os.kill(` only as `os.kill(pid, 0)` (the call and its docstring); no `killpg`, no `import signal`, no `import ray`, no `"ray"` |
| P22 | `probe_api2.py` | `pid_alive(1)` (`launchd`) true; `os.kill` raising `PermissionError` → true |
| P23 | `probe_api2.py` | `release` with `owner` and `owner.tmp`: 0, the directory gone, its parent left |
| P24 | `probe_api2.py` | two `acquire`s by the same caller: 0, then 3 |
| P25 | `probe_api3.py` | `set_pid` calls `os.replace('owner.tmp', 'owner')` once; only `owner` left |
| P26 | `probe_api3.py` | when `acquire` reads the table, `owner` exists with `pid: -` |
| P27 | `probe_api3.py` | `release`: another project with a live pid → "not the caller's", no pid message; a live pid and address `local` → the pid; address `local` and a process alive → the address; then the processes; a pid `abc` and nothing alive → released, 0 |
| P28 | `probe_api3.py` | a client server of `127.0.0.1:6400`: `status(D, "127.0.0.1:6400")` → `Ray processes of /tmp/ray-z: 1`; `status(D)` and `status(D, "in-process")` → `none` |
| P29 | `probe_api3.py` | `41 40` (no command) between a seed and its grandchild: all three listed |
| P30 | `probe_api4.py` | `status`, with and without a temp dir, free, held, held without an owner file and with the old location present: 0 each time, the tree byte-identical before and after |
| P31 | `probe_api4.py` | a 330-character command: `    9 1 <command[:150]>` in `status`'s output and in `acquire`'s refusal |
| P32 | `probe_api4.py` | the module's only `socket.` use is `socket.gethostname` |

(There is no P21.) **`probe_cli.sh`**, run as `bash $S/scripts/probe_cli.sh $S/home-cli
$S/out/cli`, with the temp dir `/tmp/ray-rpk03-cli` in a variable inside it and no process naming
it beforehand. Its record, `$S` and the scratch `HOME` abbreviated:
- `--help`: 0, stdout, first line `usage: python -m raypoolkit.rehearsal_lock [-h]`;
- no command: 2, usage and `error: the following arguments are required: command` on stderr;
- `status --ray-address 127.0.0.1:6400`: 2, `error: status: --ray-address is given only with
  --ray-temp-dir` on stderr;
- `acquire` 0 (stdout); another project's `acquire` 3 (stderr: held, the owner file indented,
  "stop and ask the user …"); `set-pid` 0 (stdout); another project's `set-pid` 1 (stderr: "the
  lock is not the caller's (project is 'P', not 'Q')", the owner indented, `caller: project: Q,
  ray_temp_dir: /tmp/ray-rpk03-cli`); `release` 1 (stderr: the recorded pid is alive); `status` 0
  (stdout: `lock: HELD`, seven indented lines, `owner pid <pid>: alive`, `Ray processes of
  /tmp/ray-rpk03-cli: none`); `ray-processes` 0, nothing printed; `set-pid` of a `sleep`, killed;
  `release` 0 (stdout: `released the rehearsal lock (…)`); `release` again 0 (stdout: `no lock to
  release (…)`); `status --ray-temp-dir …` 0, free, none;
- `~/.raypoolkit` made a plain file, then `acquire`: **exit 1**, a traceback ending
  `FileExistsError: [Errno 17] File exists: '$HOME/.raypoolkit'` from `d.parent.mkdir`; `find
  $HOME` shows only `$HOME/.raypoolkit`, still the file;
- `python -I -c 'import sys, raypoolkit.rehearsal_lock; print("ray" in sys.modules)'`: `True`;
- `HOME` empty afterwards (the script removed what it made).

### 3.10 The links and the test names, after staging

**The links.** With the eight files staged, `$S/scripts/links.py` takes every `](target)` in
`README.md`, `PROVENANCE.md`, `CLAUDE.md` and `docs/rehearsal-lock.md` that is neither a URL nor
an anchor, resolves it from the file's directory, and looks it up in `git ls-files` (which includes
the index): **30 relative links, 0 not tracked** (exit 0). The four in-page anchors used
(`#changes-in-v020`, `#the-rehearsal-lock`, `#which-handlers-a-pool-needs`) name headings that
exist.

**The test names.** `grep -o 'test_[a-z0-9_]*'` over this log gives 100 distinct names: nine are
test modules (each a file in `raypoolkit/tests/`), one is the fragment `test_` (from "`test_…`"),
and each of the other **90** is a `def <name>(` in `raypoolkit/tests/`. None is missing.

## 4. The deliberate-breakage record (prompt §3.8)

Each item is a diff against 03's `pyproject.toml`, applied by `build.sh` in its own fresh export
(`git apply --check`, `git apply`, `git apply -R --check`, all run there; "applied" printed), never
to the repository's file. No manifest was copied in for either. The wheels were installed, not
editable, into throwaway venvs (`$S/venv-break-a`, `$S/venv-break-b`, 3.13.16 / `ray==2.55.1`), not
the venvs of §3.1 or §3.3, and `$S/scripts/release_check.py` run as in §3.3, with `0.3.0` expected.

### (a) The version not moved

`$S/diffs/a.diff` (SHA-256 `7f3e53daa8fad41154059b958a35a21c3fd279c059a50153fcfab863d22e8d31`):

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "raypoolkit"
-version = "0.3.0"
+version = "0.2.0"
 description = "A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation tasks, and a shared rehearsal lock for Ray runs"
 requires-python = ">=3.12"
 dependencies = [
```

The wheel: `raypoolkit-0.2.0-py3-none-any.whl`, 21,369 bytes, 10 entries, 0 under
`raypoolkit/tests/`, SHA-256 `6f7d132e9c7b223cc41e842d828144d6c7a9bd56f39d3903008711cc4ad84644`;
`METADATA` says `Version: 0.2.0`; "absent from" 0. **The release check fails** (exit 1), on the
metadata check alone:

```text
FAIL  version("raypoolkit") == "0.3.0"  [0.2.0]
RESULT: FAIL (1 fail)
```

### (b) The tests' exclusion removed

`$S/diffs/b.diff` (SHA-256 `6962af5bb1fe323c549119d2830621a1449313836c324171c2486c666eff6c1e`):

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -16,4 +16,3 @@
 
 [tool.setuptools.packages.find]
 include = ["raypoolkit*"]
-exclude = ["raypoolkit.tests", "raypoolkit.tests.*"]
```

The wheel: `raypoolkit-0.3.0-py3-none-any.whl`, **63,134 bytes, 21 entries, 11 under
`raypoolkit/tests/`** (`__init__.py`, `standins.py` and the nine test modules,
`test_rehearsal_lock.py` among them), SHA-256
`9759c013a1353f9ef5b1125ab4d4aba1ce36071e9cb6410a8a1ff923d15214ca`; "absent from" 0 (the tests
ship as a package, so setuptools has nothing to warn about). **The release check fails** (exit 1):

```text
FAIL  file list: the five modules  [[… the five modules, then the eleven under raypoolkit/tests/ …]]
FAIL  file list: 10 entries, nothing under raypoolkit/tests/  [21]
FAIL  import raypoolkit.tests raises ModuleNotFoundError
RESULT: FAIL (3 fail)
```

and from an empty directory with `-I`, `import raypoolkit.tests, raypoolkit.tests.test_rehearsal_lock`
succeeds, from `$S/venv-break-b/lib/python3.13/site-packages/raypoolkit/tests/__init__.py` and
`…/tests/test_rehearsal_lock.py`.

Both match the orchestrator's measurement (clarification 7): (a) 21,369 bytes, (b) 21 entries, 11
under `raypoolkit/tests/`, 63,134 bytes.

## 5. Observations not acted on

1. **A non-directory at the lock's path reads as free** (clarification 5): `status` says `lock: free
   (<path> does not exist)`, `release` says there is no lock and exits 0, `set-pid` exits 1, and
   `acquire` says it is held (3). Only a hand-made file can be there. The contract states each case
   as the module tests it. Not an issue; nothing under `raypoolkit/` changes.
2. **`CLAUDE.md`'s first exception reads "imported from"** ("a provenance note may name the source a
   definition was imported from"). The lock module was written new, and its provenance note names
   the two sources it was *modelled on*; the review of 01 accepted that. The exceptions are the
   user's (2026-10-10) and are not reworded here (clarification 10). For the orchestrator to put to
   the user.
3. **The repository's `raypoolkit.egg-info/SOURCES.txt` lists 10 test files, not
   `test_rehearsal_lock.py`**, even after today's three editable installs (§3.2). Harmless:
   `include-package-data = false` keeps the listed files out, and (R2) passes with it copied in.
4. **A failed `rmdir` in `release` leaves the lock with no owner file** (P13): `_remove_lock`
   removes `owner` and `owner.tmp` before `os.rmdir`, so a lock directory holding any other file
   ends as a held lock with no owner, which `release` then refuses ("no owner file") and the user
   removes by hand. It errs on the held side, and only a hand-made file can cause it. The contract
   says so (§7). Not an issue.
5. **`docs/rehearsal-lock/ray_proof.py` takes the lock at the old location** (`lock_dir=old_lock_dir()`,
   its docstring and `:149`), as README §5 rule 9 asked for the day it ran. After the switch-over
   (G2), a re-run (05's verification) would hold a lock no project looks at. For 04 and 05; the
   contract's §11 says only that it held the lock "at the location the projects used that day".
6. **The import costs more today than README §0.3 measured** (deviation 13): 0.37–0.63 s at Ray
   2.43.0 against 0.28–0.30 s on 2026-10-23, probably the machine's load. The contract gives the
   range.
7. **An empty owner file prints one empty line in `status`** (P9), since `_indented("")` is `""`.
   Cosmetic; the contract's §8 says so.
8. **`pip`'s editable reinstall of `venv/` built its wheel under the system temp directory**
   (`/private/var/folders/…/pip-ephem-wheel-cache-…`), as `pip` always does; nothing of this
   prompt's was written there by hand.
9. **One slip of this agent's: a scratch file in `/tmp`.** Listing the test names of §3.10, one
   command first wrote them to `/tmp/x` and removed it in the same command; the list was then
   written to `$S/out/log-test-names.txt`. No process used the file, and nothing else was written
   to `/tmp`.

## 6. Issues

None opened, narrowed or closed. `docs/OPEN_ISSUES.md` is unchanged: 0 open.

## 7. State handed to the next prompt

- **`v0.3.0` is ready to be tagged once CI passes on this commit.** The tag is made, annotated, on
  this commit, and pushed, by the user or on the user's instruction (README §5 rule 10). If CI
  fails, no tag is made. Nothing is pushed: local `main` is three commits ahead of `origin/main`
  (`cc5f2d6`) with this one.
- `docs/rehearsal-lock.md` is the statement of the lock. 04's checklists are measured against
  `v0.3.0` and can cite it, section by section. Its §6 "what it asks of a caller" and §7's exit
  codes are what each client's call sites must meet. For SGK's in-process instances: a temp dir of
  their own, `set-pid` with the driver's pid, the commands run as the command line and not through
  the API inside the driver, and the dashboard on 8265 (§10).
- `README.md`'s pin says `v0.3.0`, written as of the tag.
- The suite is **226** at both ends. The index is **0**.
- Observation 5 (the proof's lock location) is for 04 and 05.
