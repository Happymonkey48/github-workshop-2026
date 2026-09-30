import json
import unittest

from tests.missions import config
from tests.missions.repo import branch_exists, file_exists, remote_tracking_exists, run_app_tests, show_file

BRANCHES = [config.BRANCHES["mobile_menu"], config.BRANCHES["matcha_promo"]]


def menu_state(branch):
    if not branch_exists(branch) or not file_exists(branch, "app/menu.json"):
        return None
    raw = show_file(branch, "app/menu.json")
    try:
        menu = json.loads(raw)
    except json.JSONDecodeError:
        menu = None
    matcha = None
    if menu:
        matcha = next((drink for drink in menu["drinks"] if drink["id"] == config.MATCHA["id"]), None)
    return {"branch": branch, "raw": raw, "menu": menu, "matcha": matcha}


def has_sizes(matcha):
    if not matcha or not isinstance(matcha.get("sizes"), list):
        return False
    return all(size in matcha["sizes"] for size in config.MATCHA["sizes"])


def is_resolved(state):
    if not state or not state["menu"] or not state["matcha"]:
        return False
    raw = state["raw"]
    if "<<<<<<<" in raw or ">>>>>>>" in raw or "=======" in raw:
        return False
    matcha = state["matcha"]
    return has_sizes(matcha) and matcha.get("featured") is True and matcha.get("price", 0) > 0


class Mission04Tests(unittest.TestCase):
    def test_both_menu_branches_still_exist(self):
        for branch in BRANCHES:
            self.assertTrue(
                branch_exists(branch) or remote_tracking_exists(branch),
                f"{branch} is missing locally and on origin.",
            )

    def test_one_branch_commits_both_matcha_changes(self):
        states = [menu_state(branch) for branch in BRANCHES if branch_exists(branch)]
        resolved = next((state for state in states if is_resolved(state)), None)
        self.assertIsNotNone(
            resolved,
            "Merge feature/mobile-menu and feature/matcha-promo. Keep Matcha Latte featured and keep the 12oz and 16oz sizes. Commit the resolved menu.json on one of those branches.",
        )
        for state in states:
            if not state:
                continue
            self.assertNotIn("<<<<<<<", state["raw"], f"{state['branch']} still has conflict markers.")
            self.assertNotIn(">>>>>>>", state["raw"], f"{state['branch']} still has conflict markers.")

    def test_application_tests_pass_on_the_integrated_branch(self):
        states = [menu_state(branch) for branch in BRANCHES if branch_exists(branch)]
        resolved = next((state for state in states if is_resolved(state)), None)
        self.assertIsNotNone(resolved, "The matcha integration is not committed yet.")
        result = run_app_tests(resolved["branch"])
        self.assertTrue(result["ok"], f"Application tests failed on {resolved['branch']}.\n{result['output']}")
