# Log — rehearsal-lock prompt 04: the switch-over checklists

**Subject:** Write the rehearsal lock's switch-over checklists · **Commit:** this commit ·
**Date:** 2026-10-24 · **Agent:** Claude Opus 5.5

**Result: landed.** `docs/adoption/rehearsal-lock/` holds four new documents: a switch-over
checklist for each client, measured read-only at its commit against `raypoolkit` `v0.3.0`, and
`switch-over.md`, the procedure for the day the three move together.
- **Every client fact was read** at its commit through `git show` and `git grep`, and every
  `path:line` the checklists cite is quoted below (§3.7, 224 citations).
- **Every command was run** against a scratch `HOME` with this repository's `venv/`, from script
  files holding the clients' values in variables (clarification 7): four transcripts, **54 commands,
  each with the exit code the documents state**; no Ray started (§3.3).
- **Every Ray start under the lock** was found by grep, not taken from the prompt's list: SGK's
  third wrapper, `run_child`'s, which passes no address, is in its checklist with the options and
  the forms that keep SGK's tests passing (clarification 1; §3.6's probe).
- **Each acceptance grep bites**: at today's commits it finds 18 lines in SGK, 5 in CPBH and 5 in
  SI, every live line of its checklist's item 7 that names the old lock; after the switch, 0 (§3.5).
- **One issue opened**, `[04-the-proof-takes-the-old-lock]`, assigned to 05; the index goes from 0
  to **1**.
- Nothing under `raypoolkit/` changed; the suite is **226 → 226**, `black` 20 files unchanged. No
  client was edited, run or imported, and each is as it was (§3.2). No Ray process was started;
  neither lock location under the real `HOME` was touched. Nothing was pushed or tagged.

**Gate, re-checked at start (20:04).**
- `HEAD` was `a2a8d37` (the orchestration note), on `b7c8200` (the prompt) and `74c3d3f`; the tree
  was clean. `git diff 67a75b9 HEAD -- raypoolkit docs pyproject.toml README.md PROVENANCE.md
  .github` was empty (clarification 10): the contract the checklists cite is the tag's.
- `venv/` (3.12.15 / Ray 2.43.0): `Ran 226 tests in 2.031s` `OK`; `./venv/bin/black --check
  raypoolkit docs`: "20 files would be left unchanged".
- No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` exit 1); no `RAY_*` variable;
  `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` did not exist.
- The clients at the prompt's commits, each clean with no stash (§3.2). G1 holds: SGK's
  `tools/rehearsal_lock.py` is blob `ea14336` and its tests `cdeecd6` (42 `def test_`); CPBH's
  `ray_cluster.sh` blob `eaae1e7`; SI's `6c8eada`, the same at SI's `main` `1c223e8`.

Every scratch file of this log is under the agent's scratch directory, `…/scratchpad/agent04/`,
written `$S` below: scripts in `$S/scripts/`, outputs in `$S/out/`, the client files read for this
log (by `git show`) in `$S/src/`, the scratch `HOME`s in `$S/home/`, and the empty directory the
scripts ran from, `$S/empty/`. Ray 2.55.1's source was read from a minimal scratch venv,
`$S/ray255` (`uv venv -p /opt/local/bin/python3.13`, `uv pip install ray==2.55.1`), never imported.

## 1. What shipped

| File | What |
|---|---|
| `docs/adoption/rehearsal-lock/secondarygwkit.md` | SGK at `216e44d`: its helper and 42 tests removed; the commands with `--project SecondaryGWKit --ray-temp-dir /tmp/ray-sgk --ray-address in-process`; its ten Ray starts, three wrappers and seven `ray.init`, each with what it needs and the forms its tests accept |
| `docs/adoption/rehearsal-lock/champbh.md` | CPBH at `807f175`: the lock half of `ray_cluster.sh` replaced by the module with `--project ChamPBH --ray-temp-dir /tmp/ray-cpbh --ray-address 127.0.0.1:6380`; every release path of `cmd_start`; `cmd_stop`'s and `cmd_status`'s options; what a person sees change |
| `docs/adoption/rehearsal-lock/stochasticinstantons.md` | SI at `7071bb8`: the same, with SI's values and lines |
| `docs/adoption/rehearsal-lock/switch-over.md` | the parties (the proof among them), the preconditions, the order and why it does not matter, the cross-check, what to do if a client cannot switch, and afterwards |
| this log, the board, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Each checklist has the prompt's eight items, in its order and under its names: the pin; what it
removes; what replaces it; its Ray starts; what it must now do differently; its tests; what goes
stale; its acceptance. Each opens with the client, its full SHA, branch, date, subject and tree.

**The acceptance greps** (each checklist's item 8; §3.5):

| Client | Pattern, over the live paths | At today's commit | After |
|---|---|---|---|
| SGK | `ScienceData\|\.rehearsal-lock\|rehearsal-lock-brief\|tools\.rehearsal_lock\|rehearsal_lock\.py`, `-- . ':!docs' ':!prompts'` | **18**: `CLAUDE.md:138`, `:152`, `:155`, `:161`; `tools/rehearsal_lock.py` 5; `tools/tests/test_rehearsal_lock.py` 9 | 0 |
| CPBH | `ScienceData\|\.rehearsal-lock\|rehearsal-lock-brief\.md, section 2\|section 2 \(the lock\)`, outside `.documents/`, `.prompts/`, `prompts/`, `science-runs/`, plus the script by name | **5**: the script `:21`, `:44`, `:76`, `:77`, `:78` | 0 |
| SI | the same | **5**: the script `:19`, `:45`, `:75`, `:76`, `:77` | 0 |

CPBH's and SI's checklists add a positive check: `git grep -c 'raypoolkit\.rehearsal_lock'` in the
script, 0 today and at least 1 after.

**The Advice items written:**
1. SGK: the temp dir `/tmp/ray-sgk` (checked unused on the machine and in all three clients, §3.5).
2. SGK: for the sweep, record the parent's pid, which outlives every child.
3. SGK: `run_child`'s wrapper takes `address="local"` with `_temp_dir`, not `_temp_dir` alone.
4. SGK: run each lock command in a shell command of its own, never in the one that launches a build.
5. SGK: `CLAUDE.md` states the protocol itself and stops pointing at
   `prompts/runregistry-extraction/README.md` §4.1.
6. CPBH and SI: drop the script's stale-cluster check; `acquire`'s exit 4 covers it.
7. CPBH and SI: keep `cmd_stop`'s first check by reading the owner file at the module's
   `default_lock_dir()`.
8. CPBH and SI: in `cmd_status`, keep the script's own process listing beside the module's.
9. The day: if a client cannot switch, no Ray in any project until it lands, held by a placeholder
   at the old location (option (a′)); revert only if the last switch is blocked for long.

## 2. Deviations from the prompt

The orchestrator's clarifications, as applied:

1. **SGK's third in-process start, `run_child`'s wrapper** (clarification 1). **STRUCTURALLY
   REQUIRED**: the prompt's §0.2 lists two wrappers and seven `ray.init`; item 4 asks for every
   start under the lock. Found by the clarification's grep (§3.5), read at
   `RunDrivers/quadsource_atol_sweep.py:482-491`, and written into SGK's item 4 with the two
   options (`_temp_dir` alone, or `address="local"` with it), what each does in Ray at both ends
   (§3.4), and Advice for the second. Its test, `test_build_rehearsal_scope.py:337-344`, is in item 6.
2. **Clarification 1's "a constant, keyword or comment naming 'rehearsal' … fails it" is not quite
   what the test does.** **STRUCTURALLY REQUIRED**, since a checklist must be true of the client.
   The test asserts `"rehearsal" not in ast.unparse(run_child)`; `ast.unparse` drops comments, and
   the match is case-sensitive. So a comment passes, and so does a name `REHEARSAL_TEMP_DIR`; a
   lower-case name, a string or a docstring containing `rehearsal` fails. Checked by a probe with
   the test's own predicate (§3.6, rows R3–R6); SGK's checklist says so.
3. **The acceptance greps bite** (clarification 3). **STRUCTURALLY REQUIRED**: as the prompt writes
   it, item 8's grep finds nothing today in CPBH or SI. Each checklist's command names the script
   explicitly beside the live paths, and its pattern is extended until it finds every live line
   of item 7 that names the old lock (§3.5).
4. **CPBH's and SI's pattern does not include the brief's name alone**, where clarification 3
   suggests `rehearsal-lock-brief`. **STRUCTURALLY REQUIRED**: the brief's §3 (the isolated
   clusters, and "Never run `ray stop`", SI's brief `:87`, `:139`) is not replaced by the contract,
   which replaces its §2 only, and the cluster half stays (D4). The scripts cite §3 for the cluster
   (CPBH `:65`, SI `:64`) and SI's `CLAUDE.md:20` cites the brief for `ray stop`; a grep matching
   every citation of the brief could reach 0 only by deleting true lines. The pattern matches the
   §2 citations instead (`rehearsal-lock-brief\.md, section 2`, `section 2 \(the lock\)`), and the
   checklists say why. SI's `CLAUDE.md:14-20` is listed in item 7 as staying true. SGK's pattern
   keeps `rehearsal-lock-brief`, since its only live citation (`CLAUDE.md:161`) calls the brief
   "the contract", which it no longer is.
5. **The forms that keep `test_ray_address_default.py` passing** (clarification 2). IMPLEMENTATION
   CHOICE at the orchestrator's direction. `_temp_dir`'s default was read at both ends
   (`worker.py:1487`, `:1645`), and the forms were checked against the tests' own predicates,
   `test_inventory_consumers.py`'s too (§3.6): the conditional keyword and `**kwargs` pass; two
   calls, an assigned call (for `main.py`) or a positional address fail.
6. **Every release in `cmd_start`, and what the module's `release` adds** (clarification 4).
   IMPLEMENTATION CHOICE at the orchestrator's direction. CPBH's and SI's item 3.1 give each of the
   four paths and the trap, the exit code and the lock's state today and after, and the options for
   the stale-cluster check with Advice to drop it.
7. **`local` in CPBH and SI** (clarification 5). IMPLEMENTATION CHOICE at the orchestrator's
   direction. Read: CPBH's `CLAUDE.md:128-134` and SI's `CLAUDE.md:14-17` put rehearsals and long
   builds on the cluster, under the lock, and offer `local` for a private instance without the
   lock. Each item 4 says so, and what a `local` build under the lock would need.
8. **What the venv rule saw** (clarification 6), with its example corrected. **STRUCTURALLY
   REQUIRED** for the correction: the clarification gives `tools/tests/test_inventory_consumers.py`
   as an SGK test that calls `ray.init`. It does not: it runs `main.py` with `ray.init` replaced by
   a function that raises (`:48-60`) and reads `main.py`'s call with `ast` (`:199-219`). `git grep
   -n -E 'ray\.init\(' 216e44d -- '*tests*'` finds no test that starts Ray, and the modules end by
   asserting Ray was not initialised. SGK's item 5 says what the venv rule saw that the temp-dir
   rule does not, and that SGK's tests lose nothing by it.
9. **The transcripts run from script files** (clarification 7). IMPLEMENTATION CHOICE at the
   orchestrator's direction: no Bash command string named a client's temp dir; each script built
   it inside (`D="/tmp/ray-$(printf sgk)"`), ran with `HOME` its own scratch directory, from
   `$S/empty`, with `venv/`'s interpreter by absolute path and `-I`. Each `HOME` was listed and was
   empty at the end.
10. **The issue for 05** (clarification 8), on the board's §3 with an **Assigned (2026-10-24):**
    line, and one row under the index's §1.2. IMPLEMENTATION CHOICE at the orchestrator's direction.
11. **No README in the new directory** (clarification 9); `switch-over.md` is its entry and links
    the three checklists. IMPLEMENTATION CHOICE at the orchestrator's direction; §5, observation 1.
12. **The contract is the tag's** (clarification 10): checked at the gate. No deviation.

The agent's own choices:

13. **SGK's acceptance has six items, CPBH's and SI's five**, where the prompt names four: SGK adds
    "the helper is gone" and "every start gives the temp dir"; CPBH and SI add the positive grep
    that the script calls the module. IMPLEMENTATION CHOICE: each is a fact item 2 or 4 sets up, and
    the positive grep makes the switch visible to a grep as well as its absence.
14. **A sixth row in CPBH's and SI's release-path table**, "`set-pid` refused", which the script does
    not have today. IMPLEMENTATION CHOICE: `set-pid` replaces `write_owner` and can exit 1 (contract
    §7), so the switched script needs a path for it.
15. **`cmd_status`: Advice to keep the script's own process listing**, where the prompt names only
    the port lines as kept. IMPLEMENTATION CHOICE, marked Advice: the two listings are by different
    rules, and the difference is what a failed release would turn on.
16. **Option (a′) in `switch-over.md` §4**, a placeholder at the old location, beside the prompt's two
    options. IMPLEMENTATION CHOICE: it is the prompt's option (a) held by U4's refusal and by the
    unswitched clients' own `mkdir`. The Advice is (a) held by (a′).
17. **`switch-over.md` §2 measures "nothing is running" by each client's `runregistrykit list`**, says
    that `~/.raypoolkit` may exist without being the lock, and §3 adds a `--help` check once a client
    has landed. IMPLEMENTATION CHOICE: each makes a precondition checkable by a command.
18. **The record counts of item 7 use the lock's names**, not bare `ScienceData`, so they are smaller
    than the prompt's §0.3 ("about 890" and "about 800"), which also counted the clients' rehearsal
    stores under `~/ScienceData/` and lines naming the script. IMPLEMENTATION CHOICE; each checklist
    states the pattern and cites the planner's figure.
19. **Each checklist states where the client's lock lives on its branches**: SGK's `main` (`d6afa05`,
    2026-09-19, 342 commits behind) has neither the helper nor a `raypoolkit` pin. IMPLEMENTATION
    CHOICE: it decides where SGK's switch is made.
20. **The commands were run with this repository's `venv/`** (3.12.15 / Ray 2.43.0), not each
    client's. STRUCTURALLY REQUIRED by the rules (no client's venv is used); the module is the tag's
    (clarification 10), and its behaviour does not depend on Ray's version.
21. **A grep of this repository's `HEAD` printed four lines of `prompts/rehearsal-lock/orchestrator/prompt-04.md`**,
    which the agent was told not to read: the first version of the `/tmp/ray-sgk` check
    (§3.5) also grepped this repository for the spelling. UNINTENDED DRIFT, in process only: the
    lines repeated what the clarifications already say (that `/tmp/ray-sgk` does not exist), nothing
    in the documents rests on them, and the check was re-run without that grep (the script below is
    the one re-run).

## 3. Verification performed

### 3.1 The suite and `black` (prompt §3.1)

| When | Command | Result |
|---|---|---|
| before (20:04, `a2a8d37`) | `./venv/bin/python -m unittest discover -s raypoolkit/tests -t .` | `Ran 226 tests in 2.031s` `OK` |
| after the documents, before staging | the same | `Ran 226 tests in 2.056s` `OK` |
| after staging | the same | `Ran 226 tests in 2.253s` `OK` |

`./venv/bin/black --check raypoolkit docs`: "20 files would be left unchanged", before and after
(`black` reads no Markdown). **226 → 226**; no test was added or changed.

### 3.2 The clients are untouched (prompt §3.2)

`git -C <client> rev-parse HEAD`, `git -C <client> status --porcelain | shasum` and `git -C
<client> stash list | wc -l`, with the branch:

| Client | Before (20:04) | After |
|---|---|---|
| SGK | `216e44d883e78df459c378c3669cf2859ecf11e6`, `da39a3e…`, 0, `handover-remedial` | the same (20:32) |
| CPBH | `807f17549f55f86c000716597492cf8b286ac982`, `da39a3e…`, 0, `jordan-normalization` | the same (20:32) |
| SI | `7071bb8452252245ca65b3161681c1a634733878`, `da39a3e…`, 0, `rrk-adoption` | the same (20:32) |

`da39a3e…` is the SHA-1 of the empty string: each tree clean. No client's venv was used; no
client's working tree was read: every client file came through `git show` or `git grep`.

### 3.3 The transcripts (prompt §2.3)

Run as `HOME=$S/home/<name> bash $S/scripts/<name>.sh > $S/out/<name>.txt 2>&1`, from `$S/empty`,
one after another; each exited 0 (`FAILS=0`). The scripts of this log, with their SHA-256:

| Script | SHA-256 |
|---|---|
| `lib.sh` | `4c34971bae156266a935324171a34d66cfe373ce9abf3a62aaacaa31ebd2a69e` |
| `sgk.sh` | `2e45ad2a4bed5ee5c94f5b494f63662c5482f75b3cfd3fcadb6c371828f9696f` |
| `cpbh.sh` | `7328d176f6b8063f4136f9bf7f23e7a16674a8df362aa2d1f23f139d63be86ed` |
| `si.sh` | `738b390ec486246cfd33ea182178a811595d74d06dd39a31ce9c98a1b2b27a01` |
| `cross.sh` | `dff94d958d4cddd622be30f662b8d3ebec5ad4e69eea4bafea26b7f89e114c38` |
| `check_sgk_dir.sh` | `591cbb1180d8aa2978e3b953ce1cd968be3e376e6bbdc00237ce70922c0aa7c2` |
| `acceptance_greps.sh` | `c8b1f101333db8e8ca86b481556a2d0dfbd45b47e0af89adea809c457b3830ff` |
| `record_counts.sh` | `21d501785a1dc4aae72c5b18723541bdaf3514f0e377db167224886939fd75c4` |
| `quote_refs.sh` | `32f24f4ebbc7db4d4c6998ae5bd7693a5332d275e16595e7240a7285d1ea8574` |
| `refs.txt` | `8b7c1f70ee0f1cb7898df5dfebd12b426b28079937c855ce5458658fbb0ecc55` |
| `ray_source.sh` | `e317603cf2c0c103bf0da2e0b27aaac07b4f569c02463b4ad9668d687cdb0b1a` |
| `probe_forms.py` | `161e2778b36f7c1fd0833fbc842e992ec999d3465be2d0353fd6803816b2f29b` |

`lib.sh`, the functions the four transcripts share:

```bash
# Shared by the transcript scripts. The interpreter is this repository's venv/, run with -I.
PY=/Users/ds283/Documents/Code/RayPoolKit/venv/bin/python
L() { "$PY" -I -m raypoolkit.rehearsal_lock "$@"; }
# run EXPECTED ARGS...: print the command (with the temp dir shown as $D), run it, compare its exit
FAILS=0
run() {
    local want="$1"; shift
    local shown="$*"
    shown="${shown//$D/\$D}"
    echo "\$ rehearsal_lock $shown"
    L "$@" 2>&1 | sed -E 's/^/    /'
    local rc=${PIPESTATUS[0]}
    if [ "$rc" = "$want" ]; then echo "  -> exit $rc (expected $want) PASS"; else echo "  -> exit $rc (expected $want) FAIL"; FAILS=$((FAILS+1)); fi
}
home_listing() { echo "-- HOME ($HOME):"; (cd "$HOME" && find . -mindepth 1 | sort | sed 's/^/    /'); echo "-- end of listing"; }
```

`sgk.sh` (SGK's checklist, item 3):

```bash
#!/bin/bash
# SGK's commands under v0.3.0 (checklist item 3), against a scratch HOME. Starts no Ray.
set -u
. "$(dirname "$0")/lib.sh"
P=SecondaryGWKit
D="/tmp/ray-$(printf sgk)"     # held in a variable: no command line of this script names it
A=in-process
echo "HOME=$HOME  P=$P  A=$A  D=$D"
run 0 status
run 0 acquire --project "$P" --purpose "sgk switch-over check" --ray-temp-dir "$D" --ray-address "$A"
run 0 status --ray-temp-dir "$D" --ray-address "$A"
run 3 acquire --project "$P" --purpose "a second acquire" --ray-temp-dir "$D" --ray-address "$A"
sleep 300 & SP=$!
echo "(a live pid of this script's: sleep $SP)"
run 0 set-pid --project "$P" --ray-temp-dir "$D" "$SP"
run 0 status --ray-temp-dir "$D" --ray-address "$A"
run 1 release --project "$P" --ray-temp-dir "$D"
kill "$SP"; wait "$SP" 2>/dev/null
echo "(sleep $SP killed and reaped)"
run 0 status
run 0 release --project "$P" --ray-temp-dir "$D"
run 0 release --project "$P" --ray-temp-dir "$D"
run 1 set-pid --project "$P" --ray-temp-dir "$D" "$$"
run 0 ray-processes --ray-temp-dir "$D"
run 2 acquire --project "$P" --purpose "x" --ray-temp-dir "$D" --ray-address local
run 2 acquire --project "$P" --purpose "x" --ray-temp-dir in-process --ray-address "$A"
home_listing
rmdir "$HOME/.raypoolkit"
home_listing
echo "FAILS=$FAILS"; exit $FAILS
```

Its output (`$S` for the scratch directory; the commands print the temp dir as `$D`, the module's
own lines print it as it is):

```text
HOME=$S/home/sgk  P=SecondaryGWKit  A=in-process  D=/tmp/ray-sgk
$ rehearsal_lock status
    lock: free ($S/home/sgk/.raypoolkit/rehearsal-lock does not exist)
    Ray processes: no temp dir given
  -> exit 0 (expected 0) PASS
