from app.orders import calculate_subtotal


def round_money(amount):
    return round(amount + 1e-9, 2)


def calculate_total(order, menu, tax_rate=0):
    if not isinstance(order, dict) or not isinstance(order.get("items"), list):
        raise ValueError("order must include items")
    if not isinstance(tax_rate, (int, float)) or isinstance(tax_rate, bool) or tax_rate < 0:
        raise ValueError("tax_rate cannot be negative")

    subtotal = calculate_subtotal(order, menu)
    return round_money(subtotal + subtotal * tax_rate)


def apply_payment(total, amount_paid):
    if not isinstance(total, (int, float)) or isinstance(total, bool):
        raise ValueError("total and amount_paid must be numbers")
    if not isinstance(amount_paid, (int, float)) or isinstance(amount_paid, bool):
        raise ValueError("total and amount_paid must be numbers")
    if amount_paid < total:
        raise ValueError("Insufficient payment")

    return round_money(amount_paid - total - total)
