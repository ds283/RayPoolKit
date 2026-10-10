# Prompt 05 — release `v0.2.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 04 landed (`0b6ffd2`), its review is recorded (`914070c`), and CI passed at both ends on
  `0b6ffd2` (run `38071307103`) and on `914070c` (run `38071490036`).
- `git status` is clean in this repository, and the suite gives `Ran 121 tests … OK`.

**Closes:** `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`. **Narrows:** nothing.
**Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The code is two lines of `pyproject.toml`. Its weight is in the prose: `README.md` and
  `PROVENANCE.md` are what a client reads when it adopts, and every statement in them has to be
  true of the package as it will be tagged, checked against the module and not against this prompt.
- The release check of 03 is re-run with a stale manifest in the export, which is the one case 03
  could not make pass.

**Read first:**

1. [`README.md`](README.md): §0.1, §1, §2 (rows 04–06), §4, §5 (rules 6, 7, 10) and §6.2 (U8).
2. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`, above all "Releases".
3. The board: §3's one issue, with its measurements; §4's seven, each with its **Resolved (04)**
   line; the review of 04; and *Release of `v0.1.0`*, which is the sequence `v0.2.0` follows.
4. [`03-supported-versions-and-ci.md`](03-supported-versions-and-ci.md) §2.2–§2.4 (the venvs, the
   hazards, the release check) and [`logs/03-supported-versions-and-ci.md`](logs/03-supported-versions-and-ci.md)
   §6.1 (the issue) and its release-check record.
5. [`logs/04-fix-the-inherited-faults.md`](logs/04-fix-the-inherited-faults.md) §1.1 (the closed
   issues and their lines), §5 (observations 1–5, which this prompt acts on in part) and §7 (what a
   caller must pass after 04).
6. The repository as 04 left it: `pyproject.toml`, `README.md`, `PROVENANCE.md`; the constructor of
   `raypoolkit/RayWorkPool.py` (`:88-206`); `raypoolkit/contract.py`.

Facts below are at `914070c` (the package and suite as at `0b6ffd2`), measured on 2026-10-10.

---

## 1. What is wanted

05 makes `v0.2.0`, the release the clients adopt (README §0.1): `v0.1.0` with the inherited faults
fixed (04). After it:

- `pyproject.toml` says `0.2.0`, and a wheel built from it holds no test file however stale the
  build directory's manifest is (§2.1);
- `README.md` is true of `v0.2.0`: what changed since `v0.1.0`, what a caller now passes, and the
  pin a client writes (§2.2);
- `PROVENANCE.md` says what it says of `v0.1.0`, and records that the package has changed in its
  own right since (§2.3);
- the suite has passed at both ends in fresh venvs, and the release check has passed, on this
  machine, before anything reaches GitHub.

**05 makes no tag and pushes nothing** (README §5 rule 10). After its review, the push is put to
the user; CI must pass at both ends on 05's commit; and only then is `v0.2.0` made, annotated, on
that commit, and pushed, by the user or on the user's instruction, as `v0.1.0` was. If CI fails, no
tag: a fix prompt lands first.

**No behaviour of the package changes.** No file under `raypoolkit/` is touched, so the suite stays
at **121** and no printed line moves.

---

## 2. What to change

### 2.1 `pyproject.toml`

- `version = "0.2.0"` (from `"0.1.0"`).
- A `[tool.setuptools]` table, placed before `[tool.setuptools.packages.find]`, holding
  `include-package-data = false`. This closes
  `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]`.
  - **Why:** setuptools merges an existing `raypoolkit.egg-info/SOURCES.txt` into a build's
    manifest, and with package data on (the default) ships every listed file inside a found
    package as data, the excluded `raypoolkit/tests/` included. The package has no data files, and
    `LICENSE` reaches `dist-info/licenses/` through the metadata, not as package data.
  - **The exclusion stays.** It and this setting do different jobs: the exclusion keeps
    `raypoolkit.tests` out of the packages; this keeps its files out as data. Breakage (b) shows
    that this setting alone does not keep the tests out.
- Nothing else. `requires-python` and `dependencies` are U7's, unchanged.

**What the planner measured**, each wheel built with `uv build --wheel` (`uv` 0.12.20, whose build
environment runs setuptools under Python 3.14) from a fresh `git archive` export of `914070c`, with
`pyproject.toml` edited in the export:

| `pyproject.toml` | Repository's `raypoolkit.egg-info/` copied in | Entries | Under `raypoolkit/tests/` | Bytes |
|---|---|---|---|---|
| `0.2.0`, with §2.1's table | no | 9 | 0 | 13,565 |
| `0.2.0`, with §2.1's table | **yes** | 9 | 0 | 13,565 |
| `0.2.0`, without it | **yes** | 19 | 10 | 42,737 |
| `0.2.0`, with it, and the `exclude` removed | no | 19 | 10 | 42,737 |
| `0.2.0`, without it | no | 9 | 0 | 13,565 |

- The repository's `raypoolkit.egg-info/SOURCES.txt` still lists the ten test files at `914070c`,
  so the issue reproduces today. With §2.1's table and the stale manifest, setuptools prints no
  "absent from the `packages` configuration" warning; its only warnings are the two
  "byte-compiling is disabled" lines every build prints.
- The 9 entries are the four modules, `dist-info/licenses/LICENSE`, `METADATA`, `WHEEL`,
  `top_level.txt` and `RECORD`, as at `v0.1.0`. The wheel is larger than `v0.1.0`'s 12,016 bytes
  because the modules now carry the header and 04's checks.
- With §2.1's `pyproject.toml`, installed **editable** from an export in fresh venvs, one resolve
  with the pins: `Ran 121 tests … OK` at 3.12.15 / 2.43.0 and at 3.13.16 / 2.55.1; `version` is
  `0.2.0` and `requires` is `['ray>=2.43']`. The editable finder still maps the whole
  `raypoolkit/` directory, so the suite finds its tests.
- The wheel of the first row, installed into a fresh 3.13.16 / 2.55.1 venv and run from an empty
  directory with `-I`: the imports of 03 §2.4 succeed from `site-packages`, `version` is `0.2.0`,
  `ray.is_initialized()` is false, and `import raypoolkit.tests` raises `ModuleNotFoundError`.
- `ray` 2.59.0 is still the newest release, for Python 3.13 and 3.14.

### 2.2 `README.md`

The README was written for `v0.1.0` (03 §2.6). Make it true of `v0.2.0`, keeping its structure and
everything in it that is still true. Each change below names the text it replaces.

- **Status** (`:10-25`). `v0.2.0` is `v0.1.0` with the faults inherited from SecondaryGWKit's copy
  fixed, and the constructor's arguments checked; it is the release the client projects adopt. Each
  fix is guarded by a test that `v0.1.0`'s module fails. Point at the board's §4 for the issues, and
  keep the paragraph on the campaign plan and the one on DatastoreKit. `v0.1.0` stays described in
  one sentence: SGK's pool at `b510bc9`, moved with its behaviour unchanged (`PROVENANCE.md`).
- **A new section, "Changes in `v0.2.0`"**, after Status. For a client moving its pin from
  `v0.1.0`, as a short list, each item one or two sentences:
  - the constructor's argument checks raise `ValueError`, where `v0.1.0` raised `RuntimeError` or
    `RuntimeWarning`; and what each check is (§2.4 of prompt 04, read from the module);
  - a pool with no compute handler needs only `compute_handler=None`: the default store and
    persist handlers apply only with a compute handler; `store_handler=None` and
    `persist_handler=None` are still accepted, and the lines it prints are the same either way;
  - now refused at construction: a store handler, persist handler, validation handler or label
    builder given explicitly with no compute handler (each was silently ignored); a compute
    handler with `store_handler=None` or `persist_handler=None`; and a `create_batch_size`,
    `process_batch_size` or `max_task_queue` below 1 (each made `run()` loop for ever or raise);
  - with no validation handler, the post handler after a persist is given the persisted object,
    the one in `results`, with its `store_id`, where `v0.1.0` gave it the object from before the
    persist;
  - `store_results=True` accepts any iterable `task_list`, a generator included;
  - in-flight work is keyed on each ref's value, so the pool no longer depends on `ray.wait`
    returning the very objects it was given;
  - **the printed lines are unchanged**, in wording and layout.

  Do not name a client's call sites. Do not list the faults' history; the board holds it.
- **Installing** (`:45-49`): the pin is `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0`.
  Written as of the tag, as 03 wrote `v0.1.0`'s: the README is committed before the tag exists.
- **The work** (`:72-73`): "pass a sequence when `store_results=True`" goes; any iterable is
  consumed into a list at construction.
- **The sizes** (`:99-104`): say that each must be at least 1.
- **"A pool with no compute handler must pass `persist_handler=None`"** (`:147-153`) is replaced by
  a section on the constructor's checks, titled for what a caller does (for example "Which handlers
  a pool needs"): with a compute handler, the store and persist handlers default to the ones in the
  table and may not be `None`; without one, neither default applies, and the four compute-path
  arguments must be left out or `None`. Give each check's exception type and the gist of its
  message; do not copy the messages whole. Name no board issue in this section.
- **Developing** (`:209-211`): the equivalence check is retired at `v0.1.0`; it describes that tag,
  and runs, locally only, from a `git worktree` of it.
- **Licence** (`:213-215`): the four package modules carry the Apache 2.0 header.
- Everything else stays, including the printed-line examples (`:155-183`), which 04 did not change:
  check each line is still verbatim in `test_printed_lines.py`.

**Check every name.** As 03 §2.6 did: list every code span in the README that names a Python name,
argument, default, exception type or value; import each importable name in `venv/`; find each
argument in `inspect.signature(RayWorkPool)`; read each default from it; and confirm each statement
of the "Changes" section and the checks section by a test in the suite that asserts it, or by a
probe in the scratchpad. The log lists each, with how it was checked.

### 2.3 `PROVENANCE.md`

`PROVENANCE.md` describes the import, and stays a description of it. Three things in it are true
of `v0.1.0` and not of `v0.2.0` (log 04 §5, observation 2):

- "The differences allowed" (`:40-42`): `raypoolkit/RayWorkPool.py` equals its source except for
  the classes listed. Make it say so **of `v0.1.0`**: "At `v0.1.0`, …".
- The sentence closing that section, "The module keeps SGK's comments, docstrings and messages as
  they are": likewise of `v0.1.0`.
- "Re-running the check" (`:59-72`): the check was retired at `v0.1.0` (prompt 04 §2.8); it is run
  from a `git worktree` of that tag. Give the commands, with the worktree in a scratch directory
  outside the repository, and say it fails by design on a later tree.

And one addition, a section **"Since `v0.1.0`"**, before "The freeze": from `v0.2.0` the module is
this repository's own, and changes here are made by this repository's campaigns; `v0.2.0`'s
changes are 04's (`0b6ffd2`), listed in its log and on the board's §4, and the README's "Changes in
`v0.2.0`" says what they mean for a caller. Two or three sentences, with the links. SGK's copy is
still frozen (U5) until SGK adopts; the freeze section stays as it is.

Nothing else in `PROVENANCE.md` changes: the file map, the classes and the freeze are a record of
the import.

---

## 3. Verification

1. **The suite**, from the repository root: in `venv/` after its editable reinstall (§3.2), and in
   two fresh scratch venvs made as 03 §2.3 made them (`uv`, `/opt/local/bin/python3.12` with
   `ray==2.43.0` and `/opt/local/bin/python3.13` with `ray==2.55.1`, each with `black==25.1.0`, the
   repository installed editable in one resolve with the pins). Each gives `Ran 121 tests … OK`. No
   Ray process of this repository's before or after any run.
2. **`venv/`'s metadata.** After §2.1, reinstall the package there editable with `--no-deps`
   (`./venv/bin/python -m pip install --no-deps -e .`). Record `importlib.metadata.version` and
   `requires` before and after (`0.1.0` → `0.2.0`, `['ray>=2.43']` both), as 03's clarification 2
   did; `pip freeze` does not show an editable version.
3. **The release check**, 03 §2.4's, twice, each from its own fresh `git archive HEAD` export in the
   scratchpad with the working tree's `pyproject.toml` copied over the export's (the only file 05
   changes that the build reads):
   - **(R1)** the export as it is;
   - **(R2)** the export with the repository's `raypoolkit.egg-info/` copied in (`cp -R`), the stale
     manifest of the issue. If the repository has no `raypoolkit.egg-info/` when you start, stop
     and ask: (R2) is the issue's test.

   Each wheel: name, size, entry count, SHA-256 and file list; 9 entries, none under
   `raypoolkit/tests/`; and the build log searched for "absent from". Install the (R2) wheel into a
   fresh venv at the high end's pins, and from an empty directory with `-I` run 03 §2.4's checks
   with `0.2.0` for the version. Every wheel is built in an export, never in the repository tree
   (03's hazard 2).
4. `./venv/bin/black --check raypoolkit docs` (25.1.0) is clean. `black` is not run on the README
   or `pyproject.toml`.
5. **The README's names**, checked as §2.2 says, and every relative link in `README.md` and
   `PROVENANCE.md` resolving to a tracked file.
6. **The breakage record.** Each item is a diff against 05's `pyproject.toml`, exactly as applied,
   with what failed; applied in a fresh export with `git apply` run there (03's clarification 8),
   never to the repository's file; checked with `git apply --check` as recorded.
   - **(a) The issue, back:** the `[tool.setuptools]` table removed, the stale manifest copied in.
     The release check fails: 19 entries, 10 under `raypoolkit/tests/`, and the warning printed.
   - **(b) The setting alone:** the table kept, the `exclude` removed, no manifest copied. The
     release check fails: the tests ship as packages, and `import raypoolkit.tests` succeeds from
     the wheel.
   - **(c) The version not moved:** `version = "0.1.0"`. The release check's metadata check fails.

---

## 4. Acceptance

1. `pyproject.toml` is §2.1's: two changes and nothing else.
2. `README.md` and `PROVENANCE.md` are §2.2's and §2.3's, and every name in the README was checked.
3. The suite passes at both ends in fresh venvs, and in `venv/`; (R1) and (R2) pass; (a)–(c) fail
   as §3.6 says.
4. **The records**, in the same commit:
   - the log, `logs/05-release-v0.2.0.md`, per README §5.1. It also has:
     - every venv's versions and verdict line, and every install command as run;
     - `venv/`'s metadata before and after;
     - (R1) and (R2), each with name, size, entry count, SHA-256, file list and outputs;
     - every name the README mentions, with how it was checked;
     - (a)–(c);
     - the test count before and after (121, 121);
   - the board: the header; §1's row for 05 (landed, "this commit", 121 → 121); a line in the
     header saying `v0.2.0` is ready to be tagged once CI passes on 05's commit, with no tag made;
     and `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` moved from §3 to §4 with a
     dated **Resolved (05)** line naming the setting and (R2);
   - `docs/OPEN_ISSUES.md`: its row deleted, **1 → 0** open;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 121, in any venv.
- (R1) or (R2) fails in a way (a)–(c) do not explain, or (R2) cannot be made because the
  repository has no `raypoolkit.egg-info/`.
- A statement the README must make (§2.2) is not true of the module, or could only be made true by
  changing a file under `raypoolkit/`.
- Passing anything would need a change to a file not in §6.
- Anything would push, make or move a tag, change the repository's settings on GitHub, start Ray,
  or delete or rewrite the repository's `raypoolkit.egg-info/` other than by an editable install;
  or would edit, run or import SecondaryGWKit, ChamPBH, StochasticInstantons or DatastoreKit.
- A download other than PyPI packages into the scratchpad would be needed.

---

## 6. What this prompt does not do

- **Files it changes:**
  - `pyproject.toml`;
  - `README.md`;
  - `PROVENANCE.md`;
  - the log, this board, `prompts/INDEX.md` and `docs/OPEN_ISSUES.md`.
- It changes nothing else: no file under `raypoolkit/` or `docs/extraction/`; not the workflow,
  whose comment about the equivalence check is still true; not `CLAUDE.md`, `LICENSE`,
  `.gitignore` or the campaign README.
- It does not clean the repository's `raypoolkit.egg-info/`. It is gitignored and rewritten by
  every editable install; after §2.1, a stale one no longer reaches a wheel.
- It makes no tag and pushes nothing.
- It writes no adoption checklist (06) and names no client call site.
- It writes no orchestration note.

---

## 7. The log and the board

`logs/05-release-v0.2.0.md`, using README §5.1, with the additions of §4.4.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 05 (landed, commit, log, suite), and §3/§4 for
the one issue.
