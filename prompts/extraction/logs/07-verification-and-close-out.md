# Log — extraction prompt 07: verification and close-out

**Subject:** Verify the extraction campaign and close it · **Commit:** `1ae1a49` ·
**Date:** 2026-10-10 · **Agent:** Claude Opus 5.5

**Result: landed; the campaign is closed.** `docs/extraction-verification.md` verifies the package
as tagged `v0.2.0` (`eaef0ce`) and the records of 01–06, in the twelve sections of the prompt's
§2.1. `docs/extraction/ray_smoke_run.py` runs the pool under a local Ray for the first time (U13):
its five steps pass at Python 3.12.15 / Ray 2.43.0 and 3.13.16 / 2.55.1, Ray leaves no process by
either check, and each run's Ray says "Usage reporting is disabled."; with fault 2's or fault 3's
fix reverted, step 3 or step 1 fails and the rest pass; with fault 1's fix reverted, every step
passes (a finding, not a breakage); with Ray already up, the script exits 2 and starts nothing. The
wheel rebuilt offline from `git archive v0.2.0` is 13,565 bytes with the 9 entries, and its four
modules are `eaef0ce`'s (U14). Nothing under `raypoolkit/` changed: the suite is **121 → 121**, in
`venv/` and at the high end; `black --check raypoolkit docs` gives **17** files unchanged (16 and
the script). **No issue is opened**, so the index stays at **0**. The board, the campaign README,
`prompts/INDEX.md` and the index say the campaign is closed, with G2–G4 open. Nothing was pushed or
tagged, and no client or DatastoreKit was written, run, imported or opened.

**Gate, re-checked at start (22:20 BST).** `HEAD` was `ff265ee` (the orchestration note; the prompt
was written at `787507a`), one commit ahead of `origin/main` (`787507a`); the tree clean; the only
worktree this checkout. `git for-each-ref refs/tags` gave `v0.1.0 0a9cdb2 4e90a8a` and
`v0.2.0 4e7eb15 eaef0ce`. `git diff eaef0ce -- raypoolkit pyproject.toml` was empty. `venv/`:
Python 3.12.15, `ray==2.43.0`, `black==25.1.0`, `raypoolkit` editable at `0.2.0`; `Ran 121 tests …
OK`; `black --check raypoolkit docs`: "16 files would be left unchanged." `docs/OPEN_ISSUES.md`: 0
open. The gate's CI run, `38086076394` on `787507a`, completed with both jobs successful (§3.8).
`~/.ray/config.json` is `{"usage_stats": true}` (read, not edited). Both Ray process patterns were
empty (§3.1); `/tmp/ray` held 51 session directories, the latest
`session_2026-10-10_21-56-07_219812_27391`. Toolchain: `uv` 0.12.20, `/opt/local/bin/python3.12`
3.12.15, `/opt/local/bin/python3.13` 3.13.16, `git` 2.56.0, macOS 27.0.1 (26A434), arm64. Every venv,
export, wheel, diff, driver and output of this log is under the agent's scratch directory,
`<session scratchpad>/agent07`, written `<scratch>` below (and `$S` in commands).

## 1. What shipped

| File | What |
|---|---|
| `docs/extraction-verification.md` | new: the verification document, §1–§12 of the prompt's §2.1 |
| `docs/extraction/ray_smoke_run.py` | new: the smoke run under a local Ray (U13), the prompt's §2.2; `black`-clean; SHA-256 `6e631106abb181c0e155453b4eb0424c69981ea700713cd734eb901aee3804aa` |
| `prompts/extraction/logs/07-verification-and-close-out.md` | this log |
| `prompts/extraction/IMPLEMENTATION_STATE.md` | the header (**CLOSED**), §1's row for 07, and §2's dated line on the gates after the close |
| `prompts/extraction/README.md` | the header, §2's row for 07 and a dated line under §7 |
| `prompts/INDEX.md` | the campaign's line, **closed**, with 0 open issues; the header's count |
| `docs/OPEN_ISSUES.md` | §1.1's heading says the campaign is closed. The header's date was already 2026-10-10 and the count stays **0** |

Nothing else changed: `git diff 71f0d66 -- raypoolkit pyproject.toml README.md PROVENANCE.md
docs/adoption` is empty (§3.10).

## 2. Deviations from the prompt

The orchestrator's brief added fourteen clarifications and additions (1–14 below). Each is an
IMPLEMENTATION CHOICE at the orchestrator's direction, except 2, which is STRUCTURALLY REQUIRED; each
item says its class.

1. **The gate's CI run is `38086076394`, on `787507a`**, cited in the document's §2.3 as "the
   gate's run", linked: `71f0d66` was pushed with `787507a` and has no run of its own, and
   `787507a` touches only `prompts/`. **IMPLEMENTATION CHOICE** (clarification 1).
2. **The commit range is 30 commits, not 28.** The document's §2.2 runs from `3f1dfd4` to `ff265ee`,
   the commit before 07's: `787507a` is classed *prompt written* and `ff265ee` *note*, and
   `3f1dfd4` is a class of its own, *repository started*, which the prompt's §2.1 list omits. So 1
   started, 1 plan, 7 prompts written, 7 notes, 6 prompts, 6 reviews, 2 release records. No further
   records commit landed before 07's (`git log` checked before committing, §3.10).
   **STRUCTURALLY REQUIRED**: the prompt's 28 is not the count at 07's commit (clarification 2).
3. **No usage report.** The script sets `os.environ["RAY_USAGE_STATS_ENABLED"] = "0"`, by
   assignment, before it imports `ray` or `raypoolkit`, and its docstring says why; (d)'s holder sets
   it too; `~/.ray/config.json` was not edited. Every session directory's `dashboard.log` says
   "Usage reporting is disabled." (§3.7). **IMPLEMENTATION CHOICE** (clarification 3).
4. **Ray's session directory is Ray's.** No `_temp_dir` was passed and `RAY_TMPDIR` was not set;
   nothing under `/tmp/ray` was deleted; each run's session directory is named (§3.6, §4).
   **IMPLEMENTATION CHOICE** (clarification 4).
5. **Two process patterns.** Before and after every run, `<scratch>/scripts/raycheck.sh` recorded
   `pgrep -lf 'gcs_server|raylet|ray::'` and `pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler'`,
   each process attributed by its id, its executable and, for a Python process, its first argument
   naming `ray/…` (§3.1). The script's refusal uses the prompt's pattern, unchanged.
   **IMPLEMENTATION CHOICE** (clarification 5).
6. **The patterns' import brings the stand-in module, which the script uses for nothing.** Before it
   starts Ray, the script checks that the pool module's `ray` is the `ray` it imported and that
   neither `ray.wait` nor `ray.get` is a `unittest.mock` object, and prints their `__module__`
   (`ray._private.worker` at both ends). **IMPLEMENTATION CHOICE** (clarification 6).
