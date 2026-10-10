# Log — extraction prompt 06: the adoption checklists

**Subject:** Write the adoption checklists and their measuring script · **Commit:** `67f3f7e` ·
**Date:** 2026-10-10 · **Agent:** Claude Opus 5.5

**Result: landed.** `docs/adoption/` holds the README, the three checklists
(`secondarygwkit.md`, `champbh.md`, `stochasticinstantons.md`), each with the same nine items in
the same order and the script's output as its appendix, and the script,
`measure_client_pools.py`. The script reads each client through `git ls-tree` and `git show` only,
and its verdicts come from `raypoolkit.RayWorkPool`'s own constructor at `0.2.0`. **Its figures
equal §0's**: imports 7, 3, 3; sites 54, 17, 16 with §0.2's splits; **all 87 sites construct**;
SI's three non-literal sizes flagged (five keywords on four calls, and no other flag); text lines
196, 43, 89; test modules 7, 0, 0. One reading of §0 differs: "Titled 54 / 17 / 16" counts the
`title` keyword, and 28 / 12 / 10 of those pass `title=None` (deviation 15). Two runs per client
are byte-identical, `--json` parses, and a missing commit exits 2. The fixture reports each case
with the prompt's verdicts, and (a)–(d) each fail as §3.7 says. No file under `raypoolkit/`
changed; the suite is **121 → 121**; `black --check raypoolkit docs` gives **16** files
unchanged. The clients' `HEAD`, status and stash are equal before and after. **No issue is opened**,
so the index stays at **0**. Nothing was pushed or tagged.

**Gate, re-checked at start.** `HEAD` was `deffdc2` (the orchestration note; the prompt was written
at `a1d64ea`), the tree clean, the only worktree this checkout, the tags `v0.1.0` and `v0.2.0`,
`origin/main` at `b2b6ab4`. `git diff eaef0ce -- raypoolkit` was empty. `venv/`: Python 3.12.15,
`ray` 2.43.0, `black` 25.1.0, `raypoolkit` `0.2.0` (editable). `Ran 121 tests in 1.397s` `OK`.
`black --check raypoolkit docs`: 15 files unchanged. No Ray process (`pgrep -lf
'gcs_server|raylet|ray::'` empty). The clients as the brief measured them (§3.4). Every scratch
file, driver, diff, output and the fixture are under the agent's scratch directory
(`…/scratchpad/agent06/`), written `$S` below.

## 1. What shipped

| File | What |
|---|---|
| `docs/adoption/measure_client_pools.py` | the script of §2.1: `sgk`, `cpbh` or `si`, `[--commit SHA] [--json]`, and `--repository PATH` (with `--commit`) for the fixture only; the six reports and the verdict; Markdown or JSON, sorted; exit 0, or 2 when it cannot read the client or the commit. Standard library, `ray` (for `ray.is_initialized()`, reported) and `raypoolkit` only. Black-clean |
| `docs/adoption/README.md` | what the three share (§2.2): the head, the table of checklists with commits and gates, §1–§7, and the nine items by number and name |
| `docs/adoption/secondarygwkit.md` | SGK at `b510bc9`: the nine items; the appendix, the script's output as printed |
| `docs/adoption/champbh.md` | CPBH at `52142d7`, likewise |
| `docs/adoption/stochasticinstantons.md` | SI at `7bb3efd`, likewise |
| this log, the board, `prompts/INDEX.md` | the records. `docs/OPEN_ISSUES.md` is unchanged: no issue is opened |

Each appendix is byte-equal to the script's output at the checklist's commit: the checklist from
its line `# \`RayWorkPool\` in …` to its end `cmp`s equal to `$S/final/<client>-1.md` (SGK from
line 293, CPBH 206, SI 232).

## 2. Deviations from the prompt

The orchestrator's brief added fourteen clarifications and additions (1–14 below). Each is an
**IMPLEMENTATION CHOICE at the orchestrator's direction**, except 1 and 6, which are
**STRUCTURALLY REQUIRED**.

1. **The constructor is cited as `raypoolkit/RayWorkPool.py:88-206`, its checks as `:109-142`**,
   not the prompt's `:88-215` (`class RayWorkPool:` is `:87`, `__init__` `:88`, the banner's
   `print` `:206`, `_build_queued_status_message` `:208`). **STRUCTURALLY REQUIRED**: the prompt's
   span is not true of `v0.2.0`.
2. **The verdict is constructed with no `title`**, so the constructor prints no banner into the
   output; the docstring says so (item 4 of its list). The script never captures stdout.
3. **A size keyword is one of the three the constructor checks** (`SIZES`); the three `notify_*`
   keywords are reported by source text only, in their own section, never passed and never
   flagged. So the only flags are SI's: three expressions, at five keywords, on four calls.
4. **A call's line is its `ast.Call`'s `lineno`**, the line of its name. The flags table gives
   each flagged keyword's own line as well (`:396`, `:505`, `:729`, `:730`, `:1107`), and the
   checklists cite both.
5. **An absent `compute_handler` is a compute pool** with the default handler: SGK has 10 compute
   pools, 6 given and 4 at the default (`main.py:1042`, `:1057`, `:1940`, `:4146`), each
   constructing.
6. **SGK's pinned block is five lines, and the checklist quotes it as it is.** `A3_OUTPUT`
   (`RunRegistry/tests/test_pipeline_adoption.py:38-44`) holds the banner (`:39`) and two
   two-line progress notifications (`:40-43`), stamped `+0100`; the comment (`:32-37`) speaks of
   six lines, the completion pair among them, which the block does not hold. The checklist says so,
   and names the comment's `:166`, `:548`, `:566` as SGK's copy's lines (the banner, a progress
   `print(msg)`, the completion `print(`). **STRUCTURALLY REQUIRED**: "six lines" is not true of
   the test.
7. **CPBH's 23 uncommitted changes are described from `git status --porcelain`'s paths**: all
   untracked, two run scripts, seventeen `.db` files, two logs, `pilot-out/` and
   `prompts/jordan-normalization/`. No `.db` file was opened, listed into or read.
8. **SI's Python** is given as `pyvenv.cfg`'s `version = 3.13.13` with MacPorts' 3.13 framework as
   its `base-executable`, and "3.13.16 today": `/opt/local/bin/python3.13 --version` (MacPorts'
   interpreter, not SI's venv) printed `Python 3.13.16`. SI's `venv/bin/python` was not run.
9. **SGK's `main.py:3247`**: `postprocess_GkSourcePolicy` (`main.py:2871`) and SGK's
   `pool.object_store` path were read through `git show`, and the checklist states what the
   handler reads and what the persisted object is, with `path:line`s (§6 below), and that this was
   settled by reading, not by running, with an **Advice:** on how SGK could measure it.
10. **DatastoreKit's checklists are linked by URL** at `v0.2.1`
    (`https://github.com/ds283/DatastoreKit/blob/v0.2.1/docs/adoption/<file>.md`), and their
    `RayTools/` rows are cited, not copied: SGK `secondarygwkit.md:92`, `:704`, `:230-232`; CPBH
    `champbh.md:93`, `:602`; SI `stochasticinstantons.md:47`, `:105`, `:578`.
11. **The verdict is `v0.2.0`'s**: the output names `raypoolkit 0.2.0` (from
    `importlib.metadata`); `git diff eaef0ce -- raypoolkit` is empty before and after; the output
    reports `ray.is_initialized()` after the verdicts (`False` in every run).
12. **The breakage is of uncommitted work**: before and after each item, the SHA-256 of every new
    file and `git status --porcelain --untracked-files=all` (`$S/scripts/state.sh`); each diff
    applied with `git apply` after `git apply --check`, checked with `git apply -R --check`, and
    reverted with `git apply -R`; each "after" state `cmp`-equal to its "before". (c)'s edit was to
    the fixture's working tree.
13. **The fixture's override is `--repository PATH`**, which requires `--commit` (argparse refuses
    it alone, exit 2) and changes nothing of a default invocation. The fixture was made with
    `git init` in `$S/fixture` and committed with `git -c user.name=fixture -c
    user.email=fixture@example.invalid`, so no configuration was written. It holds no client file.
14. **The counts**: the suite is 121 before and after (it does not see `docs/`); `black --check
    raypoolkit docs` goes from 15 files to 16.

Choices and corrections of this prompt's agent:

15. **"Titled" is split.** The prompt's §0.2 ("Titled | 54 | 17 | 16") and the brief's
    clarification 2 ("Every site in every client is titled") count the `title` keyword. Of those,
    **28 (SGK), 12 (CPBH) and 10 (SI) pass `title=None`**, which prints nothing (for example SI
    `main.py:221`, `title=None` at `:235`); 26, 5 and 6 pass a title. The script reports "with a
    `title` keyword | 54 (`title=None` 28, set 26)", and each checklist says so. The verdict is not
    affected (no title is passed, deviation 2). **STRUCTURALLY REQUIRED** (§5: a checklist
    statement must be true).
16. **SI's `main.py:729-730` is answered, not left conditional.** By reading
    (`config/model_list.py:20-30`, `:67-77`, `:112-113`; `config/pipeline_setup.py:114`;
    `main.py:1153`, `:1211`), `build_model_list` returns at least one model whenever it returns,
    and `run_all_pipelines` has no other caller; so no SI run at `7bb3efd` reaches a size of 0, and
    the checklist's "sites that must change" is empty, with the two options given for the case SI
    later allows an empty model list. **IMPLEMENTATION CHOICE.**
17. **Fault 6 reaches no printed line of CPBH or SI at their commits.** The "available" segment is
    printed only by a pool with an `available_handler` (the package's `:216`, `:261`; CPBH's copy
    `:185`, `:230`; SI's `:191`, `:236`), and no site of either gives one (the appendices'
    spelling tables). The prompt's §0.3 "changes: the rate's numbers" stays true of the package;
    the checklists add that no line the clients print at the commit changes. **IMPLEMENTATION
    CHOICE.**
18. **A row the prompt's §0.3 does not have**, in CPBH's and SI's item 5: a task builder's `None`
    under `store_results=True` is still a `RuntimeError`, with the package's message (`:329-333`)
    in place of the copies' (CPBH `:311-315`, SI `:317-321`). SGK's copy has the package's message.
    **IMPLEMENTATION CHOICE.**
19. **CPBH's `.documents/architecture-summary.md` constructor table** (from `:157`; `store_handler`
    "Persists result", `:165`) is named as stale, though `:165` names neither `RayTools` nor
    `RayWorkPool` and so is not in the script's listing. **IMPLEMENTATION CHOICE.**
20. **SGK's other readers of the printed lines** are named: `qsi_resolution_cost.py:29` and
    `stage_counts.py:18` (dated measurement scripts under `docs/datastore-integrity-verification/`),
    and `test_pipeline_adoption.py:125` (a completion line fed to `StageTracker`). Each reads lines
    that do not change. **IMPLEMENTATION CHOICE.**
21. **The script reports more than §2.1's six items**: the files under `RayTools/` with their
    blobs (item 2 of each checklist); a table of the handler keywords by spelling; the handler
    keywords' source text at each compute pool; the `title` split; the `notify_*` keywords by
    source text; files that do not parse; and counts of binary files not searched and of datastore
    files not read (by suffix; none is tracked in any client). A keyword the constructor does not
    know would be passed as an `object()`, so that the constructor's own `TypeError` is the
    verdict; `*args` gives "not evaluated"; a non-literal `store_results` is left out and flagged.
    None of these arises at a client's commit. **IMPLEMENTATION CHOICE.**
22. **The fixture has a `RayTools/` of its own**: an empty `__init__.py` and a `RayWorkPool.py`
    holding a call with `create_batch_size=0`, which the script must not count (it does not: 5
    calls, and `RayTools/` listed with its blobs). **IMPLEMENTATION CHOICE.**
23. **Each checklist advises keeping the lookup-only sites' `None`s in the adoption commit**, so
    that its diff is the imports (and, for SI, item 3). **IMPLEMENTATION CHOICE.**
24. **The README's module map says "every name in it other than `RayWorkPool` and `DatastorePool`
    is private"** (the prompt's wording) and adds that those two are the package's public names,
    `raypoolkit/__init__.py:16-18`. `DatastorePool` is in the module's namespace by its import from
    `raypoolkit.contract` (`raypoolkit/RayWorkPool.py:23`). **IMPLEMENTATION CHOICE.**

Slips:

25. **Four read-only commands outside the brief's list for other repositories**:
    `git -C ChamPBH branch --show-current` and `git -C ChamPBH remote -v`;
    `git -C DatastoreKit remote get-url origin`; and `ls -l` of `StochasticInstantons/venv/bin/python3`,
    a `stat` of a symlink in SI's working tree, which printed its target (`python`) and opened no
    file. None writes, and no fact of a checklist rests on them (CPBH's branch is the prompt's §0).
    The clients' `HEAD`, status and stash are equal before and after (§3.4). **UNINTENDED DRIFT.**
26. **The first runs of the script preceded a one-line comment fix** in it
    (`arguments = {}  # parameter -> the argument's ast node`). Every output in this log and in the
    appendices is from the script as committed (SHA-256 `7f2851c0…4ab5a7`, §3.2), and equals the
    earlier runs byte for byte. **UNINTENDED DRIFT**, corrected.

## 3. Verification performed

### 3.1 The suite (prompt §3.1)

From the repository root, `./venv/bin/python -m unittest discover -s raypoolkit/tests -t .`, output
to `$S/out/suite-before.txt` and `$S/out/suite-after.txt`, verdicts grepped:

```text
before: Ran 121 tests in 1.397s / OK
after:  Ran 121 tests in 1.068s / OK
```

**121 → 121.** No file under `raypoolkit/` changed: `git diff eaef0ce --stat -- raypoolkit` is
empty before and after.

### 3.2 The script (prompt §3.2)

The script as committed: SHA-256
`7f2851c062cd58967cd3b4da57083bd8b6e5e9393f083aefe314d4807b4ab5a7`. Each client run twice from the
repository root, output to `$S/final/<client>-1.md` and `-2.md`:

```text
sgk run 1 exit 0 stderr bytes 0      sgk run 2 exit 0 stderr bytes 0      sgk: cmp identical
cpbh run 1 exit 0 stderr bytes 0     cpbh run 2 exit 0 stderr bytes 0     cpbh: cmp identical
si run 1 exit 0 stderr bytes 0       si run 2 exit 0 stderr bytes 0       si: cmp identical
sgk json exit 0, json.loads ok       cpbh json exit 0, json.loads ok      si json exit 0, json.loads ok
```

SGK takes about 40 s (1,432 tracked files, one `git show` each), CPBH 15 s, SI 11 s.

`./venv/bin/python docs/adoption/measure_client_pools.py si --commit 0000000` exits **2**, with
nothing on stdout and on stderr `cannot read the client: git -C /Users/ds283/Documents/Code/StochasticInstantons rev-parse --verify --quiet 0000000^{commit} failed:`.
`--repository $S/nonexistent --commit HEAD` exits 2; `--repository` without `--commit` exits 2
("--repository needs --commit").

