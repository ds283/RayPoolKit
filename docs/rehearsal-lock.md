# The shared rehearsal lock

The contract of `raypoolkit.rehearsal_lock`, as released in `v0.3.0`. Every project that shares
the lock keeps it. As the statement of the lock, it replaces §2 of the brief of 2026-10-12, from
which each project wrote an implementation of its own; the module replaces those implementations.

Every statement below about the module is true of it at this release. Each is checked by a test
in [`raypoolkit/tests/test_rehearsal_lock.py`](../raypoolkit/tests/test_rehearsal_lock.py), by a
probe, or by the proof under real Ray. The checks are listed, statement by statement, in the log
of the prompt that wrote this document,
[`prompts/rehearsal-lock/logs/03-release-v0.3.0.md`](../prompts/rehearsal-lock/logs/03-release-v0.3.0.md),
and in 03a's, which corrected two of its clauses,
[`prompts/rehearsal-lock/logs/03a-correct-two-clauses-of-the-contract.md`](../prompts/rehearsal-lock/logs/03a-correct-two-clauses-of-the-contract.md).

## 1. What the lock is for

Several projects run long Ray builds on one machine. The lock lets one rehearsal or long build
run at a time. A project takes it before it starts Ray, and releases it once its Ray has stopped.

A held lock means **stop and ask the user**. Nothing waits for, queues, retries or breaks a lock.
A stale lock is removed by the user, by hand (`rm -r ~/.raypoolkit/rehearsal-lock`), once
`status` shows its pid not alive and no processes.

## 2. How it is run

```bash
<venv>/bin/python -m raypoolkit.rehearsal_lock <command> [options]
```

- `<venv>` is the project's own venv, with `raypoolkit` installed from a release pin. There is no
  console script.
- `--help` prints the usage, whose first line starts `usage: python -m raypoolkit.rehearsal_lock`.
- The module imports only the standard library. The command imports `ray` too, through the
  package root, which imports `RayWorkPool`. That costs a few tenths of a second a call (0.3–0.6 s
  measured at Ray 2.43.0).

**The Python API.** The same commands are functions of the module:

- `acquire(project, purpose, ray_temp_dir, ray_address, *, lock_dir=None)`,
  `set_pid(project, ray_temp_dir, pid, *, lock_dir=None)`,
  `release(project, ray_temp_dir, *, lock_dir=None)`,
  `status(ray_temp_dir=None, ray_address=None, *, lock_dir=None)` and
  `ray_processes_command(ray_temp_dir, ray_address=None)`. Each prints what its command prints and
  returns its exit code.
- A bad argument raises `ValueError` where the command line exits 2. No function returns 2.
  `status(ray_address=…)` with no `ray_temp_dir` raises `ValueError`.
- `lock_dir` is a keyword of the first four only, for tests and proofs (§3).
- `ray_processes(ray_temp_dir, ray_address=None)` is the process rule (§6). It returns a list of
  `(pid, ppid, command)` tuples sorted by pid, each command whole. It raises `ValueError` for a bad
  argument, and `RuntimeError` or `OSError` if the process table cannot be read. Its keywords
  `ps_text` and `self_pid` are test seams; no caller passes them.
- `default_lock_dir()` is the location (§3), `old_lock_dir()` the old one (§9), and
  `main(argv=None)` the command line.

**Run the commands in a process of their own**, as the command line. Never call them through the
Python API inside a Ray driver: a driver cannot see its own in-process instance that way (§6).

## 3. The location

The lock is the directory `~/.raypoolkit/rehearsal-lock`, computed from `HOME` each time a command
runs, never at import.

- `acquire` makes `~/.raypoolkit` if it does not exist, then makes the lock with one `os.mkdir`,
  never `exist_ok`. That `mkdir` is the atomic step: the caller whose `mkdir` succeeds holds the
  lock.
- No environment variable or command-line option moves the lock. The keyword `lock_dir` is for
  tests and proofs.
- **The lock is a directory.** A path that is not a directory, such as a plain file, reads as no
  lock to `status` (`lock: free (<path> does not exist)`), to `release` (no lock to release, exit
  0) and to `set-pid` (exit 1); `acquire` finds the path taken and exits 3. Only a file made by hand
  can be there.

## 4. The owner file

`owner`, in the lock directory: UTF-8 text, seven `key: value` lines, each ending in a newline, in
this order:

```text
project: <project>
purpose: <purpose>
acquired: 2026-10-24T12:03:45+01:00
host: <hostname -s>
ray_temp_dir: /tmp/ray-p
ray_address: in-process
pid: -
```

It is written as `owner.tmp`, in the lock directory, and renamed over `owner`: by `acquire`, and
again by `set-pid`.

