# Prompt 07 — verification and close-out

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 06 landed (`67f3f7e`) and was reviewed (`71f0d66`).
- **`main` is pushed, and CI passed at both ends on `71f0d66` or a later records commit.** CI has
  not yet run over `docs/adoption/measure_client_pools.py`, which its `black` step checks. *(Not
  yet at writing: `origin/main` was `b2b6ab4`.)* The orchestrator records the run's number before
  dispatch.
- `git status` is clean in this repository, and the suite gives `Ran 121 tests … OK`.
- The tags on `origin` are `v0.1.0` and `v0.2.0`, peeling to `4e90a8a` and `eaef0ce`.
- U13 and U14 are taken (README §6.2).

**Closes:** the campaign. **Narrows:** nothing. **Changes:** nothing of the package. **Opens:**
only what the work finds.

**Recommended model:** **Opus.**
- This is a verification prompt, and its document is the one a later reader starts from. It is
  built from six logs, six reviews and two releases, and every count in it has to be counted.
- It changes no line of the package. It writes one document and one script, and closes the board.
- For the first time in this campaign it starts Ray (U13), under the rules of §3.

**Read first:**

1. [`README.md`](README.md): every section, and §6.2 (U1–U14) in full.
2. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`: "What this repository is", "Releases", the
   campaign conventions and "Repository mechanics".
3. The board, every section. In §1, every orchestrator review in full, their "Findings", the two
   release records and *CI on 04's commit*.
4. Every log, `logs/01-…` to `logs/06-…`: at least "What shipped", the deviations, the
   observations not acted on, and the state handed on.
5. `README.md`, `PROVENANCE.md`, `docs/OPEN_ISSUES.md`, `docs/adoption/README.md`.
6. The precedent, DatastoreKit's verification document, read **only** as
   `git -C /Users/ds283/Documents/Code/DatastoreKit show 39b1348:docs/extraction-verification.md`
   (its close-out commit), for the form. Its content is about the datastore layer; do not copy it.

Facts below are at `71f0d66`, whose `raypoolkit/` is `eaef0ce`'s (`v0.2.0`), measured on
2026-10-10.

---

## 1. What is wanted

07 verifies the campaign, from the package as tagged `v0.2.0` and the records of 01–06, in **one
document**, `docs/extraction-verification.md`, and **closes the campaign**.

**The package does not change.** Nothing under `raypoolkit/` is touched, the suite stays at
**121**, and no tag is made (README §5 rule 10). 07 pushes nothing, and uses no network (U14).

One thing is done for the first time in this campaign, because the user decided so on
2026-10-10:
- **U13: a smoke run under real Ray.** Until now the pool has run only against the suite's
  in-process stand-in for `ray.wait` and `ray.get` (U6). 07 runs it under a local `ray.init()`, with
  no cluster, at both tested ends, with a script kept in `docs/extraction/`.

### 1.1 The smoke run (U13), probed

The planner probed the run on this machine from a scratch directory, with plain objects and remote
functions defined in the probe itself.
- **The ends.** Low: Python 3.12.15 / Ray 2.43.0 (the repository's `venv/`). High: 3.13.16 /
  2.55.1 (a `uv` venv made offline from the cache, `raypoolkit` on `PYTHONPATH`).
- **The start.** `ray.init(num_cpus=4, include_dashboard=False, log_to_driver=False)` starts a
  local instance, with no network beyond the loopback. `ray.shutdown()` in a `finally` leaves no
  process: `pgrep -lf 'gcs_server|raylet|ray::'` is empty after, including after a run that
  raised. At 2.55.1, `ray.init` writes a `FutureWarning` about `RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO`
  to stderr; it is Ray's, and harmless.
- **The objects.** An `Item` with `available`, `compute(label=None, payload=None)` (returning the
  `ObjectRef` of a remote function) and `store()`; a remote `lookup(n, available)` returning an
  `Item`; a `Store` actor whose `object_store` sets `store_id`, sets `available` and returns the
  object, and whose `validate` returns `True`; and a pool object whose `object_store` calls the
  actor. Defined in the script, they are pickled by value.
- **The steps**, each passing at both ends:
  1. **lookup-only**, `compute_handler=None`, a **generator** `task_list` of 20 items,
     `store_results=True`, `create_batch_size=3`, `process_batch_size=4`, `max_task_queue=5`:
     `results` holds the 20 objects in order;
  2. **the compute path**: 12 items, each built as `{"ref": …, "compute_payload": 1}`, with a
     validation handler and a label builder, `store_results=True`, `process_batch_size=3`,
     `max_task_queue=4`: every result persisted (`store_id` 1–12, `stored`, `available`), and the
     completion line counts 12 lookup, compute, store and validation;
  3. **a persist with no validation, then a post handler**: 5 items; the post handler sees each
     object's `store_id` set (fault 2's fix);
  4. **the availability path**: `compute_handler=None`, an availability handler, and a task builder
     returning `None` for one item and a list of two refs for each other: the handler is called on
     each of the 10 looked-up objects;
  5. **the printed lines in real time**: a titled lookup-only pool of 30 remote tasks of 0.05 s,
     notifying on every pass (`notify_min_time_interval=0`, `notify_time_interval=0`,
     `notify_batch_size=1`), stdout captured: 1 banner, 15 progress lines and 1 completion line
     matched `BANNER_PATTERN`, `PROGRESS_PATTERN` and `COMPLETE_PATTERN` from
     `raypoolkit/tests/test_printed_lines.py:35-39`; the stamps carry no UTC offset; `total_time`
     is set.

  Steps 1–4 took 6.0 s at the low end and 9.0 s at the high end, Ray's start included.
- **What the run tells apart**, probed at the high end on scratch copies of the module:
  - fault 2's fix reverted (`raypoolkit/RayWorkPool.py:530`, `self._post_handler(replacement_obj)`
    → `self._post_handler(obj)`): step 3 fails, every `store_id` `None`;
  - fault 3's fix reverted (`:178`, `range(self._num_total_items)` → `range(len(task_list))`):
    step 1 raises `TypeError: object of type 'generator' has no len()` at construction;
  - **fault 1's fix reverted** (the 26 `.hex()` → `.hex`): **every step passes.** Under real Ray,
    `ray.wait` returns the very refs it was given, so the bound-method keys still match; this is
    what README §0.2 said, and why fault 1 is pinned by the stand-in, which can return equal refs
    that are distinct objects. It is a finding for the document, not a breakage.
  - `v0.1.0`'s module refuses step 1's spelling at construction (`RuntimeWarning`, the default
    persist handler with no compute handler), and Ray is still shut down.

### 1.2 The release (U14)

The pin was installed from GitHub at the release, and is not fetched again: the board's
*Release of `v0.2.0`*, step 4, records `uv pip install --no-cache "raypoolkit @
git+https://github.com/ds283/RayPoolKit@v0.2.0" "ray==2.55.1"`, its `direct_url.json` naming
`v0.2.0` and `eaef0ce`, the four modules installed and no `tests/`. 07 cites that record.

