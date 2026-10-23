"""
Tests for ``raypoolkit/rehearsal_lock.py``, the shared rehearsal lock.

Most are ported from the tests of the source module named in ``rehearsal_lock``'s provenance note,
each to its nearest meaning under this package's interface (the rehearsal-lock campaign's README
§4), with neutral projects: ``ProjectA`` on ``/tmp/ray-a`` with a cluster at ``127.0.0.1:6400``,
``ProjectB`` on ``/tmp/ray-b`` at ``127.0.0.1:6500``, and ``ProjectC`` in process on
``/tmp/ray-c``. The rest test what the interface adds: the old location, the arguments, and the
process rule by temp dir.

**No real lock is reachable.** Every test runs with ``HOME`` patched to a temporary directory, and
``setUp`` checks that both locations computed from it are inside that directory before any test
body runs. Every test that does not test the default location also passes ``lock_dir``
explicitly, inside the same directory, so that a forgotten argument cannot reach a real lock.
``ps`` is never run: ``rehearsal_lock._ps_output`` is replaced by fixed text (empty unless a test
sets it), or the process rule is given ``ps_text``. No Ray.

**Each refusal test leaves exactly one reason standing**, so that a mutation of one check cannot
hide behind another: an owner that is not the caller's is tested with ``pid: -`` (or a dead pid)
and no processes; a live pid with the caller's owner and no processes; processes with the caller's
owner and ``pid: -`` or a dead pid. ``set-pid``'s refusals other than a dead pid use a live pid.
"""

import argparse
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from raypoolkit import rehearsal_lock as rl
from raypoolkit.tests.test_inherited_faults import LICENCE_HEADER

PAST = "2026-01-01T00:00:00+00:00"

A_DIR = "/tmp/ray-a"
A_ADDRESS = "127.0.0.1:6400"
B_DIR = "/tmp/ray-b"
B_ADDRESS = "127.0.0.1:6500"
C_DIR = "/tmp/ray-c"

UNREADABLE = RuntimeError("ps failed with status 1")

# the one reading of ``ps``, kept before any test replaces it, for the test of ``ps`` failing
REAL_PS_OUTPUT = rl._ps_output
REAL_SHORT_HOSTNAME = rl._short_hostname


def owner(project="ProjectA", ray_temp_dir=A_DIR, ray_address=A_ADDRESS, pid="-"):
    return rl.owner_text(
        project, "earlier", ray_temp_dir, ray_address, pid, acquired=PAST, host="h"
    )


# The three shapes the clients' owner files take today, written out as text: a cluster's
# ``host:port`` address; ``in-process`` for both Ray fields; and a pid that is ``-`` or a number.
CLUSTER_OWNER = """project: ProjectA
purpose: a rehearsal
acquired: 2026-10-12T14:19:31+01:00
host: machine
ray_temp_dir: /tmp/ray-a
ray_address: 127.0.0.1:6400
pid: -
"""
IN_PROCESS_OWNER = """project: ProjectC
purpose: a long build
acquired: 2026-10-12T14:19:40+01:00
host: machine
ray_temp_dir: in-process
ray_address: in-process
pid: 12345
"""
# the shape an in-process caller writes under this module: its own temp dir, no cluster address
TEMP_DIR_IN_PROCESS_OWNER = """project: ProjectC
purpose: a long build
acquired: 2026-10-12T14:19:40+01:00
host: machine
ray_temp_dir: /tmp/ray-c
ray_address: in-process
pid: 12345
"""


def dead_pid():
    """A pid that has just exited and been reaped."""
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    return proc.pid


def ps_line(pid, ppid, command):
    return f"{pid:>5} {ppid:>5} {command}\n"


def ps_text(*rows):
    return "".join(ps_line(*row) for row in rows)


def client_server(address):
    """A ``ray start`` cluster's Ray client server: it names its GCS address, not its temp dir."""
    return (
        "/opt/venvs/a/bin/python -m ray.util.client.server "
        f"--address={address} --host=0.0.0.0 --port=6401 --mode=proxy"
    )


# A seed, a worker below it and another below that: the processes of ``/tmp/ray-a``.
A_PS = ps_text(
    (
        100,
        1,
        f"/opt/venvs/a/raylet --raylet_socket_name={A_DIR}/session_x/sockets/raylet",
    ),
    (101, 100, "ray::IDLE"),
    (102, 101, "ray::A.method"),
)

# ---- the process trees of README §0.3 -------------------------------------------------------------
#
# Reconstructions of the planner's probe (``prompts/rehearsal-lock/planning/tempdir_probe-ray-*.txt``):
# an in-process instance started with ``_temp_dir``, two CPUs, no dashboard, four tasks and an actor.
# The trees are the probe's (pids, ppids, which process names the temp dir, which is reached only as
# a descendant, and the reaper below the driver); the commands are written out in full with neutral
# paths, since the saved outputs cut them at 150 characters and shortened the interpreter and venv.
# Each seed names the temp dir in a form Ray uses. The driver's command names none (the temp dir is
# in its code), nor does the reaper's. Prompt 02 re-measures these trees under real Ray.
#
# In both, ``7000`` is this module's own command, run from the user's shell ``6100`` (the driver's
# parent too); it names the temp dir, as a lock command does, and ``7001`` is its ``ps``.

PY = "/opt/venvs/a/bin/python"


def _ray(version):
    return f"/opt/venvs/a/lib/python{version}/site-packages/ray"


SESSION = f"{A_DIR}/session_2026-10-23_12-43-03_944000_6169"

SHELL_AND_SELF = (
    (6100, 1, "-zsh"),
    (
        7000,
        6100,
        f"{PY} -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir {A_DIR}",
    ),
    (7001, 7000, "ps -axww -o pid= -o ppid= -o command="),
)

R243 = _ray("3.12")
TREE_243 = ps_text(
    *SHELL_AND_SELF,
    (6169, 6100, f"{PY} -u driver.py"),
    (6170, 6169, f"{PY} -u {R243}/_private/ray_process_reaper.py"),
    (
        6171,
        6169,
        f"{R243}/core/src/ray/gcs/gcs_server --log_dir={SESSION}/logs "
        f"--config_list=eyJ9 --gcs_server_port=0 --metrics-agent-port=0 --node-ip-address=127.0.0.1 "
        f"--session-name=session_2026-10-23_12-43-03_944000_6169",
    ),
    (
        6172,
        6169,
        f"{PY} -u {R243}/autoscaler/_private/monitor.py --logs-dir={SESSION}/logs "
        f"--logging-rotate-bytes=536870912 --logging-rotate-backup-count=5 "
        f"--gcs-address=127.0.0.1:61234 --monitor-ip=127.0.0.1",
    ),
    (
        6173,
        6169,
        f"{PY} {R243}/_private/log_monitor.py --session-dir={SESSION} "
        f"--logs-dir={SESSION}/logs --gcs-address=127.0.0.1:61234",
    ),
    (
        6174,
        6169,
        f"{R243}/core/src/ray/raylet/raylet --raylet_socket_name={SESSION}/sockets/raylet "
        f"--store_socket_name={SESSION}/sockets/plasma_store --object_manager_port=0 "
        f"--node_manager_port=0 --node_ip_address=127.0.0.1 --temp_dir={A_DIR} "
        f"--session_dir={SESSION} --log_dir={SESSION}/logs --num_prestart_python_workers=2",
    ),
    (
        6175,
        6169,
        f"{PY} -u {R243}/_private/workers/default_worker.py --temp-dir={A_DIR} "
        f"--session-dir={SESSION} --node-ip-address=127.0.0.1",
    ),
    (
        6176,
        6174,
        f"{PY} -u {R243}/dashboard/agent.py --node-ip-address=127.0.0.1 "
        f"--temp-dir={A_DIR} --session-dir={SESSION} --log-dir={SESSION}/logs "
        f"--minimal --agent-id 1",
    ),
    (
        6177,
        6174,
        f"{PY} -u {R243}/_private/runtime_env/agent/main.py --node-ip-address=127.0.0.1 "
        f"--temp-dir={A_DIR} --log-dir={SESSION}/logs --runtime-env-agent-port=0",
    ),
    (6178, 6174, "ray::IDLE"),
    (6179, 6174, "ray::IDLE"),
    (6181, 6174, "ray::A"),
)
LISTED_243 = [6171, 6172, 6173, 6174, 6175, 6176, 6177, 6178, 6179, 6181]

