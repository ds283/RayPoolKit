# Orchestrator — prompt 04, fix the inherited faults

Read [`../README.md`](../README.md) first: §0.2 (faults 1–5), §1, §2 (rows 04–06), §4, §5 (rules
6–10) and §6.2 (U8, U11). Then read [`prompt-01.md`](prompt-01.md) §0's last list,
"Conventions", which this note keeps unless it says otherwise, and the board's *Orchestrator
review of prompt 03* and *Release of `v0.1.0`*.

**You do not write code.** You may:
- run the suite, the equivalence check (on `v0.1.0` only, after the commit) and the commands the
  log records;
- make exports and venvs of your own in the session scratchpad, and replay the log's breakage
  there, or in the tree from a clean `HEAD` at 04's commit;
- read SI's and CPBH's module headers through `git show`;
- fix small residue in a follow-up commit of your own (§4).

You do not push or tag. Pushing 04's commit, so that CI runs on it, is put to the user (§4).

**The prompt:** [`04-fix-the-inherited-faults.md`](../04-fix-the-inherited-faults.md)
**Closes:** seven issues (the prompt's list) · **Narrows:** nothing · **Opens:** none expected ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- 03 landed (`4e90a8a`), its review is recorded (`9db0619`), and `v0.1.0` is tagged on `4e90a8a`
  after green CI (`6b1ddfe`). 04 is written (`c207238`), and U8 and U11 are taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the first prompt that changes the pool, and every guard it adds must be seen to fail on
the code it replaces.** 01 moved the module, 02 pinned it as it behaves, 03 released it. 04 turns
02's pins inside out, and a guard that passes on both the old and the new module looks exactly like
one that works. The review therefore has four halves:
- **the module changes by §2 and nothing else**: the diff against `v0.1.0` is the 26 keys, one
  argument, one `range`, the rewritten checks, the sizes, the reworded comment and the header;
- **the guards bite both ways**: each fails on `v0.1.0`'s module (§4.5) and on its breakage
  (r1)–(r10), and passes on 04's;
- **no printed line moved**: every printed-line test of 02 passes unchanged, but for the
  `HANDLER_SETS` edit (README §5 rule 7);
- **the records close seven issues and open none**: the board's §3 → §4 moves, and the index
  falls from 8 to 1.

**What moves on purpose:** the four package modules; four test modules and one comment in
`test_standins.py`; the docstring of `compare_with_source.py`; the log, the board,
`prompts/INDEX.md` and `docs/OPEN_ISSUES.md`. Not `pyproject.toml`, `README.md`, `PROVENANCE.md`,
the workflow or `standins.py`. No new file under `raypoolkit/`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-10 at `c207238` (package
and suite as at `v0.1.0`, `4e90a8a`). Pass them on. Each is an IMPLEMENTATION CHOICE at the
orchestrator's direction unless it says otherwise, and the log says so.

1. **"`git status` clean after" means "the tree restored", since the work is not yet committed.**
   The breakage of §4.4 and the run of §4.5 happen on the final tree before the one commit, so
   `git status` is never clean then. Use 02's driver pattern (log 02 §5): before each item, record
   the SHA-256 of every file the work changes and `git status --porcelain --untracked-files=all`;
   after reverting, both must equal what they were. The log says "tree restored" for each.
2. **§4.5 overwrites the fixed module; keep a copy first, and never restore through git.**
   `git show v0.1.0:raypoolkit/RayWorkPool.py > raypoolkit/RayWorkPool.py` replaces uncommitted
   work, and `git checkout`, `git restore` or `git stash` would then bring back `v0.1.0`'s module,
   not 04's, or tangle the index. Copy the fixed module to the scratchpad, overwrite, run, copy it
   back, and check its SHA-256 against the copy (clarification 1). The breakage diffs are reverted
   with `git apply -R`, never with `git checkout`.
3. **The planner's expected failures for (r1)–(r10) are a floor, not the set.** The log lists what
   actually fails, and a wider set is not a stop; only an item that fails nothing is (prompt §6).
   (r4) in particular is wide: every lookup-only test spelled `LOOKUP_ONLY`
   (`{"compute_handler": None, "persist_handler": None}`, in four test modules) leaves the store
   handler at its default, so with the resolutions removed each raises at construction. Measured
   on a scratch copy with every fix applied and the suite *unchanged*: (r4) fails 71 of the 116.
   (r5) is narrow, since `LOOKUP_ONLY` passes `persist_handler=None` explicitly.
4. **Runs within one test share the clock: reset it between them.** `PoolTestCase.setUp` patches
   `time` and `datetime` with namespaces bound to `self.clock`, so assigning a new `ScriptedClock`
   to `self.clock` patches nothing, and a second run in the same test starts from the first run's
   last reading. Measured: two identical lookup-only runs in one test print different stamps and
   times. `test_a_lookup_only_pool_prints_the_same_lines_however_its_handlers_are_spelled` sets
   `self.clock.reading = 0` before each spelling's run (one `subTest` each, or a loop); then all
   three print the nine lines of `test_a_lookup_only_run_notifying_on_every_pass` exactly. Setting
   the stand-in's own public attribute is not a white-box seam of the pool, and `standins.py` does
   not change. C6 needs no reset: it reads only the queued message.
5. **The flips, re-measured.** The orchestrator's scratch copy applied every change of §2 as the
   prompt words it (the checks as one loop over `(name, value)` pairs per branch, then the sizes'
   loop) and ran the unchanged suite: `Ran 116 … FAILED (failures=6, errors=5)`, exactly §3.5's
   eleven, at both 3.12.15 / 2.43.0 and 3.13.16 / 2.55.1. Errors: C1, the fault-4b pin and the three
   `TestStatusMessages` "validation only" subtests (`ValueError` at construction); failures: C2,
   the fault-1, fault-2, fault-3 and fault-4a pins, and S4. `black` left the scratch copy's 15 files
   unchanged. The messages are §2.4's and §2.5's verbatim, each one f-string on one line; with
   several bad arguments, the first in §2.4's order is named (`store_handler` before
   `persist_handler`, before `validation_handler`, before `label_builder`).
