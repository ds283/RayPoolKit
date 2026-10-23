# Campaign — rehearsal-lock

**Written:** 2026-10-23 by Claude Opus 5.5, at the user's request, from a read-only comparison of
the three clients' rehearsal-lock code made the same day (§0.2) and two probes of an in-process Ray
instance (§0.3). The user took D1–D4 the same day (§6.1). U1–U6 (§6.2) are put with
recommendations; U1–U5 are needed before 01 is written. **No prompt is written yet.** Each is
written after the one before it has landed and been reviewed, against the tree it left, as in
`extraction`.

## 0. Why this campaign exists

Three projects share one Ray machine and one **rehearsal lock**, so that only one rehearsal or long
build runs at a time. The lock was specified in StochasticInstantons' (SI's)
`.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md` (2026-10-12; §2 the lock, §3 the isolated
clusters, §5 SecondaryGWKit's part), and each project then wrote its own implementation:

- **SecondaryGWKit (SGK):** `tools/rehearsal_lock.py`, Python, standard library only, with
  `tools/tests/test_rehearsal_lock.py` (42 tests);
- **ChamPBH (CPBH)** and **SI:** `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh`, bash,
  which also starts and stops each project's isolated Ray cluster. CPBH's was adapted from SI's.

The lock works only while the three agree, byte for byte, on its location and owner format, and
nothing keeps them in step: a project that moved the lock, or changed a key, would stop seeing the
other two without any error. The location, `~/ScienceData/.rehearsal-lock`, also assumes a
`~/ScienceData` directory that a machine need not have.

This campaign moves the lock into `raypoolkit`, at a new location in the home folder, so that the
contract has one implementation, in a tagged release that each client pins.

### 0.1 What "the lock" means here

Phase 1 of a larger possible extraction (D4). In scope: the lock directory and its owner file;
acquire, recording a pid, release and status; and the check "is any Ray process of this lock's
holder still alive", on which acquire and release depend. Out of scope: starting and stopping a
`ray start` cluster (the isolated ports, the SIGTERM → grace → SIGKILL stop, the port checks),
which stays in CPBH's and SI's `ray_cluster.sh` (§8).

### 0.2 Measurements taken by the planner (2026-10-23, read-only)

**The clients, at their HEADs (all clean):**

| Client | HEAD | File | Blob | Last change |
|---|---|---|---|---|
| SGK | `216e44d` | `tools/rehearsal_lock.py` (475 lines) | `ea14336` | `c863055`, 2026-10-12 |
| SGK | `216e44d` | `tools/tests/test_rehearsal_lock.py` (474 lines, 42 tests) | `cdeecd6` | `a5a6f6d`, 2026-10-12 |
| CPBH | `807f175` | `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` | `eaae1e7` | `288b385`, 2026-10-12 |
| SI | `8b4f615` | `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` | `6c8eada` | `8e04a7c`, 2026-10-12 |

SI's `8b4f615` is the tip of its branch `dk-and-rpk-migration`, which is not yet merged into SI's
`main` (this repository's `extraction` board, G4). All three pin `raypoolkit` at `v0.2.0`.

**The lock, as all three implement it** (the brief's §2):

- the lock is the directory `$HOME/ScienceData/.rehearsal-lock`. Acquire is
  `mkdir -p ~/ScienceData`, then a `mkdir` of the lock with no `-p`, which is atomic; then the
  owner file is written as `owner.tmp` and renamed to `owner`;
- the owner file is UTF-8, seven `key: value` lines in this order: `project`, `purpose`,
  `acquired` (ISO 8601, local time with offset), `host` (`hostname -s`), `ray_temp_dir`,
  `ray_address`, `pid` (`-` until known; the cluster's `gcs_server`, or the driver for an
  in-process instance);
- a held lock means: print the owner file, exit non-zero, and stop and ask the user. No
  implementation waits, retries or breaks a lock; a stale one is removed by the user, by hand;
- only the holder releases, after checking that the owner's `project` and `ray_temp_dir` are its
  own.

The three agree on all of this. They differ in what else they check:

| | SGK | CPBH and SI |
|---|---|---|
| Owner's `ray_temp_dir` / `ray_address` | `in-process` / `in-process` | `/tmp/ray-cpbh`, `127.0.0.1:6380` / `/tmp/ray-si`, `127.0.0.1:6390` |
| Exit codes | 0 ok; 1 refused; 2 usage; 3 held; 4 Ray alive (released again) | 3 held; 4 a stale cluster or a held port (released again) |
| "Our Ray processes" | any command line naming this checkout's `venv/…/site-packages/ray/`, and its descendants | any command line naming the temp dir (in its `/tmp` and `/private/tmp` spellings, as a whole path component), the Ray client server whose `--address` is the cluster's GCS address, and the descendants of both |
| Release refuses while | the recorded pid is alive, or any of its Ray processes is | (`stop` has already killed and checked them) |
| Never counted | this process, its ancestors and its own children | this script, its ancestors, and any command naming `ray_cluster.sh` |

**SGK's rule cannot be moved as it stands.** `venv_roots()` finds the venv from the module's own
path (`Path(__file__).parent.parent / "venv"`). Installed under `site-packages`, that path is
inside the venv, not beside it.

**The callers.** SGK runs the helper as `PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock …`
from its rehearsal scripts and its `CLAUDE.md` ("The shared rehearsal lock"); its in-process
instances are started by `RunDrivers/quadsource_atol_sweep.py:630` and
`RunDrivers/scoped_pipeline_run.py:710` (`address="local"`), and its long-build drivers
(`main.py:314`, six `extract_*.py`) call `ray.init(address=args.ray_address)`. CPBH and SI call
their scripts' `acquire_lock` / `release_lock` from `start` and `stop`, and name the lock in their
`CLAUDE.md` and campaign READMEs.

**State on this machine (2026-10-23).** No lock is held (`~/ScienceData/.rehearsal-lock` does
not exist); no Ray process is running.

### 0.3 Can one process rule serve all three? (U2)

SGK's in-process instances are started by `ray.init(address="local")`. If SGK passes Ray's
`_temp_dir` too, does every process of that instance name the temp dir, as a `ray start` cluster's
do? The planner probed this (`planning/tempdir_probe.py`, with its outputs beside it): an
in-process instance with `_temp_dir="/tmp/ray-rpkp"`, two CPUs, no dashboard, four tasks and one
actor, then the temp-dir rule (the brief's §3, as CPBH's `list_cluster_pids`) applied to `ps`.

| | Ray 2.43.0 / Python 3.12.15 | Ray 2.55.1 / Python 3.13.16 |
|---|---|---|
| Seeds (name the temp dir) | `gcs_server`, `raylet`, and five Python processes under `site-packages/ray/` (three children of the driver, two of the raylet) | `gcs_server`, `raylet`, and three Python processes under `site-packages/ray/`, all children of the driver |
| Reached as descendants of the raylet | every worker and the actor (`ray::IDLE`, `ray::A`) | the same, and `ray::DashboardAgent`, `ray::RuntimeEnvAgent` |
| Workers or actors missed | none | none |
| Not reached | `ray/_private/ray_process_reaper.py`, a child of the driver | the same |
| Ray client server | none (only `ray start` starts one) | none |
| Left after `ray.shutdown()` | nothing naming the temp dir | nothing |

The reaper exits with its driver, and the driver's pid is the one the owner file records, so
release is refused by the pid check for as long as the reaper can live. **So the temp-dir rule
serves an in-process instance, provided it is started with `_temp_dir`.** It is 2026-10-23's
observation of two versions, and 02 re-measures it on the module itself. A shell of the user's
whose command line names the temp dir is matched too (the probe matched the planner's own); the
brief already says so for the clusters.

**Importing Ray costs about 0.3 s.** `python -I -X importtime -c "import ray"`, three runs each:
0.28–0.30 s at 2.43.0, 0.33–0.37 s at 2.55.1. `import raypoolkit` imports `RayWorkPool`, hence Ray,
so any `python -m raypoolkit.<module>` pays this (U3).

## 1. Scope

**In scope:**
- a module `raypoolkit/rehearsal_lock.py` and its command line (§4): the lock at its new location,
  the owner file, the five commands, and one process rule;
- its tests, which need no Ray and touch no real lock;
- a proof of the module under real Ray at both tested ends (02);
- the release `v0.3.0`, and a contract document `docs/rehearsal-lock.md` that replaces the brief's
  §2 as the statement of the lock (03);
- one switch-over checklist per client, and the procedure for the day all three switch (04).

**Out of scope:**
- **any edit to SGK, CPBH or SI.** Each changes in a campaign of its own, on the switch-over day
  (D3, §7);
- **starting or stopping a cluster** (§0.1, §8);
- **a transitional release** that holds the old and new locations at once (D3);
- **any change to `RayWorkPool`, its printed lines, or `raypoolkit.contract`** (§5 rule 7);
- **waiting, queueing or breaking a lock.** The lock makes a clash impossible and visible; the
  user sequences the runs.

## 2. Prompts

| # | Prompt | Covers | Status |
|---|---|---|---|
| 01 | `01-the-lock-module.md` | `raypoolkit/rehearsal_lock.py` under U1, to §4's interface: the location (D2) and the old-location refusal (U4); the owner file; `acquire`, `set-pid`, `release`, `status` and `ray-processes`; the temp-dir rule (U2), with the client-server seed when the address is `host:port`; the command line. Written new, to §4, taking SGK's module as its model (the owner-file code, the ancestor walk, the exit codes) and CPBH's `list_cluster_pids` for the rule. Tests: SGK's 42 ported with neutral project names, and new ones for the rule, built from §0.3's process trees; `HOME` patched in every test. The import guard covers the new module. **Acceptance:** every refusal has a test that a named mutation fails, with only that one reason standing (as SGK's 02a); an owner file of each shape the clients write today parses, and is accepted or refused by the identity check as §4 says; no test creates anything under the real `HOME`. | not written |
| 02 | `02-prove-it-under-real-ray.md` | A script, `docs/rehearsal-lock/ray_proof.py`, not a test (as `extraction`'s U13), run at both tested ends: (a) an in-process instance with `_temp_dir`: acquire, `set-pid`, `ray-processes` lists every Ray process an independent listing finds bar the reaper, release refused while it is up, allowed after `ray.shutdown()`; (b) a `ray start --head` cluster on its own temp dir and non-default ports: the client server found by its address; the script stops it by signalling exactly what `ray-processes` listed, then release succeeds; (c) a second acquire refused. The script takes the shared lock as it stands on the day (§5 rule 9). Nothing under `raypoolkit/` changes unless the proof fails, which is a stop. | not written |
| 03 | `03-release-v0.3.0.md` | `pyproject.toml` at `0.3.0`; `README.md` (usage of the lock; "Changes in `v0.3.0`"); `PROVENANCE.md` ("Since `v0.2.0`": what came from SGK's module at blob `ea14336`, and from CPBH's and SI's scripts); `docs/rehearsal-lock.md`, the contract, written without naming a client; `CLAUDE.md` ("What this repository is"; the command line's exit codes and `status` layout are an interface). Both ends locally and in CI; **`v0.3.0`** tagged on its commit after green CI (U6). | not written |
| 04 | `04-the-switch-over-checklists.md` | `docs/adoption/rehearsal-lock/`: one checklist per client, measured read-only at a named client commit against `v0.3.0`, and `switch-over.md`, the procedure for the day. SGK: delete `tools/rehearsal_lock.py` and its tests; give each in-process `ray.init` a `_temp_dir` (and measure what Ray does when `_temp_dir` is passed with a cluster address); its owner values; its `CLAUDE.md` section. CPBH and SI: replace `acquire_lock`, `release_lock`, the owner functions and the lock half of `status` in `ray_cluster.sh` with calls to the command line, keeping the cluster code; their `CLAUDE.md` and README lines. Each: the pin. The procedure: the preconditions (no lock at either location, no Ray process of any client), the order, and what each client checks afterwards. | not written |
| 05 | `05-verification-and-close-out.md` | `docs/rehearsal-lock-verification.md`, from the package at `v0.3.0` and the records of 01–04; the campaign closed, with G2 open. | not written |

**Order.** 01 → 02 → 03 → 04 → 05. 02 precedes the release so that `v0.3.0` is a module that has
held a real lock over real Ray at both ends. 04 is measured against `v0.3.0`, the release the
clients switch to, so that its checklists need no addenda.

## 3. Datastores

**No prompt opens a store of any client**, and none needs to. A measurement that needs a client's
code (04) reads source files through `git`; it does not import a client or run a client's tests.

## 4. The interfaces between prompts

**Fixed by this plan** (subject to U1–U5):

- **The module** is `raypoolkit.rehearsal_lock`, run as `python -m raypoolkit.rehearsal_lock`
  with the client's venv's interpreter (U1). It imports only the standard library and itself; it
  does not import `ray` (the package root does, unless U3 changes that).
- **The location** is `Path.home() / ".raypoolkit" / "rehearsal-lock"`, computed when called,
  never at import (D2). Acquire creates `~/.raypoolkit` if needed, then makes the lock with one
  `os.mkdir`, never `exist_ok`. No environment variable moves it (U5); a keyword-only `lock_dir`
  argument exists for tests and for 02's proof, and the command line has no option for it.
- **The old location** (U4): while `~/ScienceData/.rehearsal-lock` exists, `acquire` refuses with
  exit 3, printing that directory's owner file and saying it is the old location.
- **The owner file** keeps the brief's seven keys, in its order, written as `owner.tmp` and renamed.
  `ray_temp_dir` is an absolute path for every caller (U2); `ray_address` is `in-process` or
  `host:port`; `pid` is `-` until `set-pid`.
- **Identity.** A lock is the caller's when the owner's `project` and `ray_temp_dir` equal the
  caller's, as the brief has it. `set-pid` and `release` touch nothing else's.
- **The process rule** (U2). From one `ps -axww -o pid= -o ppid= -o command=` (the module's one
  seam for tests): seeds are the processes whose command line contains the temp dir, in its
  spelling with and without a leading `/private`, followed by `/`, a space, `=` or the end of the
  line; and, when the address is `host:port`, the process whose command line contains
  `ray.util.client.server` and `--address=<host:port>` followed by a space or the end. Every
  descendant of a seed is added. This process, its ancestors and its own descendants are never
  listed.
- **The commands and their exit codes** (SGK's, extended):

  ```text
  acquire --project P --purpose TEXT --ray-temp-dir D --ray-address A
      0 held now; 3 held already, or the old location exists (nothing touched);
      4 a process of D is alive (released again); 1 the owner file could not be written
  set-pid --project P --ray-temp-dir D PID
      0 recorded; 1 refused (not P's lock, or PID not alive)
  release --project P --ray-temp-dir D
      0 released, or no lock; 1 refused (not P's lock, its pid alive, or a process of D alive)
  status [--ray-temp-dir D [--ray-address A]]
      0; the lock, its owner file verbatim, whether its pid is alive, and the processes of D
      (or, with no D given, of the owner's ray_temp_dir and ray_address)
  ray-processes --ray-temp-dir D [--ray-address A]
      0 none; 1 some, one per line
  ```

  Usage errors exit 2. `release` takes the address from the owner file.
- **Python API.** The five commands are functions of the module returning those exit codes
  (`acquire(project, purpose, ray_temp_dir, ray_address, *, lock_dir=None)` and so on), plus
  `default_lock_dir()`, `ray_processes(ray_temp_dir, ray_address=None)` and `main(argv=None)`. 01
  names any helper beyond these.
- **After 01:** the module and its tests; the guard covers it. **After 02:** the proof script.
  **After 03:** `docs/rehearsal-lock.md`; the tag `v0.3.0`. **After 04:**
  `docs/adoption/rehearsal-lock/`.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus
   `docs/OPEN_ISSUES.md`.
4. **Do not fix things the prompt did not ask for.** Record them, with a §3 issue.
5. **No prompt edits a client repository.** Reading one through `git` is allowed. Running a
   client's code or tests is not; running an interpreter of a client's venv with `-I` from a
   scratch directory, to use its Ray, is allowed, and is recorded.
6. **No test needs Ray, imports a client, or creates anything under the real `HOME`.** Every test
   patches `HOME` to a temporary directory and passes an explicit `lock_dir` too, so that a
   forgotten argument cannot reach a real lock. The suite count is recorded before and after each
   prompt; a count that falls is a stop.
7. **`RayWorkPool`'s printed lines are an interface** (`CLAUDE.md`). No prompt here changes them,
   or anything else in `RayWorkPool.py` or `contract.py`.
8. **Deliberate breakage.** Each prompt names mutations its tests must catch. The log records each
   as a diff, exactly as applied, so the orchestrator can replay it with `git apply`. Mutations are
   never committed.
9. **Real Ray only in 02 and 05, and only under the shared lock.** A prompt that starts Ray first
   takes the shared lock where the clients look for it on that day (the old location until the
   switch), through the module's own `acquire` with an explicit `lock_dir`, as project
   `RayPoolKit`. If it is held, stop and ask the user. It releases it before it ends, and it never
   runs `ray stop`.
10. **No tag except where a prompt says so** (03: `v0.3.0`), made on the prompt's commit once CI
    passes there, by the user or on the user's instruction; none is moved or deleted.

### 5.1 The log template

- the subject, commit and result;
- **What shipped**;
- **Deviations from the prompt**, each classified;
- **Verification performed**: suite count before and after;
- **The deliberate-breakage record**;
- **Observations not acted on**;
- **State handed to the next prompt**.

## 6. Decisions

### 6.1 Made by the user, and not reopened here

- **D1** (2026-10-23): **extract the shared rehearsal lock into RayPoolKit**, so that one
  implementation, in a tagged release, replaces the three.
- **D2** (2026-10-23): **the lock moves to the home folder**, as a hidden directory:
  `~/.raypoolkit/rehearsal-lock`. `~/ScienceData` need no longer exist.
- **D3** (2026-10-23): **the three clients switch together**, on one day, from their own code to
  `v0.3.0`. There is no transitional release that holds both locations.
- **D4** (2026-10-23): **phase 1 only**: the lock and the process check, not cluster start and
  stop.

### 6.2 Decisions this campaign needs

Each is put with a recommendation. **U1–U5 are needed before 01 is written; U6 before 03.**

- **U1: the module and how it is run** *(for 01)*. *Recommended:* `raypoolkit/rehearsal_lock.py`,
  run as `python -m raypoolkit.rehearsal_lock` with the client's venv's interpreter, and no
  console-script entry point. A console script would put a `raypoolkit-…` command on `PATH`, where
  it could come from another venv; `./venv/bin/python -m …` says whose it is, which is how all
  three clients already call their tools.
- **U2: one process rule, by Ray temp dir** *(for 01; the user asked whether SGK can use it)*.
  *Recommended:* yes. The module carries only the temp-dir rule of §4, and SGK gives every
  in-process instance that runs under the lock a temp dir of its own (`ray.init(address="local",
  _temp_dir="/tmp/ray-sgk")`), recorded in its owner file in place of `in-process`
  (`ray_address` stays `in-process`). §0.3 measured that this finds every Ray process of the
  instance at both tested ends, bar a reaper that the pid check covers. The alternative, keeping
  SGK's venv rule as a second option, was rejected: it has to be rewritten anyway (§0.2, it cannot
  find the venv once packaged), it is a second rule to keep correct, and it matches every Ray
  process of the venv, including an unrelated test run's. Caveats, for 04's SGK checklist: `_temp_dir`
  is a private keyword (stable from 2.43.0 to 2.55.1, measured); what `ray.init` does with
  `_temp_dir` and a cluster address is not measured, so SGK passes it only with `local`; and the
  temp dir is kept short, since macOS limits a Unix socket's path to about 104 bytes.
- **U3: a lazy import of `RayWorkPool` at the package root** *(for 01; the user thought it might
  be worthwhile)*. Making `raypoolkit/__init__.py` load `RayWorkPool` on first use (a module
  `__getattr__`) would let `python -m raypoolkit.rehearsal_lock` run without importing Ray.
  Measured gain: about 0.3 s a call (§0.3), and a lock command that works in a venv whose Ray is
  broken. Measured cost: `extraction`'s U4 pins that the package attribute `raypoolkit.RayWorkPool`
  is the class, shadowing the submodule, and that `from raypoolkit import RayWorkPool` gives the
  class. The planner modelled a lazy root on a two-file package (2026-10-23, Python 3.12.15): a
  `__getattr__` that imports and returns the class gives **the module** to `from pkg import
  Thing` even on a fresh import, because importing the submodule sets the package attribute
  before `__getattr__` returns; one that also rebinds the name in `globals()` gives the class on a
  fresh import, but still gives the module whenever the submodule was imported first (`import
  pkg.Thing`, or `from pkg.Thing import …`), since `__getattr__` is then never consulted. That is a
  change to a released interface, for 0.3 s. *Recommended:* **no** in this campaign; keep the
  eager import. If the
  latency matters later, the clean fix is to rename the submodule (so the class no longer shadows
  it) in a release of its own, which is a client-visible change.
- **U4: refuse while the old location exists** *(for 01)*. *Recommended:* yes, in `0.3.x`, removed
  by a later release once G2 holds. On the switch-over day it catches a client that was missed and
  still holds the old lock, and a stale old lock left behind; it costs one check and its tests. It
  cannot catch a missed client that acquires after the switch (that client cannot see the new
  lock), which is what the procedure in 04 is for.
- **U5: no environment override of the location** *(for 01)*. *Recommended:* none. A variable that
  one project set differently would recreate the problem this campaign removes. Tests and 02's
  proof pass `lock_dir` as a keyword argument; the command line has no option for it.
- **U6: the release** *(for 03)*. *Recommended:* `v0.3.0`, a new minor version: a new module and a
  new command-line interface, with `RayWorkPool` unchanged. A client moving its pin from `v0.2.0`
  changes nothing else.

## 7. Gates outside this repository

| Gate | Holds when | Needed by |
|---|---|---|
| **G1** | The clients' lock code is still what §0.2 measured: SGK `tools/rehearsal_lock.py` blob `ea14336` and its tests `cdeecd6` when 01 is written; CPBH's and SI's `ray_cluster.sh` blobs `eaae1e7` and `6c8eada` (or their successors, re-measured) when 04 is written. If a client changed its lock, the plan is re-measured first. **Holds (2026-10-23)** at SGK `216e44d`, CPBH `807f175`, SI `8b4f615`. | 01, 04 |
| **G2** | The switch-over (D3): all three clients pin `v0.3.0`, each has removed its own lock code as its checklist says, and no client names `~/ScienceData/.rehearsal-lock` outside its historical records; done on one day, in the order `switch-over.md` gives. Each client does its part in a campaign of its own. | — |

The campaign closes at 05. G2 is recorded on this board when it holds, but the campaign does not
wait for it.

## 8. Later units of work

None is in this campaign's scope. Candidates:
- **Phase 2: the cluster.** CPBH's and SI's `ray_cluster.sh` differ only in names, ports and the
  default CPU count (`diff` at the blobs of §0.2). Their start (an isolated temp dir and four fixed
  ports), their targeted stop (SIGTERM to what the process rule finds, a grace period, SIGKILL, and
  a check that the ports are free) and their status could move here as a second module, taking the
  ports as arguments. It signals processes and would need its own proof on a real cluster.
- **Dropping the old-location refusal** (U4), in the release after G2 holds.
- **Renaming the `RayWorkPool` submodule**, if a Ray-free import of the package is wanted (U3).
