#!/bin/bash
set -e

REQUIRED_VERSION="3.13"
PYTHON_BIN="python3.13"

echo "=== Checking for Python $REQUIRED_VERSION ==="

# Check if python3.13 exists
if command -v $PYTHON_BIN >/dev/null 2>&1; then
    INSTALLED_VERSION="$($PYTHON_BIN -V | awk '{print $2}')"

    if [ "$INSTALLED_VERSION" = "$REQUIRED_VERSION" ]; then
        echo "✔ Python $REQUIRED_VERSION is installed."
        USE_SYSTEM_PYTHON=true
    else
        echo "⚠ Python 3.13 found, but version is $INSTALLED_VERSION (required: $REQUIRED_VERSION)."
        USE_SYSTEM_PYTHON=false
    fi
else
    echo "❌ Python 3.13 is NOT installed."
    USE_SYSTEM_PYTHON=false
fi


echo "=== Setting up environment with uv ==="
pip install uv || pip3 install uv

echo "=== Creating uv environment ==="
uv venv .venv

echo "=== Activating venv ==="
source .venv/bin/activate


echo "=== Installing project deps from pyproject.toml ==="
uv pip install -e .

# or:
# uv pip install -r requirements.txt   # if you ever add one


# -------------------------
#   RUNNING THE PROGRAM
# -------------------------

if [ "$USE_SYSTEM_PYTHON" = true ]; then
    echo "=== Running main.py using system Python $REQUIRED_VERSION ==="
    $PYTHON_BIN main.py
else
    echo "=== Python 3.13.2 not available — installing modules and running pyexec.py instead ==="
    python pyexec.py
fi

# always run these afterwards:
echo "=== Running pyexec.py (special script) ==="
python pyexec.py

echo "=== Running Manim animation ==="
manim mymanim.py MyManimClass -p -qL

echo "=== Done! ==="
