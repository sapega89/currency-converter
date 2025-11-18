@echo off
REM Script to run all code quality checks locally on Windows

echo Running code quality checks...
echo.

echo 1. Checking code formatting with black...
python -m black --check --diff .
if %errorlevel% neq 0 (
    echo [ERROR] Black check failed. Run 'python -m black .' to fix formatting.
    exit /b 1
)
echo [OK] Black check passed
echo.

echo 2. Checking import sorting with isort...
python -m isort --check-only --diff .
if %errorlevel% neq 0 (
    echo [ERROR] isort check failed. Run 'python -m isort .' to fix imports.
    exit /b 1
)
echo [OK] isort check passed
echo.

echo 3. Running flake8 linting...
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
if %errorlevel% neq 0 (
    echo [ERROR] flake8 check found issues.
    exit /b 1
)
echo [OK] flake8 check passed
echo.

echo All checks passed!

