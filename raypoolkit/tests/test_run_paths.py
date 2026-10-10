"""
Every path through ``run()``'s dispatch loop: lookup, available, compute, store and validate; the
five exits to the post handler, with and without one; what each exit puts in ``results``; and the
unexpected item type. Inventory rows L, A, K, S, V, P and X of prompt 02 §2.4, and P0, added by
this prompt's log.

The one white-box seam here is ``TestUnexpectedItemType``, which seeds ``_inflight`` and ``_data``
(prompt 02 §2.2): no public input reaches that branch.
"""

import unittest

from raypoolkit.tests.standins import Blob, PoolTestCase, StandinDatastorePool, Work

LOOKUP_ONLY = {"compute_handler": None, "persist_handler": None}

NOT_AVAILABLE_AFTER_STORE = (
    "Object returned from store service does not satisfy the available property"
)


class RunPathTestCase(PoolTestCase):
    def available_handler(self):
        return self.ref_returning_handler("available", True)

    def validation_handler(self, value=True):
        return self.ref_returning_handler("validate", value)

    def compute_handler(self):
        """Logs ``("compute_handler", obj)`` and ``("compute_kwargs", kwargs)``; returns a ref."""

        def handler(obj, **kwargs):
            self.ray.log.append(("compute_handler", obj))
            self.ray.log.append(("compute_kwargs", kwargs))
            return self.ray.ref(None)

        return handler

    def exit_config(self, exit_number):
        """
        The builder and keyword arguments that bring one item to post-handler exit N, with a fresh
        log and datastore, so that the persisted object's ``store_id`` is 1001.
        """
        self.ray.log.clear()
        self.datastore = StandinDatastorePool()
        if exit_number == 1:
            return self.work_builder(available=True), dict(LOOKUP_ONLY)
        if exit_number == 2:
            return (lambda item: self.ray.ref(Blob(item))), dict(LOOKUP_ONLY)
        if exit_number == 3:
            return self.work_builder(available=True), dict(
                LOOKUP_ONLY, available_handler=self.available_handler()
            )
        if exit_number == 4:
            return self.work_builder(available=False), {}
        if exit_number == 5:
            return self.work_builder(available=False), {
                "validation_handler": self.validation_handler()
            }
        raise ValueError(exit_number)

    def kinds(self):
        return [e[0] for e in self.ray.log if e[0] != "wait"]


class TestLookup(RunPathTestCase):
    def test_a_completed_lookup_puts_its_object_in_results(self):
        """L1."""
        pool, _ = self.run_pool(
            ["a", "b"],
            self.work_builder(available=True),
            store_results=True,
            **LOOKUP_ONLY,
        )
        self.assertEqual([obj.name for obj in pool.results], ["a", "b"])

    def test_results_hold_what_get_returned_not_what_the_builder_minted(self):
        """L1: the object in ``results`` is a copy, as Ray's ``get`` gives (by value)."""
        minted = []

        def builder(item):
            minted.append(Work(item, available=True))
            return self.ray.ref(minted[-1])

        pool, _ = self.run_pool(["a"], builder, store_results=True, **LOOKUP_ONLY)
        self.assertEqual(pool.results[0].name, "a")
        self.assertIsNot(pool.results[0], minted[0])


class TestAvailable(RunPathTestCase):
    def test_available_with_an_availability_handler_runs_an_available_task(self):
        """L2, then A1: the post handler (exit 3) is given the lookup's object."""
        pool, _ = self.run_pool(
            ["a"],
            self.work_builder(available=True),
            available_handler=self.available_handler(),
            post_handler=self.recording_handler("post"),
            store_results=True,
            **LOOKUP_ONLY,
        )
        self.assertEqual(self.kinds(), ["available", "post"])
        self.assertEqual(self.ray.wait_calls, [(1, 1), (1, 1)])
        (looked_up,) = self.logged("available")
        self.assertIs(self.logged("post")[0], looked_up)
        self.assertIs(pool.results[0], looked_up)

    def test_available_without_an_availability_handler_exits_to_the_post_handler(self):
        """L3: exit 1, given the lookup's object; no further task."""
        pool, _ = self.run_pool(
            ["a"],
            self.work_builder(available=True),
            post_handler=self.recording_handler("post"),
            store_results=True,
            **LOOKUP_ONLY,
        )
        self.assertEqual(self.kinds(), ["post"])
        self.assertEqual(self.ray.wait_calls, [(1, 1)])
        self.assertIs(self.logged("post")[0], pool.results[0])


