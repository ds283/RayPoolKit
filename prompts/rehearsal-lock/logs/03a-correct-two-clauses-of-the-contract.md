# Log — rehearsal-lock prompt 03a: correct two clauses of the contract

**Subject:** Correct two clauses of the rehearsal lock's contract · **Commit:** this commit ·
**Date:** 2026-10-24 · **Agent:** Claude Opus 5.5

**Result: landed; `v0.3.0` is ready to be tagged on this commit once CI passes here. No tag was
made, and nothing was pushed.**
- `docs/rehearsal-lock.md` says what the module does at the two edges 03's review found: §4's
  `ray_temp_dir` rule admits a leading `//`, and §6 item 4 keeps pid 1 out of the set never listed.
  "What it asks of a caller" gains one sentence for each: never start the temp dir with `//`, and
  never use a temp dir that pid 1's command names. The opening points at this log beside 03's.
- Each correction rests on a probe against a fixed table, P-a and P-b (§3.3), whose expected output
  differs from what the old clause predicts. Both pass.
- The suite is **226 → 226**, `OK` in `venv/`. `black --check raypoolkit docs`: 20 files unchanged.
- **One issue closed**, `[03-the-contract-overstates-two-edges-of-the-module]`; none opened. The
  index goes from 1 to **0**.
- Nothing under `raypoolkit/` changed, nor `pyproject.toml`, `README.md`, `PROVENANCE.md`,
  `CLAUDE.md`, 03's log or the campaign README. No Ray was started. Neither lock location under the
  real `HOME` was touched. No client was edited or run.