7. **Step 5's count follows from its own spelling.** The step passes `process_batch_size=2` (and the
   defaults `create_batch_size=5`, `max_task_queue=200`, passed explicitly), and its
   `expected_passes()` counts the loop's passes from `raypoolkit/RayWorkPool.py:286-358`'s rule,
   giving 15, the planner's figure; at the default `process_batch_size=1` it would give 30. The
   comment says how, and the step prints the count. All eleven runs of step 5 gave 15.
   **IMPLEMENTATION CHOICE** (clarification 7; the batch size is this agent's choice within it).
8. **The ends, and which module runs.** `uv venv --offline -p /opt/local/bin/python3.1x` and `uv
   pip install --offline` of `ray==2.43.0` or `ray==2.55.1` with an export (`git archive HEAD`)
   installed editable, in one resolve; the script run from the repository root as `env -u
   PYTHONPATH <venv>/bin/python docs/extraction/ray_smoke_run.py`. Every run printed a
   `raypoolkit.__file__` under its own export (§3.6, §4). `venv/` is not a smoke-run end.
   **IMPLEMENTATION CHOICE** (clarification 8).
9. **(d)'s Ray is bounded**: `<scratch>/scripts/ray_holder.py` (§4, (d)), started in the background,
   with a ready file, a stop file and a 180 s limit, and `ray.shutdown()` in a `finally`. The script
   exited 2 while it was up and made no session directory; after the stop file both patterns were
   empty. **IMPLEMENTATION CHOICE** (clarification 9).
10. **The offline wheel's SHA-256 is not compared**; its size and entries are the check (§3.8).
    **IMPLEMENTATION CHOICE** (clarification 10).
11. **The document counts deviation entries**, not label words: §3.9 says how, and how a label in a
    sentence that classes several entries, or in a sentence that says there was none, was treated.
    **IMPLEMENTATION CHOICE** (clarification 11).
12. **Twelve sections**, the prompt's §2.1 table, with §7 (Decisions), which DatastoreKit's
    precedent (read only as `git -C …/DatastoreKit show 39b1348:docs/extraction-verification.md`)
    does not have. **IMPLEMENTATION CHOICE** (clarification 12).
13. **The equivalence check at `v0.1.0`** was run as `PROVENANCE.md`'s "Re-running the check" says,
    from `<scratch>/scripts/retired_check.sh`, with the worktree at `<scratch>/raypoolkit-v0.1.0`,
    removed after; `git worktree list` then showed this checkout alone (§3.4). It read SGK through
    `git show` at `b510bc9` only. **IMPLEMENTATION CHOICE** (clarification 13).
14. **The counts.** The suite is 121 in `venv/` and at the high end, before and after; `black
    --check raypoolkit docs` goes from 16 files to 17; the index stays at 0. **IMPLEMENTATION
    CHOICE** (clarification 14).

Choices of this prompt's agent:

15. **The steps assert a little more than §1.1 lists**, each a value the script built: step 1 that
    an untitled pool prints nothing; step 2 the compute arguments (`label="item-<n>"`, `payload=1`),
    the value each compute task returned, and that no validation warning is printed; step 3 that
    the post handler's object is the very object `results` holds; step 4 a post handler as well as
    the availability handler, called on the same 10 objects; step 5 that the banner's title is the
    script's and every progress line's total is 30. **IMPLEMENTATION CHOICE.**
16. **Steps 1, 4 and 5 pass `pool=None`**: a pool with no compute handler never uses it. Steps 2 and
    3 pass a `StorePool`, whose `object_store` calls a fresh `Store` actor, killed after the step.
    **IMPLEMENTATION CHOICE.**
17. **The script prints its Ray session directory**, read through Ray's private
    `ray._private.worker._global_node` (it prints "not read" if that fails), and, after
    `ray.shutdown()`, polls the prompt's pattern for up to 10 s and reports how many Ray processes
    are left, without judging it: the exit code stays the steps'. **IMPLEMENTATION CHOICE.**
18. **The refusal prints each process's id and the first word of its command line, no more.** A
    `ray::` process rewrites its title, and on macOS `pgrep -lf` then prints what follows it, which
    can be the process's environment (deviation 23). `raycheck.sh` prints the same, plus a Python
    process's `ray/…` argument. **IMPLEMENTATION CHOICE.**
19. **`measure_client_pools.py` was re-run** (optional, prompt §1.3): each client's output equals its
    checklist's appendix byte for byte (§3.5). It reads the clients through `git` only.
    **IMPLEMENTATION CHOICE.**
20. **`gh run view --log` was read for all eight runs** of the workflow, to cite each suite's and
    `black`'s verdict first-hand; one run, `38055185065` on `6b1ddfe`, was on no record before, and
    the document's §2.3 lists it. Nothing was written to GitHub. **IMPLEMENTATION CHOICE.**
21. **A second low-end run** (22:30:20), because the first run's `time -p` printed `real 10.:0`
    (§3.6); the document gives both. **IMPLEMENTATION CHOICE.**
22. **Each breakage in an export and venv of its own** (`<scratch>/break-a`, `-b`, `-c`), reverted
    afterwards all the same, with the module's SHA-256 checked. **IMPLEMENTATION CHOICE.**

Slip:

23. **The script's first draft printed the processes it refused on whole, and its (d) run captured
    environment text.** The first draft (SHA-256 `692ab490…ef88b89`) ran at both ends and for
    (a)–(d) between 22:24:59 and 22:27:33, with every result as in §3.6 and §4 (five steps pass at
    both ends; (a) fails step 3, (b) step 1, (c) nothing; (d) exit 2, no session directory of its
    own; no process left after any run). Its refusal, and the first `raycheck.sh`, printed
    `pgrep -lf`'s whole lines; for the holder's `ray::` processes those carried environment
    variables, which were written to a scratch output file. That file was deleted, nothing of it is
    in any committed file, and no value from it is quoted here. The script and `raycheck.sh` were
    changed to print ids and first words (deviation 18; the docstring says why), and every run of
    this log and the document was then made again with the committed script.
    **UNINTENDED DRIFT**, corrected.

## 3. Verification performed

### 3.1 Ray's processes, and the clients, at the start

```text
[22:20:38] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:20:38] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
```

```text
SecondaryGWKit HEAD=b510bc90b66985532d28996ab4e5b13b0ff71709 porcelain=da39a3ee5e6b porcelain_lines=0 stash=0 blob=b4666fa89abb26829fd585b881947d7ef5172cea
ChamPBH HEAD=52142d75aebe00855804e2daff4f63aee50ffc3e porcelain=a772db72b9bc porcelain_lines=23 stash=0 blob=aaa6dc9218658e1389fe3eeee5d184dcd8dc0d26
StochasticInstantons HEAD=7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7 porcelain=da39a3ee5e6b porcelain_lines=0 stash=0 blob=92be5b2c9e4c2c65695078bd1b8f97db2f56c7b0
```

(`porcelain` is the first twelve hex digits of `git status --porcelain | shasum`.) Each `HEAD` and
blob is the dispatch's.

### 3.2 The suite, at both ends, by module

Every run from its tree's root, `<python> -m unittest discover -s raypoolkit/tests -t . -v`, in the
foreground, output to a scratch file and the verdict grepped; both process patterns empty before and
after each. Counts by module are the verbose run's `(raypoolkit.tests.<module>.…)` lines.

| Venv | Python / Ray | Tree | Verdict |
|---|---|---|---|
| `venv/`, before | 3.12.15 / 2.43.0 | the repository at `ff265ee` | `Ran 121 tests in 0.790s` `OK` |
| `<scratch>/base-hi/venv` | 3.13.16 / 2.55.1 | `git archive HEAD` at `ff265ee`, editable (`raypoolkit.__file__` `<scratch>/base-hi/tree/raypoolkit/__init__.py`) | `Ran 121 tests in 1.464s` `OK` |
| `venv/`, at the end | 3.12.15 / 2.43.0 | the final tree | `Ran 121 tests in 0.881s` `OK` |

| Module | Before (both ends) | After (`venv/`) |
|---|---|---|
| `test_construction` | 15 | 15 |
| `test_inherited_faults` | 6 | 6 |
| `test_package_imports` | 3 | 3 |
| `test_printed_lines` | 18 | 18 |
| `test_run_paths` | 22 | 22 |
| `test_scheduling` | 7 | 7 |
| `test_standins` | 30 | 30 |
| `test_task_builder` | 20 | 20 |
| **Total** | **121** | **121** |

The high end was made as `uv venv --offline -p /opt/local/bin/python3.13 <scratch>/base-hi/venv`
and `uv pip install --offline --python <scratch>/base-hi/venv/bin/python -e <scratch>/base-hi/tree
"ray==2.55.1"` (18 packages). **Before: 121. After: 121.**

### 3.3 `black`

`./venv/bin/black --check raypoolkit docs` (25.1.0): "16 files would be left unchanged." before;
`./venv/bin/black docs/extraction/ray_smoke_run.py` reformatted the new script once (its first
draft); after, "17 files would be left unchanged."

### 3.4 `compare_with_source.py` at `v0.1.0`, whole

`<scratch>/scripts/retired_check.sh`: `PROVENANCE.md`'s commands, with `<scratch>` for the scratch
directory, exit 0:

```text
Preparing worktree (detached HEAD 4e90a8a)
HEAD is now at 4e90a8a Declare the supported versions and add CI, ready for v0.1.0
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
exit=0
/Users/ds283/Documents/Code/RayPoolKit ff265ee [main]
```

### 3.5 `measure_client_pools.py`, re-run

```text
sgk exit=0 stderr=0
sgk: appendix from line 293 byte-equal (271 lines)
cpbh exit=0 stderr=0
cpbh: appendix from line 206 byte-equal (151 lines)
si exit=0 stderr=0
si: appendix from line 232 byte-equal (196 lines)
```

Each output (`./venv/bin/python docs/adoption/measure_client_pools.py <client>`) was compared by
`cmp` with its checklist from the line `` # `RayWorkPool` in … `` to its end. Both process
patterns were empty before and after.

### 3.6 The smoke runs, whole

`<scratch>/scripts/smoke.sh <python> <label>` runs, from the repository root, `raycheck.sh`; a
listing of `/tmp/ray`'s session directories; the script's SHA-256; `time -p env -u PYTHONPATH
gtimeout 600 <python> docs/extraction/ray_smoke_run.py`; its exit code; `raycheck.sh` again; and the
new session directories, with `grep -ril usage` over each one's `logs/`. Each run is that output,
whole, with the scratch path written `<scratch>`.

**Low end** (`<scratch>/smoke-lo/venv`: `aiosignal==1.4.0 attrs==26.1.0 certifi==2026.7.22
charset-normalizer==3.5.2 click==8.5.0 filelock==4.1.0 frozenlist==1.8.0 idna==3.20
jsonschema==4.26.0 jsonschema-specifications==2025.9.1 msgpack==1.2.3 packaging==26.3
protobuf==7.36.2 pyyaml==6.0.3 ray==2.43.0 -e file://<scratch>/smoke-lo/tree referencing==0.37.0
requests==2.34.2 rpds-py==2026.9.1 typing-extensions==4.16.0 urllib3==2.8.0`):

```text
== lo: before
[22:28:22] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:28:22] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 57
script SHA-256: 6e631106abb181c0e155453b4eb0424c69981ea700713cd734eb901aee3804aa
== lo: run, 22:28:22: env -u PYTHONPATH <scratch>/smoke-lo/venv/bin/python docs/extraction/ray_smoke_run.py
2026-10-10 22:28:28,513	INFO worker.py:1841 -- Started a local Ray instance.
python: 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)]
ray: 2.43.0 (<scratch>/smoke-lo/venv/lib/python3.12/site-packages/ray/__init__.py)
raypoolkit: 0.2.0
raypoolkit.__file__: <scratch>/smoke-lo/tree/raypoolkit/__init__.py
RAY_USAGE_STATS_ENABLED: 0
ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
pgrep -lf 'gcs_server|raylet|ray::': no process
ray.init({'num_cpus': 4, 'include_dashboard': False, 'log_to_driver': False}): 4.4 s
session directory: /tmp/ray/session_2026-10-10_22-28-25_349932_50472
step 1, lookup-only, a generator task_list:
  PASS (0.0 s): results hold the 20 objects in order (0..19); nothing printed
step 2, the compute path:
  PASS (0.9 s): 12 results persisted, in order; store_ids 1-12; stored and available; labels item-0..item-11, payload 1; values from the compute tasks; completion line: Queue summary: 12 lookup (avg 14.03/sec), 12 compute (avg 14.03/sec), 12 store (avg 14.03/sec), 12 validation (avg 14.03/sec)
step 3, a persist with no validation, then a post handler:
  PASS (0.9 s): the post handler saw 5 objects, store_ids [1, 2, 3, 4, 5], each the object results holds
step 4, the availability path:
  PASS (0.0 s): the availability handler was called on the 10 objects looked up ([1, 2, 3, 4, 5, 101, 102, 103, 104, 105]), and the post handler on each; the item whose builder returned None was not looked up
step 5, the printed lines in real time:
    matched by BANNER_PATTERN:
      ** Smoke run, step 5
    matched by PROGRESS_PATTERN:
         -- 2026-10-10 22:28:31 (0.0565s running): 25/30 work items remaining = 16.67% complete
         -- 2026-10-10 22:28:31 (0.06s running): 20/30 work items remaining = 33.33% complete
         -- 2026-10-10 22:28:31 (0.11s running): 15/30 work items remaining = 50.00% complete
         -- 2026-10-10 22:28:31 (0.116s running): 10/30 work items remaining = 66.67% complete
         -- 2026-10-10 22:28:31 (0.166s running): 5/30 work items remaining = 83.33% complete
         -- 2026-10-10 22:28:31 (0.172s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.219s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.225s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.275s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.28s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.331s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.336s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.383s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.392s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:31 (0.437s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
    matched by COMPLETE_PATTERN:
         -- ALL WORK ITEMS COMPLETE in time 0.437s
  PASS (0.4 s): 35 lines captured: 1 banner, 15 progress lines (= 15 passes for 30 tasks at create_batch_size=5, process_batch_size=2), 1 completion line; no stamp has a UTC offset; total_time 0.437 s
ray.shutdown(): ray.is_initialized() is False
Ray processes left after shutdown: 0 (after 0.0 s)
Summary: 5 of 5 steps passed; 8.1 s in all
real 10.:0
user 3.65
sys 1.03
exit=0
== lo: after, 22:28:33
[22:28:33] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:28:33] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 58
new session directories: session_2026-10-10_22-28-25_349932_50472
grep -ril usage /tmp/ray/session_2026-10-10_22-28-25_349932_50472/logs:
  /tmp/ray/session_2026-10-10_22-28-25_349932_50472/logs/raylet.out
  /tmp/ray/session_2026-10-10_22-28-25_349932_50472/logs/debug_state_gcs.txt
  /tmp/ray/session_2026-10-10_22-28-25_349932_50472/logs/debug_state.txt
  /tmp/ray/session_2026-10-10_22-28-25_349932_50472/logs/dashboard.log
  /tmp/ray/session_2026-10-10_22-28-25_349932_50472/logs/gcs_server.out
```

The `time -p` line printed `real 10.:0`, as captured; its cause was not found. A second run:

```text
== lo-2: before
[22:30:18] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:30:18] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 63
script SHA-256: 6e631106abb181c0e155453b4eb0424c69981ea700713cd734eb901aee3804aa
== lo-2: run, 22:30:19: env -u PYTHONPATH <scratch>/smoke-lo/venv/bin/python docs/extraction/ray_smoke_run.py
2026-10-10 22:30:22,476	INFO worker.py:1841 -- Started a local Ray instance.
python: 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)]
ray: 2.43.0 (<scratch>/smoke-lo/venv/lib/python3.12/site-packages/ray/__init__.py)
raypoolkit: 0.2.0
raypoolkit.__file__: <scratch>/smoke-lo/tree/raypoolkit/__init__.py
RAY_USAGE_STATS_ENABLED: 0
ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
pgrep -lf 'gcs_server|raylet|ray::': no process
ray.init({'num_cpus': 4, 'include_dashboard': False, 'log_to_driver': False}): 3.3 s
session directory: /tmp/ray/session_2026-10-10_22-30-20_412001_52710
step 1, lookup-only, a generator task_list:
  PASS (0.0 s): results hold the 20 objects in order (0..19); nothing printed
step 2, the compute path:
  PASS (0.9 s): 12 results persisted, in order; store_ids 1-12; stored and available; labels item-0..item-11, payload 1; values from the compute tasks; completion line: Queue summary: 12 lookup (avg 13.8/sec), 12 compute (avg 13.8/sec), 12 store (avg 13.8/sec), 12 validation (avg 13.8/sec)
step 3, a persist with no validation, then a post handler:
  PASS (0.8 s): the post handler saw 5 objects, store_ids [1, 2, 3, 4, 5], each the object results holds
step 4, the availability path:
  PASS (0.0 s): the availability handler was called on the 10 objects looked up ([1, 2, 3, 4, 5, 101, 102, 103, 104, 105]), and the post handler on each; the item whose builder returned None was not looked up
step 5, the printed lines in real time:
    matched by BANNER_PATTERN:
      ** Smoke run, step 5
    matched by PROGRESS_PATTERN:
         -- 2026-10-10 22:30:25 (0.0591s running): 25/30 work items remaining = 16.67% complete
         -- 2026-10-10 22:30:25 (0.0597s running): 20/30 work items remaining = 33.33% complete
         -- 2026-10-10 22:30:25 (0.114s running): 15/30 work items remaining = 50.00% complete
         -- 2026-10-10 22:30:25 (0.116s running): 10/30 work items remaining = 66.67% complete
         -- 2026-10-10 22:30:25 (0.169s running): 5/30 work items remaining = 83.33% complete
         -- 2026-10-10 22:30:25 (0.171s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:30:25 (0.225s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:30:25 (0.225s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:30:25 (0.278s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:30:25 (0.28s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:30:25 (0.334s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:30:25 (0.335s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:30:25 (0.39s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:30:25 (0.39s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:30:25 (0.445s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
    matched by COMPLETE_PATTERN:
         -- ALL WORK ITEMS COMPLETE in time 0.445s
  PASS (0.4 s): 35 lines captured: 1 banner, 15 progress lines (= 15 passes for 30 tasks at create_batch_size=5, process_batch_size=2), 1 completion line; no stamp has a UTC offset; total_time 0.445 s
ray.shutdown(): ray.is_initialized() is False
Ray processes left after shutdown: 0 (after 0.0 s)
Summary: 5 of 5 steps passed; 7.2 s in all
real 8.52
user 3.61
sys 0.98
exit=0
== lo-2: after, 22:30:27
[22:30:27] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:30:27] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 64
new session directories: session_2026-10-10_22-30-20_412001_52710
grep -ril usage /tmp/ray/session_2026-10-10_22-30-20_412001_52710/logs:
  /tmp/ray/session_2026-10-10_22-30-20_412001_52710/logs/raylet.out
  /tmp/ray/session_2026-10-10_22-30-20_412001_52710/logs/debug_state_gcs.txt
  /tmp/ray/session_2026-10-10_22-30-20_412001_52710/logs/debug_state.txt
  /tmp/ray/session_2026-10-10_22-30-20_412001_52710/logs/dashboard.log
  /tmp/ray/session_2026-10-10_22-30-20_412001_52710/logs/gcs_server.out
```

**High end** (`<scratch>/smoke-hi/venv`: `attrs==26.1.0 certifi==2026.7.22
charset-normalizer==3.5.2 click==8.5.0 filelock==4.1.0 idna==3.20 jsonschema==4.26.0
jsonschema-specifications==2025.9.1 msgpack==1.2.3 packaging==26.3 protobuf==7.36.2 pyyaml==6.0.3
ray==2.55.1 -e file://<scratch>/smoke-hi/tree referencing==0.37.0 requests==2.34.2
rpds-py==2026.9.1 urllib3==2.8.0`):

```text
== hi: before
[22:28:33] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:28:33] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 58
script SHA-256: 6e631106abb181c0e155453b4eb0424c69981ea700713cd734eb901aee3804aa
== hi: run, 22:28:33: env -u PYTHONPATH <scratch>/smoke-hi/venv/bin/python docs/extraction/ray_smoke_run.py
2026-10-10 22:28:42,220	INFO worker.py:2012 -- Started a local Ray instance.
<scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
  warnings.warn(
python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
ray: 2.55.1 (<scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/__init__.py)
raypoolkit: 0.2.0
raypoolkit.__file__: <scratch>/smoke-hi/tree/raypoolkit/__init__.py
RAY_USAGE_STATS_ENABLED: 0
ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
pgrep -lf 'gcs_server|raylet|ray::': no process
ray.init({'num_cpus': 4, 'include_dashboard': False, 'log_to_driver': False}): 6.5 s
session directory: /tmp/ray/session_2026-10-10_22-28-36_890588_50884
step 1, lookup-only, a generator task_list:
  PASS (0.1 s): results hold the 20 objects in order (0..19); nothing printed
step 2, the compute path:
  PASS (1.1 s): 12 results persisted, in order; store_ids 1-12; stored and available; labels item-0..item-11, payload 1; values from the compute tasks; completion line: Queue summary: 12 lookup (avg 10.9/sec), 12 compute (avg 10.9/sec), 12 store (avg 10.9/sec), 12 validation (avg 10.9/sec)
step 3, a persist with no validation, then a post handler:
  PASS (1.0 s): the post handler saw 5 objects, store_ids [1, 2, 3, 4, 5], each the object results holds
step 4, the availability path:
  PASS (0.1 s): the availability handler was called on the 10 objects looked up ([1, 2, 3, 4, 5, 101, 102, 103, 104, 105]), and the post handler on each; the item whose builder returned None was not looked up
step 5, the printed lines in real time:
    matched by BANNER_PATTERN:
      ** Smoke run, step 5
    matched by PROGRESS_PATTERN:
         -- 2026-10-10 22:28:45 (0.0678s running): 25/30 work items remaining = 16.67% complete
         -- 2026-10-10 22:28:45 (0.0689s running): 20/30 work items remaining = 33.33% complete
         -- 2026-10-10 22:28:45 (0.13s running): 15/30 work items remaining = 50.00% complete
         -- 2026-10-10 22:28:45 (0.133s running): 10/30 work items remaining = 66.67% complete
         -- 2026-10-10 22:28:45 (0.187s running): 5/30 work items remaining = 83.33% complete
         -- 2026-10-10 22:28:45 (0.19s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.246s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.249s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.301s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.304s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.358s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:45 (0.36s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:46 (0.41s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:46 (0.414s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:28:46 (0.466s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
    matched by COMPLETE_PATTERN:
         -- ALL WORK ITEMS COMPLETE in time 0.466s
  PASS (0.5 s): 35 lines captured: 1 banner, 15 progress lines (= 15 passes for 30 tasks at create_batch_size=5, process_batch_size=2), 1 completion line; no stamp has a UTC offset; total_time 0.466 s
ray.shutdown(): ray.is_initialized() is False
Ray processes left after shutdown: 0 (after 0.0 s)
Summary: 5 of 5 steps passed; 10.7 s in all
real 13.65
user 4.01
sys 1.08
exit=0
== hi: after, 22:28:47
[22:28:47] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:28:47] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 59
new session directories: session_2026-10-10_22-28-36_890588_50884
grep -ril usage /tmp/ray/session_2026-10-10_22-28-36_890588_50884/logs:
  /tmp/ray/session_2026-10-10_22-28-36_890588_50884/logs/raylet.out
  /tmp/ray/session_2026-10-10_22-28-36_890588_50884/logs/monitor.log
  /tmp/ray/session_2026-10-10_22-28-36_890588_50884/logs/debug_state.txt
  /tmp/ray/session_2026-10-10_22-28-36_890588_50884/logs/dashboard.log
  /tmp/ray/session_2026-10-10_22-28-36_890588_50884/logs/gcs_server.out
```

**The first draft's runs** (deviation 23), 22:24:59–22:27:33, script SHA-256 `692ab490…ef88b89`,
each from the then-fresh venvs, made these session directories, each with "Usage reporting is
disabled.": lo `session_2026-10-10_22-25-02_636713_47412` (5 of 5 passed, 8.3 s, exit 0); hi
`…_22-25-23_905759_47679` (5 of 5, 11.0 s, exit 0); (a) `…_22-26-07_065707_48375` (4 of 5, step 3
failed, exit 1); (b) `…_22-26-25_955128_48581` (4 of 5, step 1, exit 1); (c)
`…_22-26-38_520960_48744` (5 of 5, exit 0); (d)'s holder `…_22-27-02_756112_49342` (the script
exit 2, no session of its own). Every step 5 gave 15 progress lines. Both patterns were empty
before each and after each, and after the holder stopped.

