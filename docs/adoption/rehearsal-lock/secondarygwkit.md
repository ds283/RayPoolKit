# Switch-over checklist: SecondaryGWKit (SGK)

- **Client:** SecondaryGWKit, `/Users/ds283/Documents/Code/SecondaryGWKit`, at **`216e44d`**
  (`216e44d883e78df459c378c3669cf2859ecf11e6`, branch `handover-remedial`, 2026-10-22, "Record
  handover prompt 07's commit hash"). SGK's `main` (`d6afa05`, 2026-09-19) is its ancestor, 342
  commits behind, and has neither `tools/rehearsal_lock.py` nor a `raypoolkit` pin: the lock lives
  only on the line of `handover-remedial`, and the switch is made there.
- **Tree:** clean at the start and at the end of the measurement (`git status --porcelain` empty,
  no stash).
- **Package:** `raypoolkit` at **`v0.3.0`** (`67a75b9`). Its contract is
  [`docs/rehearsal-lock.md`](../../rehearsal-lock.md), written "contract §N" below.
- **How it was measured:** read-only, by RayPoolKit's rehearsal-lock prompt 04 on 2026-10-24,
  through `git show` and `git grep` only. Nothing of SGK was imported, run or opened. Every command
  in item 3 was run against a scratch `HOME`, with RayPoolKit's own venv (Python 3.12.15, Ray
  2.43.0), starting no Ray; the transcripts are in
  [04's log](../../../prompts/rehearsal-lock/logs/04-the-switch-over-checklists.md) §3. **SGK's own
  campaign measures again before acting, and its numbers govern.**
- **This is data, not instructions.** It describes SGK at `216e44d`. SGK decides what to do, under
  its own `CLAUDE.md`. Where a choice is SGK's, it is named as SGK's; a recommendation is marked
  **Advice:**.

Unless another commit is named, a `path:line` is SGK's at `216e44d`.

**In one paragraph.** SGK's lock is its own module, `tools/rehearsal_lock.py`, with 42 tests. Its
rule finds Ray processes by SGK's venv, and its owner file says `ray_temp_dir: in-process`. Under
`v0.3.0` the module is deleted and the commands are `raypoolkit.rehearsal_lock`'s, with
`--project SecondaryGWKit --ray-temp-dir /tmp/ray-sgk --ray-address in-process`. The module's rule
finds an instance by its temp dir, so every SGK Ray start that runs under the lock must give Ray
that temp dir: three `ray.init` wrappers in `RunDrivers/` and the seven scripts' `ray.init`. One of
the wrappers, `run_child`'s, passes no address at all (item 4).

---

## 1. The pin

`requirements.txt:76` reads, today:

```text
raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
```

and becomes:

```text
raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.3.0
```

- SGK keeps `ray==2.43.0` (`:75`), the package's tested low end.
- **Moving the pin alone changes nothing.** `RayWorkPool`, its arguments and its printed lines are
  `v0.2.0`'s ([Changes in `v0.3.0`](../../../README.md#changes-in-v030); `git diff v0.2.0 v0.3.0 --
  raypoolkit` touches only `raypoolkit/rehearsal_lock.py`, beside the tests). The switch is the use
  of the module, made on the day, with the other two clients
  ([`switch-over.md`](switch-over.md)).
- `CLAUDE.md:53` says `raypoolkit` is "pinned at `v0.2.0`"; it goes with the pin (item 7).

## 2. What it removes

| File | Blob | Lines | Last changed |
|---|---|---|---|
| `tools/rehearsal_lock.py` | `ea1433664ff44576102a1d07a9a797650681dc2e` | 475 | `c863055`, 2026-10-12, "Add a helper for the shared rehearsal lock" |
| `tools/tests/test_rehearsal_lock.py` | `cdeecd60005c6c7939c7dab5d73e3f1b80803e69` | 474, **42 tests** | `a5a6f6d`, 2026-10-12 |

- The module is the whole of SGK's lock: the location (`default_lock_dir`, `:66-68`), the owner
  file with `project` fixed as `SecondaryGWKit` and `ray_temp_dir` and `ray_address` both
  `in-process` (`:49-50`, `owner_text` `:92-107`), the venv rule (`venv_roots` `:184-189`,
  `ray_processes` `:192-246`), the five commands and the parser (`:265-471`).
- Nothing else imports it: `git grep` finds `tools.rehearsal_lock` outside `tools/` only in
  `CLAUDE.md` (item 7) and in records under `docs/` and `prompts/`. `tools/__init__.py`,
  `tools/inventory_report.py` and the other `tools/tests/` modules stay.

## 3. What replaces it

The commands, with SGK's values, run from the repository root. No `PYTHONPATH=.` is needed: the
module is installed from the pin.

```bash
./venv/bin/python -m raypoolkit.rehearsal_lock acquire --project SecondaryGWKit --purpose "<text>" --ray-temp-dir /tmp/ray-sgk --ray-address in-process
./venv/bin/python -m raypoolkit.rehearsal_lock set-pid --project SecondaryGWKit --ray-temp-dir /tmp/ray-sgk <pid>
./venv/bin/python -m raypoolkit.rehearsal_lock release --project SecondaryGWKit --ray-temp-dir /tmp/ray-sgk
./venv/bin/python -m raypoolkit.rehearsal_lock status --ray-temp-dir /tmp/ray-sgk --ray-address in-process
./venv/bin/python -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-sgk
```

What each exit code means for SGK (contract §7), against SGK's helper today:

| Command | Exit | Meaning under `v0.3.0` | SGK's helper today |
|---|---|---|---|
| `acquire` | 0 | the lock is SGK's now, `pid: -` | the same |
| | 3 | the lock is held (anyone's, SGK's included), **or the old location `~/ScienceData/.rehearsal-lock` exists**; nothing created. Stop and ask the user | held |
| | 4 | a process of `/tmp/ray-sgk` is alive, or `ps` cannot be read; the lock released again | a Ray process under SGK's venv is alive |
| | 1 | the owner file could not be written; the lock removed | the same |
| `set-pid` | 0 / 1 | recorded / refused: the pid not alive, no lock, no owner file, not SGK's lock (`project` and `ray_temp_dir` both compared), or not one `pid:` line | the same, with `ray_temp_dir: in-process` compared |
| `release` | 0 | released, or no lock | the same |
| | 1 | refused: no owner file, not SGK's, the recorded pid alive, or a process of `/tmp/ray-sgk` alive, or `ps` unreadable | the same, by the venv rule |
| `status` | 0 | always; the layout of contract §8 (item 5) | always |
| `ray-processes` | 0 / 1 | none / some (or `ps` unreadable), the processes of `/tmp/ray-sgk` | the processes under SGK's venv |
| any | 2 | a usage error, a value breaking contract §4: `--ray-address local` is one (`in-process` is the value), and so is `--ray-temp-dir in-process` | usage errors |

- **The owner file** SGK's `acquire` writes (contract §4): `project: SecondaryGWKit`, `purpose:
  <text>`, `acquired`, `host`, `ray_temp_dir: /tmp/ray-sgk`, `ray_address: in-process`, `pid: -`.
  `set-pid` then rewrites the `pid:` line alone.
- **The pid** is the driver's, recorded once Ray is up (contract §6), as SGK's protocol already
  does from the run's `status.json` (`prompts/runregistry-extraction/README.md:447-450`). For the
  sweep, whose driver is a new child per tolerance pair (item 4), the run's pid is the parent's,
  which outlives every child. **Advice:** record the parent's.
- **The temp dir.** **Advice:** `/tmp/ray-sgk` (decision U2). On this machine on 2026-10-24 it did
  not exist (nor `/private/tmp/ray-sgk`), no process's command named it, and no line of SGK, ChamPBH
  or StochasticInstantons at the commits measured names it (04's log §3.5). It is 12 bytes, so
  Ray's socket paths under it stay well inside macOS's 104 (contract §6); it does not start with
  `//`, and pid 1 (`launchd`) does not name it. Spell it `/tmp/ray-sgk` every time: the lock
  compares the strings as given (contract §5). Where SGK keeps the value (one constant, read by the
  wrappers and the scripts of item 4) is SGK's choice.

Each command above was run, with these values, against a scratch `HOME` (04's log §3.3, script
`sgk.sh`): `acquire` 0, a second `acquire` 3, `set-pid` with a live pid 0, `release` while it lived
1, `release` once it was reaped 0, `release` with no lock 0, `set-pid` with no lock 1,
`ray-processes` 0, and `--ray-address local` and `--ray-temp-dir in-process` each 2.

## 4. Its Ray starts

Every place SGK starts Ray, found by

```bash
git -C SecondaryGWKit grep -n -E 'ray\.init\(|_real_ray_init\(' 216e44d -- ':!docs' ':!prompts'
```

which finds the three wrappers' calls (`RunDrivers/quadsource_atol_sweep.py:487`, `:629`;
`RunDrivers/scoped_pipeline_run.py:709`), the seven scripts' `ray.init` (below), a docstring line
(`RunDrivers/scoped_pipeline_run.py:24`) and a test's label (`tools/tests/test_inventory_consumers.py:215`).
No test module starts Ray (item 5).

