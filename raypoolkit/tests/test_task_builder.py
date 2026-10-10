"""
The task builder's outcomes, one pass of the batch loop at a time: what the pool accepts from a
builder, what it refuses and with which message, and how many builder calls and ``wait`` calls a
batch makes. Inventory rows R1-R9 of prompt 02 §2.4.
"""

import unittest

from raypoolkit.tests.standins import PoolTestCase, Work

LOOKUP_ONLY = {"compute_handler": None, "persist_handler": None}

NONE_WITH_STORE_RESULTS = (
    "a task builder returned None, which is not compatible with store_results=True"
)
MANY_WITH_STORE_RESULTS = "store_results=True is not compatible with returning multiple work items from a task builder"


class BuilderTestCase(PoolTestCase):
    def logging_builder(self, available=True, shape=None):
        """
        Mints one ref per item, its value ``Work(item, available)``, logs ``("build", item)``, and
        returns ``shape(ref)`` (by default the bare ref).
        """

        def builder(item):
            self.ray.log.append(("build", item))
            ref = self.ray.ref(Work(item, available=available))
            return ref if shape is None else shape(ref)

        return builder

    def events(self):
        return [e for e in self.ray.log if e[0] in ("build", "wait")]

    def post_names(self):
        return [obj.name for obj in self.logged("post")]


class TestBatchCreation(BuilderTestCase):
    def test_a_batch_is_created_only_while_the_queue_has_room(self):
        """R1: no batch while ``len(_inflight) >= max_task_queue``; the batch itself is not capped."""
        self.run_pool(
            [1, 2, 3, 4, 5, 6],
            self.logging_builder(),
            max_task_queue=2,
            create_batch_size=2,
            **LOOKUP_ONLY,
        )
        self.assertEqual(
            self.events(),
            [
                ("build", 1),
                ("build", 2),
                ("wait", 2, 1),
                ("build", 3),
                ("build", 4),
                ("wait", 3, 1),
                # two in flight, the cap: no batch
                ("wait", 2, 1),
                ("build", 5),
                ("build", 6),
                ("wait", 3, 1),
                ("wait", 2, 1),
                ("wait", 1, 1),
            ],
        )

    def test_a_batch_makes_at_most_create_batch_size_builder_calls(self):
        """R2."""
        self.run_pool(
            [1, 2, 3, 4, 5, 6, 7],
            self.logging_builder(),
            create_batch_size=3,
            process_batch_size=10,
            **LOOKUP_ONLY,
        )
        self.assertEqual(
            self.events(),
            [
                ("build", 1),
                ("build", 2),
                ("build", 3),
                ("wait", 3, 3),
                ("build", 4),
                ("build", 5),
                ("build", 6),
                ("wait", 3, 3),
                ("build", 7),
                ("wait", 1, 1),
            ],
        )

    def test_num_returns_is_the_smaller_of_process_batch_size_and_the_work_in_flight(
        self,
    ):
        """R9."""
        self.run_pool(
            [1, 2], self.logging_builder(), process_batch_size=3, **LOOKUP_ONLY
        )
        self.assertEqual(self.ray.wait_calls, [(2, 2)])


class TestSingleReturns(BuilderTestCase):
    def test_store_results_takes_a_result_index_per_single_return_in_task_order(self):
        """R3, with ``store_results``: a bare ref and a dict each take the next index."""
        shapes = {
            "a": lambda ref: ref,
            "b": lambda ref: {"ref": ref},
            "c": lambda ref: {"ref": ref, "compute_payload": None},
        }
        pool, _ = self.run_pool(
            ["a", "b", "c"],
            lambda item: shapes[item](self.ray.ref(Work(item, available=True))),
            store_results=True,
            **LOOKUP_ONLY,
        )
        self.assertEqual([obj.name for obj in pool.results], ["a", "b", "c"])

    def test_without_store_results_a_single_return_takes_no_index(self):
        """R3, without ``store_results``: there is no ``results`` and no index to take."""
        pool, _ = self.run_pool(
            ["a", "b"],
            self.logging_builder(),
            post_handler=self.recording_handler("post"),
            **LOOKUP_ONLY,
        )
        self.assertFalse(hasattr(pool, "results"))
        self.assertEqual(self.post_names(), ["a", "b"])

    def test_a_dict_with_a_compute_payload_passes_it_to_the_compute_handler(self):
        """R4, with ``"compute_payload"``: the handler gets it as ``payload``, the object itself."""
        payload = {"shard": 7}
        seen = []

        def compute_handler(obj, **kwargs):
            seen.append((obj.name, kwargs))
            return self.ray.ref(None)

        self.run_pool(
            ["a"],
            self.logging_builder(
                available=False,
                shape=lambda ref: {"ref": ref, "compute_payload": payload},
            ),
            compute_handler=compute_handler,
        )
        self.assertEqual(seen, [("a", {"payload": payload})])
        self.assertIs(seen[0][1]["payload"], payload)

    def test_a_dict_without_a_compute_payload_passes_no_payload(self):
        """R4, without ``"compute_payload"``."""
        self.run_pool(
            ["a"],
            self.logging_builder(available=False, shape=lambda ref: {"ref": ref}),
        )
        self.assertEqual(
            [e for e in self.ray.log if e[0] == "compute"], [("compute", "a", {})]
        )

    def test_a_bare_object_ref_is_enqueued(self):
        """R5."""
        self.run_pool(
            ["a"],
            self.logging_builder(),
            post_handler=self.recording_handler("post"),
            **LOOKUP_ONLY,
        )
        self.assertEqual(self.post_names(), ["a"])
        self.assertEqual(self.ray.wait_calls, [(1, 1)])


