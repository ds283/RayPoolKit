"""
The stand-ins of ``standins.py``, tested: they refuse what Ray refuses, with Ray's exception types,
copy as Ray copies, keep time as the pool's lines need, and cannot reach real Ray.
"""

import pickle
import sys
import unittest
from datetime import datetime

import ray
from ray import ObjectRef

from raypoolkit.tests.standins import (
    DEFAULT_MAX_WAIT_CALLS,
    PoolTestCase,
    RayInitCalled,
    ScriptedClock,
    StandinDatastorePool,
    StandinRay,
    Work,
)


class TestRef(PoolTestCase):
    def test_ref_mints_distinct_real_object_refs_of_28_bytes(self):
        a = self.ray.ref("a")
        b = self.ray.ref("b")
        self.assertIsInstance(a, ObjectRef)
        self.assertEqual(len(a.binary()), 28)
        self.assertNotEqual(a, b)
        self.assertEqual(self.ray.value_of(a), "a")
        self.assertEqual(self.ray.value_of(b), "b")


class TestWaitContract(PoolTestCase):
    """Ray's ``wait`` contract, clause by clause, with Ray's exception types."""

    def test_a_single_ref_is_a_type_error(self):
        with self.assertRaises(TypeError):
            self.ray.wait(self.ray.ref(1))

    def test_an_argument_that_is_not_a_list_is_a_type_error(self):
        ref = self.ray.ref(1)
        with self.assertRaises(TypeError):
            self.ray.wait((ref,))

    def test_an_element_that_is_not_a_ref_is_a_type_error(self):
        with self.assertRaises(TypeError):
            self.ray.wait([self.ray.ref(1), "not a ref"])

    def test_a_negative_timeout_is_a_value_error(self):
        with self.assertRaises(ValueError):
            self.ray.wait([self.ray.ref(1)], timeout=-1)

    def test_an_empty_list_returns_two_empty_lists_before_num_returns_is_checked(self):
        self.assertEqual(self.ray.wait([], num_returns=0), ([], []))
        self.assertEqual(self.ray.wait([], num_returns=5), ([], []))
        self.assertEqual(self.ray.wait([], num_returns=-1), ([], []))

    def test_equal_refs_are_duplicates_and_a_value_error(self):
        ref = self.ray.ref(1)
        twin = ObjectRef(ref.binary())
        self.assertIsNot(ref, twin)
        with self.assertRaises(ValueError):
            self.ray.wait([ref, twin])

    def test_num_returns_below_one_is_a_value_error(self):
        refs = [self.ray.ref(1), self.ray.ref(2)]
        for num_returns in (0, -1):
            with self.subTest(num_returns=num_returns):
                with self.assertRaises(ValueError):
                    self.ray.wait(refs, num_returns=num_returns)

    def test_num_returns_above_the_number_of_refs_is_a_value_error(self):
        refs = [self.ray.ref(1), self.ray.ref(2)]
        with self.assertRaises(ValueError):
            self.ray.wait(refs, num_returns=3)

    def test_it_returns_ready_and_remaining_in_input_order_by_default(self):
        refs = [self.ray.ref(i) for i in range(4)]
        ready, remaining = self.ray.wait(list(refs), num_returns=3)
        self.assertEqual(ready, refs[:3])
        self.assertEqual(remaining, refs[3:])
        # the very objects it was given
        for got, given in zip(ready + remaining, refs):
            self.assertIs(got, given)

    def test_order_controls_which_refs_are_ready(self):
        refs = [self.ray.ref(i) for i in range(3)]
        self.ray.order = lambda rs: list(reversed(rs))
        ready, remaining = self.ray.wait(list(refs), num_returns=1)
        self.assertEqual(ready, [refs[2]])
        self.assertEqual(remaining, [refs[1], refs[0]])

    def test_order_must_return_the_refs_it_was_given(self):
        refs = [self.ray.ref(i) for i in range(3)]
        self.ray.order = lambda rs: rs[:2]
        with self.assertRaises(AssertionError):
            self.ray.wait(refs)

    def test_each_call_is_recorded(self):
        refs = [self.ray.ref(i) for i in range(3)]
        self.ray.wait(refs, num_returns=2)
        self.ray.wait([], num_returns=0)
        self.assertEqual(self.ray.wait_calls, [(3, 2), (0, 0)])
        self.assertEqual(self.ray.log, [("wait", 3, 2), ("wait", 0, 0)])

    def test_fresh_refs_returns_equal_but_distinct_refs(self):
        refs = [self.ray.ref(i) for i in range(2)]
        self.ray.fresh_refs = True
        ready, remaining = self.ray.wait(list(refs), num_returns=1)
        for got, given in zip(ready + remaining, refs):
            self.assertEqual(got, given)
            self.assertIsNot(got, given)
            # the bound method the pool keys on differs; the hex string does not
            self.assertNotEqual(got.hex, given.hex)
            self.assertEqual(got.hex(), given.hex())

    def test_wait_raises_past_its_call_cap(self):
        self.assertEqual(DEFAULT_MAX_WAIT_CALLS, 1000)
        standin = StandinRay(max_wait_calls=3)
        for _ in range(3):
            standin.wait([], num_returns=0)
        with self.assertRaisesRegex(RuntimeError, r"called 4 times, past its cap of 3"):
            standin.wait([], num_returns=0)


