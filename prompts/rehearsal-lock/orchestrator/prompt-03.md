# Orchestrator — prompt 03, release `v0.3.0`

Read [`../README.md`](../README.md) first: §0, §1, §2, §4, §5 (rules 6, 7 and 10) and §6 (D2, D3,
U1–U6). Then [`prompt-01.md`](prompt-01.md): its §0 "Conventions", which this note keeps unless it
says otherwise. Then the board's *Orchestrator review of prompt 01* and *of prompt 02*, and the
`extraction` campaign's release precedent:
[`../../extraction/orchestrator/prompt-05.md`](../../extraction/orchestrator/prompt-05.md) (its
clarifications 2, 3 and 7, and its §4, the release sequence `v0.2.0` followed).

**You do not write code.** You may:
- run the suite, `black`, and the commands the log records;
- make venvs, exports and wheels of your own in the session scratchpad, and replay the log's
  breakage there, never in the repository tree;
- run the command line and the Python API against a scratch `HOME` with an explicit `lock_dir`,
  never the real one;
- read SGK, CPBH and SI through `git -C <client> show <commit>:<path>`, never their working trees;
- read GitHub's state with `gh api` / `gh run`, never write it;
- fix small residue in a follow-up commit of your own (§4).

You start no Ray (README §5 rule 9: real Ray is 02's and 05's). You do not push or tag. Each is put
to the user (§4).

**The prompt:** [`03-release-v0.3.0.md`](../03-release-v0.3.0.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- 02 landed (`722466a`) and was reviewed (`cc5f2d6`); CI passed at both ends on `cc5f2d6` (run
  40086680695). 03 is written (`6e0ba38`, which touches only `prompts/`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that it
  could move, and hand the agent the corrections as an addendum.
- No Ray process; neither lock location exists under the real `HOME`. One prompt at a time in this
  checkout.

## 0. What makes this prompt unusual

**Its code is two lines of `pyproject.toml`; its weight is a contract three projects will keep.**
`docs/rehearsal-lock.md` becomes the one statement of the shared lock, and the tag that follows is
what every project pins on the switch-over day (D3). A sentence in it that is not true of the
module is a lock one project reads differently from another, and `v0.3.0` is never moved once
made (README §5 rule 10). So the review has four halves:
- **the contract is the module**: every statement it makes is checked against
  `raypoolkit/rehearsal_lock.py` and its tests, not against the prompt or 01's log, and it names no
  client;
- **the documents are true of `v0.3.0`**: `README.md`, `PROVENANCE.md` and `CLAUDE.md` lose what was
  true only of `v0.2.0`, and gain only what the module bears out;
- **the distribution is right, however stale the build directory**: 10 entries, none under
  `raypoolkit/tests/`, with and without the repository's `raypoolkit.egg-info/` copied in;
- **nothing changed under `raypoolkit/` and nothing left the machine**: 226 before and after, no
  printed line moved, no tag, no push, no Ray.

**What moves on purpose:** `pyproject.toml` (two lines); `docs/rehearsal-lock.md` (new);
`README.md`, `PROVENANCE.md`, `CLAUDE.md`; the log, the board, `prompts/INDEX.md`, and
`docs/OPEN_ISSUES.md` if the work opens anything. Nothing under `raypoolkit/`,
`docs/rehearsal-lock/`, `docs/adoption/`, `docs/extraction/` or `.github/`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-24 at `6e0ba38` (the
package as at `722466a`), against the module, with probes against a scratch `HOME` and wheels built
from fresh exports; it started no Ray. Pass them on. Each is an IMPLEMENTATION CHOICE at the
orchestrator's direction unless it says otherwise, and the log says so.

1. **The Python API is not "the five functions with the same exit codes".** STRUCTURALLY REQUIRED:
   the prompt's §2.2 item 2 and README §4's list are not quite the module, and the prompt's §5 makes
   an untrue statement a stop; this is the correction, not a stop. As the module has it
   (`rehearsal_lock.py:50-52`, `:427-669`):
   - the five command functions are `acquire`, `set_pid`, `release`, `status` and
     **`ray_processes_command`**; each returns the command's exit code;
   - **`ray_processes`** is not a command function: it returns a list of `(pid, ppid, command)`
     tuples sorted by pid, each command whole (uncut), and raises `RuntimeError` or `OSError` if
     the table cannot be read;
   - **a bad argument raises `ValueError`**, where the command line exits 2. No function returns 2.
     `status(ray_address=…)` with no `ray_temp_dir` raises `ValueError`;
   - `lock_dir` is a keyword of the first four only;
   - `ray_processes`'s `ps_text` and `self_pid` are test seams (02's log §5, first observation):
     the contract says so, and that no caller passes them.
2. **"This process" is the caller's, so a Ray driver cannot check its own instance through the
   Python API.** Add this to §2.2 item 6's "what it asks of a caller". For an in-process instance
   every seed is a child of the driver: `gcs_server`, `raylet`, `monitor.py`, `log_monitor.py` and
   the dashboard all have the driver's pid as their ppid, at both ends (02's log §3.4, the a1 rows:
   `:437-447` at 2.43.0, `:810-820` at 2.55.1). Since this process's own descendants are never listed, **`ray_processes`
   called in the driver lists nothing of that instance** (the orchestrator's probe on a fixed table
   from those rows: `[]` with `self_pid` the driver's pid; the three seeds and the worker with
   `self_pid` a child of the driver). The command line run as a child of the driver sees them, since
   the driver is then an ancestor: not listed, but its other children are. So the contract says:
   the lock's commands are run in a process of their own (the command line), never through the
   Python API inside a Ray driver; and its check is
   `test_this_process_its_ancestors_and_its_children_are_never_listed` with a probe of your own.
