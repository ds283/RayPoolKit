#!/usr/bin/env python3
"""
Prove ``raypoolkit.rehearsal_lock`` under real Ray, holding the real shared lock (rehearsal-lock
prompt 02; made to hold the lock at both its locations by prompt 05).

The module's tests run on fixed process tables and never start Ray. This script is the one place
where the module meets Ray itself. It is not a test: the suite does not collect it, and it does
not run in CI.

**What it proves**, at the Ray it is run with, holding the shared lock as project ``RayPoolKit``
at **both** its locations: the default one (``~/.raypoolkit/rehearsal-lock``,
``lock_dir=default_lock_dir()``) and the old one (``~/ScienceData/.rehearsal-lock``,
``lock_dir=old_lock_dir()``). Every lock call names its location; none relies on a default. The
clients look at the old location until the switch-over and at the default one after it, and while
the module refuses to acquire beside the old location (``0.3.x``), the old one also stops a client
that has switched; so the proof is seen by every client on any day (the user's decision U7,
2026-10-24). Each part takes the default location first (the module refuses it while the old one
exists) and then the old one, before it starts Ray, and releases the old one first and then the
default one, once Ray is gone.

- **(a) An in-process instance** started with ``_temp_dir`` (``/tmp/ray-rpk02a``): the rule lists
  every Ray process that an independent witness finds, bar the reaper; ``release`` is refused while
  the instance is up, by its processes and then by its driver's pid; and allowed once the driver
  has called ``ray.shutdown()`` and exited.
- **(b) A ``ray start --head`` cluster** on ``/tmp/ray-rpk02b`` and ports 6420 (GCS), 6421 (client
  server), 8270 (dashboard) and 52370 (dashboard agent): the rule lists every process the witness
  finds, the Ray client server among them by its address; the script stops the cluster by
  signalling exactly what ``ray-processes`` listed, and nothing else; then nothing of it is left,
  its ports are free, and ``release`` succeeds.
- **(c) A second acquire is refused** while the lock is held: at the old location, as held; and at
  the default location, because the old one exists (the module checks that first). Neither owner
  file changes.

Straight after the two acquires, and before a part starts Ray, both owner files are checked: each
names ``RayPoolKit``, the part's temp dir and address, and ``pid: -``.

**How it is run.** From the repository root, with nothing of Ray running, with the interpreter of a
venv that has ``ray[default]`` and this package installed (the client server needs Ray's client
extras):

    env -u PYTHONPATH <venv>/bin/python docs/rehearsal-lock/ray_proof.py --record <scratch>/proof.json

and replayed, with no Ray and no lock, by:

    env -u PYTHONPATH <venv>/bin/python docs/rehearsal-lock/ray_proof.py --replay <scratch>/proof.json

The ``--record`` file keeps the full commands of the processes the checkpoints saw, the listings,
the witness and each check's verdict. It stays in a scratch directory and is never committed.
``--driver`` is the script's own driver mode, run by the script as its child.

**The witness.** At each checkpoint the script reads ``ps -axww -o pid= -o ppid= -o command=``
itself. The witness is: the processes absent from the part's reading taken just before it started
Ray; of those, each whose command contains this venv's ``site-packages/ray/`` directory (as
written, as ``os.path.realpath`` gives it, and either without a leading ``/private``), or
``ray.util.client.server``, or starts with ``ray::``; with every descendant of one; less the
script's own process and its children. It uses neither the temp dir nor the address. Beside it
are two readings of the rule: the **live** one (the ``ray-processes`` command, run as a child) and
the **offline** one, ``ray_processes(T, A, ps_text=<the script's reading>, self_pid=-1)``, the
rule on the very rows the witness came from with nothing held back (no row has pid or ppid -1;
pid 0 would hold back the whole table, since ``launchd``'s ppid is 0). A checkpoint repeats, one
second apart and at most 20 times, until two consecutive readings agree and the part's expectation
holds on them.

**What it never does.** It never runs ``ray stop``, never signals a process group, and never
signals anything but the stop list of part (b) (``ray-processes``'s listing at checkpoint b3) and,
when cleaning up after a failed check, its own driver. Immediately before each signal it reads the
pid's command and signals only if it is the command recorded for it. It never removes a lock: every
``acquire``, ``set_pid``, ``release`` and ``status`` is the module's own, in a fresh interpreter,
with an explicit ``lock_dir``. It never names a temp dir in its own command line or its driver's
(the driver reads its settings from stdin), since a process naming the temp dir would seed the
rule's walk. It sets
``RAY_USAGE_STATS_ENABLED=0`` for itself and every child before ``raypoolkit`` (and so ``ray``) is
imported, and passes ``--disable-usage-stats`` to ``ray start``.

**What it prints.** Every child's command (the lock children's code abbreviated), exit status,
stdout and stderr; one line per check, ``PASS`` or ``FAIL`` with what it saw; and a summary.
Process rows are cut: a ``ray::`` command keeps its first word only (a process that rewrites its
title can show its environment after it on macOS), any other is cut at 150 characters; the venv
is written ``<venv>``, the record's directory ``<scratch>`` and the home directory ``~``.

**Exit status.** 0 every check passed; 1 a check failed, and everything was stopped and the lock
released; 2 refused to start (a Ray process, a process naming a temp dir, a held port, a ``RAY_*``
variable, a record path naming a temp dir), nothing touched; 3 the shared lock is held by someone
else (either location exists before the run, or an ``acquire`` exits 3), and nothing of it is
held (a default location taken before the old one refused is released again); 4 something could
not be cleaned up, and the lock is left held at the location named: stop and ask the user.

``--replay`` reads a record of either form: 02's, which held the old location alone, or this
one's, which records both locations.
"""

import os

# Before ``raypoolkit`` (whose package root imports ``ray``) is imported, so every child inherits it.
_REFUSED_RAY_VARIABLES = sorted(
    name
    for name in os.environ
    if name.startswith("RAY_") and name != "RAY_USAGE_STATS_ENABLED"
)
os.environ["RAY_USAGE_STATS_ENABLED"] = "0"

import argparse
import importlib.metadata
import importlib.util
import json
import queue
import re
import select
import signal
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from pathlib import Path

import raypoolkit
import raypoolkit.rehearsal_lock as rl

SCRIPT = Path(__file__).resolve()

TEMP_A = "/tmp/ray-rpk02a"
TEMP_B = "/tmp/ray-rpk02b"
TEMP_C = "/tmp/ray-rpk02c"
TEMP_DIRS = (TEMP_A, TEMP_B, TEMP_C)
ADDRESS_B = "127.0.0.1:6420"
PORTS = (
    ("GCS", 6420),
    ("client server", 6421),
    ("dashboard", 8270),
    ("dashboard agent", 52370),
)
NUM_CPUS = 2
PROJECT = "RayPoolKit"
SECOND_PROJECT = "RayPoolKitSecond"

# The lock's two locations (U7), each computed when called; acquired default first, released
# old first.
LOCATIONS = {"default": rl.default_lock_dir, "old": rl.old_lock_dir}
ACQUIRE_ORDER = ("default", "old")
RELEASE_ORDER = ("old", "default")

OFFLINE_SELF_PID = -1
SETTLE_READINGS = 20
GRACE = 15
DRIVER_READY_WAIT = 300
DRIVER_REPLY_WAIT = 120
DRIVER_EXIT_WAIT = 30
DRIVER_SILENCE = 300
RAY_PATTERN = "gcs_server|raylet|ray::"
REAPER_MARK = "ray/_private/ray_process_reaper.py"
CLIENT_SERVER = "ray.util.client.server"
WIDTH = 150

