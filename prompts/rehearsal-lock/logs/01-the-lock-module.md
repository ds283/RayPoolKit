# Log — rehearsal-lock prompt 01: the lock module

**Subject:** Add the shared rehearsal lock as raypoolkit.rehearsal_lock · **Commit:** `6733447`
· **Date:** 2026-10-23 · **Agent:** Claude Opus 5.5

**Result: landed.** `raypoolkit/rehearsal_lock.py` is new: the lock at `~/.raypoolkit/rehearsal-lock`
(D2), refusing while `~/ScienceData/.rehearsal-lock` exists (U4), moved by nothing but the
keyword `lock_dir` (U5); the owner file; `acquire`, `set_pid`, `release`, `status` and
`ray_processes_command` as functions and as the five commands of `python -m
raypoolkit.rehearsal_lock`, with README §4's exit codes; and one process rule, by Ray temp dir with
the client-server seed (U2). It imports only the standard library. `raypoolkit/tests/test_rehearsal_lock.py`
is new, with **103** tests; the import guard gains **2**. The suite goes from **121 to 226**,
passing at 3.12.15 / 2.43.0 (`venv/`) and 3.13.16 / 2.55.1 (a scratch `uv` venv). Each of M1–M14
fails at least one test. No test reads the real `ps` or reaches the real `HOME`, and the real
`~/.raypoolkit` and `~/ScienceData/.rehearsal-lock` are as they were (both absent). **No issue is
opened**; the index stays at 0. Nothing else under `raypoolkit/` changed; nothing was pushed or
tagged; no Ray was started; no client was edited or run.

**Gate, re-checked at start.** `HEAD` was `10be4d5` (the orchestration note), on `50d91c7`; the
tree clean; local `main` four commits ahead of `origin/main`. G1: at SGK `216e44d`,
`tools/rehearsal_lock.py` is `ea1433664ff44576102a1d07a9a797650681dc2e` and
`tools/tests/test_rehearsal_lock.py` `cdeecd60005c6c7939c7dab5d73e3f1b80803e69`; CPBH's
`ray_cluster.sh` at `807f175` is `eaae1e75d4aa27233ef205a75d97333aeb57ea8b`. `Ran 121 tests … OK`.
No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` exit 1). The clients were read only through
`git -C <client> show <commit>:<path>`. Every scratch file of this log (venv, `HOME`s, scripts,
diffs, outputs) is under the agent's scratch directory, `…/scratchpad/agent01/`, written `$S`
below.

## 1. What shipped

| File | What |
|---|---|
| `raypoolkit/rehearsal_lock.py` (new, 738 lines) | the licence header, byte for byte (`extraction` U11); the module docstring (purpose, the five commands and their exit codes, nothing waits, retries or breaks, the provenance note naming SGK's `tools/rehearsal_lock.py` blob `ea14336` and CPBH's `ray_cluster.sh` blob `eaae1e7`, the one place a client is named); the module (§1.1) |
| `raypoolkit/tests/test_rehearsal_lock.py` (new) | 103 tests in ten classes (§1.2) |
| `raypoolkit/tests/test_package_imports.py` | two tests and one helper added; the three tests there unchanged (§1.3) |
| this log, the board, `prompts/INDEX.md` | the records |

`docs/OPEN_ISSUES.md` is unchanged: nothing was opened. `git diff --stat` before staging, with the
two new files untracked:

```text
 raypoolkit/tests/test_package_imports.py | 52 ++++++++++++++++++++++++++++++++
 1 file changed, 52 insertions(+)
```

and `git status --porcelain --untracked-files=all`:

```text
 M raypoolkit/tests/test_package_imports.py
