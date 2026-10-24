# Orchestrator — prompt 02, prove it under real Ray

Read [`../README.md`](../README.md) first: §0.3, §1, §2, §4, §5 (rules 5, 8 and 9 above all) and
§6.2 (U2, U4). Then [`prompt-01.md`](prompt-01.md): its §0 "Conventions", which this note keeps
unless it says otherwise, and its clarifications 3 and 10, which this prompt meets again under
real Ray. Then the board's *Orchestrator review of prompt 01*.

**You do not write code.** You may:
- run the suite, `black`, the agent's script and the commands the log records;
- make venvs of your own in the session scratchpad, as §0's clarification 1 says;
- start Ray **only** by running the agent's script, which takes the shared lock first (README §5
  rule 9), and never with a mutation applied;
- replay the log's deliberate-breakage diffs with `git apply`, offline (`--replay`), and revert
  them;
- read SGK, CPBH and SI through `git -C <client> show <commit>:<path>`, never their working trees;
- fix small residue in a follow-up commit of your own (§4).

You never run `ray stop`, signal a process, or remove a lock by hand. You do not push or tag.

**The prompt:** [`02-prove-it-under-real-ray.md`](../02-prove-it-under-real-ray.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- 01 landed (`6733447`) and was reviewed (`2e561e2`); CI passed at both ends on both (runs
  40031056598 and 40031383762). 02 is written (`3f1620e`, which touches only `prompts/`).
- **The user chose the proof's venvs on 2026-10-24** (clarification 1): `ray[default]` scratch
  venvs at both ends, as recommended.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that it
  could move, and hand the agent the corrections as an addendum.
- No Ray process; neither lock location exists; the four ports are free. One prompt at a time in
  this checkout.

## 0. What makes this prompt unusual

**For the first time in this campaign a prompt starts Ray, holds the real shared lock, and signals
processes.** Three projects use that lock; until the switch-over it is
`~/ScienceData/.rehearsal-lock`, and while the proof holds it, every client's rehearsal refuses to
start. A proof that dies mid-part leaves Ray up and the lock held, and a stop list that over-lists
signals someone else's process. So the review is about three things, in this order:
- **nothing is harmed**: the lock is taken and released by the module at each end, and is free
  before and after; nothing outside the stop list is signalled; `ray stop` is never run; no Ray
  process is left;
- **the witness is independent**: it finds Ray's processes by the venv's `ray` package and Ray's
  titles, never by the temp dir or the address, and it is read at the moments the prompt names;
- **the proof bites**: replayed offline from its own records, it fails under M10 and M12 at both
  ends.

**What moves on purpose:** one new file, `docs/rehearsal-lock/ray_proof.py`; the log
`logs/02-prove-it-under-real-ray.md`; the board, `prompts/INDEX.md`, and `docs/OPEN_ISSUES.md` if
the work opens anything. Nothing under `raypoolkit/`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-24 at `3f1620e`, with
`ray[default]` venvs of its own at both ends; it started no Ray. Pass them on. Each is an
IMPLEMENTATION CHOICE at the orchestrator's direction unless it says otherwise, and the log says
so.

1. **The proof runs in two `ray[default]` scratch venvs, not in `venv/`.** STRUCTURALLY REQUIRED,
   and the user's choice (2026-10-24). The prompt's §2.1 cannot pass as written: `venv/` and the
   high-end venv 01 made carry the minimal `ray`, with no `grpc`, and Ray refuses a client-server
   port without it. `ray start` sets `ray_client_server_port`, and `RayParams` raises
   `ValueError: Ray Client requires pip package ray[client]` (`ray/_private/parameter.py:413-419`
   at 2.43.0; the same check at `:404` at 2.55.1). So part (b) would never start. The clients pin
   the `ray[default]` set (`grpcio`, `aiohttp`, `opencensus` in each `requirements.txt` at the G1
   commits), so their clusters run a client server and a dashboard. Make, in your scratch
   directory:
   ```bash
   uv venv -p /opt/local/bin/python3.12 <scratch>/v243
   uv pip install --python <scratch>/v243/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray[default]==2.43.0" "black==25.1.0"
   uv venv -p /opt/local/bin/python3.13 <scratch>/v255
   uv pip install --python <scratch>/v255/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray[default]==2.55.1" "black==25.1.0"
   ```
   Both parts run at both ends in these. `venv/` is used for the suite (226) and `black` only, and
   nothing is installed into it. Record in the log each venv's `uv pip freeze`, its
   `sys.version`, `ray.__version__`, and `raypoolkit.__file__` (under the repository). The
   extras resolve to versions newer than the clients' (measured: `grpcio` 1.84.1, `aiohttp`
   3.14.5, `opencensus` 0.11.4, `pydantic` 2.14.1, at both ends); record them. If the dashboard
   fails to start at an end (`ray start` does not fail for that by default), record it and go on:
   it is not a fault of the module. The client server **is** expected at both ends now; if it
   does not run at an end, let the run finish as the prompt says ("not exercised"), then stop and
   ask: that is Ray behaving other than measured (prompt §5).