**The values.**
- `project`, `purpose`, `ray_temp_dir` and `ray_address` are the caller's arguments to `acquire`.
- `acquired` is ISO 8601, local time with its offset, to the second.
- `host` is `hostname -s`, or `socket.gethostname()` cut at its first dot if that cannot be run.
- `pid` is `-` until `set-pid` records one. `set-pid` rewrites the `pid:` line alone, and keeps
  every other byte of the file.

**The argument rules.** Every argument is checked before anything is touched. A value that breaks
a rule is a usage error (exit 2), or `ValueError` from a function.
- Every value is one line: not empty or blank, with no line break of any kind.
- `ray_temp_dir` is an absolute path in normal form, and never `in-process`. Normal form is what
  `os.path.normpath` leaves unchanged: no trailing `/`, no `.` or `..` component, and no doubled
  `/`, except a leading `//`, which POSIX keeps and the check accepts. So `//tmp/ray-a` passes,
  and `/tmp//ray-a`, `///tmp/ray-a` and `/tmp/ray-a/` do not. The process rule then matches the
  leading `//` as spelled (§6, "What it asks of a caller").
- `ray_address` is `in-process`, or `host:port`. It is split at the last colon: the host is
  non-empty with no whitespace, and the port is decimal digits. No range is checked, so
  `[::1]:6379` and `h:99999` both pass; `local` and `auto` do not.
- A pid is a positive integer. On the command line it is decimal digits only.

**Parsing.** A reader splits each line at its first `": "`. The key is before it, and the value is
everything after it, so a value may contain `": "`.

## 5. Whose lock it is

A lock is the caller's when its owner file's `project` and `ray_temp_dir` equal the caller's
`--project` and `--ray-temp-dir`.

- **The strings are compared as given.** `/private/tmp/ray-q` and `/tmp/ray-q` are one temp dir to
  the process rule (§6), and two callers here. So a caller passes the same spelling every time.
- An owner file with `ray_temp_dir: in-process`, as some projects wrote before this release, is no
  caller's: no caller can pass `in-process` as a temp dir.
- `set-pid` and `release` touch no lock that is not the caller's. They exit 1 and print both
  sides: the owner file, and the caller's `project` and `ray_temp_dir`.
- `acquire` and `status` do not check whose lock it is. A held lock is held, even by the caller.

## 6. The processes of a Ray instance

`ray_processes` is the rule, and `acquire`, `release`, `status` and `ray-processes` all use it.
For a temp dir `D`, and an address `A` if one is given, it reads the process table once, with
`ps -axww -o pid= -o ppid= -o command=`, skipping any line that does not begin with a pid and a
ppid.
Then:

1. **Temp-dir seeds.** A process is a seed if its command contains `D`, in its spelling with and
   without a leading `/private` component, followed by `/`, a space, `=` or the end of the command.
   - `D` is matched literally, and its end is a whole path component: `/tmp/ray-ab` is not a seed
     for `/tmp/ray-a`.
   - Its start has no boundary: `/var/tmp/ray-a/x` is a seed for `/tmp/ray-a`. This over-lists,
     which is the safe side.
2. **The client-server seed**, only when `A` is `host:port`. A process is a seed if its command
   contains `ray.util.client.server`, and `--address=<A>` followed by a space or the end, each
   anywhere in the command. A `ray start` cluster's Ray client server names no temp dir, and this
   finds it. With `A` `in-process`, or no `A`, there is no such seed.
3. **Descendants.** Every descendant of a seed is added. Ray's workers show only `ray::<name>`.
4. **This process is never listed**: the process reading the table, its ancestors other than
   pid 1, and its own descendants. They still seed the walk, so if an ancestor's command names
   `D`, its other descendants are listed.
   - Pid 1 is listed if its command names `D`, and then so is every descendant of pid 1 outside
     that set, which is almost every process. This over-lists, the safe side: `acquire` refuses
     with 4 and `release` with 1. On macOS pid 1 is `launchd`, whose command names no temp dir.

**What it asks of a caller.**
- **Every Ray instance run under the lock has a temp dir of its own**, recorded as
  `ray_temp_dir`.
  - An in-process instance is started with `ray.init(address="local", _temp_dir=<dir>)`, and its
    `ray_address` is `in-process`.
  - A `ray start` cluster is started with `--temp-dir <dir>`, and its `ray_address` is its
    `host:port`.
- **Keep the temp dir short**: Ray's Unix sockets live under it, and macOS limits a socket's path
  to about 104 bytes. Never use `/`, or a directory other processes name. `/` passes the argument
  checks, and then every command containing `//`, `/ ` or `/=`, or ending in `/`, is a seed.