6. **Running from a tree other than the repository.** With `-m unittest` from a directory,
   `raypoolkit` resolves to that directory's copy before the editable install (sys.path[0] wins;
   measured in the orchestrator's export). So the suite run from the repository root tests the
   working tree, and a run from an export tests the export. The guard's tests 2 and 3 run `-I` from
   a temporary directory and import the installed package, which is the repository's.
7. **The high end.** As 03 made it: `uv venv -p /opt/local/bin/python3.13`, then
   `uv pip install -e <repository> "ray==2.55.1"` in one resolve. This rewrites the gitignored
   `raypoolkit.egg-info/` at the repository root (03's clarification 1); that is allowed, never
   staged, and no wheel is built. `uv`'s cache is allowed. `venv/` needs no reinstall: the metadata
   does not change.
8. **The licence header.** SI `7bb3efd` and CPBH `52142d7` `RayTools/RayWorkPool.py` lines 1–14
   are identical (`cmp`), SHA-256 `e73e93340148903e1dc2ffdba80b9870faeee548ea4275ab89f488d9c42e1ab9`,
   and line 15 is blank in both. Take it with `git -C …/StochasticInstantons show
   7bb3efd:RayTools/RayWorkPool.py | head -14`, and prepend it and one `"\n"` to each module
   programmatically. `_timing.py` and `contract.py` open with their docstrings, which stay their
   module docstrings below a comment block. The header test's constant is the 14 lines and the
   blank line, 15 lines; the log gives its SHA-256 beside SI's.

**The facts, checked by the orchestrator.** Pass them on.

- **The baseline at `c207238`.** `venv/`: Python 3.12.15, `ray==2.43.0`, `black==25.1.0`,
  `raypoolkit` editable. `Ran 116 tests … OK`, by module `test_construction` 12,
  `test_inherited_faults` 5, `test_package_imports` 3, `test_printed_lines` 17, `test_run_paths`
  22, `test_scheduling` 7, `test_standins` 30, `test_task_builder` 20. `compare_with_source.py`
  exits 0 (572 identical, 2 D-imp, 1 D-pool, 4 D-int, 12 declared files, 0 undeclared, `RESULT:
  OK`). `black --check raypoolkit docs`: 15 files unchanged.
- **The prompt's line numbers hold** at `v0.1.0`: the 26 `.hex` lines are exactly the board's list,
  `:260 … :506`, one `.hex` each; the checks are `:94-102`; `range(len(task_list))` is `:138`; the
  call `self._post_handler(obj)` in the `"store"` branch is `:490`, the only one in that branch;
  "the Datastore service" is `:424`, its only occurrence. The header moves every line by 15.
- **The prompt's §2.4 holds**, on the scratch copy: `compute_handler=None` with nothing else, with
  `persist_handler=None`, with `store_handler=None` and with both, each constructs and its queued
  message is `0 lookup`; titled, each prints the same nine lines. Each of the four compute-path
  arguments given a callable without a compute handler, and `store_handler=None` or
  `persist_handler=None` with one, raises `ValueError` with its message. Each size at 0 and -1
  raises `"<name> must be at least 1, not 0"` (or `-1`), and at 1 constructs.
- **Expected counts.** The suite is **116** before and **121** after: `test_construction` 12 → 15
  (C5, C6, C7), `test_inherited_faults` 5 → 6 (the header test), `test_printed_lines` 17 → 18 (the
  spelling test); the other five unchanged. The index is **8** now and **1** after (the
  `[03-…egg-info…]` row).
- **The check's last run.** It is run once, before any change, and its whole output goes in the log.
  After 04 it fails by design. DatastoreKit's retired paragraph (`HEAD`, lines 1–8) is the
  precedent for the wording only; this one names `v0.1.0`, README §5 rule 8 and prompt 04 §2.8.
- **Nothing outside the repository runs.** The workflow (`.github/workflows/tests.yml`) does not
  run `compare_with_source.py`, and no test does. `origin/main` is `6b1ddfe`; local `main` is
  ahead by `c207238` and this note. The tag `v0.1.0` is on `4e90a8a`.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty), before
  or after the orchestrator's runs.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §7 files changed; `pyproject.toml`, `README.md`,
  `PROVENANCE.md`, the workflow, `standins.py` and every other test untouched; no new file; no tag;
  nothing pushed.
