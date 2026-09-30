import unittest

from tests.missions import config
from tests.missions.repo import (
    branch_exists,
    checkpoint,
    commit_by_message,
    is_ancestor,
    load_module,
    remote_ref,
    remote_tracking_exists,
    resolve_branch,
    rev_parse,
    run_app_tests,
    show_file,
)

CHECKOUT_BRANCH = config.BRANCHES["checkout"]
PAYMENT_BRANCH = config.BRANCHES["payment"]


def change_due(ref):
    checkout = load_module(ref, "app/checkout.py")
    return {
        "underpaid": lambda: checkout.apply_payment(10, 3),
        "exact": checkout.apply_payment(3.5, 3.5),
        "change": checkout.apply_payment(4.5, 10),
    }


class Mission02Tests(unittest.TestCase):
    def test_unfinished_checkout_work_is_still_present(self):
        checkout_ref = resolve_branch(CHECKOUT_BRANCH)
        self.assertIsNotNone(
            checkout_ref,
            "feature/checkout is missing. Keep that branch so the tax work can be recovered.",
        )
        wip = checkpoint(
            "checkout_wip",
            lambda: commit_by_message(checkout_ref, config.MESSAGES["checkout_wip"]),
        )
        tax = show_file(checkout_ref, "app/tax.py")
        self.assertIn(config.MARKERS["checkout_wip"], tax)
        self.assertTrue(
            is_ancestor(wip, checkout_ref),
            "The unfinished tax calculator commit is no longer on feature/checkout.",
        )

    def test_application_tests_still_pass_on_feature_checkout(self):
        checkout_ref = resolve_branch(CHECKOUT_BRANCH)
        self.assertIsNotNone(checkout_ref, "feature/checkout is missing.")
        result = run_app_tests(checkout_ref)
        self.assertTrue(result["ok"], f"Application tests failed on feature/checkout.\n{result['output']}")

    def test_hotfix_commits_the_corrected_change_calculation(self):
        self.assertTrue(branch_exists(PAYMENT_BRANCH), "hotfix/payment does not exist locally.")
        paid = change_due(PAYMENT_BRANCH)
        with self.assertRaisesRegex(ValueError, "Insufficient payment"):
            paid["underpaid"]()
        self.assertEqual(paid["exact"], 0, "Paying the exact total should return 0 change.")
        self.assertEqual(
            paid["change"],
            5.5,
            "A 4.50 order paid with 10.00 should return 5.50. Commit the fix on hotfix/payment.",
        )

    def test_application_tests_pass_on_hotfix(self):
        self.assertTrue(branch_exists(PAYMENT_BRANCH), "hotfix/payment does not exist locally.")
        result = run_app_tests(PAYMENT_BRANCH)
        self.assertTrue(result["ok"], f"Application tests failed on hotfix/payment.\n{result['output']}")

    def test_payment_hotfix_is_pushed_to_origin(self):
        self.assertTrue(branch_exists(PAYMENT_BRANCH), "hotfix/payment does not exist locally.")
        remote = remote_ref(PAYMENT_BRANCH)
        self.assertTrue(
            remote_tracking_exists(PAYMENT_BRANCH),
            f"{PAYMENT_BRANCH} exists locally, but {remote} is missing. Push the hotfix.",
        )
        published = change_due(remote)
        self.assertEqual(published["change"], 5.5, f"{remote} still has the payment bug. Push hotfix/payment.")
        self.assertTrue(
            is_ancestor(rev_parse(PAYMENT_BRANCH), remote),
            "origin is missing your latest hotfix/payment commit. Push the branch.",
        )