class TestNotAvailable(RunPathTestCase):
    def run_compute(self, **kwargs):
        return self.run_pool(
            ["a"],
            self.work_builder(available=False),
            compute_handler=self.compute_handler(),
            **kwargs,
        )

    def test_not_available_with_a_compute_handler_runs_a_compute_task(self):
        """L4: the compute handler is given the lookup's object."""
        pool, _ = self.run_compute(store_results=True)
        self.assertEqual(self.logged("compute_kwargs"), [{}])
        (computed,) = self.logged("compute_handler")
        self.assertEqual((computed.name, computed.store_id), ("a", None))

    def test_a_label_from_the_label_builder_is_passed_as_label(self):
        """L4."""
        labelled = []

        def label_builder(obj):
            labelled.append(obj)
            return f"label-{obj.name}"

        self.run_compute(label_builder=label_builder)
        self.assertEqual(self.logged("compute_kwargs"), [{"label": "label-a"}])
        self.assertIs(labelled[0], self.logged("compute_handler")[0])

    def test_a_label_builder_returning_none_passes_no_label(self):
        """L4."""
        self.run_compute(label_builder=lambda obj: None)
        self.assertEqual(self.logged("compute_kwargs"), [{}])

    def test_a_label_and_a_payload_are_passed_together(self):
        """L4: ``payload`` from the builder's ``"compute_payload"``."""
        self.run_pool(
            ["a"],
            lambda item: {
                "ref": self.ray.ref(Work(item)),
                "compute_payload": ("p", item),
            },
            compute_handler=self.compute_handler(),
            label_builder=lambda obj: "L",
        )
        self.assertEqual(
            self.logged("compute_kwargs"), [{"label": "L", "payload": ("p", "a")}]
        )

    def test_not_available_without_a_compute_handler_does_nothing(self):
        """
        L5: no task, no post handler, and ``results`` keeps the unavailable object. Pinned as it
        behaves; prompt 02's planner does not classify it as a fault.
        """
        pool, lines = self.run_pool(
            ["a", "b"],
            self.work_builder(available=False),
            post_handler=self.recording_handler("post"),
            store_results=True,
            **LOOKUP_ONLY,
        )
        self.assertEqual(self.kinds(), [])
        self.assertEqual(self.ray.wait_calls, [(2, 1), (1, 1)])
        self.assertEqual(
            [(obj.name, obj.available) for obj in pool.results],
            [("a", False), ("b", False)],
        )
        self.assertEqual(lines, [])


class TestBlob(RunPathTestCase):
    def test_an_object_without_available_exits_to_the_post_handler(self):
        """L6: exit 2, given the blob; no availability or compute task even when handlers exist."""
        pool, _ = self.run_pool(
            ["a"],
            lambda item: self.ray.ref(Blob(item)),
            available_handler=self.available_handler(),
            compute_handler=self.compute_handler(),
            post_handler=self.recording_handler("post"),
            store_results=True,
        )
        self.assertEqual(self.kinds(), ["post"])
        self.assertIsInstance(pool.results[0], Blob)
        self.assertIs(self.logged("post")[0], pool.results[0])


