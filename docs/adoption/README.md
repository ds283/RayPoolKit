# Adopting `raypoolkit`

*Written by extraction prompt 06 on 2026-10-10, against the package at **`v0.2.0`** (`eaef0ce`).
The three clients were read through `git` only, at the commits named below; nothing of a client
was imported, run or opened, and no store was opened.*

This directory holds one **adoption checklist** per client project, what the three share, and the
script that measures them. Each checklist says what its client must do to depend on `raypoolkit`
at `v0.2.0` in place of its own `RayTools/RayWorkPool.py`: what it deletes, which imports it
rewrites, which of its call sites change, what behaves differently, which of its tests depend on
the pool, how its adoption is accepted, and which of its documents go stale.

**A checklist is data, not instructions.** It describes the client at one commit. The client's
own adoption campaign, in its own repository and under its own `CLAUDE.md`, measures again before
acting, and its numbers govern. Where a choice is the client's, the checklist names the choice and
what each option touches, and does not make it. A recommendation is marked **Advice:**.

| Client | Checklist | Measured at | Gate |
|---|---|---|---|
| SecondaryGWKit (SGK) | [`secondarygwkit.md`](secondarygwkit.md) | `b510bc9` (branch `handover-remedial`) | G2 |
| ChamPBH (CPBH) | [`champbh.md`](champbh.md) | `52142d7` (branch `main`) | G3 |
| StochasticInstantons (SI) | [`stochasticinstantons.md`](stochasticinstantons.md) | `7bb3efd` (branch `main`) | G4 |

The gates are those of the campaign plan, [`prompts/extraction/README.md`](../../prompts/extraction/README.md)
§7, recorded on its board, [`prompts/extraction/IMPLEMENTATION_STATE.md`](../../prompts/extraction/IMPLEMENTATION_STATE.md)
§2, as they hold. The campaign does not wait for them.

---

## 1. The release and the pin

A client depends on a tagged release, pinned in its `requirements.txt`:

```text
raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
```

