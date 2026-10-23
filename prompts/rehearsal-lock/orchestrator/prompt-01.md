# Orchestrator — prompt 01, the lock module

Read [`../README.md`](../README.md) first: all of §0, §1, §4, §5 and §6. This is the campaign's
first note. Its conventions are `extraction`'s (`../../extraction/orchestrator/prompt-01.md` §0's
last list, and `prompt-04.md`'s two additions), restated below where they bind the agent.

**You do not write code.** You may:
- run the suite, `black`, and the commands the log records;
- replay the log's deliberate-breakage diffs with `git apply`, and revert them;
- make a high-end venv of your own in the session scratchpad;
- run the command line against a scratch `HOME`, never the real one;
- read SGK, CPBH and SI through `git -C <client> show <commit>:<path>`, never their working trees;
- fix small residue in a follow-up commit of your own (§4).

You start no Ray (README §5 rule 9: real Ray is 02's and 05's, under the lock). You do not push or
tag.

**The prompt:** [`01-the-lock-module.md`](../01-the-lock-module.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** none expected ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- The plan is committed (`6e559bf`), the prompt is written and U1–U6 recorded (`d7d914d`), and
  phase 2's wait for G2 is recorded (`50d91c7`).
- G1 holds for 01: SGK's `tools/rehearsal_lock.py` and its tests are blobs `ea14336` and `cdeecd6`
  at `216e44d`.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that it
  could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the first code of the campaign, and every line of it is a safety property shared by three
projects.** A check that is too loose lets two rehearsals run at once; one that is too strict
leaves a lock nobody can release. The module is small, so the review is mostly about the tests:
- **each refusal stands alone**: every refusal test leaves exactly one reason standing, and a
  mutation of that one check fails it (§3.1's M1–M14, and the orchestrator's (o1)–(o4) of §3);
- **the process rule is CPBH's `awk` in Python**, with SGK's treatment of this process's tree;
  its corners (the `/private` spelling, the whole-component end, the client server, ancestors)
  are where a quiet mistake hides;
- **nothing reaches the real lock**: no test and no transcript touches `~/.raypoolkit` or
  `~/ScienceData/.rehearsal-lock` under the real `HOME`;
- **the package names no client** but in the module's provenance note.

**What moves on purpose:** two new files, `raypoolkit/rehearsal_lock.py` and
`raypoolkit/tests/test_rehearsal_lock.py`; two tests added to
`raypoolkit/tests/test_package_imports.py`; the log, the board and `prompts/INDEX.md`.
Nothing else under `raypoolkit/`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-23 at `50d91c7`. Pass
them on. Each is an IMPLEMENTATION CHOICE at the orchestrator's direction unless it says otherwise,
and the log says so.

1. **The licence header is not covered by the existing header test, and that test is not 01's to
   change.** `test_inherited_faults.py:35` is a fixed tuple, `PACKAGE_MODULES = ("RayWorkPool.py",
   "_timing.py", "contract.py", "__init__.py")`, and the file is outside the prompt's §6 list. So
   `test_rehearsal_lock.py` carries one test of its own: the module's first 15 lines equal
   `LICENCE_HEADER`, **imported** from `raypoolkit.tests.test_inherited_faults` (the constant
   only, never a `TestCase` class, which unittest would then collect twice and inflate the count).
   Record in "Observations not acted on" that `PACKAGE_MODULES` does not grow by itself; it is not
   an issue, since the new test covers the new module.
2. **The guard's `-m` test.** `_run_child(code)` runs `-c` only; leave it, and the three tests,
   unchanged. Add a sibling helper for an argument list. Recommended: one child,
   `[sys.executable, "-I", "-X", "importtime", "-m", "raypoolkit.rehearsal_lock", "--help"]`, from
   an empty temporary directory with `CHILD_TIMEOUT`: it exits 0, its stdout starts
   `usage: python -m raypoolkit.rehearsal_lock`, and no module named in stderr's `import time:`
   lines (the last `|` column, stripped) has a root in `FORBIDDEN_ROOTS`. This runs the literal
   command, not a stand-in for it. **`ray` is loaded by it**, through the package root (U3), so the
   test must not assert that `ray` is absent; the module's own imports are test (a)'s business.
   Test (a) uses the guard's `imported_modules` and `sys.stdlib_module_names` with neither `ray`
   nor `raypoolkit` allowed.
3. **Ancestors seed the walk; they are never listed.** The prompt's §2.3 and README §4 take seeds
   from every process and subtract the safe set at the end (step 5). So an ancestor whose command
   names the temp dir seeds the descendant walk, and its other children (this process's siblings)
   are listed. That is SGK's rule (its `ray_processes`, "this process and its ancestors seed the
   walk … but are never themselves listed"), and not CPBH's (`if (p in safe) continue` before
   marking, so an ancestor never seeds). Implement the prompt's, which lists more and so is the
   safe side for `acquire`. Pin it with a test: an ancestor naming the temp dir is not listed, and
   its other child is. Not a deviation (it is what the prompt says); the log states it. **Do not
   add CPBH's `ray_cluster.sh` exclusion**: §4 has none, and it would name a client's script in
   the package.
4. **`/private` is stripped as a whole leading component only**: when the directory starts with
   `/private/`. CPBH's `${1#/private}` turns `/privateer/ray-a` into `er/ray-a`, which then matches
   `/tmp/er/ray-a`. Pin it: for `/privateer/ray-a`, a command naming `/tmp/er/ray-a` is not listed.
   **No leading boundary** is added: §4 says "contains", so `/var/tmp/ray-a/x` matches
   `/tmp/ray-a`. That over-lists, the safe side; record it in "Observations not acted on", not as
   an issue.
5. **An owner file whose values fail §2.2's checks.** An owner file of a client's shape today can
   carry `ray_temp_dir: in-process`, and a hand-edited one anything. No valid caller can pass
   `in-process` (§2.2), so such a lock is never the caller's; the identity tests of §2.6 item 8
   say so. Two places read the owner's values without a caller's to compare:
   - **`status` with no `--ray-temp-dir`** uses the owner's `ray_temp_dir` and `ray_address` only
     when both pass §2.2's checks. Otherwise its last line is exactly
     `Ray processes: the owner's ray_temp_dir or ray_address is not usable`, pinned by a test.
   - **`release`** has passed the identity check, so the owner's temp dir is the caller's, valid.
     If the owner's `ray_address` is neither `in-process` nor `host:port`, the process check
     cannot be run as §4 says: **refuse (1)**, naming the value, as for an unreadable table. Pin it
     with a test whose only reason is that (dead pid, no processes).
6. **`ray_processes` checks its arguments** as §2.2 says (`ValueError`), as every command does. It
   catches nothing: the commands catch `RuntimeError` and `OSError` from it (SGK's pair).
7. **Name the identity helper** (for example SGK's shape, `_not_callers_reason(owner, project,
   ray_temp_dir)` → `None` or why not), and every other helper beyond README §4's list, in the log.
8. **The process-rule fixtures are reconstructions.** `planning/tempdir_probe-ray-*.txt` cut each
   command at 150 characters and replace the interpreter and venv by `<python>` and `<venv>`; the
   2.55.1 run was made with a client's venv and names its path. Keep the trees (pids, ppids, which
   process is a seed, a descendant or neither, and the reaper below the driver), and write each
   command out in full with neutral paths (for example `/opt/venvs/a/bin/python` and
   `/opt/venvs/a/lib/python3.12/site-packages/ray/…`). Each seed names the temp dir in a form Ray
   uses (`--log_dir=/tmp/ray-a/session_<stamp>/logs`,
   `--raylet_socket_name=/tmp/ray-a/session_<stamp>/sockets/raylet`, `--temp-dir=/tmp/ray-a`,
   `--session-dir=/tmp/ray-a/session_<stamp>`); the driver's names none (the temp dir is in its
   code); the reaper is `…/site-packages/ray/_private/ray_process_reaper.py`, naming none. A comment
   says they are reconstructions of README §0.3's trees, which 02 re-measures. The orchestrator did
   not start Ray to capture full lines (rule 9).
9. **No client name in the tests**, in code, strings, docstrings or comments (`CLAUDE.md`). SGK's
   tests name two clients in their fixtures and docstring; the port does not. The test module's
   docstring may say its tests are ported from the source module named in `rehearsal_lock`'s
   provenance note, without naming it.
10. **§3.2's transcript runs as a script file**, `cli.sh` in your scratch directory, run as
    `HOME=<scratch home> bash cli.sh`, with the temp dir (for example `/tmp/ray-rpk01-cli`) set in
    a variable inside it. The Bash tool's shell carries its whole command string in its argv; if
    that names the temp dir, the shell is an ancestor that seeds the walk (clarification 3), and
    the `sleep` it started is listed as a process of the temp dir, so the first `release` would be
    refused for two reasons. The log records the script, its output and each exit status. Check
    first that no process names the temp dir (`ps -axww -o command= | grep -F <dir>` empty but for
    the `grep`).
11. **macOS paths in tests.** `tempfile` directories are under `/var/folders/…`, which resolves to
    `/private/var/folders/…`; the old-location comparison resolves both sides (prompt §2.2 step 1),
    so a patched `HOME` compares right. `Path.home()` reads `HOME` at each call on POSIX (3.12 and
    3.13).

**The facts, checked by the orchestrator on 2026-10-23.** Pass them on.

- **The tree.** Branch `main`, `HEAD` `50d91c7` before this note, clean; this checkout is the only
  worktree. Local `main` is three commits ahead of `origin/main` (`7ba95fc`): `6e559bf`,
  `d7d914d`, `50d91c7`, and this note makes four. CI has run on none of them. Tags `v0.1.0`
  (`4e90a8a`) and `v0.2.0` (`eaef0ce`).
- **G1.** SGK `HEAD` is `216e44d` (branch `handover-remedial`), clean;
  `tools/rehearsal_lock.py` is `ea1433664ff4…` and `tools/tests/test_rehearsal_lock.py`
  `cdeecd600052…` at both `216e44d` and `HEAD`; the module's last change is `c863055`. SGK's
  `prompts/runregistry-extraction/02a-the-rehearsal-lock-helper.md` exists at `216e44d`. CPBH
  `HEAD` is `807f175` (branch `jordan-normalization`), `ray_cluster.sh` blob `eaae1e7` there.
  **SI's `HEAD` has moved** to `60687f0` (branch `rrk-adoption`); `8b4f615` is its ancestor, SI's
  `main` is `1c223e8` ("Record the merge of dk-and-rpk-migration into main"), and `ray_cluster.sh`
  is still blob `6c8eada` at `HEAD`. 01 reads SI only at `8b4f615` (the brief, blob `d86ad43`), so
  this is not a stop; it is recorded for 04.
- **SGK's module, as the model.** 475 lines; 42 tests (`grep -c '    def test_'`), in classes
  `TestAcquire` 6, `TestSetPid` 9, `TestRelease` 11, `TestRayProcesses` 7 (two of them on
  `venv_roots`, which is not carried), `TestDefaultLockDirectory` 2, `TestOwnerParser` 3,
  `TestCommandLine` 4. `pid_alive` treats `PermissionError` as alive; `_recorded_pid` reads `-` or
  a non-number as no pid; `parse_owner` keeps the value after the first `": "`; the ancestor walk
  stops at pid 1 or a pid missing from the table. Its `_ps_output` raises `RuntimeError` on a
  non-zero status, and the commands catch `(RuntimeError, OSError)`.
- **CPBH's rule** (`ray_cluster.sh:152-189` at `807f175`): `temp_dir_regex` strips `/private` by
  `${1#/private}`, escapes only `.`, and appends `([/ =]|$)`; the client-server regex is
  `ray[.]util[.]client[.]server --address=127[.]0[.]0[.]1:<port>( |$)`, adjacent and with a fixed
  host. The prompt's (§2.3) takes `re.escape` of the whole directory, any host, and the two parts
  anywhere in the command; follow the prompt.
- **The guard** (`test_package_imports.py`): `ALLOWED_ROOTS = {"ray", "raypoolkit"}`,
  `FORBIDDEN_ROOTS = ("datastorekit", "Datastore", "RayTools", "utilities")`, `CHILD_TIMEOUT = 300`.
  Test 1 walks every `.py` under `raypoolkit/`, the tests included, so the new test module may
  import only the standard library and `raypoolkit`.
- **The workflow** runs the suite on `ubuntu-24.04` at 3.12.15 / 2.43.0 and 3.13.16 / 2.55.1, and
  `black --check raypoolkit docs` at the low end. No test may read the real `ps`.
- **The toolchain.** `venv/`: Python 3.12.15, `ray==2.43.0`, `black==25.1.0`, 25 packages with the
  editable `raypoolkit` (at `50d91c7`). `uv` is `/opt/local/bin/uv`; `/opt/local/bin/python3.13`
  exists. The high end, as `extraction` 03 made it: `uv venv -p /opt/local/bin/python3.13 <dir>`,
  then `uv pip install --python <dir>/bin/python -e <repository> "ray==2.55.1" "black==25.1.0"`.
  That rewrites the gitignored `raypoolkit.egg-info/`; allowed, never staged.
- **The baseline.** `Ran 121 tests … OK`, by module: `test_construction` 15,
  `test_inherited_faults` 6, `test_package_imports` 3, `test_printed_lines` 18, `test_run_paths`
  22, `test_scheduling` 7, `test_standins` 30, `test_task_builder` 20. `black --check raypoolkit
  docs`: 17 files unchanged.
- **Expected counts.** The suite is **121** before and **121 + 2 + N** after, N the new module's.
  The index is **0** now, and 0 after unless the work opens something.
- **The real `HOME`.** `~/.raypoolkit` does not exist. `~/ScienceData` exists;
  `~/ScienceData/.rehearsal-lock` does not.
- **Ray.** No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §6 files changed; `__init__.py`, `RayWorkPool.py`,
  `contract.py`, `_timing.py`, `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md` and
  every other test untouched. Nothing pushed or tagged.
- **(E2) The interface.** The module is README §4 and the prompt's §2.2–§2.3, with §0's
  clarifications; standard library only; no client named outside its provenance note; no option to
  break, wait, retry or move the lock.
- **(E3) The suite.** 121 → 121 + 2 + N, OK, at both ends.
- **(E4) The refusals bite.** M1–M14 each fail what the log says, and (o1)–(o4) of §3 fail too.
- **(E5) Isolation.** No test reads the real `ps` or reaches the real `HOME`.
- **(E6) The records.** The log with the prompt's §4.3 additions; the board, `prompts/INDEX.md`,
  the index.

**Conventions.** All bind the agent:
- stage by explicit path only, and show `git diff --cached --name-only` before committing;
  `venv/` and `*.egg-info/` are gitignored and never staged;
- write "this commit" for the SHA; the orchestrator substitutes it;
- run every suite in the foreground, its output written to a scratch file and the verdict grepped
  from it;
- record each breakage as a diff that `git apply` replays on the committed tree; check it with
  `git apply --check`, and `-R --check` once applied; replay in `bash`. The work is uncommitted
  while the breakage runs, so "restored" means: the SHA-256 of every changed file and
  `git status --porcelain --untracked-files=all` equal what they were before the item. Revert with
  `git apply -R`, never `git checkout`, `git restore` or `git stash`;
- name diff and output files so that none differs from another only by case (`m01.diff` …
  `m14.diff`): the filesystem is case-insensitive;
- use the scratchpad subdirectory you are given, never `/tmp` for files; no scratch file under the
  repository, least of all under `raypoolkit/` (the suite and the guard collect it);
- read the clients only through `git -C <client> show <commit>:<path>`; never their working trees,
  never their code or tests;
- start no Ray; leave any Ray process you find alone, and say so;
- nothing outward-facing: no `git push`, no `git tag`, no `gh` command that writes;
- a stop goes to the user through the orchestrator;
- check `git log` before committing, and never assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` are
   empty; `git worktree list` shows this checkout alone.
2. **G1.** Re-run `git -C …/SecondaryGWKit rev-parse 216e44d:tools/rehearsal_lock.py
   216e44d:tools/tests/test_rehearsal_lock.py`; `ea14336…`, `cdeecd6…`.
3. **The baseline.** 121, OK; `black --check` clean.
4. **The real `HOME`** and **Ray**: record both, as above.
5. **Scratch.** Make the agent's subdirectory of the session scratchpad, empty, and give it the
   path; keep your own measurements in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md` and `CLAUDE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in its scratch directory.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's eleven clarifications. Clarifications 3, 4 and 5 are
the ones that change behaviour; 2 and 10 keep a test and the transcript honest.

Tell it plainly:
- **One commit, at the end**, with the log `logs/01-the-lock-module.md` in README §5.1's form and
  the prompt's §4.3 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else.** In particular not
  `__init__.py`, `RayWorkPool.py`, `contract.py`, `_timing.py`, `test_inherited_faults.py` or any
  other existing test, `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `.github/`, the
  campaign README, or anything under `orchestrator/` or `planning/`.
- **It pushes nothing and tags nothing.**
- **It edits no client repository and runs none of their code.**
- **It starts no Ray, and touches neither real lock location.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — nine checks

1. **E1, scope.** `git show --stat <commit>` lists only the prompt's §6 files. `git diff 50d91c7
   <commit> -- raypoolkit/__init__.py raypoolkit/RayWorkPool.py raypoolkit/contract.py
   raypoolkit/_timing.py raypoolkit/tests/test_inherited_faults.py raypoolkit/tests/standins.py
   pyproject.toml README.md PROVENANCE.md CLAUDE.md .github` is empty. `git diff` of
   `test_package_imports.py` adds two tests and at most one helper, and changes no existing line
   but imports. `git tag` and `git ls-remote origin` unchanged.
2. **E2, the module, by reading.** Read `rehearsal_lock.py` whole against README §4 and the
   prompt's §2.2–§2.3: the header byte for byte; locations computed per call, no environment read
   but `HOME` through `Path.home()`; the arguments checked before anything is touched; `acquire`'s
   five steps in order, the old-location check before any `mkdir`; `os.mkdir` without `exist_ok`;
   `set_pid` and `release` refuse as listed; `status`'s layout; argparse with no `--force`,
   `--wait`, `--retry` or `--lock-dir`; stderr for refusals. The rule: `/private` stripped as a
   component; the end boundary `(/| |=|$)`; the client-server seed only for `host:port`, with
   `( |$)`; ancestors seed but are never listed. `grep -niE
   'secondarygwkit|champbh|stochasticinstantons|\bsgk\b|\bcpbh\b'` over the two new files finds
   the provenance note only.
3. **E3, the suite, by running.** In a fresh shell, `venv/` gives `Ran 121+2+N … OK`, by module.
   Then **your own** high-end venv (3.13.16 / 2.55.1): the same count, OK.
4. **E4, the breakage, by replaying.** Extract M1–M14 from the log and replay each from the clean
   tree at 01's commit; each fails the tests the log lists. Then four of the orchestrator's own:
   - (o1) the seeds skip the safe set (CPBH's rule): the sibling test of clarification 3 fails;
   - (o2) `/private` stripped by `removeprefix("/private")`: the `/privateer` test fails;
   - (o3) the client-server seed without its `( |$)`: the `127.0.0.1:64000` test fails;
   - (o4) the old-location check moved after the parent's `mkdir`: the "creates nothing at the new
     location" test fails.
   `git status` is clean after each.
5. **E5, isolation, by running.** Run the suite with `HOME` set to an empty scratch directory; it
   holds no `.raypoolkit` and no `ScienceData` afterwards. The real `~/.raypoolkit` and
   `~/ScienceData/.rehearsal-lock` are as §0 records. `grep -n "_ps_output\|subprocess" ` over the
   test module shows every `ps` patched and no real `ps` read.
6. **The command line, by running.** Your own §3.2 transcript, from a script, against a scratch
   `HOME`: the exit statuses equal the log's.
7. **The tests, by reading.** Every refusal test leaves one reason standing (a dead pid or `pid: -`
   with no processes for an identity refusal; the caller's owner and no processes for a live pid;
   the caller's owner and `pid: -` for processes). `status` pinned line by line. The fixtures are
   neutral, and the reconstructed trees say so. Every test patches `HOME` and, but for the
   location tests, passes `lock_dir`.
8. **`black`.** `./venv/bin/black --check raypoolkit docs` is clean.
9. **E6, the records.** The log has every section of README §5.1 and the prompt's §4.3 additions:
   `pip freeze`, the counts before and after (by module), the transcript, the real `HOME` before and
   after, `git diff --stat`, the helpers named, §0's clarifications recorded as deviations. The
   board's header and 01's row; `prompts/INDEX.md`'s line; the index counted, matching its header.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph, in the form of
  `extraction`'s. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 01, and its header;
  - a notes line on the board, with this note marked "used for 01".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Put the push to the user, and do none of it unasked.** CI has not run on anything since
  `7ba95fc`. *Recommended:* push 01's commit (`git push origin <01's SHA>:main`) so that CI runs on
  it, then the review's follow-up.
- **Report to the user:**
  - what landed, and the count, 121 → 121 + 2 + N, at each end;
  - the interface in a few lines: the location, the five commands and their exit codes;
  - the process rule, and clarifications 3–5 as the choices they are;
  - M1–M14 and (o1)–(o4);
  - anything opened;
  - the push, as a decision for them;
  - that 02 can now be written, against the tree 01 left; it is the first prompt to start Ray, and
    takes the shared lock at the old location (README §5 rule 9).