- **Never start the temp dir with `//`.** The check accepts a leading `//` (§4), and the rule
  matches the spelling given: for `//tmp/ray-a`, a command naming `//tmp/ray-a/…` is a seed and
  one naming `/tmp/ray-a/…` is not. So a process that names the same directory as `/tmp/…` would
  not be listed. That is the unsafe side.
- **Record a pid with `set-pid` once Ray is up**: the driver's for an in-process instance, and the
  `gcs_server`'s for a cluster. `release` refuses while the recorded pid is alive. Ray's process
  reaper (`ray/_private/ray_process_reaper.py`) is a child of an in-process driver and names no
  temp dir, so the rule does not list it. The recorded pid covers it, and the reaper was measured
  to exit at `ray.shutdown()` (Ray 2.43.0 and 2.55.1).
- **Run the lock's commands as the command line, not inside a Ray driver.** Every process of an
  in-process instance descends from its driver: `gcs_server`, `raylet`, `monitor.py`,
  `log_monitor.py` and the dashboard are its children, and the workers descend from the raylet.
  The rule never lists the descendants of the process reading the table. So `ray_processes`,
  called in the driver, lists nothing of the driver's own instance. The command line, run as a
  child of the driver or from anywhere else, lists them all, bar the reaper.
- **Any process whose command names the temp dir is listed**: a shell, an editor, a `tail` of a
  Ray log. If such a process is an ancestor of the lock command, its other descendants are listed
  too, the driver among them. So a script that runs the lock's commands names the temp dir in no
  command line of its own, and passes it some other way (a variable set inside the script, or
  standard input).
- **Never use a temp dir that pid 1's command names.** Pid 1 is not kept out of the listing (§6
  item 4), so it and almost every other process would be listed, and `acquire` and `release`
  would refuse for as long as pid 1 runs.

## 7. The commands

**`acquire --project P --purpose TEXT --ray-temp-dir D --ray-address A`**

Takes the lock for `P`. In order, after its arguments: it checks the old location (§9); makes
`~/.raypoolkit` if needed; makes the lock; writes the owner file with `pid: -`; then reads the
processes of `D` and `A` (§6).
- **0**: the lock is held now.
- **3**: the old location exists, and nothing is created; or the lock is held, and nothing is
  touched. Either way the owner file found there is printed, indented (or `(no owner file)`), with
  the instruction to stop and ask the user.
- **4**: a process of `D`, or of `A`'s Ray client server, is alive (each is listed), or the
  process table cannot be read. The lock is released again. If that removal fails, `acquire` says
  that it could not release the lock again, and still exits 4.
- **1**: the owner file could not be written. The lock is removed.

**`set-pid --project P --ray-temp-dir D PID`**

Records `PID` in `P`'s lock.
- **0**: recorded.
- **1**, with nothing changed:
  - `PID` is not a live process. This is checked first, before the lock is looked at. "Live" is
    `os.kill(PID, 0)`, which sends no signal; a process the caller may not signal is live.
  - There is no lock (its path is not a directory).
  - The lock has no owner file.
  - The lock is not the caller's (§5).
  - The owner file has no `pid:` line, or more than one.

**`release --project P --ray-temp-dir D`**

Removes `P`'s lock (`owner`, any `owner.tmp`, then the directory) once nothing of it is alive. The
address whose client server it checks is the owner file's `ray_address`, not an argument.
- **0**: released; or there is no lock (its path is not a directory).
- **1**: refused, with the reason, and nothing removed. The checks are in this order:
  - the lock has no owner file;
  - the lock is not the caller's (§5);
  - the recorded pid is alive (a pid of `-`, or one that is not a number, is not checked);
  - the owner's `ray_address` is neither `in-process` nor `host:port`;
  - a process of `D`, or of the owner's address's Ray client server, is alive (each is listed);
  - the process table cannot be read.
- **1** also when the lock directory could not be removed, for instance because it holds a file
  other than `owner` and `owner.tmp`. By then the owner file has been removed, so the lock is left
  held with no owner file, for the user.

**`status [--ray-temp-dir D [--ray-address A]]`**

Prints the lock's state, in the layout of §8, and changes nothing.
- **0**, always, an unreadable process table included.
- With `D` given, the processes listed are those of `D`, and of `A`'s client server if `A` is
  given and is `host:port`; never the owner's. With no `D`, they are those of the owner file's
  `ray_temp_dir` and `ray_address`.

**`ray-processes --ray-temp-dir D [--ray-address A]`**

Lists the processes of `D` (§6), one per line.
- **0**: none.
- **1**: some; or the process table cannot be read.

**For every command:**
- **Usage errors exit 2**: a missing or unknown command or option, or a value that breaks an
  argument rule of §4. There is no option to force, wait, retry, break or move the lock.
