"""Main entry point for the currency converter application."""

# Import CurrencyClient from app package
from app.main import CurrencyClient

# Check if script is run directly (not imported as module)
if __name__ == "__main__":
    # Create client instance with default settings
    client = CurrencyClient()
    # Run application (mode will be determined automatically)
    client.run()
