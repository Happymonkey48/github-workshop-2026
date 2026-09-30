import unittest

from tests.missions import config
from tests.missions.repo import (
    branch_exists,
    checkpoint,
    commit_by_message,
    is_ancestor,
    rev_parse,
    run_app_tests,
    show_file,
)

BRANCH = config.BRANCHES["receipt_debug"]


class Mission05Tests(unittest.TestCase):
    def test_debug_pricing_is_gone_and_the_bad_commit_remains(self):
        self.assertTrue(branch_exists(BRANCH), "feature/receipt-debug is missing.")
        bad = checkpoint("debug_pricing", lambda: commit_by_message(BRANCH, config.MESSAGES["debug_pricing"]))
        tip = rev_parse(BRANCH)
        tip_source = show_file(BRANCH, "app/checkout.py")
        bad_source = show_file(bad, "app/checkout.py")

        self.assertIn(config.MARKERS["debug_function"], bad_source)
        self.assertTrue(
            is_ancestor(bad, BRANCH),
            "The debug commit disappeared from feature/receipt-debug. Undo it with a new commit and leave the old one in history.",
        )
        self.assertNotEqual(tip, bad, "Add a new commit that removes the debug pricing output.")
        self.assertNotIn(config.MARKERS["debug_pricing"], tip_source, "checkout.py still contains the debug pricing output.")
        self.assertNotIn(config.MARKERS["debug_function"], tip_source, "checkout.py still defines debug_pricing.")

    def test_application_tests_pass(self):
        self.assertTrue(branch_exists(BRANCH), "feature/receipt-debug is missing.")
        result = run_app_tests(BRANCH)
        self.assertTrue(result["ok"], f"Application tests failed on feature/receipt-debug.\n{result['output']}")
