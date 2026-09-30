import unittest

from tests.missions import config
from tests.missions.repo import (
    branch_exists,
    checkpoint,
    commit_by_message,
    file_exists,
    is_ancestor,
    read_json,
    remote_ref,
    remote_tracking_exists,
    rev_parse,
    run_app_tests,
)

BRANCH = config.BRANCHES["menu"]


def mocha_on(ref):
    menu = read_json(ref, "app/menu.json")
    return next((drink for drink in menu["drinks"] if drink["id"] == config.MOCHA["id"]), None)


class Mission01Tests(unittest.TestCase):
    def test_feature_menu_exists_locally(self):
        self.assertTrue(branch_exists(BRANCH), "Create or check out feature/menu locally.")

    def test_mocha_is_finished_on_the_local_commit(self):
        self.assertTrue(branch_exists(BRANCH), "feature/menu does not exist locally.")
        draft = checkpoint("menu_draft", lambda: commit_by_message(BRANCH, config.MESSAGES["menu_draft"]))
        tip = rev_parse(BRANCH)
        finished = mocha_on(BRANCH)
        drafted = mocha_on(draft)

        self.assertIsNotNone(finished, "feature/menu is missing the mocha drink.")
        self.assertEqual(finished["name"], config.MOCHA["name"], "Mocha should be named Mocha.")
        self.assertEqual(
            finished["price"],
            config.MOCHA["price"],
            f"Mocha still costs {finished['price']}. It should cost {config.MOCHA['price']}. Commit that change on feature/menu.",
        )
        self.assertEqual(drafted["price"], config.MOCHA["draft_price"], "The original draft commit should stay in history.")
        self.assertTrue(is_ancestor(draft, BRANCH), "Keep the draft commit and commit the finished menu on top of it.")
        self.assertNotEqual(tip, draft, "feature/menu is still the unfinished draft. Commit the finished mocha.")

    def test_application_tests_pass_on_feature_menu(self):
        self.assertTrue(branch_exists(BRANCH), "feature/menu does not exist locally.")
        result = run_app_tests(BRANCH)
        self.assertTrue(result["ok"], f"Application tests failed on feature/menu.\n{result['output']}")

    def test_finished_branch_is_on_origin(self):
        self.assertTrue(branch_exists(BRANCH), "feature/menu does not exist locally.")
        remote = remote_ref(BRANCH)
        self.assertTrue(
            remote_tracking_exists(BRANCH),
            f"{BRANCH} exists locally, but {remote} is missing. Push the branch.",
        )
        self.assertTrue(file_exists(remote, "app/menu.json"), f"{remote} does not contain app/menu.json.")
        published = mocha_on(remote)
        self.assertIsNotNone(published, f"{remote} does not contain mocha.")
        self.assertEqual(
            published["price"],
            config.MOCHA["price"],
            f"{remote} still has the unfinished mocha. Push feature/menu.",
        )
        self.assertTrue(is_ancestor(BRANCH, remote), "origin is missing your latest feature/menu commit. Push the branch.")
