#!/usr/bin/env python3
"""
Measure a client project's use of ``RayTools`` and ``RayWorkPool``, for the adoption checklists
(extraction prompt 06 §2.1).

    ./venv/bin/python docs/adoption/measure_client_pools.py sgk  [--commit SHA] [--json]
    ./venv/bin/python docs/adoption/measure_client_pools.py cpbh [--commit SHA] [--json]
    ./venv/bin/python docs/adoption/measure_client_pools.py si   [--commit SHA] [--json]

**How the client is read.** Only through ``git -C <repository> ls-tree -r <commit>`` and
``git -C <repository> show <commit>:<path>``, never from the client's working tree, so an
uncommitted change in the client does not reach the output. The default commit is the one the
checklists were measured at (``CLIENTS``). Nothing of the client is imported or run. A file whose
extension marks it as a datastore (``STORE_SUFFIXES``) is never read, and a file whose first 8,000
bytes hold a NUL is taken as binary and not searched.

**What it reports.**

1. Every import of a ``RayTools`` module (``import RayTools…`` or ``from RayTools… import …``) in a
   tracked ``.py`` file outside ``RayTools/``, parsed with ``ast``, at module level or nested, with
   file, line, the enclosing function or class (``(module)`` at module level), and the names
   imported; a name that begins with ``_`` is flagged as private.
2. String literals that name ``RayTools``, and ``importlib.import_module`` / ``import_module`` /
   ``__import__`` calls whose first argument is a string naming it.
3. Every ``RayWorkPool(...)`` call (an ``ast.Call`` whose function is the name or an attribute
   ``RayWorkPool``), at the line of the call's name: the positional count; whether it has
   ``*args`` or ``**kwargs``; each of the seven handler keywords (``HANDLERS``) as absent, ``None``
   or set; the source text of each size keyword (``SIZES``) and of each notification keyword
   (``NOTIFY``); ``store_results``; and ``title``.
4. **For each call, ``v0.2.0``'s verdict, from the package's own constructor**, not from a
   restatement of its rules. The call's arguments are rebuilt: ``pool``, ``task_list`` and
   ``task_builder`` (where the call gives them) become a stand-in pool, an empty list and a trivial
   builder; a handler keyword that is ``None`` stays ``None``, one that is set becomes a distinct
   callable, and one that is absent is left out; a size keyword that is a literal is evaluated with
   ``ast.literal_eval``, and one that is not is replaced by 1 and **flagged**; ``store_results`` is
   evaluated when it is a literal and left out (and flagged) when it is not. **The notification
   keywords and ``title`` are never passed**: the notifications change no check, and a titled pool
   prints its banner from the constructor, which would put one banner per site into this output.
   ``raypoolkit.RayWorkPool`` is then constructed with what is left; construction calls no Ray. The
   verdict is "constructs", or the exception's type and message. **It is only as good as the
   classes**: a keyword whose value is a name or expression is "set" whatever that name holds at
   run time, and a non-literal size is taken to be at least 1.
5. Tracked files other than ``.py`` that name ``RayTools`` or ``RayWorkPool``: lines counted by top
   directory (a file at the root counts under its own name), and each line outside the campaign
   record directories (``RECORD_DIRS``) listed.
6. The client's test modules (``test_*.py``, ``*_test.py``, or a ``.py`` file under a ``tests/``
   directory), outside ``RayTools/``, that name ``RayWorkPool`` or ``RayTools``, with the lines.

It also names the files under ``RayTools/`` at the commit, with their blobs, and any ``.py`` file
that does not parse.

**Output.** Markdown by default (the checklists' appendices), JSON with ``--json``. Everything is
sorted, so two runs at one commit give the same bytes. The script exits 0 on success and 2 when it
cannot read the client's repository or the commit. It writes nothing.

**The repository override.** ``--repository PATH`` reads another repository in place of the
client's, and requires ``--commit``. It exists only to check the script against a fixture
repository (prompt 06 §3.3); without it, the client's own repository is read, at the default
commit unless ``--commit`` is given.

This script names the client projects, as ``docs/extraction/compare_with_source.py`` names its
source. Nothing under ``raypoolkit/`` does. It imports only the standard library and
``raypoolkit``. It is not a test, the suite does not collect it, and it does not run in CI.
"""

import argparse
import ast
import importlib.metadata
import json
import subprocess
import sys
from collections import Counter
from pathlib import PurePosixPath

