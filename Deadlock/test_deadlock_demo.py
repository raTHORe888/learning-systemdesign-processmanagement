import unittest

from deadlock_demo import run_demo


class DeadlockDemoTest(unittest.TestCase):
    def test_both_processes_acquire_first_lock(self) -> None:
        result = run_demo()
        self.assertTrue(result.process_one_first_lock)
        self.assertTrue(result.process_two_first_lock)

    def test_both_processes_block_on_second_lock(self) -> None:
        result = run_demo()
        self.assertFalse(result.process_one_second_lock)
        self.assertFalse(result.process_two_second_lock)


if __name__ == "__main__":
    unittest.main()
