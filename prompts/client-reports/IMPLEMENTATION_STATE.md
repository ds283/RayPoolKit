# client-reports — board

**Last updated:** 2026-10-27 · **Status: OPEN — no prompts; holds 1 issue reported by ChamPBH on
2026-10-27, until a campaign takes it over.**

**Plan:** [`README.md`](README.md) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.3

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

Code is cited at `991aa64`, where `raypoolkit/` is unchanged since `v0.3.0` (`67a75b9`).

---

## 3. Active and unresolved issues

- **[00-a-pass-blocks-until-process-batch-size-tasks-complete]** — *reported 2026-10-27 by ChamPBH
  (its user's ruling of that day: "we want to pass this upstream"). From: ChamPBH
  `prompts/rrk-adoption/IMPLEMENTATION_STATE.md` §3, `[04-the-pool-waits-for-every-in-flight-item-when-fewer-than-three]`,
  with measurements in ChamPBH's `.documents/rrk-adoption-verification.md` §1.11 and
  `.documents/jordan-normalization-verification.md` §1.10. Read in the package, measured in the
  client. Unassigned.*
  - **What the package does.** Each pass of `RayWorkPool.run` blocks in
    `ray.wait(list(self._inflight.values()), num_returns=min(self._process_batch_size, len(self._inflight)))`
    (`raypoolkit/RayWorkPool.py:355-358`), and only then handles what returned: a finished compute
    task becomes a store task (`:462-487`), a finished store task a validation task (`:489-525`),
    and new work is taken only at the top of the next pass (`:286-353`). This is as documented:
    `process_batch_size` is "how many completed tasks one pass asks `ray.wait` for and handles"
    (`README.md:161`), default 1 (`:27`). With a value above 1 the pass waits for that many
    completions, and when that many or fewer tasks are in flight, for **all** of them. A task that
    has finished then waits behind the slowest one in flight before its next step is submitted.
  - **What the client saw.** ChamPBH passes `process_batch_size=3` to its three titled queues, to
    handle several completions per pass. In its rehearsals (`ray` 2.53 and 2.59, `v0.2.0` and
    `v0.3.0`):
    - a stored row stayed unvalidated for as long as the slowest compute in flight (195.7 s), so a
      `SIGTERM` in that window discarded completed work, which the resume recomputed;
    - a computed result waited 102.0 s and 102.5 s to be stored, behind a slower one, and others
      18.9–19.5 s;
    - the queue's progress line, printed only after a pass's `ray.wait` returns (`:564-595`), came
      as late, which matters to a caller that judges liveness by its output.
  - **Impact.** No result is wrong. The cost is latency of the next step: at a queue's end, and
    whenever few tasks are in flight, a caller that asks for more than one completion per pass
    loses the pipelining of store and validation behind compute, and an interruption in that
    window costs recomputation. For tasks of seconds it is invisible; ChamPBH's tasks take minutes.
  - **Next step.** A change of semantics, for a campaign here to decide and release: make
    `process_batch_size` an upper bound rather than a quota. For example, wait for one completion,
    then take any others already finished, up to the batch size, with `ray.wait(…, timeout=0)`
    (or `ray.wait(…, num_returns=…, timeout=…)` with a short timeout). A test with tasks of unequal
    length, a fake `ray.wait` as the suite's others use, would show a finished task handled while a
    slower one is still in flight. At the default, 1, nothing changes, so only callers that pass
    more than 1 are affected. Until a release, a client can pass `process_batch_size=1` itself, at
    the cost of one `ray.wait` per completion.

## 4. Resolved issues

None.
