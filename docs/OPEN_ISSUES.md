# Open issues — project-wide index

One line per open issue, pointing at the board that holds it. The board is right if the two
disagree. See `CLAUDE.md` for the maintenance rule.

**Last updated:** 2026-10-10 · **6 open**, all on this repository's boards.

## 1. By campaign

### 1.1 `extraction` ([board](../prompts/extraction/IMPLEMENTATION_STATE.md))

| Issue | Hook |
|---|---|
| `[00-in-flight-work-is-keyed-on-a-bound-method]` | Dictionaries keyed on `ref.hex` (the method), which works only because `ray.wait` returns the refs it was given *(04)* |
| `[00-a-post-handler-after-persist-gets-the-unpersisted-object]` | With no validation step, the post handler gets the pre-persist copy, without `store_id`; reachable at SGK `main.py:3247`, harmless there *(04)* |
| `[00-store-results-sizes-from-len-of-the-task-list]` | `store_results=True` with a generator `task_list` raises `TypeError` *(04)* |
| `[00-the-constructor-checks-its-handlers-unevenly]` | Raises `RuntimeWarning` for a persist handler without compute, so lookup-only pools must pass `persist_handler=None`; no store-handler check *(04, U8)* |
| `[00-messages-say-maker-and-the-module-has-no-licence-header]` | Cosmetic: "maker" in two messages; no licence header *(04)* |
| `[01-a-kept-comment-names-the-datastore-service]` | A comment kept from SGK (`RayWorkPool.py:424`) names the client's `Datastore` service *(04)* |