_PS_ROW = re.compile(r"^\s*([0-9]+)\s+([0-9]+)(?:\s+(.*))?$")
_LISTED_ROW = re.compile(r"^([0-9]+) ([0-9]+)(?: |$)")
_PROCESS_LINE = re.compile(r"^(\s*[0-9]+ [0-9]+ )(.*)$")
# A framework build's interpreter, as ``ps`` shows a venv's ``python``.
_FRAMEWORK_PYTHON = re.compile(
    r"\S*/Python\.framework/Versions/[^/\s]+/Resources/Python\.app/Contents/MacOS/Python\b"
)

# The code of every lock child: one function of the module, at the location its payload names,
# always passed as ``lock_dir``; a location it does not know is an exit, never a default.
LOCK_CODE = """\
import json, sys
import raypoolkit.rehearsal_lock as rl
a = json.loads(sys.argv[1])
if a["function"] not in ("acquire", "set_pid", "release", "status"):
    sys.exit("not a lock function: " + repr(a["function"]))
dirs = {"default": rl.default_lock_dir, "old": rl.old_lock_dir}
if a.get("location") not in dirs:
    sys.exit("not a lock location: " + repr(a.get("location")))
sys.exit(getattr(rl, a["function"])(*a["args"], lock_dir=dirs[a["location"]]()))
"""


class CheckFailed(Exception):
    """A check failed; the part stops and cleans up."""


class Interrupted(BaseException):
    """SIGTERM or SIGHUP reached the script; the part stops and cleans up."""


class LeftHeld(Exception):
    """The cleanup could not finish; the lock is left held (exit 4)."""


class HeldByOther(Exception):
    """``acquire`` exited 3: the shared lock is someone else's; nothing is touched (exit 3)."""


# ---- reading the process table ------------------------------------------------------------------


def parse_table(text):
    table = {}
    for line in text.splitlines():
        m = _PS_ROW.match(line)
        if m:
            table[int(m.group(1))] = (int(m.group(2)), m.group(3) or "")
    return table


