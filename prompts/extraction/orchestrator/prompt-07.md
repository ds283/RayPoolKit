# Orchestrator — prompt 07, verification and close-out

Read [`../README.md`](../README.md) first: every section, as the prompt asks of its agent, and
§6.2 (U13, U14) closely. Then read [`prompt-01.md`](prompt-01.md) §0's last list, "Conventions",
which this note keeps unless it says otherwise; [`prompt-04.md`](prompt-04.md) §0's clarification
1, the driver pattern for breakage of uncommitted work; [`prompt-06.md`](prompt-06.md) §0's
"Conventions" additions; and the board's *Orchestrator review of prompt 06*.

**You do not write code.** You may:
- run the suite, the agent's smoke script, `compare_with_source.py` and the commands the log
  records;
- make venvs, exports, worktrees and wheels of your own in the session scratchpad, and replay the
  log's breakage there, never in the repository;
- start a local Ray **only** by running the agent's script, or for (d) as §0's clarification 9
  says, each with `RAY_USAGE_STATS_ENABLED=0` (clarification 3) and with Ray's processes recorded
  before and after;
- read the three clients and DatastoreKit through `git -C <repository> show`, `ls-tree`, `log`,
  `rev-parse`, `status --porcelain` and `stash list`, never their working trees' files;
- read GitHub's state with `gh run view` / `gh run list`, writing nothing;
- fix small residue in a follow-up commit of your own (§4).

You do not push or tag. Pushing, so that CI runs `black` over the new script, is put to the user
(§4).

**The prompt:** [`07-verification-and-close-out.md`](../07-verification-and-close-out.md)
**Closes:** the campaign · **Narrows:** nothing · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- 06 landed (`67f3f7e`) and was reviewed (`71f0d66`). 07 is written (`787507a`); U13 and U14 are
  taken.
- **`main` is pushed, and CI passed at both ends on a later records commit.** `origin/main` is
  `787507a`, and the workflow's run
  [`38086076394`](https://github.com/ds283/RayPoolKit/actions/runs/38086076394) on it passed both
  jobs: `suite (low)`, Ray 2.43.0, `raypoolkit-0.2.0` installed, `Ran 121 tests … OK` and `black`
  "16 files would be left unchanged."; `suite (high)`, `Ran 121 tests … OK`. That is the first CI
  run over `docs/adoption/measure_client_pools.py`.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- The tags on `origin` are `v0.1.0` (tag object `0a9cdb2`) peeling to `4e90a8a` and `v0.2.0`
  (`4e7eb15`) peeling to `eaef0ce`, and locally the same.
- No Ray process is up (hazard 1). One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It writes no line of the package, and it is the first prompt here to start Ray.** 01–06 drove
the pool only through the suite's in-process stand-in (U6). Under U13, 07 runs it under a local
`ray.init()` at both tested ends, and under U14 it does so with no network. Its product is the
document a later reader starts from, built from six logs, six reviews and two releases. The review
has four halves:
- **the run under Ray is real and leaves nothing behind**: the script starts and stops its own
  Ray, refuses when one is up, reports nothing to anyone, and passes at both ends; (a) and (b)
  fail as they should, (c) shows what it shows, and (d) refuses;
- **the document's counts are counted**: every table is built from the records and recounts as
  stated; where the document and a log disagree, it says which is right;
- **the release is what was released**: the offline wheel from `v0.2.0` has the 9 entries, and its
  four modules are `eaef0ce`'s;
- **the campaign is closed, and nothing else moved**: the package, `docs/adoption/`, the other
  documents, the clients and GitHub are as they were.

**What moves on purpose:** two new files, `docs/extraction-verification.md` and
`docs/extraction/ray_smoke_run.py`; the log; the board, the campaign README, `prompts/INDEX.md` and
`docs/OPEN_ISSUES.md`, as the prompt's §2.4 says. Nothing under `raypoolkit/` or `docs/adoption/`,
not `compare_with_source.py`, `pyproject.toml`, `README.md`, `PROVENANCE.md` or `.github/`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-10 at `787507a` (the
package as at `eaef0ce`), with offline scratch venvs of its own at both ends; it started no Ray.
Pass them on. Each is an IMPLEMENTATION CHOICE at the orchestrator's direction unless it says
otherwise, and the log says so.

1. **The gate's CI run is `38086076394`, on `787507a`.** `71f0d66` was pushed with `787507a` and
   has no run of its own; the run on `787507a` covers its tree, since `787507a` touches only
   `prompts/`. The document's §2 cites it as "the gate's run" (the prompt's §1.3), linked.
2. **The commit range is 30 commits, not 28.** The prompt's §1.3 counts `3f1dfd4` to `71f0d66`
   (28, measured). The document's §2 runs "to the commit before 07's", which is now this note's
   commit: add `787507a` (07 written, U13 and U14 recorded) as *prompt written*, and this note's
   commit as *note*. `3f1dfd4` is a class of its own, *repository started*, which the prompt's
   §1.3 names and its §2.1's list of classes omits. So: 1 started, 1 plan, 7 prompts written, 7
   notes, 6 prompts, 6 reviews, 2 release records. If a further records commit lands before 07's,
   class it too and say so. Record as STRUCTURALLY REQUIRED: the prompt's 28 is not the count at
   07's commit.
3. **No network means no usage report from Ray.** This machine's `~/.ray/config.json` is
   `{"usage_stats": true}`, which enables Ray's usage reporting to `usage-stats.ray.io`. The
   reporter is the API server's `UsageStatsHead`, which declares itself a minimal module
   (`ray/dashboard/modules/usage_stats/usage_stats_head.py:213` at 2.43.0, `:216` at 2.55.1), so it
   runs under `include_dashboard=False`. The environment variable `RAY_USAGE_STATS_ENABLED=0` takes
   priority over the file (`ray/_private/usage/usage_lib.py:349-352` at 2.43.0; the constant is in
   `ray/_common/usage/usage_constants.py` at 2.55.1). So:
   - the script sets `os.environ["RAY_USAGE_STATS_ENABLED"] = "0"` (assignment, not `setdefault`)
     before it imports `ray` or `raypoolkit`, and its docstring says why. It does not change the
     prompt's `ray.init(...)` call;
   - (d)'s session sets it too;
   - `~/.ray/config.json` is not edited, and is not the agent's to change;
   - the log quotes what each run's Ray session directory says of usage stats (`grep -ril usage`
     over its `logs/`), whatever that is.
   The planner's probe at 07's writing did not set it; whether it reported is not known, and is
   not this prompt's to find out.
