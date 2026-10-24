# Provenance

`RayWorkPool` was imported from **SecondaryGWKit** (SGK):

- **Repository:** <https://github.com/ds283/SecondaryGWKit>, checked out at
  `/Users/ds283/Documents/Code/SecondaryGWKit`.
- **Import commit:** `b510bc9` (`b510bc90b66985532d28996ab4e5b13b0ff71709`), "Freeze the datastore
  layer while it moves to DatastoreKit".
- **The source module:** `RayTools/RayWorkPool.py` at the import commit is blob `b4666fa`
  (`b4666fa89abb26829fd585b881947d7ef5172cea`), 575 lines. It was last changed by `0ee16a8`
  ("Split RayWorkPool store_handler into store and persist handlers", 2026-09-04), and is unchanged
  from there to the import commit.

This is a fresh import (decision U2): SGK's history is not carried here. How the pool came to be is
SGK's history, reachable through the import commit. The import was made by
`prompts/extraction/01-import-the-pool.md`.

## The file map

| SGK at `b510bc9` | Here |
|---|---|
| `RayTools/RayWorkPool.py` | `raypoolkit/RayWorkPool.py` |
| `utilities.py`'s `SECONDS_PER_MINUTE`, `SECONDS_PER_HOUR`, `SECONDS_PER_DAY` (lines 20–22) and `format_time` (lines 25–61) | `raypoolkit/_timing.py` (those, nothing else) |
| `RayTools/__init__.py` (empty) | no counterpart |

**New here, with no source:**

- `raypoolkit/__init__.py`: re-exports `RayWorkPool` and `DatastorePool` from the package root
  (decision U4). The package attribute `raypoolkit.RayWorkPool` is therefore the class, and
  shadows the submodule of the same name; the module stays reachable through `sys.modules`,
  `importlib.import_module`, `from raypoolkit.RayWorkPool import …` and string targets to
  `unittest.mock.patch`.
- `raypoolkit/contract.py`: `DatastorePool`, a `typing.Protocol` stating the one method the
  default persist handler calls on the pool, `object_store` (decision U3).
- `raypoolkit/tests/__init__.py` (empty) and `raypoolkit/tests/test_package_imports.py`, the
  import guard.

## The differences allowed

At `v0.1.0`, `raypoolkit/RayWorkPool.py` equals its source at `b510bc9` except for these classes
of difference (prompt 01 §2.4), and `raypoolkit/_timing.py` holds its four definitions as D-int
states. Nothing else differs.

- **D-imp, the import rewrite.** Two whole `from … import …` statements, and no others:
  `from Datastore.SQL.ShardedPool import ShardedPool` → `from raypoolkit.contract import
  DatastorePool`, and `from utilities import format_time` → `from raypoolkit._timing import
  format_time`.
- **D-pool, the type hint.** The constructor's parameter `pool: ShardedPool,` →
  `pool: DatastorePool,`. `ShardedPool` appears nowhere else in the source.
- **D-int, the internalised definitions.** `_timing.py` holds SGK's `utilities.py` lines 20–22 and
  25–61 byte for byte, under a module docstring naming their source. `format_time` uses no import,
  so the module has none.
- **D-fmt, formatting.** `black` 25.1.0, with no configuration. It changes nothing: the source is
  black-clean and the rewritten lines are no longer than their sources. So the check has no D-fmt
  rule, and the package module's line numbers are SGK's.

At `v0.1.0`, the module keeps SGK's comments, docstrings and messages as they are.

## Re-running the check

The check was retired at `v0.1.0` (prompt 04 §2.8). It describes that tag, and on any later tree it
fails by design, since the package has changed in its own right ("Since `v0.1.0`", below).
It is run from a `git worktree` of the tag, kept in a scratch directory outside the repository,
with the repository's venv. From the repository root, with `<scratch>` standing for that
directory:

```bash
REPO=$(pwd)
git worktree add --detach <scratch>/raypoolkit-v0.1.0 v0.1.0
cd <scratch>/raypoolkit-v0.1.0
"$REPO"/venv/bin/python docs/extraction/compare_with_source.py
cd "$REPO"
git worktree remove <scratch>/raypoolkit-v0.1.0
```

