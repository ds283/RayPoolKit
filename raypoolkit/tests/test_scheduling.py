"""
Scheduling: ``max_task_queue``, ``create_batch_size`` and ``process_batch_size``, read from the
stand-in's ``wait_calls`` and from the builder's calls; and ``results``, which keeps the task
list's order whatever order the tasks complete in.

No test here builds a pool with any of the three sizes below 1: such a pool never finishes (or,
with ``process_batch_size=0``, makes ``ray.wait`` raise), which prompt 02's log records as an
observation, not a behaviour to pin.
"""

import unittest

from raypoolkit.tests.standins import PoolTestCase, Work

LOOKUP_ONLY = {"compute_handler": None, "persist_handler": None}


class SchedulingTestCase(PoolTestCase):
    def counting_builder(self, available=True):
        def builder(item):
            self.ray.log.append(("build", item))
            return self.ray.ref(Work(item, available=available))

        return builder

    def events(self):
        return [e for e in self.ray.log if e[0] in ("build", "wait")]

    def builds(self):
        return [e[1] for e in self.ray.log if e[0] == "build"]


class TestSizes(SchedulingTestCase):
    def test_max_task_queue_holds_back_the_next_batch_until_the_queue_drains_below_it(
        self,
    ):
        self.run_pool(
            [1, 2, 3, 4, 5, 6],
            self.counting_builder(),
            max_task_queue=1,
            create_batch_size=3,
            **LOOKUP_ONLY,
        )
        self.assertEqual(
            self.events(),
            [
                ("build", 1),
                ("build", 2),
                ("build", 3),
                ("wait", 3, 1),
                ("wait", 2, 1),
                ("wait", 1, 1),
                ("build", 4),
                ("build", 5),
                ("build", 6),
                ("wait", 3, 1),
                ("wait", 2, 1),
                ("wait", 1, 1),
            ],
        )

    def test_the_default_sizes_build_five_at_a_time_and_process_one_at_a_time(self):
        self.run_pool(list(range(7)), self.counting_builder(), **LOOKUP_ONLY)
        self.assertEqual(
            self.events()[:7],
            [("build", i) for i in range(5)] + [("wait", 5, 1)] + [("build", 5)],
        )
        self.assertEqual(self.builds(), list(range(7)))
        self.assertEqual(len(self.ray.wait_calls), 7)

    def test_process_batch_size_sets_how_many_tasks_each_wait_returns(self):
        self.run_pool(
            [1, 2, 3, 4, 5],
            self.counting_builder(),
            process_batch_size=2,
            **LOOKUP_ONLY,
        )
        self.assertEqual(self.ray.wait_calls, [(5, 2), (3, 2), (1, 1)])

    def test_process_batch_size_applies_to_every_stage(self):
        """Lookups, computes and stores of two items are each processed two at a time."""
        self.run_pool(
            [1, 2], self.counting_builder(available=False), process_batch_size=2
        )
        self.assertEqual(self.ray.wait_calls, [(2, 2), (2, 2), (2, 2)])

    def test_one_builder_call_per_item(self):
        self.run_pool(
            list(range(12)),
            self.counting_builder(),
            create_batch_size=4,
            max_task_queue=3,
            process_batch_size=2,
            **LOOKUP_ONLY,
        )
        self.assertEqual(self.builds(), list(range(12)))


class TestResultsOrder(SchedulingTestCase):
    def test_results_keep_task_order_when_lookups_complete_in_reverse(self):
        self.ray.order = lambda refs: list(reversed(refs))
        pool, _ = self.run_pool(
            ["a", "b", "c", "d", "e"],
            self.counting_builder(),
            post_handler=self.recording_handler("post"),
            process_batch_size=2,
            store_results=True,
            **LOOKUP_ONLY,
        )
        completed = [obj.name for obj in self.logged("post")]
        self.assertNotEqual(completed, ["a", "b", "c", "d", "e"])
        self.assertEqual(sorted(completed), ["a", "b", "c", "d", "e"])
        self.assertEqual([obj.name for obj in pool.results], ["a", "b", "c", "d", "e"])

    def test_results_keep_task_order_through_compute_and_store(self):
        self.ray.order = lambda refs: list(reversed(refs))
        pool, _ = self.run_pool(
            ["a", "b", "c", "d"],
            self.counting_builder(available=False),
            post_handler=self.recording_handler("post"),
            process_batch_size=3,
            create_batch_size=2,
            store_results=True,
        )
        completed = [obj.name for obj in self.logged("post")]
        self.assertNotEqual(completed, ["a", "b", "c", "d"])
        self.assertEqual([obj.name for obj in pool.results], ["a", "b", "c", "d"])
        self.assertEqual(
            sorted(obj.store_id for obj in pool.results), [1001, 1002, 1003, 1004]
        )


if __name__ == "__main__":
    unittest.main()