R255 = _ray("3.13")
TREE_255 = ps_text(
    *SHELL_AND_SELF,
    (6212, 6100, f"{PY} -u driver.py"),
    (6221, 6212, f"{PY} -u {R255}/_private/ray_process_reaper.py"),
    (
        6222,
        6212,
        f"{R255}/core/src/ray/gcs/gcs_server --log_dir={SESSION}/logs "
        f"--config_list=eyJ9 --gcs_server_port=0 --node-ip-address=127.0.0.1",
    ),
    (
        6241,
        6212,
        f"{PY} -u {R255}/autoscaler/_private/monitor.py --logs-dir={SESSION}/logs "
        f"--gcs-address=127.0.0.1:61234 --monitor-ip=127.0.0.1",
    ),
    (
        6244,
        6212,
        f"{PY} {R255}/_private/log_monitor.py --session-dir={SESSION} "
        f"--logs-dir={SESSION}/logs --gcs-address=127.0.0.1:61234",
    ),
    (
        6262,
        6212,
        f"{PY} -u {R255}/dashboard/dashboard.py --host=127.0.0.1 --port=0 "
        f"--temp-dir={A_DIR} --log-dir={SESSION}/logs --session-dir={SESSION} --minimal",
    ),
    (
        6263,
        6212,
        f"{R255}/core/src/ray/raylet/raylet --raylet_socket_name={SESSION}/sockets/raylet "
        f"--store_socket_name={SESSION}/sockets/plasma_store --temp_dir={A_DIR} "
        f"--session_dir={SESSION} --log_dir={SESSION}/logs",
    ),
    (6264, 6263, "ray::DashboardAgent"),
    (6265, 6263, "ray::RuntimeEnvAgent"),
    (6268, 6263, "ray::IDLE"),
    (6269, 6263, "ray::IDLE"),
    (6270, 6263, "ray::A"),
)
LISTED_255 = [6222, 6241, 6244, 6262, 6263, 6264, 6265, 6268, 6269, 6270]


class LockTestCase(unittest.TestCase):
    """
    ``HOME`` and ``ps`` patched; ``self.lock`` is an explicit lock directory, its parent absent.

    Every test class derives from this one, those that touch no lock included, so that every test
    runs with ``HOME`` patched.
    """

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        patch_env = mock.patch.dict(os.environ, {"HOME": str(self.home)})
        patch_env.start()
        self.addCleanup(patch_env.stop)
        # never go on unless both locations are inside the temporary directory
        for location in (rl.default_lock_dir(), rl.old_lock_dir()):
            if not location.is_relative_to(self.home):
                raise AssertionError(
                    f"{location} is not under the patched HOME {self.home}; not running"
                )
        self.ps = ""
        patch_ps = mock.patch.object(rl, "_ps_output", self.fake_ps)
        patch_ps.start()
        self.addCleanup(patch_ps.stop)
        # ``hostname -s`` is slow on some machines; the real one is tested once, by acquire
        patch_host = mock.patch.object(rl, "_short_hostname", return_value="testhost")
        patch_host.start()
        self.addCleanup(patch_host.stop)
        self.lock = self.tmp / "locks" / "rehearsal-lock"
        self.new_default = self.home / ".raypoolkit" / "rehearsal-lock"
        self.old = self.home / "ScienceData" / ".rehearsal-lock"

    def fake_ps(self):
        if isinstance(self.ps, Exception):
            raise self.ps
        return self.ps

    def run_cmd(self, func, *args, **kwargs):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = func(*args, **kwargs)
        return rc, out.getvalue(), err.getvalue()

    def run_main(self, argv):
        """``main(argv)``'s exit status (a usage error's ``SystemExit`` code too), stdout, stderr."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                rc = rl.main(argv)
            except SystemExit as exc:
                rc = exc.code
        return rc, out.getvalue(), err.getvalue()

    def make_lock(self, text, where=None):
        """Create a lock directory by hand; ``text=None`` leaves it without an owner file."""
        where = self.lock if where is None else where
        where.mkdir(parents=True)
        if text is not None:
            (where / "owner").write_bytes(text.encode("utf-8"))

    def tree(self):
        """Every path under the temporary directory, with each file's bytes."""
        found = {}
        for path in sorted(self.tmp.rglob("*")):
            rel = str(path.relative_to(self.tmp))
            found[rel] = path.read_bytes() if path.is_file() else "<dir>"
        return found

    def assertUntouched(self, before):
        self.assertEqual(self.tree(), before)


# ---- acquire ------------------------------------------------------------------------------------


