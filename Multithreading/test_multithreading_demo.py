import unittest

from multithreading_demo import (
    run_sequential_cpu,
    run_sequential_io,
    run_threaded_cpu,
    run_threaded_io,
    simulate_counter_race,
)


class MultithreadingDemoTest(unittest.TestCase):
    def test_io_threading_is_faster_than_sequential(self) -> None:
        seq = run_sequential_io(worker_count=6, delay=0.08)
        thr = run_threaded_io(worker_count=6, delay=0.08)

        print(f"\nSequential I/O: {seq.elapsed_seconds:.4f}s")
        print(f"Threaded   I/O: {thr.elapsed_seconds:.4f}s")

        self.assertLess(thr.elapsed_seconds, seq.elapsed_seconds)

    def test_cpu_threading_not_massively_faster(self) -> None:
        seq = run_sequential_cpu(worker_count=4, iterations=220_000)
        thr = run_threaded_cpu(worker_count=4, iterations=220_000)

        print(f"\nSequential CPU: {seq.elapsed_seconds:.4f}s")
        print(f"Threaded   CPU: {thr.elapsed_seconds:.4f}s")

        # In CPython, CPU-bound threads are usually similar/slower due to GIL.
        # Keep this threshold tolerant for CI variability.
        self.assertGreaterEqual(thr.elapsed_seconds, seq.elapsed_seconds * 0.60)

    def test_lock_prevents_counter_race(self) -> None:
        result = simulate_counter_race(thread_count=8, increments_per_thread=500)

        print("\nCounter race demo")
        print(f"Expected   : {result.expected}")
        print(f"No lock    : {result.without_lock}")
        print(f"With lock  : {result.with_lock}")

        self.assertEqual(result.with_lock, result.expected)
        self.assertLessEqual(result.without_lock, result.expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