**Gate, re-checked at start (19:24).**
- `HEAD` was `b2ee2b3` (the prompt), on `b4edd2c` (03's review) and `89d6875` (03). The tree was
  clean, and this checkout was the only worktree. Tags `v0.1.0` and `v0.2.0`; `origin/main`
  `cc5f2d6`.
- `venv/`: `Ran 226 tests in 2.320s` `OK`. `./venv/bin/black --check raypoolkit docs`: "20 files
  would be left unchanged."
- No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` exit 1).
- `~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` did not exist.
- The board's §3 held the one issue, and `docs/OPEN_ISSUES.md` said **1 open**.

Every scratch file of this log is under the agent's scratch directory,
`…/scratchpad/agent03a/`, written `$S` below: the scripts in `$S/scripts/`, their outputs in
`$S/out/`, and the empty directory they ran from, `$S/empty/`.

## 1. What shipped

| File | What |
|---|---|
| `docs/rehearsal-lock.md` | the opening's pointer to this log; §4's `ray_temp_dir` bullet; §6 item 4 and its sub-item on pid 1; two sentences in §6's "What it asks of a caller" |
| this log, the board, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

**The two clauses, as corrected.**

§4, the argument rules (was: "`ray_temp_dir` is an absolute path in normal form (`os.path.normpath`
leaves it as it is, so no trailing `/`, `.`, `..` or `//`), and never `in-process`."):

> - `ray_temp_dir` is an absolute path in normal form, and never `in-process`. Normal form is what
>   `os.path.normpath` leaves unchanged: no trailing `/`, no `.` or `..` component, and no doubled
>   `/`, except a leading `//`, which POSIX keeps and the check accepts. So `//tmp/ray-a` passes,
>   and `/tmp//ray-a`, `///tmp/ray-a` and `/tmp/ray-a/` do not. The process rule then matches the
>   leading `//` as spelled (§6, "What it asks of a caller").

§6 item 4 (was: "**This process is never listed**: the process reading the table, its ancestors,
and its own descendants. They still seed the walk, so if an ancestor's command names `D`, its other
descendants are listed."):

> 4. **This process is never listed**: the process reading the table, its ancestors other than
>    pid 1, and its own descendants. They still seed the walk, so if an ancestor's command names
>    `D`, its other descendants are listed.
>    - Pid 1 is listed if its command names `D`, and then so is every descendant of pid 1 outside
>      that set, which is almost every process. This over-lists, the safe side: `acquire` refuses
>      with 4 and `release` with 1. On macOS pid 1 is `launchd`, whose command names no temp dir.

**The caller sentences**, in §6's "What it asks of a caller". After "Keep the temp dir short":

> - **Never start the temp dir with `//`.** The check accepts a leading `//` (§4), and the rule
>   matches the spelling given: for `//tmp/ray-a`, a command naming `//tmp/ray-a/…` is a seed and
>   one naming `/tmp/ray-a/…` is not. So a process that names the same directory as `/tmp/…` would
>   not be listed. That is the unsafe side.

Last in the list:

> - **Never use a temp dir that pid 1's command names.** Pid 1 is not kept out of the listing (§6
>   item 4), so it and almost every other process would be listed, and `acquire` and `release`
>   would refuse for as long as pid 1 runs.

**The opening** now ends: "… in the log of the prompt that wrote this document, [03's log], and in
03a's, which corrected two of its clauses, [this log]."

**The reading of the whole document (prompt §2.3).** Read through again, with `rehearsal_lock.py`
beside it, for any other sentence that repeats either claim. None does:
- §2's "a driver cannot see its own in-process instance that way (§6)" and §6's driver paragraph
  ("The rule never lists the descendants of the process reading the table") are about the reading
  process's descendants, which the walk does keep out (`_closure({self_pid}, children)`).
- §6's "Any process whose command names the temp dir is listed … If such a process is an ancestor
  of the lock command, its other descendants are listed too" (`:166-170` at `89d6875`) is true as
  written, pid 1 included.
- §5's "`/private/tmp/ray-q` and `/tmp/ray-q` are one temp dir to the process rule" names spellings
  without a leading `//`, and is true.
- §4's other bullets, §6 items 1–3 and §10's "It cannot see some processes" make neither claim.

`README.md`, `PROVENANCE.md` and `CLAUDE.md` were grepped too (`ancestor`, `normal form`,
`normpath`, `pid 1`, `launchd`): only `PROVENANCE.md:102` repeats the pid 1 claim, and it is left
as the prompt says (§5, observation 2).

## 2. Deviations from the prompt

1. **"Every descendant of pid 1 outside that set, which is almost every process"**, where the
   prompt's §2.2 says "then so is every process outside that set". **STRUCTURALLY REQUIRED.** The
   module lists the descendants of the seeds less the set (`_closure(seeds, children) - safe`), and
   not every process descends from pid 1: on Linux, `kthreadd` is pid 2 with ppid 0, and the kernel
   threads are its children. Probe P-c (1), on such a table with pid 1 naming `D`, gives `[1, 30]`:
   pid 2 and its thread are not listed. The prompt's wording would be untrue of the module there,
   which §1 forbids. On macOS every process `ps -ax` shows descends from `launchd`, so the prompt's
   measurement `[1, 30, 31]` stands.
2. **Pid 1 as a sub-item of §6 item 4**, not a further sentence of the item. IMPLEMENTATION CHOICE:
   the item keeps its form, and the exception reads as one.
3. **The pid 1 caller sentence is this agent's wording.** The prompt's §1 asks for what each
   correction means for a caller, and its §2.2 gives the clause but no caller sentence. "Never use
   a temp dir that pid 1's command names" is what the clause implies: pid 1 runs as long as the
   machine (or container), so the lock could be neither taken nor released. Placed last, beside the
   advice on processes whose command names the temp dir. IMPLEMENTATION CHOICE.
4. **The `//` advice is a bullet of its own** after "Keep the temp dir short", in bold like its
   neighbours, rather than a sentence inside that bullet. IMPLEMENTATION CHOICE: the short-path
   bullet is about the socket limit and `/`; this one is a separate rule.
5. **§4's bullet gives the four measured spellings** (`//tmp/ray-a` passes; `/tmp//ray-a`,
   `///tmp/ray-a`, `/tmp/ray-a/` do not) and points at §6 for what the rule then does.
   IMPLEMENTATION CHOICE: "no doubled `/` except a leading `//`" alone could be read as admitting
   `///`, which `normpath` collapses to `/` and the check refuses.
6. **A third probe, P-c**, beyond the prompt's P-a and P-b, run the same way: (1) the Linux-shaped
   table of deviation 1; (2) a `//private/…` temp dir (observation 3); (3) the reader being pid 1
   itself. It checks the wording chosen, and no statement of the prompt's §2 rests on it.
   IMPLEMENTATION CHOICE.
