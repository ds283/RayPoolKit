"""
The constructor: its handler checks and its size checks, with their exception and messages
exactly as they are; the three default handlers; ``results``; the banner; and the attributes not
set when not asked for.
"""

import unittest

from raypoolkit.tests.standins import PoolTestCase, Work

COMPUTE_PATH_ARGUMENT_WITHOUT_COMPUTE = "No compute handler was supplied, so {name} would never be called; leave it out, or pass None"
NONE_WITH_COMPUTE = "A compute handler was supplied, so {name} must not be None; leave it out to use the default"
SIZE_BELOW_ONE = "{name} must be at least 1, not {value!r}"

COMPUTE_PATH_ARGUMENTS = (
    "store_handler",
    "persist_handler",
    "validation_handler",
    "label_builder",
)
SIZES = ("create_batch_size", "process_batch_size", "max_task_queue")


class TestHandlerChecks(PoolTestCase):
    def test_a_compute_handler_with_persist_handler_none_raises_value_error(self):
        """C1."""
        with self.assertRaises(ValueError) as caught:
            self.make_pool([1], self.work_builder(), persist_handler=None)
        self.assertIs(type(caught.exception), ValueError)
        self.assertEqual(
            str(caught.exception), NONE_WITH_COMPUTE.format(name="persist_handler")
        )

    def test_a_compute_handler_with_store_handler_none_raises_value_error(self):
        """C5."""
        with self.assertRaises(ValueError) as caught:
            self.make_pool([1], self.work_builder(), store_handler=None)
        self.assertIs(type(caught.exception), ValueError)
        self.assertEqual(
            str(caught.exception), NONE_WITH_COMPUTE.format(name="store_handler")
        )

    def test_an_explicit_compute_path_argument_without_a_compute_handler_raises_value_error(
        self,
    ):
        """
        C2: each of the four arguments only a compute handler would use, given a callable with
        ``compute_handler=None``, is refused, and the message names it.
        """
        for name in COMPUTE_PATH_ARGUMENTS:
            with self.subTest(argument=name):
                with self.assertRaises(ValueError) as caught:
                    self.make_pool(
                        [1],
                        self.work_builder(),
                        compute_handler=None,
                        **{name: lambda *args, **kwargs: None},
                    )
                self.assertIs(type(caught.exception), ValueError)
                self.assertEqual(
                    str(caught.exception),
                    COMPUTE_PATH_ARGUMENT_WITHOUT_COMPUTE.format(name=name),
                )

    def test_a_pool_without_a_compute_handler_constructs_however_it_is_spelled(self):
        """
        C6: with ``compute_handler=None``, the default store and persist handlers are not used,
        whether each is left out or passed as ``None``; the queued message has no store segment.
        """
        spellings = {
            "nothing else": {},
            "persist_handler=None": {"persist_handler": None},
            "store_handler=None": {"store_handler": None},
            "both None": {"store_handler": None, "persist_handler": None},
        }
        for name, kwargs in spellings.items():
            with self.subTest(spelling=name):
                pool, lines = self.make_pool(
                    [1], self.work_builder(), compute_handler=None, **kwargs
                )
                self.assertEqual(pool._build_queued_status_message(), "0 lookup")
                self.assertEqual(lines, [])

    def test_neither_handler_constructs(self):
        pool, lines = self.make_pool(
            [1], self.work_builder(), compute_handler=None, persist_handler=None
        )
        self.assertEqual(lines, [])

    def test_both_handlers_construct(self):
        pool, lines = self.make_pool([1], self.work_builder())
        self.assertEqual(lines, [])


class TestSizeChecks(PoolTestCase):
    def test_a_size_below_one_raises_value_error(self):
        """C7: each size at 0 and at -1 is refused, and the message names it; at 1 it constructs."""
        for name in SIZES:
            for value in (0, -1):
                with self.subTest(size=name, value=value):
                    with self.assertRaises(ValueError) as caught:
                        self.make_pool([1], self.work_builder(), **{name: value})
                    self.assertIs(type(caught.exception), ValueError)
                    self.assertEqual(
                        str(caught.exception),
                        SIZE_BELOW_ONE.format(name=name, value=value),
                    )
            with self.subTest(size=name, value=1):
                pool, lines = self.make_pool([1], self.work_builder(), **{name: 1})
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