3. **Every exit code, as the module has it, not as README §4 lists it.** The prompt's §2.2 item 7
   says this already; these are the conditions §4's list leaves out. Not a deviation.
   - `acquire` 4: a process of `D`, **or of `A`'s Ray client server**, is alive, or the table
     cannot be read; the lock is released again, and if that removal fails it prints `could not
     release the lock again (…)` and still exits 4. `acquire` 1: the owner file could not be
     written (the lock is removed).
   - `set-pid` 1 also: the lock has no owner file; the owner file has no `pid` line, or more than
     one (`test_an_owner_file_with_no_pid_line_is_refused`, `…_with_two_pid_lines_…`). The pid's
     liveness is checked before the lock is looked at.
   - `release` 1 also: the lock has no owner file; the owner's `ray_address` is neither
     `in-process` nor `host:port` (`test_an_owner_address_that_is_not_usable_is_refused`); the lock
     directory could not be removed.
   - `ray-processes` 1 also when the table cannot be read (to stderr).
   - `status` returns 0 always, an unreadable table included (its line says so).
   - **An `OSError` the module does not handle ends the command with a traceback and exit 1.**
     Measured: with `~/.raypoolkit` a plain file under a scratch `HOME`, `acquire` ends in
     `FileExistsError` from `d.parent.mkdir`, exit 1, and creates nothing (the board's review of 01,
     "Observed, not opened"). The contract says so in one sentence, and lists no traceback as an
     interface.
