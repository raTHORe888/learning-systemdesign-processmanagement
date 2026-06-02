"""Multithreading demo for OS learning (Python).

This module demonstrates:
1) I/O-bound threading speedup
2) CPU-bound threading limitation in CPython (GIL effect)
3) Race condition vs lock-protected shared state
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock, Thread
from time import perf_counter, sleep


@dataclass
class TimingResult:
    name: str
    elapsed_seconds: float


@dataclass
class CounterResult:
    expected: int
    without_lock: int
    with_lock: int


def _io_task(delay: float) -> None:
    sleep(delay)


def run_sequential_io(worker_count: int = 5, delay: float = 0.1) -> TimingResult:
    start = perf_counter()
    for _ in range(worker_count):
        _io_task(delay)
    end = perf_counter()
    return TimingResult("Sequential I/O", end - start)


def run_threaded_io(worker_count: int = 5, delay: float = 0.1) -> TimingResult:
    start = perf_counter()
    threads = [Thread(target=_io_task, args=(delay,)) for _ in range(worker_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = perf_counter()
    return TimingResult("Threaded I/O", end - start)


def _cpu_task(iterations: int) -> int:
    total = 0
    for i in range(iterations):
        total += i * i
    return total


def run_sequential_cpu(worker_count: int = 4, iterations: int = 250_000) -> TimingResult:
    start = perf_counter()
    for _ in range(worker_count):
        _cpu_task(iterations)
    end = perf_counter()
    return TimingResult("Sequential CPU", end - start)


def run_threaded_cpu(worker_count: int = 4, iterations: int = 250_000) -> TimingResult:
    start = perf_counter()
    threads = [Thread(target=_cpu_task, args=(iterations,)) for _ in range(worker_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = perf_counter()
    return TimingResult("Threaded CPU", end - start)


def simulate_counter_race(thread_count: int = 8, increments_per_thread: int = 500) -> CounterResult:
    expected = thread_count * increments_per_thread

    # without lock (intentionally unsafe read-modify-write)
    shared_unsafe = {"value": 0}

    def unsafe_worker() -> None:
        for _ in range(increments_per_thread):
            snapshot = shared_unsafe["value"]
            sleep(0)  # force context switch opportunity
            shared_unsafe["value"] = snapshot + 1

    unsafe_threads = [Thread(target=unsafe_worker) for _ in range(thread_count)]
    for t in unsafe_threads:
        t.start()
    for t in unsafe_threads:
        t.join()

    # with lock (safe)
    shared_safe = {"value": 0}
    lock = Lock()

    def safe_worker() -> None:
        for _ in range(increments_per_thread):
            with lock:
                shared_safe["value"] += 1

    safe_threads = [Thread(target=safe_worker) for _ in range(thread_count)]
    for t in safe_threads:
        t.start()
    for t in safe_threads:
        t.join()

    return CounterResult(
        expected=expected,
        without_lock=shared_unsafe["value"],
        with_lock=shared_safe["value"],
    )


def run_demo_report() -> dict[str, object]:
    seq_io = run_sequential_io()
    thr_io = run_threaded_io()
    seq_cpu = run_sequential_cpu()
    thr_cpu = run_threaded_cpu()
    counter = simulate_counter_race()

    return {
        "io": (seq_io, thr_io),
        "cpu": (seq_cpu, thr_cpu),
        "counter": counter,
    }


if __name__ == "__main__":
    report = run_demo_report()
    seq_io, thr_io = report["io"]
    seq_cpu, thr_cpu = report["cpu"]
    counter = report["counter"]

    print("\n=== I/O-bound comparison ===")
    print(f"{seq_io.name:>18}: {seq_io.elapsed_seconds:.4f}s")
    print(f"{thr_io.name:>18}: {thr_io.elapsed_seconds:.4f}s")

    print("\n=== CPU-bound comparison ===")
    print(f"{seq_cpu.name:>18}: {seq_cpu.elapsed_seconds:.4f}s")
    print(f"{thr_cpu.name:>18}: {thr_cpu.elapsed_seconds:.4f}s")

    print("\n=== Race condition demo ===")
    print(f"Expected count       : {counter.expected}")
    print(f"Without lock result  : {counter.without_lock}")
    print(f"With lock result     : {counter.with_lock}")
