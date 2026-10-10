# Orchestrator — prompt 06, the adoption checklists

Read [`../README.md`](../README.md) first: §0.2, §1, §2 (rows 05–07), §3, §4, §5 (rules 5, 6, 9),
§6.2 (U4, U5, U8, U10, U12) and §7. Then read [`prompt-01.md`](prompt-01.md) §0's last list,
"Conventions", which this note keeps unless it says otherwise; [`prompt-04.md`](prompt-04.md)
§0's clarification 1, the driver pattern for breakage of uncommitted work; and the board's
*Orchestrator review of prompt 05* and *Release of `v0.2.0`*.

**You do not write code.** You may:
- run the suite, the agent's script and the commands the log records;
- read the three clients and DatastoreKit through `git -C <repository> show <commit>:<path>`,
  `git ls-tree`, `git log` and `git status --porcelain`, never their working trees' files, and
  read a client's `venv/pyvenv.cfg` as text;
- make fixture repositories, copies of the script and venvs of your own in the session
  scratchpad, and replay the log's breakage there or on the committed tree, restoring it after;
- fix small residue in a follow-up commit of your own (§4).

You do not push or tag. Pushing, so that CI runs `black` over the new script, is put to the user
(§4).

**The prompt:** [`06-the-adoption-checklists.md`](../06-the-adoption-checklists.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- 05 landed (`eaef0ce`), its review is recorded (`9a00f80`), `v0.2.0` is tagged on `eaef0ce`
  (tag object `4e7eb15`) after green CI (run `38075908457`), and the release is recorded
  (`b2b6ab4`, CI run `38076190172` green). 06 is written (`a1d64ea`); U10 and U12 are taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- Each client's `HEAD` is still the commit of the prompt's §0, and its `RayTools/RayWorkPool.py`
  the blob there. If one has moved, the prompt's §5 makes it a stop: put it to the user before
  dispatch.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**Its subject is three other repositories, which it may read and must not touch, and its product
is documents another campaign will act on.** 01–05 changed this package and checked it against
itself. 06 changes nothing the package does; it states facts about SGK, CPBH and SI at named
commits, and the client's own adoption campaign will plan from them. A wrong `path:line` here
becomes a wrong edit there. The review has four halves:
- **the script measures what it says, and its verdict is the package's**: it reads the clients
  only through `git`, its figures equal the planner's and the orchestrator's, and each "constructs"
  comes from `raypoolkit.RayWorkPool`'s own constructor at `v0.2.0`, not from a restated rule;
- **the script would catch a site that does not construct**: the fixture and the breakage (a)–(d)
  show each class and each walk bites;
- **the checklists are true at their commits**: every `path:line` sampled reads as cited, every
  statement about the package holds of `v0.2.0`, and each checklist has the nine items in order;
- **nothing outside this repository moved**: each client's `HEAD`, status and stash list, before
  and after, are equal, and nothing was pushed or tagged.

**What moves on purpose:** five new files under `docs/adoption/` (`README.md`,
`secondarygwkit.md`, `champbh.md`, `stochasticinstantons.md`, `measure_client_pools.py`); the
log, the board, `prompts/INDEX.md`, and `docs/OPEN_ISSUES.md` if an issue is opened. Nothing under
`raypoolkit/`, `docs/extraction/` or `.github/`.

**Clarifications and additions.** Checked by the orchestrator on 2026-10-10 at `a1d64ea` (the
package as at `eaef0ce`), and at SGK `b510bc9`, CPBH `52142d7` and SI `7bb3efd`, by a scratch
script of its own that walked each client's tracked `.py` files at the commit with `ast` and
constructed `raypoolkit.RayWorkPool` for each call. Pass them on. Each is an IMPLEMENTATION
CHOICE at the orchestrator's direction unless it says otherwise, and the log says so.

1. **The constructor is `raypoolkit/RayWorkPool.py:88-206`, not `:88-215`.** `class RayWorkPool:`
   is `:87`, `__init__` opens at `:88`, and the last line of the constructor is `:206`;
   `_build_queued_status_message` begins at `:208`. Cite `:88-206` (the checks are `:109-142`).
   Record as STRUCTURALLY REQUIRED: the prompt's span is not true of `v0.2.0`.
2. **Construct with no `title`.** A titled pool prints its banner from the constructor
   (`:205-206`, `print(f"\n** {title}")`), so a verdict built with the site's title would put a
   banner per site into the script's Markdown. Every site in every client is titled; the title
   changes no check. Leave `title` out of the verdict's keywords (or capture stdout and discard
   it), and say which in the docstring.