class TestAcquire(LockTestCase):
    def acquire(self, **kwargs):
        args = dict(
            project="ProjectA",
            purpose="a purpose",
            ray_temp_dir=A_DIR,
            ray_address=A_ADDRESS,
            lock_dir=self.lock,
        )
        args.update(kwargs)
        return self.run_cmd(rl.acquire, **args)

    def test_free_lock_is_created_with_the_seven_keys(self):
        with mock.patch.object(rl, "_short_hostname", REAL_SHORT_HOSTNAME):
            rc, out, _ = self.acquire()
        self.assertEqual(rc, 0)
        self.assertIn("ProjectA: a purpose", out)
        self.assertEqual(sorted(p.name for p in self.lock.iterdir()), ["owner"])
        text = (self.lock / "owner").read_text(encoding="utf-8")
        lines = text.splitlines()
        self.assertEqual([l.split(": ")[0] for l in lines], list(rl.OWNER_KEYS))
        self.assertEqual(
            rl.OWNER_KEYS,
            (
                "project",
                "purpose",
                "acquired",
                "host",
                "ray_temp_dir",
                "ray_address",
                "pid",
            ),
        )
        parsed = rl.parse_owner(text)
        self.assertEqual(parsed["project"], "ProjectA")
        self.assertEqual(parsed["purpose"], "a purpose")
        self.assertEqual(parsed["ray_temp_dir"], A_DIR)
        self.assertEqual(parsed["ray_address"], A_ADDRESS)
        self.assertEqual(parsed["pid"], "-")
        stamp = datetime.fromisoformat(parsed["acquired"])
        self.assertIsNotNone(stamp.utcoffset())
        self.assertTrue(parsed["host"] and "." not in parsed["host"])
        self.assertTrue(text.endswith("\n"))

    def test_an_in_process_caller_is_recorded_with_its_temp_dir(self):
        rc, _, _ = self.acquire(
            project="ProjectC", ray_temp_dir=C_DIR, ray_address="in-process"
        )
        self.assertEqual(rc, 0)
        parsed = rl.parse_owner((self.lock / "owner").read_text(encoding="utf-8"))
        self.assertEqual(parsed["ray_temp_dir"], C_DIR)
        self.assertEqual(parsed["ray_address"], "in-process")

    def test_parent_is_created_and_the_lock_by_one_os_mkdir(self):
        self.assertFalse(self.lock.parent.exists())
        calls = []
        real_mkdir = os.mkdir

        def recording_mkdir(path, *args, **kwargs):
            calls.append(Path(path))
            return real_mkdir(path, *args, **kwargs)

        with mock.patch.object(rl.os, "mkdir", recording_mkdir):
            rc, _, _ = self.acquire()
        self.assertEqual(rc, 0)
        self.assertTrue(self.lock.parent.is_dir())
        self.assertEqual(calls.count(self.lock), 1)

    def held_case(self, text):
        self.make_lock(text)
        before = self.tree()
        rc, out, err = self.acquire(purpose="new")
        self.assertEqual(rc, 3, out + err)
        self.assertUntouched(before)
        self.assertIn("stop and ask the user", err)
        self.assertNotIn("old location", err)
        return err

    def test_held_by_the_caller_returns_3_and_prints_the_owner(self):
        err = self.held_case(owner())
        self.assertIn("    purpose: earlier", err)

    def test_held_by_another_project_returns_3_and_prints_the_owner(self):
        err = self.held_case(owner("ProjectB", B_DIR, B_ADDRESS))
        self.assertIn("    project: ProjectB", err)
        self.assertIn("    ray_address: 127.0.0.1:6500", err)

    def test_held_in_process_by_another_project_returns_3(self):
        err = self.held_case(IN_PROCESS_OWNER)
        self.assertIn("    project: ProjectC", err)

    def test_held_with_no_owner_file_returns_3_and_says_so(self):
        err = self.held_case(None)
        self.assertIn("(no owner file)", err)
        self.assertEqual(list(self.lock.iterdir()), [])

    def test_processes_of_the_temp_dir_return_4_and_leave_no_lock(self):
        self.ps = A_PS
        rc, out, err = self.acquire()
        self.assertEqual(rc, 4, out + err)
        self.assertFalse(self.lock.exists())
        self.assertTrue(self.lock.parent.is_dir())
        self.assertIn("    100 1 ", err)
        self.assertIn("    101 100 ray::IDLE", err)
        self.assertIn("released the lock again", err)

    def test_the_client_server_of_the_address_returns_4(self):
        self.ps = ps_text((300, 1, client_server(A_ADDRESS)))
        rc, _, err = self.acquire()
        self.assertEqual(rc, 4, err)
        self.assertFalse(self.lock.exists())

    def test_an_unreadable_table_returns_4_and_leaves_no_lock(self):
        for exc in (UNREADABLE, OSError("no ps")):
            with self.subTest(exc=exc):
                self.ps = exc
                rc, _, err = self.acquire()
                self.assertEqual(rc, 4, err)
                self.assertFalse(self.lock.exists())
                self.assertIn("cannot read the process table", err)

    def test_another_projects_processes_do_not_stop_it(self):
        self.ps = ps_text(
            (200, 1, f"/opt/venvs/b/raylet --temp_dir={B_DIR}"),
            (201, 200, "ray::IDLE"),
            (210, 1, client_server(B_ADDRESS)),
        )
        rc, _, err = self.acquire()
        self.assertEqual(rc, 0, err)

    def test_an_owner_file_that_cannot_be_written_returns_1_and_leaves_no_lock(self):
        with mock.patch.object(rl, "_replace_owner", side_effect=OSError("disk full")):
            rc, _, err = self.acquire()
        self.assertEqual(rc, 1, err)
        self.assertFalse(self.lock.exists())
        self.assertIn("could not write the owner file", err)


class TestOldLocation(LockTestCase):
    """Decision U4: while ``~/ScienceData/.rehearsal-lock`` exists, ``acquire`` refuses."""

    def acquire(self, **kwargs):
        args = dict(
            project="ProjectA",
            purpose="p",
            ray_temp_dir=A_DIR,
            ray_address=A_ADDRESS,
            lock_dir=self.lock,
        )
        args.update(kwargs)
        return self.run_cmd(rl.acquire, **args)

    def refused(self, text):
        self.make_lock(text, where=self.old)
        before = self.tree()
        rc, out, err = self.acquire()
        self.assertEqual(rc, 3, out + err)
        self.assertUntouched(before)
        self.assertFalse(self.lock.parent.exists())
        self.assertIn(
            f"the old location of the rehearsal lock exists ({self.old})", err
        )
        self.assertIn("removes it by hand", err)
        return err

    def test_the_old_location_with_an_owner_file_returns_3_and_prints_it(self):
        err = self.refused(owner("ProjectB", B_DIR, B_ADDRESS))
        self.assertIn("    project: ProjectB", err)

    def test_the_old_location_without_an_owner_file_returns_3(self):
        err = self.refused(None)
        self.assertIn("(no owner file)", err)

    def test_the_old_location_refuses_the_default_location_too(self):
        self.make_lock(None, where=self.old)
        before = self.tree()
        rc, _, err = self.run_cmd(rl.acquire, "ProjectA", "p", A_DIR, A_ADDRESS)
        self.assertEqual(rc, 3, err)
        self.assertUntouched(before)
        self.assertFalse((self.home / ".raypoolkit").exists())

    def test_with_only_its_parent_present_acquire_succeeds(self):
        self.old.parent.mkdir()
        rc, _, err = self.acquire()
        self.assertEqual(rc, 0, err)
        self.assertTrue((self.lock / "owner").is_file())

    def test_acquiring_the_old_location_itself_is_not_refused_by_this_check(self):
        rc, _, err = self.acquire(lock_dir=rl.old_lock_dir())
        self.assertEqual(rc, 0, err)
        self.assertTrue((self.old / "owner").is_file())
        # held now: refused as a held lock, not as the old location
        before = self.tree()
        rc, _, err = self.acquire(lock_dir=rl.old_lock_dir())
        self.assertEqual(rc, 3)
        self.assertUntouched(before)
        self.assertIn("the rehearsal lock is held", err)
        self.assertNotIn("old location", err)


# ---- set-pid ------------------------------------------------------------------------------------


class TestSetPid(LockTestCase):
    def test_live_pid_changes_pid_and_only_pid(self):
        before_text = owner()
        self.make_lock(before_text)
        rc, out, _ = self.run_cmd(
            rl.set_pid, "ProjectA", A_DIR, os.getpid(), lock_dir=self.lock
        )
        self.assertEqual(rc, 0)
        self.assertIn(f"recorded pid {os.getpid()}", out)
        after = (self.lock / "owner").read_text(encoding="utf-8")
        self.assertEqual(after, before_text.replace("pid: -", f"pid: {os.getpid()}"))
        self.assertEqual(sorted(p.name for p in self.lock.iterdir()), ["owner"])

    def test_a_recorded_pid_is_replaced(self):
        self.make_lock(owner(pid=dead_pid()))
        rc, _, _ = self.run_cmd(
            rl.set_pid, "ProjectA", A_DIR, os.getpid(), lock_dir=self.lock
        )
        self.assertEqual(rc, 0)
        parsed = rl.parse_owner((self.lock / "owner").read_text(encoding="utf-8"))
        self.assertEqual(parsed["pid"], str(os.getpid()))

    def refused(self, text, pid=None, project="ProjectA", ray_temp_dir=A_DIR):
        pid = os.getpid() if pid is None else pid
        if text is not False:
            self.make_lock(text)
        before = self.tree()
        rc, out, err = self.run_cmd(
            rl.set_pid, project, ray_temp_dir, pid, lock_dir=self.lock
        )
        self.assertEqual(rc, 1, out + err)
        self.assertUntouched(before)
        return err

    def test_a_dead_pid_is_refused(self):
        self.refused(owner(), pid=dead_pid())

    def test_pid_zero_is_refused(self):
        self.make_lock(owner())
        before = self.tree()
        with self.assertRaises(ValueError):
            rl.set_pid("ProjectA", A_DIR, 0, lock_dir=self.lock)
        self.assertUntouched(before)

    def test_no_lock_is_refused(self):
        err = self.refused(False)
        self.assertFalse(self.lock.exists())
        self.assertIn("there is no lock", err)

    def test_no_owner_file_is_refused(self):
        self.refused(None)

    def test_another_projects_lock_is_refused(self):
        self.refused(owner("ProjectB", B_DIR, B_ADDRESS))

    def test_the_same_project_with_another_temp_dir_is_refused(self):
        err = self.refused(owner("ProjectA", B_DIR, A_ADDRESS))
        self.assertIn("ray_temp_dir is '/tmp/ray-b', not '/tmp/ray-a'", err)

    def test_another_project_with_the_callers_temp_dir_is_refused(self):
        err = self.refused(owner("ProjectB", A_DIR, A_ADDRESS))
        self.assertIn("project is 'ProjectB', not 'ProjectA'", err)

    def test_an_in_process_owner_is_never_the_callers(self):
        self.refused(IN_PROCESS_OWNER, project="ProjectC", ray_temp_dir=C_DIR)

    def test_an_owner_file_with_two_pid_lines_is_refused(self):
        err = self.refused(owner() + "pid: 1\n")
        self.assertIn("2 pid lines", err)

    def test_an_owner_file_with_no_pid_line_is_refused(self):
        text = "".join(l for l in owner().splitlines(True) if not l.startswith("pid:"))
        err = self.refused(text)
        self.assertIn("0 pid lines", err)