class TestComputeStoreValidate(RunPathTestCase):
    def test_a_completed_compute_runs_the_store_handler_then_the_persist_handler(self):
        """K1: each is handed the computed object and the pool; then a store task."""
        seen = []

        def store_handler(obj, pool):
            seen.append(("store_handler", obj, pool))

        def persist_handler(obj, pool):
            seen.append(("persist_handler", obj, pool))
            return pool.object_store(obj)

        self.run_pool(
            ["a"],
            self.work_builder(available=False),
            compute_handler=self.compute_handler(),
            store_handler=store_handler,
            persist_handler=persist_handler,
        )
        (computed,) = self.logged("compute_handler")
        self.assertEqual(
            seen,
            [
                ("store_handler", computed, self.datastore),
                ("persist_handler", computed, self.datastore),
            ],
        )
        self.assertIs(seen[0][1], computed)
        self.assertIs(seen[1][1], computed)
        # lookup, compute, store
        self.assertEqual(self.ray.wait_calls, [(1, 1), (1, 1), (1, 1)])

    def test_a_store_whose_object_is_not_available_raises(self):
        """S1."""
        datastore = StandinDatastorePool(available_after_store=False)
        with self.assertRaises(RuntimeError) as caught:
            self.run_pool(["a"], self.work_builder(available=False), pool=datastore)
        self.assertEqual(str(caught.exception), NOT_AVAILABLE_AFTER_STORE)

    def test_a_completed_store_replaces_the_results_entry_with_the_persisted_object(
        self,
    ):
        """S2."""
        pool, _ = self.run_pool(
            ["a", "b"], self.work_builder(available=False), store_results=True
        )
        self.assertEqual(
            [
                (obj.name, obj.store_id, obj.available, obj.stored)
                for obj in pool.results
            ],
            [("a", 1001, True, True), ("b", 1002, True, True)],
        )

    def test_a_validation_handler_runs_a_validate_task_on_the_persisted_object(self):
        """S3, then V2: exit 5 is given the persisted object."""
        pool, lines = self.run_pool(
            ["a"],
            self.work_builder(available=False),
            validation_handler=self.validation_handler(),
            post_handler=self.recording_handler("post"),
            store_results=True,
        )
        (validated,) = self.logged("validate")
        self.assertEqual((validated.name, validated.store_id), ("a", 1001))
        self.assertIs(self.logged("post")[0], validated)
        self.assertIs(pool.results[0], validated)
        # lookup, compute, store, validate
        self.assertEqual(self.ray.wait_calls, [(1, 1)] * 4)
        self.assertEqual(lines, [])

    def test_without_a_validation_handler_a_completed_store_exits_to_the_post_handler(
        self,
    ):
        """S4: exit 4, given the object the compute ran on (the board's fault 2)."""
        pool, _ = self.run_pool(
            ["a"],
            self.work_builder(available=False),
            compute_handler=self.compute_handler(),
            post_handler=self.recording_handler("post"),
            store_results=True,
        )
        self.assertEqual(
            self.kinds(),
            ["compute_handler", "compute_kwargs", "store", "object_store", "post"],
        )
        self.assertIs(self.logged("post")[0], self.logged("compute_handler")[0])
        self.assertEqual(self.ray.wait_calls, [(1, 1)] * 3)

    def test_a_validation_that_is_not_true_prints_the_warning(self):
        """V1: anything but ``True``, with no title."""
        for value in (False, None, 1, "yes"):
            with self.subTest(value=value):
                self.datastore = StandinDatastorePool()
                pool, lines = self.run_pool(
                    ["a"],
                    self.work_builder(available=False),
                    validation_handler=self.validation_handler(value),
                    post_handler=self.recording_handler("post"),
                )
                self.assertEqual(
                    lines,
                    [
                        "!! WARNING: Work object with store_id=1001 did not validate after "
                        "being emplaced in the datastore"
                    ],
                )
                # the exit is still taken
                self.assertEqual(self.logged("post")[-1].store_id, 1001)

    def test_a_validation_that_is_true_prints_nothing(self):
        """V1."""
        pool, lines = self.run_pool(
            ["a"],
            self.work_builder(available=False),
            validation_handler=self.validation_handler(True),
        )
        self.assertEqual(lines, [])


