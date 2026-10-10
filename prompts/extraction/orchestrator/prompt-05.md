# Orchestrator — prompt 05, release `v0.2.0`

Read [`../README.md`](../README.md) first: §0.1, §1, §2 (rows 04–06), §4, §5 (rules 6, 7, 10)
and §6.2 (U8). Then read [`prompt-01.md`](prompt-01.md) §0's last list, "Conventions", which this
note keeps unless it says otherwise; [`prompt-03.md`](prompt-03.md) §4, the release sequence
`v0.1.0` followed; and the board's *Release of `v0.1.0`*, *Orchestrator review of prompt 04* and
*CI on 04's commit*.

**You do not write code.** You may:
- run the suite and the commands the log records;
- make venvs, exports and wheels of your own in the session scratchpad, and replay the log's
  breakage there, never in the repository tree;
- make a `git worktree` of `v0.1.0` in the scratchpad to run the retired check, and remove it
  after;
- read GitHub's state with `gh api` / `gh run`, never write it;
- fix small residue in a follow-up commit of your own (§4).

You do not push or tag. Each is put to the user (§4).

**The prompt:** [`05-release-v0.2.0.md`](../05-release-v0.2.0.md)
**Closes:** `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` · **Narrows:** nothing ·
**Opens:** none expected · **Model:** Opus, as the prompt recommends.

**Gate:**
- 04 landed (`0b6ffd2`), its review is recorded (`914070c`), and CI passed at both ends on
  `0b6ffd2` (run `38071307103`) and on `914070c` (run `38071490036`). 05 is written (`f839209`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**Its work is prose and one setting, and the tag that follows it is what the clients pin.** 03
released SGK's pool; 04 changed it; 05 changes no behaviour and touches no file under
`raypoolkit/`, but it writes what a client reads when it moves its pin, and the release check is
the last time the wheel is looked at before a tag that is never moved (README §5 rule 10). The
review has four halves:
- **the distribution is right, however stale the build directory**: a wheel from a fresh export
  of 05's commit has 9 entries, and so does one with the repository's stale
  `raypoolkit.egg-info/` copied in, with no "absent from" warning;
- **the README is true of `v0.2.0`, and its history true of `v0.1.0`**: every name, argument,
  default and exception checked against the module, and every "was" in "Changes in `v0.2.0`"
  checked against `v0.1.0`'s module;
- **`PROVENANCE.md` stays a record of the import**: three statements made "of `v0.1.0`", one
  section added, and the retired check's commands shown to work;
- **nothing changed under `raypoolkit/` and nothing left the machine**: the suite is 121 before
  and after, no printed line moved, no tag, no push.

**What moves on purpose:** `pyproject.toml` (two changes), `README.md`, `PROVENANCE.md`; the log,
the board, `prompts/INDEX.md` and `docs/OPEN_ISSUES.md`. Nothing under `raypoolkit/`, `docs/` other
than the index, or `.github/`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-10 at `f839209` (the
package and suite as at `0b6ffd2`). Pass them on. Each is an IMPLEMENTATION CHOICE at the
orchestrator's direction unless it says otherwise, and the log says so.

1. **The "now refused" bullet of §2.2 is wrong about `v0.1.0`, and the README must not repeat
   it.** The prompt says a store handler, persist handler, validation handler or label builder
   given with no compute handler "was silently ignored", and lists "a compute handler with
   `store_handler=None` or `persist_handler=None`" as newly refused. Read from `git show
   v0.1.0:raypoolkit/RayWorkPool.py`, lines 94–102:
   - **a persist handler with no compute handler was already refused**, with `RuntimeWarning`
     raised as an exception, the default persist handler included (which is why every
     lookup-only pool passed `persist_handler=None`);
   - **a compute handler with `persist_handler=None` was already refused**, with `RuntimeError`;
   - **a compute handler with `store_handler=None` was not refused, nor ignored**: it constructed,
     and `run()` raised `TypeError` at the first completed compute (fault 4,
     `[00-the-constructor-checks-its-handlers-unevenly]`);
   - a store handler, validation handler or label builder with no compute handler was silently
     ignored; and each size below 1 made `run()` loop for ever (`create_batch_size`,
     `max_task_queue`) or raise from `ray.wait` (`process_batch_size`, with work in flight), as
     the prompt says (board §4, `[02-the-constructor-does-not-check-its-sizes]`).

   So the README says, in substance: **newly refused** at construction, with `ValueError`: a
   store handler, validation handler or label builder given with no compute handler (`v0.1.0`
   ignored it); a compute handler with `store_handler=None` (`v0.1.0` failed in `run()`); a size
   below 1. **Already refused, now with `ValueError`**: an explicit persist handler with no compute
   handler (`RuntimeWarning`), and a compute handler with `persist_handler=None` (`RuntimeError`);
   the first bullet, on the exception types, may carry these. The wording is the agent's. Record
   it as a deviation, **STRUCTURALLY REQUIRED**: the prompt's §5 makes a statement untrue of the
   module a stop, and this is the correction, not a stop.
2. **`uv build -q` hides the warning the release check searches for.** With `-q` the build log is
   empty, so "searched for 'absent from'" finds nothing whatever happens. Measured: breakage (a)
   built with `-q` gives a 0-byte log; without it, the log holds
   `_Warning: Package 'raypoolkit.tests' is absent from the \`packages\` configuration` and a
   second line containing "absent from", so `grep -c "absent from"` gives **2**. Build every wheel
   **without** `-q`, capture stdout and stderr to a file, and record the count: 0 for (R1) and
   (R2), 2 for (a). Every build also prints the two "byte-compiling is disabled, skipping" lines.
3. **(R2) stays the issue's test after the agent's own installs.** The repository's
   `raypoolkit.egg-info/` was rewritten at 18:14 by 04's review; its `PKG-INFO` says `0.1.0` and
   its `SOURCES.txt` still lists the ten files under `raypoolkit/tests/`. An editable install with
   05's `pyproject.toml` rewrites it, but setuptools merges the old `SOURCES.txt`: measured in an
   export with the stale copy and 05's `pyproject.toml`, after `uv pip install -e`, `PKG-INFO`
   says `0.2.0` and `SOURCES.txt` still lists the ten. So §3.1's and §3.2's installs, which run
   from the repository root, do not defeat (R2). Before each build that copies it in, record the
   copy's `Version:` line and `grep -c tests/ SOURCES.txt` (10) in the log.
4. **"Verbatim in `test_printed_lines.py`" means the lines the test expects, rendered.** The
   README's examples were copied by 03 from
   `test_printed_lines.TestProgressAndCompletion.test_a_lookup_only_run_notifying_on_every_pass`
   (log 03 §4.2). That test builds its progress lines with `progress(...)` and the `SUFFIX`
   constant, so `grep -F` of the README's progress line in the test module finds nothing (measured:
   0 hits). Check them as 03 did: run that test with `assertEqual` wrapped to record the list it
   compares, and confirm that each README line is one of its nine, leading spaces included. The
   other four example lines are literal in the module.
