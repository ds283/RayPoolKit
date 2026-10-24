# Prompt 03 — release `v0.3.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 02 landed (`722466a`) and was reviewed (`cc5f2d6`). CI passed at both ends on `cc5f2d6` (run
  40086680695), the first run over `docs/rehearsal-lock/ray_proof.py`.
- `git status` is clean in this repository, and the suite gives `Ran 226 tests … OK`.

**Closes:** nothing. **Narrows:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The code is one line of `pyproject.toml`. The weight is in the prose. `docs/rehearsal-lock.md`
  becomes the one statement of a contract three projects keep: a sentence in it that is not true
  of the module is a lock that one project reads differently from another. So every statement has
  to be checked against the module and its tests, not against this prompt or 01's log.
- `README.md`, `PROVENANCE.md` and `CLAUDE.md` are what a client and a later agent read first, and
  each has text that is true of `v0.2.0` and not of `v0.3.0`.

**Read first:**

1. [`README.md`](README.md): §0 (all of it), §1, §2 (rows 01–04), §4, §5 (rules 6, 7 and 10) and
   §6 (D2, D3, U1–U6).
2. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`, above all "What this repository is" and
   "Releases".
3. The board: the reviews of 01 and 02, and each one's "Observed, not opened".
4. `logs/01-the-lock-module.md`: §1.1 (the names and the helpers), §2 (deviations 3–5, 12–17),
   §3.2 (the command-line transcript) and §5. `logs/02-prove-it-under-real-ray.md`: the header,
   §3.4–§3.5 (one run's output is enough), §3.9 and §5.
5. `raypoolkit/rehearsal_lock.py` whole, and `raypoolkit/tests/test_rehearsal_lock.py`'s classes
   `TestCommandLine`, `TestArguments`, `TestOwnerFile` and `TestRayProcesses`. These are the source
   of every statement §2.2 asks for.
6. The precedent for a release: `prompts/extraction/05-release-v0.2.0.md` (§2–§3), and the
   extraction board's *Release of `v0.2.0`*.
7. The repository as 02 left it: `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md`.
8. The brief whose §2 the contract document replaces, read **only** through `git show`: `git -C
   /Users/ds283/Documents/Code/StochasticInstantons show
   8b4f615:.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md` (blob `d86ad43`), §2 and §3.

Facts below are at `cc5f2d6`, measured on 2026-10-24.

---

## 1. What is wanted

03 makes `v0.3.0` (U6): `v0.2.0` with the shared rehearsal lock, `raypoolkit.rehearsal_lock`, that
01 wrote and 02 proved under real Ray. After it:

- `pyproject.toml` says `0.3.0` (§2.1);
- **`docs/rehearsal-lock.md` states the lock**: its location, its owner file, its identity
  check, its process rule and what that asks of a caller, its commands, exit codes and `status`
  layout, and what it does not do. It names no client. It replaces the brief's §2 as the
  statement of the lock (§2.2);
- `README.md` is true of `v0.3.0`: what changed since `v0.2.0`, how the lock is run, and the pin
  (§2.3);
- `PROVENANCE.md` says where the lock module came from, and stops saying that a client's copy of
  the pool is still frozen (§2.4);
- `CLAUDE.md` says that the repository holds the lock, and that the lock's location, owner file,
  command line and `status` layout are interfaces (§2.5);
- the suite has passed at both ends in fresh venvs, and the release check has passed, on this
  machine, before anything reaches GitHub.

**03 makes no tag and pushes nothing** (README §5 rule 10). After the review, the push is put to
the user. CI must pass at both ends on 03's commit, and only then is `v0.3.0` made, annotated, on
that commit, and pushed, by the user or on the user's instruction, as `v0.2.0` was. If CI fails,
no tag is made: a fix prompt lands first.

**No behaviour of the package changes.** No file under `raypoolkit/` is touched, so the suite stays
at **226** and no printed line moves. `git diff v0.2.0 HEAD -- raypoolkit` holds only
`rehearsal_lock.py`, its tests and the guard's two tests (measured): `RayWorkPool.py`,
`contract.py`, `_timing.py` and `__init__.py` are `v0.2.0`'s.

**No Ray is started** (README §5 rule 9), and neither lock location under the real `HOME` is
touched.

---

## 2. What to change

### 2.1 `pyproject.toml`

- `version = "0.3.0"` (from `"0.2.0"`).
- `description`: `"A Ray work queue (RayWorkPool) that drives lookup, compute, store and validation
  tasks, and a shared rehearsal lock for Ray runs"`.