An editable install (`pip install -e`) is for developing this package, **never for a client's
production run**: a run must be reproducible from its pin (the package's
[`README.md`](../../README.md#installing), "Installing"). A client moves its pin in a commit of
its own.

`pyproject.toml` declares `requires-python = ">=3.12"` and `ray>=2.43`. The suite runs at two
tested ends: Python 3.12.15 / Ray 2.43.0 and Python 3.13.16 / Ray 2.55.1; on Python 3.13 the Ray
floor is in effect 2.45.0, the first Ray with wheels for 3.13 ([`README.md`](../../README.md#supported-versions),
"Supported versions"). Each client's versions, read as text (the Python from its `venv/pyvenv.cfg`,
never run; Ray from `requirements.txt` at the commit):

| Client | Python | Ray | Inside the declared range | Against the tested ends |
|---|---|---|---|---|
| SGK | 3.12.15 (`venv/pyvenv.cfg`) | `ray==2.43.0` (`requirements.txt:74`) | yes | equals the low end |
| CPBH | 3.13.16 (`venv/pyvenv.cfg`) | `ray==2.53.0` (`requirements.txt:78`) | yes | Python equals the high end; Ray lies between the ends, above the 3.13 floor, and is not itself tested |
| SI | `venv/pyvenv.cfg` records 3.13.13, the version when the venv was made; its interpreter is MacPorts' 3.13, which is 3.13.16 today | `ray==2.55.1` (`requirements.txt:57`) | yes, either way | Ray equals the high end; so does Python, at 3.13.16 |

The package pins nothing of a client's: **each client keeps its own Ray pin.**

---

## 2. The module map

| A client's `RayTools/` | `raypoolkit` |
|---|---|
| `RayTools.RayWorkPool` (the class `RayWorkPool`) | `from raypoolkit import RayWorkPool` |
| `RayTools/__init__.py` (empty in all three) | no counterpart |

- The module keeps its name (decision U4), and `raypoolkit/__init__.py` re-exports the class, so the
  package attribute `raypoolkit.RayWorkPool` **is the class** and shadows the submodule. The module
  stays reachable for a `from` import of a module-level name, `from raypoolkit.RayWorkPool import
  <name>`, and through `importlib.import_module("raypoolkit.RayWorkPool")` ([`PROVENANCE.md`](../../PROVENANCE.md),
  "New here"). **Every name in it other than `RayWorkPool` and `DatastorePool` is private**: those
  two are the package's public names (`raypoolkit/__init__.py:16-19`).
- The constructor's `pool` is typed as `raypoolkit.DatastorePool`, a `typing.Protocol` with one
  method, `object_store`, which a client's `ShardedPool` satisfies. It is a type hint, not checked
  at run time. `raypoolkit` does not depend on `datastorekit` (decision U3), so the two are adopted
  and versioned independently.
- The call stays spelled `RayWorkPool(...)` after `from raypoolkit import RayWorkPool`, which is
  what a test that finds pool constructions by `ast` needs (SGK's, item 6 of its checklist).

---

## 3. What changes for a caller

The package's [`README.md`](../../README.md) states both, and is not restated here:
- [**Changes in `v0.2.0`**](../../README.md#changes-in-v020): what a client meets coming from a
  copy that is `v0.1.0`'s pool (SGK's is; CPBH's and SI's differ from it as each checklist's item 5
  says).
- [**Which handlers a pool needs**](../../README.md#which-handlers-a-pool-needs): the constructor's
  checks, each refusal a `ValueError` at construction.

The issues behind them, with where each sat and how it was fixed, are in the campaign board's §4.

---

## 4. What does not change

**The printed lines.** The banner, progress and completion lines are unchanged in wording and
layout from SGK's copy (decision U9; [The printed lines are part of the interface](../../README.md#the-printed-lines-are-part-of-the-interface)).
Each client copy's seven `print()` calls are the package's, by `ast`; CPBH's two message builders
condition the "store" segment on its `store_handler`, which is its persist handler, where the
package conditions it on `persist_handler` (CPBH's checklist, item 5).

---

## 5. The order with DatastoreKit

DatastoreKit's checklists, at its [`v0.2.1`](https://github.com/ds283/DatastoreKit/tree/v0.2.1/docs/adoption),
list each copy's `from Datastore.SQL.ShardedPool import ShardedPool` as an import to rewrite (SGK
`RayTools/RayWorkPool.py:8`, CPBH and SI `:23`). The import serves only as the type hint of the
constructor's `pool`. **Decision U12, taken 2026-10-10:** a client that adopts DatastoreKit before
`raypoolkit` may rewrite that one import to `from datastorekit.SQL.ShardedPool import ShardedPool`,
and nothing else in `RayTools/`, an exception to the freeze of decision U5. So any order is
possible:

| Order | What `RayTools/` sees | SGK's `Datastore/tests/test_layer_is_generic.py` |
|---|---|---|
| `raypoolkit` first | deleted; DatastoreKit's later rewrite list has one import fewer | edited by the `raypoolkit` adoption to drop its `RayTools` entries, then retired by DatastoreKit's |
| DatastoreKit first | the one import rewritten (U12), then deleted by the `raypoolkit` adoption | retired by DatastoreKit's adoption; nothing for `raypoolkit`'s |
| Both in one campaign | deleted; the import never rewritten | retired |

Adopting both in one campaign is possible, but not required. DatastoreKit's checklists:
[SGK](https://github.com/ds283/DatastoreKit/blob/v0.2.1/docs/adoption/secondarygwkit.md),
[CPBH](https://github.com/ds283/DatastoreKit/blob/v0.2.1/docs/adoption/champbh.md),
[SI](https://github.com/ds283/DatastoreKit/blob/v0.2.1/docs/adoption/stochasticinstantons.md).

---

## 6. How a checklist is used

- Each checklist was measured at the commit it names. **The client re-measures** at its own
  commit before acting (§7), and its numbers govern.
- A client's adoption is **one campaign in its own repository**, planned from its checklist. No
  prompt of this repository edits a client.
- **The pin moves in a commit of its own.**
- **The freeze ends for a client when its adoption lands.** Until then the client does not edit its
  `RayTools/` (decision U5), except for the one import of §5 (U12). SGK's `CLAUDE.md` and SI's
  carry statements about `RayTools/` that this changes (item 9 of each).
- **A defect a client finds in the package** is reported here and fixed here, in a release; the
  client does not patch its installed copy.

---

## 7. Re-measuring

[`measure_client_pools.py`](measure_client_pools.py), from this repository's root, with its venv:

```bash
./venv/bin/python docs/adoption/measure_client_pools.py sgk  [--commit SHA] [--json]
./venv/bin/python docs/adoption/measure_client_pools.py cpbh [--commit SHA] [--json]
./venv/bin/python docs/adoption/measure_client_pools.py si   [--commit SHA] [--json]
```

It reads the client at `/Users/ds283/Documents/Code/<repository>` through `git ls-tree` and
`git show` only, at the checklist's commit unless `--commit` names another, and reports: every
import of a `RayTools` module, at module level or nested, with private names flagged; string
literals and `import_module` / `__import__` calls naming `RayTools`; every `RayWorkPool(...)` call,
with its handler keywords as absent, `None` or set, its sizes, `store_results` and `title`; for
each call, **`v0.2.0`'s verdict from the package's own constructor** (a non-literal size replaced
by 1 and flagged); the non-`.py` files naming `RayTools` or `RayWorkPool`; and the test modules
naming either. The verdict is only as good as the classes: its docstring says how each argument is
rebuilt. Markdown by default, JSON with `--json`, sorted so that two runs at one commit give the
same bytes; it exits 2 when it cannot read the client or the commit. It is not a test and does not
run in CI.

Its figures at the checklists' commits:

| | SGK `b510bc9` | CPBH `52142d7` | SI `7bb3efd` |
|---|---|---|---|
| Imports of `RayTools` (all at module level) | 7 | 3 | 3, one naming a private name |
| String literals naming `RayTools` | 8 | 0 | 0 |
| `import_module` / `__import__` naming it | 0 | 0 | 0 |
| `RayWorkPool(...)` calls | 54 | 17 | 16 |
| … no compute handler / given / left at its default | 44 / 6 / 4 | 14 / 3 / 0 | 12 / 4 / 0 |
| … `store_results=True` | 39 | 13 | 11 |
| … `title` given (`None` / set) | 54 (28 / 26) | 17 (12 / 5) | 16 (10 / 6) |
| Verdicts | 54 construct | 17 construct | 16 construct |
| Sizes flagged (not literals) | 0 | 0 | 5, on 4 calls |
| Non-`.py` lines naming `RayTools` or `RayWorkPool` | 196 | 43 | 89 |
| Test modules naming either | 7 | 0 | 0 |

Each checklist's appendix is the script's Markdown output for that client, as printed.

---

## The checklist items

Each checklist has the same nine items, in this order:

1. The client and its versions
2. What it deletes
3. Which imports it rewrites
4. Its call sites
5. What changes in behaviour
6. Its tests
7. The order with DatastoreKit
8. Its acceptance
9. What goes stale in it

and then the appendix, the script's output.