4. **The match, identity and the argument checks, stated exactly.** Not deviations; each is a
   place where the prompt's shorthand would overclaim.
   - **The temp-dir seed has no leading boundary.** The pattern is `(/private)?` + the directory
     (with a leading `/private` component removed first) + `(?:[/ =]|$)`, searched anywhere in the
     command (`:307-312`). So "as a whole path component" is true at its end only: `/var/tmp/ray-a/x`
     is listed for `/tmp/ray-a` (01's log §5). It over-lists, the safe side. Say "contains …
     followed by", as the module's docstring does.
   - **The client-server seed** needs both `ray.util.client.server` and `--address=<A>` followed by a
     space or the end, each anywhere in the command, for any host (`:315-316`, `:389`).
   - **Identity compares the strings as given.** `/private/tmp/ray-q` and `/tmp/ray-q` are one temp
     dir to the process rule and two callers to the identity check (the orchestrator's probe:
     `acquire` with the first, then `release` with the second exits 1, both sides printed; with the
     first, 0). So a caller passes the same spelling every time.
   - `/` passes the temp-dir checks and over-lists badly (01's log §5): the temp dir is the
     caller's own directory.
   - `ray_address`'s check splits at the **last** colon: a non-empty host with no whitespace, and a
     port of decimal digits, with no range check (`:138-153`). Promise no more than that.
   - `host` is `hostname -s`, or `socket.gethostname()` cut at its first dot if that cannot be run
     (`:187-198`).
   - `owner pid: - (no pid recorded yet)` is printed for `-`, for a missing `pid` line, and for a
     value that is not a number (`_recorded_pid`, `:279-282`).
5. **The lock is a directory; a plain file at its path reads as free.** `status` prints `lock: free
   (<path> does not exist)` whenever the path is not a directory, `release` says `no lock to
   release` and exits 0, and `acquire` says it is held and exits 3 (01's log §5). Only a hand-made
   file can be there. The contract states each condition as the module tests it ("is not a
   directory") and quotes the message as it is. Record it under "Observations not acted on"; it is
   not an issue, and nothing under `raypoolkit/` changes.
6. **What goes where, and how a process is printed.** Refusals and errors go to stderr. These go to
   stdout: `release`'s `no lock to release`, every success line, every line of `status` (its
   unreadable-table line included), and `ray-processes`'s listing. A listed process is `<pid>
   <ppid> <command cut to 150 characters>` (`COMMAND_WIDTH`, `:92`, `:402-403`;
   `test_a_listed_command_is_cut_to_150_characters`), indented four spaces in `status` and in a
   refusal, not indented by `ray-processes`. `status`'s layout is an interface (§2.5), so each line
   and its condition is pinned to a test.
7. **The release check, as `extraction` 05 ran it.**
   - **Build every wheel without `-q`**, its stdout and stderr captured, and record `grep -c "absent
     from"` (extraction 05's clarification 2: `-q` empties the log, so the search can never fail).
   - **The manifest.** The repository's `raypoolkit.egg-info/` was rewritten at 11:29 today: its
     `PKG-INFO` says `0.2.0`, and its `SOURCES.txt` lists **10** files under `raypoolkit/tests/`
     (not `test_rehearsal_lock.py`). §3.1's and §3.2's editable installs rewrite it; that is
     allowed. Before (R2), record its `Version:` line and `grep -c tests/ SOURCES.txt`.
   - **Exports and breakage** as extraction 05's clarification 7: `git archive HEAD | tar -x -C
     <new empty dir>`, the working tree's `pyproject.toml` copied over the export's, each diff
     applied with `git apply` run in the export after `git apply --check`.
   - **What the orchestrator measured**, with 03's two lines applied in each export (`uv` 0.12.20):

     | Build | Entries | Under `raypoolkit/tests/` | Bytes | "absent from" |
     |---|---|---|---|---|
     | (R1) no manifest | 10 | 0 | 21,368 | 0 |
     | (R2) the manifest copied in | 10 | 0 | 21,368 | 0 |
     | (a) `version = "0.2.0"` | 10 | 0 | 21,369 | 0 |
     | (b) the `exclude` line deleted, no manifest | 21 | 11 | 63,134 | 0 |

     (a)'s wheel reports `0.2.0`, so the metadata check fails. (b)'s, installed into a throwaway
     3.13.16 / `ray==2.55.1` venv, gives `import raypoolkit.tests` from `site-packages`. The (R2)
     wheel in a fresh 3.13.16 / `ray==2.55.1` venv passed every item of the prompt's §3.3 from an
     empty directory with `-I`. SHA-256s depend on the export's file times and need not match.
8. **The `ray-processes` check runs from a script file**, the temp dir in a variable inside it (as
   01's clarification 10). The Bash tool's shell carries its whole command string in its argv; if
   that names `/tmp/ray-rpk03-none`, the shell is an ancestor that seeds the walk, and any sibling
   it starts (a `tee`, a pipe's other end) is listed, so the check exits 1. "No process names that
   directory" means none but the checking `grep` and its subshell.
9. **The README's statements of the outside world.** PyPI's newest `ray` is still **2.59.0**
   (2026-10-24), so "Ray up to 2.59.0 today" stays. "Changes in `v0.3.0`" says that moving the pin
   from `v0.2.0` changes nothing else and that the projects move to the new lock together; it does
   not say when a project moves its pin relative to that day, which is 04's to set.
10. **`CLAUDE.md`'s first exception reads "imported from".** The lock module was written new, and its
    provenance note names the two sources it was modelled on; the review of 01 accepted that. The
    exceptions are the user's (2026-10-10), and the prompt keeps the rest of the section: do not
    reword them. Record it under "Observations not acted on"; the orchestrator puts it to the user.
11. **`venv/` stays the low end and is not rebuilt.** Its editable reinstall is `--no-deps` (prompt
    §3.2). The fresh suite venvs, the wheel venv and the breakage venvs are separate, in your scratch
    directory, made with `uv` (`/opt/local/bin/python3.12` and `python3.13`).
12. **The board and the README.** The agent updates the board's header and 03's row, and
    `prompts/INDEX.md`. README §2's status for 03 is the review's.

**The facts, checked by the orchestrator on 2026-10-24.** Pass them on.

- **The tree.** Branch `main`, `HEAD` `6e0ba38` before this note, clean; this checkout is the only
  worktree. `origin/main` is `cc5f2d6`; local `main` is one commit ahead (`6e0ba38`), and this note
  makes two. Tags `v0.1.0` (object `0a9cdb2`, on `4e90a8a`) and `v0.2.0` (object `4e7eb15`, on
  `eaef0ce`), the same on `origin`. `git diff cc5f2d6 HEAD` touches only `prompts/`.
- **The baseline.** `venv/` (3.12.15 / 2.43.0 / `black` 25.1.0): `Ran 226 tests … OK` (2.3 s);
  `importlib.metadata` gives `0.2.0` and `['ray>=2.43']`. `./venv/bin/black --check raypoolkit
  docs`: 20 files unchanged. `pyproject.toml` is as the prompt's §2.1 says.
- **The machine.** No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` exit 1). No `RAY_*`
  variable. `~/ScienceData` is a directory; `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` do
  not exist. `/tmp/ray`, `/tmp/ray-cpbh`, `/tmp/ray-cpbh-decoy`, `/tmp/ray-decoy`, `/tmp/ray-rpk02a`,
  `/tmp/ray-rpk02b`, `/tmp/ray-rpkp` and `/tmp/ray-si` exist and are not touched.
- **The clients, read only.** SGK `216e44d` (branch `handover-remedial`), CPBH `807f175`
  (`jordan-normalization`), SI `7071bb8` (`rrk-adoption`; `8b4f615` is its ancestor). Each pins
  `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0` in `requirements.txt` and has no
  `RayTools/` at that commit. SGK's `tools/rehearsal_lock.py` and its tests are still blobs
  `ea14336` and `cdeecd6`; CPBH's `ray_cluster.sh` `eaae1e7`; SI's `6c8eada`; the brief is blob
  `d86ad43` at `8b4f615`. The `extraction` board gives G2 and G3 holding since 2026-10-12, G4 since
  2026-10-20, with `RayTools/` deleted at SGK `643c3b2`, CPBH `303324b` and SI `ef13445`.
- **The prompt's line references hold** at `6e0ba38`: `README.md` opening `:1-8`, Status `:10-27`
  (DatastoreKit's paragraph `:25-27`), Supported versions `:58-72`, the pin `:79`, Developing
  `:235-255`, Licence `:257-260`; `PROVENANCE.md` `:3`, "Since `v0.1.0`" `:84-92`, the freeze
  `:94-101`; `CLAUDE.md` "What this repository is" `:7-28`, Releases `:79-92`, Repository mechanics
  `:94-`.
- **The module and its tests.** `rehearsal_lock.py` 738 lines; `test_rehearsal_lock.py` 103 tests
  in ten classes and `TestLicenceHeader`. 01's log §1.2: "41 of the 42 are carried, onto 39 tests".
  02's log §5 and §3.9 (`:1282`): the in-process dashboard on 8265 under `ray[default]`, despite
  `include_dashboard=False`, at both ends; the reaper gone at `ray.shutdown()`.
- **Expected counts.** The suite is **226** before and after, in every venv. The index is **0** now,
  and 0 after unless the work opens something.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §6 files changed; nothing under `raypoolkit/`; no tag; nothing
  pushed; no Ray.
- **(E2) `pyproject.toml`.** Two lines, and nothing else.
- **(E3) The suite.** 226, OK, in `venv/` (reporting `0.3.0`) and at both ends in fresh venvs.
- **(E4) The distribution.** 10 entries with and without the manifest; the release check passes at
  `0.3.0`, the CLI's three checks included.
- **(E5) The breakage.** (a) and (b) fail as logged.
- **(E6) The contract.** Every statement numbered and checked; clarifications 1–6 reflected; no
  client named.
- **(E7) The other documents.** `README.md`, `PROVENANCE.md` and `CLAUDE.md` as §2.3–§2.5, every
  README name checked, every relative link resolving.
- **(E8) The records.** The log with the prompt's §4.5 additions; the board, `prompts/INDEX.md`,
  the index.

**Conventions.** 01's note's (its §0's last list), and all bind the agent:
- stage by explicit path only, and show `git diff --cached --name-only` before committing; `venv/`
  and `*.egg-info/` are gitignored and never staged;
- write "this commit" for the SHA; the orchestrator substitutes it;
- run every suite in the foreground, its output written to a scratch file and the verdict grepped
  from it;
- record each breakage as a diff, exactly as applied, with `git apply --check` (and `-R --check`
  once applied);
- use the scratchpad subdirectory you are given, never `/tmp` (but for the probe's nonexistent temp
  dir name), and put no scratch file under the repository, least of all under `raypoolkit/`;
- start no Ray, and never touch `~/ScienceData/.rehearsal-lock`, `~/.raypoolkit` or anything under
  `/tmp/ray*`;
- a stop goes to the user;
- check `git log` before committing.

Three additions, from `extraction` 05:
- **Nothing outward-facing.** No `git push`, no `git tag`, no `gh` command that writes.
- **One export per build**, made fresh; a wheel is never built in the repository tree.
- **The venvs you verify with are not the venvs you break.**

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` are
   empty; `git worktree list` shows this checkout alone. `git diff 722466a -- raypoolkit
   pyproject.toml README.md PROVENANCE.md CLAUDE.md .github` is empty.
2. **The baseline.** 226, OK; `black --check` 20 files; `git tag` is `v0.1.0` and `v0.2.0`, and
   `git ls-remote origin` shows `main` at `cc5f2d6` and both tags as §0.
3. **The machine.** `pgrep`, the real `HOME`, the `RAY_*` environment: as §0.
4. **The manifest.** `raypoolkit.egg-info/` exists; record its `Version:` and its count under
   `tests/`.
5. **Scratch.** Make the agent's subdirectory of the session scratchpad, empty, and give it the
   path; keep your own measurements in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md` and `CLAUDE.md`, and logs 01
  and 02 (the sections the prompt names);
- `HEAD`, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in its scratch directory.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's twelve clarifications. Clarifications 1–6 are the ones
that matter: each corrects or sharpens a statement the contract would otherwise make untrue of the
module, and 2 adds the one thing a caller most needs that the prompt does not say.

Tell it plainly:
- **One commit, at the end**, with the log `logs/03-release-v0.3.0.md` in README §5.1's form and
  the prompt's §4.5 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else.** Nothing under
  `raypoolkit/`, `docs/rehearsal-lock/`, `docs/adoption/` or `docs/extraction/`; not `.github/`,
  `LICENSE`, `.gitignore`, the campaign README, or anything under `orchestrator/` or `planning/`;
  and it must not delete, clean or hand-edit `raypoolkit.egg-info/`.
- **It pushes nothing and tags nothing**, and writes nothing to GitHub.
- **It builds no wheel in the repository tree.**
- **It edits no client repository and runs none of their code.**
- **It starts no Ray**, and touches neither lock location under the real `HOME`.
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — eleven checks

1. **E1, scope.** `git show --stat <commit>` lists only the prompt's §6 files. `git diff 6e0ba38
   <commit> -- raypoolkit docs/rehearsal-lock docs/adoption docs/extraction .github LICENSE
   .gitignore prompts/rehearsal-lock/README.md` is empty. `git tag` and `git ls-remote origin`
   unchanged; no `build/` or `dist/` in the repository root; `git worktree list` this checkout
   alone. No Ray process; neither lock location under the real `HOME`.
2. **E2, `pyproject.toml`.** `git diff 6e0ba38 <commit> -- pyproject.toml` is the version and the
   description, as §2.1, and nothing else.
3. **E3, the suite, by running.** `venv/`: `Ran 226 tests … OK`, and `importlib.metadata` gives
   `0.3.0` and `['ray>=2.43']`. Then **your own** fresh venv at the high end (3.13.16 / 2.55.1,
   editable, one resolve): 226, OK.
4. **E4, the distribution, re-built.** (R1') and (R2') from fresh exports of `git archive
   <commit>`, built without `-q`: 10 entries each, the list of clarification 7's table, 0 "absent
   from"; the five modules byte-equal to the commit's. Install (R2') into a fresh 3.13.16 /
   `ray==2.55.1` venv and run the prompt's §3.3 checks from an empty directory with `-I`, the
   `ray-processes` check from a script file (clarification 8). This is the build the tag will stand
   on.
5. **E5, the breakage, by replaying.** Extract (a) and (b) from the log's text and replay each in a
   fresh export: (a) gives a `0.2.0` wheel; (b) 21 entries, 11 under `raypoolkit/tests/`, and
   `import raypoolkit.tests` from a throwaway venv. Then the orchestrator's own:
   - (o1) `include-package-data = true` with the manifest copied in: it must ship the tests its
     `SOURCES.txt` lists, with 2 "absent from" lines (measured at `6e0ba38`: 20 entries, 10 tests,
     51,047 bytes), so that the setting, not the `exclude` alone, still guards a stale manifest.
6. **E6, the contract, by reading it against the module.** Read `docs/rehearsal-lock.md` whole,
   with `rehearsal_lock.py` open beside it. Its sections are §2.2's eleven, in order. Every exit
   code and condition is the module's (clarification 3); the Python API is clarification 1's; the
   process rule is clarification 4's, exactly; clarification 2's paragraph is there; every `status`
   line is quoted as the module prints it, with its condition (clarifications 5 and 6). Then take
   the log's numbered table of statements and check ten of them yourself, choosing those with a
   probe rather than a named test first, against a scratch `HOME`.
7. **E6, no client.** `grep -n -i -E 'secondary|sgk|champbh|cpbh|stochastic|instanton'` over
   `docs/rehearsal-lock.md`, and over the README's added lines (`git diff 6e0ba38 <commit> --
   README.md | grep '^+'`), finds nothing; no client's port or file is named.
8. **E7, the README.** Every code span in its new and changed text that names a Python name,
   option, command, exit code or path is in the log's list, with how it was checked; spot-check
   five. Status describes `v0.3.0` and keeps `v0.2.0`, `v0.1.0` and DatastoreKit; "Changes in
   `v0.3.0`" is before "Changes in `v0.2.0`" and says nothing of when a client moves its pin
   (clarification 9); the pin is `@v0.3.0`; "The rehearsal lock" sits between "Using it" and
   "Developing" and does not copy the contract; Licence says five modules. Every relative link in
   the four documents resolves to a file tracked at `<commit>`.
9. **E7, `PROVENANCE.md` and `CLAUDE.md`.** `git diff 6e0ba38 <commit> --` each. `PROVENANCE.md`:
   the opening names `RayWorkPool`; "Since `v0.1.0`" no longer says SGK's copy is frozen; "Since
   `v0.2.0`" gives every blob and commit of §2.4 as §0's facts have them; the freeze section gains
   one sentence with G2–G4's dates; nothing else changed. `CLAUDE.md`: the first sentence, the
   table (pins at the three commits, each client's own lock until the switch-over, dated
   2026-10-24), the Releases paragraph, the mechanics bullet; the exceptions' wording unchanged
   (clarification 10).
10. **`black`.** `./venv/bin/black --check raypoolkit docs`: 20 files unchanged.
11. **E8, the records.** The log has every section of README §5.1 and the prompt's §4.5 additions:
    every venv's versions, install commands and verdict; `venv/`'s metadata before and after;
    (R1) and (R2) in full, with the manifest's state; the statements table; the README's names;
    (a) and (b); 226 → 226; §0's clarifications recorded, clarification 1 as STRUCTURALLY
    REQUIRED. The board's header says `v0.3.0` is ready to be tagged once CI passes on 03's commit
    and that no tag was made; 03's row (landed, "this commit", 226 → 226); `prompts/INDEX.md`'s
    line; the index counted, matching its header.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 03* paragraph, in the form of
  02's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 03, and its header;
  - the notes line, with this note added and marked "used for 03".
- Anything the review finds that is not residue is opened on the board's §3 and in the index. An
  open issue is not by itself a bar to the tag; one that makes the contract, the README or the wheel
  untrue is, and goes to a fix prompt first.
- **Put the release sequence to the user, and do none of it unasked.** It is outward-facing, and
  `v0.3.0` is the tag every project pins on the switch-over day; it cannot be moved once made.
  1. **Push.** *Recommended:* push 03's commit alone first (`git push origin <03's SHA>:main`), so
     that CI runs on it; `6e0ba38` and this note go with it, touching only `prompts/`. Then the
     review's follow-up.
  2. **CI.** Both ends green on 03's commit, read with `gh run list` / `gh run view`. If either is
     red, no tag: the failure goes on the board's §3, and a fix prompt is written first.
  3. **The tag.** `v0.3.0`, annotated (`raypoolkit 0.3.0`, as `v0.2.0`'s), on 03's commit, and
     pushed. Made by the user, or on the user's explicit instruction in that turn (`CLAUDE.md`,
     "Releases"; README §5 rule 10).
  4. **A client's install, checked**, as `v0.2.0`'s was: `uv pip install --no-cache "raypoolkit @
     git+https://github.com/ds283/RayPoolKit@v0.3.0" "ray==2.55.1"` into a fresh 3.13.16 venv in
     the scratchpad: `direct_url.json` names `v0.3.0` and 03's commit; the installed package is the
     five modules and no `tests/`; from an empty directory with `-I`, `version` is `0.3.0`,
     `requires` is `['ray>=2.43']`, `ray.is_initialized()` is false, `import raypoolkit.tests`
     raises `ModuleNotFoundError`, and `python -I -m raypoolkit.rehearsal_lock status` with `HOME`
     an empty scratch directory exits 0 and leaves it empty.
  5. **Record it** on the board as *Release of `v0.3.0`*, in a commit of its own, with the header,
     README §2's row 03 and `prompts/INDEX.md` saying `v0.3.0` is tagged; then put that push to the
     user too.
- **Report to the user:**
  - what landed: `v0.3.0`'s two lines, the contract, the three documents; the suite 226 → 226 at
    each end; nothing under `raypoolkit/` changed;
  - what the contract says that the prompt did not (clarifications 1–5), above all that a Ray
    driver cannot check its own instance through the Python API;
  - the wheel: 10 entries with and without the manifest, the orchestrator's rebuild matching, (a),
    (b) and (o1);
  - clarification 10's wording, as a decision for them;
  - the release sequence above, as a decision for them;
  - that 04, the switch-over checklists, is measured against `v0.3.0` and can be written once the
    tag exists.