class TestRefusedReturns(BuilderTestCase):
    """R6: anything that is not None, a sequence, a ref, or a dict with ``"ref"``."""

    def assert_refused(self, returned, type_name, contents):
        with self.assertRaises(RuntimeError) as caught:
            self.run_pool(["a"], lambda item: returned, **LOOKUP_ONLY)
        self.assertEqual(
            str(caught.exception),
            f'could not interpret output from task builder (object type="{type_name}", '
            f"contents={contents})",
        )

    def test_an_int_is_refused(self):
        self.assert_refused(5, "int", "5")

    def test_a_string_is_refused(self):
        self.assert_refused("abc", "str", "abc")

    def test_a_dict_without_ref_is_refused(self):
        self.assert_refused({"x": 1}, "dict", "{'x': 1}")

    def test_a_nested_list_is_refused(self):
        inner = [self.ray.ref(Work("a"))]
        self.assert_refused([inner], "list", str(inner))

    def test_a_refused_element_of_a_sequence_is_refused(self):
        self.assert_refused((self.ray.ref(Work("a")), 7), "int", "7")


class TestNoneReturns(BuilderTestCase):
    def test_none_from_every_builder_enqueues_nothing_and_waits_on_nothing(self):
        """R7 and R9: ``ray.wait([], num_returns=0)``, which Ray accepts."""
        pool, lines = self.run_pool(
            [1, 2, 3],
            lambda item: None,
            post_handler=self.recording_handler("post"),
            **LOOKUP_ONLY,
        )
        self.assertEqual(self.ray.wait_calls, [(0, 0)])
        self.assertEqual(self.logged("post"), [])
        self.assertEqual(lines, [])

    def test_none_for_some_items_enqueues_the_others(self):
        """R7."""
        builder = self.logging_builder()
        self.run_pool(
            [1, 2, 3, 4],
            lambda item: None if item % 2 else builder(item),
            post_handler=self.recording_handler("post"),
            **LOOKUP_ONLY,
        )
        self.assertEqual(self.post_names(), [2, 4])

    def test_none_with_store_results_raises(self):
        """R7, with ``store_results``."""
        with self.assertRaises(RuntimeError) as caught:
            self.run_pool([1], lambda item: None, store_results=True, **LOOKUP_ONLY)
        self.assertEqual(str(caught.exception), NONE_WITH_STORE_RESULTS)


class TestSequenceReturns(BuilderTestCase):
    def test_a_list_a_tuple_and_a_set_are_each_enqueued_element_by_element(self):
        """R8: each element through R4-R5."""
        for kind in (list, tuple, set):
            with self.subTest(kind=kind.__name__):
                self.ray.log.clear()

                def builder(item):
                    first = self.ray.ref(Work(f"{item}-1", available=True))
                    second = self.ray.ref(Work(f"{item}-2", available=True))
                    if kind is set:
                        return {first, second}
                    return kind([first, {"ref": second}])

                self.run_pool(
                    ["x", "y"],
                    builder,
                    post_handler=self.recording_handler("post"),
                    **LOOKUP_ONLY,
                )
                self.assertEqual(
                    sorted(self.post_names()), ["x-1", "x-2", "y-1", "y-2"]
                )

    def test_a_sequence_element_carries_its_compute_payload(self):
        """R8 with R4: an element's ``"compute_payload"`` reaches its compute."""

        def builder(item):
            return [
                {"ref": self.ray.ref(Work(f"{item}-p")), "compute_payload": "P"},
                self.ray.ref(Work(f"{item}-q")),
            ]

        self.run_pool(["x"], builder)
        self.assertEqual(
            [e for e in self.ray.log if e[0] == "compute"],
            [("compute", "x-p", {"payload": "P"}), ("compute", "x-q", {})],
        )

    def test_an_empty_sequence_enqueues_nothing(self):
        """R8."""
        self.run_pool([1, 2], lambda item: [], **LOOKUP_ONLY)
        self.assertEqual(self.ray.wait_calls, [(0, 0)])

    def test_a_sequence_with_store_results_raises(self):
        """R8, with ``store_results``."""
        for kind in (list, tuple, set):
            with self.subTest(kind=kind.__name__):
                with self.assertRaises(RuntimeError) as caught:
                    self.run_pool(
                        [1],
                        lambda item: kind([self.ray.ref(Work(item))]),
                        store_results=True,
                        **LOOKUP_ONLY,
                    )
                self.assertEqual(str(caught.exception), MANY_WITH_STORE_RESULTS)


if __name__ == "__main__":
    unittest.main()