- Nothing else. `requires-python`, `dependencies`, `include-package-data = false` and the `exclude`
  stay as they are.

**What the planner measured.** A wheel built with `uv build --wheel` (`uv` 0.12.20) from a fresh
`git archive cc5f2d6` export, with only the version changed in the export:
`raypoolkit-0.3.0-py3-none-any.whl`, 21,341 bytes, **10 entries**. These are the five modules
(`RayWorkPool.py`, `__init__.py`, `_timing.py`, `contract.py`, `rehearsal_lock.py`),
`dist-info/licenses/LICENSE`, `METADATA`, `WHEEL`, `top_level.txt` and `RECORD`. None is under
`raypoolkit/tests/`. The build printed only the two "byte-compiling is disabled" warnings. The
wheel was installed into a fresh 3.13.16 / `ray==2.55.1` venv and run from an empty directory with
`-I`:
- the four modules and the two public names import from `site-packages`;
- `version` is `0.3.0` and `requires` is `['ray>=2.43']`;
- `ray.is_initialized()` is false;
- `import raypoolkit.tests` raises `ModuleNotFoundError`;
- `python -I -m raypoolkit.rehearsal_lock --help` prints the usage;
- `status` with `HOME` set to an empty directory prints `lock: free (…/.raypoolkit/rehearsal-lock
  does not exist)` and `Ray processes: no temp dir given`, exits 0, and leaves `HOME` empty.

The description changes the wheel's size by a few bytes.

### 2.2 `docs/rehearsal-lock.md`, the contract (new)

The statement of the lock that every project sharing it keeps. It is written for a reader in any
of them, so it **names no client**, no client's file and no client's port. It may say that the lock
replaces per-project implementations written from a brief of 2026-10-12, without naming them.
Every statement is true of `raypoolkit.rehearsal_lock` at this commit and is checked (§3.5).

Its sections, in this order, each as short as its content allows:

1. **What the lock is for.** Several projects run long Ray builds on one machine. The lock lets one
   rehearsal or long build run at a time. A held lock means stop and ask the user. Nothing waits,
   queues, retries or breaks a lock, and a stale lock is removed by the user, by hand, once
   `status` shows its pid not alive and no processes.
2. **How it is run.** `<venv>/bin/python -m raypoolkit.rehearsal_lock <command>`, with the project's
   own venv (U1), from a release pin. The five functions are a Python API with the same exit codes.
   The command imports Ray through the package root, about 0.3 s (U3).
3. **The location.** `~/.raypoolkit/rehearsal-lock`, computed from `HOME` each time. `acquire`
   makes `~/.raypoolkit` if needed, then the lock with one `os.mkdir`, which is the atomic step. No
   environment variable or command-line option moves it; the keyword `lock_dir` is for tests and
   proofs (U5).
4. **The owner file.** `owner` in the lock directory: UTF-8, seven `key: value` lines in the order
   `project`, `purpose`, `acquired`, `host`, `ray_temp_dir`, `ray_address`, `pid`, written as
   `owner.tmp` and renamed.
   - What each value is: `acquired` is ISO 8601, local time with its offset, to the second;
     `host` is `hostname -s`; `pid` is `-` until `set-pid`.
   - The argument rules each value obeys: every value one line; `ray_temp_dir` an absolute path in
     normal form, never `in-process`; `ray_address` `in-process` or `host:port`; a pid a positive
     integer.
   - How a reader parses it: the value is everything after the first `": "`.
5. **Whose lock it is.** A lock is the caller's when the owner's `project` and `ray_temp_dir` are
   the caller's. `set-pid` and `release` touch no other lock, and print both sides of a mismatch.
