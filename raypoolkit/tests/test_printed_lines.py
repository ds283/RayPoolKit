"""
The lines the pool prints, pinned word for word (decision U9).

**What the pool prints is part of its interface** (``CLAUDE.md``, "Releases"): a consumer parses
the banner, progress and completion lines, so a change to their wording or layout is a change to
the interface, made only by a prompt that says so and released under a new minor version.

Every test captures stdout and compares whole lines. The clock is the ``ScriptedClock``: its
reading starts at 0 and every ``perf_counter()`` call advances it by 1 s and returns the new
reading. The pool calls ``perf_counter()`` at construction (the start), on every pass of its loop,
after each notification, and at completion; ``datetime.now()`` returns the naive base
``2026-10-10 12:00:00`` plus the reading, so the stamp carries no UTC offset. The comment above
each expected block gives the readings it was derived from.

The pure functions ``format_time``, ``_readable_rate`` and ``_format_rates``, and the two status
messages, are also called directly (the white-box seam of prompt 02 §2.2), for the cases the
pool's run never reaches.
"""

import re
import unittest

from raypoolkit._timing import format_time
from raypoolkit.RayWorkPool import _format_rates, _readable_rate
from raypoolkit.tests.standins import PoolTestCase, StandinDatastorePool, Work

LOOKUP_ONLY = {"compute_handler": None, "persist_handler": None}
EVERY_PASS = {"notify_min_time_interval": 0, "notify_time_interval": 0}

SUFFIX = " (may be waiting for compute/store/validate tasks to finish)"
NO_COMPUTE = "      (no compute items were evaluated - all assets read from datastore)"

# The three patterns a consumer of this output is known to parse it with, copied as they are.
# Changing a line one of them matches changes the pool's interface.
BANNER_PATTERN = re.compile(r"^\s*(?:\*\*|>>)\s+(\S.*?)\s*$")
PROGRESS_PATTERN = re.compile(
    r"(\d+)/(\d+)\s+work items remaining\s*=\s*([\d.]+)%\s+complete"
)
COMPLETE_PATTERN = re.compile(r"ALL WORK ITEMS COMPLETE")


def progress(stamp_seconds, running, remaining, total, percent, suffix=False):
    line = (
        f"   -- 2026-10-10 12:00:{stamp_seconds:02d} ({running} running): "
        f"{remaining}/{total} work items remaining = {percent} complete"
    )
    return line + (SUFFIX if suffix else "")


class TestPureFunctions(unittest.TestCase):
    def test_format_time_at_its_edges(self):
        cases = {
            0.00499: "0.00499s",
            1: "1s",
            60: "60s",
            61: "1m 1s",
            125: "2m 5s",
            3600: "60m 0s",
            86400: "24h 0s",
            90061.25: "1d 1h 1m 1.25s",
        }
        for interval, expected in cases.items():
            with self.subTest(interval=interval):
                self.assertEqual(format_time(interval), expected)

    def test_readable_rate_units(self):
        """T1: ``/sec``, ``/min``, ``/hr``, ``/day``."""
        cases = {
            0: "0/day",
            0.01: "36/hr",
            0.2: "12/min",
            1: "60/min",
            10: "10/sec",
            12345.6: "1.235e+04/sec",
        }
        for rate, expected in cases.items():
            with self.subTest(rate=rate):
                self.assertEqual(_readable_rate(rate), expected)

    def test_format_rates(self):
        """T2: the interval rate needs a delta and a last value; the average needs a total."""
        self.assertEqual(_format_rates(10.0, 20.0, 5, 2), "18/min, avg 15/min")
        self.assertEqual(_format_rates(None, 2.0, 6, None), "avg 180/min")
        self.assertEqual(_format_rates(1.0, 2.0, 6, None), "avg 180/min")
        self.assertEqual(_format_rates(None, 2.0, 6, 3), "avg 180/min")
        self.assertEqual(_format_rates(10.0, None, 5, 2), "18/min")
        self.assertEqual(_format_rates(None, None, 3, None), "")


