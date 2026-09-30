def create_order(customer_name=None):
    return {
        "customerName": customer_name or "Guest",
        "items": [],
    }


def add_drink(order, drink_id, quantity=1):
    if not isinstance(order, dict) or not isinstance(order.get("items"), list):
        raise ValueError("order must include items")
    if not drink_id:
        raise ValueError("drink_id is required")
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
        raise ValueError("quantity must be a positive integer")

    existing = next((item for item in order["items"] if item["drinkId"] == drink_id), None)
    if existing:
        existing["quantity"] += quantity
    else:
        order["items"].append({"drinkId": drink_id, "quantity": quantity})
    return order


def calculate_subtotal(order, menu):
    if not isinstance(order, dict) or not isinstance(order.get("items"), list):
        raise ValueError("order must include items")
    if not isinstance(menu, dict) or not isinstance(menu.get("drinks"), list):
        raise ValueError("menu must include drinks")

    total = 0
    for item in order["items"]:
        drink = next((entry for entry in menu["drinks"] if entry["id"] == item["drinkId"]), None)
        if drink is None:
            raise ValueError(f"Unknown drink: {item['drinkId']}")
        total += drink["price"] * item["quantity"]
    return total