**What `_temp_dir` does** (read in Ray's source at 2.43.0 and 2.55.1; 04's log §3.4). `ray.init`
takes it as `kwargs.pop("_temp_dir", None)` (`ray/_private/worker.py:1487` at 2.43.0, `:1645` at
2.55.1): a private keyword, stable over that range, and `_temp_dir=None` is the same as not passing
it. Then:
- with `address="local"`, Ray starts a new instance with that temp dir, ignoring `RAY_ADDRESS`
  (`services.canonicalize_bootstrap_address`, `services.py:549` / `:688`). This is the form the
  contract asks for (§6);
- with `address=None`, Ray first takes `RAY_ADDRESS`, then the address in
  `<_temp_dir>/ray_current_cluster` (`/tmp/ray/ray_current_cluster` with no temp dir), and connects
  there if it finds one; it starts a new instance only if it finds none (`services.py:389-435` /
  `:408-454`). Only `ray start` writes that file, at the end of its `start` command
  (`ray/scripts/scripts.py:1072` / `:1153`);
- with `auto`, the address is looked up in `<_temp_dir>/ray_current_cluster` in place of
  `/tmp/ray/…`, so the temp dir changes which cluster is found;
- with a `host:port`, the driver connects as a node of its own with the temp dir given
  (`worker.py:1791` / `:1960`), which it takes in place of the head's (`node.py:442-462` /
  `:533-547`): the driver's files split from the cluster's.