- `status` takes `--ray-address` only with `--ray-temp-dir`; an address alone is a usage error.
- **Where the output goes.** Refusals and errors go to stderr. Every success line, `release`'s "no
  lock to release", every line of `status` (its unreadable-table line included) and
  `ray-processes`'s listing go to stdout.
- **A listed process** is printed as `<pid> <ppid> <command>`, the command cut to 150 characters:
  indented four spaces in `status` and in a refusal, and not indented by `ray-processes`.
- **An `OSError` the module does not handle** ends the command with a Python traceback and exit 1.
  For example, when `~/.raypoolkit` is a plain file, `acquire` ends that way and creates nothing.
  The traceback is not part of the interface.

## 8. `status`'s layout

A caller may match these lines, so each is quoted as the module prints it. `<lock>` is the lock's
path and `<old>` the old location's. The lines come in this order:

| # | Line | When |
|---|---|---|
| 1 | `lock: HELD (<lock>)` | the lock's path is a directory |
| | `lock: free (<lock> does not exist)` | it is not (nothing there, or not a directory) |
| 2 | the owner file's lines, each indented four spaces | held, with an owner file. An empty owner file prints one empty line. |
| | `    (no owner file)` | held, with no owner file |
| 3 | `owner pid: - (no pid recorded yet)` | held, with an owner file whose `pid` is `-`, missing, or not a number |
| | `owner pid <pid>: alive` | held, with an owner file whose pid is alive |
| | `owner pid <pid>: NOT alive` | held, with an owner file whose pid is not alive |
| 4 | `old location: PRESENT (<old>)` | anything exists at the old location (§9) |
| 5 | `Ray processes: no temp dir given` | no `--ray-temp-dir`, and no owner file to take one from |
| | `Ray processes: the owner's ray_temp_dir or ray_address is not usable` | no `--ray-temp-dir`, and the owner's values break §4's rules or are missing |
| | `Ray processes of <D>: cannot read the process table (<reason>)` | the table cannot be read |
| | `Ray processes of <D>: none` | no process of `D` (§7, `status`) |
| | `Ray processes of <D>: <n>`, then `n` lines `    <pid> <ppid> <command>` | `n` processes, the command cut to 150 characters |

`<D>` is the temp dir given, or else the owner's. Lines 2 and 3 appear only when the lock is held,
and line 4 only when the old location exists.

## 9. The old location

Before this release, every project kept the lock at `~/ScienceData/.rehearsal-lock`. In `0.3.x`,
while anything exists at that path:
- `acquire` refuses with exit 3 before it creates anything, printing that directory's owner file
  (or `(no owner file)`) and saying that it is the old location;
- `status` prints its `old location: PRESENT` line.

`set-pid`, `release` and `ray-processes` do not look at it.

The refusal is removed in a later release, once every project has moved. It catches a project that
was missed and still holds the old lock, and a stale old lock left behind. It cannot catch a
project that acquires at the old location after the move, since that project cannot see the new
location.

## 10. What the lock does not do

- It starts and stops no Ray, and signals no process.
- **It checks no port.** An in-process instance under `ray[default]` starts a headless dashboard
  on Ray's default port, 8265, even with `include_dashboard=False` (measured at Ray 2.43.0 and
  2.55.1).
- **It cannot see some processes.** A process of the instance whose command names neither the temp
  dir nor the client server's address, and that descends from no process that does, is not listed.
- **Its process rule was proven under real Ray on macOS only.** The suite, which runs on Ubuntu in
  CI too, reads no real `ps`.

## 11. How it was proven

- **The suite's tests of the module**, [`raypoolkit/tests/test_rehearsal_lock.py`](../raypoolkit/tests/test_rehearsal_lock.py),
  103 tests. They need no Ray. Each runs with `HOME` patched to a temporary directory, and none
  touches the real `HOME` or reads the real `ps`. Each refusal has a test that leaves only that
  reason standing. CI runs them at both tested ends.
- **The proof under real Ray**, [`docs/rehearsal-lock/ray_proof.py`](rehearsal-lock/ray_proof.py),
  run at Python 3.12.15 / Ray 2.43.0 and 3.13.16 / Ray 2.55.1, holding the real shared lock at the
  location the projects used that day. It proves three things:
  - an in-process instance with `_temp_dir`, listed whole bar the reaper, with `release` refused
    while it is up;
  - a `ray start --head` cluster, its client server found by its address, stopped by signalling
    exactly what `ray-processes` listed;
  - a second `acquire` refused.

  It is run in a venv with `ray[default]` and this package, with nothing of Ray running, in the
  background, from a command that names no temp dir. Its docstring gives the commands. Its results
  are in the log of the prompt that ran it,
  [`prompts/rehearsal-lock/logs/02-prove-it-under-real-ray.md`](../prompts/rehearsal-lock/logs/02-prove-it-under-real-ray.md).