6. **The processes of a Ray instance.** The rule, exactly as `ray_processes` implements it:
   - the one reading of `ps -axww -o pid= -o ppid= -o command=`;
   - the temp-dir seed, in both its spellings and as a whole path component;
   - the client-server seed, only for a `host:port` address;
   - every descendant of a seed;
   - this process, its ancestors and its own descendants never listed, though they seed the walk.

   Then **what it asks of a caller**:
   - every Ray instance run under the lock has a temp dir of its own, recorded as `ray_temp_dir`.
     An in-process instance is started with `ray.init(address="local", _temp_dir=<dir>)`, with
     `ray_address` `in-process`. A `ray start` cluster gets `--temp-dir <dir>`, and its address
     `host:port`;
   - keep the temp dir short, since a Unix socket's path is limited to about 104 bytes on macOS,
     and never `/` or a directory other processes name (01's log §5);
   - record a pid with `set-pid` once Ray is up: the driver's for an in-process instance, the
     `gcs_server`'s for a cluster. Ray's process reaper is a child of an in-process driver and
     names no temp dir, so the rule does not list it. The recorded pid covers it, and the reaper
     was measured to exit at `ray.shutdown()` (02, at Ray 2.43.0 and 2.55.1);
   - any process whose command names the temp dir is listed: a shell, an editor, a `tail` of a Ray
     log. If such a process is an ancestor of the lock command, its other descendants are listed
     too. So a script that runs the lock names the temp dir in no command line of its own, and
     passes it some other way.
7. **The commands.** For each of `acquire`, `set-pid`, `release`, `status` and `ray-processes`:
   - its synopsis and what it does;
   - every exit code, with the condition that gives it (README §4's list, as the module has it).

   Then: usage errors exit 2. `release` takes the address from the owner file. `status` takes
   `--ray-address` only with `--ray-temp-dir` (01's deviation 13). Refusals and errors go to stderr.
8. **`status`'s layout**, line by line: every line it can print, in order, with the condition for
   each. Read them from the module, and pin each to the test that asserts it.
9. **The old location** (U4). In `0.3.x`, while `~/ScienceData/.rehearsal-lock` exists, `acquire`
   refuses with exit 3, printing that directory's owner file, and `status` reports it. It is
   removed in a later release, once every project has moved. It catches a project that was missed
   and still holds the old lock, and a stale old lock. It cannot catch a project that acquires at
   the old location after the move.
10. **What the lock does not do.**
    - It starts and stops no Ray, and signals no process.
    - It checks no port. An in-process instance under `ray[default]` starts a headless dashboard on
      Ray's default port, 8265, even with `include_dashboard=False` (measured, 02).
    - It cannot see a process of the instance whose command names neither the temp dir nor the
      address and that descends from no process that does.
    - Its process rule was proven under real Ray on macOS only. The suite, which runs on Ubuntu in
      CI, reads no real `ps`.
11. **How it was proven.**
    - The suite's tests of the module (`raypoolkit/tests/test_rehearsal_lock.py`, 103 tests),
      which need no Ray and touch no real `HOME`.
    - The proof under real Ray at both tested ends, holding the real lock:
      [`docs/rehearsal-lock/ray_proof.py`](rehearsal-lock/ray_proof.py), with how it is run (a
      `ray[default]` venv, in the background, from a command that names no temp dir) and a link to
      02's log for its results.

Use the module's names and messages as they are. Quote a message only where a caller is meant to
match it, and say so.

### 2.3 `README.md`

Make it true of `v0.3.0`. Keep its structure, and everything in it that is still true. Each change
below names the text it replaces or follows.

- **The opening** (`:1-8`) describes the pool alone. Add one short paragraph after it: the package
  also holds the shared rehearsal lock, `raypoolkit.rehearsal_lock`, which lets several projects on
  one machine run one Ray rehearsal or long build at a time. Link the contract document.
- **Status** (`:10-27`):
  - `v0.3.0` is `v0.2.0` with the lock added, and `RayWorkPool` unchanged: no change to its
    module, its arguments or its printed lines. Point at the `rehearsal-lock` campaign's README and
    board, as the paragraph does for `extraction`'s.
  - `v0.2.0` stays described, cut to what is still true: the faults inherited from SGK's copy fixed
    and the constructor's arguments checked, with its "Changes" section kept.
  - `v0.1.0`'s paragraph and the DatastoreKit paragraph stay.
- **A new section, "Changes in `v0.3.0`"**, before "Changes in `v0.2.0`". It is for a project moving
  its pin from `v0.2.0`, and is a short list:
  - `RayWorkPool` is unchanged, so moving the pin changes nothing else;
  - the new module and its command line, linking the contract;
  - the lock lives at `~/.raypoolkit/rehearsal-lock`. Every project that shares the lock moves to
    it on the same day, since a project still on its own implementation cannot see the new
    location; while the old location exists, `acquire` refuses.

  Name no client, and no client's file.
- **Supported versions** (`:58-72`). Add one item: the lock module is standard library only. Its
  process rule reads `ps` as macOS has it, and was proven under real Ray there (02). CI runs its
  tests, which read no real `ps`, on Ubuntu.
- **Installing** (`:79`): the pin is `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.3.0`.
  It is written as of the tag, as 05 of `extraction` wrote `v0.2.0`'s: the README is committed
  before the tag exists.
- **A new section, "The rehearsal lock"**, after "Using it" and before "Developing". It covers:
  - how it is run (`./venv/bin/python -m raypoolkit.rehearsal_lock …`);
  - the five commands in a table, with their exit codes;
  - the sequence a caller follows: `acquire`; start Ray on its own temp dir; `set-pid`; the work;
    stop Ray; `release`; and on exit 3, stop and ask the user;
  - a link to the contract for everything else.

  Do not copy the contract into the README. Name no client.
- **Developing** (`:235-255`). Add one paragraph: the lock's proof under real Ray,
  `docs/rehearsal-lock/ray_proof.py`, runs locally only, not in CI. It needs a venv with
  `ray[default]`, and it takes the real shared lock. Link its docstring for the rest.
- **Licence** (`:257-260`): "The four package modules" becomes the five.

**Check every name and statement.** Do this as `extraction` 05 §2.2 did:
- list every code span in the README's new and changed text that names a Python name, argument,
  command, option, exit code or path;
- import each importable name in `venv/`, and find each option in `build_parser()`;
- confirm each exit code by a test that asserts it, or by a probe against a scratch `HOME`.

The log lists each, with how it was checked.

### 2.4 `PROVENANCE.md`

- **The opening** (`:3`) says that `raypoolkit` was imported from SGK. Make it say that
  `RayWorkPool` was, and leave the rest of the opening as it is.
- **"Since `v0.1.0`"** (`:84-92`). Its last sentence, "SGK's copy stays frozen until SGK adopts a
  release", is no longer true: say that the freeze ended (below).
- **A new section, "Since `v0.2.0`"**, after "Since `v0.1.0`". It says:
  - `raypoolkit/rehearsal_lock.py` was written new for this package by `rehearsal-lock` prompt 01
    (`6733447`). It was not imported, and no client's history is carried;
  - its models, as its docstring names them: SGK's `tools/rehearsal_lock.py` at SGK `216e44d`
    (blob `ea14336`), for the owner file, `pid_alive`, the ancestor walk, the `ps` seam and the
    commands' structure and exit codes; and ChamPBH's
    `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` at ChamPBH `807f175` (blob
    `eaae1e7`), for `temp_dir_regex` and `list_cluster_pids`;
  - SGK's 42 tests (`tools/tests/test_rehearsal_lock.py`, blob `cdeecd6`), of which 41 were ported
    onto 39 tests (01's log §1.2);
  - the specification: the brief at StochasticInstantons `8b4f615`
    (`.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md`, blob `d86ad43`), §2, which
    [`docs/rehearsal-lock.md`](docs/rehearsal-lock.md) now replaces. StochasticInstantons'
    `ray_cluster.sh` (blob `6c8eada` at `8b4f615`) is the one ChamPBH's was adapted from;
  - where the module departs from its models (the location, D2; the old-location refusal, U4; one
    process rule by temp dir in place of SGK's rule by venv, U2), in one sentence each, linking
    the campaign README and 01's log for the rest.
- **"The freeze (decision U5)"** (`:94-101`) stays as the record of the freeze, with one sentence
  added saying it ended when the last client adopted: G2 held 2026-10-12, G3 2026-10-12 and G4
  2026-10-20 (the `extraction` board's §2), and each client has deleted its `RayTools/`.

Nothing else in `PROVENANCE.md` changes.

### 2.5 `CLAUDE.md`

- **"What this repository is"** (`:7-28`).
  - The first sentence: RayPoolKit holds the `RayWorkPool` work-queue layer **and the shared
    rehearsal lock**, both shared by three client projects.
  - The table's "Its copy today" column is out of date: every client's `RayTools/` is gone. Replace
    it with what each client has today: its pin (`v0.2.0` at SGK `216e44d`, ChamPBH `807f175` and
    StochasticInstantons `7071bb8`), and its own rehearsal-lock implementation until the
    switch-over (SGK's `tools/rehearsal_lock.py`; ChamPBH's and StochasticInstantons'
    `ray_cluster.sh`). Date the column 2026-10-24.
  - The rest of the section stays. The lock module names no client outside its provenance note,
    which the first exception already allows.
- **"Releases"** (`:79-92`). Add a paragraph after the one on printed lines: **the rehearsal lock
  is an interface shared by every project on the machine.**
  - Its location and owner file are a contract between projects. A change to either silently
    stops one project seeing another's lock, so it is made only by a prompt that says so, released
    under a new minor version, and adopted by every project on one day.
  - Its command line (commands, options, exit codes) and `status`'s layout are an interface, like
    the pool's printed lines.
  - [`docs/rehearsal-lock.md`](docs/rehearsal-lock.md) is its statement.
- **"Repository mechanics"** (`:94-`). Add one bullet: no test reads the real `ps` or reaches the
  real `HOME` (the lock's tests patch both). The lock's proof under real Ray,
  `docs/rehearsal-lock/ray_proof.py`, is run locally only, in a `ray[default]` venv, under the real
  lock.

Nothing else in `CLAUDE.md` changes.

---

## 3. Verification

1. **The suite**, from the repository root:
   - in `venv/` after its editable reinstall (§3.2);
   - in two fresh scratch venvs, made as 01's log §3.1 made the high end (`uv`;
     `/opt/local/bin/python3.12` with `ray==2.43.0`, and `/opt/local/bin/python3.13` with
     `ray==2.55.1`; each with `black==25.1.0` and the repository installed editable in one resolve
     with the pins).

   Each gives `Ran 226 tests … OK`. No Ray process before or after any run.
2. **`venv/`'s metadata.** After §2.1, reinstall the package editable with `--no-deps`
   (`./venv/bin/python -m pip install --no-deps -e .`). Record `importlib.metadata.version` and
   `requires` before and after: `0.2.0` → `0.3.0`, and `['ray>=2.43']` both times.
3. **The release check**, as `extraction` 05 §3.3 ran it, twice. Each run uses its own fresh `git
   archive HEAD` export in the scratchpad, with the working tree's `pyproject.toml` copied over the
   export's (the only file 03 changes that the build reads):
   - **(R1)** the export as it is;
   - **(R2)** the export with the repository's `raypoolkit.egg-info/` copied in (`cp -R`).

   For each wheel, record its name, size, entry count, SHA-256 and file list. It must have **10
   entries** and none under `raypoolkit/tests/`; search the build log for "absent from". Install
   the (R2) wheel, not editable, into a fresh venv at the high end's pins (`ray==2.55.1`, the
   minimal `ray`). Then, from an empty directory with `-I` and `PYTHONPATH` unset:
   - the imports of `extraction` 03 §2.4 and `raypoolkit.rehearsal_lock` succeed, from
     `site-packages`;
   - `version` is `0.3.0`, and `requires` is `['ray>=2.43']`;
   - `ray.is_initialized()` is false;
   - `import raypoolkit.tests` raises `ModuleNotFoundError`;
   - `python -I -m raypoolkit.rehearsal_lock --help` exits 0, its first line `usage: python -m
     raypoolkit.rehearsal_lock`;
   - with `HOME` set to an empty scratch directory: `status` exits 0 and prints `lock: free (…)`;
     and `ray-processes --ray-temp-dir /tmp/ray-rpk03-none` exits 0 and prints nothing, once you
     have checked that no process names that directory. `HOME` is still empty afterwards.

   Every wheel is built in an export, never in the repository tree.
4. **`black`**: `./venv/bin/black --check raypoolkit docs` (25.1.0) is clean. `black` is not run
   on Markdown or `pyproject.toml`.
5. **The contract's statements.** Number every statement of `docs/rehearsal-lock.md` that a test
   could falsify: each exit code, each `status` line, each argument rule, each step of the process
   rule and each owner-file rule. For each, name the test in `raypoolkit/tests/` that asserts it,
   or the probe in the scratchpad that showed it (`HOME` a scratch directory, `lock_dir` explicit,
   no Ray). Name 02's log where a statement rests on the proof under real Ray. A statement with
   none of these is a stop (§5).
6. **The README's names**, as §2.2 says; and every relative link in `README.md`, `PROVENANCE.md`,
   `CLAUDE.md` and `docs/rehearsal-lock.md` resolves to a tracked file.
7. **No client named** where none may be: `grep -n -i -E
   'secondary|sgk|champbh|cpbh|stochastic|instanton'` over `docs/rehearsal-lock.md` and the README's
   new and changed text finds nothing. `PROVENANCE.md` and `CLAUDE.md` name clients by design.
8. **The breakage record.** Each item is a diff against 03's `pyproject.toml`, applied in a fresh
   export with `git apply` run there, never to the repository's file. Record each exactly as
   applied, and say what failed:
   - **(a) The version not moved** (`version = "0.2.0"`): the release check's metadata check fails.
   - **(b) The tests' exclusion removed** (the `exclude` line deleted), with no manifest copied in:
     the wheel holds `raypoolkit/tests/`, and `import raypoolkit.tests` succeeds from it.
9. **The real `HOME` and Ray.** `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` are as they
   were, before and after; record both. `pgrep -lf 'gcs_server|raylet|ray::'` finds nothing, before
   and after.

---

## 4. Acceptance

1. `pyproject.toml` is §2.1's: two changed lines and nothing else.
2. `docs/rehearsal-lock.md` exists and is §2.2's, and every statement in it is checked (§3.5).
3. `README.md`, `PROVENANCE.md` and `CLAUDE.md` are §2.3–§2.5's, and every name in the README is
   checked.
4. The suite passes at both ends in fresh venvs and in `venv/`; (R1) and (R2) pass; (a) and (b)
   fail as §3.8 says.
5. **The records**, in the same commit:
   - the log, `logs/03-release-v0.3.0.md`, per README §5.1. It also has:
     - every venv's versions and verdict line, and every install command as run;
     - `venv/`'s metadata before and after;
     - (R1) and (R2), each with name, size, entry count, SHA-256, file list and outputs;
     - §3.5's table of the contract's statements, and the README's names, each with how it was
       checked;
     - (a) and (b);
     - the test count before and after (226, 226);
   - this board:
     - the header, with a line saying that `v0.3.0` is ready to be tagged once CI passes on 03's
       commit, and that no tag was made;
     - §1's row for 03 (landed, "this commit", 226 → 226);
   - `prompts/INDEX.md`: the campaign's line;
   - `docs/OPEN_ISSUES.md`, if the work opens anything.

---

## 5. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 226, in any venv.
- (R1) or (R2) fails in a way (a) and (b) do not explain.
- A statement §2.2 or §2.3 asks for is not true of the module, could not be checked (§3.5), or
  could only be made true by changing a file under `raypoolkit/`.
- Passing anything would need a change to a file not in §6.
- Anything would push, make or move a tag, or change the repository's settings on GitHub.
- Anything would start Ray, or touch `~/ScienceData/.rehearsal-lock` or `~/.raypoolkit` under the
  real `HOME`.
- Anything would edit, run or import SecondaryGWKit, ChamPBH or StochasticInstantons, or delete or
  rewrite the repository's `raypoolkit.egg-info/` other than by an editable install.
- A download other than PyPI packages into the scratchpad would be needed.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `pyproject.toml`;
  - `docs/rehearsal-lock.md` (new);
  - `README.md`, `PROVENANCE.md` and `CLAUDE.md`;
  - the log, this board and `prompts/INDEX.md`;
  - `docs/OPEN_ISSUES.md`, if needed.
- It changes nothing else:
  - no file under `raypoolkit/`, `docs/rehearsal-lock/`, `docs/adoption/` or `docs/extraction/`;
  - not the workflow, `LICENSE`, `.gitignore` or the campaign README.
- It makes no tag and pushes nothing.
- It writes no switch-over checklist (04), and names no client's call site.
- It runs no proof under Ray, and does not re-run 02's.
- It writes no orchestration note.

---

## 7. The log and the board

`logs/03-release-v0.3.0.md`, using README §5.1, with the additions of §4.5.

`IMPLEMENTATION_STATE.md`: the header, and §1's row for 03 (landed, commit, log, suite 226 → 226).