2. **The command that runs the proof names no temp dir, and nothing runs beside it.** The Bash
   tool's shell carries its whole command string in its argv and is an ancestor of the script. If
   it names `/tmp/ray-rpk02a`, `…b` or `…c`, it seeds the walk (01's clarification 3): the driver,
   its sibling's descendant, is then listed, and the offline listing (`self_pid=0`) lists the
   script itself. The same holds for any command of yours alive while the proof runs (a
   `ps | grep`, a `tail` of a Ray log), which would also land in b3's stop list. So: the `--record`
   path names no temp dir; look at the temp dirs only between runs; run nothing else in the
   session while a proof runs. The orchestrator runs nothing naming them while you work.
3. **Run each proof in the background, and never under a tool timeout.** The Bash tool kills a
   foreground command at its timeout, and a proof killed mid-part leaves Ray up and the lock held.
   Run each with `run_in_background`, its stdout and stderr to a scratch file, and wait for it to
   exit; never kill it. If it has not exited after 15 minutes, stop and ask; do not signal it.
4. **The script cleans up after any exception, not only a failed check.** Each part's body is in a
   `try` whose handler treats an unexpected exception as a failed check (prompt §2.2, "On a failed
   check"), so a traceback can never end the script with Ray up or the lock held without the
   cleanup having run. A run that still ends with a traceback, or an exit other than 0, 1 or 2,
   is a stop: nothing is cleaned up by hand.
5. **What the stop signals, narrowed twice.** Neither change lets it signal anything the prompt's
   would not.
   - **A pid is the process recorded at b3, not the number.** Immediately before each `SIGTERM`
     and each `SIGKILL`, the script reads that pid's command (`ps -ww -o command= -p <pid>`) and
     signals only if it equals the command recorded at b3; otherwise it signals nothing and prints
     both. A pid freed in the grace period can be reused by someone else.
   - **On a failed check in part (b)**, where b3 has not passed, the stop list is the latest live
     listing **intersected with** the latest witness; a pid in only one of them is printed and not
     signalled. Where b3 passed, the two are equal, and this is the prompt's stop list.
   Never `os.killpg`, never a pid of 1 or less, never the script's own process or an ancestor of
   it (asserted before signalling).
6. **Before anything starts, two more refusals** (exit 2, touching nothing): any `RAY_*` variable
   in the script's environment other than its own `RAY_USAGE_STATS_ENABLED`, printed by name
   (`RAY_ADDRESS` would redirect a driver; `RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER` would move the node
   off the loopback, clarification 7); and a scratch directory or `--record` path that names a temp
   dir. `RAY_USAGE_STATS_ENABLED=0` is set in `os.environ` before `raypoolkit` is imported, as
   `ray_smoke_run.py` does, so that every child inherits it.
7. **The client server's address is `127.0.0.1:6420`.** On macOS Ray takes the loopback as the
   node's address unless `RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER` is set (`get_node_ip_address` in
   `ray/_private/services.py`; at 2.55.1 through `get_localhost_ip()`, IPv4 first), and starts the
   client server as `<python> -m ray.util.client.server --address=<GCS address> --host=…
   --port=6421 --mode=proxy …`. CPBH's script says the same of a real cluster
   (`ray_cluster.sh:161-164` at `807f175`). If the client server's `--address` is anything else,
   b1 fails on a fact about Ray, not the module: let the run clean up, then stop and ask. The
   record keeps its whole command.
8. **`ray` is loaded in every mode.** `import raypoolkit.rehearsal_lock` imports the package root,
   which imports `RayWorkPool` and so `ray` (U3); importing it starts nothing. The script's own
   `import ray` stays in driver mode, and the log says that `ray` is loaded in every mode. The
   prompt's "it imports `ray` only in its driver mode" is read so.
9. **The witness's venv directory** is the scratch venv's `site-packages/ray/`, which lives under
   the scratchpad (`/private/tmp/…`, also spelled `/tmp/…`). Match it as written, as
   `os.path.realpath` gives it, and without a leading `/private`, and invoke each venv's
   interpreter by one absolute path, the same in every run. The witness never uses the temp dir or
   the address.
10. **Develop offline first.** Every run against Ray takes the real lock, and a crashed run is a
    stop. Before the first real run: check the witness and the checkpoint logic on a `ps` reading
    of the idle machine, and `--replay` on a record you build by hand. Then one real run at the low
    end; then the high end. Every real run is the whole script; nothing starts Ray outside it. Each
    run's output, exit status and readings before and after go in the log, the failed ones too.
11. **The replay never reaches a lock.** Run every `--replay`, mutated or not, with `HOME` set to an
    empty scratch directory, and check that it is still empty afterwards. The breakage follows 01's
    conventions: diffs that `git apply` replays on `6733447`'s module, each checked and reverted,
    the SHA-256 of every changed file and `git status --porcelain --untracked-files=all` equal
    before and after each item. 01's `m08`–`m12` diffs are in its log (§4); name them if applied
    unchanged.
12. **Ray's session directories stay.** After the runs, `/tmp/ray-rpk02a` and `/tmp/ray-rpk02b`
    hold Ray's session directories; the script and the agent delete nothing there, and the log
    records that they exist. A later run uses the same temp dirs: the pre-flight asks that no
    process names them, not that they are absent. `/tmp/ray`, `/tmp/ray-rpkp` (the planner's
    probe), `/tmp/ray-cpbh`, `/tmp/ray-si`, `/tmp/ray-decoy` and `/tmp/ray-cpbh-decoy` exist and
    are not touched.
13. **The board and the README.** The agent updates the board's header and 02's row, and
    `prompts/INDEX.md`. It records clarification 1 in its log as a deviation, STRUCTURALLY
    REQUIRED, the user's choice of 2026-10-24. README §2's status for 02 is the review's.

**The facts, checked by the orchestrator on 2026-10-24.** Pass them on.

- **The tree.** Branch `main`, `HEAD` `3f1620e` before this note, clean; this checkout is the only
  worktree. `origin/main` is `2e561e2`; local `main` is one commit ahead (`3f1620e`), and this note
  makes two. Tags `v0.1.0` and `v0.2.0`. `docs/rehearsal-lock/` does not exist.
- **The baseline.** `venv/`: `Ran 226 tests … OK` (1.9 s). `./venv/bin/black --check raypoolkit
  docs`: 19 files unchanged.
- **The machine.** No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` exit 1). Ports 6420,
  6421, 8270 and 52370 have no listener. No process names `ray-rpk02` but the orchestrator's own
  `grep`; no `/tmp/ray-rpk02*` exists. No `RAY_*` variable in the orchestrator's environment.
- **The real `HOME`.** `~/ScienceData` is a directory; `~/ScienceData/.rehearsal-lock` and
  `~/.raypoolkit` do not exist.
- **`venv/`'s Ray is minimal**: `ray==2.43.0` with none of `grpc`, `aiohttp`, `opencensus`,
  `prometheus_client`, `pydantic`, `smart_open`.
- **The `ray[default]` venvs resolve** at both ends (the orchestrator's, without the editable
  install: 53 packages at 3.12.15 / 2.43.0, 57 at 3.13.16 / 2.55.1). `ray start --help` lists
  `--temp-dir`, `--ray-client-server-port`, `--dashboard-port`, `--dashboard-agent-listen-port`,
  `--disable-usage-stats`, `--num-cpus` and `--node-ip-address` at both. `uv` is
  `/opt/local/bin/uv`; `/opt/local/bin/python3.12` and `python3.13` exist.
- **The clients' cluster.** CPBH's `ray start` (`ray_cluster.sh:308-310` at `807f175`) is the
  prompt's form with its own ports and ten CPUs. Its stop lists again after the grace period and
  kills anything newly listed; the prompt's kills only what is still alive of the stop list.
  Follow the prompt.
- **The module** (`6733447`): `ray_processes(ray_temp_dir, ray_address=None, *, ps_text=None,
  self_pid=None)`; `old_lock_dir()`; `acquire`'s old-location refusal does not apply when the lock
  being acquired is the old location (`rehearsal_lock.py:435-436`), and it comes before any
  `mkdir`, so (c)'s default-location acquire creates nothing.
- **Expected counts.** The suite is **226** before and after. The index is **0** now, and 0 after
  unless the work opens something.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §6 files changed; nothing under `raypoolkit/`; nothing pushed
  or tagged.
- **(E2) Safety.** The lock was taken and released by the module at each run, and is free before
  and after; `~/.raypoolkit` never appeared; nothing but the stop list was signalled, each pid
  checked against its command; `ray stop` never run; no Ray process left.
- **(E3) The witness.** Independent of the rule, read at the prompt's checkpoints, settled.
- **(E4) The proof passes** at both ends, run by the agent and again by the orchestrator.
- **(E5) The proof bites.** M10 and M12 fail their checkpoints at both ends by `--replay`; M8, M9
  and M11 are recorded with the reason they can or cannot be caught.
- **(E6) The records.** The log with the prompt's §4.4 additions, §3.6's comparison, the board,
  `prompts/INDEX.md`, the index.

**Conventions.** 01's (its note, §0's last list) bind the agent, with these changes and additions:
- "start no Ray" becomes: start Ray only by running the whole script, at the times clarification
  10 says, and never with a mutation applied;
- never run `ray stop`, `kill` or `pkill`, and never remove `~/ScienceData/.rehearsal-lock`,
  `~/.raypoolkit` or anything under `/tmp/ray*`;
- a run that exits 3 or 4, or ends any other way than 0, 1 or 2, is a stop: report the owner file
  and `pgrep -lf 'gcs_server|raylet|ray::'` (pids and first words only) and wait;
- the record files stay in scratch and are never committed.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` are
   empty; `git worktree list` shows this checkout alone.
2. **The baseline.** 226, OK; `black --check` clean.
3. **The machine.** `pgrep`, the four ports, the real `HOME`, the `RAY_*` environment: as §0.
4. **Tell the user** that the agent's runs hold the shared lock at the old location for a few
   minutes each, so a client's rehearsal started meanwhile refuses with exit 3; and that macOS may
   ask whether Python may accept incoming connections when the cluster starts, which is theirs to
   answer.
5. **Scratch.** Make the agent's subdirectory of the session scratchpad, empty, and give it the
   path; keep your own measurements in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md` and `CLAUDE.md`;
- `HEAD`, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in its scratch directory.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's thirteen clarifications. Clarification 1 changes where
the proof runs; 2–5 keep the real lock and other people's processes safe; 7 is the one fact about
Ray the client-server check rests on.

Tell it plainly:
- **One commit, at the end**, with the log `logs/02-prove-it-under-real-ray.md` in README §5.1's
  form and the prompt's §4.4 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else.** Nothing under
  `raypoolkit/`; not `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `pyproject.toml`, `.github/`, the
  campaign README, or anything under `orchestrator/` or `planning/`.
- **It pushes nothing and tags nothing.**
- **It edits no client repository and runs none of their code.**
- **It starts Ray only by running its script**, under the lock, and never runs `ray stop`, signals
  a process outside its script's stop list, or removes a lock.
- **Stop and ask** on any of the prompt's §5 conditions, and on clarifications 1, 3, 4 and 7's.

While it works, run nothing that names a temp dir (clarification 2), and start no Ray.

## 3. The review — nine checks

1. **E1, scope.** `git show --stat <commit>` lists only the prompt's §6 files. `git diff 3f1620e
   <commit> -- raypoolkit pyproject.toml README.md PROVENANCE.md CLAUDE.md .github
   prompts/rehearsal-lock/README.md` is empty. `git tag` and `git ls-remote origin` unchanged.
2. **E2, the machine after the agent.** No Ray process; the four ports free; neither lock location
   exists; `/tmp/ray-rpk02a` and `…b` exist, `…c` does not.
3. **The script, by reading.** Read it whole against the prompt's §2.2–§2.3 and §0's
   clarifications: the environment before `raypoolkit` is imported; the pre-flight and its exit
   codes; every lock call in a fresh `-I` interpreter from an empty directory, `lock_dir=
   old_lock_dir()` but for (c)'s default-location call; no temp dir in the script's or the
   driver's argv; the witness built from the venv's `ray` directory, `ray.util.client.server` and
   `ray::` alone, minus the script and its children; each checkpoint's settling loop and bound;
   the stop: SIGTERM, 15 s, SIGKILL, each pid checked against its b3 command, nothing else
   signalled, no `ray stop` anywhere (`grep -n '"stop"\|ray stop\|killpg\|pkill'`); the
   exception handling of clarification 4; the exit codes; the record's contents; it names no
   client.
4. **E4, the proof, by running.** In your own `ray[default]` venvs at both ends (yours, made as
   clarification 1 says, with the editable install), from a command naming no temp dir, in the
   background: exit 0 at each end, every check `PASS`. Readings before and after: no Ray, the lock
   free, `~/.raypoolkit` absent. Compare the checkpoints' listings with the log's by role (the
   pids differ).
5. **E5, the breakage, by replaying.** Extract M10 and M12 (and M8, M9, M11) from the log, and
   replay each against **your own** records with `HOME` an empty scratch directory: M10 fails a1
   and b2, M12 fails b1, at each end; M8, M9 and M11 as the log says. Then the agent's records:
   the same. `git status` clean after each.
6. **E3, the witness, by reading the records.** For one end, from the record: every pid of the
   witness at a1 and b1 is a `ray` process, a `ray::` process or a descendant of one; the reaper is
   in the witness and not in either listing; the client server is in the witness, and in the
   listing with the address only.
7. **The suite and `black`.** `venv/`: `Ran 226 tests … OK`. `./venv/bin/black --check raypoolkit
   docs`: 20 files unchanged.
8. **§3.6, the fixtures against the real lines.** The log names, for each role of 01's
   reconstructed trees, its real counterpart at each end and the argument that names the temp dir;
   any difference that changes what a test of 01 proves is opened as an issue, and none of 01's
   tests changed.
9. **E6, the records.** The log has every section of README §5.1 and the prompt's §4.4 additions;
   clarification 1 recorded as STRUCTURALLY REQUIRED; both venvs' freezes; each run's output,
   duration and readings. The board's header and 02's row; `prompts/INDEX.md`'s line; the index
   counted, matching its header.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02* paragraph, in the form of
  01's, with the user's choice of venvs (clarification 1) stated. Fix small residue in a follow-up
  commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 02, and its header;
  - the notes line on the board, with this note marked "used for 02".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Put the push to the user, and do none of it unasked.** CI has not run `black` over the new
  script. *Recommended:* push `main` as it stands after the follow-up, so that CI runs on it.
- **Report to the user:**
  - what landed: the proof script; the suite 226 → 226; nothing under `raypoolkit/` changed;
  - the proof at both ends: its time, the lock taken and released, no process left, the stop list
    and what it held, the client server found by its address;
  - the breakage replayed, and what M8, M9 and M11 can and cannot show on real records;
  - where the real process trees differ from 01's reconstructions, and anything opened;
  - the push, as a decision for them;
  - that 03 (the release `v0.3.0`) can now be written, against the tree 02 left.
