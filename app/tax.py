"""WIP tax calculator."""


# WIP: tax rules are not finished. Do not ship this.
def estimate_tax(subtotal):
    if not isinstance(subtotal, (int, float)) or isinstance(subtotal, bool):
        raise ValueError("subtotal must be a number")

    # Regional rates are not wired up yet.
    return None