Offline, the planner rebuilt the wheel from `git archive v0.2.0` with `uv build --wheel --offline`:
`raypoolkit-0.2.0-py3-none-any.whl`, **13,565 bytes**, the **9** entries of 05's log
(`raypoolkit/RayWorkPool.py`, `__init__.py`, `_timing.py`, `contract.py`, and the dist-info's
`licenses/LICENSE`, `METADATA`, `WHEEL`, `top_level.txt`, `RECORD`), and no "absent from" line in
the build log.

### 1.3 The records to collect

- **Prompts and commits.** 01 `49f3ddf`, 02 `b9f6dec`, 03 `4e90a8a`, 04 `0b6ffd2`, 05 `eaef0ce`,
  06 `67f3f7e`. Reviews: `53477ff`, `307ed96`, `9db0619`, `914070c`, `9a00f80`, `71f0d66`. Notes:
  `310db6e`, `319099a`, `e136eee`, `a7d9252`, `1868b6e`, `deffdc2`. The other commits on `main`,
  from `3f1dfd4` (the repository started) to `71f0d66`: the plan (`4cb493f`); each prompt written,
  with the decisions it recorded (`97f9ff0`, `d9adb9b`, `c73fc91`, `c207238`, `f839209`,
  `a1d64ea`); the two release records (`6b1ddfe`, `b2b6ab4`). 28 commits in all; class each.
