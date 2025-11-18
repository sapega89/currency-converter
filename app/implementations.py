"""Interface implementations."""

# Import sys for checking input type (interactive or not)
import sys

# Import Decimal for precise calculations and InvalidOperation for error handling
from decimal import Decimal, InvalidOperation

# Import types for annotations
from typing import Dict, Mapping, Optional, Tuple

# Import DTOs (Data Transfer Objects)
from .dtos import ConversionDTO  # DTO for conversion request
from .dtos import ConversionResultDTO  # DTO for conversion result
from .dtos import DecimalInputDTO  # DTO for decimal input request
from .dtos import MenuItemDTO  # DTO for menu item
from .dtos import RateUpdateDTO  # DTO for rate update

# Import enumerations and base rates
from .enums import BaseRate, Currency, MenuOption

# Import class for positive number validation
from .fields import PositiveDecimal

# Import abstract interfaces that we implement
from .interfaces import CurrencyConverter  # Interface for conversion
from .interfaces import InputHandler  # Interface for input
from .interfaces import OutputHandler  # Interface for output
from .interfaces import RateRepository  # Interface for rate storage

# Import all text messages
from .messages import (
    CHOICE_OUT_OF_RANGE,
    CHOOSE_RATE_TO_CHANGE,
    CONVERSION_RESULT,
    CURRENCY_AMOUNT_FORMAT,
    CURRENT_EXCHANGE_RATES,
    EMPTY_INPUT_NOT_ALLOWED,
    EMPTY_INPUT_USE_DEFAULT,
    EMPTY_LINE,
    EXCHANGE_MENU_HEADER,
    INVALID_NUMBER,
    INVALID_VALUE,
    MENU_ITEM_FORMAT,
    NO_RATE_FOUND,
    OPTION_NUMBER,
    PLEASE_ENTER_VALID_NUMBER,
    RATE_FORMAT,
    RATE_SELECTION_ITEM_FORMAT,
    WARN_PREFIX,
    YOUR_CHOICE,
)


class ConsoleInputHandler(InputHandler):
    """Console input handler implementation."""

    def read_decimal(self, dto: DecimalInputDTO) -> Decimal:
        """Reads a decimal number from the user."""
        # Infinite loop for retrying on input error
        while True:
            # Read string from user, strip whitespace from start and end
            raw = input(dto.prompt).strip()

            # If input is empty and default value exists
            if not raw and dto.default is not None:
                # Print warning and use default value
                self._print_warning(EMPTY_INPUT_USE_DEFAULT.format(default=dto.default))
                value = dto.default
            # If input is empty and no default value
            elif not raw:
                # Print error and continue loop (request input again)
                self._print_error(EMPTY_INPUT_NOT_ALLOWED)
                continue
            # If input is not empty
            else:
                try:
                    # Try to convert string to Decimal
                    value = Decimal(raw)
                # If conversion failed (not a number)
                except (InvalidOperation, ValueError):
                    # Print error and continue loop
                    self._print_error(INVALID_NUMBER)
                    continue

            # Try to validate value (e.g., check that it's positive)
            try:
                # Call validation method from DTO
                dto.validate(value)
            # If validation failed
            except ValueError as exc:
                # Print error message and continue loop
                self._print_error(INVALID_VALUE.format(error=exc))
                continue

            # If all checks passed, return value
            return value

    def read_menu_choice(self) -> str:
        """Reads user's menu choice."""
        # Read string from user, strip whitespace
        return input(YOUR_CHOICE).strip()

    def read_rate_index(self, max_index: int) -> int:
        """Reads selected rate index."""
        # Infinite loop for retrying on error
        while True:
            # Read user's choice
            choice = input(OPTION_NUMBER).strip()
            try:
                # Try to convert string to integer
                index = int(choice)
            # If conversion failed
            except ValueError:
                # Print error and continue loop
                self._print_error(PLEASE_ENTER_VALID_NUMBER)
                continue

            # Check if index is in valid range (from 1 to max_index)
            if 1 <= index <= max_index:
                # Return index decreased by 1 (user enters 1..N, we use 0..N-1)
                return index - 1

            # If index out of range, print error and continue loop
            self._print_error(CHOICE_OUT_OF_RANGE)

    def is_interactive(self) -> bool:
        """Checks if input is interactive."""
        try:
            # Check if terminal is connected (isatty = "is a teletype")
            # True if user inputs from keyboard, False if input from file/pipe
            return sys.stdin.isatty()
        # If any error occurred (e.g., stdin unavailable)
        except Exception:
            # Consider input as non-interactive
            return False

    # Static method (doesn't require class instance to call)
    @staticmethod
    def _print_warning(message: str) -> None:
        # Prints warning with [WARN] prefix
        print(f"{WARN_PREFIX} {message}")

    @staticmethod
    def _print_error(message: str) -> None:
        # Prints error message
        print(message)


