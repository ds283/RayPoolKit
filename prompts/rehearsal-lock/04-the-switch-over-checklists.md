# Prompt 04 — the switch-over checklists

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- **`v0.3.0`** is tagged on `67a75b9` after green CI (run 40121254667), and its release is recorded
  (`2c518ee`, CI run 40122144103 green).
- G1 holds for 04 (§0.1).
- `git status` is clean in this repository, and the suite gives `Ran 226 tests … OK`.

**Closes:** nothing. **Narrows:** nothing. **Opens:** one issue, for 05 (§2.5), and anything else
the work finds.

**Recommended model:** **Opus.** There is no code. The work is four documents that three other
repositories will act on, on one day. Each fact has to be true of a client at a named commit and of
`v0.3.0`, and has to be read, not inferred.

**Read first:**
1. [`README.md`](README.md): §0, §1, §4, §5 (rules 5, 9) and §6 (D2, D3, U1, U2, U4), and §7 (G1,
   G2).
2. The contract, [`../../docs/rehearsal-lock.md`](../../docs/rehearsal-lock.md), whole. Every
   command a checklist gives must agree with it.
3. The board: the reviews of 02, 03 and 03a, and *Release of `v0.3.0`*.
4. The precedent for the form: `prompts/extraction/06-the-adoption-checklists.md` §2.3, and
   `docs/adoption/secondarygwkit.md`. Take the form, not the content.
5. The clients, read **only** through `git -C <client> show <commit>:<path>` and `git -C <client>
   grep … <commit>`, at the commits of §0.1:
   - SGK `tools/rehearsal_lock.py`, `CLAUDE.md`, `RunDrivers/quadsource_atol_sweep.py`,
     `RunDrivers/scoped_pipeline_run.py`, `main.py`, the six `extract_*.py`, and
     `ComputeTargets/tests/test_ray_address_default.py`;
   - CPBH's and SI's `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` and `CLAUDE.md`.

Facts below are at this repository's `74c3d3f` and at the client commits of §0.1, measured
read-only by the planner on 2026-10-24.

---

## 0. What the planner measured

### 0.1 The clients

| Client | Commit (branch) | Tree | Lock code | Ray | Pin |
|---|---|---|---|---|---|
| SGK | `216e44d` (`handover-remedial`; `main` is its ancestor) | clean | `tools/rehearsal_lock.py` blob `ea14336`, its tests `cdeecd6` | `ray==2.43.0` with `grpcio`, `aiohttp`, `opencensus` | `v0.2.0` |
| CPBH | `807f175` (`jordan-normalization`; `main` an ancestor) | clean | `ray_cluster.sh` blob `eaae1e7` (400 lines) | `ray==2.53.0`, the same extras | `v0.2.0` |
| SI | `7071bb8` (`rrk-adoption`; `main` `1c223e8` an ancestor) | clean | `ray_cluster.sh` blob `6c8eada` (398 lines), the same at `main` | `ray==2.55.1`, the same extras | `v0.2.0` |

G1 holds: each lock file is the blob §0.2 of the campaign README measured. Each client's
`ray_cluster.sh` path is `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh`. The clients
pin the `ray[default]` set, so an in-process instance starts a headless dashboard on 8265 (02's log
§5). A checklist names the commit it was measured at; the client re-measures before it acts.

### 0.2 SGK

- **Its lock** is `tools/rehearsal_lock.py` (project fixed as `SecondaryGWKit`, `ray_temp_dir` and
  `ray_address` both `in-process`, `:49-50`, `:92-104`). Its command line is `acquire --purpose
  TEXT`, `set-pid PID`, `release`, `status` and `ray-processes`, run as `PYTHONPATH=.
  ./venv/bin/python -m tools.rehearsal_lock …`. Its rule finds Ray processes by this checkout's
  venv (`venv_roots`, `:184`). No tracked code outside `tools/`, `docs/` and `prompts/` calls it.
  The callers are people and agents, following `CLAUDE.md`, and campaign scripts under `docs/`
  that are records.
