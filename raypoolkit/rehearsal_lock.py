# (c) University of Sussex 2026
# Created by David Seery
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The shared rehearsal lock: one rehearsal or long build under Ray at a time on a machine.

Several projects on one machine run Ray builds. They share one lock, the directory
``~/.raypoolkit/rehearsal-lock``, so that only one rehearsal or long build runs at a time. Taking
it is one ``os.mkdir``, which is atomic; the directory holds an ``owner`` file of seven
``key: value`` lines (``project``, ``purpose``, ``acquired``, ``host``, ``ray_temp_dir``,
``ray_address``, ``pid``), written as ``owner.tmp`` and renamed. A lock is the caller's when its
owner's ``project`` and ``ray_temp_dir`` are the caller's.

Run with the project's own interpreter::

    ./venv/bin/python -m raypoolkit.rehearsal_lock <command>

Commands (each prints what it did; refusals and errors go to stderr):

``acquire --project P --purpose TEXT --ray-temp-dir D --ray-address A``
    Exit 0 held now; 3 held already, or the old location ``~/ScienceData/.rehearsal-lock`` exists
    (nothing is touched, and the owner file is printed); 4 a process of ``D`` (or of ``A``'s Ray
    client server) is alive, or the process table cannot be read (the lock is released again);
    1 the owner file could not be written.
``set-pid --project P --ray-temp-dir D PID``
    Record ``PID`` in ``P``'s lock, changing no other line. Exit 0; 1 refused (no lock, not
    ``P``'s lock, or ``PID`` not alive).
``release --project P --ray-temp-dir D``
    Remove ``P``'s lock, once its recorded pid is ``-`` or dead and no process of the owner's
    ``ray_temp_dir`` and ``ray_address`` is alive. Exit 0 released, or no lock; 1 refused, with
    the reason.
