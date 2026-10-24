# The switch-over to the rehearsal lock of `raypoolkit` `v0.3.0`

*Written by RayPoolKit's rehearsal-lock prompt 04 on 2026-10-24, against `raypoolkit` **`v0.3.0`**
(`67a75b9`) and its contract, [`docs/rehearsal-lock.md`](../../rehearsal-lock.md) (written
"contract §N" below). The three clients were read through `git` only; every command below was run
against a scratch `HOME`, starting no Ray
([04's log](../../../prompts/rehearsal-lock/logs/04-the-switch-over-checklists.md) §3).*

This is the procedure for the day on which the three projects that share the rehearsal lock move,
together, from their own implementations to `raypoolkit.rehearsal_lock` (decision D3: one day, no
transitional release). Each client's part is in its checklist; this page is what they do together.
Like the checklists, it is data: each client acts in a campaign of its own, under its own
`CLAUDE.md`, and a recommendation is marked **Advice:**.

## 1. The parties

| Party | Checklist | Measured at | Its lock today | After the switch |
|---|---|---|---|---|
| SecondaryGWKit (SGK) | [`secondarygwkit.md`](secondarygwkit.md) | `216e44d` (`handover-remedial`, 2026-10-22) | `tools/rehearsal_lock.py` | `--project SecondaryGWKit --ray-temp-dir /tmp/ray-sgk --ray-address in-process` |
| ChamPBH (CPBH) | [`champbh.md`](champbh.md) | `807f175` (`jordan-normalization`, 2026-10-22) | the lock half of `ray_cluster.sh` | `--project ChamPBH --ray-temp-dir /tmp/ray-cpbh --ray-address 127.0.0.1:6380` |
| StochasticInstantons (SI) | [`stochasticinstantons.md`](stochasticinstantons.md) | `7071bb8` (`rrk-adoption`, 2026-10-23) | the lock half of `ray_cluster.sh` | `--project StochasticInstantons --ray-temp-dir /tmp/ray-si --ray-address 127.0.0.1:6390` |
| **RayPoolKit's proof** | — | [`docs/rehearsal-lock/ray_proof.py`](../../rehearsal-lock/ray_proof.py) | takes the lock at `old_lock_dir()`, `~/ScienceData/.rehearsal-lock` (its `:149`) | must move to the default location before it is run again, by a later prompt of this repository (`[04-the-proof-takes-the-old-lock]`, assigned to 05). Until then it is **not run** after the switch: it would hold a lock no project looks at |

*2026-10-24, prompt 05:* the proof now holds the lock at both locations, the default one first
and then the old one (decision U7), so it may be run before the switch-over and after it alike;
`[04-the-proof-takes-the-old-lock]` is closed
([`docs/rehearsal-lock-verification.md`](../../rehearsal-lock-verification.md) §4). The row above
is as 04 measured it.

Every project's lock moves from `~/ScienceData/.rehearsal-lock` to `~/.raypoolkit/rehearsal-lock`
(contract §3). A project still on its own implementation cannot see the new location, and a project
on the module refuses to `acquire` while anything exists at the old one (contract §9, decision U4).
That is why the three move on one day.

## 2. Before the day

**Each client, in its own repository:**
- its switch is ready on a branch: the pin at `v0.3.0` and its lock code replaced, as its
  checklist says, measured again against the client's commit of that day;
- its suites pass on that branch, with any fall in count explained (SGK's falls by 42, its
  checklist's item 6);
- the branch is **not merged**.

**At the start of the day**, before anything is merged:
- **no Ray process** on the machine: `pgrep -lf 'gcs_server|raylet|ray::'` finds nothing (exit 1);
- **neither lock location exists**: `ls -d ~/ScienceData/.rehearsal-lock ~/.raypoolkit/rehearsal-lock`
  finds neither. A lock at the old location is a project's that has not released it, or a stale
  one: stop and ask the user, who removes it by hand once nothing holds it (contract §1).
  `~/.raypoolkit` itself may exist, empty; it is not the lock;
- **nothing is running in any client**: in each, `./venv/bin/python -m runregistrykit list` shows
  no run `running` or stale, and no rehearsal is in progress.

These hold until the cross-check of §3 is done: **no project starts Ray during the day**.

## 3. The day

**The order.** Each client merges its switch and installs its venv from the new pin, in any order.
While no project runs Ray, the order does not matter:
- nobody holds either lock, and nothing acquires one until all three have landed;
- a client that has switched refuses to `acquire` while the old location exists (U4), so if a
  project that has not yet switched took the old lock in the meantime, the switched one would stop
  with exit 3 rather than run beside it.

**Each client, once it has landed**, from its repository root: `./venv/bin/python -m
raypoolkit.rehearsal_lock --help` prints a first line starting `usage: python -m
raypoolkit.rehearsal_lock` (contract §2), and its checklist's acceptance (item 8) holds at the
merged commit.

**After all three have landed**, the cross-check. Each command is run in its own repository, with
its own venv, from the repository root, as a shell command of its own (contract §6). None starts
Ray: `acquire` and `release` with nothing running are safe.

1. **The lock is free.** In any one client:

   ```bash
   ./venv/bin/python -m raypoolkit.rehearsal_lock status
   ```

   Exit **0**; the first line is `lock: free (<home>/.raypoolkit/rehearsal-lock does not exist)`,
   and there is no `old location: PRESENT` line.
2. **One client acquires.** In SGK (any one of the three will do):

   ```bash
   ./venv/bin/python -m raypoolkit.rehearsal_lock acquire --project SecondaryGWKit --purpose "switch-over cross-check" --ray-temp-dir /tmp/ray-sgk --ray-address in-process
   ```

   Exit **0**: `acquired the rehearsal lock (…) for SecondaryGWKit: switch-over cross-check`.
3. **Each of the other two acquires, and is refused.** In CPBH:

   ```bash
   ./venv/bin/python -m raypoolkit.rehearsal_lock acquire --project ChamPBH --purpose "switch-over cross-check" --ray-temp-dir /tmp/ray-cpbh --ray-address 127.0.0.1:6380
   ```

   and in SI:

   ```bash
   ./venv/bin/python -m raypoolkit.rehearsal_lock acquire --project StochasticInstantons --purpose "switch-over cross-check" --ray-temp-dir /tmp/ray-si --ray-address 127.0.0.1:6390
   ```

   Each exits **3**, printing SGK's owner file: the three see one lock.
4. **The first releases.** In SGK:

   ```bash
   ./venv/bin/python -m raypoolkit.rehearsal_lock release --project SecondaryGWKit --ray-temp-dir /tmp/ray-sgk
   ```

   Exit **0**; `status` (step 1) then shows the lock free again.

These four steps were run with all three projects' values against a scratch `HOME` (04's log §3.3,
script `cross.sh`): 0, 0, 3, 3, 0 and 0, as above. With a directory made at the old location there,
an `acquire` exited 3, naming it the old location, and `status` printed `old location: PRESENT`.

**Then G2 is recorded** on this repository's rehearsal-lock board
([`IMPLEMENTATION_STATE.md`](../../../prompts/rehearsal-lock/IMPLEMENTATION_STATE.md) §2), with each
client's merged commit and the cross-check's exit codes. Ray may be run again from then on, under
the new lock.

## 4. If a client cannot switch that day

Say SGK and CPBH have landed and SI cannot. The hazard runs one way:
- a switched client cannot see a lock that SI takes at the old location; but while that old lock
  exists, a switched client's `acquire` refuses with 3 (U4), so it cannot start beside SI;
- SI cannot see the new lock at all: if a switched client holds it, SI's old code takes the old
  location and runs **beside it**, and neither knows.

The options:
- **(a) No Ray in any project until the last one lands.** Nothing needs undoing; the switched
  clients wait. It rests on every person and agent of all three projects knowing, since each
  unswitched project's own documents still say to take the old lock.
- **(a′) The same, held by the lock itself.** The user makes a directory at the old location, with
  an owner file saying why (`purpose: switch-over pending`): every switched client's `acquire` then
  refuses with 3, naming the old location (contract §9), and the unswitched client's old code
  refuses with 3 too, finding the lock held. The user removes it by hand when the last client has
  landed, before §3's cross-check. It stops nothing that runs Ray without the lock.
- **(b) The switched clients revert.** Each reverts its switch commit, its pin and its old lock
  code, so all three are on the old location again, and the day is held again later, with the
  checklists measured again. Costs two commits and a second day per switched client, and Ray can
  run meanwhile.

**Advice:** (a), held by (a′), for as long as the last client takes to land, if that is a day or
two. U4's refusal exists for exactly this, and (a′) makes the wait visible to every project rather
than remembered. Take (b) only if the last client's switch is blocked for longer than the projects
can do without Ray.

## 5. Afterwards

- **The proof moves.** RayPoolKit's `docs/rehearsal-lock/ray_proof.py` takes the default location
  before it is run again (`[04-the-proof-takes-the-old-lock]`, prompt 05).
  *2026-10-24, prompt 05:* it holds both locations instead (U7), so it may be run before and after
  the switch-over alike; `[04-the-proof-takes-the-old-lock]` is closed.
- **U4's refusal is dropped** by a later release, once G2 holds (the campaign plan,
  [`prompts/rehearsal-lock/README.md`](../../../prompts/rehearsal-lock/README.md) §8). Until then
  any directory at `~/ScienceData/.rehearsal-lock` stops every `acquire`.
- **Phase 2, the cluster** (the start, the targeted stop and the status of CPBH's and SI's
  `ray_cluster.sh` as a module here), waits for G2 (README §8).
- [`docs/adoption/README.md`](../README.md) describes the adoption of `v0.2.0`'s `RayWorkPool`, not
  this switch; this page is the entry to this directory.