import ray

import raypoolkit

CODE_ROOT = "/Users/ds283/Documents/Code"

# label -> (repository, name, short name, commit the checklists were measured at)
CLIENTS = {
    "sgk": (
        "SecondaryGWKit",
        "SecondaryGWKit",
        "SGK",
        "b510bc90b66985532d28996ab4e5b13b0ff71709",
    ),
    "cpbh": (
        "ChamPBH",
        "ChamPBH",
        "CPBH",
        "52142d75aebe00855804e2daff4f63aee50ffc3e",
    ),
    "si": (
        "StochasticInstantons",
        "StochasticInstantons",
        "SI",
        "7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7",
    ),
}

POOL_DIR = "RayTools"
RECORD_DIRS = ("prompts", ".prompts")
STORE_SUFFIXES = (".db", ".sqlite", ".sqlite3", ".db-wal", ".db-shm", ".db-journal")
TEXT_NEEDLES = ("RayTools", "RayWorkPool")

PARAMETERS = (
    "pool",
    "task_list",
    "task_builder",
    "compute_handler",
    "store_handler",
    "persist_handler",
    "available_handler",
    "validation_handler",
    "post_handler",
    "label_builder",
    "create_batch_size",
    "process_batch_size",
    "max_task_queue",
    "notify_batch_size",
    "notify_time_interval",
    "notify_min_time_interval",
    "title",
    "store_results",
)
STANDINS = ("pool", "task_list", "task_builder")
HANDLERS = (
    "compute_handler",
    "store_handler",
    "persist_handler",
    "available_handler",
    "validation_handler",
    "post_handler",
    "label_builder",
)
SIZES = ("create_batch_size", "process_batch_size", "max_task_queue")
NOTIFY = ("notify_batch_size", "notify_time_interval", "notify_min_time_interval")

ABSENT = "absent"


class CannotRead(Exception):
    pass


# --- reading the client through git ---------------------------------------------------------------