7. **The new caller sentences are rows S46a and S50a** of §3.4, numbered beside the rows they follow
   in 03's numbering, so that 03's S1–S98 keep their numbers. IMPLEMENTATION CHOICE.
8. **`prompts/INDEX.md`'s count of prompts written** is corrected with the campaign's line, from "3
   of 5 written" to "4 of 6", with 03a named, as the board's header has had it since 03a was
   written (`b2ee2b3`). IMPLEMENTATION CHOICE: the line is the one this prompt updates.

No UNINTENDED DRIFT was found.

## 3. Verification performed

### 3.1 The suite (prompt §3.1)

| When | Command | Result |
|---|---|---|
| before (19:24, `b2ee2b3`) | `./venv/bin/python -m unittest discover -s raypoolkit/tests -t .` | `Ran 226 tests in 2.320s` `OK` |
| after, the files staged (19:29) | the same | `Ran 226 tests in 2.113s` `OK` |

`./venv/bin/black --check raypoolkit docs`: "20 files would be left unchanged", before and after.
`black` reads no Markdown, so the count is unchanged by this prompt's files.

**226 → 226.** No test was added or changed.

### 3.2 Nothing reaches the wheel (prompt §3.2)

`git diff 89d6875 HEAD -- raypoolkit pyproject.toml`, after this commit: empty (§3.7). No wheel was
built.

### 3.3 The probes (prompt §3.3)

Each ran in `venv/` (3.12.15 / Ray 2.43.0), from the empty `$S/empty`, as `env -u PYTHONPATH
…/venv/bin/python -I $S/scripts/probe_<x>.py`, on fixed text passed as `ps_text` with an explicit
`self_pid`. No probe reads the real `ps`, takes a lock or starts Ray. Each prints `module:
…/raypoolkit/rehearsal_lock.py`, the checkout's (the editable install of `venv/`), and exits 0
with every line PASS; `$S/empty` was still empty after.

| Script | SHA-256 |
|---|---|
| `probe_a.py` | `9c54f0d2f7004114526f02eaa3c49e4b2098cdc0952b9198544bcb4e76356fa8` |
| `probe_b.py` | `323b500b3a385015648e61606a4c6e297cab282510c256d517005a01d2904267` |
| `probe_c.py` | `25cc14e5ba996dc8d2207a874dffdf39d33067d16f6cc8a24196f870301d7054` |

**(P-a) `probe_a.py`: a leading `//`.**

```python
"""P-a: a leading // passes the ray_temp_dir check, and the rule matches the spelling given."""

import os

from raypoolkit import rehearsal_lock as rl

print("module:", rl.__file__)
fails = 0


print("-- _check_ray_temp_dir (old clause: no '//' at all, so all four refused)")
expected = {"//tmp/ray-a": "accepted", "/tmp//ray-a": "refused", "///tmp/ray-a": "refused", "/tmp/ray-a/": "refused"}
for value, want in expected.items():
    try:
        rl._check_ray_temp_dir(value)
        got = "accepted"
    except ValueError as exc:
        got = f"refused (ValueError: {exc})"
    tag = "PASS" if got.startswith(want) else "FAIL"
    fails += tag == "FAIL"
    print(f"{tag}  {value!r:16} normpath={os.path.normpath(value)!r:14} old: refused   module: {got}")

TABLE = """\
    1     0 /sbin/launchd
   40     1 python worker.py --temp-dir=/tmp/ray-a/session_x
   41     1 python worker.py --temp-dir=//tmp/ray-a/session_x
"""
print("-- the table (self_pid=-1, in no row)")
print(TABLE, end="")


def listing(d):
    try:
        return [p for p, _, _ in rl.ray_processes(d, ps_text=TABLE, self_pid=-1)]
    except ValueError as exc:
        return f"ValueError: {exc}"


got = listing("//tmp/ray-a")
tag = "PASS" if got == [41] else "FAIL"
fails += tag == "FAIL"
print(f"{tag}  D='//tmp/ray-a'  old: ValueError (not normal form)   module: {got}   expected [41]")
got = listing("/tmp/ray-a")
tag = "PASS" if got == [40, 41] else "FAIL"
fails += tag == "FAIL"
print(f"{tag}  D='/tmp/ray-a'   old: [40, 41]                         module: {got}   expected [40, 41]")
print("RESULT:", "PASS" if not fails else f"FAIL ({fails})")
raise SystemExit(1 if fails else 0)
```