class TestStatusMessages(PoolTestCase):
    """Q1 and Q2: each optional segment, per handler set, called directly (§2.2's seam)."""

    HANDLER_SETS = {
        "lookup only": (LOOKUP_ONLY, ["lookup"]),
        "available": (
            dict(LOOKUP_ONLY, available_handler=lambda obj: None),
            ["lookup", "available"],
        ),
        "compute": ({}, ["lookup", "compute", "store"]),
        "every handler": (
            {
                "available_handler": lambda obj: None,
                "validation_handler": lambda obj: None,
            },
            ["lookup", "compute", "store", "available", "validation"],
        ),
        "validation only": (
            dict(LOOKUP_ONLY, validation_handler=lambda obj: None),
            ["lookup", "validation"],
        ),
    }

    def pool_for(self, kwargs):
        return self.make_pool([1], lambda item: None, **kwargs).pool

    def test_the_queued_message_has_a_segment_per_handler(self):
        """Q1."""
        for name, (kwargs, segments) in self.HANDLER_SETS.items():
            with self.subTest(handlers=name):
                pool = self.pool_for(kwargs)
                self.assertEqual(
                    pool._build_queued_status_message(),
                    ", ".join(f"0 {s}" for s in segments),
                )

    def test_the_completed_message_without_rates(self):
        """Q2, with no times: no parentheses."""
        for name, (kwargs, segments) in self.HANDLER_SETS.items():
            with self.subTest(handlers=name):
                pool = self.pool_for(kwargs)
                self.assertEqual(
                    pool._build_completed_status_message(),
                    ", ".join(f"0 {s}" for s in segments),
                )

    def test_the_completed_message_with_rates(self):
        """Q2, with a total and an interval but no last counts: the average alone."""
        for name, (kwargs, segments) in self.HANDLER_SETS.items():
            with self.subTest(handlers=name):
                pool = self.pool_for(kwargs)
                self.assertEqual(
                    pool._build_completed_status_message(
                        total_time_in_seconds=2.0, since_last_notify_in_seconds=1.0
                    ),
                    ", ".join(f"0 {s} (avg 0/day)" for s in segments),
                )