4. **Ray's session directory is Ray's.** `ray.init` writes `/tmp/ray/session_<date>_<pid>/` and
   repoints `/tmp/ray/session_latest`. That is Ray's default, shared with other sessions on this
   machine (51 session directories at writing, the latest
   `session_2026-10-10_21-56-07_219812_27391`); it is not a scratch file under the conventions. Do
   not pass `_temp_dir` or set `RAY_TMPDIR` (the scratchpad's path is too long for Ray's Unix
   sockets), and delete nothing under `/tmp/ray`. The log names the session directory each run
   created.
5. **Record a wider process check alongside the prompt's.** `pgrep -lf
   'gcs_server|raylet|ray::'` does not match the Python processes a local Ray also starts (its
   dashboard and agent, log monitor and monitor, whose command lines name
   `ray/dashboard/…`, `ray/_private/…` and `ray/autoscaler/…`). Before and after every run, record
   both that and `pgrep -lf 'ray/dashboard|ray/_private|ray/autoscaler'`, each process attributed
   by its path. The script's refusal uses the prompt's pattern, unchanged.
6. **The patterns' import brings the stand-in module with it, and that is allowed.**
   `raypoolkit/tests/test_printed_lines.py:25` imports `raypoolkit.tests.standins`. Measured in
   `venv/`: importing it patches nothing; `ray.is_initialized()` stays false and the pool module's
   `ray.wait` is `ray.wait`. "Imports no stand-in" (§2.2) means it uses none. The script checks,
   before it starts Ray, that the pool module's `ray` is the `ray` it imported and that neither
   `ray.wait` nor `ray.get` is a `unittest.mock` object, and prints their `__module__`.
7. **Step 5's progress count follows from the step's own spelling.** The prompt gives step 5's
   notify settings but not its batch sizes. With `notify_min_time_interval=0` and
   `notify_time_interval=0`, every pass of `run()` that waits prints one notification
   (`raypoolkit/RayWorkPool.py:563-595`), and each pass consumes exactly
   `min(process_batch_size, len(inflight))` refs (`:355-358`). So 30 tasks give 30 progress lines
   at the default `process_batch_size=1` and 15 at 2, the planner's figure. The script asserts the
   count its spelling implies, says how in a comment, and prints it. A figure other than 15 that
   follows from the spelling is not a stop; a count that differs between two runs of one spelling
   is (§6, "the smoke script fails").
8. **The ends, and which module runs.** Probed by the orchestrator with `uv` 0.12.20: `uv venv
   --offline -p /opt/local/bin/python3.13` and `uv pip install --offline "ray==2.55.1"` give
   3.13.16 / 2.55.1, and the same with `python3.12` and `"ray==2.43.0"` give 3.12.15 / 2.43.0,
   from the cache. The export is `git archive HEAD` (its `raypoolkit/` is `eaef0ce`'s), installed
   editable with `--offline`. Run the script from the repository root as `env -u PYTHONPATH
   <venv>/bin/python docs/extraction/ray_smoke_run.py`: `sys.path[0]` is then `docs/extraction/`,
   so `raypoolkit` comes from the export, and the printed `raypoolkit.__file__` must be under it,
   which the log checks. (a)–(c) edit the export's module, never the repository's, each in a fresh
   export or reverted with `git apply -R` and its SHA-256 checked. `venv/` is not a smoke-run end.
9. **(d)'s Ray is bounded.** Start it as a background Python process of your own, in the
   scratchpad: it sets `RAY_USAGE_STATS_ENABLED=0`, calls the prompt's `ray.init(...)`, writes a
   ready file, waits for a stop file for at most 180 s, and calls `ray.shutdown()` in a `finally`.
   Run the script while it is up (exit 2, no new session directory of its own), then write the stop
   file and check both process patterns are empty. Anything left is a stop.
10. **The offline wheel, probed.** `git archive v0.2.0` extracted in the scratchpad and built with
    `uv build --wheel --offline` exits 0 with no "absent from" line, and gives
    `raypoolkit-0.2.0-py3-none-any.whl`, **13,565 bytes**, the prompt's 9 entries. Its SHA-256 is
    not compared: an export's file times are its commit's, and a wheel's bytes follow them, so the
    size and entries are the check (03's review).
11. **The deviation counts.** The label counts per log are the prompt's, measured: 01 1 / 8 / 1,
    02 0 / 7 / 1, 03 2 / 5 / 1, 04 0 / 10 / 1, 05 2 / 10 / 2, 06 4 / 9 / 2. Each log's sections
    of observations are where the prompt says (01 §5, 02 §6, 03 §6, 04 §5, 05 §6, 06 §9). The
    document's §8 counts **entries**, and the log says how it counted; where a label appears in a
    sentence that classes several deviations, or in a sentence that says there was none, say how
    it was treated.
12. **DatastoreKit's precedent has eleven sections; this document has twelve.** Its
    `docs/extraction-verification.md` at `39b1348` has no section of decisions. The prompt's §2.1
    table governs: its §7, Decisions, is new here. Read it only through `git -C … show
    39b1348:docs/extraction-verification.md`.
13. **The equivalence check at `v0.1.0`.** Run as `PROVENANCE.md`'s "Re-running the check" says,
    with the worktree in your scratchpad, and remove it after (`git worktree remove`); `git
    worktree list` shows this checkout alone at the end. It reads SGK through `git show` at
    `b510bc9` only.
14. **The counts.** The suite stays **121** in `venv/` and at the high end; it does not see
    `docs/`. `black --check raypoolkit docs` goes from 16 files to **17**, and CI runs it, so the
    script must be black-clean. The index is **0** now, and stays 0 unless the work opens an issue.

**The facts, checked by the orchestrator.** Pass them on.

- **The baseline at `787507a`.** `venv/`: Python 3.12.15, `ray==2.43.0`, `black==25.1.0`,
  `raypoolkit` editable at `0.2.0`. `Ran 121 tests … OK`. `black --check raypoolkit docs`: 16 files
  unchanged. `git diff eaef0ce -- raypoolkit pyproject.toml` is empty. `docs/` holds `adoption/`,
  `extraction/` (`compare_with_source.py` alone) and `OPEN_ISSUES.md`. `git diff 71f0d66` touches
  only `prompts/`.
- **The module's lines the prompt cites**, read at `787507a`: `:530` is
  `replacement_obj = self._post_handler(replacement_obj)`; `:178` is
  `self.results = [None for _ in range(self._num_total_items)]`; 26 lines carry `.hex()`;
  `test_printed_lines.py:35-39` are the three patterns.
- **The clients, at writing.**

  | Client | `HEAD` | Porcelain lines (hash) | Stash | Blob of `RayTools/RayWorkPool.py` |
  |---|---|---|---|---|
  | SGK | `b510bc90b66985532d28996ab4e5b13b0ff71709` | 0 (`da39a3ee5e6b`) | 0 | `b4666fa89abb` |
  | CPBH | `52142d75aebe00855804e2daff4f63aee50ffc3e` | 23 (`a772db72b9bc`) | 0 | `aaa6dc921865` |
  | SI | `7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7` | 0 (`da39a3ee5e6b`) | 0 | `92be5b2c9e4c` |

  The hash is `git status --porcelain | shasum`, first twelve characters.
- **DatastoreKit.** `39b1348` is "Verify the extraction campaign and close it", and adds
  `docs/extraction-verification.md`.
- **Ray.** None was up at writing: both patterns of clarification 5 empty.
- **GitHub, read only.** `origin/main` is `787507a`; local `main` is ahead by this note's commit.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §7 files changed; nothing under `raypoolkit/` or
  `docs/adoption/`; no tag; nothing pushed; no client or DatastoreKit touched; no scratch file in
  the tree.
- **(E2) The script, by reading.** Usage stats off before `ray` is imported; the refusal; the
  versions and `__file__`; the five steps, each isolated; its own values only; exit codes;
  `ray.shutdown()` in a `finally`; imports the standard library, `ray` and `raypoolkit` only.
- **(E3) The script, by running.** Exit 0 at both ends from the orchestrator's own venvs; no Ray
  process left by either pattern; no usage report.
- **(E4) The script bites.** (a), (b) and (d) fail as the prompt's §4.5 says; (c) passes, as
  §1.1 found.
- **(E5) The document.** Twelve sections; its counts recount; its links resolve; its `path:line`s
  read at `eaef0ce`; its reproduction commands run as written.
- **(E6) The release.** The offline wheel's size, entries and modules.
- **(E7) The records and the close.** The log with §5 item 6's additions; the board **CLOSED**;
  the README, `prompts/INDEX.md` and the index in step; the clients unchanged.

**Conventions.** Prompt 01's note's and 06's additions, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run every suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it, and never while a Ray process is up;
- check each breakage diff with `git apply --check` (and `-R --check` once applied), replay it in
  `bash`, and record each export's state before and after (prompt 04's note, clarification 1);
- use the scratchpad subdirectory you are given, never `/tmp` for your own files (Ray's session
  directory is clarification 4's), and put no scratch file under the repository;
- a stop goes to the user;
- check `git log` before committing.
- **Nothing outward-facing.** No `git push`, no `git tag`, no `git fetch`, no `gh` command that
  writes, no install from a URL; every `uv` call `--offline`.
- **Read-only toward every other repository**, as 06's note said: only `git show`, `ls-tree`,
  `log`, `rev-parse`, `status --porcelain` and `stash list`; never a command that writes `.git/`;
  never a file of a working tree; never import, run or open a store of one.
- **Diff and output files have distinct names on this case-insensitive filesystem**: `a.diff` …
  `d.diff`, and nothing that differs from another only by case.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. `git diff eaef0ce -- raypoolkit
   pyproject.toml` is empty.
2. **The baseline.** The suite gives `Ran 121 tests … OK`; `black` 16 files. `git tag` is `v0.1.0`
   and `v0.2.0`; `git ls-remote origin` shows `main` at `787507a` and the two tags as above.
3. **The clients.** Record each one's `rev-parse HEAD`, `status --porcelain | shasum`, `stash list
   | wc -l` and the blob, and check them against the table.
4. **Ray.** Both patterns of clarification 5, attributed by path; and the count and latest of
   `/tmp/ray/session_2*`.
5. **The index.** 0 now; 0 after unless an issue is opened. Tell the agent.
6. **Scratch.** Make the agent's subdirectory of the session scratchpad, empty, and tell it the
   path. Keep your own measurements in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, and its "Read first" list, which it reads itself;
- `HEAD`, the counts, the clients' table, the gate's CI run and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's fourteen clarifications and additions. Clarifications
3, 7 and 9 are the ones that matter: the first so that a run uses no network, the second so that
step 5 asserts what it can know, the third so that (d) cannot leave a Ray behind.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/07-verification-and-close-out.md`, in README
  §5.1's form, with the prompt's §5 item 6 additions.