# ---- release ------------------------------------------------------------------------------------


class TestRelease(LockTestCase):
    def release(self, project="ProjectA", ray_temp_dir=A_DIR):
        return self.run_cmd(rl.release, project, ray_temp_dir, lock_dir=self.lock)

    def test_pid_dash_with_no_processes_releases(self):
        self.make_lock(owner(pid="-"))
        (self.lock / "owner.tmp").write_text("leftover")
        rc, out, _ = self.release()
        self.assertEqual(rc, 0)
        self.assertIn("released the rehearsal lock", out)
        self.assertFalse(self.lock.exists())
        self.assertTrue(self.lock.parent.is_dir())

    def test_dead_pid_with_no_processes_releases(self):
        self.make_lock(owner(pid=dead_pid()))
        rc, _, _ = self.release()
        self.assertEqual(rc, 0)
        self.assertFalse(self.lock.exists())

    def test_an_in_process_owner_with_its_temp_dir_releases(self):
        self.make_lock(TEMP_DIR_IN_PROCESS_OWNER.replace("pid: 12345", "pid: -"))
        rc, _, err = self.release("ProjectC", C_DIR)
        self.assertEqual(rc, 0, err)
        self.assertFalse(self.lock.exists())

    def test_another_projects_processes_do_not_stop_it(self):
        self.ps = ps_text(
            (200, 1, f"/opt/venvs/b/raylet --temp_dir={B_DIR}"),
            (210, 1, client_server(B_ADDRESS)),
        )
        self.make_lock(owner())
        rc, _, err = self.release()
        self.assertEqual(rc, 0, err)

    def test_no_lock_returns_0(self):
        rc, out, _ = self.release()
        self.assertEqual(rc, 0)
        self.assertIn("no lock to release", out)
        self.assertFalse(self.lock.exists())

    def refused(self, text, project="ProjectA", ray_temp_dir=A_DIR):
        self.make_lock(text)
        before = self.tree()
        rc, out, err = self.release(project, ray_temp_dir)
        self.assertEqual(rc, 1, out + err)
        self.assertUntouched(before)
        return err

    def test_another_project_is_refused_and_both_sides_printed(self):
        err = self.refused(owner("ProjectB", B_DIR, B_ADDRESS))
        self.assertIn("ProjectB", err)
        self.assertIn("ProjectA", err)
        self.assertIn(B_DIR, err)
        self.assertIn(A_DIR, err)

    def test_the_same_project_with_another_temp_dir_is_refused(self):
        err = self.refused(owner("ProjectA", B_DIR, A_ADDRESS))
        self.assertIn("ray_temp_dir is '/tmp/ray-b', not '/tmp/ray-a'", err)
        self.assertIn("caller: project: ProjectA, ray_temp_dir: /tmp/ray-a", err)

    def test_another_project_with_the_callers_temp_dir_is_refused(self):
        err = self.refused(owner("ProjectB", A_DIR, A_ADDRESS))
        self.assertIn("project is 'ProjectB', not 'ProjectA'", err)
        self.assertIn("caller: project: ProjectA, ray_temp_dir: /tmp/ray-a", err)

    def test_an_in_process_owner_is_never_the_callers(self):
        self.refused(
            IN_PROCESS_OWNER.replace("pid: 12345", "pid: -"), "ProjectC", C_DIR
        )

    def test_no_owner_file_is_refused(self):
        err = self.refused(None)
        self.assertIn("no owner file", err)
        self.assertIn("ProjectA", err)

    def test_a_live_pid_is_refused(self):
        err = self.refused(owner(pid=os.getpid()))
        self.assertIn(f"the recorded pid {os.getpid()} is alive", err)

    def test_a_process_of_the_temp_dir_is_refused_with_pid_dash(self):
        self.ps = A_PS
        err = self.refused(owner(pid="-"))
        self.assertIn("    100 1 ", err)

    def test_a_process_of_the_temp_dir_is_refused_with_a_dead_pid(self):
        self.ps = A_PS
        self.refused(owner(pid=dead_pid()))

    def test_the_owners_client_server_alone_is_refused(self):
        self.ps = ps_text((300, 1, client_server(A_ADDRESS)))
        err = self.refused(owner(pid="-"))
        self.assertIn("    300 1 ", err)

    def test_an_unreadable_table_is_refused(self):
        for exc in (UNREADABLE, OSError("no ps")):
            with self.subTest(exc=exc):
                self.ps = exc
                self.make_lock(owner(pid="-"))
                before = self.tree()
                rc, _, err = self.release()
                self.assertEqual(rc, 1, err)
                self.assertUntouched(before)
                self.assertIn("cannot read the process table", err)
                for name in ("owner",):
                    os.remove(self.lock / name)
                os.rmdir(self.lock)

    def test_an_owner_address_that_is_not_usable_is_refused(self):
        err = self.refused(owner(ray_address="local", pid=dead_pid()))
        self.assertIn("ray_address 'local'", err)


# ---- the process rule ---------------------------------------------------------------------------