class TestProgressAndCompletion(PoolTestCase):
    def test_a_lookup_only_run_notifying_on_every_pass(self):
        """
        The banner, two progress pairs and the completion lines (C4, N2, N3, N4, N5, F1, F2).

        Readings: construction 1 (the start); pass 1 at 2, notified, then 3; pass 2 at 4,
        notified, then 5; completion at 6, so ``total_time`` is 5. Every item is built in the first
        batch, so ``0/2`` remain and 100% is printed with the suffix while work is in flight.
        """
        pool, lines = self.run_pool(
            ["a", "b"],
            self.work_builder(available=True),
            title="Stage one",
            **EVERY_PASS,
            **LOOKUP_ONLY,
        )
        self.assertEqual(
            lines,
            [
                "",
                "** Stage one",
                progress(2, "1s", 0, 2, "100.00%", suffix=True),
                "      inflight: 1 lookup | completed: 1 lookup (avg 60/min)",
                progress(4, "3s", 0, 2, "100.00%", suffix=True),
                "      inflight: 0 lookup | completed: 2 lookup (60/min, avg 40/min)",
                "   -- ALL WORK ITEMS COMPLETE in time 5s",
                "      Queue summary: 2 lookup (avg 24/min)",
                NO_COMPUTE,
            ],
        )
        self.assertEqual(pool.total_time, 5)

    def test_the_percentage_counts_items_whose_task_is_not_yet_built(self):
        """
        N3: one item built per pass, so 3, 2, 1 and 0 of 4 remain. N4: the suffix only at 100%.

        Readings: start 1; passes at 2, 4, 6, 8, each notified (then 3, 5, 7, 9); completion 10.
        """
        pool, lines = self.run_pool(
            [1, 2, 3, 4],
            self.work_builder(available=True),
            title="T",
            max_task_queue=1,
            create_batch_size=1,
            **EVERY_PASS,
            **LOOKUP_ONLY,
        )
        self.assertEqual(
            lines,
            [
                "",
                "** T",
                progress(2, "1s", 3, 4, "25.00%"),
                "      inflight: 0 lookup | completed: 1 lookup (avg 60/min)",
                progress(4, "3s", 2, 4, "50.00%"),
                "      inflight: 0 lookup | completed: 2 lookup (60/min, avg 40/min)",
                progress(6, "5s", 1, 4, "75.00%"),
                "      inflight: 0 lookup | completed: 3 lookup (60/min, avg 36/min)",
                progress(8, "7s", 0, 4, "100.00%", suffix=True),
                "      inflight: 0 lookup | completed: 4 lookup (60/min, avg 34.29/min)",
                "   -- ALL WORK ITEMS COMPLETE in time 9s",
                "      Queue summary: 4 lookup (avg 26.67/min)",
                NO_COMPUTE,
            ],
        )

    def test_no_progress_lines_without_a_title(self):
        """N1: no title, no progress and no completion lines, however often it may notify."""
        pool, lines = self.run_pool(
            ["a", "b"], self.work_builder(available=True), **EVERY_PASS, **LOOKUP_ONLY
        )
        self.assertEqual(lines, [])
        self.assertFalse(hasattr(pool, "total_time"))

    def test_no_progress_lines_before_the_minimum_interval_has_passed(self):
        """
        N1 with the defaults (a minimum of 60 s, an interval of 300 s, a batch of 500): a short run
        prints the banner and completion only. The minimum alone is pinned by the next test.

        Readings: start 1; passes at 2 and 3; completion 4.
        """
        pool, lines = self.run_pool(
            ["a", "b"], self.work_builder(available=True), title="T", **LOOKUP_ONLY
        )
        self.assertEqual(
            lines,
            [
                "",
                "** T",
                "   -- ALL WORK ITEMS COMPLETE in time 3s",
                "      Queue summary: 2 lookup (avg 40/min)",
                NO_COMPUTE,
            ],
        )

    def test_the_minimum_interval_is_a_strict_bound(self):
        """
        N1: with a minimum of 1 s, pass 1 (1 s since the start) is not notified; pass 2 (2 s) is.

        Readings: start 1; pass 1 at 2; pass 2 at 3, notified, then 4; completion 5.
        """
        pool, lines = self.run_pool(
            ["a", "b"],
            self.work_builder(available=True),
            title="T",
            notify_min_time_interval=1,
            notify_time_interval=0,
            **LOOKUP_ONLY,
        )
        self.assertEqual(
            lines,
            [
                "",
                "** T",
                progress(3, "2s", 0, 2, "100.00%", suffix=True),
                "      inflight: 0 lookup | completed: 2 lookup (avg 60/min)",
                "   -- ALL WORK ITEMS COMPLETE in time 4s",
                "      Queue summary: 2 lookup (avg 30/min)",
                NO_COMPUTE,
            ],
        )

    def test_a_pair_when_the_notify_interval_has_passed(self):
        """
        N2, by time: an interval of 2 s is passed (strictly) at 3 s since the last notification.

        Readings: start 1; passes at 2, 3, 4 (notified, then 5) and 6; completion 7.
        """
        pool, lines = self.run_pool(
            [1, 2, 3, 4],
            self.work_builder(available=True),
            title="T",
            notify_min_time_interval=0,
            notify_time_interval=2,
            **LOOKUP_ONLY,
        )
        self.assertEqual(
            lines,
            [
                "",
                "** T",
                progress(4, "3s", 0, 4, "100.00%", suffix=True),
                "      inflight: 1 lookup | completed: 3 lookup (avg 60/min)",
                "   -- ALL WORK ITEMS COMPLETE in time 6s",
                "      Queue summary: 4 lookup (avg 40/min)",
                NO_COMPUTE,
            ],
        )

    def test_a_pair_when_more_than_notify_batch_size_items_were_processed(self):
        """
        N2, by count: with ``notify_batch_size=1`` a pair follows every second item processed.

        Readings: start 1; passes at 2, 3 (notified, then 4), 5 and 6 (notified, then 7);
        completion 8.
        """
        pool, lines = self.run_pool(
            [1, 2, 3, 4],
            self.work_builder(available=True),
            title="T",
            notify_min_time_interval=0,
            notify_time_interval=100,
            notify_batch_size=1,
            **LOOKUP_ONLY,
        )
        self.assertEqual(
            lines,
            [
                "",
                "** T",
                progress(3, "2s", 0, 4, "100.00%", suffix=True),
                "      inflight: 2 lookup | completed: 2 lookup (avg 60/min)",
                progress(6, "5s", 0, 4, "100.00%", suffix=True),
                "      inflight: 0 lookup | completed: 4 lookup (60/min, avg 48/min)",
                "   -- ALL WORK ITEMS COMPLETE in time 7s",
                "      Queue summary: 4 lookup (avg 34.29/min)",
                NO_COMPUTE,
            ],
        )

    def test_the_available_rate_is_per_interval(self):
        """
        N5 for the available count, which is not the store count: here no store ever completes, so
        a last-available count taken from the store count would print 120/min in the fourth pair.

        Readings: start 1; passes at 2, 4, 6, 8, each notified (then 3, 5, 7, 9); completion 10.
        Pass 1 completes lookup a; pass 2 lookup b; passes 3 and 4 the two available tasks.
        """
        pool, lines = self.run_pool(
            ["a", "b"],
            self.work_builder(available=True),
            available_handler=self.ref_returning_handler("available"),
            title="T",
            **EVERY_PASS,
            **LOOKUP_ONLY,
        )
        self.assertEqual(
            lines,
            [
                "",
                "** T",
                progress(2, "1s", 0, 2, "100.00%", suffix=True),
                "      inflight: 1 lookup, 1 available | completed: 1 lookup (avg 60/min), "
                "0 available (avg 0/day)",
                progress(4, "3s", 0, 2, "100.00%", suffix=True),
                "      inflight: 0 lookup, 2 available | completed: 2 lookup (60/min, avg 40/min), "
                "0 available (0/day, avg 0/day)",
                progress(6, "5s", 0, 2, "100.00%", suffix=True),
                "      inflight: 0 lookup, 1 available | completed: 2 lookup (0/day, avg 24/min), "
                "1 available (60/min, avg 12/min)",
                progress(8, "7s", 0, 2, "100.00%", suffix=True),
                "      inflight: 0 lookup, 0 available | completed: 2 lookup (0/day, avg 17.14/min), "
                "2 available (60/min, avg 17.14/min)",
                "   -- ALL WORK ITEMS COMPLETE in time 9s",
                "      Queue summary: 2 lookup (avg 13.33/min), 2 available (avg 13.33/min)",
                NO_COMPUTE,
            ],
        )

    def test_a_compute_run_with_validation_notifying_on_every_pass(self):
        """
        Q1 and Q2 through the pool's own lines, with compute, store and validation segments; F2's
        line absent once a compute has completed.

        Readings: start 1; passes at 2, 4, 6, 8, each notified (then 3, 5, 7, 9); completion 10.
        The four passes complete the lookup, the compute, the store and the validation.
        """
        pool, lines = self.run_pool(
            ["a"],
            self.work_builder(available=False),
            validation_handler=self.ref_returning_handler("validate", True),
            title="T",
            **EVERY_PASS,
        )
        self.assertEqual(
            lines,
            [
                "",
                "** T",
                progress(2, "1s", 0, 1, "100.00%", suffix=True),
                "      inflight: 0 lookup, 1 compute, 0 store, 0 validation | completed: "
                "1 lookup (avg 60/min), 0 compute (avg 0/day), 0 store (avg 0/day), "
                "0 validation (avg 0/day)",
                progress(4, "3s", 0, 1, "100.00%", suffix=True),
                "      inflight: 0 lookup, 0 compute, 1 store, 0 validation | completed: "
                "1 lookup (0/day, avg 20/min), 1 compute (60/min, avg 20/min), "
                "0 store (0/day, avg 0/day), 0 validation (0/day, avg 0/day)",
                progress(6, "5s", 0, 1, "100.00%", suffix=True),
                "      inflight: 0 lookup, 0 compute, 0 store, 1 validation | completed: "
                "1 lookup (0/day, avg 12/min), 1 compute (0/day, avg 12/min), "
                "1 store (60/min, avg 12/min), 0 validation (0/day, avg 0/day)",
                progress(8, "7s", 0, 1, "100.00%", suffix=True),
                "      inflight: 0 lookup, 0 compute, 0 store, 0 validation | completed: "
                "1 lookup (0/day, avg 514.3/hr), 1 compute (0/day, avg 514.3/hr), "
                "1 store (0/day, avg 514.3/hr), 1 validation (60/min, avg 514.3/hr)",
                "   -- ALL WORK ITEMS COMPLETE in time 9s",
                "      Queue summary: 1 lookup (avg 400/hr), 1 compute (avg 400/hr), "
                "1 store (avg 400/hr), 1 validation (avg 400/hr)",
            ],
        )

    def test_the_validation_warning_among_the_titled_lines(self):
        """
        V1 with a title: the warning, printed between the banner and the completion pair.

        Readings: start 1; passes at 2, 3, 4 and 5 (the validation); completion 6.
        """
        pool, lines = self.run_pool(
            ["a"],
            self.work_builder(available=False),
            validation_handler=self.ref_returning_handler("validate", False),
            title="T",
        )
        self.assertEqual(
            lines,
            [
                "",
                "** T",
                "!! WARNING: Work object with store_id=1001 did not validate after being "
                "emplaced in the datastore",
                "   -- ALL WORK ITEMS COMPLETE in time 5s",
                "      Queue summary: 1 lookup (avg 12/min), 1 compute (avg 12/min), "
                "1 store (avg 12/min), 1 validation (avg 12/min)",
            ],
        )