**Another session's Ray.** At 22:30:38, after this prompt's last Ray run had ended (22:30:30), both
patterns found a local Ray of another session, every process under
`<claude scratchpads>/-Users-ds283-Documents-Code-DatastoreKit/…/scratchpad/orch02/hi/…`, with
session `/tmp/ray/session_2026-10-10_22-30-32_859694_52828`. It was not this repository's or this
session's. It was left alone, no run was made while it was up, and at 22:32:22 both patterns were
empty again; `measure_client_pools.py` (which starts no Ray) and the final suite ran after that.

### 3.7 Usage statistics

Each of this prompt's thirteen session directories, `grep -h -o 'Usage reporting is [a-z]*\.'
<dir>/logs/dashboard.log`, and `grep -ril usage <dir>/logs` by file name:

```text
session_2026-10-10_22-25-02_636713_47412: Usage reporting is disabled.   (draft, low)
session_2026-10-10_22-25-23_905759_47679: Usage reporting is disabled.   (draft, high)
session_2026-10-10_22-26-07_065707_48375: Usage reporting is disabled.   (draft, (a))
session_2026-10-10_22-26-25_955128_48581: Usage reporting is disabled.   (draft, (b))
session_2026-10-10_22-26-38_520960_48744: Usage reporting is disabled.   (draft, (c))
session_2026-10-10_22-27-02_756112_49342: Usage reporting is disabled.   (draft, (d)'s holder)
session_2026-10-10_22-28-25_349932_50472: usage_stats_head.py:197 -- Usage reporting is disabled. | files naming usage: dashboard.log debug_state_gcs.txt debug_state.txt gcs_server.out raylet.out  | usage_stats file: 0
session_2026-10-10_22-28-36_890588_50884: usage_stats_head.py:200 -- Usage reporting is disabled. | files naming usage: dashboard.log debug_state.txt gcs_server.out monitor.log raylet.out  | usage_stats file: 0
session_2026-10-10_22-29-03_386918_51164: usage_stats_head.py:200 -- Usage reporting is disabled. | files naming usage: dashboard.log debug_state.txt gcs_server.out monitor.log raylet.out  | usage_stats file: 0
session_2026-10-10_22-29-22_848341_51457: usage_stats_head.py:200 -- Usage reporting is disabled. | files naming usage: dashboard.log debug_state.txt gcs_server.out monitor.log raylet.out  | usage_stats file: 0
session_2026-10-10_22-29-39_766865_51710: usage_stats_head.py:200 -- Usage reporting is disabled. | files naming usage: dashboard.log debug_state.txt gcs_server.out monitor.log raylet.out  | usage_stats file: 0
session_2026-10-10_22-30-02_371190_52353: usage_stats_head.py:200 -- Usage reporting is disabled. | files naming usage: dashboard.log debug_state.txt gcs_server.out monitor.log raylet.out  | usage_stats file: 0
session_2026-10-10_22-30-20_412001_52710: usage_stats_head.py:197 -- Usage reporting is disabled. | files naming usage: dashboard.log debug_state_gcs.txt debug_state.txt gcs_server.out raylet.out  | usage_stats file: 0
```

("usage_stats file" is `find <dir> -iname '*usage_stats*' | wc -l`.) In the first low-end session
the matching lines were read: `dashboard.log`'s are the `UsageStatsHead` module's loading (`Available
modules: [<class 'ray.dashboard.modules.usage_stats.usage_stats_head.UsageStatsHead'>]`, `Loaded 1
modules`) and the line above; `raylet.out`'s "Current usage: 0 / 2.14748 GB", "Resource usage {"
and "Object store current usage"; `debug_state*.txt` and `gcs_server.out`'s "Resource usage" and
"GetAllResourceUsage request count: 0"; at the high end, `monitor.log`'s "Total Usage:". The
session count under `/tmp/ray` went from 51 to 64 by this prompt's runs (65 with the other
session's).

### 3.8 The release (U14) and CI

**The offline wheel**, from `<scratch>/export-v020` (`git archive v0.2.0`), `uv build --wheel
--offline --out-dir <scratch>/wheel <scratch>/export-v020`, exit 0, "absent from" **0** lines, its
log whole:

```text
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
creating '<scratch>/wheel/.tmp-82tqkn6a/raypoolkit-0.2.0-py3-none-any.whl' and adding 'build/bdist.macosx-27.0-arm64/wheel' to it
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
Successfully built <scratch>/wheel/raypoolkit-0.2.0-py3-none-any.whl
```

`raypoolkit-0.2.0-py3-none-any.whl`, **13,565 bytes**, SHA-256 `e8c0def1…0879986e` (not compared,
deviation 10), **9 entries** (the document's §5.2 lists them with sizes), none under
`raypoolkit/tests/`; each of `RayWorkPool.py`, `__init__.py`, `_timing.py` and `contract.py` equal
to `git show eaef0ce:raypoolkit/<module>` (Python's `zipfile` and `subprocess`, byte comparison);
`METADATA` `Version: 0.2.0`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`; `WHEEL`
`Generator: setuptools (84.0.0)`, `Tag: py3-none-any`.

**CI**, read only (`gh run list --limit 20`; `gh run view <id> --json jobs`; `gh run view <id>
--log`, grepped for the suite's and `black`'s verdicts):

```text
38054782562 | 4e90a8a | low: Ran 116 tests | high: Ran 116 tests | OK lines: 2 | black: 15 files would be left unchanged
38055129804 | 9db0619 | low: Ran 116 tests | high: Ran 116 tests | OK lines: 2 | black: 15 files would be left unchanged
38055185065 | 6b1ddfe | low: Ran 116 tests | high: Ran 116 tests | OK lines: 2 | black: 15 files would be left unchanged
38071307103 | 0b6ffd2 | low: Ran 121 tests | high: Ran 121 tests | OK lines: 2 | black: 15 files would be left unchanged
38071490036 | 914070c | low: Ran 121 tests | high: Ran 121 tests | OK lines: 2 | black: 15 files would be left unchanged
38075908457 | eaef0ce | low: Ran 121 tests | high: Ran 121 tests | OK lines: 2 | black: 15 files would be left unchanged
38076190172 | b2b6ab4 | low: Ran 121 tests | high: Ran 121 tests | OK lines: 2 | black: 15 files would be left unchanged
38086076394 | 787507a | low: Ran 121 tests | high: Ran 121 tests | OK lines: 2 | black: 16 files would be left unchanged
```

Every run "completed/success", each with `suite (low)` and `suite (high)` successful.

### 3.9 The documents' checks, and how each count was made

**Links.** `<scratch>/scripts/check_links.py` reads every Markdown link outside fenced blocks;
relative ones must resolve to a tracked file or one of the three new files, an anchor to a heading
of its target, and external ones must be `https://github.com/ds283/…` naming a tag, a commit or a
run: `docs/extraction-verification.md`, **13 links, 0 bad** (4 relative to the campaign's files, 1
to the script, 8 to runs); this log, no Markdown link (it names its files in code spans).

**`path:line`s.** Every `path:line` the document cites at `v0.2.0` was read at `eaef0ce` with `git
show eaef0ce:<path> | sed -n …`: `raypoolkit/RayWorkPool.py:88-206`, `:109-134`, `:109-142`,
`:136-142`, `:141`, `:178`, `:286-358`, `:290`, `:300`, `:302`, `:355-358`, `:380`, `:443`, `:452`,
`:464`, `:477`, `:510`, `:530`, `:546`, `:548`, `:563-595`, `:612-615` and the 26 `.hex()` lines
(`grep -n`: 300 … 546, 26 lines); `raypoolkit/__init__.py:16-19`;
`raypoolkit/tests/standins.py:111`, `:182`, `:243`; `test_standins.py:187`;
`test_printed_lines.py:25`, `:35-39`, `:371`; `test_run_paths.py:277`, `:405`;
`test_inherited_faults.py:44`, `:103`, `:124`, `:141`, `:158`, `:177`; `test_construction.py:96`;
`docs/extraction/compare_with_source.py:121`. Each says what the document says. The lines cited
at other trees are cited with them: `:487-492` and `:489`-`:490` at `v0.1.0` (the board's Package
line), `:88-215` (prompt 06's span, which log 06 corrected), SGK's `main.py:3247` and
`test_layer_is_generic.py:357` (log 06's, not re-read).

**The counts**, each made here, not carried:
- *Commits*: `git log --reverse --format='%h %s' ff265ee`, 30 lines, each classed by its subject
  and the board's notes line (§2.2 of the document): 1 + 1 + 7 + 7 + 6 + 6 + 2.
- *Prompts, notes, reviews and suite counts*: the board's §1 table and notes line, and each log's
  header and suite section.
- *Tags*: `git for-each-ref refs/tags`. *CI*: §3.8.
- *Issues*: the board's §4 headings, `^### \`[` after "## 4. Resolved issues": **8**; §3 says
  "None."; `docs/OPEN_ISSUES.md`: 0.
- *Decisions*: README §6.2's `- **U<n>` items: U1–U14, 14; the commit that recorded each from its
  subject (`4cb493f`'s README holds U1–U3 as taken).
- *Deviation entries*: `<scratch>/scripts/count_deviations.py` takes each log's §2 and lists each
  top-level numbered or bulleted item with the labels in its text, and counts the labels' words line
  by line. Its summary:

  ```text
  01-import-the-pool.md: label words by line 1, 8, 1; numbered or bulleted items 9; label in the item: SR ['6'], IC ['1', '2', '3', '4', '5', '7', '8', '9'], UD []; none []
  02-the-test-suite.md: label words by line 0, 7, 1; numbered or bulleted items 13; label in the item: SR [], IC ['4', '8', '9', '10', '11', '12', '13'], UD []; none ['1', '2', '3', '5', '6', '7']
  03-supported-versions-and-ci.md: label words by line 2, 5, 1; numbered or bulleted items 15; label in the item: SR ['9', '10'], IC ['11', '12', '13', '14', '15'], UD []; none ['1', '2', '3', '4', '5', '6', '7', '8']
  04-fix-the-inherited-faults.md: label words by line 0, 10, 1; numbered or bulleted items 18; label in the item: SR [], IC ['9', '10', '11', '12', '13', '14', '15', '16', '17', '18'], UD []; none ['1', '2', '3', '4', '5', '6', '7', '8']
  05-release-v0.2.0.md: label words by line 2, 10, 2; numbered or bulleted items 20; label in the item: SR ['1', '9'], IC ['10', '11', '12', '13', '14', '15', '16', '17', '18'], UD []; none ['2', '3', '4', '5', '6', '7', '8', '-', '-']
  06-the-adoption-checklists.md: label words by line 4, 9, 2; numbered or bulleted items 26; label in the item: SR ['1', '6', '15'], IC ['16', '17', '18', '19', '20', '21', '22', '23', '24'], UD ['25', '26']; none ['2', '3', '4', '5', '7', '8', '9', '10', '11', '12', '13', '14']
  ```

  The word counts are the prompt's §1.3 figures. Then, by reading: an item with no label in its
  text is classed by the section's sentence ("Each is an IMPLEMENTATION CHOICE at the orchestrator's
  direction", covering items 1–7, 1–8, 1–8, 1–8 and 1–14 of logs 02–06, with "except 1" in 05 and
  "except 1 and 6" in 06 STRUCTURALLY REQUIRED); 05's two slip bullets end "**UNINTENDED DRIFT**,
  corrected" (their label is on a continuation line the parser did not join); log 04's slip is a
  paragraph after item 18, labelled UNINTENDED DRIFT, counted as an entry; "No UNINTENDED DRIFT."
  (01, 02, 03) is not an entry. Entries: 9, 13, 15, 19, 20, 26 = **102**; 8 / 89 / 5.
- *Observations*: the numbered items of 01 §5, 02 §6, 03 §6, 04 §5, 05 §6 and 06 §9, by a regex
  over each section: 7, 7, 6, 6, 5, 7 = **38**; each read, with its disposition decided from the
  later logs, the board and `eaef0ce`. Tally 12 / 2 / 24.
- *The wheel's entries*: `zipfile.ZipFile(...).namelist()`, 9.
- *The suite's modules*: §3.2.
- *The STRUCTURALLY REQUIRED entries that changed a delivered file*: the 8 read one by one; 5
  changed a file the prompt delivered (05 items 1, 9; 06 items 1, 6, 15), 3 a procedure.

**Where the document corrects a log, or adds to the record:**
- log 01 §5.6 says `pip freeze` names the `HEAD` at the install; log 03 §6.3 is right, it names the
  `HEAD` at the freeze, and here `venv/`'s freeze names `ff265ee`, a commit made after its install
  (the document's §9);
- prompt 07 §1.3's 28 commits are 30 at 07's commit (deviation 2), and its deviation figures are
  label words, not entries (§8 of the document);
- run `38055185065` (`6b1ddfe`) was on no record (the document's §2.3);
- log 06 deviation 24's `raypoolkit/__init__.py:16-18` and README §7's "six pinned lines" were
  corrected by 06's review, and the document cites the corrected forms.

### 3.10 The end

```text
SecondaryGWKit HEAD=b510bc90b66985532d28996ab4e5b13b0ff71709 porcelain=da39a3ee5e6b porcelain_lines=0 stash=0 blob=b4666fa89abb26829fd585b881947d7ef5172cea
ChamPBH HEAD=52142d75aebe00855804e2daff4f63aee50ffc3e porcelain=a772db72b9bc porcelain_lines=23 stash=0 blob=aaa6dc9218658e1389fe3eeee5d184dcd8dc0d26
StochasticInstantons HEAD=7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7 porcelain=da39a3ee5e6b porcelain_lines=0 stash=0 blob=92be5b2c9e4c2c65695078bd1b8f97db2f56c7b0
```

The clients' `HEAD`, porcelain hash and line count, stash count and blob equal §3.1's.
DatastoreKit was read only through `git show 39b1348:docs/extraction-verification.md`.

`git diff 71f0d66 -- raypoolkit pyproject.toml README.md PROVENANCE.md docs/adoption` is empty;
`git diff eaef0ce -- raypoolkit pyproject.toml` is empty; `git worktree list` shows this checkout
alone; `git status --porcelain` lists only the seven files of §1, and `--ignored` only
`raypoolkit.egg-info/`, `raypoolkit/__pycache__/` and `venv/`, as before. `git log` before the
commit: `HEAD` was still `ff265ee`. Both process patterns were empty at the end.

### 3.11 The hazards (prompt §3)

1. **Ray started only by the script and by (d)'s holder**, each run's processes recorded before and
   after by both patterns; never `ray start`, never `address=`, never the suite while Ray was up.
   One Ray of another session was found and left alone (§3.6).
2. **No network** but `gh run list` and `gh run view` (read only). Every venv and install was
   `uv … --offline`; no `git fetch`, `git push` or install from a URL.
3. **The package did not change** (§3.10). The breakages edited scratch exports only.
4. **Additive documents**: under `docs/`, two files added and `docs/OPEN_ISSUES.md` changed.
5. **No client touched**: read only through `git` (`rev-parse`, `status --porcelain`, `stash list`,
   and the two scripts' `git show` / `ls-tree`); no `.db` file opened.
6. **The suite ran with no Ray up**, in `venv/` and at the high end before the smoke runs, and in
   `venv/` at the end.
7. **The document's tables were built from the records**; §3.9 says how each count was made.

## 4. The deliberate-breakage record

Each of (a)–(c) is a diff exactly as applied, with `git apply` inside a fresh export of `HEAD` at
the high end (`<scratch>/break-<x>/tree`, its own venv, `ray==2.55.1`), by
`<scratch>/scripts/break.sh` (`bash`): the module's SHA-256 recorded; `git apply --check`; `git
apply`; `git apply -R --check`; the run (`smoke.sh`); `git apply -R`; the SHA-256 compared. Never
applied to the repository, never committed.

### (a) fault 2's fix reverted

`a.diff`:

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

```text
module SHA-256 before: 8f4c1d7d5aa2b133626fe2498d043f05d2c59618a08ccf1b64ae1886fd8ce919
git apply --check: ok
git apply: ok
git apply -R --check: ok
module SHA-256 applied: 0a6f05134dd63abeca950ad66219272ee97b8a638a91eec46c05c2d2eae85f0c
== break-a: before
[22:28:57] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:28:57] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 59
script SHA-256: 6e631106abb181c0e155453b4eb0424c69981ea700713cd734eb901aee3804aa
== break-a: run, 22:28:57: env -u PYTHONPATH <scratch>/break-a/venv/bin/python docs/extraction/ray_smoke_run.py
2026-10-10 22:29:08,982	INFO worker.py:2012 -- Started a local Ray instance.
<scratch>/break-a/venv/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
  warnings.warn(
python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
ray: 2.55.1 (<scratch>/break-a/venv/lib/python3.13/site-packages/ray/__init__.py)
raypoolkit: 0.2.0
raypoolkit.__file__: <scratch>/break-a/tree/raypoolkit/__init__.py
RAY_USAGE_STATS_ENABLED: 0
ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
pgrep -lf 'gcs_server|raylet|ray::': no process
ray.init({'num_cpus': 4, 'include_dashboard': False, 'log_to_driver': False}): 7.0 s
session directory: /tmp/ray/session_2026-10-10_22-29-03_386918_51164
step 1, lookup-only, a generator task_list:
  PASS (0.2 s): results hold the 20 objects in order (0..19); nothing printed
step 2, the compute path:
  PASS (1.5 s): 12 results persisted, in order; store_ids 1-12; stored and available; labels item-0..item-11, payload 1; values from the compute tasks; completion line: Queue summary: 12 lookup (avg 483.7/min), 12 compute (avg 483.7/min), 12 store (avg 483.7/min), 12 validation (avg 483.7/min)
step 3, a persist with no validation, then a post handler:
  FAIL (1.1 s): __main__.StepFailure: the post handler was given store_id None for items [0, 1, 2, 3, 4] (store_ids it saw: [None, None, None, None, None]) [ray_smoke_run.py:328]
step 4, the availability path:
  PASS (0.1 s): the availability handler was called on the 10 objects looked up ([1, 2, 3, 4, 5, 101, 102, 103, 104, 105]), and the post handler on each; the item whose builder returned None was not looked up
step 5, the printed lines in real time:
    matched by BANNER_PATTERN:
      ** Smoke run, step 5
    matched by PROGRESS_PATTERN:
         -- 2026-10-10 22:29:13 (0.067s running): 25/30 work items remaining = 16.67% complete
         -- 2026-10-10 22:29:13 (0.0693s running): 20/30 work items remaining = 33.33% complete
         -- 2026-10-10 22:29:13 (0.126s running): 15/30 work items remaining = 50.00% complete
         -- 2026-10-10 22:29:13 (0.128s running): 10/30 work items remaining = 66.67% complete
         -- 2026-10-10 22:29:13 (0.184s running): 5/30 work items remaining = 83.33% complete
         -- 2026-10-10 22:29:13 (0.185s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:13 (0.244s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:13 (0.244s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:13 (0.303s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:13 (0.303s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:13 (0.362s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:13 (0.363s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:13 (0.419s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:13 (0.422s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:13 (0.476s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
    matched by COMPLETE_PATTERN:
         -- ALL WORK ITEMS COMPLETE in time 0.476s
  PASS (0.5 s): 35 lines captured: 1 banner, 15 progress lines (= 15 passes for 30 tasks at create_batch_size=5, process_batch_size=2), 1 completion line; no stamp has a UTC offset; total_time 0.476 s
ray.shutdown(): ray.is_initialized() is False
Ray processes left after shutdown: 0 (after 0.0 s)
Summary: 4 of 5 steps passed; 11.6 s in all
real 17.59
user 4.36
sys 1.24
exit=1
== break-a: after, 22:29:14
[22:29:15] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:29:15] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 60
new session directories: session_2026-10-10_22-29-03_386918_51164
grep -ril usage /tmp/ray/session_2026-10-10_22-29-03_386918_51164/logs:
  /tmp/ray/session_2026-10-10_22-29-03_386918_51164/logs/raylet.out
  /tmp/ray/session_2026-10-10_22-29-03_386918_51164/logs/monitor.log
  /tmp/ray/session_2026-10-10_22-29-03_386918_51164/logs/debug_state.txt
  /tmp/ray/session_2026-10-10_22-29-03_386918_51164/logs/dashboard.log
  /tmp/ray/session_2026-10-10_22-29-03_386918_51164/logs/gcs_server.out
git apply -R: ok
module SHA-256 after revert: 8f4c1d7d5aa2b133626fe2498d043f05d2c59618a08ccf1b64ae1886fd8ce919 (equal to before: yes)
repository status: ?? docs/extraction/ray_smoke_run.py 
```

**Step 3 fails, naming the five `None` `store_id`s; steps 1, 2, 4 and 5 pass; exit 1.**

### (b) fault 3's fix reverted

`b.diff`:

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

```text
module SHA-256 before: 8f4c1d7d5aa2b133626fe2498d043f05d2c59618a08ccf1b64ae1886fd8ce919
git apply --check: ok
git apply: ok
git apply -R --check: ok
module SHA-256 applied: e162215c026111fd250f168302f41311b9cbdba9d7a17d5d3ef4a39688bfc0b6
== break-b: before
[22:29:18] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:29:18] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 60
script SHA-256: 6e631106abb181c0e155453b4eb0424c69981ea700713cd734eb901aee3804aa
== break-b: run, 22:29:18: env -u PYTHONPATH <scratch>/break-b/venv/bin/python docs/extraction/ray_smoke_run.py
2026-10-10 22:29:28,498	INFO worker.py:2012 -- Started a local Ray instance.
<scratch>/break-b/venv/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
  warnings.warn(
python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
ray: 2.55.1 (<scratch>/break-b/venv/lib/python3.13/site-packages/ray/__init__.py)
raypoolkit: 0.2.0
raypoolkit.__file__: <scratch>/break-b/tree/raypoolkit/__init__.py
RAY_USAGE_STATS_ENABLED: 0
ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
pgrep -lf 'gcs_server|raylet|ray::': no process
ray.init({'num_cpus': 4, 'include_dashboard': False, 'log_to_driver': False}): 6.9 s
session directory: /tmp/ray/session_2026-10-10_22-29-22_848341_51457
step 1, lookup-only, a generator task_list:
  FAIL (0.0 s): builtins.TypeError: object of type 'generator' has no len() [RayWorkPool.py:178]
step 2, the compute path:
  PASS (0.3 s): 12 results persisted, in order; store_ids 1-12; stored and available; labels item-0..item-11, payload 1; values from the compute tasks; completion line: Queue summary: 12 lookup (avg 38.29/sec), 12 compute (avg 38.29/sec), 12 store (avg 38.29/sec), 12 validation (avg 38.29/sec)
step 3, a persist with no validation, then a post handler:
  PASS (1.2 s): the post handler saw 5 objects, store_ids [1, 2, 3, 4, 5], each the object results holds
step 4, the availability path:
  PASS (0.1 s): the availability handler was called on the 10 objects looked up ([1, 2, 3, 4, 5, 101, 102, 103, 104, 105]), and the post handler on each; the item whose builder returned None was not looked up
step 5, the printed lines in real time:
    matched by BANNER_PATTERN:
      ** Smoke run, step 5
    matched by PROGRESS_PATTERN:
         -- 2026-10-10 22:29:31 (0.0746s running): 25/30 work items remaining = 16.67% complete
         -- 2026-10-10 22:29:31 (0.0817s running): 20/30 work items remaining = 33.33% complete
         -- 2026-10-10 22:29:31 (0.134s running): 15/30 work items remaining = 50.00% complete
         -- 2026-10-10 22:29:31 (0.14s running): 10/30 work items remaining = 66.67% complete
         -- 2026-10-10 22:29:31 (0.192s running): 5/30 work items remaining = 83.33% complete
         -- 2026-10-10 22:29:31 (0.199s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:31 (0.249s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:31 (0.256s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:31 (0.311s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:31 (0.319s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:31 (0.37s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:31 (0.375s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:31 (0.435s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:31 (0.436s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:31 (0.487s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
    matched by COMPLETE_PATTERN:
         -- ALL WORK ITEMS COMPLETE in time 0.487s
  PASS (0.5 s): 35 lines captured: 1 banner, 15 progress lines (= 15 passes for 30 tasks at create_batch_size=5, process_batch_size=2), 1 completion line; no stamp has a UTC offset; total_time 0.487 s
ray.shutdown(): ray.is_initialized() is False
Ray processes left after shutdown: 0 (after 0.0 s)
Summary: 4 of 5 steps passed; 10.7 s in all
real 14.89
user 4.16
sys 1.14
exit=1
== break-b: after, 22:29:33
[22:29:33] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:29:33] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 61
new session directories: session_2026-10-10_22-29-22_848341_51457
grep -ril usage /tmp/ray/session_2026-10-10_22-29-22_848341_51457/logs:
  /tmp/ray/session_2026-10-10_22-29-22_848341_51457/logs/raylet.out
  /tmp/ray/session_2026-10-10_22-29-22_848341_51457/logs/monitor.log
  /tmp/ray/session_2026-10-10_22-29-22_848341_51457/logs/debug_state.txt
  /tmp/ray/session_2026-10-10_22-29-22_848341_51457/logs/dashboard.log
  /tmp/ray/session_2026-10-10_22-29-22_848341_51457/logs/gcs_server.out
git apply -R: ok
module SHA-256 after revert: 8f4c1d7d5aa2b133626fe2498d043f05d2c59618a08ccf1b64ae1886fd8ce919 (equal to before: yes)
repository status: ?? docs/extraction/ray_smoke_run.py 
```

**Step 1 fails with `TypeError: object of type 'generator' has no len()` at `RayWorkPool.py:178`;
steps 2–5 run and pass; exit 1.**

### (c) fault 1's fix reverted: a probe

`c.diff`, the 26 `.hex()` → `.hex`:

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

```text
module SHA-256 before: 8f4c1d7d5aa2b133626fe2498d043f05d2c59618a08ccf1b64ae1886fd8ce919
git apply --check: ok
git apply: ok
git apply -R --check: ok
module SHA-256 applied: ba18d2561cd52674ede46850394eda79bcb9395e169e30c16fcc14b4da6e290b
== break-c: before
[22:29:36] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:29:36] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 61
script SHA-256: 6e631106abb181c0e155453b4eb0424c69981ea700713cd734eb901aee3804aa
== break-c: run, 22:29:36: env -u PYTHONPATH <scratch>/break-c/venv/bin/python docs/extraction/ray_smoke_run.py
2026-10-10 22:29:44,093	INFO worker.py:2012 -- Started a local Ray instance.
<scratch>/break-c/venv/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
  warnings.warn(
python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
ray: 2.55.1 (<scratch>/break-c/venv/lib/python3.13/site-packages/ray/__init__.py)
raypoolkit: 0.2.0
raypoolkit.__file__: <scratch>/break-c/tree/raypoolkit/__init__.py
RAY_USAGE_STATS_ENABLED: 0
ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
pgrep -lf 'gcs_server|raylet|ray::': no process
ray.init({'num_cpus': 4, 'include_dashboard': False, 'log_to_driver': False}): 5.4 s
session directory: /tmp/ray/session_2026-10-10_22-29-39_766865_51710
step 1, lookup-only, a generator task_list:
  PASS (0.1 s): results hold the 20 objects in order (0..19); nothing printed
step 2, the compute path:
  PASS (1.6 s): 12 results persisted, in order; store_ids 1-12; stored and available; labels item-0..item-11, payload 1; values from the compute tasks; completion line: Queue summary: 12 lookup (avg 444/min), 12 compute (avg 444/min), 12 store (avg 444/min), 12 validation (avg 444/min)
step 3, a persist with no validation, then a post handler:
  PASS (1.1 s): the post handler saw 5 objects, store_ids [1, 2, 3, 4, 5], each the object results holds
step 4, the availability path:
  PASS (0.1 s): the availability handler was called on the 10 objects looked up ([1, 2, 3, 4, 5, 101, 102, 103, 104, 105]), and the post handler on each; the item whose builder returned None was not looked up
step 5, the printed lines in real time:
    matched by BANNER_PATTERN:
      ** Smoke run, step 5
    matched by PROGRESS_PATTERN:
         -- 2026-10-10 22:29:48 (0.0751s running): 25/30 work items remaining = 16.67% complete
         -- 2026-10-10 22:29:48 (0.0772s running): 20/30 work items remaining = 33.33% complete
         -- 2026-10-10 22:29:48 (0.138s running): 15/30 work items remaining = 50.00% complete
         -- 2026-10-10 22:29:48 (0.139s running): 10/30 work items remaining = 66.67% complete
         -- 2026-10-10 22:29:48 (0.195s running): 5/30 work items remaining = 83.33% complete
         -- 2026-10-10 22:29:48 (0.198s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:48 (0.257s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:48 (0.257s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:48 (0.392s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:48 (0.393s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:48 (0.456s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:48 (0.457s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:48 (0.522s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:48 (0.522s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
         -- 2026-10-10 22:29:48 (0.579s running): 0/30 work items remaining = 100.00% complete (may be waiting for compute/store/validate tasks to finish)
    matched by COMPLETE_PATTERN:
         -- ALL WORK ITEMS COMPLETE in time 0.58s
  PASS (0.6 s): 35 lines captured: 1 banner, 15 progress lines (= 15 passes for 30 tasks at create_batch_size=5, process_batch_size=2), 1 completion line; no stamp has a UTC offset; total_time 0.580 s
ray.shutdown(): ray.is_initialized() is False
Ray processes left after shutdown: 0 (after 0.0 s)
Summary: 5 of 5 steps passed; 10.6 s in all
real 13.44
user 4.03
sys 1.08
exit=0
== break-c: after, 22:29:50
[22:29:50] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:29:50] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
session directories: 62
new session directories: session_2026-10-10_22-29-39_766865_51710
grep -ril usage /tmp/ray/session_2026-10-10_22-29-39_766865_51710/logs:
  /tmp/ray/session_2026-10-10_22-29-39_766865_51710/logs/raylet.out
  /tmp/ray/session_2026-10-10_22-29-39_766865_51710/logs/monitor.log
  /tmp/ray/session_2026-10-10_22-29-39_766865_51710/logs/debug_state.txt
  /tmp/ray/session_2026-10-10_22-29-39_766865_51710/logs/dashboard.log
  /tmp/ray/session_2026-10-10_22-29-39_766865_51710/logs/gcs_server.out
git apply -R: ok
module SHA-256 after revert: 8f4c1d7d5aa2b133626fe2498d043f05d2c59618a08ccf1b64ae1886fd8ce919 (equal to before: yes)
repository status: ?? docs/extraction/ray_smoke_run.py 
```

**Every step passes; exit 0.** Under real Ray, `ray.wait` returns the very refs it was given, so
the bound-method keys still match (the document's §4.5).

### (d) Ray already up

There is no `d.diff`: (d) changes no file. `<scratch>/scripts/ray_holder.py`, run as
`env -u PYTHONPATH <scratch>/smoke-hi/venv/bin/python <scratch>/scripts/ray_holder.py
<scratch>/hold/ready <scratch>/hold/stop` in the background, from `<scratch>/hold`:

```python
"""(d)'s Ray: a bounded session of the agent's own (prompt 07 §4.5 (d); note clarification 9)."""

import os

os.environ["RAY_USAGE_STATS_ENABLED"] = "0"

import pathlib
import sys
import time

import ray

ready = pathlib.Path(sys.argv[1])
stop = pathlib.Path(sys.argv[2])
try:
    ray.init(num_cpus=4, include_dashboard=False, log_to_driver=False)
    node = ray._private.worker._global_node
    print(f"holder: Ray up, session {node.get_session_dir_path()}", flush=True)
    ready.write_text("ready\n")
    deadline = time.monotonic() + 180
    while not stop.exists() and time.monotonic() < deadline:
        time.sleep(0.5)
    print(f"holder: stop file seen: {stop.exists()}", flush=True)
finally:
    ray.shutdown()
    print(f"holder: ray.shutdown(); ray.is_initialized() is {ray.is_initialized()}", flush=True)
```

Before it started (22:29:54):

```text
[22:29:54] pgrep -lf 'gcs_server|raylet|ray::':
  (none, exit 1)
[22:29:54] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  (none, exit 1)
```

The script's run while it was up (`smoke.sh … d`), whole:

```text
== d: before
[22:30:08] pgrep -lf 'gcs_server|raylet|ray::':
  52372 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server
  52400 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/workers/setup_worker.py
  52402 ray::DashboardAgent
  52403 ray::RuntimeEnvAgent
  52431 ray::IDLE
  52432 ray::IDLE
  52433 ray::IDLE
  52434 ray::IDLE
[22:30:08] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  52371 /opt/local/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/ray_process_reaper.py
  52393 /opt/local/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py
  52394 /opt/local/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/dashboard/dashboard.py
  52399 /opt/local/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/log_monitor.py
  52400 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/workers/setup_worker.py
session directories: 63
script SHA-256: 6e631106abb181c0e155453b4eb0424c69981ea700713cd734eb901aee3804aa
== d: run, 22:30:09: env -u PYTHONPATH <scratch>/smoke-hi/venv/bin/python docs/extraction/ray_smoke_run.py
python: 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
ray: 2.55.1 (<scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/__init__.py)
raypoolkit: 0.2.0
raypoolkit.__file__: <scratch>/smoke-hi/tree/raypoolkit/__init__.py
RAY_USAGE_STATS_ENABLED: 0
ray.wait: ray._private.worker; ray.get: ray._private.worker; the pool module's ray is this ray: True
REFUSED: pgrep -lf 'gcs_server|raylet|ray::' exited 0:
  52372 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server
  52400 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet
  52402 ray::DashboardAgent
  52403 ray::RuntimeEnvAgent
  52431 ray::IDLE
  52432 ray::IDLE
  52433 ray::IDLE
  52434 ray::IDLE
real 1.09
user 0.82
sys 0.16
exit=2
== d: after, 22:30:10
[22:30:10] pgrep -lf 'gcs_server|raylet|ray::':
  52372 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/gcs/gcs_server
  52400 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/workers/setup_worker.py
  52402 ray::DashboardAgent
  52403 ray::RuntimeEnvAgent
  52431 ray::IDLE
  52432 ray::IDLE
  52433 ray::IDLE
  52434 ray::IDLE
[22:30:10] pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler':
  52371 /opt/local/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/ray_process_reaper.py
  52393 /opt/local/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/autoscaler/_private/monitor.py
  52394 /opt/local/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/dashboard/dashboard.py
  52399 /opt/local/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/log_monitor.py
  52400 <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/core/src/ray/raylet/raylet <scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/workers/setup_worker.py
session directories: 63
new session directories: none
```

**Exit 2 before starting anything; no new session directory.** The holder's output, after the stop
file:

```text
2026-10-10 22:30:06,542	INFO worker.py:2012 -- Started a local Ray instance.
<scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
  warnings.warn(
holder: Ray up, session /tmp/ray/session_2026-10-10_22-30-02_371190_52353
holder: stop file seen: True
holder: ray.shutdown(); ray.is_initialized() is False
holder exit=0
```

Both patterns at 22:30:12, after the holder exited: empty. Session directories: 62 before the
holder, 63 with it, 63 after the script.

## 5. Observations not acted on

1. **Fault 1's fix is not observable under real Ray** ((c)): it is guarded by the stand-in's
   `fresh_refs` only. Recorded in the document's §4.5 and §10; not a defect, so no issue.
2. **`pgrep -lf` on macOS prints a `ray::` process's rewritten title, and what follows it can be the
   process's environment** (deviation 23). Anyone recording Ray's processes with `-lf` captures it;
   the script and `raycheck.sh` print ids and first words only. No issue: nothing in the package
   does this.
3. **Another session's local Ray** (DatastoreKit's `orch02`) was up from 22:30:32 to before
   22:32:22, sharing `/tmp/ray`; it overlapped no run of this prompt (§3.6).
4. **This prompt added 13 session directories under `/tmp/ray`** (Ray's default; clarification 4),
   and deleted none.
5. **`time -p` printed `real 10.:0`** for the first low-end run; the cause was not found, and a
   second run printed `real 8.52`.
6. **The script reads its session directory through a private Ray attribute**
   (`ray._private.worker._global_node`); a Ray release that moves it makes the script print "not
   read", and nothing else.
7. **Run `38055185065`** (`6b1ddfe`, the release record of `v0.1.0`) passed both jobs and was on no
   record before the document's §2.3.

## 6. Issues

**Opened:** none. **Closed:** none. **Narrowed:** none. `docs/OPEN_ISSUES.md` stays at **0** open;
its §1.1 heading says the campaign is closed.

## 7. State handed on

- The campaign is **closed** (2026-10-10). The board, the campaign README, `prompts/INDEX.md` and
  the index say so. G2–G4 have not held; each is recorded on the board when it holds, in a records
  commit of its own.
- `raypoolkit/` is `eaef0ce`'s (`v0.2.0`). **Suite: 121**, at both ends. `black --check raypoolkit
  docs`: 17 files.
- `docs/extraction-verification.md` is additive from `1ae1a49` (`CLAUDE.md` rule 6): a later
  measurement is a new dated subsection.
- `docs/extraction/ray_smoke_run.py` runs from a checkout or export with the tests in the tree, with
  no Ray up; it is not a test and not in CI.
- No tag was made and nothing was pushed. Local `main` is ahead of `origin/main` (`787507a`) by
  `ff265ee` and `1ae1a49`.
- The drivers, venvs, exports, the wheel and the outputs (`<scratch>`) are not committed; every
  diff they applied is in §4, exactly as applied.
