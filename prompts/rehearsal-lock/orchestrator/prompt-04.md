# Orchestrator — prompt 04, the switch-over checklists

Read [`../README.md`](../README.md) first: §0, §1, §4, §5 (rules 5, 9 and 10), §6 (D2, D3, U1,
U2, U4) and §7. Then [`prompt-03.md`](prompt-03.md): its §0 "Conventions", which this note keeps
unless it says otherwise. Then the board's *Orchestrator review of prompt 03a* and *Release of
`v0.3.0`*, and `extraction`'s checklist precedent:
[`../../extraction/06-the-adoption-checklists.md`](../../extraction/06-the-adoption-checklists.md)
§2.3 and [`../../../docs/adoption/secondarygwkit.md`](../../../docs/adoption/secondarygwkit.md).

**You do not write code.** You may:
- run the suite, `black`, and the commands the log records;
- run the command line against a scratch `HOME`, never the real one, from a script file;
- make a minimal `ray==2.55.1` venv in the session scratchpad to read Ray's source, never to
  import it;
- read SGK, CPBH and SI through `git -C <client> show <commit>:<path>` and `git -C <client> grep`,
  never their working trees or venvs;
- fix small residue in a follow-up commit of your own (§4).

You start no Ray (README §5 rule 9). You do not push or tag.