class ConsoleOutputHandler(OutputHandler):
    """Console output handler implementation."""

    def print(self, message: str) -> None:
        """Prints a message."""
        # Simply print message to console
        print(message)

    def print_rates(self, rates: dict) -> None:
        """Prints current exchange rates."""
        # Print header
        self.print(CURRENT_EXCHANGE_RATES)
        # Iterate through all rates in dictionary
        # rates.items() returns (key, value) pairs
        # Key is tuple (currency1, currency2), value is rate
        for (from_cur, to_cur), rate in rates.items():
            # Print rate in format "1 EUR = 1.25 USD"
            self.print(RATE_FORMAT.format(from_currency=from_cur.value, rate=rate, to_currency=to_cur.value))
        # Print empty line for separation
        self.print(EMPTY_LINE)

    def print_conversion_result(self, result: ConversionResultDTO) -> None:
        """Prints conversion result."""
        # Print header
        self.print(CONVERSION_RESULT)
        # Print EUR amount (result.eur - attribute of ConversionResultDTO object)
        self.print(CURRENCY_AMOUNT_FORMAT.format(currency=Currency.EUR.value, amount=result.eur))
        # Print USD amount
        self.print(CURRENCY_AMOUNT_FORMAT.format(currency=Currency.USD.value, amount=result.usd))
        # Print CNY amount
        self.print(CURRENCY_AMOUNT_FORMAT.format(currency=Currency.CNY.value, amount=result.cny))

    def print_menu(self, menu_items: list) -> None:
        """Prints menu."""
        # Print menu header
        self.print(EXCHANGE_MENU_HEADER)
        # Iterate through all menu items
        for item in menu_items:
            # Print each item in format "1 - Description"
            # item.option.value - option value (e.g., "1"), item.description - description
            self.print(MENU_ITEM_FORMAT.format(option=item.option.value, description=item.description))

    def print_rate_selection(self, pairs: list) -> None:
        """Prints list of available rates for modification."""
        # Print header
        self.print(CHOOSE_RATE_TO_CHANGE)
        # Iterate through currency pairs with numbering starting from 1
        # enumerate(pairs, start=1) returns (index, element), indices start from 1
        for idx, (from_cur, to_cur) in enumerate(pairs, start=1):
            # Print each rate in format "1. EUR -> USD"
            self.print(RATE_SELECTION_ITEM_FORMAT.format(index=idx, from_currency=from_cur.value, to_currency=to_cur.value))