- **`CLAUDE.md`**:
  - "The shared rehearsal lock" (`:149-162`) gives the location, the `acquire`/`set-pid`/`release`
    commands and the brief at `d6d550b`;
  - the hard-kill route (`:137-142`) checks `tools.rehearsal_lock ray-processes` for a `SIGKILL`ed
    driver's GCS server.
- **Its Ray starts.** Each of these starts an in-process instance with `address="local"` and no
  `_temp_dir`:
  - `RunDrivers/quadsource_atol_sweep.py:629-634` and `RunDrivers/scoped_pipeline_run.py:709-714`
    each wrap `ray.init` with `_real_ray_init(address="local", num_cpus=…,
    include_dashboard=False, ignore_reinit_error=True)`;
  - `main.py:314` and the six readers (`extract_GkSource_data.py:118`, `extract_GkWKB_data.py:110`,
    `extract_Gk_data.py:109`, `extract_QuadSourceIntegral_data.py:130`, `extract_TkWKB_data.py:106`,
    `extract_tensor_source_data.py:110`) call `ray.init(address=args.ray_address)`, whose
    `--ray-address` defaults to `local`; `auto` or a `host:port` attaches to a cluster.

  `ComputeTargets/tests/test_ray_address_default.py` pins that each of the seven has exactly one
  `ray.init`, whose `address` is `args.ray_address`, and that the default is `local`.
- **Its tests.** `tools/tests/test_rehearsal_lock.py` holds 42 tests. Deleting it lowers SGK's count
  by 42, which SGK's own rules treat as a stop unless explained.

### 0.3 CPBH and SI

The two scripts differ only in names, ports, the default CPU count and their header comments
(`diff` at the commits). Each holds the lock and the cluster together. In CPBH's (SI's line
numbers differ by one or two; measure them):
- **the lock:** `LOCK_PROJECT`, `LOCK_PARENT`, `LOCK_DIR`, `OWNER_FILE` (`:66`, `:77-79`); `iso_now`,
  `owner_field`, `write_owner`, `print_owner` (`:86-116`); `acquire_lock` (`:118-129`);
  `release_lock` (`:131-148`);
- **the cluster:** `temp_dir_regex` and `list_cluster_pids` (`:152-189`, the rule the module was
  modelled on, with its `ray_cluster.sh` exclusion); `describe_pid`, `port_listeners`, `alive`,
  `stop_cluster` (`:191-263`);
- **the commands:**
  - `cmd_start` (`:267-338`): `acquire_lock`; a stale-cluster check by `list_cluster_pids` (exit 4,
    the lock released); a check of the four ports (exit 4, released); `ray start --head --temp-dir
    /tmp/ray-cpbh` on the fixed ports; the `gcs_server`'s pid found and written with `write_owner`;
    an `INT`/`TERM` trap that stops the cluster and calls `release_lock`;
  - `cmd_stop` (`:340-356`): refuses if the lock is another project's, judged by `owner_field`; then
    `stop_cluster` and `release_lock`;
  - `cmd_status` (`:358-385`): the lock half (`:359-370`), then the cluster's processes and ports.
- Owner values: CPBH `ChamPBH`, `/tmp/ray-cpbh`, `127.0.0.1:6380`; SI `StochasticInstantons`,
  `/tmp/ray-si`, `127.0.0.1:6390`.
- **Other live lines.**
  - CPBH: `CLAUDE.md:128-134` ("Ray on this machine"); `config/argument_parser.py:341` and
    `ComputeTargets/tests/test_ray_address.py:47` name `ray_cluster.sh`, not the lock, and stay
    true.
  - SI: `CLAUDE.md:14-20`, which cites the brief.
  - Everything else naming the lock is under `.documents/`, `.prompts/`, `prompts/` or
    `science-runs/`, campaign and run records. CPBH has about 890 such lines, SI about 800.

### 0.4 Ray, when `_temp_dir` is given with a cluster address