?? raypoolkit/rehearsal_lock.py
?? raypoolkit/tests/test_rehearsal_lock.py
```

`__init__.py`, `RayWorkPool.py`, `contract.py`, `_timing.py`, every other test, `standins.py`,
`pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md` and `.github/` are untouched.
`raypoolkit.egg-info/` (gitignored) was rewritten by the high-end editable install and is not
staged.

### 1.1 The module

**README §4's names**, all present: `acquire(project, purpose, ray_temp_dir, ray_address, *,
lock_dir=None)`, `set_pid(project, ray_temp_dir, pid, *, lock_dir=None)`, `release(project,
ray_temp_dir, *, lock_dir=None)`, `status(ray_temp_dir=None, ray_address=None, *, lock_dir=None)`,
`ray_processes_command(ray_temp_dir, ray_address=None)`, `default_lock_dir()`,
`ray_processes(ray_temp_dir, ray_address=None, *, ps_text=None, self_pid=None)` and
`main(argv=None)`.

**The helpers beyond README §4** (clarification 7):

| Name | Public | What |
|---|---|---|
| `old_lock_dir()` | yes (named by the prompt) | `~/ScienceData/.rehearsal-lock`, from `Path.home()` when called |
| `owner_text(project, purpose, ray_temp_dir, ray_address, pid, acquired=None, host=None)` | yes (named by the prompt) | the seven lines |
| `parse_owner(text)` | yes (named by the prompt) | SGK's parser: the value after the first `": "` |
| `read_owner(lock_dir)` | yes (SGK's name) | the owner file's text, or `None` |
| `pid_alive(pid)` | yes (SGK's name) | `os.kill(pid, 0)`; `PermissionError` is alive; `pid <= 0` is not (deviation 15) |
| `build_parser()` | yes (SGK's name) | the argparse parser of `main` |
| `IN_PROCESS`, `OWNER_KEYS`, `PS_COMMAND`, `COMMAND_WIDTH` | yes | `"in-process"`; the seven keys in order; the `ps` argv; 150 |
| `_not_callers_reason(owner, project, ray_temp_dir)` | no | **the identity check**: `None`, or why not, naming both sides of each mismatch |
| `_callers_lock(d, verb, project, ray_temp_dir)` | no | no lock, no owner file, not the caller's: prints why and returns `None`; else `(text, owner)` (SGK's `_own_lock`) |
| `_check_line`, `_check_ray_temp_dir`, `_check_ray_address`, `_check_pid` | no | §2.2's argument rules, each raising `ValueError` |
| `_argument(check)`, `_pid_argument(text)` | no | argparse `type=` callables: a `ValueError` becomes a usage error (exit 2) |
| `_short_hostname()` | no | SGK's: `hostname -s`, else `socket.gethostname()` cut at its first dot |
| `_replace_owner(lock_dir, text)` | no | `owner.tmp` written, then `os.replace` over `owner` |
| `_recorded_pid(owner)` | no | the owner's pid as an integer, or `None` for `-` or anything not ASCII digits |
| `_usable_owner_values(owner)` | no | the owner's `(ray_temp_dir, ray_address)` if both pass §2.2's checks, else `None` (clarification 5) |
| `_ps_output()` | no | the module's one call of `ps`; non-zero status → `RuntimeError` (SGK's) |
| `_temp_dir_pattern(d)`, `_client_server_pattern(a)` | no | the two seed patterns of §2.3 |
| `_closure(start, children)` | no | `start` and all its descendants (used for the seeds and for this process's own children) |
| `_indented`, `_process_lines`, `_whose`, `_remove_lock`, `_release_again`, `_resolve` | no | printing, removing, and `lock_dir=None` → `default_lock_dir()` |

**The process rule, as implemented** (`ray_processes`): the table is parsed with
`^\s*([0-9]+)\s+([0-9]+)(?:\s+(.*))?$`, other lines skipped. The safe set is `self_pid`, its
ancestors (SGK's walk: while the pid is in the table, not yet safe, and above 1), and the
closure of `self_pid` through the children map. Seeds are every process whose command matches
`(/private)?<re.escape(d)>(?:[/ =]|$)`, where `d` is the temp dir with a leading `/private`
removed only when it starts `/private/` (clarification 4); and, when the address is `host:port`,
every process whose command contains `ray.util.client.server` and matches
`--address=<re.escape(host:port)>(?: |$)`. The result is the closure of the seeds, minus the safe
set, sorted by pid. **Ancestors seed the walk and are never listed** (clarification 3, which is the
prompt's §2.3 step 5 read as written, and SGK's rule): so an ancestor naming the temp dir makes its
other children listed, pinned by `test_an_ancestor_naming_the_temp_dir_seeds_its_other_children`.
CPBH's `ray_cluster.sh` exclusion is not carried. The docstring says that the reaper is not listed
and that the driver's pid covers it.

**The order of each command** is the prompt's §2.2. `acquire`: the arguments; the old location
(`os.path.lexists`, resolved paths compared); `mkdir(parents=True, exist_ok=True)` of the parent;
one `os.mkdir` of the lock; the owner with `pid: -`; the processes of the temp dir and the
address. `set_pid`: the arguments; the pid alive; the lock, its owner file, the identity; exactly
one `pid:` line; that line rewritten through `owner.tmp`. `release`: the arguments; no lock → 0;
no owner file, not the caller's; the recorded pid alive; the owner's `ray_address` unusable
(clarification 5); the processes of the caller's (= the owner's) temp dir and the owner's address,
or an unreadable table; then `owner`, `owner.tmp` and the directory removed.

### 1.2 The tests

| Class | Tests | Covers (prompt §2.6) |
|---|---|---|
| `TestAcquire` | 12 | item 1 |
| `TestOldLocation` | 5 | item 2 (U4) |
| `TestSetPid` | 12 | item 3 |
| `TestRelease` | 16 | item 4, and clarification 5's release refusal |
| `TestRayProcesses` | 26 | item 5, and clarifications 3, 4 and 6 |
| `TestLocations` | 3 | item 6 |
| `TestArguments` | 6 | item 7 |
| `TestOwnerFile` | 7 | item 8 |
| `TestCommandLine` | 15 | item 9, and clarification 5's `status` line |
| `TestLicenceHeader` | 1 | clarification 1 |

Every class derives from `LockTestCase`, whose `setUp` patches `HOME` to a temporary directory,
**refuses to go on unless `default_lock_dir()` and `old_lock_dir()` are both under it**, replaces
`_ps_output` with fixed text, and replaces `_short_hostname` (deviation 19). Every test that does
not test the default location passes `lock_dir` inside the temporary directory. The process-rule
tests pass `ps_text` and `self_pid`. The fixtures are neutral (`ProjectA`/`/tmp/ray-a`/
`127.0.0.1:6400`, `ProjectB`/`/tmp/ray-b`/`127.0.0.1:6500`, `ProjectC`/`/tmp/ray-c`/`in-process`),
and the trees of README §0.3 are reconstructions, commented as such (clarification 8).
`grep -n -i "secondary\|sgk\|champbh\|cpbh\|stochastic\|instanton"` over the module, its tests and
the guard finds only the module's provenance note (lines 61 and 65).

**SGK's 42 tests, ported** (each to its nearest meaning; SGK's class and name → this module's):

| SGK | Here |
|---|---|
| `TestAcquire.test_free_lock_is_created_with_the_seven_keys` | `TestAcquire.test_free_lock_is_created_with_the_seven_keys` (the caller's four values; the real `_short_hostname`) |
| `…test_parent_is_created_but_never_the_lock_with_exist_ok` | `TestAcquire.test_parent_is_created_and_the_lock_by_one_os_mkdir` (adapted: `os.mkdir` is recorded, called once on the lock) |
| `…test_held_by_sgk_returns_3_and_prints_the_owner` | `TestAcquire.test_held_by_the_caller_returns_3_and_prints_the_owner` |
| `…test_held_by_si_returns_3_and_prints_the_owner` | `TestAcquire.test_held_by_another_project_returns_3_and_prints_the_owner` |
| `…test_held_with_no_owner_file_returns_3_and_says_so` | the same name |
| `…test_ray_processes_return_4_and_leave_no_lock` | `TestAcquire.test_processes_of_the_temp_dir_return_4_and_leave_no_lock` |
| `TestSetPid.test_live_pid_changes_pid_and_only_pid` | the same name |
| `…test_dead_pid_is_refused` | `TestSetPid.test_a_dead_pid_is_refused` |
| `…test_pid_zero_is_refused` | `TestSetPid.test_pid_zero_is_refused` (`ValueError`, nothing changed: deviation 12) |
| `…test_si_lock_is_refused`, `…test_champbh_lock_is_refused` | `TestSetPid.test_another_projects_lock_is_refused` (two other projects' files are one case with neutral fixtures: deviation 20) |
| `…test_other_project_with_in_process_temp_dir_is_refused` | `TestSetPid.test_another_project_with_the_callers_temp_dir_is_refused` (only the project differs) |
| `…test_sgk_project_with_another_temp_dir_is_refused` | `TestSetPid.test_the_same_project_with_another_temp_dir_is_refused` |
| `…test_missing_owner_is_refused` | `TestSetPid.test_no_owner_file_is_refused` |
| `…test_missing_lock_is_refused` | `TestSetPid.test_no_lock_is_refused` |
| `TestRelease.test_pid_dash_with_no_processes_releases` | the same name |
| `…test_dead_pid_with_no_processes_releases` | the same name |
| `…test_no_lock_returns_0` | the same name |
| `…test_si_owner_is_refused_and_both_sides_printed`, `…test_champbh_owner_is_refused` | `TestRelease.test_another_project_is_refused_and_both_sides_printed` (deviation 20) |
| `…test_other_project_with_in_process_temp_dir_is_refused` | `TestRelease.test_another_project_with_the_callers_temp_dir_is_refused` |
| `…test_sgk_project_with_another_temp_dir_is_refused` | `TestRelease.test_the_same_project_with_another_temp_dir_is_refused` |
| `…test_missing_owner_is_refused` | `TestRelease.test_no_owner_file_is_refused` |
| `…test_live_pid_is_refused` | `TestRelease.test_a_live_pid_is_refused` |
| `…test_ray_processes_are_refused` | `TestRelease.test_a_process_of_the_temp_dir_is_refused_with_pid_dash` |
| `…test_ray_processes_are_refused_with_a_dead_pid` | `TestRelease.test_a_process_of_the_temp_dir_is_refused_with_a_dead_pid` |
| `TestRayProcesses.test_finds_gcs_raylet_agent_and_the_workers_below_a_raylet` | `TestRayProcesses.test_the_tree_at_ray_2_43`, `…test_the_tree_at_ray_2_55` |
| `…test_a_worker_child_of_a_raylet_is_listed_though_it_names_no_path` | `TestRayProcesses.test_a_descendant_of_a_seed_is_listed_though_it_names_nothing` |
| `…test_skips_other_projects_and_search_commands` | `TestRayProcesses.test_another_projects_processes_are_not_listed`, `…test_any_command_naming_the_temp_dir_is_listed` (a `pgrep` or `grep` that names no temp dir is not listed; one that names it is) |
| `…test_skips_its_own_pid_and_its_ancestors` | `TestRayProcesses.test_this_process_its_ancestors_and_its_children_are_never_listed`, `…test_an_ancestor_naming_the_temp_dir_seeds_its_other_children` |
| `…test_matches_the_path_as_written_and_its_realpath` | `TestRayProcesses.test_the_private_spelling_is_matched_both_ways` (the two spellings of one directory; the venv rule is not carried) |
| `…test_venv_roots_includes_the_realpath` | not carried: `venv_roots()` is not in the module (prompt §2.4) |
| `…test_reads_the_process_table_through_one_function` | the same name |
| `TestDefaultLockDirectory.test_default_is_computed_from_home_at_call_time` | `TestLocations.test_both_locations_follow_home_changed_after_import` |
| `…test_commands_without_an_argument_use_the_patched_home` | `TestLocations.test_commands_without_lock_dir_use_the_patched_home` |
| `TestOwnerParser.test_reads_si_and_champbh_owner_files` | `TestOwnerFile.test_the_three_shapes_written_today_parse` |
| `…test_value_is_everything_after_the_first_colon_space` | the same name |
| `…test_round_trips_its_own_file` | the same name |
| `TestCommandLine.test_commands_and_exit_statuses` | the same name |
| `…test_status_shows_owner_pid_and_processes` | `TestCommandLine.test_status_held_with_a_live_and_a_dead_pid`, `…test_status_with_processes_of_the_owners_temp_dir_and_address` |
| `…test_usage_errors_exit_2` | the same name |
| `…test_there_is_no_option_to_break_wait_or_retry` | `TestCommandLine.test_there_is_no_option_to_break_wait_retry_or_move_the_lock` (extended: `--lock-dir` on every command, and the parser's whole set of option strings pinned) |

So 41 of the 42 are carried, onto 39 tests; one is dropped by §2.4. The other 64 are new.

**One reason standing.** Each refusal test of `release` uses the caller's owner with `pid: -` or
a dead pid and an empty table, except in the one respect it tests; each refusal of `set_pid` uses
a live pid (this process's), an owner file with one `pid:` line and the caller's identity, except
in the one respect it tests. Every refusal test snapshots the whole temporary tree (paths and
bytes) before and compares after.

### 1.3 The guard

`raypoolkit/tests/test_package_imports.py`: a helper, `_run_child_args(args)`, a sibling of
`_run_child(code)` that runs `sys.executable` with an argument list from an empty temporary
directory with `CHILD_TIMEOUT`; and two tests (clarification 2):

- `test_the_lock_module_imports_only_the_standard_library`: `imported_modules(rehearsal_lock.py)`,
  each root in `sys.stdlib_module_names` minus `{"ray", "raypoolkit"}`;
- `test_the_lock_command_runs_with_no_client`: `[sys.executable, "-I", "-X", "importtime", "-m",
  "raypoolkit.rehearsal_lock", "--help"]` exits 0; stdout starts `usage: python -m
  raypoolkit.rehearsal_lock`; the names in stderr's `import time:` lines (the last `|` column,
  stripped) include `raypoolkit` and none has a root in `FORBIDDEN_ROOTS`. `ray` is loaded (by the
  package root, U3) and is not asserted absent.

The module docstring gains items 4 and 5. The three existing tests and `_run_child` are unchanged.

## 2. Deviations from the prompt

The orchestrator's clarifications (its note's §0, eleven items), applied, each an IMPLEMENTATION
CHOICE at the orchestrator's direction unless said otherwise:

1. **The licence header test** (clarification 1). `TestLicenceHeader.test_the_module_opens_with_the_licence_header`
   compares the module's first 15 lines with `LICENCE_HEADER`, imported from
   `raypoolkit.tests.test_inherited_faults` (the constant only). `PACKAGE_MODULES` there is not
   changed (§5). IMPLEMENTATION CHOICE at the orchestrator's direction.
2. **The guard's `-m` test** (clarification 2), as §1.3. IMPLEMENTATION CHOICE at the
   orchestrator's direction.
3. **Ancestors seed the walk; they are never listed** (clarification 3). Not a deviation: it is
   §2.3 as written. Stated here as the orchestrator asked, and pinned (§1.1).
4. **`/private` stripped only as a whole leading component**, and no leading boundary
   (clarification 4). Pinned by `test_private_is_stripped_only_as_a_whole_component` (for
   `/privateer/ray-a`, a command naming `/tmp/er/ray-a` is not listed). IMPLEMENTATION CHOICE at
   the orchestrator's direction.
5. **Owner values that fail §2.2's checks** (clarification 5). `status` with no `--ray-temp-dir`
   uses the owner's pair only when both pass; otherwise its last line is `Ray processes: the
   owner's ray_temp_dir or ray_address is not usable` (`test_status_with_owner_values_that_are_not_usable`,
   three shapes). `release` refuses (1), naming the value, when the owner's `ray_address` is
   unusable (`test_an_owner_address_that_is_not_usable_is_refused`, dead pid, no processes).
   IMPLEMENTATION CHOICE at the orchestrator's direction.