class TestRayProcesses(LockTestCase):
    def pids(self, text, ray_temp_dir=A_DIR, ray_address=None, self_pid=9999):
        return [
            p
            for p, _, _ in rl.ray_processes(
                ray_temp_dir, ray_address, ps_text=text, self_pid=self_pid
            )
        ]

    def test_the_tree_at_ray_2_43(self):
        self.assertEqual(self.pids(TREE_243, self_pid=7000), LISTED_243)
        self.assertEqual(
            self.pids(TREE_243, ray_address="in-process", self_pid=7000), LISTED_243
        )

    def test_the_tree_at_ray_2_55(self):
        self.assertEqual(self.pids(TREE_255, self_pid=7000), LISTED_255)

    def test_the_reaper_and_the_driver_are_not_listed(self):
        for tree, reaper, driver in ((TREE_243, 6170, 6169), (TREE_255, 6221, 6212)):
            with self.subTest(reaper=reaper):
                found = self.pids(tree, self_pid=7000)
                self.assertNotIn(reaper, found)
                self.assertNotIn(driver, found)

    def test_returns_pid_ppid_and_the_whole_command(self):
        found = rl.ray_processes(A_DIR, ps_text=A_PS, self_pid=9999)
        self.assertEqual(
            found,
            [
                (
                    100,
                    1,
                    f"/opt/venvs/a/raylet --raylet_socket_name={A_DIR}/session_x/sockets/raylet",
                ),
                (101, 100, "ray::IDLE"),
                (102, 101, "ray::A.method"),
            ],
        )

    def test_a_descendant_of_a_seed_is_listed_though_it_names_nothing(self):
        text = ps_text(
            (100, 1, f"raylet --temp_dir={A_DIR}"),
            (101, 100, "ray::IDLE"),
            (102, 1, "ray::IDLE"),
        )
        self.assertEqual(self.pids(text), [100, 101])

    def test_the_private_spelling_is_matched_both_ways(self):
        text = ps_text(
            (100, 1, "raylet --temp_dir=/private/tmp/ray-a"),
            (101, 1, "raylet --temp_dir=/tmp/ray-a"),
        )
        self.assertEqual(self.pids(text, "/tmp/ray-a"), [100, 101])
        self.assertEqual(self.pids(text, "/private/tmp/ray-a"), [100, 101])

    def test_a_private_spelling_command_alone_is_listed(self):
        text = ps_text((100, 1, "raylet --temp_dir=/private/tmp/ray-a"))
        self.assertEqual(self.pids(text, "/tmp/ray-a"), [100])

    def test_a_tmp_spelling_command_alone_is_listed_for_the_private_spelling(self):
        text = ps_text((100, 1, "raylet --temp_dir=/tmp/ray-a"))
        self.assertEqual(self.pids(text, "/private/tmp/ray-a"), [100])

    def test_private_is_stripped_only_as_a_whole_component(self):
        text = ps_text(
            (100, 1, "raylet --temp_dir=/tmp/er/ray-a"),
            (101, 1, "raylet --temp_dir=/privateer/ray-a"),
        )
        self.assertEqual(self.pids(text, "/privateer/ray-a"), [101])

    def test_the_match_is_a_whole_path_component(self):
        for command in (
            "raylet --temp_dir=/tmp/ray-ab",
            "raylet --temp_dir=/tmp/ray-a.old",
            "raylet --temp_dir=/tmp/ray-a-2/session",
            "raylet --temp_dir=/tmp/ray",
            "raylet --temp_dir=/tmp/ray/session_x",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.pids(ps_text((100, 1, command))), [])

    def test_the_directory_is_matched_literally(self):
        text = ps_text((100, 1, "raylet --temp_dir=/tmp/rayXa"))
        self.assertEqual(self.pids(text, "/tmp/ray.a"), [])
        text = ps_text((100, 1, "raylet --temp_dir=/tmp/ray.a"))
        self.assertEqual(self.pids(text, "/tmp/ray.a"), [100])

    def test_the_match_ends_at_a_slash_a_space_an_equals_or_the_end(self):
        for command in (
            "raylet --log_dir=/tmp/ray-a/session_x/logs",
            "gcs_server --temp-dir /tmp/ray-a --port=0",
            "python -c x --temp-dir=/tmp/ray-a=",
            "ray start --head --temp-dir=/tmp/ray-a",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.pids(ps_text((100, 1, command))), [100])

    def test_any_command_naming_the_temp_dir_is_listed(self):
        text = ps_text(
            (100, 1, "tail -f /tmp/ray-a/session_latest/logs/raylet.out"),
            (101, 1, "pgrep -lf gcs_server|raylet|ray::"),
            (102, 1, "grep ray"),
        )
        self.assertEqual(self.pids(text), [100])

    def test_the_client_server_of_the_address_is_listed(self):
        text = ps_text(
            (300, 1, client_server("127.0.0.1:6400")),
            (301, 300, "ray::IDLE"),
        )
        self.assertEqual(self.pids(text, ray_address="127.0.0.1:6400"), [300, 301])

    def test_the_client_server_must_name_the_whole_address(self):
        for address in ("127.0.0.1:6401", "127.0.0.1:64000", "127.0.0.2:6400"):
            with self.subTest(address=address):
                text = ps_text((300, 1, client_server(address)))
                self.assertEqual(self.pids(text, ray_address="127.0.0.1:6400"), [])

    def test_the_client_server_address_may_end_the_line(self):
        text = ps_text(
            (
                300,
                1,
                f"{PY} -m ray.util.client.server --port=6401 --address=127.0.0.1:6400",
            )
        )
        self.assertEqual(self.pids(text, ray_address="127.0.0.1:6400"), [300])

    def test_an_address_alone_is_not_a_client_server(self):
        text = ps_text((300, 1, f"{PY} driver.py --address=127.0.0.1:6400"))
        self.assertEqual(self.pids(text, ray_address="127.0.0.1:6400"), [])

    def test_no_client_server_seed_in_process_or_with_no_address(self):
        text = ps_text((300, 1, client_server("127.0.0.1:6400")))
        self.assertEqual(self.pids(text, ray_address="in-process"), [])
        self.assertEqual(self.pids(text, ray_address=None), [])

    def test_another_projects_processes_are_not_listed(self):
        text = ps_text(
            (200, 1, f"/opt/venvs/b/raylet --temp_dir={B_DIR} --session_dir={B_DIR}/s"),
            (201, 200, "ray::IDLE"),
            (210, 1, client_server(B_ADDRESS)),
            (211, 210, "ray::IDLE"),
        )
        self.assertEqual(self.pids(text, ray_address=A_ADDRESS), [])

    def test_this_process_its_ancestors_and_its_children_are_never_listed(self):
        text = ps_text(
            (400, 1, f"bash run.sh --ray-temp-dir {A_DIR}"),
            (
                401,
                400,
                f"python -m raypoolkit.rehearsal_lock status --ray-temp-dir {A_DIR}",
            ),
            (402, 401, "ps -axww -o pid= -o ppid= -o command="),
            (403, 402, "a grandchild"),
        )
        self.assertEqual(self.pids(text, self_pid=401), [])

    def test_an_ancestor_naming_the_temp_dir_seeds_its_other_children(self):
        text = ps_text(
            (400, 1, f"bash run.sh --ray-temp-dir {A_DIR}"),
            (401, 400, "python -m raypoolkit.rehearsal_lock release"),
            (402, 400, "sleep 60"),
            (403, 402, "a grandchild"),
        )
        self.assertEqual(self.pids(text, self_pid=401), [402, 403])

    def test_lines_that_do_not_parse_are_skipped(self):
        text = "  PID  PPID COMMAND\n\ngarbage\n" + A_PS + "12x 1 /tmp/ray-a\n"
        self.assertEqual(self.pids(text), [100, 101, 102])

    def test_reads_the_process_table_through_one_function(self):
        with mock.patch.object(rl, "_ps_output", return_value=A_PS) as ps:
            self.assertEqual(
                [p for p, _, _ in rl.ray_processes(A_DIR, self_pid=9999)],
                [100, 101, 102],
            )
        ps.assert_called_once_with()

    def test_the_default_self_pid_is_this_process(self):
        text = ps_text(
            (os.getpid(), 1, f"python --ray-temp-dir {A_DIR}"),
            (os.getpid() + 1, 1, f"raylet --temp_dir={A_DIR}"),
        )
        self.assertEqual(
            [p for p, _, _ in rl.ray_processes(A_DIR, ps_text=text)],
            [os.getpid() + 1],
        )

    def test_a_failing_ps_raises_runtime_error(self):
        failed = subprocess.CompletedProcess(rl.PS_COMMAND, 1, stdout="", stderr="")
        with mock.patch.object(rl.subprocess, "run", return_value=failed) as run:
            with self.assertRaises(RuntimeError):
                REAL_PS_OUTPUT()
        self.assertEqual(run.call_args.args[0], rl.PS_COMMAND)
        self.assertEqual(
            rl.PS_COMMAND,
            ["ps", "-axww", "-o", "pid=", "-o", "ppid=", "-o", "command="],
        )

    def test_bad_arguments_raise_value_error(self):
        for args in (
            ("tmp/ray-a",),
            ("/tmp/ray-a/",),
            ("in-process",),
            (A_DIR, "local"),
        ):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    rl.ray_processes(*args, ps_text="", self_pid=1)