**The prompt:** [`04-the-switch-over-checklists.md`](../04-the-switch-over-checklists.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** `[04-the-proof-takes-the-old-lock]`,
assigned to 05, and anything else the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- `v0.3.0` is tagged (object `caf0076`) on `67a75b9` after CI run 40121254667 passed at both ends;
  the release is recorded (`2c518ee`, `origin/main`). 04 is written (`b7c8200`, which touches only
  `prompts/`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that it
  could move, and hand the agent the corrections as an addendum.
- No Ray process; neither lock location exists under the real `HOME`. One prompt at a time in this
  checkout.

## 0. What makes this prompt unusual

**It has no code, and its readers are three other repositories acting on one day.** A checklist
that misses a place where a client starts Ray leaves an instance the lock cannot see; an acceptance
grep that finds nothing today proves nothing on the day. So the review has four halves:
- **every client fact is read**: each `path:line` quoted in the log at the client's commit, and
  every place the client starts Ray under the lock found by a grep the log records, not taken from
  the prompt's list;
- **every command is run**: each checklist's commands and `switch-over.md` §3's cross-check run
  against a scratch `HOME`, with the exit codes the documents state;
- **each acceptance grep bites**: run at today's commit, it finds every live line of the
  checklist's item 7, and none of them is under a path it leaves out;
- **nothing else moved**: four new documents and the records; nothing under `raypoolkit/`; no
  client touched; no Ray; no tag; no push.

**What moves on purpose:** `docs/adoption/rehearsal-lock/` (new: `secondarygwkit.md`,
`champbh.md`, `stochasticinstantons.md`, `switch-over.md`); the log, the board,
`docs/OPEN_ISSUES.md` and `prompts/INDEX.md`. Nothing under `raypoolkit/`, `docs/rehearsal-lock/`
or `.github/`; not `docs/rehearsal-lock.md`, `docs/adoption/`'s existing files, `README.md`,
`PROVENANCE.md`, `CLAUDE.md` or the campaign README.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-24 at `b7c8200`, against
the clients at the prompt's commits and Ray 2.43.0's source in `venv/`; it started no Ray. Pass
them on. Each is an IMPLEMENTATION CHOICE at the orchestrator's direction unless it says otherwise,
and the log says so.

1. **SGK has a third in-process start, which the prompt's §0.2 does not list.** STRUCTURALLY
   REQUIRED: the prompt's item 4 asks for "every place the client starts Ray that runs under the
   lock", and its list is short of that. `RunDrivers/quadsource_atol_sweep.py:478-491`, in
   `run_child` (one tolerance pair of the sweep, a child build under the lock), replaces `ray.init`
   with `_local_ray_init(*_a, **_kw)` before `main.py` runs, and that wrapper calls
   `_real_ray_init(num_cpus=args.cpus, include_dashboard=False, ignore_reinit_error=True)` with
   **no address** (`:487-489`). Three consequences for the SGK checklist, each to be read, not
   taken from here:
   - in a sweep child, `main.py`'s `ray.init(address=args.ray_address)` reaches this wrapper, which
     ignores its arguments, so a `_temp_dir` gated on `args.ray_address` in `main.py` does nothing
     there: the temp dir has to be given in the wrapper itself;
   - with `address=None`, Ray's `canonicalize_bootstrap_address(None, temp_dir)` follows
     `RAY_ADDRESS`, then `<temp_dir>/ray_current_cluster` (`/tmp/ray/…` with no temp dir), and
     connects to that cluster if it finds one; it starts a new instance only if it finds none
     (`ray/_private/services.py:389-435` and `:534-556` at 2.43.0). Read it at 2.55.1 too. So
     adding `_temp_dir` alone changes which file is read. The checklist names the options
     (`_temp_dir` alone, or `address="local"` with it) and what each does; **Advice:** the agent's;
   - two SGK tests read these wrappers with `ast`, and item 6 names both:
     `RunDrivers/tests/test_killed_handler.py:476-517` pins the `_local_ray_init` of
     `scoped_pipeline_run.main` and `quadsource_atol_sweep.run_build` (one `_real_ray_init`, its
     `address` the constant `"local"`, the handler installed after it), not `run_child`'s; and
     `RunDrivers/tests/test_build_rehearsal_scope.py:337-344` asserts that the text `rehearsal`
     appears **nowhere** in `run_child`'s source, so a constant, keyword or comment naming
     "rehearsal" added there fails it.

   Find every other start by grep, not from the prompt's list: `git -C SecondaryGWKit grep -n -E
   'ray\.init\(|_real_ray_init\(' 216e44d -- ':!docs' ':!prompts'` finds the seven `ray.init`
   calls and the three wrappers' calls (`:487`, `:629`, `:709`), outside tests. Record the
   command and its output.
2. **The form that keeps `test_ray_address_default.py` passing.** Not a deviation. At 2.43.0
   `ray.init` takes `_temp_dir` as `kwargs.pop("_temp_dir", None)` (`worker.py:1487`), so
   `_temp_dir=None` is the same as not passing it. The test (`:138-145`) requires exactly one
   `ray.init` per script, no positional argument, and an `address` keyword that unparses to
   `args.ray_address`; it says nothing of other keywords. So `ray.init(address=args.ray_address,
   _temp_dir=<dir> if args.ray_address == "local" else None)` passes it, and gives Ray no temp dir
   for any other address (prompt §0.4). Check `_temp_dir`'s default at 2.55.1 (`worker.py:1645`).
   The checklist may name other forms; each says whether the test still passes, and why.
3. **CPBH's and SI's acceptance greps must bite.** STRUCTURALLY REQUIRED: as the prompt writes it,
   item 8's grep would find nothing today in either client, so it could not fail on the day.
   - `ray_cluster.sh` is at `.documents/dk-and-rpk-migration/rehearsal/`, under the directory the
     prompt's §0.3 counts as records. It is live code. Each checklist's live paths name it
     explicitly.
   - The script spells the location in two lines, `LOCK_PARENT="$HOME/ScienceData"` and
     `LOCK_DIR="$LOCK_PARENT/.rehearsal-lock"` (CPBH `:77-78`, SI `:76-77`), which
     `ScienceData/\.rehearsal-lock` does not match; only its usage text (CPBH `:44`) does. SI's
     `CLAUDE.md:20` names the brief, which the pattern does not match either.
   - So each checklist's grep uses the prompt's pattern **extended** until, run at the client's
     commit, it finds every live line of that checklist's item 7 and the lock half of item 2
     (for example adding `ScienceData`, `\.rehearsal-lock` and `rehearsal-lock-brief`). Give the
     command, today's count and the lines it finds; the count after the switch is 0. Do the same
     for SGK, whose `CLAUDE.md:161-162` names the brief and `prompts/runregistry-extraction/README.md`
     §4.1 as "this repository's protocol": a live line that points at a record. Item 7 says what
     that line becomes; whether §4.1 is rewritten is SGK's choice.
4. **Every release in `cmd_start`, and what the module's `release` adds.** Not a deviation; the
   prompt's item 3 names the trap and the port check only. In CPBH's script (SI's lines are one or
   two less):
   - `release_lock` is called on four paths of `cmd_start`: the stale-cluster check (`:282-288`),
     the held port (`:300-303`), `ray start` failing (`:311-318`, after `stop_cluster`), and no
     `gcs_server` found (`:320-330`, after `stop_cluster`); and by the trap (`:305`).
   - The script's `release_lock` (`:131-148`) checks identity only. The module's `release` also
     refuses while the recorded pid or any process of `D` is alive, or the table cannot be read
     (contract §7). So where `stop_cluster` leaves something running, the lock now stays held
     where today it was removed. The checklist says, path by path, what the script's exit code and
     the lock's state become.
   - The stale-cluster check (`:282-288`) duplicates `acquire`'s exit 4, by a different rule (the
     module has no `ray_cluster.sh` exclusion, and ancestors seed its walk; contract §6). Name the
     options, keep both or drop the script's, and what each costs; **Advice:** the agent's.
5. **CPBH and SI also start in-process instances.** Each driver takes `--ray-address local` for a
   private instance (CPBH `config/argument_parser.py:341`, `CLAUDE.md:128-134`; SI `CLAUDE.md:14-16`;
   `ray.init(address=args.ray_address)` at CPBH `main.py:134`, `plot_by_beta.py:125`,
   `plot_ScalarHistory.py:106`, SI `main.py:131`, `plot_GradientCoupledSolutions.py:973`,
   `plot_InstantonSolutions.py:1207`). Such an instance names no lock temp dir, so the module's
   rule cannot see it, as the script's cannot today. Item 4 says whether the client's documents
   let a run under the lock use `local`; if they do, it needs a `_temp_dir` as SGK's does. Read
   it; do not assume.
6. **What the venv rule saw that the temp-dir rule does not.** SGK's rule listed any Ray process
   under SGK's venv, its own test runs included (for example `tools/tests/test_inventory_consumers.py`,
   which calls `ray.init`). After the switch, an SGK Ray process started without the temp dir
   blocks nothing: a test run, a reader started with `--ray-address auto`, or an instance left from
   before the switch. Item 5 says so, with the grep that finds SGK's other `ray.init` calls in
   tests.
7. **The §2.3 transcripts run from script files**, the client's values in variables inside each
   (as 03's clarification 8): if the Bash tool's command string names `/tmp/ray-sgk`,
   `/tmp/ray-cpbh` or `/tmp/ray-si`, its shell is an ancestor that seeds the walk and its other
   children are listed. Run each as `HOME=<scratch home> bash <script>`, from a directory outside
   the repository, with `venv/`'s interpreter by absolute path and `-I`. The live pid for `set-pid`
   is a `sleep` started by the script; `release` is run once while it lives (exit 1) and once after
   it is killed and reaped (exit 0). The scratch `HOME` is listed after each script and is empty at
   the end. `/tmp/ray-sgk` does not exist on this machine today; the scripts do not create it.
8. **The issue for 05** goes on the board's §3 with an **Assigned (2026-10-24):** line naming 05,
   and as one row under the index's §1.2, whose count becomes 1 (plus anything else opened).
9. **`docs/adoption/README.md` describes `v0.2.0`'s checklists** and is not changed (prompt §6).
   The new directory has no README: `switch-over.md` is its entry, and links the three checklists.
   Record it under "Observations not acted on"; it is not an issue.
10. **`74c3d3f` changed `CLAUDE.md` after the tag** (the provenance exception's wording). Nothing
    else outside `prompts/` has changed since `67a75b9`: `git diff 67a75b9 HEAD -- raypoolkit docs
    pyproject.toml README.md PROVENANCE.md .github` is empty. So the contract the checklists cite
    is the tag's.

**The facts, checked by the orchestrator on 2026-10-24.** Pass them on.

- **The tree.** Branch `main`, `HEAD` `b7c8200` before this note, clean; this checkout is the only
  worktree. `origin/main` is `2c518ee`; local `main` is two commits ahead (`74c3d3f`, `b7c8200`),
  and this note makes three. Tags `v0.1.0`, `v0.2.0` and `v0.3.0` (object `caf0076`, on
  `67a75b9`), the same on `origin`.
- **The baseline.** `venv/` (3.12.15 / 2.43.0 / `black` 25.1.0): `Ran 226 tests … OK` (2.2 s).
  `./venv/bin/black --check raypoolkit docs`: 20 files unchanged.
- **The machine.** No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` exit 1). No `RAY_*`
  variable. `~/ScienceData` is a directory; `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` do
  not exist. `/tmp/ray`, `/tmp/ray-cpbh`, `/tmp/ray-cpbh-decoy`, `/tmp/ray-decoy`,
  `/tmp/ray-rpk02a`, `/tmp/ray-rpk02b`, `/tmp/ray-rpkp` and `/tmp/ray-si` exist and are not touched;
  `/tmp/ray-sgk` and `/tmp/ray/ray_current_cluster` do not exist.
- **The clients, read only**, each clean with no stash (`git status --porcelain | shasum`
  `da39a3e…`, the empty string's):

  | Client | `HEAD` (branch) | Date, subject | Lock blob | Ray | Pin |
  |---|---|---|---|---|---|
  | SGK | `216e44d883e78df459c378c3669cf2859ecf11e6` (`handover-remedial`) | 2026-10-22, "Record handover prompt 07's commit hash" | `ea14336`, tests `cdeecd6` (42) | `requirements.txt:75` `ray==2.43.0` | `:76` `v0.2.0` |
  | CPBH | `807f17549f55f86c000716597492cf8b286ac982` (`jordan-normalization`) | 2026-10-22, "Place e-fold plot event labels by the e-fold shift, not the redshift factor" | `eaae1e7` | `:79` `ray==2.53.0` | `:80` `v0.2.0` |
  | SI | `7071bb8452252245ca65b3161681c1a634733878` (`rrk-adoption`; `main` `1c223e8` an ancestor, same blob) | 2026-10-23, "Add the run registry's config, rules, discovery hook and config test (rrk-adoption prompt 01, C2-C5)" | `6c8eada` | `:58` `ray==2.55.1` | `:59` `v0.2.0` |

  Each `main` is an ancestor of its `HEAD`. G1 holds.
- **The prompt's line references hold** where the orchestrator read them: SGK `tools/rehearsal_lock.py:49-50`,
  `:92-104`, `:184`; `CLAUDE.md:137-142`, `:149-162`; the wrappers `:629-634` and `:709-714`;
  the seven `ray.init` lines; CPBH's `ray_cluster.sh` `:66`, `:77-79`, `:86-148`, `:152-189`,
  `:267-385`; SI's `acquire_lock` `:117`, `release_lock` `:130`, `cmd_start` `:265`, `cmd_stop`
  `:338`, `cmd_status` `:356`. `diff` of the two scripts: names, ports, the default CPU count
  (10, 4), comments and the usage text, as the prompt says.
- **Nothing outside the clients sources or imports their lock code** in live code: the sourcing
  of `ray_cluster.sh` (header `:30-31`) is by records only; `tools.rehearsal_lock` is imported only
  by its own tests. RunRegistryKit and DatastoreKit name the lock only in records.
- **Expected counts.** The suite is **226** before and after. The index is **0** now, and **1**
  after, plus anything else the work opens.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §6 files changed; nothing under `raypoolkit/`; no client
  touched; no tag; nothing pushed; no Ray.
- **(E2) Every Ray start.** Each checklist's item 4 lists every start the review's own grep finds,
  `run_child`'s included (clarification 1), with a form that keeps the client's tests passing.
- **(E3) The commands.** Every command in the four documents agrees with the contract, and the
  log's transcripts show the exit codes the documents state.
- **(E4) The greps bite.** Each acceptance grep, run by the orchestrator at today's commit, finds
  the lines item 7 lists, `ray_cluster.sh`'s included (clarification 3).
- **(E5) The `path:line`s.** Each one quoted in the log is what the client's commit holds.
- **(E6) The procedure.** `switch-over.md` as the prompt's §2.2: parties (the proof included),
  preconditions, the order and why it does not matter, the cross-check, the fallback with its
  advice, afterwards.
- **(E7) The records.** The log, the board (with the issue assigned to 05), `docs/OPEN_ISSUES.md`
  at 1, `prompts/INDEX.md`.

**Conventions.** 03's note's, and all bind the agent:
- stage by explicit path only, and show `git diff --cached --name-only` before committing; `venv/`
  and `*.egg-info/` are gitignored and never staged;
- write "this commit" for the SHA; the orchestrator substitutes it;
- run every suite in the foreground, its output written to a scratch file and the verdict grepped
  from it;
- use the scratchpad subdirectory you are given, never `/tmp`, and put no scratch file under the
  repository;
- start no Ray, and never touch `~/ScienceData/.rehearsal-lock`, `~/.raypoolkit` or anything under
  `/tmp/ray*`;
- in zsh, write `"${C}:path"`, never `$C:path` (`:t`, `:h` and the like are modifiers);
- a stop goes to the user;
- check `git log` before committing;
- nothing outward-facing: no `git push`, no `git tag`, no `gh` command that writes.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` are
   empty; `git worktree list` shows this checkout alone. `git diff 67a75b9 -- raypoolkit docs
   pyproject.toml README.md PROVENANCE.md .github` is empty.
2. **The baseline.** 226, OK; `black --check` 20 files; `git tag` is the three tags.
3. **The machine.** `pgrep`, the real `HOME`, the `RAY_*` environment: as §0.
4. **The clients.** For each: `rev-parse HEAD`, `status --porcelain | shasum`, `stash list | wc
   -l`, as §0's table. Keep them; the review compares.
5. **Scratch.** Make the agent's subdirectory of the session scratchpad, empty, and give it the
   path; keep your own measurements in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, the contract
  `docs/rehearsal-lock.md`, and logs 02 and 03a (the sections the prompt names);
- `HEAD`, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in its scratch directory.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's ten clarifications. Clarifications 1, 3 and 4 are the
ones that matter: each is a place where a checklist written from the prompt's text alone would be
wrong on the day.

Tell it plainly:
- **One commit, at the end**, with the log `logs/04-the-switch-over-checklists.md` in README §5.1's
  form and the prompt's §4 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else.**
- **It edits, runs and imports no client, and uses no client's venv.** It reads them through `git`
  only, at §0's commits.
- **It starts no Ray**, and touches neither lock location under the real `HOME`.
- **It pushes nothing and tags nothing**, and writes nothing to GitHub.
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **E1, scope.** `git show --stat <commit>` lists only the prompt's §6 files. `git diff b7c8200
   <commit> -- raypoolkit docs/rehearsal-lock docs/rehearsal-lock.md docs/adoption/README.md
   docs/adoption/secondarygwkit.md docs/adoption/champbh.md docs/adoption/stochasticinstantons.md
   README.md PROVENANCE.md CLAUDE.md prompts/rehearsal-lock/README.md .github` is empty. `git tag`
   and `git ls-remote origin` unchanged. Each client's three values equal §1 step 4's. No Ray
   process; neither lock location under the real `HOME`; `/tmp/ray-sgk` absent.
2. **The suite and `black`.** `venv/`: `Ran 226 tests … OK`; `black --check raypoolkit docs`: 20
   files unchanged.
3. **E2, every Ray start.** Re-run clarification 1's grep in SGK, and `ray\.init\(` over CPBH's
   and SI's live code; each start is in its checklist's item 4. Read `run_child`'s entry against
   `quadsource_atol_sweep.py:478-491` and the two tests of clarification 1. Check clarification
   2's form against `test_ray_address_default.py:138-145`.
4. **E3, the commands, by running.** Write your own script per client from the checklists' text
   (not the log's), run it as clarification 7 against a fresh scratch `HOME`, and compare each exit
   code with the document's. Then `switch-over.md` §3's cross-check with all three projects'
   values.
5. **E3, against the contract.** Read each checklist's item 3 and item 5 with
   `docs/rehearsal-lock.md` open: every command, option, exit code and `status` line is the
   contract's; every statement about the lock cites a section that says it.
6. **E4, the greps.** Run each checklist's acceptance grep at its commit: today's count is the
   document's, and the lines it finds include every live line of item 7 and `ray_cluster.sh`'s lock
   lines (`LOCK_PARENT`, `LOCK_DIR`).
7. **E5, the `path:line`s.** Choose ten from the log's quotations, at least three per client, and
   read each through `git show`; each is what the client holds.
8. **E6, the procedure.** `switch-over.md` against the prompt's §2.2, item by item; the
   preconditions are commands, not descriptions; the fallback names both options with what each
   risks and an **Advice:**.
9. **Links.** Every relative link in the four documents resolves to a file tracked at `<commit>`.
10. **E7, the records.** The log has every section of README §5.1, the clients' untouched-checks,
    the transcripts, the quotations and 226 → 226, with §0's clarifications recorded (1 and 3 as
    STRUCTURALLY REQUIRED). The board's header, 04's row (landed, "this commit", 226 → 226), §2's
    G2 row pointing at `switch-over.md`, §3 with the issue assigned to 05; the index at 1, matching
    its header; `prompts/INDEX.md`'s line.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 04* paragraph, in the form of
  03a's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 04, and its header;
  - the notes line, with this note added and marked "used for 04".
- Anything the review finds that is not residue is opened on the board's §3 and in the index. A
  checklist fact that is wrong goes to a fix prompt (as 03a), not an orchestrator edit, unless the
  user says otherwise: the clients will act on these documents.
- **Put to the user, and do none of it unasked:**
  - the push of 04's commit and the review's, to `origin/main`;
  - that 05, the verification and close-out, can be written, and that it must move the proof to
    the default location first (`[04-the-proof-takes-the-old-lock]`);
  - that the switch-over itself is the clients' (G2), each in a campaign of its own, from its
    checklist, on the day `switch-over.md` describes.
- **Report to the user:** what landed; what the checklists say that the prompt did not
  (clarifications 1, 3–6), above all `run_child`'s start with no address; each checklist's
  **Advice:** items, as the clients' decisions to come.