6. **`ray_processes` checks its arguments** (`ValueError`) and catches nothing; the commands catch
   `(RuntimeError, OSError)` (clarification 6). IMPLEMENTATION CHOICE at the orchestrator's
   direction.
7. **The identity helper is `_not_callers_reason(owner, project, ray_temp_dir)`**, and every
   helper is named in §1.1 (clarification 7). IMPLEMENTATION CHOICE at the orchestrator's
   direction.
8. **The process-rule fixtures are reconstructions** of README §0.3's trees with neutral, full
   commands, commented as such (clarification 8). The pids, ppids and roles are the probe's; the
   arguments of each seed are plausible Ray arguments naming the temp dir, not captured lines. In
   each tree, a lock command (`7000`, naming the temp dir) and its `ps` (`7001`) are added below
   the user's shell (`6100`, also the driver's parent), and the probe's own `ps` below the driver
   is left out. IMPLEMENTATION CHOICE at the orchestrator's direction.
9. **No client name in the tests** (clarification 9); the test module's docstring refers to "the
   source module named in `rehearsal_lock`'s provenance note". IMPLEMENTATION CHOICE at the
   orchestrator's direction.
10. **§3.2's transcript runs as a script file**, `$S/cli.sh`, as `HOME=$S/home bash $S/cli.sh`,
    the temp dir in a variable inside it, after checking that no process named it (§3.2).
    IMPLEMENTATION CHOICE at the orchestrator's direction.
