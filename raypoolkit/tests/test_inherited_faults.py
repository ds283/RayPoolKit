"""
Faults 1-5 of the extraction campaign's board, each now a guard of its fix.

Prompt 02 pinned each fault as it behaved; prompt 04 fixed them and turned each pin into a test of
the fixed behaviour, which the unfixed module (``v0.1.0``) fails. The issues are in the board's §4
(Resolved issues). Fault 5's messages are checked by ``test_construction``'s message assertions;
its licence header is checked here.
"""

import pathlib
import unittest

import raypoolkit
from raypoolkit.tests.standins import Blob, PoolTestCase, StandinDatastorePool

# The licence header every package module opens with, and the blank line after it (decision U11).
LICENCE_HEADER = (
    "# (c) University of Sussex 2026\n"
    "# Created by David Seery\n"
    "#\n"
    '# Licensed under the Apache License, Version 2.0 (the "License");\n'
    "# you may not use this file except in compliance with the License.\n"
    "# You may obtain a copy of the License at\n"
    "#\n"
    "#    http://www.apache.org/licenses/LICENSE-2.0\n"
    "#\n"
    "# Unless required by applicable law or agreed to in writing, software\n"
    '# distributed under the License is distributed on an "AS IS" BASIS,\n'
    "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
    "# See the License for the specific language governing permissions and\n"
    "# limitations under the License.\n"
    "\n"
)

PACKAGE_MODULES = ("RayWorkPool.py", "_timing.py", "contract.py", "__init__.py")

STORE_HANDLER_NONE_WITH_COMPUTE = (
    "A compute handler was supplied, so store_handler must not be None; leave it out to use "
    "the default"
)


