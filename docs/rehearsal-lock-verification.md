# The rehearsal-lock campaign: verification

**Campaign:** [`prompts/rehearsal-lock/README.md`](../prompts/rehearsal-lock/README.md) ·
**Board:** [`prompts/rehearsal-lock/IMPLEMENTATION_STATE.md`](../prompts/rehearsal-lock/IMPLEMENTATION_STATE.md) ·
**Written by:** [rehearsal-lock prompt 05](../prompts/rehearsal-lock/05-verification-and-close-out.md),
log [`05-verification-and-close-out.md`](../prompts/rehearsal-lock/logs/05-verification-and-close-out.md) ·
**Date:** 2026-10-24 · **Verifies:** the package as tagged **`v0.3.0`**, commit `67a75b9` (tag
object `caf0076`), and the records of prompts 01, 02, 03, 03a and 04, and of 05 itself.
`git diff 67a75b9 -- raypoolkit pyproject.toml` is empty at the commit that adds this document.

*This document is additive from the day it is committed (`CLAUDE.md` rule 6): a later measurement is
added as a new dated subsection, and what is here is not rewritten.*

Every fact below carries a commit, a `path:line` at a named tree, or a command and its output. A
statement of a log is cited by log and section ("log 02 §3.4" is
`prompts/rehearsal-lock/logs/02-prove-it-under-real-ray.md` §3.4); "the board" is the campaign's
`IMPLEMENTATION_STATE.md`, and "README" without a path is the campaign's plan,
`prompts/rehearsal-lock/README.md`. Where this document and a log disagree, it says which is right
and why; it does not rewrite the log. `<scratch>` stands for the scratch directory of prompt 05's
run (`<session scratchpad>/agent05`), outside the repository; `$S` is the same directory in the
commands of §11. `~` is the real `HOME`, `/Users/ds283`, unless a scratch `HOME` is named.

---

## 1. What this document is

**What the campaign set out to do** (README §0, §0.1, §1, §6.1). Three projects share one Ray machine
and one rehearsal lock, so that one rehearsal or long build runs at a time: SecondaryGWKit (SGK) in
`tools/rehearsal_lock.py`, ChamPBH (CPBH) and StochasticInstantons (SI) in their `ray_cluster.sh`,
each an implementation of its own of one brief (README §0). They worked only while all three agreed
byte for byte on the lock's location and owner format, and nothing kept them in step. The user
decided on 2026-10-23 to extract the lock into `raypoolkit` (**D1**), to move it to
`~/.raypoolkit/rehearsal-lock` (**D2**), to switch the three clients over together on one day
(**D3**), and to take phase 1 only, the lock and the process check, not cluster start and stop
(**D4**).

**What it delivered.**
- **The module** `raypoolkit/rehearsal_lock.py` (01, `6733447`): the lock at its new location,
  refusing while the old one exists (U4); the owner file; `acquire`, `set-pid`, `release`, `status`
  and `ray-processes`; one process rule, by Ray temp dir with the client-server seed (U2); standard
  library only; 103 tests and two guard tests (log 01 §1).
- **The proof** `docs/rehearsal-lock/ray_proof.py` (02, `722466a`): the module under real Ray,
  holding the real shared lock, at both tested ends (log 02 §3.4). Changed by 05 to hold the lock at
  both its locations (U7) and run again (§4).
- **The release `v0.3.0`** (03, `89d6875`, and its fix 03a, `67a75b9`): `pyproject.toml` at
  `0.3.0`; the contract [`docs/rehearsal-lock.md`](rehearsal-lock.md); `README.md`,
  `PROVENANCE.md` and `CLAUDE.md` true of it; tagged on `67a75b9` after green CI (§2.3, §5).
- **The switch-over checklists** (04, `127b2b4`):
  [`docs/adoption/rehearsal-lock/`](adoption/rehearsal-lock/switch-over.md), one checklist per
  client measured read-only against `v0.3.0`, and the procedure for the day.
- **This document** and the campaign's close (05).

**The headline.**
- One release, `v0.3.0`, tag object `caf0076` on `67a75b9`, made after CI passed at both ends there
  (run 40121254667). Its wheel, rebuilt offline here, has the 10 entries and `67a75b9`'s five
  modules (§5).
- The suite is **226** at both tested ends, 3.12.15 / Ray 2.43.0 and 3.13.16 / Ray 2.55.1, from 121
  before 01 (§3.1).
- The module has held the real shared lock over real Ray twice: in 02, at the old location, 31
  checks of 31 at both ends (log 02 §3.4); and here, at **both** locations, **46 checks of 46** at
  both ends, leaving no Ray process and neither lock location (§4).
- Four documents tell the three clients how to switch (04).
- **No issue is open.** Two were opened and both resolved (§6).
- **What remains is G2**, the switch-over itself, which each client makes in a campaign of its own
  (§10).

---

## 2. Reconciliation

### 2.1 The prompts

Each prompt landed as one commit, was written in a commit of its own, was dispatched from an
orchestration note (03a excepted: its prompt carries the orchestrator's measurements) and reviewed
in a commit of its own (the board's notes line and its §1 reviews). The suite count is each log's
"after"; the closed and opened issues are the board's §3 and §4.

| Prompt | Commit | Written | Note | Review | Suite after | Closed | Opened |
|---|---|---|---|---|---|---|---|
| 01 | `6733447` | `d7d914d` | `10be4d5` | `2e561e2` | 226 | — | — |
| 02 | `722466a` | `3f1620e` | `ae1e064` | `cc5f2d6` | 226 | — | — |
| 03 | `89d6875` | `6e0ba38` | `8c0dfff` | `b4edd2c` | 226 | — | the review, `[03-the-contract-overstates-two-edges-of-the-module]` |
| 03a | `67a75b9` | `b2ee2b3` | — | `c1164a5` | 226 | `[03-the-contract-overstates-two-edges-of-the-module]` | — |
| 04 | `127b2b4` | `b7c8200` | `a2a8d37` | `6284b3b` | 226 | — | `[04-the-proof-takes-the-old-lock]` |
| 05 | the commit that adds this document | `2861b38` | `636a02a` | — | 226 | `[04-the-proof-takes-the-old-lock]`, and the campaign | — |

The suite went 121 → 226 (01) and stayed 226 (logs 02 §3.1, 03 §3.1, 03a §3.1, 04 §3.1, and §3.1
below). The open count, read as `git show <commit>:docs/OPEN_ISSUES.md`: 0 at `6e559bf`, `6733447`,
`722466a` and `89d6875`; 1 at `b4edd2c` (03's review); 0 at `67a75b9` (03a); 1 at `127b2b4` (04),
`6284b3b`, `2861b38` and `636a02a`; 0 at the commit that adds this document.

### 2.2 Every other commit

`git log --reverse --format='%h %s' 6e559bf^..636a02a` lists **25** commits, from `6e559bf` (the
plan) to `636a02a`, the commit before 05's. Five are the prompts of §2.1. The other 20, by class:

| Class | Count | Commits |
|---|---|---|
| prompt written | 6 | `d7d914d` (01, with U1–U6), `3f1620e` (02, and 01's green CI), `6e0ba38` (03, and 02's green CI), `b2ee2b3` (03a), `b7c8200` (04), `2861b38` (05, with U7) |
| note | 5 | `10be4d5` (01), `ae1e064` (02), `8c0dfff` (03), `a2a8d37` (04), `636a02a` (05) |
| review | 5 | `2e561e2` (01), `cc5f2d6` (02), `b4edd2c` (03), `c1164a5` (03a), `6284b3b` (04) |
| others | 4 | `6e559bf` (the plan), `50d91c7` (phase 2 waits for G2), `2c518ee` (the release record of `v0.3.0`), `74c3d3f` (the user's widening of `CLAUDE.md`'s provenance exception to sources modelled on) |

5 prompts and 6 + 5 + 5 + 4 others: 25. Prompt 05's §0.4 counted 23, to `6284b3b`; `2861b38` (the
prompt) and `636a02a` (its note) landed after it was written, so 25 is the count at 05's commit (log
05 §2, deviation 1).

### 2.3 Tags and CI

`git for-each-ref refs/tags --format='%(refname:short) %(objectname:short) %(*objectname:short)'`:

```text
v0.1.0 0a9cdb2 4e90a8a
v0.2.0 4e7eb15 eaef0ce
v0.3.0 caf0076 67a75b9
```

`v0.3.0` is annotated (message "raypoolkit 0.3.0", `git cat-file -p caf0076`), made on `67a75b9`
after run 40121254667 passed there, on the user's instruction, and pushed (the board, *Release of
`v0.3.0`*, step 4). No tag has moved.

