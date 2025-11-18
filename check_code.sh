#!/bin/bash
# Script to run all code quality checks locally

echo "Running code quality checks..."
echo ""

echo "1. Checking code formatting with black..."
black --check --diff .
if [ $? -ne 0 ]; then
    echo "❌ Black check failed. Run 'black .' to fix formatting."
    exit 1
fi
echo "✅ Black check passed"
echo ""

echo "2. Checking import sorting with isort..."
isort --check-only --diff .
if [ $? -ne 0 ]; then
    echo "❌ isort check failed. Run 'isort .' to fix imports."
    exit 1
fi
echo "✅ isort check passed"
echo ""

echo "3. Running flake8 linting..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
if [ $? -ne 0 ]; then
    echo "❌ flake8 check found issues."
    exit 1
fi
echo "✅ flake8 check passed"
echo ""

echo "🎉 All checks passed!"

