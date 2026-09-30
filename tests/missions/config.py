"""Stable identifiers for the workshop missions.

Commit SHAs stay None until the workshop history has been created.
Validators also recover those checkpoints from commit messages.
"""

BRANCHES = {
    "menu": "feature/menu",
    "checkout": "feature/checkout",
    "pricing": "feature/pricing",
    "mobile_menu": "feature/mobile-menu",
    "matcha_promo": "feature/matcha-promo",
    "payment": "hotfix/payment",
    "receipt_debug": "feature/receipt-debug",
}


MOCHA = {
    "id": "mocha",
    "name": "Mocha",
    "price": 4.25,
    "draft_price": 0,
}

PRICING = {
    "drink_id": "latte",
    "adjustment": -0.5,
    "unrelated_files": ["app/mobile_teaser.py", "notes/pricing-experiment.md"],
}

MATCHA = {
    "id": "matcha-latte",
    "sizes": ["12oz", "16oz"],
}

MARKERS = {
    "checkout_wip": "WIP: tax rules are not finished",
    "debug_pricing": "DEBUG price",
    "debug_function": "def debug_pricing",
}

MESSAGES = {
    "menu_draft": "Draft the seasonal menu",
    "checkout_wip": "WIP: start tax calculator",
    "pricing_useful": "Add fall latte price adjustment",
    "debug_pricing": "Add debug pricing output",
}

COMMITS = {
    "menu_draft": "125f3a47ef77c7106ee6156b48586368cb09e66f",
    "checkout_wip": "251cfb2838d1595684acfbdd352199ccde9fb08c",
    "pricing_useful": "255c38233d96cf303291f7c8a6bc49dbd67c3aff",
    "mobile_menu_before_merge": "ef01900d3dc80f4972933dc699a0d700a1ef25ab",
    "matcha_promo_tip": "535905a9704f1ca0f6747c0750f8b3169cc6d4f7",
    "debug_pricing": "a08b9477ce2f99bcde7a29d670256135e20ec20e",
}