# Log — rehearsal-lock prompt 05: verification and close-out

**Subject:** Verify the rehearsal-lock campaign and hold the proof's lock at both locations ·
**Commit:** `41cc35e` · **Date:** 2026-10-24 · **Agent:** Claude Opus 5.5

**Result: landed; the campaign is closed, with G2 open.**
- `docs/rehearsal-lock/ray_proof.py` holds the shared lock at **both** its locations (U7): the
  default one, `~/.raypoolkit/rehearsal-lock`, first, then the old one,
  `~/ScienceData/.rehearsal-lock`; it releases the old one first. Every lock call names its
  location and passes it as `lock_dir`. `[04-the-proof-takes-the-old-lock]` is closed.
- **It exited 0 at both tested ends under real Ray, holding the real shared lock at both
  locations**, 46 checks of 46 each:
  - 3.12.15 / Ray 2.43.0: 67.9 s;
  - 3.13.16 / Ray 2.55.1: 72.9 s.

  Before and after each run: no Ray process, neither lock location, the four ports (and 8265) free.
  `~/.raypoolkit` was made by the first run and is left, empty.
- **The replays**: both new records and both of 02's exit 0 unmutated; under M10 and M12 each fails
  at exactly the checkpoints log 02 §4 names for its end.
- **The breakage of the change**: P1 and P2 fail the new owner-files check with exit 1 before any Ray
  starts, the cleanup releasing what was taken; P3 and P4 are refused by the preflight with exit 3,
  nothing made at the other location. At both ends.
- **`docs/rehearsal-lock-verification.md`** is new: the campaign verified from `v0.3.0` and the
  records of 01–05, in its twelve sections.
- The offline wheel from `v0.3.0`: 21,368 bytes, the 10 entries, the five modules `67a75b9`'s.
- Nothing under `raypoolkit/` changed; the suite is **226 → 226** at both ends; `black` 20 files
  unchanged. One issue closed, none opened: the index goes from **1** to **0**. Nothing was pushed
  or tagged; no client was edited, run or imported, and each is as it was.

**Gate, re-checked at start (21:10).**
- `HEAD` was `636a02a` (the orchestration note), on `2861b38` (the prompt). The tree was clean, and
  this checkout was the only worktree. `origin/main` `6284b3b`; tags `v0.1.0`, `v0.2.0`, `v0.3.0`.
- `venv/` (3.12.15 / Ray 2.43.0 / `black` 25.1.0): `Ran 226 tests in 2.165s` `OK`;
  `./venv/bin/black --check raypoolkit docs`: "20 files would be left unchanged."
