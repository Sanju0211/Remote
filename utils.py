def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculates the Body Mass Index (BMI) given weight in kilograms and height in meters.

    Args:
        weight_kg (float): Weight of the person in kilograms.
        height_m (float): Height of the person in meters.

    Returns:
        float: The calculated BMI. Returns 0.0 if height_m is zero to prevent
               ZeroDivisionError.
    """
    if height_m == 0:
        return 0.0
    try:
        bmi = weight_kg / (height_m ** 2)
        return bmi
    except ZeroDivisionError:
        # This case should ideally be caught by the check above,
        # but as a safeguard:
        return 0.0