class TestGet(PoolTestCase):
    def test_get_returns_the_value_by_value(self):
        value = Work("w", available=True)
        ref = self.ray.ref(value)
        got = self.ray.get(ref)
        self.assertIsNot(got, value)
        self.assertEqual((got.name, got.available), ("w", True))
        # a mutation of the copy does not reach the table
        got.available = False
        self.assertTrue(self.ray.get(ref).available)
        self.assertEqual(self.ray.get_calls, [ref, ref])

    def test_get_resolves_an_equal_ref_built_from_the_same_bytes(self):
        ref = self.ray.ref("value")
        self.assertEqual(self.ray.get(ObjectRef(ref.binary())), "value")

    def test_get_of_a_ref_it_did_not_mint_names_the_ref(self):
        stranger = ObjectRef((10**9).to_bytes(28, "big"))
        with self.assertRaises(KeyError) as caught:
            self.ray.get(stranger)
        self.assertIn(stranger.hex(), str(caught.exception))

    def test_get_refuses_a_list(self):
        with self.assertRaises(TypeError):
            self.ray.get([self.ray.ref(1)])

    def test_namespace_has_wait_and_get_and_nothing_else(self):
        namespace = self.ray.namespace()
        self.assertEqual(sorted(vars(namespace)), ["get", "wait"])
        with self.assertRaises(AttributeError):
            namespace.put


class TestScriptedClock(unittest.TestCase):
    def test_perf_counter_advances_by_its_step_on_every_call(self):
        clock = ScriptedClock()
        self.assertEqual([clock.perf_counter() for _ in range(3)], [1, 2, 3])
        clock.step = 5
        self.assertEqual(clock.perf_counter(), 8)
        self.assertEqual(clock.perf_counter_calls, 4)

    def test_advance_jumps_without_a_call(self):
        clock = ScriptedClock()
        clock.advance(100)
        self.assertEqual(clock.perf_counter(), 101)
        self.assertEqual(clock.perf_counter_calls, 1)

    def test_now_is_naive_base_plus_the_reading_and_does_not_advance(self):
        clock = ScriptedClock()
        clock.perf_counter()
        clock.perf_counter()
        now = clock.now()
        self.assertIsNone(now.tzinfo)
        self.assertEqual(now, datetime(2026, 10, 10, 12, 0, 2))
        self.assertEqual(clock.now(), now)
        self.assertEqual(clock.reading, 2)
        # with no offset, %z prints nothing
        self.assertEqual(f"{now:%Y-%m-%d %H:%M:%S%z}", "2026-10-10 12:00:02")
        self.assertEqual(clock.stamp(2), "2026-10-10 12:00:02")


class TestWorkObjectsAndDatastore(PoolTestCase):
    def test_work_objects_pickle(self):
        work = Work("w")
        copy = pickle.loads(pickle.dumps(work))
        self.assertEqual((copy.name, copy.available, copy.store_id), ("w", False, None))

    def test_compute_records_its_arguments_and_returns_a_minted_ref(self):
        work = Work("w")
        ref = work.compute(label="L", payload=3)
        self.assertIsInstance(ref, ObjectRef)
        self.assertEqual(work.compute_kwargs, {"label": "L", "payload": 3})
        self.assertEqual(self.ray.log, [("compute", "w", {"label": "L", "payload": 3})])

    def test_store_records_that_it_ran(self):
        work = Work("w")
        work.store()
        self.assertTrue(work.stored)
        self.assertEqual(self.ray.log, [("store", "w")])

    def test_object_store_returns_a_ref_to_a_persisted_copy(self):
        work = Work("w")
        ref = self.datastore.object_store(work)
        persisted = self.ray.get(ref)
        self.assertEqual((persisted.store_id, persisted.available), (1001, True))
        self.assertIsNone(work.store_id)
        self.assertFalse(work.available)
        self.assertEqual(self.datastore.calls, [work])

    def test_object_store_can_return_an_unavailable_copy(self):
        datastore = StandinDatastorePool(available_after_store=False)
        persisted = self.ray.get(datastore.object_store(Work("w")))
        self.assertEqual((persisted.store_id, persisted.available), (1001, False))


class TestRayInitGuard(PoolTestCase):
    """No test can start Ray: ``ray.init`` is refused, and the pool module's names are stand-ins."""

    def test_real_get_and_wait_reach_the_refused_ray_init(self):
        ref = self.ray.ref(1)
        with self.assertRaises(RayInitCalled):
            ray.get(ref)
        with self.assertRaises(RayInitCalled):
            ray.wait([ref])
        # and again: the auto-init lock was released
        with self.assertRaises(RayInitCalled):
            ray.get(ref)
        self.assertFalse(ray.is_initialized())

    def test_the_pool_module_sees_the_stand_ins(self):
        module = sys.modules["raypoolkit.RayWorkPool"]
        self.assertEqual(sorted(vars(module.ray)), ["get", "wait"])
        self.assertEqual(sorted(vars(module.time)), ["perf_counter"])
        self.assertEqual(sorted(vars(module.datetime)), ["now"])
        self.assertIs(module.ObjectRef, ObjectRef)


if __name__ == "__main__":
    unittest.main()
