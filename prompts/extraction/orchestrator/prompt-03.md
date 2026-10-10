# Orchestrator — prompt 03, supported versions and CI

Read [`../README.md`](../README.md) first: §0.2 (the runtime versions), §1, §2 (rows 03–05), §4,
§5 (rules 6–10) and §6.2 (U7). Then read [`prompt-01.md`](prompt-01.md) §0's last list,
"Conventions", which this note keeps unless it says otherwise, and the board's *Orchestrator
review of prompt 02*.

**You do not write code.** You may:
- run the suite, the equivalence check and the commands the log records;
- make venvs, exports and wheels of your own in the session scratchpad, and replay the log's
  breakage there, never in the repository tree;
- read the workflow file and parse it; read GitHub's state with `gh api`, never write it;
- fix small residue in a follow-up commit of your own (§4).

You do not push, tag, or run the workflow on GitHub. Each of those is put to the user (§4).

**The prompt:** [`03-supported-versions-and-ci.md`](../03-supported-versions-and-ci.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** none expected ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- 02 landed (`b9f6dec`) and its review is recorded (`307ed96`). 03 is written (`c73fc91`), and U7
  is taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the first prompt whose work is meant to leave this machine, and it must not.** 01 and 02
changed what the package is; 03 changes what it *claims*: a supported range, a distribution, a
README a client will follow, and a workflow GitHub will run. Every claim has to have been tested
here before it is committed, because the next step (push, CI, tag) is outward-facing and a tag is
never moved (README §5 rule 10). The review has four halves:
- **the range is what was tested**: the suite passed in fresh venvs at both ends, and the declared
  `pyproject.toml` admits both pins in one resolve and refuses outside them;
- **the distribution is right**: the wheel carries the four modules and no test package, and was
  built from a fresh export, never from a tree with a `build/` (hazard 2);
- **the README is true of the package**: every name, argument and default it gives was checked
  against the package, not against the prompt;
- **nothing left the machine**: no push, no tag, no change to GitHub's settings, and no file under
  `raypoolkit/` touched, so `compare_with_source.py` gives 02's result.

**What moves on purpose:** `pyproject.toml` (three lines: the version, the Ray floor, the
exclusion); `.github/workflows/tests.yml` (new); `README.md` (rewritten); the log, the board and
`prompts/INDEX.md`; `docs/OPEN_ISSUES.md` only if something is opened. Nothing under `raypoolkit/`
or `docs/extraction/`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-10 at `c73fc91`
(package files as at `49f3ddf`, suite as at `b9f6dec`). Pass them on. Each is an IMPLEMENTATION
CHOICE at the orchestrator's direction unless it says otherwise, and the log says so.

1. **An editable install from the repository root rewrites `raypoolkit.egg-info/` there.** It is
   gitignored (`*.egg-info/`), and the planner's own measurement left it at 12:50, saying
   `0.1.0.dev0`. So the prompt's "with nothing in the repository written" is true of tracked
   files, and the agent's installs will rewrite it again. That is allowed: it is not a build in
   the tree in hazard 2's sense, it is never staged, and `git status` stays clean. A *wheel* is
   never built in the tree; `uv build` and `pip wheel` run only in exports.
2. **`pip freeze` does not show the version of an editable install.** In `venv/` it prints
   `-e git+https://github.com/ds283/RayPoolKit.git@<HEAD>#egg=raypoolkit`, with the `HEAD` at the
   time of install and no version. So §2.3's "its metadata says `0.1.0`" is checked with
   `importlib.metadata.version("raypoolkit")` and `requires("raypoolkit")` in `venv/`, before and
   after the reinstall (`0.1.0.dev0`, `['ray']` → `0.1.0`, `['ray>=2.43']`). Record those and the
   two `pip freeze` outputs as printed. `venv/`'s pip is 26.2.1; the reinstall builds in isolation
   and fetches `setuptools` from PyPI, as 01's did.
3. **`uv`'s cache is allowed.** `uv` keeps its cache at `~/.cache/uv` (2.7 GB now), outside the
   scratchpad. It already holds every wheel §2.3 needs: the orchestrator's installs at both ends
   resolved in about 5 s. The venvs, exports and wheels are in the scratchpad; the cache is `uv`'s
   own and is what the planner used. Do not pass `--no-cache` and do not clean it.
4. **The matrix: quote every version, and name the ends with a key.** Recommended form:
   `strategy.matrix.include` with two entries, each `{end: low|high, python: "<x.y.z>", ray:
   "<x.y.z>"}`, every version a quoted string so that YAML cannot read one as a float; the job's
   `name: suite (${{ matrix.end }})`; step 6 under `if: matrix.end == 'low'`. The PyYAML check
   compares the loaded strings with §2.3's table. Another key name is fine if the log says so.
5. **The actions are referenced by major tag, `@v7`, as the prompt says.** Both tags exist
   (`actions/checkout` `v7` → `3d3c42e`, latest `v7.0.1`; `actions/setup-python` `v7` →
   `5fda3b9`, latest `v7.0.0`). The repository requires no SHA pinning
   (`sha_pinning_required: false`). Do not pin to a SHA.
6. **The README's constructor facts**, from `inspect.signature(RayWorkPool)` at `c73fc91`:
   18 parameters, no `self`. `pool: DatastorePool`, `task_list`, `task_builder`; `compute_handler`,
   `store_handler` and `persist_handler` default to the module functions `_default_compute_handler`
   (`obj.compute(**kwargs)`), `_default_store_handler` (`obj.store()`) and
   `_default_persist_handler` (`pool.object_store(obj)`), at `RayWorkPool.py:60-69`;
   `available_handler`, `validation_handler`, `post_handler` and `label_builder` default to `None`;
   `create_batch_size=5`, `process_batch_size=1`, `max_task_queue=200`, `notify_batch_size=500`,
   `notify_time_interval=300`, `notify_min_time_interval=60`, `title=None`, `store_results=False`.
   - The README gives the three handler defaults **by what they do**, not by their private names,
     and gives the sizes as values, not as the private `DEFAULT_*` constants. The log records, for
     each, the signature's default and the body it was read from.
   - Only the store and persist handlers are given the pool (`:431`, `:441`). The compute handler
     is given `(obj, **compute_args)` (`:384`); the available, validation and post handlers the
     object alone (`:348`, `:475`, the five post-handler calls). Read each from the module.
7. **The README's printed-line examples are copied from one pinned whole-run test**, and the log
   names it (`test_printed_lines.TestProgressAndCompletion.test_a_compute_run_with_validation_notifying_on_every_pass`
   is one; any whole-run test will do). The README says the stamps, counts and rates in them are
   illustrative. Do not compose a line by hand.
8. **The breakage diffs to `pyproject.toml` are written against 03's own `pyproject.toml`**, the
   one committed, so that `git apply` replays them from a clean tree at 03's commit. Apply (c)–(f)
   **inside exports**, with `git apply` run there (it works outside a repository), so that the
   diff that ran is the diff logged, and the repository's `pyproject.toml` is touched only by
   §2.1's edit. (b) and (c) are `uv pip install --dry-run` into a throwaway venv, as the planner
   measured them.

**The facts, checked by the orchestrator.** Pass them on. Measured from the orchestrator's own
scratchpad with fresh exports and venvs; nothing in the repository was written, not even
`raypoolkit.egg-info/` (every editable install was made from an export).

- **The baseline at `c73fc91`.** `venv/`: Python 3.12.15, `ray==2.43.0`, `black==25.1.0`,
  `raypoolkit` editable; `Ran 116 tests … OK`. `compare_with_source.py` exits 0 (572 identical,
  2 D-imp, 1 D-pool, 4 D-int, 12 declared files, 0 undeclared). `black --check raypoolkit docs`:
  15 files unchanged.
- **The toolchain.** `uv` 0.12.20 at `/opt/local/bin/uv`; `/opt/local/bin/python3.12` is 3.12.15
  and `/opt/local/bin/python3.13` is 3.13.16. (`/opt/local/bin/python3.14` exists too; hazard 4
  says it is not tested, and it is not used.)
- **The prompt's §2.2 holds**, with §2.1's and §2.4's `pyproject.toml` applied to an export:
  - **the wheel**, by `uv build --wheel` from a fresh `git archive HEAD` export:
    `raypoolkit-0.1.0-py3-none-any.whl`, 12,016 bytes, 9 entries (the four modules,
    `dist-info/licenses/LICENSE`, `METADATA`, `WHEEL`, `top_level.txt`, `RECORD`);
  - installed into a fresh 3.13.16 / Ray 2.55.1 venv and run from an empty directory with `-I`:
    every import of §2.4 succeeds, `raypoolkit.__file__` is in the venv's `site-packages`,
    `ray.is_initialized()` is `False`, `version` is `0.1.0`, `requires` is `['ray>=2.43']`, and
    `import raypoolkit.tests` raises `ModuleNotFoundError`;
  - **the suite**, the package installed editable with the exclusion, in one resolve with its pins:
    `Ran 116 tests … OK` at 3.12.15 / 2.43.0 and at 3.13.16 / 2.55.1. No Ray process before or
    after;
  - **the refusals**: `ray==2.42.1` ("raypoolkit==0.1.0 depends on ray>=2.43 … unsatisfiable"), and
    `requires-python = ">=3.13"` at the low end ("the current Python version (3.12.15) does not
    satisfy Python>=3.13");
  - **(d)**: `exclude` gaining `"raypoolkit"` gives a wheel of 5 entries, all under `dist-info/`;
  - **(f), hazard 2**: with no exclusion, then the exclusion restored in the same export, both
    wheels have 19 entries, 10 of them under `raypoolkit/tests/`;
  - **PyYAML** 6.0.3 is in the scratch venvs.
- **GitHub, read only.** `ds283/RayPoolKit` is public, default branch `main`, unprotected; Actions
  enabled, all actions allowed, no SHA pinning; 0 workflows and 0 runs; no tag. `origin/main` is
  `97f9ff0`, 8 commits behind local `main` before this note.
- **SGK.** `HEAD` is still `b510bc9`, `RayTools/RayWorkPool.py` blob `b4666fa`. 03 does not read
  it except through `compare_with_source.py`.
- **Expected counts.** The suite is **116** before and **116** after, by module 3, 30, 12, 20, 22,
  7, 17, 5 (log 02 §3.1). The check gives the counts above before and after. The index is **7**
  now, and 7 after unless the work finds something.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) Scope.** Only §6's files changed; nothing under `raypoolkit/` or `docs/extraction/`; no
  tag; nothing pushed.
- **(E2) The range.** `pyproject.toml` is §2.1 and §2.4 and nothing else; the suite passes in
  fresh venvs at both ends, installed from the repository at 03's commit, and in `venv/`.
- **(E3) The distribution.** A wheel built from a fresh export of 03's commit, with no file copied
  in, has the log's file list and passes §2.4's release check.
- **(E4) The workflow.** §2.5's file, parsing, its matrix equal to §2.3, its steps replayed as the
  log records.
- **(E5) The breakage.** (a)–(f) each fail as logged.
- **(E6) The README.** Every name, argument and default true of the package; the statements §2.6
  asks for, and no fault list.
- **(E7) The records.** The log with the prompt's §4.5 additions; the board with the "ready to be
  tagged" line; `prompts/INDEX.md`; the index.

**Conventions.** Prompt 01's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run every suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff with `git apply --check` (and `-R --check` once applied), replay it in
  `bash`, and check that `git status` is clean after it;
- use the scratchpad subdirectory you are given, never `/tmp`, and put no scratch file under the
  repository, least of all under `raypoolkit/`;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

Three additions:
- **Nothing outward-facing.** No `git push`, no `git tag`, no `gh` command that writes (no
  `gh workflow run`, no `gh api -X POST/PUT/PATCH/DELETE`, no release). Reading with `gh api` is
  allowed but not needed.
- **One export per build**, made fresh with `git archive HEAD | tar -x -C <new empty dir>`; never
  reuse an export for a second build except in (f), where the reuse is the point.
- **The venvs you verify with are not the venvs you break.** (a) and every other breakage run in
  throwaway venvs; the low, high and wheel venvs are made once and left as they were verified.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone.
2. **The baseline.** The suite gives `Ran 116 tests … OK`, and `compare_with_source.py` exits 0
   with the counts above. `git tag` is empty, and `git ls-remote origin` shows `main` at `97f9ff0`
   and no tag.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
4. **The index.** 7 now; 7 after unless the work finds something. Tell the agent both.
5. **Scratch.** Make the agent's subdirectory of the session scratchpad, empty, and tell it the
   path. Keep your own measurements in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, and logs 01 and
  02 (the sections the prompt names);
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's eight clarifications and additions. Clarifications 1
and 8 are the ones that matter: the first so that a rewritten `raypoolkit.egg-info/` is not taken
for a stop, the second so that the breakage diffs replay from 03's commit.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/03-supported-versions-and-ci.md`, in README §5.1's
  form, with the prompt's §4.5 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else.** In particular it
  must not touch any file under `raypoolkit/` or `docs/extraction/`, nor `PROVENANCE.md`,
  `CLAUDE.md`, `LICENSE`, `.gitignore`, `.idea/`, the campaign README, or anything under
  `orchestrator/`.
- **It pushes nothing and tags nothing**, and writes nothing to GitHub.
- **It builds no wheel in the repository tree.**
- **It edits no client repository and not DatastoreKit, and runs none of their code.**
- **It starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **E1, scope.** `git show --stat <commit>` touches only `pyproject.toml`,
   `.github/workflows/tests.yml`, `README.md`, the log, the board, `prompts/INDEX.md` and, if
   needed, the index. `git diff c73fc91 <commit> -- raypoolkit docs/extraction PROVENANCE.md
   CLAUDE.md LICENSE .gitignore prompts/extraction/README.md` is empty. `git tag` is empty, and
   `git ls-remote origin` still shows `main` at `97f9ff0` and no tag. No `build/` or `dist/` in the
   repository root; `raypoolkit.egg-info/` may have been rewritten (clarification 1).
2. **E2, `pyproject.toml`, by reading.** `git diff c73fc91 <commit> -- pyproject.toml` is three
   changes: `version = "0.1.0"`, `"ray>=2.43"`, and the `exclude` line. Nothing else.
3. **E2, the suite, by running.** In a fresh shell: `venv/` gives `Ran 116 tests … OK`, and
   `importlib.metadata` there gives `0.1.0` and `['ray>=2.43']`. Then make **your own** two fresh
   venvs at §2.3's pins, install the repository editable in one resolve with them, and run the
   suite from the root: 116, OK, at each, with the versions printed. No Ray process before or
   after.
4. **E3, the distribution, re-built.** `git archive <commit>` into a new export, with **no file
   copied in**, and `uv build --wheel` there. Its entry list must equal the log's. Its SHA-256
   need not: the export's file times are the commit's, so compare the unzipped contents with the
   log's account instead (the four modules byte for byte against the commit's). Install it into a
   fresh venv at the high end's pins and run §2.4's checks from an empty directory with `-I`.
   This is the build the tag will stand on; the agent's was made before the commit existed.