- **(E2) The module.** `git diff v0.1.0 <commit> -- raypoolkit/` is §2's changes and nothing else.
- **(E3) The suite.** 121, OK, at both ends.
- **(E4) The guards bite.** (r1)–(r10) each fail what the log says; §4.5's run fails every guard.
- **(E5) The lines.** Every printed-line test of 02 unchanged but `HANDLER_SETS`.
- **(E6) The tests are the prompt's.** Names, docstrings and assertions as §3 tabulates.
- **(E7) The records.** The log with §5.5's additions; the board's seven moves; the index at 1;
  `prompts/INDEX.md`.

**Conventions.** Prompt 01's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run every suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff with `git apply --check` (and `-R --check` once applied), replay it in
  `bash`, and check the tree is restored after it (clarification 1);
- use the scratchpad subdirectory you are given, never `/tmp`, and put no scratch file under the
  repository, least of all under `raypoolkit/` (the suite collects it);
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

Two additions:
- **Nothing outward-facing.** No `git push`, no `git tag`, no `gh` command that writes.
- **Diff and output files have distinct names on this case-insensitive filesystem** (log 02 §5's
  slip): name them `r01.diff` … `r10.diff`, not anything that differs from another only by case.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. `git diff v0.1.0 --
   raypoolkit` is empty.
2. **The baseline.** The suite gives `Ran 116 tests … OK`, and `compare_with_source.py` exits 0
   with the counts above. `git tag` is `v0.1.0` alone; `git ls-remote origin` shows `main` at
   `6b1ddfe` and the tag on `4e90a8a`.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