11. **macOS paths** (clarification 11): the old-location check compares resolved paths, so a
    `tempfile` `HOME` under `/var/folders` compares right with `/private/var/folders`. IMPLEMENTATION
    CHOICE at the orchestrator's direction.

This agent's own:

12. **`set_pid(…, 0)` raises `ValueError`**, and `set-pid … 0` exits 2, where SGK's returned 1.
    §2.2 makes `pid` a positive integer and a bad argument a `ValueError` / exit 2, and §2.6 item 3
    lists pid 0 among the refusals "with nothing changed"; the test checks both. STRUCTURALLY
    REQUIRED.
13. **`status`: `--ray-address` only with `--ray-temp-dir`.** §2.2 says the process lines use "the
    `ray_temp_dir` given, or else the owner's (and likewise the address)"; README §4's synopsis is
    `status [--ray-temp-dir D [--ray-address A]]` and "the processes of D (or, with no D given, of
    the owner's ray_temp_dir and ray_address)". Read together: with `D` given, the listing is of `D`
    and the `A` given (none if none), never the owner's address; with no `D`, the owner's pair.
    An address without a temp dir is a usage error (exit 2; `ValueError` from the function). Pinned
    by `test_status_takes_an_address_only_with_a_temp_dir` and
    `test_status_with_a_temp_dir_given_uses_it_not_the_owners`. IMPLEMENTATION CHOICE.
14. **The argument rules, made precise.** "One line" is `value.splitlines() == [value]`, which also
    refuses `\v`, `\f`, `\x1c`–`\x1e`, `\x85` and ` `/` `, since `parse_owner` splits on
    them. `ray_address`'s host is everything before the last `:`, non-empty and without whitespace
    (so `[::1]:6379` is accepted), and its port ASCII digits. On the command line a pid is ASCII
    digits (`+5`, ` 5`, `1.5` refused). IMPLEMENTATION CHOICE: each is stricter than, or equal to,
    the letter of §2.2, and keeps every owner value one line and one `ps` token.
15. **`pid_alive(pid)` is `False` for `pid <= 0`.** `os.kill(0, 0)` signals the process group and
    would call a hand-edited `pid: 0` alive, leaving a lock that `release` always refuses.
    `_recorded_pid` takes ASCII digits only (`str.isdigit` would accept `"٣"`). IMPLEMENTATION
    CHOICE.
16. **A listed process's line cuts the command to 150 characters** (`<pid> <ppid> <command[:150]>`),
    as §2.2's layout says, where SGK's cut the whole line. Pinned by
    `test_a_listed_command_is_cut_to_150_characters`. IMPLEMENTATION CHOICE (the prompt's
    reading).
17. **Small robustness choices**, each IMPLEMENTATION CHOICE: a `ps` line with a pid and ppid but
    no command parses (command `""`), so that a descendant chain is not cut; the ancestor walk
    stops at pid 1 without adding it to the safe set (SGK's walk, §5); `set_pid` rewrites only the
    `pid:` line and keeps its line ending and every other byte (`splitlines(keepends=True)`);
    `read_owner` decodes with `errors="replace"` and treats `NotADirectoryError` as no owner file,
    so `status` prints and returns 0 for any owner file; the old location's presence is
    `os.path.lexists`, so a dangling link there refuses, as a client's `mkdir` would fail on it;
    `acquire` reports, rather than raises, a failure to remove the lock again after a process
    refusal (`_release_again`).
18. **`setUp` refuses to run a test unless both locations are under the patched `HOME`.** A guard
    on rule 6: a mutation or a regression that fixed the location at import cannot reach a real
    lock through any test. Its consequence for M13 is in §4. IMPLEMENTATION CHOICE.
19. **`_short_hostname` is replaced in every test but one** (`return_value="testhost"`). `hostname
    -s` took 0.27 s a call on this machine (18 calls, 4.9 s, measured with `cProfile`); the seven-keys
    test uses the real one, kept as `REAL_SHORT_HOSTNAME`. IMPLEMENTATION CHOICE.
20. **SGK's two other-project tests merged, twice** (`si`/`champbh` in `TestSetPid` and
    `TestRelease`): with neutral fixtures they are one case. Every class derives from
    `LockTestCase`, those that touch no lock included, so that every test runs with `HOME`
    patched (README §5 rule 6, literally). IMPLEMENTATION CHOICE.
21. **M9's named test cannot fail.** §2.3 makes a seed a command that *contains* the temp dir, and
    clarification 4 adds no leading boundary, so a command naming `/private/tmp/ray-a` contains
    `/tmp/ray-a` whatever the `/private` treatment: "`/private/tmp/ray-a` listed for `/tmp/ray-a`"
    (`test_a_private_spelling_command_alone_is_listed`) passes under M9 by construction. M9 is
    caught by the reverse direction, `/tmp/ray-a` listed for `/private/tmp/ray-a` (two tests,
    §4). STRUCTURALLY REQUIRED.

No UNINTENDED DRIFT was found.

## 3. Verification performed

### 3.1 The suite, by venv and by module (prompt §3.1)

