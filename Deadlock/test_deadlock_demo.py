import unittest

from deadlock_demo import run_demo


def _status(flag: bool) -> str:
    return "✅ ACQUIRED" if flag else "❌ BLOCKED (deadlock)"


def _print_report(result, title: str) -> None:
    separator = "─" * 58
    print(f"\n{separator}")
    print(f"  TEST: {title}")
    print(separator)
    print(f"  {'Process':<12}  {'Resource':<14}  {'Outcome'}")
    print(f"  {'-------':<12}  {'--------':<14}  {'-------'}")
    print(f"  {'P1':<12}  {'Lock A (1st)':<14}  {_status(result.process_one_first_lock)}")
    print(f"  {'P1':<12}  {'Lock B (2nd)':<14}  {_status(result.process_one_second_lock)}")
    print(f"  {'P2':<12}  {'Lock B (1st)':<14}  {_status(result.process_two_first_lock)}")
    print(f"  {'P2':<12}  {'Lock A (2nd)':<14}  {_status(result.process_two_second_lock)}")
    print(separator)

    deadlocked = (
        not result.process_one_second_lock and not result.process_two_second_lock
    )
    conclusion = "⚠️  DEADLOCK DETECTED" if deadlocked else "✅  No deadlock - processes completed"
    print(f"  Conclusion : {conclusion}")
    print(f"{separator}\n")


class DeadlockDemoTest(unittest.TestCase):
    def test_both_processes_acquire_first_lock(self) -> None:
        """P1 must acquire Lock A and P2 must acquire Lock B as their first lock."""
        result = run_demo()
        _print_report(result, "Both processes acquire their FIRST lock")

        self.assertTrue(
            result.process_one_first_lock,
            "P1 should have acquired Lock A",
        )
        self.assertTrue(
            result.process_two_first_lock,
            "P2 should have acquired Lock B",
        )

    def test_both_processes_block_on_second_lock(self) -> None:
        """P1 must fail to acquire Lock B and P2 must fail to acquire Lock A (deadlock)."""
        result = run_demo()
        _print_report(result, "Both processes BLOCK on their second lock")

        self.assertFalse(
            result.process_one_second_lock,
            "P1 should NOT have acquired Lock B - it is held by P2",
        )
        self.assertFalse(
            result.process_two_second_lock,
            "P2 should NOT have acquired Lock A - it is held by P1",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