5. **`PROVENANCE.md`'s "Re-running the check": these commands work**, and the README's
   Developing paragraph may point at them. Measured at `f839209`, the worktree in the
   scratchpad:
   ```bash
   git worktree add --detach <scratch>/raypoolkit-v0.1.0 v0.1.0
   cd <scratch>/raypoolkit-v0.1.0
   /Users/ds283/Documents/Code/RayPoolKit/venv/bin/python docs/extraction/compare_with_source.py
   cd /Users/ds283/Documents/Code/RayPoolKit
   git worktree remove <scratch>/raypoolkit-v0.1.0
   ```
   The script finds the package from its own path (`REPO_ROOT = Path(__file__).resolve().parents[2]`),
   so it checks the worktree's `v0.1.0` tree: `RESULT: OK`, exit 0, with 572 identical, 2 D-imp,
   1 D-pool, 4 D-int, 12 declared files, 0 undeclared. From the repository root on `HEAD` it gives
   `RESULT: FAIL`, exit 1, by design. It reads SGK through `git -C … show b510bc9:<path>`, which is
   reading, not running, SGK (README §5 rule 5). `PROVENANCE.md` writes the scratch directory as a
   placeholder outside the repository, not as this session's path. If the agent runs the commands
   to check them (recommended), it removes the worktree, and `git worktree list` shows this
   checkout alone after.
6. **`PROVENANCE.md`'s "New here, with no source" lists only 01's new files** (`__init__.py`,
   `contract.py`, the guard and `tests/__init__.py`), though `v0.1.0` declared 12 (02 added the
   suite). It is a record of the import made by 01, and the prompt says nothing else in the file
   changes. Leave it. The agent may record it under "Observations not acted on"; it is not an
   issue.