$ rehearsal_lock acquire --project SecondaryGWKit --purpose sgk switch-over check --ray-temp-dir $D --ray-address in-process
    acquired the rehearsal lock ($S/home/sgk/.raypoolkit/rehearsal-lock) for SecondaryGWKit: sgk switch-over check
  -> exit 0 (expected 0) PASS
$ rehearsal_lock status --ray-temp-dir $D --ray-address in-process
    lock: HELD ($S/home/sgk/.raypoolkit/rehearsal-lock)
        project: SecondaryGWKit
        purpose: sgk switch-over check
        acquired: 2026-10-24T20:14:04+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-sgk
        ray_address: in-process
        pid: -
    owner pid: - (no pid recorded yet)
    Ray processes of /tmp/ray-sgk: none
  -> exit 0 (expected 0) PASS
$ rehearsal_lock acquire --project SecondaryGWKit --purpose a second acquire --ray-temp-dir $D --ray-address in-process
    the rehearsal lock is held ($S/home/sgk/.raypoolkit/rehearsal-lock); its owner file:
        project: SecondaryGWKit
        purpose: sgk switch-over check
        acquired: 2026-10-24T20:14:04+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-sgk
        ray_address: in-process
        pid: -
    stop and ask the user; nothing here waits on, retries or breaks the lock
  -> exit 3 (expected 3) PASS
