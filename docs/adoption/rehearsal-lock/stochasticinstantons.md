# Switch-over checklist: StochasticInstantons (SI)

- **Client:** StochasticInstantons, `/Users/ds283/Documents/Code/StochasticInstantons`, at
  **`7071bb8`** (`7071bb8452252245ca65b3161681c1a634733878`, branch `rrk-adoption`, 2026-10-23, "Add
  the run registry's config, rules, discovery hook and config test (rrk-adoption prompt 01,
  C2-C5)"). SI's `main` (`1c223e8`) is its ancestor, with the same `ray_cluster.sh` (blob
  `6c8eada`).
- **Tree:** clean at the start and at the end of the measurement (`git status --porcelain` empty,
  no stash).
- **Package:** `raypoolkit` at **`v0.3.0`** (`67a75b9`). Its contract is
  [`docs/rehearsal-lock.md`](../../rehearsal-lock.md), written "contract §N" below.
- **How it was measured:** read-only, by RayPoolKit's rehearsal-lock prompt 04 on 2026-10-24,
  through `git show` and `git grep` only. Nothing of SI was imported, run or opened. Every command
  in item 3 was run against a scratch `HOME`, with RayPoolKit's own venv (Python 3.12.15, Ray
  2.43.0), starting no Ray; the transcripts are in
  [04's log](../../../prompts/rehearsal-lock/logs/04-the-switch-over-checklists.md) §3. **SI's own
  campaign measures again before acting, and its numbers govern.**
- **This is data, not instructions.** It describes SI at `7071bb8`. SI decides what to do, under
  its own `CLAUDE.md`. Where a choice is SI's, it is named as SI's; a recommendation is marked
  **Advice:**.

Unless another commit is named, a `path:line` is SI's at `7071bb8`, and **"the script"** is
`.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` (blob `6c8eada1cd412a9b4abf462f45adcfa409e974fe`,
398 lines, last changed `8e04a7c`, 2026-10-12). It sits under `.documents/`, among records, but it
is live: `CLAUDE.md:16-18` runs every rehearsal and long build through it.

**In one paragraph.** SI's lock is the lock half of the script, which also starts and stops SI's
isolated cluster; ChamPBH's script was adapted from it, and the two differ only in names, ports,
the default CPU count (4 here, 10 there) and their comments. Under `v0.3.0` the lock half goes, and
the script calls `raypoolkit.rehearsal_lock` with `--project StochasticInstantons --ray-temp-dir
/tmp/ray-si --ray-address 127.0.0.1:6390`; the cluster half stays (decision D4). No Ray start
changes. What changes is in the script's paths: `release` now also refuses while anything of the
cluster is alive, so where `stop_cluster` leaves something running, the lock now stays held where
today it is removed (item 3).

---

## 1. The pin

`requirements.txt:59` reads, today:

```text
raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
```

and becomes:

```text
raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.3.0
```

- SI keeps `ray==2.55.1` (`:58`), the package's tested high end, at which the module was proven
  under real Ray (02's log). `python -m raypoolkit.rehearsal_lock` imports Ray through the package
  root (contract §2), a few tenths of a second a call.
- **Moving the pin alone changes nothing.** `RayWorkPool`, its arguments and its printed lines are
  `v0.2.0`'s ([Changes in `v0.3.0`](../../../README.md#changes-in-v030)). The switch is the use of
  the module, made on the day, with the other two clients ([`switch-over.md`](switch-over.md)).
- `CLAUDE.md:142-143` names the pin, "`raypoolkit` `v0.2.0`"; it goes with the pin (item 7).

## 2. What it removes

The **lock half** of the script, and not the cluster half (D4):

| Lines | What |
|---|---|
| `:75-78` | `LOCK_PARENT="$HOME/ScienceData"`, `LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"`, `OWNER_FILE` |
| `:85-88` | `iso_now` |
| `:90-94` | `owner_field` |
| `:96-107` | `write_owner` (the seven keys, `owner.tmp` renamed) |
| `:109-115` | `print_owner` |
| `:117-128` | `acquire_lock` (`mkdir -p` of the parent, then `mkdir` of the lock; 3 when held) |
| `:130-147` | `release_lock` (identity only: the owner's `project` and `ray_temp_dir`) |
| in `cmd_start`, `:278`, `:284`, `:299`, `:303`, `:313`, `:325`, `:329` | the calls of `acquire_lock`, `release_lock` and `write_owner` |
| in `cmd_stop`, `:340-349`, `:351` | the owner check and `release_lock` |
| in `cmd_status`, `:357-368` | the lock's lines |

**What stays:** `LOCK_PROJECT` and the cluster's values (`:65-73`), `say` and `err` (`:82-83`),
`temp_dir_regex` and `list_cluster_pids` (`:151-188`), `describe_pid`, `port_listeners`, `alive`
and `stop_cluster` (`:190-261`), the commands' cluster steps, and `main` (`:385-393`).
`owner_field` and `print_owner` may stay in another form if SI keeps `cmd_stop`'s first check by
reading the owner file (item 3).

## 3. What replaces it

The commands, with SI's values, as the script runs them from the repository root (it already calls
`./venv/bin/ray`, `:73`):

```bash
./venv/bin/python -m raypoolkit.rehearsal_lock acquire --project StochasticInstantons --purpose "<PURPOSE>" --ray-temp-dir /tmp/ray-si --ray-address 127.0.0.1:6390
./venv/bin/python -m raypoolkit.rehearsal_lock set-pid --project StochasticInstantons --ray-temp-dir /tmp/ray-si <gcs_server pid>
./venv/bin/python -m raypoolkit.rehearsal_lock release --project StochasticInstantons --ray-temp-dir /tmp/ray-si
./venv/bin/python -m raypoolkit.rehearsal_lock status --ray-temp-dir /tmp/ray-si --ray-address 127.0.0.1:6390
```

In the script the values come from its own variables (`$LOCK_PROJECT`, `$SI_TEMP_DIR`,
`$SI_ADDRESS`, `:65-71`), so the script's command line names none of them (contract §6; item 5).
Spell the address `127.0.0.1:6390`: it is what the cluster's Ray client server carries as
`--address=` (`:163`), and the module looks for that spelling (contract §6 item 2).

The owner file `acquire` writes (contract §4): `project: StochasticInstantons`, `purpose:
<PURPOSE>`, `acquired`, `host`, `ray_temp_dir: /tmp/ray-si`, `ray_address: 127.0.0.1:6390`, `pid:
-`, the same keys and values the script writes today. `set-pid` then rewrites the `pid:` line
alone, where `write_owner "$purpose" "$gcs"` (`:329`) rewrote all seven, `acquired` included.

### 3.1 `cmd_start` (`:265-336`)

`acquire` in place of `acquire_lock` (`:278`), passing its exit through as the script does now
(`|| return $?`): **0** go on; **3** held, or the old location exists (contract §7, §9), nothing
created; **4** a process of `/tmp/ray-si` or of the client server for `127.0.0.1:6390` is alive, or
`ps` cannot be read, the lock released again; **1** the owner file could not be written; **2** a
usage error, which here would be a fault in the script's values. Then `ray start` (`:305-308`)
unchanged, and `set-pid` with the `gcs_server`'s pid in place of `write_owner` (`:329`).

**Every path that releases**, today and after:

| Path | Today | After | Exit |
|---|---|---|---|
| **stale cluster**, `:280-286`: `list_cluster_pids` finds a process naming `/tmp/ray-si` | `release_lock`, lock removed | `acquire` makes this check itself and exits 4 with the lock released (contract §7). If the script keeps its own check after `acquire`, it is reached only if a process appears between the two; then `release` refuses (a process of `/tmp/ray-si` alive), and the lock **stays held** | 4 |
| **held port**, `:288-301` | `release_lock`, lock removed | `release` with `pid: -`: 0 when nothing of the cluster is alive, which `acquire` has just checked (transcript: `release` 0); 1, lock held, only if a process of `/tmp/ray-si` or the client server appeared since | 4 |
| **`ray start` failed**, `:309-316`: `stop_cluster`, then `release_lock` | lock removed whatever `stop_cluster` returned | `release` 0 if `stop_cluster` left nothing the module lists; otherwise 1 and the lock **stays held**, where today it is removed | 1 |
| **no `gcs_server`**, `:318-328`: the same | the same | the same | 1 |
| **`set-pid` refused** (new): the `gcs_server` gone before it was recorded, or the lock not SI's | — | treat as the row above: `stop_cluster`, `release`, return 1 | 1 |
| **the trap**, `:303`, on `INT` or `TERM` between `:303` and `:330`: `stop_cluster`, `release_lock`, `exit 130` | lock removed | as the `ray start` row: held if anything is left. The pid is `-` until `set-pid`, so only the rule can refuse | 130 |

The script's `release_lock` checks identity only (`:130-147`). The module's `release` also refuses
while the recorded pid is alive, while any process of `/tmp/ray-si` or of the client server for
the owner's address is alive, or when `ps` cannot be read (contract §7). A lock left held this way
is the protection working: something of the cluster is still running. The person runs `status`, and
`stop` again, or asks the user.

**The stale-cluster check (`:280-286`)** duplicates `acquire`'s exit 4, by a different rule (item 5:
the module has no `ray_cluster.sh` exclusion, and the script's ancestors seed its walk). The
options:
- **drop the script's check**: `acquire`'s 4 covers it, with the same exit code; its message is the
  module's (below). Costs nothing but the message;
- **keep both**: one more `ps` per start, and a path whose `release` would now refuse, leaving the
  lock held with exit 4 where today it is removed.

**Advice:** drop it. The module's rule is the one `release` will apply to this lock, and the
module's own check releases the lock again before it exits 4.

### 3.2 `cmd_stop` (`:338-354`)

`stop_cluster` (`:350`) unchanged, then `release` in place of `release_lock` (`:351`): **0**
released, or no lock; **1** refused. After a `stop_cluster` that returned 0 the `gcs_server` is
gone (it checks every pid with `kill -0`, `:242-249`), so `release` refuses only if the module
lists something the script's rule did not (item 5).

**The first check** (`:340-349`): if the lock is another project's, touch nothing (the usage text,
`:55-56`, promises it). The module has no command for "whose lock is it". The options:
- **read the owner file at the new location.** The owner format is a contract (§4), and so is the
  location (§3); `owner_field` keeps working on it. The location can be asked of the pinned
  package, so the script never spells it: the module's function `default_lock_dir()` (contract
  §2), for example `./venv/bin/python -c 'from raypoolkit.rehearsal_lock import default_lock_dir;
  print(default_lock_dir())'`. Costs one more Python start (a few tenths of a second) per `stop`,
  and a function of the API in a shell script. Run in the transcript: it printed
  `$HOME/.raypoolkit/rehearsal-lock`, and the owner's `project` read there was
  `StochasticInstantons`, then `ChamPBH` once CPBH held the lock;
