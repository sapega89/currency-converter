# Import Decimal for working with monetary amounts
from decimal import Decimal

# Import Enum for creating enumerations
from enum import Enum

# Import types for annotations
from typing import Dict, Tuple


# Create currency enumeration
# Enum is a class for creating enumerations (named constants)
class Currency(Enum):
    """
    Enumeration of supported currencies.
    Each currency has a string value for display.
    """

    # Euro with value "EUR"
    EUR = "EUR"
    # US Dollar with value "USD"
    USD = "USD"
    # Chinese Yuan with value "CNY"
    CNY = "CNY"


# Create menu option enumeration
class MenuOption(Enum):
    """
    Menu option enumeration.
    Values are strings that user enters to select option.
    """

    # Convert option with value "1" (user enters "1")
    CONVERT = "1"
    # Change rate option with value "2" (user enters "2")
    CHANGE_RATE = "2"
    # Exit option with value "0" (user enters "0")
    EXIT = "0"


# Create input validation type enumeration
class InputKind(Enum):
    """
    Input validation type enumeration.
    Defines what checks to perform when entering a number.
    """

    # Any number (no restrictions)
    ANY = "any"
    # Only positive number (greater than zero)
    POSITIVE = "positive"


# Create application run mode enumeration
class RunMode(Enum):
    """
    Application run mode enumeration.
    """

    # Interactive mode (with menu and user input)
    INTERACTIVE = "interactive"
    # Demonstration mode (shows example without input)
    DEMO = "demo"


# Create base exchange rate enumeration
class BaseRate(Enum):
    """
    Base exchange rate enumeration.
    Each element contains tuple: (currency1, currency2, rate).
    """

    # Rate EUR -> USD: 1 euro = 1.25 dollars
    # Value is tuple of three elements
    EUR_USD = (Currency.EUR, Currency.USD, Decimal("1.25"))
    # Rate USD -> CNY: 1 dollar = 6.91 yuan
    USD_CNY = (Currency.USD, Currency.CNY, Decimal("6.91"))

    # Property for getting currency pair from enumeration value
    @property
    def pair(self) -> Tuple[Currency, Currency]:
        """
        Returns currency pair from enumeration value.

        Returns:
            Tuple[Currency, Currency]: Tuple (currency1, currency2)
        """
        # self.value is tuple (Currency.EUR, Currency.USD, Decimal("1.25"))
        # [0] - first currency, [1] - second currency
        return self.value[0], self.value[1]

    # Property for getting rate from enumeration value
    @property
    def rate(self) -> Decimal:
        """
        Returns exchange rate from enumeration value.

        Returns:
            Decimal: Exchange rate
        """
        # self.value[2] is third element of tuple (rate)
        return self.value[2]

    # Class method (works with class, not instance)
    @classmethod
    def to_rates(cls) -> Dict:
        """
        Converts all enumeration elements to rates dictionary.

        Returns:
            Dict: Dictionary {(currency1, currency2): rate}
        """
        # Dictionary comprehension
        # Iterate through all enumeration elements (cls is BaseRate class)
        # For each element create key-value pair: (currency pair): rate
        return {member.pair: member.rate for member in cls}