class TestInheritedFaults(PoolTestCase):
    def test_fresh_refs_from_wait_complete_every_path(self):
        """
        Guards the fix of ``[00-in-flight-work-is-keyed-on-a-bound-method]`` (resolved).

        With the stand-in's ``fresh_refs``, ``ray.wait`` returns refs equal to, but distinct from,
        those it was given. Every path runs to completion with the expected ``results``. The
        unfixed module keyed its in-flight work on ``ref.hex``, the bound method, so the first
        completed task raised ``KeyError`` from ``item_type, payload = self._data[ref.hex]``.
        """
        lookup_only = {"compute_handler": None, "persist_handler": None}
        paths = {
            "lookup only": (
                self.work_builder(available=True),
                dict(lookup_only),
                [("a", True, None), ("b", True, None)],
            ),
            "availability handler": (
                self.work_builder(available=True),
                dict(
                    lookup_only,
                    available_handler=self.ref_returning_handler("available"),
                ),
                [("a", True, None), ("b", True, None)],
            ),
            "compute with validation": (
                self.work_builder(available=False),
                {"validation_handler": self.ref_returning_handler("validate")},
                [("a", True, 1001), ("b", True, 1002)],
            ),
            "compute without validation": (
                self.work_builder(available=False),
                {},
                [("a", True, 1001), ("b", True, 1002)],
            ),
        }
        self.ray.fresh_refs = True
        for name, (builder, kwargs, expected) in paths.items():
            with self.subTest(path=name):
                self.datastore = StandinDatastorePool()
                pool, lines = self.run_pool(
                    ["a", "b"], builder, store_results=True, **kwargs
                )
                self.assertEqual(
                    [(obj.name, obj.available, obj.store_id) for obj in pool.results],
                    expected,
                )
                self.assertEqual(lines, [])

        with self.subTest(path="blobs"):
            pool, lines = self.run_pool(
                ["a", "b"],
                lambda item: self.ray.ref(Blob(item)),
                store_results=True,
                **lookup_only,
            )
            self.assertEqual([type(obj) for obj in pool.results], [Blob, Blob])
            self.assertEqual([obj.name for obj in pool.results], ["a", "b"])
            self.assertEqual(lines, [])

    def test_the_post_handler_after_persist_gets_the_persisted_object(self):
        """
        Guards the fix of ``[00-a-post-handler-after-persist-gets-the-unpersisted-object]``
        (resolved).

        With no validation handler, the post handler at the store exit (exit 4) is given the
        persisted object the datastore returned, with its ``store_id``, which is also the entry in
        ``results``. The unfixed module gave it the object from before the persist, whose
        ``store_id`` was ``None``.
        """
        pool, _ = self.run_pool(
            ["a"],
            self.work_builder(available=False),
            post_handler=self.recording_handler("post"),
            store_results=True,
        )
        (given,) = self.logged("post")
        self.assertEqual(given.name, "a")
        self.assertEqual(given.store_id, 1001)
        self.assertIs(pool.results[0], given)

    def test_store_results_accepts_a_generator_task_list(self):
        """
        Guards the fix of ``[00-store-results-sizes-from-len-of-the-task-list]`` (resolved).

        With ``store_results=True`` a generator ``task_list`` constructs, runs, and fills
        ``results`` in order. The unfixed module sized ``results`` from ``len(task_list)``, so a
        generator raised ``TypeError`` at construction.
        """
        pool, _ = self.run_pool(
            (item for item in ["a", "b", "c"]),
            self.work_builder(available=True),
            compute_handler=None,
            persist_handler=None,
            store_results=True,
        )
        self.assertEqual([obj.name for obj in pool.results], ["a", "b", "c"])

    def test_a_lookup_only_pool_needs_no_persist_handler(self):
        """
        Guards the fix of ``[00-the-constructor-checks-its-handlers-unevenly]`` (resolved), its
        first half.

        ``compute_handler=None`` alone constructs and runs: the default store and persist handlers
        apply only with a compute handler (decision U8), so the queued message has no store
        segment. The unfixed module raised ``RuntimeWarning``, an exception, at construction, so a
        lookup-only pool had to pass ``persist_handler=None``.
        """
        pool, _ = self.make_pool(
            ["a"], self.work_builder(available=True), compute_handler=None
        )
        self.assertEqual(pool._build_queued_status_message(), "0 lookup")
        self.run_existing(pool)
        self.assertEqual(self.ray.wait_calls, [(1, 1)])

    def test_store_handler_none_with_compute_is_refused_at_construction(self):
        """
        Guards the fix of ``[00-the-constructor-checks-its-handlers-unevenly]`` (resolved), its
        second half.

        ``store_handler=None`` with a compute handler raises ``ValueError`` at construction, before
        any work is waited on or stored. The unfixed module did not check it: the pool
        constructed, then raised ``TypeError`` when the first compute completed and it called the
        store handler.
        """
        with self.assertRaises(ValueError) as caught:
            self.make_pool(
                ["a"], self.work_builder(available=False), store_handler=None
            )
        self.assertIs(type(caught.exception), ValueError)
        self.assertEqual(str(caught.exception), STORE_HANDLER_NONE_WITH_COMPUTE)
        self.assertEqual(self.ray.wait_calls, [])
        self.assertEqual(self.datastore.calls, [])

    def test_every_package_module_carries_the_licence_header(self):
        """
        Guards the fix of ``[00-messages-say-maker-and-the-module-has-no-licence-header]``
        (resolved), its header.

        Each of the four package modules, found beside ``raypoolkit.__file__``, opens with the
        14-line Apache 2.0 header and a blank line (decision U11). The unfixed ``RayWorkPool.py``
        opened with ``import time``, and the other three had no header either.
        """
        package = pathlib.Path(raypoolkit.__file__).parent
        for name in PACKAGE_MODULES:
            with self.subTest(module=name):
                with open(package / name, encoding="utf-8") as module:
                    head = [module.readline() for _ in range(15)]
                self.assertEqual("".join(head), LICENCE_HEADER)


if __name__ == "__main__":
    unittest.main()