def read_ps():
    result = subprocess.run(rl.PS_COMMAND, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ps exited {result.returncode}: {result.stderr.strip()}")
    return result.stdout


def descendants(start, table):
    children = {}
    for p, (pp, _) in table.items():
        children.setdefault(pp, []).append(p)
    found = set(start)
    todo = list(start)
    while todo:
        for c in children.get(todo.pop(), ()):
            if c not in found:
                found.add(c)
                todo.append(c)
    return found


def ancestors(pid, table):
    found = set()
    while pid in table and pid not in found and pid > 1:
        found.add(pid)
        pid = table[pid][0]
    return found


def ray_dir_spellings():
    """This venv's ``site-packages/ray/``: as found, its realpath, and each without ``/private``."""
    spec = importlib.util.find_spec("ray")
    written = os.path.dirname(spec.origin)
    out = []
    for d in (written, os.path.realpath(written)):
        for s in (d, d[len("/private") :] if d.startswith("/private/") else d):
            s = s.rstrip("/") + "/"
            if s not in out:
                out.append(s)
    return out


def witness(table, pre_pids, me, spellings):
    """The independent listing: new, Ray's by the venv's path or Ray's titles, and descendants."""
    new = set(table) - pre_pids
    rays = {
        p
        for p in new
        if any(s in table[p][1] for s in spellings)
        or CLIENT_SERVER in table[p][1]
        or table[p][1].startswith("ray::")
    }
    mine = {me} | {p for p, (pp, _) in table.items() if pp == me}
    return descendants(rays, table) - mine


def offline_listing(ps_text, temp_dir, address):
    procs = rl.ray_processes(
        temp_dir, address, ps_text=ps_text, self_pid=OFFLINE_SELF_PID
    )
    return {p for p, _, _ in procs}


def names_temp_dir(text, temp_dir):
    d = temp_dir[len("/private") :] if temp_dir.startswith("/private/") else temp_dir
    return d in text


def command_now(pid):
    """The command of ``pid`` now, or ``None`` if there is no such process."""
    result = subprocess.run(
        ["ps", "-ww", "-o", "command=", "-p", str(pid)], capture_output=True, text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return result.stdout.rstrip("\n")


def port_listeners(port):
    result = subprocess.run(
        ["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN"], capture_output=True, text=True
    )
    return [line for line in result.stdout.splitlines()[1:] if line.strip()]


def lock_dir(location):
    """The lock directory at ``location`` (``default`` or ``old``), computed now, as the module does."""
    return LOCATIONS[location]()


# ---- the expectations, shared by the run and the replay -----------------------------------------


def _fmt(pids):
    return "[" + ", ".join(str(p) for p in sorted(pids)) + "]"


def _diff(name, got, want):
    if got == want:
        return []
    return [
        f"{name} {_fmt(got)} is not {_fmt(want)} "
        f"(extra {_fmt(got - want)}, missing {_fmt(want - got)})"
    ]


def _client_servers(view, pids):
    return sorted(p for p in pids if CLIENT_SERVER in view["rows"][p][1])


def _client_server_of(cmd, address):
    return re.search(r"--address=" + re.escape(address) + r"(?: |$)", cmd) is not None


def evaluate(kind, view):
    """
    The part's expectation at a checkpoint: ``(problems, facts)``. ``view`` holds ``rows``
    (pid -> (ppid, command)), the sets ``witness``, ``live``, ``offline`` (and ``live_na``,
    ``offline_na``, the listings without the address, in part (b)), and ``extra`` (the driver's
    pid, its workers, the ports). Used by the run and by ``--replay`` alike.
    """
    rows = view["rows"]
    w, live, off = view["witness"], view["live"], view["offline"]
    extra = view.get("extra", {})
    problems, facts = [], {}
    driver = extra.get("driver_pid")
    actor = extra.get("actor")
    tasks = set(extra.get("tasks", []))
    # The actor is held by the driver, so it must be alive; a task's worker may have been ended
    # by Ray as a surplus idle worker, so it must be listed only while it is alive (in the rows).
    workers = ({actor} if actor is not None else set()) | (tasks & set(rows))

    def driver_absent():
        if driver is not None and driver in (w | live | off):
            problems.append(f"the driver {driver} is in the witness or a listing")

    def workers_listed():
        facts["task workers alive"] = f"{len(tasks & set(rows))} of {len(tasks)}"
        missing = workers - (live & off & w)
        if missing:
            problems.append(
                f"workers {_fmt(missing)} are not in the witness and both listings"
            )

    if kind == "a1":
        reapers = sorted(p for p in w if REAPER_MARK in rows[p][1])
        facts["reaper"] = reapers
        if len(reapers) != 1:
            problems.append(
                f"{len(reapers)} reapers in the witness, not one: {reapers}"
            )
        want = w - set(reapers)
        problems += _diff("live", live, want) + _diff("offline", off, want)
        if not want:
            problems.append("the witness minus the reaper is empty")
        driver_absent()
        workers_listed()
    elif kind == "a2":
        reapers = sorted(p for p in w if REAPER_MARK in rows[p][1])
        facts["reaper_alive"] = bool(reapers)
        problems += _diff("witness minus the reaper", w - set(reapers), set())
        problems += _diff("live", live, set()) + _diff("offline", off, set())
    elif kind in ("a3", "b4"):
        problems += _diff("witness", w, set())
        problems += _diff("live", live, set()) + _diff("offline", off, set())
        if kind == "b4":
            problems += _diff("live without the address", view["live_na"], set())
            problems += _diff("offline without the address", view["offline_na"], set())
            held = {str(p): v for p, v in extra.get("ports", {}).items() if v}
            if held:
                problems.append(f"ports held: {sorted(held)}")
    elif kind in ("b1", "b2", "b3"):
        problems += _diff("live", live, w) + _diff("offline", off, w)
        if not w:
            problems.append("the witness is empty")
        gcs = sorted(p for p in live if "gcs_server" in rows.get(p, (0, ""))[1])
        facts["gcs_server"] = gcs
        if len(gcs) != 1:
            problems.append(
                f"{len(gcs)} listed processes name gcs_server, not one: {gcs}"
            )
        driver_absent()
        if kind == "b2":
            workers_listed()
            raylets = sorted(
                p
                for p in live
                if os.path.basename(rows.get(p, (0, ""))[1].split(" ")[0]) == "raylet"
            )
            facts["raylet"] = raylets
            for p in sorted(workers & set(rows)):
                cmd = rows[p][1]
                if not (set(raylets) & ancestors(p, rows)):
                    problems.append(
                        f"worker {p} is not a descendant of the raylet {raylets}"
                    )
                if names_temp_dir(cmd, view["temp_dir"]) or view["address"] in cmd:
                    problems.append(f"worker {p} names the temp dir or the address")
    elif kind == "b1cs":
        servers = _client_servers(view, w)
        facts["client_server"] = servers
        if not servers:
            return ["NOT EXERCISED: no Ray client server in the witness"], facts
        for p in servers:
            cmd = rows[p][1]
            facts[f"client_server {p} names the temp dir"] = names_temp_dir(
                cmd, view["temp_dir"]
            )
            if not _client_server_of(cmd, view["address"]):
                problems.append(
                    f"the client server {p}'s --address is not {view['address']}"
                )
        tree = descendants(set(servers), rows)
        facts["client_server_tree"] = sorted(tree)
        problems += _diff("live without the address", view["live_na"], live - tree)
        problems += _diff("offline without the address", view["offline_na"], off - tree)
    else:
        raise ValueError(f"no expectation {kind!r}")
    return problems, facts


# ---- the driver mode ----------------------------------------------------------------------------


def driver_main():
    """Read settings from stdin, start or attach to Ray, run four tasks and an actor, obey stdin."""
    buffer = b""

    def read_line(timeout):
        nonlocal buffer
        deadline = time.monotonic() + timeout
        while b"\n" not in buffer:
            left = deadline - time.monotonic()
            if left <= 0:
                return None
            ready, _, _ = select.select([0], [], [], left)
            if ready:
                chunk = os.read(0, 4096)
                if not chunk:
                    return ""
                buffer += chunk
        line, _, buffer = buffer.partition(b"\n")
        return line.decode()

    first = read_line(DRIVER_SILENCE)
    if not first:
        print("NO SETTINGS", flush=True)
        return 3
    settings = json.loads(first)

    import ray

    kwargs = {"address": settings["address"], "log_to_driver": False}
    if settings.get("temp_dir"):
        kwargs.update(
            _temp_dir=settings["temp_dir"], num_cpus=NUM_CPUS, include_dashboard=False
        )
    ray.init(**kwargs)

    @ray.remote
    class A:
        def pid(self):
            return os.getpid()

    @ray.remote
    def f():
        return os.getpid()

    actor = A.remote()
    tasks = sorted(set(ray.get([f.remote() for _ in range(4)])))
    actor_pid = ray.get(actor.pid.remote())
    print("WORKERS " + json.dumps({"tasks": tasks, "actor": actor_pid}), flush=True)
    print(f"READY {os.getpid()}", flush=True)
    while True:
        line = read_line(DRIVER_SILENCE)
        if line is None or line == "":
            print("TIMEOUT" if line is None else "EOF", flush=True)
            if ray.is_initialized():
                ray.shutdown()
            return 3
        command = line.strip()
        if command == "shutdown":
            actor = None
            ray.shutdown()
            print("SHUTDOWN", flush=True)
        elif command == "exit":
            if ray.is_initialized():
                ray.shutdown()
            print("EXIT", flush=True)
            return 0
        else:
            print(f"UNKNOWN {command!r}", flush=True)


# ---- the proof ----------------------------------------------------------------------------------


class Proof:
    def __init__(self, record_path):
        self.record_path = Path(record_path)
        self.scratch = self.record_path.parent
        self.stem = self.record_path.stem
        self.me = os.getpid()
        self.home = str(Path.home())
        self.spellings = ray_dir_spellings()
        self.venv = str(Path(sys.executable).parent.parent)
        self.ray_bin = Path(sys.executable).parent / "ray"
        self.python_version = sys.version.split()[0]
        self.ray_version = importlib.metadata.version("ray")
        self.cwd = None
        self.results = []
        self.record = {
            "python": sys.version,
            "ray": self.ray_version,
            "raypoolkit": raypoolkit.__file__,
            "executable": sys.executable,
            "ray_dir_spellings": self.spellings,
            "offline_self_pid": OFFLINE_SELF_PID,
            "lock_dirs": {loc: str(lock_dir(loc)) for loc in LOCATIONS},
            "acquire_order": list(ACQUIRE_ORDER),
            "release_order": list(RELEASE_ORDER),
            "checkpoints": [],
            "checks": [],
        }
        self._interrupted = False

    # -- printing --

    def _abbreviate(self, text):
        for venv in sorted(
            {self.venv, os.path.realpath(self.venv)}
            | {
                v[len("/private") :]
                for v in (self.venv, os.path.realpath(self.venv))
                if v.startswith("/private/")
            },
            key=len,
            reverse=True,
        ):
            text = text.replace(venv, "<venv>")
        scratch = str(self.scratch)
        for s in sorted(
            {scratch, os.path.realpath(scratch)}
            | {
                v[len("/private") :]
                for v in (scratch, os.path.realpath(scratch))
                if v.startswith("/private/")
            },
            key=len,
            reverse=True,
        ):
            text = text.replace(s, "<scratch>")
        text = _FRAMEWORK_PYTHON.sub("<python>", text)
        return text.replace(self.home, "~")

    def cut(self, cmd):
        if cmd.startswith("ray::"):
            return cmd.split()[0] if cmd.split() else cmd
        return self._abbreviate(cmd)[:WIDTH]

    def clean(self, line):
        m = _PROCESS_LINE.match(line)
        if m:
            return m.group(1) + self.cut(m.group(2))
        return self._abbreviate(line)

    def say(self, text=""):
        for line in str(text).splitlines() or [""]:
            print(self.clean(line), flush=True)

    def show_output(self, label, text):
        lines = text.splitlines()
        if not lines:
            self.say(f"    {label}: (empty)")
            return
        self.say(f"    {label}:")
        for line in lines:
            self.say("      " + line)

    def check(self, name, ok, detail):
        verdict = "PASS" if ok else "FAIL"
        self.results.append((name, verdict))
        self.record["checks"].append(
            {"name": name, "verdict": verdict, "detail": detail}
        )
        self.say(f"{verdict} {name}: {detail}")
        self.save()
        if not ok:
            raise CheckFailed(f"{name}: {detail}")

    def note(self, name, verdict, detail):
        self.results.append((name, verdict))
        self.record["checks"].append(
            {"name": name, "verdict": verdict, "detail": detail}
        )
        self.say(f"{verdict} {name}: {detail}")
        self.save()

    def save(self):
        tmp = self.record_path.with_name(self.record_path.name + ".tmp")
        tmp.write_text(json.dumps(self.record, indent=1, sort_keys=True) + "\n")
        os.replace(tmp, self.record_path)

    # -- children --

    def lock_call(self, function, *args, location):
        payload = json.dumps(
            {"function": function, "args": list(args), "location": location}
        )
        self.say(f"  $ {sys.executable} -I -c LOCK_CODE '{payload}'")
        result = subprocess.run(
            [sys.executable, "-I", "-c", LOCK_CODE, payload],
            cwd=self.cwd,
            capture_output=True,
            text=True,
        )
        self.say(f"    exit {result.returncode}")
        self.show_output("stdout", result.stdout)
        self.show_output("stderr", result.stderr)
        if "Traceback" in result.stderr:
            raise CheckFailed(f"{function} ended in a traceback")
        return result.returncode, result.stdout, result.stderr

    def live_listing(self, temp_dir, address):
        argv = [
            sys.executable,
            "-I",
            "-m",
            "raypoolkit.rehearsal_lock",
            "ray-processes",
            "--ray-temp-dir",
            temp_dir,
        ]
        if address is not None:
            argv += ["--ray-address", address]
        result = subprocess.run(argv, cwd=self.cwd, capture_output=True, text=True)
        pids = set()
        for line in result.stdout.splitlines():
            m = _LISTED_ROW.match(line)
            if not m:
                raise CheckFailed("ray-processes printed a line that is not a row")
            pids.add(int(m.group(1)))
        if (
            result.returncode not in (0, 1)
            or result.stderr.strip()
            or (result.returncode == 1) != bool(pids)
        ):
            self.say(f"  $ {' '.join(argv)}")
            self.say(f"    exit {result.returncode}")
            self.show_output("stderr", result.stderr)
            raise CheckFailed(f"ray-processes exited {result.returncode}")
        return pids, argv, result.returncode

    def owner_bytes(self):
        """Both owner files' bytes, by location (``None`` where there is none)."""
        out = {}
        for loc in LOCATIONS:
            try:
                out[loc] = (lock_dir(loc) / "owner").read_bytes()
            except (FileNotFoundError, NotADirectoryError):
                out[loc] = None
        return out

    def show_owner(self, label="owner file"):
        data = self.owner_bytes()
        for loc in LOCATIONS:
            self.say(f"  {label}, {loc} location ({lock_dir(loc) / 'owner'}):")
            if data[loc] is None:
                self.say("    (none)")
            else:
                for line in data[loc].decode("utf-8", "replace").splitlines():
                    self.say("    " + line)
        return data

    # -- readings and checkpoints --

    def reading(self, part, with_noaddr, ports):
        text = read_ps()
        table = parse_table(text)
        w = witness(table, part["pre_pids"], self.me, self.spellings)
        live, live_argv, _ = self.live_listing(part["temp_dir"], part["address"])
        off = offline_listing(text, part["temp_dir"], part["address"])
        r = {"table": table, "witness": w, "live": live, "offline": off}
        r["argv"] = [live_argv]
        if with_noaddr:
            r["live_na"], argv_na, _ = self.live_listing(part["temp_dir"], None)
            r["offline_na"] = offline_listing(text, part["temp_dir"], None)
            r["argv"].append(argv_na)
        if ports:
            r["ports"] = {str(p): bool(port_listeners(p)) for _, p in PORTS}
        return r

    @staticmethod
    def _key(r):
        return tuple(
            (k, tuple(sorted(r[k])) if isinstance(r[k], set) else json.dumps(r[k]))
            for k in ("witness", "live", "offline", "live_na", "offline_na", "ports")
            if k in r
        )

    def checkpoint(self, part, name, kind, extra=None, extra_kinds=()):
        """Read until two consecutive readings agree and the expectation holds on them."""
        with_noaddr = part["address"] is not None
        ports = part["name"] == "b"
        self.say(f"checkpoint {name} ({kind}):")
        prev = None
        problems = ["no reading"]
        for n in range(1, SETTLE_READINGS + 1):
            if n > 1:
                time.sleep(1)
            r = self.reading(part, with_noaddr, ports)
            settled = prev is not None and self._key(prev) == self._key(r)
            view = self._view(part, r, extra)
            problems, facts = evaluate(kind, view)
            line = (
                f"  reading {n}: witness {_fmt(r['witness'])}; live {_fmt(r['live'])}; "
                f"offline {_fmt(r['offline'])}"
            )
            if with_noaddr:
                line += (
                    f"; without the address live {_fmt(r['live_na'])}, "
                    f"offline {_fmt(r['offline_na'])}"
                )
            if ports:
                line += f"; ports held {[p for p, v in r['ports'].items() if v]}"
            line += "; settled" if settled else ""
            if problems:
                line += f"; {len(problems)} problem(s), the first: {problems[0]}"
            self.say(line)
            prev = r
            if settled and not problems:
                break
        for argv in r["argv"]:
            self.say(f"  live listing: $ {' '.join(argv)}")
        cp = self._record_checkpoint(part, name, kind, r, view, n, settled, facts)
        self._show_rows(cp, r["table"])
        ok = settled and not problems
        detail = (
            f"settled after {n} readings; "
            if settled
            else f"not settled in {n} readings; "
        ) + ("; ".join(problems) if problems else f"as expected; {facts}")
        cp["verdict"] = "PASS" if ok else "FAIL"
        cp["problems"] = problems
        results = {}
        for extra_kind in extra_kinds:
            p2, f2 = evaluate(extra_kind, view)
            cp.setdefault("extra_kinds", {})[extra_kind] = {"problems": p2, "facts": f2}
            results[extra_kind] = (p2, f2)
        self.check(name, ok, detail)
        return r, view, facts, results

    def _view(self, part, r, extra):
        listed = set(r["witness"]) | r["live"] | r["offline"]
        listed |= r.get("live_na", set()) | r.get("offline_na", set())
        table = r["table"]
        rows = {p: table[p] for p in listed if p in table}
        e = dict(extra or {})
        if "ports" in r:
            e["ports"] = r["ports"]
        view = {
            "rows": rows,
            "witness": set(r["witness"]),
            "live": set(r["live"]),
            "offline": set(r["offline"]),
            "temp_dir": part["temp_dir"],
            "address": part["address"],
            "extra": e,
        }
        if "live_na" in r:
            view["live_na"] = set(r["live_na"])
            view["offline_na"] = set(r["offline_na"])
        return view

    def _record_checkpoint(self, part, name, kind, r, view, n, settled, facts):
        table = r["table"]
        parents = {}
        for p, (pp, _) in view["rows"].items():
            if pp not in view["rows"] and pp in table:
                words = table[pp][1].split()
                parents[str(pp)] = words[0] if words else ""
        cp = {
            "name": name,
            "kind": kind,
            "part": part["name"],
            "temp_dir": part["temp_dir"],
            "address": part["address"],
            "readings": n,
            "settled": settled,
            "rows": {str(p): list(v) for p, v in sorted(view["rows"].items())},
            "witness": sorted(view["witness"]),
            "live": sorted(view["live"]),
            "offline": sorted(view["offline"]),
            "extra": view["extra"],
            "facts": facts,
            "outside_parents": parents,
        }
        if "live_na" in view:
            cp["live_na"] = sorted(view["live_na"])
            cp["offline_na"] = sorted(view["offline_na"])
        self.record["checkpoints"].append(cp)
        return cp

    def _show_rows(self, cp, table):
        if not cp["rows"]:
            self.say("  rows: none")
            return
        self.say("  rows (W witness, L live, O offline; l, o without the address):")
        for p in sorted(int(k) for k in cp["rows"]):
            pp, cmd = cp["rows"][str(p)]
            tags = (
                ("W" if p in cp["witness"] else "-")
                + ("L" if p in cp["live"] else "-")
                + ("O" if p in cp["offline"] else "-")
            )
            if "live_na" in cp:
                tags += ("l" if p in cp["live_na"] else "-") + (
                    "o" if p in cp["offline_na"] else "-"
                )
            self.say(f"    {tags} {p} {pp} {self.cut(cmd)}")
        for pp, word in sorted(cp["outside_parents"].items(), key=lambda x: int(x[0])):
            self.say(f"  parent outside the rows: {pp} {self.cut(word)}")

    # -- the driver --

    def start_driver(self, part, settings):
        stderr_path = self.scratch / f"{self.stem}-driver-{part['name']}.txt"
        argv = [sys.executable, "-I", str(SCRIPT), "--driver"]
        self.say(f"  $ {' '.join(argv)}   (stderr to {stderr_path})")
        self.say(f"    stdin: {json.dumps(settings)}")
        stderr = open(stderr_path, "w")
        proc = subprocess.Popen(
            argv,
            cwd=self.cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=stderr,
            text=True,
            bufsize=1,
        )
        stderr.close()
        lines = queue.Queue()

        def pump():
            for line in proc.stdout:
                lines.put(line.rstrip("\n"))
            lines.put(None)

        threading.Thread(target=pump, daemon=True).start()
        part["driver"] = {"proc": proc, "lines": lines, "stderr": stderr_path}
        proc.stdin.write(json.dumps(settings) + "\n")
        proc.stdin.flush()
        return proc

    def driver_expect(self, part, word, timeout):
        d = part["driver"]
        deadline = time.monotonic() + timeout
        while True:
            left = deadline - time.monotonic()
            if left <= 0:
                return None
            try:
                line = d["lines"].get(timeout=left)
            except queue.Empty:
                return None
            if line is None:
                return None
            self.say(f"    driver: {line}")
            if line.split(" ")[0] == word:
                return line

    def driver_send(self, part, command):
        self.say(f"  driver <- {command}")
        d = part["driver"]
        d["proc"].stdin.write(command + "\n")
        d["proc"].stdin.flush()

    def driver_wait(self, part, timeout):
        d = part["driver"]
        try:
            code = d["proc"].wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            return None
        return code

    def show_driver_stderr(self, part):
        d = part.get("driver")
        if d:
            self.show_output(
                f"driver stderr ({d['stderr']})", Path(d["stderr"]).read_text()
            )

    # -- signals --

    def guard(self, pid):
        """Never pid 1 or less, never this process or an ancestor of it."""
        table = parse_table(read_ps())
        if pid <= 1 or pid == self.me or pid in ancestors(self.me, table):
            raise AssertionError(
                f"refusing to signal {pid}: pid 1 or less, or this script's line"
            )

    def signal_if_same(self, pid, recorded, sig):
        """Signal ``pid`` only if its command now is the one recorded for it."""
        self.guard(pid)
        now = command_now(pid)
        if now is None:
            self.say(f"    {pid}: gone; nothing sent")
            return False
        if now.rstrip() != recorded.rstrip():
            self.say(f"    {pid}: its command is not the recorded one; nothing sent")
            self.say(f"      recorded: {self.cut(recorded)}")
            self.say(f"      now:      {self.cut(now)}")
            return False
        os.kill(pid, sig)
        self.say(f"    {sig.name} -> {pid} {self.cut(recorded)}")
        return True

    def alive_as_recorded(self, pid, recorded):
        now = command_now(pid)
        return now is not None and now.rstrip() == recorded.rstrip()

    def stop(self, stop_list):
        """SIGTERM each pid of the stop list; a grace of GRACE s; SIGKILL to each still alive."""
        self.record.setdefault("stops", []).append(
            {
                pid: cmd
                for pid, cmd in ((str(p), c) for p, c in sorted(stop_list.items()))
            }
        )
        self.say(f"  the stop list ({len(stop_list)}): {_fmt(stop_list)}")
        sent = {}
        for pid, cmd in sorted(stop_list.items()):
            sent[pid] = self.signal_if_same(pid, cmd, signal.SIGTERM)
        deadline = time.monotonic() + GRACE
        while time.monotonic() < deadline:
            if not any(self.alive_as_recorded(p, c) for p, c in stop_list.items()):
                break
            time.sleep(0.5)
        left = sorted(p for p, c in stop_list.items() if self.alive_as_recorded(p, c))
        self.say(f"  after the grace ({GRACE} s at most): still alive {_fmt(left)}")
        for pid in left:
            self.signal_if_same(pid, stop_list[pid], signal.SIGKILL)
        if left:
            time.sleep(1)
        return left

    def stop_driver(self, part):
        d = part.get("driver")
        if not d or d["proc"].poll() is not None:
            return
        proc = d["proc"]
        try:
            self.driver_send(part, "exit")
        except OSError as exc:
            self.say(f"  could not write to the driver ({exc})")
        if self.driver_wait(part, DRIVER_EXIT_WAIT) is None:
            recorded = part.get("driver_command")
            if recorded is None:
                recorded = command_now(proc.pid)
            for sig, wait in ((signal.SIGTERM, 10), (signal.SIGKILL, 5)):
                if recorded is not None:
                    self.signal_if_same(proc.pid, recorded, sig)
                if self.driver_wait(part, wait) is not None:
                    break
        self.say(f"  driver exit status: {proc.poll()}")

    # -- preflight --

    def preflight(self):
        self.say(
            f"the lock, default location: {lock_dir('default')} "
            "(where every client looks after the switch-over)"
        )
        self.say(
            f"the lock, old location: {lock_dir('old')} "
            "(where the clients look until the switch-over)"
        )
        print(f"~ is {self.home}", flush=True)
        self.say(f"python: {sys.version}")
        self.say(f"executable: {sys.executable}")
        self.say(f"ray: {self.ray_version} ({importlib.util.find_spec('ray').origin})")
        self.say(f"raypoolkit.__file__: {raypoolkit.__file__}")
        self.say(f"this venv's ray directory, as matched: {self.spellings}")
        self.say(
            f"RAY_USAGE_STATS_ENABLED: {os.environ.get('RAY_USAGE_STATS_ENABLED')}"
        )
        refused = []
        if _REFUSED_RAY_VARIABLES:
            refused.append(
                f"RAY_* variables in the environment: {_REFUSED_RAY_VARIABLES}"
            )
        paths = {str(self.record_path), str(self.scratch)}
        paths |= {os.path.realpath(p) for p in paths}
        for p in sorted(paths):
            if any(names_temp_dir(p, t) for t in TEMP_DIRS):
                refused.append(f"the record path names a temp dir: {p}")
        if not self.scratch.is_dir():
            refused.append(f"the record's directory does not exist: {self.scratch}")
        if not self.ray_bin.exists():
            refused.append(f"{self.ray_bin} does not exist")
        if refused:
            for r in refused:
                self.say(f"REFUSED: {r}")
            return 2
        present = [loc for loc in LOCATIONS if os.path.lexists(lock_dir(loc))]
        for loc in present:
            self.say(
                f"REFUSED: the shared lock exists at its {loc} location ({lock_dir(loc)}); "
                "its owner file:"
            )
            self.say(rl._indented(rl.read_owner(lock_dir(loc))))
        if present:
            self.say("it is someone's: stop and ask the user")
            return 3

        result = subprocess.run(
            ["pgrep", "-lf", RAY_PATTERN], capture_output=True, text=True
        )
        if result.returncode != 1:
            self.say(f"REFUSED: pgrep -lf '{RAY_PATTERN}' exited {result.returncode}:")
            for line in result.stdout.splitlines():
                self.say("  " + " ".join(line.split()[:2]))
            return 2
        self.say(f"pgrep -lf '{RAY_PATTERN}': no process")
        self.cwd = tempfile.mkdtemp(prefix=f"{self.stem}-cwd-", dir=self.scratch)
        for temp_dir, address in ((TEMP_A, None), (TEMP_B, ADDRESS_B), (TEMP_C, None)):
            pids, argv, code = self.live_listing(temp_dir, address)
            self.say(f"$ {' '.join(argv)}  -> exit {code}, {_fmt(pids)}")
            if pids:
                self.say(f"REFUSED: processes name {temp_dir}")
                return 2
        held = []
        for label, port in PORTS:
            listeners = port_listeners(port)
            self.say(f"port {port} ({label}): {'HELD' if listeners else 'free'}")
            if listeners:
                held.append(port)
        if held:
            self.say(f"REFUSED: ports held: {held}")
            return 2
        self.raypoolkit_dir = Path(self.home) / ".raypoolkit"
        self.raypoolkit_before = os.path.lexists(self.raypoolkit_dir)
        self.say(
            f"{self.raypoolkit_dir}: {'exists' if self.raypoolkit_before else 'does not exist'}"
        )
        self.record["preflight"] = {
            "raypoolkit_dir_exists": self.raypoolkit_before,
            "lock_exists": {loc: False for loc in LOCATIONS},
        }
        return 0

    # -- the steps shared by the parts --

    def acquire_step(self, part, label, purpose):
        """The default location, then the old one; then both owner files are checked."""
        args = (PROJECT, purpose, part["temp_dir"], part["address"] or "in-process")
        for loc in ACQUIRE_ORDER:
            code, out, _ = self.lock_call("acquire", *args, location=loc)
            if code == 3:
                self.note(
                    f"{label} ({loc})",
                    "FAIL",
                    f"acquire at the {loc} location exited 3: the lock is someone else's",
                )
                raise HeldByOther(label)
            if code == 0:
                part["held"][loc] = True
            self.check(
                f"{label} ({loc})",
                code == 0 and "acquired" in out,
                f"acquire at the {loc} location exited {code}",
            )
        self.owner_files_step(part, f"{label}-owner-files")

    def owner_files_step(self, part, label):
        """Both owner files exist, each naming this project, the part's temp dir and address."""
        want = {
            "project": PROJECT,
            "ray_temp_dir": part["temp_dir"],
            "ray_address": part["address"] or "in-process",
            "pid": "-",
        }
        problems = []
        for loc in LOCATIONS:
            text = rl.read_owner(lock_dir(loc))
            if text is None:
                problems.append(f"the {loc} location has no owner file")
                continue
            owner = rl.parse_owner(text)
            wrong = {k: owner.get(k) for k, v in want.items() if owner.get(k) != v}
            if wrong:
                problems.append(f"the {loc} location's owner file has {wrong}")
        self.show_owner()
        self.check(
            label,
            not problems,
            (
                "; ".join(problems)
                if problems
                else f"both owner files exist, each with {want}"
            ),
        )

    def release_refused(self, part, label, reason):
        for loc in RELEASE_ORDER:
            before = self.owner_bytes()
            code, _, err = self.lock_call(
                "release", PROJECT, part["temp_dir"], location=loc
            )
            after = self.owner_bytes()
            if reason == "processes":
                saw = (
                    "release: processes of" in err
                    and "release: the recorded pid" not in err
                )
            else:
                saw = f"release: the recorded pid {reason} is alive" in err
            self.check(
                f"{label} ({loc})",
                code == 1 and saw and before == after,
                f"release at the {loc} location exited {code}; the reason "
                f"{'is' if saw else 'is NOT'} "
                f"{'the processes' if reason == 'processes' else f'the recorded pid {reason}'}; "
                f"both owner files {'unchanged' if before == after else 'CHANGED'}",
            )

    def set_pid_step(self, part, label, pid):
        for loc in RELEASE_ORDER:
            before = self.owner_bytes()
            code, _, _ = self.lock_call(
                "set_pid", PROJECT, part["temp_dir"], pid, location=loc
            )
            after = self.owner_bytes()
            b = before[loc].decode().splitlines() if before[loc] else []
            a = after[loc].decode().splitlines() if after[loc] else []
            changed = [(x, y) for x, y in zip(b, a) if x != y]
            others = all(before[o] == after[o] for o in LOCATIONS if o != loc)
            ok = (
                code == 0
                and len(a) == len(b) == 7
                and changed == [("pid: -", f"pid: {pid}")]
                and others
            )
            self.check(
                f"{label} ({loc})",
                ok,
                f"set_pid at the {loc} location exited {code}; {len(b)} lines before, "
                f"{len(a)} after; changed: {changed}; the other owner file "
                f"{'unchanged' if others else 'CHANGED'}",
            )
        self.show_owner()

    def second_acquire_step(self, part, label):
        before = self.owner_bytes()
        purpose = f"rehearsal-lock 02 proof (c), second acquirer, during part ({part['name']})"
        code1, _, err1 = self.lock_call(
            "acquire", SECOND_PROJECT, purpose, TEMP_C, "in-process", location="old"
        )
        code2, _, err2 = self.lock_call(
            "acquire", SECOND_PROJECT, purpose, TEMP_C, "in-process", location="default"
        )
        after = self.owner_bytes()
        held = "the rehearsal lock is held (" in err1
        old = "the old location of the rehearsal lock exists (" in err2
        self.check(
            label,
            code1 == 3 and code2 == 3 and held and old and before == after,
            f"at the old location exit {code1} ({'as held' if held else 'NOT as held'}); "
            f"at the default location exit {code2} "
            f"({'the old location' if old else 'NOT the old location'}); both owner files "
            f"{'unchanged' if before == after else 'CHANGED'}",
        )

    def release_free_step(self, part, label):
        for loc in RELEASE_ORDER:
            code, out, _ = self.lock_call(
                "release", PROJECT, part["temp_dir"], location=loc
            )
            if code == 0:
                part["held"][loc] = os.path.lexists(lock_dir(loc))
            self.check(
                f"{label} release ({loc})",
                code == 0 and "released" in out,
                f"release at the {loc} location exited {code}",
            )
        args = [part["temp_dir"]] + ([part["address"]] if part["address"] else [])
        for loc in RELEASE_ORDER:
            code, out, _ = self.lock_call("status", *args, location=loc)
            free = f"lock: free ({lock_dir(loc)} does not exist)" in out
            old_present = "old location: PRESENT" in out
            exist = [o for o in LOCATIONS if os.path.lexists(lock_dir(o))]
            self.check(
                f"{label} status ({loc})",
                code == 0 and free and not old_present and not exist,
                f"status at the {loc} location exited {code}; it says "
                f"{'free' if free else 'NOT free'}"
                f"{'; old location: PRESENT' if old_present else ''}; "
                f"existing: {exist if exist else 'neither location'}",
            )

    # -- part (a) --

    def part_a(self):
        part = {
            "name": "a",
            "temp_dir": TEMP_A,
            "address": None,
            "held": {loc: False for loc in LOCATIONS},
        }
        self.say("")
        self.say("== part (a): an in-process instance with _temp_dir")
        started = time.monotonic()
        try:
            self.acquire_step(
                part,
                "a1-acquire",
                f"rehearsal-lock 02 proof (a), Python {self.python_version} / Ray {self.ray_version}",
            )
            part["pre_pids"] = set(parse_table(read_ps()))
            self.say(f"  the pre-start reading: {len(part['pre_pids'])} processes")
            self.start_driver(part, {"address": "local", "temp_dir": TEMP_A})
            workers = self.driver_expect(part, "WORKERS", DRIVER_READY_WAIT)
            ready = (
                self.driver_expect(part, "READY", DRIVER_READY_WAIT)
                if workers
                else None
            )
            self.check(
                "a2-driver-ready", ready is not None, f"the driver said {ready!r}"
            )
            driver_pid = int(ready.split()[1])
            self.check(
                "a2-driver-pid",
                driver_pid == part["driver"]["proc"].pid,
                f"READY {driver_pid}; the child's pid {part['driver']['proc'].pid}",
            )
            part["driver_command"] = command_now(driver_pid)
            w = json.loads(workers.split(" ", 1)[1])
            extra = {"driver_pid": driver_pid, "actor": w["actor"], "tasks": w["tasks"]}
            self.checkpoint(part, "a1", "a1", extra)
            self.release_refused(part, "a4-release-refused-by-processes", "processes")
            self.set_pid_step(part, "a5-set-pid-driver", driver_pid)
            self.second_acquire_step(part, "a6-second-acquire-refused")
            self.release_refused(part, "a7-release-refused", driver_pid)
            self.driver_send(part, "shutdown")
            got = self.driver_expect(part, "SHUTDOWN", DRIVER_REPLY_WAIT)
            self.check("a8-shutdown", got is not None, f"the driver said {got!r}")
            _, _, facts, _ = self.checkpoint(
                part, "a2", "a2", {"driver_pid": driver_pid}
            )
            self.say(
                f"  the reaper after ray.shutdown(): {'alive' if facts.get('reaper_alive') else 'gone'}"
            )
            self.release_refused(part, "a8-release-refused-by-pid", driver_pid)
            self.driver_send(part, "exit")
            got = self.driver_expect(part, "EXIT", DRIVER_REPLY_WAIT)
            code = self.driver_wait(part, DRIVER_EXIT_WAIT)
            self.check(
                "a9-driver-exit",
                code == 0,
                f"the driver said {got!r} and exited {code}",
            )
            self.show_driver_stderr(part)
            self.checkpoint(part, "a3", "a3", {"driver_pid": driver_pid})
            self.release_free_step(part, "a9")
        except HeldByOther:
            return self.refused_by_other(part)
        except (CheckFailed, Exception, Interrupted) as exc:
            self.failure(exc)
            return self.cleanup(part)
        self.say(f"part (a): {time.monotonic() - started:.1f} s")
        self.record["part_a_seconds"] = round(time.monotonic() - started, 1)
        return 0

    # -- part (b) --

    def part_b(self):
        part = {
            "name": "b",
            "temp_dir": TEMP_B,
            "address": ADDRESS_B,
            "held": {loc: False for loc in LOCATIONS},
        }
        self.say("")
        self.say("== part (b): a ray start --head cluster")
        started = time.monotonic()
        try:
            self.acquire_step(
                part,
                "b1-acquire",
                f"rehearsal-lock 02 proof (b), Python {self.python_version} / Ray {self.ray_version}",
            )
            part["pre_pids"] = set(parse_table(read_ps()))
            self.say(f"  the pre-start reading: {len(part['pre_pids'])} processes")
            argv = [str(self.ray_bin), "start", "--head", "--temp-dir", TEMP_B]
            argv += ["--port", "6420", "--ray-client-server-port", "6421"]
            argv += [
                "--dashboard-port",
                "8270",
                "--dashboard-agent-listen-port",
                "52370",
            ]
            argv += ["--num-cpus", str(NUM_CPUS), "--disable-usage-stats"]
            out_path = self.scratch / f"{self.stem}-ray-start.txt"
            self.say(f"  $ {' '.join(argv)}   (output to {out_path})")
            part["cluster_started"] = True
            t = time.monotonic()
            with open(out_path, "w") as out:
                code = subprocess.run(
                    argv, cwd=self.cwd, stdout=out, stderr=subprocess.STDOUT
                ).returncode
            self.say(f"    exit {code} ({time.monotonic() - t:.1f} s)")
            self.show_output("output", out_path.read_text())
            self.check("b2-ray-start", code == 0, f"ray start exited {code}")
            r, view, facts, extras = self.checkpoint(part, "b1", "b1", {}, ("b1cs",))
            problems, cs_facts = extras["b1cs"]
            if problems and problems[0].startswith("NOT EXERCISED"):
                self.note("b4-client-server", "NOT EXERCISED", problems[0])
                self.record["client_server_exercised"] = False
            else:
                self.record["client_server_exercised"] = True
                self.check(
                    "b4-client-server",
                    not problems,
                    "; ".join(problems) if problems else f"as expected; {cs_facts}",
                )
            gcs = facts["gcs_server"][0]
            self.release_refused(part, "b5-release-refused-by-processes", "processes")
            self.set_pid_step(part, "b5-set-pid-gcs_server", gcs)
            self.second_acquire_step(part, "b5-second-acquire-refused")
            self.release_refused(part, "b5-release-refused", gcs)
            self.start_driver(part, {"address": ADDRESS_B})
            workers = self.driver_expect(part, "WORKERS", DRIVER_READY_WAIT)
            ready = (
                self.driver_expect(part, "READY", DRIVER_READY_WAIT)
                if workers
                else None
            )
            self.check(
                "b6-driver-ready", ready is not None, f"the driver said {ready!r}"
            )
            driver_pid = int(ready.split()[1])
            part["driver_command"] = command_now(driver_pid)
            w = json.loads(workers.split(" ", 1)[1])
            extra = {"driver_pid": driver_pid, "actor": w["actor"], "tasks": w["tasks"]}
            self.checkpoint(part, "b2", "b2", extra)
            self.driver_send(part, "shutdown")
            got = self.driver_expect(part, "SHUTDOWN", DRIVER_REPLY_WAIT)
            self.driver_send(part, "exit")
            got2 = self.driver_expect(part, "EXIT", DRIVER_REPLY_WAIT)
            code = self.driver_wait(part, DRIVER_EXIT_WAIT)
            self.check(
                "b6-driver-exit",
                got is not None and code == 0,
                f"the driver said {got!r}, {got2!r} and exited {code}",
            )
            self.show_driver_stderr(part)
            r, _, _, _ = self.checkpoint(part, "b3", "b3", {"driver_pid": driver_pid})
            stop_list = {p: r["table"][p][1] for p in r["live"]}
            part["stop_list"] = stop_list
            self.say("  the stop (never ray stop):")
            part["stopped"] = True
            self.stop(stop_list)
            self.checkpoint(part, "b4", "b4", {})
            self.release_free_step(part, "b9")
        except HeldByOther:
            return self.refused_by_other(part)
        except (CheckFailed, Exception, Interrupted) as exc:
            self.failure(exc)
            return self.cleanup(part)
        self.say(f"part (b): {time.monotonic() - started:.1f} s")
        self.record["part_b_seconds"] = round(time.monotonic() - started, 1)
        return 0

    # -- failure and cleanup --

    def failure(self, exc):
        if isinstance(exc, CheckFailed):
            self.say(f"a check failed ({exc}); cleaning up what this run started")
        else:
            self.say(
                f"an unexpected {type(exc).__name__}: {exc}; treated as a failed check"
            )
            for line in traceback.format_exception(exc):
                self.say("  " + line.rstrip("\n"))
            self.results.append((f"unexpected {type(exc).__name__}", "FAIL"))
            self.record["checks"].append(
                {"name": "unexpected exception", "verdict": "FAIL", "detail": repr(exc)}
            )

    def cleanup(self, part):
        """Stop only what this part started, then release through the module; 1, or 4 if not."""
        self._interrupted = True  # a later SIGTERM or SIGHUP is ignored from here on
        self.say(f"cleanup of part ({part['name']}):")
        try:
            self.stop_driver(part)
            if part.get("cluster_started") and not part.get("stopped"):
                part["stopped"] = True
                if "stop_list" in part:
                    stop_list = part["stop_list"]
                else:
                    r = self.reading(part, True, False)
                    both = r["live"] & r["witness"]
                    for p in sorted((r["live"] | r["witness"]) - both):
                        where = "live listing" if p in r["live"] else "witness"
                        cmd = r["table"].get(p, (0, ""))[1]
                        self.say(
                            f"  only in the {where}, not signalled: {p} {self.cut(cmd)}"
                        )
                    stop_list = {p: r["table"][p][1] for p in both}
                self.stop(stop_list)
            left = set()
            if "pre_pids" in part:
                for _ in range(SETTLE_READINGS):
                    r = self.reading(part, part["address"] is not None, False)
                    left = r["witness"] | r["live"] | r["offline"]
                    if not left:
                        break
                    time.sleep(1)
                for p in sorted(left):
                    self.say(f"  left: {p} {self.cut(r['table'].get(p, (0, ''))[1])}")
            if left:
                raise LeftHeld(f"processes left: {_fmt(left)}")
            self.release_held(part)
        except (LeftHeld, Exception) as exc:
            return self.left_held(exc)
        self.record["cleanup"] = "complete"
        self.say(
            "cleanup complete: nothing of this part is left, and the lock is released"
        )
        return 1

    def release_held(self, part):
        """Release, through the module, each location this part holds, old first; stop at a refusal."""
        for loc in RELEASE_ORDER:
            if not part["held"][loc]:
                continue
            code, _, _ = self.lock_call(
                "release", PROJECT, part["temp_dir"], location=loc
            )
            if code != 0:
                raise LeftHeld(
                    f"release at the {loc} location ({lock_dir(loc)}) exited {code}"
                )
            part["held"][loc] = os.path.lexists(lock_dir(loc))
            if part["held"][loc]:
                raise LeftHeld(f"the {loc} location ({lock_dir(loc)}) still exists")

    def left_held(self, exc):
        self.say(
            f"CLEANUP INCOMPLETE ({type(exc).__name__}: {exc}): the lock is left as it is "
            "at both locations"
        )
        self.show_owner("the lock's owner file")
        self.record["cleanup"] = f"incomplete: {exc!r}"
        return 4

    def refused_by_other(self, part):
        """An ``acquire`` exited 3: release what this part holds (the default location), then 3."""
        self._interrupted = True  # a later SIGTERM or SIGHUP is ignored from here on
        held = [loc for loc in RELEASE_ORDER if part["held"][loc]]
        self.say(
            "the shared lock is someone else's; this part holds it at "
            + (
                " and ".join(f"the {loc} location" for loc in held)
                if held
                else "neither location"
            )
        )
        self.show_owner("owner file")
        try:
            self.release_held(part)
        except (LeftHeld, Exception) as exc:
            return self.left_held(exc)
        self.record["cleanup"] = "refused: someone else's lock; nothing of it held"
        return 3

    def _on_signal(self, signum, frame):
        if self._interrupted:
            return
        self._interrupted = True
        raise Interrupted(signal.Signals(signum).name)

    # -- the run --

    def run(self):
        started = time.monotonic()
        code = self.preflight()
        if code:
            return code
        signal.signal(signal.SIGTERM, self._on_signal)
        signal.signal(signal.SIGHUP, self._on_signal)
        self.save()
        code = self.part_a()
        if code == 0:
            code = self.part_b()
        if code == 0:
            self.say("")
            self.say("== after both parts")
            try:
                exist = [o for o in LOCATIONS if os.path.lexists(lock_dir(o))]
                rp = os.path.lexists(self.raypoolkit_dir)
                rp_entries = sorted(os.listdir(self.raypoolkit_dir)) if rp else []
                self.check(
                    "after-both",
                    not exist and not rp_entries,
                    f"existing: {exist if exist else 'neither location'}; "
                    f"~/.raypoolkit {'exists' if rp else 'does not exist'} (before: "
                    f"{'exists' if self.raypoolkit_before else 'does not exist'}), holding "
                    f"{rp_entries if rp_entries else 'nothing'}",
                )
            except CheckFailed:
                code = 1
        elapsed = time.monotonic() - started
        passed = sum(1 for _, v in self.results if v == "PASS")
        failed = [n for n, v in self.results if v == "FAIL"]
        other = [f"{n} ({v})" for n, v in self.results if v not in ("PASS", "FAIL")]
        self.say("")
        self.say(
            f"Summary: {passed} checks passed, {len(failed)} failed{': ' + ', '.join(failed) if failed else ''}"
            f"{'; ' + ', '.join(other) if other else ''}; exit {code}; {elapsed:.1f} s in all"
        )
        self.record["exit"] = code
        self.record["seconds"] = round(elapsed, 1)
        self.save()
        return code


# ---- the replay ---------------------------------------------------------------------------------


def replay(path):
    record = json.loads(Path(path).read_text())
    print(f"replay of {path}")
    print(
        f"  recorded at Python {record['python'].split()[0]} / Ray {record['ray']}; exit {record.get('exit')}"
    )
    if "lock_dirs" in record:
        held = ", ".join(f"{k} {v}" for k, v in sorted(record["lock_dirs"].items()))
        print(f"  the lock held at both locations (05's form): {held}")
    else:
        print("  the lock held at the old location alone (02's form)")
    print(f"  the module as imported: {rl.__file__}")
    print(f"  HOME: {os.environ.get('HOME')}")
    failures = 0
    for cp in record["checkpoints"]:
        rows = {int(p): (v[0], v[1]) for p, v in cp["rows"].items()}
        ps_text = "".join(f"{p} {pp} {cmd}\n" for p, (pp, cmd) in sorted(rows.items()))
        view = {
            "rows": rows,
            "witness": set(cp["witness"]),
            "live": set(cp["live"]),
            "offline": offline_listing(ps_text, cp["temp_dir"], cp["address"]),
            "temp_dir": cp["temp_dir"],
            "address": cp["address"],
            "extra": cp["extra"],
        }
        if "live_na" in cp:
            view["live_na"] = set(cp["live_na"])
            view["offline_na"] = offline_listing(ps_text, cp["temp_dir"], None)
        same = view["offline"] == set(cp["offline"]) and (
            "live_na" not in cp or view["offline_na"] == set(cp["offline_na"])
        )
        kinds = [cp["kind"]] + sorted(cp.get("extra_kinds", {}))
        for kind in kinds:
            problems, facts = evaluate(kind, view)
            name = cp["name"] if kind == cp["kind"] else f"{cp['name']}/{kind}"
            if problems and problems[0].startswith("NOT EXERCISED"):
                print(f"NOT EXERCISED {name}: {problems[0]}")
                continue
            ok = cp["settled"] and not problems
            failures += not ok
            print(
                f"{'PASS' if ok else 'FAIL'} {name} (recorded {cp['verdict']}; the offline listing "
                f"{'as recorded' if same else 'DIFFERS from the record'}): "
                + ("; ".join(problems) if problems else "as expected")
            )
    print(f"replay: {failures} checkpoint check(s) failed; exit {1 if failures else 0}")
    return 1 if failures else 0


# ---- the command line ---------------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="ray_proof.py", description=__doc__.split("\n")[1]
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--record", help="run the proof, keeping its record in this file"
    )
    group.add_argument(
        "--replay", help="replay a record offline, with no Ray and no lock"
    )
    group.add_argument("--driver", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.driver:
        return driver_main()
    if args.replay:
        return replay(args.replay)
    sys.stdout.reconfigure(line_buffering=True)
    proof = Proof(os.path.abspath(args.record))
    return proof.run()


if __name__ == "__main__":
    sys.exit(main())