class TestExits(RunPathTestCase):
    """P1, and P0: at each of the five exits."""

    # what results holds at exit N when the post handler returns None
    def kept(self, exit_number, pool):
        obj = pool.results[0]
        if exit_number == 2:
            self.assertIsInstance(obj, Blob)
        elif exit_number in (4, 5):
            self.assertEqual(obj.store_id, 1001)
        else:
            self.assertEqual((obj.name, obj.store_id), ("a", None))
        return obj

    def test_a_returned_replacement_replaces_the_results_entry(self):
        """P1, with ``store_results``: a non-None return replaces the entry."""
        for exit_number in (1, 2, 3, 4, 5):
            with self.subTest(exit=exit_number):
                builder, kwargs = self.exit_config(exit_number)
                replacement = ("replacement", exit_number)
                pool, _ = self.run_pool(
                    ["a"],
                    builder,
                    post_handler=self.recording_handler(
                        "post", returns=lambda obj: replacement
                    ),
                    store_results=True,
                    **kwargs,
                )
                self.assertEqual(len(self.logged("post")), 1)
                self.assertIs(pool.results[0], replacement)

    def test_a_returned_none_leaves_the_results_entry(self):
        """P1, with ``store_results``: ``None`` leaves the entry as it was."""
        for exit_number in (1, 2, 3, 4, 5):
            with self.subTest(exit=exit_number):
                builder, kwargs = self.exit_config(exit_number)
                pool, _ = self.run_pool(
                    ["a"],
                    builder,
                    post_handler=self.recording_handler("post"),
                    store_results=True,
                    **kwargs,
                )
                self.assertEqual(len(self.logged("post")), 1)
                self.kept(exit_number, pool)

    def test_a_returned_replacement_without_store_results_is_dropped(self):
        """P1, without ``store_results``: there is no ``results`` to replace into."""
        for exit_number in (1, 2, 3, 4, 5):
            with self.subTest(exit=exit_number):
                builder, kwargs = self.exit_config(exit_number)
                pool, _ = self.run_pool(
                    ["a"],
                    builder,
                    post_handler=self.recording_handler(
                        "post", returns=lambda obj: "replacement"
                    ),
                    **kwargs,
                )
                self.assertEqual(len(self.logged("post")), 1)
                self.assertFalse(hasattr(pool, "results"))

    def test_each_exit_without_a_post_handler_calls_nothing(self):
        """P0 (added by prompt 02's log): no post handler, no call, and the entry is kept."""
        for exit_number in (1, 2, 3, 4, 5):
            with self.subTest(exit=exit_number):
                builder, kwargs = self.exit_config(exit_number)
                pool, _ = self.run_pool(["a"], builder, store_results=True, **kwargs)
                self.kept(exit_number, pool)


class TestUnexpectedItemType(RunPathTestCase):
    def test_an_unexpected_item_type_raises(self):
        """
        X1, seeded through ``_inflight`` and ``_data`` (the white-box seam of §2.2).

        ``_data`` is seeded under both ``ref.hex``, the bound method the module keys on today, and
        ``ref.hex()``, the string the board's fault 1 would key on, so that this test pins the
        branch and not the keying.
        """
        pool, _ = self.make_pool([], self.work_builder(), **LOOKUP_ONLY)
        ref = self.ray.ref(None)
        pool._inflight[ref.hex] = ref
        pool._data[ref.hex] = ("unexpected", None)
        pool._data[ref.hex()] = ("unexpected", None)
        with self.assertRaises(RuntimeError) as caught:
            self.run_existing(pool)
        self.assertEqual(
            str(caught.exception), 'Unexpected work queue item type "unexpected"'
        )


if __name__ == "__main__":
    unittest.main()