- **Tags and CI.**
  - `v0.1.0` (tag object `0a9cdb2`) on `4e90a8a`, after
    [run 38054782562](https://github.com/ds283/RayPoolKit/actions/runs/38054782562);
  - `v0.2.0` (tag object `4e7eb15`) on `eaef0ce`, after
    [run 38075908457](https://github.com/ds283/RayPoolKit/actions/runs/38075908457);
  - also green: runs `38071307103` (`0b6ffd2`), `38071490036` (`914070c`), `38076190172`
    (`b2b6ab4`), and the gate's run on 06's records.
- **The suite** went 0 → 3 (01) → 116 (02) → 116 (03) → 121 (04) → 121 (05) → 121 (06). Each log
  records its count before and after, and by module from 02 on.
- **Issues.** Eight were opened and resolved on the board (§4): the five `[00-…]` inherited from
  the source (opened at planning, pinned by 02, fixed by 04), `[01-a-kept-comment-names-the-datastore-service]`
  and `[02-the-constructor-does-not-check-its-sizes]` (fixed by 04), and
  `[03-a-stale-egg-info-manifest-ships-the-tests-in-a-wheel]` (fixed by 05). None is open. The
  plan's fault 6 (the "available" rate in CPBH's and SI's copies) was never an issue here: the
  source already had the fix.
- **Decisions.** U1–U14, every one taken as recommended, U8 and U9 with amendments, U5 amended by
  U12 (README §6.2).
- **Deviations.** Every log classifies its deviations. A count of the three labels' words gives
  01: 1 / 8 / 1, 02: 0 / 7 / 1, 03: 2 / 5 / 1, 04: 0 / 10 / 1, 05: 2 / 10 / 2, 06: 4 / 9 / 2
  (STRUCTURALLY REQUIRED / IMPLEMENTATION CHOICE / UNINTENDED DRIFT). **A word is not an entry**:
  06's log, for one, classes fourteen deviations in one sentence. Count the entries yourself.
- **Observations not acted on**: each log has a section of them (01 §5, 02 §6, 03 §6, 04 §5, 05 §6,
  06 §9).
- **The equivalence check at `v0.1.0`.** `PROVENANCE.md`'s "Re-running the check" (a `git
  worktree` of `v0.1.0` in the scratchpad, run with `venv/`'s Python, removed after) exits 0 with
  `RESULT: OK`: 572 identical lines, 2 D-imp, 1 D-pool, 4 D-int, 12 declared files, 0 undeclared
  (04's last run; 05's and 06's reviews). It reads SGK through `git show` only.
- **The adoption checklists.** `docs/adoption/`'s figures (06): imports 7, 3, 3; call sites 54, 17,
  16, every one constructing under `v0.2.0`. Re-running `measure_client_pools.py` is optional; if
  run, its output must equal each checklist's appendix byte for byte.

---

## 2. What to write

### 2.1 `docs/extraction-verification.md`

A new file, named as DatastoreKit's. It is additive from the day it is committed (`CLAUDE.md`
rule 6). Its head names the campaign, the board, this prompt, the date, and the package it
verifies: `v0.2.0`, `eaef0ce`, and that `git diff eaef0ce -- raypoolkit pyproject.toml` is empty
at the commit that adds it.

| § | Section | What it holds |
|---|---|---|
| 1 | What this document is | What the campaign set out to do (README §0, §1, D1–D2), what it delivered, and the headline: two releases, the suite at both ends, the run under Ray, the checklists, no open issue, and what remains. |
| 2 | Reconciliation | **Git history:** a table of every prompt, its commit, review commit and note, the suite count after it, and what it closed or opened; every other commit on `main` from `3f1dfd4` to the commit before 07's, classed (plan, prompt written, note, review, release record). **Tags and CI**, as §1.3, each run linked. **The environment** of every measurement below. |
| 3 | Each prompt's acceptance, at `v0.2.0` | A table: the prompt; its acceptance in brief (README §2 and the prompt's own); what its review found; what holds at `v0.2.0`, with how it was re-measured here or why it cannot be. Re-measure here: the suite at both ends; the import guard (in the suite); `black`; the equivalence check at `v0.1.0`; the offline wheel (§1.2). |
| 4 | The package under Ray (U13) | §2.2's script: the command, the ends, every step's output, the timing, and Ray's processes before and after. The breakage (a)–(b), and the fault-1 probe (c) with what it shows (§1.1). |
| 5 | The release (U14) | The release record cited, step by step; the offline rebuild, with its entry list and size; that the four modules in it equal `eaef0ce`'s. |
| 6 | Issues | The eight resolved, one line each, with the prompt and commit that closed it and the test that guards it. None open. Fault 6, and why it was never an issue here. |
| 7 | Decisions | U1–U14, one line each: what was decided, when, for which prompt, and where it is applied (a commit, or "not applicable"). |
| 8 | Deviations across the campaign | A table of entry counts per log and class. Then every UNINTENDED DRIFT entry in one line each, with its log, and every STRUCTURALLY REQUIRED entry that changed what a prompt delivered. |
| 9 | Observations not acted on | Every item of every log's section, one line each, with its log, and its disposition at `v0.2.0`: addressed (by which prompt, review or decision), opened as an issue, still an observation, or no longer true. Decide from the later logs and the board, never by changing anything. |
| 10 | Known gaps | **G2–G4**: no client has adopted; the checklists are measured at commits that will move. **What remains unverified**: a multi-node cluster; a client's own suites under the package; Python 3.14 and Ray above 2.55.1, inside the declared range and untested (U7). **Fault 1 is guarded by the stand-in only** (§4). **DatastoreKit's README** still says `RayWorkPool` is not part of a package; that is DatastoreKit's to change (README §1). |
| 11 | Reproduction | Every command of §3–§5, verbatim, runnable from a clean checkout of the commit that adds this document. |
| 12 | Summary for the board | Five to ten lines. |

Every fact carries a commit, a `path:line` at a named tree, or a command and its output. A
statement of a log is cited by log and section. Where the document and a log disagree, the document
says which is right and why; it does not rewrite the log.

### 2.2 `docs/extraction/ray_smoke_run.py` (U13)

A script, not a test. The suite never collects it and stays free of Ray (`CLAUDE.md`). Write it in
the form of `docs/extraction/compare_with_source.py` and `docs/adoption/measure_client_pools.py`:
a module docstring saying what it is, how it is run and what it prints; `black`-clean.
- **How it is run:** from a checkout or an export, with the package importable, as
  `python docs/extraction/ray_smoke_run.py`. It imports `raypoolkit` and the three patterns from
  `raypoolkit.tests.test_printed_lines` (so it needs the tests in the tree, not an installed wheel),
  and otherwise only the standard library and `ray`. Its objects are its own, as §1.1's; it imports
  no stand-in and no client.
- **It starts Ray itself**, with §1.1's call, and calls `ray.shutdown()` in a `finally`. It refuses
  to run, exiting 2 before starting anything, if `ray.is_initialized()` is already true or `pgrep
  -lf 'gcs_server|raylet|ray::'` finds a process.
- **It prints** Python's, Ray's and `raypoolkit`'s versions (the last from `importlib.metadata`),
  and `raypoolkit.__file__`, so that a run shows which module it ran.
- **The steps are §1.1's five**, each isolated: an exception in a step is that step's `FAIL`, with
  its type and message, and the next step runs. Each prints `PASS` or `FAIL` with what it saw.
  Step 5 captures stdout and prints the lines it matched.
- **Its exit code** is 0 only if every step passes, 1 if one fails.
- **Every value it asserts is the script's own**: counts and orders it built, never a figure read
  from a log.

### 2.3 The release (U14)

As §1.2: rebuild the wheel offline from `git archive v0.2.0`, in a fresh scratch directory, with
the build log captured and searched for "absent from"; list its entries; compare its four modules
with `git show eaef0ce:raypoolkit/<module>`. **No network**: no `git fetch`, no install from
GitHub, every `uv` call `--offline`. Nothing of it is committed.

### 2.4 Closing the campaign

- **The board.**
  - Its header says **CLOSED** (2026-10-10, by prompt 07), with all seven prompts landed.
  - §1's row for 07.
  - §2's gates are unchanged: G2–G4 have not held, and the campaign does not wait for them (README
    §7). Add a dated line under §2: after the close, a gate is recorded on this board when it
    holds, in a records commit of its own.
- **The campaign README.** Its header, §2's row for 07, and a dated line under §7: the campaign
  closed at 07, with G2–G4 open.
- **`prompts/INDEX.md`**: the campaign's line, **closed**, with its open-issue count.
- **`docs/OPEN_ISSUES.md`**: the header's date; §1.1's heading says the campaign is closed. Its
  count changes only if 07 opens an issue.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Ray is started only by the script**, once per run, and stopped by it; the one exception is
   §4.5 (d), whose Ray is started and stopped in a session of your own. Before and after every
   run, `pgrep -lf 'gcs_server|raylet|ray::'` is recorded, each process attributed by its path. If
   one is up before a run, find whose it is: if it is this repository's or this session's, stop
   and ask; if another session's, do not touch it, do not run, and ask. Never `ray start`, never
   pass `address=`, and never run the suite while Ray is up.
2. **No network** (U14). Every venv and install is `uv … --offline`, from the cache. `git fetch`,
   `git push` and any install from a URL are not run. Reading GitHub's state with `gh run view`
   is allowed, to cite a run; nothing is written to GitHub.
3. **The package does not change.** `git diff 71f0d66 -- raypoolkit pyproject.toml README.md
   PROVENANCE.md docs/adoption` is empty at the end. A finding is recorded, not fixed (rule 4).
   The breakage edits scratch exports only.
4. **Additive documents.** Under `docs/`, 07 adds two files and changes only
   `docs/OPEN_ISSUES.md`.
5. **No client is touched.** SGK is read only through `git show`, by `compare_with_source.py` at
   `v0.1.0` (and, if run, `measure_client_pools.py`). No client is written, run, imported or
   opened; no `.db` file is opened.
6. **The suite runs with no Ray up.** Run it in `venv/` and at the high end before the smoke runs,
   and in `venv/` again at the end.
7. **The document is long.** Its tables are built from the records, never from memory. Each count
   it states is one you counted, and the log says how.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 121 tests … OK` before and after. At the high end, in a fresh
   offline scratch venv (3.13.16, `ray==2.55.1`, a `git archive` of your tree installed editable):
   `Ran 121 tests … OK`.
2. **The checks.**
   - `./venv/bin/black --check raypoolkit docs` (25.1.0) leaves **17** files unchanged (16 and the
     script).
   - `compare_with_source.py` at `v0.1.0`, as §1.3, the worktree removed after.
3. **The smoke run** at both ends, each from a fresh offline scratch venv with an export of your
   tree installed editable (low: `/opt/local/bin/python3.12`, `ray==2.43.0`; high:
   `/opt/local/bin/python3.13`, `ray==2.55.1`). The script exits 0. Record its whole output, its
   time, and Ray's processes before and after.
4. **The release**, as §2.3.
5. **The breakage record.** Each item is a diff exactly as applied, to `raypoolkit/RayWorkPool.py`
   in a fresh scratch export at the high end, never to the repository. Check each with `git apply
   --check` and, once applied, `-R --check`.
   - **(a)** fault 2's fix reverted at `:530`: step 3 fails, naming the `None` `store_id`s; the
     other steps pass.
   - **(b)** fault 3's fix reverted at `:178`: step 1 fails with `TypeError`; the other steps run
     and pass (the step isolation of §2.2).
   - **(c)**, a probe, not a breakage: fault 1's fix reverted (the 26 `.hex()` → `.hex`): every
     step passes. Record it as §1.1 says, in the document's §4 and §10.
   - **(d)** the script with Ray already up: start `ray.init(...)` in a Python session of your own,
     run the script, and it exits 2 before starting Ray; then shut your session's Ray down and
     confirm no process is left.
6. **The documents.**
   - Every relative link and anchor in `docs/extraction-verification.md` resolves, checked by a
     scratch script as 06's review did; every external link is to `github.com/ds283/…` and names
     a tag, a commit or a run.
   - Every `path:line` the document cites at `v0.2.0` is read at `eaef0ce`.
   - Every count it states is recounted, and the log says how.
7. **The clients.** Record each client's `HEAD`, `git status --porcelain | shasum` and `git stash
   list | wc -l`, at the start and the end, unchanged.

---

## 5. Acceptance

1. `docs/extraction-verification.md` holds §2.1's twelve sections, and every fact in it carries its
   source.
2. `docs/extraction/ray_smoke_run.py` exits 0 at both ends under real Ray, leaves no Ray process,
   and (a), (b) and (d) fail as §4.5 says.
3. The offline wheel from `v0.2.0` has the 9 entries, and its four modules are `eaef0ce`'s.
4. The campaign is closed on the board, in the README, in `prompts/INDEX.md` and in the index.
5. §4.1–§4.7 hold.
6. **The records**, in the same commit:
   - the log, `logs/07-verification-and-close-out.md`, per README §5.1. In place of
     `compare_with_source.py`'s output it has:
     - the suite at both ends, by module;
     - `compare_with_source.py` at `v0.1.0`, whole;
     - the smoke runs, whole, with Ray's processes before and after each;
     - the offline wheel;
     - (a)–(d);
     - the documents' checks, and how each count was made;
     - the clients' states, at the start and the end;
   - the board, as §2.4;
   - `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` and the campaign README, as §2.4.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 121, in any venv.
- The smoke script fails at either end. A defect found is opened, not fixed; stop before writing it
  up, and report.
- The offline wheel differs from §1.2.
- A Ray process is up before a run, or is left after one.
- Anything would change a file under `raypoolkit/`, `pyproject.toml`, `README.md`,
  `PROVENANCE.md`, `docs/adoption/`, the other scripts of `docs/extraction/`, the workflow, or any
  file not in §7.
- Anything would push, make or move a tag, connect to a Ray cluster, use the network, or write,
  run, import or open anything of a client or of DatastoreKit.

---

## 7. What this prompt changes, and what it does not

- **Files it adds:** `docs/extraction-verification.md`, `docs/extraction/ray_smoke_run.py` and the
  log.
- **Files it changes:** `docs/OPEN_ISSUES.md`; the board, the campaign README (its header, §2's
  row for 07 and §7's line), and `prompts/INDEX.md`.
- **It changes nothing else:** no file under `raypoolkit/`; not `pyproject.toml`, `README.md`,
  `PROVENANCE.md`, `docs/adoption/`, `docs/extraction/compare_with_source.py` or the workflow; not
  `CLAUDE.md`, `LICENSE` or `.gitignore`.
- **It touches no client repository, and not DatastoreKit**, beyond reading through `git`.
- **It makes no tag, pushes nothing, and uses no network.**

---

## 8. The log and the board

`logs/07-verification-and-close-out.md`, using README §5.1, with §5 item 6's additions.

`IMPLEMENTATION_STATE.md`: the header (**CLOSED**), §1's row for 07, and §2's dated line.
