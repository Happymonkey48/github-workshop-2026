import unittest

from tests.missions import config
from tests.missions.repo import (
    branch_exists,
    checkpoint,
    file_exists,
    git_ok,
    is_ancestor,
    read_json,
    rev_parse,
    run_app_tests,
    show_file,
)

BRANCH = config.BRANCHES["loyalty"]
TAG = config.TAGS["loyalty_backup"]


class Mission06Tests(unittest.TestCase):
    def test_dropped_loyalty_commit_is_restored(self):
        self.assertTrue(branch_exists(BRANCH), "feature/loyalty is missing.")
        self.assertTrue(
            git_ok(["rev-parse", "--verify", "--quiet", f"refs/tags/{TAG}"]),
            f"The recoverable loyalty tip {TAG} is missing.",
        )
        lost = checkpoint("loyalty_lost", lambda: rev_parse(TAG))
        self.assertEqual(rev_parse(TAG), lost, f"{TAG} no longer points at the dropped loyalty commit.")
        self.assertTrue(is_ancestor(lost, BRANCH), "The dropped loyalty commit is not on feature/loyalty yet.")
        self.assertTrue(file_exists(BRANCH, "app/rewards.json"), "app/rewards.json is still missing.")
        self.assertRegex(show_file(BRANCH, "app/loyalty.py"), r"def redeem\s*\(")
        rewards = read_json(BRANCH, "app/rewards.json")
        ids = [reward["id"] for reward in rewards["rewards"]]
        self.assertIn("free-americano", ids)
        self.assertIn("free-latte", ids)

    def test_application_tests_pass(self):
        self.assertTrue(branch_exists(BRANCH), "feature/loyalty is missing.")
        result = run_app_tests(BRANCH)
        self.assertTrue(result["ok"], f"Application tests failed on feature/loyalty.\n{result['output']}")
