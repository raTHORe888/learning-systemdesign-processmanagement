"""CPU Scheduling Algorithms: FCFS, SJF, Round Robin, Priority (Non-Preemptive)."""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
from copy import deepcopy


@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 0
    remaining_time: int = field(init=False)
    completion_time: int = field(init=False, default=0)
    turnaround_time: int = field(init=False, default=0)
    waiting_time: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        self.remaining_time = self.burst_time


@dataclass
class ScheduleResult:
    algorithm: str
    processes: list[Process]
    avg_turnaround_time: float
    avg_waiting_time: float


def _compute_times(processes: list[Process]) -> None:
    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time


def fcfs(processes: list[Process]) -> ScheduleResult:
    """First Come First Serve — non-preemptive, ordered by arrival time."""
    procs = deepcopy(sorted(processes, key=lambda p: p.arrival_time))
    time = 0
    for p in procs:
        time = max(time, p.arrival_time) + p.burst_time
        p.completion_time = time
    _compute_times(procs)
    avg_tat = sum(p.turnaround_time for p in procs) / len(procs)
    avg_wt = sum(p.waiting_time for p in procs) / len(procs)
    return ScheduleResult("First Come First Serve (FCFS)", procs, avg_tat, avg_wt)


def sjf(processes: list[Process]) -> ScheduleResult:
    """Shortest Job First — non-preemptive."""
    procs = deepcopy(processes)
    completed: list[Process] = []
    time = 0
    remaining = list(procs)

    while remaining:
        available = [p for p in remaining if p.arrival_time <= time]
        if not available:
            time = min(p.arrival_time for p in remaining)
            available = [p for p in remaining if p.arrival_time <= time]
        shortest = min(available, key=lambda p: p.burst_time)
        time += shortest.burst_time
        shortest.completion_time = time
        remaining.remove(shortest)
        completed.append(shortest)

    _compute_times(completed)
    avg_tat = sum(p.turnaround_time for p in completed) / len(completed)
    avg_wt = sum(p.waiting_time for p in completed) / len(completed)
    return ScheduleResult("Shortest Job First (SJF)", completed, avg_tat, avg_wt)


def round_robin(processes: list[Process], time_quantum: int = 3) -> ScheduleResult:
    """Round Robin scheduling with a configurable time quantum."""
    procs = deepcopy(sorted(processes, key=lambda p: p.arrival_time))
    queue: deque[Process] = deque()
    time = 0
    index = 0
    completed: list[Process] = []

    if procs:
        queue.append(procs[index])
        index += 1

    while queue:
        p = queue.popleft()
        exec_time = min(p.remaining_time, time_quantum)
        time += exec_time
        p.remaining_time -= exec_time

        while index < len(procs) and procs[index].arrival_time <= time:
            queue.append(procs[index])
            index += 1

        if p.remaining_time == 0:
            p.completion_time = time
            completed.append(p)
        else:
            queue.append(p)

        if not queue and index < len(procs):
            time = procs[index].arrival_time
            queue.append(procs[index])
            index += 1

    _compute_times(completed)
    avg_tat = sum(p.turnaround_time for p in completed) / len(completed)
    avg_wt = sum(p.waiting_time for p in completed) / len(completed)
    return ScheduleResult(
        f"Round Robin (Time Quantum = {time_quantum})", completed, avg_tat, avg_wt
    )


def priority_scheduling(processes: list[Process]) -> ScheduleResult:
    """Priority Scheduling — non-preemptive, lower number = higher priority."""
    procs = deepcopy(processes)
    completed: list[Process] = []
    time = 0
    remaining = list(procs)

    while remaining:
        available = [p for p in remaining if p.arrival_time <= time]
        if not available:
            time = min(p.arrival_time for p in remaining)
            available = [p for p in remaining if p.arrival_time <= time]
        highest = min(available, key=lambda p: p.priority)
        time += highest.burst_time
        highest.completion_time = time
        remaining.remove(highest)
        completed.append(highest)

    _compute_times(completed)
    avg_tat = sum(p.turnaround_time for p in completed) / len(completed)
    avg_wt = sum(p.waiting_time for p in completed) / len(completed)
    return ScheduleResult("Priority Scheduling (Non-Preemptive)", completed, avg_tat, avg_wt)


SAMPLE_PROCESSES = [
    Process(pid="P1", arrival_time=0, burst_time=5, priority=2),
    Process(pid="P2", arrival_time=1, burst_time=3, priority=3),
    Process(pid="P3", arrival_time=2, burst_time=8, priority=1),
    Process(pid="P4", arrival_time=3, burst_time=6, priority=4),
]

if __name__ == "__main__":
    for result in [
        fcfs(SAMPLE_PROCESSES),
        sjf(SAMPLE_PROCESSES),
        round_robin(SAMPLE_PROCESSES, time_quantum=3),
        priority_scheduling(SAMPLE_PROCESSES),
    ]:
        print(f"\nAlgorithm : {result.algorithm}")
        print(f"Avg TAT   : {result.avg_turnaround_time:.2f}")
        print(f"Avg WT    : {result.avg_waiting_time:.2f}")