Its output, `$S/out/probe_a.txt` (`module:` path shortened):

```text
module: …/RayPoolKit/raypoolkit/rehearsal_lock.py
-- _check_ray_temp_dir (old clause: no '//' at all, so all four refused)
PASS  '//tmp/ray-a'    normpath='//tmp/ray-a'  old: refused   module: accepted
PASS  '/tmp//ray-a'    normpath='/tmp/ray-a'   old: refused   module: refused (ValueError: ray_temp_dir must be in normal form ('/tmp/ray-a'), not '/tmp//ray-a')
PASS  '///tmp/ray-a'   normpath='/tmp/ray-a'   old: refused   module: refused (ValueError: ray_temp_dir must be in normal form ('/tmp/ray-a'), not '///tmp/ray-a')
PASS  '/tmp/ray-a/'    normpath='/tmp/ray-a'   old: refused   module: refused (ValueError: ray_temp_dir must be in normal form ('/tmp/ray-a'), not '/tmp/ray-a/')
-- the table (self_pid=-1, in no row)
    1     0 /sbin/launchd
   40     1 python worker.py --temp-dir=/tmp/ray-a/session_x
   41     1 python worker.py --temp-dir=//tmp/ray-a/session_x
PASS  D='//tmp/ray-a'  old: ValueError (not normal form)   module: [41]   expected [41]
PASS  D='/tmp/ray-a'   old: [40, 41]                         module: [40, 41]   expected [40, 41]
RESULT: PASS
```

The old clause predicts four refusals and, for `D` = `//tmp/ray-a`, a `ValueError`; the module
accepts `//tmp/ray-a` and lists `[41]`. For `D` = `/tmp/ray-a` both give `[40, 41]`. This is the
prompt's §2.1 measurement exactly.

**(P-b) `probe_b.py`: pid 1.**

```python
"""P-b: pid 1 is not kept out of the listing."""

from raypoolkit import rehearsal_lock as rl

print("module:", rl.__file__)
fails = 0


def run(label, table, self_pid, old, want):
    global fails
    got = [p for p, _, _ in rl.ray_processes("/tmp/ray-a", ps_text=table, self_pid=self_pid)]
    tag = "PASS" if got == want else "FAIL"
    fails += tag == "FAIL"
    print(f"-- {label} (D='/tmp/ray-a', self_pid={self_pid})")
    print(table, end="")
    print(f"{tag}  old clause predicts: {old}   module: {got}   expected {want}")


T1 = """\
    1     0 /init --temp-dir=/tmp/ray-a
   10     1 -bash
   20    10 python -m raypoolkit.rehearsal_lock ray-processes
   30     1 /usr/sbin/sshd
   31    30 sshd: someone@pts/0
"""
T2 = T1.replace("/init --temp-dir=/tmp/ray-a", "/init --temp-dir=/tmp/ray-b")
run("pid 1 names D", T1, 20, [30, 31], [1, 30, 31])
run("pid 1 names another directory", T2, 20, [], [])
print("RESULT:", "PASS" if not fails else f"FAIL ({fails})")
raise SystemExit(1 if fails else 0)
```

Its output, `$S/out/probe_b.txt`:

```text
module: …/RayPoolKit/raypoolkit/rehearsal_lock.py
-- pid 1 names D (D='/tmp/ray-a', self_pid=20)
    1     0 /init --temp-dir=/tmp/ray-a
   10     1 -bash
   20    10 python -m raypoolkit.rehearsal_lock ray-processes
   30     1 /usr/sbin/sshd
   31    30 sshd: someone@pts/0
PASS  old clause predicts: [30, 31]   module: [1, 30, 31]   expected [1, 30, 31]
-- pid 1 names another directory (D='/tmp/ray-a', self_pid=20)
    1     0 /init --temp-dir=/tmp/ray-b
   10     1 -bash
   20    10 python -m raypoolkit.rehearsal_lock ray-processes
   30     1 /usr/sbin/sshd
   31    30 sshd: someone@pts/0
PASS  old clause predicts: []   module: []   expected []
RESULT: PASS
```