(a live pid of this script's: sleep 29702)
$ rehearsal_lock set-pid --project SecondaryGWKit --ray-temp-dir $D 29702
    recorded pid 29702 in $S/home/sgk/.raypoolkit/rehearsal-lock/owner
  -> exit 0 (expected 0) PASS
$ rehearsal_lock status --ray-temp-dir $D --ray-address in-process
    lock: HELD ($S/home/sgk/.raypoolkit/rehearsal-lock)
        project: SecondaryGWKit
        purpose: sgk switch-over check
        acquired: 2026-10-24T20:14:04+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-sgk
        ray_address: in-process
        pid: 29702
    owner pid 29702: alive
    Ray processes of /tmp/ray-sgk: none
  -> exit 0 (expected 0) PASS
$ rehearsal_lock release --project SecondaryGWKit --ray-temp-dir $D
    release: the recorded pid 29702 is alive; not releasing
  -> exit 1 (expected 1) PASS
(sleep 29702 killed and reaped)
$ rehearsal_lock status
    lock: HELD ($S/home/sgk/.raypoolkit/rehearsal-lock)
        project: SecondaryGWKit
        purpose: sgk switch-over check
        acquired: 2026-10-24T20:14:04+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-sgk
        ray_address: in-process
        pid: 29702
    owner pid 29702: NOT alive
    Ray processes of /tmp/ray-sgk: none
  -> exit 0 (expected 0) PASS
$ rehearsal_lock release --project SecondaryGWKit --ray-temp-dir $D
    released the rehearsal lock ($S/home/sgk/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
$ rehearsal_lock release --project SecondaryGWKit --ray-temp-dir $D
    no lock to release ($S/home/sgk/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
$ rehearsal_lock set-pid --project SecondaryGWKit --ray-temp-dir $D 29684
    set-pid: there is no lock at $S/home/sgk/.raypoolkit/rehearsal-lock
  -> exit 1 (expected 1) PASS
$ rehearsal_lock ray-processes --ray-temp-dir $D
  -> exit 0 (expected 0) PASS
$ rehearsal_lock acquire --project SecondaryGWKit --purpose x --ray-temp-dir $D --ray-address local
    usage: python -m raypoolkit.rehearsal_lock acquire [-h] --project PROJECT
                                                       --purpose PURPOSE
                                                       --ray-temp-dir RAY_TEMP_DIR
                                                       --ray-address RAY_ADDRESS
    python -m raypoolkit.rehearsal_lock acquire: error: argument --ray-address: ray_address must be 'in-process' or host:port, not 'local'
  -> exit 2 (expected 2) PASS
$ rehearsal_lock acquire --project SecondaryGWKit --purpose x --ray-temp-dir in-process --ray-address in-process
    usage: python -m raypoolkit.rehearsal_lock acquire [-h] --project PROJECT
                                                       --purpose PURPOSE
                                                       --ray-temp-dir RAY_TEMP_DIR
                                                       --ray-address RAY_ADDRESS
    python -m raypoolkit.rehearsal_lock acquire: error: argument --ray-temp-dir: ray_temp_dir must be an absolute path, not 'in-process'
  -> exit 2 (expected 2) PASS
-- HOME ($S/home/sgk):
    ./.raypoolkit
-- end of listing
-- HOME ($S/home/sgk):
-- end of listing
FAILS=0
```

`cpbh.sh` (CPBH's checklist, item 3, with the held-port path and `cmd_stop`'s first check):

```bash
#!/bin/bash
# ChamPBH's commands under v0.3.0 (checklist item 3), against a scratch HOME. Starts no Ray.
set -u
. "$(dirname "$0")/lib.sh"
P=ChamPBH
D="/tmp/ray-$(printf cpbh)"     # held in a variable: no command line of this script names it
A=127.0.0.1:6380
echo "HOME=$HOME  P=$P  A=$A  D=$D"
echo "== cmd_start, the held-port path: acquire, then release with nothing recorded"
run 0 status --ray-temp-dir "$D" --ray-address "$A"
run 0 acquire --project "$P" --purpose "cpbh switch-over check (port path)" --ray-temp-dir "$D" --ray-address "$A"
run 0 release --project "$P" --ray-temp-dir "$D"
echo "== cmd_start, the ordinary path: acquire, (ray start), set-pid with the gcs_server's pid"
run 0 acquire --project "$P" --purpose "cpbh switch-over check" --ray-temp-dir "$D" --ray-address "$A"
run 3 acquire --project "$P" --purpose "a second start" --ray-temp-dir "$D" --ray-address "$A"
sleep 300 & SP=$!
echo "(a live pid of this script's, standing for the gcs_server: sleep $SP)"
run 0 set-pid --project "$P" --ray-temp-dir "$D" "$SP"
echo "== cmd_status: the module's status, with this project's values"
run 0 status --ray-temp-dir "$D" --ray-address "$A"
echo "== cmd_stop's first check, by the owner file at the module's own location (Advice)"
LOCK="$("$PY" -I -c 'from raypoolkit.rehearsal_lock import default_lock_dir; print(default_lock_dir())')"
echo "default_lock_dir() -> ${LOCK/#$HOME/\$HOME}"
echo "owner project: $(sed -n 's/^project: //p' "$LOCK/owner" | head -n 1)"
echo "owner ray_temp_dir: $(sed -n 's/^ray_temp_dir: //p' "$LOCK/owner" | head -n 1 | sed "s#$D#\$D#")"
echo "== the trap, or cmd_stop, while the recorded pid lives: release refused"
run 1 release --project "$P" --ray-temp-dir "$D"
kill "$SP"; wait "$SP" 2>/dev/null
echo "(sleep $SP killed and reaped: stop_cluster's work done)"
run 0 release --project "$P" --ray-temp-dir "$D"
run 0 release --project "$P" --ray-temp-dir "$D"
echo "== another project's lock: StochasticInstantons holds it"
OD="/tmp/ray-$(printf si)"
run 0 acquire --project StochasticInstantons --purpose "the other project" --ray-temp-dir "$OD" --ray-address 127.0.0.1:6390
echo "owner project read by cmd_stop's check: $(sed -n 's/^project: //p' "$LOCK/owner" | head -n 1)"
run 1 release --project "$P" --ray-temp-dir "$D"
run 1 set-pid --project "$P" --ray-temp-dir "$D" "$$"
run 3 acquire --project "$P" --purpose "cpbh while another holds it" --ray-temp-dir "$D" --ray-address "$A"
run 0 release --project StochasticInstantons --ray-temp-dir "$OD"
run 0 ray-processes --ray-temp-dir "$D" --ray-address "$A"
home_listing
rmdir "$HOME/.raypoolkit"
home_listing
echo "FAILS=$FAILS"; exit $FAILS
```

```text
HOME=$S/home/cpbh  P=ChamPBH  A=127.0.0.1:6380  D=/tmp/ray-cpbh
== cmd_start, the held-port path: acquire, then release with nothing recorded
$ rehearsal_lock status --ray-temp-dir $D --ray-address 127.0.0.1:6380
    lock: free ($S/home/cpbh/.raypoolkit/rehearsal-lock does not exist)
    Ray processes of /tmp/ray-cpbh: none
  -> exit 0 (expected 0) PASS
$ rehearsal_lock acquire --project ChamPBH --purpose cpbh switch-over check (port path) --ray-temp-dir $D --ray-address 127.0.0.1:6380
    acquired the rehearsal lock ($S/home/cpbh/.raypoolkit/rehearsal-lock) for ChamPBH: cpbh switch-over check (port path)
  -> exit 0 (expected 0) PASS
$ rehearsal_lock release --project ChamPBH --ray-temp-dir $D
    released the rehearsal lock ($S/home/cpbh/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
== cmd_start, the ordinary path: acquire, (ray start), set-pid with the gcs_server's pid
$ rehearsal_lock acquire --project ChamPBH --purpose cpbh switch-over check --ray-temp-dir $D --ray-address 127.0.0.1:6380
    acquired the rehearsal lock ($S/home/cpbh/.raypoolkit/rehearsal-lock) for ChamPBH: cpbh switch-over check
  -> exit 0 (expected 0) PASS
$ rehearsal_lock acquire --project ChamPBH --purpose a second start --ray-temp-dir $D --ray-address 127.0.0.1:6380
    the rehearsal lock is held ($S/home/cpbh/.raypoolkit/rehearsal-lock); its owner file:
        project: ChamPBH
        purpose: cpbh switch-over check
        acquired: 2026-10-24T20:14:12+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-cpbh
        ray_address: 127.0.0.1:6380
        pid: -
    stop and ask the user; nothing here waits on, retries or breaks the lock
  -> exit 3 (expected 3) PASS
(a live pid of this script's, standing for the gcs_server: sleep 29774)
$ rehearsal_lock set-pid --project ChamPBH --ray-temp-dir $D 29774
    recorded pid 29774 in $S/home/cpbh/.raypoolkit/rehearsal-lock/owner
  -> exit 0 (expected 0) PASS
== cmd_status: the module's status, with this project's values
$ rehearsal_lock status --ray-temp-dir $D --ray-address 127.0.0.1:6380
    lock: HELD ($S/home/cpbh/.raypoolkit/rehearsal-lock)
        project: ChamPBH
        purpose: cpbh switch-over check
        acquired: 2026-10-24T20:14:12+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-cpbh
        ray_address: 127.0.0.1:6380
        pid: 29774
    owner pid 29774: alive
    Ray processes of /tmp/ray-cpbh: none
  -> exit 0 (expected 0) PASS
== cmd_stop's first check, by the owner file at the module's own location (Advice)
default_lock_dir() -> $HOME/.raypoolkit/rehearsal-lock
owner project: ChamPBH
owner ray_temp_dir: $D
== the trap, or cmd_stop, while the recorded pid lives: release refused
$ rehearsal_lock release --project ChamPBH --ray-temp-dir $D
    release: the recorded pid 29774 is alive; not releasing
  -> exit 1 (expected 1) PASS
(sleep 29774 killed and reaped: stop_cluster's work done)
$ rehearsal_lock release --project ChamPBH --ray-temp-dir $D
    released the rehearsal lock ($S/home/cpbh/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
$ rehearsal_lock release --project ChamPBH --ray-temp-dir $D
    no lock to release ($S/home/cpbh/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
== another project's lock: StochasticInstantons holds it
$ rehearsal_lock acquire --project StochasticInstantons --purpose the other project --ray-temp-dir /tmp/ray-si --ray-address 127.0.0.1:6390
    acquired the rehearsal lock ($S/home/cpbh/.raypoolkit/rehearsal-lock) for StochasticInstantons: the other project
  -> exit 0 (expected 0) PASS
owner project read by cmd_stop's check: StochasticInstantons
$ rehearsal_lock release --project ChamPBH --ray-temp-dir $D
    release: the lock is not the caller's (project is 'StochasticInstantons', not 'ChamPBH'; ray_temp_dir is '/tmp/ray-si', not '/tmp/ray-cpbh'); not touching it
        owner:
        project: StochasticInstantons
        purpose: the other project
        acquired: 2026-10-24T20:14:15+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-si
        ray_address: 127.0.0.1:6390
        pid: -
        caller: project: ChamPBH, ray_temp_dir: /tmp/ray-cpbh
  -> exit 1 (expected 1) PASS
$ rehearsal_lock set-pid --project ChamPBH --ray-temp-dir $D 29748
    set-pid: the lock is not the caller's (project is 'StochasticInstantons', not 'ChamPBH'; ray_temp_dir is '/tmp/ray-si', not '/tmp/ray-cpbh'); not touching it
        owner:
        project: StochasticInstantons
        purpose: the other project
        acquired: 2026-10-24T20:14:15+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-si
        ray_address: 127.0.0.1:6390
        pid: -
        caller: project: ChamPBH, ray_temp_dir: /tmp/ray-cpbh
  -> exit 1 (expected 1) PASS
$ rehearsal_lock acquire --project ChamPBH --purpose cpbh while another holds it --ray-temp-dir $D --ray-address 127.0.0.1:6380
    the rehearsal lock is held ($S/home/cpbh/.raypoolkit/rehearsal-lock); its owner file:
        project: StochasticInstantons
        purpose: the other project
        acquired: 2026-10-24T20:14:15+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-si
        ray_address: 127.0.0.1:6390
        pid: -
    stop and ask the user; nothing here waits on, retries or breaks the lock
  -> exit 3 (expected 3) PASS
$ rehearsal_lock release --project StochasticInstantons --ray-temp-dir /tmp/ray-si
    released the rehearsal lock ($S/home/cpbh/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
$ rehearsal_lock ray-processes --ray-temp-dir $D --ray-address 127.0.0.1:6380
  -> exit 0 (expected 0) PASS
-- HOME ($S/home/cpbh):
    ./.raypoolkit
-- end of listing
-- HOME ($S/home/cpbh):
-- end of listing
FAILS=0
```

`si.sh` is `cpbh.sh` with SI's values (`P=StochasticInstantons`, `D` built from `si`,
`A=127.0.0.1:6390`) and ChamPBH as the other project; the two differ in those lines only.

```text
HOME=$S/home/si  P=StochasticInstantons  A=127.0.0.1:6390  D=/tmp/ray-si
== cmd_start, the held-port path: acquire, then release with nothing recorded
$ rehearsal_lock status --ray-temp-dir $D --ray-address 127.0.0.1:6390
    lock: free ($S/home/si/.raypoolkit/rehearsal-lock does not exist)
    Ray processes of /tmp/ray-si: none
  -> exit 0 (expected 0) PASS
$ rehearsal_lock acquire --project StochasticInstantons --purpose si switch-over check (port path) --ray-temp-dir $D --ray-address 127.0.0.1:6390
    acquired the rehearsal lock ($S/home/si/.raypoolkit/rehearsal-lock) for StochasticInstantons: si switch-over check (port path)
  -> exit 0 (expected 0) PASS
$ rehearsal_lock release --project StochasticInstantons --ray-temp-dir $D
    released the rehearsal lock ($S/home/si/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
== cmd_start, the ordinary path: acquire, (ray start), set-pid with the gcs_server's pid
$ rehearsal_lock acquire --project StochasticInstantons --purpose si switch-over check --ray-temp-dir $D --ray-address 127.0.0.1:6390
    acquired the rehearsal lock ($S/home/si/.raypoolkit/rehearsal-lock) for StochasticInstantons: si switch-over check
  -> exit 0 (expected 0) PASS
$ rehearsal_lock acquire --project StochasticInstantons --purpose a second start --ray-temp-dir $D --ray-address 127.0.0.1:6390
    the rehearsal lock is held ($S/home/si/.raypoolkit/rehearsal-lock); its owner file:
        project: StochasticInstantons
        purpose: si switch-over check
        acquired: 2026-10-24T20:14:20+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-si
        ray_address: 127.0.0.1:6390
        pid: -
    stop and ask the user; nothing here waits on, retries or breaks the lock
  -> exit 3 (expected 3) PASS
(a live pid of this script's, standing for the gcs_server: sleep 29860)
$ rehearsal_lock set-pid --project StochasticInstantons --ray-temp-dir $D 29860
    recorded pid 29860 in $S/home/si/.raypoolkit/rehearsal-lock/owner
  -> exit 0 (expected 0) PASS
== cmd_status: the module's status, with this project's values
$ rehearsal_lock status --ray-temp-dir $D --ray-address 127.0.0.1:6390
    lock: HELD ($S/home/si/.raypoolkit/rehearsal-lock)
        project: StochasticInstantons
        purpose: si switch-over check
        acquired: 2026-10-24T20:14:20+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-si
        ray_address: 127.0.0.1:6390
        pid: 29860
    owner pid 29860: alive
    Ray processes of /tmp/ray-si: none
  -> exit 0 (expected 0) PASS
== cmd_stop's first check, by the owner file at the module's own location (Advice)
default_lock_dir() -> $HOME/.raypoolkit/rehearsal-lock
owner project: StochasticInstantons
owner ray_temp_dir: $D
== the trap, or cmd_stop, while the recorded pid lives: release refused
$ rehearsal_lock release --project StochasticInstantons --ray-temp-dir $D
    release: the recorded pid 29860 is alive; not releasing
  -> exit 1 (expected 1) PASS
(sleep 29860 killed and reaped: stop_cluster's work done)
$ rehearsal_lock release --project StochasticInstantons --ray-temp-dir $D
    released the rehearsal lock ($S/home/si/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
$ rehearsal_lock release --project StochasticInstantons --ray-temp-dir $D
    no lock to release ($S/home/si/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
== another project's lock: ChamPBH holds it
$ rehearsal_lock acquire --project ChamPBH --purpose the other project --ray-temp-dir /tmp/ray-cpbh --ray-address 127.0.0.1:6380
    acquired the rehearsal lock ($S/home/si/.raypoolkit/rehearsal-lock) for ChamPBH: the other project
  -> exit 0 (expected 0) PASS
owner project read by cmd_stop's check: ChamPBH
$ rehearsal_lock release --project StochasticInstantons --ray-temp-dir $D
    release: the lock is not the caller's (project is 'ChamPBH', not 'StochasticInstantons'; ray_temp_dir is '/tmp/ray-cpbh', not '/tmp/ray-si'); not touching it
        owner:
        project: ChamPBH
        purpose: the other project
        acquired: 2026-10-24T20:14:23+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-cpbh
        ray_address: 127.0.0.1:6380
        pid: -
        caller: project: StochasticInstantons, ray_temp_dir: /tmp/ray-si
  -> exit 1 (expected 1) PASS
$ rehearsal_lock set-pid --project StochasticInstantons --ray-temp-dir $D 29836
    set-pid: the lock is not the caller's (project is 'ChamPBH', not 'StochasticInstantons'; ray_temp_dir is '/tmp/ray-cpbh', not '/tmp/ray-si'); not touching it
        owner:
        project: ChamPBH
        purpose: the other project
        acquired: 2026-10-24T20:14:23+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-cpbh
        ray_address: 127.0.0.1:6380
        pid: -
        caller: project: StochasticInstantons, ray_temp_dir: /tmp/ray-si
  -> exit 1 (expected 1) PASS
$ rehearsal_lock acquire --project StochasticInstantons --purpose si while another holds it --ray-temp-dir $D --ray-address 127.0.0.1:6390
    the rehearsal lock is held ($S/home/si/.raypoolkit/rehearsal-lock); its owner file:
        project: ChamPBH
        purpose: the other project
        acquired: 2026-10-24T20:14:23+01:00
        host: mps026088
        ray_temp_dir: /tmp/ray-cpbh
        ray_address: 127.0.0.1:6380
        pid: -
    stop and ask the user; nothing here waits on, retries or breaks the lock
  -> exit 3 (expected 3) PASS
$ rehearsal_lock release --project ChamPBH --ray-temp-dir /tmp/ray-cpbh
    released the rehearsal lock ($S/home/si/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
$ rehearsal_lock ray-processes --ray-temp-dir $D --ray-address 127.0.0.1:6390
  -> exit 0 (expected 0) PASS
-- HOME ($S/home/si):
    ./.raypoolkit
-- end of listing
-- HOME ($S/home/si):
-- end of listing
FAILS=0
```

`cross.sh` (`switch-over.md` §3, then the old location of U4, made in the scratch `HOME`):

```bash
#!/bin/bash
# switch-over.md section 3: the cross-check with all three projects' values, then the old location
# (U4). Against a scratch HOME. Starts no Ray.
set -u
. "$(dirname "$0")/lib.sh"
D_SGK="/tmp/ray-$(printf sgk)"; D_CPBH="/tmp/ray-$(printf cpbh)"; D_SI="/tmp/ray-$(printf si)"
D="$D_SGK"   # for the shown commands
show() { local s="$*"; s="${s//$D_SGK/\$D_SGK}"; s="${s//$D_CPBH/\$D_CPBH}"; s="${s//$D_SI/\$D_SI}"; echo "$s"; }
run2() { local want="$1"; shift; echo "\$ rehearsal_lock $(show "$*")"; L "$@" 2>&1 | while IFS= read -r line; do echo "    $(show "$line")"; done; local rc=${PIPESTATUS[0]}; if [ "$rc" = "$want" ]; then echo "  -> exit $rc (expected $want) PASS"; else echo "  -> exit $rc (expected $want) FAIL"; FAILS=$((FAILS+1)); fi; }
echo "== 1. status: the lock free, no old location"
run2 0 status
echo "== 2. SGK acquires"
run2 0 acquire --project SecondaryGWKit --purpose "switch-over cross-check" --ray-temp-dir "$D_SGK" --ray-address in-process
echo "== 3. ChamPBH and StochasticInstantons each acquire, and get 3"
run2 3 acquire --project ChamPBH --purpose "switch-over cross-check" --ray-temp-dir "$D_CPBH" --ray-address 127.0.0.1:6380
run2 3 acquire --project StochasticInstantons --purpose "switch-over cross-check" --ray-temp-dir "$D_SI" --ray-address 127.0.0.1:6390
echo "== 4. SGK releases"
run2 0 release --project SecondaryGWKit --ray-temp-dir "$D_SGK"
run2 0 status
echo "== U4: an old lock left at ~/ScienceData/.rehearsal-lock (made here, in the scratch HOME)"
mkdir -p "$HOME/ScienceData/.rehearsal-lock"
printf 'project: ChamPBH\npurpose: an unswitched start\nacquired: 2026-10-24T12:00:00+01:00\nhost: h\nray_temp_dir: %s\nray_address: 127.0.0.1:6380\npid: -\n' "$D_CPBH" > "$HOME/ScienceData/.rehearsal-lock/owner"
run2 3 acquire --project StochasticInstantons --purpose "after the switch" --ray-temp-dir "$D_SI" --ray-address 127.0.0.1:6390
run2 0 status
rm "$HOME/ScienceData/.rehearsal-lock/owner"; rmdir "$HOME/ScienceData/.rehearsal-lock" "$HOME/ScienceData"
home_listing
rmdir "$HOME/.raypoolkit"
home_listing
echo "FAILS=$FAILS"; exit $FAILS
```

```text
== 1. status: the lock free, no old location
$ rehearsal_lock status
    lock: free ($S/home/cross/.raypoolkit/rehearsal-lock does not exist)
    Ray processes: no temp dir given
  -> exit 0 (expected 0) PASS
== 2. SGK acquires
$ rehearsal_lock acquire --project SecondaryGWKit --purpose switch-over cross-check --ray-temp-dir $D_SGK --ray-address in-process
    acquired the rehearsal lock ($S/home/cross/.raypoolkit/rehearsal-lock) for SecondaryGWKit: switch-over cross-check
  -> exit 0 (expected 0) PASS
== 3. ChamPBH and StochasticInstantons each acquire, and get 3
$ rehearsal_lock acquire --project ChamPBH --purpose switch-over cross-check --ray-temp-dir $D_CPBH --ray-address 127.0.0.1:6380
    the rehearsal lock is held ($S/home/cross/.raypoolkit/rehearsal-lock); its owner file:
        project: SecondaryGWKit
        purpose: switch-over cross-check
        acquired: 2026-10-24T20:14:27+01:00
        host: mps026088
        ray_temp_dir: $D_SGK
        ray_address: in-process
        pid: -
    stop and ask the user; nothing here waits on, retries or breaks the lock
  -> exit 3 (expected 3) PASS
$ rehearsal_lock acquire --project StochasticInstantons --purpose switch-over cross-check --ray-temp-dir $D_SI --ray-address 127.0.0.1:6390
    the rehearsal lock is held ($S/home/cross/.raypoolkit/rehearsal-lock); its owner file:
        project: SecondaryGWKit
        purpose: switch-over cross-check
        acquired: 2026-10-24T20:14:27+01:00
        host: mps026088
        ray_temp_dir: $D_SGK
        ray_address: in-process
        pid: -
    stop and ask the user; nothing here waits on, retries or breaks the lock
  -> exit 3 (expected 3) PASS
== 4. SGK releases
$ rehearsal_lock release --project SecondaryGWKit --ray-temp-dir $D_SGK
    released the rehearsal lock ($S/home/cross/.raypoolkit/rehearsal-lock)
  -> exit 0 (expected 0) PASS
$ rehearsal_lock status
    lock: free ($S/home/cross/.raypoolkit/rehearsal-lock does not exist)
    Ray processes: no temp dir given
  -> exit 0 (expected 0) PASS
== U4: an old lock left at ~/ScienceData/.rehearsal-lock (made here, in the scratch HOME)
$ rehearsal_lock acquire --project StochasticInstantons --purpose after the switch --ray-temp-dir $D_SI --ray-address 127.0.0.1:6390
    the old location of the rehearsal lock exists ($S/home/cross/ScienceData/.rehearsal-lock); its owner file:
        project: ChamPBH
        purpose: an unswitched start
        acquired: 2026-10-24T12:00:00+01:00
        host: h
        ray_temp_dir: $D_CPBH
        ray_address: 127.0.0.1:6380
        pid: -
    it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
  -> exit 3 (expected 3) PASS
$ rehearsal_lock status
    lock: free ($S/home/cross/.raypoolkit/rehearsal-lock does not exist)
    old location: PRESENT ($S/home/cross/ScienceData/.rehearsal-lock)
    Ray processes: no temp dir given
  -> exit 0 (expected 0) PASS
-- HOME ($S/home/cross):
    ./.raypoolkit
-- end of listing
-- HOME ($S/home/cross):
-- end of listing
FAILS=0
```

**Every exit code is the one the documents state**: 54 commands, 54 PASS. In each script the live
pid for `set-pid` is a `sleep` the script started; `release` was run once while it lived (1) and
once after it was killed and reaped (0). The port-refusal path's `release`, with nothing recorded,
is CPBH's and SI's first `release` (0). Each scratch `HOME` held `.raypoolkit/` (empty) after the
last release, since `release` removes the lock and not its parent; the script removed it, and the
`HOME` was empty at the end. No command started Ray.

### 3.4 Ray's source, at both ends (prompt §3.4; clarifications 1 and 2)

Read from the files only: 2.43.0 in `venv/`, 2.55.1 in the scratch venv `$S/ray255`. Nothing was
imported. `$S/scripts/ray_source.sh`:

```text
== Ray 2.43.0 (Version: 2.43.0)
-- _private/worker.py:1487, :1651, :1687, :1791
 1487      _temp_dir: Optional[str] = kwargs.pop("_temp_dir", None)
 1651      bootstrap_address = services.canonicalize_bootstrap_address(address, _temp_dir)
 1687      if bootstrap_address is None:
 1791              temp_dir=_temp_dir,
-- _private/services.py:402-407, :424-427, :547-550
  402      env_addr = os.environ.get(ray_constants.RAY_ADDRESS_ENVIRONMENT_VARIABLE)
  403      if env_addr is not None and env_addr != "":
  404          addr = env_addr
  405  
  406      if addr is not None and addr != "auto":
  407          return addr
  424      if bootstrap_addr is None:
  425          if addr is None:
  426              # Caller should start a new instance.
  427              return None
  547      if addr is None or addr == "auto":
  548          addr = get_ray_address_from_environment(addr, temp_dir)
  549      if addr is None or addr == "local":
  550          return None
-- _private/utils.py:112-115 (the address file), :146-151 (read)
  112  def get_ray_address_file(temp_dir: Optional[str]):
  113      if temp_dir is None:
  114          temp_dir = get_ray_temp_dir()
  115      return os.path.join(temp_dir, "ray_current_cluster")
  146  def read_ray_address(temp_dir: Optional[str] = None) -> str:
  147      address_file = get_ray_address_file(temp_dir)
  148      if not os.path.exists(address_file):
  149          return None
  150      with open(address_file, "r") as f:
  151          return f.read().strip()
-- scripts/scripts.py:1072 (the only writer)
 1072      ray._private.utils.write_ray_address(ray_params.gcs_address, temp_dir)
-- _private/node.py:451-462 (a connecting node's temp dir)
  451          else:
  452              if self._ray_params.temp_dir is None:
  453                  assert not self._default_worker
  454                  temp_dir = ray._private.utils.internal_kv_get_with_retry(
  455                      self.get_gcs_client(),
  456                      "temp_dir",
  457                      ray_constants.KV_NAMESPACE_SESSION,
  458                      num_retries=ray_constants.NUM_REDIS_GET_RETRIES,
  459                  )
  460                  self._temp_dir = ray._private.utils.decode(temp_dir)
  461              else:
  462                  self._temp_dir = self._ray_params.temp_dir
== Ray 2.55.1 (Version: 2.55.1)
-- _private/worker.py:1645, :1811, :1843, :1960
 1645      _temp_dir: Optional[str] = kwargs.pop("_temp_dir", None)
 1811      bootstrap_address = services.canonicalize_bootstrap_address(address, _temp_dir)
 1843      if bootstrap_address is None:
 1960              temp_dir=_temp_dir,
-- _private/services.py:421-426, :443-446, :686-689
  421      env_addr = os.environ.get(ray_constants.RAY_ADDRESS_ENVIRONMENT_VARIABLE)
  422      if env_addr is not None and env_addr != "":
  423          addr = env_addr
  424  
  425      if addr is not None and addr != "auto":
  426          return addr
  443      if bootstrap_addr is None:
  444          if addr is None:
  445              # Caller should start a new instance.
  446              return None
  686      if addr is None or addr == "auto":
  687          addr = get_ray_address_from_environment(addr, temp_dir)
  688      if addr is None or addr == "local":
  689          return None
-- _common/utils.py:342-345 (the address file)
  342  def get_ray_address_file(temp_dir: Optional[str]):
  343      if temp_dir is None:
  344          temp_dir = get_default_ray_temp_dir()
  345      return os.path.join(temp_dir, "ray_current_cluster")
-- scripts/scripts.py:1153 (the only writer)
 1153      ray._private.utils.write_ray_address(ray_params.gcs_address, temp_dir)
-- _private/node.py:537-547 (a connecting node's temp dir)
  537          self.temp_dir = self._ray_params.temp_dir
  538          if self.temp_dir is None:
  539              if node_to_connect_info is not None:
  540                  self.temp_dir = node_to_connect_info.temp_dir
  541              else:
  542                  if self.head:
  543                      self.temp_dir = ray._common.utils.get_default_ray_temp_dir()
  544                  else:
  545                      assert not self._default_worker
  546                      self.temp_dir = self._head_temp_dir
  547  
-- writers of ray_current_cluster at each end
<2.43.0>/scripts/scripts.py:1072:    ray._private.utils.write_ray_address(ray_params.gcs_address, temp_dir)
<2.55.1>/scripts/scripts.py:1153:    ray._private.utils.write_ray_address(ray_params.gcs_address, temp_dir)
```

What this bears out, at both ends, for SGK's item 4:
- `_temp_dir` is a keyword popped from `kwargs` with default `None`, so `_temp_dir=None` is not
  passing it (clarification 2);
- `address="local"` returns `None` from `canonicalize_bootstrap_address` before the environment
  is consulted: a new instance, `RAY_ADDRESS` ignored;
- `address=None` takes `RAY_ADDRESS`, then `<temp_dir>/ray_current_cluster` (`/tmp/ray/…` with no
  temp dir), and starts a new instance only if neither gives an address (clarification 1). Only
  `ray start` writes the file, at the end of its `start` command, head or not (corrected in SGK's
  checklist from a first draft's "`ray start --head`");
- with a `host:port`, the connecting node takes `_temp_dir` as its own temp dir when it is given,
  and the head's otherwise (prompt §0.4).

### 3.5 The machine, the greps and the counts

**`/tmp/ray-sgk`** (SGK's Advice), `$S/scripts/check_sgk_dir.sh`, run as `TMPDIR=$S bash …` from
`$S/empty`:

```bash
#!/bin/bash
# Is the SGK temp dir named by any file or process on this machine? The value is held in a
# variable built from parts, so no command line of this script's own names it, and the process
# table is read into a file first, so the filter's own command line is not in it.
D="/tmp/ray-$(printf 'sgk')"
T="$(mktemp "${TMPDIR:-/tmp}/ps.XXXXXX")"
echo "exists: $( [ -e "$D" ] && echo yes || echo no )"
echo "exists as /private: $( [ -e "/private$D" ] && echo yes || echo no )"
ps -axww -o pid= -o command= > "$T"
echo "processes whose command names it: $(grep -c -F "$D" "$T")"
rm -f "$T"
for c in SecondaryGWKit ChamPBH StochasticInstantons; do
  case $c in SecondaryGWKit) r=216e44d;; ChamPBH) r=807f175;; StochasticInstantons) r=7071bb8;; esac
  echo "$c at $r: $(git -C /Users/ds283/Documents/Code/$c grep -h -c -F "$D" $r -- | awk '{s+=$1} END{print s+0}') lines name it"
done
```

```text
exists: no
exists as /private: no
processes whose command names it: 0
SecondaryGWKit at 216e44d: 0 lines name it
ChamPBH at 807f175: 0 lines name it
StochasticInstantons at 7071bb8: 0 lines name it
```

**SGK's Ray starts** (clarification 1's grep, SGK's item 4):

```text
$ git -C SecondaryGWKit grep -n -E 'ray\.init\(|_real_ray_init\(' 216e44d -- ':!docs' ':!prompts'
216e44d:RunDrivers/quadsource_atol_sweep.py:487:        return _real_ray_init(
216e44d:RunDrivers/quadsource_atol_sweep.py:629:        context = _real_ray_init(
216e44d:RunDrivers/scoped_pipeline_run.py:24:  1. patches ray.init so that main.py's own `ray.init(address=...)` bootstraps a local instance
216e44d:RunDrivers/scoped_pipeline_run.py:709:        context = _real_ray_init(
216e44d:extract_GkSource_data.py:118:ray.init(address=args.ray_address)
216e44d:extract_GkWKB_data.py:110:ray.init(address=args.ray_address)
216e44d:extract_Gk_data.py:109:ray.init(address=args.ray_address)
216e44d:extract_QuadSourceIntegral_data.py:130:ray.init(address=args.ray_address)
216e44d:extract_TkWKB_data.py:106:ray.init(address=args.ray_address)
216e44d:extract_tensor_source_data.py:110:ray.init(address=args.ray_address)
216e44d:main.py:314:ray.init(address=args.ray_address)
216e44d:tools/tests/test_inventory_consumers.py:215:        ray_init = self.index_of(is_ray_init, "ray.init(...)")
```

**The acceptance greps**, `$S/scripts/acceptance_greps.sh` (each grep's lines go to stderr and its
count to stdout):

```bash
#!/bin/bash
# Each checklist's acceptance grep (item 8), run at the client's commit of the checklist.
P_SGK='ScienceData|\.rehearsal-lock|rehearsal-lock-brief|tools\.rehearsal_lock|rehearsal_lock\.py'
P_CL='ScienceData|\.rehearsal-lock|rehearsal-lock-brief\.md, section 2|section 2 \(the lock\)'
RC=.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh
cd /Users/ds283/Documents/Code
echo "== SecondaryGWKit 216e44d"
git -C SecondaryGWKit grep -n -E "$P_SGK" 216e44d -- . ':!docs' ':!prompts' | tee /dev/stderr | wc -l
for c in ChamPBH:807f175 StochasticInstantons:7071bb8; do
  n=${c%%:*}; r=${c#*:}
  echo "== $n $r"
  { git -C "$n" grep -n -E "$P_CL" "$r" -- . ':!.documents' ':!.prompts' ':!prompts' ':!science-runs'
    git -C "$n" grep -n -E "$P_CL" "$r" -- "$RC"; } | tee /dev/stderr | wc -l
  echo "-- the module's calls in the script (0 today)"
  git -C "$n" grep -c 'raypoolkit\.rehearsal_lock' "$r" -- "$RC" || echo 0
done
```

```text
== SecondaryGWKit 216e44d
216e44d:CLAUDE.md:138:   `PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock ray-processes`: a `SIGKILL`ed driver's GCS
216e44d:CLAUDE.md:152:lock, the directory `~/ScienceData/.rehearsal-lock`, lets only one rehearsal or long build run at a
216e44d:CLAUDE.md:155:- A rehearsal or long build takes it with `PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock
216e44d:CLAUDE.md:161:- The contract is StochasticInstantons' `rehearsal-lock-brief.md` at its `d6d550b`;
216e44d:tools/rehearsal_lock.py:5:They share one lock, the directory ``~/ScienceData/.rehearsal-lock``, so that only one rehearsal or
216e44d:tools/rehearsal_lock.py:7:``.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md`` at its commit ``d6d550b``, sections 2 and
216e44d:tools/rehearsal_lock.py:12:    PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock <command>
216e44d:tools/rehearsal_lock.py:68:    return Path.home() / "ScienceData" / ".rehearsal-lock"
216e44d:tools/rehearsal_lock.py:441:        prog="python -m tools.rehearsal_lock",
216e44d:tools/tests/test_rehearsal_lock.py:2:Tests for ``tools/rehearsal_lock.py``, SGK's side of the shared rehearsal lock
216e44d:tools/tests/test_rehearsal_lock.py:6:directory, so that a forgotten argument cannot reach the real ``~/ScienceData``. ``ps`` is replaced
216e44d:tools/tests/test_rehearsal_lock.py:101:        self.lock = self.tmp / "ScienceData" / ".rehearsal-lock"
216e44d:tools/tests/test_rehearsal_lock.py:315:                ps_line(302, 50, f"{VENV}/bin/python -m tools.rehearsal_lock status"),
216e44d:tools/tests/test_rehearsal_lock.py:367:            rl.default_lock_dir(), self.home / "ScienceData" / ".rehearsal-lock"
216e44d:tools/tests/test_rehearsal_lock.py:374:                rl.default_lock_dir(), other / "ScienceData" / ".rehearsal-lock"
216e44d:tools/tests/test_rehearsal_lock.py:381:            (self.home / "ScienceData" / ".rehearsal-lock" / "owner").is_file()
216e44d:tools/tests/test_rehearsal_lock.py:385:        self.assertFalse((self.home / "ScienceData" / ".rehearsal-lock").exists())
216e44d:tools/tests/test_rehearsal_lock.py:441:        home_lock = self.home / "ScienceData" / ".rehearsal-lock"
18
== ChamPBH 807f175
807f175:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:21:# .prompts/dk-and-rpk-migration/rehearsal-lock-brief.md at ed9399a: section 2 (the lock) and
807f175:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:44:  start PURPOSE   take the rehearsal lock (~/ScienceData/.rehearsal-lock), then start ChamPBH's Ray
807f175:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:76:# ---- the shared lock (rehearsal-lock-brief.md, section 2) ----
807f175:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:77:LOCK_PARENT="$HOME/ScienceData"
807f175:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:78:LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"
5
-- the module's calls in the script (0 today)
0
== StochasticInstantons 7071bb8
7071bb8:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:19:# .prompts/dk-and-rpk-migration/rehearsal-lock-brief.md: section 2 (the lock) and section 3 (the
7071bb8:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:45:  start PURPOSE   take the rehearsal lock (~/ScienceData/.rehearsal-lock), then start SI's Ray
7071bb8:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:75:# ---- the shared lock (rehearsal-lock-brief.md, section 2) ----
7071bb8:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:76:LOCK_PARENT="$HOME/ScienceData"
7071bb8:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:77:LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"
5
-- the module's calls in the script (0 today)
0
```

**The record counts** (item 7), `$S/scripts/record_counts.sh`:

```bash
#!/bin/bash
# Item 7's record counts: lines naming the old location, the old helper or the brief, by directory.
P='\.rehearsal-lock|rehearsal-lock-brief|tools\.rehearsal_lock|rehearsal_lock\.py'
RC=.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh
cd /Users/ds283/Documents/Code
for c in SecondaryGWKit:216e44d:docs,prompts ChamPBH:807f175:.documents,.prompts,prompts,science-runs StochasticInstantons:7071bb8:.documents,.prompts,prompts,science-runs; do
  n=${c%%:*}; rest=${c#*:}; r=${rest%%:*}; dirs=${rest#*:}
  echo "== $n $r"
  for d in ${dirs//,/ }; do
    git -C "$n" grep -n -E "$P" "$r" -- "$d" ":!$RC" | sed "s/^$r://" | awk -F: -v d="$d" '{split($1,a,"/"); k=a[1]"/"a[2]; c[k]++; f[$1]=1; t++} END{nf=0; for(x in f) nf++; printf "  %s: %d lines in %d files\n", d, t, nf; for(k in c) printf "    %s %d\n", k, c[k]}' | sort
  done
done
```

```text
== SecondaryGWKit 216e44d
    docs/handover 80
    docs/rrk-v020-adoption 76
    docs/rrk-v020-adoption-verification.md 13
    docs/runregistry-extraction 94
    docs/runregistry-extraction-verification.md 13
  docs: 276 lines in 22 files
    prompts/handover 6
    prompts/INDEX.md 1
    prompts/rrk-v020-adoption 19
    prompts/runregistry-extraction 129
  prompts: 155 lines in 31 files
== ChamPBH 807f175
    .documents/read-only-plots 2
    .documents/review-remediation-verification.md 1
    .documents/rrk-adoption 6
  .documents: 9 lines in 3 files
  .prompts: 0 lines in 0 files
    prompts/dk-and-rpk-migration 24
    prompts/read-only-plots 2
    prompts/rrk-adoption 1
  prompts: 27 lines in 10 files
  science-runs: 0 lines in 0 files
== StochasticInstantons 7071bb8
    .documents/dk-and-rpk-migration 12
  .documents: 12 lines in 2 files
    .prompts/dk-and-rpk-migration 28
    .prompts/rrk-adoption 1
  .prompts: 29 lines in 11 files
  prompts: 0 lines in 0 files
  science-runs: 0 lines in 0 files
```

**Who reads the scripts' lines** (CPBH's and SI's item 3.3): `git grep -n -E 'lock: (HELD|free)|owner
pid|cluster \(/tmp|port [0-9]+: (held|free)|ray_cluster\.sh"? status|cmd_status'` at each commit,
outside the record directories, finds nothing; over `*.sh` and `*.py` it finds only the script
itself. `git grep -l -E 'ray_cluster|stop_cluster'` over every file that is not `.md`, `.txt`,
`.log` or `.json` finds, beside the script, CPBH's `ComputeTargets/tests/test_ray_address.py`,
`config/argument_parser.py` and the two `science-runs/…/full_run_2026.6.0*.sh` (a comment, `:4`),
and nothing in SI.

**SGK's other measurements:** `def test_` per `tools/tests` module at `216e44d`:
`test_inventory_consumers` 11, `test_inventory_report` 19, `test_inventory_report_labels` 19,
`test_rehearsal_lock` 42. `git -C SecondaryGWKit merge-base --is-ancestor main 216e44d`: yes; `git
rev-list --count main..216e44d`: 342; `main` has no `tools/rehearsal_lock.py` and no `raypoolkit`
line in `requirements.txt`. No test of any client reads the `raypoolkit` pin (`git grep` for
`RayPoolKit@` and `requirements` in test modules: nothing).

### 3.6 The forms SGK's tests accept (clarifications 1 and 2)

`$S/scripts/probe_forms.py`, run as `venv/bin/python -I` from `$S/empty`. Its predicates are
copied from SGK's tests as `git show` gave them; the sources it judges are written in it. Nothing
of SGK was run or imported.

```python
"""Which spellings of SGK's Ray starts keep SGK's ast tests passing?

The predicates are copied from SGK at 216e44d (read through `git show`, not imported):
- T1 `ComputeTargets/tests/test_ray_address_default.py:95-104, :138-145` (each of the seven scripts);
- T2 `tools/tests/test_inventory_consumers.py:199-204` (main.py: `ray.init` a top-level expression);
- T3 `RunDrivers/tests/test_killed_handler.py:484-495` (the address of `_real_ray_init` in a wrapper);
- T4 `RunDrivers/tests/test_build_rehearsal_scope.py:337-344` ("rehearsal" not in run_child's unparse).
Nothing of SGK is run or imported; the candidate sources are written here.
"""

import ast

D = "/tmp/ray-" + "sgk"


def t1(tree):
    calls = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "init"
        and isinstance(n.func.value, ast.Name)
        and n.func.value.id == "ray"
    ]
    if len(calls) != 1 or calls[0].args != []:
        return False
    kws = {kw.arg: kw.value for kw in calls[0].keywords}
    return "address" in kws and ast.unparse(kws["address"]) == "args.ray_address"


def t2(tree):
    return any(
        isinstance(n, ast.Expr)
        and isinstance(n.value, ast.Call)
        and ast.unparse(n.value.func) == "ray.init"
        for n in tree.body
    )


def t3(fn):
    real = [n for n in ast.walk(fn) if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "_real_ray_init"]
    if len(real) != 1:
        return False
    address = [k.value for k in real[0].keywords if k.arg == "address"]
    return len(address) == 1 and isinstance(address[0], ast.Constant) and address[0].value == "local"


def t4(fn):
    return "rehearsal" not in ast.unparse(fn)


SCRIPTS = {
    "S0 today": "ray.init(address=args.ray_address)",
    "S1 conditional keyword": f'ray.init(address=args.ray_address, _temp_dir="{D}" if args.ray_address == "local" else None)',
    "S2 a constant, conditional": 'ray.init(address=args.ray_address, _temp_dir=SGK_RAY_TEMP_DIR if args.ray_address == "local" else None)',
    "S3 **kwargs from a helper": "ray.init(address=args.ray_address, **ray_temp_dir_kwargs(args.ray_address))",
    "S4 if/else, two calls": f'if args.ray_address == "local":\n    ray.init(address=args.ray_address, _temp_dir="{D}")\nelse:\n    ray.init(address=args.ray_address)',
    "S5 assigned (main.py)": f'context = ray.init(address=args.ray_address, _temp_dir="{D}" if args.ray_address == "local" else None)',
    "S6 address positional": f'ray.init(args.ray_address, _temp_dir="{D}")',
}
print("The seven scripts: T1 (each), T2 (main.py only)")
for name, src in SCRIPTS.items():
    tree = ast.parse(src)
    print(f"  {name:30} T1 {'pass' if t1(tree) else 'FAIL'}   T2 {'pass' if t2(tree) else 'FAIL'}")

WRAPPERS = {
    "W0 run_build/scoped today": 'def _local_ray_init(*_a, **_kw):\n    context = _real_ray_init(address="local", num_cpus=args.cpus, include_dashboard=False, ignore_reinit_error=True)\n',
    "W1 + _temp_dir constant": 'def _local_ray_init(*_a, **_kw):\n    context = _real_ray_init(address="local", _temp_dir=SGK_RAY_TEMP_DIR, num_cpus=args.cpus, include_dashboard=False, ignore_reinit_error=True)\n',
    "R0 run_child today": 'def _local_ray_init(*_a, **_kw):\n    return _real_ray_init(num_cpus=args.cpus, include_dashboard=False, ignore_reinit_error=True)\n',
    "R1 + _temp_dir only": f'def _local_ray_init(*_a, **_kw):\n    return _real_ray_init(_temp_dir="{D}", num_cpus=args.cpus, include_dashboard=False, ignore_reinit_error=True)\n',
    "R2 + address local + _temp_dir": 'def _local_ray_init(*_a, **_kw):\n    return _real_ray_init(address="local", _temp_dir=SGK_RAY_TEMP_DIR, num_cpus=args.cpus, include_dashboard=False, ignore_reinit_error=True)\n',
    "R3 R2 + a comment 'rehearsal lock'": 'def _local_ray_init(*_a, **_kw):\n    # the rehearsal lock finds this instance by its temp dir\n    return _real_ray_init(address="local", _temp_dir=SGK_RAY_TEMP_DIR, num_cpus=args.cpus)\n',
    "R4 R2 with REHEARSAL_TEMP_DIR": 'def _local_ray_init(*_a, **_kw):\n    return _real_ray_init(address="local", _temp_dir=REHEARSAL_TEMP_DIR, num_cpus=args.cpus)\n',
    "R5 R2 with rehearsal_temp_dir": 'def _local_ray_init(*_a, **_kw):\n    return _real_ray_init(address="local", _temp_dir=rehearsal_temp_dir, num_cpus=args.cpus)\n',
    "R6 R2 + a message naming it": 'def _local_ray_init(*_a, **_kw):\n    print("** under the rehearsal lock")\n    return _real_ray_init(address="local", _temp_dir=SGK_RAY_TEMP_DIR, num_cpus=args.cpus)\n',
}
print("The wrappers: T3 (run_build's and scoped_pipeline_run's), T4 (run_child's)")
for name, src in WRAPPERS.items():
    fn = ast.parse(src).body[0]
    print(f"  {name:36} T3 {'pass' if t3(fn) else 'FAIL'}   T4 {'pass' if t4(fn) else 'FAIL'}")
```

```text
The seven scripts: T1 (each), T2 (main.py only)
  S0 today                       T1 pass   T2 pass
  S1 conditional keyword         T1 pass   T2 pass
  S2 a constant, conditional     T1 pass   T2 pass
  S3 **kwargs from a helper      T1 pass   T2 pass
  S4 if/else, two calls          T1 FAIL   T2 FAIL
  S5 assigned (main.py)          T1 pass   T2 FAIL
  S6 address positional          T1 FAIL   T2 pass
The wrappers: T3 (run_build's and scoped_pipeline_run's), T4 (run_child's)
  W0 run_build/scoped today            T3 pass   T4 pass
  W1 + _temp_dir constant              T3 pass   T4 pass
  R0 run_child today                   T3 FAIL   T4 pass
  R1 + _temp_dir only                  T3 FAIL   T4 pass
  R2 + address local + _temp_dir       T3 pass   T4 pass
  R3 R2 + a comment 'rehearsal lock'   T3 pass   T4 pass
  R4 R2 with REHEARSAL_TEMP_DIR        T3 pass   T4 pass
  R5 R2 with rehearsal_temp_dir        T3 pass   T4 FAIL
  R6 R2 + a message naming it          T3 pass   T4 FAIL
```

T3 is applied by SGK's test to `run_build`'s and `scoped_pipeline_run`'s wrappers only
(`test_killed_handler.py:479`), so rows R0 and R1's T3 column is what it would say, not a test SGK
runs on `run_child`.

### 3.7 Every `path:line` the checklists cite (prompt §2.4)

`$S/scripts/quote_refs.sh $S/scripts/refs.txt`: every citation in the three checklists, by
`git show <commit>:<path>`; a range longer than eight lines is quoted by its first three and last
two lines. 224 citations. The script:

```bash
#!/bin/bash
# Quote every path:line the checklists cite, as the client's commit holds it (git show only).
# A range of more than 8 lines is quoted by its first three and last two lines.
while IFS='|' read -r client commit path specs; do
  [ -z "$client" ] && continue
  text="$(git -C "/Users/ds283/Documents/Code/$client" show "${commit}:${path}")"
  for spec in $specs; do
    a=${spec%-*}; b=${spec#*-}
    echo "### $client $commit $path:$spec"
    n=$((b - a + 1))
    if [ "$n" -le 8 ]; then
      printf '%s\n' "$text" | awk -v a="$a" -v b="$b" 'NR>=a && NR<=b {printf "%5d  %s\n", NR, substr($0,1,150)}'
    else
      printf '%s\n' "$text" | awk -v a="$a" -v b="$b" 'NR>=a && NR<=a+2 {printf "%5d  %s\n", NR, substr($0,1,150)} NR==a+3 {print "    …"} NR>=b-1 && NR<=b {printf "%5d  %s\n", NR, substr($0,1,150)}'
    fi
  done
done < "$1"
```

```text
### SecondaryGWKit 216e44d requirements.txt:2
    2  aiohttp==3.11.14
### SecondaryGWKit 216e44d requirements.txt:26
   26  grpcio==1.71.0
### SecondaryGWKit 216e44d requirements.txt:52
   52  opencensus==0.11.4
### SecondaryGWKit 216e44d requirements.txt:75-76
   75  ray==2.43.0
   76  raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
### SecondaryGWKit 216e44d CLAUDE.md:53
   53  (`/Users/ds283/Documents/Code/RayPoolKit`, https://github.com/ds283/RayPoolKit), pinned at `v0.2.0`.
### SecondaryGWKit 216e44d CLAUDE.md:137-142
  137     is reaped by its `sh`. After `end`, check
  138     `PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock ray-processes`: a `SIGKILL`ed driver's GCS
  139     server may be left alive, reparented to pid 1, stuck in its own shutdown where a `SIGTERM` cannot
  140     end it (`[03-a-sigkilled-drivers-gcs-server-deadlocks-in-shutdown]`). One still listed ten
  141     minutes after the kill is ended **by a person** with `kill -KILL <pid>`, by its pid, never by
  142     pattern and never with `ray stop`; until then the rehearsal lock cannot be released.
### SecondaryGWKit 216e44d CLAUDE.md:138
  138     `PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock ray-processes`: a `SIGKILL`ed driver's GCS
### SecondaryGWKit 216e44d CLAUDE.md:149-162
  149  ## The shared rehearsal lock
  150  
  151  Three projects on this machine (this one, ChamPBH and StochasticInstantons) run Ray builds. One
    …
  161  - The contract is StochasticInstantons' `rehearsal-lock-brief.md` at its `d6d550b`;
  162    `prompts/runregistry-extraction/README.md` §4.1 is this repository's protocol.
### SecondaryGWKit 216e44d CLAUDE.md:151-153
  151  Three projects on this machine (this one, ChamPBH and StochasticInstantons) run Ray builds. One
  152  lock, the directory `~/ScienceData/.rehearsal-lock`, lets only one rehearsal or long build run at a
  153  time.
### SecondaryGWKit 216e44d CLAUDE.md:155-158
  155  - A rehearsal or long build takes it with `PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock
  156    acquire --purpose "<text>"`, records the pid at each launch with `set-pid`, and releases it with
  157    `release` once its last Ray process is gone. **A held lock (exit 3) means stop and ask the user.**
  158    Never wait, retry or remove it. The helper has no option to do so.
### SecondaryGWKit 216e44d CLAUDE.md:159-160
  159  - Every Ray driver names its address (`local` for this repository's), never `auto`, and `ray stop`
  160    is never run: it stops every project's Ray processes.
### SecondaryGWKit 216e44d CLAUDE.md:161-162
  161  - The contract is StochasticInstantons' `rehearsal-lock-brief.md` at its `d6d550b`;
  162    `prompts/runregistry-extraction/README.md` §4.1 is this repository's protocol.
### SecondaryGWKit 216e44d CLAUDE.md:169-175
  169    PYTHONPATH=. ./venv/bin/python -m unittest discover -s AdaptiveLevin/tests -t .
  170    PYTHONPATH=. ./venv/bin/python -m unittest discover -s ComputeTargets/tests -t .
  171    PYTHONPATH=. ./venv/bin/python -m unittest discover -s CosmologyModels/tests -t .
  172    PYTHONPATH=. ./venv/bin/python -m unittest discover -s LiouvilleGreen/tests -t .
  173    PYTHONPATH=. ./venv/bin/python -m unittest discover -s ObjectFactories/tests -t .
  174    PYTHONPATH=. ./venv/bin/python -m unittest discover -s RunDrivers/tests -t .
  175    PYTHONPATH=. ./venv/bin/python -m unittest discover -s tools/tests -t .
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:5
    5  They share one lock, the directory ``~/ScienceData/.rehearsal-lock``, so that only one rehearsal or
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:7
    7  ``.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md`` at its commit ``d6d550b``, sections 2 and
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:12
   12      PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock <command>
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:49-50
   49  PROJECT = "SecondaryGWKit"
   50  IN_PROCESS = "in-process"
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:66-68
   66  def default_lock_dir():
   67      """The shared lock, computed when called (it reads ``HOME`` at that moment, never at import)."""
   68      return Path.home() / "ScienceData" / ".rehearsal-lock"
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:92-107
   92  def owner_text(purpose, pid, acquired=None, host=None):
   93      """The seven lines of the owner file, in the brief's order."""
   94      if acquired is None:
    …
  106      ]
  107      return "\n".join(lines) + "\n"
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:184-189
  184  def venv_roots():
  185      """This checkout's ``venv/`` as written and as ``realpath`` gives it (one entry when they agree)."""
  186      root = Path(__file__).resolve().parent.parent
  187      written = Path(os.path.abspath(Path(__file__).parent.parent)) / "venv"
  188      roots = [str(written), os.path.realpath(root / "venv")]
  189      return list(dict.fromkeys(roots))
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:192-246
  192  def ray_processes(ps_text=None, roots=None, self_pid=None):
  193      """
  194      Every process of this repository's Ray, as ``(pid, ppid, command)`` sorted by pid.
    …
  245      # Ray's), but are never themselves listed
  246      return [(p, table[p][0], table[p][1]) for p in sorted(marked - safe)]
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:265-471
  265  def acquire(purpose, lock_dir=None):
  266      d = _resolve(lock_dir)
  267      d.parent.mkdir(parents=True, exist_ok=True)
    …
  470          return status()
  471      return ray_processes_command()
### SecondaryGWKit 216e44d tools/rehearsal_lock.py:441
  441          prog="python -m tools.rehearsal_lock",
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:2
    2  Tests for ``tools/rehearsal_lock.py``, SGK's side of the shared rehearsal lock
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:6
    6  directory, so that a forgotten argument cannot reach the real ``~/ScienceData``. ``ps`` is replaced
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:26
   26  from tools import rehearsal_lock as rl
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:101
  101          self.lock = self.tmp / "ScienceData" / ".rehearsal-lock"
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:315
  315                  ps_line(302, 50, f"{VENV}/bin/python -m tools.rehearsal_lock status"),
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:367
  367              rl.default_lock_dir(), self.home / "ScienceData" / ".rehearsal-lock"
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:374
  374                  rl.default_lock_dir(), other / "ScienceData" / ".rehearsal-lock"
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:381
  381              (self.home / "ScienceData" / ".rehearsal-lock" / "owner").is_file()
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:385
  385          self.assertFalse((self.home / "ScienceData" / ".rehearsal-lock").exists())
### SecondaryGWKit 216e44d tools/tests/test_rehearsal_lock.py:441
  441          home_lock = self.home / "ScienceData" / ".rehearsal-lock"
### SecondaryGWKit 216e44d RunDrivers/quadsource_atol_sweep.py:482-491
  482      def _local_ray_init(*_a, **_kw):
  483          print(
  484              f"** quadsource_atol_sweep: bootstrapping a local Ray instance "
    …
  490  
  491      ray.init = _local_ray_init
### SecondaryGWKit 216e44d RunDrivers/quadsource_atol_sweep.py:487-489
  487          return _real_ray_init(
  488              num_cpus=args.cpus, include_dashboard=False, ignore_reinit_error=True
  489          )
### SecondaryGWKit 216e44d RunDrivers/quadsource_atol_sweep.py:624-636
  624      def _local_ray_init(*_a, **_kw):
  625          print(
  626              f"** quadsource_atol_sweep --build: bootstrapping a local Ray instance "
    …
  635          scoped.install_killed_handler(run, latch)
  636          return context
### SecondaryGWKit 216e44d RunDrivers/quadsource_atol_sweep.py:629-634
  629          context = _real_ray_init(
  630              address="local",
  631              num_cpus=args.cpus,
  632              include_dashboard=False,
  633              ignore_reinit_error=True,
  634          )
### SecondaryGWKit 216e44d RunDrivers/quadsource_atol_sweep.py:906-910
  906                      "Refreshed by the parent after each tolerance pair's child process exits, and "
  907                      "the `stage` names the pair just finished. A pair can legitimately take an hour "
  908                      "at the tight end of the atol axis -- that is the measurement -- so this run "
  909                      "goes stale while it is working and stale means go and look at the child's "
  910                      "output in this directory. It does not mean dead."
### SecondaryGWKit 216e44d RunDrivers/quadsource_atol_sweep.py:949-965
  949              child = subprocess.run(
  950                  [
  951                      sys.executable,
    …
  964                  env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
  965              )
### SecondaryGWKit 216e44d RunDrivers/scoped_pipeline_run.py:24
   24    1. patches ray.init so that main.py's own `ray.init(address=...)` bootstraps a local instance
### SecondaryGWKit 216e44d RunDrivers/scoped_pipeline_run.py:704-716
  704      def _local_ray_init(*_args, **_kwargs):
  705          print(
  706              f"** scoped_pipeline_run: bootstrapping a local Ray instance "
    …
  715          install_killed_handler(run, latch)
  716          return context
### SecondaryGWKit 216e44d RunDrivers/scoped_pipeline_run.py:709-714
  709          context = _real_ray_init(
  710              address="local",
  711              num_cpus=args.cpus,
  712              include_dashboard=False,
  713              ignore_reinit_error=True,
  714          )
### SecondaryGWKit 216e44d main.py:99
   99  DEFAULT_RAY_ADDRESS = "local"
### SecondaryGWKit 216e44d main.py:251-260
  251  parser.add_argument(
  252      "--ray-address",
  253      default=DEFAULT_RAY_ADDRESS,
    …
  259      ),
  260  )
### SecondaryGWKit 216e44d main.py:314
  314  ray.init(address=args.ray_address)
### SecondaryGWKit 216e44d extract_GkSource_data.py:95-96
   95      "--ray-address",
   96      default="local",
### SecondaryGWKit 216e44d extract_GkSource_data.py:118
  118  ray.init(address=args.ray_address)
### SecondaryGWKit 216e44d extract_GkWKB_data.py:87-88
   87      "--ray-address",
   88      default="local",
### SecondaryGWKit 216e44d extract_GkWKB_data.py:110
  110  ray.init(address=args.ray_address)
### SecondaryGWKit 216e44d extract_Gk_data.py:86-87
   86      "--ray-address",
   87      default="local",
### SecondaryGWKit 216e44d extract_Gk_data.py:109
  109  ray.init(address=args.ray_address)
### SecondaryGWKit 216e44d extract_QuadSourceIntegral_data.py:104-105
  104      "--ray-address",
  105      default="local",
### SecondaryGWKit 216e44d extract_QuadSourceIntegral_data.py:130
  130  ray.init(address=args.ray_address)
### SecondaryGWKit 216e44d extract_TkWKB_data.py:83-84
   83      "--ray-address",
   84      default="local",
### SecondaryGWKit 216e44d extract_TkWKB_data.py:106
  106  ray.init(address=args.ray_address)
### SecondaryGWKit 216e44d extract_tensor_source_data.py:84-85
   84      "--ray-address",
   85      default="local",
### SecondaryGWKit 216e44d extract_tensor_source_data.py:110
  110  ray.init(address=args.ray_address)
### SecondaryGWKit 216e44d ComputeTargets/tests/test_ray_address_default.py:49-51
   49  def tearDownModule():
   50      if ray.is_initialized():
   51          raise AssertionError("Ray was initialised by test_ray_address_default")
### SecondaryGWKit 216e44d ComputeTargets/tests/test_ray_address_default.py:95-104
   95  def _ray_init_calls(tree):
   96      return [
   97          node
    …
  103          and node.func.value.id == "ray"
  104      ]
### SecondaryGWKit 216e44d ComputeTargets/tests/test_ray_address_default.py:138-145
  138      def test_each_ray_init_takes_the_flag(self):
  139          for name, tree in self.trees.items():
  140              with self.subTest(script=name):
  141                  calls = _ray_init_calls(tree)
  142                  self.assertEqual(len(calls), 1)
  143                  self.assertEqual(calls[0].args, [])
  144                  address = _keywords(calls[0])["address"]
  145                  self.assertEqual(ast.unparse(address), "args.ray_address")
### SecondaryGWKit 216e44d ComputeTargets/tests/test_ray_address_default.py:153-162
  153      def test_local_ignores_RAY_ADDRESS(self):
  154          with mock.patch.dict(os.environ, {"RAY_ADDRESS": self.ELSEWHERE}):
  155              self.assertIsNone(services.canonicalize_bootstrap_address(DEFAULT))
    …
  161                  services.canonicalize_bootstrap_address("auto"), self.ELSEWHERE
  162              )
### SecondaryGWKit 216e44d tools/tests/test_inventory_consumers.py:48-60
   48  # run main.py as __main__ in this interpreter, with ray.init replaced by a function that raises
   49  _GUARDED_MAIN = """
   50  import runpy
    …
   59  
   60  ray.init = _refuse
### SecondaryGWKit 216e44d tools/tests/test_inventory_consumers.py:199-219
  199          def is_ray_init(node):
  200              return (
  201                  isinstance(node, ast.Expr)
    …
  218          self.assertLess(parse, branch)
  219          self.assertLess(branch, ray_init)
### SecondaryGWKit 216e44d tools/tests/test_inventory_consumers.py:215
  215          ray_init = self.index_of(is_ray_init, "ray.init(...)")
### SecondaryGWKit 216e44d RunDrivers/tests/test_killed_handler.py:476-517
  476  class TestTheDrivers(unittest.TestCase):
  477      """Read with `ast`: `main.py` cannot be run here, and neither can the drivers."""
  478  
    …
  516                  ]
  517                  self.assertEqual(args, ["run", "latch"])
### SecondaryGWKit 216e44d RunDrivers/tests/test_killed_handler.py:479
  479      DRIVERS = ((DRIVER, "main"), (SWEEP, "run_build"))
### SecondaryGWKit 216e44d RunDrivers/tests/test_killed_handler.py:489-495
  489                  wrapper = _function(self.outer(path, name), "_local_ray_init")
  490                  real = _calls(wrapper, "_real_ray_init")
  491                  self.assertEqual(len(real), 1)
  492                  address = [k.value for k in real[0].keywords if k.arg == "address"]
  493                  self.assertEqual(len(address), 1, "the real ray.init passes no address")
  494                  self.assertIsInstance(address[0], ast.Constant)
  495                  self.assertEqual(address[0].value, "local")
### SecondaryGWKit 216e44d RunDrivers/tests/test_build_rehearsal_scope.py:337-344
  337      def test_run_child_does_not_read_the_scope(self):
  338          names = {
  339              node.id
  340              for node in ast.walk(self.functions["run_child"])
  341              if isinstance(node, ast.Name)
  342          }
  343          self.assertNotIn("build_scope", names)
  344          self.assertNotIn("rehearsal", ast.unparse(self.functions["run_child"]))
### SecondaryGWKit 216e44d prompts/runregistry-extraction/README.md:431
  431    - `ray_temp_dir: in-process` and `ray_address: in-process`;
### SecondaryGWKit 216e44d prompts/runregistry-extraction/README.md:435-436
  435  - **The helper.** From 02a on, each step below is a command of `tools/rehearsal_lock.py`, run as
  436    `PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock <command>`. The helper writes the owner
### SecondaryGWKit 216e44d prompts/runregistry-extraction/README.md:445-446
  445  - **Hold it through all four launches and L3's readers.** It is one lock for the whole rehearsal,
  446    not one per launch: other projects must not start between the launches either.
### SecondaryGWKit 216e44d prompts/runregistry-extraction/README.md:447-448
  447  - **At each launch, set `pid`** with `set-pid <pid>`, using that run's driver pid from its
  448    `status.json`, in the same check that confirms the run started. The readers leave it alone. Between launches the pid is
### SecondaryGWKit 216e44d prompts/runregistry-extraction/README.md:447-450
  447  - **At each launch, set `pid`** with `set-pid <pid>`, using that run's driver pid from its
  448    `status.json`, in the same check that confirms the run started. The readers leave it alone. Between launches the pid is
  449    the previous driver's and is dead. The lock is still held then: only the user removes a lock,
  450    by hand, after looking.
### SecondaryGWKit 216e44d prompts/runregistry-extraction/README.md:458-461
  458  **Ray addresses.** Every Ray driver this protocol runs gets an explicit address and starts its own
  459  instance:
  460  - `quadsource_atol_sweep.py --build` replaces `main.py`'s `ray.init` with `address="local"`;
  461  - `run_readers.sh` passes `--ray-address local`.
### SecondaryGWKit 216e44d prompts/INDEX.md:22
   22  | [`runregistry-extraction`](runregistry-extraction/IMPLEMENTATION_STATE.md) | closed 10 / 10, 2026-10-16 | 2026-10-12 → 2026-10-16 | `RunRegistry/`
### ChamPBH 807f175 requirements.txt:79-80
   79  ray==2.53.0
   80  raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
### ChamPBH 807f175 CLAUDE.md:61-62
   61  - **The packages.** The database layer is `datastorekit` and the work queue is `raypoolkit`, each
   62    pinned to a tag in `requirements.txt` and never installed editable. ChamPBH supplies the registry
### ChamPBH 807f175 CLAUDE.md:128-134
  128  - **Ray on this machine.** A run that needs a cluster here starts ChamPBH's isolated one with
  129    `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh start "<purpose>"` (its own temp dir
  130    and ports, GCS 6380, under the rehearsal lock shared with StochasticInstantons and SecondaryGWKit),
  131    passes `--ray-address 127.0.0.1:6380` to every driver (never `auto`), and stops it with the
  132    script's `stop`. The drivers (`main.py`, `plot_by_beta.py`, `plot_ScalarHistory.py`) refuse to
  133    start Ray without `--ray-address` and refuse `auto` outright (exit 2, before `ray.init`);
  134    `main.py --inventory` starts no Ray and needs none. **No one runs `ray stop`**, which stops every
### ChamPBH 807f175 CLAUDE.md:128-135
  128  - **Ray on this machine.** A run that needs a cluster here starts ChamPBH's isolated one with
  129    `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh start "<purpose>"` (its own temp dir
  130    and ports, GCS 6380, under the rehearsal lock shared with StochasticInstantons and SecondaryGWKit),
  131    passes `--ray-address 127.0.0.1:6380` to every driver (never `auto`), and stops it with the
  132    script's `stop`. The drivers (`main.py`, `plot_by_beta.py`, `plot_ScalarHistory.py`) refuse to
  133    start Ray without `--ray-address` and refuse `auto` outright (exit 2, before `ray.init`);
  134    `main.py --inventory` starts no Ray and needs none. **No one runs `ray stop`**, which stops every
  135    Ray process on the machine, other projects' builds included. The script's `--help` is the detail.
### ChamPBH 807f175 config/argument_parser.py:330-332
  330          help="address of the Ray cluster; required whenever Ray starts (main.py --inventory starts no "
  331          "Ray and needs none). On this machine ChamPBH's cluster is 127.0.0.1:6380; 'local' starts a "
  332          "private instance. 'auto' is refused",
### ChamPBH 807f175 config/argument_parser.py:338-344
  338  RAY_ADDRESS_PROBLEM = (
  339      "!! --ray-address is required whenever Ray starts. Give the address of a running cluster "
  340      "(ChamPBH's on this machine is 127.0.0.1:6380, started by "
  341      ".documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh), or 'local' for a private instance. "
  342      "'auto' is refused: with the projects' clusters isolated, it attaches to whichever cluster it "
  343      "finds first."
  344  )
### ChamPBH 807f175 config/argument_parser.py:341
  341      ".documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh), or 'local' for a private instance. "
### ChamPBH 807f175 ComputeTargets/tests/test_ray_address.py:47
   47          self.assertIn("ray_cluster.sh", message)
### ChamPBH 807f175 RunDrivers/registered_run.py:816-824
  816      _real_ray_init = ray.init
  817      latch = SignalLatch()
  818  
    …
  823  
  824      ray.init = _registered_ray_init
### ChamPBH 807f175 main.py:134
  134  ray.init(address=args.ray_address)
### ChamPBH 807f175 plot_by_beta.py:125
  125  ray.init(address=args.ray_address)
### ChamPBH 807f175 plot_ScalarHistory.py:106
  106  ray.init(address=args.ray_address)
### ChamPBH 807f175 science-runs/2026-10-03-science-2026.6.0/full_run_2026.6.0.sh:4
    4  #   .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh start "<purpose>"
### ChamPBH 807f175 science-runs/2026-10-03-science-2026.6.0/full_run_2026.6.0-refresh.sh:4
    4  #   .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh start "<purpose>"
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:17-23
   17  # ChamPBH's rehearsal cluster, and the rehearsal lock it shares with StochasticInstantons (SI) and
   18  # SecondaryGWKit. Written for dk-and-rpk-migration prompt 05a, under U5 (README section 4.1 and
   19  # section 6.6 of this campaign). Adapted from SI's script at StochasticInstantons commit 3556148
   20  # (.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh), and it keeps the contract of SI's
   21  # .prompts/dk-and-rpk-migration/rehearsal-lock-brief.md at ed9399a: section 2 (the lock) and
   22  # section 3 (the cluster) are followed exactly, because the contract is shared with the other
   23  # projects.
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:21
   21  # .prompts/dk-and-rpk-migration/rehearsal-lock-brief.md at ed9399a: section 2 (the lock) and
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:28
   28  # their parent). It never waits on a held lock, and never removes a lock that is not ChamPBH's.
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:44
   44    start PURPOSE   take the rehearsal lock (~/ScienceData/.rehearsal-lock), then start ChamPBH's Ray
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:44-51
   44    start PURPOSE   take the rehearsal lock (~/ScienceData/.rehearsal-lock), then start ChamPBH's Ray
   45                    head on /tmp/ray-cpbh: GCS 6380, client 6381, dashboard 8267, dashboard agent
   46                    52367, N CPUs (default 10: R0's cluster had 10, Ray's default on this machine,
   47                    and R1 and R2 are compared with R0, wall-clock limits included). PURPOSE is
   48                    written to the lock's owner file, e.g. "dk-and-rpk-migration 06 (R1)". If the
   49                    lock is held, prints its owner file and exits 3, starting nothing. If any of the
   50                    four ports is already held, releases the lock and exits 4, starting nothing.
   51                    Prints the cluster's address and the command that lists its actors.
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:52-57
   52    stop            stop ChamPBH's processes (SIGTERM to every process naming /tmp/ray-cpbh, to
   53                    the Ray client server whose address is 127.0.0.1:6380, and to their
   54                    descendants; a grace period of $RAY_CLUSTER_GRACE seconds, default 15; then
   55                    SIGKILL), confirm none is left and all four ports (6380, 6381, 8267, 52367) are
   56                    free, then release the lock if its owner is ChamPBH's. Touches nothing if the
   57                    lock is another project's.
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:56-57
   56                    free, then release the lock if its owner is ChamPBH's. Touches nothing if the
   57                    lock is another project's.
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:58-59
   58    status          the lock, its owner file, whether the owner's pid is alive, ChamPBH's processes
   59                    and its four ports.
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:65
   65  # ---- ChamPBH's cluster (rehearsal-lock-brief.md, section 3; README section 4.1, U5) ----
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:66-72
   66  LOCK_PROJECT="ChamPBH"
   67  CPBH_TEMP_DIR="/tmp/ray-cpbh"
   68  CPBH_GCS_PORT=6380
   69  CPBH_CLIENT_PORT=6381
   70  CPBH_DASHBOARD_PORT=8267
   71  CPBH_AGENT_PORT=52367
   72  CPBH_ADDRESS="127.0.0.1:${CPBH_GCS_PORT}"
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:66-74
   66  LOCK_PROJECT="ChamPBH"
   67  CPBH_TEMP_DIR="/tmp/ray-cpbh"
   68  CPBH_GCS_PORT=6380
    …
   73  CPBH_DASHBOARD="http://127.0.0.1:${CPBH_DASHBOARD_PORT}"
   74  RAY_BIN="./venv/bin/ray"
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:74
   74  RAY_BIN="./venv/bin/ray"
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:76
   76  # ---- the shared lock (rehearsal-lock-brief.md, section 2) ----
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:77
   77  LOCK_PARENT="$HOME/ScienceData"
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:78
   78  LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:79
   79  OWNER_FILE="$LOCK_DIR/owner"
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:83-84
   83  say() { echo ">> ray_cluster: $*"; }
   84  err() { echo ">> ray_cluster: $*" >&2; }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:86-89
   86  iso_now() {
   87      # ISO 8601, local time with its offset as +HH:MM (macOS date gives +HHMM).
   88      date +%Y-%m-%dT%H:%M:%S%z | sed -E 's/([+-][0-9]{2})([0-9]{2})$/\1:\2/'
   89  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:91-95
   91  owner_field() {
   92      # owner_field KEY: the value of KEY in the owner file ("" if absent or no file).
   93      [ -f "$OWNER_FILE" ] || return 0
   94      sed -n "s/^$1: //p" "$OWNER_FILE" | head -n 1
   95  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:97-108
   97  write_owner() {
   98      # write_owner PURPOSE PID: the seven keys, in the brief's order; written to owner.tmp, renamed.
   99      {
    …
  107      } > "$LOCK_DIR/owner.tmp" && mv "$LOCK_DIR/owner.tmp" "$OWNER_FILE"
  108  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:110-116
  110  print_owner() {
  111      if [ -f "$OWNER_FILE" ]; then
  112          sed 's/^/    /' "$OWNER_FILE"
  113      else
  114          echo "    (no owner file)"
  115      fi
  116  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:118-129
  118  acquire_lock() {
  119      # acquire_lock PURPOSE. mkdir WITHOUT -p: the atomic step. Returns 3 when the lock is held.
  120      mkdir -p "$LOCK_PARENT" || return 1
    …
  128      return 3
  129  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:131-148
  131  release_lock() {
  132      # Release only if the owner's project and ray_temp_dir are ChamPBH's (brief section 2).
  133      if [ ! -d "$LOCK_DIR" ]; then
    …
  147      return 0
  148  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:152-158
  152  temp_dir_regex() {
  153      # temp_dir_regex DIR: an ERE matching DIR in its /tmp and /private/tmp spellings, as a whole
  154      # path component (so /tmp/ray-cpbh does not match /tmp/ray-cpbhx).
  155      local d="${1#/private}"
  156      d="$(printf '%s' "$d" | sed 's/[.]/[.]/g')"
  157      printf '(/private)?%s([/ =]|$)' "$d"
  158  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:152-189
  152  temp_dir_regex() {
  153      # temp_dir_regex DIR: an ERE matching DIR in its /tmp and /private/tmp spellings, as a whole
  154      # path component (so /tmp/ray-cpbh does not match /tmp/ray-cpbhx).
    …
  188          }' | sort -n
  189  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:160-189
  160  list_cluster_pids() {
  161      # list_cluster_pids DIR GCS_PORT: one pid per line: every process whose command line names DIR,
  162      # and every descendant of those. Also the cluster's Ray client server, found on a real
    …
  188          }' | sort -n
  189  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:164
  164      # launchd) and carries no temp dir, only `-m ray.util.client.server --address=127.0.0.1:GCS_PORT`.
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:169
  169      re2="ray[.]util[.]client[.]server --address=127[.]0[.]0[.]1:$2( |\$)"
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:174
  174              p=self; while (p in par && p > 1) { safe[p]=1; p=par[p] }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:174-176
  174              p=self; while (p in par && p > 1) { safe[p]=1; p=par[p] }
  175              for (p in all) {
  176                  if (p in safe) continue
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:177
  177                  if (cmd[p] ~ /ray_cluster[.]sh/) continue
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:184
  184                      if ((par[p] in mark) && !(cmd[p] ~ /ray_cluster[.]sh/)) { mark[p]=1; changed=1 }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:191-263
  191  describe_pid() {
  192      ps -ww -o pid= -o ppid= -o command= -p "$1" 2>/dev/null | cut -c1-150
  193  }
    …
  262      return 0
  263  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:202-263
  202  stop_cluster() {
  203      # stop_cluster DIR GCS_PORT CLIENT_PORT DASHBOARD_PORT AGENT_PORT. Returns 0 when nothing is
  204      # left and all four ports are free. (Prompt 05a, change 3: SI's checks the GCS port alone.)
    …
  262      return 0
  263  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:244-251
  244      left=""
  245      for p in $pids $(list_cluster_pids "$dir" "$port"); do
  246          alive "$p" && left="$left $p"
  247      done
  248      if [ -n "$left" ]; then
  249          err "processes still alive after SIGKILL:$left"
  250          return 1
  251      fi
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:267-338
  267  cmd_start() {
  268      if [ $# -lt 1 ]; then usage >&2; return 2; fi
  269      local purpose="$1" ncpus=10
    …
  337      return 0
  338  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:280
  280      acquire_lock "$purpose" || return $?
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:282-288
  282      # The lock is free but ChamPBH's temp dir is named by a live process: a stale cluster. Not ours to
  283      # guess about; release the lock and say so.
  284      if [ -n "$(list_cluster_pids "$CPBH_TEMP_DIR" "$CPBH_GCS_PORT")" ]; then
  285          err "processes naming $CPBH_TEMP_DIR are already running (a stale cluster?); not starting. Run 'stop' first."
  286          release_lock
  287          return 4
  288      fi
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:286
  286          release_lock
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:290-303
  290      # Prompt 05a, change 4: a held port is not ours to take. Without this, a ray start that fails
  291      # on a foreign listener leaves a stop whose port check cannot pass, and the lock held.
  292      local q held=""
    …
  302          return 4
  303      fi
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:301
  301          release_lock
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:305
  305      trap 'err "interrupted; stopping what was started"; stop_cluster "$CPBH_TEMP_DIR" "$CPBH_GCS_PORT" "$CPBH_CLIENT_PORT" "$CPBH_DASHBOARD_PORT" "$CP
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:307-310
  307      local t0=$SECONDS
  308      "$RAY_BIN" start --head --temp-dir "$CPBH_TEMP_DIR" --port "$CPBH_GCS_PORT" \
  309          --ray-client-server-port "$CPBH_CLIENT_PORT" --dashboard-port "$CPBH_DASHBOARD_PORT" \
  310          --dashboard-agent-listen-port "$CPBH_AGENT_PORT" --num-cpus "$ncpus" --disable-usage-stats
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:311-318
  311      local rc=$?
  312      if [ "$rc" -ne 0 ]; then
  313          err "ray start failed (exit $rc); stopping what it started and releasing the lock"
  314          stop_cluster "$CPBH_TEMP_DIR" "$CPBH_GCS_PORT" "$CPBH_CLIENT_PORT" "$CPBH_DASHBOARD_PORT" "$CPBH_AGENT_PORT"
  315          release_lock
  316          trap - INT TERM
  317          return 1
  318      fi
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:315
  315          release_lock
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:320-330
  320      local gcs
  321      gcs="$(list_cluster_pids "$CPBH_TEMP_DIR" "$CPBH_GCS_PORT" | while read -r p; do
  322          describe_pid "$p" | grep -q 'gcs_server' && echo "$p"
    …
  329          return 1
  330      fi
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:327
  327          release_lock
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:331
  331      write_owner "$purpose" "$gcs"
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:332
  332      trap - INT TERM
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:340-356
  340  cmd_stop() {
  341      local t0=$SECONDS
  342      if [ -d "$LOCK_DIR" ]; then
    …
  355      return 0
  356  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:342-351
  342      if [ -d "$LOCK_DIR" ]; then
  343          local proj tdir
  344          proj="$(owner_field project)"
    …
  350          fi
  351      fi
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:352
  352      stop_cluster "$CPBH_TEMP_DIR" "$CPBH_GCS_PORT" "$CPBH_CLIENT_PORT" "$CPBH_DASHBOARD_PORT" "$CPBH_AGENT_PORT" || return 1
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:353
  353      release_lock || return 1
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:358-385
  358  cmd_status() {
  359      if [ -d "$LOCK_DIR" ]; then
  360          echo "lock: HELD ($LOCK_DIR)"
    …
  384      return 0
  385  }
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:359-370
  359      if [ -d "$LOCK_DIR" ]; then
  360          echo "lock: HELD ($LOCK_DIR)"
  361          print_owner
    …
  369          echo "lock: free ($LOCK_DIR does not exist)"
  370      fi
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:371-379
  371      local pids
  372      pids="$(list_cluster_pids "$CPBH_TEMP_DIR" "$CPBH_GCS_PORT")"
  373      if [ -z "$pids" ]; then
    …
  378          for p in $pids; do describe_pid "$p" | sed 's/^/    /'; done
  379      fi
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:380-383
  380      local q
  381      for q in "$CPBH_GCS_PORT" "$CPBH_CLIENT_PORT" "$CPBH_DASHBOARD_PORT" "$CPBH_AGENT_PORT"; do
  382          if [ -n "$(port_listeners "$q")" ]; then echo "port $q: held"; else echo "port $q: free"; fi
  383      done
### ChamPBH 807f175 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:387-395
  387  main() {
  388      case "${1:-}" in
  389          start) shift; cmd_start "$@" ;;
    …
  394      esac
  395  }
### StochasticInstantons 7071bb8 requirements.txt:58-59
   58  ray==2.55.1
   59  raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
### StochasticInstantons 7071bb8 CLAUDE.md:14-16
   14  `--ray-address` is required by `main.py` and both plot scripts; there is no
   15  `auto` default. Pass `local` for a private in-process Ray instance, or a
   16  cluster's GCS address. Rehearsals and long builds run on SI's isolated cluster
### StochasticInstantons 7071bb8 CLAUDE.md:14-20
   14  `--ray-address` is required by `main.py` and both plot scripts; there is no
   15  `auto` default. Pass `local` for a private in-process Ray instance, or a
   16  cluster's GCS address. Rehearsals and long builds run on SI's isolated cluster
   17  under the shared rehearsal lock: `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh
   18  start PURPOSE`, then `--ray-address 127.0.0.1:6390`. Never run `ray stop`: it
   19  stops every Ray process on the machine, other projects' clusters included (see
   20  `.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md`).
### StochasticInstantons 7071bb8 CLAUDE.md:16-17
   16  cluster's GCS address. Rehearsals and long builds run on SI's isolated cluster
   17  under the shared rehearsal lock: `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh
### StochasticInstantons 7071bb8 CLAUDE.md:16-18
   16  cluster's GCS address. Rehearsals and long builds run on SI's isolated cluster
   17  under the shared rehearsal lock: `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh
   18  start PURPOSE`, then `--ray-address 127.0.0.1:6390`. Never run `ray stop`: it
### StochasticInstantons 7071bb8 CLAUDE.md:20
   20  `.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md`).
### StochasticInstantons 7071bb8 CLAUDE.md:29-30
   29  67 `integration`-marked tests, which need a live Ray instance and a SQLite
   30  store (`RAY_ADDRESS=local pytest -m integration`), and the 69 `slow`-marked
### StochasticInstantons 7071bb8 CLAUDE.md:142-143
  142  `RayWorkPool` is the `raypoolkit` package. Each is pinned to a tag in
  143  `requirements.txt` (`datastorekit` `v0.5.0`, `raypoolkit` `v0.2.0`), installed
### StochasticInstantons 7071bb8 main.py:131
  131  ray.init(address=args.ray_address)
### StochasticInstantons 7071bb8 plot_GradientCoupledSolutions.py:973
  973      ray.init(address=args.ray_address, ignore_reinit_error=True)
### StochasticInstantons 7071bb8 plot_InstantonSolutions.py:1207
 1207      ray.init(address=args.ray_address, ignore_reinit_error=True)
### StochasticInstantons 7071bb8 tests/conftest.py:55
   55      ray.init(ignore_reinit_error=True)
### StochasticInstantons 7071bb8 tests/test_inventory_store.py:80
   80  ray.init(address="local", include_dashboard=False)
### StochasticInstantons 7071bb8 tests/test_inflaton_trajectory_prune.py:464
  464  ray.init(address="local", include_dashboard=False)
### StochasticInstantons 7071bb8 .prompts/dk-and-rpk-migration/rehearsal-lock-brief.md:46
   46  ## 2. The shared lock — identical in every project
### StochasticInstantons 7071bb8 .prompts/dk-and-rpk-migration/rehearsal-lock-brief.md:87
   87  ## 3. Isolating a `ray start` cluster — ChamPBH and SI
### StochasticInstantons 7071bb8 .prompts/dk-and-rpk-migration/rehearsal-lock-brief.md:139
  139  - **Never run `ray stop`** in any project, by any prompt, from now on. A cluster a project did not
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:17-20
   17  # StochasticInstanton's rehearsal cluster, and the rehearsal lock it shares with ChamPBH and
   18  # SecondaryGWKit. Written for dk-and-rpk-migration prompt 01a, which implements
   19  # .prompts/dk-and-rpk-migration/rehearsal-lock-brief.md: section 2 (the lock) and section 3 (the
   20  # cluster) are followed exactly, because the contract is shared with the other projects.
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:19
   19  # .prompts/dk-and-rpk-migration/rehearsal-lock-brief.md: section 2 (the lock) and section 3 (the
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:25
   25  # parent). It never waits on a held lock, and never removes a lock that is not SI's.
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:45
   45    start PURPOSE   take the rehearsal lock (~/ScienceData/.rehearsal-lock), then start SI's Ray
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:45-51
   45    start PURPOSE   take the rehearsal lock (~/ScienceData/.rehearsal-lock), then start SI's Ray
   46                    head on /tmp/ray-si: GCS 6390, client 6391, dashboard 8266, dashboard agent
   47                    52366, N CPUs (default 4). PURPOSE is written to the lock's owner file, e.g.
   48                    "dk-and-rpk-migration 02 (RH0)". If the lock is held, prints its owner file and
   49                    exits 3, starting nothing. If any of the four ports is already held, releases
   50                    the lock and exits 4, starting nothing. Prints the cluster's address and the
   51                    command that lists its actors.
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:52-56
   52    stop            stop SI's processes (SIGTERM to every process naming /tmp/ray-si, to the Ray
   53                    client server whose address is 127.0.0.1:6390, and to their descendants; a grace
   54                    period of $RAY_CLUSTER_GRACE seconds, default 15; then SIGKILL), confirm none is
   55                    left and all four ports (6390, 6391, 8266, 52366) are free, then release the
   56                    lock if its owner is SI's. Touches nothing if the lock is another project's.
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:55-56
   55                    left and all four ports (6390, 6391, 8266, 52366) are free, then release the
   56                    lock if its owner is SI's. Touches nothing if the lock is another project's.
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:57-58
   57    status          the lock, its owner file, whether the owner's pid is alive, SI's processes and
   58                    its four ports.
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:64
   64  # ---- SI's cluster (rehearsal-lock-brief.md, section 3) ----
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:65-71
   65  LOCK_PROJECT="StochasticInstantons"
   66  SI_TEMP_DIR="/tmp/ray-si"
   67  SI_GCS_PORT=6390
   68  SI_CLIENT_PORT=6391
   69  SI_DASHBOARD_PORT=8266
   70  SI_AGENT_PORT=52366
   71  SI_ADDRESS="127.0.0.1:${SI_GCS_PORT}"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:65-73
   65  LOCK_PROJECT="StochasticInstantons"
   66  SI_TEMP_DIR="/tmp/ray-si"
   67  SI_GCS_PORT=6390
    …
   72  SI_DASHBOARD="http://127.0.0.1:${SI_DASHBOARD_PORT}"
   73  RAY_BIN="./venv/bin/ray"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:73
   73  RAY_BIN="./venv/bin/ray"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:75
   75  # ---- the shared lock (rehearsal-lock-brief.md, section 2) ----
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:76
   76  LOCK_PARENT="$HOME/ScienceData"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:77
   77  LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:75-78
   75  # ---- the shared lock (rehearsal-lock-brief.md, section 2) ----
   76  LOCK_PARENT="$HOME/ScienceData"
   77  LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"
   78  OWNER_FILE="$LOCK_DIR/owner"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:76-77
   76  LOCK_PARENT="$HOME/ScienceData"
   77  LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:76-78
   76  LOCK_PARENT="$HOME/ScienceData"
   77  LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"
   78  OWNER_FILE="$LOCK_DIR/owner"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:82-83
   82  say() { echo ">> ray_cluster: $*"; }
   83  err() { echo ">> ray_cluster: $*" >&2; }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:85-88
   85  iso_now() {
   86      # ISO 8601, local time with its offset as +HH:MM (macOS date gives +HHMM).
   87      date +%Y-%m-%dT%H:%M:%S%z | sed -E 's/([+-][0-9]{2})([0-9]{2})$/\1:\2/'
   88  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:90-94
   90  owner_field() {
   91      # owner_field KEY: the value of KEY in the owner file ("" if absent or no file).
   92      [ -f "$OWNER_FILE" ] || return 0
   93      sed -n "s/^$1: //p" "$OWNER_FILE" | head -n 1
   94  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:96-107
   96  write_owner() {
   97      # write_owner PURPOSE PID: the seven keys, in the brief's order; written to owner.tmp, renamed.
   98      {
    …
  106      } > "$LOCK_DIR/owner.tmp" && mv "$LOCK_DIR/owner.tmp" "$OWNER_FILE"
  107  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:109-115
  109  print_owner() {
  110      if [ -f "$OWNER_FILE" ]; then
  111          sed 's/^/    /' "$OWNER_FILE"
  112      else
  113          echo "    (no owner file)"
  114      fi
  115  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:117-128
  117  acquire_lock() {
  118      # acquire_lock PURPOSE. mkdir WITHOUT -p: the atomic step. Returns 3 when the lock is held.
  119      mkdir -p "$LOCK_PARENT" || return 1
    …
  127      return 3
  128  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:130-147
  130  release_lock() {
  131      # Release only if the owner's project and ray_temp_dir are SI's (brief section 2).
  132      if [ ! -d "$LOCK_DIR" ]; then
    …
  146      return 0
  147  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:151-157
  151  temp_dir_regex() {
  152      # temp_dir_regex DIR: an ERE matching DIR in its /tmp and /private/tmp spellings, as a whole
  153      # path component (so /tmp/ray-si does not match /tmp/ray-simple).
  154      local d="${1#/private}"
  155      d="$(printf '%s' "$d" | sed 's/[.]/[.]/g')"
  156      printf '(/private)?%s([/ =]|$)' "$d"
  157  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:151-188
  151  temp_dir_regex() {
  152      # temp_dir_regex DIR: an ERE matching DIR in its /tmp and /private/tmp spellings, as a whole
  153      # path component (so /tmp/ray-si does not match /tmp/ray-simple).
    …
  187          }' | sort -n
  188  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:159-188
  159  list_cluster_pids() {
  160      # list_cluster_pids DIR GCS_PORT: one pid per line: every process whose command line names DIR,
  161      # and every descendant of those. Also the cluster's Ray client server, found on a real
    …
  187          }' | sort -n
  188  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:163
  163      # launchd) and carries no temp dir, only `-m ray.util.client.server --address=127.0.0.1:GCS_PORT`.
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:168
  168      re2="ray[.]util[.]client[.]server --address=127[.]0[.]0[.]1:$2( |\$)"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:173
  173              p=self; while (p in par && p > 1) { safe[p]=1; p=par[p] }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:173-175
  173              p=self; while (p in par && p > 1) { safe[p]=1; p=par[p] }
  174              for (p in all) {
  175                  if (p in safe) continue
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:176
  176                  if (cmd[p] ~ /ray_cluster[.]sh/) continue
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:183
  183                      if ((par[p] in mark) && !(cmd[p] ~ /ray_cluster[.]sh/)) { mark[p]=1; changed=1 }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:190-261
  190  describe_pid() {
  191      ps -ww -o pid= -o ppid= -o command= -p "$1" 2>/dev/null | cut -c1-150
  192  }
    …
  260      return 0
  261  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:201-261
  201  stop_cluster() {
  202      # stop_cluster DIR GCS_PORT CLIENT_PORT DASHBOARD_PORT AGENT_PORT. Returns 0 when nothing is
  203      # left and all four ports are free. All five arguments are required: a call with fewer would
    …
  260      return 0
  261  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:242-249
  242      left=""
  243      for p in $pids $(list_cluster_pids "$dir" "$port"); do
  244          alive "$p" && left="$left $p"
  245      done
  246      if [ -n "$left" ]; then
  247          err "processes still alive after SIGKILL:$left"
  248          return 1
  249      fi
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:265-336
  265  cmd_start() {
  266      if [ $# -lt 1 ]; then usage >&2; return 2; fi
  267      local purpose="$1" ncpus=4
    …
  335      return 0
  336  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:278
  278      acquire_lock "$purpose" || return $?
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:280-286
  280      # The lock is free but SI's temp dir is named by a live process: a stale cluster. Not ours to
  281      # guess about; release the lock and say so.
  282      if [ -n "$(list_cluster_pids "$SI_TEMP_DIR" "$SI_GCS_PORT")" ]; then
  283          err "processes naming $SI_TEMP_DIR are already running (a stale cluster?); not starting. Run 'stop' first."
  284          release_lock
  285          return 4
  286      fi
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:284
  284          release_lock
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:288-301
  288      # A held port is not ours to take. Without this, a ray start that fails on a foreign listener
  289      # leaves a stop whose port check cannot pass, and the lock held.
  290      local q held=""
    …
  300          return 4
  301      fi
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:299
  299          release_lock
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:303
  303      trap 'err "interrupted; stopping what was started"; stop_cluster "$SI_TEMP_DIR" "$SI_GCS_PORT" "$SI_CLIENT_PORT" "$SI_DASHBOARD_PORT" "$SI_AGENT_P
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:305-308
  305      local t0=$SECONDS
  306      "$RAY_BIN" start --head --temp-dir "$SI_TEMP_DIR" --port "$SI_GCS_PORT" \
  307          --ray-client-server-port "$SI_CLIENT_PORT" --dashboard-port "$SI_DASHBOARD_PORT" \
  308          --dashboard-agent-listen-port "$SI_AGENT_PORT" --num-cpus "$ncpus" --disable-usage-stats
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:309-316
  309      local rc=$?
  310      if [ "$rc" -ne 0 ]; then
  311          err "ray start failed (exit $rc); stopping what it started and releasing the lock"
  312          stop_cluster "$SI_TEMP_DIR" "$SI_GCS_PORT" "$SI_CLIENT_PORT" "$SI_DASHBOARD_PORT" "$SI_AGENT_PORT"
  313          release_lock
  314          trap - INT TERM
  315          return 1
  316      fi
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:313
  313          release_lock
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:318-328
  318      local gcs
  319      gcs="$(list_cluster_pids "$SI_TEMP_DIR" "$SI_GCS_PORT" | while read -r p; do
  320          describe_pid "$p" | grep -q 'gcs_server' && echo "$p"
    …
  327          return 1
  328      fi
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:325
  325          release_lock
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:329
  329      write_owner "$purpose" "$gcs"
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:330
  330      trap - INT TERM
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:338-354
  338  cmd_stop() {
  339      local t0=$SECONDS
  340      if [ -d "$LOCK_DIR" ]; then
    …
  353      return 0
  354  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:340-349
  340      if [ -d "$LOCK_DIR" ]; then
  341          local proj tdir
  342          proj="$(owner_field project)"
    …
  348          fi
  349      fi
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:350
  350      stop_cluster "$SI_TEMP_DIR" "$SI_GCS_PORT" "$SI_CLIENT_PORT" "$SI_DASHBOARD_PORT" "$SI_AGENT_PORT" || return 1
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:351
  351      release_lock || return 1
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:356-383
  356  cmd_status() {
  357      if [ -d "$LOCK_DIR" ]; then
  358          echo "lock: HELD ($LOCK_DIR)"
    …
  382      return 0
  383  }
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:357-368
  357      if [ -d "$LOCK_DIR" ]; then
  358          echo "lock: HELD ($LOCK_DIR)"
  359          print_owner
    …
  367          echo "lock: free ($LOCK_DIR does not exist)"
  368      fi
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:369-377
  369      local pids
  370      pids="$(list_cluster_pids "$SI_TEMP_DIR" "$SI_GCS_PORT")"
  371      if [ -z "$pids" ]; then
    …
  376          for p in $pids; do describe_pid "$p" | sed 's/^/    /'; done
  377      fi
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:378-381
  378      local q
  379      for q in "$SI_GCS_PORT" "$SI_CLIENT_PORT" "$SI_DASHBOARD_PORT" "$SI_AGENT_PORT"; do
  380          if [ -n "$(port_listeners "$q")" ]; then echo "port $q: held"; else echo "port $q: free"; fi
  381      done
### StochasticInstantons 7071bb8 .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh:385-393
  385  main() {
  386      case "${1:-}" in
  387          start) shift; cmd_start "$@" ;;
    …
  392      esac
  393  }
```

### 3.8 Links (prompt §3.5)

With the files staged, `$S/scripts/links.py` (every `](…)` outside code that is neither a URL nor an anchor, resolved from its file's directory and looked up in `git ls-files`, which includes the index), run with `/usr/bin/python3 -I` from `$S/empty`:

```text
docs/adoption/rehearsal-lock/secondarygwkit.md: 5 relative links, 5 tracked
docs/adoption/rehearsal-lock/champbh.md: 5 relative links, 5 tracked
docs/adoption/rehearsal-lock/stochasticinstantons.md: 5 relative links, 5 tracked
docs/adoption/rehearsal-lock/switch-over.md: 9 relative links, 9 tracked
prompts/rehearsal-lock/logs/04-the-switch-over-checklists.md: 0 relative links, 0 tracked
prompts/rehearsal-lock/IMPLEMENTATION_STATE.md: 21 relative links, 21 tracked
docs/OPEN_ISSUES.md: 2 relative links, 2 tracked
RESULT: PASS
```

Every relative link in `docs/adoption/rehearsal-lock/` resolves to a tracked file: 24 links. The README anchor `#changes-in-v030` is the heading "Changes in `v0.3.0`" (`README.md:40`).

### 3.9 The real `HOME` and Ray (prompt §3.6)

`~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` absent, and `pgrep -lf
'gcs_server|raylet|ray::'` exit 1, before (20:04), after the transcripts, and after staging
(§3.10). `/tmp/ray-sgk` was never created. Nothing under `/tmp/ray*` was touched.

### 3.10 After staging

Run at 20:32 with the eight files staged, before committing:
- `git diff --cached --name-only`: `docs/OPEN_ISSUES.md`, `docs/adoption/rehearsal-lock/champbh.md`,
  `docs/adoption/rehearsal-lock/secondarygwkit.md`, `docs/adoption/rehearsal-lock/stochasticinstantons.md`,
  `docs/adoption/rehearsal-lock/switch-over.md`, `prompts/INDEX.md`,
  `prompts/rehearsal-lock/IMPLEMENTATION_STATE.md`,
  `prompts/rehearsal-lock/logs/04-the-switch-over-checklists.md`. Nothing under `raypoolkit/`,
  `docs/rehearsal-lock/` or `.github/`, and not `docs/rehearsal-lock.md`, `docs/adoption/`'s
  existing files, `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `pyproject.toml` or the campaign
  README.
- The suite: `Ran 226 tests in 2.253s` `OK`; `black --check raypoolkit docs`: "20 files would be
  left unchanged."
- The clients: as §3.2, identical to before (`diff` of the two records empty).
- Neither lock location under the real `HOME`; `pgrep` exit 1; every scratch `HOME` empty.
- The links: §3.8.

## 4. The deliberate-breakage record

There is no code, so there is no mutation (prompt §3). In its place, §3.3's transcripts: each
command's exit code is compared with the one the documents state, and a difference would print
FAIL and make the script exit non-zero. None did. §3.6's probe does the same for the forms: each
row's verdict is the one SGK's checklist states.

## 5. Observations not acted on

1. **`docs/adoption/README.md` describes `v0.2.0`'s adoption checklists** (clarification 9), and
   the new directory has no README. `switch-over.md` is its entry, links the three checklists, and
   points at the old README as being about `RayWorkPool`. Not changed (prompt §6); not an issue.
2. **SGK's `main` is 342 commits behind `handover-remedial`** and has neither the lock helper nor a
   `raypoolkit` pin. SGK's switch is made on the line that has them; the checklist says so. For SGK.
3. **Four SGK record scripts call the helper** (`docs/handover/a3-v2/launch/scripts/prelaunch.sh`,
   `docs/handover/a3-v2/rehearsal/scripts/{after_run,check_and_setpid,prelaunch}.sh`). They stop
   working when it is deleted. They are records; the checklist counts them. For SGK.
4. **`ray start` writes `<temp dir>/ray_current_cluster` and only `ray stop` removes it** (§3.4).
   CPBH and SI never run `ray stop`, so their temp dirs likely keep the file between clusters. It
   is harmless while their drivers pass an explicit address, and SGK's Advice keeps `_temp_dir`
   with `address="local"`. Not checked on the machine: nothing under `/tmp/ray*` was read.
5. **The contract says "a script that runs the lock's commands names the temp dir in no command line
   of its own"** (§6), while each command takes `--ray-temp-dir D` on its own command line. The
   reading process is never listed and its own descendants are kept out, so its own argument is
   harmless, and the transcripts show it. A client might still misread the sentence; the CPBH and
   SI checklists spell the distinction out. For 05's verification document, perhaps; not an issue.
6. **SGK's readers record no pid**, so under the module the rule alone covers them, and it does not
   list a driver's reaper (contract §6). The reaper was measured to exit at `ray.shutdown()`. SGK's
   checklist names the choice; for SGK.
7. **CPBH runs Ray 2.53.0**, between the module's proven ends. The switch relies on nothing of Ray
   but `ray start --temp-dir`, which CPBH already uses; Ray 2.53.0's source was not read.
8. **The clients' Python versions** are this repository's `CLAUDE.md`'s (3.12 for SGK, 3.13 for
   CPBH and SI); no client venv was read to confirm them.
9. **`status` with no `--ray-temp-dir` and no lock prints `Ray processes: no temp dir given`**, so a
   client's habitual bare `status` (SGK's helper took no options) no longer shows its processes
   when the lock is free. SGK's checklist says to pass the temp dir. Not an issue.

## 6. Issues

**Opened:** `[04-the-proof-takes-the-old-lock]`, on the board's §3 with an **Assigned
(2026-10-24):** line naming 05, and in `docs/OPEN_ISSUES.md` §1.2. `docs/rehearsal-lock/ray_proof.py`
holds the lock at `old_lock_dir()` (`:149`; 02's log §5); after the switch-over a re-run would hold
a lock no project looks at. 05, which re-runs the proof, moves it to the default location first,
or says why not. None narrowed or closed. The index goes from **0** to **1**.

## 7. State handed to the next prompt

- `docs/adoption/rehearsal-lock/` holds `switch-over.md` and the three checklists, measured at SGK
  `216e44d`, CPBH `807f175` and SI `7071bb8` against `v0.3.0`. Each client re-measures before it
  acts. G2 does not hold yet; it is recorded on the board's §2 when the day is done.
- **05** moves `docs/rehearsal-lock/ray_proof.py` to the default location before re-running it
  (`[04-the-proof-takes-the-old-lock]`); part (c)'s default-location `acquire`, refused today as the
  old location, then needs a new expectation. Its verification document can cite this log's
  transcripts for the commands of the switch.
- The scripts and outputs of §3 are in `$S/scripts/` and `$S/out/`, and are not committed.
- The suite is **226**. The index is **1**. Nothing is pushed: local `main` is four commits ahead of
  `origin/main` with this one.
