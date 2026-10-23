"""
The package's import guard: ``raypoolkit`` imports only the standard library, ``ray`` and itself.

1. Every module under ``raypoolkit/`` (the tests included) is parsed with ``ast``, and every module
   it imports is collected, at any depth, so imports inside functions and classes are included. A
   relative import is resolved against the package the module sits in. The root of each imported
   module must be in ``sys.stdlib_module_names``, or be ``ray`` or ``raypoolkit``.
2. In a fresh, isolated interpreter (``-I``, run from an empty temporary directory, so that the
   package is found only through its installation), the package and its two public names import,
   and no client module and no ``datastorekit`` has been loaded.
3. In a fresh, isolated interpreter, the re-export of the class from the package root is pinned
   (see that test's docstring).
4. ``raypoolkit/rehearsal_lock.py`` imports only the standard library: neither ``ray`` nor the
   rest of the package.
5. In a fresh, isolated interpreter, ``python -I -m raypoolkit.rehearsal_lock --help`` exits 0 and
   loads no client module and no ``datastorekit``. It does load ``ray``, through the package root.

This guard is about imports only. Ray is imported by the child interpreters, never started.
"""

import ast
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_NAME = "raypoolkit"
PACKAGE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_ROOTS = {"ray", PACKAGE_NAME}

# modules that must not be loaded by importing the package: DatastoreKit, and the client modules
# the pool's source imported
FORBIDDEN_ROOTS = ("datastorekit", "Datastore", "RayTools", "utilities")

# importing ray takes several seconds; allow plenty
CHILD_TIMEOUT = 300


def _package_parts(path: Path):
    """The dotted package that ``path`` sits in, as a list of names."""
    relative = path.relative_to(PACKAGE_DIR.parent)
    return list(relative.parent.parts)


def imported_modules(path: Path):
    """Every module ``path`` imports, as (line, dotted name), relative imports resolved."""
    tree = ast.parse(path.read_text(), filename=str(path))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                found.append((node.lineno, node.module))
                continue
            parts = _package_parts(path)
            up = node.level - 1
            if up >= len(parts):
                found.append(
                    (node.lineno, "<relative import beyond the top-level package>")
                )
                continue
            base = parts[: len(parts) - up]
            if node.module:
                base = base + node.module.split(".")
            found.append((node.lineno, ".".join(base)))
    return found


def _run_child(code: str):
    """Run ``code`` in a fresh, isolated interpreter from an empty temporary directory."""
    with tempfile.TemporaryDirectory() as cwd:
        return subprocess.run(
            [sys.executable, "-I", "-c", code],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=CHILD_TIMEOUT,
        )


def _run_child_args(args):
    """Run ``sys.executable`` with ``args`` from an empty temporary directory."""
    with tempfile.TemporaryDirectory() as cwd:
        return subprocess.run(
            [sys.executable, *args],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=CHILD_TIMEOUT,
        )


