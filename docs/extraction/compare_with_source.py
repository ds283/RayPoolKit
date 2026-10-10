#!/usr/bin/env python3
"""
The equivalence check of the extraction campaign (prompt 01 §2.5; README §5 rule 8).

The package's ``RayWorkPool`` module is SecondaryGWKit's ``RayTools/RayWorkPool.py`` at the import
commit, changed only by the classes of difference prompt 01 §2.4 allows, and ``_timing.py`` holds
four definitions of its ``utilities.py``, byte for byte. This script checks both, from the
repository root, with the venv's interpreter:

    ./venv/bin/python docs/extraction/compare_with_source.py

It reads each source with ``git -C <SGK> show <commit>:<path>``, never from the source's working
tree, and first checks that ``RayTools/RayWorkPool.py`` at the commit is the expected blob.

**How a line of ``RayWorkPool.py`` is classified.** The source and the package file are compared
line by line (``difflib``, no junk heuristic). Lines that are equal need no class. Where a run of
source lines is replaced by a run of package lines *of the same length*, each pair is taken in
turn, and each class is a *rule*: a substitution applied to the source line, giving the line the
package must hold. The pair takes the class whose image of the source line equals the package line
exactly, indentation included; it must be exactly one class. A pair that no rule maps, and every
line added or deleted (a run replaced by one of a different length is treated as such), is
UNCLASSIFIED. No line number appears in any rule.

- **D-imp**, the import rewrite. The source line is one whole ``from <module> import <name>``
  statement (parsed with ``ast``: one ``ImportFrom``, level 0, one alias, no ``as``), spelled as
  ``ast.unparse`` spells it, and ``(<module>, <name>)`` is a key of ``IMPORT_MAP``. Its image is the
  statement of the mapped ``(module, name)``, at the same indentation. The map has two entries;
  anything else, an alias included, is not D-imp.
- **D-pool**, the type hint. The source line is one function parameter, ``<name>: ShardedPool,``
  (parsed with ``ast`` as the only parameter of a function, with no default, its annotation the bare
  name), and ``ShardedPool`` occurs on it once. Its image is the line with that one identifier
  replaced by ``DatastorePool``.
- There is **no D-fmt rule**. ``black`` 25.1.0 leaves the source unchanged and the rewritten lines
  are no longer than their sources, so formatting accounts for no difference; a line ``black`` had
  changed would be UNCLASSIFIED here.

**How ``_timing.py`` is checked (D-int).** Both files are parsed with ``ast``. The four definitions
of ``TIMING_NAMES`` are found in the source by name. The package module must hold its docstring,
which names the source file and the import commit, and then exactly those four definitions, in
source order, each with a source segment equal to the source's; nothing else. In addition, its text
from the first definition to the end of the file must be the source's text over the same span, byte
for byte, and only blank lines may stand between the docstring and that span, so that a comment,
which ``ast`` does not see, is caught too.

**Every file is accounted for.** Every ``.py`` file under ``raypoolkit/`` (outside
``__pycache__``) is either a file with a source (``FILES``) or a declared new file with none
(``NO_SOURCE``). Any other is NOT DECLARED, and a declared file that is missing is MISSING; either
fails the check. A prompt that adds a file to the package declares it here.

The script prints, for each file, its count per class and every line it could not classify. It
exits 0 when every differing line is classified and every file is present and declared; 1 when not;
and 2 when it cannot run (``git`` fails, or the source blob is not the expected one). It writes
nothing.
"""

import ast
import difflib
import re
import subprocess
import sys
from pathlib import Path

# --- the source -----------------------------------------------------------------------------------

SGK_PATH = "/Users/ds283/Documents/Code/SecondaryGWKit"
IMPORT_COMMIT = "b510bc90b66985532d28996ab4e5b13b0ff71709"
POOL_SOURCE_PATH = "RayTools/RayWorkPool.py"
POOL_SOURCE_BLOB = "b4666fa89abb26829fd585b881947d7ef5172cea"

REPO_ROOT = Path(__file__).resolve().parents[2]