7. **The breakage is applied inside exports, against 05's own `pyproject.toml`.** Each export is
   `git archive HEAD` with the working tree's `pyproject.toml` copied over the export's, then the
   diff applied with `git apply` run in the export (it works outside a repository), so that each
   diff replays from a fresh export of 05's commit. The repository's `pyproject.toml` is touched
   only by §2.1's edit. (b) needs no manifest; (a) does.
8. **Another session's Ray is up, and is not this repository's.** At writing, `pgrep -lf
   'gcs_server|raylet|ray::'` shows a cluster started from DatastoreKit's session scratchpad
   (`…-Users-ds283-Documents-Code-DatastoreKit/…/agent11/work/break-b/venv`, Python 3.13). Record
   what is up before and after each suite run, attribute each process by its path, and leave it
   alone. A process whose path is in this repository or in this session's scratchpad is a stop.

**The facts, checked by the orchestrator.** Pass them on. Measured from the orchestrator's own
scratchpad with fresh exports and venvs.

- **The baseline at `f839209`.** `venv/`: Python 3.12.15, `ray==2.43.0`, `black==25.1.0`,
  `raypoolkit` editable, pip 26.2.1; `importlib.metadata` gives `0.1.0` and `['ray>=2.43']`.
  `Ran 121 tests … OK`, by module `test_construction` 15, `test_inherited_faults` 6,
  `test_package_imports` 3, `test_printed_lines` 18, `test_run_paths` 22, `test_scheduling` 7,
  `test_standins` 30, `test_task_builder` 20. `black --check raypoolkit docs`: 15 files unchanged.
  No `build/` or `dist/` in the repository root. `pyproject.toml` has no `readme` key, so the
  README does not reach the wheel and an export's stale README does not change it.
- **The toolchain.** `uv` 0.12.20; `/opt/local/bin/python3.12` 3.12.15, `/opt/local/bin/python3.13`
  3.13.16. PyPI's newest `ray` is still **2.59.0**, so the README's "Ray up to 2.59.0 today" holds.
  `stat` on this machine's `PATH` is GNU's: use `wc -c <` for a size.