- No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` exit 1); ports 6420, 6421, 8270, 52370 and
  8265 had no listener; no `RAY_*` variable. `~/ScienceData` is a directory;
  `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` did not exist.
- `/tmp/ray`, `/tmp/ray-cpbh`, `/tmp/ray-cpbh-decoy`, `/tmp/ray-decoy`, `/tmp/ray-rpk02a`,
  `/tmp/ray-rpk02b`, `/tmp/ray-rpkp` and `/tmp/ray-si` existed; `/tmp/ray-rpk02c` did not. None was
  touched.
- The clients, read only through `git`, each clean with no stash (§3.10).

Every scratch file of this log is under the agent's scratch directory, `…/scratchpad/agent05/`,
written `$S` below: the venvs `$S/v243` and `$S/v255`; the real runs' records and outputs in
`$S/runs/`; the scratch `HOME`s in `$S/homes/`; the scripts in `$S/scripts/`; their outputs in
`$S/out/`; the diffs in `$S/breakage/`; the readings in `$S/state/`; 02's records and diffs in
`$S/from02/` (clarification 6).

## 1. What shipped

| File | What |
|---|---|
| `docs/rehearsal-lock/ray_proof.py` | both locations (U7), prompt §2.2 items 1–11 (§1.1); 1,615 lines, SHA-256 `578b7d68…bd02a2a`, the file both real runs used |
| `docs/rehearsal-lock-verification.md` (new) | the verification document, §2.1's twelve sections |
| `docs/adoption/rehearsal-lock/switch-over.md` | one dated line under §1's table and one under §5's first bullet (prompt §2.4); nothing rewritten |
| `docs/OPEN_ISSUES.md` | the row removed; **0 open**; §1.2 says the campaign is closed |
| the board | the header **CLOSED**; §1's row for 05; §2's dated line; §3 empty; the issue in §4 with its **Resolved (05, 2026-10-24)** line. The "Orchestrator notes" line is left to the review (clarification 13) |
| the campaign README | its header; §2's row for 05; a dated line under §7 |
| `prompts/INDEX.md` | the campaign's line: **closed**, 0 open issues |
| this log | the record |

**The contract is not changed.** `docs/rehearsal-lock.md` §11 says the proof was run "holding the
real shared lock at the location the projects used that day", which is true of 02's run, which it
cites; the verification document's §4 is the record of this one (prompt §2.4). Nor are
`raypoolkit/`, `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md`, the three checklists,
`docs/adoption/`'s other files, `docs/extraction/` or `.github/`.

### 1.1 The script

**The diff from `722466a`, function by function** (`$S/scripts/same_functions.py`, comparing each
function's `ast.dump` between the two files):
- **unchanged**: `witness`, `evaluate`, `checkpoint`, `reading`, `live_listing`, `offline_listing`,
  `stop`, `guard`, `signal_if_same`, `alive_as_recorded`, `stop_driver`, `start_driver`,
  `driver_main`, `failure`, `_record_checkpoint`, `_view`, `_show_rows`, the printing helpers,
  `check`, `note`, `save` and `main`: 50 functions in all;
- **changed**: `lock_call` (a required keyword `location`), `owner_bytes` and `show_owner` (both
  files), `preflight` (both locations), `acquire_step`, `release_refused`, `set_pid_step`,
  `second_acquire_step`, `release_free_step` (both locations), `part_a` and `part_b` (the held state
  by location; `HeldByOther` to `refused_by_other`), `cleanup` (`release_held`), `run` (the
  after-both check), `replay` (one line naming the record's form), `Proof.__init__` (the record's
  fields);
- **new**: `lock_dir`, `owner_files_step`, `release_held`, `left_held`, `refused_by_other`;
- the module docstring, the constants `LOCATIONS`, `ACQUIRE_ORDER`, `RELEASE_ORDER` and `LOCK_CODE`.

Item by item (prompt §2.2):
1. **`LOCK_CODE`** reads `location` from its payload, maps `default` to `rl.default_lock_dir()` and
   `old` to `rl.old_lock_dir()`, and always passes it as `lock_dir`; any other value, or none (02's
   payload), is `sys.exit("not a lock location: …")`, exit 1, before any function is called
   (clarification 3). `lock_call` takes `location` as a required keyword, so no call can rely on a
   default. The project, the purpose strings ("rehearsal-lock 02 proof …", clarification 8), the
   temp dirs and the addresses are 02's.
2. **The preflight's** first lines name both locations, and a third, `~ is <HOME>`, is printed
   unabbreviated, so that a scratch `HOME` shows in the output (clarification 5). It refuses with
   exit 3 while either location exists, printing each existing location's owner file, after the
   exit-2 refusals and before anything is made.
3. **Acquire**: `ACQUIRE_ORDER = ("default", "old")`. An `acquire` exiting 3 is noted as a failure
   and raises `HeldByOther`; the part's handler, `refused_by_other`, prints both owner files,
   releases through the module whatever the part holds (the default location, if the old one
   refused), and exits 3, or 4 if that release is refused (clarification 4). Any other failure is a
   failed check, and the cleanup releases what is held. `part["held"]` is per location.
4. **The new check**, `a1-acquire-owner-files` and `b1-acquire-owner-files`, straight after the two
   acquires and before the part's `pre_pids` reading: both owner files exist, each with
   `project: RayPoolKit`, the part's `ray_temp_dir` and `ray_address`, and `pid: -`.
5. **`set_pid`, every refused `release` and every `release`** are made at both locations in
   `RELEASE_ORDER = ("old", "default")`, each a check of its own, each comparing **both** owner files
   before and after; `set_pid`'s also requires the other file unchanged.
6. **`owner_bytes`** returns both files' bytes by location; **`show_owner`** prints both, each
   labelled with its path.
7. **After a part**, `release` at each location, then `status` at each: `lock: free (<that location>
   does not exist)`, no `old location: PRESENT`, and neither location existing. **After both
   parts**: neither location exists, and `~/.raypoolkit` is absent or empty.
8. **Part (c)**: the second acquirer at the old location (refused as held) and at the default
   (refused by the old location), both owner files unchanged; 02's `~/.raypoolkit` comparison is
   gone.
9. **The cleanup** calls `release_held`: each held location, old first; a refusal raises `LeftHeld`
   naming the location, and nothing further is released; `left_held` prints both owner files and
   exits 4.
10. **The docstring** says what the script holds and why (U7), names 05 beside 02, and states exit 3
    and 4 for two locations; the exit codes keep their meanings.
11. **The record** gains `lock_dirs`, `acquire_order`, `release_order` and a per-location
    `preflight.lock_exists`; its checkpoints are 02's in form, so `--replay` reads either. The replay
    prints which form it read.

**The checks, 02's and 05's** (clarification 8; 31 → 46 at each end):

| 02's check | 05's checks |
|---|---|
| `a1-acquire` | `a1-acquire (default)`, `a1-acquire (old)`, and the new `a1-acquire-owner-files` |
| `a2-driver-ready`, `a2-driver-pid`, `a1` | the same |
| `a4-release-refused-by-processes` | `… (old)`, `… (default)` |
| `a5-set-pid-driver` | `… (old)`, `… (default)` |
| `a6-second-acquire-refused` | the same name; both owner files; no `~/.raypoolkit` comparison |
| `a7-release-refused` | `… (old)`, `… (default)` |
| `a8-shutdown`, `a2` | the same |
| `a8-release-refused-by-pid` | `… (old)`, `… (default)` |
| `a9-driver-exit`, `a3` | the same |
| `a9 release`, `a9 status` | `a9 release (old)`, `a9 release (default)`, `a9 status (old)`, `a9 status (default)` |
| `b1-acquire` | `b1-acquire (default)`, `b1-acquire (old)`, and the new `b1-acquire-owner-files` |
| `b2-ray-start`, `b1`, `b4-client-server` | the same |
| `b5-release-refused-by-processes`, `b5-set-pid-gcs_server` | each `… (old)`, `… (default)` |
| `b5-second-acquire-refused` | the same name, as `a6` |
| `b5-release-refused` | `… (old)`, `… (default)` |
| `b6-driver-ready`, `b2`, `b6-driver-exit`, `b3`, `b4` | the same |
| `b9 release`, `b9 status` | each `(old)` and `(default)` |
| `after-both` | the same name: neither location; `~/.raypoolkit` absent or empty |

Part (a) 15 → 23, part (b) 15 → 22, and `after-both`: 46.

## 2. Deviations from the prompt

The orchestrator's clarifications (its note's §0, thirteen items) were all applied. Each is an
IMPLEMENTATION CHOICE at the orchestrator's direction unless it says otherwise.

1. **The commit that adds the prompt has no CI run** (clarification 1). **STRUCTURALLY REQUIRED**:
   the prompt's §0.4 asks for that run, and there is none: `2861b38` and `636a02a` are local
   (`origin/main` `6284b3b`), and nothing is pushed before 05 lands. The document's §2.3 says so
   and cites 40126954690 on `6284b3b` as the last run over the package's tree, and its §2.2 counts
   **25** commits from `6e559bf` to `636a02a`, classing both (a prompt written; a note).
2. **The venvs** (clarification 2): `$S/v243` and `$S/v255`, `ray[default]`, built offline (§3.2).
   `venv/` ran only the suite and `black`, and nothing was installed into it. IMPLEMENTATION CHOICE
   at the orchestrator's direction.
3. **Every lock call passes an explicit `lock_dir`** (clarification 3); an unknown location is an
   exit of the child (§1.1 item 1). IMPLEMENTATION CHOICE at the orchestrator's direction.
4. **One refused acquire, one held lock** (clarification 4): `refused_by_other` (§1.1 item 3),
   exercised offline by S1 and S2 (§3.3). IMPLEMENTATION CHOICE at the orchestrator's direction.
5. **A scratch `HOME` for everything but the two real runs** (clarification 5): every replay and
   every P1–P4 run was made by `$S/scripts/scratch_run.sh`, which refuses a `HOME` outside
   `$S/homes/` or one that exists already, makes it, lists it before and after, and runs the proof
   from the repository root. The proof's third line, `~ is <HOME>`, showed the scratch `HOME` each
   time. IMPLEMENTATION CHOICE at the orchestrator's direction.
6. **02's records replayed** (clarification 6), unmutated and under M10 and M12, with the changed
   script (§3.6). IMPLEMENTATION CHOICE at the orchestrator's direction.
7. **The real runs** (clarification 7): each in the background, output to `$S/runs/`, never under a
   tool timeout and never killed, from a command naming no temp dir, with `git diff -- raypoolkit`
   empty just before; offline development first, then the low end, then the high end. Item 23
   records the one lapse. IMPLEMENTATION CHOICE at the orchestrator's direction.
8. **What stays as it is** (clarification 8): the purpose strings keep "02"; the docstring names 05;
   the checks split by location are mapped in §1.1. IMPLEMENTATION CHOICE at the orchestrator's
   direction.
9. **`~/.raypoolkit` is made by the first real run, and left** (clarification 9): recorded before and
   after each run (§3.4). IMPLEMENTATION CHOICE at the orchestrator's direction.
10. **Ray's session directories stay** (clarification 10): `/tmp/ray-rpk02a` and `…b` now hold two
    more each (§3.7); `/tmp/ray-rpk02c` was not made; nothing under `/tmp/ray*` was deleted.
    IMPLEMENTATION CHOICE at the orchestrator's direction.
11. **The offline wheel** (clarification 11), rebuilt as §0.3 says; it matches (§3.8).
    IMPLEMENTATION CHOICE at the orchestrator's direction.
12. **The CI the document cites** (clarification 12), read with `gh run list` and `gh run view`
    only; the document says the proof never runs in CI and that `black` reaches the changed script
    only once 05's commit is pushed. IMPLEMENTATION CHOICE at the orchestrator's direction.
13. **The board's "Orchestrator notes" line is left to the review** (clarification 13); the header,
    §1's row, §2's dated line, §3 and §4 are updated, and README's header, §2's row and §7's line.
    IMPLEMENTATION CHOICE at the orchestrator's direction.

This agent's own:

14. **The breakage P1 and P2 are one-line diffs of `ACQUIRE_ORDER`**, a constant read only by
    `acquire_step`; every place that looks at "both locations" iterates `LOCATIONS` instead. The
    first draft iterated `ACQUIRE_ORDER` everywhere, under which dropping a location from it would
    also have dropped it from the owner-files check and the preflight; that was seen when the diffs
    were made, before any P run, and the script was changed so that the diff drops the `acquire`
    alone. IMPLEMENTATION CHOICE.
15. **The preflight prints `~ is <HOME>` unabbreviated** (`print`, not the abbreviating `say`), so
    that the output shows which `HOME` the run used; in the real runs it reads `~ is /Users/ds283`.
    IMPLEMENTATION CHOICE.
16. **Each per-location check compares both owner files**, and `set_pid`'s also requires the other
    file unchanged, where the prompt asks for "the owner file unchanged by it". Never weaker.
    `set_pid` is made old first too, in `RELEASE_ORDER`. IMPLEMENTATION CHOICE.
17. **`status` and `after-both` are a little stricter than §2.2 item 7**: each `status` check also
    requires no `old location: PRESENT` line and neither location existing; `after-both` reads "holds
    nothing" as `~/.raypoolkit` absent or empty, and prints its entries. IMPLEMENTATION CHOICE.
18. **The cleanup stops at the first refused release** ("leaving both as they are", item 9): if the
    old location's release is refused, the default one is not attempted. IMPLEMENTATION CHOICE.
19. **The record's new fields and the replay's form line** (item 11): `lock_dirs`,
    `acquire_order`, `release_order`, `preflight.lock_exists` by location; the replay prints "the
    lock held at both locations (05's form)" or "the lock held at the old location alone (02's
    form)". IMPLEMENTATION CHOICE.
20. **An offline harness for clarification 4's path and the unknown location**, S1–S3 (§3.3),
    beyond P1–P4. IMPLEMENTATION CHOICE: neither path can be reached from the command line without a
    race.
21. **P1–P4 at both ends**, where clarification 5 asks for the low end at least. IMPLEMENTATION
    CHOICE.
22. **The verification document counts deviation entries by class, and the items that say they are
    not deviations apart** (its §8), and counts 05's own beside 01–04's. IMPLEMENTATION CHOICE.
23. **Something else ran during the low-end real run.** UNINTENDED DRIFT, in process only.
    Clarification 7 says nothing else runs while a real run does. During the low-end run (21:18:57
    → 21:20:06) two Bash commands ran: `date '+%H:%M:%S'` at 21:19:38, and `date` with `cat` of the
    run's time file (`$S/runs/proof-2.43.0.time`) at 21:19:49. Neither reads the process table,
    names a temp dir, or touches the lock, the module or the script; neither could enter a reading's
    witness or listing (neither names the venv's `ray` directory, a temp dir or an address), and the
    run's checks are unaffected. During the high-end
    run no command ran; three documents were edited with the editor (`switch-over.md`,
    `docs/OPEN_ISSUES.md`, the board), none of which the run reads, and the run's own output and time
    file were read with the file reader.

## 3. Verification performed

### 3.1 The suite and `black` (prompt §4.1, §4.2)

Each run in the foreground, with no Ray up, its output in `$S/state/` and the verdict grepped from it.

| When | Venv | Result |
|---|---|---|
| before | `venv/` | `Ran 226 tests in 2.165s` `OK` |
| before | `$S/v255` (3.13.16 / Ray 2.55.1, editable) | `Ran 226 tests in 2.124s` `OK` |
| after both real runs, the replays and the breakage | `venv/` | `Ran 226 tests in 1.974s` `OK` |
| after | `$S/v255` | `Ran 226 tests in 2.124s` `OK` |
| before and after | `./venv/bin/black --check raypoolkit docs` | "20 files would be left unchanged." |

### 3.2 The venvs (clarification 2)

```bash
uv venv -p /opt/local/bin/python3.12 $S/v243
uv pip install --offline --python $S/v243/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray[default]==2.43.0" "black==25.1.0"
uv venv -p /opt/local/bin/python3.13 $S/v255
uv pip install --offline --python $S/v255/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray[default]==2.55.1" "black==25.1.0"
```

Both installs exited 0. Read with `$S/v2NN/bin/python -I -c …` from an empty directory:

| Venv | `sys.version` | `ray.__version__` | `grpc` | `raypoolkit.__file__` | packages |
|---|---|---|---|---|---|
| `$S/v243` | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | 1.84.1 | `/Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py` | 57 |
| `$S/v255` | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | 1.84.1 | the same | 61 |

`uv pip freeze` of `$S/v243` is **equal, line for line, to log 02 §3.2's** (`diff` of the two
lists: nothing). `$S/v255`'s is the same with `ray==2.55.1` for `ray==2.43.0`, and four more:

```text
opentelemetry-exporter-prometheus==0.66b1
opentelemetry-proto==1.45.1
opentelemetry-sdk==1.45.1
opentelemetry-semantic-conventions==0.66b1
```

The editable installs rewrote the repository's `raypoolkit.egg-info/` (gitignored, not staged).

### 3.3 Offline development (clarification 7)

Before the first real run, against scratch `HOME`s, with the final script (SHA-256
`578b7d68…bd02a2a`; an earlier draft was run first and differed only in deviation 14 and one message
of `refused_by_other`; every run below was repeated on the final file):
1. **02's records replayed** unmutated with the changed script: exit 0 at both (§3.6).
2. **P3 and P4** at both ends: exit 3 from the preflight (§4).
3. **P1 and P2** at both ends: exit 1 at the owner-files check (§4).
4. **S1–S3**, `$S/scripts/harness.py`, run by `$S/scripts/harness_run.sh` with `HOME` a fresh
   scratch directory, at the low end. The harness imports the script from its path and subclasses
   `Proof`, overriding `lock_call` only; it starts no Ray (each scenario ends in part (a)'s
   `acquire_step`):
   - **S1**: after the default location's `acquire` exits 0, the harness makes the old location with
     an owner file of another project. The old `acquire` exits 3; `refused_by_other` prints both
     owner files, releases the default location (exit 0), and the run exits **3**. The scratch
     `HOME` after: `.raypoolkit/` empty, and the other project's old location untouched.
   - **S2**: as S1, and the default location's owner file then names another project. Its release
     is refused (exit 1, "not the caller's"); `CLEANUP INCOMPLETE (LeftHeld: release at the default
     location (~/.raypoolkit/rehearsal-lock) exited 1): the lock is left as it is at both
     locations`; both owner files printed; exit **4**; both locations left as they were.
   - **S3**: `LOCK_CODE` with `"location": "elsewhere"` exits 1, `not a lock location:
     'elsewhere'`; with 02's payload (`old_location`, no `location`) exits 1, `not a lock location:
     None`. The `HOME` stayed empty.

S1's part (a), as printed (`$S` for the scratch directory):

```text
== part (a): an in-process instance with _temp_dir
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0", "/tmp/ray-rpk02a", "in-process"], "location": "default"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/.raypoolkit/rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    stderr: (empty)
HARNESS: made the old location, someone else's
PASS a1-acquire (default): acquire at the default location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0", "/tmp/ray-rpk02a", "in-process"], "location": "old"}'
    exit 3
    stdout: (empty)
    stderr:
      the rehearsal lock is held (~/ScienceData/.rehearsal-lock); its owner file:
          project: Other
          purpose: x
          acquired: -
          host: h
          ray_temp_dir: /tmp/ray-other
          ray_address: in-process
          pid: -
      stop and ask the user; nothing here waits on, retries or breaks the lock
FAIL a1-acquire (old): acquire at the old location exited 3: the lock is someone else's
the shared lock is someone else's; this part holds it at the default location
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:18:35+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: -
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    project: Other
    purpose: x
    acquired: -
    host: h
    ray_temp_dir: /tmp/ray-other
    ray_address: in-process
    pid: -
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 0
    stdout:
      released the rehearsal lock (~/.raypoolkit/rehearsal-lock)
    stderr: (empty)

Summary: 1 checks passed, 1 failed: a1-acquire (old); exit 3; 3.1 s in all
run returned 3
exit 3
HOME after:
  .
  ./.raypoolkit
  ./ScienceData
  ./ScienceData/.rehearsal-lock
  ./ScienceData/.rehearsal-lock/owner
$S/homes/h-S1/ScienceData/.rehearsal-lock/owner:
    project: Other
    purpose: x
    acquired: -
    host: h
    ray_temp_dir: /tmp/ray-other
    ray_address: in-process
    pid: -
