# Import dataclass decorator for creating data classes
from dataclasses import dataclass

# Import Decimal for working with monetary amounts
from decimal import Decimal

# Import Optional for specifying optional fields
from typing import Optional

# Import currency, menu option, and input type enumerations
from .enums import Currency, InputKind, MenuOption

# Import class for positive number validation and validation function
from .fields import PositiveDecimal, ensure_positive_decimal


# @dataclass decorator automatically creates __init__, __repr__, __eq__ and other methods
# frozen=True means object is immutable after creation
@dataclass(frozen=True)
class CurrencyPairDTO:
    """
    DTO (Data Transfer Object) for currency pair.
    Used as base class for other DTOs.
    """

    # Source currency (from which we convert)
    from_currency: Currency
    # Target currency (to which we convert)
    to_currency: Currency


# Inherit from CurrencyPairDTO, adding amount field
@dataclass(frozen=True)
class ConversionDTO(CurrencyPairDTO):
    """
    DTO for currency conversion request.
    Contains currency pair and amount for conversion.
    """

    # Amount for conversion (wrapped in PositiveDecimal for validation)
    amount: PositiveDecimal


# Inherit from CurrencyPairDTO, adding rate field
@dataclass(frozen=True)
class RateUpdateDTO(CurrencyPairDTO):
    """
    DTO for exchange rate update.
    Contains currency pair and new rate.
    """

    # New exchange rate (wrapped in PositiveDecimal for validation)
    rate: PositiveDecimal


# Doesn't inherit from CurrencyPairDTO, as it contains conversion results
@dataclass(frozen=True)
class ConversionResultDTO:
    """
    DTO for conversion result.
    Contains amounts in all three currencies after conversion.
    """

    # Amount in euros (original or after conversion)
    eur: Decimal
    # Amount in dollars (after conversion from EUR)
    usd: Decimal
    # Amount in yuan (after conversion from USD)
    cny: Decimal


@dataclass(frozen=True)
class MenuItemDTO:
    """
    DTO for menu item.
    Contains menu option and its description.
    """

    # Menu option (e.g., MenuOption.CONVERT with value "1")
    option: MenuOption
    # Text description of option (e.g., "Convert amount")
    description: str


@dataclass(frozen=True)
class DecimalInputDTO:
    """
    DTO for decimal number input request.
    Contains parameters for input configuration (prompt, default value, validation type).
    """

    # Prompt text shown to user before input
    prompt: str
    # Default value (if user presses Enter without input)
    # Optional means this field can be None
    default: Optional[Decimal] = None
    # Validation type (ANY - any number, POSITIVE - only positive)
    # Default is ANY (any number)
    kind: InputKind = InputKind.ANY

    def validate(self, value: Decimal) -> None:
        """
        Validates entered value according to validation type.

        Args:
            value: Value to validate

        Raises:
            ValueError: If value doesn't pass validation
        """
        # If positive validation required
        if self.kind is InputKind.POSITIVE:
            # Call validation function (will raise ValueError if value <= 0)
            ensure_positive_decimal(value, "value")
