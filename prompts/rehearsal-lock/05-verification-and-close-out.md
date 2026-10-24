# Prompt 05 — verification and close-out

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 04 landed (`127b2b4`) and was reviewed (`6284b3b`); `main` is pushed, and CI passed at both ends
  on `6284b3b` (run 40126954690).
- U7 is taken (README §6.2; the user, 2026-10-24).
- `git status` is clean in this repository, and the suite gives `Ran 226 tests … OK`.
- No Ray process; neither lock location exists under the real `HOME`; the proof's four ports are
  free. G2 has not held.

**Closes:** `[04-the-proof-takes-the-old-lock]` and the campaign. **Narrows:** nothing.
**Changes:** nothing of the package. **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- It is the campaign's verification prompt: its document is the one a later reader starts from,
  built from five logs, five reviews and one release, and every count in it has to be counted.
- It changes one script, `docs/rehearsal-lock/ray_proof.py`, so that it takes the shared lock at
  both locations (U7), and re-runs it under real Ray holding the real lock, at both ends.
- It changes no line of the package.

**Read first:**
1. [`README.md`](README.md): every section; §5 rule 9 and §6.2 (U1–U7) in full.
2. `CLAUDE.md`: "What this repository is", "Releases", the campaign conventions and "Repository
   mechanics".
3. The board, every section. In §1, every orchestrator review in full and *Release of
   `v0.3.0`*; §3, the issue this prompt closes.
4. Every log, `logs/01-…` to `logs/04-…` and `logs/03a-…`: at least "What shipped", the
   deviations, the observations not acted on, and the state handed on. 02's log whole: its §3 is
   the run this prompt repeats, and its §4 holds the mutations M10 and M12 replayed below.
5. The contract, [`../../docs/rehearsal-lock.md`](../../docs/rehearsal-lock.md);
   [`../../docs/adoption/rehearsal-lock/switch-over.md`](../../docs/adoption/rehearsal-lock/switch-over.md);
   `docs/OPEN_ISSUES.md`; `README.md`; `PROVENANCE.md`.
6. The precedent for form: `extraction`'s [`07-verification-and-close-out.md`](../extraction/07-verification-and-close-out.md)
   and [`../../docs/extraction-verification.md`](../../docs/extraction-verification.md). Take the
   form, not the content.

Facts below are at `6284b3b`, whose `raypoolkit/` and `pyproject.toml` are `v0.3.0`'s (`67a75b9`),
measured by the planner on 2026-10-24.

---

## 0. What the planner measured

### 0.1 Why the proof holds both locations (U7)

`docs/rehearsal-lock/ray_proof.py` (1,476 lines, unchanged since `722466a`) takes the lock only at
`old_lock_dir()`: `LOCK_CODE` (`:142-151`) passes `lock_dir=old_lock_dir()` unless told not;
`preflight` (`:938-1010`) refuses only while the old location exists (`:968-974`); `owner_bytes`
and `show_owner` (`:627-643`) read the old location's owner file; `release_free_step`
(`:1099-1115`) and the after-both check (`:1374-1386`) look only there. The issue
`[04-the-proof-takes-the-old-lock]` asked 05 to move it to the default location.

