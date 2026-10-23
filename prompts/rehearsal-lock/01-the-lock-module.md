# Prompt 01 — the lock module

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- The plan is committed (`6e559bf`), and U1–U6 are taken (README §6.2).
- G1 holds: at SGK `216e44d`, `git rev-parse 216e44d:tools/rehearsal_lock.py` is `ea14336…` and
  `git rev-parse 216e44d:tools/tests/test_rehearsal_lock.py` is `cdeecd6…`.
- `git status` is clean in this repository, and the suite gives `Ran 121 tests … OK`.

**Closes:** nothing. **Narrows:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The module is small, but every refusal in it is a safety property shared by three projects: a
  check that is too loose lets two rehearsals run at once, and one that is too strict leaves a lock
  nobody can release. Each has to be tested with only one reason standing.
- The process rule is new in Python. It is CPBH's `awk` program (README §0.2), with SGK's
  treatment of this process's own tree, and its corner cases (the `/private` spelling, the
  whole-path-component match, the client server) are where a quiet mistake would hide.

**Read first:**

1. [`README.md`](README.md): all of §0, §1, §4, §5 and §6. §4 is the interface this prompt
   implements; where this prompt and §4 disagree, stop and ask.
2. `/Users/ds283/Documents/Code/RayPoolKit/CLAUDE.md`, above all "What this repository is" (no
   client is named in the package) and "Repository mechanics".
3. SGK's module and tests, the model for most of this prompt, read through `git`:
   `git -C /Users/ds283/Documents/Code/SecondaryGWKit show 216e44d:tools/rehearsal_lock.py` and
   `…:tools/tests/test_rehearsal_lock.py`. Read SGK's prompt that specified them too,
   `216e44d:prompts/runregistry-extraction/02a-the-rehearsal-lock-helper.md` §2.1–§2.2.
