"""
Faults 1-4 of the extraction campaign's board, each pinned **as it behaves**.

These tests pin the faults, not the intended behaviour. Each fails once its fault is fixed: prompt
04 fixes them, and inverts and renames these tests as it does. Fault 5 (the constructor's messages
say "maker") is pinned by ``test_construction``'s message assertions.
"""

import traceback
import unittest

from raypoolkit.tests.standins import PoolTestCase, Work


def raised_by(expected, call, *args, **kwargs):
    """
    Call ``call`` and return the ``expected`` exception it raises, with the source text of the
    line in the pool module that raised it. (``assertRaises`` drops the traceback, so this keeps
    it.) Anything else raised propagates; no exception is an ``AssertionError``.
    """
    try:
        call(*args, **kwargs)
    except expected as exception:
        frames = [
            frame
            for frame in traceback.extract_tb(exception.__traceback__)
            if frame.filename.endswith("RayWorkPool.py")
        ]
        return exception, (frames[-1].line if frames else None)
    raise AssertionError(f"{expected.__name__} not raised")


class TestInheritedFaults(PoolTestCase):
    def test_fault_in_flight_work_is_keyed_on_a_bound_method(self):
        """
        Pins ``[00-in-flight-work-is-keyed-on-a-bound-method]``, the fault, not the intended
        behaviour.

        The pool keys its in-flight work on ``ref.hex``, the bound method. When ``ray.wait``
        returns refs equal to, but distinct from, those it was given, the first completed lookup's
        key is not found: ``KeyError`` from ``item_type, payload = self._data[ref.hex]``.
        """
        self.ray.fresh_refs = True
        _, line = raised_by(
            KeyError,
            self.run_pool,
            ["a"],
            self.work_builder(available=True),
            compute_handler=None,
            persist_handler=None,
        )
        self.assertEqual(line, "item_type, payload = self._data[ref.hex]")
        self.assertEqual(self.ray.wait_calls, [(1, 1)])

    def test_fault_post_handler_after_persist_gets_the_unpersisted_object(self):
        """
        Pins ``[00-a-post-handler-after-persist-gets-the-unpersisted-object]``, the fault, not the
        intended behaviour.

        With no validation handler, the post handler at the store exit (exit 4) is given the
        object from before the persist, whose ``store_id`` is ``None``, while ``results`` holds the
        persisted object the datastore returned.
        """
        pool, _ = self.run_pool(
            ["a"],
            self.work_builder(available=False),
            post_handler=self.recording_handler("post"),
            store_results=True,
        )
        (given,) = self.logged("post")
        self.assertEqual(given.name, "a")
        self.assertIsNone(given.store_id)
        self.assertEqual(pool.results[0].store_id, 1001)
        self.assertIsNot(pool.results[0], given)

    def test_fault_store_results_sizes_from_len_of_the_task_list(self):
        """
        Pins ``[00-store-results-sizes-from-len-of-the-task-list]``, the fault, not the intended
        behaviour.

        With ``store_results=True`` the constructor sizes ``results`` from ``len(task_list)``, so
        a generator raises ``TypeError`` at construction. Without ``store_results`` the same
        generator runs.
        """
        _, line = raised_by(
            TypeError,
            self.make_pool,
            (item for item in ["a", "b"]),
            self.work_builder(available=True),
            compute_handler=None,
            persist_handler=None,
            store_results=True,
        )
        self.assertEqual(line, "self.results = [None for _ in range(len(task_list))]")

        self.run_pool(
            (item for item in ["a", "b"]),
            self.work_builder(available=True),
            compute_handler=None,
            persist_handler=None,
            post_handler=self.recording_handler("post"),
        )
        self.assertEqual([obj.name for obj in self.logged("post")], ["a", "b"])

    def test_fault_persist_handler_without_compute_raises_runtime_warning(self):
        """
        Pins ``[00-the-constructor-checks-its-handlers-unevenly]``, the fault, not the intended
        behaviour.

        ``compute_handler=None`` with the default persist handler raises ``RuntimeWarning``, an
        exception, at construction; so a lookup-only pool must pass ``persist_handler=None``.
        """
        with self.assertRaises(RuntimeWarning):
            self.make_pool(["a"], self.work_builder(), compute_handler=None)

    def test_fault_store_handler_none_with_compute_fails_at_first_compute(self):
        """
        Pins ``[00-the-constructor-checks-its-handlers-unevenly]``, the fault, not the intended
        behaviour.

        ``store_handler=None`` with a compute handler is not checked: the pool constructs, then
        raises ``TypeError`` when the first compute completes and the pool calls the store handler.
        """
        pool, _ = self.make_pool(
            ["a"], self.work_builder(available=False), store_handler=None
        )
        _, line = raised_by(TypeError, self.run_existing, pool)
        self.assertEqual(line, "self._store_handler(obj, self._pool)")
        # the lookup and the compute completed; the persist never ran
        self.assertEqual(self.ray.wait_calls, [(1, 1), (1, 1)])
        self.assertEqual(self.datastore.calls, [])


if __name__ == "__main__":
    unittest.main()