``status [--ray-temp-dir D [--ray-address A]]``
    The lock, its owner file verbatim, whether the recorded pid is alive, whether the old location
    exists, and the processes of ``D`` (or, with no ``D``, of the owner's). Exit 0.
``ray-processes --ray-temp-dir D [--ray-address A]``
    The processes of ``D``, one per line. Exit 0 none; 1 some, or the table cannot be read.

Usage errors exit 2. The same five commands are the functions ``acquire``, ``set_pid``,
``release``, ``status`` and ``ray_processes_command``, which return those exit codes and raise
``ValueError`` for a bad argument.

Nothing in this module waits on, retries or breaks a lock. A held lock means stop and ask the
user; a stale lock is the user's to remove by hand. It never starts or stops Ray, and signals no
process. No environment variable moves the lock; the keyword argument ``lock_dir`` exists for
tests and proofs, and the command line has no option for it.

Standard library only: it imports neither ``ray`` nor the rest of ``raypoolkit``.

Provenance. Written new for this package, taking two sources as its models. From SecondaryGWKit's
``tools/rehearsal_lock.py`` (blob ``ea14336``): the owner file's writing and parsing,
``pid_alive``, ``_short_hostname``, the walk that keeps this process, its ancestors and its own
children out of the listing, ``_ps_output`` as the one reading of ``ps``, and the commands'
structure, exit codes and messages. From ChamPBH's ``ray_cluster.sh`` (blob ``eaae1e7``), the
functions ``temp_dir_regex`` and ``list_cluster_pids``: the rule that finds a Ray instance's
processes by its temp dir, in both its spellings and as a whole path component, and by its Ray
client server's address, with every descendant of those.
"""

import argparse
import functools
import os
import re
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path

IN_PROCESS = "in-process"
OWNER_KEYS = (
    "project",
    "purpose",
    "acquired",
    "host",
    "ray_temp_dir",
    "ray_address",
    "pid",
)
PS_COMMAND = ["ps", "-axww", "-o", "pid=", "-o", "ppid=", "-o", "command="]
COMMAND_WIDTH = 150

_PS_LINE = re.compile(r"^\s*([0-9]+)\s+([0-9]+)(?:\s+(.*))?$")
_DIGITS = re.compile(r"[0-9]+")
_CLIENT_SERVER = "ray.util.client.server"


# ---- the locations -----------------------------------------------------------------------------


def default_lock_dir():
    """The shared lock, ``~/.raypoolkit/rehearsal-lock``, computed from ``HOME`` when called."""
    return Path.home() / ".raypoolkit" / "rehearsal-lock"


def old_lock_dir():
    """The lock's old location, ``~/ScienceData/.rehearsal-lock``, computed when called."""
    return Path.home() / "ScienceData" / ".rehearsal-lock"


def _resolve(lock_dir):
    return default_lock_dir() if lock_dir is None else Path(lock_dir)


# ---- the arguments -----------------------------------------------------------------------------


def _check_line(name, value):
    """``value`` is one non-empty line, or ``ValueError``."""
    if not isinstance(value, str) or not value.strip() or value.splitlines() != [value]:
        raise ValueError(f"{name} must be one non-empty line, not {value!r}")
    return value


def _check_ray_temp_dir(value):
    """An absolute path, one line, in normal form, and not ``in-process``; or ``ValueError``."""
    _check_line("ray_temp_dir", value)
    if value == IN_PROCESS or not os.path.isabs(value):
        raise ValueError(f"ray_temp_dir must be an absolute path, not {value!r}")
    if os.path.normpath(value) != value:
        raise ValueError(
            f"ray_temp_dir must be in normal form ({os.path.normpath(value)!r}), not {value!r}"
        )
    return value


def _check_ray_address(value):
    """``in-process``, or ``host:port`` with a non-empty host and a decimal port; or ``ValueError``."""
    _check_line("ray_address", value)
    if value == IN_PROCESS:
        return value
    host, sep, port = value.rpartition(":")
    if (
        not sep
        or not host
        or any(c.isspace() for c in host)
        or not _DIGITS.fullmatch(port)
    ):
        raise ValueError(
            f"ray_address must be {IN_PROCESS!r} or host:port, not {value!r}"
        )
    return value


def _check_pid(value):
    """A positive integer, or ``ValueError``."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"pid must be a positive integer, not {value!r}")
    return value


def _argument(check):
    """An argparse ``type=`` callable: ``check`` on the text, its ``ValueError`` a usage error."""

    def convert(text):
        try:
            return check(text)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(str(exc)) from None

    convert.__name__ = getattr(check, "__name__", "value")
    return convert


def _pid_argument(text):
    if not _DIGITS.fullmatch(text):
        raise argparse.ArgumentTypeError(
            f"pid must be a positive integer, not {text!r}"
        )
    return _argument(_check_pid)(int(text))


# ---- the owner file ----------------------------------------------------------------------------


def _short_hostname():
    """``hostname -s``; if that cannot be run, ``socket.gethostname()`` cut at its first dot."""
    try:
        result = subprocess.run(
            ["hostname", "-s"], capture_output=True, text=True, check=True
        )
        name = result.stdout.strip()
        if name:
            return name
    except (OSError, subprocess.CalledProcessError):
        pass
    return socket.gethostname().split(".")[0]


def owner_text(
    project, purpose, ray_temp_dir, ray_address, pid, acquired=None, host=None
):
    """The seven lines of the owner file, in the contract's order."""
    if acquired is None:
        acquired = datetime.now().astimezone().isoformat(timespec="seconds")
    if host is None:
        host = _short_hostname()
    lines = [
        f"project: {project}",
        f"purpose: {purpose}",
        f"acquired: {acquired}",
        f"host: {host}",
        f"ray_temp_dir: {ray_temp_dir}",
        f"ray_address: {ray_address}",
        f"pid: {pid}",
    ]
    return "\n".join(lines) + "\n"


def _replace_owner(lock_dir, text):
    """Write ``owner.tmp`` in the lock directory, then rename it over ``owner``."""
    tmp = lock_dir / "owner.tmp"
    tmp.write_bytes(text.encode("utf-8"))
    os.replace(tmp, lock_dir / "owner")


def parse_owner(text):
    """Any project's owner file: one ``key: value`` per line, the value after the first ``": "``."""
    owner = {}
    for line in text.splitlines():
        key, sep, value = line.partition(": ")
        if not sep:
            key = line.rstrip(":")
            value = ""
        owner[key] = value
    return owner


def read_owner(lock_dir):
    """The owner file's text, or ``None`` when there is none."""
    try:
        return (Path(lock_dir) / "owner").read_text(encoding="utf-8", errors="replace")
    except (FileNotFoundError, NotADirectoryError):
        return None


def _indented(text):
    if text is None:
        return "    (no owner file)"
    return "\n".join("    " + line for line in text.splitlines())


def pid_alive(pid):
    """Whether ``pid`` names a live process (``os.kill(pid, 0)``; a process we may not signal is alive)."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _not_callers_reason(owner, project, ray_temp_dir):
    """``None`` when the owner is the caller's (``project`` and ``ray_temp_dir``), otherwise why not."""
    problems = []
    if owner.get("project") != project:
        problems.append(f"project is {owner.get('project')!r}, not {project!r}")
    if owner.get("ray_temp_dir") != ray_temp_dir:
        problems.append(
            f"ray_temp_dir is {owner.get('ray_temp_dir')!r}, not {ray_temp_dir!r}"
        )
    return "; ".join(problems) if problems else None


def _recorded_pid(owner):
    """The owner's pid as an integer, or ``None`` for ``-`` or anything that is not a number."""
    value = owner.get("pid", "-").strip()
    return int(value) if _DIGITS.fullmatch(value) else None


def _usable_owner_values(owner):
    """The owner's ``(ray_temp_dir, ray_address)`` if both pass the argument checks, else ``None``."""
    try:
        return (
            _check_ray_temp_dir(owner.get("ray_temp_dir")),
            _check_ray_address(owner.get("ray_address")),
        )
    except ValueError:
        return None


# ---- the processes of a Ray instance -----------------------------------------------------------


def _ps_output():
    """The process table. The one place ``ps`` is read; tests replace it with fixed text."""
    result = subprocess.run(PS_COMMAND, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ps failed with status {result.returncode}")
    return result.stdout


def _temp_dir_pattern(ray_temp_dir):
    """``ray_temp_dir`` in its spellings with and without ``/private``, as a whole path component."""
    d = ray_temp_dir
    if d.startswith("/private/"):
        d = d[len("/private") :]
    return re.compile(r"(/private)?" + re.escape(d) + r"(?:[/ =]|$)")


def _client_server_pattern(ray_address):
    return re.compile(r"--address=" + re.escape(ray_address) + r"(?: |$)")


def _closure(start, children):
    """``start`` and every descendant of it, through the ``children`` map."""
    found = set(start)
    queue = list(start)
    while queue:
        for child in children.get(queue.pop(), ()):
            if child not in found:
                found.add(child)
                queue.append(child)
    return found


def ray_processes(ray_temp_dir, ray_address=None, *, ps_text=None, self_pid=None):
    """
    Every process of the Ray instance with this temp dir, as ``(pid, ppid, command)`` by pid.

    From one reading of the process table (``ps -axww -o pid= -o ppid= -o command=``, through
    ``_ps_output``, unless ``ps_text`` is given):

    - a process is a **seed** if its command line contains ``ray_temp_dir``, in its spelling with
      and without a leading ``/private`` component, followed by ``/``, a space, ``=`` or the end
      of the line (so ``/tmp/ray-a`` does not match ``/tmp/ray-ab``); or, when ``ray_address`` is
      ``host:port``, if its command line contains ``ray.util.client.server`` and
      ``--address=<host:port>`` followed by a space or the end of the line (a ``ray start``
      cluster's client server names no temp dir);
    - every **descendant** of a seed is added (Ray's workers show only ``ray::<name>``);
    - this process (``self_pid``, by default ``os.getpid()``), its ancestors and its own
      descendants are **never listed**. They seed the walk like any other process, so the other
      children of an ancestor that names the temp dir are listed.

    Ray's process reaper (``ray/_private/ray_process_reaper.py``) is a child of an in-process
    instance's driver and names no temp dir, so it is not listed. The driver's pid, recorded in
    the owner file, covers it: release is refused while the driver is alive, and the reaper exits
    with it.

    Raises ``ValueError`` for a bad argument, and ``RuntimeError`` or ``OSError`` if the table
    cannot be read.
    """
    _check_ray_temp_dir(ray_temp_dir)
    if ray_address is not None:
        _check_ray_address(ray_address)
    if ps_text is None:
        ps_text = _ps_output()
    if self_pid is None:
        self_pid = os.getpid()

    table = {}
    for line in ps_text.splitlines():
        m = _PS_LINE.match(line)
        if m:
            table[int(m.group(1))] = (int(m.group(2)), m.group(3) or "")
    children = {}
    for p, (ppid, _) in table.items():
        children.setdefault(ppid, []).append(p)

    safe = set()
    pid = self_pid
    while pid in table and pid not in safe and pid > 1:
        safe.add(pid)
        pid = table[pid][0]
    safe |= _closure({self_pid}, children)

    temp_dir = _temp_dir_pattern(ray_temp_dir)
    client = None
    if ray_address is not None and ray_address != IN_PROCESS:
        client = _client_server_pattern(ray_address)
    seeds = {
        p
        for p, (_, cmd) in table.items()
        if temp_dir.search(cmd)
        or (client is not None and _CLIENT_SERVER in cmd and client.search(cmd))
    }
    listed = _closure(seeds, children) - safe
    return [(p, table[p][0], table[p][1]) for p in sorted(listed)]


def _whose(ray_temp_dir, ray_address):
    """Whose processes a listing is of, for the commands' messages."""
    if ray_address is None or ray_address == IN_PROCESS:
        return f"of {ray_temp_dir}"
    return f"of {ray_temp_dir} or of the Ray client server for {ray_address}"


def _process_lines(processes):
    return [f"{p} {pp} {cmd[:COMMAND_WIDTH]}" for p, pp, cmd in processes]


def _remove_lock(lock_dir):
    for name in ("owner", "owner.tmp"):
        try:
            os.remove(lock_dir / name)
        except FileNotFoundError:
            pass
    os.rmdir(lock_dir)


def _release_again(lock_dir):
    try:
        _remove_lock(lock_dir)
    except OSError as exc:
        print(f"could not release the lock again ({exc})", file=sys.stderr)
        return
    print("released the lock again; not acquired", file=sys.stderr)


# ---- the commands ------------------------------------------------------------------------------


def acquire(project, purpose, ray_temp_dir, ray_address, *, lock_dir=None):
    """Take the lock for ``project``; returns the command's exit code (see the module docstring)."""
    _check_line("project", project)
    _check_line("purpose", purpose)
    _check_ray_temp_dir(ray_temp_dir)
    _check_ray_address(ray_address)
    d = _resolve(lock_dir)

    old = old_lock_dir()
    if os.path.lexists(old) and old.resolve() != d.resolve():
        print(
            f"the old location of the rehearsal lock exists ({old}); its owner file:",
            file=sys.stderr,
        )
        print(_indented(read_owner(old)), file=sys.stderr)
        print(
            "it is the old location: stop and ask the user, who removes it by hand once nothing "
            "holds it; nothing was created",
            file=sys.stderr,
        )
        return 3

    d.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.mkdir(d)  # never exist_ok: this is the atomic step
    except FileExistsError:
        print(f"the rehearsal lock is held ({d}); its owner file:", file=sys.stderr)
        print(_indented(read_owner(d)), file=sys.stderr)
        print(
            "stop and ask the user; nothing here waits on, retries or breaks the lock",
            file=sys.stderr,
        )
        return 3

    try:
        _replace_owner(d, owner_text(project, purpose, ray_temp_dir, ray_address, "-"))
    except OSError as exc:
        print(f"could not write the owner file ({exc}); releasing", file=sys.stderr)
        try:
            _remove_lock(d)
        except OSError:
            pass
        return 1

    try:
        procs = ray_processes(ray_temp_dir, ray_address)
    except (RuntimeError, OSError) as exc:
        print(f"cannot read the process table ({exc})", file=sys.stderr)
        _release_again(d)
        return 4
    if procs:
        print(
            f"processes {_whose(ray_temp_dir, ray_address)} are alive:", file=sys.stderr
        )
        for line in _process_lines(procs):
            print("    " + line, file=sys.stderr)
        _release_again(d)
        return 4

    print(f"acquired the rehearsal lock ({d}) for {project}: {purpose}")
    return 0


def _callers_lock(d, verb, project, ray_temp_dir):
    """``(owner_text, owner)`` if ``d`` is the caller's lock; otherwise prints why and returns ``None``."""
    if not d.is_dir():
        print(f"{verb}: there is no lock at {d}", file=sys.stderr)
        return None
    text = read_owner(d)
    if text is None:
        print(f"{verb}: the lock has no owner file; not touching it", file=sys.stderr)
        print(
            f"    lock: {d}\n    caller: project {project!r}, ray_temp_dir {ray_temp_dir!r}",
            file=sys.stderr,
        )
        return None
    owner = parse_owner(text)
    reason = _not_callers_reason(owner, project, ray_temp_dir)
    if reason is not None:
        print(
            f"{verb}: the lock is not the caller's ({reason}); not touching it",
            file=sys.stderr,
        )
        print("    owner:\n" + _indented(text), file=sys.stderr)
        print(
            f"    caller: project: {project}, ray_temp_dir: {ray_temp_dir}",
            file=sys.stderr,
        )
        return None
    return text, owner


def set_pid(project, ray_temp_dir, pid, *, lock_dir=None):
    """Record ``pid`` in the caller's lock, changing no other line; returns 0, or 1 if refused."""
    _check_line("project", project)
    _check_ray_temp_dir(ray_temp_dir)
    _check_pid(pid)
    d = _resolve(lock_dir)
    if not pid_alive(pid):
        print(f"set-pid: {pid} is not a live process; nothing changed", file=sys.stderr)
        return 1
    held = _callers_lock(d, "set-pid", project, ray_temp_dir)
    if held is None:
        return 1
    text, _ = held
    lines = text.splitlines(keepends=True)
    index = [i for i, line in enumerate(lines) if line.startswith("pid:")]
    if len(index) != 1:
        print(
            f"set-pid: the owner file has {len(index)} pid lines, not one; nothing changed",
            file=sys.stderr,
        )
        return 1
    old = lines[index[0]]
    ending = old[len(old.rstrip("\r\n")) :]
    lines[index[0]] = f"pid: {pid}" + ending
    _replace_owner(d, "".join(lines))
    print(f"recorded pid {pid} in {d / 'owner'}")
    return 0


def release(project, ray_temp_dir, *, lock_dir=None):
    """Remove the caller's lock once nothing of it is alive; returns 0, or 1 if refused."""
    _check_line("project", project)
    _check_ray_temp_dir(ray_temp_dir)
    d = _resolve(lock_dir)
    if not d.is_dir():
        print(f"no lock to release ({d})")
        return 0
    held = _callers_lock(d, "release", project, ray_temp_dir)
    if held is None:
        return 1
    _, owner = held
    pid = _recorded_pid(owner)
    if pid is not None and pid_alive(pid):
        print(
            f"release: the recorded pid {pid} is alive; not releasing", file=sys.stderr
        )
        return 1
    address = owner.get("ray_address")
    try:
        _check_ray_address(address)
    except ValueError:
        print(
            f"release: the owner's ray_address {address!r} is neither {IN_PROCESS!r} nor "
            "host:port, so its processes cannot be checked; not releasing",
            file=sys.stderr,
        )
        return 1
    try:
        procs = ray_processes(ray_temp_dir, address)
    except (RuntimeError, OSError) as exc:
        print(
            f"release: cannot read the process table ({exc}); not releasing",
            file=sys.stderr,
        )
        return 1
    if procs:
        print(
            f"release: processes {_whose(ray_temp_dir, address)} are alive:",
            file=sys.stderr,
        )
        for line in _process_lines(procs):
            print("    " + line, file=sys.stderr)
        return 1
    try:
        _remove_lock(d)
    except OSError as exc:
        print(f"release: could not remove {d} ({exc})", file=sys.stderr)
        return 1
    print(f"released the rehearsal lock ({d})")
    return 0


def status(ray_temp_dir=None, ray_address=None, *, lock_dir=None):
    """Print the lock, its owner, the old location and the processes; always returns 0."""
    if ray_temp_dir is None and ray_address is not None:
        raise ValueError("ray_address is given only with ray_temp_dir")
    if ray_temp_dir is not None:
        _check_ray_temp_dir(ray_temp_dir)
    if ray_address is not None:
        _check_ray_address(ray_address)
    d = _resolve(lock_dir)

    owner = None
    if d.is_dir():
        print(f"lock: HELD ({d})")
        text = read_owner(d)
        print(_indented(text))
        if text is not None:
            owner = parse_owner(text)
            pid = _recorded_pid(owner)
            if pid is None:
                print("owner pid: - (no pid recorded yet)")
            elif pid_alive(pid):
                print(f"owner pid {pid}: alive")
            else:
                print(f"owner pid {pid}: NOT alive")
    else:
        print(f"lock: free ({d} does not exist)")

    old = old_lock_dir()
    if os.path.lexists(old):
        print(f"old location: PRESENT ({old})")

    if ray_temp_dir is None:
        if owner is None:
            print("Ray processes: no temp dir given")
            return 0
        values = _usable_owner_values(owner)
        if values is None:
            print(
                "Ray processes: the owner's ray_temp_dir or ray_address is not usable"
            )
            return 0
        ray_temp_dir, ray_address = values
    try:
        procs = ray_processes(ray_temp_dir, ray_address)
    except (RuntimeError, OSError) as exc:
        print(f"Ray processes of {ray_temp_dir}: cannot read the process table ({exc})")
        return 0
    if not procs:
        print(f"Ray processes of {ray_temp_dir}: none")
    else:
        print(f"Ray processes of {ray_temp_dir}: {len(procs)}")
        for line in _process_lines(procs):
            print("    " + line)
    return 0


def ray_processes_command(ray_temp_dir, ray_address=None):
    """Print the processes of ``ray_temp_dir``, one per line; returns 0 none, 1 some or unreadable."""
    _check_ray_temp_dir(ray_temp_dir)
    if ray_address is not None:
        _check_ray_address(ray_address)
    try:
        procs = ray_processes(ray_temp_dir, ray_address)
    except (RuntimeError, OSError) as exc:
        print(f"cannot read the process table ({exc})", file=sys.stderr)
        return 1
    for line in _process_lines(procs):
        print(line)
    return 1 if procs else 0


# ---- the command line --------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="python -m raypoolkit.rehearsal_lock",
        description=(
            "The shared rehearsal lock. Never breaks, waits for or retries a lock; a held lock "
            "means stop and ask the user."
        ),
    )
    project = _argument(functools.partial(_check_line, "project"))
    purpose = _argument(functools.partial(_check_line, "purpose"))
    temp_dir = _argument(_check_ray_temp_dir)
    address = _argument(_check_ray_address)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "acquire",
        help="take the lock (exit 3 if held or the old location exists, 4 if a process is alive)",
    )
    p.add_argument("--project", required=True, type=project)
    p.add_argument("--purpose", required=True, type=purpose)
    p.add_argument("--ray-temp-dir", required=True, type=temp_dir)
    p.add_argument("--ray-address", required=True, type=address)

    p = sub.add_parser("set-pid", help="record a live pid in the caller's lock")
    p.add_argument("--project", required=True, type=project)
    p.add_argument("--ray-temp-dir", required=True, type=temp_dir)
    p.add_argument("pid", type=_pid_argument)

    p = sub.add_parser("release", help="release the caller's lock (exit 1 if refused)")
    p.add_argument("--project", required=True, type=project)
    p.add_argument("--ray-temp-dir", required=True, type=temp_dir)

    p = sub.add_parser(
        "status", help="the lock, its owner, the old location, and the processes"
    )
    p.add_argument("--ray-temp-dir", type=temp_dir)
    p.add_argument("--ray-address", type=address)

    p = sub.add_parser(
        "ray-processes", help="the processes of a temp dir (exit 1 if any)"
    )
    p.add_argument("--ray-temp-dir", required=True, type=temp_dir)
    p.add_argument("--ray-address", type=address)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "acquire":
        return acquire(args.project, args.purpose, args.ray_temp_dir, args.ray_address)
    if args.command == "set-pid":
        return set_pid(args.project, args.ray_temp_dir, args.pid)
    if args.command == "release":
        return release(args.project, args.ray_temp_dir)
    if args.command == "status":
        if args.ray_address is not None and args.ray_temp_dir is None:
            parser.error("status: --ray-address is given only with --ray-temp-dir")
        return status(args.ray_temp_dir, args.ray_address)
    return ray_processes_command(args.ray_temp_dir, args.ray_address)


if __name__ == "__main__":
    sys.exit(main())