That cannot be done before the switch-over, and 05 runs before it (G2 has not held): README §5
rule 9 has a prompt take the lock "where the clients look for it on that day", and until the
switch the clients look at the old location. A proof holding only the default location would be
invisible to them. **The user took U7 on 2026-10-24: the proof holds both.** It is right on any
day:
- **before G2**, the old location is seen by the clients that have not switched, and by any that
  have (the module's `acquire` refuses while the old location exists, U4);
- **after G2**, the default location is seen by every client, and, while U4's refusal stands, the
  old one too;
- **after U4's refusal is dropped** (README §8), the default location alone is seen, and the proof
  still holds it.

What the module does with two locations, read at `raypoolkit/rehearsal_lock.py` (`v0.3.0`):
- `acquire` at the default location refuses with 3 while the old location exists
  (`:435-447`: `os.path.lexists(old) and old.resolve() != d.resolve()`), so the default location
  is acquired **first**. `acquire` with `lock_dir=old_lock_dir()` skips that check, since `d` is
  the old location itself, and so succeeds while the default is held.
- Each location has its own owner file, its own `set_pid` and its own `release`; nothing ties the
  two.
- `acquire` at the default location creates `~/.raypoolkit` if needed (`d.parent.mkdir(parents=
  True, exist_ok=True)`, `:449`), and nothing removes it. `~/.raypoolkit` does not exist under the
  real `HOME` today, so the first run leaves it, empty. `switch-over.md` §2 already says that
  `~/.raypoolkit` may exist, empty, and is not the lock.
- Part (c)'s second acquirer, at the default location, is still refused by the old location
  (checked first), not as held; at the old location it is refused as held. So part (c)'s two
  expectations (`:1069-1097`) still hold, except its check that `~/.raypoolkit` is unchanged.

### 0.2 The environment

- **The repository.** `HEAD` `6284b3b`, clean, `origin/main` the same; this checkout the only
  worktree. `venv/`: Python 3.12.15, Ray 2.43.0, `black` 25.1.0. Suite `Ran 226 tests … OK`;
  `./venv/bin/black --check raypoolkit docs` 20 files unchanged. `git diff 67a75b9 -- raypoolkit
  pyproject.toml` is empty.
- **The proof's venvs.** `venv/` has no `grpc`, and part (b)'s client server needs it (the board's
  review of 02, "Before dispatch"). As 02, the proof runs in two `ray[default]` scratch venvs:
  `/opt/local/bin/python3.12` with `ray[default]==2.43.0`, and `/opt/local/bin/python3.13` (3.13.16)
  with `ray[default]==2.55.1`, each with this checkout installed editable. **Both resolve offline**
  from `uv`'s cache (`uv pip install --offline --dry-run`, `uv` 0.12.20, 2026-10-24).
- **02's runs**: exit 0, 31 checks of 31, 60.2 s at the low end and 65.7 s at the high end (the
  orchestrator's, board's review of 02 check 4). Temp dirs `/tmp/ray-rpk02a`, `…b`, `…c`; ports
  6420, 6421, 8270, 52370. `/tmp/ray-rpk02a` and `…b` hold Ray's session directories from 02 and
  are left as they are; the proof refuses a *process* naming a temp dir, not its existence.
- **The machine.** No Ray process; no `RAY_*` variable; `~/ScienceData` exists, and neither
  `~/ScienceData/.rehearsal-lock` nor `~/.raypoolkit` does.
- **The clients**, read only if at all: SGK `216e44d`, CPBH `807f175`, SI `7071bb8`, each clean.

### 0.3 The release, rebuilt offline