4. **The index.** 8 now; 1 after. Tell the agent both.
5. **Scratch.** Make the agent's subdirectory of the session scratchpad, empty, and tell it the
   path. Keep your own measurements in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, and logs 02 and
  03 (the sections the prompt names);
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's eight clarifications and additions. Clarifications 2
and 4 are the ones that matter: the first so that §4.5 does not destroy the work, the second so
that the spelling test compares like with like.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/04-fix-the-inherited-faults.md`, in README §5.1's
  form, with the prompt's §5.5 additions.
- **The files it may change are the prompt's §7 list, and nothing else.** In particular it must
  not touch `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore`,
  `.github/`, `standins.py`, any other test, the campaign README, or anything under
  `orchestrator/`; and it adds no file under `raypoolkit/`.
- **It pushes nothing and tags nothing**, and writes nothing to GitHub.
- **It edits no client repository and not DatastoreKit, and runs none of their code**; it reads
  SI's header and DatastoreKit's docstring through `git show` only.
- **It starts no Ray.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — ten checks

1. **E1, scope.** `git show --stat <commit>` touches only the prompt's §7 files.
   `git diff c207238 <commit> -- pyproject.toml README.md PROVENANCE.md CLAUDE.md LICENSE
   .gitignore .github raypoolkit/tests/standins.py raypoolkit/tests/test_package_imports.py
   raypoolkit/tests/test_scheduling.py raypoolkit/tests/test_task_builder.py
   prompts/extraction/README.md` is empty, and `git diff` of `test_standins.py` is the one comment.
   `git ls-files raypoolkit` lists the same files as at `v0.1.0`. `git tag` is `v0.1.0` alone and
   `git ls-remote origin` is unchanged.
2. **E2, the module, by reading.** Read `git diff v0.1.0 <commit> -- raypoolkit/RayWorkPool.py`
   whole. It is: the header and its blank line; the constructor's checks of §2.4 and §2.5, the
   resolution by identity, the resolved values stored; `range(self._num_total_items)`; the
   reworded comment; 26 lines `.hex` → `.hex()` and nothing else on them; `:490`'s argument. Count
   the `.hex()` lines (26) and check that no `.hex\b` without `()` remains. The other three modules
   differ from `v0.1.0` by the header, and `contract.py` also by §2.7's sentence. The signature is
   unchanged: `inspect.signature(RayWorkPool)` at the commit and at `v0.1.0` give the same string.
3. **E3, the suite, by running.** In a fresh shell: `venv/` gives `Ran 121 tests … OK`, by module as
   §0 expects. Then **your own** fresh high-end venv (3.13.16 / 2.55.1, editable from the repository
   in one resolve): 121, OK. No Ray process before or after.
4. **E4, the breakage, by replaying.** Extract (r1)–(r10) from the log's text and replay each from
   the clean tree at 04's commit, the whole suite under a 300 s timeout. Each must fail exactly the
   tests the log lists for it. `git status` is clean after each (here it is: the work is committed).
   Then two of the orchestrator's own, not in the log:
   - (o1) the size check `value < 1` → `value <= 1`: C7's cases at 1 must fail (and most of the
     suite with them, since `process_batch_size` defaults to 1);
   - (o2) `("store_handler", store_handler),` dropped from the no-compute tuple only: C2's
     `store_handler` subtest must fail, since an explicit store handler without a compute handler
     then constructs.
5. **E4, the guards on `v0.1.0`.** Make a fresh export of 04's commit, copy `v0.1.0`'s
   `raypoolkit/RayWorkPool.py` over it, and run the suite from the export (clarification 6). The
   failing set must equal the log's §4.5 account: every guard of §3.1, C1, C2, C5, C6, C7, S4, X1,
   the spelling test and the new `HANDLER_SETS` subtests, the header test for `RayWorkPool.py`
   only. Every test 04 did not change passes there (for example `test_neither_handler_constructs`).
6. **E5, the lines.** `git diff c207238 <commit> -- raypoolkit/tests/test_printed_lines.py`
   changes only `HANDLER_SETS` (one key gone, two added) and adds the one test; no expected line of
   an existing test changes. Read the spelling test: three spellings, the clock reset before each,
   compared with the existing test's nine lines.
7. **E6, the tests, by reading.** `test_inherited_faults.py`: the five new names of §3.1's table,
   each docstring naming its resolved issue and the old behaviour, the module docstring naming the
   board's §4; the fault-1 guard has one `subTest` per path of §2.1 and asserts each run's own
   `results`; the header test finds the modules from `raypoolkit.__file__`. `test_construction.py`:
   the three message templates replace the two constants, C1/C2 renamed with `type(...) is
   ValueError` and messages whole, C5–C7 as tabulated. `test_run_paths.py`: S4 asserts identity with
   `results[0]` and `store_id` 1001; X1 seeds under `ref.hex()` only. No new white-box seam:
   `grep -nE "\._[a-z]" raypoolkit/tests/test_*.py` finds nothing 02's review did not.
8. **The check, retired.** `git diff c207238 <commit> -- docs/extraction/compare_with_source.py`
   adds one paragraph to the top of the docstring and nothing else. From a `git worktree` of
   `v0.1.0` in the scratchpad (removed after, so that `git worktree list` is this checkout alone):
   the check exits 0 with the counts above. The log holds the agent's last run, whole.
9. **`black`.** `./venv/bin/black --check raypoolkit docs` (25.1.0) is clean.
10. **E7, the records.** The log has every section of README §5.1 and each of the prompt's §5.5
    additions: the check's last output; the module's diff against `v0.1.0`, whole; each closed
    issue with its new lines and its guard; the counts by module, 116 → 121; (r1)–(r10) and §4.5;
    both venvs' versions and verdicts; §0's clarifications recorded as deviations. Board: the
    header; 04's row (landed, "this commit", 116 → 121); §3 holds one issue, and §4 the seven, each
    with a dated **Resolved (04)** line naming its fix and its guard; U8 and U11 shown as applied.
    Index: count it (1), and check the header matches. `prompts/INDEX.md`: the campaign's line.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 04* paragraph, in the form of
  03's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 04, and its header;
  - the notes line, with this note added and marked "used for 04".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Put the push to the user, and do none of it unasked.** CI has not run on 04's tree, and 05 will
  tag `v0.2.0` only on green CI. *Recommended:* push 04's commit alone first (`git push origin
  <04's SHA>:main`), so that the run is on it, then the review's follow-up. `c207238` and this
  note go with it; they touch only `prompts/`.
- **Report to the user:**
  - what landed, and the count, 116 → 121, at each end;
  - the module's diff against `v0.1.0`, in a line per fault;
  - what a caller may now leave out (both handlers, without a compute handler), and what is now
    refused at construction, with `ValueError`;
  - (r1)–(r10), the orchestrator's (o1)–(o2), and the guards failing on `v0.1.0`;
  - the seven issues closed, the index at 1;
  - the push, as a decision for them;
  - that 05 can be written once 04's CI is green, and that it is the natural owner of
    `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`.
