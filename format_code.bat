@echo off
REM Script to automatically format code with black and isort

echo Formatting code...
echo.

echo Running black...
python -m black .
if %errorlevel% neq 0 (
    echo [ERROR] Black formatting failed.
    exit /b 1
)
echo [OK] Black formatting completed
echo.

echo Running isort...
python -m isort .
if %errorlevel% neq 0 (
    echo [ERROR] isort formatting failed.
    exit /b 1
)
echo [OK] isort formatting completed
echo.

echo Code formatting completed successfully!