Every run is `<python> -m unittest discover -s raypoolkit/tests -t .` from the repository root
(the "before" at the high end from a `git archive 10be4d5 raypoolkit` export in `$S/head-tree`, since
the work was by then in the tree and `git stash` is not used), in the foreground, its output
written to `$S/suites/` and the verdict grepped from it. Counts by module are the loader's
(`$S/count.py` walks `unittest.defaultTestLoader.discover`).

| Venv | `sys.version` | `ray` | Tree | Verdict |
|---|---|---|---|---|
| `venv/`, before | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | the repository at `10be4d5` | `Ran 121 tests in 1.947s` `OK` |
| `$S/venv313`, before | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | `git archive 10be4d5` export | `Ran 121 tests in 0.800s` `OK` |
| `venv/`, after | as above | 2.43.0 | the final tree | `Ran 226 tests in 1.909s` `OK` |
| `$S/venv313`, after | as above | 2.55.1 | the final tree | `Ran 226 tests in 2.275s` `OK` |

| Module | Before (both ends) | After (both ends) |
|---|---|---|
| `test_construction` | 15 | 15 |
| `test_inherited_faults` | 6 | 6 |
| `test_package_imports` | 3 | **5** (the two guard tests) |
| `test_printed_lines` | 18 | 18 |
| `test_rehearsal_lock` | — | **103** (new) |
| `test_run_paths` | 22 | 22 |
| `test_scheduling` | 7 | 7 |
| `test_standins` | 30 | 30 |
| `test_task_builder` | 20 | 20 |
| **Total** | **121** | **226** = 121 + 2 + 103 |

**`pip freeze` of `venv/`** (at the start; the editable line names `HEAD` then):

```text
aiosignal==1.4.0
attrs==26.1.0
black==25.1.0
certifi==2026.7.22
charset-normalizer==3.5.2
click==8.5.0
filelock==4.1.0
frozenlist==1.8.0
idna==3.20
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
msgpack==1.2.3
mypy_extensions==1.1.0
packaging==26.3
pathspec==1.1.1
platformdirs==4.12.4
protobuf==7.36.2
PyYAML==6.0.3
ray==2.43.0
-e git+https://github.com/ds283/RayPoolKit.git@10be4d572392ae134df0c4c8de72924090c5c757#egg=raypoolkit
referencing==0.37.0
requests==2.34.2
rpds-py==2026.9.1
typing_extensions==4.16.0
urllib3==2.8.0
```

**The high end**: `uv venv -p /opt/local/bin/python3.13 $S/venv313`, then `uv pip install --python
$S/venv313/bin/python -e /Users/ds283/Documents/Code/RayPoolKit "ray==2.55.1" "black==25.1.0"`
(exit 0). `uv pip freeze`: 22 packages, among them `black==25.1.0`, `ray==2.55.1` and `-e
file:///Users/ds283/Documents/Code/RayPoolKit`.

### 3.2 The command line (prompt §3.2)

`$S/cli.sh`, run as `HOME=$S/home bash $S/cli.sh` with `$S/home` empty. Beforehand `ps -axww -o
command= | grep -F /tmp/ray-rpk01 | grep -v grep` printed nothing. The script:

```bash
#!/usr/bin/env bash
# rehearsal-lock prompt 01, §3.2: the command line in a fresh shell, HOME a scratch directory.
set -u
PY=/Users/ds283/Documents/Code/RayPoolKit/venv/bin/python
TD=/tmp/ray-rpk01-cli
export PYTHONUNBUFFERED=1
run() {
    echo "\$ python -m raypoolkit.rehearsal_lock $*"
    "$PY" -m raypoolkit.rehearsal_lock "$@"
    echo "[exit $?]"
}
cd "$(dirname "$0")/clicwd" || exit 1
echo "HOME=$HOME"
echo "processes naming $TD before the run: $(ps -axww -o command= | grep -F "$TD" | grep -v -c grep)"
run acquire --project RayPoolKit --purpose "rehearsal-lock 01 CLI transcript" --ray-temp-dir "$TD" --ray-address in-process
run status
sleep 60 &
SP=$!
echo "started sleep 60, pid $SP"
run set-pid --project RayPoolKit --ray-temp-dir "$TD" "$SP"
run acquire --project RayPoolKit --purpose "a second acquire" --ray-temp-dir "$TD" --ray-address in-process
run release --project RayPoolKit --ray-temp-dir "$TD"
kill "$SP"
wait "$SP"
echo "killed and waited for pid $SP [wait exit $?]"
run release --project RayPoolKit --ray-temp-dir "$TD"
run status
run ray-processes --ray-temp-dir /tmp/ray-rpk01-nothing
echo "\$ mkdir -p \$HOME/ScienceData/.rehearsal-lock"
mkdir -p "$HOME/ScienceData/.rehearsal-lock"
run acquire --project RayPoolKit --purpose "after the old location" --ray-temp-dir "$TD" --ray-address in-process
run status
echo "\$ find \$HOME"
find "$HOME" | sed "s|^$HOME|\$HOME|"
```