So SGK passes `_temp_dir` only with `local` (decision U2's caveat).

| # | Start | Today | Under the lock | What it needs |
|---|---|---|---|---|
| 1 | `run_build`'s wrapper, `RunDrivers/quadsource_atol_sweep.py:624-636` (the call `:629-634`) | `_real_ray_init(address="local", num_cpus=…, include_dashboard=False, ignore_reinit_error=True)` | yes: `--build`, A3 v2 and its rehearsals (`prompts/runregistry-extraction/README.md:458-461`) | `_temp_dir=<dir>` in the call |
| 2 | `scoped_pipeline_run.main`'s wrapper, `RunDrivers/scoped_pipeline_run.py:704-716` (the call `:709-714`) | the same | when it runs a rehearsal or long build (`CLAUDE.md:155`) | the same |
| 3 | **`run_child`'s wrapper**, `RunDrivers/quadsource_atol_sweep.py:482-491` (the call `:487-489`) | `_real_ray_init(num_cpus=…, include_dashboard=False, ignore_reinit_error=True)`: **no address** | when the sweep runs as a long build: one child per tolerance pair, launched by `sweep` (`:949-965`), a pair taking up to an hour (`:906-910`) | `_temp_dir=<dir>` in the wrapper, and an address (below) |
| 4 | `main.py:314` | `ray.init(address=args.ray_address)`, `--ray-address` defaulting to `DEFAULT_RAY_ADDRESS = "local"` (`:99`, `:251-260`) | when run directly as a long build. Under the three drivers its call reaches the wrapper, which ignores its arguments (`_local_ray_init(*_a, **_kw)`, `:482`, `:624`; `scoped_pipeline_run.py:704`) | `_temp_dir=<dir>` only when `args.ray_address == "local"`; under a driver, nothing: the wrapper carries it |
| 5–10 | the six readers: `extract_GkSource_data.py:118`, `extract_GkWKB_data.py:110`, `extract_Gk_data.py:109`, `extract_QuadSourceIntegral_data.py:130`, `extract_TkWKB_data.py:106`, `extract_tensor_source_data.py:110` | `ray.init(address=args.ray_address)`, default `"local"` (e.g. `extract_Gk_data.py:86-87`) | yes: the rehearsal protocol holds the lock through the readers (`prompts/runregistry-extraction/README.md:445-446`), run with `--ray-address local` | as `main.py` |

**`run_child` (row 3)** passes no address, so adding `_temp_dir` alone changes which file Ray reads:
- **`_temp_dir` alone**: Ray takes `RAY_ADDRESS` if it is set, and connects there with the temp dir
  given (the `host:port` case above). Otherwise it reads `/tmp/ray-sgk/ray_current_cluster`, which
  nothing writes unless a `ray start --temp-dir /tmp/ray-sgk` is run, and starts a new
  instance;
- **`address="local"` with `_temp_dir`**: always a new instance, `RAY_ADDRESS` ignored, as the
  other two wrappers do today.

**Advice:** `address="local"` with `_temp_dir`. It is the form of contract §6, it is what rows 1
and 2 already do, and it removes the one case in which `_temp_dir` would meet a cluster address.

**The forms that keep SGK's tests passing** (item 6), each checked against the tests' own
predicates on written-out sources (04's log §3.6):

| Form | `test_ray_address_default` | `test_inventory_consumers` (`main.py`) |
|---|---|---|
| `ray.init(address=args.ray_address, _temp_dir=SGK_RAY_TEMP_DIR if args.ray_address == "local" else None)` | passes | passes |
| the same with the path as a literal | passes | passes |
| `ray.init(address=args.ray_address, **temp_dir_kwargs(args.ray_address))` | passes | passes |
| `if`/`else` with two `ray.init` calls | **fails** (one call per script) | **fails** |
| `context = ray.init(…)` | passes | **fails** (`ray.init` must be an expression statement) |
| the address positional | **fails** | passes |

| Wrapper form | `test_killed_handler` (rows 1, 2) | `test_build_rehearsal_scope` (row 3) |
|---|---|---|
| `_real_ray_init(address="local", _temp_dir=SGK_RAY_TEMP_DIR, …)` | passes | passes |
| row 3 with `_temp_dir` and no address | not applied to `run_child` | passes |
| row 3 with a comment naming "rehearsal" | — | passes (`ast.unparse` drops comments) |
| row 3 with a name or string containing `rehearsal` in lower case (`rehearsal_temp_dir`, a message "under the rehearsal lock") | — | **fails** |
| row 3 with `REHEARSAL_TEMP_DIR` | — | passes (the test's match is case-sensitive) |

`SGK_RAY_TEMP_DIR` stands for wherever SGK keeps the value; the names are SGK's.

## 5. What it must now do differently

- **The rule finds the instance by its temp dir, not by SGK's venv** (contract §6; SGK's rule is
  `venv_roots` and `ray_processes`, `tools/rehearsal_lock.py:184-246`). An SGK Ray process started
  without `/tmp/ray-sgk` is not seen by `acquire`, `release`, `status` or `ray-processes`:
  - **an instance from before the switch**, still running or left behind. `switch-over.md` §2 asks
    for no Ray process at the start of the day;
  - **a driver run with `--ray-address auto` or a `host:port`**: it attaches to another instance,
    and names no temp dir of SGK's. `CLAUDE.md:159-160` already forbids `auto`;
  - **a start item 4 misses**, now or later. Item 8's grep and SGK's tests are the guard.
- **The hard-kill route** (`CLAUDE.md:137-142`) checks for a `SIGKILL`ed driver's GCS server. It
  becomes `./venv/bin/python -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir
  /tmp/ray-sgk`, and finds that server only if its driver started the instance with
  `/tmp/ray-sgk`: `gcs_server` names the temp dir (it is a seed at both tested ends, 02's log §3.4).
  For a driver started before the switch the old check is gone with the module, which is one more
  reason for `switch-over.md` §2's precondition.
- **What the venv rule saw that the temp-dir rule does not.** The venv rule listed every Ray
  process under SGK's venv, an unrelated run's included. In SGK's tests that loses nothing: no test
  module starts Ray. `git grep -n -E 'ray\.init\(' 216e44d -- '*tests*'` finds only text and `ast`
  predicates; `tools/tests/test_inventory_consumers.py:48-60` runs `main.py` with `ray.init`
  replaced by a function that raises, and modules end by asserting that Ray was not initialised
  (e.g. `ComputeTargets/tests/test_ray_address_default.py:49-51`).
- **The commands run as the command line, never through the Python API inside a Ray driver**
  (contract §2, §6): a driver sees nothing of its own instance that way. SGK's drivers do not call
  the lock today.
- **No command line that runs the lock's commands names the temp dir, other than the lock command
  itself** (contract §6). A shell whose command line names `/tmp/ray-sgk` (an agent's shell
  command, for instance) is an ancestor of the lock command and seeds the walk, so every other
  process it started is listed: a driver launched from it makes `acquire` exit 4 and `release` exit
  1. **Advice:** run each lock command in a shell command of its own, never in the one that launches
  a build. A `--purpose` naming the temp dir is harmless here (it is the lock command's own
  argument), but there is no reason for one.
- **`status`'s layout is the module's** (contract §8). Against SGK's: the lock's path is
  `~/.raypoolkit/rehearsal-lock`; the process line reads `Ray processes of /tmp/ray-sgk: …` in place
  of `Ray processes of this repository: …`; an `old location: PRESENT (…)` line appears while the
  old location exists. With no `--ray-temp-dir` and no lock, `status` prints `Ray processes: no temp
  dir given` (04's log §3.3), so pass the temp dir to see SGK's processes. Nothing live in SGK reads
  these lines: `git grep` finds them only in `tools/` and its tests, and in records (item 7).
- **The old location** (contract §9): `acquire` refuses with 3 while `~/ScienceData/.rehearsal-lock`
  exists, printing its owner file. The module's `release` does not look there, so an old SGK lock
  is released with SGK's helper before the switch, or removed by the user by hand.
- **The readers record no pid** (`prompts/runregistry-extraction/README.md:447-448`, "The readers
  leave it alone"). Under the module the rule alone then covers them, and it does not list a
  driver's process reaper (contract §6), which was measured to exit at `ray.shutdown()`. SGK may
  `set-pid` each reader as it starts, or leave it so.
- **The in-process dashboard.** SGK pins the `ray[default]` set (`grpcio`, `aiohttp`, `opencensus`;
  `requirements.txt:2`, `:26`, `:52`), so each in-process instance starts a headless dashboard on
  port 8265 even with `include_dashboard=False` (02's log §5; contract §10). The lock checks no
  port; it is not the lock's to check, and the switch does not change it.

## 6. Its tests

| Test | What it pins | Under the switch |
|---|---|---|
| `tools/tests/test_rehearsal_lock.py` (42 tests, imports `from tools import rehearsal_lock as rl`, `:26`) | SGK's helper | **deleted** with it (item 2). The `tools/tests` root (`CLAUDE.md:175`) falls by 42: by `def test_` count, 91 → 49 (`test_inventory_consumers` 11, `test_inventory_report` 19, `test_inventory_report_labels` 19). SGK's rules treat a falling count as a stop unless explained; this is the explanation |
| `ComputeTargets/tests/test_ray_address_default.py:138-145` | each of the seven scripts has exactly one `ray.init` (`:95-104`), with no positional argument, and an `address` that unparses to `args.ray_address`; it says nothing of other keywords | passes with the forms of item 4; fails with two calls or a positional address |
| `ComputeTargets/tests/test_ray_address_default.py:153-162` | Ray resolves `local` to a new instance and `auto` to `RAY_ADDRESS` | unchanged: it calls `canonicalize_bootstrap_address` with no temp dir |
| `tools/tests/test_inventory_consumers.py:199-219` | `main.py`'s `ray.init` is a top-level expression statement, after `if args.inventory:` | passes unless the call is assigned or moved into a block |
| `tools/tests/test_inventory_consumers.py:48-60` | runs `main.py --inventory` with `ray.init` replaced by `_refuse(*args, **kwargs)` | unchanged: the stand-in takes any keyword |
| `RunDrivers/tests/test_killed_handler.py:476-517` | in `scoped_pipeline_run.main` and `quadsource_atol_sweep.run_build` (`:479`), `_local_ray_init` makes one `_real_ray_init` call whose `address` is the constant `"local"`, then installs the handler | passes with `_temp_dir` added; not applied to `run_child` |
| `RunDrivers/tests/test_build_rehearsal_scope.py:337-344` | `run_child` reads no `build_scope`, and `"rehearsal"` is not in `ast.unparse(run_child)` | passes unless a name, string or docstring added to `run_child` contains `rehearsal` in lower case (item 4) |

No other SGK test names the lock, and none reads the `raypoolkit` pin.

## 7. What goes stale

Live lines (outside `docs/` and `prompts/`):

| Line | Says | Becomes |
|---|---|---|
| `requirements.txt:76` | the pin at `v0.2.0` | `v0.3.0` (item 1) |
| `CLAUDE.md:53` | `raypoolkit` "pinned at `v0.2.0`" | `v0.3.0` |
| `CLAUDE.md:137-142` | after `end`, check `PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock ray-processes` (`:138`) | `./venv/bin/python -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-sgk`; the rest stays true ("until then the rehearsal lock cannot be released") |
| `CLAUDE.md:151-153` | "One lock, the directory `~/ScienceData/.rehearsal-lock`" | `~/.raypoolkit/rehearsal-lock`, the lock of `raypoolkit.rehearsal_lock` |
| `CLAUDE.md:155-158` | `PYTHONPATH=. ./venv/bin/python -m tools.rehearsal_lock acquire --purpose "<text>"`, `set-pid`, `release`; "The helper has no option to do so" | item 3's commands with SGK's values; "the module has no option to do so" (contract §7) |
| `CLAUDE.md:159-160` | every driver names its address, `local` for SGK's; `ray stop` never run | stays true; SGK may add that a start under the lock gives Ray `/tmp/ray-sgk` (item 4) |
| `CLAUDE.md:161-162` | "The contract is StochasticInstantons' `rehearsal-lock-brief.md` at its `d6d550b`; `prompts/runregistry-extraction/README.md` §4.1 is this repository's protocol" | the contract is RayPoolKit's `docs/rehearsal-lock.md` at `v0.3.0`. §4.1 is a closed campaign's record, and names the helper and `ray_temp_dir: in-process` (`README.md:431`, `:435-436`) |
| `tools/rehearsal_lock.py`, `tools/tests/test_rehearsal_lock.py` | the helper and its tests | deleted (item 2) |

**The protocol pointer** (`CLAUDE.md:162`) is SGK's choice: state the protocol in `CLAUDE.md`
itself (take the lock before the first launch, `set-pid` at each launch, hold it through the
readers, release after them) and stop pointing at §4.1; or keep the pointer, saying that the lock's
commands and values are now `CLAUDE.md`'s. Whether §4.1 itself is rewritten is SGK's choice too;
its rules keep records as written. **Advice:** the first, which leaves no live line resting on a
record.

**Records**, counted and not rewritten (lines naming `\.rehearsal-lock`, `rehearsal-lock-brief`,
`tools\.rehearsal_lock` or `rehearsal_lock\.py`; 04's log §3.5):
- `docs/`: 276 lines in 22 files, all under `docs/handover/`, `docs/rrk-v020-adoption*` and
  `docs/runregistry-extraction*`. Four are scripts that call the helper:
  `docs/handover/a3-v2/launch/scripts/prelaunch.sh` and
  `docs/handover/a3-v2/rehearsal/scripts/{after_run,check_and_setpid,prelaunch}.sh`. They are
  records of dated runs, and stop working once the helper is deleted;
- `prompts/`: 155 lines in 31 files (`runregistry-extraction` 129, `rrk-v020-adoption` 19,
  `handover` 6, and `prompts/INDEX.md:22`, the closed campaign's line).

## 8. Its acceptance

1. **The pin** reads `v0.3.0`: `git -C SecondaryGWKit show <commit>:requirements.txt | grep
   raypoolkit` prints item 1's line, and SGK's venv is installed from it.
2. **The helper is gone**: `git -C SecondaryGWKit ls-tree <commit> tools/rehearsal_lock.py
   tools/tests/test_rehearsal_lock.py` prints nothing.
3. **No live line names the old lock**:

   ```bash
   git -C SecondaryGWKit grep -n -E 'ScienceData|\.rehearsal-lock|rehearsal-lock-brief|tools\.rehearsal_lock|rehearsal_lock\.py' <commit> -- . ':!docs' ':!prompts'
   ```

   At `216e44d` it finds **18 lines**: `CLAUDE.md:138`, `:152`, `:155`, `:161`;
   `tools/rehearsal_lock.py:5`, `:7`, `:12`, `:68`, `:441`; and nine in
   `tools/tests/test_rehearsal_lock.py` (`:2`, `:6`, `:101`, `:315`, `:367`, `:374`, `:381`, `:385`,
   `:441`). After the switch it finds **0**. The bullet `CLAUDE.md:161-162` is found by its first
   line.
4. **Every Ray start of item 4 gives the temp dir**: by reading, the three wrappers pass
   `_temp_dir` (and `run_child`'s an address), and each of the seven `ray.init` calls passes it
   when `args.ray_address == "local"`. The grep of item 4, at the new commit, finds no start that
   item 4 does not list.
5. **SGK's suites pass**, all seven roots of `CLAUDE.md:169-175`, with the `tools/tests` count
   lower by exactly 42, and `test_ray_address_default.py`, `test_inventory_consumers.py`,
   `test_killed_handler.py` and `test_build_rehearsal_scope.py` among the passing.
6. **On the day**, the checks of [`switch-over.md`](switch-over.md) §3 pass.