The old clause keeps every ancestor of the reader (20) out, pid 1 among them, while pid 1 still
seeds the walk: `[30, 31]`. The module gives `[1, 30, 31]`. With pid 1 naming another directory,
both give `[]`, the control. This is the prompt's §2.2 measurement exactly.

**(P-c) `probe_c.py`: the wording chosen** (deviations 1 and 6).

```python
"""P-c: two edges behind the wording chosen. Not a statement of the prompt's §2."""

from raypoolkit import rehearsal_lock as rl

print("module:", rl.__file__)
fails = 0

# (1) A process whose ppids do not reach pid 1 (Linux's kthreadd, pid 2, ppid 0, and a kernel
# thread under it) is not listed when pid 1 names D: "every descendant of pid 1", not "every process".
T = """\
    1     0 /init --temp-dir=/tmp/ray-a
    2     0 [kthreadd]
    3     2 [rcu_gp]
   10     1 -bash
   20    10 python -m raypoolkit.rehearsal_lock ray-processes
   30     1 /usr/sbin/sshd
"""
got = [p for p, _, _ in rl.ray_processes("/tmp/ray-a", ps_text=T, self_pid=20)]
want = [1, 30]
tag = "PASS" if got == want else "FAIL"
fails += tag == "FAIL"
print(T, end="")
print(f"{tag}  (1) pid 1 names D, kthreadd outside its tree: module {got}, expected {want}")

# (2) /private is stripped only from a D that starts '/private/'; '//private/...' is matched as given.
T2 = """\
    1     0 /sbin/launchd
   50     1 x --temp-dir=/tmp/ray-a/s
   51     1 x --temp-dir=/private/tmp/ray-a/s
   52     1 x --temp-dir=//private/tmp/ray-a/s
"""
print(T2, end="")
for d, want in [("/private/tmp/ray-a", [50, 51, 52]), ("//private/tmp/ray-a", [52])]:
    got = [p for p, _, _ in rl.ray_processes(d, ps_text=T2, self_pid=-1)]
    tag = "PASS" if got == want else "FAIL"
    fails += tag == "FAIL"
    print(f"{tag}  (2) D={d!r}: module {got}, expected {want}")

# (3) The reader is pid 1 itself: never listed (it is the reading process, not an ancestor).
got = [p for p, _, _ in rl.ray_processes("/tmp/ray-a", ps_text=T, self_pid=1)]
want = []
tag = "PASS" if got == want else "FAIL"
fails += tag == "FAIL"
print(f"{tag}  (3) self_pid=1 over the first table: module {got}, expected {want}")
print("RESULT:", "PASS" if not fails else f"FAIL ({fails})")
raise SystemExit(1 if fails else 0)
```

Its output, `$S/out/probe_c.txt`:

```text
module: …/RayPoolKit/raypoolkit/rehearsal_lock.py
    1     0 /init --temp-dir=/tmp/ray-a
    2     0 [kthreadd]
    3     2 [rcu_gp]
   10     1 -bash
   20    10 python -m raypoolkit.rehearsal_lock ray-processes
   30     1 /usr/sbin/sshd
PASS  (1) pid 1 names D, kthreadd outside its tree: module [1, 30], expected [1, 30]
    1     0 /sbin/launchd
   50     1 x --temp-dir=/tmp/ray-a/s
   51     1 x --temp-dir=/private/tmp/ray-a/s
   52     1 x --temp-dir=//private/tmp/ray-a/s
PASS  (2) D='/private/tmp/ray-a': module [50, 51, 52], expected [50, 51, 52]
PASS  (2) D='//private/tmp/ray-a': module [52], expected [52]
PASS  (3) self_pid=1 over the first table: module [], expected []
RESULT: PASS
```

(1): "every process outside that set" would predict `[1, 2, 3, 30]`; the module gives `[1, 30]`.
(3): with the reader pid 1, its own descendants are kept out, so nothing is listed; the corrected
clause ("the process reading the table … and its own descendants") says so.