From `git archive v0.3.0` in an empty scratch directory, `uv build --wheel --offline`, the build
log captured (2026-10-24): `raypoolkit-0.3.0-py3-none-any.whl`, **21,368 bytes**, **10** entries
(`raypoolkit/RayWorkPool.py`, `__init__.py`, `_timing.py`, `contract.py`, `rehearsal_lock.py`, and
the dist-info's `licenses/LICENSE`, `METADATA`, `WHEEL`, `top_level.txt`, `RECORD`), no "absent
from" line, and each of the five modules byte-equal to `git show 67a75b9:raypoolkit/<module>`.
The pin was installed from GitHub at the release (the board's *Release of `v0.3.0`*, step 5) and is
not fetched again.

### 0.4 The records to collect

- **Commits.** From `6e559bf` (the plan) to `6284b3b`, 23 commits, then this prompt's own:
  - the prompts' commits: 01 `6733447`, 02 `722466a`, 03 `89d6875`, 03a `67a75b9`, 04 `127b2b4`;
  - the reviews: `2e561e2`, `cc5f2d6`, `b4edd2c`, `c1164a5`, `6284b3b`;
  - the notes: `10be4d5`, `ae1e064`, `8c0dfff`, `a2a8d37` (03a has none);
  - the prompts written: `d7d914d` (01, with U1–U6), `3f1620e`, `6e0ba38`, `b2ee2b3`, `b7c8200`,
    and the commit that adds this prompt (05, with U7);
  - the others: `6e559bf` (the plan), `50d91c7` (phase 2 waits for G2), `2c518ee` (the release
    record), `74c3d3f` (the user's widening of `CLAUDE.md`'s provenance exception).

  Class each.
- **Tags and CI.** `v0.3.0` (tag object `caf0076`) on `67a75b9`, after run 40121254667. Also green:
  40031056598 (`6733447`), 40031383762 (`2e561e2`), 40086680695 (`cc5f2d6`), 40121340908
  (`c1164a5`), 40122144103 (`2c518ee`), 40126954690 (`6284b3b`), and the run on the commit that
  adds this prompt, which the orchestrator records before dispatch. `89d6875`, `722466a` and
  `127b2b4` have no run of their own (each was pushed with a later commit).
- **The suite** went 121 → 226 (01), then 226 at every prompt after.
- **Issues.** Two opened and resolved: `[03-the-contract-overstates-two-edges-of-the-module]`
  (opened by the review of 03, closed by 03a) and `[04-the-proof-takes-the-old-lock]` (opened by
  04, closed here).
- **Decisions.** D1–D4 (the user, 2026-10-23); U1–U6 (2026-10-23, each as recommended); U7
  (2026-10-24, as recommended); and the user's choice of 2026-10-24 to run 02 in `ray[default]`
  scratch venvs.
- **Deviations.** A count of the three labels' words gives 01: 1 / 16 / 1, 02: 2 / 10 / 1, 03:
  1 / 17 / 1, 03a: 1 / 7 / 1, 04: 4 / 11 / 1 (STRUCTURALLY REQUIRED / IMPLEMENTATION CHOICE /
  UNINTENDED DRIFT). **A word is not an entry**: count the entries yourself.
- **Observations not acted on**: each log's §5.

---

## 1. What is wanted

05 does three things:
1. **The proof holds both locations** (U7, §2.2), and closes `[04-the-proof-takes-the-old-lock]`.
2. **It is re-run** under real Ray at both ends, holding the real shared lock at both locations, and
   its records replayed under 02's mutations M10 and M12 (§2.3).
3. **One document**, `docs/rehearsal-lock-verification.md`, verifies the campaign from the package
   as tagged `v0.3.0` and the records of 01–04 and of this prompt; and the campaign is closed, with
   G2 open (§2.1, §2.5).

**The package does not change.** Nothing under `raypoolkit/` or `pyproject.toml` is touched; the
suite stays at **226**; no tag is made (README §5 rule 10). 05 pushes nothing, and installs nothing
from the network.

---

## 2. What to write

### 2.1 `docs/rehearsal-lock-verification.md`

A new file, named as `extraction`'s. Additive from the day it is committed (`CLAUDE.md` rule 6).
Its head names the campaign, the board, this prompt, the date and the package it verifies:
`v0.3.0`, `67a75b9`, and that `git diff 67a75b9 -- raypoolkit pyproject.toml` is empty at the
commit that adds it.

| § | Section | What it holds |
|---|---|---|
| 1 | What this document is | What the campaign set out to do (README §0, §1, D1–D4), what it delivered, and the headline: one release, the suite at both ends, the module under real Ray twice (02, and here at both locations), the switch-over checklists, no open issue, and what remains (G2). |
| 2 | Reconciliation | **Git history:** a table of every prompt, its commit, review and note, the suite after it, and what it closed or opened; every other commit from `6e559bf` to the commit before 05's, classed (§0.4). **Tags and CI**, each run linked. **The environment** of every measurement below. |
| 3 | Each prompt's acceptance, at `v0.3.0` | A table: 01, 02, 03, 03a, 04; the acceptance in brief (README §2 and the prompt's own); what its review found; what holds at `v0.3.0`, and how it was re-measured here or why it cannot be. Re-measure here: the suite at both ends; the import guard (in the suite); `black`; the offline wheel (§0.3); each checklist's acceptance grep at its client commit (read-only, optional). |
| 4 | The module under real Ray | The proof as changed (§2.2), its command and venvs, each end's whole summary and timing, the roles seen at each checkpoint against 02's, Ray's processes and both lock locations before and after. The breakage of §2.3, and what each shows. |
| 5 | The release | The release record cited, step by step; the offline rebuild with its entry list and size; the five modules equal to `67a75b9`'s. |
| 6 | Issues | The two resolved, one line each, with the commit that closed each and what guards it. None open. |
| 7 | Decisions | D1–D4, U1–U7 and the `ray[default]` choice, one line each: what was decided, when, for which prompt, and where it is applied. |
| 8 | Deviations across the campaign | A table of entry counts per log and class. Then every UNINTENDED DRIFT entry in one line each, with its log, and every STRUCTURALLY REQUIRED entry that changed what a prompt delivered. |
| 9 | Observations not acted on | Every item of every log's §5, one line each, with its log and its disposition at `v0.3.0`: addressed (by which prompt, review or decision), opened as an issue, still an observation, or no longer true. Decide from the later logs and the board, never by changing anything. |
| 10 | Known gaps | **G2**: no client has switched; the checklists are measured at commits that will move. **U4's refusal** stays until a release after G2 (README §8). **Phase 2**, the cluster, waits for G2. **What remains unproven**: Ray between the ends (CPBH's 2.53.0), any platform but macOS, a multi-node cluster, Python 3.14 and Ray above 2.55.1. **What the module's own text omits**: the docstrings at `rehearsal_lock.py:63-64` and `:345-347` and `PROVENANCE.md:102` say ancestors are never listed, without 03a's pid 1 exception (the board's review of 03a); they change only in a later release. |
| 11 | Reproduction | Every command of §3–§5, verbatim, runnable from a clean checkout of the commit that adds this document. |
| 12 | Summary for the board | Five to ten lines. |

Every fact carries a commit, a `path:line` at a named tree, or a command and its output. A
statement of a log is cited by log and section. Where the document and a log disagree, the
document says which is right and why; it does not rewrite the log.

### 2.2 `docs/rehearsal-lock/ray_proof.py`: both locations (U7)

The script's own design stands: its witness, its checkpoints, its signalling rules, its refusals,
its record and replay. Change only what taking the lock at two locations needs.

1. **Every lock call names its location.** `LOCK_CODE` takes the location from its payload, `old`
   or `default`; no call relies on a default of the script's. The proof's project, purpose, temp
   dirs and addresses are unchanged.
2. **The preflight** refuses with exit 3, touching nothing, if **either** location exists, printing
   that location's owner file. Its first lines name both locations.
3. **Acquire**: the default location first, then the old. If the default `acquire` exits 3, exit 3
   with nothing touched. If it exits 0 and the old one exits 3, release the default location and
   exit 3. Any other failure of either is a failed check, and the cleanup releases what is held.
   Each location's held state is tracked separately.
4. **A new check, straight after the two acquires and before the part starts Ray**: both owner
   files exist, each with `project: RayPoolKit`, the part's `ray_temp_dir` and `ray_address`, and
   `pid: -`. It is the check the breakage P1 and P2 of §2.3 fail, before any Ray is started.
5. **`set_pid`, every refused `release` and every `release`** are made at both locations, each
   checked as today (the reason for a refusal, the owner file unchanged by it, the one `pid:` line
   changed by `set_pid`). Release the old location first, then the default.
6. **`owner_bytes` and `show_owner`** read and print both owner files, each labelled with its
   path.
7. **`release_free_step` and the after-both check**: after a part, `status` at each location says
   `lock: free (<that location> does not exist)`, and neither location exists. `~/.raypoolkit` may
   exist after the run, whatever it was before, and holds nothing (§0.1).
8. **Part (c)**: the second acquirer at each location, as today: at the old location refused as
   held, at the default location refused by the old location (§0.1). Both owner files are unchanged
   by it. Drop only its `~/.raypoolkit` comparison.
9. **The cleanup** releases whichever locations are held, old first. A refusal at either is
   `LeftHeld` (exit 4), naming the location and leaving both as they are.
10. **The docstring** says what the script now holds and why (U7, in a sentence: the clients look at
    the old location until the switch-over and at the default one after, and the old one stops a
    switched client while U4 stands), and names this prompt beside 02. The exit statuses keep their
    meanings.
11. **`--replay`** replays a record of either form, 02's or this prompt's; the record gains
    whatever fields the two locations need.

The script stays `black`-clean and names no client.

### 2.3 Run it, and break it

- **The runs.** At each end, in its `ray[default]` scratch venv (§0.2) with this checkout
  installed editable, from a command that names no temp dir, in the background:
  `env -u PYTHONPATH <venv>/bin/python docs/rehearsal-lock/ray_proof.py --record <scratch>/proof.json`.
  It exits 0 with every check passing. Record the whole output, the time, and before and after:
  `pgrep -lf 'gcs_server|raylet|ray::'`, both lock locations, `~/.raypoolkit`, and the four ports.
- **The replays.** Each record replayed (`--replay`) unmutated exits 0. Under **M10** and **M12**
  (02's log §4, applied to `raypoolkit/rehearsal_lock.py` exactly as recorded there, and reverted
  after each) the replays fail at the checkpoints 02's log names for each end, or the log says
  where and why they differ. `git status` is clean after each.
- **The breakage of the change**, each a diff of `ray_proof.py` exactly as applied, run with `HOME`
  an empty scratch directory (so that no real lock is touched), and starting no Ray:
  - **(P1)** the old location's `acquire` dropped: the check of §2.2 item 4 fails; nothing of Ray
    starts; the cleanup releases the default location; exit 1; the scratch `HOME` holds no lock.
  - **(P2)** the default location's `acquire` dropped: the same, with the old location released.
  - **(P3)** unmutated, with a directory at the scratch `HOME`'s default location: exit 3 from the
    preflight; nothing created at the old location.
  - **(P4)** unmutated, with a directory at the scratch `HOME`'s old location: exit 3 from the
    preflight; nothing created at the default location.

  Before each, confirm from the code that it reaches no Ray start: P1 and P2 fail before the part's
  first Ray start, P3 and P4 before any part.

### 2.4 The rest of the records

- **`switch-over.md`** gains one dated line under §1's table and one under §5's first bullet: on
  2026-10-24 prompt 05 made the proof hold both locations (U7), so it may be run before and after
  the switch-over alike, and `[04-the-proof-takes-the-old-lock]` is closed. The lines already there
  are not rewritten (`CLAUDE.md` rule 6).
- **The contract** (`docs/rehearsal-lock.md`) is not changed: §11's "holding the real shared lock at
  the location the projects used that day" is true of 02's run. The verification document's §4 is
  the record of this one. Say so in the log.

### 2.5 Closing the campaign

- **The board.** Its header says **CLOSED** (2026-10-24, by prompt 05), all six prompts landed. §1's
  row for 05. §2's gates unchanged, with a dated line: after the close, G2 is recorded on this
  board when it holds, in a records commit of its own. §3 empty; the issue moves to §4 with a
  **Resolved (05, 2026-10-24)** line.
- **The campaign README.** Its header, §2's row for 05, and a dated line under §7: the campaign
  closed at 05, with G2 open.
- **`prompts/INDEX.md`**: the campaign's line, **closed**, with 0 open issues.
- **`docs/OPEN_ISSUES.md`**: the row removed, the count **0** and the date; §1.2's heading says the
  campaign is closed.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Real Ray is started only by the proof**, under the real lock, once per end, and stopped by it.
   Before and after every run, `pgrep -lf 'gcs_server|raylet|ray::'` is recorded, each process
   attributed by its path. If one is up before a run, find whose it is: if it is this repository's
   or this session's, stop and ask; if another session's or a client's, do not touch it, do not run,
   and ask. Never `ray start` yourself, never `ray stop`, never signal a process the proof did not
   list, and never run the suite while Ray is up.
2. **The shared lock.** If either location exists before a run, it is someone's: stop and ask
   (README §5 rule 9). Never remove a lock, at either location, under the real `HOME`; the proof's
   own `release` is the only release. If a run ends with exit 4, stop and ask.
3. **No network.** Every venv and install is `uv … --offline`. No `git fetch`, `git push` or
   install from a URL. Reading GitHub with `gh run view` / `gh run list` is allowed, to cite a run.
4. **The package does not change.** `git diff 6284b3b -- raypoolkit pyproject.toml README.md
   PROVENANCE.md CLAUDE.md docs/rehearsal-lock.md docs/adoption .github` is empty at the end, but
   for `docs/adoption/rehearsal-lock/switch-over.md`'s two lines (§2.4). A finding is recorded, not
   fixed (rule 4). The breakage edits scratch copies or is reverted, and is never committed.
5. **No client is touched.** A client is read only through `git -C <client> show` and `git grep`,
   if at all. Record each client's `HEAD`, `status --porcelain | shasum` and `stash list | wc -l`
   at the start and the end.
6. **No command line of yours names a temp dir.** The Bash tool's whole command string is on its
   shell's command line; a shell naming `/tmp/ray-rpk02…` seeds the rule's walk (03's note,
   clarification 8). Run the proof by its own command, which names none.
7. **The document is long.** Its tables are built from the records, never from memory. Each count it
   states is one you counted, and the log says how.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 226 tests … OK` before and after, with no Ray up. At the high end,
   in an offline scratch venv (3.13.16, `ray==2.55.1`, this checkout editable): 226, OK.
2. **`black`.** `./venv/bin/black --check raypoolkit docs` leaves **20** files unchanged.
3. **The proof** at both ends, as §2.3: exit 0, every check passing, its count stated; no Ray process
   after; neither lock location after; the four ports free.
4. **The replays and the breakage**, as §2.3: unmutated 0; M10 and M12 as 02's log; P1–P4 as
   stated. Each diff checked with `git apply --check` before and `-R --check` after.
5. **The release**, as §0.3, offline.
6. **The documents.**
   - Every relative link and anchor in `docs/rehearsal-lock-verification.md` resolves to a file
     tracked at your commit, checked by a scratch script; every external link is to
     `github.com/ds283/…` and names a tag, a commit or a run.
   - Every `path:line` the document cites at `v0.3.0` is read at `67a75b9`.
   - Every count it states is recounted, and the log says how.
7. **The clients**, unchanged from start to end (§3 hazard 5).

---

## 5. Acceptance

1. `docs/rehearsal-lock/ray_proof.py` holds both locations as §2.2 says, exits 0 at both ends
   under real Ray holding the real lock, leaves no Ray process and no lock, and P1–P4, M10 and M12
   behave as §2.3 says.
2. `docs/rehearsal-lock-verification.md` holds §2.1's twelve sections, and every fact in it carries
   its source.
3. The offline wheel from `v0.3.0` has the 10 entries, and its five modules are `67a75b9`'s.
4. `[04-the-proof-takes-the-old-lock]` is resolved, and the campaign is closed on the board, in
   the README, in `prompts/INDEX.md` and in the index, at 0 open.
5. §4.1–§4.7 hold.
6. **The records**, in the same commit:
   - the log, `logs/05-verification-and-close-out.md`, per README §5.1, with: the suite at both
     ends; the proof's runs whole, with Ray's processes and both locations before and after each;
     the replays; P1–P4 and M10/M12 as diffs; the offline wheel; the documents' checks and how each
     count was made; the clients' states at the start and the end;
   - the board, the campaign README, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md` and `switch-over.md`,
     as §2.4–§2.5.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 226, in any venv.
- Either lock location exists before a run, or a Ray process is up before one or left after one.
- The proof fails at either end, or ends with exit 3 or 4. A defect found is opened, not fixed; stop
  before writing it up, and report.
- A replay or a breakage does not behave as §2.3 says, and the log cannot say why from the records.
- The offline wheel differs from §0.3.
- Anything would change a file under `raypoolkit/`, `pyproject.toml`, `README.md`, `PROVENANCE.md`,
  `CLAUDE.md`, `docs/rehearsal-lock.md`, the workflow, or any file not in §7.
- Anything would push, make or move a tag, use the network, or write, run, import or open anything
  of a client.

---

## 7. What this prompt changes, and what it does not

- **Files it adds:** `docs/rehearsal-lock-verification.md` and the log.
- **Files it changes:** `docs/rehearsal-lock/ray_proof.py` (§2.2);
  `docs/adoption/rehearsal-lock/switch-over.md` (two dated lines, §2.4); `docs/OPEN_ISSUES.md`;
  the board, the campaign README (its header, §2's row for 05 and §7's line) and
  `prompts/INDEX.md`.
- **It changes nothing else:** no file under `raypoolkit/`; not `pyproject.toml`, `README.md`,
  `PROVENANCE.md`, `CLAUDE.md`, `docs/rehearsal-lock.md`, the checklists, `docs/adoption/`'s other
  files, `docs/extraction/` or the workflow; not `LICENSE` or `.gitignore`.
- **It touches no client repository**, beyond reading through `git`.
- **It makes no tag, pushes nothing, and uses no network.**

---

## 8. The log and the board

`logs/05-verification-and-close-out.md`, using README §5.1, with §5 item 6's additions.

`IMPLEMENTATION_STATE.md`: the header (**CLOSED**), §1's row for 05, §2's dated line, and §3/§4.