class TestPackageImports(unittest.TestCase):
    def test_every_import_is_stdlib_ray_or_the_package(self):
        modules = sorted(
            p for p in PACKAGE_DIR.rglob("*.py") if "__pycache__" not in p.parts
        )
        self.assertGreater(len(modules), 0)
        allowed = set(sys.stdlib_module_names) | ALLOWED_ROOTS
        offending = []
        for path in modules:
            for line, name in imported_modules(path):
                if name.split(".")[0] not in allowed:
                    offending.append(
                        f"{path.relative_to(PACKAGE_DIR.parent)}:{line}: imports {name}"
                    )
        self.assertEqual(offending, [], "\n".join(offending))

    def test_the_package_imports_with_no_client(self):
        code = (
            "import json, sys\n"
            "import raypoolkit\n"
            "from raypoolkit import RayWorkPool, DatastorePool\n"
            f"forbidden = {FORBIDDEN_ROOTS!r}\n"
            "print(json.dumps(sorted(m for m in sys.modules "
            "if m.split('.')[0] in forbidden)))\n"
        )
        result = _run_child(code)
        self.assertEqual(result.returncode, 0, result.stderr)
        loaded = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(loaded, [], f"importing the package loaded {loaded}")

    def test_the_class_is_re_exported_and_shadows_its_module(self):
        """
        Decision U4: the module keeps its source's name, ``RayWorkPool``, and the class of the same
        name is re-exported from the package root, so that a client writes
        ``from raypoolkit import RayWorkPool``.

        The consequence, pinned here for every later prompt: once ``raypoolkit/__init__.py`` binds
        the class, the package attribute ``raypoolkit.RayWorkPool`` is the **class**, and shadows
        the submodule of the same name. ``import raypoolkit.RayWorkPool as m`` gives the class too.
        The module is reachable as ``sys.modules["raypoolkit.RayWorkPool"]``, through
        ``importlib.import_module("raypoolkit.RayWorkPool")``, by
        ``from raypoolkit.RayWorkPool import ...``, and through a string target to
        ``unittest.mock.patch`` such as ``"raypoolkit.RayWorkPool.ray"``.

        **So patch the module through a string target or through ``sys.modules``, never through
        the package attribute**: ``mock.patch.object(raypoolkit.RayWorkPool, "ray", ...)`` would
        patch an attribute of the class, not the module the pool's code reads ``ray`` from.
        """
        code = """
import importlib, json, sys, types
from unittest import mock

import raypoolkit
import raypoolkit.contract
import raypoolkit.RayWorkPool as imported_as

module = sys.modules["raypoolkit.RayWorkPool"]
sentinel = object()
with mock.patch("raypoolkit.RayWorkPool.ray", sentinel):
    patched_module = module.ray is sentinel

facts = {
    "package attribute is a class": isinstance(raypoolkit.RayWorkPool, type),
    "package attribute is named RayWorkPool": raypoolkit.RayWorkPool.__name__ == "RayWorkPool",
    "import ... as gives the class": imported_as is raypoolkit.RayWorkPool,
    "sys.modules entry is a module": isinstance(module, types.ModuleType),
    "import_module gives that module": importlib.import_module("raypoolkit.RayWorkPool") is module,
    "module's class is the package's": module.RayWorkPool is raypoolkit.RayWorkPool,
    "string-target patch reaches the module": patched_module,
    "DatastorePool is contract's": raypoolkit.DatastorePool is raypoolkit.contract.DatastorePool,
}
print(json.dumps(facts))
"""
        result = _run_child(code)
        self.assertEqual(result.returncode, 0, result.stderr)
        facts = json.loads(result.stdout.strip().splitlines()[-1])
        failed = sorted(k for k, v in facts.items() if v is not True)
        self.assertEqual(failed, [], f"U4's re-export does not hold: {failed}")

    def test_the_lock_module_imports_only_the_standard_library(self):
        path = PACKAGE_DIR / "rehearsal_lock.py"
        found = imported_modules(path)
        self.assertGreater(len(found), 0)
        allowed = set(sys.stdlib_module_names) - ALLOWED_ROOTS
        offending = [
            f"{path.relative_to(PACKAGE_DIR.parent)}:{line}: imports {name}"
            for line, name in found
            if name.split(".")[0] not in allowed
        ]
        self.assertEqual(offending, [], "\n".join(offending))

    def test_the_lock_command_runs_with_no_client(self):
        """
        The literal command, ``python -I -m raypoolkit.rehearsal_lock --help``, with ``-X
        importtime`` so that every module it loads is named on stderr. ``ray`` is among them,
        imported by the package root (the rehearsal-lock campaign's decision U3), so it is not
        checked here; the module's own imports are the previous test's.
        """
        result = _run_child_args(
            ["-I", "-X", "importtime", "-m", "raypoolkit.rehearsal_lock", "--help"]
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            result.stdout.startswith("usage: python -m raypoolkit.rehearsal_lock"),
            result.stdout,
        )
        loaded = [
            line.rsplit("|", 1)[-1].strip()
            for line in result.stderr.splitlines()
            if line.startswith("import time:")
        ]
        self.assertIn(PACKAGE_NAME, loaded)
        forbidden = sorted(m for m in loaded if m.split(".")[0] in FORBIDDEN_ROOTS)
        self.assertEqual(forbidden, [], f"the lock command loaded {forbidden}")


if __name__ == "__main__":
    unittest.main()
