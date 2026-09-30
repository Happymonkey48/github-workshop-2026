import unittest

from tests.missions import config
from tests.missions.repo import (
    checkpoint,
    commit_by_message,
    file_exists,
    load_module,
    resolve_branch,
    run_app_tests,
)

BRANCH = config.BRANCHES["pricing"]


class Mission03Tests(unittest.TestCase):
    def test_main_has_only_the_fall_latte_adjustment(self):
        self.assertTrue(
            file_exists("main", "app/pricing.py"),
            "main is missing app/pricing.py. Bring over only the fall latte adjustment.",
        )
        pricing = load_module("main", "app/pricing.py")
        self.assertEqual(pricing.adjustment_for(config.PRICING["drink_id"]), config.PRICING["adjustment"])
        self.assertEqual(pricing.adjustment_for("americano"), 0)
        for path in config.PRICING["unrelated_files"]:
            self.assertFalse(file_exists("main", path), f"{path} should stay off main.")

    def test_feature_pricing_still_holds_the_unrelated_work(self):
        pricing_ref = resolve_branch(BRANCH)
        self.assertIsNotNone(pricing_ref, "feature/pricing is missing.")
        checkpoint("pricing_useful", lambda: commit_by_message(pricing_ref, config.MESSAGES["pricing_useful"]))
        for path in config.PRICING["unrelated_files"]:
            self.assertTrue(
                file_exists(pricing_ref, path),
                f"{path} should remain on feature/pricing so the whole branch is not required.",
            )

    def test_application_tests_pass_on_main(self):
        result = run_app_tests("main")
        self.assertTrue(result["ok"], f"Application tests failed on main.\n{result['output']}")
