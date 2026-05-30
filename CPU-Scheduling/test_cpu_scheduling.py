import unittest

from cpu_scheduling import (
    SAMPLE_PROCESSES,
    ScheduleResult,
    fcfs,
    priority_scheduling,
    round_robin,
    sjf,
)


def _print_report(result: ScheduleResult) -> None:
    sep = "─" * 66
    has_priority = result.algorithm.startswith("Priority")
    print(f"\n{sep}")
    print(f"  ALGORITHM: {result.algorithm}")
    print(sep)
    if has_priority:
        print(f"  {'Process':<9} {'Arrival':>7} {'Burst':>6} {'Priority':>8} {'Completion':>11} {'TAT':>5} {'Waiting':>8}")
        print(f"  {'-------':<9} {'-------':>7} {'-----':>6} {'--------':>8} {'----------':>11} {'---':>5} {'-------':>8}")
        for p in result.processes:
            print(
                f"  {p.pid:<9} {p.arrival_time:>7} {p.burst_time:>6} {p.priority:>8}"
                f" {p.completion_time:>11} {p.turnaround_time:>5} {p.waiting_time:>8}"
            )
    else:
        print(f"  {'Process':<9} {'Arrival':>7} {'Burst':>6} {'Completion':>11} {'TAT':>5} {'Waiting':>8}")
        print(f"  {'-------':<9} {'-------':>7} {'-----':>6} {'----------':>11} {'---':>5} {'-------':>8}")
        for p in result.processes:
            print(
                f"  {p.pid:<9} {p.arrival_time:>7} {p.burst_time:>6}"
                f" {p.completion_time:>11} {p.turnaround_time:>5} {p.waiting_time:>8}"
            )
    print(sep)
    print(f"  Avg Turn Around Time : {result.avg_turnaround_time:.2f}")
    print(f"  Avg Waiting Time     : {result.avg_waiting_time:.2f}")
    print(f"{sep}\n")


class FCFSTest(unittest.TestCase):
    """First Come First Serve — processes execute in arrival order."""

    def setUp(self) -> None:
        self.result = fcfs(SAMPLE_PROCESSES)

    def test_completion_order(self) -> None:
        pids = [p.pid for p in self.result.processes]
        self.assertEqual(pids, ["P1", "P2", "P3", "P4"])

    def test_avg_waiting_time(self) -> None:
        _print_report(self.result)
        self.assertAlmostEqual(self.result.avg_waiting_time, 5.75)

    def test_avg_turnaround_time(self) -> None:
        self.assertAlmostEqual(self.result.avg_turnaround_time, 11.25)


class SJFTest(unittest.TestCase):
    """Shortest Job First — shortest burst time goes next."""

    def setUp(self) -> None:
        self.result = sjf(SAMPLE_PROCESSES)

    def test_p2_runs_before_p3(self) -> None:
        pids = [p.pid for p in self.result.processes]
        self.assertLess(pids.index("P2"), pids.index("P3"))

    def test_avg_waiting_time(self) -> None:
        _print_report(self.result)
        self.assertAlmostEqual(self.result.avg_waiting_time, 5.25)

    def test_avg_turnaround_time(self) -> None:
        self.assertAlmostEqual(self.result.avg_turnaround_time, 10.75)


class RoundRobinTest(unittest.TestCase):
    """Round Robin with time quantum = 3."""

    def setUp(self) -> None:
        self.result = round_robin(SAMPLE_PROCESSES, time_quantum=3)

    def test_all_processes_complete(self) -> None:
        _print_report(self.result)
        self.assertEqual(len(self.result.processes), 4)

    def test_no_remaining_time(self) -> None:
        for p in self.result.processes:
            self.assertEqual(p.remaining_time, 0)

    def test_avg_waiting_time(self) -> None:
        self.assertAlmostEqual(self.result.avg_waiting_time, 8.50)


class PriorityTest(unittest.TestCase):
    """Priority Scheduling (non-preemptive) — lower number = higher priority."""

    def setUp(self) -> None:
        self.result = priority_scheduling(SAMPLE_PROCESSES)

    def test_p3_runs_before_p2(self) -> None:
        """P3 has priority 1 (highest), P2 has priority 3."""
        _print_report(self.result)
        pids = [p.pid for p in self.result.processes]
        self.assertLess(pids.index("P3"), pids.index("P2"))

    def test_avg_waiting_time(self) -> None:
        self.assertAlmostEqual(self.result.avg_waiting_time, 7.00)

    def test_avg_turnaround_time(self) -> None:
        self.assertAlmostEqual(self.result.avg_turnaround_time, 12.50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