- **The files it may change are the prompt's §7 list, and nothing else.**
- **It pushes nothing, tags nothing, fetches nothing, installs nothing from a URL**, and writes
  nothing to GitHub.
- **It starts Ray only by running its script, and for (d)**, each with usage stats off, and leaves
  no process behind.
- **It edits, runs and imports no client and not DatastoreKit**, and opens no `.db` file.
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — ten checks

1. **E1, scope.** `git show --stat <commit>` touches only the two new files, the log, the board,
   the campaign README, `prompts/INDEX.md` and the index. `git diff <note> <commit> -- raypoolkit
   pyproject.toml README.md PROVENANCE.md docs/adoption docs/extraction/compare_with_source.py
   .github CLAUDE.md LICENSE .gitignore` is empty. `git tag` and `git ls-remote origin` are
   unchanged; `git worktree list` is this checkout alone.
2. **E7, the clients.** Each client's `HEAD`, porcelain hash, stash count and blob equal §1's.
3. **E2, the script, by reading.** Read it whole, against the prompt's §2.2 and clarifications 3,
   5–7: the environment variable before any import of `ray`; the refusal before anything starts
   (`ray.is_initialized()`, then the prompt's `pgrep`), exiting 2; the versions, `__file__` and the
   mock check; each step in its own `try`, each assertion against values the script built; step
   5's count derived from its spelling; exit 0 or 1; `ray.shutdown()` in a `finally`; imports the
   standard library, `ray` and `raypoolkit` only; a docstring in the form of
   `compare_with_source.py`'s.
4. **E3, the script, by running.** In your own fresh offline venvs at both ends, with your own
   `git archive` export of the commit installed editable, run it as clarification 8 says: exit 0,
   every step `PASS`, `raypoolkit.__file__` under your export, both process patterns empty before
   and after, one new session directory per run. Grep that directory's `logs/` for usage stats, as
   the log did. Run it twice at the high end: step 5's count is the same.
5. **E4, the breakage, by replaying.** Extract (a)–(c) from the log's text and apply each to a
   fresh export of the commit at the high end, each first checked with `git apply --check`: (a)
   fails step 3 alone, naming `None` `store_id`s; (b) fails step 1 with `TypeError`, the others
   pass; (c) passes every step. (d) as clarification 9, with your own bounded session: exit 2,
   nothing started by the script, nothing left after.
6. **E6, the release.** Rebuild the wheel offline from `git archive v0.2.0`, as clarification 10:
   13,565 bytes, the 9 entries, no "absent from" line, and each of its four modules byte-equal to
   `git show eaef0ce:raypoolkit/<module>`. The document's §5 cites the release record's step 4 and
   matches it.
7. **E5, the document, by reading.** Read it whole. Twelve sections under the prompt's §2.1
   names. Its head names `v0.2.0`, `eaef0ce` and the empty diff. Then recount at least these from
   the records yourself: §2's commits (30, by class, clarification 2) and the suite counts; §6's
   eight issues against the board's §4; §7's fourteen decisions against README §6.2; §8's entry
   counts for two logs of your choice, and every UNINTENDED DRIFT entry against its log; §9's items
   for two logs of your choice, each disposition checked against the later logs or the board.
   Each matches, or the document says why not.
8. **E5, the document's sources.** Every relative link and anchor resolves (a scratch script, as
   06's review used); every external link is to `github.com/ds283/…` and names a tag, commit or
   run, and each run cited exists (`gh run view`). Sample ten `path:line`s it cites at `v0.2.0`
   and read each at `eaef0ce`. Run §11's reproduction commands for the suite, `black`, the check
   at `v0.1.0` and the wheel, as written, from a fresh export: each gives what §3–§5 say.
9. **The suite and `black`.** `venv/`: `Ran 121 tests … OK`, with no Ray up. `./venv/bin/black
   --check raypoolkit docs` (25.1.0): 17 files unchanged.
10. **E7, the records and the close.** The log has every section of README §5.1 and each of the
    prompt's §5 item 6 additions; §0's clarifications recorded as deviations (2
    STRUCTURALLY REQUIRED). The board's header says **CLOSED** with 07's row and §2's dated line;
    the README's header, §2 row and §7 line; `prompts/INDEX.md` says closed with its open-issue
    count; the index's date and §1.1 heading, its count matching its rows.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 07* paragraph, in the form of
  06's, after the close. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the document if it says so, and in
    `prompts/INDEX.md`;
  - README §2's status for 07, and its header;
  - the notes line, with this note added and marked "used for 07".
- Anything the review finds that is not residue is opened on the board's §3 and in the index,
  and the campaign's line in `prompts/INDEX.md` gives the count; a closed campaign may carry an
  open issue, as long as the index says so.
- **Put the push to the user, and do none of it unasked.** CI has not run `black` over the smoke
  script. *Recommended:* push `main` as it stands after the follow-up; no tag (07 changes no
  release).
- **Report to the user:**
  - what landed: the verification document and the smoke script, and the campaign closed; the
    suite 121 → 121;
  - the run under Ray at both ends, its time, and that it left no process and made no usage
    report; (a)–(d), and what (c) means for fault 1;
  - the offline wheel;
  - any count the document had to correct against a log;
  - G2–G4 still open, and that each client's adoption is a campaign in its own repository;
  - the push, as a decision for them.
