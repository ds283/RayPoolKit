# Prompt 03a — correct two clauses of the contract

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 03 landed (`89d6875`) and was reviewed (`b4edd2c`). The review opened
  `[03-the-contract-overstates-two-edges-of-the-module]` (the board's §3), and `v0.3.0` is not
  tagged.
- `git status` is clean in this repository, and the suite gives `Ran 226 tests … OK`.

**Closes:** `[03-the-contract-overstates-two-edges-of-the-module]` · **Narrows:** nothing ·
**Opens:** only what the work finds.

**Recommended model:** **Opus.** The edit is two clauses. They have to say exactly what the module
does, in a document three projects keep, and the tag will stand on this commit.

**Read first:**
1. The board: the *Orchestrator review of prompt 03* (check 6) and the issue in §3.
2. [`../../docs/rehearsal-lock.md`](../../docs/rehearsal-lock.md) whole, above all §4 ("The argument
   rules") and §6 (the rule and "What it asks of a caller").
3. `raypoolkit/rehearsal_lock.py`: `_check_ray_temp_dir` (`:126-135`), `_temp_dir_pattern`
   (`:307-312`) and `ray_processes` (`:331-392`), the ancestor walk at `:374-379` above all.
4. `logs/03-release-v0.3.0.md` §3.5, rows S25, S43 and S46, and §3.9 (how 03's probes were run).
5. README §5, rules 4, 6 and 10, and `CLAUDE.md`'s rule 6 ("Verification documents are additive").

Facts below are at `b4edd2c`, measured by the orchestrator on 2026-10-24.

---

## 1. What is wanted

`docs/rehearsal-lock.md` says nothing that is untrue of `raypoolkit.rehearsal_lock`. Two clauses,
found by 03's review, say more than the module does. Correct each, and add to "What it asks of a
caller" what each now means for a caller. Change nothing under `raypoolkit/`.

After this prompt, `v0.3.0` is tagged on **03a's commit**, not 03's, once CI passes there (README §5
rule 10). Their trees differ only in `docs/` and `prompts/`, neither of which reaches the wheel.

---

## 2. What to change

### 2.1 §4, the `ray_temp_dir` rule

**Now** (`docs/rehearsal-lock.md:99-100`): "`ray_temp_dir` is an absolute path in normal form
(`os.path.normpath` leaves it as it is, so no trailing `/`, `.`, `..` or `//`), and never
`in-process`."

**What the module does.** POSIX's `os.path.normpath` keeps a leading `//`, so a temp dir that
starts with exactly two slashes passes. Measured, `_check_ray_temp_dir`:
- accepts `//tmp/ray-a`;
- refuses `/tmp//ray-a`, `///tmp/ray-a` and `/tmp/ray-a/`.

The rule then matches the spelling it was given:
- for `D` = `//tmp/ray-a`, a command naming `/tmp/ray-a/…` is **not** a seed, and one naming
  `//tmp/ray-a/…` is;
- for `D` = `/tmp/ray-a`, both are seeds, since there is no leading boundary.

Measured on a fixed table with `self_pid=-1`: `[41]` against `[40, 41]`.

**Make it say:**
- normal form is what `os.path.normpath` leaves unchanged: no trailing `/`, no `.` or `..`
  component, and no doubled `/` except a leading `//`, which POSIX keeps and the check accepts;
- in "What it asks of a caller", next to the advice on keeping the temp dir short: **never start
  it with `//`.** The rule matches the spelling given, so a process that names the same directory
  as `/tmp/…` would not be listed. That is the unsafe side.

### 2.2 §6 item 4, the processes never listed

**Now** (`:141-143`): "**This process is never listed**: the process reading the table, its
ancestors, and its own descendants. They still seed the walk, so if an ancestor's command names
`D`, its other descendants are listed."

**What the module does.** The walk up from the reading process stops before pid 1
(`while pid in table and pid not in safe and pid > 1`), so pid 1 is never in the set kept out of
the listing. Pid 1 is listed whenever its command names `D`. Every process descends from pid 1, so
every one is then listed, bar the reading process, its other ancestors and its own descendants.
Measured on a fixed table:
- with pid 1's command `/init --temp-dir=/tmp/ray-a`, an ancestor of the reader (pid 20, under a
  shell, pid 10), and an unrelated `sshd` (30) with a child (31): `[1, 30, 31]`;
- with pid 1 naming another directory: `[]`.

**Make it say:** never listed are the reading process, its ancestors **other than pid 1**, and its
own descendants. Pid 1 is listed if its command names `D`, and then so is every process outside
that set. This over-lists, the safe side: `acquire` refuses with 4 and `release` with 1. On macOS
pid 1 is `launchd`, whose command names no temp dir.

### 2.3 Nothing else in the document

Read the whole document again for any other sentence that repeats either claim, and correct it the
same way. The orchestrator found none: §6's later mention of ancestors (`:166-170`) is true as
written. The opening's statement that every statement is checked stays. It points at 03's
log, so add "and 03a's" with a link.

The module's own docstrings make the same pid 1 claim (`rehearsal_lock.py:63-64`, `:345-347`), and
so does `PROVENANCE.md:102`, which follows the docstring. They are not changed here: the first is
under `raypoolkit/`, and the second describes what was taken from the model. Record both under
"Observations not acted on".

---

## 3. Verification

1. **The suite.** `venv/`: `Ran 226 tests … OK`, before and after. `./venv/bin/black --check
   raypoolkit docs`: 20 files unchanged.
2. **Nothing reaches the wheel.** `git diff 89d6875 HEAD -- raypoolkit pyproject.toml` is empty
   after your commit. No wheel need be built.
3. **The probes.** Write each as a script in your scratch directory and run it with `venv/`'s
   interpreter from an empty directory with `-I`. Use fixed tables (`ps_text`, `self_pid`) only,
   with no real `ps`, no lock and no Ray. Record each script and its output in the log:
   - **(P-a)** `_check_ray_temp_dir` on `//tmp/ray-a`, `/tmp//ray-a`, `///tmp/ray-a` and
     `/tmp/ray-a/`: one accepted, three refused. Then `ray_processes` for both spellings of `D`
     over one table holding a `/tmp/ray-a` seed and a `//tmp/ray-a` seed, as §2.1.
   - **(P-b)** `ray_processes` over §2.2's table, with pid 1 naming `D` and then naming another
     directory, as §2.2.

   Each probe must be able to fail: its expected output differs from what the old clause would
   predict. Show it beside the actual result.
4. **The statements.** In the log, add rows **S25′** and **S43′**, each with its probe, and a row
   for each new sentence in "What it asks of a caller". Leave 03's log as it is (rule 6). Every
   relative link in `docs/rehearsal-lock.md` resolves to a tracked file.
5. **No client named.** `grep -n -i -E 'secondary|sgk|champbh|cpbh|stochastic|instanton'
   docs/rehearsal-lock.md` finds nothing.
6. **The real `HOME` and Ray.** `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` are absent
   before and after, and `pgrep -lf 'gcs_server|raylet|ray::'` finds nothing.

**Deliberate breakage.** No test changes, so there is no mutation to catch. Verification 3's
contrast between the old clause's prediction and the module's output stands in for it. Record it
in the log's breakage section.

---

## 4. Acceptance

1. §2.1's and §2.2's corrections are in `docs/rehearsal-lock.md`, with their caller advice, and
   §2.3's reading is recorded.
2. Verification 1–6 pass.
3. **The records**, in the same commit:
   - the log, `logs/03a-correct-two-clauses-of-the-contract.md`, per README §5.1;
   - the board:
     - the header, saying that `v0.3.0` is ready to be tagged on 03a's commit once CI passes
       there, and that no tag was made;
     - §1's row for 03a (landed, "this commit", 226 → 226);
     - the issue moved from §3 to §4, with a dated **Resolved (03a)** line naming the two clauses
       and the probes;
   - `docs/OPEN_ISSUES.md`: the issue's row deleted, the count back to **0**, and the date;
   - `prompts/INDEX.md`: the campaign's line, with its open-issue count at 0.

---

## 5. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 226.
- A probe gives other than §2's measurements.
- Making the document true would need a change to a file under `raypoolkit/`, or to any file not
  in §6.
- Anything would push, make or move a tag, start Ray, touch either lock location under the real
  `HOME`, or edit or run a client.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `docs/rehearsal-lock.md`;
  - the log, the board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- It changes nothing else:
  - not `raypoolkit/` (the docstrings included), `pyproject.toml`, `README.md`, `PROVENANCE.md`
    or `CLAUDE.md`;
  - not 03's log, the campaign README, or anything under `orchestrator/` or `planning/`.
- It adds no test, and builds no wheel.
- It makes no tag and pushes nothing.
