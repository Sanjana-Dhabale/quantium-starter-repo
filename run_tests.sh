#!/bin/bash

# ==========================================
# Quantium - Automated Test Runner Script
# ==========================================

echo "=========================================="
echo "   Quantium Pink Morsel Test Suite"
echo "=========================================="

# Step 1: Activate the virtual environment
echo ""
echo ">> Activating virtual environment..."

# Windows (Git Bash) path
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    echo ">> Virtual environment activated (Windows)"
# Mac/Linux path
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo ">> Virtual environment activated (Mac/Linux)"
else
    echo "ERROR: Virtual environment not found!"
    exit 1
fi

# Step 2: Run the test suite
echo ""
echo ">> Running test suite..."
echo "------------------------------------------"

pytest test_app.py -v

# Step 3: Capture exit code and return it
EXIT_CODE=$?

echo "------------------------------------------"

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ All tests passed! Exit code: 0"
    echo "=========================================="
    exit 0
else
    echo ""
    echo "❌ Some tests failed! Exit code: 1"
    echo "=========================================="
    exit 1
fi