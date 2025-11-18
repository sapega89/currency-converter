"""Interfaces for following Dependency Inversion Principle (DIP)."""

# Import ABC (Abstract Base Class) for creating abstract classes
from abc import ABC, abstractmethod

# Import Decimal for working with monetary amounts
from decimal import Decimal

# Import Optional for specifying optional types
from typing import Optional

# Import DTOs (Data Transfer Objects) - objects for data transfer
from dtos import ConversionDTO, ConversionResultDTO, DecimalInputDTO, RateUpdateDTO

# Import currency and menu option enumerations
from enums import Currency, MenuOption


class InputHandler(ABC):
    """Abstraction for handling user input."""

    # @abstractmethod decorator means method must be implemented in child classes
    @abstractmethod
    def read_decimal(self, dto: DecimalInputDTO) -> Decimal:
        """
        Reads a decimal number from the user.

        Args:
            dto: Object with request parameters (prompt, default value, validation type)
        Returns:
            Decimal: Read decimal number
        """
        # pass means method has no implementation (abstract)
        pass

    @abstractmethod
    def read_menu_choice(self) -> str:
        """
        Reads user's menu choice.

        Returns:
            str: String with user's choice (e.g., "1", "2", "0")
        """
        pass

    @abstractmethod
    def read_rate_index(self, max_index: int) -> int:
        """
        Reads selected rate index.

        Args:
            max_index: Maximum allowed index (number of available rates)
        Returns:
            int: Selected rate index (from 0 to max_index-1)
        """
        pass

    @abstractmethod
    def is_interactive(self) -> bool:
        """
        Checks if input is interactive.

        Returns:
            bool: True if there is interactive terminal, False if input from file/pipe
        """
        pass


class OutputHandler(ABC):
    """Abstraction for outputting information to user."""

    @abstractmethod
    def print(self, message: str) -> None:
        """
        Prints a message.

        Args:
            message: Message text to output
        """
        pass

    @abstractmethod
    def print_rates(self, rates: dict) -> None:
        """
        Prints current exchange rates.

        Args:
            rates: Dictionary of rates {(currency1, currency2): rate}
        """
        pass

    @abstractmethod
    def print_conversion_result(self, result: ConversionResultDTO) -> None:
        """
        Prints conversion result.

        Args:
            result: Object with conversion results (EUR, USD, CNY)
        """
        pass

    @abstractmethod
    def print_menu(self, menu_items: list) -> None:
        """
        Prints menu.

        Args:
            menu_items: List of menu items to display
        """
        pass

    @abstractmethod
    def print_rate_selection(self, pairs: list) -> None:
        """
        Prints list of available rates for modification.

        Args:
            pairs: List of currency pairs [(currency1, currency2), ...]
        """
        pass


class CurrencyConverter(ABC):
    """Abstraction for currency conversion."""

    @abstractmethod
    def convert(self, dto: ConversionDTO) -> Decimal:
        """
        Converts amount from one currency to another.

        Args:
            dto: Object with conversion parameters (from which currency, to which, amount)
        Returns:
            Decimal: Converted amount
        """
        pass

    @abstractmethod
    def convert_eur_usd_cny(self, eur_amount: Decimal) -> ConversionResultDTO:
        """
        Converts EUR -> USD -> CNY (conversion chain).

        Args:
            eur_amount: Amount in euros for conversion
        Returns:
            ConversionResultDTO: Object with conversion results in all three currencies
        """
        pass


class RateRepository(ABC):
    """Abstraction for storing and managing exchange rates."""

    @abstractmethod
    def get_rate(self, from_currency: Currency, to_currency: Currency) -> Optional[Decimal]:
        """
        Gets exchange rate between currencies.

        Args:
            from_currency: Source currency
            to_currency: Target currency
        Returns:
            Optional[Decimal]: Exchange rate or None if rate not found
        """
        pass

    @abstractmethod
    def update_rate(self, dto: RateUpdateDTO) -> None:
        """
        Updates exchange rate.

        Args:
            dto: Object with data for rate update (currency pair and new rate)
        """
        pass

    @abstractmethod
    def get_all_rates(self) -> dict:
        """
        Returns all rates.

        Returns:
            dict: Dictionary of all rates {(currency1, currency2): rate}
        """
        pass

    @abstractmethod
    def has_rate(self, from_currency: Currency, to_currency: Currency) -> bool:
        """
        Checks if rate exists between currencies.

        Args:
            from_currency: Source currency
            to_currency: Target currency
        Returns:
            bool: True if rate exists (direct or reverse), False otherwise
        """
        pass