Its whole output, `$S` written for the scratch directory (the `[exit N]` after each command is
the command's status):

```text
HOME=$S/home
processes naming /tmp/ray-rpk01-cli before the run: 0
$ python -m raypoolkit.rehearsal_lock acquire --project RayPoolKit --purpose rehearsal-lock 01 CLI transcript --ray-temp-dir /tmp/ray-rpk01-cli --ray-address in-process
acquired the rehearsal lock ($S/home/.raypoolkit/rehearsal-lock) for RayPoolKit: rehearsal-lock 01 CLI transcript
[exit 0]
$ python -m raypoolkit.rehearsal_lock status
lock: HELD ($S/home/.raypoolkit/rehearsal-lock)
    project: RayPoolKit
    purpose: rehearsal-lock 01 CLI transcript
    acquired: 2026-10-23T14:45:08+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk01-cli
    ray_address: in-process
    pid: -
owner pid: - (no pid recorded yet)
Ray processes of /tmp/ray-rpk01-cli: none
[exit 0]
started sleep 60, pid 24082
$ python -m raypoolkit.rehearsal_lock set-pid --project RayPoolKit --ray-temp-dir /tmp/ray-rpk01-cli 24082
recorded pid 24082 in $S/home/.raypoolkit/rehearsal-lock/owner
[exit 0]
$ python -m raypoolkit.rehearsal_lock acquire --project RayPoolKit --purpose a second acquire --ray-temp-dir /tmp/ray-rpk01-cli --ray-address in-process
the rehearsal lock is held ($S/home/.raypoolkit/rehearsal-lock); its owner file:
    project: RayPoolKit
    purpose: rehearsal-lock 01 CLI transcript
    acquired: 2026-10-23T14:45:08+01:00
    host: mps026088
    ray_temp_dir: /tmp/ray-rpk01-cli
    ray_address: in-process
    pid: 24082
stop and ask the user; nothing here waits on, retries or breaks the lock
[exit 3]
$ python -m raypoolkit.rehearsal_lock release --project RayPoolKit --ray-temp-dir /tmp/ray-rpk01-cli
release: the recorded pid 24082 is alive; not releasing
[exit 1]
killed and waited for pid 24082 [wait exit 143]
$ python -m raypoolkit.rehearsal_lock release --project RayPoolKit --ray-temp-dir /tmp/ray-rpk01-cli
released the rehearsal lock ($S/home/.raypoolkit/rehearsal-lock)
[exit 0]
$ python -m raypoolkit.rehearsal_lock status
lock: free ($S/home/.raypoolkit/rehearsal-lock does not exist)
Ray processes: no temp dir given
[exit 0]
$ python -m raypoolkit.rehearsal_lock ray-processes --ray-temp-dir /tmp/ray-rpk01-nothing
[exit 0]
$ mkdir -p $HOME/ScienceData/.rehearsal-lock
$ python -m raypoolkit.rehearsal_lock acquire --project RayPoolKit --purpose after the old location --ray-temp-dir /tmp/ray-rpk01-cli --ray-address in-process
the old location of the rehearsal lock exists ($S/home/ScienceData/.rehearsal-lock); its owner file:
    (no owner file)
it is the old location: stop and ask the user, who removes it by hand once nothing holds it; nothing was created
[exit 3]
$ python -m raypoolkit.rehearsal_lock status
lock: free ($S/home/.raypoolkit/rehearsal-lock does not exist)
old location: PRESENT ($S/home/ScienceData/.rehearsal-lock)
Ray processes: no temp dir given
[exit 0]
$ find $HOME
$HOME
$HOME/ScienceData
$HOME/ScienceData/.rehearsal-lock
$HOME/.raypoolkit
```

So: `acquire` 0; `status` 0 (held, `pid: -`); `set-pid` of the `sleep`'s pid 0; a second
`acquire` 3; `release` 1 (the pid alive); the `sleep` killed and waited for; `release` 0; `status`
0 (free); `ray-processes` for a temp dir nothing names 0; then, with
`$HOME/ScienceData/.rehearsal-lock` made by hand, `acquire` 3 (the old location, nothing created)
and `status` 0, reporting it.

### 3.3 `black` (prompt §3.3)

`./venv/bin/black` (25.1.0) on the three changed files, then again: no change.
`./venv/bin/black --check raypoolkit docs`: "19 files would be left unchanged" (17 before, and the
two new files).

### 3.4 The real `HOME` (prompt §3.4)

Before any work and after every suite, the transcript and the breakage, `ls -ld` of each:

| Path | Before | After |
|---|---|---|
| `~/.raypoolkit` | does not exist | does not exist |
| `~/ScienceData` | exists (`drwxr-xr-x … Oct 22 21:35`) | the same |
| `~/ScienceData/.rehearsal-lock` | does not exist | does not exist |

The breakage suites ran with `HOME=$S/mhome`, which was empty afterwards. Computing
`default_lock_dir()` once by hand (a smoke check, printing it) created nothing.

### 3.5 No Ray

No Ray was started. `pgrep -lf 'gcs_server|raylet|ray::'` exited 1 (nothing) at the start and at
the end. No test reads the real `ps`: `_ps_output` is replaced in every test, the rule's tests pass
`ps_text`, and the one test of `_ps_output` itself replaces `subprocess.run`.

## 4. The deliberate-breakage record (prompt §3.1)

Each diff below is exactly as applied, generated by `$S/make_mutations.py` from the final module,
and kept as `$S/mutations/mNN.diff`. For each: `git apply --check`, `git apply`, `git apply -R
--check`, the whole suite with `HOME=$S/mhome` (output `$S/mutations/mNN-out.txt`), `git apply
-R`; then the SHA-256 of the three changed files and `git status --porcelain
--untracked-files=all` compared with their values before the item (`$S/mutations/mNN-before.state`,
`…-after.state`): **equal for all fourteen**. Every other module's tests passed under every
mutation.

| # | Mutation | Verdict | Failing tests (all in `test_rehearsal_lock`) |
|---|---|---|---|
| M1 | the lock's `os.mkdir(d)` → `d.mkdir(exist_ok=True)` | failures=6 | `TestAcquire.test_held_by_the_caller_returns_3_and_prints_the_owner`, `…test_held_by_another_project_returns_3_and_prints_the_owner`, `…test_held_in_process_by_another_project_returns_3`, `…test_held_with_no_owner_file_returns_3_and_says_so`; `TestCommandLine.test_commands_and_exit_statuses`; `TestOldLocation.test_acquiring_the_old_location_itself_is_not_refused_by_this_check` |
| M2 | the identity check compares `project` only | failures=6 | `TestSetPid.test_the_same_project_with_another_temp_dir_is_refused`, `TestRelease.test_the_same_project_with_another_temp_dir_is_refused`; `TestSetPid.test_an_in_process_owner_is_never_the_callers`, `TestRelease.test_an_in_process_owner_is_never_the_callers`; `TestOwnerFile.test_the_identity_check_judges_each_shape`, `…test_a_missing_key_is_not_the_callers` |
| M3 | the identity check compares `ray_temp_dir` only | failures=3 | `TestSetPid.test_another_project_with_the_callers_temp_dir_is_refused`, `TestRelease.test_another_project_with_the_callers_temp_dir_is_refused`; `TestOwnerFile.test_the_identity_check_judges_each_shape` |
| M4 | `release` skips the pid check | failures=3 | `TestRelease.test_a_live_pid_is_refused`; `TestCommandLine.test_commands_and_exit_statuses`; `TestLocations.test_commands_without_lock_dir_use_the_patched_home` |
| M5 | `release` skips the process check | failures=6 (5 tests; one in two subtests) | `TestRelease.test_a_process_of_the_temp_dir_is_refused_with_pid_dash`, `…test_a_process_of_the_temp_dir_is_refused_with_a_dead_pid`, `…test_the_owners_client_server_alone_is_refused`, `…test_an_unreadable_table_is_refused` (both subtests); `TestCommandLine.test_commands_and_exit_statuses` |
| M6 | `acquire` skips the process check | failures=4 (3 tests) | `TestAcquire.test_processes_of_the_temp_dir_return_4_and_leave_no_lock`, `…test_the_client_server_of_the_address_returns_4`, `…test_an_unreadable_table_returns_4_and_leaves_no_lock` (both subtests) |
| M7 | the old-location check removed | failures=3 | `TestOldLocation.test_the_old_location_with_an_owner_file_returns_3_and_prints_it`, `…test_the_old_location_without_an_owner_file_returns_3`, `…test_the_old_location_refuses_the_default_location_too` |
| M8 | the temp-dir match drops its boundary | failures=3 (1 test) | `TestRayProcesses.test_the_match_is_a_whole_path_component`, subtests `/tmp/ray-ab`, `/tmp/ray-a.old`, `/tmp/ray-a-2/session` |
| M9 | the `/private` spelling dropped (the stripping and the optional prefix) | failures=2 | `TestRayProcesses.test_the_private_spelling_is_matched_both_ways`, `…test_a_tmp_spelling_command_alone_is_listed_for_the_private_spelling`. The named direction cannot fail (deviation 21) |
| M10 | the descendant walk removed | failures=11 | `TestRayProcesses.test_a_descendant_of_a_seed_is_listed_though_it_names_nothing` (`ray::IDLE` below a raylet), `…test_the_tree_at_ray_2_43`, `…test_the_tree_at_ray_2_55`, `…test_an_ancestor_naming_the_temp_dir_seeds_its_other_children`, `…test_lines_that_do_not_parse_are_skipped`, `…test_reads_the_process_table_through_one_function`, `…test_returns_pid_ppid_and_the_whole_command`, `…test_the_client_server_of_the_address_is_listed`; `TestAcquire.test_processes_of_the_temp_dir_return_4_and_leave_no_lock`; `TestCommandLine.test_commands_and_exit_statuses`, `…test_status_with_processes_of_the_owners_temp_dir_and_address` |
| M11 | the ancestor walk removed | failures=2 | `TestRayProcesses.test_this_process_its_ancestors_and_its_children_are_never_listed` (an ancestor naming the temp dir), `…test_an_ancestor_naming_the_temp_dir_seeds_its_other_children` |
| M12 | the client-server seed removed | failures=6 | `TestRayProcesses.test_the_client_server_of_the_address_is_listed`, `…test_the_client_server_address_may_end_the_line`; `TestRelease.test_the_owners_client_server_alone_is_refused`; `TestAcquire.test_the_client_server_of_the_address_returns_4`; `TestCommandLine.test_the_client_server_option_of_ray_processes`, `…test_status_with_processes_of_the_owners_temp_dir_and_address` |
| M13 | `default_lock_dir()` returns a module constant computed at import | failures=103 | **every test of the module, in `setUp`**: the location is not under the patched `HOME`, so the guard of deviation 18 stops each test before its body (`AssertionError: … is not under the patched HOME …; not running`, 103 times). The named test, `TestLocations.test_both_locations_follow_home_changed_after_import`, is among them. The suite ran with `HOME=$S/mhome`, so the constant was `$S/mhome/.raypoolkit/rehearsal-lock`; nothing was created there |
| M14 | `acquired` and `host` swapped in `owner_text` | failures=2 | `TestAcquire.test_free_lock_is_created_with_the_seven_keys`; `TestCommandLine.test_status_held_with_no_pid` |

Each mutation's named test fails, except M9's, which cannot (deviation 21), and M13's, which fails
in `setUp` rather than in its body.

The fourteen diffs, as `git apply` replays them on `6733447`'s tree:

**M1: the lock's `os.mkdir` replaced by `mkdir(exist_ok=True)`** (`m01.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -448,7 +448,7 @@
 
     d.parent.mkdir(parents=True, exist_ok=True)
     try:
-        os.mkdir(d)  # never exist_ok: this is the atomic step
+        d.mkdir(exist_ok=True)  # never exist_ok: this is the atomic step
     except FileExistsError:
         print(f"the rehearsal lock is held ({d}); its owner file:", file=sys.stderr)
         print(_indented(read_owner(d)), file=sys.stderr)
```

**M2: the identity check compares `project` only** (`m02.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -269,10 +269,6 @@
     problems = []
     if owner.get("project") != project:
         problems.append(f"project is {owner.get('project')!r}, not {project!r}")
-    if owner.get("ray_temp_dir") != ray_temp_dir:
-        problems.append(
-            f"ray_temp_dir is {owner.get('ray_temp_dir')!r}, not {ray_temp_dir!r}"
-        )
     return "; ".join(problems) if problems else None
 
 
```

**M3: the identity check compares `ray_temp_dir` only** (`m03.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -267,8 +267,6 @@
 def _not_callers_reason(owner, project, ray_temp_dir):
     """``None`` when the owner is the caller's (``project`` and ``ray_temp_dir``), otherwise why not."""
     problems = []
-    if owner.get("project") != project:
-        problems.append(f"project is {owner.get('project')!r}, not {project!r}")
     if owner.get("ray_temp_dir") != ray_temp_dir:
         problems.append(
             f"ray_temp_dir is {owner.get('ray_temp_dir')!r}, not {ray_temp_dir!r}"
```

**M4: `release` skips the pid check** (`m04.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -558,11 +558,6 @@
         return 1
     _, owner = held
     pid = _recorded_pid(owner)
-    if pid is not None and pid_alive(pid):
-        print(
-            f"release: the recorded pid {pid} is alive; not releasing", file=sys.stderr
-        )
-        return 1
     address = owner.get("ray_address")
     try:
         _check_ray_address(address)
```

**M5: `release` skips the process check** (`m05.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -574,7 +574,7 @@
         )
         return 1
     try:
-        procs = ray_processes(ray_temp_dir, address)
+        procs = []
     except (RuntimeError, OSError) as exc:
         print(
             f"release: cannot read the process table ({exc}); not releasing",
```

**M6: `acquire` skips the process check** (`m06.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -469,7 +469,7 @@
         return 1
 
     try:
-        procs = ray_processes(ray_temp_dir, ray_address)
+        procs = []
     except (RuntimeError, OSError) as exc:
         print(f"cannot read the process table ({exc})", file=sys.stderr)
         _release_again(d)
```

**M7: the old-location check removed** (`m07.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -432,20 +432,6 @@
     _check_ray_address(ray_address)
     d = _resolve(lock_dir)
 
-    old = old_lock_dir()
-    if os.path.lexists(old) and old.resolve() != d.resolve():
-        print(
-            f"the old location of the rehearsal lock exists ({old}); its owner file:",
-            file=sys.stderr,
-        )
-        print(_indented(read_owner(old)), file=sys.stderr)
-        print(
-            "it is the old location: stop and ask the user, who removes it by hand once nothing "
-            "holds it; nothing was created",
-            file=sys.stderr,
-        )
-        return 3
-
     d.parent.mkdir(parents=True, exist_ok=True)
     try:
         os.mkdir(d)  # never exist_ok: this is the atomic step
```

**M8: the temp-dir match drops its boundary** (`m08.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -309,7 +309,7 @@
     d = ray_temp_dir
     if d.startswith("/private/"):
         d = d[len("/private") :]
-    return re.compile(r"(/private)?" + re.escape(d) + r"(?:[/ =]|$)")
+    return re.compile(r"(/private)?" + re.escape(d))
 
 
 def _client_server_pattern(ray_address):
```

**M9: the `/private` spelling dropped** (`m09.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -307,9 +307,7 @@
 def _temp_dir_pattern(ray_temp_dir):
     """``ray_temp_dir`` in its spellings with and without ``/private``, as a whole path component."""
     d = ray_temp_dir
-    if d.startswith("/private/"):
-        d = d[len("/private") :]
-    return re.compile(r"(/private)?" + re.escape(d) + r"(?:[/ =]|$)")
+    return re.compile(re.escape(d) + r"(?:[/ =]|$)")
 
 
 def _client_server_pattern(ray_address):
```

**M10: the descendant walk removed** (`m10.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -388,7 +388,7 @@
         if temp_dir.search(cmd)
         or (client is not None and _CLIENT_SERVER in cmd and client.search(cmd))
     }
-    listed = _closure(seeds, children) - safe
+    listed = seeds - safe
     return [(p, table[p][0], table[p][1]) for p in sorted(listed)]
 
 
```

**M11: the ancestor walk removed** (`m11.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -373,9 +373,6 @@
 
     safe = set()
     pid = self_pid
-    while pid in table and pid not in safe and pid > 1:
-        safe.add(pid)
-        pid = table[pid][0]
     safe |= _closure({self_pid}, children)
 
     temp_dir = _temp_dir_pattern(ray_temp_dir)
```

**M12: the client-server seed removed** (`m12.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -386,7 +386,6 @@
         p
         for p, (_, cmd) in table.items()
         if temp_dir.search(cmd)
-        or (client is not None and _CLIENT_SERVER in cmd and client.search(cmd))
     }
     listed = _closure(seeds, children) - safe
     return [(p, table[p][0], table[p][1]) for p in sorted(listed)]