5. **E4, the workflow, by reading and parsing.** The comment at the top says both things §2.5
   asks. Triggers: `push` to `main`, `pull_request`, `workflow_dispatch`. One job, on
   `ubuntu-24.04`, `fail-fast: false`, a matrix of exactly two entries with quoted versions equal
   to §2.3. The six steps, in order, `@v7` for both actions; `black` on the low end only;
   `permissions: contents: read`; no secret, cache, artefact or other action; nothing that runs
   `compare_with_source.py`. `yaml.safe_load` parses it, and the matrix's values are strings.
6. **E4, the replay.** The log's commands stand for steps 3–6 one for one, at both ends, and it
   names the steps with no local counterpart (1, 2, and the pip upgrade).
7. **E5, the breakage, by replaying.** In throwaway venvs and fresh exports of 03's commit: (a)
   fails the guard's tests 2 and 3 and only those; (b) and (c) refuse, naming the floor; (d)
   gives a wheel with no module, and `import raypoolkit` fails from it; (e) ships the tests and
   `import raypoolkit.tests` succeeds; (f)'s second wheel still lists `raypoolkit/tests/`. Each
   diff applies with `git apply --check` as recorded. Then one of the orchestrator's own, not in
   the log: `dependencies = ["ray>=2.56"]` in an export, installed `--dry-run` at the high end's
   pins; the resolver must refuse `ray==2.55.1`. The repository's `git status` is clean
   throughout.