4. CPBH's script, the model for the process rule: `git -C /Users/ds283/Documents/Code/ChamPBH show
   807f175:.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh`, the functions
   `temp_dir_regex` and `list_cluster_pids`.
5. The brief, the contract the clients implement today: `git -C
   /Users/ds283/Documents/Code/StochasticInstantons show
   8b4f615:.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md` §2 and §3 ("Stop").
6. [`planning/`](planning/): the probe and its two outputs, from which §2.6's fixtures are drawn.
7. This repository: `raypoolkit/__init__.py`, `raypoolkit/_timing.py` (the licence header),
   `raypoolkit/tests/test_package_imports.py`, `.github/workflows/tests.yml`.

Facts below are at `6e559bf`, measured on 2026-10-23.

---

## 1. What is wanted

A module, `raypoolkit/rehearsal_lock.py`, that every client can use in place of its own lock code,
and its tests. After it:

- `python -m raypoolkit.rehearsal_lock` with five commands, and the same five as functions, to
  README §4;
- the lock at `~/.raypoolkit/rehearsal-lock` (D2), refusing to be taken while the old location
  exists (U4), with no way to move it but a keyword argument (U5);
- one process rule, by Ray temp dir, with the client-server seed (U2);
- tests that need no Ray and touch no real lock, each refusal pinned with only one reason standing;
- the import guard extended to the new module.

The module is **written new**, to README §4, not copied: SGK's is hard-wired to one project and to
its venv rule. Take SGK's code where it already does what §4 says (the owner file's writing and
parsing, `pid_alive`, `_short_hostname`, the ancestor walk, the commands' structure and messages),
and CPBH's `list_cluster_pids` for the rule.

**Nothing else in the package changes.** `RayWorkPool.py`, `contract.py`, `_timing.py` and
`__init__.py` are untouched (README §5 rule 7, and U3: no lazy import). No version, README,
`PROVENANCE.md` or `CLAUDE.md` change: those are 03's.

---

## 2. What to change

### 2.1 The venv

The repository's `venv` (Python 3.12.15, Ray 2.43.0, `black` 25.1.0), with the package installed
editable. Record `pip freeze` in the log. For the high end, make a scratch venv in the session
scratchpad from `/opt/local/bin/python3.13` (3.13.16), as `extraction` 03 did
(`uv pip install --python <venv>/bin/python -e . "ray==2.55.1" "black==25.1.0"`), and run the suite
there too. If the scratch venv cannot be made (no network), say so in the log; CI covers the high
end once the commit is pushed.

### 2.2 The module, `raypoolkit/rehearsal_lock.py`

The licence header of the other package modules (`extraction` U11), byte for byte, then a module
docstring that says what the lock is for, the five commands and their exit codes, that nothing in
it waits on, retries or breaks a lock, and a provenance note: what was taken from SGK's
`tools/rehearsal_lock.py` (blob `ea14336`) and from CPBH's `ray_cluster.sh` (blob `eaae1e7`). That
note is the one place the module may name a client (`CLAUDE.md`). Standard library only: it does not
import `ray` or any other part of `raypoolkit`.

**Locations** (D2, U4, U5), each computed from `Path.home()` when called, never at import:
- `default_lock_dir()` → `~/.raypoolkit/rehearsal-lock`;
- `old_lock_dir()` → `~/ScienceData/.rehearsal-lock`.

No environment variable is read for either. Every command takes a keyword-only `lock_dir=None`;
`None` means `default_lock_dir()`.

**Arguments.** Checked before anything is touched; a bad one raises `ValueError` from a function
and exits 2 from the command line (argparse `type=` callables):
- `project`, `purpose`: one non-empty line;
- `ray_temp_dir`: an absolute path, one line, already in normal form (`os.path.normpath(d) == d`,
  so no trailing `/`, no `..`), and not `in-process` (U2);
- `ray_address`: `in-process`, or `host:port` with a non-empty host and a decimal port;
- `pid`: a positive integer.

**The owner file.** README §4: the seven keys in the brief's order, `owner.tmp` written and renamed
to `owner`. `owner_text(project, purpose, ray_temp_dir, ray_address, pid, acquired=None,
host=None)` builds it (the two keywords for tests); `parse_owner(text)` reads any project's, as
SGK's does (the value after the first `": "`).

**Identity.** A lock is the caller's when the owner's `project` and `ray_temp_dir` both equal the
caller's. A lock with no owner file is nobody's.

**`acquire(project, purpose, ray_temp_dir, ray_address, *, lock_dir=None)`**, in this order:
1. if `old_lock_dir()` exists and is not the lock being acquired (compare resolved paths): print
   that it is the old location, its owner file (or that it has none), and that the user removes it
   by hand once nothing holds it; return **3**, having created nothing;
2. create the lock's parent (`mkdir(parents=True, exist_ok=True)`), then `os.mkdir` the lock, never
   with `exist_ok`. If it exists: print its owner file (or that it has none) and "stop and ask the
   user"; return **3**, having touched nothing;
3. write the owner with `pid: -`. If that fails, remove the lock and return **1**;
4. list the processes of `ray_temp_dir` and `ray_address` (§2.3). If the table cannot be read, or
   any is listed: print them, remove the lock, and return **4**;
5. print that the lock is held, by whom and for what; return **0**.

**`set_pid(project, ray_temp_dir, pid, *, lock_dir=None)`**: refuse (**1**, nothing changed) if
`pid` is not alive, if there is no lock, if it has no owner file, if it is not the caller's, or if
the owner file has not exactly one `pid:` line; otherwise rewrite that line only, through
`owner.tmp`, and return **0**.

**`release(project, ray_temp_dir, *, lock_dir=None)`**: no lock → print so and return **0**.
Otherwise refuse (**1**, nothing changed, the reason printed with both sides of any mismatch) if it
has no owner file, if it is not the caller's, if its recorded pid is alive, or if any process of
the owner's `ray_temp_dir` and `ray_address` is listed (or the table cannot be read). Otherwise
remove `owner`, any `owner.tmp`, and the directory; return **0**.

**`status(ray_temp_dir=None, ray_address=None, *, lock_dir=None)`**: always **0**. Prints, in this
order and this layout (pinned by §2.6):

```text
lock: HELD (<lock dir>)                        or   lock: free (<lock dir> does not exist)
    <the owner file, each line indented 4>          (when held)
    (no owner file)                                 (when held with none)