```

**M13: `default_lock_dir()` replaced by a module constant computed at import** (`m13.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -99,9 +99,12 @@
 # ---- the locations -----------------------------------------------------------------------------
 
 
+_DEFAULT_LOCK_DIR = Path.home() / ".raypoolkit" / "rehearsal-lock"
+
+
 def default_lock_dir():
     """The shared lock, ``~/.raypoolkit/rehearsal-lock``, computed from ``HOME`` when called."""
-    return Path.home() / ".raypoolkit" / "rehearsal-lock"
+    return _DEFAULT_LOCK_DIR
 
 
 def old_lock_dir():
```

**M14: two owner keys swapped in `owner_text`** (`m14.diff`)

```diff
diff --git a/raypoolkit/rehearsal_lock.py b/raypoolkit/rehearsal_lock.py
--- a/raypoolkit/rehearsal_lock.py
+++ b/raypoolkit/rehearsal_lock.py
@@ -209,8 +209,8 @@
     lines = [
         f"project: {project}",
         f"purpose: {purpose}",
+        f"host: {host}",
         f"acquired: {acquired}",
-        f"host: {host}",
         f"ray_temp_dir: {ray_temp_dir}",
         f"ray_address: {ray_address}",
         f"pid: {pid}",
```

## 5. Observations not acted on

- **`PACKAGE_MODULES` does not grow by itself** (`test_inherited_faults.py:35`, a fixed tuple). The
  new module's header is covered by `TestLicenceHeader` instead (clarification 1). Not an issue.
- **No leading boundary**: §2.3's "contains" matches `/var/tmp/ray-a/x` for `/tmp/ray-a`, and any
  longer path ending in the temp dir. It over-lists, the safe side for `acquire` and `release`
  (clarification 4). Not an issue.
- **`/` passes the temp-dir checks** (absolute, one line, normal form). Its pattern,
  `(/private)?/(?:[/ =]|$)`, lists every process whose command contains `//`, `/ `, `/=` or ends
  in `/`, so `acquire` would almost always refuse with 4. It over-lists; no caller passes it.
  Not an issue; 03's contract document may say that the temp dir is a caller's own directory.
- **pid 1 is not put in the safe set** (SGK's walk). It matters only if pid 1's command names the
  temp dir (a container whose init is a Ray process), and then lists it, the safe side.
- **A file (not a directory) at the lock path**: `acquire` says it is held (3, `os.mkdir` raises
  `FileExistsError`); `release` says there is no lock (0, `is_dir()` false) and removes nothing;
  `status` says it is free. Only a hand-made file can be there. Not an issue.
- **`hostname -s` takes about 0.27 s a call on this machine**, so `acquire` pays it once. Not an
  issue.
- **SI's `HEAD` has moved** to `60687f0` (the orchestrator's facts); `ray_cluster.sh` is still blob
  `6c8eada` there. 01 read SI only at `8b4f615`. For 04.
- **`python -m raypoolkit.rehearsal_lock` imports Ray**, through the package root (U3), so the
  guard's `-m` test sees `ray` loaded; measured here, `raypoolkit`'s cumulative import was 0.62 s
  in `-X importtime` at the low end. Known and decided (U3).

## 6. Issues

None opened, narrowed or closed. `docs/OPEN_ISSUES.md` is unchanged: 0 open.

## 7. State handed to the next prompt

- `raypoolkit.rehearsal_lock` exists, to README §4 and §1.1 above. `acquire(…, lock_dir=…)` is the
  entry point 02's proof uses, with `lock_dir=old_lock_dir()` while the clients still use the old
  location (README §5 rule 9); `acquire` does not refuse the old location as "the old location"
  when it is the lock being acquired (`test_acquiring_the_old_location_itself_is_not_refused_by_this_check`).
- The suite is **226** at both ends; `test_rehearsal_lock` 103, `test_package_imports` 5.
- The process rule is proven on reconstructed trees only. 02 re-measures README §0.3 on the module
  itself, under real Ray, and should compare its listing with the fixtures' roles (seeds, descendants,
  the reaper) and say where a real command line differs from §1.2's reconstructions.
- The command line's exit codes and `status` layout are those of §3.2's transcript; 03 makes them an
  interface in `CLAUDE.md`.
- Nothing is pushed: local `main` is five commits ahead of `origin/main` with this one. CI has not
  run on the new module.