# ---- the locations ------------------------------------------------------------------------------


class TestLocations(LockTestCase):
    def test_both_locations_follow_home_changed_after_import(self):
        self.assertEqual(rl.default_lock_dir(), self.new_default)
        self.assertEqual(rl.old_lock_dir(), self.old)
        other = self.tmp / "other"
        other.mkdir()
        with mock.patch.dict(os.environ, {"HOME": str(other)}):
            self.assertEqual(
                rl.default_lock_dir(), other / ".raypoolkit" / "rehearsal-lock"
            )
            self.assertEqual(
                rl.old_lock_dir(), other / "ScienceData" / ".rehearsal-lock"
            )
        self.assertEqual(list(self.home.iterdir()), [])
        self.assertEqual(list(other.iterdir()), [])

    def test_commands_without_lock_dir_use_the_patched_home(self):
        rc, _, err = self.run_cmd(rl.acquire, "ProjectA", "p", A_DIR, A_ADDRESS)
        self.assertEqual(rc, 0, err)
        self.assertTrue((self.new_default / "owner").is_file())
        rc, out, _ = self.run_cmd(rl.status)
        self.assertIn(f"lock: HELD ({self.new_default})", out)
        rc, _, err = self.run_cmd(rl.set_pid, "ProjectA", A_DIR, os.getpid())
        self.assertEqual(rc, 0, err)
        rc, _, _ = self.run_cmd(rl.release, "ProjectA", A_DIR)
        self.assertEqual(rc, 1)
        (self.new_default / "owner").write_text(owner(pid="-"))
        rc, _, err = self.run_cmd(rl.release, "ProjectA", A_DIR)
        self.assertEqual(rc, 0, err)
        self.assertFalse(self.new_default.exists())
        self.assertTrue(self.new_default.parent.is_dir())

    def test_no_environment_variable_moves_the_lock(self):
        elsewhere = self.tmp / "elsewhere"
        variables = {
            name: str(elsewhere / name)
            for name in (
                "RAYPOOLKIT_REHEARSAL_LOCK",
                "RAYPOOLKIT_REHEARSAL_LOCK_DIR",
                "RAYPOOLKIT_LOCK_DIR",
                "REHEARSAL_LOCK",
                "REHEARSAL_LOCK_DIR",
                "XDG_STATE_HOME",
                "XDG_RUNTIME_DIR",
                "XDG_CONFIG_HOME",
            )
        }
        with mock.patch.dict(os.environ, variables):
            self.assertEqual(rl.default_lock_dir(), self.new_default)
            self.assertEqual(rl.old_lock_dir(), self.old)
            rc, _, err = self.run_cmd(rl.acquire, "ProjectA", "p", A_DIR, A_ADDRESS)
            self.assertEqual(rc, 0, err)
        self.assertTrue((self.new_default / "owner").is_file())
        self.assertFalse(elsewhere.exists())


# ---- the arguments ------------------------------------------------------------------------------

BAD_LINES = ["", "   ", "a\nb", "a\r", "a\n", "a\x0bb"]
BAD_TEMP_DIRS = [
    "",
    "tmp/ray-a",
    "/tmp/ray-a/",
    "/tmp/../tmp/ray-a",
    "/tmp/./ray-a",
    "/tmp//ray-a",
    "in-process",
    "/tmp/ray-a\nx",
]
BAD_ADDRESSES = [
    "",
    "local",
    "auto",
    "127.0.0.1",
    ":6400",
    "127.0.0.1:",
    "127.0.0.1:64a",
    "127.0.0.1:-1",
    "127.0.0.1: 6400",
    "a b:6400",
    "127.0.0.1:6400\n",
]
BAD_PIDS = [0, -1, True, "12", 1.5, None]
BAD_PID_TEXTS = ["0", "-1", "x", "+5", "1.5", " 5", ""]


class TestArguments(LockTestCase):
    def assertRefusedByFunction(self, func, *args, **kwargs):
        before = self.tree()
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):
                func(*args, lock_dir=self.lock, **kwargs)
        self.assertUntouched(before)

    def assertRefusedByCommandLine(self, argv):
        before = self.tree()
        rc, _, err = self.run_main(argv)
        self.assertEqual(rc, 2, err)
        self.assertUntouched(before)

    def test_project_and_purpose_must_be_one_non_empty_line(self):
        for bad in BAD_LINES:
            with self.subTest(bad=bad):
                self.assertRefusedByFunction(rl.acquire, bad, "p", A_DIR, A_ADDRESS)
                self.assertRefusedByFunction(rl.acquire, "P", bad, A_DIR, A_ADDRESS)
                self.assertRefusedByFunction(rl.set_pid, bad, A_DIR, os.getpid())
                self.assertRefusedByFunction(rl.release, bad, A_DIR)
                self.assertRefusedByCommandLine(
                    ["acquire", "--project", bad, "--purpose", "p"]
                    + ["--ray-temp-dir", A_DIR, "--ray-address", A_ADDRESS]
                )
                self.assertRefusedByCommandLine(
                    ["acquire", "--project", "P", "--purpose", bad]
                    + ["--ray-temp-dir", A_DIR, "--ray-address", A_ADDRESS]
                )
                self.assertRefusedByCommandLine(
                    ["set-pid", "--project", bad, "--ray-temp-dir", A_DIR, "1"]
                )
                self.assertRefusedByCommandLine(
                    ["release", "--project", bad, "--ray-temp-dir", A_DIR]
                )

    def test_ray_temp_dir_must_be_absolute_normal_and_not_in_process(self):
        for bad in BAD_TEMP_DIRS:
            with self.subTest(bad=bad):
                self.assertRefusedByFunction(rl.acquire, "P", "p", bad, A_ADDRESS)
                self.assertRefusedByFunction(rl.set_pid, "P", bad, os.getpid())
                self.assertRefusedByFunction(rl.release, "P", bad)
                self.assertRefusedByFunction(rl.status, bad)
                with self.assertRaises(ValueError):
                    rl.ray_processes_command(bad)
                self.assertRefusedByCommandLine(
                    ["acquire", "--project", "P", "--purpose", "p"]
                    + ["--ray-temp-dir", bad, "--ray-address", A_ADDRESS]
                )
                self.assertRefusedByCommandLine(
                    ["set-pid", "--project", "P", "--ray-temp-dir", bad, "1"]
                )
                self.assertRefusedByCommandLine(
                    ["release", "--project", "P", "--ray-temp-dir", bad]
                )
                self.assertRefusedByCommandLine(["status", "--ray-temp-dir", bad])
                self.assertRefusedByCommandLine(
                    ["ray-processes", "--ray-temp-dir", bad]
                )

    def test_ray_address_must_be_in_process_or_host_port(self):
        for bad in BAD_ADDRESSES:
            with self.subTest(bad=bad):
                self.assertRefusedByFunction(rl.acquire, "P", "p", A_DIR, bad)
                self.assertRefusedByFunction(rl.status, A_DIR, bad)
                with self.assertRaises(ValueError):
                    rl.ray_processes_command(A_DIR, bad)
                self.assertRefusedByCommandLine(
                    ["acquire", "--project", "P", "--purpose", "p"]
                    + ["--ray-temp-dir", A_DIR, "--ray-address", bad]
                )
                self.assertRefusedByCommandLine(
                    ["status", "--ray-temp-dir", A_DIR, "--ray-address", bad]
                )
                self.assertRefusedByCommandLine(
                    ["ray-processes", "--ray-temp-dir", A_DIR, "--ray-address", bad]
                )

    def test_good_addresses_are_accepted(self):
        for good in ("in-process", "127.0.0.1:6400", "head.example:1", "[::1]:6379"):
            with self.subTest(good=good):
                rc, _, err = self.run_cmd(
                    rl.acquire, "P", "p", A_DIR, good, lock_dir=self.lock
                )
                self.assertEqual(rc, 0, err)
                rc, _, err = self.run_cmd(rl.release, "P", A_DIR, lock_dir=self.lock)
                self.assertEqual(rc, 0, err)

    def test_pid_must_be_a_positive_integer(self):
        self.make_lock(owner())
        for bad in BAD_PIDS:
            with self.subTest(bad=bad):
                self.assertRefusedByFunction(rl.set_pid, "ProjectA", A_DIR, bad)
        for bad in BAD_PID_TEXTS:
            with self.subTest(bad=bad):
                self.assertRefusedByCommandLine(
                    ["set-pid", "--project", "ProjectA", "--ray-temp-dir", A_DIR, bad]
                )

    def test_status_takes_an_address_only_with_a_temp_dir(self):
        self.assertRefusedByFunction(rl.status, None, A_ADDRESS)
        self.assertRefusedByCommandLine(["status", "--ray-address", A_ADDRESS])