```

### 3.4 The proof at both ends (prompt §2.3, §4.3)

**The readings before and after each run** (`$S/state/before-243.txt`, `after-243.txt`,
`before-255.txt`, `after-255.txt`):

| | 2.43.0 before (21:18:51) | 2.43.0 after (21:20:14) | 2.55.1 before (21:20:31) | 2.55.1 after (21:21:58) |
|---|---|---|---|---|
| `git diff -- raypoolkit` | empty | — | empty | empty |
| `pgrep -lf 'gcs_server\|raylet\|ray::'` | exit 1, nothing | exit 1, nothing | exit 1, nothing | exit 1, nothing |
| `~/ScienceData/.rehearsal-lock` | does not exist | does not exist | does not exist | does not exist |
| `~/.raypoolkit` | does not exist | `drwxr-xr-x … 21:20 .`, empty | the same | `drwxr-xr-x … 21:21 .`, empty |
| ports 6420, 6421, 8270, 52370, 8265 | no listener | no listener | no listener | no listener |
| `RAY_*` in the environment | none | — | none | — |

`~/ScienceData` holds its two entries (`ChamPBH-rehearsals`, `StochasticInstantons-rehearsals`)
before and after; its modification time moved to 21:21, since the old lock was made and removed in
it.

| Run | Wall clock | The script's own time | Exit | Checks |
|---|---|---|---|---|
| 3.12.15 / 2.43.0 | 21:18:57 → 21:20:06 | 67.9 s (part (a) 21.9 s, part (b) 44.3 s) | **0** | 46 PASS |
| 3.13.16 / 2.55.1 | 21:20:37 → 21:21:51 | 72.9 s (part (a) 23.0 s, part (b) 48.0 s) | **0** | 46 PASS |

The commands, each a `run_in_background` Bash command from the repository root:

```bash
env -u PYTHONPATH $S/v243/bin/python docs/rehearsal-lock/ray_proof.py --record $S/runs/proof-2.43.0.json > $S/runs/proof-2.43.0.out 2>&1
env -u PYTHONPATH $S/v255/bin/python docs/rehearsal-lock/ray_proof.py --record $S/runs/proof-2.55.1.json > $S/runs/proof-2.55.1.out 2>&1
```

Each run's whole output follows, as the script printed it (already cut). The only edit is that
`ray start`'s and the driver's ANSI colour codes are removed (`$S/runs/proof-<ray>.clean.out`).

**3.12.15 / Ray 2.43.0:**

```text
the lock, default location: ~/.raypoolkit/rehearsal-lock (where every client looks after the switch-over)
the lock, old location: ~/ScienceData/.rehearsal-lock (where the clients look until the switch-over)
~ is /Users/ds283
python: 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)]
executable: <venv>/bin/python
ray: 2.43.0 (<venv>/lib/python3.12/site-packages/ray/__init__.py)
raypoolkit.__file__: ~/Documents/Code/RayPoolKit/raypoolkit/__init__.py
this venv's ray directory, as matched: ['<venv>/lib/python3.12/site-packages/ray/', '<venv>/lib/python3.12/site-packages/ray/']
RAY_USAGE_STATS_ENABLED: 0
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
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0", "/tmp/ray-rpk02a", "in-process"], "location": "default"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/.raypoolkit/rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    stderr: (empty)
PASS a1-acquire (default): acquire at the default location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0", "/tmp/ray-rpk02a", "in-process"], "location": "old"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/ScienceData/.rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    stderr: (empty)
PASS a1-acquire (old): acquire at the old location exited 0
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:19:00+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: -
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:19:00+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: -
PASS a1-acquire-owner-files: both owner files exist, each with {'project': 'RayPoolKit', 'ray_temp_dir': '/tmp/ray-rpk02a', 'ray_address': 'in-process', 'pid': '-'}
  the pre-start reading: 933 processes
  $ <venv>/bin/python -I ~/Documents/Code/RayPoolKit/docs/rehearsal-lock/ray_proof.py --driver   (stderr to <scratch>/proof-2.43.0-driver-a.txt)
    stdin: {"address": "local", "temp_dir": "/tmp/ray-rpk02a"}
    driver: WORKERS {"tasks": [39192], "actor": 39191}
    driver: READY 39174
PASS a2-driver-ready: the driver said 'READY 39174'
PASS a2-driver-pid: READY 39174; the child's pid 39174
checkpoint a1 (a1):
  reading 1: witness [39176, 39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39193, 39194]; live [39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39193, 39194]; offline [39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39193, 39194]
  reading 2: witness [39176, 39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39194]; live [39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39194]; offline [39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39194]
  reading 3: witness [39176, 39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39194]; live [39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39194]; offline [39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39194]; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows (W witness, L live, O offline; l, o without the address):
    W-- 39176 39174 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/ray_process_reaper.py
    WLO 39177 39174 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02a/session_2026-10-24_21-19-01_394932_39174/logs --config_l
    WLO 39178 39174 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02a/session_2026-10-24_21-19-01_394932_39174
    WLO 39180 39174 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8265 --port-retries=50 --temp-dir=/tmp/ray-rpk02a --lo
    WLO 39181 39174 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02a/session_2026-10-24_21-19-01_394932_39174/socke
    WLO 39182 39174 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02a/session_2026-10-24_21-19-01_394932_39174 --l
    WLO 39189 39181 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=63518 --dashboard-agent-port=
    WLO 39190 39181 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=62470 --gc
    WLO 39191 39181 ray::A
    WLO 39192 39181 ray::IDLE
    WLO 39194 39181 ray::IDLE
  parent outside the rows: 39174 <python>
PASS a1: settled after 3 readings; as expected; {'reaper': [39176], 'task workers alive': '1 of 1'}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02a are alive:
          39177 39174 <venv>/lib/python3.12/site-pack
          39178 39174 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39180 39174 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          39181 39174 <venv>/lib/python3.12/site-pack
          39182 39174 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39189 39181 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39190 39181 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39191 39181 ray::A
          39192 39181 ray::IDLE
          39194 39181 ray::IDLE
PASS a4-release-refused-by-processes (old): release at the old location exited 1; the reason is the processes; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02a are alive:
          39177 39174 <venv>/lib/python3.12/site-pack
          39178 39174 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39180 39174 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          39181 39174 <venv>/lib/python3.12/site-pack
          39182 39174 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39189 39181 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39190 39181 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39191 39181 ray::A
          39192 39181 ray::IDLE
          39194 39181 ray::IDLE
PASS a4-release-refused-by-processes (default): release at the default location exited 1; the reason is the processes; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02a", 39174], "location": "old"}'
    exit 0
    stdout:
      recorded pid 39174 in ~/ScienceData/.rehearsal-lock/owner
    stderr: (empty)
PASS a5-set-pid-driver (old): set_pid at the old location exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 39174')]; the other owner file unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02a", 39174], "location": "default"}'
    exit 0
    stdout:
      recorded pid 39174 in ~/.raypoolkit/rehearsal-lock/owner
    stderr: (empty)