# --- the classes of difference (prompt 01 §2.4) ---------------------------------------------------

# D-imp: whole `from <module> import <name>` statements, (module, name) -> (module, name)
IMPORT_MAP = {
    ("Datastore.SQL.ShardedPool", "ShardedPool"): (
        "raypoolkit.contract",
        "DatastorePool",
    ),
    ("utilities", "format_time"): ("raypoolkit._timing", "format_time"),
}

# D-pool: the one identifier of a parameter annotation, old -> new
POOL_HINT = ("ShardedPool", "DatastorePool")

# D-int: the definitions internalised from the source's utilities module
TIMING_NAMES = (
    "SECONDS_PER_MINUTE",
    "SECONDS_PER_HOUR",
    "SECONDS_PER_DAY",
    "format_time",
)

# --- the files ------------------------------------------------------------------------------------

# package file -> (how it is compared, its source path at the import commit)
FILES = {
    "raypoolkit/RayWorkPool.py": ("module", POOL_SOURCE_PATH),
    "raypoolkit/_timing.py": ("internalised", "utilities.py"),
}

# package files with no source, and the prompt that declared each
NO_SOURCE = {
    "raypoolkit/__init__.py": "01 §2.2: the re-export of RayWorkPool and DatastorePool",
    "raypoolkit/contract.py": "01 §2.3: the DatastorePool protocol",
    "raypoolkit/tests/__init__.py": "01 §2.2: empty",
    "raypoolkit/tests/test_package_imports.py": "01 §2.7: the import guard",
    "raypoolkit/tests/standins.py": "02 §2.1: the Ray, clock, work-object and pool stand-ins",
    "raypoolkit/tests/test_standins.py": "02 §2.1: the stand-ins' own tests",
    "raypoolkit/tests/test_construction.py": "02 §2.3: the constructor",
    "raypoolkit/tests/test_task_builder.py": "02 §2.3: the task builder's outcomes",
    "raypoolkit/tests/test_run_paths.py": "02 §2.3: the paths through the dispatch loop",
    "raypoolkit/tests/test_scheduling.py": "02 §2.3: the queue and batch sizes",
    "raypoolkit/tests/test_printed_lines.py": "02 §2.3: the printed lines (U9)",
    "raypoolkit/tests/test_inherited_faults.py": "02 §2.3: faults 1-4, pinned as they behave",
}


class CannotRun(Exception):
    pass


def git(*args) -> str:
    result = subprocess.run(
        ["git", "-C", SGK_PATH, *args], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise CannotRun(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def source_text(path: str) -> str:
    return git("show", f"{IMPORT_COMMIT}:{path}")


# --- the rules ------------------------------------------------------------------------------------


def _indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip())]


def d_imp(source_line: str):
    """The image of ``source_line`` under D-imp, or None if the rule does not apply to it."""
    try:
        tree = ast.parse(source_line.strip())
    except SyntaxError:
        return None
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.ImportFrom):
        return None
    node = tree.body[0]
    if node.level != 0 or len(node.names) != 1 or node.names[0].asname is not None:
        return None
    key = (node.module, node.names[0].name)
    if key not in IMPORT_MAP:
        return None
    indent = _indent(source_line)
    # the whole line is the statement, as ast spells it: no comment or other text is carried
    if source_line != indent + ast.unparse(node):
        return None
    module, name = IMPORT_MAP[key]
    image = ast.ImportFrom(module=module, names=[ast.alias(name=name)], level=0)
    return indent + ast.unparse(image)


def d_pool(source_line: str):
    """The image of ``source_line`` under D-pool, or None if the rule does not apply to it."""
    old, new = POOL_HINT
    pattern = rf"\b{re.escape(old)}\b"
    if len(re.findall(pattern, source_line)) != 1:
        return None
    stripped = source_line.strip()
    if not stripped.endswith(","):
        return None
    try:
        tree = ast.parse(f"def _f({stripped[:-1]}): pass")
    except SyntaxError:
        return None
    args = tree.body[0].args
    params = args.posonlyargs + args.args + args.kwonlyargs
    if args.vararg or args.kwarg or len(params) != 1:
        return None
    if args.defaults or any(d is not None for d in args.kw_defaults):
        return None
    annotation = params[0].annotation
    if not (isinstance(annotation, ast.Name) and annotation.id == old):
        return None
    return re.sub(pattern, new, source_line)


