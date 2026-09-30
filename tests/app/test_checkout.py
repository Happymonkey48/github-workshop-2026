import json
import unittest
from pathlib import Path

from app.checkout import calculate_total
from app.orders import add_drink, calculate_subtotal, create_order


MENU = json.loads((Path(__file__).resolve().parents[2] / "app" / "menu.json").read_text())


class CheckoutTests(unittest.TestCase):
    def test_an_order_starts_empty_and_can_collect_drinks(self):
        order = create_order("Avery")
        self.assertEqual(order["customerName"], "Avery")
        self.assertEqual(order["items"], [])

        add_drink(order, "americano")
        add_drink(order, "latte", 2)
        add_drink(order, "americano")

        self.assertEqual(
            order["items"],
            [
                {"drinkId": "americano", "quantity": 2},
                {"drinkId": "latte", "quantity": 2},
            ],
        )

    def test_subtotal_uses_menu_prices(self):
        order = create_order()
        add_drink(order, "americano")
        add_drink(order, "cappuccino", 2)
        self.assertEqual(calculate_subtotal(order, MENU), 3.5 + 4.75 * 2)

    def test_checkout_total_adds_tax_to_the_subtotal(self):
        order = create_order()
        add_drink(order, "latte")
        self.assertEqual(calculate_total(order, MENU, 0), 4.5)
        self.assertEqual(calculate_total(order, MENU, 0.08), 4.86)

    def test_unknown_drinks_are_rejected(self):
        order = create_order()
        add_drink(order, "espresso")
        with self.assertRaisesRegex(ValueError, "Unknown drink: espresso"):
            calculate_subtotal(order, MENU)