owner pid <n>: alive  |  owner pid <n>: NOT alive  |  owner pid: - (no pid recorded yet)
old location: PRESENT (<old dir>)                   (only when it exists)
Ray processes of <temp dir>: none  |  Ray processes of <temp dir>: <count>
    <pid> <ppid> <command, cut to 150 characters>   (one per process)
```

The process lines use the `ray_temp_dir` given, or else the owner's (and likewise the address); with
neither, the last line is `Ray processes: no temp dir given`. If the table cannot be read, that
line says so.

**`ray_processes_command(ray_temp_dir, ray_address=None)`**: the listing, one line per process as
above; **0** none, **1** some or the table unreadable (to stderr).

**`main(argv=None)`**: argparse, `prog="python -m raypoolkit.rehearsal_lock"`, the five
subcommands with README §4's options, `required=True` on the subparsers; usage errors exit 2.
**There is no option to break, wait, retry or move the lock** (no `--force`, `--wait`, `--retry`,
`--lock-dir`). The module ends with `if __name__ == "__main__": sys.exit(main())`. Refusals and
errors go to stderr, everything else to stdout, as SGK's.

### 2.3 The process rule (U2)

`ray_processes(ray_temp_dir, ray_address=None, *, ps_text=None, self_pid=None)` returns
`(pid, ppid, command)` tuples sorted by pid. `ps_text=None` reads the table through
`_ps_output()`, the module's only call of `ps`
(`ps -axww -o pid= -o ppid= -o command=`; a non-zero status raises `RuntimeError`). Tests replace
`_ps_output`, or pass `ps_text`.

1. **Parse** each line as `pid ppid command`; skip lines that do not parse.
2. **Never listed** ("safe"): `self_pid` (default `os.getpid()`), its ancestors up to pid 1, and
   its own descendants (its `ps`).
3. **Seeds:**
   - every process whose command contains the temp dir in either spelling: with any leading
     `/private` removed, the regex `(/private)?<re.escape(dir)>` followed by `/`, a space, `=` or
     the end of the line;
   - when `ray_address` is `host:port`: every process whose command contains
     `ray.util.client.server` and `--address=<host:port>` followed by a space or the end of the
     line.
4. **Descendants:** add every process whose parent is listed, until nothing changes.
5. Return everything listed except the safe set.

Ray's process reaper is a child of the driver and names no temp dir, so it is not listed; the
driver's pid in the owner file covers it (README §0.3). Say so in the function's docstring.

### 2.4 What is not carried over from SGK

- `venv_roots()` and the venv rule (U2).
- `PROJECT`, `IN_PROCESS` as a temp dir, and `_not_sgk_reason`: identity is the caller's.
- The `~/ScienceData` default (D2).

### 2.5 The import guard, `raypoolkit/tests/test_package_imports.py`

Add, without changing the three tests there:
- a test that `raypoolkit/rehearsal_lock.py` imports only the standard library (by the guard's own
  `imported_modules`), so neither `ray` nor the rest of the package;
- a test that, in a fresh isolated interpreter (`_run_child`), `python -I -m
  raypoolkit.rehearsal_lock --help` exits 0 and loads no forbidden module.

### 2.6 The tests, `raypoolkit/tests/test_rehearsal_lock.py`

`unittest`, no Ray. **Every test patches `HOME`** to a temporary directory (README §5 rule 6), and
every test that does not test the default location also passes `lock_dir` explicitly, inside that
temporary directory. `_ps_output` is patched to fixed text (empty unless a test sets it). No client
name appears: use neutral fixtures, such as project `ProjectA` with `/tmp/ray-a` and
`127.0.0.1:6400`, `ProjectB` with `/tmp/ray-b`, and `ProjectC` in process with `/tmp/ray-c`.

Port SGK's 42 tests to this module, each to its nearest meaning under README §4, and add what §2.2
and §2.3 need. At least:

1. **Acquire.** A free lock is created, with the seven keys in order, the caller's four values,
   `pid: -`, an `acquired` that parses with `datetime.fromisoformat` and has an offset, a `host`
   with no dot, and no `owner.tmp` left; the parent is created, the lock never with `exist_ok`
   (SGK's test of this, adapted). A held lock, whether the caller's, another project's, or with no
   owner file, returns 3, prints the owner or says it is missing, and leaves everything
   byte-identical. Processes of the temp dir return 4 and leave no lock; so does an unreadable
   table.
2. **The old location (U4).** With `~/ScienceData/.rehearsal-lock` present (with an owner file, and
   without), `acquire` returns 3, prints it, and creates nothing at the new location; with it
   absent but `~/ScienceData` present, `acquire` succeeds; acquiring the old location itself, by
   `lock_dir`, is not refused by this check.
3. **Set-pid.** A live pid (the test's own) changes `pid` and only `pid`. Refused, with nothing
   changed: a dead pid (SGK's `dead_pid()`), pid 0, no lock, no owner file, another project, the
   same project with another temp dir, and an owner file with two `pid:` lines.
4. **Release.** Releases with `pid: -` or a dead pid and no processes; with no lock returns 0.
   Refused, everything byte-identical, both sides printed: another project; the same project with
   another temp dir; another project with the caller's temp dir; no owner file; a live pid; a
   process of the temp dir with `pid: -`; a process of the temp dir with a dead pid; the owner's
   address's client server alone; an unreadable table. **Each refusal test leaves exactly one
   reason standing** (SGK's docstring says how).
5. **The rule.** On fixed text: the `gcs_server`, `raylet` and Python seeds of §0.3's trees, at
   each version, with the workers, actor and agents found as descendants, and the reaper not
   (build the fixtures from `planning/tempdir_probe-ray-*.txt`, with commands written out in full:
   the saved outputs are cut at 150 characters); a command naming `/private/tmp/ray-a` for
   `/tmp/ray-a`, and the reverse; not `/tmp/ray-ab`, `/tmp/ray-a.old` or `/tmp/ray`, for
   `/tmp/ray-a`; a match ending at `=` (`--temp-dir=/tmp/ray-a`) and at the end of the line; the
   client server for `127.0.0.1:6400` listed, and one for `127.0.0.1:6401` or `127.0.0.1:64000`
   not; no client-server seed for `in-process`; another project's processes (`/tmp/ray-b`, its own
   client server) not listed; this process, its ancestors (including one whose command names the
   temp dir) and its own children never listed; a descendant of a seed listed though its command
   names nothing (`ray::IDLE`).
6. **Locations.** `default_lock_dir()` and `old_lock_dir()` follow a `HOME` changed after import,
   and computing them creates nothing; each command called without `lock_dir` uses the patched
   `HOME`. No environment variable other than `HOME` moves the lock (set a few plausible ones,
   such as `RAYPOOLKIT_REHEARSAL_LOCK`, and check the location does not change).
7. **Arguments.** Each rule of §2.2's "Arguments" refused, by the function (`ValueError`, nothing
   created) and by the command line (exit 2).
8. **Owner file.** SGK's parser tests, with neutral fixtures; the three shapes the clients write
   today (a cluster's `host:port` address, `in-process` for both, and a `pid` that is `-` or a
   number), as text in the test, parsed and judged by the identity check.
9. **Command line.** Each command and exit status, through `main([...])`; `status`'s layout, pinned
   line by line, held and free, with and without an owner file, with the old location present, and
   with processes; no `--force`, `--wait`, `--retry` or `--lock-dir` (SGK's test, extended).

Tests run on Linux in CI (`.github/workflows/tests.yml`, Ubuntu). None may depend on macOS: no
test reads the real `ps`, or relies on `/private` existing; `dead_pid()` and `os.getpid()` work on
both.

---

## 3. Verification

1. **The suite** at the low end: `./venv/bin/python -m unittest discover -s raypoolkit/tests -t .`
   gives `Ran N tests … OK`, with N above 121 (the count before). Record N, and the count of the new
   module and of the guard's additions. At the high end, the same, if §2.1's scratch venv could be
   made.
2. **The command line** in a fresh shell with `HOME` set to a scratch directory (never the real
   one): `acquire`; `status`; start `sleep 60 &` and `set-pid` its pid (`$!`); a second `acquire`
   (3); `release` (1, the pid is alive); kill the `sleep` and `wait` for it; `release` (0);
   `status` again; and `ray-processes` for a temp dir nothing names. Record the transcript in the log, with the exit status after each command. Then make
   `$HOME/ScienceData/.rehearsal-lock` by hand in that scratch `HOME` and show `acquire` refusing
   and `status` reporting it.
3. **`black` 25.1.0** on the files changed: no change after formatting. `black --check raypoolkit
   docs` passes, as CI runs it.
4. **Nothing reached the real `HOME`**: `~/.raypoolkit` does not exist after the suite and §3.2,
   unless it existed before (record which), and `~/ScienceData/.rehearsal-lock` is as it was before
   (record both before and after).

### 3.1 Deliberate breakage

Apply each, run the suite, record the failing tests, revert. The log records each as a diff that
`git apply` replays (README §5 rule 8). At least:

| # | Mutation | A test that must fail |
|---|---|---|
| M1 | the lock's `os.mkdir` replaced by `mkdir(exist_ok=True)` | acquire on a held lock |
| M2 | the identity check compares `project` only | release / set-pid of the same project with another temp dir |
| M3 | the identity check compares `ray_temp_dir` only | release / set-pid of another project with the caller's temp dir |
| M4 | `release` skips the pid check | release with a live pid |
| M5 | `release` skips the process check | release with a process of the temp dir and `pid: -` |
| M6 | `acquire` skips the process check | acquire with a process of the temp dir |
| M7 | the old-location check removed | acquire with the old location present |
| M8 | the temp-dir match drops its boundary | `/tmp/ray-ab` not listed for `/tmp/ray-a` |
| M9 | the `/private` spelling dropped | `/private/tmp/ray-a` listed for `/tmp/ray-a` |
| M10 | the descendant walk removed | `ray::IDLE` below a raylet listed |
| M11 | the ancestor walk removed | an ancestor naming the temp dir not listed |
| M12 | the client-server seed removed | the client server for the owner's address listed |
| M13 | `default_lock_dir()` replaced by a module constant computed at import | the location follows a `HOME` changed after import |
| M14 | two owner keys swapped in `owner_text` | the seven keys in order |

---

## 4. Acceptance

1. §2.2–§2.6's files exist, and README §4's interface holds of them; nothing else under
   `raypoolkit/` changed (`git diff --stat` in the log).
2. §3.1–§3.4 hold, and each mutation of §3.1 fails at least one test.
3. **The records**, in the same commit:
   - the log, `logs/01-the-lock-module.md`, per README §5.1, with `pip freeze`, the suite counts
     before and after, §3.2's transcript and §3.4's before-and-after;
   - this board: the header, §1's row for 01 (landed, commit, suite);
   - `prompts/INDEX.md`: the campaign's line;
   - `docs/OPEN_ISSUES.md`, if the work opens or changes anything.

---

## 5. Stop conditions — stop and ask the user

- G1 no longer holds.
- README §4 cannot be implemented as written: two of its statements conflict, or one of them would
  let two callers hold the lock at once, or leave a lock nobody can release.
- A test cannot be written without Ray, without the real `HOME`, or without naming a client.
- The module would need anything beyond the standard library.
- Anything under `raypoolkit/` other than §2's files would have to change, including
  `__init__.py` (U3).
- The suite count falls, or an existing test fails.
- Anything would require editing or running SGK, ChamPBH or StochasticInstantons, or touching the
  real lock at either location. Reading the clients through `git show` is the only access this
  prompt has.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `raypoolkit/rehearsal_lock.py` (new);
  - `raypoolkit/tests/test_rehearsal_lock.py` (new);
  - `raypoolkit/tests/test_package_imports.py` (two tests added);
  - the log, this board and `prompts/INDEX.md`;
  - `docs/OPEN_ISSUES.md`, if needed.
- It starts no Ray, and takes no real lock (02).
- It does not change the version, `README.md`, `PROVENANCE.md` or `CLAUDE.md`, write
  `docs/rehearsal-lock.md`, or tag (03).
- It does not touch `RayWorkPool.py`, `contract.py`, `_timing.py` or `__init__.py`.
- It writes no client checklist (04), and nothing about cluster start or stop (D4).

---

## 7. The log and the board

`logs/01-the-lock-module.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, and §1's row for 01 (landed, commit, log, suite).