Read from Ray's source at 2.43.0 (`venv/`) and 2.55.1. **This prompt starts no Ray** (README §5
rule 9).
- `ray.init` accepts `_temp_dir` with any address, and raises nothing for it
  (`ray/_private/worker.py:1487` at 2.43.0, `:1645` at 2.55.1).
- With `auto`, the address is looked up with that temp dir: `canonicalize_bootstrap_address(address,
  _temp_dir)` (`worker.py:1651` / `:1811`) calls `get_ray_address_from_environment(addr,
  temp_dir)` (`services.py:389` / `:408`), so `<_temp_dir>/ray_current_cluster` is read in place
  of `/tmp/ray/ray_current_cluster`.
- With a `host:port`, the driver connects as a connect-only node with `temp_dir=_temp_dir`
  (`worker.py:1791` / `:1960`). That node takes the given temp dir as its own, in place of the
  head's (`node.py:442-462` at 2.43.0, `:533-547` at 2.55.1), and makes it if missing.
- So `_temp_dir` is safe only with `local`. With a cluster it splits the driver's files from the
  cluster's, and with `auto` it can change which cluster is found. This bears out U2's caveat. Each
  checklist that starts Ray in process says so.

### 0.5 What the module asks, in the clients' terms

From the contract:
- one temp dir per instance, spelled the same every time, short, with no leading `//`;
- `set-pid` with the driver's pid, or the `gcs_server`'s;
- the commands run as the command line, never through the Python API inside a Ray driver;
- no command line of the script's own, including a `PURPOSE`, naming the temp dir (§6);
- `acquire` does the stale-process check itself (exit 4, released again).

---

## 1. What is wanted

04 writes **`docs/adoption/rehearsal-lock/`**: one checklist per client and `switch-over.md`, the
procedure for the day. After it, each client can plan its switch from its checklist in a campaign of
its own, and the user can run the day from `switch-over.md`.

- **A checklist is data, not instructions.** It describes the client at its commit. Where a choice
  is the client's, it names the options and what each touches; a recommendation is marked
  **Advice:**.
- **Every client fact carries a `path:line`** at the client's commit; every statement about the lock
  cites the contract's section.
- **Nothing in this repository's code changes.** No file under `raypoolkit/`; the suite stays at
  **226**. No client is edited, imported or run.

---

## 2. What to write

### 2.1 The three checklists

`docs/adoption/rehearsal-lock/secondarygwkit.md`, `champbh.md` and `stochasticinstantons.md`. Each
opens with the client, its commit (full SHA, branch, date, subject) and its tree's state. Then the
**same eight items, in the same order and under the same names**:

1. **The pin.** `v0.2.0` → `v0.3.0`, the line as it will read. Moving the pin alone changes nothing
   (`RayWorkPool` is unchanged). The switch is the use of the module, made on the day (§2.2).
2. **What it removes**, by `path:line`.
   - SGK: `tools/rehearsal_lock.py` and its tests, with their blobs and the 42 tests.
   - CPBH and SI: the lock half of `ray_cluster.sh` (§0.3), and not the cluster half (D4).
