# Prompt 02 — prove it under real Ray

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 01 landed (`6733447`) and was reviewed (`2e561e2`). CI passed at both ends on `6733447` (run
  40031056598) and on `2e561e2` (run 40031383762).
- `git status` is clean in this repository, and the suite gives `Ran 226 tests … OK`.
- **No Ray process is running** (`pgrep -lf 'gcs_server|raylet|ray::'` finds nothing), and
  `~/ScienceData/.rehearsal-lock` does not exist. If either fails at the start of the work, stop
  and ask the user: the machine is someone else's to use until then.

**Closes:** nothing. **Narrows:** nothing. **Changes:** nothing of the package. **Opens:** only
what the work finds.

**Recommended model:** **Opus.**
- For the first time in this campaign a prompt starts Ray, holds the **real** shared lock that
  three projects use, and signals processes. A mistake here can stop another project's cluster or
  leave the lock held, and each step has to be checked before the next is taken.
- The proof's value is its witness: a listing of Ray's processes that does not use the rule it
  checks. Designing that witness, and the moments it is read, is where a weak proof would pass.

**Read first:**

1. [`README.md`](README.md): §0.3, §1, §2 (row 02), §4, §5 (rules 5, 8 and 9 above all) and §8.
2. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`.
3. The board, and its *Orchestrator review of prompt 01*.
4. `logs/01-the-lock-module.md`: "What shipped", the deviations (3, 13, 18 and 21 above all), the
   observations and the state handed on.
5. `raypoolkit/rehearsal_lock.py` whole, and in `raypoolkit/tests/test_rehearsal_lock.py` the
   reconstructed trees (`TREE_243`, `TREE_255`) and their comment.
6. [`planning/`](planning/): the probe and its two outputs.
7. The precedent for a script that starts Ray: `docs/extraction/ray_smoke_run.py` (its docstring:
   usage statistics off, a refusal to run beside another Ray, how it is run), and
   `prompts/extraction/07-verification-and-close-out.md` §3.
8. How the clients start a cluster today, read **only** through `git show`: `git -C
   /Users/ds283/Documents/Code/ChamPBH show
   807f175:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` (`cmd_start`,
   `stop_cluster`), and the brief's §3, `git -C /Users/ds283/Documents/Code/StochasticInstantons
   show 8b4f615:.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md`.

Facts below are at `2e561e2`, measured on 2026-10-23.

---

## 1. What is wanted

01 tested the module on fixed process tables. 02 runs it against **real Ray at both tested ends**,
holding **the real shared lock**, so that the release 03 makes is a module that has done its job
once on this machine. One script, `docs/rehearsal-lock/ray_proof.py`, not a test (as
`extraction`'s U13), proves three things:

- **(a) An in-process instance** started with `_temp_dir` (README U2, the shape a client's
  in-process driver will take): the rule lists every Ray process that an independent witness
  finds, bar the reaper; `release` is refused while the instance is up, by its processes alone
  and then by its driver's pid; and it is allowed once the driver has called `ray.shutdown()` and
  exited.
- **(b) A `ray start --head` cluster** on its own temp dir and four non-default ports (the shape
  of the clients' clusters): the rule lists every process the witness finds, the Ray client
  server among them by its address; the script stops the cluster by signalling **exactly** what
  `ray-processes` listed, and nothing else; then nothing of it is left, its ports are free, and
  `release` succeeds.
- **(c) A second acquire is refused** while the lock is held: at the lock's own location, as held;
  and at the default location, because the old one exists (U4).

**The lock is the real one, where the clients look for it today** (README §5 rule 9): the old
location, `~/ScienceData/.rehearsal-lock`, taken through the module's own functions with
`lock_dir=old_lock_dir()`, as project `RayPoolKit`. The clients' own implementations see it and
refuse while the proof holds it, which is the lock doing its job. Each part takes the lock before
it starts Ray and releases it after Ray is gone; between the parts the lock is free.

**The package does not change.** Nothing under `raypoolkit/` is touched; the suite stays at
**226**. If the proof finds a fault in the module, that is a stop (§5), not a fix.

---

## 2. What to change

### 2.1 The venvs

The repository's `venv/` (3.12.15, Ray 2.43.0) and, for the high end, a scratch venv as 01 made
it (`uv venv -p /opt/local/bin/python3.13 <dir>`, then `uv pip install --python <dir>/bin/python
-e <repository> "ray==2.55.1" "black==25.1.0"`). The proof runs with each venv's interpreter, which
also gives it that venv's `ray` executable (`Path(sys.executable).parent / "ray"`). Record each
venv's versions in the log.

### 2.2 The script, `docs/rehearsal-lock/ray_proof.py`

A shebang and a module docstring in the form of `ray_smoke_run.py`'s: what it proves, how it is
run, what it never does. No licence header (the package's modules carry it; `docs/` scripts do
not). It imports the standard library and `raypoolkit.rehearsal_lock`; it imports `ray` only in
its driver mode. It names no client. It sets `RAY_USAGE_STATS_ENABLED=0` in the environment of
every child, and passes `--disable-usage-stats` to `ray start`.

Run as, from the repository root, with nothing running:

```bash
env -u PYTHONPATH ./venv/bin/python docs/rehearsal-lock/ray_proof.py --record <scratch>/proof-2.43.0.json
```

**Fixed names.** Temp dirs `/tmp/ray-rpk02a` (part a), `/tmp/ray-rpk02b` (part b) and
`/tmp/ray-rpk02c` (the second acquirer's; never started). The cluster's ports: GCS `6420`, client
server `6421`, dashboard `8270`, dashboard agent `52370`, none of them a client's (`6380`–`6381`,
`6390`–`6391`, `8266`–`8267`, `52366`–`52367`) or Ray's default. Two CPUs everywhere. Project
`RayPoolKit` for the lock; `RayPoolKitSecond` for the second acquirer.

**The script's own command line names no temp dir.** A process whose command names the temp dir
seeds the rule's walk, ancestors included (log 01, deviation 3), so the script never puts one in
its own `argv`, nor in the driver's: the driver reads its settings from one JSON line on stdin.

**Every lock operation runs in a fresh interpreter.** The rule never lists the calling process,
its ancestors or **its own descendants**. The driver of part (a) is the script's child, so a call
of `release` from the script's own process could not see the driver's Ray processes at all. So
every `acquire`, `set_pid`, `release` and `status` is a child process, `[sys.executable, "-I",
"-c", CODE, <json arguments>]` run from an empty temporary directory, where `CODE` imports
`raypoolkit.rehearsal_lock`, calls the named function with `lock_dir=old_lock_dir()` (or with no
`lock_dir`, for (c)'s default-location acquire) and exits with its return code. The driver is
then the child's sibling, and visible. Every listing is the real command,
`[sys.executable, "-I", "-m", "raypoolkit.rehearsal_lock", "ray-processes", "--ray-temp-dir", T,
…]`. The script prints each child's command (without `CODE` in full), exit status, stdout and
stderr.

**The witness.** An independent listing of the instance's processes, from one reading of
`ps -axww -o pid= -o ppid= -o command=` that the script makes itself:
- **new**: the pids absent from the part's reading taken just before it started Ray;
- **Ray's**: of those, each whose command contains this venv's `site-packages/ray/` directory
  (as written and as `os.path.realpath` gives it), or `ray.util.client.server`, or starts with
  `ray::`; and every descendant of one;
- minus the script's own process and its children (the driver, the lock children, `ps`).

It uses neither the temp dir nor the address, which is what makes it independent of the rule.
Beside it, at each checkpoint, two readings of the rule: the **live** one (the `ray-processes`
command's output) and an **offline** one, `ray_processes(T, A, ps_text=<the script's reading>,
self_pid=0)`, which evaluates the rule on the very rows the witness was computed from (pid 0 is in
no table, so nothing is held back as "safe").

**A checkpoint** reads the table, the live listing and the offline listing, and repeats (one
second apart, at most 20 times) until two consecutive readings agree, since Ray starts workers and
agents on its own schedule. It then checks the part's expectation (below) and records:
the witness, both listings and, for every pid in any of them, `pid`, `ppid` and command. A
checkpoint that does not settle is a failed check.

**What is printed and what is kept.** Printed rows (and so the log) are cut: a command that starts
`ray::` keeps its first word only (a process that rewrites its title can show its environment
after it on macOS), any other is cut at 150 characters, and the home directory is written `~`. The
`--record` file, in a scratch directory and never committed, keeps those rows' full commands, the
listings, the witness and each check's verdict, for §2.3. Nothing else of the machine's process
table is printed or kept.

**Before anything starts** (exit 2 if any fails, having touched nothing): no Ray process
(`pgrep -lf 'gcs_server|raylet|ray::'`, printing each pid and the first word of its command only);
no process names any of the three temp dirs (the live listing of each, empty); the four ports free
(`lsof -nP -iTCP:<p> -sTCP:LISTEN` empty); `~/.raypoolkit`'s presence recorded. If
`~/ScienceData/.rehearsal-lock` exists, the script prints its owner file and exits 3: the lock is
someone's, and the user is asked.

**Part (a), in process.** In order, each step checked before the next:
1. `acquire("RayPoolKit", "rehearsal-lock 02 proof (a), Python <v> / Ray <v>", "/tmp/ray-rpk02a",
   "in-process")` → 0. Any other result ends the run: 3 is exit 3 (someone else's lock), anything
   else a failure.
2. The pre-start reading; then the driver: this script in its driver mode
   (`ray_proof.py --driver`), which reads its settings, calls `ray.init(address="local",
   _temp_dir="/tmp/ray-rpk02a", num_cpus=2, include_dashboard=False, log_to_driver=False)`, runs
   four remote tasks and creates one actor (as the planner's probe), prints `READY <pid>`, and then
   obeys `shutdown` (`ray.shutdown()`, then `SHUTDOWN`) and `exit` from stdin. It exits by itself
   if it hears nothing for 300 s.
3. **Checkpoint a1, up:** the live and offline listings each equal the witness minus the reaper
   (the one process of the witness whose command names `ray/_private/ray_process_reaper.py`). The
   reaper is alive and not listed; the driver is in neither.
4. `release` → 1, the reason **processes** (the owner's `pid` is still `-`: one reason standing);
   the owner file byte-identical.
5. `set_pid("RayPoolKit", "/tmp/ray-rpk02a", <the driver's pid>)` → 0; only the `pid` line
   changed.
6. **(c)**: `acquire("RayPoolKitSecond", …, "/tmp/ray-rpk02c", "in-process")` at the old location
   → 3, as held; the same with no `lock_dir` → 3, the old location's refusal; the owner file
   byte-identical, and `~/.raypoolkit` as it was before.
7. `release` → 1 (the pid alive, and the processes).
8. `shutdown` → `SHUTDOWN`; **checkpoint a2, shut down:** both listings and the witness minus the
   reaper empty (within the checkpoint's bound). Record whether the reaper is still alive.
   `release` → 1, the reason **the recorded pid** (the driver is alive: one reason standing).
9. `exit`; the driver exits 0 within 30 s; **checkpoint a3, gone:** the witness empty, reaper
   included, and both listings empty. `release` → 0; `status` (fresh interpreter, old location)
   says free.

**Part (b), a cluster.** In order:
1. `acquire("RayPoolKit", "rehearsal-lock 02 proof (b), …", "/tmp/ray-rpk02b", "127.0.0.1:6420")`
   → 0, as (a)1.
2. The pre-start reading; then `<venv>/bin/ray start --head --temp-dir /tmp/ray-rpk02b --port 6420
   --ray-client-server-port 6421 --dashboard-port 8270 --dashboard-agent-listen-port 52370
   --num-cpus 2 --disable-usage-stats` (the clients' form, brief §3), its output to the scratch
   directory. A non-zero exit goes to the stop (step 8) and then ends the run as a failure.
3. **Checkpoint b1, up:** the live and offline listings with `--ray-address 127.0.0.1:6420` each
   equal the witness. The `gcs_server` is the one listed process whose command names
   `gcs_server`. Record each listed process's parent (whether `ray start`'s processes are
   re-parented, and to what).
4. **The client server.** The listings without `--ray-address` equal those with it, less the
   client server (the process whose command contains `ray.util.client.server` and
   `--address=127.0.0.1:6420`) and its descendants. Record whether its command names the temp dir.
   If no client server is running at this end, the check is recorded as **not exercised**, with
   `ray start`'s output, and the run goes on.
5. `release` → 1, the reason processes (`pid: -`, one reason standing). `set_pid` with the
   `gcs_server`'s pid → 0. **(c)** as (a)6. `release` → 1.
6. A driver attached to the cluster (driver mode with `address="127.0.0.1:6420"`, no `_temp_dir`):
   four tasks and one actor, `READY`; **checkpoint b2, with workers:** as b1, the workers and the
   actor now among the listed (each a descendant of the raylet, naming nothing). Then `shutdown`,
   `exit`; the driver exits 0.
7. **Checkpoint b3, before the stop:** as b1. Its live listing, with the address, is **the stop
   list**.
8. **The stop**, as the brief's §3 and never `ray stop`: `SIGTERM` to each pid of the stop list; a
   grace of 15 s; `SIGKILL` to each pid of the stop list still alive. **Nothing outside the stop
   list is ever signalled**, whatever else the script sees. Then **checkpoint b4, stopped:** the
   witness and both listings empty, and the four ports free. If anything of the witness is alive,
   it is printed, the lock is left held, and the run ends with exit 4 (stop and ask).
9. `release` → 0; `status` says free.

**After both parts:** `~/ScienceData/.rehearsal-lock` does not exist, and `~/.raypoolkit` is as it
was before (the default-location acquire of (c) is refused before it creates anything). The
script prints one line per check (`PASS` or `FAIL`, with what it saw) and a summary.

**On a failed check** the script does not go on to the next step of that part. It cleans up only
what it started: the part (a) driver by `exit`, then `SIGTERM` and `SIGKILL` to the driver alone;
the part (b) cluster by step 8's stop. Then it releases the lock through the module, whose own
checks decide. If the module refuses, or anything of the witness is left, it prints the owner file
and what is left, and exits 4: **the lock stays held and the user is asked**. It never removes the
lock directory itself.

**Exit codes:** 0 every check passed; 1 a check failed, and everything was stopped and the lock
released; 2 refused to start (§2.2's preflight), nothing touched; 3 the shared lock is held by
someone else, nothing touched; 4 something could not be cleaned up, and the lock is left held.

### 2.3 The replay, `ray_proof.py --replay <record>`

Reads a `--record` file and, with no Ray and no lock, recomputes each checkpoint's offline listing
from its recorded rows with the module as imported, and checks it against the recorded witness and
the part's expectation exactly as the run did. Exit 0 when every check passes again, 1 otherwise,
printing each. It is how the proof is shown to bite (§3.3) without ever running a broken module
against Ray or the real lock.

---

## 3. Verification

1. **The proof at both ends.** `venv/` and the scratch high-end venv: each exits 0. Record each
   run's whole printed output in the log (it is already cut, §2.2), its duration, and the
   readings before and after: `pgrep`, `~/ScienceData/.rehearsal-lock`, `~/.raypoolkit`.
2. **The replay.** `--replay` of each end's record, unmutated: exit 0.
3. **Deliberate breakage** (README §5 rule 8), **offline only**, by `--replay` of both records with
   01's mutations of the rule applied to the module and reverted after each: **M10** (the
   descendant walk removed) must fail checkpoints a1 and b2; **M12** (the client-server seed
   removed) must fail b1 at each end where the client server ran. M8, M9 and M11 too: record for
   each whether the real records can catch it, and why not where they cannot (01's deviation 21
   says why M9 cannot). The log records the diffs as 01's did (or names 01's, if applied
   unchanged) and the failing checks. **No mutation is ever run against Ray or the real lock.**
4. **The suite** at `venv/`: `Ran 226 tests … OK`, before and after.
5. **`black` 25.1.0**: `black --check raypoolkit docs` passes.
6. **The fixtures against the real lines.** For each role in 01's reconstructed trees (seeds by
   kind, descendants, the reaper, the driver), the real counterpart at each end, and which
   argument of each seed names the temp dir. Where the real trees differ from 01's in a way that
   changes what a test of 01 proves, open an issue: changing 01's tests is not this prompt's.

