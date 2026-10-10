# Orchestrator — prompt 01, import the pool

Read [`../README.md`](../README.md) first: §0.2, §1, §4, §5 and §6.2. This is the campaign's first
note, so it states the conventions in full. They are DatastoreKit's `extraction` notes'
(`DatastoreKit/prompts/extraction/orchestrator/prompt-01.md` §0's last list), adapted to a
repository whose package is one module, with no store and, until this prompt lands, no suite.

**You do not write code.** You may:
- run the suite, the equivalence check and the tests the log names;
- replay the log's deliberate-breakage diffs with `git apply`, and revert them;
- run an in-process check or a probe from the session scratchpad, never committing one;
- read SGK through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show b510bc9:<path>`, and
  DatastoreKit's one method through `git -C /Users/ds283/Documents/Code/DatastoreKit show
  v0.2.0:<path>`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`01-import-the-pool.md`](../01-import-the-pool.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** none expected ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- G1 holds: SGK's `RayTools/RayWorkPool.py` is blob `b4666fa` at the import commit `b510bc9`.
  U1–U5 are taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the campaign's foundation, and its only code is a move.** Every later prompt and every
client's adoption stands on two things it delivers: the package as imported, and
`compare_with_source.py`, the check that the package still *is* SGK's pool (README §5 rule 8).
The review therefore has two halves:
- **the package is SGK's pool**, under §4's names, changed only by D-imp, D-pool, D-int and D-fmt;
- **the equivalence check would catch a real difference**, not only pass on this one. A check that
  accepts everything is worse than none, because 02 and 03 will cite it.

**What moves on purpose:** nothing that behaves. New files only: `pyproject.toml`,
`PROVENANCE.md`, `raypoolkit/` (`__init__.py`, `RayWorkPool.py`, `_timing.py`, `contract.py`,
`tests/__init__.py`, `tests/test_package_imports.py`), `docs/extraction/compare_with_source.py`,
the log, and the records.

**The equivalence check: the hard part.** The prompt asks for rules, not line lists, and asks
them to be narrow. Recommended design, consistent with DatastoreKit's check:
- **A rule is a substitution applied to the source line.** A differing line pair is classified
  under a rule when the source line, with the rule applied, equals the package line exactly
  (indentation included). D-imp is a two-entry mapping of whole statements, read with `ast`: an
  `ImportFrom` at level 0 with one alias and no `asname`, whose `(module, name)` is
  `("Datastore.SQL.ShardedPool", "ShardedPool")` → `("raypoolkit.contract", "DatastorePool")` or
  `("utilities", "format_time")` → `("raypoolkit._timing", "format_time")`. D-pool is the one
  identifier `ShardedPool` → `DatastorePool` on a line that is a parameter annotation
  (`<indent><name>: DatastorePool,` after the substitution). A pair is replaced line for line
  (`difflib`'s `replace` opcode with equal lengths); an insertion or deletion is never classified.
- **No D-fmt rule is needed, and the recommendation is to have none.** SGK's module is black-clean
  under 25.1.0 (measured below) and the three rewritten lines are no longer than their sources, so
  `black` changes nothing. A check with no D-fmt class is stricter, and a line `black` did change
  is already a stop (prompt §5). If the agent does add one, it compares token for token
  (`tokenize`, ignoring `NL`/`NEWLINE`/`INDENT`/`DEDENT`) and the log says why it exists.
- **Breakage (h), the orchestrator's addition: an alias that keeps the old name.** Change
  `RayWorkPool.py:8` to `from raypoolkit.contract import DatastorePool as ShardedPool`, leaving
  `:75` as SGK's `pool: ShardedPool,`. The module behaves the same, but the import is not D-imp's
  mapping, and the check must exit non-zero and name line 8. Record it with (a)–(g), as an
  IMPLEMENTATION CHOICE made at the orchestrator's direction.

**The facts, checked by the orchestrator on 2026-10-10 at SGK `b510bc9`** (by `git show` and an
export to the orchestrator's scratchpad; no SGK code was run). Pass them on.
- **The gate.** SGK's `HEAD` is `b510bc9` (`b510bc90b66985532d28996ab4e5b13b0ff71709`, "Freeze the
  datastore layer while it moves to DatastoreKit"), its tree clean. `RayTools/RayWorkPool.py` there
  is blob `b4666fa89abb26829fd585b881947d7ef5172cea`, 575 lines, last changed by `0ee16a8`
  (2026-09-04, "Split RayWorkPool store_handler into store and persist handlers").
  `RayTools/__init__.py` is 0 bytes.
- **The prompt's line numbers hold.** `:8` and `:9` are the two client imports; `ShardedPool`
  occurs at `:8` and `:75` only; `format_time` is used at `:545` and `:567`. The other imports are
  `time`, `datetime.datetime`, `typing.Optional`, `ray` and `ray.ObjectRef` (`:1-6`).
- **`black` 25.1.0 leaves SGK's module unchanged** (`black --check` on the export: "1 file would
  be left unchanged").
- **Package line numbers equal SGK's.** D-imp and D-pool replace one line with one line, and
  `black` changes nothing, so every line of `raypoolkit/RayWorkPool.py` sits where it sat in SGK.
  The board's §3 lines will therefore be the planner's numbers. The agent still reads each from
  the package, and the log says so. Where the five faults sit, at SGK `b510bc9`:
  - in-flight keys on `ref.hex`: 26 lines from `:260` to `:506` (`self._inflight[…hex]`,
    `self._data[…hex]`, `self._compute_data[…hex]` and the `.pop`s);
  - the post handler after a persist: `:488-491`, the call at `:489`;
  - `results` from `len(task_list)`: `:138`;
  - the uneven checks: the `RuntimeWarning` at `:99-102`. (`:94-97` raises `RuntimeError` for a
    compute handler without a persist handler; that check is sound and stays);
  - "maker": `:96` and `:101`.
- **The internalised definitions.** SGK's `utilities.py` at `b510bc9` is 80 lines. `:20-22` are the
  three `SECONDS_PER_*` constants and `:25-61` is `format_time`, which uses no import. It binds a
  local named `str`, shadowing the builtin. That is copied byte for byte and not "fixed" (D-int).
  Do not copy DatastoreKit's `_timing.py`: it also holds `WallclockTimer`, which this package does
  not use.
- **The protocol.** DatastoreKit `v0.2.0` (`240028e`), `datastorekit/SQL/ShardedPool.py:3339`, is
  `def object_store(self, objects):`, unannotated. It returns one `ObjectRef` for one object, and
  a list of them for a list or tuple. The pool calls it with one object (`_default_persist_handler`,
  SGK `:68-69`). So `DatastorePool.object_store(self, objects) -> ObjectRef`, as the prompt says,
  states what the pool needs. The protocol does not model the list form, and its docstring may say
  that the pool passes one object. IMPLEMENTATION CHOICE; the log says so.
- **U4's shadowing**, re-measured by the orchestrator at Python 3.12.15 on a two-file package of
  the same shape. The package attribute and `import pkg.Mod as m` both give the class.
  `sys.modules["pkg.Mod"]` and `importlib.import_module("pkg.Mod")` give the module, whose class
  is the package's. `mock.patch("pkg.Mod.json", …)` patches the module.
- **Ray at import.** `import ray` takes about 3.3 s in this venv. It brings none of `datastorekit`,
  `Datastore`, `RayTools`, `utilities` or `config` into `sys.modules`, and leaves
  `ray.is_initialized()` false. The guard's tests 2 and 3 each start an interpreter that imports
  it. Give each `subprocess.run` a timeout of at least 120 s.
- **`-I` and the editable install.** `-I` drops `PYTHONPATH`, the user site and the script's
  directory, but keeps `site-packages`, where the editable install's hook lives. So from a
  scratch directory, `-I` finds `raypoolkit` only through the install, which is what tests 2 and
  3 should prove. Run before `pip install -e .`, test 2 fails. That is expected, not a fault.
- **The toolchain.** `venv/` exists from set-up: Python 3.12.15, `ray==2.43.0`, `black==25.1.0`,
  22 packages, `raypoolkit` not installed. `pip install -e .` builds in an isolated environment
  and fetches `setuptools` from PyPI, which was reachable at writing. `pip freeze` afterwards gains
  the editable `raypoolkit` line. Record it as printed.
- **In-repository state.** `.gitignore` already excludes `venv/`, `*.egg-info/`, `__pycache__/`,
  `build/`, `dist/`, `.idea` and `.DS_Store`. The repository root holds `docs/` and `prompts/`
  beside the package, and `docs/extraction/` will hold a `.py`, so `include = ["raypoolkit*"]` is
  needed, as the prompt says.
- **Expected counts:** the suite here is **0** before (there are no tests) and **3** after. The
  index is **5** open now, and 5 after unless the work finds something.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) The files.** Every file of the prompt's §2.2 and §2.3 exists under its name, and nothing
  else is in `raypoolkit/`.
- **(E2) Equivalence.** `compare_with_source.py` exits 0, and by reading, its rules are narrow:
  each is a mapping applied to the source, not a pattern that accepts a class of line.
- **(E3) The check bites.** (a)–(h) each exit non-zero and name what is wrong.
- **(E4) The guard.** 3 tests pass. Test 1 sees imports inside functions and relative imports;
  tests 2 and 3 run a fresh interpreter.
- **(E5) No client is reachable.** The prompt's §3.1 holds from a clean shell.
- **(E6) The pins.** The `numpy` import, the `datastorekit` import in `contract.py` and the
  removed re-export each fail as recorded.
- **(E7) The records.** The log in README §5.1's form with the prompt's §4.3 additions; the board,
  `prompts/INDEX.md`, the index (5) and `PROVENANCE.md`.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/` and `*.egg-info/` are gitignored and must not be
  staged. Count, then paste. A log states only what the diff, the check and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** Use `CLAUDE.md`'s command, from the repository root. Write the output to a file
  in the scratchpad and grep the verdict from it. Run it **in the foreground**, within the turn.
- **Breakage diffs** are recorded so that `git apply` replays them from a clean tree at the
  agent's commit. Check each with `git apply --check` and `-R --check`, and replay in `bash`, not
  zsh. None is committed. After each, `git status` must be clean. Breakage (g) adds an untracked
  file; record it as a `git apply`-able new-file diff, and delete the file after.
- **SGK is read only through `git show b510bc9:<path>`**, and DatastoreKit only through
  `git show v0.2.0:<path>`. Never from either working tree, never by importing either, never by
  running their code or tests (README §5 rule 5).
- **Scratch.** The agent uses its own subdirectory of the session scratchpad, never `/tmp`. The
  prompt's §3.1 runs "from `/tmp`"; any directory outside this repository that holds no
  `raypoolkit/` will do, and the scratchpad is one. Python's `tempfile` in tests is fine. **No
  scratch `.py` goes under `raypoolkit/`**, even for a moment: the guard and the check scan it.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A difference that fits no class is a stop, never a widened rule.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. `venv/` must hold no
   `raypoolkit`.
2. **G1.** Re-run `git -C SecondaryGWKit rev-parse b510bc9:RayTools/RayWorkPool.py`; it must be
   `b4666fa…`. Record SGK's `HEAD`, and whether `RayTools/` or `utilities.py` moved after
   `b510bc9` (U5 is in force from 01's commit; a move before it is not a stop, since the prompt
   reads `b510bc9`, but it is reported).
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
4. **The index.** 5 now, 5 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md` and `CLAUDE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's facts and its one addition (breakage (h)), and its two
recommendations (rules as substitutions; no D-fmt rule).

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01-import-the-pool.md`, in README §5.1's form, with
  the prompt's §4.3 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else.** In particular it
  must not touch `README.md`, `CLAUDE.md`, `LICENSE`, `.gitignore`, `.idea/`, the campaign README
  or anything under `orchestrator/`.
- **It edits no client repository and not DatastoreKit, and runs none of their code.**
- **It runs no build beyond `pip install -e .`, and starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — nine checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list and the records. No
   file under `venv/`, no `*.egg-info`, no `.idea/`, no scratch file.
2. **E1, the files.** `git ls-files raypoolkit` lists exactly `__init__.py`, `RayWorkPool.py`,
   `_timing.py`, `contract.py`, `tests/__init__.py` and `tests/test_package_imports.py`.
   `raypoolkit/__init__.py` binds `RayWorkPool` and `DatastorePool` and nothing else, with both
   in `__all__`. `contract.py` imports only `typing` and `ray`, is not `runtime_checkable`, and
   names no client or `datastorekit` class.
3. **E2, by running.** In a fresh shell, `./venv/bin/python docs/extraction/compare_with_source.py`
   exits 0. It reports two D-imp lines and one D-pool line, four matching definitions and the
   declared new files, and its counts equal the log's.
4. **E2, by reading.** Read `compare_with_source.py` in full. The blob is checked first. Each rule
   is a mapping from source to package text: D-imp is exactly the two statements, and D-pool the
   one identifier on a parameter line. No rule is a list of line numbers, and none accepts a line
   because it merely contains `raypoolkit` or `DatastorePool`. `_timing.py` is compared by `ast`
   segment, with nothing but the docstring besides. The walk skips `__pycache__` and fails on an
   undeclared `.py`.
5. **E3, the check bites.** Replay (a)–(h) from the log, one at a time, in `bash`. Each must exit
   non-zero and name the line or file. Then one of the orchestrator's own, not in the log: append
   SGK's `WallclockTimer` (`utilities.py:6-17`, with `import time` and `from traceback import
   print_tb`) to `raypoolkit/_timing.py`; it must fail as "something else in the module". Revert
   each, and check `git status` is clean.
6. **E4, the guard, by running and reading.** `./venv/bin/python -m unittest discover -s
   raypoolkit/tests -t .` gives `Ran 3 tests … OK`. Read `test_package_imports.py`: test 1 walks
   every module including `tests/`, uses `ast.walk` (so it sees function-level imports), resolves
   a relative import to `raypoolkit`, and names file, line and module on failure. Tests 2 and 3
   run `sys.executable -I` from a `tempfile` directory. Test 3's docstring states the patching rule.
7. **E5, isolation.** From the scratchpad, with `env -u PYTHONPATH`, run the prompt's §3.1 triple:
   the package import succeeds, and `import RayTools` and `import datastorekit` each fail with
   `ModuleNotFoundError`.
8. **E6, the pins.** Replay the `numpy` diff, the `datastorekit` diff in `contract.py` and the
   re-export removal, each in `bash`, and check that the failures are the log's. The suite is 3
   again after each.
9. **E7, the records.**
   - The log has every section of README §5.1; `pip freeze` (Python 3.12.15, `ray==2.43.0`,
     `black==25.1.0`, the editable `raypoolkit`); the check's whole output; the count before (0)
     and after (3); and, for each of the five §3 issues, the line in the package where its code
     sits, read from the package.
   - `PROVENANCE.md` has the six items of the prompt's §2.8, and the SGK commit's subject line is
     right ("Freeze the datastore layer while it moves to DatastoreKit"), as is `0ee16a8`'s.
   - The board has 01's row (landed, suite 3), and §3's five issues point at
     `raypoolkit/RayWorkPool.py` lines. The index counts 5 by counting, matching its header.
     `prompts/INDEX.md`'s row says 01 landed.
   - `./venv/bin/black --check raypoolkit docs` is clean.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph, in the form of
  DatastoreKit's `extraction` board. Fix small residue in a follow-up commit of its own. That
  includes:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status column for 01;
  - a list of orchestrator notes on the board, with this note marked "used for 01".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - what landed, and the count, 3;
  - the equivalence check's design, its counts per class, and (a)–(h) plus the orchestrator's own
    breakage failing it;
  - where the five inherited faults now sit in the package;
  - anything opened;
  - that 02 can now be written, against the tree 01 left, with U6 and U9 to put to the user.