- **drop the check, and rely on `release`'s refusal after the stop.** `release` exits 1 on another
  project's lock and prints both sides (transcript), but `stop_cluster` has run by then: SI's own
  cluster is stopped even while another project holds the lock. The usage text's "touches nothing"
  is lost;
- **parse `status`.** Its layout is a contract (§8): the owner file's lines indented four spaces.
  Costs a read of the process table, and a parse of a layout written for people.

**Advice:** read the owner file at `default_lock_dir()`. It keeps the promise of `:55-56`, uses
only what the contract fixes, and does not spell the location in SI.

### 3.3 `cmd_status` (`:356-383`)

The module's `status --ray-temp-dir /tmp/ray-si --ray-address 127.0.0.1:6390` in place of the
lock's lines (`:357-368`), then the script's port lines (`:378-381`), unchanged. Exit 0 always, as
both are today. The module's `status` lists the processes of `/tmp/ray-si` and of the client server
for `127.0.0.1:6390`, by its rule. The script's own listing (`:369-377`) is what `stop` would
signal, by the script's rule. **Advice:** keep both, the script's under its own heading: where the
two differ, `stop` will leave something that `release` then refuses on, and `status` is where a
person sees it.

**Does anything read `cmd_status`'s lines?** No. `git grep -n -E 'lock: (HELD|free)|owner
pid|cluster \(/tmp|port [0-9]+: (held|free)|ray_cluster\.sh"? status|cmd_status' 7071bb8` finds
them only in the script itself. No tracked file runs or sources the script; `CLAUDE.md:16-18`
tells a person to run it.

### 3.4 What a person sees change

| Today (the script) | After (the module, contract §7–§8) |
|---|---|
| `>> ray_cluster: the rehearsal lock is held (…/.rehearsal-lock); its owner file:` … `stop and ask the user; this script never waits on, or breaks, the lock` | `the rehearsal lock is held (…/.raypoolkit/rehearsal-lock); its owner file:` … `stop and ask the user; nothing here waits on, retries or breaks the lock` |
| — | `the old location of the rehearsal lock exists (…); its owner file:` …, exit 3 |
| `>> ray_cluster: processes naming /tmp/ray-si are already running (a stale cluster?); not starting. Run 'stop' first.` | `processes of /tmp/ray-si or of the Ray client server for 127.0.0.1:6390 are alive:`, the list, `released the lock again; not acquired` |
| `>> ray_cluster: released the rehearsal lock` / `no lock to release` | `released the rehearsal lock (<path>)` / `no lock to release (<path>)` |
| `the lock is not SI's; not releasing it. owner has project=… ray_temp_dir=…` | `release: the lock is not the caller's (…); not touching it`, the owner file and the caller |
| — | `release: the recorded pid <pid> is alive; not releasing` and `release: processes of … are alive:` |
| `lock: HELD (…)` / `lock: free (… does not exist)` | the same words, the new path |
| `owner pid: - (no cluster pid recorded yet)` | `owner pid: - (no pid recorded yet)` |
| `SI cluster (/tmp/ray-si): no processes` | `Ray processes of /tmp/ray-si: none` (and the script's own line, if kept) |
| — | `old location: PRESENT (…)` while the old location exists |

The module writes its refusals to stderr and its other lines to stdout (contract §7), as the
script's `err` and `say` do; it has no `>> ray_cluster:` prefix. The script's exit codes are
unchanged on every path but those of 3.1, where the code is the same and the lock's state differs.

Each command above was run with SI's values against a scratch `HOME` (04's log §3.3, script
`si.sh`): `acquire` 0, `release` with nothing recorded 0 (the held-port path), `acquire` 0 and a
second `acquire` 3, `set-pid` with a live pid 0, `status` 0, `release` while that pid lived 1, then
0 once it was reaped, then 0 with no lock; with CPBH holding the lock, SI's `release` 1, `set-pid`
1 and `acquire` 3; `ray-processes` 0.

## 4. Its Ray starts

- **The cluster**: `ray start --head --temp-dir "$SI_TEMP_DIR"` on fixed ports (`:305-308`). It
  already has a temp dir of its own, which is what the module's rule needs (contract §6). Nothing
  changes.
- **The drivers** connect by address: `main.py:131`, `plot_GradientCoupledSolutions.py:973` and
  `plot_InstantonSolutions.py:1207` call `ray.init(address=args.ray_address…)`, and
  `CLAUDE.md:16-18` runs rehearsals and long builds with `--ray-address 127.0.0.1:6390`. A driver
  connected this way is not a process of the instance by either rule; the recorded pid is the
  `gcs_server`'s. Nothing changes.
- **`--ray-address local`** starts "a private in-process Ray instance" (`CLAUDE.md:14-16`). SI's
  documents do not put such a run under the lock: "Rehearsals and long builds run on SI's isolated
  cluster under the shared rehearsal lock" (`:16-17`). The integration tests start in-process
  instances (`tests/conftest.py:55`, `tests/test_inventory_store.py:80`,
  `tests/test_inflaton_trajectory_prune.py:464`; `CLAUDE.md:29-30`), outside the lock, today and
  after. If SI ever runs a `local` build under the lock, it needs `_temp_dir` as SGK's starts do
  (SGK's checklist, item 4), and its owner values would be `ray_address: in-process` with a temp
  dir of its own, not the cluster's.

## 5. What it must now do differently

- **The module's rule replaces the script's for the lock; the script's still drives
  `stop_cluster`** (`:201-261`, by `list_cluster_pids`, `:159-188`). Where the two differ (contract
  §6 against `:151-188`):
  - **the `ray_cluster.sh` exclusion.** The script never lists a process whose command names
    `ray_cluster.sh` (`:176`, `:183`); the module has no such exclusion. A process naming both the
    script and `/tmp/ray-si` (another invocation whose `PURPOSE` names the temp dir, say) is listed
    by the module and not signalled by `stop`, so `release` then refuses. It over-lists, the safe
    side;
  - **ancestors.** The script keeps itself and its ancestors out of the listing and out of the
    walk (`:173-175`). The module keeps the reading process's ancestors out of the listing but lets
    them seed the walk (contract §6 item 4): if the script's command line, or the shell's that runs
    it, names `/tmp/ray-si`, every other process that ancestor started is listed;
  - **the client server.** The script matches `ray.util.client.server --address=127.0.0.1:6390` as
    one string, the host fixed (`:168`). The module matches `ray.util.client.server` and
    `--address=127.0.0.1:6390`, each anywhere in the command, with the address taken from the
    argument (`acquire`, `status`) or from the owner file (`release`). With SI's address spelled as
    today they find the same server;
  - **pid 1.** Both stop the ancestor walk before pid 1 (`:173`; contract §6 item 4). On macOS pid 1
    is `launchd`, which names no temp dir.
- **No command line of the script's own names the temp dir** (contract §6). `start PURPOSE` puts
  `PURPOSE` on the script's command line, so a `PURPOSE` must not name `/tmp/ray-si`; nor may the
  command that runs the script (an agent's shell command, for instance). The script passes the
  values to the module from its variables, which no command line of its own shows.
- **`acquire` does the stale-process check itself** (exit 4, the lock released again; contract §7),
  by the module's rule (3.1).
- **`release` refuses while the `gcs_server` lives** (the recorded pid), and while anything of the
  cluster is listed (3.1).
- **`status`'s layout is the module's** (contract §8; 3.4).
- **The old location** (contract §9): `acquire` refuses with 3 while `~/ScienceData/.rehearsal-lock`
  exists. The module's `release` does not look there, so a lock SI holds at the old location is
  released with the old script before the switch, or removed by the user by hand.
- **Each lock command is a Python start** that imports Ray (contract §2): `start` makes two
  (`acquire`, `set-pid`), `stop` one or two, `status` one.

## 6. Its tests

- **No SI test touches the lock.** `git grep` finds no test naming the old location, the brief,
  the script or its lock functions.
- The tests that start Ray in process (item 4) are outside the lock and unchanged.
- No SI test reads the `raypoolkit` pin. SI's counts do not change.

## 7. What goes stale

Live lines (outside `.documents/`, `.prompts/`, `prompts/` and `science-runs/`, and the script):

| Line | Says | Becomes |
|---|---|---|
| `requirements.txt:59` | the pin at `v0.2.0` | `v0.3.0` (item 1) |
| `CLAUDE.md:142-143` | "Each is pinned to a tag in `requirements.txt` (`datastorekit` `v0.5.0`, `raypoolkit` `v0.2.0`)" | `raypoolkit` `v0.3.0` |
| `CLAUDE.md:14-20` | `--ray-address` required, `local` for a private instance; rehearsals and long builds on SI's cluster "under the shared rehearsal lock" with the script; never `ray stop` "(see `.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md`)" (`:20`) | stays true: it names neither the location nor the helper, and `:20` cites the brief for `ray stop`, which is the brief's §3 (the brief's `:139`), not the §2 the contract replaces. SI may add a pointer to RayPoolKit's `docs/rehearsal-lock.md` for the lock |
| the script `:17-20` (header) | it implements the brief: "section 2 (the lock) and section 3 (the cluster)" (`:19`) | the lock is `raypoolkit.rehearsal_lock`'s, whose contract is RayPoolKit's `docs/rehearsal-lock.md` at `v0.3.0`; the brief's §3 still governs the cluster |
| the script `:25` | "never removes a lock that is not SI's" | stays true (contract §5) |
| the script `:45-51` (usage, `start`) | "take the rehearsal lock (~/ScienceData/.rehearsal-lock)"; exit 3 if held; exit 4 on a held port, the lock released | the lock at `~/.raypoolkit/rehearsal-lock`, through `raypoolkit.rehearsal_lock`; exit 3 also for the old location; exit 4 also for a live process of the cluster (3.1) |
| the script `:52-56` (usage, `stop`) | "release the lock if its owner is SI's. Touches nothing if the lock is another project's" | as SI's choice in 3.2 leaves it |
| the script `:57-58` (usage, `status`) | the lock, its owner file, the pid, the processes and ports | stays true |
| the script `:64` | "SI's cluster (rehearsal-lock-brief.md, section 3)" | stays true |
| the script `:75` | "the shared lock (rehearsal-lock-brief.md, section 2)" | gone with `:76-78`, or a pointer to the contract |
| the script `:76-77` | `LOCK_PARENT="$HOME/ScienceData"`, `LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"` | gone (item 2) |

**Records**, counted and not rewritten (lines naming `\.rehearsal-lock`, `rehearsal-lock-brief`,
`tools\.rehearsal_lock` or `rehearsal_lock\.py`; 04's log §3.5): `.documents/` 12 lines in 2 files
(the script excepted), `.prompts/` 29 lines in 11 files (the brief itself among them, at
`.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md`), `prompts/` and `science-runs/` none.
Lines that name only `~/ScienceData/` (SI's rehearsal stores live under it) or the script are more:
the planner counted about 800 lines that name the lock or the script.

## 8. Its acceptance

1. **The pin** reads `v0.3.0`: `git -C StochasticInstantons show <commit>:requirements.txt | grep
   raypoolkit` prints item 1's line, and SI's venv is installed from it.
2. **No live line names the old lock**:

   ```bash
   P='ScienceData|\.rehearsal-lock|rehearsal-lock-brief\.md, section 2|section 2 \(the lock\)'
   { git -C StochasticInstantons grep -n -E "$P" <commit> -- . ':!.documents' ':!.prompts' ':!prompts' ':!science-runs'
     git -C StochasticInstantons grep -n -E "$P" <commit> -- .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh; } | wc -l
   ```

   At `7071bb8` it finds **5 lines**, all in the script: `:19`, `:45`, `:75`, `:76`, `:77`. After
   the switch it finds **0**. The pattern does not match the brief's name alone: the brief's §3
   still governs the cluster, and `CLAUDE.md:20` and the script (`:64`) may go on citing it.
3. **The script calls the module**: `git -C StochasticInstantons grep -c 'raypoolkit\.rehearsal_lock'
   <commit> -- .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` is 0 at `7071bb8`, and at
   least 1 after. By reading, `start`, `stop` and `status` make the calls of item 3.
4. **SI's suites pass**, with no count changed.
5. **On the day**, the checks of [`switch-over.md`](switch-over.md) §3 pass.