---

## 4. Acceptance

1. `docs/rehearsal-lock/ray_proof.py` exists and does §2; nothing under `raypoolkit/` changed
   (`git diff --stat` in the log).
2. §3.1–§3.6 hold: the proof exits 0 at both ends, and its replay bites as §3.3 says.
3. The real lock was taken and released by the module at each end, and was free before and after;
   nothing but the stop list was signalled; `ray stop` was never run.
4. **The records**, in the same commit:
   - the log, `logs/02-prove-it-under-real-ray.md`, per README §5.1, with both runs' output,
     §3.3's record and §3.6's comparison;
   - this board: the header, §1's row for 02;
   - `prompts/INDEX.md`: the campaign's line;
   - `docs/OPEN_ISSUES.md`, if the work opens or changes anything.

---

## 5. Stop conditions — stop and ask the user

- At the start: a Ray process is running, the old location exists, or one of the four ports is
  held.
- The proof exits 3 or 4, at any run. The lock is then someone's, or left held; nothing more is
  run until the user says.
- A check fails because of the module (a listing that misses a process the witness finds, a
  refusal that does not happen or one that should not, an owner file changed by a refusal). The
  module is not changed here; the finding goes to the user, who decides whether 01 is reopened.
- Ray behaves differently from README §0.3 in a way the proof cannot tell from a fault, such as a
  witness that never settles.
- Anything would require editing or running SGK, ChamPBH or StochasticInstantons, running
  `ray stop`, signalling a process the stop list does not name, or removing a lock by hand.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `docs/rehearsal-lock/ray_proof.py` (new);
  - the log, this board and `prompts/INDEX.md`;
  - `docs/OPEN_ISSUES.md`, if needed.
- It changes nothing under `raypoolkit/`, adds no test, and does not change 01's fixtures.
- It does not change the version, `README.md`, `PROVENANCE.md` or `CLAUDE.md`, write
  `docs/rehearsal-lock.md`, or tag (03).
- It does not take or touch the new location's lock, and runs no proof at it.
- It pushes nothing.

---

## 7. The log and the board

`logs/02-prove-it-under-real-ray.md`, using README §5.1, with the additions of §4.4.

`IMPLEMENTATION_STATE.md`: the header, and §1's row for 02 (landed, commit, log, suite 226 → 226).
