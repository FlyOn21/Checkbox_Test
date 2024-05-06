from decimal import Decimal, Context, ROUND_HALF_UP


def number_to_decimal(number: float | Decimal | int) -> Decimal:
    """
    Convert float to Decimal
    :param number: float or Decimal
    :return: Decimal
    """
    TWOPLACES = Decimal("0.01")
    DECIMAL_CONTEXT = Context(prec=28, rounding=ROUND_HALF_UP)
    # Validate the input
    if not isinstance(number, (float, Decimal, int)):
        raise ValueError("Input must be a float or Decimal")
    if isinstance(number, int):
        number = float(number)
    return Decimal(str(number), context=DECIMAL_CONTEXT).quantize(TWOPLACES)


def test_number_to_decimal():
    assert number_to_decimal(100) == Decimal("100.00")
