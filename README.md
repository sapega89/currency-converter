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
├── main.py                # Main application entry point
├── app/                   # Application package
│   ├── __init__.py        # Package initialization
│   ├── main.py            # Main application class (CurrencyClient)
│   ├── interfaces.py      # Abstract interfaces (DIP)
│   ├── implementations.py # Concrete implementations
│   ├── modes.py           # Application modes (Interactive, Demo)
│   ├── menu_handler.py    # Menu handling
│   ├── dtos.py            # Data Transfer Objects
│   ├── enums.py           # Enumerations
│   ├── fields.py          # Field validation
│   └── messages.py        # Centralized text messages
├── dist/                  # Build output (executable files)
│   └── currency-converter.exe  # Standalone executable
├── build_exe.bat          # Script to build executable
├── build_exe.spec         # PyInstaller spec file
└── .github/               # CI/CD workflows
    └── workflows/
        └── lint.yml
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
```

The executable will be created in the `dist/` directory as `currency-converter.exe` (Windows) or `currency-converter` (Linux/Mac).

**Requirements:**
- Install build dependencies: `pip install -r requirements-build.txt`
- Or PyInstaller will be installed automatically by the build script

## Design Patterns

- **Facade Pattern**: `CurrencyClient` provides simple interface to complex subsystem
- **Dependency Injection**: Components can be injected for testing and flexibility
- **Strategy Pattern**: Different modes (Interactive, Demo) can be easily added

## Development

### Code Quality

The project uses automated code quality checks:

- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting

### Local Setup

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

### Running Checks Locally

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Check code with flake8
flake8 .

# Run all checks
black --check . && isort --check-only . && flake8 .
```

### CI/CD

GitHub Actions automatically runs code quality checks on:
- Every push to `main` or `develop` branches
- Every pull request

The pipeline checks:
- Code formatting (black)
- Import sorting (isort)
- Code linting (flake8)

## Building Executable

To create a standalone executable file for Windows:

### Prerequisites

Install build dependencies:

```bash
pip install -r requirements-build.txt
```

### Build Process

Run the build script:

Or manually:

```bash
python -m PyInstaller --onefile --name currency-converter --console main.py
```

The executable will be created in:
- `dist/currency-converter.exe` (build output)
- `app/currency-converter.exe` (application folder, ready for distribution)

### Manual Build with Spec File

For more control, use the spec file:

```bash
python -m PyInstaller build_exe.spec
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)
- PyInstaller (only for building executable)

## License

MIT
