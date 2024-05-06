from decimal import Decimal

from src.settings.checkbox_settings import settings


def validate_decimal_places(value: float | Decimal) -> bool:
    """
    Validate that the number of decimal places in a float or Decimal does not exceed 2.

    Args:
        value (float | Decimal): The value to check.

    Returns:
        bool: True if the number of decimal places is 2 or less, False otherwise.

    Raises:
        ValueError: If the value is not a float, Decimal, or int.
    """
    if not isinstance(value, (int, float, Decimal)):
        raise ValueError("Value must be a Decimal, float, or int")
    value_str = str(value)
    if "." in value_str:
        decimal_part = value_str.split(".")[1]
        if len(decimal_part) > settings.decimal_places:
            return False
    return True
