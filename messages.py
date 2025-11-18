"""Centralized storage for all application text messages.

This file contains all strings that are displayed to the user.
Centralizing messages simplifies:
- Internationalization (i18n) - easy to add support for other languages
- Text changes - everything in one place
- Maintenance - easy to find and change any message
"""

# ============================================================================
# Error and warning messages
# ============================================================================

# Warning about empty input using default value
EMPTY_INPUT_USE_DEFAULT = "Empty input, using default value: {default}"

# Error: empty input not allowed
EMPTY_INPUT_NOT_ALLOWED = "Empty input is not allowed here, please enter a number."

# Error: invalid number format
INVALID_NUMBER = "Invalid number, please try again."

# Error: invalid value (general validation error)
INVALID_VALUE = "Invalid value: {error}"

# Error: please enter a valid number
PLEASE_ENTER_VALID_NUMBER = "Please enter a valid number."

# Error: choice out of valid range
CHOICE_OUT_OF_RANGE = "Choice out of range, try again."

# Error: exchange rate not found for currency pair
NO_RATE_FOUND = "No rate for {from_currency} -> {to_currency}"

# Error: unsupported run mode
UNSUPPORTED_RUN_MODE = "Unsupported run mode: {mode}"

# Error: unknown command
UNKNOWN_COMMAND = "Unknown command, please try again."

# Warning prefix
WARN_PREFIX = "[WARN]"

# Validation error message: value must be positive
VALUE_MUST_BE_POSITIVE = "{field_name} must be greater than zero"


# ============================================================================
# User input prompts
# ============================================================================

# Menu choice prompt
YOUR_CHOICE = "Your choice: "

# Option number prompt
OPTION_NUMBER = "Option number: "

# EUR amount input prompt
ENTER_AMOUNT_EUR = "Enter amount in EUR (Enter = 100): "

# New rate input prompt (with current rate in hint)
ENTER_NEW_RATE = "Enter new rate (Enter = keep {current_rate}): "


# ============================================================================
# Exit and completion messages
# ============================================================================

# Application exit message
EXIT_MESSAGE = "Exit."


# ============================================================================
# Headers and output formatting
# ============================================================================

# Exchange rates list header
CURRENT_EXCHANGE_RATES = "\nCurrent exchange rates:"

# Exchange rate display format (1 EUR = 1.25 USD)
RATE_FORMAT = "  1 {from_currency} = {rate} {to_currency}"

# Empty line for separation
EMPTY_LINE = ""

# Conversion result header
CONVERSION_RESULT = "\nConversion result:"

# Currency amount display format (EUR: 100.00)
CURRENCY_AMOUNT_FORMAT = "  {currency}: {amount}"

# Menu header
EXCHANGE_MENU_HEADER = "=== Exchange menu ==="

# Menu item format (1 - Description)
MENU_ITEM_FORMAT = "{option} - {description}"

# Rate selection header
CHOOSE_RATE_TO_CHANGE = "\nChoose a rate to change:"

# Rate list item format (1. EUR -> USD)
RATE_SELECTION_ITEM_FORMAT = "  {index}. {from_currency} -> {to_currency}"

# Current rate message
CURRENT_RATE_MESSAGE = "\nCurrent rate {from_currency} -> {to_currency}: {rate}"

# New rate message
NEW_RATE_MESSAGE = "New rate {from_currency} -> {to_currency}: {rate}"


# ============================================================================
# Menu item descriptions
# ============================================================================

# Convert option description
MENU_CONVERT_DESCRIPTION = "Convert amount (EUR -> USD -> CNY)"

# Change rate option description
MENU_CHANGE_RATE_DESCRIPTION = "Change rate"

# Exit option description
MENU_EXIT_DESCRIPTION = "Exit"


# ============================================================================
# Demo mode
# ============================================================================

# Demo mode message
DEMO_MESSAGE = "[DEMO] Using current rates and amount 100 EUR"
