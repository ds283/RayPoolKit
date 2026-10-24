# Orchestrator — prompt 05, verification and close-out

Read [`../README.md`](../README.md) first: every section, and §5 rule 9 and §6.2 (U4, U7) in full.
Then [`prompt-02.md`](prompt-02.md): its §0, whose clarifications 2–5 and 9–12 this prompt meets
again under real Ray, and its conventions. Then [`prompt-04.md`](prompt-04.md)'s "Conventions",
which this note keeps unless it says otherwise. Then the board's *Orchestrator review of prompt
02* and *Orchestrator review of prompt 04*.

**You do not write code.** You may:
- run the suite, `black`, the agent's script and the commands the log records;
- make venvs of your own in the session scratchpad, offline, as clarification 2 says;
- start Ray **only** by running the agent's script, which takes the shared lock first at both
  locations (README §5 rule 9, U7), and never with a mutation applied;
- replay records offline (`--replay`), and apply and revert the log's diffs with `git apply`;
- run the proof's breakage with `HOME` an empty scratch directory;
- read SGK, CPBH and SI through `git -C <client> show` and `git -C <client> grep`, never their
  working trees or venvs;
- fix small residue in a follow-up commit of your own (§4).

You never run `ray stop`, signal a process, or remove a lock by hand, at either location. You do
not push or tag.

**The prompt:** [`05-verification-and-close-out.md`](../05-verification-and-close-out.md)
**Closes:** `[04-the-proof-takes-the-old-lock]` and the campaign · **Narrows:** nothing ·
**Opens:** only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 04 landed (`127b2b4`) and was reviewed (`6284b3b`); `origin/main` is `6284b3b`, and CI run
  40126954690 passed both jobs there (`suite (high)`, `suite (low)`). 05 is written (`2861b38`,
  which touches only `prompts/` and `docs/OPEN_ISSUES.md`), with U7 taken by the user on
  2026-10-24.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that it
  could move, and hand the agent the corrections as an addendum.
- No Ray process; neither lock location exists under the real `HOME`; the proof's four ports are
  free; no `RAY_*` variable. G2 has not held. One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It does two things no earlier prompt combined: it changes the proof that holds the real shared
lock, and then runs it.** For about a minute at each end the proof holds the lock at both
locations, so every client's `acquire` refuses, switched or not. A change that takes one location
and not the other, or a cleanup that releases one and forgets the other, leaves a real lock held
that three projects look at. And the verification document is the campaign's last word: every
count in it is one a reader will trust. So the review has four halves:
- **nothing is harmed**: both locations taken and released by the module at each end, and absent
  before and after; nothing outside the stop list signalled; no Ray process left; no `ray stop`;
- **the change is only the change**: `ray_proof.py`'s diff from `722466a` is what §2.2 asks and
  nothing else; its witness, checkpoints, stop and replay unchanged;
- **the proof still bites, and the change bites**: M10 and M12 fail their checkpoints by replay at
  both ends, on the new records and on 02's; P1–P4 behave as §2.3 says;
- **the document is true**: its tables recounted from the records, its links and `path:line`s
  resolved, nothing claimed that a command did not show.