3. **A "size keyword" is one of the three the constructor checks**: `create_batch_size`,
   `process_batch_size`, `max_task_queue`. These are evaluated and passed, and a non-literal one is
   replaced by 1 and flagged. The three `notify_*` keywords are reported by source text only,
   never passed and never flagged: SGK's `main.py` alone passes
   `notify_min_time_interval=MIN_NOTIFY_INTERVAL` ten times, which would swamp the flag. With this
   reading the orchestrator's flags are SI's alone, as the prompt expects: three expressions,
   at five keyword occurrences, on four calls.
4. **A call's line is the `ast.Call`'s `lineno`, the line its name is on.** So SI's flagged calls
   are `main.py:383` (`MAX_INFLIGHT_PIPELINE_UNIFIED`, its keyword at `:396`), `:492` and `:1092`
   (`MAX_INFLIGHT_PIPELINE`), and `:718` (`len(traj_payloads)` twice, its keywords at
   `:729-730`). The prompt's `:396` and `:729-730` are keyword lines. A checklist may cite both;
   the script's line is the call's. The same holds for every site the prompt lists by line (SGK's
   `:1042`, `:1057`, `:1940`, `:4146`, `:3247`; CPBH's `:276`, `:533`, `:820`; SI's `:492`,
   `:1092`), each of which is the call's line, measured.
5. **"Absent" `compute_handler` is a compute pool**, with `_default_compute_handler`
   (`raypoolkit/RayWorkPool.py:75-76`), not a lookup-only one. So SGK has 10 compute pools (6
   given, 4 left at the default), as README §0.2 says. Its four defaults: `main.py:1042` and
   `:1057` pass no handler at all; `:1940` passes a validation handler and a label builder; `:4146`
   passes `validation_handler=None` and a label builder. Each constructs.