RULES = (("D-imp", d_imp), ("D-pool", d_pool))


# --- the comparisons ------------------------------------------------------------------------------


def _lines(text: str):
    """The lines of ``text``, without their newlines; a missing final newline is marked."""
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    else:
        lines[-1] += "  <no newline at end of file>"
    return lines


def compare_module(package_path: str, source_path: str):
    """Compare a module line by line; returns (counts, classified, unclassified)."""
    src = _lines(source_text(source_path))
    pkg = _lines((REPO_ROOT / package_path).read_text())

    counts = {"identical": 0}
    counts.update({name: 0 for name, _ in RULES})
    classified = []
    unclassified = []

    matcher = difflib.SequenceMatcher(None, src, pkg, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            counts["identical"] += i2 - i1
            continue

        if tag == "replace" and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                s, p = src[i1 + k], pkg[j1 + k]
                matches = [name for name, rule in RULES if rule(s) == p]
                where = f"source :{i1 + k + 1} / package :{j1 + k + 1}"
                if len(matches) == 1:
                    counts[matches[0]] += 1
                    classified.append(f"{matches[0]:7s} {where}\n    - {s}\n    + {p}")
                else:
                    why = "no rule maps it" if not matches else f"ambiguous: {matches}"
                    unclassified.append(
                        f"CHANGED ({why}) {where}\n    - {s}\n    + {p}"
                    )
            continue

        # an insertion, a deletion, or a replacement of a different length: never classified
        for i in range(i1, i2):
            unclassified.append(f"DELETED source :{i + 1}\n    - {src[i]}")
        for j in range(j1, j2):
            unclassified.append(f"ADDED   package :{j + 1}\n    + {pkg[j]}")

    return counts, classified, unclassified


def _definition_name(node):
    if isinstance(node, ast.FunctionDef):
        return node.name
    if (
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
    ):
        return node.targets[0].id
    return None


def compare_internalised(package_path: str, source_path: str):
    """Check D-int for an internalised module; returns (counts, classified, unclassified)."""
    src_text = source_text(source_path)
    pkg_text = (REPO_ROOT / package_path).read_text()
    src_tree = ast.parse(src_text)
    pkg_tree = ast.parse(pkg_text)

    counts = {"D-int": 0}
    classified = []
    unclassified = []

    src_defs = {}
    for node in src_tree.body:
        name = _definition_name(node)
        if name in TIMING_NAMES:
            src_defs[name] = node
    for name in TIMING_NAMES:
        if name not in src_defs:
            raise CannotRun(
                f"{source_path} at the import commit does not define {name}"
            )
    src_order = sorted(TIMING_NAMES, key=lambda n: src_defs[n].lineno)

    body = list(pkg_tree.body)
    docstring = ast.get_docstring(pkg_tree, clean=False)
    if docstring is None:
        unclassified.append(
            "NO DOCSTRING: the module must open with one naming its source"
        )
    else:
        body = body[1:]
        for needle in (source_path, IMPORT_COMMIT[:7]):
            if needle not in docstring:
                unclassified.append(f"DOCSTRING does not name {needle!r}")

    pkg_names = [_definition_name(node) for node in body]
    if pkg_names != src_order:
        unclassified.append(
            f"BODY: the module holds {pkg_names} after its docstring; "
            f"it must hold exactly {src_order}, in that order"
        )

    pkg_by_name = {
        _definition_name(node): node for node in body if _definition_name(node)
    }
    for name in src_order:
        node = pkg_by_name.get(name)
        if node is None:
            unclassified.append(f"MISSING definition {name}")
            continue
        s = ast.get_source_segment(src_text, src_defs[name])
        p = ast.get_source_segment(pkg_text, node)
        if s == p:
            counts["D-int"] += 1
            classified.append(
                f"D-int   {name}: package :{node.lineno}-{node.end_lineno} equals "
                f"source :{src_defs[name].lineno}-{src_defs[name].end_lineno}"
            )
        else:
            diff = "\n".join(
                "    " + d
                for d in difflib.unified_diff(
                    s.split("\n"), p.split("\n"), "source", "package", lineterm="", n=0
                )
            )
            unclassified.append(f"CHANGED definition {name}\n{diff}")

    # byte for byte over the span, comments included, which ast does not see
    first, last = src_defs[src_order[0]], src_defs[src_order[-1]]
    src_lines = src_text.split("\n")
    span = "\n".join(src_lines[first.lineno - 1 : last.end_lineno]) + "\n"
    pkg_lines = pkg_text.split("\n")
    start = pkg_by_name[src_order[0]].lineno if src_order[0] in pkg_by_name else None
    if start is None:
        unclassified.append("SPAN: the first definition is missing")
    else:
        if "\n".join(pkg_lines[start - 1 :]) != span:
            unclassified.append(
                f"SPAN: package :{start}-end is not source "
                f":{first.lineno}-{last.end_lineno} byte for byte"
            )
        doc_end = pkg_tree.body[0].end_lineno if docstring is not None else 0
        between = pkg_lines[doc_end : start - 1]
        if any(line.strip() for line in between):
            unclassified.append(
                f"TEXT between the docstring and package :{start} is not blank: {between}"
            )
        else:
            classified.append(
                f"D-int   span: package :{start}-end equals source "
                f":{first.lineno}-{last.end_lineno} byte for byte"
            )

    return counts, classified, unclassified


COMPARERS = {"module": compare_module, "internalised": compare_internalised}


def package_files():
    root = REPO_ROOT / "raypoolkit"
    return sorted(
        p.relative_to(REPO_ROOT).as_posix()
        for p in root.rglob("*.py")
        if "__pycache__" not in p.parts
    )


def main() -> int:
    print(
        f"Equivalence check: raypoolkit against SecondaryGWKit ({SGK_PATH}) "
        f"at {IMPORT_COMMIT}"
    )

    blob = git("rev-parse", f"{IMPORT_COMMIT}:{POOL_SOURCE_PATH}").strip()
    if blob != POOL_SOURCE_BLOB:
        raise CannotRun(
            f"{POOL_SOURCE_PATH} at the import commit is blob {blob}, "
            f"expected {POOL_SOURCE_BLOB}"
        )
    print(f"source blob of {POOL_SOURCE_PATH}: {blob} (as expected)")

    failed = False

    for package_path, (kind, source_path) in FILES.items():
        print()
        print(f"{package_path}  <-  {source_path}  [{kind}]")
        if not (REPO_ROOT / package_path).is_file():
            print("  MISSING: the package file does not exist")
            failed = True
            continue
        counts, classified, unclassified = COMPARERS[kind](package_path, source_path)
        for name, n in counts.items():
            print(f"  {name}: {n}")
        print(f"  unclassified: {len(unclassified)}")
        for line in classified:
            print("    " + line.replace("\n", "\n    "))
        for line in unclassified:
            print("  !! " + line.replace("\n", "\n  "))
        if unclassified:
            failed = True

    print()
    print("Files with no source (declared):")
    for path, why in NO_SOURCE.items():
        present = (REPO_ROOT / path).is_file()
        print(f"  {path}: {'present' if present else 'MISSING'} ({why})")
        if not present:
            failed = True

    undeclared = [p for p in package_files() if p not in FILES and p not in NO_SOURCE]
    print()
    print(f"Undeclared files under raypoolkit/: {len(undeclared)}")
    for path in undeclared:
        print(f"  !! NOT DECLARED: {path}")
    if undeclared:
        failed = True

    print()
    print("RESULT: " + ("FAIL" if failed else "OK"))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CannotRun as e:
        print(f"CANNOT RUN: {e}")
        sys.exit(2)