**The figures against §0** (from the JSON's `totals`):

| | §0 | Script: SGK | Script: CPBH | Script: SI |
|---|---|---|---|---|
| Imports (all module level) | 7, 3, 3 | 7 | 3 | 3, 1 naming a private name (`_default_store_handler`) |
| String literals naming `RayTools` | 8, 0, 0 | 8 | 0 | 0 |
| `import_module` / `__import__` | 0 | 0 | 0 | 0 |
| Sites | 54, 17, 16 | 54 | 17 | 16 |
| No compute handler / given / default | 44/6/4, 14/3/0, 12/4/0 | 44 / 6 / 4 | 14 / 3 / 0 | 12 / 4 / 0 |
| … spelled | §0.2 | 44 with both `None`s | 14 with `store_handler=None` only | 12 with both `None`s |
| `store_results=True` | 39, 13, 11 | 39 | 13 | 11 |
| Titled | 54, 17, 16 | 54 keywords (28 `None`, 26 set) | 17 (12 / 5) | 16 (10 / 6) |
| Positional arguments | 2 everywhere | 2 at 54 | 2 at 17 | 2 at 16 |
| `**kwargs` / `*args` | none | 0 / 0 | 0 / 0 | 0 / 0 |
| Verdicts | all construct | 54 construct | 17 construct | 16 construct |
| Flags | SI's three | 0 | 0 | 5 on 4 calls |
| Non-`.py` lines | 196, 43, 89 | 196 (`CLAUDE.md` 1, `docs/` 39, `prompts/` 156) | 43 (`.documents/` 22, `prompts/` 21) | 89 (`.claude/` 17, `.documents/` 44, `.prompts/` 27, `CLAUDE.md` 1) |
| Test modules | 7, 0, 0 | 7 | 0 | 0 |
| `ray.is_initialized()` after | — | False | False | False |

Every figure equals §0's, the "titled" row read as deviation 15 says.

### 3.3 The fixture (prompt §3.3)

`$S/fixture`, `git init` and one commit, `58d2b67015f46387113cf02caa0d2a8a7fe64494`
("Fixture for measure_client_pools.py"), holding `main.py`, `tests/test_pool.py`, `README.md`,
`RayTools/RayWorkPool.py` and `RayTools/__init__.py` (deviation 22). Run as
`./venv/bin/python docs/adoption/measure_client_pools.py sgk --repository $S/fixture --commit 58d2b67…`,
exit 0, twice, `cmp` identical. Each case of §3.3 is reported (the whole output is §5):

| §3.3 case | Reported |
|---|---|
| module-level `from RayTools.RayWorkPool import RayWorkPool, _private` | `main.py:3`, `(module)`, private `_private` |
| nested, the same | `main.py:13`, scope `run`, private `_private` |
| `import_module("RayTools.RayWorkPool")` | `main.py:15`, in the `import_module` table (and as a string literal) |
| lookup-only, both `None`s | `main.py:17`: `constructs` |
| `compute_handler=None, label_builder=f` | `main.py:27`: `ValueError: No compute handler was supplied, so label_builder would never be called; leave it out, or pass None` |
| compute handler and `store_handler=None` | `main.py:34`: `ValueError: A compute handler was supplied, so store_handler must not be None; leave it out to use the default` |
| `create_batch_size=0` | `main.py:41`: `ValueError: create_batch_size must be at least 1, not 0` |
| `max_task_queue=N` | `main.py:47`: `constructs`, **flagged** (`max_task_queue=N is not a literal; replaced by 1`, keyword at `:51`) |
| a test module naming `RayWorkPool` | `tests/test_pool.py:6` |
| a Markdown file naming `RayTools` | `README.md:3`, under top directory `README.md` |

The fixture's `RayTools/RayWorkPool.py` call is not counted (5 calls).

### 3.4 The clients are untouched (prompt §3.4)

`$S/scripts/clients_check.sh`, at the start (`$S/out/clients-before.txt`) and after every other
check of this log (`$S/out/clients-after.txt`); the two files `cmp` equal:

```text
SecondaryGWKit HEAD=b510bc90b66985532d28996ab4e5b13b0ff71709 porcelain=da39a3ee5e6b porcelain_lines=0 stash=0 blob=b4666fa89abb26829fd585b881947d7ef5172cea
ChamPBH HEAD=52142d75aebe00855804e2daff4f63aee50ffc3e porcelain=a772db72b9bc porcelain_lines=23 stash=0 blob=aaa6dc9218658e1389fe3eeee5d184dcd8dc0d26
StochasticInstantons HEAD=7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7 porcelain=da39a3ee5e6b porcelain_lines=0 stash=0 blob=92be5b2c9e4c2c65695078bd1b8f97db2f56c7b0
```

(`porcelain` is the first 12 hex digits of `git status --porcelain | shasum`.) Each `HEAD` and
`RayTools/RayWorkPool.py` blob is §0's. CPBH's 23 lines are its untracked files (deviation 7). No
client's `venv/` was used: `venv/pyvenv.cfg` was read as text for each; SI's
`venv/bin/python3` was `stat`ed once (deviation 25). DatastoreKit was read only through `git show
v0.2.1:<path>` and `git rev-parse`; afterwards `HEAD=d06b46a1d054…`, status empty, no stash.

### 3.5 `black` (prompt §3.5)

`./venv/bin/black --check raypoolkit docs` (25.1.0): "16 files would be left unchanged."

### 3.6 The links (prompt §3.6)

`$S/scripts/check_links.py` reads every Markdown link and autolink in the four documents, outside
fenced blocks: **40 links, 0 bad**. Every relative link resolves to a tracked file (or one of the
five new files), and every anchor to a heading of its target (`README.md#installing`,
`#supported-versions`, `#changes-in-v020`, `#which-handlers-a-pool-needs`,
`#the-printed-lines-are-part-of-the-interface`). Every external link is to
`https://github.com/ds283/DatastoreKit/…/v0.2.1/…`.

### 3.7 No Ray

`pgrep -lf 'gcs_server|raylet|ray::'` was empty at the start and at the end. Every run of the
script reports `ray.is_initialized()` `False` after its verdicts.

### 3.8 The printed lines of each copy against `v0.2.0`

`$S/scripts/compare_prints.py` reads each copy through `git show` and `eaef0ce`'s module, and
compares, by `ast.unparse`, every `print()` call and the four helpers `_readable_rate`,
`_format_rates`, `_build_queued_status_message` and `_build_completed_status_message`:

```text
SGK: prints 7 vs 7, equal=True
   _build_completed_status_message: equal=True
   _build_queued_status_message: equal=True
   _format_rates: equal=True
   _readable_rate: equal=True
CPBH: prints 7 vs 7, equal=True
   _build_completed_status_message: equal=False
      -    if self._persist_handler is not None:
      +    if self._store_handler is not None:
   _build_queued_status_message: equal=False
      -    if self._persist_handler is not None:
      +    if self._store_handler is not None:
   _format_rates: equal=True
   _readable_rate: equal=True
SI: prints 7 vs 7, equal=True
   _build_completed_status_message: equal=True
   _build_queued_status_message: equal=True
   _format_rates: equal=True
   _readable_rate: equal=True
```

CPBH's one difference is the condition of the "store" segment, which agrees with the package's at
every CPBH site (`champbh.md`, item 5).

## 4. The script's output, per client, whole

### SGK, `$S/final/sgk-1.md` (= `sgk-2.md`)

````text
# `RayWorkPool` in SecondaryGWKit (SGK) at `b510bc9`

- **Repository:** `/Users/ds283/Documents/Code/SecondaryGWKit`, read through `git` only.
- **Commit:** `b510bc90b66985532d28996ab4e5b13b0ff71709`.
- **Verdicts by:** `raypoolkit 0.2.0`, its own constructor.
- **Files:** 1432 tracked; 460 `.py` files outside `RayTools/` parsed; 0 did not parse; 0 binary, not searched; 0 datastores, not read.
- **`ray.is_initialized()` after the verdicts:** False.

## `RayTools/` at the commit

| File | Blob |
|---|---|
| `RayTools/RayWorkPool.py` | `b4666fa89abb26829fd585b881947d7ef5172cea` |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |

## Totals

| Measure | Count |
|---|---|
| Imports of a `RayTools` module | 7 (module level 7, nested 0) |
| … naming a private name | 0 |
| String literals naming `RayTools` | 8 |
| `import_module` / `__import__` calls naming `RayTools` | 0 |
| `RayWorkPool(...)` calls | 54 |
| … no compute handler (`compute_handler=None`) | 44 |
| … compute handler given | 6 |
| … compute handler left at its default | 4 |
| … `store_results=True` | 39 |
| … with a `title` keyword | 54 (`title=None` 28, set 26) |
| … positional arguments | 2 at 54 |
| … with `*args` / `**kwargs` | 0 / 0 |
| Verdicts | `constructs` 54 |
| Calls with a flag / flags | 0 / 0 |
| Lines of non-`.py` files naming `RayTools` or `RayWorkPool` | 196 |
| Test modules naming `RayTools` or `RayWorkPool` | 7 |

## The handler keywords, by spelling

Each handler keyword as absent (—), `None` or set; a row per spelling, with its calls.

| `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` | Calls |
|---|---|---|---|---|---|---|---|
| None | None | None | None | None | None | None | 6 |
| None | None | None | None | None | — | None | 27 |
| None | None | None | None | None | set | None | 1 |
| None | None | None | — | — | — | — | 10 |
| — | — | — | — | None | — | set | 1 |
| — | — | — | — | — | — | — | 2 |
| — | — | — | — | set | — | set | 1 |
| set | — | — | — | None | set | None | 1 |
| set | — | — | — | set | None | set | 1 |
| set | — | — | — | set | — | set | 2 |
| set | — | — | — | set | set | set | 2 |

## Imports of a `RayTools` module (7)

| File:line | Scope | Statement | Private names |
|---|---|---|---|
| `extract_GkSource_data.py:37` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_GkWKB_data.py:35` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_Gk_data.py:32` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_QuadSourceIntegral_data.py:42` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_TkWKB_data.py:30` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `extract_tensor_source_data.py:31` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `main.py:63` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |

## String literals naming `RayTools` (8)

```text
Datastore/tests/test_layer_is_generic.py:1 [(module)] "\nThe generic layer names nothing of the project, and imports nothing of it but two generic\nmodules (prompts/datastore-generic, prompt 09; README \u00a75 rule
Datastore/tests/test_layer_is_generic.py:70 [layer_files] "RayTools"
Datastore/tests/test_layer_is_generic.py:88 [(module)] "RayTools/RayWorkPool.py"
Datastore/tests/test_layer_is_generic.py:120 [(module)] "RayTools"
Datastore/tests/test_layer_is_generic.py:192 [import_allowed] "RayTools"
Datastore/tests/test_layer_is_generic.py:357 [TestTheLayerImportsNoProjectPackage.test_the_allow_list] "RayTools.RayWorkPool"
docs/tolerance-convergence/inventory.py:382 [(module)] "RayTools"
prompts/datastore-generic/orchestrator/measure-09/scripts/m3_make_mutations.py:33 [(module)] "    for path in (REPO_ROOT / \"RayTools\").glob(\"*.py\"):\n        found.add(path.relative_to(REPO_ROOT).as_posix())\n"
```

## `import_module` / `__import__` calls naming `RayTools` (0)

None.

## `RayWorkPool(...)` calls (54)

Each call at the line of its name. Handlers: absent (—), `None` or set. Sizes: the source text of each size keyword given. `results`: `store_results`. Verdict: `v0.2.0`'s constructor, given the classes.

| File:line | Scope | Pos. | `**` | compute | store | persist | available | validation | post | label | Sizes | `results` | Title | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `extract_GkSource_data.py:812` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_GkSource_data.py:825` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_GkSource_data.py:910` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_GkWKB_data.py:403` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_GkWKB_data.py:416` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_GkWKB_data.py:483` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_Gk_data.py:359` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_Gk_data.py:372` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_Gk_data.py:432` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_QuadSourceIntegral_data.py:1105` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_QuadSourceIntegral_data.py:1118` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_QuadSourceIntegral_data.py:1272` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_TkWKB_data.py:422` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_TkWKB_data.py:472` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `extract_tensor_source_data.py:355` | `run_pipeline` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `extract_tensor_source_data.py:399` | `run_pipeline` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `main.py:1042` | `run_pipeline` | 2 | — | — | — | — | — | — | — | — | `create_batch_size=10`, `process_batch_size=10`, `max_task_queue=30` | True | set | `constructs` |
| `main.py:1057` | `run_pipeline` | 2 | — | — | — | — | — | — | — | — | `create_batch_size=10`, `process_batch_size=10`, `max_task_queue=30` | True | set | `constructs` |
| `main.py:1319` | `run_pipeline.build_Tk_numeric_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1420` | `run_pipeline` | 2 | — | set | — | — | — | set | set | set | `create_batch_size=2`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:1483` | `run_pipeline.build_Tk_WKB_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1550` | `run_pipeline.build_Tk_WKB_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1634` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:1701` | `run_pipeline.build_tensor_source_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1767` | `run_pipeline.build_tensor_source_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1824` | `run_pipeline.build_tensor_source_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1940` | `run_pipeline` | 2 | — | — | — | — | — | set | — | set | `create_batch_size=1`, `process_batch_size=20`, `max_task_queue=300` | False | set | `constructs` |
| `main.py:1993` | `run_pipeline.build_Gk_numeric_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2115` | `run_pipeline` | 2 | — | set | — | — | — | set | set | set | `create_batch_size=2`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:2188` | `run_pipeline.build_Gk_WKB_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2265` | `run_pipeline.build_Gk_WKB_work` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2428` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:2502` | `run_pipeline.resolve_GkSource_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=5`, `process_batch_size=10` | True | None | `constructs` |
| `main.py:2584` | `run_pipeline.build_GkSource_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2659` | `run_pipeline.build_missing_GkSource` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=5`, `process_batch_size=10` | True | None | `constructs` |
| `main.py:2926` | `run_pipeline.build_incomplete_GkSourcePolicy` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:2974` | `run_pipeline.build_incomplete_GkSourcePolicy` | 2 | — | None | None | None | None | None | set | None | `create_batch_size=20`, `process_batch_size=20` | False | None | `constructs` |
| `main.py:3034` | `run_pipeline.build_GkSourcePolicy_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3074` | `run_pipeline.build_GkSourcePolicy_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3163` | `run_pipeline.build_missing_GkSourcePolicy` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3229` | `run_pipeline` | 2 | — | set | — | — | — | set | None | set | `create_batch_size=1`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:3247` | `run_pipeline` | 2 | — | set | — | — | — | None | set | None | `create_batch_size=1`, `process_batch_size=50`, `max_task_queue=100` | False | set | `constructs` |
| `main.py:3350` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3398` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3460` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3515` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3557` | `run_pipeline.resolve_QuadSourceIntegral_parents` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3686` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3783` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3824` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3886` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3958` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:3997` | `run_pipeline.build_QuadSourceIntegral_batch` | 2 | — | None | None | None | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:4146` | `run_pipeline` | 2 | — | — | — | — | — | None | — | set | `create_batch_size=1`, `process_batch_size=100`, `max_task_queue=1000` | False | set | `constructs` |

## Calls with a compute path: the handlers given (10)

The source text of each handler keyword given, at each call whose compute handler is given or left at its default.

| File:line | `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` |
|---|---|---|---|---|---|---|---|
| `main.py:1042` | — | — | — | — | — | — | — |
| `main.py:1057` | — | — | — | — | — | — | — |
| `main.py:1420` | `compute_Tk_numeric_work` | — | — | — | `validate_Tk_numeric_work` | `lambda obj: record_unresolved_osc(Tk_unresolved_osc, obj)` | `build_Tk_numeric_work_label` |
| `main.py:1634` | `compute_Tk_numeric_work` | — | — | — | `validate_Tk_numeric_work` | — | `build_Tk_numeric_work_label` |
| `main.py:1940` | — | — | — | — | `validate_tensor_source_work` | — | `build_tensor_source_work_label` |
| `main.py:2115` | `compute_Gk_numeric_work` | — | — | — | `validate_Gk_numeric_work` | `lambda obj: record_unresolved_osc(Gk_unresolved_osc, obj)` | `build_Gk_numeric_work_label` |
| `main.py:2428` | `compute_Gk_WKB_work` | — | — | — | `validate_Gk_WKB_work` | — | `build_Gk_WKB_work_label` |
| `main.py:3229` | `compute_GkSource_work` | — | — | — | `validate_GkSource_work` | `None` | `build_GkSource_work_label` |
| `main.py:3247` | `compute_GkSourcePolicy_work` | — | — | — | `None` | `postprocess_GkSourcePolicy` | `None` |
| `main.py:4146` | — | — | — | — | `None` | — | `build_QuadSourceIntegral_label` |

## Flags (0, on 0 calls)

None.

## Notification keywords, by source text (16 calls; never passed)

| File:line | Keywords |
|---|---|
| `extract_GkSource_data.py:910` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_GkWKB_data.py:483` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_Gk_data.py:432` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_QuadSourceIntegral_data.py:1272` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_TkWKB_data.py:472` | `notify_batch_size=50`, `notify_time_interval=120` |
| `extract_tensor_source_data.py:399` | `notify_batch_size=50`, `notify_time_interval=120` |
| `main.py:1042` | `notify_batch_size=10`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:1057` | `notify_batch_size=10`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:1420` | `notify_batch_size=500`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:1634` | `notify_batch_size=500`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:1940` | `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:2115` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:2428` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:3229` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:3247` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:4146` | `notify_batch_size=2000`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |

## Non-`.py` files naming `RayTools` or `RayWorkPool` (196 lines)

| Top directory | Lines | Files |
|---|---|---|
| `CLAUDE.md` | 1 | 1 |
| `docs/` | 39 | 10 |
| `prompts/` | 156 | 44 |

Each line outside the campaign records (`prompts/`, `.prompts/`), 40:

```text
CLAUDE.md:71: `RayTools/` files are not frozen either: they are not part of this extraction. SecondaryGWKit's
docs/a3-v2-readiness-audit.md:88: - **Helpers that make no `pool.` call** [read]: `RayWorkPool` with `compute_handler`,
docs/a3-v2-readiness-audit.md:90: only its `task_builder` and never stores (`RayTools/RayWorkPool.py`, the `lookup` branch);
docs/a3-v2-readiness-audit.md:232: measured. `RayWorkPool`'s `ray.wait` has no timeout (read: `RayTools/RayWorkPool.py`, the main
docs/a3-v2-readiness-audit.md:583: `KeyboardInterrupt` keeps its type; anything else is held until the wait ends, and `RayWorkPool`'s
docs/a3-v2-readiness-audit.md:584: wait has no timeout (S1, measured; RayWorkPool read). **So the handler must record the signal
docs/a3-v2-readiness-verification.md:536: File ".../RayTools/RayWorkPool.py", line 331, in run
docs/a3-v2-readiness/rehearsal/reader_rows.txt:10: File "/Users/ds283/Documents/Code/SecondaryGWKit/RayTools/RayWorkPool.py", line 331, in run
docs/backport-modules-audit.md:16: | `RayTools/RayWorkPool.py` | 558 lines | 580 | 590 |
docs/backport-modules-audit.md:48: - `RayWorkPool.py`: differs by exactly one change, present **only in `SI`** (item **E1**).
docs/backport-modules-audit.md:78: | **B4** | `RayWorkPool` task builder returning `None` | CPBH→SI | **Backport** | XS |
docs/backport-modules-audit.md:81: | **E1** | `store_handler` / `persist_handler` split in `RayWorkPool` | SI | **Backport with care** | M (35 call sites) |
docs/backport-modules-audit.md:220: ### B4. `RayWorkPool` does not tolerate a task builder returning `None`
docs/backport-modules-audit.md:222: - **SGWK location:** `RayTools/RayWorkPool.py:283-297` (the `list`/`tuple`/`set` vs. scalar dispatch)
docs/backport-modules-audit.md:256: ### E1. `RayWorkPool`: `store_handler` / `persist_handler` split
docs/backport-modules-audit.md:258: - **SGWK locations:** `RayTools/RayWorkPool.py:64-65` (`_default_store_handler`), `89-97`
docs/backport-modules-audit.md:284: `extract_TkWKB_data.py`, `extract_tensor_source_data.py`; 45 `RayWorkPool(...)` constructions in
docs/backport-modules-audit.md:429: - **D4.** `RayWorkPool` notification bookkeeping: `self._last_num_available_complete = self._num_store_complete`
docs/backport-modules-audit.md:430: (`SGWK/RayWorkPool.py:543`, `SI:575`) — copy-paste; should be `self._num_available_complete`.
docs/backport-modules-audit.md:456: `RayWorkPool` + `ClientPool`.
docs/backport-modules-audit.md:459: 5. **Commit 5 — `persist_handler` split (E1), if wanted.** `RayWorkPool` + all 35 `store_handler=None`
docs/backport-modules-verification.md:40: e81b145 Tidy up latent faults in ShardedPool, RayWorkPool and ClientPool (prompt 03)
docs/backport-modules-verification.md:44: 0ee16a8 Split RayWorkPool store_handler into store and persist handlers (prompt 05)
docs/backport-modules-verification.md:75: | `RayWorkPool(` | 45 | **45** |
docs/backport-modules-verification.md:110: | Byte-compile | `./venv/bin/python3 -m py_compile main.py extract_*.py Datastore/SQL/*.py Datastore/SQL/ObjectFactories/*.py RayTools/*.py config/sharding.py tools/*.py` | exit 0 |
docs/backport-modules-verification.md:112: | Import, for real | `import Datastore.SQL.ShardedPool`, `Datastore.SQL.Datastore`, `RayTools.RayWorkPool`, `config.sharding` | all import clean, **no `sys.modules` stub needed** — confirms `d6f4a43` generalises |
docs/backport-modules-verification.md:140: | 6 | Task builder returning `None` completes under `store_results=False`, raises under `store_results=True` | **RUN — PASS** | Against a real `RayWorkPool(pool, ...)` built from the live pool (prompt 03's own verification used a dummy `pool` stand-in): both branches behave exactly as B4 requires. |
docs/backport-modules-verification.md:141: | 7 | Default handlers still store a result correctly | **NOT RUN** | Needs a real compute-target object (`.available`/`.compute()`/`.store()` contract) carried through `RayWorkPool`'s compute→store→persist cycle. See §5. |
docs/backport-modules-verification.md:179: - **Check 7 (default handlers store a real compute result end-to-end).** `RayWorkPool`'s
docs/backport-modules-verification.md:183: for real needs one genuine compute-target object carried through a live `RayWorkPool`, which means
docs/backport-modules-verification.md:215: `Datastore`/`ShardedPool`/`RayWorkPool` test suite is future work, not something to bolt on here.
docs/backport-modules-verification.md:285: - `[01-shard-key-persistence]` and the `read_table`/`RayWorkPool`-negative-case half of
docs/datastore-generic-audit.md:242: `Datastore/shard_paths.py` and `RayTools/RayWorkPool.py`. The factories under OF are the client.
docs/datastore-generic-audit.md:244: infrastructure contract), `RayWorkPool.py` and `ProfileAgent.py` hold no project knowledge.
docs/gktk-remedial-verification.md:562: 16's wiring survives a real `RayWorkPool` with `store_results=False`.
docs/gktk-remedial-verification.md:704: 4. Prompt 16's per-$k$ unresolved-oscillation summary works in a real `RayWorkPool`: **16 printed
docs/one-loop-planning/resonance-scaffolding-v1/sigw-resonance-reconciliation.md:199: for every response `k`. It is looped, not vectorised over grid points (the `RayWorkPool` batches
docs/one-loop-planning/resonance-scaffolding-v1/sigw-resonance-reconciliation.md:287: **Vectorised or looped?** Looped over `(z_response, k, q, r)` work items through `RayWorkPool`, with
docs/source-remediation-verification.md:31: the oracle is valid.** A real `ShardedPool`/`RayWorkPool` run on a locally bootstrapped Ray
docs/tolerance-convergence/TOLERANCE-INVENTORY.md:563: Every keyword argument named `amplitude_rtol`, `atol`, `deriv_rtol`, `epsabs`, `epsrel`, `phase_atol`, `rtol`, `xtol` whose value is a numeric literal, in the production trees `AdaptiveLevin`, `ComputeTargets`, `CosmologyConcepts`, `CosmologyModels`, `Datastore`, `LiouvilleGreen`, `MetadataConcepts`, `Quadrature`, `RayTools`, `Units`, `config`, `utilities`, in `main.py` and in the `extract_*.py` readers. Test trees, `docs/` and `prompts/` are excluded: they measure the pipeline, they are not it.
```

## Test modules naming `RayTools` or `RayWorkPool` (7)

```text
ComputeTargets/tests/test_gksource_parent_set_main.py:218: """Stands in for RayWorkPool: runs the task builder over the items, in order, and keeps the
ComputeTargets/tests/test_gksource_parent_set_main.py:270: "RayWorkPool": _WorkPool,
ComputeTargets/tests/test_main_plumbing.py:432: """Both numeric RayWorkPool constructions pass a post_handler, and both are followed by a
ComputeTargets/tests/test_main_plumbing.py:449: and call.func.id == "RayWorkPool"
ComputeTargets/tests/test_main_plumbing.py:700: of the batch the enclosing `RayWorkPool` dispatches over. `unclassified` holds any site whose
ComputeTargets/tests/test_main_plumbing.py:730: # calls reached through a RayWorkPool task_builder: the tolerance is in the batch
ComputeTargets/tests/test_main_plumbing.py:736: and node.func.id == "RayWorkPool"
ComputeTargets/tests/test_main_plumbing.py:764: label = f"{scope_label}: RayWorkPool({batch_name}) line {call.lineno}"
ComputeTargets/tests/test_quadsource_integral_parent_main.py:615: """Stands in for RayWorkPool: runs the task builder over the items, in order, and keeps the
ComputeTargets/tests/test_quadsource_integral_parent_main.py:790: "RayWorkPool": _WorkPool,
ComputeTargets/tests/test_quadsource_policy_main.py:136: the ``key`` entry or keyword). "query" is a RayWorkPool dispatch over a batch of payload
ComputeTargets/tests/test_quadsource_policy_main.py:145: and node.func.id == "RayWorkPool"
ComputeTargets/tests/test_wkb_numeric_parent_main.py:77: RayWorkPool dispatch over a batch (an existence query or a stage lookup) and "construction" for
ComputeTargets/tests/test_wkb_numeric_parent_main.py:86: and node.func.id == "RayWorkPool"
ComputeTargets/tests/test_wkb_numeric_parent_main.py:114: """The RayWorkPool lines of `scope` dispatching a lookup of `cls`."""
ComputeTargets/tests/test_wkb_numeric_parent_main.py:120: and node.func.id == "RayWorkPool"
Datastore/tests/test_layer_is_generic.py:7: module of ``RayTools/``. ``layer_files()`` derives the set from the filesystem, not from
Datastore/tests/test_layer_is_generic.py:70: for path in (REPO_ROOT / "RayTools").glob("*.py"):
Datastore/tests/test_layer_is_generic.py:88: "RayTools/RayWorkPool.py",
Datastore/tests/test_layer_is_generic.py:120: _NOT_PROJECT_PACKAGES = {"Datastore", "RayTools", "config"}
Datastore/tests/test_layer_is_generic.py:182: # WallclockTimer and format_time (Datastore, ProfileAgent, RayWorkPool): a shared helper that
Datastore/tests/test_layer_is_generic.py:192: if root == "RayTools":
Datastore/tests/test_layer_is_generic.py:357: "RayTools.RayWorkPool",
RunRegistry/tests/test_pipeline_adoption.py:32: # Six lines in the vocabulary `RayWorkPool` prints, in the order it prints them: the banner from
```

## Files that do not parse (0)

None.
````

### CPBH, `$S/final/cpbh-1.md` (= `cpbh-2.md`)

````text
# `RayWorkPool` in ChamPBH (CPBH) at `52142d7`

- **Repository:** `/Users/ds283/Documents/Code/ChamPBH`, read through `git` only.
- **Commit:** `52142d75aebe00855804e2daff4f63aee50ffc3e`.
- **Verdicts by:** `raypoolkit 0.2.0`, its own constructor.
- **Files:** 478 tracked; 203 `.py` files outside `RayTools/` parsed; 0 did not parse; 4 binary, not searched; 0 datastores, not read.
- **`ray.is_initialized()` after the verdicts:** False.

## `RayTools/` at the commit

| File | Blob |
|---|---|
| `RayTools/RayWorkPool.py` | `aaa6dc9218658e1389fe3eeee5d184dcd8dc0d26` |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |

## Totals

| Measure | Count |
|---|---|
| Imports of a `RayTools` module | 3 (module level 3, nested 0) |
| … naming a private name | 0 |
| String literals naming `RayTools` | 0 |
| `import_module` / `__import__` calls naming `RayTools` | 0 |
| `RayWorkPool(...)` calls | 17 |
| … no compute handler (`compute_handler=None`) | 14 |
| … compute handler given | 3 |
| … compute handler left at its default | 0 |
| … `store_results=True` | 13 |
| … with a `title` keyword | 17 (`title=None` 12, set 5) |
| … positional arguments | 2 at 17 |
| … with `*args` / `**kwargs` | 0 / 0 |
| Verdicts | `constructs` 17 |
| Calls with a flag / flags | 0 / 0 |
| Lines of non-`.py` files naming `RayTools` or `RayWorkPool` | 43 |
| Test modules naming `RayTools` or `RayWorkPool` | 0 |

## The handler keywords, by spelling

Each handler keyword as absent (—), `None` or set; a row per spelling, with its calls.

| `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` | Calls |
|---|---|---|---|---|---|---|---|
| None | None | — | None | None | None | None | 1 |
| None | None | — | None | None | — | None | 13 |
| set | — | — | — | set | — | set | 3 |

## Imports of a `RayTools` module (3)

| File:line | Scope | Statement | Private names |
|---|---|---|---|
| `main.py:50` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `plot_ScalarModel.py:44` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `plot_by_beta.py:38` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |

## String literals naming `RayTools` (0)

None.

## `import_module` / `__import__` calls naming `RayTools` (0)

None.

## `RayWorkPool(...)` calls (17)

Each call at the line of its name. Handlers: absent (—), `None` or set. Sizes: the source text of each size keyword given. `results`: `store_results`. Verdict: `v0.2.0`'s constructor, given the classes.

| File:line | Scope | Pos. | `**` | compute | store | persist | available | validation | post | label | Sizes | `results` | Title | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `main.py:193` | `run_pipeline.build_solver_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:276` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=3`, `max_task_queue=24` | False | set | `constructs` |
| `main.py:355` | `run_pipeline.build_adiabatic_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:405` | `run_pipeline.build_adiabatic_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:473` | `run_pipeline.build_adiabatic_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:533` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=3`, `max_task_queue=24` | False | set | `constructs` |
| `main.py:611` | `run_pipeline.build_bbn_data_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:663` | `run_pipeline.build_bbn_data_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:736` | `run_pipeline.build_bbn_data_batch` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:820` | `run_pipeline` | 2 | — | set | — | — | — | set | — | set | `create_batch_size=2`, `process_batch_size=3`, `max_task_queue=24` | False | set | `constructs` |
| `plot_ScalarModel.py:1556` | `run_pipeline` | 2 | — | None | None | — | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `plot_by_beta.py:715` | `run_pipeline.report_dropped_bbn_models` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:803` | `run_pipeline.report_dropped_scalar_models` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:865` | `run_pipeline.build_plot_work` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:899` | `run_pipeline.build_plot_work` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:926` | `run_pipeline.build_plot_work` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `plot_by_beta.py:959` | `run_pipeline` | 2 | — | None | None | — | None | None | — | None | `create_batch_size=10`, `max_task_queue=10` | True | set | `constructs` |

## Calls with a compute path: the handlers given (3)

The source text of each handler keyword given, at each call whose compute handler is given or left at its default.

| File:line | `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` |
|---|---|---|---|---|---|---|---|
| `main.py:276` | `compute_solver_batch` | — | — | — | `validate_solver_batch` | — | `build_solver_batch_label` |
| `main.py:533` | `compute_adiabatic_batch` | — | — | — | `validate_adiabatic_batch` | — | `build_adiabatic_batch_label` |
| `main.py:820` | `compute_bbn_data_batch` | — | — | — | `validate_bbn_data_batch` | — | `build_bbn_data_batch_label` |

## Flags (0, on 0 calls)

None.

## Notification keywords, by source text (5 calls; never passed)

| File:line | Keywords |
|---|---|
| `main.py:276` | `notify_batch_size=2`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:533` | `notify_batch_size=2`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `main.py:820` | `notify_batch_size=2`, `notify_min_time_interval=MIN_NOTIFY_INTERVAL` |
| `plot_ScalarModel.py:1556` | `notify_batch_size=50`, `notify_time_interval=120` |
| `plot_by_beta.py:959` | `notify_batch_size=10`, `notify_min_time_interval=120` |

## Non-`.py` files naming `RayTools` or `RayWorkPool` (43 lines)

| Top directory | Lines | Files |
|---|---|---|
| `.documents/` | 22 | 2 |
| `prompts/` | 21 | 11 |

Each line outside the campaign records (`prompts/`, `.prompts/`), 22:

```text
.documents/architecture-summary.md:35: ├── RayTools/
.documents/architecture-summary.md:36: │   └── RayWorkPool.py               # Generic distributed work queue
.documents/architecture-summary.md:153: ### 3.2 `RayWorkPool` (`RayTools/RayWorkPool.py`)
.documents/architecture-summary.md:155: `RayWorkPool` is the single generic orchestrator for all computation phases. It is instantiated with a list of work items and a set of handler callables, and its `run()` method drives a state machine until every item has been processed.
.documents/architecture-summary.md:244: The `available` property is the sentinel used by `RayWorkPool` to distinguish "already in database" from "needs computation".
.documents/architecture-summary.md:355: 2. For missing items only, call `object_get(...)` without `_do_not_populate`. This creates skeleton rows and returns objects ready for `RayWorkPool` to compute and store.
.documents/architecture-summary.md:585: The `RayWorkPool` handles steps 3–4 automatically via its default `compute_handler` and `store_handler`.
.documents/architecture-summary.md:648: 5. Store sampled `SampleValues` in memory; `RayWorkPool` will later call `store()` and then `pool.object_store()`.
.documents/architecture-summary.md:829: - `store_tag`: groups related computations; used by `RayWorkPool` to tag outputs (e.g. `SamplesPerLog10Z_250`)
.documents/architecture-summary.md:855: → RayWorkPool with compute_handler = ScalarModel.compute()
.documents/architecture-summary.md:856: → RayWorkPool with validation_handler = pool.object_validate()
.documents/architecture-summary.md:862: → RayWorkPool with compute_handler = AdiabaticHistory.compute()
.documents/architecture-summary.md:868: → RayWorkPool with compute_handler = BBNData.compute(payload={"small_network": True})
.documents/architecture-summary.md:920: query_queue = RayWorkPool(
.documents/architecture-summary.md:969: **`RayWorkPool` resilience:** The work pool does not bail out if individual tasks fail — it continues processing remaining items. The `_do_not_populate` two-pass pattern means failed objects are skipped in downstream stages (checked via `obj.failure`).
.documents/architecture-summary.md:999: - `RayWorkPool` (entire file)
.documents/architecture-summary.md:1056: # Copies computation result into self (called by RayWorkPool after compute)
.documents/architecture-summary.md:1086: work_pool = RayWorkPool(
.documents/architecture-summary.md:1108: 4. **`compute()` must return an `ObjectRef`.** `RayWorkPool` expects a Ray future from `compute_handler`. If the computation is CPU-bound and cannot be a Ray task (rare), wrap it in `ray.remote`.
.documents/architecture-summary.md:1110: 5. **`store()` is called on the driver side, not in Ray.** After `ray.get(compute_ref)` completes, `RayWorkPool` calls `obj.store()` on the Python object in the driver process. This should copy data from the compute result into the object's fields. Then `pool.object_store(obj)` is called to serialize to the database.
.documents/architecture-summary.md:1116: 8. **`store_results=True` in `RayWorkPool` is only for query-only passes.** When `task_builder` returns lists of refs (the vectorized case), the indices break. Use `store_results=True` only with scalar-returning `task_builder`s.
.documents/integrator-audit-2026-09-30/README.md:69: short). Only `ComputationFailureError` is caught (`:823`). `RayTools/RayWorkPool.py` calls
```

## Test modules naming `RayTools` or `RayWorkPool` (0)

None.

## Files that do not parse (0)

None.
````

### SI, `$S/final/si-1.md` (= `si-2.md`)

````text
# `RayWorkPool` in StochasticInstantons (SI) at `7bb3efd`

- **Repository:** `/Users/ds283/Documents/Code/StochasticInstantons`, read through `git` only.
- **Commit:** `7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7`.
- **Verdicts by:** `raypoolkit 0.2.0`, its own constructor.
- **Files:** 363 tracked; 193 `.py` files outside `RayTools/` parsed; 0 did not parse; 1 binary, not searched; 0 datastores, not read.
- **`ray.is_initialized()` after the verdicts:** False.

## `RayTools/` at the commit

| File | Blob |
|---|---|
| `RayTools/RayWorkPool.py` | `92be5b2c9e4c2c65695078bd1b8f97db2f56c7b0` |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |

## Totals

| Measure | Count |
|---|---|
| Imports of a `RayTools` module | 3 (module level 3, nested 0) |
| … naming a private name | 1 |
| String literals naming `RayTools` | 0 |
| `import_module` / `__import__` calls naming `RayTools` | 0 |
| `RayWorkPool(...)` calls | 16 |
| … no compute handler (`compute_handler=None`) | 12 |
| … compute handler given | 4 |
| … compute handler left at its default | 0 |
| … `store_results=True` | 11 |
| … with a `title` keyword | 16 (`title=None` 10, set 6) |
| … positional arguments | 2 at 16 |
| … with `*args` / `**kwargs` | 0 / 0 |
| Verdicts | `constructs` 16 |
| Calls with a flag / flags | 4 / 5 |
| Lines of non-`.py` files naming `RayTools` or `RayWorkPool` | 89 |
| Test modules naming `RayTools` or `RayWorkPool` | 0 |

## The handler keywords, by spelling

Each handler keyword as absent (—), `None` or set; a row per spelling, with its calls.

| `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` | Calls |
|---|---|---|---|---|---|---|---|
| None | None | None | None | None | None | None | 2 |
| None | None | None | — | None | — | — | 10 |
| set | set | set | — | set | — | set | 4 |

## Imports of a `RayTools` module (3)

| File:line | Scope | Statement | Private names |
|---|---|---|---|
| `main.py:45` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool, _default_store_handler` | `_default_store_handler` |
| `plot_GradientCoupledSolutions.py:100` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |
| `plot_InstantonSolutions.py:72` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool` | — |

## String literals naming `RayTools` (0)

None.

## `import_module` / `__import__` calls naming `RayTools` (0)

None.

## `RayWorkPool(...)` calls (16)

Each call at the line of its name. Handlers: absent (—), `None` or set. Sizes: the source text of each size keyword given. `results`: `store_results`. Verdict: `v0.2.0`'s constructor, given the classes.

| File:line | Scope | Pos. | `**` | compute | store | persist | available | validation | post | label | Sizes | `results` | Title | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `main.py:221` | `_run_pipeline_queue` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:249` | `_run_pipeline_queue` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:316` | `_run_pipeline_queue` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:383` | `_run_pipeline_queue` | 2 | — | set | set | set | — | set | — | set | `create_batch_size=5`, `process_batch_size=3`, `max_task_queue=MAX_INFLIGHT_PIPELINE_UNIFIED` **flagged** | False | set | `constructs` |
| `main.py:445` | `_run_instanton_queue` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:492` | `_run_instanton_queue` | 2 | — | set | set | set | — | set | — | set | `create_batch_size=5`, `process_batch_size=3`, `max_task_queue=MAX_INFLIGHT_PIPELINE` **flagged** | False | set | `constructs` |
| `main.py:589` | `_run_gradient_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:718` | `run_all_pipelines` | 2 | — | set | set | set | — | set | — | set | `create_batch_size=len(traj_payloads)` **flagged**, `process_batch_size=len(traj_payloads)` **flagged** | True | set | `constructs` |
| `main.py:871` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:900` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:964` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1015` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1041` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | None | None | None | — | None | — | — | `create_batch_size=20`, `process_batch_size=20` | True | None | `constructs` |
| `main.py:1092` | `run_all_pipelines._run_homogeneous_branch` | 2 | — | set | set | set | — | set | — | set | `create_batch_size=5`, `process_batch_size=3`, `max_task_queue=MAX_INFLIGHT_PIPELINE` **flagged** | False | set | `constructs` |
| `plot_GradientCoupledSolutions.py:938` | `run_plots` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |
| `plot_InstantonSolutions.py:1171` | `run_plots` | 2 | — | None | None | None | None | None | None | None | `create_batch_size=10`, `process_batch_size=10` | False | set | `constructs` |

## Calls with a compute path: the handlers given (4)

The source text of each handler keyword given, at each call whose compute handler is given or left at its default.

| File:line | `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` |
|---|---|---|---|---|---|---|---|
| `main.py:383` | `lambda obj, **kw: obj.compute(**kw)` | `pipeline_store_handler` | `pipeline_persist_handler` | — | `lambda obj: pool.object_validate(obj)` | — | `lambda obj: f"Pipeline(dNstar={float(obj.delta_Nstar):.4g})"` |
| `main.py:492` | `lambda obj, **kwargs: obj.compute(**kwargs)` | `store_handler` | `persist_handler` | — | `lambda obj: pool.object_validate(obj)` | — | `label_builder` |
| `main.py:718` | `lambda obj, **kwargs: obj.compute(**kwargs)` | `inflaton_trajectory_store_handler` | `lambda obj, pool: pool.object_store(obj)` | — | `lambda obj: pool.object_validate(obj)` | — | `lambda obj: "InflatonTrajectory"` |
| `main.py:1092` | `lambda obj, **kwargs: obj.compute(**kwargs)` | `_default_store_handler` | `lambda obj, pool: pool.object_store(obj)` | — | `lambda obj: pool.object_validate(obj)` | — | `lambda obj: ( f"CompactionFunction(dNstar={float(obj.delta_Nstar):.4g})" )` |

## Flags (5, on 4 calls)

| Call | Keyword line | Flag |
|---|---|---|
| `main.py:383` | `:396` | `max_task_queue=MAX_INFLIGHT_PIPELINE_UNIFIED is not a literal; replaced by 1` |
| `main.py:492` | `:505` | `max_task_queue=MAX_INFLIGHT_PIPELINE is not a literal; replaced by 1` |
| `main.py:718` | `:729` | `create_batch_size=len(traj_payloads) is not a literal; replaced by 1` |
| `main.py:718` | `:730` | `process_batch_size=len(traj_payloads) is not a literal; replaced by 1` |
| `main.py:1092` | `:1107` | `max_task_queue=MAX_INFLIGHT_PIPELINE is not a literal; replaced by 1` |

## Notification keywords, by source text (2 calls; never passed)

| File:line | Keywords |
|---|---|
| `plot_GradientCoupledSolutions.py:938` | `notify_batch_size=50`, `notify_time_interval=120` |
| `plot_InstantonSolutions.py:1171` | `notify_batch_size=50`, `notify_time_interval=120` |

## Non-`.py` files naming `RayTools` or `RayWorkPool` (89 lines)

| Top directory | Lines | Files |
|---|---|---|
| `.claude/` | 17 | 3 |
| `.documents/` | 44 | 8 |
| `.prompts/` | 27 | 8 |
| `CLAUDE.md` | 1 | 1 |

Each line outside the campaign records (`prompts/`, `.prompts/`), 62:

```text
.claude/rules/compute-targets.md:105: logging. `RayWorkPool` supplies it via `label_builder` if one is configured.
.claude/rules/datastore-factories.md:13: This is the most important rule in this file. Violating it causes `RayWorkPool`
.claude/rules/datastore-factories.md:23: Note: `RayWorkPool` has three distinct handler slots — `store_handler` (calls
.claude/rules/datastore-factories.md:42: # Not found — return UNPOPULATED object; RayWorkPool will call compute()
.claude/rules/datastore-factories.md:113: guaranteed by the `store_handler` step in `RayWorkPool`, which runs before
.claude/rules/datastore-factories.md:223: and `validated = True`. This flag is used by `RayWorkPool` for the initial
.claude/rules/ray-dispatch.md:58: """Must return an ObjectRef. RayWorkPool waits on this."""
.claude/rules/ray-dispatch.md:65: """Called on the DRIVER by RayWorkPool after compute() resolves.
.claude/rules/ray-dispatch.md:99: ## Why `RayWorkPool` requires plain classes
.claude/rules/ray-dispatch.md:101: `RayTools/RayWorkPool.py` accesses compute targets as plain Python objects:
.claude/rules/ray-dispatch.md:106: return an `ObjectRef`; `RayWorkPool` never calls `.remote()` on it
.claude/rules/ray-dispatch.md:116: class Foo(DatastoreObject):          # NEVER — breaks RayWorkPool
.claude/rules/ray-dispatch.md:214: The custom handler must be wired in explicitly at the `RayWorkPool` call site
.claude/rules/ray-dispatch.md:229: O(grid_size). Run this inside a `RayWorkPool` with large batch sizes
.claude/rules/ray-dispatch.md:236: Feed only the missing items into a second `RayWorkPool` with a conservative
.claude/rules/ray-dispatch.md:237: `max_task_queue` (e.g. 20). `RayWorkPool`'s main loop guards task creation
.claude/rules/ray-dispatch.md:245: `RayWorkPool`. This overlaps queries with compute, but has two drawbacks that
.documents/FILE_MAP.md:31: | `RayTools_RayWorkPool.py` | `RayTools/RayWorkPool.py` | `RayWorkPool` class: the core distributed work-queue abstraction; manages the **lookup → compute → store → persist → validate** state machine over a list of compute targets using `ray.wait()`; provides `create_batch_size`, `process_batch_size`, `max_task_queue` controls |
.documents/FILE_MAP.md:287: | `RayTools/` (other files)                               | Only `RayWorkPool.py` is directly relevant                                  |
.documents/INFRASTRUCTURE.md:1: # INFRASTRUCTURE — how `Datastore`, `ShardedPool`, and `RayWorkPool` work
.documents/INFRASTRUCTURE.md:4: (`Datastore`) and distributed dispatch (`RayWorkPool`). It does not cover the
.documents/INFRASTRUCTURE.md:46: `RayWorkPool` uses to decide whether a grid point needs computing at all.
.documents/INFRASTRUCTURE.md:128: is exactly the signal `RayWorkPool` needs to decide computation is required.
.documents/INFRASTRUCTURE.md:286: **Why `Foo` must stay a plain class:** `RayWorkPool` accesses compute targets
.documents/INFRASTRUCTURE.md:289: *return* an `ObjectRef` rather than `RayWorkPool` calling `.remote()` on
.documents/INFRASTRUCTURE.md:346: handler is wired explicitly at the `RayWorkPool` call site — never hidden
.documents/INFRASTRUCTURE.md:351: ## 9. `RayWorkPool` — the distributed work-queue
.documents/INFRASTRUCTURE.md:353: `RayTools/RayWorkPool.py` drives every compute stage through five states:
.documents/INFRASTRUCTURE.md:357: RayWorkPool(
.documents/INFRASTRUCTURE.md:411: `RayWorkPool`, with a conservative `max_task_queue` (e.g. 20). Because
.documents/INFRASTRUCTURE.md:412: `RayWorkPool`'s own loop already caps in-flight tasks, no separate manual
.documents/INFRASTRUCTURE.md:418: `RayWorkPool`. That approach overlaps queries with compute but has two
.documents/INFRASTRUCTURE.md:452: MISS path, inside RayWorkPool:
.documents/INFRASTRUCTURE.md:478: RayWorkPool over compute_list:
.documents/architecture-summary.md:27: RayTools/
.documents/architecture-summary.md:28: RayWorkPool.py               — distributed work-queue abstraction
.documents/architecture-summary.md:172: persisted. `RayWorkPool` reads this property directly.
.documents/architecture-summary.md:188: which signals to `RayWorkPool` that computation is needed.
.documents/architecture-summary.md:245: **Why `Foo` must be a plain class:** `RayWorkPool` accesses compute targets as
.documents/architecture-summary.md:319: ## RayWorkPool
.documents/architecture-summary.md:321: `RayTools/RayWorkPool.py` provides the main distributed work-queue abstraction.
.documents/architecture-summary.md:328: RayWorkPool(
.documents/architecture-summary.md:349: `RayWorkPool.run()` drives a state machine over all in-flight `ObjectRef`s:
.documents/architecture-summary.md:419: One `RayWorkPool` runs over all `(model, phi0, pi0, potential)` combinations.
.documents/architecture-summary.md:482: RayWorkPool(
.documents/architecture-summary.md:518: MISS path in RayWorkPool:
.documents/architecture-summary.md:556: RayWorkPool:
.documents/gradient-coupled-instanton/24-prerequisite-wallclock-safeguard.md:75: the Ray dispatch layer, and `RayTools/RayWorkPool.py` is protected
.documents/gradient-coupled-instanton/24-prerequisite-wallclock-safeguard.md:78: through the *real* `main.py`/`RayWorkPool` pipeline (per the prompt's own
.documents/gradient-coupled-instanton/24-prerequisite-wallclock-safeguard.md:86: driver that bypasses `RayWorkPool` and dispatches
.documents/gradient-coupled-plotting/DESIGN_gradient_coupled_plotting.md:65: dispatch.py          # RayWorkPool wiring, generic _render_item wrapper,
.documents/gradient-coupled-plotting/DESIGN_gradient_coupled_plotting.md:336: the terminal `RayWorkPool(..., store_results=False)` drain stay exactly as they
.documents/gradient-coupled-plotting/PROMPT_AUTHORING_BRIEF.md:209: `RayWorkPool(..., store_results=False)` drain must be preserved exactly.
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:4: `2026-06-14_Codebase-evaluation-and-refactoring-strategy.md`, `2026-06-16_Inflaton-trajectory-sampling-and-database-storage-strategy.md`, `2026-06-16_InflatonTrajectory-validation-failure-diagnosis.md`, `2026-06-16_Refactoring-plotting-scripts-for-RayWorkPool-integration.md`, `2026-06-16_Converting-instanton-trajectories-to-primordial-black-hole-d.md`, `2026-06-21_Enhancing-instanton-solution-plot-styling-and-metadata.md`, `2026-06-21_Radial-density-profile-and-compaction-function-analysis.md`, `2026-06-22_Ray-failure-mode-identification.md`, `2026-06-22_DOE-meaning-in-project-context.md`.
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:20: **14 Jun 20:46.** David's brief (reproduced verbatim as `.prompts/base-implementation/01-initial.md`): reuse ChamPBH's three layers — `RayWorkPool`, `Datastore`/`ShardedPool`, the lookup–compute–store "unit of work"; single-field scope but "build the code in such a way that the extensions of multiple field models is considered from the beginning"; no slow-roll approximation, state `(φ, π=dφ/dN)` doubled by MSR response fields `P₁, P₂`; the compaction-function pipeline sketch (end-of-inflation surface fixes `k_end`; at each step "only the core region continues on the instanton; the outer region detaches"). **Recorded** (01-initial.md).
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:22: **14 Jun 20:47 — Claude's keep/drop evaluation.** Keep: `RayWorkPool`, `ShardedPool`/`Datastore`/`SerialPoolBroker`, `DatastoreObject`, Dimensionless/Dimensionful quantities and factories, `tolerance`/`version`/`store_tag`, `IntegrationSupervisor`/`RHS_timer`, `phi_value`/`pi_value`. Drop: `ConformalCouplings/`, `QCD_Cosmology`, chameleon `StateVector`/`ODEPolicy`, `ScalarModel*`, `AdiabaticHistory`, `BBNData`, `redshift`/`temperature` as time coordinate (replaced by `efold_value`/`efold_array`). Also flagged: `main.py` bug `allowed_drop_actions` undefined (neutralised by hollowing out `main.py`). **Recorded** only at the level of the resulting layout (architecture-summary "Repository layout", CLAUDE.md protected list); the keep/drop *reasoning* and the ChamPBH→instanton correspondence table (e.g. `CompactionFunction` "analogous to `AdiabaticHistory`", `PBHMassFunction` "analogous to `BBNData`") are **NOT recorded**.
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:32: **15 Jun 11:26–12:25 — the `@ray.remote`-on-classes incident.** Claude Code had decorated `InflatonTrajectory` as a Ray actor and used `Foo.__ray_actor_class__(...)` in the factory; David asked why, since `ScalarModel` in ChamPBH was never an actor. Diagnosis: `RayWorkPool` reads `obj.available`, calls `obj.store()` on the driver, and expects `compute()` to return an `ObjectRef`; corrective Prompt 3.5. **Recorded** fully (ray-dispatch.md, datastore-factories.md, CLAUDE.md rule 1).
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:42: ### 16 June — sampling strategy, `RayWorkPool` handlers, time convention
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:48: **16 Jun 10:15–10:29 — backpressure.** Claude's draft left `main.py` driving Ray manually; David: `RayWorkPool` "is supposed to be the abstraction for work queue management. We don't want to submit all tasks to Ray simultaneously otherwise it gets overwhelmed"; a lookup queue then a work queue, as in ChamPBH. David also refused to defer the custom store handler ("The whole point of this refactoring is that `InflatonTrajectory` needs to mint the `efold_value` objects"). **Recorded** (two-pass dispatch in ray-dispatch.md and INFRASTRUCTURE §10, with the grouper-batch comparison).
.documents/handoff-notes/2026-10-08/summary-E-june-pipeline.md:54: **16 Jun 11:39–11:58 — plotting refactor.** `plot_InstantonSolutions.py` must go through `RayWorkPool` "to prevent the machine on which the plotting code is running from being overwhelmed"; `read_table` on sharded tables is forbidden (reads one shard); fetch per-item via `object_get` keyed by `delta_Nstar`; `read_table_config` extended by David to `delta_Nstar`, `efold_value`, `inflaton_mass`, `quartic_coupling`, `phi_value`, `pi_value`. **Recorded** (pool-read-apis.md).
.documents/handoff-notes/2026-10-08/summary-F-june-science.md:15: *Design decisions (all recorded).* Step-1 N_final-decoupling test; Sobol/LHC in (δN★, ΔN) with coarse N_final; GP regressor on the signed distance C̄_max − 0.4 rather than a classifier; scalars-only storage; Sobol indices on the surrogate. David rejected weighting-down extrapolated points: the extrapolation "is done using an exact analytic formula and should be reliable". David proposed the unified single-`RayWorkPool` pipeline (prompts 6–8) after noticing the two-pass architecture made `set_store_full_values(False)` unsafe. David set the integrity rule: a recompute whose scalars disagree with a stored row "is an integrity failure and shouldn't happen ... we would raise an exception" (`PIPELINE_SCALAR_INTEGRITY_RTOL = 1e-4`). Footer provenance `[summary-only]` added after David could not tell the two smoke-test runs apart. Output: prompts 01–10 and `handoff-sparse-sampling.md`.
CLAUDE.md:95: RayTools/                          Datastore/SQL/ShardedPool.py
```

## Test modules naming `RayTools` or `RayWorkPool` (0)

None.

## Files that do not parse (0)

None.
````

## 5. The fixture's output

````text
# `RayWorkPool` in `/private/tmp/claude-35086/-Users-ds283-Documents-Code-RayPoolKit/efa28c68-9285-420b-8568-d547d98564d3/scratchpad/agent06/fixture` (in place of SecondaryGWKit) at `58d2b67`

- **Repository:** `/private/tmp/claude-35086/-Users-ds283-Documents-Code-RayPoolKit/efa28c68-9285-420b-8568-d547d98564d3/scratchpad/agent06/fixture`, read through `git` only.
- **Commit:** `58d2b67015f46387113cf02caa0d2a8a7fe64494`.
- **Verdicts by:** `raypoolkit 0.2.0`, its own constructor.
- **Files:** 5 tracked; 2 `.py` files outside `RayTools/` parsed; 0 did not parse; 0 binary, not searched; 0 datastores, not read.
- **`ray.is_initialized()` after the verdicts:** False.

## `RayTools/` at the commit

| File | Blob |
|---|---|
| `RayTools/RayWorkPool.py` | `cdd22855dfd5d2a0ed51ba00c625dd02def3b540` |
| `RayTools/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |

## Totals

| Measure | Count |
|---|---|
| Imports of a `RayTools` module | 2 (module level 1, nested 1) |
| … naming a private name | 2 |
| String literals naming `RayTools` | 1 |
| `import_module` / `__import__` calls naming `RayTools` | 1 |
| `RayWorkPool(...)` calls | 5 |
| … no compute handler (`compute_handler=None`) | 2 |
| … compute handler given | 1 |
| … compute handler left at its default | 2 |
| … `store_results=True` | 1 |
| … with a `title` keyword | 1 (`title=None` 0, set 1) |
| … positional arguments | 2 at 5 |
| … with `*args` / `**kwargs` | 0 / 0 |
| Verdicts | `ValueError: A compute handler was supplied, so store_handler must not be None; leave it out to use the default` 1; `ValueError: No compute handler was supplied, so label_builder would never be called; leave it out, or pass None` 1; `ValueError: create_batch_size must be at least 1, not 0` 1; `constructs` 2 |
| Calls with a flag / flags | 1 / 1 |
| Lines of non-`.py` files naming `RayTools` or `RayWorkPool` | 1 |
| Test modules naming `RayTools` or `RayWorkPool` | 1 |

## The handler keywords, by spelling

Each handler keyword as absent (—), `None` or set; a row per spelling, with its calls.

| `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` | Calls |
|---|---|---|---|---|---|---|---|
| None | None | None | — | — | — | — | 1 |
| None | — | — | — | — | — | set | 1 |
| — | — | — | — | — | — | — | 2 |
| set | None | — | — | — | — | — | 1 |

## Imports of a `RayTools` module (2)

| File:line | Scope | Statement | Private names |
|---|---|---|---|
| `main.py:3` | `(module)` | `from RayTools.RayWorkPool import RayWorkPool, _private` | `_private` |
| `main.py:13` | `run` | `from RayTools.RayWorkPool import RayWorkPool, _private` | `_private` |

## String literals naming `RayTools` (1)

```text
main.py:15 [run] "RayTools.RayWorkPool"
```

## `import_module` / `__import__` calls naming `RayTools` (1)

| File:line | Scope | Call |
|---|---|---|
| `main.py:15` | `run` | `importlib.import_module("RayTools.RayWorkPool")` |

## `RayWorkPool(...)` calls (5)

Each call at the line of its name. Handlers: absent (—), `None` or set. Sizes: the source text of each size keyword given. `results`: `store_results`. Verdict: `v0.2.0`'s constructor, given the classes.

| File:line | Scope | Pos. | `**` | compute | store | persist | available | validation | post | label | Sizes | `results` | Title | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `main.py:17` | `run` | 2 | — | None | None | None | — | — | — | — | — | True | set | `constructs` |
| `main.py:27` | `run` | 2 | — | None | — | — | — | — | — | set | — | — | — | `ValueError: No compute handler was supplied, so label_builder would never be called; leave it out, or pass None` |
| `main.py:34` | `run` | 2 | — | set | None | — | — | — | — | — | — | — | — | `ValueError: A compute handler was supplied, so store_handler must not be None; leave it out to use the default` |
| `main.py:41` | `run` | 2 | — | — | — | — | — | — | — | — | `create_batch_size=0` | — | — | `ValueError: create_batch_size must be at least 1, not 0` |
| `main.py:47` | `run` | 2 | — | — | — | — | — | — | — | — | `max_task_queue=N` **flagged** | — | — | `constructs` |

## Calls with a compute path: the handlers given (3)

The source text of each handler keyword given, at each call whose compute handler is given or left at its default.

| File:line | `compute_handler` | `store_handler` | `persist_handler` | `available_handler` | `validation_handler` | `post_handler` | `label_builder` |
|---|---|---|---|---|---|---|---|
| `main.py:34` | `f` | `None` | — | — | — | — | — |
| `main.py:41` | — | — | — | — | — | — | — |
| `main.py:47` | — | — | — | — | — | — | — |

## Flags (1, on 1 calls)

| Call | Keyword line | Flag |
|---|---|---|
| `main.py:47` | `:51` | `max_task_queue=N is not a literal; replaced by 1` |

## Notification keywords, by source text (0 calls; never passed)

None.

## Non-`.py` files naming `RayTools` or `RayWorkPool` (1 lines)

| Top directory | Lines | Files |
|---|---|---|
| `README.md` | 1 | 1 |

Each line outside the campaign records (`prompts/`, `.prompts/`), 1:

```text
README.md:3: The pool lives in `RayTools/`.
```

## Test modules naming `RayTools` or `RayWorkPool` (1)

```text
tests/test_pool.py:6: self.assertEqual("RayWorkPool", "RayWorkPool")
```

## Files that do not parse (0)

None.
````

## 6. Every `path:line` the checklists cite, with the text read there

Printed by `$S/scripts/cite.py` from `git show <commit>:<path>` at each client's commit, at
DatastoreKit's `v0.2.1`, and at this repository's `eaef0ce` (a range of more than six lines shows
its first three and last two; a line over 150 characters is cut, marked `[…]`). The lines each
checklist's item 9 lists from the script's text search (SGK's `docs/`, CPBH's `.documents/`, SI's
`.claude/` and `.documents/`) are quoted whole in §4, with their text; the ones item 9 discusses are
also below. `venv/pyvenv.cfg` was read as text from each working tree: SGK `version = 3.12.15`;
CPBH `version = 3.13.16`; SI `version = 3.13.13`, `version_info = 3.13.13.final.0`,
`base-executable = /opt/local/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`.

````text
# SGK, at b510bc9

requirements.txt:74: ray==2.43.0
CLAUDE.md:69: The factories under `Datastore/SQL/ObjectFactories/` (other than `base.py`), `config/`, and every
    :70: caller of the layer are **not** frozen. They are this project's code, and change as usual. The
    :71: `RayTools/` files are not frozen either: they are not part of this extraction. SecondaryGWKit's
    :72: adoption will be a campaign in this repository, planned from DatastoreKit's adoption checklist;
    :73: the freeze ends when that campaign lands.
CLAUDE.md:106: - **Tests** live in `<package>/tests/` as `unittest` modules and run from the repository root:
    :107:   ```bash
    :108:   PYTHONPATH=. ./venv/bin/python -m unittest discover -s ComputeTargets/tests -t .
    :109:   ```
CLAUDE.md:114: - **`main.py` cannot be imported** — it parses `sys.argv`, opens a Ray connection and a
    :115:   `ShardedPool` at module scope, then runs the pipeline. To exercise it, use
    :116:   `docs/source-remediation-verification/scoped_pipeline_run.py`; to extract one of its functions
    :117:   for a test, use `ComputeTargets/tests/test_main_plumbing.load_main_py_functions`, which reads it
    :118:   with `ast` rather than executing it.
RayTools/RayWorkPool.py:8: from Datastore.SQL.ShardedPool import ShardedPool
RayTools/RayWorkPool.py:9: from utilities import format_time
RayTools/RayWorkPool.py:64: def _default_store_handler(obj, pool) -> None:
    :65:     obj.store()
    :66: 
    :67: 
    :68: def _default_persist_handler(obj, pool) -> ObjectRef:
    :69:     return pool.object_store(obj)
RayTools/RayWorkPool.py:75:         pool: ShardedPool,
RayTools/RayWorkPool.py:166:             print(f"\n** {title}")
RayTools/RayWorkPool.py:548:                     print(msg)
RayTools/RayWorkPool.py:566:             print(
main.py:63: from RayTools.RayWorkPool import RayWorkPool
extract_GkSource_data.py:37: from RayTools.RayWorkPool import RayWorkPool
extract_GkWKB_data.py:35: from RayTools.RayWorkPool import RayWorkPool
extract_Gk_data.py:32: from RayTools.RayWorkPool import RayWorkPool
extract_QuadSourceIntegral_data.py:42: from RayTools.RayWorkPool import RayWorkPool
extract_TkWKB_data.py:30: from RayTools.RayWorkPool import RayWorkPool
extract_tensor_source_data.py:31: from RayTools.RayWorkPool import RayWorkPool
main.py:297:     except RuntimeError as e:
main.py:505:     except RuntimeError:
main.py:520:     except RuntimeError:
main.py:1042:     source_k_exit_queue = RayWorkPool(
main.py:1057:     response_k_exit_queue = RayWorkPool(
main.py:1420:         Tk_numeric_queue = RayWorkPool(
main.py:1634:         Tk_WKB_queue = RayWorkPool(
main.py:1940:         QuadSource_queue = RayWorkPool(
main.py:2115:         Gk_numeric_queue = RayWorkPool(
main.py:2428:         Gk_WKB_queue = RayWorkPool(
main.py:2871:     def postprocess_GkSourcePolicy(obj: GkSourcePolicyData):
main.py:2874:         policy: GkSourcePolicy = obj.policy
main.py:2875:         policy_label = policy.label
main.py:2876:         key = policy_label if policy_label is not None else policy.store_id
main.py:2882:         type: str = obj.type
main.py:2883:         quality: str = obj.quality
main.py:2974:         query_queue = RayWorkPool(
main.py:3229:         GkSource_queue = RayWorkPool(
main.py:3247:         GkSourcePolicy_queue = RayWorkPool(
main.py:3265:         print("\n** GkSourcePolicyData SUMMARY STATISTICS")
main.py:4146:         QuadSourceIntegral_queue = RayWorkPool(
Datastore/SQL/ShardedPool.py:3328:     def object_store(self, objects):
Datastore/SQL/ShardedPool.py:3418:         return [self._shards[shard_id].object_store.remote(item)]
config/sharding.py:32:     "GkSourcePolicyData": "k",
Datastore/SQL/Datastore.py:598:     def object_store(self, objects, *, insert_timestamp: Optional[datetime] = None):
Datastore/SQL/Datastore.py:648:                             stored = factory.store(
Datastore/SQL/Datastore.py:658:                         output_objects.append(stored)
Datastore/SQL/Datastore.py:670:             return output_objects[0]
Datastore/SQL/ObjectFactories/GkSourcePolicyData.py:150:     def store(obj: GkSourcePolicyData, conn, table, inserter, tables, inserters):
    :151:         store_id = inserter(
    :152:             conn,
    …
    :173: 
    :174:         return obj
ComputeTargets/GkSourcePolicyData.py:519:         self._policy: GkSourcePolicy = policy
ComputeTargets/GkSourcePolicyData.py:574:         self._type = payload["type"]
    :575:         self._quality = payload["quality"]
ComputeTargets/GkSourcePolicyData.py:584:     @property
    :585:     def policy(self) -> GkSourcePolicy:
    :586:         return self._policy
    …
    :599: 
    :600:         return self._quality
RunRegistry/tests/test_pipeline_adoption.py:30: DRIVER = os.path.join(REPO_ROOT, "docs", "gktk-remedial", "scoped_pipeline_run.py")
RunRegistry/tests/test_pipeline_adoption.py:32: # Six lines in the vocabulary `RayWorkPool` prints, in the order it prints them: the banner from
    :33: # its constructor (:166), two progress notifications (:548) and the completion pair (:566). They
    :34: # are transcribed from `var/runs/a3-pilot/run.out`, the stdout of the 10 h 33 m A3 baseline run,
    …
    :43:       inflight: 0 lookup, 1 compute, 0 store | completed: 12 lookup, 12 compute, 12 store
    :44: """
RunRegistry/tests/test_pipeline_adoption.py:125:         self.assertTrue(tracker.feed("   -- ALL WORK ITEMS COMPLETE in time 4.3s"))
docs/gktk-remedial/scoped_pipeline_run.py:120: _STAGE_BANNER = re.compile(r"^\s*(?:\*\*|>>)\s+(\S.*?)\s*$")
    :121: _QUEUE_PROGRESS = re.compile(
    :122:     r"(\d+)/(\d+)\s+work items remaining\s*=\s*([\d.]+)%\s+complete"
    :123: )
    :124: _QUEUE_COMPLETE = re.compile(r"ALL WORK ITEMS COMPLETE")
docs/datastore-integrity-verification/qsi_resolution_cost.py:29: COMPLETE = re.compile(r"ALL WORK ITEMS COMPLETE in time (?:(\d+)m )?([\d.]+)s")
docs/datastore-integrity-verification/stage_counts.py:18: SUMMARY = re.compile(r"Queue summary: (.*)$")
ComputeTargets/tests/test_main_plumbing.py:445:             for call in ast.walk(node):
    :446:                 if not (
    :447:                     isinstance(call, ast.Call)
    :448:                     and isinstance(call.func, ast.Name)
    :449:                     and call.func.id == "RayWorkPool"
    :450:                 ):
ComputeTargets/tests/test_main_plumbing.py:733:             if not (
    :734:                 isinstance(node, ast.Call)
    :735:                 and isinstance(node.func, ast.Name)
    :736:                 and node.func.id == "RayWorkPool"
    :737:             ):
ComputeTargets/tests/test_quadsource_policy_main.py:142:             if not (
    :143:                 isinstance(node, ast.Call)
    :144:                 and isinstance(node.func, ast.Name)
    :145:                 and node.func.id == "RayWorkPool"
    :146:             ):
ComputeTargets/tests/test_wkb_numeric_parent_main.py:83:         if not (
    :84:             isinstance(node, ast.Call)
    :85:             and isinstance(node.func, ast.Name)
    :86:             and node.func.id == "RayWorkPool"
    :87:         ):
ComputeTargets/tests/test_wkb_numeric_parent_main.py:117:         if not (
    :118:             isinstance(node, ast.Call)
    :119:             and isinstance(node.func, ast.Name)
    :120:             and node.func.id == "RayWorkPool"
    :121:         ):
ComputeTargets/tests/test_gksource_parent_set_main.py:262: def _load_helper(pool):
    :263:     """main.py's own resolve_GkSource_parents, compiled from its source alone, its free names
    :264:     bound to stand-ins: the pool, the work pool, the run's model, tolerances, tags and grid.
    …
    :289:     exec(code, namespace)
    :290:     return namespace[HELPER]
ComputeTargets/tests/test_gksource_parent_set_main.py:270:         "RayWorkPool": _WorkPool,
ComputeTargets/tests/test_quadsource_integral_parent_main.py:782: def _load_helper(pool):
ComputeTargets/tests/test_quadsource_integral_parent_main.py:790:         "RayWorkPool": _WorkPool,
Datastore/tests/test_layer_is_generic.py:1: """
Datastore/tests/test_layer_is_generic.py:5: **What the layer is.** Every module under ``Datastore/`` but its tests and the client's factories,
    :6: with ``Datastore/SQL/ObjectFactories/base.py`` (the factory contract the layer imports), and every
    :7: module of ``RayTools/``. ``layer_files()`` derives the set from the filesystem, not from
Datastore/tests/test_layer_is_generic.py:70:     for path in (REPO_ROOT / "RayTools").glob("*.py"):
    :71:         found.add(path.relative_to(REPO_ROOT).as_posix())
Datastore/tests/test_layer_is_generic.py:88:     "RayTools/RayWorkPool.py",
Datastore/tests/test_layer_is_generic.py:120: _NOT_PROJECT_PACKAGES = {"Datastore", "RayTools", "config"}
Datastore/tests/test_layer_is_generic.py:182:     # WallclockTimer and format_time (Datastore, ProfileAgent, RayWorkPool): a shared helper that
Datastore/tests/test_layer_is_generic.py:192:     if root == "RayTools":
    :193:         return True
Datastore/tests/test_layer_is_generic.py:303:     def test_the_derived_files_hold_the_audits_list(self):
    :304:         self.assertLessEqual(AUDIT_LIST, set(self.files))
Datastore/tests/test_layer_is_generic.py:357:             "RayTools.RayWorkPool",
docs/tolerance-convergence/inventory.py:373: PRODUCTION_TREES = (
    :374:     "AdaptiveLevin",
    :375:     "ComputeTargets",
    …
    :385:     "utilities",
    :386: )
docs/tolerance-convergence/inventory.py:382:     "RayTools",
docs/tolerance-convergence/inventory.py:418:     for tree in PRODUCTION_TREES:
    :419:         root = REPO_ROOT / tree
    :420:         if not root.exists():
    :421:             continue
docs/tolerance-convergence/inventory.py:1350:         + ", ".join(f"`{t}`" for t in PRODUCTION_TREES)
docs/tolerance-convergence/TOLERANCE-INVENTORY.md:563: Every keyword argument named `amplitude_rtol`, `atol`, `deriv_rtol`, `epsabs`, `epsrel`, `phase_atol`, `rtol`, `xtol` whose value is a numeric literal […]
prompts/datastore-generic/orchestrator/measure-09/scripts/m3_make_mutations.py:33:         '    for path in (REPO_ROOT / "RayTools").glob("*.py"):\n        found.add(path.relative_to(REPO_ROOT).as_posix())\n',
docs/adoption/secondarygwkit.md:92: | `RayTools/` | 1 | 0 | `RayTools/RayWorkPool.py:8`, `ShardedPool`, a type hint |
docs/adoption/secondarygwkit.md:230:   `test_drop_refuses_dangling_references`, and `test_layer_is_generic`. The last imports the layer
    :231:   at module level, and its `layer_files()` (`Datastore/tests/test_layer_is_generic.py:60`) would
    :232:   find only `RayTools/` once the layer is gone; the package's own guard replaces it.
docs/adoption/secondarygwkit.md:704: | `RayTools/RayWorkPool.py:8` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
# CPBH, at 52142d7

requirements.txt:78: ray==2.53.0
CLAUDE.md:63:   ```bash
    :64:   PYTHONPATH=. ./venv/bin/python -m unittest discover -s CosmologyModels/tests -t .
    :65:   PYTHONPATH=. ./venv/bin/python -m unittest discover -s ComputeTargets/tests -t .
    :66:   PYTHONPATH=. ./venv/bin/python -m unittest discover -s Datastore/tests -t .
    :67:   ```
RayTools/RayWorkPool.py:23: from Datastore.SQL.ShardedPool import ShardedPool
RayTools/RayWorkPool.py:24: from utilities import format_time
RayTools/RayWorkPool.py:79: def _default_store_handler(obj, pool) -> ObjectRef:
    :80:     return pool.object_store(obj)
RayTools/RayWorkPool.py:86:         pool: ShardedPool,
RayTools/RayWorkPool.py:90:         store_handler=_default_store_handler,
RayTools/RayWorkPool.py:104:         if compute_handler is not None and store_handler is None:
    :105:             raise RuntimeError(
    :106:                 "If a compute maker is supplied, a store maker must also be supplied to serialize the result of the computation"
    :107:             )
RayTools/RayWorkPool.py:109:         if compute_handler is None and store_handler is not None:
    :110:             raise RuntimeWarning(
    :111:                 "No compute maker was supplied, but a store maker was provided. This will have no effect because there will be no compute results to s […]
    :112:             )
RayTools/RayWorkPool.py:106:                 "If a compute maker is supplied, a store maker must also be supplied to serialize the result of the computation"
RayTools/RayWorkPool.py:111:                 "No compute maker was supplied, but a store maker was provided. This will have no effect because there will be no compute results to s […]
RayTools/RayWorkPool.py:182:         if self._store_handler is not None:
RayTools/RayWorkPool.py:185:         if self._available_handler is not None:
RayTools/RayWorkPool.py:219:         if self._store_handler is not None:
RayTools/RayWorkPool.py:230:         if self._available_handler is not None:
RayTools/RayWorkPool.py:311:                     elif ref_data is None:
    :312:                         if self._store_results:
    :313:                             raise RuntimeError(
    :314:                                 "store_results=True is not compatible with returning None values from a task builder"
    :315:                             )
RayTools/RayWorkPool.py:436:                     obj.store()
RayTools/RayWorkPool.py:439:                     self._inflight.pop(ref.hex, None)
    :440:                     self._data.pop(ref.hex, None)
RayTools/RayWorkPool.py:446:                     store_task: ObjectRef = self._store_handler(obj, self._pool)
RayTools/RayWorkPool.py:449:                     self._inflight[store_task.hex] = store_task
    :450:                     self._data[store_task.hex] = ("store", payload)
RayTools/RayWorkPool.py:565:                     self._last_num_available_complete = self._num_store_complete
main.py:50: from RayTools.RayWorkPool import RayWorkPool
main.py:276:     solver_queue = RayWorkPool(
main.py:533:     adiabatic_queue = RayWorkPool(
main.py:820:     bbn_data_queue = RayWorkPool(
plot_ScalarModel.py:44: from RayTools.RayWorkPool import RayWorkPool
plot_ScalarModel.py:1556:     work_queue = RayWorkPool(
plot_by_beta.py:38: from RayTools.RayWorkPool import RayWorkPool
.documents/architecture-summary.md:35: ├── RayTools/
    :36: │   └── RayWorkPool.py               # Generic distributed work queue
.documents/architecture-summary.md:153: ### 3.2 `RayWorkPool` (`RayTools/RayWorkPool.py`)
.documents/architecture-summary.md:157: **Constructor parameters:**
.documents/architecture-summary.md:165: | `store_handler` | `Callable(obj, pool) → ObjectRef` | `pool.object_store(obj)` | Persists result |
.documents/architecture-summary.md:585: The `RayWorkPool` handles steps 3–4 automatically via its default `compute_handler` and `store_handler`.
.documents/architecture-summary.md:648: 5. Store sampled `SampleValues` in memory; `RayWorkPool` will later call `store()` and then `pool.object_store()`.
.documents/architecture-summary.md:920: query_queue = RayWorkPool(
    :921:     pool, query_batch,
    :922:     task_builder=lambda x: pool.object_get_vectorized("ScalarModel", x["shard_key"], x["payload"]),
    :923:     compute_handler=None, store_handler=None,
    :924:     store_results=True,
    :925: )
.documents/architecture-summary.md:999: - `RayWorkPool` (entire file)
.documents/architecture-summary.md:1086: work_pool = RayWorkPool(
    :1087:     pool,
    :1088:     work_batches,
    …
    :1093:     title="COMPUTE INSTANTON SOLUTIONS",
    :1094: )
.documents/integrator-audit-2026-09-30/README.md:69:   short). Only `ComputationFailureError` is caught (`:823`). `RayTools/RayWorkPool.py` calls
docs/adoption/champbh.md:93: | `ShardedPool` | 6 | `RayTools/RayWorkPool.py:23` (a type hint), `config/model_list.py:19`, `main.py:48`, `plot_ScalarModel.py:42`, `plot_by_beta.py: […]
docs/adoption/champbh.md:602: | `RayTools/RayWorkPool.py:23` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
# SI, at 7bb3efd

requirements.txt:57: ray==2.55.1
CLAUDE.md:21: Default test run: `pytest -m "not integration and not slow"` (~464 of 571
CLAUDE.md:89: ## Protected infrastructure
    :90: 
    :91: Never modify these files unless a prompt explicitly names them and describes
    …
    :108: Units/    MetadataConcepts/    utilities.py    constants.py
    :109: ```
CLAUDE.md:91: Never modify these files unless a prompt explicitly names them and describes
    :92: exactly what to change:
CLAUDE.md:95: RayTools/                          Datastore/SQL/ShardedPool.py
RayTools/RayWorkPool.py:23: from Datastore.SQL.ShardedPool import ShardedPool
RayTools/RayWorkPool.py:24: from utilities import format_time
RayTools/RayWorkPool.py:79: def _default_store_handler(obj, pool) -> None:
    :80:     obj.store()
RayTools/RayWorkPool.py:90:         pool: ShardedPool,
RayTools/RayWorkPool.py:109:         if compute_handler is not None and persist_handler is None:
    :110:             raise RuntimeError(
    :111:                 "If a compute handler is supplied, a persist handler must also be supplied to serialize the result of the computation"
    …
    :116:                 "No compute handler was supplied, but a persist handler was provided. This will have no effect because there will be no compute result […]
    :117:             )
RayTools/RayWorkPool.py:191:         if self._available_handler is not None:
RayTools/RayWorkPool.py:236:         if self._available_handler is not None:
RayTools/RayWorkPool.py:261:         while len(self._inflight) > 0 or len(self._todo) > 0:
RayTools/RayWorkPool.py:317:                     elif ref_data is None:
    :318:                         if self._store_results:
    :319:                             raise RuntimeError(
    :320:                                 "store_results=True is not compatible with returning None values from a task builder"
    :321:                             )
RayTools/RayWorkPool.py:575:                     self._last_num_available_complete = self._num_store_complete
main.py:45: from RayTools.RayWorkPool import RayWorkPool, _default_store_handler
main.py:61: MAX_INFLIGHT_PIPELINE = 50
main.py:79: MAX_INFLIGHT_PIPELINE_UNIFIED = MAX_INFLIGHT_PIPELINE // 3
main.py:383:     pipeline_queue = RayWorkPool(
main.py:396:         max_task_queue=MAX_INFLIGHT_PIPELINE_UNIFIED,
main.py:401: def _run_instanton_queue(
main.py:410:     store_handler,
main.py:492:     work_queue = RayWorkPool(
main.py:497:         store_handler=store_handler,
main.py:505:         max_task_queue=MAX_INFLIGHT_PIPELINE,
main.py:664:         store_handler=_default_store_handler,
main.py:670: def run_all_pipelines(
main.py:705:     traj_payloads = [
    :706:         dict(
    :707:             phi0=phi0,
    …
    :715:         for model_data in model_list
    :716:     ]
main.py:718:     traj_queue = RayWorkPool(
main.py:729:         create_batch_size=len(traj_payloads),
    :730:         process_batch_size=len(traj_payloads),
main.py:824:             store_handler=_default_store_handler,
main.py:848:             store_handler=_default_store_handler,
main.py:1092:             cf_work_queue = RayWorkPool(
main.py:1097:                 store_handler=_default_store_handler,
main.py:1107:                 max_task_queue=MAX_INFLIGHT_PIPELINE,
main.py:1153:     model_list = inputs["model_list"]
main.py:1211:     run_all_pipelines(
plot_GradientCoupledSolutions.py:100: from RayTools.RayWorkPool import RayWorkPool
plot_GradientCoupledSolutions.py:938:     work_queue = RayWorkPool(
plot_InstantonSolutions.py:72: from RayTools.RayWorkPool import RayWorkPool
plot_InstantonSolutions.py:1171:     work_queue = RayWorkPool(
config/pipeline_setup.py:114:     model_list = build_model_list(pool, units, args)
config/model_list.py:5: def build_model_list(pool, units, args):
config/model_list.py:20:         if len(args.m_values_Mp) > 0:
    :21:             m_sample = sorted(args.m_values_Mp)
config/model_list.py:23:             n = max(1, round(
    :24:                 args.samples_per_log10_m
    :25:                 * (args.log10_m_high_Mp - args.log10_m_low_Mp) + 0.5
    …
    :29:                             n, endpoint=True).tolist()
    :30:             )
config/model_list.py:67:         if len(args.lambda_values) > 0:
    :68:             lambda_sample = sorted(args.lambda_values)
config/model_list.py:70:             n = max(1, round(
    :71:                 args.samples_per_log10_lambda
    :72:                 * (args.log10_lambda_high - args.log10_lambda_low) + 0.5
    …
    :76:                             n, endpoint=True).tolist()
    :77:             )
config/model_list.py:112:     else:
    :113:         raise ValueError(f"Unknown potential type: {args.potential_type!r}")
.claude/rules/ray-dispatch.md:99: ## Why `RayWorkPool` requires plain classes
    :100: 
    :101: `RayTools/RayWorkPool.py` accesses compute targets as plain Python objects:
    …
    :105: - **Line 393:** `compute_task = compute_handler(obj)` — `compute()` must
    :106:   return an `ObjectRef`; `RayWorkPool` never calls `.remote()` on it
.claude/rules/datastore-factories.md:23: Note: `RayWorkPool` has three distinct handler slots — `store_handler` (calls
    :24: `obj.store()` on the compute target to resolve the Ray future and populate
    :25: `obj._values`), then `persist_handler` (calls `pool.object_store(obj)`, which
    :26: in turn calls this factory's `store()` method). The factory's `store()` is
    :27: invoked only from `persist_handler`, after `obj._values` is fully populated.
.documents/FILE_MAP.md:31: | `RayTools_RayWorkPool.py` | `RayTools/RayWorkPool.py` | `RayWorkPool` class: the core distributed work-queue abstraction; manages the **lookup → com […]
.documents/FILE_MAP.md:287: | `RayTools/` (other files)                               | Only `RayWorkPool.py` is directly relevant                                  |
.documents/INFRASTRUCTURE.md:351: ## 9. `RayWorkPool` — the distributed work-queue
    :352: 
    :353: `RayTools/RayWorkPool.py` drives every compute stage through five states:
    …
    :372:     title=None,
    :373: )
.documents/INFRASTRUCTURE.md:353: `RayTools/RayWorkPool.py` drives every compute stage through five states:
.documents/architecture-summary.md:27: RayTools/
    :28:   RayWorkPool.py               — distributed work-queue abstraction
.documents/architecture-summary.md:319: ## RayWorkPool
    :320: 
    :321: `RayTools/RayWorkPool.py` provides the main distributed work-queue abstraction.
    …
    :343:     title=None,                   # display name for progress reporting
    :344: )
.documents/architecture-summary.md:321: `RayTools/RayWorkPool.py` provides the main distributed work-queue abstraction.
.documents/gradient-coupled-instanton/24-prerequisite-wallclock-safeguard.md:75:   the Ray dispatch layer, and `RayTools/RayWorkPool.py` is protected
docs/adoption/stochasticinstantons.md:47:   `RayTools/`, `Datastore/object.py`, `Datastore/SQL/ClientPool.py`, `ShardedPool.py`,
docs/adoption/stochasticinstantons.md:105:     `plot_InstantonSolutions.py:42`, `RayTools/RayWorkPool.py:23` (a type hint),
docs/adoption/stochasticinstantons.md:578: | `RayTools/RayWorkPool.py:23` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
# The package, at eaef0ce

raypoolkit/RayWorkPool.py:75: def _default_compute_handler(obj, **kwargs) -> ObjectRef:
    :76:     return obj.compute(**kwargs)
    :77: 
    …
    :83: def _default_persist_handler(obj, pool) -> ObjectRef:
    :84:     return pool.object_store(obj)
raypoolkit/RayWorkPool.py:88:     def __init__(
raypoolkit/RayWorkPool.py:94:         store_handler=_default_store_handler,
raypoolkit/RayWorkPool.py:109:         if compute_handler is None:
    :110:             if store_handler is _default_store_handler:
    :111:                 store_handler = None
    :112:             if persist_handler is _default_persist_handler:
    :113:                 persist_handler = None
raypoolkit/RayWorkPool.py:109:         if compute_handler is None:
    :110:             if store_handler is _default_store_handler:
    :111:                 store_handler = None
    …
    :141:             if value < 1:
    :142:                 raise ValueError(f"{name} must be at least 1, not {value!r}")
raypoolkit/RayWorkPool.py:178:             self.results = [None for _ in range(self._num_total_items)]
raypoolkit/RayWorkPool.py:205:         if title is not None:
    :206:             print(f"\n** {title}")
raypoolkit/RayWorkPool.py:213:         if self._persist_handler is not None:
raypoolkit/RayWorkPool.py:216:         if self._available_handler is not None:
raypoolkit/RayWorkPool.py:250:         if self._persist_handler is not None:
raypoolkit/RayWorkPool.py:261:         if self._available_handler is not None:
raypoolkit/RayWorkPool.py:329:                     if ref_data is None:
    :330:                         if self._store_results:
    :331:                             raise RuntimeError(
    :332:                                 "a task builder returned None, which is not compatible with store_results=True"
    :333:                             )
raypoolkit/RayWorkPool.py:529:                     elif self._post_handler is not None:
    :530:                         replacement_obj = self._post_handler(replacement_obj)
raypoolkit/RayWorkPool.py:584:                     now = datetime.now()
    :585:                     msg = f"   -- {now:%Y-%m-%d %H:%M:%S%z} ({format_time(elapsed_since_start)} running): {len(self._todo)}/{self._num_total_items} wo […]
raypoolkit/RayWorkPool.py:588:                     print(msg)
raypoolkit/RayWorkPool.py:600:                     self._last_num_available_complete = self._num_available_complete
raypoolkit/RayWorkPool.py:606:             print(
raypoolkit/__init__.py:15: 
    :16: from raypoolkit.RayWorkPool import RayWorkPool
    :17: from raypoolkit.contract import DatastorePool
    :18: 
````

Also read at the commits, and cited for their dates and subjects: `git log -1` of each `HEAD`
(SGK `b510bc9` 2026-10-07 "Freeze the datastore layer while it moves to DatastoreKit"; CPBH
`52142d7` 2026-10-07 "Store each shard key under its own serial"; SI `7bb3efd` 2026-10-09 "Record
the R1 calculation review and open its issues board") and of each `RayTools/RayWorkPool.py` (SGK
`0ee16a8` 2026-09-04; CPBH `79fb527` 2026-01-25; SI `7cf4123` 2026-06-16); `git ls-tree` of each
`RayTools/` (the blobs of item 2; `__init__.py` `e69de29…` in all three); line counts by `git show
| wc -l` (575, 580, 590).

## 7. Every statement about the package, and how it was checked

| Statement (where) | Checked against `v0.2.0` |
|---|---|
| The pin `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0`; an editable install never for production (README §1; item 1 of each) | `README.md`, "Installing" |
| `requires-python = ">=3.12"`, `ray>=2.43`; tested 3.12.15 / 2.43.0 and 3.13.16 / 2.55.1; Ray's floor on 3.13 in effect 2.45.0 (README §1) | `pyproject.toml:9-11`; `README.md`, "Supported versions" |
| `from raypoolkit import RayWorkPool`; the attribute `raypoolkit.RayWorkPool` is the class; the module reachable by a `from` import and `import_module`; `RayWorkPool` and `DatastorePool` the public names (README §2) | `raypoolkit/__init__.py:16-18`; `PROVENANCE.md`, "New here"; probe from `$S` with `-I`: `raypoolkit.RayWorkPool` is a class, `from raypoolkit.RayWorkPool import _default_store_handler` works and is the module's, `__all__ == ['RayWorkPool', 'DatastorePool']` |
| `DatastorePool` is a `typing.Protocol` with `object_store`, a hint not checked at run time; no dependency on `datastorekit` (README §2) | `raypoolkit/contract.py`; `README.md`, "The constructor"; `importlib.metadata.requires` gives `['ray>=2.43']` |
| The defaults: compute `obj.compute(**kwargs)`, store `obj.store()`, persist `pool.object_store(obj)` (items 4, 5) | `raypoolkit/RayWorkPool.py:75-84`, `:93-95` |
| A pool with no compute handler needs only `compute_handler=None`; `store_handler=None`, `persist_handler=None` accepted; the default persist does not apply; `available_handler` and `post_handler` allowed (item 4 of each) | `:109-124`; `README.md`, "Which handlers a pool needs"; the fixture's lookup-only call constructs; `test_printed_lines`' spelling test (log 04 §3.4) |
| With a compute handler, `store_handler=None` or `persist_handler=None` raises `ValueError` (README §3; fixture) | `:126-134`; the fixture's `main.py:34` |
| A size below 1 raises `ValueError: <name> must be at least 1, not <value>` (SI item 4) | `:136-142`; the fixture's `main.py:41` |
| Constructing calls no Ray | every run's `ray.is_initialized()` after the verdicts: `False` |
| The post handler after a persist with no validation gets the persisted object (SGK item 5) | `:529-530` |
| `results` sized from the items, so a generator is accepted (item 5) | `:178`; board §4 |
| In-flight work keyed on `ref.hex()` (item 5) | `:300`, … (board §4's 26 lines) |
| The available rate from the available count (CPBH, SI item 5) | `:600` |
| The available segment printed only with an availability handler; the store segment with a persist handler (CPBH, SI item 5) | `:213`, `:216`, `:250`, `:261` |
| A task builder's `None` under `store_results=True`: `RuntimeError`, the package's message (CPBH, SI item 5) | `:329-333` |
| The constructor's messages say "handler" | `:123`, `:133`, `:142` |
| The printed lines are unchanged; each copy's `print()` calls are the package's (README §4; item 5 of each) | §3.8; `README.md`, "The printed lines are part of the interface"; decision U9 |
| The pool prints no UTC offset (SGK item 6) | `:584-585`: `datetime.now()` is naive, so `%z` is empty |
| The banner, a progress `print(msg)` and the completion `print(` are at `:206`, `:588`, `:606` (SGK item 6) | read at `eaef0ce` (§6) |
| Each verdict "constructs" (item 4 of each) | the script's, by the package's own constructor (§3.2, §4) |

## 8. The deliberate-breakage record (prompt §3.7)

Each diff is against the script as committed, made with `diff -u` from an edited copy in `$S/mk/`
and saved as `$S/diffs/<x>.diff`. For each: `bash $S/scripts/breakage.sh <x>` (the state, then
`git apply --check`, `git apply`, `git apply -R --check`), the runs below, then
`bash $S/scripts/revert.sh <x>` (`git apply -R`, the state again, `cmp` with the state before).
Every state, before and after every item, was:

```text
7f2851c062cd58967cd3b4da57083bd8b6e5e9393f083aefe314d4807b4ab5a7  docs/adoption/measure_client_pools.py
?? docs/adoption/measure_client_pools.py
```

(The four documents were written after the breakage; the script was the only new file then.) Every
`--check` printed "ok", and every revert ended "tree restored: state identical". The fixture runs
used `--repository $S/fixture --commit 58d2b67…`; the "committed run" is `$S/out/fixture.md` (§5).

**Summary.** (a) reports the label-builder call "constructs"; (b) misses the nested import; (c)
reports an uncommitted edit of the fixture, which the committed script does not; (d) gives the same
bytes on two runs, but changes the order of two tables against the committed run. **4 items, 4 fail
as §3.7 says.**

### (a) The verdict by a restated rule that forgets `label_builder`

```diff
--- a/docs/adoption/measure_client_pools.py
+++ b/docs/adoption/measure_client_pools.py
@@ -436,10 +436,18 @@
         kwargs["store_results"] = call["store_results_value"]
     for name in unknown_keywords:
         kwargs[name] = object()
-    try:
-        raypoolkit.RayWorkPool(**kwargs)
-    except Exception as error:  # the verdict is whatever the constructor raises
-        return f"{type(error).__name__}: {error}"
+    # a restated rule in place of the constructor
+    if kwargs.get("compute_handler", "default") is None:
+        for name in ("store_handler", "persist_handler", "validation_handler"):
+            if kwargs.get(name) is not None:
+                return f"ValueError: No compute handler was supplied, so {name} would never be called; leave it out, or pass None"
+    else:
+        for name in ("store_handler", "persist_handler"):
+            if name in kwargs and kwargs[name] is None:
+                return f"ValueError: A compute handler was supplied, so {name} must not be None; leave it out to use the default"
+    for name in ("create_batch_size", "process_batch_size", "max_task_queue"):
+        if kwargs.get(name, 1) < 1:
+            return f"ValueError: {name} must be at least 1, not {kwargs[name]!r}"
     return "constructs"
 
 
```

The fixture, against the committed run:

```text
32c32
< | Verdicts | `ValueError: A compute handler was supplied, so store_handler must not be None; leave it out to use the default` 1; `ValueError: No compute handler was supplied, so label_builder would never be called; leave it out, or pass None` 1; `ValueError: create_batch_size must be at least 1, not 0` 1; `constructs` 2 |
---
> | Verdicts | `ValueError: A compute handler was supplied, so store_handler must not be None; leave it out to use the default` 1; `ValueError: create_batch_size must be at least 1, not 0` 1; `constructs` 3 |
74c74
< | `main.py:27` | `run` | 2 | — | None | — | — | — | — | — | set | — | — | — | `ValueError: No compute handler was supplied, so label_builder would never be called; leave it out, or pass None` |
---
> | `main.py:27` | `run` | 2 | — | None | — | — | — | — | — | set | — | — | — | `constructs` |
```

`main.py:27` (`compute_handler=None, label_builder=f`) reports `constructs`, and the verdicts total
3 "constructs" for 2.

### (b) Nested imports not walked

```diff
--- a/docs/adoption/measure_client_pools.py
+++ b/docs/adoption/measure_client_pools.py
@@ -258,7 +258,7 @@
 
     def visit_ImportFrom(self, node):
         module = node.module or ""
-        if node.level == 0 and names_a_pool_module(module):
+        if node.level == 0 and names_a_pool_module(module) and not self.scope:
             names = [alias.name for alias in node.names]
             self.imports.append(
                 {
```

```text
20,21c20,21
< | Imports of a `RayTools` module | 2 (module level 1, nested 1) |
< | … naming a private name | 2 |
---
> | Imports of a `RayTools` module | 1 (module level 1, nested 0) |
> | … naming a private name | 1 |
48c48
< ## Imports of a `RayTools` module (2)
---
> ## Imports of a `RayTools` module (1)
53d52
< | `main.py:13` | `run` | `from RayTools.RayWorkPool import RayWorkPool, _private` | `_private` |
```

The nested import at `main.py:13` is missed: 1 import, 0 nested.

### (c) The working tree read in place of `git show`

```diff
--- a/docs/adoption/measure_client_pools.py
+++ b/docs/adoption/measure_client_pools.py
@@ -183,7 +183,8 @@
 
 
 def show(repository, commit, path):
-    return git(repository, "show", f"{commit}:{path}")
+    with open(f"{repository}/{path}", "rb") as handle:
+        return handle.read()
 
 
 # --- the parts of a file ---------------------------------------------------------------------------
```

1. On the clean fixture the output equals the committed run (`cmp`).
2. An uncommitted edit, appended to the fixture's `main.py` (SHA-256 before
   `d1d2436b…aeac7e1`; `git -C $S/fixture status --porcelain` then ` M main.py`):
   ```python


   def extra(pool, items):
       return RayWorkPool(pool, items, task_builder=f, process_batch_size=0)
   ```
   The output changes against the committed run (below).
3. After the revert, with the edit still in place, the committed script's output equals the
   committed run (`cmp`): it reads `58d2b67`, not the working tree.
4. The edit was removed by copying back the saved `main.py`: SHA-256 `d1d2436b…aeac7e1` again,
   `git -C $S/fixture status --porcelain` empty.

Step 2's output against the committed run: a sixth call, `main.py:57`, with its `ValueError`.

```text
24c24
< | `RayWorkPool(...)` calls | 5 |
---
> | `RayWorkPool(...)` calls | 6 |
27c27
< | … compute handler left at its default | 2 |
---
> | … compute handler left at its default | 3 |
30c30
< | … positional arguments | 2 at 5 |
---
> | … positional arguments | 2 at 6 |
32c32
< | Verdicts | `ValueError: A compute handler was supplied, so store_handler must not be None; leave it out to use the default` 1; `ValueError: No compute handler was supplied, so label_builder would never be called; leave it out, or pass None` 1; `ValueError: create_batch_size must be at least 1, not 0` 1; `constructs` 2 |
---
> | Verdicts | `ValueError: A compute handler was supplied, so store_handler must not be None; leave it out to use the default` 1; `ValueError: No compute handler was supplied, so label_builder would never be called; leave it out, or pass None` 1; `ValueError: create_batch_size must be at least 1, not 0` 1; `ValueError: process_batch_size must be at least 1, not 0` 1; `constructs` 2 |
45c45
< | — | — | — | — | — | — | — | 2 |
---
> | — | — | — | — | — | — | — | 3 |
67c67
< ## `RayWorkPool(...)` calls (5)
---
> ## `RayWorkPool(...)` calls (6)
77a78
> | `main.py:57` | `extra` | 2 | — | — | — | — | — | — | — | — | `process_batch_size=0` | — | — | `ValueError: process_batch_size must be at least 1, not 0` |
79c80
< ## Calls with a compute path: the handlers given (3)
---
> ## Calls with a compute path: the handlers given (4)
87a89
> | `main.py:57` | — | — | — | — | — | — | — |
```

### (d) The sort removed

```diff
--- a/docs/adoption/measure_client_pools.py
+++ b/docs/adoption/measure_client_pools.py
@@ -179,7 +179,7 @@
         if kind != b"blob" or mode == b"120000":
             continue
         blobs.append((path.decode("utf-8", "surrogateescape"), blob.decode()))
-    return sorted(blobs)
+    return blobs
 
 
 def show(repository, commit, path):
@@ -509,10 +509,6 @@
         report["dynamic_imports"].extend(walker.dynamic)
         report["calls"].extend(walker.calls)
 
-    position = lambda entry: (entry["path"], entry["line"])
-    for key in ("imports", "literals", "dynamic_imports", "calls", "text_lines"):
-        report[key].sort(key=position)
-    report["test_modules"].sort(key=lambda entry: entry["path"])
     report["ray_initialized_after"] = ray.is_initialized()
     report["totals"] = totals(report)
     return report
@@ -555,16 +551,16 @@
             str(k): v
             for k, v in sorted(Counter(c["positional"] for c in calls).items())
         },
-        "verdicts": dict(sorted(Counter(c["verdict"] for c in calls).items())),
+        "verdicts": dict(Counter(c["verdict"] for c in calls).items()),
         "calls_flagged": sum(1 for c in calls if c["flags"]),
         "flags": sum(len(c["flags"]) for c in calls),
         "handler_spellings": [
             {"handlers": dict(zip(HANDLERS, key)), "calls": count}
-            for key, count in sorted(spellings.items())
+            for key, count in spellings.items()
         ],
         "text_lines": len(report["text_lines"]),
-        "text_lines_by_group": dict(sorted(groups.items())),
-        "text_files_by_group": dict(sorted(group_files.items())),
+        "text_lines_by_group": dict(groups.items()),
+        "text_files_by_group": dict(group_files.items()),
         "test_modules": len(report["test_modules"]),
     }
 
```

Two runs each, of the fixture and of SI: each pair `cmp` identical, since `git ls-tree`'s order
and the walk are deterministic. Against the committed runs the order changes: the verdicts and the
spelling table come in order of first appearance, not sorted.

The fixture:

```text
32c32
< | Verdicts | `ValueError: A compute handler was supplied, so store_handler must not be None; leave it out to use the default` 1; `ValueError: No compute handler was supplied, so label_builder would never be called; leave it out, or pass None` 1; `ValueError: create_batch_size must be at least 1, not 0` 1; `constructs` 2 |
---
> | Verdicts | `constructs` 2; `ValueError: No compute handler was supplied, so label_builder would never be called; leave it out, or pass None` 1; `ValueError: A compute handler was supplied, so store_handler must not be None; leave it out to use the default` 1; `ValueError: create_batch_size must be at least 1, not 0` 1 |
45d44
< | — | — | — | — | — | — | — | 2 |
46a46
> | — | — | — | — | — | — | — | 2 |
```

SI (`$S/final/si-1.md` against `$S/out/si-d1.md`):

```text
43d42
< | None | None | None | None | None | None | None | 2 |
45a45
> | None | None | None | None | None | None | None | 2 |
```

## 9. Observations not acted on

1. **The campaign plan's G2 says "including the six pinned lines"** (README §7). What
   `test_pipeline_adoption.py` pins is the five-line `A3_OUTPUT` block (deviation 6); SGK's
   checklist (item 8) says so. The plan is not in §6's list. No issue: it is the plan's wording,
   and the board's G2 row now points at the checklist.
2. **The prompt's §0.2 "Titled" row and the brief's clarification 2** count the keyword
   (deviation 15). Recorded; the checklists and the script say what is there.
3. **`test_layer_is_generic.py:357`** would keep passing after `RayTools/` is deleted only because
   `:192-193` still allows the name; it would then test an allowance for a package that is gone.
   SGK's checklist advises removing the entries together.
4. **SI's `.claude/rules/ray-dispatch.md:103-105`** cite the copy's lines 354, 436 and 393. Whether
   they were right at `7bb3efd` was not checked: they go with the file either way.
5. **The script reads one blob per `git show`** (§2.1's two commands), about 40 s on SGK's 1,432
   files. `git cat-file --batch` would be faster; it is not one of the prompt's commands.
6. **CPBH's remote is named `github`** (`https://ds283@github.com/ds283/ChamPBH`), not `origin`
   (seen through `git remote -v`, deviation 25). Nothing here depends on it.
7. **SGK's `main.py:3247` was settled by reading** (deviation 9); its checklist says how SGK's
   campaign could measure it.

## 10. Issues

**Opened:** none. **Closed:** none. **Narrowed:** none. `docs/OPEN_ISSUES.md` stays at **0** open,
unchanged.

## 11. State handed to the next prompt

- `HEAD` is `67f3f7e`. `raypoolkit/` is unchanged since `0b6ffd2` (`git diff eaef0ce --
  raypoolkit` empty); `pyproject.toml`, `README.md` and `PROVENANCE.md` are `v0.2.0`'s.
- **Suite: 121 tests**, passing in `venv/` (3.12.15 / 2.43.0).
- **`docs/adoption/`**: the README, the three checklists and `measure_client_pools.py`, which 07
  cites. Its figures at `b510bc9`, `52142d7` and `7bb3efd` are §3.2's.
- The board's gates G2–G4 point at the checklists; none holds yet.
- No tag was made and nothing was pushed. Local `main` is ahead of `origin/main` (`b2b6ab4`) by
  `a1d64ea`, `deffdc2` and `67f3f7e`.
- The drivers, the fixture and the outputs (`$S/`) are not committed; every diff they applied is in
  §8, exactly as applied.
