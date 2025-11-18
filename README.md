# Currency Converter

A well-structured currency converter application following SOLID principles and OOP best practices.

## Features

- Convert currencies: EUR → USD → CNY
- Interactive menu-driven interface
- Demo mode for quick testing
- Exchange rate management
- Clean architecture with separation of concerns

## Architecture

The project follows SOLID principles:

- **Single Responsibility Principle (SRP)**: Each class has a single, well-defined responsibility
- **Open/Closed Principle (OCP)**: Easy to extend with new modes and implementations
- **Liskov Substitution Principle (LSP)**: Implementations can be substituted
- **Interface Segregation Principle (ISP)**: Interfaces are specific and focused
- **Dependency Inversion Principle (DIP)**: Dependencies on abstractions, not concrete implementations

## Project Structure

```
convertert/
├── tetete.py              # Main application class (Facade pattern)
├── interfaces.py          # Abstract interfaces (DIP)
├── implementations.py      # Concrete implementations
├── modes.py               # Application modes (Interactive, Demo)
├── menu_handler.py        # Menu handling
├── dtos.py                # Data Transfer Objects
├── enums.py               # Enumerations
├── fields.py              # Field validation
└── messages.py            # Centralized text messages
```

## Usage

### Basic Usage

```python
from convertert import CurrencyClient

# Create client with default settings
client = CurrencyClient()

# Run application (mode determined automatically)
client.run()
```

### With Custom Settings

```python
from convertert import CurrencyClient
from convertert.enums import RunMode

# Create client
client = CurrencyClient()

# Run in specific mode
client.run(RunMode.DEMO)  # or RunMode.INTERACTIVE
```

### Direct Execution

```bash
python tetete.py
```

## Design Patterns

- **Facade Pattern**: `CurrencyClient` provides simple interface to complex subsystem
- **Dependency Injection**: Components can be injected for testing and flexibility
- **Strategy Pattern**: Different modes (Interactive, Demo) can be easily added

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## License

MIT

