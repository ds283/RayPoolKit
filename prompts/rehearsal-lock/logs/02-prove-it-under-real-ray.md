# Log — rehearsal-lock prompt 02: prove it under real Ray

**Subject:** Prove the rehearsal lock under real Ray at both ends · **Commit:** `722466a` ·
**Date:** 2026-10-24 · **Agent:** Claude Opus 5.5

**Result: landed.** `docs/rehearsal-lock/ray_proof.py` is new: a script, not a test, which takes
the real shared lock (`~/ScienceData/.rehearsal-lock`, through the module's own functions with
`lock_dir=old_lock_dir()`, as project `RayPoolKit`) and proves the module under real Ray. **It
exited 0 at both tested ends**, 31 checks of 31 each:
- 3.12.15 / Ray 2.43.0: 58.0 s;
- 3.13.16 / Ray 2.55.1: 68.0 s.

Both ran in `ray[default]` scratch venvs (clarification 1, the user's choice of 2026-10-24). The
lock was free before and after each run, and taken and released by the module twice in each (once
per part). `~/.raypoolkit` never appeared. Nothing but the stop list of part (b) was signalled, each
pid checked against its recorded command. `ray stop` was never run, and no Ray process was left.

The **replay** of each record exits 0. Under 01's mutations, offline only:
- **M10 fails a1 and b2 at both ends**, and b1 and b3 too at 2.55.1;
- **M12 fails b1, b2 and b3 at both ends** (the client server ran at both);
- M8, M9 and M11 cannot be caught by records of this kind (§4).

The real process trees match 01's reconstructions in every role a test of 01 relies on (§3.9).
**No issue is opened**; the index stays at 0. Nothing under `raypoolkit/` changed, and the suite
is **226 → 226**. Nothing was pushed or tagged, and no client was edited or run.

**Gate, re-checked at start.** `HEAD` was `ae1e064` (the orchestration note), on `3f1620e`. The
tree was clean, and this checkout was the only worktree. `Ran 226 tests … OK` (1.970 s).
`./venv/bin/black --check raypoolkit docs`: 19 files unchanged. No Ray process (`pgrep -lf
'gcs_server|raylet|ray::'` exit 1). Ports 6420, 6421, 8270 and 52370 had no listener. No `RAY_*`
variable was set. `~/ScienceData` is a directory; `~/ScienceData/.rehearsal-lock` and
`~/.raypoolkit` did not exist. `/tmp/ray-rpk02*` did not exist. Every scratch file of this log
(venvs, records, outputs, `HOME`s, diffs, the development harness) is under the agent's scratch
directory, `…/scratchpad/agent02/`, written `$S` below. The clients were read only through `git
show`, as the prompt's "Read first" item 8 says: CPBH's `ray_cluster.sh` at `807f175` and SI's
brief at `8b4f615`. None was run.

## 1. What shipped

| File | What |
|---|---|
| `docs/rehearsal-lock/ray_proof.py` (new, 1476 lines after `black`, SHA-256 `c07ca417…c797c9`) | the proof (§1.1); the file both runs used: last written at 11:09:25, before the first run started at 11:09:51 |
| this log, the board, `prompts/INDEX.md` | the records |

`docs/OPEN_ISSUES.md` is unchanged: nothing was opened. Nothing under `raypoolkit/` changed:
`git diff --stat` before staging is empty, and `git status --porcelain --untracked-files=all`
was:

```text
?? docs/rehearsal-lock/ray_proof.py
```

### 1.1 The script

- **Its form.** A shebang and a module docstring in the form of `ray_smoke_run.py`'s: what it
  proves, how it is run, the witness, what it never does, what it prints, and the exit codes. It
  has no licence header. It imports the standard library, `raypoolkit` and
  `raypoolkit.rehearsal_lock`, and `ray` only inside its driver mode (clarification 8: `ray` is
  loaded in every mode through the package root). It names no client: `grep -n -i
  "secondary\|sgk\|champbh\|cpbh\|stochastic\|instanton"` finds nothing.
- **Usage statistics.** The `RAY_*` refusal list is computed first, and
  `RAY_USAGE_STATS_ENABLED=0` is then set in `os.environ`, both before `raypoolkit` is imported,
  so every child inherits the setting. `ray start` gets `--disable-usage-stats`.
- **Modes.** `--record <file>` runs the proof; `--replay <file>` replays a record offline (§2.3
  of the prompt); `--driver` is the script's own driver, run as its child, which reads one JSON
  line of settings from stdin.
- **The lock children.** Every `acquire`, `set_pid`, `release` and `status` is `[sys.executable,
  "-I", "-c", LOCK_CODE, <json>]`. `LOCK_CODE` imports `raypoolkit.rehearsal_lock`, accepts only
  those four names, and calls the one named with `lock_dir=old_lock_dir()` (or with none, for
  (c)'s default-location acquire). It exits with the function's return code. A traceback in a
  child's stderr is a failed check.
- **Every listing.** Every listing is the real command, `[sys.executable, "-I", "-m",
  "raypoolkit.rehearsal_lock", "ray-processes", "--ray-temp-dir", T, …]`. All children run from
  one empty directory made under the record's directory.
- **The witness** (`witness()`) is computed from the script's own reading of `ps -axww -o pid= -o
  ppid= -o command=` and has three steps:
  - It takes the pids absent from the part's pre-start reading.
  - Of those, it keeps each whose command contains this venv's `site-packages/ray/` (as found by
    `importlib.util.find_spec`, as `os.path.realpath` gives it, and either without a leading
    `/private`), or `ray.util.client.server`, or starts with `ray::`; every descendant of one is
    added.
  - It removes the script's own process and its children.

  It uses neither the temp dir nor the address.
- **The offline listing.** It is `ray_processes(T, A, ps_text=<that reading>, self_pid=-1)`
  (deviation 14).
- **A checkpoint** reads the table, the live listing (and, in part (b), the live listing without
  the address) and the offline listings, once a second for at most 20 readings. It passes when two
  consecutive readings agree and the part's expectation holds on them (deviation 15). It records
  the rows of every pid in the witness or any listing, and the first word of each such row's
  parent when that parent is not itself in the rows.
- **One expectation function.** `evaluate(kind, view)` holds the expectation of each checkpoint
  kind (`a1`, `a2`, `a3`, `b1`, `b2`, `b3`, `b4`, and `b1cs` for step (b)4). The run and
  `--replay` both use it, so the replay checks "exactly as the run did".
- **The stop** (`stop()`):
  1. `SIGTERM` to each pid of the stop list;
  2. a grace of at most 15 s, ending early once nothing of the list is alive as recorded;
  3. `SIGKILL` to each one still alive as recorded.

  Before every signal, `guard()` refuses pid ≤ 1, the script's own pid and its ancestors (read
  afresh), and `signal_if_same()` reads `ps -ww -o command= -p <pid>`. It signals only if that
  command equals the one recorded at b3, ignoring trailing white space, and otherwise prints both
  commands and sends nothing. It never uses `os.killpg`.
- **On a failed check, or any exception** (and on `SIGTERM`/`SIGHUP` to the script), the part's
  `try` hands over to `cleanup()`:
  1. its driver, by `exit`, then `SIGTERM` and `SIGKILL` to it alone, each command-checked;
  2. in part (b), the stop, with b3's list if b3 passed, and otherwise the latest live listing
     intersected with the latest witness (a pid in only one is printed and not signalled);
  3. up to 20 readings for the witness and both listings to empty;
  4. `release` through the module.

  If anything is left, or the module refuses, it prints the owner file and exits 4 with the lock
  left held. It never removes the lock itself.
- **Exit codes** are the prompt's: 0, 1, 2, 3 and 4.

## 2. Deviations from the prompt

The orchestrator's clarifications (its note's §0, thirteen items) were all applied. Each is an
IMPLEMENTATION CHOICE at the orchestrator's direction unless it says otherwise.

1. **The proof runs in two `ray[default]` scratch venvs, not in `venv/`** (clarification 1).
   **STRUCTURALLY REQUIRED, the user's choice of 2026-10-24.** `venv/` carries the minimal `ray`,
   with no `grpc`, and Ray refuses a client-server port without it. So `$S/v243` (3.12.15, Ray
   2.43.0) and `$S/v255` (3.13.16, Ray 2.55.1) were made, each with `-e` this repository,
   `ray[default]` and `black==25.1.0` (§3.2). `venv/` ran only the suite and `black`, and nothing
   was installed into it. The prompt's run command becomes `env -u PYTHONPATH
   $S/v2NN/bin/python docs/rehearsal-lock/ray_proof.py --record $S/runs/proof-<ray>.json`.
2. **No temp dir in any command of the session during a run** (clarification 2). The record
   paths are `$S/runs/proof-2.43.0.json` and `…-2.55.1.json`. The temp dirs were looked at only
   between runs, and nothing else ran in the session while a proof ran. The script refuses a
   record path naming a temp dir (deviation 6).
3. **Each run in the background, never under a tool timeout** (clarification 3). Each was a
   `run_in_background` Bash command with stdout and stderr to `$S/runs/proof-<ray>.out`, waited
   for until it exited (59 s and 69 s of wall time). None was signalled.
4. **Cleanup after any exception** (clarification 4): §1.1. `Interrupted` (`SIGTERM`/`SIGHUP`)
   is a `BaseException` caught with the rest. The cleanup ignores a second signal.
5. **The stop's two narrowings** (clarification 5): a pid is signalled only if its command now is
   the one recorded at b3; and, on a failed check before b3, the stop list is the live listing
   intersected with the witness. Never `os.killpg`, never pid ≤ 1, the script or an ancestor
   (`guard()`, read afresh before each signal). The narrowing acted once in a real run, in the
   safe direction: at 2.55.1, seven of the dashboard's children had already exited when their
   turn came, so nothing was sent to them (§3.4).
6. **Two more refusals before anything starts** (clarification 6): any `RAY_*` variable other
   than `RAY_USAGE_STATS_ENABLED`, printed by name; and a record path or record directory that
   names a temp dir (as written or as its realpath). Both exit 2. Tested offline (§3.3).
7. **The client server's address is `127.0.0.1:6420`** (clarification 7). b1's client-server check
   requires `--address=127.0.0.1:6420` followed by a space or the end. It held at both ends, and
   the record keeps each client server's whole command.
8. **`ray` is loaded in every mode** (clarification 8): the prompt's "imports `ray` only in its
   driver mode" is read as "the script's own `import ray` is in its driver mode".
9. **The witness's venv directory** (clarification 9) is matched in four spellings (§1.1). Each
   venv's interpreter was invoked by one absolute path in every run, `$S/v243/bin/python` and
   `$S/v255/bin/python`, with `$S` under `/private/tmp`. The two spellings printed in the
   output's fifth line are the `/private/tmp` and `/tmp` forms, both written `<venv>`.
10. **Developed offline first** (clarification 10), §3.3. One real run at the low end, then one at
    the high end, each the whole script, each exiting 0. No other run started Ray.
11. **The replay never reaches a lock** (clarification 11). Every `--replay` ran with `HOME` an
    empty scratch directory (`$S/replay/home`, `$S/breakage/home`), and each was empty afterwards.
    The breakage follows 01's conventions (§4).
12. **Ray's session directories stay** (clarification 12). `/tmp/ray-rpk02a` and `/tmp/ray-rpk02b`
    now each hold two session directories and `session_latest`. Nothing there was deleted, and
    `/tmp/ray-rpk02c` was never made.
13. **The board and the README** (clarification 13). The board's header and 02's row, and
    `prompts/INDEX.md`, are updated. README §2's status for 02 is left for the review.

This agent's own:

14. **The offline listing uses `self_pid=-1`, not `self_pid=0`.** STRUCTURALLY REQUIRED. On macOS
    `/sbin/launchd` is pid 1 with ppid **0** (`ps -axww -o pid= -o ppid=`, measured 2026-10-24),
    so "pid 0 and its own descendants" is the whole table.
    - Measured offline, on the real table plus two synthetic rows (a raylet naming
      `/tmp/ray-zz9` and a `ray::IDLE` below it): `ray_processes("/tmp/ray-zz9", ps_text=…,
      self_pid=0)` returned `[]`; with `self_pid=-1` it returned both rows; with `self_pid=0`
      and launchd's row removed, it returned both.
    - The prompt's `self_pid=0` would have made every offline listing empty, so a1 could never
      pass.
    - No row has pid or ppid −1, so `-1` gives what the prompt intends: the rule on the very rows,
      with nothing held back. The module was not changed (§5).
15. **A checkpoint passes when two consecutive readings agree *and* the expectation holds on them;
    otherwise it reads on, to 20.** The prompt says the checkpoint repeats until two consecutive
    readings agree, then checks. Its a2 asks for emptiness "within the checkpoint's bound", which
    a check made once on the first settled pair could not give. The verdict still needs both
    conditions on one settled pair, so a pass is never weaker. A failed checkpoint reports the
    problems of its last reading, and each reading's line prints its first problem.
    IMPLEMENTATION CHOICE.
16. **The workers in a1 and b2: the actor must be listed; a task's worker only while it is
    alive.** The driver reports the four tasks' worker pids and the actor's pid (`WORKERS {…}`,
    printed before `READY`).
    - Ray ends surplus idle workers on its own schedule. At 2.43.0's b2, reading 1 showed an
      extra `ray::IDLE` (90644) that was gone by reading 2.
    - So `evaluate` requires the actor in the witness and both listings, and each task worker
      still in the rows (alive) to be there too, and it records how many task workers were
      alive: 2 of 2, 1 of 1, 2 of 2 and 2 of 2.
    - In b2 each listed worker must also be a descendant of the raylet and name neither the temp
      dir nor the address.

    IMPLEMENTATION CHOICE: an addition beyond the prompt's a1, which does not name the workers.
17. **Printing.** Rows are cut as the prompt says (`ray::` to its first word, others at 150, the
    home directory `~`), after three abbreviations: the venv's root `<venv>`, a framework
    interpreter (`…/Python.framework/Versions/<v>/Resources/Python.app/Contents/MacOS/Python`,
    as `ps` shows a venv's `python` on this machine) `<python>`, and the record's directory
    `<scratch>`. Without them a 150-character cut ends inside the interpreter's path. A listing
    child's stdout is printed as its pid set at each reading, with the rows once per checkpoint
    (cut), rather than raw: the module's own cut is 150 characters of an uncut `ray::` title. The
    lock children's stdout and stderr are printed whole, with every line of the form `<pid> <ppid>
    <command>` cut by the same rule. IMPLEMENTATION CHOICE.
18. **Extra checks:** `READY`'s pid equals the driver child's pid (a2-driver-pid); the
    second-acquire check also compares `~/.raypoolkit`'s presence before and after each pair; the
    `status` children are given the part's temp dir (and address), so they also print the
    processes ("none"). IMPLEMENTATION CHOICE.
19. **A failed part ends the run**: part (b) does not start after a failed (a). The prompt says
    only that a failed check stops "that part". A run with a failed part already ends in exit
    1 or 4, so it should not start more Ray. IMPLEMENTATION CHOICE.
20. **Part (b)'s driver is cleaned up as part (a)'s** (`exit`, then `SIGTERM` and `SIGKILL` to it
    alone, command-checked). The prompt names only part (a)'s. IMPLEMENTATION CHOICE.
21. **The grace ends early** once no pid of the stop list is alive with its recorded command. This
    is CPBH's loop, and equivalent to waiting 15 s when nothing is left. At both ends the grace
    ran its full 15 s, since `gcs_server` and the autoscaler's `monitor.py` ignored `SIGTERM`.
    IMPLEMENTATION CHOICE.
22. **"Equal to the command recorded at b3"** ignores trailing white space (`ps -o command=`
    pads nothing, but `ray::` titles carry trailing spaces). IMPLEMENTATION CHOICE.
23. **The record keeps, beside the rows, the first word of each row's parent when the parent is
    outside the rows**: `/sbin/launchd`, or the driver's interpreter. It is what §2.2 step (b)3
    asks to record (the re-parenting), and nothing else of the table is kept. IMPLEMENTATION
    CHOICE.
24. **The client-server check (`b1cs`) is checked at b1 only**, as step (b)4 says, and the replay
    replays it only there. IMPLEMENTATION CHOICE.

No UNINTENDED DRIFT was found.

## 3. Verification performed

### 3.1 The suite and `black` (prompt §3.4, §3.5)

| When | Command | Result |
|---|---|---|
| before | `./venv/bin/python -m unittest discover -s raypoolkit/tests -t .` | `Ran 226 tests in 1.970s` `OK` |
| after both runs and the breakage | the same | `Ran 226 tests in 4.047s` `OK` |
| after | `./venv/bin/black --check raypoolkit docs` | `20 files would be left unchanged.` (19 before, and the script) |

### 3.2 The venvs (clarification 1)

Made with:
```bash
uv venv -p /opt/local/bin/python3.12 $S/v243
uv pip install --python $S/v243/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray[default]==2.43.0" "black==25.1.0"
uv venv -p /opt/local/bin/python3.13 $S/v255
uv pip install --python $S/v255/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray[default]==2.55.1" "black==25.1.0"
```

Both installs exited 0. Read with `$S/v2NN/bin/python -I -c …` from an empty directory:

| Venv | `sys.version` | `ray.__version__` | `raypoolkit.__file__` | packages |
|---|---|---|---|---|
| `$S/v243` | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | `/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py` | 57 |
| `$S/v255` | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | the same | 61 |

The extras resolved to `grpcio==1.84.1`, `aiohttp==3.14.5`, `opencensus==0.11.4` and
`pydantic==2.14.1` at both ends, as the orchestrator measured. These are newer than the clients'
pins.

`uv pip freeze` of `$S/v243`:

```text
aiohappyeyeballs==2.7.1
aiohttp==3.14.5
aiohttp-cors==0.8.1
aiosignal==1.4.0
annotated-types==0.8.0
attrs==26.1.0
black==25.1.0
certifi==2026.10.23
cffi==2.1.1
charset-normalizer==3.5.2
click==8.5.0
colorful==0.5.8
cryptography==50.0.2
distlib==0.4.4
filelock==4.2.4
frozenlist==1.8.0
google-api-core==2.43.0
google-auth==2.62.0
googleapis-common-protos==1.76.0
grpcio==1.84.1
idna==3.20
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
msgpack==1.2.3
multidict==7.2.0
mypy-extensions==1.1.0
opencensus==0.11.4
opencensus-context==0.1.3
opentelemetry-api==1.45.1
packaging==26.3
pathspec==1.1.1
platformdirs==4.13.5
prometheus-client==0.26.0
propcache==0.5.4
proto-plus==1.29.0
protobuf==7.36.2
py-spy==0.4.2
pyasn1==0.6.4
pyasn1-modules==0.4.2
pycparser==3.12
pydantic==2.14.1
pydantic-core==2.50.1
python-discovery==1.6.4
pyyaml==6.0.3
ray==2.43.0
-e file:///Users/ds283/Documents/Code/RayPoolKit
referencing==0.37.0
requests==2.34.2
rpds-py==2026.9.1
six==1.17.0
smart-open==8.0.4
typing-extensions==4.16.0
typing-inspection==0.4.4
urllib3==2.8.0
virtualenv==21.14.13
wrapt==2.5.1
yarl==1.25.1
```

`$S/v255` is the same with `ray==2.55.1` in place of `ray==2.43.0`, plus four packages:

```text
opentelemetry-exporter-prometheus==0.66b1
opentelemetry-proto==1.45.1
opentelemetry-sdk==1.45.1
opentelemetry-semantic-conventions==0.66b1
ray==2.55.1
```

### 3.3 Offline development (clarification 10)

Before the first real run, with `HOME` a scratch directory each time, in this order:

1. **`self_pid=0` measured** (deviation 14).
2. **The witness and the checkpoints on the idle machine's real `ps`** (`$S/dev/harness.py`,
   `$S/dev/fake_tree.py`). The harness imported the script from its path and ran its
   `checkpoint()`, `guard()` and `signal_if_same()` against fake trees:
   - **The fake trees.** Short-lived processes whose argv named the venv's `site-packages/ray/`
     and a development temp dir (`/tmp/ray-rpkdev`, `/tmp/ray-rpkdev2`, never one of the three),
     with `ray::IDLE` titles made by `exec -a`. They were started detached (adopted by
     `launchd`) and each exited by itself after 30 s. Nothing was signalled.
   - **The verdicts.** A cluster-like tree with a fake client server for `127.0.0.1:6499`: b1
     PASS and the client-server check PASS (the client server listed only with the address). An
     in-process-like tree: a1 PASS, with the reaper in the witness alone. A tree with a stray
     process naming the venv's ray directory but not the temp dir: a1 FAIL, as it must. Once
     every fake had exited: a3 and b4 PASS.
   - **The guards.** `guard()` refused the harness's own pid and its parent. `signal_if_same()`
     with a wrong recorded command sent nothing, and with the right command its comparison
     matched.
3. **`--replay` on records built by hand** (`$S/dev/hand_record.py`). 01's `TREE_243` became a1,
   and a gcs_server, a raylet, a `ray::IDLE` and 01's `client_server("127.0.0.1:6400")` became b1:
   PASS on a1, b1 and b1/b1cs, exit 0. The same with the raylet's `/tmp/ray-a` renamed: FAIL a1,
   the offline listing missing the raylet and its three workers, exit 1.
4. **The preflight's refusals**, under a scratch `HOME`:
   - `RAY_ADDRESS=x`: exit 2, naming `RAY_ADDRESS`;
   - a record path under `/tmp/ray-rpk02a-x/` (built in a shell variable): exit 2;
   - the old location made under the scratch `HOME` with an owner file: exit 3, printing it.

   Every scratch `HOME` held only what the test put there.

### 3.4 The proof at both ends (prompt §3.1)

**The readings before and after each run** (`pgrep -lf 'gcs_server|raylet|ray::'`, the lock,
`~/.raypoolkit`, the four ports):

| | 2.43.0 before (11:09:43) | 2.43.0 after (11:11:00) | 2.55.1 before (11:11:16) | 2.55.1 after (11:12:38) |
|---|---|---|---|---|
| `pgrep` | exit 1, nothing | exit 1, nothing | exit 1, nothing | exit 1, nothing |
| `~/ScienceData/.rehearsal-lock` | does not exist | does not exist | does not exist | does not exist |
| `~/.raypoolkit` | does not exist | does not exist | does not exist | does not exist |
| ports 6420, 6421, 8270, 52370 | no listener | no listener | no listener | no listener |
| `RAY_*` in the environment | none | — | none | — |

| Run | Wall clock | The script's own time | Exit | Checks |
|---|---|---|---|---|
| 3.12.15 / 2.43.0 | 11:09:51 → 11:10:50 | 58.0 s (part (a) 16.0 s, part (b) 40.4 s) | **0** | 31 PASS |
| 3.13.16 / 2.55.1 | 11:11:22 → 11:12:31 | 68.0 s (part (a) 18.4 s, part (b) 48.0 s) | **0** | 31 PASS |

The client server ran at both ends, so b1's client-server check was exercised at both. Its
`--address` was `127.0.0.1:6420` at both (clarification 7).

Each run's whole printed output follows, as the script printed it (already cut). The only edit is
that `ray start`'s ANSI colour codes are removed. The record files (`$S/runs/proof-<ray>.json`),
`ray start`'s output and the drivers' stderr stay in scratch.

**3.12.15 / Ray 2.43.0:**

```text
python: 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)]
executable: <venv>/bin/python
ray: 2.43.0 (<venv>/lib/python3.12/site-packages/ray/__init__.py)
raypoolkit.__file__: ~/Documents/Code/RayPoolKit/raypoolkit/__init__.py
this venv's ray directory, as matched: ['<venv>/lib/python3.12/site-packages/ray/', '<venv>/lib/python3.12/site-packages/ray/']
RAY_USAGE_STATS_ENABLED: 0
the lock: ~/ScienceData/.rehearsal-lock (the old location, where the clients look today)
pgrep -lf 'gcs_server|raylet|ray::': no process
$ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a  -> exit 0, []
$ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420  -> exit 0, []
$ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02c  -> exit 0, []
port 6420 (GCS): free
port 6421 (client server): free
port 8270 (dashboard): free
port 52370 (dashboard agent): free
~/.raypoolkit: does not exist