6. **SGK's pinned lines are five, not six, and the checklist says what is there.**
   `RunRegistry/tests/test_pipeline_adoption.py:38-44` is `A3_OUTPUT`, holding the banner (`:39`)
   and two progress notifications of two lines each (`:40-43`); the completion pair the comment
   (`:32-37`) names is not in it. The stamps carry `+0100`, which the pool does not print (README
   §0.2's note). The module names `RayWorkPool` once, in that comment (`:32`), and `RayTools`
   nowhere; the comment cites the pool's lines `:166`, `:548` and `:566` without naming the file,
   and they are SGK's copy's (the banner, a progress `print(msg)`, the completion `print(`). Quote
   the block as it is; do not repeat "six lines" as a fact of the test. Record as STRUCTURALLY
   REQUIRED.
7. **CPBH's 23 uncommitted changes are all untracked** (`??`): two run scripts, seventeen pilot
   `.db` files, two logs, `pilot-out/` and `prompts/jordan-normalization/`. No tracked file is
   modified, and none is under `RayTools/`. The checklist may say so from `git status
   --porcelain`'s paths. **The `.db` files are datastores:** do not open, list the contents of, or
   read one (README §3; the prompt's §5).
8. **SI's interpreter.** `venv/pyvenv.cfg` says `version = 3.13.13` and names MacPorts' 3.13
   framework as `base-executable`; `/opt/local/bin/python3.13` reports 3.13.16 today. Do not run
   SI's `venv/bin/python` (the prompt's §5): the checklist gives `pyvenv.cfg`'s version, says the
   interpreter is MacPorts' 3.13, and that either version is inside `>=3.12`. CPBH's says
   `version = 3.13.16`; SGK's `3.12.15`.
9. **SGK's post handler at `main.py:3247`** is `postprocess_GkSourcePolicy`, defined at
   `main.py:2871`. It reads `obj.policy`, `policy.label`, `policy.store_id` (only when the label is
   `None`, and the policy's, not `obj`'s), `obj.type` and `obj.quality`. Whether the object the
   default persist handler returns carries those as the local one did is for the agent to read
   (SGK's `pool.object_store` path, through `git show`) and state with its `path:line`s; if it
   cannot be settled by reading, the checklist says so and names what SGK's campaign should check.
10. **DatastoreKit.** Its `origin` is `https://github.com/ds283/DatastoreKit`, public; link its
    checklists as `https://github.com/ds283/DatastoreKit/blob/v0.2.1/docs/adoption/<file>.md`.
    Their `RayTools/` rows, at `v0.2.1`: SGK `secondarygwkit.md:92` and `:704` (and `:232`, on
    the layer guard after the layer is gone); CPBH `champbh.md:93`, `:602`; SI
    `stochasticinstantons.md:105`, `:578` (and `:47`, its protected list). Read, do not copy.
11. **The verdict is `v0.2.0`'s.** `venv/` has `raypoolkit` editable at `0.2.0`, and
    `git diff eaef0ce -- raypoolkit` is empty at `a1d64ea`. The script records the package's
    version in its output (Markdown and JSON), and the log records the diff's emptiness before
    and after. Constructing calls no Ray: measured, `ray.is_initialized()` is false after a
    construction.
12. **The breakage is of uncommitted work**, as 04's was: record the SHA-256 of every new file
    and `git status --porcelain --untracked-files=all` before each item; apply with `git apply`,
    revert with `git apply -R` (never `git checkout`, `restore` or `stash`); both must equal what
    they were after. The diffs are against the script as it will be committed; (c)'s edit is to the
    fixture's working tree, not to a client's.
13. **The fixture's path override** is the agent's choice (an option, or an environment
    variable), used only by §3.3, and it must not change which repository or commit the default
    invocation reads. Make the fixture with `git init` in the scratchpad, committing with `git -c
    user.name=… -c user.email=…` so that no configuration is written. It holds no client file.
14. **The counts.** The suite is not affected: `discover -s raypoolkit/tests` does not see
    `docs/`. `black --check raypoolkit docs` goes from 15 files to **16**, and CI runs it, so
    the script must be black-clean.

**The facts, checked by the orchestrator.** Pass them on.

- **The baseline at `a1d64ea`.** `venv/`: Python 3.12.15, `ray==2.43.0`, `black==25.1.0`,
  `raypoolkit` editable at `0.2.0`. `Ran 121 tests … OK`. `black --check raypoolkit docs`: 15
  files unchanged. `docs/` holds `extraction/` and `OPEN_ISSUES.md`; there is no `docs/adoption/`.
- **The clients, at writing.**

  | Client | `HEAD` (branch) | Porcelain lines | Stash | Blob of `RayTools/RayWorkPool.py` | `ray` pin |
  |---|---|---|---|---|---|
  | SGK | `b510bc90b66985532d28996ab4e5b13b0ff71709` (`handover-remedial`), 2026-10-07, "Freeze the datastore layer while it moves to DatastoreKit" | 0 | 0 | `b4666fa89abb…` | `ray==2.43.0` |
  | CPBH | `52142d75aebe00855804e2daff4f63aee50ffc3e` (`main`), 2026-10-07, "Store each shard key under its own serial" | 23, all `??` | 0 | `aaa6dc92186…` | `ray==2.53.0` |
  | SI | `7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7` (`main`), 2026-10-09, "Record the R1 calculation review and open its issues board" | 0 | 0 | `92be5b2c9e4c…` | `ray==2.55.1` |

  CPBH has no `origin` remote; SGK's and SI's are `github.com/ds283/<name>`.
- **The prompt's §0 figures hold**, by the orchestrator's script:
  - imports: SGK 7, CPBH 3, SI 3, each `from RayTools.RayWorkPool import …` at column 0, at the
    prompt's lines; SI's `main.py:45` imports `RayWorkPool, _default_store_handler`, the only
    private name; no `import RayTools…` statement; no `import_module` or `__import__` naming
    `RayTools`;
  - string literals naming `RayTools` in `.py` files: SGK 8 (six in
    `Datastore/tests/test_layer_is_generic.py`, at `:1`, `:70`, `:88`, `:120`, `:192`, `:357`;
    `docs/tolerance-convergence/inventory.py:382`;
    `prompts/datastore-generic/orchestrator/measure-09/scripts/m3_make_mutations.py:33`); CPBH 0;
    SI 0;
  - sites: SGK 54 (44 with both `None`s; 6 compute given; 4 left at default), CPBH 17 (14 with
    `store_handler=None` only; 3 compute), SI 16 (12 with both `None`s; 4 compute, each setting
    store and persist handlers); `store_results=True` 39, 13, 11; titled 54, 17, 16; two
    positional arguments everywhere; no `**kwargs`;
  - verdicts: all 87 **construct**; flags as clarification 3;
  - non-`.py` lines naming `RayTools` or `RayWorkPool`: SGK 196 (`prompts/` 156, `docs/` 39,
    `CLAUDE.md` 1), CPBH 43 (`.documents/` 22, `prompts/` 21), SI 89 (`.documents/` 44,
    `.prompts/` 27, `.claude/` 17, `CLAUDE.md` 1);
  - test modules naming either: SGK 7 (`test_layer_is_generic.py`, `test_pipeline_adoption.py`
    and the five `ComputeTargets/tests/` modules of §0.4); CPBH 0; SI 0.
- **Lines spot-read at the commits**, as the prompt cites them: SI `main.py:45`, `:61`, `:79`,
  `:396`, `:401`, `:497`, `:664`, `:824`, `:848`, `:1097`, `:705-716`, `:729-730`;
  `model_list` comes from `inputs["model_list"]` at `:1153`; SI `RayTools/RayWorkPool.py:23`,
  `:79-80`, `:90`, `:261`; SI `CLAUDE.md:89-95`; SGK `CLAUDE.md:70-73` (the paragraph is
  `:69-73`; the `RayTools/` sentence `:70-71`); SGK `test_layer_is_generic.py:70-71`, `:88`,
  `:120`, `:192-193`, `:303-304`, `:357`. The agent reads every one again, and the others.
- **The package, at `v0.2.0`.** `from raypoolkit.RayWorkPool import _default_store_handler`
  works (U4's note); `raypoolkit.RayWorkPool` is the class. `create_batch_size=0` raises
  `ValueError: create_batch_size must be at least 1, not 0`. The defaults are `:75-84`.
- **Expected counts.** The suite is **121** before and after. The index is **0** now, and stays
  0 unless the work opens an issue.
- **Ray.** None was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).
- **GitHub, read only.** `origin/main` is `b2b6ab4`; local `main` is ahead by `a1d64ea` and this
  note. The tags are `v0.1.0` (on `4e90a8a`) and `v0.2.0` (on `eaef0ce`), locally and on
  `origin`.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §6 files changed; nothing under `raypoolkit/`,
  `docs/extraction/` or `.github/`; no tag; nothing pushed; no client or DatastoreKit touched.
- **(E2) The script, by reading.** `git` only, at a commit; `ast`; the six reports; the verdict
  from the package's constructor, built as the prompt's §2.1 item 4 and clarifications 2–3 say;
  sorted output; exit codes; standard library and `raypoolkit` only.
- **(E3) The script, by running.** Its figures equal the facts above; two runs `cmp`-equal;
  `--json` parses; a missing commit exits 2.
- **(E4) The script bites.** The fixture reports each case with the prompt's verdicts; (a)–(d)
  fail as logged; the orchestrator's own fail.
- **(E5) The checklists.** Nine items, in order, under the same names, in each; every sampled
  `path:line` reads as cited at its commit; every package statement true of `v0.2.0`; the
  appendix equal to the script's output at the commit.
- **(E6) The clients untouched.** `HEAD`, porcelain hash and stash count equal before and after.
- **(E7) The records.** The log with §4.5's additions; the board's header, 06's row and G2–G4;
  `prompts/INDEX.md`; the index unchanged, or in step with §3.

**Conventions.** Prompt 01's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run every suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff with `git apply --check` (and `-R --check` once applied), replay it in
  `bash`, and check the tree is restored after it (clarification 12);
- use the scratchpad subdirectory you are given, never `/tmp`, and put no scratch file under the
  repository, least of all under `raypoolkit/` (the suite collects it);
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

Three additions:
- **Nothing outward-facing.** No `git push`, no `git tag`, no `gh` command that writes.
- **Read-only toward every other repository.** For SGK, CPBH, SI and DatastoreKit: only `git
  show`, `git ls-tree`, `git log`, `git rev-parse`, `git grep <commit>`, `git status --porcelain`
  and `git stash list`; never `git checkout`, `switch`, `stash`, `fetch`, `worktree`, `config`, or
  any command that writes `.git/`; never open a file in a working tree but `venv/pyvenv.cfg`, as
  text; never import, run or open a store of one.
- **Diff and output files have distinct names on this case-insensitive filesystem** (log 02 §5's
  slip): `a.diff` … `d.diff`, and nothing that differs from another only by case.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. `git diff eaef0ce --
   raypoolkit` is empty.
2. **The baseline.** The suite gives `Ran 121 tests … OK`. `git tag` is `v0.1.0` and `v0.2.0`;
   `git ls-remote origin` shows `main` at `b2b6ab4` and the two tags as above.
3. **The clients.** For each, record `rev-parse HEAD`, `status --porcelain | shasum`, `stash list
   | wc -l`, and the blob of `RayTools/RayWorkPool.py` at the commit. Each `HEAD` and blob is the
   table's; if not, stop (gate).
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`, attributed by path.
5. **The index.** 0 now; 0 after unless an issue is opened. Tell the agent.
6. **Scratch.** Make the agent's subdirectory of the session scratchpad, empty, and tell it the
   path. Keep your own measurements in another.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, the package's
  `README.md` and `PROVENANCE.md`, and logs 04 and 05 (for what changed and how it was checked);
- `HEAD`, the counts, the clients' table and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's fourteen clarifications and additions. Clarifications
2, 3 and 6 are the ones that matter: the first two so that the script's output and flags are
what the prompt expects, the third so that SGK's checklist does not repeat a miscount about SGK's
own test.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/06-the-adoption-checklists.md`, in README §5.1's
  form, with the prompt's §4.5 additions.
- **The files it may change are the prompt's §6 list, and nothing else.** In particular nothing
  under `raypoolkit/`, `docs/extraction/` or `.github/`; not `README.md`, `PROVENANCE.md`,
  `pyproject.toml`, `CLAUDE.md`, `LICENSE`, `.gitignore`, `.idea/`, the campaign README or
  anything under `orchestrator/`.
- **It pushes nothing and tags nothing**, and writes nothing to GitHub.
- **It edits, runs and imports no client and not DatastoreKit**, and reads them only as the
  conventions allow; it opens no `.db` file.
- **It starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **E1, scope.** `git show --stat <commit>` touches only the five files under `docs/adoption/`,
   the log, the board, `prompts/INDEX.md`, and the index if an issue was opened.
   `git diff a1d64ea <commit> -- raypoolkit docs/extraction .github README.md PROVENANCE.md
   pyproject.toml CLAUDE.md LICENSE .gitignore prompts/extraction/README.md` is empty.
   `git tag` and `git ls-remote origin` are unchanged. No scratch file in the tree.
2. **E6, the clients.** Each client's `HEAD`, porcelain hash and stash count equal §1's record.
3. **E2, the script, by reading.** Read it whole. It calls `git` with `ls-tree -r` and
   `show <commit>:<path>` only, and never opens a path under the client's directory; it walks
   with `ast.walk` (or an equivalent that reaches nested imports and calls); its handler classes
   are absent, `None` (the literal), and set; the verdict builds keywords as clarifications 2–3 say
   and calls `raypoolkit.RayWorkPool`, with no restated rule; every output list is sorted; exit 2
   on an unreadable client or commit; its imports are the standard library and `raypoolkit`; its
   docstring says the verdict is only as good as the classes.
4. **E3, the script, by running.** In a fresh shell, from the repository root: each client twice,
   `cmp`-equal, exit 0, the figures of §0; `--json` for each parses with `json.loads`, and its
   counts equal the Markdown's; `--commit 0000000` exits 2 for each. Each appendix in the
   checklists equals the script's Markdown for that client (strip the appendix and `diff`).
5. **E4, the fixture, re-made.** Make your own fixture as the prompt's §3.3 lists, with the
   agent's override, and run the script on it: each case reported, with the verdicts the prompt
   gives. Then the orchestrator's own:
   - (o1) the script with "absent" `compute_handler` passed as `None`: SGK's `main.py:1940` and
     `:4146` must stop constructing (each gives a label builder with what the script then thinks
     is no compute handler), so the absent/`None` distinction is what keeps them right;
   - (o2) a fixture call written as `raypoolkit_alias.RayWorkPool(...)` (an attribute call) and
     one as `RayWorkPool(pool, tasks, build, None)` with `compute_handler` passed positionally:
     the first must be found; for the second, the log or the docstring must say how a positional
     handler is treated (no client has one: every site passes two positional arguments).
6. **E4, the breakage, by replaying.** Extract (a)–(d) from the log's text and replay each on the
   committed script, each first checked with `git apply --check`, the fixture and the clients as
   the log says: each fails as logged. `git status` is clean after each.
7. **E5, the checklists, by reading.** Read the adoption README and all three checklists whole.
   Each checklist has the nine items of the prompt's §2.3, in order, under the same names, and
   opens with the full SHA, branch, date and subject. Then sample at least ten `path:line`s per
   checklist, including every one the prompt's §0 names and every one the prompt did not, and
   read each with `git show` at its commit: each says what the checklist says it does. Each
   statement about the package is checked against `v0.2.0` (its README, a test, or a probe);
   in particular SI's `_default_store_handler` advice, CPBH's U10 paragraph, SI's
   `main.py:718`/`:729-730` options, and SGK's `:3247` finding (clarification 9).
8. **E5, the order with DatastoreKit.** The adoption README's §5 table equals the prompt's §0.6;
   each checklist's item 7 names the `RayTools/` import's line and links that client's
   DatastoreKit checklist at `v0.2.1` by URL; U12 is stated in one sentence with its date. SGK's
   item 6 says, for each order, what `test_layer_is_generic.py` needs, by line.
9. **Links and `black`.** Every relative link under `docs/adoption/` resolves to a file in the
   commit; every external link is to `github.com/ds283/…` at a named tag, and each such file
   exists at that tag (`git show <tag>:<path>` in the repository named). `./venv/bin/black --check
   raypoolkit docs` (25.1.0): 16 files unchanged. The suite: 121, OK.
10. **E7, the records.** The log has every section of README §5.1 and each of the prompt's §4.5
    additions; §0's clarifications recorded as deviations (1 and 6 STRUCTURALLY REQUIRED). Board:
    the header; 06's row (landed, "this commit", 121 → 121); G2–G4 each pointing at its
    checklist. Index: count it, and check the header matches. `prompts/INDEX.md`: the campaign's
    line.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 06* paragraph, in the form of
  05's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 06, and its header;
  - the notes line, with this note added and marked "used for 06".
- Anything the review finds that is not residue is opened on the board's §3 and in the index. A
  checklist statement found untrue goes to a fix before 07, since a client campaign will act on it.
- **Put the push to the user, and do none of it unasked.** CI has not run `black` over the new
  script. *Recommended:* push `main` as it stands after the follow-up; no tag (06 changes no
  release).
- **Report to the user:**
  - what landed: the three checklists, the README and the script, and the count, 121 → 121;
  - the script's figures for each client, and that every one of the 87 sites constructs under
    `v0.2.0` by the package's own constructor;
  - what each client must change on adoption, in a line each (SI's private import and its empty
    `model_list` case; CPBH nothing at its sites; SGK its layer guard, depending on the order);
  - (a)–(d), and the orchestrator's (o1)–(o2);
  - the push, as a decision for them;
  - that 07, the verification and close-out, can be written next.
