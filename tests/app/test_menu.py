import json
import unittest
from pathlib import Path


MENU_PATH = Path(__file__).resolve().parents[2] / "app" / "menu.json"


def load_menu():
    return json.loads(MENU_PATH.read_text())


class MenuTests(unittest.TestCase):
    def test_menu_lists_the_core_drinks(self):
        menu = load_menu()
        ids = [drink["id"] for drink in menu["drinks"]]
        self.assertEqual(ids[:3], ["americano", "latte", "cappuccino"])

    def test_every_drink_has_a_unique_id_name_and_positive_price(self):
        menu = load_menu()
        ids = set()
        for drink in menu["drinks"]:
            self.assertIsInstance(drink["id"], str)
            self.assertGreater(len(drink["id"]), 0)
            self.assertIsInstance(drink["name"], str)
            self.assertGreater(len(drink["name"]), 0)
            self.assertIsInstance(drink["price"], (int, float))
            self.assertNotIsInstance(drink["price"], bool)
            self.assertGreater(drink["price"], 0, f"{drink['id']} should cost more than 0")
            self.assertNotIn(drink["id"], ids, f"{drink['id']} is duplicated")
            ids.add(drink["id"])
