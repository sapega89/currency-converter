# Import dataclass decorator for creating data classes
from dataclasses import dataclass

# Import Decimal for working with monetary amounts
from decimal import Decimal

# Import validation error message
from messages import VALUE_MUST_BE_POSITIVE


def ensure_positive_decimal(value: Decimal, field_name: str) -> None:
    """
    Checks that Decimal value is positive.

    Args:
        value: Value to check
        field_name: Field name (for error message)

    Raises:
        ValueError: If value is less than or equal to zero
    """
    # Check that value is greater than zero
    if value <= 0:
        # If value is not positive, raise exception with descriptive message
        raise ValueError(VALUE_MUST_BE_POSITIVE.format(field_name=field_name))


# @dataclass decorator automatically creates __init__, __repr__, __eq__ and other methods
# frozen=True means object is immutable after creation
@dataclass(frozen=True)
class PositiveDecimal:
    """
    Wrapper class for Decimal, ensuring value is positive.
    Used for validating monetary amounts and exchange rates.
    """

    # amount attribute stores Decimal value
    amount: Decimal

    # __post_init__ method is called automatically after __init__
    # Used for additional validation after object creation
    def __post_init__(self) -> None:
        """
        Performs value validation after object creation.
        Called automatically after __init__.
        """
        # Call validation function to check that amount > 0
        # If value is not positive, ValueError will be raised
        ensure_positive_decimal(self.amount, "amount")
