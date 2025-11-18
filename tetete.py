"""Main application class implementing the Facade pattern."""
# Import types for type annotations (Optional - optional parameter, Mapping - dictionary, Tuple - tuple)
from typing import Optional, Mapping, Tuple
# Import Decimal for precise monetary calculations (avoiding float rounding errors)
from decimal import Decimal

# Import application run mode enumeration
from enums import RunMode
# Import abstract interfaces (DIP principle - dependency on abstractions)
from interfaces import InputHandler, OutputHandler, CurrencyConverter, RateRepository
# Import concrete interface implementations (console input/output handlers, repository, converter)
from implementations import (
    ConsoleInputHandler,      # Implementation for reading data from console
    ConsoleOutputHandler,    # Implementation for outputting data to console
    DefaultRateRepository,   # Storage of exchange rates in memory
    DefaultCurrencyConverter,  # Currency conversion logic
)
# Import menu handler
from menu_handler import MenuHandler
# Import application mode classes
from modes import InteractiveMode, DemoMode
# Import text messages
from messages import UNSUPPORTED_RUN_MODE


class CurrencyClient:
    """
    Facade for working with currency converter.
    
    The class coordinates the work of various system components,
    providing a simple interface for client code.
    Follows SOLID principles:
    - SRP: only coordination of components
    - DIP: depends on abstractions, not concrete implementations
    - OCP: easily extensible with new modes and implementations
    """

    def __init__(
        self,
        # Optional input handler (if not provided, will be created by default)
        input_handler: Optional[InputHandler] = None,
        # Optional output handler (if not provided, will be created by default)
        output_handler: Optional[OutputHandler] = None,
        # Optional rate repository (if not provided, will be created by default)
        rate_repository: Optional[RateRepository] = None,
        # Optional converter (if not provided, will be created by default)
        converter: Optional[CurrencyConverter] = None,
        # Optional initial exchange rates (dictionary: (currency1, currency2) -> rate)
        initial_rates: Optional[Mapping[Tuple, Decimal]] = None,
    ) -> None:
        """
        Initializes client with optional dependency injection.
        
        Args:
            input_handler: Input handler (default: ConsoleInputHandler)
            output_handler: Output handler (default: ConsoleOutputHandler)
            rate_repository: Rate repository (default: DefaultRateRepository)
            converter: Currency converter (default: DefaultCurrencyConverter)
            initial_rates: Initial exchange rates
        """
        # If output handler not provided, create console one by default
        # 'or' operator returns first truthy element (if output_handler is None, creates ConsoleOutputHandler)
        self._output = output_handler or ConsoleOutputHandler()
        # If input handler not provided, create console one by default
        self._input = input_handler or ConsoleInputHandler()
        # If repository not provided, create new one with initial rates (or default)
        self._rate_repository = rate_repository or DefaultRateRepository(initial_rates)
        # If converter not provided, create new one, passing rate repository to it
        self._converter = converter or DefaultCurrencyConverter(self._rate_repository)
        # Create menu handler, passing output handler for menu display
        self._menu_handler = MenuHandler(self._output)

    def run(self, mode: Optional[RunMode] = None) -> None:
        """
        Runs the application in specified mode.
        
        Args:
            mode: Run mode (INTERACTIVE or DEMO).
                 If None, determined automatically based on input type.
        """
        # If mode not explicitly specified, determine automatically
        if mode is None:
            # Check if input is interactive (is there a terminal)
            # If yes - interactive mode, otherwise - demo mode
            mode = RunMode.INTERACTIVE if self._input.is_interactive() else RunMode.DEMO

        # Depending on selected mode, run corresponding logic
        if mode is RunMode.INTERACTIVE:
            # Run interactive mode (with menu and user input)
            self._run_interactive()
        elif mode is RunMode.DEMO:
            # Run demo mode (shows example work without input)
            self._run_demo()
        else:
            # If mode not supported, raise exception
            raise ValueError(UNSUPPORTED_RUN_MODE.format(mode=mode))

    def _run_interactive(self) -> None:
        """Runs interactive mode."""
        # Create interactive mode object, passing all necessary components
        interactive_mode = InteractiveMode(
            input_handler=self._input,        # Input handler for reading user commands
            output_handler=self._output,     # Output handler for displaying information
            converter=self._converter,       # Converter for performing currency conversion
            rate_repository=self._rate_repository,  # Repository for working with rates
            menu_handler=self._menu_handler,  # Handler for displaying menu
        )
        # Run interactive mode (menu loop starts)
        interactive_mode.run()

    def _run_demo(self) -> None:
        """Runs demonstration mode."""
        # Create demo mode object, passing necessary components
        demo_mode = DemoMode(
            output_handler=self._output,     # Output handler for showing results
            converter=self._converter,       # Converter for performing conversion
            rate_repository=self._rate_repository,  # Repository for getting rates
        )
        # Run demo mode (shows conversion example)
        demo_mode.run()


# Check if script is run directly (not imported as module)
if __name__ == "__main__":
    # Create client instance with default settings
    client = CurrencyClient()
    # Can explicitly specify mode: client.run(RunMode.DEMO)
    # Run application (mode will be determined automatically)
    client.run()
