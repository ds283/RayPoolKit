# RayPoolKit

A driver-side work queue for [Ray](https://www.ray.io/). `RayWorkPool` takes a list of work
items, builds a lookup task for each, and carries every object it gets back through a fixed
cycle: if the object is already available it is finished (optionally after an availability
task), and if not it is computed, stored locally, persisted, and optionally validated, with a
post-processing hook at each exit. It caps the number of tasks in flight, so a long queue never
floods Ray's object store, and reports progress and rates as it drains.

**Status: being extracted.** The code does not live here yet. It is the `RayTools/RayWorkPool.py`
of [SecondaryGWKit](https://github.com/ds283/SecondaryGWKit), and is shared in origin with ChamPBH
and StochasticInstantons, each of which carries its own lightly diverged copy. The plan for moving
it here, and for the three projects to depend on one copy, is
[`prompts/extraction/README.md`](prompts/extraction/README.md); its status board is
[`prompts/extraction/IMPLEMENTATION_STATE.md`](prompts/extraction/IMPLEMENTATION_STATE.md).

RayPoolKit does not depend on [DatastoreKit](https://github.com/ds283/DatastoreKit), the
datastore layer extracted from the same projects. A `RayWorkPool` is handed any pool object its
handlers understand; the default persist handler calls only its `object_store` method.

## Licence

Apache License 2.0; see [`LICENSE`](LICENSE).
