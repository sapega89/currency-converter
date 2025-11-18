"""Implementations of various application modes."""
# Import Decimal for working with monetary amounts
from decimal import Decimal
# Import Tuple for type annotations
from typing import Tuple

# Import DTOs for data handling
from dtos import ConversionResultDTO, DecimalInputDTO, RateUpdateDTO
# Import enumerations
from enums import Currency, MenuOption, InputKind
# Import class for positive number validation
from fields import PositiveDecimal
# Import interfaces for typing
from interfaces import InputHandler, OutputHandler, CurrencyConverter, RateRepository
# Import text messages
from messages import (
    EXIT_MESSAGE,
    UNKNOWN_COMMAND,
    CURRENT_RATE_MESSAGE,
    ENTER_NEW_RATE,
    INVALID_VALUE,
    NEW_RATE_MESSAGE,
    ENTER_AMOUNT_EUR,
    DEMO_MESSAGE,
)


class InteractiveMode:
    """Interactive user interaction mode."""

    def __init__(
        self,
        # Input handler for reading user commands
        input_handler: InputHandler,
        # Output handler for displaying information
        output_handler: OutputHandler,
        # Converter for performing currency conversion
        converter: CurrencyConverter,
        # Repository for working with exchange rates
        rate_repository: RateRepository,
        # Menu handler (no typing as it's not an interface)
        menu_handler,
    ) -> None:
        # Save input handler as class attribute
        self._input = input_handler
        # Save output handler as class attribute
        self._output = output_handler
        # Save converter as class attribute
        self._converter = converter
        # Save repository as class attribute
        self._rate_repository = rate_repository
        # Save menu handler as class attribute
        self._menu_handler = menu_handler

    def run(self) -> None:
        """Runs interactive mode."""
        # Infinite menu loop (until user chooses exit)
        while True:
            # Get all rates from repository and display them
            self._output.print_rates(self._rate_repository.get_all_rates())
            # Display menu to user
            self._menu_handler.display_menu()

            # Read user's menu choice
            choice = self._input.read_menu_choice()

            # If user chose exit
            if choice == MenuOption.EXIT.value:
                # Print exit message
                self._output.print(EXIT_MESSAGE)
                # Break loop and exit method
                break

            # If user chose rate change
            if choice == MenuOption.CHANGE_RATE.value:
                # Call rate change handling method
                self._handle_rate_change()
                # Continue loop (return to start, show menu again)
                continue

            # If user chose conversion
            if choice == MenuOption.CONVERT.value:
                # Call conversion handling method
                self._handle_conversion()
                # Continue loop
                continue

            # If choice not recognized, print error message
            self._output.print(UNKNOWN_COMMAND)

    def _handle_rate_change(self) -> None:
        """Handles exchange rate change."""
        # Get list of all currency pairs from repository
        # .keys() returns dictionary keys (currency pairs), list() converts to list
        pairs = list(self._rate_repository.get_all_rates().keys())
        # Display list of available rates for selection
        self._output.print_rate_selection(pairs)

        # Read selected rate index from user
        # len(pairs) - number of available rates
        index = self._input.read_rate_index(len(pairs))
        # Get currency pair by selected index
        # pairs[index] is tuple (currency1, currency2)
        from_cur, to_cur = pairs[index]
        # Get current rate for selected currency pair
        current_rate = self._rate_repository.get_all_rates()[(from_cur, to_cur)]

        # Display current rate to user
        self._output.print(CURRENT_RATE_MESSAGE.format(from_currency=from_cur.value, to_currency=to_cur.value, rate=current_rate))

        # Infinite loop for retrying on input error
        while True:
            # Request new rate from user
            new_rate_value = self._input.read_decimal(
                DecimalInputDTO(
                    prompt=ENTER_NEW_RATE.format(current_rate=current_rate),  # Hint with current rate
                    default=current_rate,  # Default value (if Enter pressed)
                    kind=InputKind.POSITIVE,  # Validation: rate must be positive
                )
            )
            try:
                # Create DTO for rate update
                rate_dto = RateUpdateDTO(
                    from_currency=from_cur,  # Source currency
                    to_currency=to_cur,      # Target currency
                    rate=PositiveDecimal(new_rate_value),  # New rate (wrapped for validation)
                )
            # If validation failed (e.g., rate is negative)
            except ValueError as exc:
                # Print error message and continue loop
                self._output.print(INVALID_VALUE.format(error=exc))
                continue

            # Update rate in repository
            self._rate_repository.update_rate(rate_dto)
            # Print success message with new rate
            self._output.print(
                NEW_RATE_MESSAGE.format(
                    from_currency=rate_dto.from_currency.value,
                    to_currency=rate_dto.to_currency.value,
                    rate=rate_dto.rate.amount
                )
            )
            # Break loop (rate successfully updated)
            break

    def _handle_conversion(self) -> None:
        """Handles currency conversion."""
        # Request EUR amount from user
        eur_amount = self._input.read_decimal(
            DecimalInputDTO(
                prompt=ENTER_AMOUNT_EUR,  # Hint
                default=Decimal("100"),  # Default value (100 euros)
                kind=InputKind.POSITIVE,  # Validation: amount must be positive
            )
        )

        try:
            # Perform conversion EUR -> USD -> CNY
            result = self._converter.convert_eur_usd_cny(eur_amount)
        # If conversion failed (e.g., no rate)
        except ValueError as exc:
            # Print error message and exit method
            self._output.print(INVALID_VALUE.format(error=exc))
            return

        # Display conversion result to user
        self._output.print_conversion_result(result)


class DemoMode:
    """Application demonstration mode."""

    def __init__(
        self,
        # Output handler for displaying results
        output_handler: OutputHandler,
        # Converter for performing conversion
        converter: CurrencyConverter,
        # Repository for getting rates
        rate_repository: RateRepository,
    ) -> None:
        # Save output handler
        self._output = output_handler
        # Save converter
        self._converter = converter
        # Save repository
        self._rate_repository = rate_repository

    def run(self) -> None:
        """Runs demonstration mode."""
        # Perform conversion of 100 euros to USD and then to CNY
        result = self._converter.convert_eur_usd_cny(Decimal("100"))
        # Print informational message about demo mode
        self._output.print(DEMO_MESSAGE)
        # Print current exchange rates
        self._output.print_rates(self._rate_repository.get_all_rates())
        # Print conversion result
        self._output.print_conversion_result(result)