The script finds the package from its own path, so it checks the worktree's tree, `v0.1.0`'s. It
checks that `RayTools/RayWorkPool.py` at the import commit is still blob `b4666fa`, reads each
source with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show b510bc9:<path>`, and accounts
for every line on which the package differs: each class above is a rule applied to the source line,
and a line no rule maps, or any line added or deleted, fails the check. Every `.py` file under
`raypoolkit/` must be a file with a source or a declared new file. It exits 0 only when all of that
holds, as it does at `v0.1.0`. The rules are described in the script's docstring.

## Since `v0.1.0`

From `v0.2.0`, `raypoolkit/RayWorkPool.py` is this repository's own module, and changes to it are
made by this repository's campaigns. `v0.2.0`'s changes are prompt 04's (`0b6ffd2`), listed in its
log, [`prompts/extraction/logs/04-fix-the-inherited-faults.md`](prompts/extraction/logs/04-fix-the-inherited-faults.md),
and in §4 of the campaign's status board,
[`prompts/extraction/IMPLEMENTATION_STATE.md`](prompts/extraction/IMPLEMENTATION_STATE.md); the
README's "Changes in `v0.2.0`" ([`README.md`](README.md)) says what they mean for a caller. The
freeze of the clients' copies (below) has ended: every client has adopted a release and deleted its
copy.

## Since `v0.2.0`

`raypoolkit/rehearsal_lock.py`, the shared rehearsal lock, was written new for this package by
`prompts/rehearsal-lock/01-the-lock-module.md` (`6733447`). It was not imported, and no client's
history is carried here. Its models, as its docstring names them:

- SGK's `tools/rehearsal_lock.py` at SGK `216e44d` (blob `ea14336`): the owner file's writing and
  parsing, `pid_alive`, `_short_hostname`, the walk that keeps a process, its ancestors and its own
  children out of the listing, `_ps_output` as the one reading of `ps`, and the commands'
  structure, exit codes and messages;
- ChamPBH's `.documents/dk-and-rpk-migration/rehearsal/ray_cluster.sh` at ChamPBH `807f175` (blob
  `eaae1e7`): its `temp_dir_regex` and `list_cluster_pids`, the rule that finds a Ray instance's
  processes by its temp dir and its Ray client server's address. StochasticInstantons'
  `ray_cluster.sh` (blob `6c8eada` at `8b4f615`) is the one ChamPBH's was adapted from.

SGK's tests of its module (`tools/tests/test_rehearsal_lock.py`, blob `cdeecd6`, 42 tests) were
ported to `raypoolkit/tests/test_rehearsal_lock.py`: 41 of the 42, onto 39 tests, with neutral
project names (prompt 01's log, §1.2). The specification was the brief at StochasticInstantons
`8b4f615` (`.prompts/dk-and-rpk-migration/rehearsal-lock-brief.md`, blob `d86ad43`), §2, which
[`docs/rehearsal-lock.md`](docs/rehearsal-lock.md) now replaces as the statement of the lock.

Where the module departs from its models, each decided in
[`prompts/rehearsal-lock/README.md`](prompts/rehearsal-lock/README.md) §6, with the detail in
[prompt 01's log](prompts/rehearsal-lock/logs/01-the-lock-module.md):

- **The location** (D2): `~/.raypoolkit/rehearsal-lock`, where the models used
  `~/ScienceData/.rehearsal-lock`.
- **The old location** (U4): in `0.3.x`, `acquire` refuses while `~/ScienceData/.rehearsal-lock`
  exists.
- **One process rule, by Ray temp dir** (U2), for every caller, in place of SGK's rule by venv,
  which found Ray processes by this checkout's `venv/…/site-packages/ray/` and could not find the
  venv once packaged.

## The freeze (decision U5)

From the commit of prompt 01 until each client has adopted the package (gates G2–G4 of
`prompts/extraction/README.md` §7), no client edits its `RayTools/`. A fix wanted in a client's
pool is made here and reaches the client when it adopts a release. The clients are SGK
(`RayTools/RayWorkPool.py`, the source of this import), ChamPBH and StochasticInstantons.

The freeze is recorded here. Prompt 01 does not edit any client to announce it.

The freeze ended when the last client adopted: G2 held on 2026-10-12, G3 on 2026-10-12 and G4 on
2026-10-20 (§2 of [`prompts/extraction/IMPLEMENTATION_STATE.md`](prompts/extraction/IMPLEMENTATION_STATE.md)),
and each client has deleted its `RayTools/`.