== part (a): an in-process instance with _temp_dir
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0", "/tmp/ray-rpk02a", "in-process"], "old_location": true}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/ScienceData/.rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    stderr: (empty)
PASS a1-acquire: acquire exited 0
  owner file (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T11:09:54+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: -
  the pre-start reading: 931 processes
  $ <venv>/bin/python -I ~/Documents/Code/RayPoolKit/docs/rehearsal-lock/ray_proof.py --driver   (stderr to <scratch>/proof-2.43.0-driver-a.txt)
    stdin: {"address": "local", "temp_dir": "/tmp/ray-rpk02a"}
    driver: WORKERS {"tasks": [90540, 90541], "actor": 90543}
    driver: READY 90522
PASS a2-driver-ready: the driver said 'READY 90522'
PASS a2-driver-pid: READY 90522; the child's pid 90522
checkpoint a1 (a1):
  reading 1: witness [90523, 90524, 90528, 90529, 90536, 90537, 90538, 90539, 90540, 90541, 90543]; live [90524, 90528, 90529, 90536, 90537, 90538, 90539, 90540, 90541, 90543]; offline [90524, 90528, 90529, 90536, 90537, 90538, 90539, 90540, 90541, 90543]
  reading 2: witness [90523, 90524, 90528, 90529, 90536, 90537, 90538, 90539, 90540, 90541, 90543]; live [90524, 90528, 90529, 90536, 90537, 90538, 90539, 90540, 90541, 90543]; offline [90524, 90528, 90529, 90536, 90537, 90538, 90539, 90540, 90541, 90543]; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows (W witness, L live, O offline; l, o without the address):
    W-- 90523 90522 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/ray_process_reaper.py
    WLO 90524 90522 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02a/session_2026-10-24_11-09-54_779396_90522/logs --config_l
    WLO 90528 90522 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02a/session_2026-10-24_11-09-54_779396_90522
    WLO 90529 90522 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8265 --port-retries=50 --temp-dir=/tmp/ray-rpk02a --lo
    WLO 90536 90522 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02a/session_2026-10-24_11-09-54_779396_90522/socke
    WLO 90537 90522 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02a/session_2026-10-24_11-09-54_779396_90522 --l
    WLO 90538 90536 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=63234 --dashboard-agent-port=
    WLO 90539 90536 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=63212 --gc
    WLO 90540 90536 ray::IDLE
    WLO 90541 90536 ray::IDLE
    WLO 90543 90536 ray::A
  parent outside the rows: 90522 <python>
PASS a1: settled after 2 readings; as expected; {'reaper': [90523], 'task workers alive': '2 of 2'}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02a are alive:
          90524 90522 <venv>/lib/python3.12/site-pack
          90528 90522 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          90529 90522 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          90536 90522 <venv>/lib/python3.12/site-pack
          90537 90522 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          90538 90536 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          90539 90536 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          90540 90536 ray::IDLE
          90541 90536 ray::IDLE
          90543 90536 ray::A
PASS a4-release-refused-by-processes: release exited 1; the reason is the processes; the owner file unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02a", 90522], "old_location": true}'
    exit 0
    stdout:
      recorded pid 90522 in ~/ScienceData/.rehearsal-lock/owner
    stderr: (empty)
PASS a5-set-pid-driver: set_pid exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 90522')]
  owner file (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T11:09:54+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: 90522
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (a)", "/tmp/ray-rpk02c", "in-process"], "old_location": true}'
    exit 3
    stdout: (empty)
    stderr:
      the rehearsal lock is held (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
          acquired: 2026-10-24T11:09:54+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02a
          ray_address: in-process
          pid: 90522
      stop and ask the user; nothing here waits on, retries or breaks the lock
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (a)", "/tmp/ray-rpk02c", "in-process"], "old_location": false}'
    exit 3
    stdout: (empty)
    stderr:
      the old location of the rehearsal lock exists (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
          acquired: 2026-10-24T11:09:54+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02a
          ray_address: in-process
          pid: 90522
      it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
PASS a6-second-acquire-refused: at the old location exit 3 (as held); at the default location exit 3 (the old location); the owner file unchanged; ~/.raypoolkit does not exist, as before: True
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 90522 is alive; not releasing
PASS a7-release-refused: release exited 1; the reason is the recorded pid 90522; the owner file unchanged
  driver <- shutdown
    driver: SHUTDOWN
PASS a8-shutdown: the driver said 'SHUTDOWN'
checkpoint a2 (a2):
  reading 1: witness []; live []; offline []
  reading 2: witness []; live []; offline []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows: none
PASS a2: settled after 2 readings; as expected; {'reaper_alive': False}
  the reaper after ray.shutdown(): gone
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 90522 is alive; not releasing
PASS a8-release-refused-by-pid: release exited 1; the reason is the recorded pid 90522; the owner file unchanged
  driver <- exit
    driver: EXIT
PASS a9-driver-exit: the driver said 'EXIT' and exited 0
    driver stderr (<scratch>/proof-2.43.0-driver-a.txt):
      2026-10-24 11:09:57,937	INFO worker.py:1841 -- Started a local Ray instance.
checkpoint a3 (a3):
  reading 1: witness []; live []; offline []
  reading 2: witness []; live []; offline []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows: none
PASS a3: settled after 2 readings; as expected; {}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "old_location": true}'
    exit 0
    stdout:
      released the rehearsal lock (~/ScienceData/.rehearsal-lock)
    stderr: (empty)
PASS a9 release: release exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02a"], "old_location": true}'
    exit 0
    stdout:
      lock: free (~/ScienceData/.rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02a: none
    stderr: (empty)
PASS a9 status: status exited 0; it says free
part (a): 16.0 s

== part (b): a ray start --head cluster
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0", "/tmp/ray-rpk02b", "127.0.0.1:6420"], "old_location": true}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/ScienceData/.rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
    stderr: (empty)
PASS b1-acquire: acquire exited 0
  owner file (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T11:10:10+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: -
  the pre-start reading: 935 processes
  $ <venv>/bin/ray start --head --temp-dir /tmp/ray-rpk02b --port 6420 --ray-client-server-port 6421 --dashboard-port 8270 --dashboard-agent-listen-port 52370 --num-cpus 2 --disable-usage-stats   (output to <scratch>/proof-2.43.0-ray-start.txt)
    exit 0 (2.1 s)
    output:
      2026-10-24 11:10:11,218	INFO usage_lib.py:441 -- Usage stats collection is disabled.
      2026-10-24 11:10:11,219	INFO scripts.py:865 -- Local node IP: 127.0.0.1
      2026-10-24 11:10:12,319	SUCC scripts.py:902 -- --------------------
      2026-10-24 11:10:12,320	SUCC scripts.py:903 -- Ray runtime started.
      2026-10-24 11:10:12,320	SUCC scripts.py:904 -- --------------------
      2026-10-24 11:10:12,320	INFO scripts.py:906 -- Next steps
      2026-10-24 11:10:12,320	INFO scripts.py:921 -- To connect to this Ray cluster:
      2026-10-24 11:10:12,320	INFO scripts.py:923 -- import ray
      2026-10-24 11:10:12,320	INFO scripts.py:924 -- ray.init()
      2026-10-24 11:10:12,320	INFO scripts.py:936 -- To submit a Ray job using the Ray Jobs CLI:
      2026-10-24 11:10:12,320	INFO scripts.py:937 --   RAY_ADDRESS='http://127.0.0.1:8270' ray job submit --working-dir . -- python my_script.py
      2026-10-24 11:10:12,320	INFO scripts.py:946 -- See https://docs.ray.io/en/latest/cluster/running-applications/job-submission/index.html 
      2026-10-24 11:10:12,320	INFO scripts.py:950 -- for more information on submitting Ray jobs to the Ray cluster.
      2026-10-24 11:10:12,320	INFO scripts.py:955 -- To terminate the Ray runtime, run
      2026-10-24 11:10:12,320	INFO scripts.py:956 --   ray stop
      2026-10-24 11:10:12,320	INFO scripts.py:959 -- To view the status of the cluster, use
      2026-10-24 11:10:12,320	INFO scripts.py:960 --   ray status
      2026-10-24 11:10:12,320	INFO scripts.py:964 -- To monitor and debug Ray, view the dashboard at 
      2026-10-24 11:10:12,320	INFO scripts.py:965 --   127.0.0.1:8270
      2026-10-24 11:10:12,320	INFO scripts.py:972 -- If connection to the dashboard fails, check your firewall settings and network configuration.
PASS b2-ray-start: ray start exited 0
checkpoint b1 (b1):
  reading 1: witness [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; live [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; offline [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; without the address live [90597, 90598, 90600, 90601, 90602, 90603, 90604], offline [90597, 90598, 90600, 90601, 90602, 90603, 90604]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; live [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; offline [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; without the address live [90597, 90598, 90600, 90601, 90602, 90603, 90604], offline [90597, 90598, 90600, 90601, 90602, 90603, 90604]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 90597 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596/logs --config_l
    WLOlo 90598 1 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596
    WLO-- 90599 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:621
    WLOlo 90600 1 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 90601 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596/socke
    WLOlo 90602 1 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596 --l
    WLOlo 90603 90601 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=60773 --dashboard-agent-port=
    WLOlo 90604 90601 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=62107 --gc
  parent outside the rows: 1 /sbin/launchd
PASS b1: settled after 2 readings; as expected; {'gcs_server': [90597]}
PASS b4-client-server: as expected; {'client_server': [90599], 'client_server 90599 names the temp dir': False, 'client_server_tree': [90599]}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02b or of the Ray client server for 127.0.0.1:6420 are alive:
          90597 1 <venv>/lib/python3.12/site-pack
          90598 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          90599 1 <python> -m ray.util.client.server --address=127.0.0.1:
          90600 1 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          90601 1 <venv>/lib/python3.12/site-pack
          90602 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          90603 90601 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          90604 90601 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
PASS b5-release-refused-by-processes: release exited 1; the reason is the processes; the owner file unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02b", 90597], "old_location": true}'
    exit 0
    stdout:
      recorded pid 90597 in ~/ScienceData/.rehearsal-lock/owner
    stderr: (empty)
PASS b5-set-pid-gcs_server: set_pid exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 90597')]
  owner file (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T11:10:10+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: 90597
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (b)", "/tmp/ray-rpk02c", "in-process"], "old_location": true}'
    exit 3
    stdout: (empty)
    stderr:
      the rehearsal lock is held (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
          acquired: 2026-10-24T11:10:10+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02b
          ray_address: 127.0.0.1:6420
          pid: 90597
      stop and ask the user; nothing here waits on, retries or breaks the lock
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (b)", "/tmp/ray-rpk02c", "in-process"], "old_location": false}'
    exit 3
    stdout: (empty)
    stderr:
      the old location of the rehearsal lock exists (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
          acquired: 2026-10-24T11:10:10+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02b
          ray_address: 127.0.0.1:6420
          pid: 90597
      it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
PASS b5-second-acquire-refused: at the old location exit 3 (as held); at the default location exit 3 (the old location); the owner file unchanged; ~/.raypoolkit does not exist, as before: True
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 90597 is alive; not releasing
PASS b5-release-refused: release exited 1; the reason is the recorded pid 90597; the owner file unchanged
  $ <venv>/bin/python -I ~/Documents/Code/RayPoolKit/docs/rehearsal-lock/ray_proof.py --driver   (stderr to <scratch>/proof-2.43.0-driver-b.txt)
    stdin: {"address": "127.0.0.1:6420"}
    driver: WORKERS {"tasks": [90641], "actor": 90642}
    driver: READY 90640
PASS b6-driver-ready: the driver said 'READY 90640'
checkpoint b2 (b2):
  reading 1: witness [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643, 90644]; live [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643, 90644]; offline [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643, 90644]; without the address live [90597, 90598, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643, 90644], offline [90597, 90598, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643, 90644]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643]; live [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643]; offline [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643]; without the address live [90597, 90598, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643], offline [90597, 90598, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643]; ports held ['6420', '6421', '8270', '52370']
  reading 3: witness [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643]; live [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643]; offline [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643]; without the address live [90597, 90598, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643], offline [90597, 90598, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 90597 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596/logs --config_l
    WLOlo 90598 1 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596
    WLO-- 90599 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:621
    WLOlo 90600 1 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 90601 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596/socke
    WLOlo 90602 1 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596 --l
    WLOlo 90603 90601 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=60773 --dashboard-agent-port=
    WLOlo 90604 90601 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=62107 --gc
    WLOlo 90641 90601 ray::IDLE
    WLOlo 90642 90601 ray::A
    WLOlo 90643 90601 ray::IDLE
  parent outside the rows: 1 /sbin/launchd
PASS b2: settled after 3 readings; as expected; {'gcs_server': [90597], 'task workers alive': '1 of 1', 'raylet': [90601]}
  driver <- shutdown
    driver: SHUTDOWN
  driver <- exit
    driver: EXIT
PASS b6-driver-exit: the driver said 'SHUTDOWN', 'EXIT' and exited 0
    driver stderr (<scratch>/proof-2.43.0-driver-b.txt):
      2026-10-24 11:10:17,918	INFO worker.py:1654 -- Connecting to existing Ray cluster at address: 127.0.0.1:6420...
      2026-10-24 11:10:17,926	INFO worker.py:1832 -- Connected to Ray cluster. View the dashboard at http://127.0.0.1:8270 
checkpoint b3 (b3):
  reading 1: witness [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; live [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; offline [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; without the address live [90597, 90598, 90600, 90601, 90602, 90603, 90604], offline [90597, 90598, 90600, 90601, 90602, 90603, 90604]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; live [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; offline [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]; without the address live [90597, 90598, 90600, 90601, 90602, 90603, 90604], offline [90597, 90598, 90600, 90601, 90602, 90603, 90604]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 90597 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596/logs --config_l
    WLOlo 90598 1 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596
    WLO-- 90599 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:621
    WLOlo 90600 1 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 90601 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596/socke
    WLOlo 90602 1 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596 --l
    WLOlo 90603 90601 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=60773 --dashboard-agent-port=
    WLOlo 90604 90601 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=62107 --gc
  parent outside the rows: 1 /sbin/launchd
PASS b3: settled after 2 readings; as expected; {'gcs_server': [90597]}
  the stop (never ray stop):
  the stop list (8): [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604]
    SIGTERM -> 90597 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596/logs --config_l
    SIGTERM -> 90598 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596
    SIGTERM -> 90599 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:621
    SIGTERM -> 90600 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    SIGTERM -> 90601 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596/socke
    SIGTERM -> 90602 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596 --l
    SIGTERM -> 90603 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=60773 --dashboard-agent-port=
    SIGTERM -> 90604 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=62107 --gc
  after the grace (15 s at most): still alive [90597, 90598]
    SIGKILL -> 90597 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596/logs --config_l
    SIGKILL -> 90598 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596
checkpoint b4 (b4):
  reading 1: witness []; live []; offline []; without the address live [], offline []; ports held []
  reading 2: witness []; live []; offline []; without the address live [], offline []; ports held []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows: none
PASS b4: settled after 2 readings; as expected; {}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "old_location": true}'
    exit 0
    stdout:
      released the rehearsal lock (~/ScienceData/.rehearsal-lock)
    stderr: (empty)
PASS b9 release: release exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02b", "127.0.0.1:6420"], "old_location": true}'
    exit 0
    stdout:
      lock: free (~/ScienceData/.rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02b: none
    stderr: (empty)
PASS b9 status: status exited 0; it says free
part (b): 40.4 s

== after both parts
PASS after-both: ~/ScienceData/.rehearsal-lock does not exist; ~/.raypoolkit does not exist (before: does not exist)

Summary: 31 checks passed, 0 failed; exit 0; 58.0 s in all
```

**3.13.16 / Ray 2.55.1:**

```text
python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
executable: <venv>/bin/python
ray: 2.55.1 (<venv>/lib/python3.13/site-packages/ray/__init__.py)
raypoolkit.__file__: ~/Documents/Code/RayPoolKit/raypoolkit/__init__.py
this venv's ray directory, as matched: ['<venv>/lib/python3.13/site-packages/ray/', '<venv>/lib/python3.13/site-packages/ray/']
RAY_USAGE_STATS_ENABLED: 0
the lock: ~/ScienceData/.rehearsal-lock (the old location, where the clients look today)
pgrep -lf 'gcs_server|raylet|ray::': no process
$ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a  -> exit 0, []
$ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420  -> exit 0, []
$ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02c  -> exit 0, []
port 6420 (GCS): free
port 6421 (client server): free
port 8270 (dashboard): free
port 52370 (dashboard agent): free
~/.raypoolkit: does not exist

== part (a): an in-process instance with _temp_dir
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1", "/tmp/ray-rpk02a", "in-process"], "old_location": true}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/ScienceData/.rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
    stderr: (empty)
PASS a1-acquire: acquire exited 0
  owner file (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T11:11:25+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: -
  the pre-start reading: 935 processes
  $ <venv>/bin/python -I ~/Documents/Code/RayPoolKit/docs/rehearsal-lock/ray_proof.py --driver   (stderr to <scratch>/proof-2.55.1-driver-a.txt)
    stdin: {"address": "local", "temp_dir": "/tmp/ray-rpk02a"}
    driver: WORKERS {"tasks": [90969, 90970], "actor": 90971}
    driver: READY 90956
PASS a2-driver-ready: the driver said 'READY 90956'
PASS a2-driver-pid: READY 90956; the child's pid 90956
checkpoint a1 (a1):
  reading 1: witness [90957, 90958, 90959, 90961, 90963, 90964, 90966, 90967, 90969, 90970, 90971]; live [90958, 90959, 90961, 90963, 90964, 90966, 90967, 90969, 90970, 90971]; offline [90958, 90959, 90961, 90963, 90964, 90966, 90967, 90969, 90970, 90971]
  reading 2: witness [90957, 90958, 90959, 90961, 90963, 90964, 90966, 90967, 90969, 90970, 90971]; live [90958, 90959, 90961, 90963, 90964, 90966, 90967, 90969, 90970, 90971]; offline [90958, 90959, 90961, 90963, 90964, 90966, 90967, 90969, 90970, 90971]; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows (W witness, L live, O offline; l, o without the address):
    W-- 90957 90956 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/ray_process_reaper.py
    WLO 90958 90956 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02a/session_2026-10-24_11-11-26_385683_90956/logs --config_l
    WLO 90959 90956 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02a/session_2026-10-24_11-11-26_385683_90956
    WLO 90961 90956 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8265 --port-retries=50 --temp-dir=/tmp/ray-rpk02a --lo
    WLO 90963 90956 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02a/session_2026-10-24_11-11-26_385683_90956 --l
    WLO 90964 90956 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02a/session_2026-10-24_11-11-26_385683_90956/socke
    WLO 90966 90964 ray::DashboardAgent
    WLO 90967 90964 ray::RuntimeEnvAgent
    WLO 90969 90964 ray::IDLE
    WLO 90970 90964 ray::IDLE
    WLO 90971 90964 ray::A
  parent outside the rows: 90956 <python>
PASS a1: settled after 2 readings; as expected; {'reaper': [90957], 'task workers alive': '2 of 2'}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02a are alive:
          90958 90956 <venv>/lib/python3.13/site-pack
          90959 90956 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          90961 90956 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          90963 90956 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          90964 90956 <venv>/lib/python3.13/site-pack
          90966 90964 ray::DashboardAgent
          90967 90964 ray::RuntimeEnvAgent
          90969 90964 ray::IDLE
          90970 90964 ray::IDLE
          90971 90964 ray::A
PASS a4-release-refused-by-processes: release exited 1; the reason is the processes; the owner file unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02a", 90956], "old_location": true}'
    exit 0
    stdout:
      recorded pid 90956 in ~/ScienceData/.rehearsal-lock/owner
    stderr: (empty)
PASS a5-set-pid-driver: set_pid exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 90956')]
  owner file (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T11:11:25+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: 90956
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (a)", "/tmp/ray-rpk02c", "in-process"], "old_location": true}'
    exit 3
    stdout: (empty)
    stderr:
      the rehearsal lock is held (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
          acquired: 2026-10-24T11:11:25+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02a
          ray_address: in-process
          pid: 90956
      stop and ask the user; nothing here waits on, retries or breaks the lock
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (a)", "/tmp/ray-rpk02c", "in-process"], "old_location": false}'
    exit 3
    stdout: (empty)
    stderr:
      the old location of the rehearsal lock exists (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
          acquired: 2026-10-24T11:11:25+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02a
          ray_address: in-process
          pid: 90956
      it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
PASS a6-second-acquire-refused: at the old location exit 3 (as held); at the default location exit 3 (the old location); the owner file unchanged; ~/.raypoolkit does not exist, as before: True
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 90956 is alive; not releasing
PASS a7-release-refused: release exited 1; the reason is the recorded pid 90956; the owner file unchanged
  driver <- shutdown
    driver: SHUTDOWN
PASS a8-shutdown: the driver said 'SHUTDOWN'
checkpoint a2 (a2):
  reading 1: witness []; live []; offline []
  reading 2: witness []; live []; offline []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows: none
PASS a2: settled after 2 readings; as expected; {'reaper_alive': False}
  the reaper after ray.shutdown(): gone
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 90956 is alive; not releasing
PASS a8-release-refused-by-pid: release exited 1; the reason is the recorded pid 90956; the owner file unchanged
  driver <- exit
    driver: EXIT
PASS a9-driver-exit: the driver said 'EXIT' and exited 0
    driver stderr (<scratch>/proof-2.55.1-driver-a.txt):
      2026-10-24 11:11:31,151	INFO worker.py:2012 -- Started a local Ray instance.
      <venv>/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
        warnings.warn(
checkpoint a3 (a3):
  reading 1: witness []; live []; offline []
  reading 2: witness []; live []; offline []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows: none
PASS a3: settled after 2 readings; as expected; {}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "old_location": true}'
    exit 0
    stdout:
      released the rehearsal lock (~/ScienceData/.rehearsal-lock)
    stderr: (empty)
PASS a9 release: release exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02a"], "old_location": true}'
    exit 0
    stdout:
      lock: free (~/ScienceData/.rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02a: none
    stderr: (empty)
PASS a9 status: status exited 0; it says free
part (a): 18.4 s

== part (b): a ray start --head cluster
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1", "/tmp/ray-rpk02b", "127.0.0.1:6420"], "old_location": true}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/ScienceData/.rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
    stderr: (empty)
PASS b1-acquire: acquire exited 0
  owner file (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T11:11:44+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: -
  the pre-start reading: 938 processes
  $ <venv>/bin/ray start --head --temp-dir /tmp/ray-rpk02b --port 6420 --ray-client-server-port 6421 --dashboard-port 8270 --dashboard-agent-listen-port 52370 --num-cpus 2 --disable-usage-stats   (output to <scratch>/proof-2.55.1-ray-start.txt)
    exit 0 (5.3 s)
    output:
      2026-10-24 11:11:45,206	INFO usage_lib.py:448 -- Usage stats collection is disabled.
      2026-10-24 11:11:45,208	INFO scripts.py:940 -- Local node IP: 127.0.0.1
      2026-10-24 11:11:49,464	SUCC scripts.py:979 -- --------------------
      2026-10-24 11:11:49,464	SUCC scripts.py:980 -- Ray runtime started.
      2026-10-24 11:11:49,464	SUCC scripts.py:981 -- --------------------
      2026-10-24 11:11:49,464	INFO scripts.py:983 -- Next steps
      2026-10-24 11:11:49,464	INFO scripts.py:1000 -- To connect to this Ray cluster:
      2026-10-24 11:11:49,464	INFO scripts.py:1002 -- import ray
      2026-10-24 11:11:49,465	INFO scripts.py:1003 -- ray.init()
      2026-10-24 11:11:49,465	INFO scripts.py:1017 -- To submit a Ray job using the Ray Jobs CLI:
      2026-10-24 11:11:49,465	INFO scripts.py:1018 --   RAY_API_SERVER_ADDRESS='http://127.0.0.1:8270' ray job submit --working-dir . -- python my_script.py
      2026-10-24 11:11:49,465	INFO scripts.py:1027 -- See https://docs.ray.io/en/latest/cluster/running-applications/job-submission/index.html 
      2026-10-24 11:11:49,465	INFO scripts.py:1031 -- for more information on submitting Ray jobs to the Ray cluster.
      2026-10-24 11:11:49,465	INFO scripts.py:1036 -- To terminate the Ray runtime, run
      2026-10-24 11:11:49,465	INFO scripts.py:1037 --   ray stop
      2026-10-24 11:11:49,465	INFO scripts.py:1040 -- To view the status of the cluster, use
      2026-10-24 11:11:49,465	INFO scripts.py:1041 --   ray status
      2026-10-24 11:11:49,465	INFO scripts.py:1045 -- To monitor and debug Ray, view the dashboard at 
      2026-10-24 11:11:49,465	INFO scripts.py:1046 --   127.0.0.1:8270
      2026-10-24 11:11:49,465	INFO scripts.py:1053 -- If connection to the dashboard fails, check your firewall settings and network configuration.
PASS b2-ray-start: ray start exited 0
checkpoint b1 (b1):
  reading 1: witness [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; live [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; offline [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; without the address live [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047], offline [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; live [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; offline [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; without the address live [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047], offline [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 91030 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028/logs --config_l
    WLOlo 91031 1 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028
    WLO-- 91032 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:0 -
    WLOlo 91033 1 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 91034 91033 <python> -B -c from multiprocessing.resource_tracker import main;main(25)
    WLOlo 91035 91033 ray-dashboard-MetricsHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=28)" --multiprocessing
    WLOlo 91036 91033 ray-dashboard-DataHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=31)" --multiprocessing-fo
    WLOlo 91037 91033 ray-dashboard-EventHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=34)" --multiprocessing-f
    WLOlo 91038 91033 ray-dashboard-JobHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=37)" --multiprocessing-for
    WLOlo 91039 91033 ray-dashboard-NodeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=40)" --multiprocessing-fo
    WLOlo 91040 91033 ray-dashboard-ReportHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=43)" --multiprocessing-
    WLOlo 91041 91033 ray-dashboard-ServeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=46)" --multiprocessing-f
    WLOlo 91042 91033 ray-dashboard-StateHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=49)" --multiprocessing-f
    WLOlo 91043 91033 ray-dashboard-TrainHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=52)" --multiprocessing-f
    WLOlo 91044 1 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028 --l
    WLOlo 91045 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028/socke
    WLOlo 91046 91045 ray::DashboardAgent
    WLOlo 91047 91045 ray::RuntimeEnvAgent
  parent outside the rows: 1 /sbin/launchd
PASS b1: settled after 2 readings; as expected; {'gcs_server': [91030]}
PASS b4-client-server: as expected; {'client_server': [91032], 'client_server 91032 names the temp dir': False, 'client_server_tree': [91032]}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02b or of the Ray client server for 127.0.0.1:6420 are alive:
          91030 1 <venv>/lib/python3.13/site-pack
          91031 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          91032 1 <python> -m ray.util.client.server --address=127.0.0.1:
          91033 1 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          91034 91033 <python> -B -c from multiprocessing.resource_tracker im
          91035 91033 ray-dashboard-MetricsHead-0 <python> -B -c "from multi
          91036 91033 ray-dashboard-DataHead-0 <python> -B -c "from multipro
          91037 91033 ray-dashboard-EventHead-0 <python> -B -c "from multipr
          91038 91033 ray-dashboard-JobHead-0 <python> -B -c "from multiproc
          91039 91033 ray-dashboard-NodeHead-0 <python> -B -c "from multipro
          91040 91033 ray-dashboard-ReportHead-0 <python> -B -c "from multip
          91041 91033 ray-dashboard-ServeHead-0 <python> -B -c "from multipr
          91042 91033 ray-dashboard-StateHead-0 <python> -B -c "from multipr
          91043 91033 ray-dashboard-TrainHead-0 <python> -B -c "from multipr
          91044 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          91045 1 <venv>/lib/python3.13/site-pack
          91046 91045 ray::DashboardAgent
          91047 91045 ray::RuntimeEnvAgent
PASS b5-release-refused-by-processes: release exited 1; the reason is the processes; the owner file unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02b", 91030], "old_location": true}'
    exit 0
    stdout:
      recorded pid 91030 in ~/ScienceData/.rehearsal-lock/owner
    stderr: (empty)
PASS b5-set-pid-gcs_server: set_pid exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 91030')]
  owner file (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T11:11:44+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: 91030
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (b)", "/tmp/ray-rpk02c", "in-process"], "old_location": true}'
    exit 3
    stdout: (empty)
    stderr:
      the rehearsal lock is held (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
          acquired: 2026-10-24T11:11:44+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02b
          ray_address: 127.0.0.1:6420
          pid: 91030
      stop and ask the user; nothing here waits on, retries or breaks the lock
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (b)", "/tmp/ray-rpk02c", "in-process"], "old_location": false}'
    exit 3
    stdout: (empty)
    stderr:
      the old location of the rehearsal lock exists (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
          acquired: 2026-10-24T11:11:44+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02b
          ray_address: 127.0.0.1:6420
          pid: 91030
      it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
PASS b5-second-acquire-refused: at the old location exit 3 (as held); at the default location exit 3 (the old location); the owner file unchanged; ~/.raypoolkit does not exist, as before: True
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "old_location": true}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 91030 is alive; not releasing
PASS b5-release-refused: release exited 1; the reason is the recorded pid 91030; the owner file unchanged
  $ <venv>/bin/python -I ~/Documents/Code/RayPoolKit/docs/rehearsal-lock/ray_proof.py --driver   (stderr to <scratch>/proof-2.55.1-driver-b.txt)
    stdin: {"address": "127.0.0.1:6420"}
    driver: WORKERS {"tasks": [91136, 91137], "actor": 91138}
    driver: READY 91133
PASS b6-driver-ready: the driver said 'READY 91133'
checkpoint b2 (b2):
  reading 1: witness [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138]; live [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138]; offline [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138]; without the address live [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138], offline [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138]; live [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138]; offline [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138]; without the address live [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138], offline [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 91030 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028/logs --config_l
    WLOlo 91031 1 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028
    WLO-- 91032 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:0 -
    WLOlo 91033 1 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 91034 91033 <python> -B -c from multiprocessing.resource_tracker import main;main(25)
    WLOlo 91035 91033 ray-dashboard-MetricsHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=28)" --multiprocessing
    WLOlo 91036 91033 ray-dashboard-DataHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=31)" --multiprocessing-fo
    WLOlo 91037 91033 ray-dashboard-EventHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=34)" --multiprocessing-f
    WLOlo 91038 91033 ray-dashboard-JobHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=37)" --multiprocessing-for
    WLOlo 91039 91033 ray-dashboard-NodeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=40)" --multiprocessing-fo
    WLOlo 91040 91033 ray-dashboard-ReportHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=43)" --multiprocessing-
    WLOlo 91041 91033 ray-dashboard-ServeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=46)" --multiprocessing-f
    WLOlo 91042 91033 ray-dashboard-StateHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=49)" --multiprocessing-f
    WLOlo 91043 91033 ray-dashboard-TrainHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=52)" --multiprocessing-f
    WLOlo 91044 1 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028 --l
    WLOlo 91045 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028/socke
    WLOlo 91046 91045 ray::DashboardAgent
    WLOlo 91047 91045 ray::RuntimeEnvAgent
    WLOlo 91136 91045 ray::IDLE
    WLOlo 91137 91045 ray::IDLE
    WLOlo 91138 91045 ray::A
  parent outside the rows: 1 /sbin/launchd
PASS b2: settled after 2 readings; as expected; {'gcs_server': [91030], 'task workers alive': '2 of 2', 'raylet': [91045]}
  driver <- shutdown
    driver: SHUTDOWN
  driver <- exit
    driver: EXIT
PASS b6-driver-exit: the driver said 'SHUTDOWN', 'EXIT' and exited 0
    driver stderr (<scratch>/proof-2.55.1-driver-b.txt):
      2026-10-24 11:11:57,813	INFO worker.py:1814 -- Connecting to existing Ray cluster at address: 127.0.0.1:6420...
      2026-10-24 11:11:57,874	INFO worker.py:2003 -- Connected to Ray cluster. View the dashboard at http://127.0.0.1:8270 
      <venv>/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
        warnings.warn(
checkpoint b3 (b3):
  reading 1: witness [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; live [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; offline [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; without the address live [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047], offline [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; live [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; offline [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; without the address live [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047], offline [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 91030 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028/logs --config_l
    WLOlo 91031 1 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028
    WLO-- 91032 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:0 -
    WLOlo 91033 1 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 91034 91033 <python> -B -c from multiprocessing.resource_tracker import main;main(25)
    WLOlo 91035 91033 ray-dashboard-MetricsHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=28)" --multiprocessing
    WLOlo 91036 91033 ray-dashboard-DataHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=31)" --multiprocessing-fo
    WLOlo 91037 91033 ray-dashboard-EventHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=34)" --multiprocessing-f
    WLOlo 91038 91033 ray-dashboard-JobHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=37)" --multiprocessing-for
    WLOlo 91039 91033 ray-dashboard-NodeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=40)" --multiprocessing-fo
    WLOlo 91040 91033 ray-dashboard-ReportHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=43)" --multiprocessing-
    WLOlo 91041 91033 ray-dashboard-ServeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=46)" --multiprocessing-f
    WLOlo 91042 91033 ray-dashboard-StateHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=49)" --multiprocessing-f
    WLOlo 91043 91033 ray-dashboard-TrainHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=52)" --multiprocessing-f
    WLOlo 91044 1 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028 --l
    WLOlo 91045 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028/socke
    WLOlo 91046 91045 ray::DashboardAgent
    WLOlo 91047 91045 ray::RuntimeEnvAgent
  parent outside the rows: 1 /sbin/launchd
PASS b3: settled after 2 readings; as expected; {'gcs_server': [91030]}
  the stop (never ray stop):
  the stop list (18): [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047]
    SIGTERM -> 91030 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028/logs --config_l
    SIGTERM -> 91031 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028
    SIGTERM -> 91032 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:0 -
    SIGTERM -> 91033 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    SIGTERM -> 91034 <python> -B -c from multiprocessing.resource_tracker import main;main(25)
    SIGTERM -> 91035 ray-dashboard-MetricsHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=28)" --multiprocessing
    91036: gone; nothing sent
    SIGTERM -> 91037 ray-dashboard-EventHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=34)" --multiprocessing-f
    91038: gone; nothing sent
    91039: gone; nothing sent
    91040: gone; nothing sent
    91041: gone; nothing sent
    91042: gone; nothing sent
    91043: gone; nothing sent
    SIGTERM -> 91044 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028 --l
    SIGTERM -> 91045 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028/socke
    SIGTERM -> 91046 ray::DashboardAgent
    SIGTERM -> 91047 ray::RuntimeEnvAgent
  after the grace (15 s at most): still alive [91030, 91031]
    SIGKILL -> 91030 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028/logs --config_l
    SIGKILL -> 91031 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028
checkpoint b4 (b4):
  reading 1: witness []; live []; offline []; without the address live [], offline []; ports held []
  reading 2: witness []; live []; offline []; without the address live [], offline []; ports held []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows: none
PASS b4: settled after 2 readings; as expected; {}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "old_location": true}'
    exit 0
    stdout:
      released the rehearsal lock (~/ScienceData/.rehearsal-lock)
    stderr: (empty)
PASS b9 release: release exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02b", "127.0.0.1:6420"], "old_location": true}'
    exit 0
    stdout:
      lock: free (~/ScienceData/.rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02b: none
    stderr: (empty)
PASS b9 status: status exited 0; it says free
part (b): 48.0 s

== after both parts
PASS after-both: ~/ScienceData/.rehearsal-lock does not exist; ~/.raypoolkit does not exist (before: does not exist)

Summary: 31 checks passed, 0 failed; exit 0; 68.0 s in all
```

### 3.5 The lock, the signals and what was left (acceptance 3)

- **The lock.** At each end, part (a) and part (b) each acquired with exit 0 and released with
  exit 0, all through the module in fresh interpreters, and `status` then said `lock: free`.
  Between the parts and after the run it did not exist. Every refusal left the owner file
  byte-identical (each `release`-refused and second-acquire check compares the bytes). Each
  `set_pid` changed the `pid:` line alone.
- **`~/.raypoolkit`** never existed: (c)'s default-location acquire was refused, as the old
  location, before it created anything (two acquires at each end).
- **The signals.** Only part (b)'s stop list was signalled: 8 pids at 2.43.0 and 18 at 2.55.1.
  Each was b3's live listing, which equalled its witness and its offline listing. Every signal
  followed a command check. The drivers exited by `exit`, with status 0, and were never
  signalled. At 2.55.1, seven dashboard children (91036, 91038–91043) were gone by their turn
  and got nothing. `gcs_server` and the autoscaler's `monitor.py` outlived `SIGTERM` at both
  ends and were ended by `SIGKILL` after the 15 s grace.
- **`ray stop`** was never run.
- **Left behind.** b4: the witness, all four listings empty and the four ports free, settled after
  2 readings at both ends. No Ray process remained (`pgrep` exit 1 after each run).

### 3.6 The replay (prompt §3.2)

Each record replayed unmutated, with `HOME=$S/replay/home` (empty before and after):

```text
replay of $S/runs/proof-2.43.0.json
  recorded at Python 3.12.15 / Ray 2.43.0; exit 0
  the module as imported: /Users/ds283/Documents/Code/RayPoolKit/raypoolkit/rehearsal_lock.py
  HOME: $S/replay/home
PASS a1 (recorded PASS; the offline listing as recorded): as expected
PASS a2 (recorded PASS; the offline listing as recorded): as expected
PASS a3 (recorded PASS; the offline listing as recorded): as expected
PASS b1 (recorded PASS; the offline listing as recorded): as expected
PASS b1/b1cs (recorded PASS; the offline listing as recorded): as expected
PASS b2 (recorded PASS; the offline listing as recorded): as expected
PASS b3 (recorded PASS; the offline listing as recorded): as expected
PASS b4 (recorded PASS; the offline listing as recorded): as expected
replay: 0 checkpoint check(s) failed; exit 0
```

```text
replay of $S/runs/proof-2.55.1.json
  recorded at Python 3.13.16 / Ray 2.55.1; exit 0
  the module as imported: /Users/ds283/Documents/Code/RayPoolKit/raypoolkit/rehearsal_lock.py
  HOME: $S/replay/home
PASS a1 (recorded PASS; the offline listing as recorded): as expected
PASS a2 (recorded PASS; the offline listing as recorded): as expected
PASS a3 (recorded PASS; the offline listing as recorded): as expected
PASS b1 (recorded PASS; the offline listing as recorded): as expected
PASS b1/b1cs (recorded PASS; the offline listing as recorded): as expected
PASS b2 (recorded PASS; the offline listing as recorded): as expected
PASS b3 (recorded PASS; the offline listing as recorded): as expected
PASS b4 (recorded PASS; the offline listing as recorded): as expected
replay: 0 checkpoint check(s) failed; exit 0
```

### 3.7 The real `HOME`

`~/ScienceData` is the directory it was. `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` did
not exist before the work, between the runs or after them.

### 3.8 Ray's session directories (clarification 12)

They exist, and nothing in them was touched:
- `/tmp/ray-rpk02a/session_2026-10-24_11-09-54_779396_90522`
- `/tmp/ray-rpk02a/session_2026-10-24_11-11-26_385683_90956`
- `/tmp/ray-rpk02b/session_2026-10-24_11-10-11_221426_90596`
- `/tmp/ray-rpk02b/session_2026-10-24_11-11-45_256883_91028`

Each temp dir also holds `session_latest`.

### 3.9 The fixtures against the real lines (prompt §3.6)

01's reconstructed trees (`TREE_243`, `TREE_255` in `raypoolkit/tests/test_rehearsal_lock.py`),
role by role, against the real checkpoint a1 at each end, with the argument names of each seed
that name the temp dir. The rows are from the records, by argument name only:

| Role | 01's reconstruction | Real, 2.43.0 (a1) | Real, 2.55.1 (a1) |
|---|---|---|---|
| the driver | `python -u driver.py`, child of the user's shell, names nothing | the script's `--driver` child, names nothing, in no listing | the same |
| the reaper | `_private/ray_process_reaper.py`, child of the driver, names no temp dir | the same; in the witness, in neither listing; **gone after `ray.shutdown()`** (a2) | the same |
| seeds, children of the driver | 2.43: `gcs_server` (`--log_dir=`), `monitor.py` (`--logs-dir=`), `log_monitor.py`, `raylet`, `default_worker.py` (`--temp-dir=`); 2.55: `gcs_server`, `monitor.py`, `log_monitor.py`, `dashboard.py --minimal` (`--temp-dir=`), `raylet` | `gcs_server` (`--log_dir=`, `--ray_log_filepath=`, `--ray_err_log_filepath=`); `monitor.py` (`--logs-dir=`); `dashboard.py` (`--temp-dir=`, `--log-dir=`, `--session-dir=`); `raylet` (18 argument names, `--temp_dir=` and `--temp-dir=` among them); `log_monitor.py` (`--session-dir=`, `--logs-dir=`) | `gcs_server` (`--log_dir=`, `--session-dir=`, `--stdout_filepath=`, `--stderr_filepath=`); `monitor.py` (`--logs-dir=`, `--stdout-filepath=`, `--stderr-filepath=`); `dashboard.py` (`--temp-dir=` and four more); `log_monitor.py`; `raylet` (22 argument names) |
| seeds below the raylet | 2.43: `dashboard/agent.py`, `runtime_env/agent/main.py` (`--temp-dir=`); 2.55: none | `dashboard/agent.py` (`--temp-dir=` and four more), `runtime_env/agent/main.py` (`--temp-dir=`, `--log-dir=`, `--runtime-env-dir=`) | none |
| reached only as descendants of the raylet | 2.43: `ray::IDLE` ×2, `ray::A`; 2.55: `ray::DashboardAgent`, `ray::RuntimeEnvAgent`, `ray::IDLE` ×2, `ray::A` | `ray::IDLE` ×2, `ray::A` | `ray::DashboardAgent`, `ray::RuntimeEnvAgent`, `ray::IDLE` ×2, `ray::A` |
| the Ray client server | `client_server()`: `python -m ray.util.client.server --address=A --host=0.0.0.0 --port=6401 --mode=proxy`, no temp dir | (b) `<python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=…`, parent `launchd`, **no temp dir**, the address followed by a space | (b) the same, with `--node-id=…` after it |

**Where the real trees differ:**
- **The 2.43 tree's two seed scripts.** 01's `TREE_243` labels two of the driver's seed
  children `log_monitor.py` (6173) and `default_worker.py` (6175). The real 2.43.0 instance has
  no `default_worker.py` child of the driver. Its five seed children are, in pid order,
  `gcs_server`, `monitor.py` (`-u`), `dashboard.py` (no `-u`), `raylet` and `log_monitor.py`
  (`-u`). That is the probe's order and flags (`-u`, no `-u`, raylet, `-u`), so the probe's 6173
  was `dashboard.py` and its 6175 `log_monitor.py`. Both are seeds naming the temp dir and
  children of the driver, which is all any test uses them for.
- **The in-process dashboard is not `--minimal`.** It is a headless dashboard (`--port=8265
  --port-retries=50 … --modules-to-load … --disable-frontend`) at both ends under
  `ray[default]`, despite `include_dashboard=False`. 01's `--minimal` in `TREE_255` is a
  plausible argument, not a captured one. No test depends on it.
- **The cluster, which 01 does not reconstruct.**
  - `ray start` leaves every process it started re-parented to `launchd` (ppid 1), bar those
    below the raylet and, at 2.55.1, the dashboard's children (b1's rows, "parent outside the
    rows: 1 /sbin/launchd").
  - At 2.55.1 the dashboard runs ten `multiprocessing` children: a `resource_tracker` and nine
    titled `ray-dashboard-<Module>Head-0`. They name nothing and are reached only as its
    descendants, so 12 of the cluster's 18 processes depend on the descendant walk at 2.55.1
    (hence M10 failing b1 and b3 there).
  - At 2.43.0 every process of b1 names the temp dir or is the client server.
  - Neither `ray start` nor an attached driver started a reaper.

**No difference changes what a test of 01 proves.** Every role a test relies on holds in the real
trees:
- seeds are processes naming the temp dir after a whole path component;
- `ray::` processes are reached only as descendants;
- the reaper is a child of the driver naming no temp dir;
- the driver names nothing;
- the client server names its address, followed by a space, and no temp dir.

**No issue is opened.** A fixture of the real cluster tree could be added to 01's tests by a
later prompt (§5).

## 4. The deliberate-breakage record (prompt §3.3)

**01's M8–M12, applied unchanged.** Each diff was extracted verbatim from
`logs/01-the-lock-module.md` §4's fenced blocks into `$S/breakage/mNN.diff` (01's own files no
longer exist, so the log's text is the source). The extracted files' SHA-256 are:

| Diff | SHA-256 |
|---|---|
| m08 | `109cd221f6f2561d5272fc199528b312bd59c53792c4fc8fd1cc20a2e006197b` |
| m09 | `74431a820efd089ecbdad7a549e48d33606b31964fe773c03043b699d23fd01f` |
| m10 | `4a87ba4ed6e946f1eef4ed1608651d7c2f800ebbdceaae3926a96846a203b29f` |
| m11 | `474b0b90ddd69b970a3fd1895c308789a838163b2f61e97006868835dc362507` |
| m12 | `0ac8883882e3d74b7bfe554c959e67e8202a983f1015cdcc72d74ad7d704cf65` |

`raypoolkit/rehearsal_lock.py` at `HEAD` is `6733447`'s (`git diff --stat 6733447 HEAD --
raypoolkit/rehearsal_lock.py` is empty). `$S/breakage/run.sh` took these steps for each item:
1. the SHA-256 of `raypoolkit/rehearsal_lock.py` (`92754f2e…bb7f50`) and `git status --porcelain
   --untracked-files=all`, saved;
2. `git apply --check`, `git apply` and `git apply -R --check`;
3. `--replay` of both records, with `HOME=$S/breakage/home`;
4. `git apply -R`;
5. the state taken again and compared.

The state was **equal before and after all five**, and `$S/breakage/home` was empty at the end.
**No mutation was ever run against Ray or the real lock.**

| # | Mutation | 2.43.0 replay | 2.55.1 replay |
|---|---|---|---|
| M8 | the temp-dir match drops its boundary | exit 0: every check passes | exit 0 |
| M9 | the `/private` spelling dropped | exit 0 | exit 0 |
| **M10** | the descendant walk removed | **exit 1: FAIL a1, b2** | **exit 1: FAIL a1, b1, b2, b3** |
| M11 | the ancestor walk removed | exit 0 | exit 0 |
| **M12** | the client-server seed removed | **exit 1: FAIL b1, b2, b3** | **exit 1: FAIL b1, b2, b3** |

The failing lines, as printed (cut at 400 characters):

```text
== M08, 2.43.0: replay: 0 checkpoint check(s) failed; exit 0
== M08, 2.55.1: replay: 0 checkpoint check(s) failed; exit 0
== M09, 2.43.0: replay: 0 checkpoint check(s) failed; exit 0
== M09, 2.55.1: replay: 0 checkpoint check(s) failed; exit 0
== M10, 2.43.0: replay: 2 checkpoint check(s) failed; exit 1
  FAIL a1 (recorded PASS; the offline listing DIFFERS from the record): offline [90524, 90528, 90529, 90536, 90537, 90538, 90539] is not [90524, 90528, 90529, 90536, 90537, 90538, 90539, 90540, 90541, 90543] (extra [], missing [90540, 90541, 90543]); workers [90540, 90541, 90543] are not in the witness and both listings
  FAIL b2 (recorded PASS; the offline listing DIFFERS from the record): offline [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604] is not [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643] (extra [], missing [90641, 90642, 90643]); workers [90641, 90642] are not in the witness and both listings
== M10, 2.55.1: replay: 4 checkpoint check(s) failed; exit 1
  FAIL a1 (recorded PASS; the offline listing DIFFERS from the record): offline [90958, 90959, 90961, 90963, 90964] is not [90958, 90959, 90961, 90963, 90964, 90966, 90967, 90969, 90970, 90971] (extra [], missing [90966, 90967, 90969, 90970, 90971]); workers [90969, 90970, 90971] are not in the witness and both listings
  FAIL b1 (recorded PASS; the offline listing DIFFERS from the record): offline [91030, 91031, 91032, 91033, 91044, 91045] is not [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047] (extra [], missing [91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91046, 91047])
  FAIL b2 (recorded PASS; the offline listing DIFFERS from the record): offline [91030, 91031, 91032, 91033, 91044, 91045] is not [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138] (extra [], missing [91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91046, 91047, 91136, 91137, 91138]
  FAIL b3 (recorded PASS; the offline listing DIFFERS from the record): offline [91030, 91031, 91032, 91033, 91044, 91045] is not [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047] (extra [], missing [91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91046, 91047])
== M11, 2.43.0: replay: 0 checkpoint check(s) failed; exit 0
== M11, 2.55.1: replay: 0 checkpoint check(s) failed; exit 0
== M12, 2.43.0: replay: 3 checkpoint check(s) failed; exit 1
  FAIL b1 (recorded PASS; the offline listing DIFFERS from the record): offline [90597, 90598, 90600, 90601, 90602, 90603, 90604] is not [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604] (extra [], missing [90599])
  FAIL b2 (recorded PASS; the offline listing DIFFERS from the record): offline [90597, 90598, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643] is not [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604, 90641, 90642, 90643] (extra [], missing [90599])
  FAIL b3 (recorded PASS; the offline listing DIFFERS from the record): offline [90597, 90598, 90600, 90601, 90602, 90603, 90604] is not [90597, 90598, 90599, 90600, 90601, 90602, 90603, 90604] (extra [], missing [90599])
== M12, 2.55.1: replay: 3 checkpoint check(s) failed; exit 1
  FAIL b1 (recorded PASS; the offline listing DIFFERS from the record): offline [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047] is not [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047] (extra [], missing [91032])
  FAIL b2 (recorded PASS; the offline listing DIFFERS from the record): offline [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138] is not [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047, 91136, 91137, 91138] (extra [], missing [91032]
  FAIL b3 (recorded PASS; the offline listing DIFFERS from the record): offline [91030, 91031, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047] is not [91030, 91031, 91032, 91033, 91034, 91035, 91036, 91037, 91038, 91039, 91040, 91041, 91042, 91043, 91044, 91045, 91046, 91047] (extra [], missing [91032])
```

**Why M10 and M12 bite.**
- **M10.** At a1 the offline listing loses every `ray::` process (2.43.0: 90540, 90541, 90543;
  2.55.1: also the two agents). At b2 it loses the workers and the actor. At 2.55.1 it also loses
  the dashboard's ten children and the two agents at b1 and b3. At 2.43.0, b1 and b3 pass under
  M10, because every process there names the temp dir or is the client server.
- **M12.** At b1–b3 the offline listing loses the client server (90599; 91032). b1's
  client-server check passes under M12, since both listings then lack it alike, so b1 itself is
  the check that catches it, as the prompt says.

**Why M8, M9 and M11 cannot be caught by these records.**
- **M8 (the boundary).** It only over-lists a process whose command names a longer path beginning
  with the temp dir (`/tmp/ray-rpk02ab`, `/tmp/ray-rpk02a.old`). No such process existed during
  the runs. The record keeps only the rows of processes in the witness or a listing, so it can
  never hold one. Catching M8 would take a decoy process naming such a path, alive at a
  checkpoint and kept in the record. That is a process the prompt does not start and a row it
  does not keep. 01's `test_the_match_is_a_whole_path_component` catches it on fixed tables.
- **M9 (the `/private` spelling).** 01's deviation 21. The temp dirs are given in their `/tmp`
  spelling, and the rule's "contains" has no leading boundary, so a command naming
  `/private/tmp/ray-rpk02a` would contain `/tmp/ray-rpk02a` however `/private` is handled. And
  every real Ray command names the `/tmp` spelling it was given. Only a temp dir given as
  `/private/tmp/…` would show M9, and the proof's are fixed at `/tmp/…`. 01's two reverse-direction
  tests catch it.
- **M11 (the ancestor walk).** The offline listing is evaluated with `self_pid=-1`, which has no
  ancestors, so the walk does nothing to it. The live listing is recorded, not recomputed. And in
  a correct run no ancestor of the live listing (the script, the tool's shell) names a temp dir
  (clarification 2), so the walk's one effect, keeping such an ancestor out of the listing, never
  arises. 01's `test_this_process_its_ancestors_and_its_children_are_never_listed` catches it.

## 5. Observations not acted on

- **`ray_processes(…, self_pid=0)` holds back the whole table on macOS** (deviation 14), since
  `launchd`'s ppid is 0. `self_pid` is a test seam, unchecked, and every caller but a test leaves
  it at `os.getpid()`. 03's contract document may say that `self_pid` is for tests. Not an issue.
- **An in-process instance under `ray[default]` starts a headless dashboard on Ray's default port
  8265** (with `--port-retries=50`), at both ends, although `include_dashboard=False`. This is for
  04's SGK checklist, whose in-process instances run under `ray[default]`. It is not this
  repository's issue.
- **`gcs_server` and the autoscaler's `monitor.py` ignore `SIGTERM`** at both ends. The brief's §3
  names only `gcs_server`. The 15 s grace always runs.
- **The reaper exits at `ray.shutdown()`** at both ends (a2: "gone"), not with the driver. So
  release at a2 was refused by the driver's pid alone, as the prompt expects, and the reaper
  needs no cover after shutdown.
- **01's `TREE_243` misattributes two seed scripts** (§3.9). It changes nothing proved. A later
  prompt that touches 01's fixtures might relabel them, and could add a cluster tree from §3.9's
  rows.
- **The module's own process lines** (in `release`'s refusal) cut at 150 characters before the
  script's abbreviations, so a long venv path fills them. This is cosmetic.
- **The proof needs a `ray[default]` venv** (clarification 1); 05's verification document will
  need one at each end too.
- **`ray start`'s output carries ANSI colour codes**, removed in this log only.

## 6. Issues

None opened, narrowed or closed. `docs/OPEN_ISSUES.md` is unchanged: 0 open.

## 7. State handed to the next prompt

- `docs/rehearsal-lock/ray_proof.py` exists and has passed at both tested ends against
  `6733447`'s module, holding the real shared lock at its old location. Its records are in
  `$S/runs/` and are not committed.
- To re-run it (the review, or 05):
  - **The venvs.** Make `ray[default]` venvs as §3.2, and run with nothing of Ray up, the lock
    free and no `RAY_*` variable.
  - **The command.** Run it in the background, with a record path that names no temp dir.
  - **Leave Ray's directories.** `/tmp/ray-rpk02a` and `/tmp/ray-rpk02b` will exist from these
    runs. The preflight asks only that no process names them.
- The suite is **226** at both ends. The index is **0**.
- 03 may cite this log for "`v0.3.0` is a module that has held a real lock over real Ray at both
  ends". §5's first two observations are for 03's contract document and 04's SGK checklist.
- Nothing is pushed: local `main` is three commits ahead of `origin/main` with this one.
