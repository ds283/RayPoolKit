# Open issues — project-wide index

One line per open issue, pointing at the board that holds it. The board is right if the two
disagree. See `CLAUDE.md` for the maintenance rule.

**Last updated:** 2026-10-27 · **1 open**, on this repository's boards.

## 1. By campaign

### 1.1 `extraction` ([board](../prompts/extraction/IMPLEMENTATION_STATE.md)) — closed 2026-10-10

None open. The board's §4 records the resolved issues.

### 1.2 `rehearsal-lock` ([board](../prompts/rehearsal-lock/IMPLEMENTATION_STATE.md)) — closed 2026-10-24

None open. The board's §4 records the resolved issues.

### 1.3 `client-reports` ([board](../prompts/client-reports/IMPLEMENTATION_STATE.md)) — opened 2026-10-27, no prompts

Issues a client found in the package and reported here, each held until a campaign takes it over.

| Issue | Hook |
|---|---|
| `[00-a-pass-blocks-until-process-batch-size-tasks-complete]` | With `process_batch_size` above 1, a pass waits for that many completions (all of them when as few are in flight), so a finished task's store and validation wait behind the slowest; reported by ChamPBH |