3. **What replaces it**: every command, written out with the client's own values, as the client
   will run it (`./venv/bin/python -m raypoolkit.rehearsal_lock …`), and what each exit code means
   there.
   - **CPBH and SI.** `cmd_start` as `acquire` (its 3 and 4 kept as the script's exits), the port
     check followed by `release` on a held port, `ray start`, then `set-pid` with the
     `gcs_server`'s pid. The trap calls `release`. `cmd_stop` runs `stop_cluster`, then `release`.
     `cmd_status` runs the module's `status --ray-temp-dir … --ray-address …`, then keeps its own
     port lines.
     - `cmd_stop`'s first check, "is the lock another project's", has no command of its own in the
       module. Name the options: read the owner file at the new location (the owner format is a
       contract, §4); drop the check and rely on `release`'s refusal after the stop; or parse
       `status`. Say what each costs. **Advice:** the agent's, with its reason.
     - Say which of the script's messages and exit codes change, for a person or a script that
       reads them. Check, by `git grep`, whether anything in the client reads `cmd_status`'s
       lines.
   - **SGK.** The commands of `CLAUDE.md` with `--project SecondaryGWKit --ray-temp-dir <dir>
     --ray-address in-process`. **Advice:** `/tmp/ray-sgk` (U2); check that no file or process on
     the machine names it.
4. **Its Ray starts.** Every place the client starts Ray that runs under the lock, and what it needs.
   - SGK: the two wrappers and the seven `ray.init` calls of §0.2. Each in-process start gains
     `_temp_dir=<dir>`, and the seven only when `args.ray_address == "local"` (§0.4). Name the
     forms that keep `test_ray_address_default.py` passing.
   - CPBH and SI: `ray start --temp-dir` already gives the cluster its own temp dir, and the
     drivers connect by address. Say whether anything changes.
5. **What it must now do differently**, each with the contract's section:
   - the rule finds the instance by its temp dir, not by SGK's venv. So an SGK Ray process started
     without the temp dir is not seen. That includes one left from before the switch, and the
     hard-kill route's check (`CLAUDE.md:137-142`) depends on it;
   - the module's rule replaces the script's for the lock, while the script's own rule still drives
     `stop_cluster`. Where the two differ (the `ray_cluster.sh` exclusion, ancestors seeding the
     walk, the client server's host), say what each difference means here;
   - a `PURPOSE`, or any command line of the script's own, must not name the temp dir;
   - `status`'s layout is the module's (contract §8), and differs from the script's;
   - SGK: the in-process dashboard on 8265 (02), which is not the lock's to check.
6. **Its tests.** Which of the client's tests touch the lock, and what each needs: SGK's 42, deleted,
   and the count that falls; `test_ray_address_default.py`; CPBH's `test_ray_address.py:47`; any
   others the grep finds.
7. **What goes stale.** Each live line that names the old location, the old helper or the brief, by
   `path:line` with what it says and what it becomes. The records are counted by directory and not
   rewritten.
8. **Its acceptance.**
   - The pin reads `v0.3.0`.
   - `git grep -n -E 'ScienceData/\.rehearsal-lock|tools\.rehearsal_lock|rehearsal_lock\.py'
     <commit> -- <live paths>` finds nothing. Give the exact command and today's count.
   - The client's own suites pass, with any fall in count explained.
   - On the day, the checks of `switch-over.md` §3 pass.

### 2.2 `docs/adoption/rehearsal-lock/switch-over.md`

The procedure for the day (D3):
1. **The parties.** The three clients, each with its checklist and commit. Also **this
   repository's proof**, `docs/rehearsal-lock/ray_proof.py`, which takes the lock at
   `old_lock_dir()` and so must move too, by a later prompt here (§2.5).
2. **Before the day.** Each client has its switch ready on a branch, measured against its
   checklist, its suites passing, and not merged. Then, at the start of the day:
   - no Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` finds nothing);
   - neither lock location exists;
   - nothing is running in any client.
3. **The day.**
   - **The order.** While no project runs Ray, the order the switches land in does not matter.
     Say why: a switched client refuses while the old location exists (U4), and nobody holds
     either lock.
   - **After all three have landed**, these checks, each in its own repository with its own venv:
     - `status`: the lock free, no old location;
     - one client `acquire`s; each of the other two `acquire`s and gets 3; the first `release`s
       and gets 0. Give the exact commands. They start no Ray: `acquire` and `release` with nothing
       running are safe.
   - Then G2 is recorded on this board.
4. **If a client cannot switch that day.** A switched client cannot see a lock taken at the old
   location by one that has not switched, unless the old location exists (U4); and the unswitched
   one cannot see the new lock at all. Name the options and what each risks: no Ray in any
   project until the last one lands; or the switched clients revert. **Advice:** the agent's.
5. **Afterwards.**
   - A later release drops U4's refusal once G2 holds (README §8).
   - Phase 2, the cluster, waits for G2.

### 2.3 Check every statement by running it

For each checklist's commands, write a script in your scratch directory, with the client's values
held in variables inside it (contract §6: no command line of its own names the temp dir). Run it
with `HOME` set to a scratch directory and `venv/`'s interpreter, starting no Ray:
- `acquire`, `status`, `set-pid` with a live pid of the script's, `release` refused while that pid
  lives, then `release` once it is gone;
- the port-refusal path's `release` with nothing recorded;
- `switch-over.md` §3's cross-check with all three projects' values.

Record each script, its output and each exit code in the log. A command whose exit code differs
from what a checklist says is a stop.

### 2.4 Read every `path:line`

Quote each in the log, with the text read at the client's commit.

### 2.5 The issue for 05

Open `[04-the-proof-takes-the-old-lock]` on the board's §3 and in the index, assigned to 05.
`docs/rehearsal-lock/ray_proof.py` passes `lock_dir=old_lock_dir()` (02's log §5). After the
switch-over a re-run would hold a lock that no project looks at. 05, which re-runs the proof, must
move it to the default location first, or say why not.

---

## 3. Verification

1. **The suite**, `venv/`: `Ran 226 tests … OK`, before and after. `./venv/bin/black --check
   raypoolkit docs`: 20 files unchanged.
2. **The clients are untouched.** Before and after, for each: `git -C <client> rev-parse HEAD`,
   `git -C <client> status --porcelain | shasum`, `git -C <client> stash list | wc -l`, each equal.
   No client's venv is used.
3. **§2.3's transcripts** pass, with `HOME` a scratch directory that is checked afterwards.
4. **§0.4 re-read** at both Ray versions, from the source files only (a minimal `ray==2.55.1`
   scratch venv is enough for the high end), with the lines quoted.
5. **Links.** Every relative link in `docs/adoption/rehearsal-lock/` resolves to a tracked file.
6. **The real `HOME` and Ray.** Neither lock location exists, before or after; `pgrep` finds
   nothing.

**Deliberate breakage.** There is no code to break. §2.3's transcripts are the check: each shows the
exit code a checklist states.

---

## 4. Acceptance

1. `docs/adoption/rehearsal-lock/` holds the three checklists and `switch-over.md`, as §2 says, and
   nothing else.
2. Every client fact was read at its commit, and every command was run as §2.3 says.
3. §3 passes.
4. **The records**, in the same commit:
   - the log, `logs/04-the-switch-over-checklists.md`, per README §5.1, with each client's
     untouched-check, the transcripts, the quoted lines and the test count (226, 226);
   - the board: the header; §1's row for 04 (landed, "this commit", 226 → 226); §2's G2 row pointing
     at `switch-over.md`; §3 with the issue of §2.5;
   - `docs/OPEN_ISSUES.md`, with that issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- A client's `HEAD` or lock blob is not §0.1's, and you cannot tell which to measure.
- A command a checklist must give does not behave as the contract says (§2.3).
- The suite fails, or its count differs from 226.
- Anything would edit, run or import a client, use a client's venv, start Ray, touch either lock
  location under the real `HOME`, push, or tag.
- Passing anything would need a change to a file not in §6.

---

## 6. What this prompt does not do

- **Files it adds or changes:**
  - `docs/adoption/rehearsal-lock/` (new): `secondarygwkit.md`, `champbh.md`,
    `stochasticinstantons.md` and `switch-over.md`;
  - the log, the board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- It changes nothing else:
  - no file under `raypoolkit/` or `docs/rehearsal-lock/`;
  - not `docs/rehearsal-lock.md` or `docs/adoption/`'s existing files;
  - not `README.md`, `PROVENANCE.md`, `CLAUDE.md` or the campaign README.
- It edits no client, and tells no client of the switch: each learns of it from its checklist.
- It moves no proof to the new location (§2.5 is 05's).
- It makes no tag and pushes nothing.