class DefaultRateRepository(RateRepository):
    """RateRepository implementation for storing rates in memory."""

    def __init__(self, initial_rates: Optional[Mapping[Tuple[Currency, Currency], Decimal]] = None) -> None:
        # Get default rates from BaseRate enumeration
        # BaseRate.to_rates() returns dictionary {(EUR, USD): 1.25, (USD, CNY): 6.91}
        default_rates: Dict[Tuple[Currency, Currency], Decimal] = BaseRate.to_rates()
        # If initial rates provided, use them, otherwise use default rates
        # dict() creates copy of dictionary to avoid modifying original
        self._rates: Dict[Tuple[Currency, Currency], Decimal] = dict(initial_rates or default_rates)

    def get_rate(self, from_currency: Currency, to_currency: Currency) -> Optional[Decimal]:
        """Gets exchange rate between currencies."""
        # Create key for direct rate (from first currency to second)
        direct_key: Tuple[Currency, Currency] = (from_currency, to_currency)
        # If direct rate exists in dictionary
        if direct_key in self._rates:
            # Return it
            return self._rates[direct_key]

        # Create key for reverse rate (from second currency to first)
        reverse_key: Tuple[Currency, Currency] = (to_currency, from_currency)
        # If reverse rate exists in dictionary
        if reverse_key in self._rates:
            # Return it (later will need to divide by it, not multiply)
            return self._rates[reverse_key]

        # If neither direct nor reverse rate found, return None
        return None

    def update_rate(self, dto: RateUpdateDTO) -> None:
        """Updates exchange rate."""
        # Create key from currency pair
        key = (dto.from_currency, dto.to_currency)
        # Update rate in dictionary
        # dto.rate.amount - Decimal value from PositiveDecimal object
        self._rates[key] = dto.rate.amount

    def get_all_rates(self) -> dict:
        """Returns all rates."""
        # Return copy of dictionary so external code can't modify original
        return self._rates.copy()

    def has_rate(self, from_currency: Currency, to_currency: Currency) -> bool:
        """Checks if rate exists between currencies."""
        # Create key for direct rate
        direct_key = (from_currency, to_currency)
        # Create key for reverse rate
        reverse_key = (to_currency, from_currency)
        # Return True if at least one rate exists (direct or reverse)
        return direct_key in self._rates or reverse_key in self._rates


class DefaultCurrencyConverter(CurrencyConverter):
    """CurrencyConverter implementation for currency conversion."""

    def __init__(self, rate_repository: RateRepository) -> None:
        # Save rate repository for use in conversion methods
        self._rate_repository = rate_repository

    def convert(self, dto: ConversionDTO) -> Decimal:
        """Converts amount from one currency to another."""
        # Extract amount from DTO (dto.amount is PositiveDecimal, .amount is Decimal value)
        amount_value = dto.amount.amount
        # If converting currency to itself, just return amount unchanged
        if dto.from_currency == dto.to_currency:
            return amount_value

        # Get exchange rate from repository (can be direct or reverse)
        rate = self._rate_repository.get_rate(dto.from_currency, dto.to_currency)
        # If rate not found, raise exception
        if rate is None:
            raise ValueError(NO_RATE_FOUND.format(from_currency=dto.from_currency.value, to_currency=dto.to_currency.value))

        # Determine if this is direct or reverse rate
        # Create key for direct rate
        direct_key = (dto.from_currency, dto.to_currency)
        # Check if direct rate exists in repository
        if direct_key in self._rate_repository.get_all_rates():
            # If rate is direct, multiply amount by rate
            return amount_value * rate
        else:
            # If rate is reverse, divide amount by rate (to get correct result)
            return amount_value / rate

    def convert_eur_usd_cny(self, eur_amount: Decimal) -> ConversionResultDTO:
        """Converts EUR -> USD -> CNY."""
        # Create DTO for conversion from EUR to USD
        eur_to_usd = ConversionDTO(
            from_currency=Currency.EUR,  # Source currency - euro
            to_currency=Currency.USD,  # Target currency - dollar
            amount=PositiveDecimal(eur_amount),  # Amount in euros (wrapped in PositiveDecimal for validation)
        )
        # Perform first conversion: EUR -> USD
        usd_amount = self.convert(eur_to_usd)

        # Create DTO for conversion from USD to CNY
        usd_to_cny = ConversionDTO(
            from_currency=Currency.USD,  # Source currency - dollar
            to_currency=Currency.CNY,  # Target currency - yuan
            amount=PositiveDecimal(usd_amount),  # Amount in dollars (result of previous conversion)
        )
        # Perform second conversion: USD -> CNY
        cny_amount = self.convert(usd_to_cny)

        # Create and return DTO with results of all conversions
        return ConversionResultDTO(
            eur=eur_amount,  # Original amount in euros
            usd=usd_amount,  # Converted amount in dollars
            cny=cny_amount,  # Converted amount in yuan
        )