class TestConsumerPatterns(PoolTestCase):
    """
    A consumer of this output parses it with three patterns, for the banner, the progress line
    and the completion line, copied above as they are. They are checked here against the pool's
    actual lines. Changing a line they match changes the pool's interface (``CLAUDE.md``,
    "Releases").
    """

    def test_the_patterns_match_the_pool_s_lines(self):
        pool, lines = self.run_pool(
            [1, 2, 3, 4],
            self.work_builder(available=True),
            title="Stage one: lookups",
            max_task_queue=1,
            create_batch_size=1,
            **EVERY_PASS,
            **LOOKUP_ONLY,
        )
        banners = [m.group(1) for m in map(BANNER_PATTERN.search, lines) if m]
        self.assertEqual(banners, ["Stage one: lookups"])

        found = [m.groups() for m in map(PROGRESS_PATTERN.search, lines) if m]
        self.assertEqual(
            found,
            [
                ("3", "4", "25.00"),
                ("2", "4", "50.00"),
                ("1", "4", "75.00"),
                ("0", "4", "100.00"),
            ],
        )

        completions = [line for line in lines if COMPLETE_PATTERN.search(line)]
        self.assertEqual(completions, ["   -- ALL WORK ITEMS COMPLETE in time 9s"])


if __name__ == "__main__":
    unittest.main()