# ---- the owner file -----------------------------------------------------------------------------


class TestOwnerFile(LockTestCase):
    def test_the_three_shapes_written_today_parse(self):
        cluster = rl.parse_owner(CLUSTER_OWNER)
        self.assertEqual(list(cluster), list(rl.OWNER_KEYS))
        self.assertEqual(cluster["project"], "ProjectA")
        self.assertEqual(cluster["ray_temp_dir"], "/tmp/ray-a")
        self.assertEqual(cluster["ray_address"], "127.0.0.1:6400")
        self.assertEqual(cluster["acquired"], "2026-10-12T14:19:31+01:00")
        self.assertEqual(cluster["pid"], "-")
        self.assertIsNone(rl._recorded_pid(cluster))
        in_process = rl.parse_owner(IN_PROCESS_OWNER)
        self.assertEqual(list(in_process), list(rl.OWNER_KEYS))
        self.assertEqual(in_process["ray_temp_dir"], "in-process")
        self.assertEqual(in_process["ray_address"], "in-process")
        self.assertEqual(rl._recorded_pid(in_process), 12345)

    def test_the_identity_check_judges_each_shape(self):
        cluster = rl.parse_owner(CLUSTER_OWNER)
        self.assertIsNone(rl._not_callers_reason(cluster, "ProjectA", A_DIR))
        self.assertIsNotNone(rl._not_callers_reason(cluster, "ProjectB", A_DIR))
        self.assertIsNotNone(rl._not_callers_reason(cluster, "ProjectA", B_DIR))
        # no valid caller passes ``in-process`` as a temp dir, so this lock is nobody's to touch
        in_process = rl.parse_owner(IN_PROCESS_OWNER)
        self.assertIsNotNone(rl._not_callers_reason(in_process, "ProjectC", C_DIR))
        temp_dir = rl.parse_owner(TEMP_DIR_IN_PROCESS_OWNER)
        self.assertIsNone(rl._not_callers_reason(temp_dir, "ProjectC", C_DIR))
        self.assertEqual(rl._recorded_pid(temp_dir), 12345)

    def test_a_missing_key_is_not_the_callers(self):
        text = CLUSTER_OWNER.replace("ray_temp_dir: /tmp/ray-a\n", "")
        self.assertIsNotNone(
            rl._not_callers_reason(rl.parse_owner(text), "ProjectA", A_DIR)
        )

    def test_value_is_everything_after_the_first_colon_space(self):
        parsed = rl.parse_owner("purpose: a: b: c\npid: -\n")
        self.assertEqual(parsed["purpose"], "a: b: c")

    def test_round_trips_its_own_file(self):
        text = rl.owner_text(
            "ProjectA", "p: q", A_DIR, A_ADDRESS, "123", acquired=PAST, host="h"
        )
        self.assertEqual(
            rl.parse_owner(text),
            {
                "project": "ProjectA",
                "purpose": "p: q",
                "acquired": PAST,
                "host": "h",
                "ray_temp_dir": A_DIR,
                "ray_address": A_ADDRESS,
                "pid": "123",
            },
        )

    def test_a_pid_that_is_not_a_number_is_no_pid(self):
        for value in ("-", "", "abc", "12a", " "):
            with self.subTest(value=value):
                self.assertIsNone(rl._recorded_pid({"pid": value}))
        self.assertIsNone(rl._recorded_pid({}))

    def test_pid_alive(self):
        self.assertTrue(rl.pid_alive(os.getpid()))
        self.assertFalse(rl.pid_alive(dead_pid()))
        self.assertFalse(rl.pid_alive(0))


# ---- the command line ---------------------------------------------------------------------------


