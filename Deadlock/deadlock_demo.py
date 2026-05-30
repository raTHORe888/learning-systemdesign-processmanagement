"""Small, safe deadlock demonstration.

This example uses two locks and two threads. Each thread acquires one lock,
then tries to acquire the other lock with a timeout so the program does not
hang forever.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import Barrier, Lock, Thread
from time import sleep


@dataclass
class DeadlockOutcome:
    process_one_first_lock: bool
    process_one_second_lock: bool
    process_two_first_lock: bool
    process_two_second_lock: bool


class DeadlockDemo:
    def __init__(self) -> None:
        self.lock_a = Lock()
        self.lock_b = Lock()
        self.sync_point = Barrier(2)

    def _process_one(self, outcome: dict[str, bool]) -> None:
        self.lock_a.acquire()
        try:
            outcome["process_one_first_lock"] = True
            self.sync_point.wait()
            sleep(0.05)
            outcome["process_one_second_lock"] = self.lock_b.acquire(timeout=0.1)
            self.sync_point.wait()
            if outcome["process_one_second_lock"]:
                self.lock_b.release()
        finally:
            self.lock_a.release()

    def _process_two(self, outcome: dict[str, bool]) -> None:
        self.lock_b.acquire()
        try:
            outcome["process_two_first_lock"] = True
            self.sync_point.wait()
            sleep(0.05)
            outcome["process_two_second_lock"] = self.lock_a.acquire(timeout=0.1)
            self.sync_point.wait()
            if outcome["process_two_second_lock"]:
                self.lock_a.release()
        finally:
            self.lock_b.release()

    def simulate(self) -> DeadlockOutcome:
        outcome = {
            "process_one_first_lock": False,
            "process_one_second_lock": False,
            "process_two_first_lock": False,
            "process_two_second_lock": False,
        }

        thread_one = Thread(target=self._process_one, args=(outcome,))
        thread_two = Thread(target=self._process_two, args=(outcome,))

        thread_one.start()
        thread_two.start()
        thread_one.join()
        thread_two.join()

        return DeadlockOutcome(**outcome)


def run_demo() -> DeadlockOutcome:
    """Run the deadlock demo and return the captured outcome."""

    return DeadlockDemo().simulate()


if __name__ == "__main__":
    result = run_demo()
    print(result)