- **The prompt's §2.1 table holds**, rebuilt by the orchestrator, each from a fresh `git archive
  HEAD` export with `pyproject.toml` edited there:

  | Build | Entries | Under `raypoolkit/tests/` | Bytes | "absent from" lines |
  |---|---|---|---|---|
  | (R1) `0.2.0` with the table, no manifest | 9 | 0 | 13,565 | 0 |
  | (R2) `0.2.0` with the table, stale manifest | 9 | 0 | 13,565 | 0 |
  | (a) `0.2.0` without the table, stale manifest | 19 | 10 | 42,737 | 2 |
  | (b) the table kept, `exclude` removed, no manifest | 19 | 10 | 42,737 | — |

  The 9 entries are `raypoolkit/RayWorkPool.py`, `__init__.py`, `_timing.py`, `contract.py`, and
  `raypoolkit-0.2.0.dist-info/` `licenses/LICENSE`, `METADATA`, `WHEEL`, `top_level.txt`,
  `RECORD`.
- **The README's line references hold** at `f839209`: Status `:10-21` (with DatastoreKit's
  paragraph `:23-25`), Installing `:45-49`, the work `:72-73`, the sizes `:99-104`, the
  `persist_handler=None` section `:147-153`, the printed lines `:155-183`, Developing `:193-211`
  (the check's paragraph `:209-211`), Licence `:213-215`. `PROVENANCE.md`: "The differences
  allowed" `:38-57` (the sentence `:40-42`, the closing sentence `:57`), "Re-running the check"
  `:59-72`, "The freeze" `:74-81`.
- **The module, for the README's checks section** (`raypoolkit/RayWorkPool.py:109-142`): with no
  compute handler, a store or persist handler that *is* the module's default (by identity) becomes
  `None`, then any of `store_handler`, `persist_handler`, `validation_handler`, `label_builder` not
  `None` raises `ValueError("No compute handler was supplied, so <name> would never be called;
  leave it out, or pass None")`, the first in that order named; with one, `store_handler` or
  `persist_handler` `None` raises `ValueError("A compute handler was supplied, so <name> must not
  be None; leave it out to use the default")`; each of the three sizes below 1 raises
  `ValueError("<name> must be at least 1, not <value!r>")`. The other raises are unchanged from
  `v0.1.0`: `RuntimeError` at `:325`, `:331`, `:342` (the task builder's outcomes), `:499` (a
  persisted object not available) and `:559`. Log 04 §5 observation 4: a size that does not
  compare with 1 raises `TypeError`; the README need not say so.
- **Expected counts.** The suite is **121** before and **121** after, by module as above. The
  index is **1** now and **0** after; the board's §3 holds no issue after.
- **GitHub, read only.** `origin/main` is `914070c`; local `main` is ahead by `f839209` and this
  note. The tag `v0.1.0` (object `0a9cdb2`) is on `4e90a8a`, and is the only tag, locally and on
  `origin`.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §6 files changed; nothing under `raypoolkit/` or
  `docs/extraction/`; no tag; nothing pushed.
- **(E2) `pyproject.toml`.** Two changes, and nothing else.
- **(E3) The suite.** 121, OK, at both ends and in `venv/`, which reports `0.2.0`.
- **(E4) The distribution.** A wheel from a fresh export of 05's commit has 9 entries with and
  without the stale manifest, and passes 03 §2.4's release check at `0.2.0`.
- **(E5) The breakage.** (a)–(c) each fail as logged.
- **(E6) The documents.** The README true of `v0.2.0` and its "Changes" true of `v0.1.0`
  (clarification 1); `PROVENANCE.md` as §2.3, its commands working.
- **(E7) The records.** The log with §4.4's additions; the board with the "ready to be tagged"
  line and the issue in §4; the index at 0; `prompts/INDEX.md`.

**Conventions.** Prompt 01's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run every suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff with `git apply --check` (and `-R --check` once applied), replay it in
  `bash`, in an export (clarification 7);
- use the scratchpad subdirectory you are given, never `/tmp`, and put no scratch file under the
  repository, least of all under `raypoolkit/` (the suite collects it);
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

Three additions:
- **Nothing outward-facing.** No `git push`, no `git tag`, no `gh` command that writes (no
  `gh workflow run`, no `gh api -X POST/PUT/PATCH/DELETE`, no release).
- **One export per build**, made fresh with `git archive HEAD | tar -x -C <new empty dir>`; a wheel
  is never built in the repository tree.
- **The venvs you verify with are not the venvs you break.** The low, high and wheel venvs are
  made once and left as they were verified; (b)'s import check runs in a throwaway venv.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. `git diff 0b6ffd2 --
   raypoolkit pyproject.toml README.md PROVENANCE.md` is empty.
2. **The baseline.** The suite gives `Ran 121 tests … OK`. `git tag` is `v0.1.0` alone;
   `git ls-remote origin` shows `main` at `914070c` and the tag on `4e90a8a`. The repository has
   `raypoolkit.egg-info/`, and its `SOURCES.txt` lists ten files under `raypoolkit/tests/` (if not,
   (R2) cannot be made: the prompt's §5 makes it a stop, so put it to the user before dispatch).
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`, attributed (clarification 8).
4. **The index.** 1 now; 0 after. Tell the agent both.
5. **Scratch.** Make the agent's subdirectory of the session scratchpad, empty, and tell it the
   path. Keep your own measurements in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, and logs 03 and
  04 (the sections the prompt names);
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's eight clarifications and additions. Clarifications 1
and 2 are the ones that matter: the first so that the README does not tell a client that
`v0.1.0` ignored what it refused, the second so that the release check's warning search can fail.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/05-release-v0.2.0.md`, in README §5.1's form, with
  the prompt's §4.4 additions.
- **The files it may change are the prompt's §6 list, and nothing else.** In particular it must
  not touch any file under `raypoolkit/` or `docs/extraction/`, nor `.github/`, `CLAUDE.md`,
  `LICENSE`, `.gitignore`, `.idea/`, the campaign README, or anything under `orchestrator/`; and
  it must not delete, clean or hand-edit the repository's `raypoolkit.egg-info/`.
- **It pushes nothing and tags nothing**, and writes nothing to GitHub.
- **It builds no wheel in the repository tree.**
- **It edits no client repository and not DatastoreKit, and runs none of their code**; the
  retired check's read of SGK through `git show` is allowed.
- **It starts no Ray**, and leaves another session's alone.
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **E1, scope.** `git show --stat <commit>` touches only `pyproject.toml`, `README.md`,
   `PROVENANCE.md`, the log, the board, `prompts/INDEX.md` and `docs/OPEN_ISSUES.md`.
   `git diff f839209 <commit> -- raypoolkit docs/extraction .github CLAUDE.md LICENSE .gitignore
   prompts/extraction/README.md` is empty. `git tag` is `v0.1.0` alone, and `git ls-remote origin`
   is unchanged. No `build/` or `dist/` in the repository root; `git worktree list` is this
   checkout alone; `raypoolkit.egg-info/` may have been rewritten (clarification 3).
2. **E2, `pyproject.toml`, by reading.** `git diff f839209 <commit> -- pyproject.toml` is
   `version = "0.2.0"` and the `[tool.setuptools]` table with `include-package-data = false`,
   placed before `[tool.setuptools.packages.find]`; the `exclude` is kept. Nothing else.
3. **E3, the suite, by running.** In a fresh shell: `venv/` gives `Ran 121 tests … OK`, by module
   as §0 expects, and `importlib.metadata` there gives `0.2.0` and `['ray>=2.43']`. Then **your
   own** fresh high-end venv (3.13.16 / 2.55.1, the repository editable in one resolve): 121, OK.
   Ray before and after attributed as in clarification 8; none is this repository's.
4. **E4, the distribution, re-built.** Two fresh exports of 05's commit with `git archive
   <commit>`: (R1') with no file copied in; (R2') with the repository's `raypoolkit.egg-info/`
   copied in, its `SOURCES.txt` listing the ten test files (record it). `uv build --wheel`
   without `-q` in each, its log captured. Each: 9 entries, the list above, none under
   `raypoolkit/tests/`; `grep -c "absent from"` 0. The four modules in each wheel are byte-equal to
   the commit's (`git show <commit>:<path>`); the SHA-256 need not equal the log's (the export's
   file times are the commit's). Install (R2') into a fresh venv at the high end's pins and from an
   empty directory with `-I`: the two public names import from `site-packages`, `version` is
   `0.2.0`, `requires` is `['ray>=2.43']`, `ray.is_initialized()` is false, and `import
   raypoolkit.tests` raises `ModuleNotFoundError`. This is the build the tag will stand on.
5. **E5, the breakage, by replaying.** Extract (a)–(c) from the log's text and replay each in a
   fresh export of 05's commit, with `git apply` run there, each first checked with
   `git apply --check` as recorded: (a) with the stale manifest gives 19 entries, 10 under
   `raypoolkit/tests/`, and 2 "absent from" lines; (b) gives 19 entries, and in a throwaway venv
   `import raypoolkit.tests` succeeds from its wheel; (c)'s wheel reports `0.1.0`, so the release
   check's version check fails. The repository's `git status` is clean throughout. Then one of the
   orchestrator's own, not in the log:
   - (o1) `include-package-data = true`, the table kept, with the stale manifest: it must fail as
     (a) does (measured at `f839209`: 19 entries, 10 tests, 2 "absent from" lines), so that the
     setting's value, not the table's presence, is what closes the issue.
6. **E6, the README, by reading and checking.** Extract every code span in `README.md` that names a
   Python name, argument, default, exception type or value. Each importable name imports from
   `venv/`; each argument is in `inspect.signature(RayWorkPool)`; each default equals the
   signature's (the three handler defaults described by what their bodies do). Then:
   - **"Changes in `v0.2.0`"**: each statement of what `v0.2.0` does is asserted by a test the log
     names, or a probe; and each statement of what `v0.1.0` did is true of `git show
     v0.1.0:raypoolkit/RayWorkPool.py` (clarification 1): in particular, it does not say an
     explicit persist handler with no compute handler, or `persist_handler=None` with one, was
     accepted in `v0.1.0`. It says the printed lines are unchanged, and names no client call site
     and no fault history;
   - **the checks section** replaces `:147-153`, is titled for what a caller does, gives each
     check's exception type and the gist of its message, and names no board issue;
   - Status describes `v0.2.0` and keeps `v0.1.0` in one sentence (SGK at `b510bc9`); the pin
     line is `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0`; "pass a sequence"
     is gone; the sizes are at least 1; Developing says the check is retired at `v0.1.0` and runs
     from a worktree of it; Licence names the header on the four modules;
   - the printed-line examples are unchanged, each one of the nine lines of the test 03 named,
     rendered (clarification 4);
   - every relative link in `README.md` and `PROVENANCE.md` resolves to a file in the commit.
7. **E6, `PROVENANCE.md`.** `git diff f839209 <commit> -- PROVENANCE.md`: ":40-42" and ":57" made
   statements of `v0.1.0`; "Re-running the check" rewritten for the worktree, saying it fails by
   design on a later tree; a "Since `v0.1.0`" section before "The freeze", of two or three
   sentences, linking 04's log, the board's §4 and the README's "Changes in `v0.2.0`"; the file
   map, the classes, "New here" and the freeze unchanged. Run its commands as written, the
   worktree in your scratchpad: `RESULT: OK`, exit 0, with the counts of clarification 5; remove
   the worktree after.
8. **No behaviour moved.** `git diff 0b6ffd2 <commit> -- raypoolkit` is empty, so no printed line
   moved (README §5 rule 7).
9. **`black`.** `./venv/bin/black --check raypoolkit docs` (25.1.0) is clean, 15 files.
10. **E7, the records.** The log has every section of README §5.1 and each of the prompt's §4.4
    additions: every venv's versions, install commands and verdict; `venv/`'s metadata before and
    after; (R1) and (R2) with name, size, entry count, SHA-256, file list, the manifest's state and
    the "absent from" count; every README name and how it was checked; (a)–(c); 121 → 121; §0's
    clarifications recorded as deviations, clarification 1 as STRUCTURALLY REQUIRED. Board: the
    header, with the line saying `v0.2.0` is ready to be tagged once CI passes on 05's commit and
    no tag made; 05's row (landed, "this commit", 121 → 121); §3 empty, and the issue in §4 with a
    dated **Resolved (05)** line naming the setting and (R2). Index: count it (0), and check the
    header matches. `prompts/INDEX.md`: the campaign's line.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 05* paragraph, in the form of
  04's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 05, and its header;
  - the notes line, with this note added and marked "used for 05".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
  An open issue is not by itself a bar to the tag; one that makes the README or the wheel untrue
  is, and goes to a fix prompt first.
- **Put the release sequence to the user, and do none of it unasked.** It is outward-facing, and
  `v0.2.0` is the tag the clients pin; it cannot be moved once made.
  1. **Push.** *Recommended:* push 05's commit alone first (`git push origin <05's SHA>:main`), so
     that CI runs on it; `f839209` and this note go with it, touching only `prompts/`. Then the
     review's follow-up.
  2. **CI.** Both ends green on 05's commit, read with `gh run list` / `gh run view`. If either is
     red, no tag: the failure goes on the board's §3, and a fix prompt is written first.
  3. **The tag.** `v0.2.0`, annotated, on 05's commit, and pushed. Made by the user, or on the
     user's explicit instruction in that turn (`CLAUDE.md`, "Releases"; README §5 rule 10).
  4. **A client's install, checked**, as *Release of `v0.1.0`* step 4: `uv pip install
     "raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0" "ray==2.55.1"` into a fresh
     3.13.16 venv in the scratchpad, with `uv`'s cache bypassed (`--no-cache`, for this install
     only): `direct_url.json` names `v0.2.0` and 05's commit; the installed package is the four
     modules and no `tests/`; from an empty directory with `-I`, `version` is `0.2.0`, `requires`
     is `['ray>=2.43']`, `ray.is_initialized()` is false, and `import raypoolkit.tests` raises
     `ModuleNotFoundError`.
  5. **Record it** on the board as *Release of `v0.2.0`*, in a commit of its own, with the header,
     README §2's row 05 and `prompts/INDEX.md` saying `v0.2.0` is tagged; then push it.
- **Report to the user:**
  - what landed, and the count, 121 → 121, at each end;
  - the wheel: 9 entries with and without the stale manifest, and that the orchestrator's rebuild
    from the commit matches; the issue closed, the index at 0;
  - what the README now tells a client moving its pin, in brief, and that its account of `v0.1.0`
    was checked against `v0.1.0`'s module;
  - (a)–(c) and the orchestrator's (o1);
  - the release sequence above, as a decision for them;
  - that 06, the adoption checklists, is measured against `v0.2.0` and can be written once the tag
    exists, with U10 to put to the user then.
