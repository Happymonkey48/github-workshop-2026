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
    "menu_draft": None,
    "checkout_wip": None,
    "pricing_useful": None,
    "mobile_menu_before_merge": None,
    "matcha_promo_tip": None,
    "debug_pricing": None,
}