Every run of the `tests` workflow over the campaign, read with `gh run list` and `gh run view` on
2026-10-24: each **completed / success**, both jobs, `suite (low)` (Python 3.12 / Ray 2.43.0) and
`suite (high)` (Python 3.13 / Ray 2.55.1), each suite's verdict `Ran 226 tests` and `OK`, and
`black --check raypoolkit docs` run in the low job (`.github/workflows/tests.yml:48-52`, unchanged
by the campaign).

| Run | Commit | What it ran on | Suite, low / high | `black` |
|---|---|---|---|---|
| [40031056598](https://github.com/ds283/RayPoolKit/actions/runs/40031056598) | `6733447` (01) | the first run over the module and its tests | 226 / 226 | 19 files unchanged |
| [40031383762](https://github.com/ds283/RayPoolKit/actions/runs/40031383762) | `2e561e2` | the review of 01 | 226 / 226 | 19 |
| [40086680695](https://github.com/ds283/RayPoolKit/actions/runs/40086680695) | `cc5f2d6` | the review of 02, pushed with `3f1620e`, `ae1e064` and `722466a`; the first `black` over `ray_proof.py` | 226 / 226 | 20 |
| [40121254667](https://github.com/ds283/RayPoolKit/actions/runs/40121254667) | `67a75b9` (03a) | pushed with 03's commits; then `v0.3.0` was tagged | 226 / 226 | 20 |
| [40121340908](https://github.com/ds283/RayPoolKit/actions/runs/40121340908) | `c1164a5` | the review of 03a | 226 / 226 | 20 |
| [40122144103](https://github.com/ds283/RayPoolKit/actions/runs/40122144103) | `2c518ee` | the release record | 226 / 226 | 20 |
| [40126954690](https://github.com/ds283/RayPoolKit/actions/runs/40126954690) | `6284b3b` | the review of 04, pushed with `74c3d3f`, `b7c8200`, `a2a8d37` and `127b2b4` | 226 / 226 | 20 |

`89d6875`, `722466a` and `127b2b4` have no run of their own: each was pushed with a later commit,
whose run covers its tree. **The commit that adds prompt 05 has no run** (log 05 §2, deviation 1):
`2861b38` and `636a02a` were local when 05 ran (`origin/main` was `6284b3b`), and nothing is pushed
before 05 lands. `2861b38` touches only `prompts/` and `docs/OPEN_ISSUES.md`, and `636a02a` only
`prompts/` (`git show --stat`), so the last run over the package's tree is 40126954690. The proof
never runs in CI. CI will run `black --check` over the changed `ray_proof.py` only once 05's commit
is pushed, which is after its review; locally `black` leaves it unchanged (§3.1). This prompt pushes
nothing, makes no tag and starts no run.

### 2.4 The environment

Every measurement of §3–§5 was made on 2026-10-24, 21:10–21:50 BST, on one machine: macOS 27.0.1
(build 26A434), arm64, `git` 2.56.0, `uv` 0.12.20. Every venv but `venv/` was made by `uv venv`
with its packages installed `--offline` from `uv`'s cache. No network was used but `gh run list`
and `gh run view`.

| Venv | Python | Ray | `raypoolkit` | Used for |
|---|---|---|---|---|
| `venv/` (the repository's) | 3.12.15 | 2.43.0 (no `grpc`) | 0.3.0, editable from the checkout | the suite (low end), `black` 25.1.0 |
| `<scratch>/v243` | 3.12.15 | `ray[default]` 2.43.0, `grpcio` 1.84.1 | editable from the checkout | the proof at the low end; its replays; P1–P4 |
| `<scratch>/v255` | 3.13.16 | `ray[default]` 2.55.1, `grpcio` 1.84.1 | as above | the proof at the high end; its replays; P1–P4; the suite (high end) |

The two scratch venvs were made as 02's (log 02 §3.2), from `/opt/local/bin/python3.12` and
`/opt/local/bin/python3.13`; their `uv pip freeze` lists 57 and 61 packages, `v243`'s equal line for
line to log 02 §3.2's, and `v255`'s the same with `ray==2.55.1` and the four `opentelemetry`
packages (log 05 §3.2). `raypoolkit.__file__` is the checkout's `raypoolkit/__init__.py` in both.

The clients, at the start and at the end of 05's work (`git -C <repo> rev-parse HEAD`, the branch,
`git status --porcelain | shasum` and `git stash list | wc -l`), equal:

| Client | `HEAD` | Branch | Porcelain (hash) | Stash |
|---|---|---|---|---|
| SGK | `216e44d883e78df459c378c3669cf2859ecf11e6` | `handover-remedial` | empty (`da39a3ee5e6b`) | 0 |
| CPBH | `807f17549f55f86c000716597492cf8b286ac982` | `jordan-normalization` | empty (`da39a3ee5e6b`) | 0 |
| SI | `7071bb8452252245ca65b3161681c1a634733878` | `rrk-adoption` | empty (`da39a3ee5e6b`) | 0 |

They are the commits 04's checklists were measured at, so 04's figures still describe them.

---

## 3. Each prompt's acceptance, at `v0.3.0`

The acceptance is README §2's and the prompt's own; the review is the board's §1 paragraph for it,
each of which found "every check … passed" (03's: every check but one part of check 6, which opened
the issue 03a closed). The last column says what holds at `v0.3.0` and how it was re-measured here,
or why it was not.

| Prompt | Acceptance, in brief | What its review found | At `v0.3.0` |
|---|---|---|---|
| 01 | the module to README §4 under U1; every refusal has a test that a named mutation fails, with one reason standing; each client's owner-file shape parses and is judged as §4 says; no test creates anything under the real `HOME` | M1–M14 replayed, each failing exactly the log's count; four mutations of its own each caught; the suite 226 at both ends with `HOME` a scratch directory that stayed empty | **Re-measured:** the suite, 226 at both ends (§3.1), `test_rehearsal_lock` among them; the import guard's two tests in it. `git diff 6733447 67a75b9 -- raypoolkit/rehearsal_lock.py` is empty, so the module the mutations ran against is the tag's. Under real Ray, M10 and M12 fail the proof's records by replay (§4.4). M1–M14 were not re-run against the suite. |
| 02 | the proof, run at both ends under the real shared lock, exits 0; nothing but its stop list signalled; no `ray stop`; its replay fails under M10 and M12 | 31 of 31 at both ends, for the agent and again for the orchestrator; the replays failing as logged | **Re-measured:** the proof, as changed (§4.1), exits 0 with 46 of 46 at both ends, holding both locations (§4.2); 02's own records replay unmutated with exit 0 and fail under M10 and M12 at the checkpoints log 02 §4 names (§4.4). |
| 03 | `pyproject.toml` at `0.3.0`; the contract, naming no client; `README.md`, `PROVENANCE.md`, `CLAUDE.md` true of `v0.3.0`; the release check, 10 entries, none under `raypoolkit/tests/` | every check but two statements of the contract, opened as `[03-…]` | **Re-measured:** the wheel from `git archive v0.3.0` (§5). The contract's statements were not re-read here; its two corrected clauses are 03a's. |
| 03a | `docs/rehearsal-lock.md` §4 and §6 item 4 say what the module does; nothing under `raypoolkit/`; `v0.3.0` on its commit after green CI | every check passed; the probes re-run byte-equal | **Holds:** `v0.3.0` peels to `67a75b9` (§2.3); `rehearsal_lock.py:374-379` at `67a75b9` is the walk the corrected §6 item 4 describes (`pid > 1`). The probes were not re-run. |
| 04 | four documents under `docs/adoption/rehearsal-lock/`, measured read-only against `v0.3.0`; every command run against a scratch `HOME`; each acceptance grep bites | every check passed; two of the note's clarifications wrong and the agent's corrections right | **Re-measured, read only:** each checklist's acceptance grep at its client commit gives the counts the checklists state, SGK **18**, CPBH **5**, SI **5**, and CPBH's and SI's positive grep (`raypoolkit\.rehearsal_lock` in the script) finds nothing today (§3.1). The `path:line`s and transcripts were not re-run. |

### 3.1 What was re-measured here

| Check | Command (from the repository root) | Result |
|---|---|---|
| The suite, low end | `./venv/bin/python -m unittest discover -s raypoolkit/tests -t .` | `Ran 226 tests in 2.165s` / `OK` before any change; `Ran 226 tests in 1.974s` / `OK` after both real runs, with no Ray process up |
| The suite, high end | the same with `<scratch>/v255/bin/python` | `Ran 226 tests in 2.124s` / `OK`, before and after |
| The import guard | in the suite: `test_package_imports`, 5 tests | pass at both ends |
| `black` | `./venv/bin/black --check raypoolkit docs` (25.1.0) | 20 files unchanged, before and after (the changed `ray_proof.py` among them) |
| The package | `git diff 67a75b9 -- raypoolkit pyproject.toml` | empty |
| The acceptance greps (04) | each checklist's item 8 command, at SGK `216e44d`, CPBH `807f175` and SI `7071bb8`, `git grep` only | SGK 18 lines; CPBH 5; SI 5; the positive greps nothing |

---

## 4. The module under real Ray

### 4.1 The proof, as changed (U7)

`docs/rehearsal-lock/ray_proof.py` at `722466a` took the lock at the old location only:
`LOCK_CODE`'s `kw = {"lock_dir": rl.old_lock_dir()} if a["old_location"] else {}` (`:149`), its
preflight's refusal (`:968`), its owner-file reads (`:627-643`), its `release_free_step` (`:1099-1115`)
and its after-both check (`:1374-1386`). That was `[04-the-proof-takes-the-old-lock]`. U7 (the user,
2026-10-24) has it hold **both** locations: before the switch-over the old location is the one every
client sees (and the module refuses beside it, U4); after it the default one is, and the old one
still stops a switched client while U4 stands; once U4's refusal is dropped (README §8) the default
one alone is seen, and the proof still holds it.

The change, at the commit that adds this document (1,615 lines; 05's prompt §2.2 items 1–11):

| Item | What the script does now | Where |
|---|---|---|
| 1 | `LOCK_CODE` reads `location` (`default` or `old`) from its payload and always passes `lock_dir`; any other value is an exit of the child, never a default. The project, purpose strings, temp dirs and addresses are 02's | `ray_proof.py:164-176`, `:138-142` |
| 2 | the preflight's first lines name both locations, and `~ is <HOME>` unabbreviated; it refuses with exit 3, touching nothing, while either exists, printing that location's owner file | `:976-985`, `:1012-1022` |
| 3 | the default location is acquired first, then the old; an `acquire` exiting 3 ends the part with exit 3 after the default location is released through the module (exit 4 if that is refused); any other failure is a failed check; each location's held state is its own | `:1061-1080`, `:1440-1483` |
| 4 | a new check after the two acquires, before the part starts Ray: both owner files exist, each with `project: RayPoolKit`, the part's `ray_temp_dir` and `ray_address`, and `pid: -` | `:1082-1109` |
| 5 | `set_pid`, every refused `release` and every `release` at both locations, old first, each checked as 02 checked it, and each comparing both owner files | `:1111-1158`, `:1181-1206` |
| 6 | `owner_bytes` and `show_owner` read and print both owner files, each labelled with its path | `:660-679` |
| 7 | after a part, `status` at each location says `lock: free (<that location> does not exist)`, no `old location: PRESENT`, and neither location exists; after both parts, neither exists and `~/.raypoolkit` is absent or empty | `:1181-1206`, `:1504-1520` |
| 8 | part (c): the second acquirer at the old location (refused as held) and at the default (refused by the old location); both owner files unchanged; 02's `~/.raypoolkit` comparison dropped | `:1160-1179` |
| 9 | the cleanup releases whichever locations are held, old first; a refusal at either is `LeftHeld` (exit 4), naming the location and going no further | `:1398-1463` |
| 10 | the docstring says what the script holds and why (U7) and names 05 beside 02; the exit statuses keep their meanings | `:2-90` |
| 11 | `--replay` reads a record of either form; 05's record adds `lock_dirs`, `acquire_order`, `release_order` and a per-location `preflight.lock_exists`, and the replay prints which form it read | `:521-530`, `:1539-1549` |

Its witness, checkpoints, signalling rules, refusals, record and replay are 02's: `git diff 722466a`
of the script touches none of `witness`, `evaluate`, `checkpoint`, `stop`, `guard`,
`signal_if_same`, `driver_main` or the replay's evaluation (log 05 §1.1 gives the whole diff's
map). The checks split by location are listed in log 05 §1.1: 02's 31 become 46, 23 in part (a),
22 in part (b) and the after-both check.

### 4.2 The runs

At each end, in the background, from the repository root, with a record path in `<scratch>/runs/`
and a command naming no temp dir:

```bash
env -u PYTHONPATH <scratch>/v243/bin/python docs/rehearsal-lock/ray_proof.py --record <scratch>/runs/proof-2.43.0.json
env -u PYTHONPATH <scratch>/v255/bin/python docs/rehearsal-lock/ray_proof.py --record <scratch>/runs/proof-2.55.1.json
```

Each was made with `git diff -- raypoolkit` empty, checked just before it, and nothing else of the
proof's (no replay, suite, `git apply` or reading of the process table) ran meanwhile (log 05 §2,
deviation 23, records the one exception, a `date` and a `cat`).

| | 2.43.0 before (21:18:51) | 2.43.0 after (21:20:14) | 2.55.1 before (21:20:31) | 2.55.1 after (21:21:58) |
|---|---|---|---|---|
| `pgrep -lf 'gcs_server\|raylet\|ray::'` | exit 1, nothing | exit 1, nothing | exit 1, nothing | exit 1, nothing |
| `~/ScienceData/.rehearsal-lock` | does not exist | does not exist | does not exist | does not exist |
| `~/.raypoolkit/rehearsal-lock` | does not exist | does not exist | does not exist | does not exist |
| `~/.raypoolkit` | does not exist | exists, empty | exists, empty | exists, empty |
| ports 6420, 6421, 8270, 52370, 8265 | no listener | no listener | no listener | no listener |
| `RAY_*` in the environment | none | — | none | — |

`~/.raypoolkit` was made by the low-end run's first default-location `acquire`
(`rehearsal_lock.py:449` at `67a75b9`, `d.parent.mkdir(parents=True, exist_ok=True)`) and is left,
empty, as 05's prompt §0.1 and `switch-over.md` §2 say: it is not the lock. `~/ScienceData` holds
the two entries it held before.

| Run | Wall clock | The script's own time | Exit | Checks |
|---|---|---|---|---|
| 3.12.15 / 2.43.0 | 21:18:57 → 21:20:06 | 67.9 s (part (a) 21.9 s, part (b) 44.3 s) | **0** | 46 PASS, 0 FAIL |
| 3.13.16 / 2.55.1 | 21:20:37 → 21:21:51 | 72.9 s (part (a) 23.0 s, part (b) 48.0 s) | **0** | 46 PASS, 0 FAIL |

Each run's summary, its last lines as printed:

```text
== after both parts
PASS after-both: existing: neither location; ~/.raypoolkit exists (before: does not exist), holding nothing

Summary: 46 checks passed, 0 failed; exit 0; 67.9 s in all
```

```text
== after both parts
PASS after-both: existing: neither location; ~/.raypoolkit exists (before: exists), holding nothing

Summary: 46 checks passed, 0 failed; exit 0; 72.9 s in all
```

The whole output of each run is in log 05 §3.4. The records' SHA-256 are `4e3b61cc…2b12f2`
(2.43.0) and `1054b018…7079d3` (2.55.1); they stay in `<scratch>/runs/` and are not committed.

### 4.3 The roles at each checkpoint, against 02's

Counted from the four records by a scratch script (log 05 §3.5): the witness, the live and the
offline listings, and, in part (b), the listings without the address.

| Checkpoint | 02, 2.43.0 | 05, 2.43.0 | 02, 2.55.1 | 05, 2.55.1 |
|---|---|---|---|---|
| a1 | witness 11 (the reaper, 3 `ray::`); listings 10; task workers 2 of 2 | the same (task workers 1 of 1: Ray ran the four tasks in one worker) | witness 11 (the reaper, 5 `ray::`); listings 10; 2 of 2 | the same |
| a2, a3 | empty; the reaper gone after `ray.shutdown()` | the same | the same | the same |
| b1, b3 | 8, the client server among them (7 without the address); 6 children of `launchd` | the same | 18 (17); 6 children of `launchd`, the dashboard's 10 `multiprocessing` children | the same |
| b2 | 11 (10), 3 `ray::` | the same | 21 (20), 5 `ray::` | the same |
| the stop | 8 listed; 8 `SIGTERM`; `gcs_server` and `monitor.py` `SIGKILL`ed after the 15 s grace | the same | 18 listed; 7 gone by their turn; 11 `SIGTERM`; the same two `SIGKILL`ed | 18 listed; 8 gone by their turn; 10 `SIGTERM`; the same two `SIGKILL`ed |
| b4 | empty; the four ports free | the same | the same | the same |

Every checkpoint passed at both ends with the live and offline listings equal to the witness (less
the reaper at a1), as in 02. No process was signalled whose command was not the one recorded at b3
("not the recorded one" printed nowhere); no `ray stop` was run; the drivers exited by `exit`.

**The lock at both locations, at each end, as printed:** each part acquired the default location and
then the old one, each exit 0; both owner files carried the part's values and `pid: -`; each
refused `release` was refused at both, with both owner files unchanged; `set_pid` changed the one
`pid:` line of each file and nothing else; the second acquirer was refused at the old location as
held and at the default as the old location; each part released the old location and then the
default, each exit 0, and `status` at each then said `lock: free`.

### 4.4 The replays

Each record replayed with `--replay`, `HOME` a fresh scratch directory that was empty afterwards,
the two mutations applied to `raypoolkit/rehearsal_lock.py` exactly as 02 applied them
(`<scratch>/from02/m10.diff`, SHA-256 `4a87ba4e…03b29f`, and `m12.diff`, `0ac88838…04cf65`, equal to
log 02 §4's table), each `git apply --check`ed before and `-R --check`ed after, and reverted; the
module's SHA-256 (`92754f2e…bb7f50`) and `git status` equal before and after each.

| Record | Unmutated | M10 (the descendant walk removed) | M12 (the client-server seed removed) |
|---|---|---|---|
| 05, 2.43.0 (05's form) | exit 0 | exit 1: FAIL a1, b2 | exit 1: FAIL b1, b2, b3 |
| 05, 2.55.1 (05's form) | exit 0 | exit 1: FAIL a1, b1, b2, b3 | exit 1: FAIL b1, b2, b3 |
| 02, 2.43.0 (02's form) | exit 0 | exit 1: FAIL a1, b2 | exit 1: FAIL b1, b2, b3 |
| 02, 2.55.1 (02's form) | exit 0 | exit 1: FAIL a1, b1, b2, b3 | exit 1: FAIL b1, b2, b3 |

Each failure is the one log 02 §4 names for its end, for the reason it gives: under M10 the offline
listing loses every `ray::` process at a1 and b2 and, at 2.55.1, the dashboard's children and the two
agents at b1 and b3; under M12 it loses the client server at b1–b3.

### 4.5 The breakage of the change

Each run with `HOME` a fresh, empty scratch directory, at both ends, starting no Ray (the preflight
still required no Ray process and the four ports free, and found them so). P1 and P2 are diffs of
`ray_proof.py` applied with `git apply`, run, and reverted (log 05 §4 gives each as applied); P3 and
P4 are the unmutated script with a directory made at one location of the scratch `HOME`.

| | What | Reaches Ray? | Result, 2.43.0 and 2.55.1 | Scratch `HOME` after |
|---|---|---|---|---|
| P1 | `ACQUIRE_ORDER = ("default",)`: the old location's `acquire` dropped | no: the check fails inside `acquire_step`, which part (a) calls before its `pre_pids` reading and its driver (`:1221-1228`) | `FAIL a1-acquire-owner-files: the old location has no owner file`; the cleanup releases the default location (exit 0); exit **1**; 1 check passed, 1 failed | `.raypoolkit/`, empty |
| P2 | `ACQUIRE_ORDER = ("old",)`: the default location's `acquire` dropped | no, as P1 | `FAIL a1-acquire-owner-files: the default location has no owner file`; the cleanup releases the old location; exit **1** | `ScienceData/`, empty |
| P3 | a directory at `~/.raypoolkit/rehearsal-lock` | no: the preflight returns before part (a) | `REFUSED: the shared lock exists at its default location (…); its owner file: (no owner file)`; exit **3** | the directory made, and nothing else: nothing at the old location |
| P4 | a directory at `~/ScienceData/.rehearsal-lock` | no, as P3 | the same at the old location; exit **3** | the directory made, and nothing else: nothing at the default location |

Each shows what it was made to: the new check is the one that holds the two locations together
before any Ray starts (P1, P2), and the cleanup releases exactly what was taken; the preflight looks
at both locations (P3, P4). Beyond the prompt, a scratch harness drove the path of clarification 4
offline (log 05 §3.3): with the old location made between the two acquires, the default location was
released and the run exited 3; with the default's owner file then changed, its release was refused
and the run exited 4, leaving both as they were; and `LOCK_CODE` given an unknown location (or 02's
payload) exited 1, touching nothing.

---

## 5. The release

**The release record** (the board, *Release of `v0.3.0`*), step by step:
1. `git push origin 67a75b9:main`, carrying 03's and 03a's commits;
2. run 40121254667 on `67a75b9`, both jobs green;
3. `c1164a5`, the review of 03a, pushed: run 40121340908 green;
4. the tag `v0.3.0`, annotated (`caf0076`, "raypoolkit 0.3.0"), on `67a75b9`, pushed on the user's
   instruction; `git ls-remote origin` showed it peeling to `67a75b9`;
5. a client's install from the tag (`uv pip install --no-cache "raypoolkit @
   git+https://github.com/ds283/RayPoolKit@v0.3.0" "ray==2.55.1"`, fresh 3.13.16 venv):
   `direct_url.json` names `v0.3.0` and `67a75b9…`; the five modules byte-equal to the tag's, no
   `tests/`; `version` `0.3.0`, `requires` `['ray>=2.43']`; `status` against a scratch `HOME` exits 0.

That install is not repeated here (05's prompt §0.3; no network).

**The wheel, rebuilt offline** from `git archive v0.3.0` in an empty scratch directory with
`uv build --wheel --offline`: exit 0; `grep -c "absent from"` of the build log 0;
`raypoolkit-0.3.0-py3-none-any.whl`, **21,368 bytes**, `unzip -l`:

```text
    26152  raypoolkit/RayWorkPool.py
      740  raypoolkit/__init__.py
     2373  raypoolkit/_timing.py
     1886  raypoolkit/contract.py
    27043  raypoolkit/rehearsal_lock.py
    11357  raypoolkit-0.3.0.dist-info/licenses/LICENSE
      285  raypoolkit-0.3.0.dist-info/METADATA
       91  raypoolkit-0.3.0.dist-info/WHEEL
       11  raypoolkit-0.3.0.dist-info/top_level.txt
      814  raypoolkit-0.3.0.dist-info/RECORD
---------
    70752  10 files
```

**10 entries**, none under `raypoolkit/tests/`. Each of the five modules, `unzip -p` against
`git show 67a75b9:raypoolkit/<module>`, is byte-equal (`cmp`). This matches the board's review of
03, check 4 ((R1') and (R2'): 21,368 bytes, 10 entries), and 05's prompt §0.3.

---

## 6. Issues

Two were opened in the campaign, and both are resolved (the board's §4). **None is open.**

| Issue | Opened | Closed | What guards it now |
|---|---|---|---|
| `[03-the-contract-overstates-two-edges-of-the-module]`: §4's `//` and §6 item 4's pid 1 overstated the module | the review of 03 (`b4edd2c`) | 03a, `67a75b9`, before the tag | the corrected clauses of `docs/rehearsal-lock.md` §4 and §6 item 4, resting on log 03a §3.3's probes P-a and P-b; no test pins either edge (log 03a §5.4) |
| `[04-the-proof-takes-the-old-lock]`: the proof held the old location only | 04, `127b2b4` | 05, the commit that adds this document | the proof's both-location acquire and owner-files check, run at both ends (§4.2), and P1–P4 (§4.5) |

---

## 7. Decisions

| Decision | What | When, by | For | Where applied |
|---|---|---|---|---|
| **D1** | extract the shared rehearsal lock into RayPoolKit | 2026-10-23, the user | the campaign | `raypoolkit/rehearsal_lock.py` (01) |
| **D2** | the lock at `~/.raypoolkit/rehearsal-lock` | 2026-10-23, the user | 01 | `default_lock_dir()` (`rehearsal_lock.py:102` at `67a75b9`) |
| **D3** | the three clients switch together, on one day; no transitional release | 2026-10-23, the user | 04 | `switch-over.md` |
| **D4** | phase 1 only: the lock and the process check, not cluster start and stop | 2026-10-23, the user | the campaign | README §1, §8 (phase 2 waits for G2, `50d91c7`) |
| **U1** | the module run as `python -m raypoolkit.rehearsal_lock`; no console script | 2026-10-23, the user, as recommended | 01 | the module; the contract §2 |
| **U2** | one process rule, by Ray temp dir; SGK gives its in-process instances a temp dir | 2026-10-23, as recommended | 01, 04 | `ray_processes` (`rehearsal_lock.py:331`); SGK's checklist item 4 |
| **U3** | no lazy import of `RayWorkPool`: the eager root import kept | 2026-10-23, as recommended | 01 | `raypoolkit/__init__.py` unchanged since `v0.2.0` |
| **U4** | `acquire` refuses while the old location exists, in `0.3.x` | 2026-10-23, as recommended | 01 | `rehearsal_lock.py:435-447`; dropped after G2 (README §8) |
| **U5** | no environment override of the location; `lock_dir` keyword for tests and the proof | 2026-10-23, as recommended | 01 | `_resolve` (`rehearsal_lock.py:112`); the command line has no option |
| **U6** | the release is `v0.3.0` | 2026-10-23, as recommended | 03 | the tag `v0.3.0` |
| **U7** | the proof holds both lock locations, the default first | 2026-10-24, the user, as recommended | 05 | `ray_proof.py` (§4.1) |
| `ray[default]` venvs | the proof runs in two `ray[default]` scratch venvs, `venv/` keeping the suite and `black` | 2026-10-24, the user, before 02's dispatch | 02, and 05 | log 02 §2 deviation 1; §2.4 here |

---

## 8. Deviations across the campaign

**How they were counted.** An entry is a top-level numbered item of a log's §2, "Deviations from
the prompt". Its class is the label in its text; where the label is not in the item, the class is
the one the section's opening sentence gives it (log 02: "Each is an IMPLEMENTATION CHOICE at the
orchestrator's direction unless it says otherwise", covering its items 2–13). An item that says it is
not a deviation (log 01 item 3; log 03 items 3 and 4; log 04 item 12) is counted apart. A sentence
saying there was none ("No UNINTENDED DRIFT was found", logs 01, 02, 03 and 03a) is not an entry. A
scratch parser listed each entry with the labels in its text, and every entry without one was read
(log 05 §3.9).

| Log | Entries | STRUCTURALLY REQUIRED | IMPLEMENTATION CHOICE | UNINTENDED DRIFT | Not a deviation |
|---|---|---|---|---|---|
| 01 | 21 | 2 | 18 | 0 | 1 |
| 02 | 24 | 2 | 22 | 0 | 0 |
| 03 | 20 | 1 | 17 | 0 | 2 |
| 03a | 8 | 1 | 7 | 0 | 0 |
| 04 | 21 | 6 | 13 | 1 | 1 |
| **01–04** | **94** | **12** | **77** | **1** | **4** |
| 05 | 23 | 1 | 21 | 1 | 0 |
| **All** | **117** | **13** | **98** | **2** | **4** |

Prompt 05's §0.4 gave 1 / 16 / 1, 2 / 10 / 1, 1 / 17 / 1, 1 / 7 / 1 and 4 / 11 / 1 for logs 01, 02,
03, 03a and 04. Those are counts of the labels' words, line by line, and the parser reproduces them
exactly. They are not counts of entries: a label wrapped across two lines is not seen by a
line-by-line count (log 01's second STRUCTURALLY REQUIRED, three of its IMPLEMENTATION CHOICEs; two
of log 04's STRUCTURALLY REQUIREDs and two of its IMPLEMENTATION CHOICEs); one sentence classes
twelve of log 02's entries; and "No UNINTENDED DRIFT was found" is a word but not an entry.

**Every UNINTENDED DRIFT entry**, each in process only:
- **log 04 §2 item 21**: a grep of this repository for the SGK temp dir printed four lines of the
  orchestrator's note for 04, which the agent was not to read; nothing in the documents rests on
  them, and the check was re-run without that grep.
- **log 05 §2 item 23**: during the low-end real run one shell command ran `date`, and another
  `date` and `cat` of the run's time file, where the note asked that nothing else run; neither reads
  the process table, names a temp dir, or touches the lock or the module.

**Every STRUCTURALLY REQUIRED entry that changed what a prompt delivered.** The other four changed a
procedure, not a delivered file: log 01 item 21 (M9 is caught by two reverse-direction tests, not the
named one), log 02 item 1 and log 04 item 20 (which venv ran what), and log 05 item 1 (no CI run on
05's prompt commit; this document's count of 25).

| Log, item | What it changed |
|---|---|
| 01 §2 item 12 | `set_pid(…, 0)` raises `ValueError` and `set-pid … 0` exits 2, where SGK's returned 1 |
| 02 §2 item 14 | the proof's offline listing uses `self_pid=-1`, not the prompt's `0`, since `launchd`'s ppid is 0 on macOS |
| 03 §2 item 1 | the contract's Python API is the module's: `ray_processes_command` the fifth command function, a bad argument `ValueError`, not 2 |
| 03a §2 item 1 | the contract's §6 item 4 says "every descendant of pid 1 outside that set", not "every process" |
| 04 §2 item 1 | SGK's checklist covers a third in-process start, `run_child`'s wrapper |
| 04 §2 item 2 | SGK's checklist says what `test_build_rehearsal_scope` really rejects (`ast.unparse` drops comments) |
| 04 §2 item 3 | the acceptance greps name the script and are extended until they bite |
| 04 §2 item 4 | CPBH's and SI's grep matches the brief's §2 citations, not its name |
| 04 §2 item 8 | SGK's checklist's example of a test that starts Ray is corrected: none does |

---

## 9. Observations not acted on

Every item of every log's "Observations not acted on" section, **39** in all (01 §5: 8, 02 §5: 8,
03 §5: 9, 03a §5: 5, 04 §5: 9; the bullets or numbered items of each section). The disposition at
`v0.3.0` is decided from the later logs, the board and a read of `67a75b9`, and changes nothing.

| Log, item | Observation | At `v0.3.0` |
|---|---|---|
| 01 §5.1 | `PACKAGE_MODULES` is a fixed tuple; the lock module's header is covered by `TestLicenceHeader` | **still so** (`test_inherited_faults.py:35` at `67a75b9`) |
| 01 §5.2 | no leading boundary: the rule matches a longer path ending in the temp dir | **addressed** by 03: the contract §6 states the match as "contains … followed by" |
| 01 §5.3 | `/` passes the temp-dir checks and over-lists | **addressed** by 03: the contract states it (log 03 §2 item 4) |
| 01 §5.4 | pid 1 is not in the safe set | **addressed** by 03a: the contract §6 item 4 says so; the module's docstrings still do not (03a §5.1, below) |
| 01 §5.5 | a file at the lock path: `acquire` 3, `release` 0, `status` free | **addressed** by 03: the contract §3, §7, §8 (log 03 §5.1) |
| 01 §5.6 | `hostname -s` about 0.27 s a call | **still so**; not re-measured |
| 01 §5.7 | SI's `HEAD` had moved; 01 read SI at `8b4f615` | **addressed** by 04: G1 re-measured at SI `7071bb8`, `ray_cluster.sh` still blob `6c8eada` (the board's §2) |
| 01 §5.8 | `python -m raypoolkit.rehearsal_lock` imports Ray (U3) | **still so**, decided; the contract §2 gives the cost |
| 02 §5.1 | `self_pid=0` holds back the whole table on macOS | **addressed** by 03: the contract §2 calls `self_pid` a test seam no caller passes |
| 02 §5.2 | an in-process instance under `ray[default]` starts a dashboard on 8265 | **addressed** by 03 (the contract §10) and 04 (SGK's checklist) |
| 02 §5.3 | `gcs_server` and `monitor.py` ignore `SIGTERM` | **still so**: both outlived it at both ends here and were `SIGKILL`ed after the grace (§4.3) |
| 02 §5.4 | the reaper exits at `ray.shutdown()` | **still so**: a2 "gone" at both ends here (§4.3) |
| 02 §5.5 | 01's `TREE_243` misattributes two seed scripts | **still so**; the tests are unchanged since `6733447` |
| 02 §5.6 | the module's process lines cut at 150 characters, a long venv path filling them | **still so**, cosmetic; the same lines here |
| 02 §5.7 | the proof needs a `ray[default]` venv | **addressed**: 05 ran it in two (§2.4) |
| 02 §5.8 | `ray start`'s output carries ANSI colour codes | **still so** in 05's runs; log 05 strips them as 02's did |
| 03 §5.1 | a non-directory at the lock's path reads as free | **still so**, as the contract states it |
| 03 §5.2 | `CLAUDE.md`'s first exception reads "imported from" | **addressed** by the user's widening, `74c3d3f` ("modelled on") |
| 03 §5.3 | the repository's `raypoolkit.egg-info/SOURCES.txt` lists 10 test files, not `test_rehearsal_lock.py` | **still so** (`grep -c tests` 10, rewritten by 05's editable installs); the wheel of §5 has none |
| 03 §5.4 | a failed `rmdir` in `release` leaves a lock with no owner file | **still so**, as the contract §7 states it |
| 03 §5.5 | the proof takes the lock at the old location | **addressed**: opened by 04 as `[04-the-proof-takes-the-old-lock]`, closed by 05 (§4.1) |
| 03 §5.6 | the import costs more than README §0.3 measured | **still so**; not re-measured |
| 03 §5.7 | an empty owner file prints one empty line in `status` | **still so**, as the contract §8 states it |
| 03 §5.8 | `pip`'s editable reinstall built its wheel under the system temp directory | **still so**; a record |
| 03 §5.9 | one scratch file of 03's written to `/tmp` and removed | **still so**; a record of 03's run |
| 03a §5.1 | the module's docstrings make the old pid 1 claim (`rehearsal_lock.py:63-64`, `:345-347`) | **still so** at `67a75b9`; a known gap (§10) |
| 03a §5.2 | `PROVENANCE.md:102` repeats it | **still so**; a known gap (§10) |
| 03a §5.3 | a temp dir starting `//private/` is matched only as spelled | **still an observation**; the contract's "never start the temp dir with `//`" covers it |
| 03a §5.4 | no test pins either corrected edge | **still so**; the probes are the record |
| 03a §5.5 | on Linux, kernel threads do not descend from pid 1 | **still so**; the rule is proven under real Ray on macOS only (§10) |
| 04 §5.1 | `docs/adoption/README.md` describes `v0.2.0`'s checklists | **still so**; `switch-over.md` is the new directory's entry |
| 04 §5.2 | SGK's `main` is 342 commits behind `handover-remedial` | **still so**, SGK's; its checklist says where to switch |
| 04 §5.3 | four SGK record scripts call the old helper | **still so**, SGK's |
| 04 §5.4 | `ray start` writes `<temp dir>/ray_current_cluster`, removed only by `ray stop` | **still unverified**: nothing under `/tmp/ray*` was read here beyond listing the session directories |
| 04 §5.5 | the contract's "names the temp dir in no command line of its own" can be misread | **still so**: the reading process and its own descendants are never listed, so a lock command's own `--ray-temp-dir` argument is harmless (contract §6 item 4); recorded here for a reader |
| 04 §5.6 | SGK's readers record no pid | **still so**, SGK's |
| 04 §5.7 | CPBH runs Ray 2.53.0, between the proven ends | **still unproven**; a known gap (§10) |
| 04 §5.8 | the clients' Python versions were not read from a client venv | **still unverified** |
| 04 §5.9 | a bare `status` with no lock shows no client's processes | **still so**; SGK's checklist says to pass the temp dir |

Tally, by the last column's first words: **10 addressed** (by a prompt, a review or a decision),
**0 no longer true**, and **29 still so, still an observation, still unverified or still unproven**.
Each of the 29 was left as an observation by its log, and no later log or review opened it as an
issue; neither does this prompt.

---

## 10. Known gaps

- **G2: no client has switched.** All three still use their own lock at
  `~/ScienceData/.rehearsal-lock` and pin `v0.2.0`. Each switches in a campaign of its own, on one
  day, by its checklist and `switch-over.md`. The checklists are measured at SGK `216e44d`, CPBH
  `807f175` and SI `7071bb8`, commits that will move; each client re-measures before it acts. After
  the close, G2 is recorded on the board when it holds, in a records commit of its own.
- **U4's refusal stays** in `0.3.x`: while anything exists at `~/ScienceData/.rehearsal-lock`, every
  `acquire` refuses. It is dropped by a release after G2 (README §8).
- **Phase 2, the cluster**, waits for G2 (README §8; `50d91c7`).
- **What remains unproven.**
  - **Ray between the ends**: CPBH runs Ray 2.53.0 (log 04 §5.7); the proof ran at 2.43.0 and
    2.55.1 only.
  - **Any platform but macOS**: the process rule has met real Ray only here. The suite runs on
    Ubuntu in CI, but reads no real `ps`.
  - **A multi-node cluster**: each run is one machine.
  - **Python 3.14 and Ray above 2.55.1**, inside the declared range (`>=3.12`, `ray>=2.43`) and
    untested.
- **What the module's own text omits.** The docstrings at `rehearsal_lock.py:63-64` and `:345-347`
  (at `67a75b9`) and `PROVENANCE.md:102` say this process's ancestors are never listed, without 03a's
  pid 1 exception (the board's review of 03a; log 03a §5.1–§5.2). The contract is right; the
  docstrings change only in a later release.

---

## 11. Reproduction

From a clean checkout of the commit that adds this document, at the repository root, with no Ray
process up (`pgrep -lf 'gcs_server|raylet|ray::'` empty), neither lock location present, the four
ports free and no `RAY_*` variable. `S` is an empty scratch directory outside the repository and
outside `/tmp/ray*`; every `uv` command is offline; run the commands in `bash`.

### 11.1 The suite and the checks (§3.1)

```bash
./venv/bin/python -m unittest discover -s raypoolkit/tests -t .
./venv/bin/black --check raypoolkit docs
git diff 67a75b9 -- raypoolkit pyproject.toml

uv venv -p /opt/local/bin/python3.12 $S/v243
uv pip install --offline --python $S/v243/bin/python -e . "ray[default]==2.43.0" "black==25.1.0"
uv venv -p /opt/local/bin/python3.13 $S/v255
uv pip install --offline --python $S/v255/bin/python -e . "ray[default]==2.55.1" "black==25.1.0"
$S/v255/bin/python -m unittest discover -s raypoolkit/tests -t .

C=/Users/ds283/Documents/Code
git -C $C/SecondaryGWKit grep -n -E 'ScienceData|\.rehearsal-lock|rehearsal-lock-brief|tools\.rehearsal_lock|rehearsal_lock\.py' 216e44d -- . ':!docs' ':!prompts' | wc -l
P='ScienceData|\.rehearsal-lock|rehearsal-lock-brief\.md, section 2|section 2 \(the lock\)'
for c in ChamPBH:807f175 StochasticInstantons:7071bb8; do
  IFS=: read n h <<< "$c"
  { git -C $C/$n grep -n -E "$P" $h -- . ':!.documents' ':!.prompts' ':!prompts' ':!science-runs'
    git -C $C/$n grep -n -E "$P" $h -- .documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh; } | wc -l
done
```

### 11.2 The proof (§4.2)

Each in the background, one after the other, with nothing else running, and the state of §4.2's
table read before and after:

```bash
env -u PYTHONPATH $S/v243/bin/python docs/rehearsal-lock/ray_proof.py --record $S/runs/proof-2.43.0.json
env -u PYTHONPATH $S/v255/bin/python docs/rehearsal-lock/ray_proof.py --record $S/runs/proof-2.55.1.json
```

The run holds the real shared lock at both locations for about a minute, so every project's
`acquire` refuses meanwhile. Exit 3 means a lock was there: stop and ask the user. Exit 4 means the
lock is left held: stop and ask the user.

### 11.3 The replays and the breakage (§4.4, §4.5)

Every command below with `HOME` a fresh, empty directory under `$S` (here `$S/home-<name>`), and
listed afterwards. `m10.diff` and `m12.diff` are log 02 §4's M10 and M12, `p1.diff` and `p2.diff`
log 05 §4's:

```bash
for m in none m10 m12; do
  [ $m = none ] || { git apply --check $S/$m.diff && git apply $S/$m.diff && git apply -R --check $S/$m.diff; }
  for e in 2.43.0:v243 2.55.1:v255; do
    IFS=: read r v <<< "$e"
    mkdir $S/home-$m-$r && HOME=$S/home-$m-$r env -u PYTHONPATH $S/$v/bin/python docs/rehearsal-lock/ray_proof.py --replay $S/runs/proof-$r.json; echo "exit=$?"
  done
  [ $m = none ] || git apply -R $S/$m.diff
done
shasum -a 256 raypoolkit/rehearsal_lock.py   # 92754f2e…bb7f50

for p in p1 p2; do
  git apply --check $S/$p.diff && git apply $S/$p.diff && git apply -R --check $S/$p.diff
  mkdir $S/home-$p && HOME=$S/home-$p env -u PYTHONPATH $S/v243/bin/python docs/rehearsal-lock/ray_proof.py --record $S/$p.json; echo "exit=$?"
  git apply -R $S/$p.diff; ls -A $S/home-$p
done
mkdir -p $S/home-p3/.raypoolkit/rehearsal-lock && HOME=$S/home-p3 env -u PYTHONPATH $S/v243/bin/python docs/rehearsal-lock/ray_proof.py --record $S/p3.json; echo "exit=$?"
mkdir -p $S/home-p4/ScienceData/.rehearsal-lock && HOME=$S/home-p4 env -u PYTHONPATH $S/v243/bin/python docs/rehearsal-lock/ray_proof.py --record $S/p4.json; echo "exit=$?"
```

Unmutated 0; M10 and M12 1, failing as §4.4's table; P1 and P2 1; P3 and P4 3. 02's records, kept
in its agent's scratch directory, replay the same way.

### 11.4 The release (§5)

```bash
mkdir -p $S/export-v030 $S/wheel
git archive v0.3.0 | tar -x -C $S/export-v030
uv build --wheel --offline --out-dir $S/wheel $S/export-v030 > $S/build.log 2>&1; echo "exit=$?"
grep -c "absent from" $S/build.log
ls -l $S/wheel
unzip -l $S/wheel/raypoolkit-0.3.0-py3-none-any.whl
for m in RayWorkPool.py __init__.py _timing.py contract.py rehearsal_lock.py; do
  unzip -p $S/wheel/raypoolkit-0.3.0-py3-none-any.whl raypoolkit/$m | cmp - <(git show 67a75b9:raypoolkit/$m) && echo "$m equal"
done
```

### 11.5 The records (§2)

```bash
git log --reverse --format='%h %s' 6e559bf^..636a02a
git for-each-ref refs/tags --format='%(refname:short) %(objectname:short) %(*objectname:short)'
gh run list --limit 15
for c in 6e559bf 6733447 722466a 89d6875 b4edd2c 67a75b9 127b2b4 6284b3b 2861b38 636a02a; do
  git show $c:docs/OPEN_ISSUES.md | grep -o '\*\*[0-9]* open\*\*'
done
git show 67a75b9:raypoolkit/rehearsal_lock.py | sed -n '63,64p;102p;112p;331p;345,347p;374,379p;435,449p'
git show 67a75b9:PROVENANCE.md | sed -n '102p'
git show 722466a:docs/rehearsal-lock/ray_proof.py | sed -n '149p;968p'
```

---

## 12. Summary for the board

- The campaign delivered `raypoolkit.rehearsal_lock` (01, `6733447`), a proof of it under real Ray
  (02, `722466a`), the release `v0.3.0` with the lock's contract (03 `89d6875`, 03a `67a75b9`;
  tag `caf0076`), and a switch-over checklist per client with the procedure for the day (04,
  `127b2b4`).
- At `v0.3.0` the suite passes at both ends (226), `black` is clean over 20 files, and the wheel
  rebuilt offline has 21,368 bytes, 10 entries and `67a75b9`'s five modules.
- The proof now holds the lock at both locations (U7). Under real Ray, holding the real shared lock,
  it exits 0 with 46 checks of 46 at 3.12.15 / Ray 2.43.0 and 3.13.16 / Ray 2.55.1. It left no Ray
  process and neither lock location; `~/.raypoolkit` is left, empty.
- Its records and 02's replay unmutated with exit 0 and fail under M10 and M12 as log 02 §4 says. P1
  and P2 fail the new owner-files check before any Ray starts; P3 and P4 are refused by the
  preflight.
- Two issues opened and resolved; none open; none opened by 05.
- 117 deviation entries over six logs (13 STRUCTURALLY REQUIRED, 98 IMPLEMENTATION CHOICE, 2
  UNINTENDED DRIFT, and 4 items that say they are not deviations), and 39 observations, each with
  its disposition.
- Gaps: G2; U4's refusal until a release after G2; phase 2; Ray between the ends, platforms but
  macOS, a multi-node cluster, Python 3.14 and Ray above 2.55.1; the module's docstrings and
  `PROVENANCE.md:102` on pid 1.