class TestCommandLine(LockTestCase):
    ACQUIRE = [
        "acquire",
        "--project",
        "ProjectA",
        "--purpose",
        "p",
        "--ray-temp-dir",
        A_DIR,
        "--ray-address",
        A_ADDRESS,
    ]
    CALLER = ["--project", "ProjectA", "--ray-temp-dir", A_DIR]

    def test_commands_and_exit_statuses(self):
        self.assertEqual(self.run_main(["status"])[0], 0)
        self.assertEqual(self.run_main(self.ACQUIRE)[0], 0)
        self.assertEqual(self.run_main(self.ACQUIRE)[0], 3)
        self.assertEqual(
            self.run_main(["set-pid", *self.CALLER, str(dead_pid())])[0], 1
        )
        self.assertEqual(
            self.run_main(["set-pid", *self.CALLER, str(os.getpid())])[0], 0
        )
        self.assertEqual(self.run_main(["release", *self.CALLER])[0], 1)
        self.assertEqual(self.run_main(["status"])[0], 0)
        self.assertEqual(
            self.run_main(["ray-processes", "--ray-temp-dir", A_DIR])[0], 0
        )
        (self.new_default / "owner").write_text(owner(pid="-"))
        self.ps = A_PS
        rc, out, _ = self.run_main(["ray-processes", "--ray-temp-dir", A_DIR])
        self.assertEqual(rc, 1)
        self.assertEqual(
            out.splitlines(),
            [
                f"100 1 /opt/venvs/a/raylet --raylet_socket_name={A_DIR}/session_x/sockets/raylet",
                "101 100 ray::IDLE",
                "102 101 ray::A.method",
            ],
        )
        self.assertEqual(self.run_main(["release", *self.CALLER])[0], 1)
        self.assertEqual(self.run_main(["status"])[0], 0)
        self.ps = ""
        rc, out, _ = self.run_main(["release", *self.CALLER])
        self.assertEqual(rc, 0)
        self.assertEqual(self.run_main(["release", *self.CALLER])[0], 0)
        self.ps = UNREADABLE
        rc, _, err = self.run_main(["ray-processes", "--ray-temp-dir", A_DIR])
        self.assertEqual(rc, 1)
        self.assertIn("cannot read the process table", err)

    def test_the_client_server_option_of_ray_processes(self):
        self.ps = ps_text((300, 1, client_server(A_ADDRESS)))
        argv = ["ray-processes", "--ray-temp-dir", A_DIR]
        self.assertEqual(self.run_main(argv)[0], 0)
        self.assertEqual(self.run_main(argv + ["--ray-address", A_ADDRESS])[0], 1)

    def test_a_listed_command_is_cut_to_150_characters(self):
        long_command = f"raylet --temp_dir={A_DIR} " + "x" * 300
        self.ps = ps_text((100, 1, long_command))
        rc, out, _ = self.run_main(["ray-processes", "--ray-temp-dir", A_DIR])
        self.assertEqual(rc, 1)
        self.assertEqual(out, f"100 1 {long_command[:150]}\n")

    def status_lines(self, *args):
        rc, out, err = self.run_cmd(rl.status, *args, lock_dir=self.lock)
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        return out.splitlines()

    def test_status_free(self):
        self.assertEqual(
            self.status_lines(),
            [
                f"lock: free ({self.lock} does not exist)",
                "Ray processes: no temp dir given",
            ],
        )
        self.assertEqual(
            self.status_lines(A_DIR),
            [
                f"lock: free ({self.lock} does not exist)",
                "Ray processes of /tmp/ray-a: none",
            ],
        )

    def test_status_held_with_no_pid(self):
        self.make_lock(owner())
        self.assertEqual(
            self.status_lines(),
            [
                f"lock: HELD ({self.lock})",
                "    project: ProjectA",
                "    purpose: earlier",
                f"    acquired: {PAST}",
                "    host: h",
                "    ray_temp_dir: /tmp/ray-a",
                "    ray_address: 127.0.0.1:6400",
                "    pid: -",
                "owner pid: - (no pid recorded yet)",
                "Ray processes of /tmp/ray-a: none",
            ],
        )

    def test_status_held_with_a_live_and_a_dead_pid(self):
        pid = os.getpid()
        self.make_lock(owner(pid=pid))
        lines = self.status_lines()
        self.assertEqual(lines[8], f"owner pid {pid}: alive")
        (self.lock / "owner").write_text(owner(pid=(gone := dead_pid())))
        lines = self.status_lines()
        self.assertEqual(
            lines[7:],
            [
                f"    pid: {gone}",
                f"owner pid {gone}: NOT alive",
                "Ray processes of /tmp/ray-a: none",
            ],
        )

    def test_status_held_with_no_owner_file_and_the_old_location_present(self):
        self.make_lock(None)
        self.make_lock(None, where=self.old)
        self.assertEqual(
            self.status_lines(),
            [
                f"lock: HELD ({self.lock})",
                "    (no owner file)",
                f"old location: PRESENT ({self.old})",
                "Ray processes: no temp dir given",
            ],
        )

    def test_status_free_with_the_old_location_present(self):
        self.make_lock(owner(), where=self.old)
        self.assertEqual(
            self.status_lines(),
            [
                f"lock: free ({self.lock} does not exist)",
                f"old location: PRESENT ({self.old})",
                "Ray processes: no temp dir given",
            ],
        )

    def test_status_with_processes_of_the_owners_temp_dir_and_address(self):
        self.ps = A_PS + ps_text((300, 1, client_server(A_ADDRESS)))
        self.make_lock(owner(pid="-"))
        lines = self.status_lines()
        self.assertEqual(
            lines[8:],
            [
                "owner pid: - (no pid recorded yet)",
                "Ray processes of /tmp/ray-a: 4",
                f"    100 1 /opt/venvs/a/raylet --raylet_socket_name={A_DIR}/session_x/sockets/raylet",
                "    101 100 ray::IDLE",
                "    102 101 ray::A.method",
                f"    300 1 {client_server(A_ADDRESS)}",
            ],
        )

    def test_status_with_a_temp_dir_given_uses_it_not_the_owners(self):
        self.ps = ps_text(
            (200, 1, f"raylet --temp_dir={B_DIR}"), (300, 1, client_server(A_ADDRESS))
        )
        self.make_lock(owner())
        self.assertEqual(
            self.status_lines(B_DIR)[9:],
            ["Ray processes of /tmp/ray-b: 1", f"    200 1 raylet --temp_dir={B_DIR}"],
        )

    def test_status_with_owner_values_that_are_not_usable(self):
        for shape in (
            IN_PROCESS_OWNER,
            owner(ray_address="local"),
            CLUSTER_OWNER.replace("ray_address: 127.0.0.1:6400\n", ""),
        ):
            with self.subTest(shape=shape):
                self.make_lock(shape)
                self.assertEqual(
                    self.status_lines()[-1],
                    "Ray processes: the owner's ray_temp_dir or ray_address is not usable",
                )
                os.remove(self.lock / "owner")
                os.rmdir(self.lock)

    def test_status_with_an_unreadable_table(self):
        self.ps = UNREADABLE
        self.assertEqual(
            self.status_lines(A_DIR),
            [
                f"lock: free ({self.lock} does not exist)",
                "Ray processes of /tmp/ray-a: cannot read the process table "
                "(ps failed with status 1)",
            ],
        )

    def test_status_through_main_uses_the_default_location(self):
        rc, out, _ = self.run_main(
            ["status", "--ray-temp-dir", A_DIR, "--ray-address", A_ADDRESS]
        )
        self.assertEqual(rc, 0)
        self.assertEqual(
            out.splitlines(),
            [
                f"lock: free ({self.new_default} does not exist)",
                "Ray processes of /tmp/ray-a: none",
            ],
        )

    def test_usage_errors_exit_2(self):
        for argv in (
            [],
            ["nonsense"],
            ["acquire"],
            ["acquire", "--project", "P", "--purpose", "p", "--ray-temp-dir", A_DIR],
            ["set-pid", *self.CALLER],
            ["set-pid", "--project", "P", "1"],
            ["release", "--project", "P"],
            ["ray-processes"],
        ):
            with self.subTest(argv=argv):
                self.assertEqual(self.run_main(argv)[0], 2)

    def test_there_is_no_option_to_break_wait_retry_or_move_the_lock(self):
        for argv in (
            self.ACQUIRE + ["--force"],
            self.ACQUIRE + ["--wait"],
            self.ACQUIRE + ["--retry"],
            self.ACQUIRE + ["--lock-dir", str(self.lock)],
            ["release", *self.CALLER, "--force"],
            ["release", *self.CALLER, "--break"],
            ["release", *self.CALLER, "--lock-dir", str(self.lock)],
            ["set-pid", *self.CALLER, "1", "--retry"],
            ["status", "--lock-dir", str(self.lock)],
            ["ray-processes", "--ray-temp-dir", A_DIR, "--wait"],
        ):
            with self.subTest(argv=argv):
                self.assertEqual(self.run_main(argv)[0], 2)
        self.assertFalse(self.lock.exists())
        options = set()
        parser = rl.build_parser()
        for action in parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                for sub in action.choices.values():
                    for sub_action in sub._actions:
                        options.update(sub_action.option_strings)
        self.assertEqual(
            options,
            {
                "-h",
                "--help",
                "--project",
                "--purpose",
                "--ray-temp-dir",
                "--ray-address",
            },
        )


class TestLicenceHeader(LockTestCase):
    def test_the_module_opens_with_the_licence_header(self):
        source = Path(rl.__file__).read_text(encoding="utf-8")
        self.assertEqual("".join(source.splitlines(True)[:15]), LICENCE_HEADER)


if __name__ == "__main__":
    unittest.main()