### 3.4 The statements (prompt §3.4)

Rows superseding 03's S25 and S43 (03's log is left as it is, rule 6), and one row for each new
sentence in "What it asks of a caller". Tests are in `raypoolkit/tests/test_rehearsal_lock.py`.

| # | Statement | Checked by |
|---|---|---|
| S25′ | `ray_temp_dir`: absolute, never `in-process`, in normal form, which is what `normpath` leaves unchanged; a leading `//` kept and accepted; `//tmp/ray-a` passes, `/tmp//ray-a`, `///tmp/ray-a`, `/tmp/ray-a/` do not; the rule then matches the `//` as spelled | P-a (the four spellings, and `[41]` against `[40, 41]`); `test_ray_temp_dir_must_be_absolute_normal_and_not_in_process` (`BAD_TEMP_DIRS`: `/tmp/ray-a/`, `/tmp//ray-a`, `/tmp/../tmp/ray-a`, `/tmp/./ray-a`, a relative path, `in-process`) |
| S43′ | never listed: the reader, its ancestors other than pid 1, its own descendants; they seed the walk; pid 1 listed if it names `D`, and then every descendant of pid 1 outside that set; `acquire` 4, `release` 1; on macOS pid 1 is `launchd` | P-b (`[1, 30, 31]`; the control `[]`); P-c (1) and (3); `test_this_process_its_ancestors_and_its_children_are_never_listed`; `test_an_ancestor_naming_the_temp_dir_seeds_its_other_children`; for 4 and 1, any listed process: `test_processes_of_the_temp_dir_return_4_and_leave_no_lock`, `test_a_process_of_the_temp_dir_is_refused_with_pid_dash`; `launchd`: [02's log](02-prove-it-under-real-ray.md) deviation 14 (`/sbin/launchd` pid 1, ppid 0, measured 2026-10-24) |
| S46a | never start the temp dir with `//`: for `//tmp/ray-a`, `//tmp/ray-a/…` is a seed and `/tmp/ray-a/…` is not | P-a (`[41]`: 41 names `//tmp/ray-a/…`, 40 names `/tmp/ray-a/…`) |
| S50a | never a temp dir that pid 1's command names: pid 1 and almost every other process listed, `acquire` and `release` refusing | P-b; S43′'s tests for 4 and 1 |

The pid 1 half of S43′ and all of S46a rest on probes alone: no test has pid 1 naming the temp dir,
or a temp dir with a leading `//` (observation 4).

**The links.** With the files staged, every `](target)` in `docs/rehearsal-lock.md` that is neither
a URL nor an anchor, resolved from `docs/` and looked up in `git ls-files` (which includes the
index): **6 relative links, 0 not tracked**, this log's among them (§3.7).

### 3.5 No client named (prompt §3.5)

`grep -n -i -E 'secondary|sgk|champbh|cpbh|stochastic|instanton' docs/rehearsal-lock.md`: nothing
(exit 1).

### 3.6 The real `HOME` and Ray (prompt §3.6)

`~/ScienceData/.rehearsal-lock` and `~/.raypoolkit` absent, and `pgrep -lf
'gcs_server|raylet|ray::'` exit 1, before (19:24) and after (§3.7).

### 3.7 After staging

Run at 19:29 with the five files staged, before committing:

- `git diff --cached --name-only`: `docs/OPEN_ISSUES.md`, `docs/rehearsal-lock.md`,
  `prompts/INDEX.md`, `prompts/rehearsal-lock/IMPLEMENTATION_STATE.md`,
  `prompts/rehearsal-lock/logs/03a-correct-two-clauses-of-the-contract.md`.
- The suite: `Ran 226 tests in 2.113s` `OK`; `black --check raypoolkit docs`: "20 files would be
  left unchanged."
- `git diff --cached 89d6875 -- raypoolkit pyproject.toml`: empty (0 lines).
- The links, by `$S/scripts/links.py` (every `](…)` that is neither a URL nor an anchor, resolved
  from its file's directory and looked up in `git ls-files`): `docs/rehearsal-lock.md` 6, all
  tracked; with this log, the board and `docs/OPEN_ISSUES.md`, 26, the one reported untracked being
  this log's own mention of the pattern in a code span in §3.4, which is not a link.
- The client grep: nothing (exit 1). Neither lock location under the real `HOME`; `pgrep` exit 1.

## 4. The deliberate-breakage record

No test changes, so there is no mutation to catch (prompt §3). In its place, each probe's
expected output differs from what the old clause predicts, and is shown beside it (§3.3):
- P-a: the old §4 clause predicts `//tmp/ray-a` refused and `ray_processes("//tmp/ray-a", …)`
  raising `ValueError`; the module accepts it and lists `[41]`.
- P-b: the old §6 item 4 predicts `[30, 31]`; the module lists `[1, 30, 31]`.

Had the module been as the old clauses said, P-a's first line and its `//tmp/ray-a` listing, and
P-b's first case, would print FAIL and the probe exit 1.

## 5. Observations not acted on

1. **The module's docstrings make the pid 1 claim** (prompt §2.3): `rehearsal_lock.py:63-64`, the
   provenance note's "the walk that keeps this process, its ancestors and its own children out of
   the listing", and `:345-347`, `ray_processes`'s "this process …, its ancestors and its own
   descendants are **never listed**". Both say what the contract said before this commit. They are
   under `raypoolkit/`, which this prompt does not change. No issue is opened, as the prompt
   directs (its acceptance 3 puts the index at 0); for the orchestrator, should a later change
   under `raypoolkit/` take them.
2. **`PROVENANCE.md:102` repeats it** ("the walk that keeps a process, its ancestors and its own
   children out of the listing"), following the docstring, and describes what was taken from the
   model, SGK's walk, which also stops before pid 1 (01's log §5). Not changed, as the prompt says.
3. **A temp dir starting `//private/` is not matched without `/private`** (P-c (2)):
   `_temp_dir_pattern` strips `/private` only from a `D` that starts `/private/`, so for
   `//private/tmp/ray-a` only `//private/tmp/ray-a…` (or `/private//private/…`) is a seed, and
   `/tmp/ray-a/…` is not. §6 item 1's "in its spelling with and without a leading `/private`
   component" is true on the reading that `//private/…` begins with `//`, not with a `/private`
   component, and the corrected §4 and the new caller sentence ("the rule matches the spelling
   given"; never start the temp dir with `//`) cover the case. Not opened as an issue; for the
   orchestrator.
4. **No test pins either corrected edge.** `BAD_TEMP_DIRS` has `/tmp//ray-a` but neither
   `//tmp/ray-a` (accepted) nor `///tmp/ray-a` (refused), and no test has pid 1 naming the temp dir.
   The corrected statements rest on P-a and P-b. This prompt adds no test; a later prompt that
   touches `raypoolkit/tests/` may.
5. **On Linux, kernel threads do not descend from pid 1** (P-c (1)), which is why the corrected
   item 4 says "every descendant of pid 1" (deviation 1). The process rule has been proven under
   real Ray on macOS only (§10), and the suite reads no real `ps`, so nothing else turns on it.

## 6. Issues

**Closed:** `[03-the-contract-overstates-two-edges-of-the-module]`, moved from the board's §3 to §4
with a **Resolved (03a)** line. None opened or narrowed. `docs/OPEN_ISSUES.md`: the row deleted,
**0 open**.

## 7. State handed to the next prompt

- **`v0.3.0` is ready to be tagged on this commit once CI passes here** (README §5 rule 10), not on
  `89d6875`. The trees of the two differ only in `docs/rehearsal-lock.md` and `prompts/`; nothing
  under `raypoolkit/` or `pyproject.toml` differs, so the wheel is 03's. The tag is made by the
  user or on the user's instruction. Nothing is pushed: local `main` is ahead of `origin/main`
  (`cc5f2d6`) by 03's commits and this one.
- `docs/rehearsal-lock.md` is the statement of the lock for 04. Its "What it asks of a caller" now
  has two more rules a client's call sites must meet: no temp dir starting `//`, and none that pid
  1's command names. No client meets either case today.
- The suite is **226**. The index is **0**.
- Observations 1 and 4 are for whichever later prompt changes `raypoolkit/`.