8. **E6, the README, by reading and checking.** Extract every code span in `README.md` that
   names a Python name, argument or value. Each importable name imports from `venv/`; each
   argument is in `inspect.signature(RayWorkPool)`; each default equals the signature's (the three
   handler defaults described by what their bodies do). The README says, plainly, that as of
   `v0.1.0` a pool with no compute handler passes `persist_handler=None`; gives the pinned install
   line `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.1.0` and the editable-install
   warning; states the declared range, the two tested ends, Ray's effective 2.45.0 floor on 3.13,
   and that newer releases are allowed and untested; gives the printed-line examples, each line
   found verbatim in the test the log names; points at `raypoolkit/tests/standins.py` as not
   installed; and lists no fault. Every relative link resolves to a file in the commit.
9. **E2 and E1, the check and the formatter.** `./venv/bin/python
   docs/extraction/compare_with_source.py` exits 0 with the counts above; `./venv/bin/black
   --check raypoolkit docs` (25.1.0) is clean.
10. **E7, the records.** The log has every section of README §5.1 and each of the prompt's §4.5
    additions: every venv's versions and verdict; every install command and its workflow step; the
    release check with name, size, entry count, SHA-256, file list and outputs; the README's names
    and how each was checked; the five hazards; the check's whole output; (a)–(f); 116 → 116; §0's
    clarifications recorded as deviations. Board: the header, 03's row (landed, "this commit",
    116 → 116), and the line saying `v0.1.0` is ready to be tagged once CI passes on 03's commit,
    with no tag made. Index: count it, and check the header matches. `prompts/INDEX.md`: the
    campaign's line.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 03* paragraph, in the form of
  02's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 03, and its header;
  - the notes line, with this note added and marked "used for 03".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Put the release sequence to the user, and do none of it unasked.** It is outward-facing, and
  the tag cannot be moved once made.
  1. **Push.** A push of `main` runs the workflow on the pushed head only, which would be the
     review's follow-up commit, not 03's. That commit's tree differs from 03's only under
     `prompts/`, but the prompt asks for CI "on 03's commit". *Recommended:* push 03's commit
     alone first (`git push origin <03's SHA>:main`), so the first run is on it; push the rest
     once it is green. The alternative (push `main`, and accept a run on a tree identical outside
     `prompts/`) is the user's to choose.
  2. **CI.** Both ends green on 03's commit, read with `gh run list` / `gh run view`. If either is
     red, no tag: the failure goes on the board's §3, and a fix prompt is written before anything
     else (Linux is the one place the suite has not run, hazard 3).
  3. **The tag.** `v0.1.0`, annotated, on 03's commit, and pushed. `CLAUDE.md` says a tag is made
     by a prompt that says so or by the user; 03 says the tag is not its work, so it is made by
     the user, or on the user's explicit instruction in that turn.
- **Report to the user:**
  - what landed, and the count, 116 → 116, at each end;
  - the declared range and the two tested ends, with Ray's effective 3.13 floor;
  - the wheel: its name, entries, and that the orchestrator's rebuild from the commit matches;
  - the workflow, and that it has not yet run;
  - (a)–(f) and the orchestrator's own breakage;
  - anything opened;
  - the release sequence above, as a decision for them;
  - that 04 can be written once `v0.1.0` exists, with U8 to put to the user.