PASS a5-set-pid-driver (default): set_pid at the default location exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 39174')]; the other owner file unchanged
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:19:00+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: 39174
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:19:00+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: 39174
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (a)", "/tmp/ray-rpk02c", "in-process"], "location": "old"}'
    exit 3
    stdout: (empty)
    stderr:
      the rehearsal lock is held (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
          acquired: 2026-10-24T21:19:00+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02a
          ray_address: in-process
          pid: 39174
      stop and ask the user; nothing here waits on, retries or breaks the lock
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (a)", "/tmp/ray-rpk02c", "in-process"], "location": "default"}'
    exit 3
    stdout: (empty)
    stderr:
      the old location of the rehearsal lock exists (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
          acquired: 2026-10-24T21:19:00+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02a
          ray_address: in-process
          pid: 39174
      it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
PASS a6-second-acquire-refused: at the old location exit 3 (as held); at the default location exit 3 (the old location); both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39174 is alive; not releasing
PASS a7-release-refused (old): release at the old location exited 1; the reason is the recorded pid 39174; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39174 is alive; not releasing
PASS a7-release-refused (default): release at the default location exited 1; the reason is the recorded pid 39174; both owner files unchanged
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
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39174 is alive; not releasing
PASS a8-release-refused-by-pid (old): release at the old location exited 1; the reason is the recorded pid 39174; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39174 is alive; not releasing
PASS a8-release-refused-by-pid (default): release at the default location exited 1; the reason is the recorded pid 39174; both owner files unchanged
  driver <- exit
    driver: EXIT
PASS a9-driver-exit: the driver said 'EXIT' and exited 0
    driver stderr (<scratch>/proof-2.43.0-driver-a.txt):
      2026-10-24 21:19:05,250	INFO worker.py:1841 -- Started a local Ray instance.
checkpoint a3 (a3):
  reading 1: witness []; live []; offline []
  reading 2: witness []; live []; offline []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows: none
PASS a3: settled after 2 readings; as expected; {}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "old"}'
    exit 0
    stdout:
      released the rehearsal lock (~/ScienceData/.rehearsal-lock)
    stderr: (empty)
PASS a9 release (old): release at the old location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 0
    stdout:
      released the rehearsal lock (~/.raypoolkit/rehearsal-lock)
    stderr: (empty)
PASS a9 release (default): release at the default location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02a"], "location": "old"}'
    exit 0
    stdout:
      lock: free (~/ScienceData/.rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02a: none
    stderr: (empty)
PASS a9 status (old): status at the old location exited 0; it says free; existing: neither location
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02a"], "location": "default"}'
    exit 0
    stdout:
      lock: free (~/.raypoolkit/rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02a: none
    stderr: (empty)
PASS a9 status (default): status at the default location exited 0; it says free; existing: neither location
part (a): 21.9 s

== part (b): a ray start --head cluster
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0", "/tmp/ray-rpk02b", "127.0.0.1:6420"], "location": "default"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/.raypoolkit/rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
    stderr: (empty)
PASS b1-acquire (default): acquire at the default location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0", "/tmp/ray-rpk02b", "127.0.0.1:6420"], "location": "old"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/ScienceData/.rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
    stderr: (empty)
PASS b1-acquire (old): acquire at the old location exited 0
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:19:22+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: -
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:19:22+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: -
PASS b1-acquire-owner-files: both owner files exist, each with {'project': 'RayPoolKit', 'ray_temp_dir': '/tmp/ray-rpk02b', 'ray_address': '127.0.0.1:6420', 'pid': '-'}
  the pre-start reading: 932 processes
  $ <venv>/bin/ray start --head --temp-dir /tmp/ray-rpk02b --port 6420 --ray-client-server-port 6421 --dashboard-port 8270 --dashboard-agent-listen-port 52370 --num-cpus 2 --disable-usage-stats   (output to <scratch>/proof-2.43.0-ray-start.txt)
    exit 0 (2.4 s)
    output:
      2026-10-24 21:19:23,711	INFO usage_lib.py:441 -- Usage stats collection is disabled.
      2026-10-24 21:19:23,712	INFO scripts.py:865 -- Local node IP: 127.0.0.1
      2026-10-24 21:19:25,071	SUCC scripts.py:902 -- --------------------
      2026-10-24 21:19:25,071	SUCC scripts.py:903 -- Ray runtime started.
      2026-10-24 21:19:25,071	SUCC scripts.py:904 -- --------------------
      2026-10-24 21:19:25,071	INFO scripts.py:906 -- Next steps
      2026-10-24 21:19:25,071	INFO scripts.py:921 -- To connect to this Ray cluster:
      2026-10-24 21:19:25,071	INFO scripts.py:923 -- import ray
      2026-10-24 21:19:25,071	INFO scripts.py:924 -- ray.init()
      2026-10-24 21:19:25,071	INFO scripts.py:936 -- To submit a Ray job using the Ray Jobs CLI:
      2026-10-24 21:19:25,071	INFO scripts.py:937 --   RAY_ADDRESS='http://127.0.0.1:8270' ray job submit --working-dir . -- python my_script.py
      2026-10-24 21:19:25,071	INFO scripts.py:946 -- See https://docs.ray.io/en/latest/cluster/running-applications/job-submission/index.html 
      2026-10-24 21:19:25,071	INFO scripts.py:950 -- for more information on submitting Ray jobs to the Ray cluster.
      2026-10-24 21:19:25,071	INFO scripts.py:955 -- To terminate the Ray runtime, run
      2026-10-24 21:19:25,071	INFO scripts.py:956 --   ray stop
      2026-10-24 21:19:25,072	INFO scripts.py:959 -- To view the status of the cluster, use
      2026-10-24 21:19:25,072	INFO scripts.py:960 --   ray status
      2026-10-24 21:19:25,072	INFO scripts.py:964 -- To monitor and debug Ray, view the dashboard at 
      2026-10-24 21:19:25,072	INFO scripts.py:965 --   127.0.0.1:8270
      2026-10-24 21:19:25,072	INFO scripts.py:972 -- If connection to the dashboard fails, check your firewall settings and network configuration.
PASS b2-ray-start: ray start exited 0
checkpoint b1 (b1):
  reading 1: witness [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; live [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; offline [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; without the address live [39283, 39286, 39288, 39290, 39291, 39292, 39293], offline [39283, 39286, 39288, 39290, 39291, 39292, 39293]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; live [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; offline [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; without the address live [39283, 39286, 39288, 39290, 39291, 39292, 39293], offline [39283, 39286, 39288, 39290, 39291, 39292, 39293]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 39283 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281/logs --config_l
    WLOlo 39286 1 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281
    WLO-- 39287 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:653
    WLOlo 39288 1 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 39290 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281/socke
    WLOlo 39291 1 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281 --l
    WLOlo 39292 39290 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=63481 --dashboard-agent-port=
    WLOlo 39293 39290 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=65315 --gc
  parent outside the rows: 1 /sbin/launchd
PASS b1: settled after 2 readings; as expected; {'gcs_server': [39283]}
PASS b4-client-server: as expected; {'client_server': [39287], 'client_server 39287 names the temp dir': False, 'client_server_tree': [39287]}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02b or of the Ray client server for 127.0.0.1:6420 are alive:
          39283 1 <venv>/lib/python3.12/site-pack
          39286 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39287 1 <python> -m ray.util.client.server --address=127.0.0.1:
          39288 1 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          39290 1 <venv>/lib/python3.12/site-pack
          39291 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39292 39290 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39293 39290 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
PASS b5-release-refused-by-processes (old): release at the old location exited 1; the reason is the processes; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02b or of the Ray client server for 127.0.0.1:6420 are alive:
          39283 1 <venv>/lib/python3.12/site-pack
          39286 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39287 1 <python> -m ray.util.client.server --address=127.0.0.1:
          39288 1 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          39290 1 <venv>/lib/python3.12/site-pack
          39291 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39292 39290 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39293 39290 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
PASS b5-release-refused-by-processes (default): release at the default location exited 1; the reason is the processes; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02b", 39283], "location": "old"}'
    exit 0
    stdout:
      recorded pid 39283 in ~/ScienceData/.rehearsal-lock/owner
    stderr: (empty)
PASS b5-set-pid-gcs_server (old): set_pid at the old location exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 39283')]; the other owner file unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02b", 39283], "location": "default"}'
    exit 0
    stdout:
      recorded pid 39283 in ~/.raypoolkit/rehearsal-lock/owner
    stderr: (empty)
PASS b5-set-pid-gcs_server (default): set_pid at the default location exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 39283')]; the other owner file unchanged
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:19:22+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: 39283
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:19:22+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: 39283
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (b)", "/tmp/ray-rpk02c", "in-process"], "location": "old"}'
    exit 3
    stdout: (empty)
    stderr:
      the rehearsal lock is held (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
          acquired: 2026-10-24T21:19:22+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02b
          ray_address: 127.0.0.1:6420
          pid: 39283
      stop and ask the user; nothing here waits on, retries or breaks the lock
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (b)", "/tmp/ray-rpk02c", "in-process"], "location": "default"}'
    exit 3
    stdout: (empty)
    stderr:
      the old location of the rehearsal lock exists (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (b), Python 3.12.15 / Ray 2.43.0
          acquired: 2026-10-24T21:19:22+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02b
          ray_address: 127.0.0.1:6420
          pid: 39283
      it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
PASS b5-second-acquire-refused: at the old location exit 3 (as held); at the default location exit 3 (the old location); both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39283 is alive; not releasing
PASS b5-release-refused (old): release at the old location exited 1; the reason is the recorded pid 39283; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39283 is alive; not releasing
PASS b5-release-refused (default): release at the default location exited 1; the reason is the recorded pid 39283; both owner files unchanged
  $ <venv>/bin/python -I ~/Documents/Code/RayPoolKit/docs/rehearsal-lock/ray_proof.py --driver   (stderr to <scratch>/proof-2.43.0-driver-b.txt)
    stdin: {"address": "127.0.0.1:6420"}
    driver: WORKERS {"tasks": [39356], "actor": 39357}
    driver: READY 39355
PASS b6-driver-ready: the driver said 'READY 39355'
checkpoint b2 (b2):
  reading 1: witness [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358, 39359]; live [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358, 39359]; offline [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358, 39359]; without the address live [39283, 39286, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358, 39359], offline [39283, 39286, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358, 39359]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358]; live [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358]; offline [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358]; without the address live [39283, 39286, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358], offline [39283, 39286, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358]; ports held ['6420', '6421', '8270', '52370']
  reading 3: witness [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358]; live [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358]; offline [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358]; without the address live [39283, 39286, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358], offline [39283, 39286, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 39283 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281/logs --config_l
    WLOlo 39286 1 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281
    WLO-- 39287 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:653
    WLOlo 39288 1 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 39290 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281/socke
    WLOlo 39291 1 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281 --l
    WLOlo 39292 39290 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=63481 --dashboard-agent-port=
    WLOlo 39293 39290 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=65315 --gc
    WLOlo 39356 39290 ray::IDLE
    WLOlo 39357 39290 ray::A
    WLOlo 39358 39290 ray::IDLE
  parent outside the rows: 1 /sbin/launchd
PASS b2: settled after 3 readings; as expected; {'gcs_server': [39283], 'task workers alive': '1 of 1', 'raylet': [39290]}
  driver <- shutdown
    driver: SHUTDOWN
  driver <- exit
    driver: EXIT
PASS b6-driver-exit: the driver said 'SHUTDOWN', 'EXIT' and exited 0
    driver stderr (<scratch>/proof-2.43.0-driver-b.txt):
      2026-10-24 21:19:32,776	INFO worker.py:1654 -- Connecting to existing Ray cluster at address: 127.0.0.1:6420...
      2026-10-24 21:19:32,784	INFO worker.py:1832 -- Connected to Ray cluster. View the dashboard at http://127.0.0.1:8270 
checkpoint b3 (b3):
  reading 1: witness [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; live [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; offline [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; without the address live [39283, 39286, 39288, 39290, 39291, 39292, 39293], offline [39283, 39286, 39288, 39290, 39291, 39292, 39293]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; live [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; offline [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]; without the address live [39283, 39286, 39288, 39290, 39291, 39292, 39293], offline [39283, 39286, 39288, 39290, 39291, 39292, 39293]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 39283 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281/logs --config_l
    WLOlo 39286 1 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281
    WLO-- 39287 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:653
    WLOlo 39288 1 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 39290 1 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281/socke
    WLOlo 39291 1 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281 --l
    WLOlo 39292 39290 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=63481 --dashboard-agent-port=
    WLOlo 39293 39290 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=65315 --gc
  parent outside the rows: 1 /sbin/launchd
PASS b3: settled after 2 readings; as expected; {'gcs_server': [39283]}
  the stop (never ray stop):
  the stop list (8): [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293]
    SIGTERM -> 39283 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281/logs --config_l
    SIGTERM -> 39286 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281
    SIGTERM -> 39287 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:653
    SIGTERM -> 39288 <python> <venv>/lib/python3.12/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    SIGTERM -> 39290 <venv>/lib/python3.12/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281/socke
    SIGTERM -> 39291 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281 --l
    SIGTERM -> 39292 <python> -u <venv>/lib/python3.12/site-packages/ray/dashboard/agent.py --node-ip-address=127.0.0.1 --metrics-export-port=63481 --dashboard-agent-port=
    SIGTERM -> 39293 <python> -u <venv>/lib/python3.12/site-packages/ray/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 --runtime-env-agent-port=65315 --gc
  after the grace (15 s at most): still alive [39283, 39286]
    SIGKILL -> 39283 <venv>/lib/python3.12/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281/logs --config_l
    SIGKILL -> 39286 <python> -u <venv>/lib/python3.12/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-19-23_750988_39281
checkpoint b4 (b4):
  reading 1: witness []; live []; offline []; without the address live [], offline []; ports held []
  reading 2: witness []; live []; offline []; without the address live [], offline []; ports held []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows: none
PASS b4: settled after 2 readings; as expected; {}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "old"}'
    exit 0
    stdout:
      released the rehearsal lock (~/ScienceData/.rehearsal-lock)
    stderr: (empty)
PASS b9 release (old): release at the old location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "default"}'
    exit 0
    stdout:
      released the rehearsal lock (~/.raypoolkit/rehearsal-lock)
    stderr: (empty)
PASS b9 release (default): release at the default location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02b", "127.0.0.1:6420"], "location": "old"}'
    exit 0
    stdout:
      lock: free (~/ScienceData/.rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02b: none
    stderr: (empty)
PASS b9 status (old): status at the old location exited 0; it says free; existing: neither location
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02b", "127.0.0.1:6420"], "location": "default"}'
    exit 0
    stdout:
      lock: free (~/.raypoolkit/rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02b: none
    stderr: (empty)
PASS b9 status (default): status at the default location exited 0; it says free; existing: neither location
part (b): 44.3 s

== after both parts
PASS after-both: existing: neither location; ~/.raypoolkit exists (before: does not exist), holding nothing

Summary: 46 checks passed, 0 failed; exit 0; 67.9 s in all
```

**3.13.16 / Ray 2.55.1:**

```text
the lock, default location: ~/.raypoolkit/rehearsal-lock (where every client looks after the switch-over)
the lock, old location: ~/ScienceData/.rehearsal-lock (where the clients look until the switch-over)
~ is /Users/ds283
python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
executable: <venv>/bin/python
ray: 2.55.1 (<venv>/lib/python3.13/site-packages/ray/__init__.py)
raypoolkit.__file__: ~/Documents/Code/RayPoolKit/raypoolkit/__init__.py
this venv's ray directory, as matched: ['<venv>/lib/python3.13/site-packages/ray/', '<venv>/lib/python3.13/site-packages/ray/']
RAY_USAGE_STATS_ENABLED: 0
pgrep -lf 'gcs_server|raylet|ray::': no process
$ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a  -> exit 0, []
$ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420  -> exit 0, []
$ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02c  -> exit 0, []
port 6420 (GCS): free
port 6421 (client server): free
port 8270 (dashboard): free
port 52370 (dashboard agent): free
~/.raypoolkit: exists

== part (a): an in-process instance with _temp_dir
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1", "/tmp/ray-rpk02a", "in-process"], "location": "default"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/.raypoolkit/rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
    stderr: (empty)
PASS a1-acquire (default): acquire at the default location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1", "/tmp/ray-rpk02a", "in-process"], "location": "old"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/ScienceData/.rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
    stderr: (empty)
PASS a1-acquire (old): acquire at the old location exited 0
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T21:20:40+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: -
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T21:20:41+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: -
PASS a1-acquire-owner-files: both owner files exist, each with {'project': 'RayPoolKit', 'ray_temp_dir': '/tmp/ray-rpk02a', 'ray_address': 'in-process', 'pid': '-'}
  the pre-start reading: 930 processes
  $ <venv>/bin/python -I ~/Documents/Code/RayPoolKit/docs/rehearsal-lock/ray_proof.py --driver   (stderr to <scratch>/proof-2.55.1-driver-a.txt)
    stdin: {"address": "local", "temp_dir": "/tmp/ray-rpk02a"}
    driver: WORKERS {"tasks": [39782, 39783], "actor": 39790}
    driver: READY 39763
PASS a2-driver-ready: the driver said 'READY 39763'
PASS a2-driver-pid: READY 39763; the child's pid 39763
checkpoint a1 (a1):
  reading 1: witness [39764, 39765, 39766, 39770, 39777, 39778, 39779, 39780, 39782, 39783, 39790]; live [39765, 39766, 39770, 39777, 39778, 39779, 39780, 39782, 39783, 39790]; offline [39765, 39766, 39770, 39777, 39778, 39779, 39780, 39782, 39783, 39790]
  reading 2: witness [39764, 39765, 39766, 39770, 39777, 39778, 39779, 39780, 39782, 39783, 39790]; live [39765, 39766, 39770, 39777, 39778, 39779, 39780, 39782, 39783, 39790]; offline [39765, 39766, 39770, 39777, 39778, 39779, 39780, 39782, 39783, 39790]; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows (W witness, L live, O offline; l, o without the address):
    W-- 39764 39763 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/ray_process_reaper.py
    WLO 39765 39763 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02a/session_2026-10-24_21-20-41_782120_39763/logs --config_l
    WLO 39766 39763 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02a/session_2026-10-24_21-20-41_782120_39763
    WLO 39770 39763 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8265 --port-retries=50 --temp-dir=/tmp/ray-rpk02a --lo
    WLO 39777 39763 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02a/session_2026-10-24_21-20-41_782120_39763 --l
    WLO 39778 39763 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02a/session_2026-10-24_21-20-41_782120_39763/socke
    WLO 39779 39778 ray::DashboardAgent
    WLO 39780 39778 ray::RuntimeEnvAgent
    WLO 39782 39778 ray::IDLE
    WLO 39783 39778 ray::IDLE
    WLO 39790 39778 ray::A
  parent outside the rows: 39763 <python>
PASS a1: settled after 2 readings; as expected; {'reaper': [39764], 'task workers alive': '2 of 2'}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02a are alive:
          39765 39763 <venv>/lib/python3.13/site-pack
          39766 39763 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39770 39763 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          39777 39763 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39778 39763 <venv>/lib/python3.13/site-pack
          39779 39778 ray::DashboardAgent
          39780 39778 ray::RuntimeEnvAgent
          39782 39778 ray::IDLE
          39783 39778 ray::IDLE
          39790 39778 ray::A
PASS a4-release-refused-by-processes (old): release at the old location exited 1; the reason is the processes; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02a are alive:
          39765 39763 <venv>/lib/python3.13/site-pack
          39766 39763 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39770 39763 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          39777 39763 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39778 39763 <venv>/lib/python3.13/site-pack
          39779 39778 ray::DashboardAgent
          39780 39778 ray::RuntimeEnvAgent
          39782 39778 ray::IDLE
          39783 39778 ray::IDLE
          39790 39778 ray::A
PASS a4-release-refused-by-processes (default): release at the default location exited 1; the reason is the processes; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02a", 39763], "location": "old"}'
    exit 0
    stdout:
      recorded pid 39763 in ~/ScienceData/.rehearsal-lock/owner
    stderr: (empty)
PASS a5-set-pid-driver (old): set_pid at the old location exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 39763')]; the other owner file unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02a", 39763], "location": "default"}'
    exit 0
    stdout:
      recorded pid 39763 in ~/.raypoolkit/rehearsal-lock/owner
    stderr: (empty)
PASS a5-set-pid-driver (default): set_pid at the default location exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 39763')]; the other owner file unchanged
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T21:20:40+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: 39763
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T21:20:41+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: 39763
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (a)", "/tmp/ray-rpk02c", "in-process"], "location": "old"}'
    exit 3
    stdout: (empty)
    stderr:
      the rehearsal lock is held (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
          acquired: 2026-10-24T21:20:41+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02a
          ray_address: in-process
          pid: 39763
      stop and ask the user; nothing here waits on, retries or breaks the lock
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (a)", "/tmp/ray-rpk02c", "in-process"], "location": "default"}'
    exit 3
    stdout: (empty)
    stderr:
      the old location of the rehearsal lock exists (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (a), Python 3.13.16 / Ray 2.55.1
          acquired: 2026-10-24T21:20:41+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02a
          ray_address: in-process
          pid: 39763
      it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
PASS a6-second-acquire-refused: at the old location exit 3 (as held); at the default location exit 3 (the old location); both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39763 is alive; not releasing
PASS a7-release-refused (old): release at the old location exited 1; the reason is the recorded pid 39763; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39763 is alive; not releasing
PASS a7-release-refused (default): release at the default location exited 1; the reason is the recorded pid 39763; both owner files unchanged
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
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39763 is alive; not releasing
PASS a8-release-refused-by-pid (old): release at the old location exited 1; the reason is the recorded pid 39763; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39763 is alive; not releasing
PASS a8-release-refused-by-pid (default): release at the default location exited 1; the reason is the recorded pid 39763; both owner files unchanged
  driver <- exit
    driver: EXIT
PASS a9-driver-exit: the driver said 'EXIT' and exited 0
    driver stderr (<scratch>/proof-2.55.1-driver-a.txt):
      2026-10-24 21:20:47,208	INFO worker.py:2012 -- Started a local Ray instance.
      <venv>/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
        warnings.warn(
checkpoint a3 (a3):
  reading 1: witness []; live []; offline []
  reading 2: witness []; live []; offline []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02a
  rows: none
PASS a3: settled after 2 readings; as expected; {}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "old"}'
    exit 0
    stdout:
      released the rehearsal lock (~/ScienceData/.rehearsal-lock)
    stderr: (empty)
PASS a9 release (old): release at the old location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 0
    stdout:
      released the rehearsal lock (~/.raypoolkit/rehearsal-lock)
    stderr: (empty)
PASS a9 release (default): release at the default location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02a"], "location": "old"}'
    exit 0
    stdout:
      lock: free (~/ScienceData/.rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02a: none
    stderr: (empty)
PASS a9 status (old): status at the old location exited 0; it says free; existing: neither location
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02a"], "location": "default"}'
    exit 0
    stdout:
      lock: free (~/.raypoolkit/rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02a: none
    stderr: (empty)
PASS a9 status (default): status at the default location exited 0; it says free; existing: neither location
part (a): 23.0 s

== part (b): a ray start --head cluster
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1", "/tmp/ray-rpk02b", "127.0.0.1:6420"], "location": "default"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/.raypoolkit/rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
    stderr: (empty)
PASS b1-acquire (default): acquire at the default location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1", "/tmp/ray-rpk02b", "127.0.0.1:6420"], "location": "old"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/ScienceData/.rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
    stderr: (empty)
PASS b1-acquire (old): acquire at the old location exited 0
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T21:21:03+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: -
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T21:21:04+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: -
PASS b1-acquire-owner-files: both owner files exist, each with {'project': 'RayPoolKit', 'ray_temp_dir': '/tmp/ray-rpk02b', 'ray_address': '127.0.0.1:6420', 'pid': '-'}
  the pre-start reading: 929 processes
  $ <venv>/bin/ray start --head --temp-dir /tmp/ray-rpk02b --port 6420 --ray-client-server-port 6421 --dashboard-port 8270 --dashboard-agent-listen-port 52370 --num-cpus 2 --disable-usage-stats   (output to <scratch>/proof-2.55.1-ray-start.txt)
    exit 0 (5.9 s)
    output:
      2026-10-24 21:21:05,213	INFO usage_lib.py:448 -- Usage stats collection is disabled.
      2026-10-24 21:21:05,214	INFO scripts.py:940 -- Local node IP: 127.0.0.1
      2026-10-24 21:21:10,055	SUCC scripts.py:979 -- --------------------
      2026-10-24 21:21:10,055	SUCC scripts.py:980 -- Ray runtime started.
      2026-10-24 21:21:10,055	SUCC scripts.py:981 -- --------------------
      2026-10-24 21:21:10,055	INFO scripts.py:983 -- Next steps
      2026-10-24 21:21:10,056	INFO scripts.py:1000 -- To connect to this Ray cluster:
      2026-10-24 21:21:10,056	INFO scripts.py:1002 -- import ray
      2026-10-24 21:21:10,056	INFO scripts.py:1003 -- ray.init()
      2026-10-24 21:21:10,056	INFO scripts.py:1017 -- To submit a Ray job using the Ray Jobs CLI:
      2026-10-24 21:21:10,056	INFO scripts.py:1018 --   RAY_API_SERVER_ADDRESS='http://127.0.0.1:8270' ray job submit --working-dir . -- python my_script.py
      2026-10-24 21:21:10,056	INFO scripts.py:1027 -- See https://docs.ray.io/en/latest/cluster/running-applications/job-submission/index.html 
      2026-10-24 21:21:10,056	INFO scripts.py:1031 -- for more information on submitting Ray jobs to the Ray cluster.
      2026-10-24 21:21:10,056	INFO scripts.py:1036 -- To terminate the Ray runtime, run
      2026-10-24 21:21:10,056	INFO scripts.py:1037 --   ray stop
      2026-10-24 21:21:10,056	INFO scripts.py:1040 -- To view the status of the cluster, use
      2026-10-24 21:21:10,056	INFO scripts.py:1041 --   ray status
      2026-10-24 21:21:10,056	INFO scripts.py:1045 -- To monitor and debug Ray, view the dashboard at 
      2026-10-24 21:21:10,056	INFO scripts.py:1046 --   127.0.0.1:8270
      2026-10-24 21:21:10,056	INFO scripts.py:1053 -- If connection to the dashboard fails, check your firewall settings and network configuration.
PASS b2-ray-start: ray start exited 0
checkpoint b1 (b1):
  reading 1: witness [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; live [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; offline [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; without the address live [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901], offline [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; live [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; offline [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; without the address live [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901], offline [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 39883 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876/logs --config_l
    WLOlo 39884 1 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876
    WLO-- 39886 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:0 -
    WLOlo 39887 1 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 39888 39887 <python> -B -c from multiprocessing.resource_tracker import main;main(25)
    WLOlo 39889 39887 ray-dashboard-MetricsHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=28)" --multiprocessing
    WLOlo 39890 39887 ray-dashboard-DataHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=31)" --multiprocessing-fo
    WLOlo 39891 39887 ray-dashboard-EventHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=34)" --multiprocessing-f
    WLOlo 39892 39887 ray-dashboard-JobHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=37)" --multiprocessing-for
    WLOlo 39893 39887 ray-dashboard-NodeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=40)" --multiprocessing-fo
    WLOlo 39894 39887 ray-dashboard-ReportHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=43)" --multiprocessing-
    WLOlo 39895 39887 ray-dashboard-ServeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=46)" --multiprocessing-f
    WLOlo 39896 39887 ray-dashboard-StateHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=49)" --multiprocessing-f
    WLOlo 39897 39887 ray-dashboard-TrainHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=52)" --multiprocessing-f
    WLOlo 39898 1 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876 --l
    WLOlo 39899 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876/socke
    WLOlo 39900 39899 ray::DashboardAgent
    WLOlo 39901 39899 ray::RuntimeEnvAgent
  parent outside the rows: 1 /sbin/launchd
PASS b1: settled after 2 readings; as expected; {'gcs_server': [39883]}
PASS b4-client-server: as expected; {'client_server': [39886], 'client_server 39886 names the temp dir': False, 'client_server_tree': [39886]}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02b or of the Ray client server for 127.0.0.1:6420 are alive:
          39883 1 <venv>/lib/python3.13/site-pack
          39884 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39886 1 <python> -m ray.util.client.server --address=127.0.0.1:
          39887 1 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          39888 39887 <python> -B -c from multiprocessing.resource_tracker im
          39889 39887 ray-dashboard-MetricsHead-0 <python> -B -c "from multi
          39890 39887 ray-dashboard-DataHead-0 <python> -B -c "from multipro
          39891 39887 ray-dashboard-EventHead-0 <python> -B -c "from multipr
          39892 39887 ray-dashboard-JobHead-0 <python> -B -c "from multiproc
          39893 39887 ray-dashboard-NodeHead-0 <python> -B -c "from multipro
          39894 39887 ray-dashboard-ReportHead-0 <python> -B -c "from multip
          39895 39887 ray-dashboard-ServeHead-0 <python> -B -c "from multipr
          39896 39887 ray-dashboard-StateHead-0 <python> -B -c "from multipr
          39897 39887 ray-dashboard-TrainHead-0 <python> -B -c "from multipr
          39898 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39899 1 <venv>/lib/python3.13/site-pack
          39900 39899 ray::DashboardAgent
          39901 39899 ray::RuntimeEnvAgent
PASS b5-release-refused-by-processes (old): release at the old location exited 1; the reason is the processes; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: processes of /tmp/ray-rpk02b or of the Ray client server for 127.0.0.1:6420 are alive:
          39883 1 <venv>/lib/python3.13/site-pack
          39884 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39886 1 <python> -m ray.util.client.server --address=127.0.0.1:
          39887 1 <python> /private/tmp/claude-35086/-Users-ds283-Documen
          39888 39887 <python> -B -c from multiprocessing.resource_tracker im
          39889 39887 ray-dashboard-MetricsHead-0 <python> -B -c "from multi
          39890 39887 ray-dashboard-DataHead-0 <python> -B -c "from multipro
          39891 39887 ray-dashboard-EventHead-0 <python> -B -c "from multipr
          39892 39887 ray-dashboard-JobHead-0 <python> -B -c "from multiproc
          39893 39887 ray-dashboard-NodeHead-0 <python> -B -c "from multipro
          39894 39887 ray-dashboard-ReportHead-0 <python> -B -c "from multip
          39895 39887 ray-dashboard-ServeHead-0 <python> -B -c "from multipr
          39896 39887 ray-dashboard-StateHead-0 <python> -B -c "from multipr
          39897 39887 ray-dashboard-TrainHead-0 <python> -B -c "from multipr
          39898 1 <python> -u /private/tmp/claude-35086/-Users-ds283-Docu
          39899 1 <venv>/lib/python3.13/site-pack
          39900 39899 ray::DashboardAgent
          39901 39899 ray::RuntimeEnvAgent
PASS b5-release-refused-by-processes (default): release at the default location exited 1; the reason is the processes; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02b", 39883], "location": "old"}'
    exit 0
    stdout:
      recorded pid 39883 in ~/ScienceData/.rehearsal-lock/owner
    stderr: (empty)
PASS b5-set-pid-gcs_server (old): set_pid at the old location exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 39883')]; the other owner file unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "set_pid", "args": ["RayPoolKit", "/tmp/ray-rpk02b", 39883], "location": "default"}'
    exit 0
    stdout:
      recorded pid 39883 in ~/.raypoolkit/rehearsal-lock/owner
    stderr: (empty)
PASS b5-set-pid-gcs_server (default): set_pid at the default location exited 0; 7 lines before, 7 after; changed: [('pid: -', 'pid: 39883')]; the other owner file unchanged
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T21:21:03+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: 39883
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
    acquired: 2026-10-24T21:21:04+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02b
    ray_address: 127.0.0.1:6420
    pid: 39883
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (b)", "/tmp/ray-rpk02c", "in-process"], "location": "old"}'
    exit 3
    stdout: (empty)
    stderr:
      the rehearsal lock is held (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
          acquired: 2026-10-24T21:21:04+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02b
          ray_address: 127.0.0.1:6420
          pid: 39883
      stop and ask the user; nothing here waits on, retries or breaks the lock
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKitSecond", "rehearsal-lock 02 proof (c), second acquirer, during part (b)", "/tmp/ray-rpk02c", "in-process"], "location": "default"}'
    exit 3
    stdout: (empty)
    stderr:
      the old location of the rehearsal lock exists (~/ScienceData/.rehearsal-lock); its owner file:
          project: RayPoolKit
          purpose: rehearsal-lock 02 proof (b), Python 3.13.16 / Ray 2.55.1
          acquired: 2026-10-24T21:21:04+01:00
          host: mps026088
          ray_temp_dir: /tmp/ray-rpk02b
          ray_address: 127.0.0.1:6420
          pid: 39883
      it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
PASS b5-second-acquire-refused: at the old location exit 3 (as held); at the default location exit 3 (the old location); both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "old"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39883 is alive; not releasing
PASS b5-release-refused (old): release at the old location exited 1; the reason is the recorded pid 39883; both owner files unchanged
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "default"}'
    exit 1
    stdout: (empty)
    stderr:
      release: the recorded pid 39883 is alive; not releasing
PASS b5-release-refused (default): release at the default location exited 1; the reason is the recorded pid 39883; both owner files unchanged
  $ <venv>/bin/python -I ~/Documents/Code/RayPoolKit/docs/rehearsal-lock/ray_proof.py --driver   (stderr to <scratch>/proof-2.55.1-driver-b.txt)
    stdin: {"address": "127.0.0.1:6420"}
    driver: WORKERS {"tasks": [39963, 39964], "actor": 39965}
    driver: READY 39962
PASS b6-driver-ready: the driver said 'READY 39962'
checkpoint b2 (b2):
  reading 1: witness [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965]; live [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965]; offline [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965]; without the address live [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965], offline [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965]; live [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965]; offline [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965]; without the address live [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965], offline [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 39883 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876/logs --config_l
    WLOlo 39884 1 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876
    WLO-- 39886 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:0 -
    WLOlo 39887 1 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 39888 39887 <python> -B -c from multiprocessing.resource_tracker import main;main(25)
    WLOlo 39889 39887 ray-dashboard-MetricsHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=28)" --multiprocessing
    WLOlo 39890 39887 ray-dashboard-DataHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=31)" --multiprocessing-fo
    WLOlo 39891 39887 ray-dashboard-EventHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=34)" --multiprocessing-f
    WLOlo 39892 39887 ray-dashboard-JobHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=37)" --multiprocessing-for
    WLOlo 39893 39887 ray-dashboard-NodeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=40)" --multiprocessing-fo
    WLOlo 39894 39887 ray-dashboard-ReportHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=43)" --multiprocessing-
    WLOlo 39895 39887 ray-dashboard-ServeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=46)" --multiprocessing-f
    WLOlo 39896 39887 ray-dashboard-StateHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=49)" --multiprocessing-f
    WLOlo 39897 39887 ray-dashboard-TrainHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=52)" --multiprocessing-f
    WLOlo 39898 1 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876 --l
    WLOlo 39899 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876/socke
    WLOlo 39900 39899 ray::DashboardAgent
    WLOlo 39901 39899 ray::RuntimeEnvAgent
    WLOlo 39963 39899 ray::IDLE
    WLOlo 39964 39899 ray::IDLE
    WLOlo 39965 39899 ray::A
  parent outside the rows: 1 /sbin/launchd
PASS b2: settled after 2 readings; as expected; {'gcs_server': [39883], 'task workers alive': '2 of 2', 'raylet': [39899]}
  driver <- shutdown
    driver: SHUTDOWN
  driver <- exit
    driver: EXIT
PASS b6-driver-exit: the driver said 'SHUTDOWN', 'EXIT' and exited 0
    driver stderr (<scratch>/proof-2.55.1-driver-b.txt):
      2026-10-24 21:21:17,951	INFO worker.py:1814 -- Connecting to existing Ray cluster at address: 127.0.0.1:6420...
      2026-10-24 21:21:17,998	INFO worker.py:2003 -- Connected to Ray cluster. View the dashboard at http://127.0.0.1:8270 
      <venv>/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
        warnings.warn(
checkpoint b3 (b3):
  reading 1: witness [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; live [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; offline [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; without the address live [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901], offline [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; ports held ['6420', '6421', '8270', '52370']
  reading 2: witness [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; live [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; offline [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; without the address live [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901], offline [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]; ports held ['6420', '6421', '8270', '52370']; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows (W witness, L live, O offline; l, o without the address):
    WLOlo 39883 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876/logs --config_l
    WLOlo 39884 1 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876
    WLO-- 39886 1 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:0 -
    WLOlo 39887 1 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    WLOlo 39888 39887 <python> -B -c from multiprocessing.resource_tracker import main;main(25)
    WLOlo 39889 39887 ray-dashboard-MetricsHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=28)" --multiprocessing
    WLOlo 39890 39887 ray-dashboard-DataHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=31)" --multiprocessing-fo
    WLOlo 39891 39887 ray-dashboard-EventHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=34)" --multiprocessing-f
    WLOlo 39892 39887 ray-dashboard-JobHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=37)" --multiprocessing-for
    WLOlo 39893 39887 ray-dashboard-NodeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=40)" --multiprocessing-fo
    WLOlo 39894 39887 ray-dashboard-ReportHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=43)" --multiprocessing-
    WLOlo 39895 39887 ray-dashboard-ServeHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=46)" --multiprocessing-f
    WLOlo 39896 39887 ray-dashboard-StateHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=49)" --multiprocessing-f
    WLOlo 39897 39887 ray-dashboard-TrainHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=52)" --multiprocessing-f
    WLOlo 39898 1 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876 --l
    WLOlo 39899 1 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876/socke
    WLOlo 39900 39899 ray::DashboardAgent
    WLOlo 39901 39899 ray::RuntimeEnvAgent
  parent outside the rows: 1 /sbin/launchd
PASS b3: settled after 2 readings; as expected; {'gcs_server': [39883]}
  the stop (never ray stop):
  the stop list (18): [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901]
    SIGTERM -> 39883 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876/logs --config_l
    SIGTERM -> 39884 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876
    SIGTERM -> 39886 <python> -m ray.util.client.server --address=127.0.0.1:6420 --host=127.0.0.1 --port=6421 --mode=proxy --runtime-env-agent-address=http://127.0.0.1:0 -
    SIGTERM -> 39887 <python> <venv>/lib/python3.13/site-packages/ray/dashboard/dashboard.py --host=127.0.0.1 --port=8270 --port-retries=0 --temp-dir=/tmp/ray-rpk02b --log
    SIGTERM -> 39888 <python> -B -c from multiprocessing.resource_tracker import main;main(25)
    39889: gone; nothing sent
    39890: gone; nothing sent
    SIGTERM -> 39891 ray-dashboard-EventHead-0 <python> -B -c "from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=26, pipe_handle=34)" --multiprocessing-f
    39892: gone; nothing sent
    39893: gone; nothing sent
    39894: gone; nothing sent
    39895: gone; nothing sent
    39896: gone; nothing sent
    39897: gone; nothing sent
    SIGTERM -> 39898 <python> -u <venv>/lib/python3.13/site-packages/ray/_private/log_monitor.py --session-dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876 --l
    SIGTERM -> 39899 <venv>/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet --raylet_socket_name=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876/socke
    SIGTERM -> 39900 ray::DashboardAgent
    SIGTERM -> 39901 ray::RuntimeEnvAgent
  after the grace (15 s at most): still alive [39883, 39884]
    SIGKILL -> 39883 <venv>/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server --log_dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876/logs --config_l
    SIGKILL -> 39884 <python> -u <venv>/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py --logs-dir=/tmp/ray-rpk02b/session_2026-10-24_21-21-05_256780_39876
checkpoint b4 (b4):
  reading 1: witness []; live []; offline []; without the address live [], offline []; ports held []
  reading 2: witness []; live []; offline []; without the address live [], offline []; ports held []; settled
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b --ray-address 127.0.0.1:6420
  live listing: $ <venv>/bin/python -I -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk02b
  rows: none
PASS b4: settled after 2 readings; as expected; {}
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "old"}'
    exit 0
    stdout:
      released the rehearsal lock (~/ScienceData/.rehearsal-lock)
    stderr: (empty)
PASS b9 release (old): release at the old location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02b"], "location": "default"}'
    exit 0
    stdout:
      released the rehearsal lock (~/.raypoolkit/rehearsal-lock)
    stderr: (empty)
PASS b9 release (default): release at the default location exited 0
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02b", "127.0.0.1:6420"], "location": "old"}'
    exit 0
    stdout:
      lock: free (~/ScienceData/.rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02b: none
    stderr: (empty)
PASS b9 status (old): status at the old location exited 0; it says free; existing: neither location
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "status", "args": ["/tmp/ray-rpk02b", "127.0.0.1:6420"], "location": "default"}'
    exit 0
    stdout:
      lock: free (~/.raypoolkit/rehearsal-lock does not exist)
      Ray processes of /tmp/ray-rpk02b: none
    stderr: (empty)
PASS b9 status (default): status at the default location exited 0; it says free; existing: neither location
part (b): 48.0 s

== after both parts
PASS after-both: existing: neither location; ~/.raypoolkit exists (before: exists), holding nothing

Summary: 46 checks passed, 0 failed; exit 0; 72.9 s in all
```

### 3.5 The lock, the signals and the roles

- **The lock.** At each end, in each part, the default location and then the old one were acquired
  with exit 0, through the module in fresh interpreters; both owner files carried the part's values
  and `pid: -` (`a1-acquire-owner-files`, `b1-acquire-owner-files`); every refusal left both owner
  files byte-identical; each `set_pid` changed the one `pid:` line of its file and left the other
  file as it was; the old location and then the default one were released with exit 0, and `status`
  at each then said `lock: free`. Between the parts and after the runs neither location existed.
- **`~/.raypoolkit`** was created by the low end's first default `acquire` (`rehearsal_lock.py:449`)
  and is left, empty (clarification 9).
- **The signals.** Only part (b)'s stop list: 8 pids at 2.43.0 (8 `SIGTERM`, then `SIGKILL` to
  `gcs_server` and `monitor.py` after the 15 s grace); 18 at 2.55.1 (8 of the dashboard's children
  gone by their turn and sent nothing, 10 `SIGTERM`, the same two `SIGKILL`ed). Every signal followed
  a command check; "not the recorded one" is printed nowhere. The drivers exited by `exit`, with
  status 0. `ray stop` was never run.
- **The roles** (`$S/scripts/roles.py` over the four records), against 02's:

| Checkpoint | 02, 2.43.0 | 05, 2.43.0 | 02, 2.55.1 | 05, 2.55.1 |
|---|---|---|---|---|
| a1 | witness 11 (reaper, 3 `ray::`), listings 10; 2 of 2 task workers | the same; 1 of 1 (four tasks in one worker); settled at reading 3 (an extra `ray::IDLE` gone) | 11 (reaper, 5 `ray::`), 10; 2 of 2 | the same |
| a2, a3 | empty; the reaper gone | the same | the same | the same |
| b1, b3 | 8 (7 without the address); 6 children of `launchd` | the same | 18 (17) | the same |
| b2 | 11 (10), 3 `ray::` | the same, settled at reading 3 | 21 (20), 5 `ray::` | the same |
| stop | 8; 2 `SIGKILL` | the same | 18; 7 gone; 11 `SIGTERM`; 2 `SIGKILL` | 18; 8 gone; 10 `SIGTERM`; 2 `SIGKILL` |
| b4 | empty; ports free | the same | the same | the same |

The client server ran at both ends, so `b4-client-server` was exercised at both, with
`--address=127.0.0.1:6420` and no temp dir.

### 3.6 The replays (prompt §2.3; clarification 6)

`$S/scripts/scratch_run.sh <name> <venv> none --replay <record>`, `HOME` a fresh scratch directory,
empty before and after each. The mutations are 02's M10 and M12 (`$S/from02/m10.diff`, SHA-256
`4a87ba4ed6e946f1eef4ed1608651d7c2f800ebbdceaae3926a96846a203b29f`; `m12.diff`,
`0ac8883882e3d74b7bfe554c959e67e8202a983f1015cdcc72d74ad7d704cf65`; equal to log 02 §4's table),
each `git apply --check`ed, applied, `-R --check`ed, the four records replayed, and reverted. The
SHA-256 of `raypoolkit/rehearsal_lock.py` and `ray_proof.py` and `git status --porcelain
--untracked-files=all` were equal before and after each (module `92754f2e…bb7f50`). The records:
05's `4e3b61cc…ba2b12f2` (2.43.0) and `1054b018…efc7079d3` (2.55.1); 02's `5f8c82ad…` and
`cdb2b63c…`. Each record replayed in its own end's venv.

| Record | Form printed | Unmutated | M10 | M12 |
|---|---|---|---|---|
| 05, 2.43.0 | both locations (05's form) | exit 0 | exit 1: FAIL a1, b2 | exit 1: FAIL b1, b2, b3 |
| 05, 2.55.1 | both locations | exit 0 | exit 1: FAIL a1, b1, b2, b3 | exit 1: FAIL b1, b2, b3 |
| 02, 2.43.0 | the old location alone (02's form) | exit 0 | exit 1: FAIL a1, b2 | exit 1: FAIL b1, b2, b3 |
| 02, 2.55.1 | the old location alone | exit 0 | exit 1: FAIL a1, b1, b2, b3 | exit 1: FAIL b1, b2, b3 |

Each failure is at the checkpoints log 02 §4 names for its end. 05's failing lines (cut at 300
characters):

```text
== M10, 2.43.0: replay: 2 checkpoint check(s) failed; exit 1
  FAIL a1 (recorded PASS; the offline listing DIFFERS from the record): offline [39177, 39178, 39180, 39181, 39182, 39189, 39190] is not [39177, 39178, 39180, 39181, 39182, 39189, 39190, 39191, 39192, 39194] (extra [], missing [39191, 39192, 39194]); workers [39191, 39192] are not in the witness and b
  FAIL b2 (recorded PASS; the offline listing DIFFERS from the record): offline [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293] is not [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358] (extra [], missing [39356, 39357, 39358]); workers [39356, 39357] are not in the
== M10, 2.55.1: replay: 4 checkpoint check(s) failed; exit 1
  FAIL a1 (recorded PASS; the offline listing DIFFERS from the record): offline [39765, 39766, 39770, 39777, 39778] is not [39765, 39766, 39770, 39777, 39778, 39779, 39780, 39782, 39783, 39790] (extra [], missing [39779, 39780, 39782, 39783, 39790]); workers [39782, 39783, 39790] are not in the witnes
  FAIL b1 (recorded PASS; the offline listing DIFFERS from the record): offline [39883, 39884, 39886, 39887, 39898, 39899] is not [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901] (extra [], missing [39888, 39889, 39890, 3989
  FAIL b2 (recorded PASS; the offline listing DIFFERS from the record): offline [39883, 39884, 39886, 39887, 39898, 39899] is not [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965] (extra [], missing [3988
  FAIL b3 (recorded PASS; the offline listing DIFFERS from the record): offline [39883, 39884, 39886, 39887, 39898, 39899] is not [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901] (extra [], missing [39888, 39889, 39890, 3989
== M12, 2.43.0: replay: 3 checkpoint check(s) failed; exit 1
  FAIL b1 (recorded PASS; the offline listing DIFFERS from the record): offline [39283, 39286, 39288, 39290, 39291, 39292, 39293] is not [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293] (extra [], missing [39287])
  FAIL b2 (recorded PASS; the offline listing DIFFERS from the record): offline [39283, 39286, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358] is not [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293, 39356, 39357, 39358] (extra [], missing [39287])
  FAIL b3 (recorded PASS; the offline listing DIFFERS from the record): offline [39283, 39286, 39288, 39290, 39291, 39292, 39293] is not [39283, 39286, 39287, 39288, 39290, 39291, 39292, 39293] (extra [], missing [39287])
== M12, 2.55.1: replay: 3 checkpoint check(s) failed; exit 1
  FAIL b1 (recorded PASS; the offline listing DIFFERS from the record): offline [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901] is not [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 398
  FAIL b2 (recorded PASS; the offline listing DIFFERS from the record): offline [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901, 39963, 39964, 39965] is not [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 398
  FAIL b3 (recorded PASS; the offline listing DIFFERS from the record): offline [39883, 39884, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 39897, 39898, 39899, 39900, 39901] is not [39883, 39884, 39886, 39887, 39888, 39889, 39890, 39891, 39892, 39893, 39894, 39895, 39896, 398
```

### 3.7 Ray's session directories (clarification 10)

`ls -d /tmp/ray-rpk0*/session_*`, read after both runs: `/tmp/ray-rpk02a` and `/tmp/ray-rpk02b`
each hold six session directories and `session_latest`: two of 02's agent (11:09–11:11, log 02
§3.8), two from 11:29–11:30 (by their time, the orchestrator's runs in the review of 02), and two of
05's (`session_2026-10-24_21-19-01_394932_39174`,
`session_2026-10-24_21-20-41_782120_39763`; `session_2026-10-24_21-19-23_750988_39281`,
`session_2026-10-24_21-21-05_256780_39876`). `/tmp/ray-rpk02c` does not exist. Nothing there was
touched or deleted.

### 3.8 The release (prompt §4.5; clarification 11)

```bash
mkdir -p $S/export-v030 $S/wheel
git archive v0.3.0 | tar -x -C $S/export-v030
uv build --wheel --offline --out-dir $S/wheel $S/export-v030 > $S/state/build.log 2>&1   # exit 0
```

`grep -c "absent from"`: 0. `raypoolkit-0.3.0-py3-none-any.whl`, **21,368 bytes** (SHA-256
`fa3c6ba3…3a124ec`), **10 entries**: `raypoolkit/RayWorkPool.py`, `__init__.py`, `_timing.py`,
`contract.py`, `rehearsal_lock.py`, and `raypoolkit-0.3.0.dist-info/licenses/LICENSE`, `METADATA`,
`WHEEL`, `top_level.txt`, `RECORD`. Each of the five modules is byte-equal (`cmp`) to `git show
67a75b9:raypoolkit/<module>`. It matches §0.3 and the orchestrator's measurement.

### 3.9 The documents (prompt §4.6)

- **Links.** `$S/scripts/links.py` read every Markdown link of each file this commit adds or
  changes (but the script), resolved each relative target against the file's directory (and its
  anchor, if any, against the target's headings), and checked it with `git ls-files
  --error-unmatch` after staging. The document: 6 relative and 7 external links; `switch-over.md`:
  10 relative; the board: 27; `prompts/INDEX.md`: 2; `docs/OPEN_ISSUES.md`: 2; the campaign README
  and this log have none. **0 bad.** Every external link is to
  `github.com/ds283/RayPoolKit/actions/runs/<id>`, a run.
- **`path:line`s at `v0.3.0`.** Every one the document cites at `67a75b9` was read with `git show
  67a75b9:<path> | sed -n …` (§11.5's command): `rehearsal_lock.py:63-64`, `:102`, `:112`, `:331`,
  `:345-347`, `:374-379`, `:435-447`, `:449`; `test_inherited_faults.py:35`; `PROVENANCE.md:102`;
  each is what the document says. The script's own lines (`ray_proof.py:138-142`, `:164-176`, … at
  this commit; `:149`, `:627-643`, `:968`, `:1099-1115`, `:1374-1386` at `722466a`) were read with
  `sed -n` the same way, and `.github/workflows/tests.yml:48-52` at `HEAD`.
- **The counts, and how each was made.**
  - the commits, 25: `git rev-list --count 6e559bf^..636a02a`, and the list by `git log --reverse`,
    classed by subject and by `git show --stat`;
  - the open count at each commit: `git show <c>:docs/OPEN_ISSUES.md | grep -o '\*\*[0-9]* open\*\*'`;
  - the runs, 7, and their jobs and verdicts: `gh run list`, `gh run view <id> --json jobs`, and
    `gh run view <id> --log | grep -E 'Ran [0-9]+ tests|files would be left unchanged'`;
  - the deviations: `$S/scripts/deviations.py`, which splits each log's §2 into its top-level
    numbered items and lists the labels in each (wrapped labels matched); every item without a label
    was read. It also counts the labels' words line by line, and reproduces the prompt's §0.4
    figures exactly (1/16/1, 2/10/1, 1/17/1, 1/7/1, 4/11/1). Entries: 21, 24, 20, 8, 21, and 23 for
    this log;
  - the observations, 39: the bullets of logs 01 and 02 §5 (8 and 8) and the numbered items of logs
    03, 03a and 04 §5 (9, 5 and 9), each listed in the document's §9 table and counted there; the
    tally of dispositions counted from the table's last column;
  - the checks, 46, and the roles: `grep -c '^PASS'` of each output, and `$S/scripts/roles.py` over
    the records;
  - the acceptance greps (18, 5, 5): the checklists' item 8 commands, with `git grep` at the client
    commits (`$S/state/greps.txt`).

### 3.10 The clients (prompt §4.7; hazard 5)

`git -C <client> rev-parse HEAD`, the branch, `git status --porcelain | shasum` and `git stash list
| wc -l`, at the start (21:10) and at the end (21:35):

| Client | `HEAD` | Branch | Porcelain | Stash | Start = end |
|---|---|---|---|---|---|
| SGK | `216e44d883e78df459c378c3669cf2859ecf11e6` | `handover-remedial` | `da39a3ee…` (empty) | 0 | yes |
| CPBH | `807f17549f55f86c000716597492cf8b286ac982` | `jordan-normalization` | `da39a3ee…` (empty) | 0 | yes |
| SI | `7071bb8452252245ca65b3161681c1a634733878` | `rrk-adoption` | `da39a3ee…` (empty) | 0 | yes |

The clients were read only by `git grep` at the checklists' commits (§3.9's acceptance greps); no
client file was opened, run or imported, and no client venv was used.

### 3.11 Scope (prompt §3 hazard 4)

`git diff 6284b3b -- raypoolkit pyproject.toml README.md PROVENANCE.md CLAUDE.md
docs/rehearsal-lock.md docs/adoption .github` before staging: only
`docs/adoption/rehearsal-lock/switch-over.md`'s two dated lines (prompt §2.4). Staged by path:

```text
docs/OPEN_ISSUES.md
docs/adoption/rehearsal-lock/switch-over.md
docs/rehearsal-lock-verification.md
docs/rehearsal-lock/ray_proof.py
prompts/INDEX.md
prompts/rehearsal-lock/IMPLEMENTATION_STATE.md
prompts/rehearsal-lock/README.md
prompts/rehearsal-lock/logs/05-verification-and-close-out.md
```

## 4. The deliberate-breakage record

**P1 and P2**, each a diff of `docs/rehearsal-lock/ray_proof.py` exactly as applied
(`$S/breakage/p1.diff`, SHA-256 `369c74a7…a7953d4`, and `p2.diff`, `32744ee3…29d24ae0`; each applies cleanly to
the final script). For each: `git apply --check`, `git apply`, `git apply -R --check`; the run at each end with
a fresh scratch `HOME`; `git apply -R`; the SHA-256 of the script and the module and `git status
--porcelain --untracked-files=all` equal before and after.

```diff
--- a/docs/rehearsal-lock/ray_proof.py
+++ b/docs/rehearsal-lock/ray_proof.py
@@ -138,7 +138,7 @@
 # The lock's two locations (U7), each computed when called; acquired default first, released
 # old first.
 LOCATIONS = {"default": rl.default_lock_dir, "old": rl.old_lock_dir}
-ACQUIRE_ORDER = ("default", "old")
+ACQUIRE_ORDER = ("default",)
 RELEASE_ORDER = ("old", "default")
 
 OFFLINE_SELF_PID = -1
```

```diff
--- a/docs/rehearsal-lock/ray_proof.py
+++ b/docs/rehearsal-lock/ray_proof.py
@@ -138,7 +138,7 @@
 # The lock's two locations (U7), each computed when called; acquired default first, released
 # old first.
 LOCATIONS = {"default": rl.default_lock_dir, "old": rl.old_lock_dir}
-ACQUIRE_ORDER = ("default", "old")
+ACQUIRE_ORDER = ("old",)
 RELEASE_ORDER = ("old", "default")
 
 OFFLINE_SELF_PID = -1
```

**Before each, from the code:** `ACQUIRE_ORDER` is read only by `acquire_step` (`:1064`), which ends
in `owner_files_step` (`:1080`); part (a) calls it (`:1221`) before its `pre_pids` reading
(`:1226`) and its driver (`:1228`), and part (b) before its `ray start` (`:1295`, `:1300`,
`:1313`). A failed check there goes to `cleanup`, which, with no driver, no `cluster_started` and no
`pre_pids`, only releases what is held. So P1 and P2 fail before the first Ray start. **P3 and P4**
are refused by the preflight (`:1012-1021`), which `run` calls before part (a).

| | Setup | 2.43.0 | 2.55.1 | Scratch `HOME` after |
|---|---|---|---|---|
| P1 | `p1.diff`; `HOME` empty | exit 1: `FAIL a1-acquire-owner-files: the old location has no owner file`; the cleanup's `release` at the default location exit 0 | the same | `.raypoolkit/` (empty) |
| P2 | `p2.diff`; `HOME` empty | exit 1: `FAIL a1-acquire-owner-files: the default location has no owner file`; the cleanup's `release` at the old location exit 0 | the same | `ScienceData/` (empty) |
| P3 | unmutated; `mkdir -p $HOME/.raypoolkit/rehearsal-lock` | exit 3: `REFUSED: the shared lock exists at its default location (~/.raypoolkit/rehearsal-lock); its owner file: (no owner file)` | the same | `.raypoolkit/rehearsal-lock/` only: nothing at the old location |
| P4 | unmutated; `mkdir -p $HOME/ScienceData/.rehearsal-lock` | exit 3: the same at the old location | the same | `ScienceData/.rehearsal-lock/` only: nothing at the default location |

Each preflight printed `~ is $S/homes/<name>`, the scratch `HOME`, and both locations under it. P1
at the low end, whole:

```text
HOME=$S/homes/p1-243 (setup: none)
HOME before:
  .
the lock, default location: ~/.raypoolkit/rehearsal-lock (where every client looks after the switch-over)
the lock, old location: ~/ScienceData/.rehearsal-lock (where the clients look until the switch-over)
~ is $S/homes/p1-243
python: 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)]
executable: <venv>/bin/python
ray: 2.43.0 (<venv>/lib/python3.12/site-packages/ray/__init__.py)
raypoolkit.__file__: /Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py
this venv's ray directory, as matched: ['<venv>/lib/python3.12/site-packages/ray/', '<venv>/lib/python3.12/site-packages/ray/']
RAY_USAGE_STATS_ENABLED: 0
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
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "acquire", "args": ["RayPoolKit", "rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0", "/tmp/ray-rpk02a", "in-process"], "location": "default"}'
    exit 0
    stdout:
      acquired the rehearsal lock (~/.raypoolkit/rehearsal-lock) for RayPoolKit: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    stderr: (empty)
PASS a1-acquire (default): acquire at the default location exited 0
  owner file, default location (~/.raypoolkit/rehearsal-lock/owner):
    project: RayPoolKit
    purpose: rehearsal-lock 02 proof (a), Python 3.12.15 / Ray 2.43.0
    acquired: 2026-10-24T21:18:21+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk02a
    ray_address: in-process
    pid: -
  owner file, old location (~/ScienceData/.rehearsal-lock/owner):
    (none)
FAIL a1-acquire-owner-files: the old location has no owner file
a check failed (a1-acquire-owner-files: the old location has no owner file); cleaning up what this run started
cleanup of part (a):
  $ <venv>/bin/python -I -c LOCK_CODE '{"function": "release", "args": ["RayPoolKit", "/tmp/ray-rpk02a"], "location": "default"}'
    exit 0
    stdout:
      released the rehearsal lock (~/.raypoolkit/rehearsal-lock)
    stderr: (empty)
cleanup complete: nothing of this part is left, and the lock is released

Summary: 1 checks passed, 1 failed: a1-acquire-owner-files; exit 1; 2.7 s in all
exit 1
HOME after:
  .
  ./.raypoolkit
```

P4 at the high end, whole:

```text
HOME=$S/homes/p4-255 (setup: make-old)
HOME before:
  .
  ./ScienceData
  ./ScienceData/.rehearsal-lock
the lock, default location: ~/.raypoolkit/rehearsal-lock (where every client looks after the switch-over)
the lock, old location: ~/ScienceData/.rehearsal-lock (where the clients look until the switch-over)
~ is $S/homes/p4-255
python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
executable: <venv>/bin/python
ray: 2.55.1 (<venv>/lib/python3.13/site-packages/ray/__init__.py)
raypoolkit.__file__: /Users/ds283/Documents/Code/RayPoolKit/raypoolkit/__init__.py
this venv's ray directory, as matched: ['<venv>/lib/python3.13/site-packages/ray/', '<venv>/lib/python3.13/site-packages/ray/']
RAY_USAGE_STATS_ENABLED: 0
REFUSED: the shared lock exists at its old location (~/ScienceData/.rehearsal-lock); its owner file:
    (no owner file)
it is someone's: stop and ask the user
exit 3
HOME after:
  .
  ./ScienceData
  ./ScienceData/.rehearsal-lock
```

**M10 and M12** are 02's, replayed as §3.6. No mutation was ever applied during a real run, or run
against Ray or the real lock.

## 5. Observations not acted on

1. **The owner files of a 05 run say "rehearsal-lock 02 proof"** (clarification 8: the purpose
   strings are 02's). A person reading a held lock during a run sees "02"; the project
   (`RayPoolKit`) and the temp dirs say whose it is. Not an issue.
2. **`~/ScienceData`'s modification time moves with each run**, since the old lock is made and
   removed inside it; its entries do not change. Harmless.
3. **`/tmp/ray-rpk02a` and `…b` keep growing**: six session directories each now, nothing deleting
   them (clarification 10). Each is a few files; a later run adds two more.
4. **At 2.43.0's a1, Ray ran the four tasks in one worker** (1 of 1), where 02's runs had two; the
   expectation covers either (log 02 §2 item 16).
5. **The real runs print the home directory once, unabbreviated** (`~ is /Users/ds283`, deviation
   15), so that a scratch `HOME` can be seen; 02's output never named it.
6. **`black` has not checked the changed script in CI**: the workflow runs it once 05's commit is
   pushed, after the review. Locally it leaves it unchanged.
7. **04 §5.5's sentence of the contract** ("names the temp dir in no command line of its own") is
   explained in the verification document's §9; the contract is not changed (prompt §2.4).

## 6. Issues

**Closed:** `[04-the-proof-takes-the-old-lock]`, moved from the board's §3 to §4 with a **Resolved
(05, 2026-10-24)** line. None opened or narrowed. `docs/OPEN_ISSUES.md`: the row deleted, **0
open**, §1.2 headed "closed 2026-10-24".

## 7. State handed to the next prompt

- **The campaign is closed** (2026-10-24, by 05): six prompts landed, `v0.3.0` tagged, no issue open.
  The board, the README, `prompts/INDEX.md` and the index say so.
- **G2 is open.** Each client switches in a campaign of its own, by its checklist and
  `switch-over.md`. G2 is recorded on the board when it holds, in a records commit of its own.
- **The proof may be run before and after the switch-over alike.** It needs a `ray[default]` venv,
  nothing of Ray running, neither lock location present and no `RAY_*` variable; it holds both
  locations for about a minute, during which every project's `acquire` refuses.
- The records of 05's runs are `$S/runs/proof-2.43.0.json` and `$S/runs/proof-2.55.1.json`, with
  their outputs; 02's are in `$S/from02/`. None is committed.
- The suite is **226** at both ends. The index is **0**. Nothing is pushed: local `main` is three
  commits ahead of `origin/main` (`6284b3b`) with this one; CI's first run over the changed script
  waits for that push.