def git(repository, *args):
    result = subprocess.run(
        ["git", "-C", repository, *args],
        capture_output=True,
    )
    if result.returncode != 0:
        raise CannotRead(
            f"git -C {repository} {' '.join(args)} failed: "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout


def resolve_commit(repository, commit):
    """The full SHA of the commit, or CannotRead."""
    out = git(repository, "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}")
    return out.decode().strip()


def tracked_blobs(repository, commit):
    """(path, blob) for every regular file tracked at the commit, sorted by path."""
    out = git(repository, "ls-tree", "-r", "-z", "--full-tree", commit)
    blobs = []
    for entry in out.split(b"\0"):
        if not entry:
            continue
        meta, path = entry.split(b"\t", 1)
        mode, kind, blob = meta.split(b" ")
        if kind != b"blob" or mode == b"120000":
            continue
        blobs.append((path.decode("utf-8", "surrogateescape"), blob.decode()))
    return sorted(blobs)


def show(repository, commit, path):
    return git(repository, "show", f"{commit}:{path}")


# --- the parts of a file ---------------------------------------------------------------------------


def top_group(path):
    parts = PurePosixPath(path).parts
    return parts[0] + "/" if len(parts) > 1 else parts[0]


def is_test_module(path):
    p = PurePosixPath(path)
    return (
        p.name.startswith("test_")
        or p.name.endswith("_test.py")
        or "tests" in p.parts[:-1]
    )


def text_lines(text):
    # split on newlines only, as git and editors count lines
    return [line.rstrip("\r") for line in text.split("\n")]


def names_a_pool_module(module):
    return module == POOL_DIR or module.startswith(POOL_DIR + ".")


class Walker(ast.NodeVisitor):
    """Collects imports, string literals, dynamic imports and pool calls, with their scopes."""

    def __init__(self, path, text):
        self.path = path
        self.text = text
        self.scope = []
        self.imports = []
        self.literals = []
        self.dynamic = []
        self.calls = []

    def where(self):
        return ".".join(self.scope) if self.scope else "(module)"

    def _scoped(self, node):
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    visit_FunctionDef = _scoped
    visit_AsyncFunctionDef = _scoped
    visit_ClassDef = _scoped

    def segment(self, node):
        text = ast.get_source_segment(self.text, node)
        return " ".join(text.split()) if text is not None else ast.unparse(node)

    def visit_Import(self, node):
        for alias in node.names:
            if names_a_pool_module(alias.name):
                self.imports.append(
                    {
                        "path": self.path,
                        "line": node.lineno,
                        "scope": self.where(),
                        "statement": ast.unparse(node),
                        "module": alias.name,
                        "names": [],
                        "private": [],
                    }
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        if node.level == 0 and names_a_pool_module(module):
            names = [alias.name for alias in node.names]
            self.imports.append(
                {
                    "path": self.path,
                    "line": node.lineno,
                    "scope": self.where(),
                    "statement": ast.unparse(node),
                    "module": module,
                    "names": names,
                    "private": [n for n in names if n.startswith("_")],
                }
            )
        self.generic_visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, str) and POOL_DIR in node.value:
            self.literals.append(
                {
                    "path": self.path,
                    "line": node.lineno,
                    "scope": self.where(),
                    "text": node.value,
                }
            )

    def visit_Call(self, node):
        func = node.func
        name = (
            func.id
            if isinstance(func, ast.Name)
            else func.attr if isinstance(func, ast.Attribute) else None
        )
        if name in ("import_module", "__import__") and node.args:
            first = node.args[0]
            if (
                isinstance(first, ast.Constant)
                and isinstance(first.value, str)
                and POOL_DIR in first.value
            ):
                self.dynamic.append(
                    {
                        "path": self.path,
                        "line": node.lineno,
                        "scope": self.where(),
                        "call": self.segment(node),
                    }
                )
        if name == "RayWorkPool":
            self.calls.append(describe_call(self, node))
        self.generic_visit(node)


# --- a pool call, and its verdict -------------------------------------------------------------------


def classify(value):
    if isinstance(value, ast.Constant) and value.value is None:
        return "None"
    return "set"


def describe_call(walker, node):
    arguments = {}  # parameter -> the argument's ast node
    starred = False
    for index, arg in enumerate(node.args):
        if isinstance(arg, ast.Starred):
            starred = True
        elif index < len(PARAMETERS):
            arguments[PARAMETERS[index]] = arg
    double_star = False
    others = []
    for keyword in node.keywords:
        if keyword.arg is None:
            double_star = True
        elif keyword.arg in PARAMETERS:
            arguments[keyword.arg] = keyword.value
        else:
            others.append(keyword.arg)

    call = {
        "path": walker.path,
        "line": node.lineno,
        "scope": walker.where(),
        "positional": len(node.args),
        "starred_args": starred,
        "double_star_kwargs": double_star,
        "unknown_keywords": sorted(others),
        "standins": [p for p in STANDINS if p in arguments],
        "handlers": {},
        "handler_source": {},
        "sizes": {},
        "notify": {},
        "store_results": ABSENT,
        "title": ABSENT,
        "flags": [],
    }
    for handler in HANDLERS:
        if handler in arguments:
            call["handlers"][handler] = classify(arguments[handler])
            call["handler_source"][handler] = walker.segment(arguments[handler])
        else:
            call["handlers"][handler] = ABSENT
    for size in SIZES:
        if size in arguments:
            value = arguments[size]
            entry = {"source": walker.segment(value), "line": value.lineno}
            try:
                entry["value"] = ast.literal_eval(value)
                entry["literal"] = True
            except (ValueError, TypeError, SyntaxError):
                entry["value"] = 1
                entry["literal"] = False
                call["flags"].append(
                    f"{size}={entry['source']} is not a literal; replaced by 1"
                )
            call["sizes"][size] = entry
    for notify in NOTIFY:
        if notify in arguments:
            call["notify"][notify] = walker.segment(arguments[notify])
    if "store_results" in arguments:
        call["store_results"] = walker.segment(arguments["store_results"])
        try:
            call["store_results_value"] = ast.literal_eval(arguments["store_results"])
        except (ValueError, TypeError, SyntaxError):
            call["flags"].append(
                f"store_results={call['store_results']} is not a literal; left out"
            )
    if "title" in arguments:
        call["title"] = classify(arguments["title"])
    if starred:
        call["flags"].append("*args not evaluated")
    if double_star:
        call["flags"].append("**kwargs not evaluated")
    call["verdict"] = verdict(call, others)
    return call


class StandinPool:
    """The pool handed to the constructor: it satisfies the protocol, and is never called."""

    def object_store(self, objects):
        raise AssertionError("the verdict's pool is never used")


def _never_called(*args, **kwargs):
    raise AssertionError("the verdict's callables are never called")


def a_distinct_callable():
    def handler(*args, **kwargs):
        return _never_called(*args, **kwargs)

    return handler


def verdict(call, unknown_keywords):
    if call["starred_args"]:
        return "not evaluated: *args"
    kwargs = {}
    standin_values = {
        "pool": StandinPool(),
        "task_list": [],
        "task_builder": lambda item: None,
    }
    for name in call["standins"]:
        kwargs[name] = standin_values[name]
    for handler, cls in call["handlers"].items():
        if cls == "None":
            kwargs[handler] = None
        elif cls == "set":
            kwargs[handler] = a_distinct_callable()
    for size, entry in call["sizes"].items():
        kwargs[size] = entry["value"]
    if "store_results_value" in call:
        kwargs["store_results"] = call["store_results_value"]
    for name in unknown_keywords:
        kwargs[name] = object()
    try:
        raypoolkit.RayWorkPool(**kwargs)
    except Exception as error:  # the verdict is whatever the constructor raises
        return f"{type(error).__name__}: {error}"
    return "constructs"


# --- the measurement --------------------------------------------------------------------------------


def measure(repository, commit):
    blobs = tracked_blobs(repository, commit)
    report = {
        "repository": repository,
        "commit": commit,
        "package": "raypoolkit " + importlib.metadata.version("raypoolkit"),
        "files_tracked": len(blobs),
        "pool_files": [
            {"path": path, "blob": blob}
            for path, blob in blobs
            if PurePosixPath(path).parts[0] == POOL_DIR
        ],
        "py_files_parsed": 0,
        "unparsed": [],
        "imports": [],
        "literals": [],
        "dynamic_imports": [],
        "calls": [],
        "text_lines": [],
        "test_modules": [],
        "binary_skipped": 0,
        "stores_skipped": [],
    }
    for path, blob in blobs:
        if path.lower().endswith(STORE_SUFFIXES):
            report["stores_skipped"].append(path)
            continue
        data = show(repository, commit, path)
        if b"\0" in data[:8000]:
            report["binary_skipped"] += 1
            continue
        text = data.decode("utf-8", "replace")
        in_pool_dir = PurePosixPath(path).parts[0] == POOL_DIR
        if not path.endswith(".py"):
            for number, line in enumerate(text_lines(text), start=1):
                if any(needle in line for needle in TEXT_NEEDLES):
                    report["text_lines"].append(
                        {"path": path, "line": number, "text": line.strip()}
                    )
            continue
        if in_pool_dir:
            continue
        if is_test_module(path):
            hits = [
                {"line": number, "text": line.strip()}
                for number, line in enumerate(text_lines(text), start=1)
                if any(needle in line for needle in TEXT_NEEDLES)
            ]
            if hits:
                report["test_modules"].append({"path": path, "lines": hits})
        try:
            tree = ast.parse(text, filename=path)
        except (SyntaxError, ValueError) as error:
            report["unparsed"].append({"path": path, "error": str(error)})
            continue
        report["py_files_parsed"] += 1
        walker = Walker(path, text)
        walker.visit(tree)
        report["imports"].extend(walker.imports)
        report["literals"].extend(walker.literals)
        report["dynamic_imports"].extend(walker.dynamic)
        report["calls"].extend(walker.calls)

    position = lambda entry: (entry["path"], entry["line"])
    for key in ("imports", "literals", "dynamic_imports", "calls", "text_lines"):
        report[key].sort(key=position)
    report["test_modules"].sort(key=lambda entry: entry["path"])
    report["ray_initialized_after"] = ray.is_initialized()
    report["totals"] = totals(report)
    return report


def totals(report):
    calls = report["calls"]
    no_compute = [c for c in calls if c["handlers"]["compute_handler"] == "None"]
    given = [c for c in calls if c["handlers"]["compute_handler"] == "set"]
    default = [c for c in calls if c["handlers"]["compute_handler"] == ABSENT]
    groups = Counter(top_group(t["path"]) for t in report["text_lines"])
    group_files = Counter(
        top_group(path) for path in {t["path"] for t in report["text_lines"]}
    )
    spellings = Counter(tuple(c["handlers"][h] for h in HANDLERS) for c in calls)
    return {
        "imports": len(report["imports"]),
        "imports_module_level": sum(
            1 for i in report["imports"] if i["scope"] == "(module)"
        ),
        "imports_nested": sum(1 for i in report["imports"] if i["scope"] != "(module)"),
        "imports_naming_a_private_name": sum(
            1 for i in report["imports"] if i["private"]
        ),
        "literals": len(report["literals"]),
        "dynamic_imports": len(report["dynamic_imports"]),
        "calls": len(calls),
        "calls_no_compute_handler": len(no_compute),
        "calls_compute_handler_given": len(given),
        "calls_compute_handler_default": len(default),
        "calls_store_results_true": sum(
            1 for c in calls if c.get("store_results_value") is True
        ),
        "calls_title_keyword": sum(1 for c in calls if c["title"] != ABSENT),
        "calls_title_none": sum(1 for c in calls if c["title"] == "None"),
        "calls_titled": sum(1 for c in calls if c["title"] == "set"),
        "calls_double_star_kwargs": sum(1 for c in calls if c["double_star_kwargs"]),
        "calls_starred_args": sum(1 for c in calls if c["starred_args"]),
        "positional_counts": {
            str(k): v
            for k, v in sorted(Counter(c["positional"] for c in calls).items())
        },
        "verdicts": dict(sorted(Counter(c["verdict"] for c in calls).items())),
        "calls_flagged": sum(1 for c in calls if c["flags"]),
        "flags": sum(len(c["flags"]) for c in calls),
        "handler_spellings": [
            {"handlers": dict(zip(HANDLERS, key)), "calls": count}
            for key, count in sorted(spellings.items())
        ],
        "text_lines": len(report["text_lines"]),
        "text_lines_by_group": dict(sorted(groups.items())),
        "text_files_by_group": dict(sorted(group_files.items())),
        "test_modules": len(report["test_modules"]),
    }


# --- Markdown --------------------------------------------------------------------------------------


def code(text):
    """An inline code span holding text, whatever backticks it contains."""
    text = str(text).replace("|", "\\|")
    run, longest = 0, 0
    for ch in text:
        run = run + 1 if ch == "`" else 0
        longest = max(longest, run)
    fence = "`" * (longest + 1)
    pad = " " if text.startswith("`") or text.endswith("`") else ""
    return f"{fence}{pad}{text}{pad}{fence}"


def fenced(lines):
    body = "\n".join(lines)
    run, longest = 0, 0
    for ch in body:
        run = run + 1 if ch == "`" else 0
        longest = max(longest, run)
    fence = "`" * max(3, longest + 1)
    return [fence + "text", *lines, fence]


def cell(handler_class):
    return "—" if handler_class == ABSENT else handler_class


def markdown(report, title):
    t = report["totals"]
    out = [
        f"# `RayWorkPool` in {title} at `{report['commit'][:7]}`",
        "",
        f"- **Repository:** `{report['repository']}`, read through `git` only.",
        f"- **Commit:** `{report['commit']}`.",
        f"- **Verdicts by:** `{report['package']}`, its own constructor.",
        f"- **Files:** {report['files_tracked']} tracked; {report['py_files_parsed']} `.py` files "
        f"outside `{POOL_DIR}/` parsed; {len(report['unparsed'])} did not parse; "
        f"{report['binary_skipped']} binary, not searched; {len(report['stores_skipped'])} "
        "datastores, not read.",
        f"- **`ray.is_initialized()` after the verdicts:** {report['ray_initialized_after']}.",
        "",
        f"## `{POOL_DIR}/` at the commit",
        "",
        "| File | Blob |",
        "|---|---|",
    ]
    out += [f"| `{f['path']}` | `{f['blob']}` |" for f in report["pool_files"]]
    verdicts = "; ".join(f"{code(v)} {n}" for v, n in t["verdicts"].items()) or "—"
    positional = (
        ", ".join(f"{k} at {v}" for k, v in t["positional_counts"].items()) or "—"
    )
    out += [
        "",
        "## Totals",
        "",
        "| Measure | Count |",
        "|---|---|",
        f"| Imports of a `{POOL_DIR}` module | {t['imports']} (module level {t['imports_module_level']}, nested {t['imports_nested']}) |",
        f"| … naming a private name | {t['imports_naming_a_private_name']} |",
        f"| String literals naming `{POOL_DIR}` | {t['literals']} |",
        f"| `import_module` / `__import__` calls naming `{POOL_DIR}` | {t['dynamic_imports']} |",
        f"| `RayWorkPool(...)` calls | {t['calls']} |",
        f"| … no compute handler (`compute_handler=None`) | {t['calls_no_compute_handler']} |",
        f"| … compute handler given | {t['calls_compute_handler_given']} |",
        f"| … compute handler left at its default | {t['calls_compute_handler_default']} |",
        f"| … `store_results=True` | {t['calls_store_results_true']} |",
        f"| … with a `title` keyword | {t['calls_title_keyword']} (`title=None` {t['calls_title_none']}, set {t['calls_titled']}) |",
        f"| … positional arguments | {positional} |",
        f"| … with `*args` / `**kwargs` | {t['calls_starred_args']} / {t['calls_double_star_kwargs']} |",
        f"| Verdicts | {verdicts} |",
        f"| Calls with a flag / flags | {t['calls_flagged']} / {t['flags']} |",
        f"| Lines of non-`.py` files naming `RayTools` or `RayWorkPool` | {t['text_lines']} |",
        f"| Test modules naming `RayTools` or `RayWorkPool` | {t['test_modules']} |",
        "",
        "## The handler keywords, by spelling",
        "",
        "Each handler keyword as absent (—), `None` or set; a row per spelling, with its calls.",
        "",
        "| " + " | ".join(f"`{h}`" for h in HANDLERS) + " | Calls |",
        "|" + "---|" * (len(HANDLERS) + 1),
    ]
    for row in t["handler_spellings"]:
        out.append(
            "| "
            + " | ".join(cell(row["handlers"][h]) for h in HANDLERS)
            + f" | {row['calls']} |"
        )

    out += [
        "",
        f"## Imports of a `{POOL_DIR}` module ({t['imports']})",
        "",
    ]
    if report["imports"]:
        out += [
            "| File:line | Scope | Statement | Private names |",
            "|---|---|---|---|",
        ]
        for i in report["imports"]:
            private = ", ".join(f"`{n}`" for n in i["private"]) or "—"
            out.append(
                f"| `{i['path']}:{i['line']}` | {code(i['scope'])} | {code(i['statement'])} | {private} |"
            )
    else:
        out.append("None.")

    out += ["", f"## String literals naming `{POOL_DIR}` ({t['literals']})", ""]
    if report["literals"]:
        out += fenced(
            [
                f"{x['path']}:{x['line']} [{x['scope']}] {json.dumps(x['text'])[:160]}"
                for x in report["literals"]
            ]
        )
    else:
        out.append("None.")

    out += [
        "",
        f"## `import_module` / `__import__` calls naming `{POOL_DIR}` ({t['dynamic_imports']})",
        "",
    ]
    if report["dynamic_imports"]:
        out += ["| File:line | Scope | Call |", "|---|---|---|"]
        for x in report["dynamic_imports"]:
            out.append(
                f"| `{x['path']}:{x['line']}` | {code(x['scope'])} | {code(x['call'])} |"
            )
    else:
        out.append("None.")

    out += [
        "",
        f"## `RayWorkPool(...)` calls ({t['calls']})",
        "",
        "Each call at the line of its name. Handlers: absent (—), `None` or set. Sizes: the source "
        "text of each size keyword given. `results`: `store_results`. Verdict: `v0.2.0`'s "
        "constructor, given the classes.",
        "",
        "| File:line | Scope | Pos. | `**` | compute | store | persist | available | validation "
        "| post | label | Sizes | `results` | Title | Verdict |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for c in report["calls"]:
        sizes = (
            ", ".join(
                f"{code(k + '=' + e['source'])}{'' if e['literal'] else ' **flagged**'}"
                for k, e in c["sizes"].items()
            )
            or "—"
        )
        out.append(
            f"| `{c['path']}:{c['line']}` | {code(c['scope'])} | {c['positional']} | "
            f"{'yes' if c['double_star_kwargs'] else '—'} | "
            + " | ".join(cell(c["handlers"][h]) for h in HANDLERS)
            + f" | {sizes} | {cell(c['store_results'])} | {cell(c['title'])} | {code(c['verdict'])} |"
        )

    compute = [c for c in report["calls"] if c["handlers"]["compute_handler"] != "None"]
    out += [
        "",
        f"## Calls with a compute path: the handlers given ({len(compute)})",
        "",
        "The source text of each handler keyword given, at each call whose compute handler is "
        "given or left at its default.",
        "",
        "| File:line | " + " | ".join(f"`{h}`" for h in HANDLERS) + " |",
        "|" + "---|" * (len(HANDLERS) + 1),
    ]
    for c in compute:
        out.append(
            f"| `{c['path']}:{c['line']}` | "
            + " | ".join(
                code(c["handler_source"][h]) if h in c["handler_source"] else "—"
                for h in HANDLERS
            )
            + " |"
        )

    flagged = [c for c in report["calls"] if c["flags"]]
    out += ["", f"## Flags ({t['flags']}, on {t['calls_flagged']} calls)", ""]
    if flagged:
        out += ["| Call | Keyword line | Flag |", "|---|---|---|"]
        for c in flagged:
            for flag in c["flags"]:
                name = flag.split("=", 1)[0]
                line = c["sizes"][name]["line"] if name in c["sizes"] else c["line"]
                out.append(f"| `{c['path']}:{c['line']}` | `:{line}` | {code(flag)} |")
    else:
        out.append("None.")

    notified = [c for c in report["calls"] if c["notify"]]
    out += [
        "",
        f"## Notification keywords, by source text ({len(notified)} calls; never passed)",
        "",
    ]
    if notified:
        out += ["| File:line | Keywords |", "|---|---|"]
        for c in notified:
            out.append(
                f"| `{c['path']}:{c['line']}` | "
                + ", ".join(code(f"{k}={v}") for k, v in c["notify"].items())
                + " |"
            )
    else:
        out.append("None.")

    out += [
        "",
        f"## Non-`.py` files naming `RayTools` or `RayWorkPool` ({t['text_lines']} lines)",
        "",
        "| Top directory | Lines | Files |",
        "|---|---|---|",
    ]
    for group, count in t["text_lines_by_group"].items():
        out.append(f"| `{group}` | {count} | {t['text_files_by_group'][group]} |")
    listed = [
        x
        for x in report["text_lines"]
        if PurePosixPath(x["path"]).parts[0] not in RECORD_DIRS
    ]
    out += [
        "",
        f"Each line outside the campaign records ({', '.join(f'`{d}/`' for d in RECORD_DIRS)}), "
        f"{len(listed)}:",
        "",
    ]
    if listed:
        out += fenced([f"{x['path']}:{x['line']}: {x['text']}" for x in listed])
    else:
        out.append("None.")

    out += [
        "",
        f"## Test modules naming `RayTools` or `RayWorkPool` ({t['test_modules']})",
        "",
    ]
    if report["test_modules"]:
        lines = []
        for m in report["test_modules"]:
            for hit in m["lines"]:
                lines.append(f"{m['path']}:{hit['line']}: {hit['text']}")
        out += fenced(lines)
    else:
        out.append("None.")

    out += ["", f"## Files that do not parse ({len(report['unparsed'])})", ""]
    if report["unparsed"]:
        out += [f"- `{u['path']}`: {u['error']}" for u in report["unparsed"]]
    else:
        out.append("None.")
    return "\n".join(out) + "\n"


# --- the command line ------------------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Measure a client's use of RayTools and RayWorkPool, read through git."
    )
    parser.add_argument("client", choices=sorted(CLIENTS))
    parser.add_argument("--commit", help="the client commit (default: the checklist's)")
    parser.add_argument("--json", action="store_true", help="print JSON, not Markdown")
    parser.add_argument(
        "--repository",
        help="read this repository in place of the client's (the fixture check only; needs --commit)",
    )
    args = parser.parse_args(argv)

    folder, name, short, default_commit = CLIENTS[args.client]
    if args.repository is not None:
        if args.commit is None:
            parser.error("--repository needs --commit")
        repository = args.repository
        title = f"`{repository}` (in place of {name})"
    else:
        repository = f"{CODE_ROOT}/{folder}"
        title = f"{name} ({short})"
    commit = args.commit or default_commit

    try:
        resolved = resolve_commit(repository, commit)
        report = measure(repository, resolved)
    except CannotRead as error:
        print(f"cannot read the client: {error}", file=sys.stderr)
        return 2
    report["client"] = args.client

    if args.json:
        sys.stdout.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    else:
        sys.stdout.write(markdown(report, title))
    return 0


if __name__ == "__main__":
    sys.exit(main())
