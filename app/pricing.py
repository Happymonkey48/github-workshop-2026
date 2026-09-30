FALL_ADJUSTMENTS = {
    "latte": -0.5,
}


def adjustment_for(drink_id):
    if drink_id in FALL_ADJUSTMENTS:
        return FALL_ADJUSTMENTS[drink_id]
    return 0
