"""
The constructor: its two handler checks, with their exceptions and messages exactly as they are;
the three default handlers; ``results``; the banner; and the attributes not set when not asked for.

The messages say "maker" for "handler". That is the board's
``[00-messages-say-maker-and-the-module-has-no-licence-header]``, pinned here as it is; prompt 04
rewords them and changes these assertions.
"""

import unittest

from raypoolkit.tests.standins import PoolTestCase, Work

COMPUTE_WITHOUT_PERSIST = (
    "If a compute maker is supplied, a persist maker must also be supplied to serialize the "
    "result of the computation"
)
PERSIST_WITHOUT_COMPUTE = (
    "No compute maker was supplied, but a persist maker was provided. This will have no effect "
    "because there will be no compute results to store"
)


class TestHandlerChecks(PoolTestCase):
    def test_compute_handler_without_persist_handler_raises_runtime_error(self):
        """C1."""
        with self.assertRaises(RuntimeError) as caught:
            self.make_pool([1], self.work_builder(), persist_handler=None)
        self.assertIs(type(caught.exception), RuntimeError)
        self.assertEqual(str(caught.exception), COMPUTE_WITHOUT_PERSIST)

    def test_persist_handler_without_compute_handler_raises_runtime_warning(self):
        """C2 (the board's fault 4 pins the same in ``test_inherited_faults``)."""
        with self.assertRaises(RuntimeWarning) as caught:
            self.make_pool([1], self.work_builder(), compute_handler=None)
        self.assertIs(type(caught.exception), RuntimeWarning)
        self.assertEqual(str(caught.exception), PERSIST_WITHOUT_COMPUTE)

    def test_neither_handler_constructs(self):
        pool, lines = self.make_pool(
            [1], self.work_builder(), compute_handler=None, persist_handler=None
        )
        self.assertEqual(lines, [])

    def test_both_handlers_construct(self):
        pool, lines = self.make_pool([1], self.work_builder())
        self.assertEqual(lines, [])


class TestDefaultHandlers(PoolTestCase):
    """Each default handler, reached through a pool built with its default."""

    def test_the_default_compute_handler_calls_compute_with_the_arguments(self):
        self.run_pool(
            ["a"],
            self.work_builder(available=False),
            label_builder=lambda obj: f"label-{obj.name}",
        )
        self.assertEqual(
            [e for e in self.ray.log if e[0] == "compute"],
            [("compute", "a", {"label": "label-a"})],
        )

    def test_the_default_store_handler_calls_store(self):
        self.run_pool(["a"], self.work_builder(available=False))
        self.assertIn(("store", "a"), self.ray.log)
        # the store handler runs after the compute and before the persist
        names = [e[0] for e in self.ray.log if e[0] != "wait"]
        self.assertEqual(names, ["compute", "store", "object_store"])

    def test_the_default_persist_handler_calls_object_store_on_the_pool(self):
        pool, _ = self.run_pool(
            ["a"], self.work_builder(available=False), store_results=True
        )
        self.assertEqual([obj.name for obj in self.datastore.calls], ["a"])
        # the object handed to object_store is the one store() ran on
        self.assertTrue(self.datastore.calls[0].stored)
        self.assertEqual(pool.results[0].store_id, 1001)


class TestResultsAndTitle(PoolTestCase):
    def test_store_results_sizes_results_and_fills_it_with_none(self):
        """C3."""
        pool, _ = self.make_pool([1, 2, 3], self.work_builder(), store_results=True)
        self.assertEqual(pool.results, [None, None, None])

    def test_results_is_not_set_without_store_results(self):
        pool, _ = self.run_pool([1, 2], self.work_builder(available=True))
        self.assertFalse(hasattr(pool, "results"))

    def test_a_title_prints_the_banner_at_construction(self):
        """C4: a blank line, then the title."""
        pool, lines = self.make_pool([1], self.work_builder(), title="The title")
        self.assertEqual(lines, ["", "** The title"])

    def test_no_title_prints_nothing(self):
        pool, lines = self.run_pool(
            [1, 2], self.work_builder(available=False), store_results=True
        )
        self.assertEqual(lines, [])

    def test_total_time_is_set_only_with_a_title(self):
        untitled, _ = self.run_pool([1], self.work_builder(available=True))
        self.assertFalse(hasattr(untitled, "total_time"))
        titled, _ = self.run_pool([1], self.work_builder(available=True), title="T")
        self.assertTrue(hasattr(titled, "total_time"))


if __name__ == "__main__":
    unittest.main()