**What moves on purpose:** `docs/rehearsal-lock/ray_proof.py` (changed);
`docs/rehearsal-lock-verification.md` (new); `docs/adoption/rehearsal-lock/switch-over.md` (two
dated lines); the log `logs/05-verification-and-close-out.md`; the board, the campaign README
(its header, §2's row for 05, a dated line under §7), `prompts/INDEX.md` and
`docs/OPEN_ISSUES.md`. Nothing under `raypoolkit/`; not `pyproject.toml`, `README.md`,
`PROVENANCE.md`, `CLAUDE.md`, `docs/rehearsal-lock.md`, the three checklists, `docs/adoption/`'s
other files or `.github/`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-24 at `2861b38`, with
`ray[default]` venvs of its own at both ends, built offline; it started no Ray. Pass them on. Each
is an IMPLEMENTATION CHOICE at the orchestrator's direction unless it says otherwise, and the log
says so.

1. **The commit that adds the prompt has no CI run.** STRUCTURALLY REQUIRED: the prompt's §0.4 asks
   for "the run on the commit that adds this prompt, which the orchestrator records before
   dispatch". `2861b38` is not pushed (`origin/main` is `6284b3b`), and nothing is pushed before
   05 lands, so there is none. The document's §2 says so: `2861b38` and the commit that adds this
   note are local when 05 runs, each touches only `prompts/` (and `docs/OPEN_ISSUES.md`), and the
   last run on the package's tree is 40126954690 on `6284b3b`. It lists both commits among the
   "others" it classes (a prompt written; a note), so the count from `6e559bf` to the commit
   before 05's is **25**: §0.4's 23, `2861b38` and this note's.
2. **The venvs.** As 02 (its note's clarification 1), the proof runs in two `ray[default]` scratch
   venvs, built **offline** from `uv`'s cache, in your scratch directory:
   ```bash
   uv venv -p /opt/local/bin/python3.12 <scratch>/v243
   uv pip install --offline --python <scratch>/v243/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray[default]==2.43.0" "black==25.1.0"
   uv venv -p /opt/local/bin/python3.13 <scratch>/v255
   uv pip install --offline --python <scratch>/v255/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray[default]==2.55.1" "black==25.1.0"
   ```
   The orchestrator built both so on 2026-10-24: they resolve, give 3.12.15 / 2.43.0 and 3.13.16 /
   2.55.1, `grpc` 1.84.1 at both, and `raypoolkit.__file__` under the repository. `v255` is also
   the high-end venv of §4.1 (226 tests). Record each venv's `uv pip freeze`, `sys.version`,
   `ray.__version__` and `raypoolkit.__file__`. `venv/` is used for the suite and `black` only, and
   nothing is installed into it.
3. **Every lock call passes an explicit `lock_dir`.** README §5 rule 9 says the proof takes the
   lock "through the module's own `acquire` with an explicit `lock_dir`". So `LOCK_CODE` maps the
   payload's location to `rl.old_lock_dir()` or `rl.default_lock_dir()` and always passes it; no
   call omits it, and an unknown location is an exit of the child, not a default. Part (c)'s
   default-location acquirer is included.
4. **One refused acquire, one held lock.** Prompt §2.2 item 3: if the default `acquire` exits 0
   and the old one exits 3, the default location is released **through the module** before the
   script exits 3. If that release is refused, it is `LeftHeld`: exit 4, and a stop. The old
   location's owner file is printed in that case, since it is someone else's lock. Nothing is
   released by hand.
5. **A scratch `HOME` for everything but the two real runs.** Every `--replay` and every P1–P4 run
   is made from a script file that sets `HOME` to a fresh, empty scratch directory, asserts that
   `HOME` is under your scratch directory before running anything, and lists that directory after.
   The proof's first lines name both locations (§2.2 item 2): check from its output that both are
   under the scratch `HOME`. "Holds no lock" (P1, P2) means neither lock directory exists; the
   parents `acquire` makes (`.raypoolkit`, and `ScienceData` for the old location) may remain,
   empty, and the log lists them. P1–P4 start no Ray, but the preflight still requires no Ray
   process and the four ports free; run them at the low end at least, and say at which.
6. **02's records survive, and are in your scratch directory.** `from02/proof-2.43.0.json` and
   `from02/proof-2.55.1.json` are 02's agent's records (SHA-256 `5f8c82ad…`, `cdb2b63c…`), and
   `from02/m10.diff` and `from02/m12.diff` are 01's M10 and M12 as 02 applied them, their SHA-256
   equal to 02's log §4 table (`4a87ba4e…`, `0ac88838…`). The orchestrator checked on 2026-10-24
   that both diffs pass `git apply --check` on `HEAD`'s module (unchanged since `6733447`), and that
   the script at `722466a` replays both records unmutated with exit 0 and a scratch `HOME` that
   stays empty. Prompt §2.2 item 11 asks that `--replay` reads 02's form too: replay both 02
   records with your changed script, unmutated (exit 0) and under M10 and M12 (02's log §4's
   failures), as well as your own records.
7. **The real runs.** As 02's note's clarifications 2 and 3, which bind you:
   - the command names no temp dir (`/tmp/ray-rpk02a`, `…b`, `…c`), and neither does the
     `--record` path; look at the temp dirs only between runs;
   - each run in the background (`run_in_background`), output to a scratch file, never under a tool
     timeout and never killed; if one has not exited after 15 minutes, stop and ask;
   - **nothing else runs while a real run does**: no `ps | grep`, no replay, no suite, no `git
     apply`. A mutation applied to `raypoolkit/rehearsal_lock.py` during a real run would change
     the module the run's lock children import;
   - the real runs are made only with `git diff -- raypoolkit` empty, checked just before each.
   Develop offline first (02's clarification 10): build and check the change against a scratch
   `HOME` with P1–P4 and the replays, then one real run at the low end, then the high end.
8. **What stays as it is.** The purpose strings keep their "02" (prompt §2.2 item 1: the project,
   purpose, temp dirs and addresses are unchanged); the docstring is where 05 is named. The check
   names are yours to choose where a check splits in two; the log maps each check of the new
   script to 02's, and states the count at each end (02's was 31).
9. **`~/.raypoolkit` is made by the first real run, and left.** It does not exist under the real
   `HOME` today. The default `acquire` creates it (`rehearsal_lock.py:449`), and nothing removes
   it; after both runs it exists and is empty. That is expected (prompt §0.1) and is not to be
   removed. Record `ls -la ~/.raypoolkit` before and after each run. A lock directory at either
   location before a run is someone's: stop and ask.
10. **Ray's session directories stay.** `/tmp/ray-rpk02a` and `/tmp/ray-rpk02b` exist from 02 and
    are reused; `/tmp/ray-rpk02c` does not exist and is not made. `/tmp/ray`, `/tmp/ray-cpbh`,
    `/tmp/ray-cpbh-decoy`, `/tmp/ray-decoy`, `/tmp/ray-rpkp` and `/tmp/ray-si` exist and are not
    touched. Nothing under `/tmp/ray*` is deleted.
11. **The offline wheel is already measured.** The orchestrator rebuilt it on 2026-10-24 as §0.3
    says (`git archive v0.3.0`, `uv build --wheel --offline`): exit 0, 21,368 bytes, the 10 entries,
    no "absent from" line, the five modules byte-equal to `67a75b9`'s. Repeat it yourself for the
    document; it should match.
12. **The CI the document cites.** Read with `gh run view` / `gh run list` only. The proof itself
    never runs in CI; CI runs `black --check` over `ray_proof.py` only once 05's commit is pushed,
    which is after the review. The document says both.
13. **The board's notes line and README rows.** The prompt's §2.5 has you update README's header,
    §2's row for 05 and §7's dated line, as well as the board's header, §1's row, §2's dated line
    and §3/§4. Leave the board's "Orchestrator notes" line to the review.

**The facts, checked by the orchestrator on 2026-10-24.** Pass them on.

- **The tree.** Branch `main`, `HEAD` `2861b38` before this note, clean; this checkout is the only
  worktree. `origin/main` is `6284b3b`; local `main` is one commit ahead, and this note makes two.
  Tags `v0.1.0`, `v0.2.0`, `v0.3.0` (object `caf0076`, on `67a75b9`), the same on `origin`.
  `git diff 67a75b9 HEAD -- raypoolkit pyproject.toml` is empty; since `67a75b9`, `CLAUDE.md`
  (`74c3d3f`), `docs/OPEN_ISSUES.md` and `docs/adoption/rehearsal-lock/` (04) have changed outside
  `prompts/`. `docs/rehearsal-lock/ray_proof.py` is 1,476 lines, last changed in `722466a`.
- **The baseline.** `venv/` (3.12.15 / 2.43.0 / `black` 25.1.0): `Ran 226 tests … OK` (2.1 s).
  `./venv/bin/black --check raypoolkit docs`: 20 files unchanged.
- **The machine.** No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` exit 1). Ports 6420,
  6421, 8270, 52370 and 8265 have no listener. No `RAY_*` variable. `~/ScienceData` is a directory;
  `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` do not exist.
- **The module's lines the change rests on** (`67a75b9`, unchanged since `6733447`): `acquire`
  `:427`, its old-location refusal `:434-447` (before any `mkdir`), `d.parent.mkdir` `:449`;
  `release` `:548`, which prints `no lock to release` and returns 0 when there is none; `status`
  `:601`, which prints `lock: free (<d> does not exist)` (`:626`) and, while the old location
  exists, `old location: PRESENT (…)` (`:630`); `read_owner` `:240`, `None` with no owner file.
- **The proof's lines** (`722466a`): as the prompt's §0.1 gives them, read and confirmed. `cleanup`
  (`:1302-1351`) releases one lock, after the process check, on one `lock_held` flag;
  `HeldByOther` returns 3 from a part with no cleanup (`:1177-1178`, `:1277-1278`); the after-both
  check is `:1374-1386`.
- **The clients, read only**, each clean with no stash (`status --porcelain | shasum` `da39a3e…`):
  SGK `216e44d883e78df459c378c3669cf2859ecf11e6` (`handover-remedial`), CPBH
  `807f17549f55f86c000716597492cf8b286ac982` (`jordan-normalization`), SI
  `7071bb8452252245ca65b3161681c1a634733878` (`rrk-adoption`).
- **The records the document counts.** The 23 commits of §0.4, confirmed by `git log --reverse
  6e559bf^..6284b3b`, each in the class §0.4 gives; then `2861b38` and this note's
  (clarification 1). Green runs: 40031056598, 40031383762, 40086680695, 40121254667,
  40121340908, 40122144103, 40126954690.
- **Expected counts.** The suite is **226** before and after, at both ends. `black`: **20** files
  before and after. The index is **1** now, and **0** after.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §7 files changed; nothing under `raypoolkit/`; no client
  touched; no tag; nothing pushed.
- **(E2) Safety.** Both locations taken and released by the module at each run, and absent before
  and after; nothing but the stop list signalled; no `ray stop`; no Ray process left.
- **(E3) The change.** `ray_proof.py` differs from `722466a` only as §2.2 items 1–11 ask.
- **(E4) The proof passes** at both ends, run by the agent and again by the orchestrator.
- **(E5) It bites.** M10 and M12 by replay, on the new records and 02's; P1–P4 as §2.3.
- **(E6) The document.** Its twelve sections; every count recounted; links and `path:line`s
  resolved.
- **(E7) The records.** The log, the board **CLOSED**, the README, `prompts/INDEX.md`, the index at
  0, `switch-over.md`'s two lines.

**Conventions.** 04's note's, with 02's for real Ray, and all bind the agent:
- stage by explicit path only, and show `git diff --cached --name-only` before committing; `venv/`
  and `*.egg-info/` are gitignored and never staged;
- write "this commit" for the SHA; the orchestrator substitutes it;
- run every suite in the foreground, with no Ray up, its output written to a scratch file and the
  verdict grepped from it;
- use the scratchpad subdirectory you are given, never `/tmp`, and put no scratch file under the
  repository; the record files stay in scratch and are never committed;
- start Ray only by running the whole script, at the times clarification 7 says, and never with a
  mutation applied; never run `ray stop`, `kill` or `pkill`; never remove either lock location,
  `~/.raypoolkit` or anything under `/tmp/ray*`;
- a run that exits 3 or 4, or ends any other way than 0, 1 or 2, is a stop: report both owner
  files and `pgrep -lf 'gcs_server|raylet|ray::'` (pids and first words only) and wait;
- in zsh, write `"${C}:path"`, never `$C:path`;
- a stop goes to the user;
- check `git log` before committing;
- nothing outward-facing: no `git push`, no `git tag`, no `gh` command that writes, no network
  install.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` are
   empty; `git worktree list` shows this checkout alone.
2. **The baseline.** 226, OK; `black --check` 20 files; `git tag` is the three tags.
3. **The machine.** `pgrep`, the five ports, both lock locations and `~/.raypoolkit` under the real
   `HOME`, the `RAY_*` environment: as §0.
4. **The clients.** For each: `rev-parse HEAD`, `status --porcelain | shasum`, `stash list | wc
   -l`, as §0. Keep them; the review compares.
5. **Tell the user** that each real run holds the shared lock at **both** locations for about a
   minute, so any client's rehearsal started meanwhile refuses with exit 3; that the first run
   leaves `~/.raypoolkit`, empty; and that macOS may ask whether Python may accept incoming
   connections when part (b)'s cluster starts, which is theirs to answer.
6. **Scratch.** Make the agent's subdirectory of the session scratchpad, holding only `from02/`
   (clarification 6), and give it the path; keep your own measurements and venvs in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout, in the background. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, and the files the
  prompt's "Read first" names;
- `HEAD`, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in its scratch directory.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's thirteen clarifications. Clarifications 3–5 and 7 are
the ones that keep the real lock safe; 1 and 6 change what the document and the replays can cite.

Tell it plainly:
- **One commit, at the end**, with the log `logs/05-verification-and-close-out.md` in README
  §5.1's form and the prompt's §5 item 6 additions.
- **The files it may add or change are the prompt's §7 list, and nothing else.**
- **It edits, runs and imports no client, and uses no client's venv.**
- **It starts Ray only by running the proof**, under the real lock at both locations, twice, and
  never runs `ray stop`, signals a process outside the proof's stop list, or removes a lock.
- **It pushes nothing and tags nothing**, uses no network, and writes nothing to GitHub.
- **Stop and ask** on any of the prompt's §6 conditions.

While it works, run nothing that names a temp dir, start no Ray, and touch nothing under
`raypoolkit/`.

## 3. The review — eleven checks

1. **E1, scope.** `git show --stat <commit>` lists only the prompt's §7 files. `git diff 2861b38
   <commit> -- raypoolkit pyproject.toml README.md PROVENANCE.md CLAUDE.md docs/rehearsal-lock.md
   docs/adoption .github` is empty but for `switch-over.md`'s two added lines (`git diff` of it
   shows additions only). `git tag` and `git ls-remote origin` unchanged. Each client's three values
   equal §1 step 4's.
2. **E2, the machine after the agent.** No Ray process; the five ports free; neither lock location;
   `~/.raypoolkit` exists and is empty; `/tmp/ray-rpk02a` and `…b` exist, `…c` does not.
3. **E3, the change, by reading.** `git diff 722466a <commit> -- docs/rehearsal-lock/ray_proof.py`
   read whole against §2.2 items 1–11 and clarifications 3, 4 and 8: every lock call passes an
   explicit `lock_dir`; the preflight refuses on either location; acquire default then old, with
   item 3's two exits; the new owner-file check before any Ray start; `set_pid` and every release
   at both, old first; `owner_bytes`/`show_owner` labelled per location; the after-both check;
   part (c) at both, its `~/.raypoolkit` comparison gone; the cleanup per location, old first,
   `LeftHeld` naming the location; the docstring. Nothing else of the witness, checkpoints,
   `signal_if_same`, `stop` or `replay` changed. `grep -n '"stop"\|ray stop\|killpg\|pkill'` finds
   nothing new; there is still one `os.kill`.
4. **E4, the proof, by running.** In your own offline `ray[default]` venvs (clarification 2), from a
   command naming no temp dir, in the background: exit 0 at each end, every check `PASS`, the count
   the log states. Before and after each: no Ray, neither location, `~/.raypoolkit` empty, the
   ports free. Compare the checkpoints' listings with the log's by role.
5. **E5, the replays.** With `HOME` an empty scratch directory that stays empty: your two records,
   the agent's two and 02's two, each unmutated (exit 0), under M10 and under M12 (from `from02/`,
   SHA-256 checked), with the failures 02's log §4 names per end, or the log's explanation of a
   difference. `git status` and the module's SHA-256 restored after each.
6. **E5, the breakage of the change.** Apply each of the log's P1 and P2 diffs to `ray_proof.py`
   with `git apply --check` first, run as clarification 5 with a fresh scratch `HOME`, revert with
   `-R --check` then `-R`: exit 1, the owner-file check failing, no Ray started, the scratch `HOME`
   with no lock directory. P3 and P4 unmutated: exit 3 from the preflight, nothing made at the
   other location.
7. **The suite and `black`.** `venv/`: `Ran 226 tests … OK`; the high-end venv: 226, OK. `black
   --check raypoolkit docs`: 20 files unchanged.
8. **E6, the document's counts.** Recount from the records, not the log: the commit table (25
   before 05's, each class); the deviation-entry table, one log at least whole and the totals for
   all; §9's observations against each log's §5, one log at least whole; the check counts of §4
   against the records' `checks`.
9. **E6, links and lines.** A scratch script resolves every relative link and anchor in
   `docs/rehearsal-lock-verification.md` to a file tracked at `<commit>`; every external link is
   `github.com/ds283/…` naming a tag, commit or run. Ten `path:line`s cited at `v0.3.0`, read at
   `67a75b9`; §11's commands run as written from a clean checkout of `<commit>`, bar the real
   proof (run by check 4).
10. **E6, what the document claims.** No statement beyond its sources: G2 open; U4's refusal and
    phase 2 waiting on it; the unproven ranges of §2.1 row 10; the docstrings' pid 1 omission;
    clarification 1's two unpushed commits.
11. **E7, the records.** The log has every section of README §5.1 and the prompt's §5 item 6
    additions, with clarification 1 recorded as STRUCTURALLY REQUIRED. The board's header
    **CLOSED**, 05's row ("this commit", 226 → 226), §2's dated line, §3 empty, the issue in §4
    with its **Resolved (05, 2026-10-24)** line; the README's header, §2 row and §7 line;
    `prompts/INDEX.md` closed with 0; the index at 0 matching its header; `switch-over.md`'s two
    dated lines, nothing else of it changed.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 05* paragraph, in the form of
  04's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the README, in `prompts/INDEX.md` and in
    the verification document if it names it;
  - the notes line, with this note added and marked "used for 05".
- Anything the review finds that is not residue is opened on the board's §3 and in the index, and
  the campaign is reopened until it is closed; a fact of the document that is wrong goes to a fix
  prompt (as 03a), not an orchestrator edit, unless the user says otherwise.
- **Put to the user, and do none of it unasked:**
  - the push of `2861b38`, this note, 05's commit and the review's, to `origin/main`, so that CI
    runs `black` over the changed proof; *Recommended:* push once the review's commit is made;
  - that G2, the switch-over, is the clients': each in a campaign of its own, from its checklist,
    on the day `switch-over.md` describes, and recorded on this board when it holds;
  - that the later units of README §8 (dropping U4's refusal; phase 2, the cluster) wait for G2.
- **Report to the user:** what landed; the proof at both ends holding both locations, its time
  and check count; the replays and the breakage; the document's headline and its known gaps;
  `~/.raypoolkit` now existing, empty; the push, as a decision for them.
