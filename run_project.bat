@echo off
setlocal ENABLEEXTENSIONS

set REQUIRED_VERSION=3.13
set PYTHON_BIN=python3.13

echo === Checking for Python %REQUIRED_VERSION% ===

:: Check if python3.13 command exists
where %PYTHON_BIN% >nul 2>&1
if %ERRORLEVEL%==0 (
    for /f "tokens=2 delims= " %%v in ('%PYTHON_BIN% -V') do set INSTALLED_VERSION=%%v

    if "%INSTALLED_VERSION%"=="%REQUIRED_VERSION%" (
        echo ✔ Python %REQUIRED_VERSION% is installed.
        set USE_SYSTEM_PYTHON=true
    ) else (
        echo ⚠ Python 3.13 found, but version is %INSTALLED_VERSION% (required: %REQUIRED_VERSION%).
        set USE_SYSTEM_PYTHON=false
    )
) else (
    echo ❌ Python 3.13.2 is NOT installed.
    set USE_SYSTEM_PYTHON=false
)

echo.
echo === Installing uv ===
pip install uv || pip3 install uv

echo.
echo === Creating uv virtual environment ===
uv venv .venv

echo.
echo === Activating venv ===
call .venv\Scripts\activate.bat

echo.
echo === Installing project dependencies from pyproject.toml ===
uv pip install -e .

echo.
echo ------------------------------
echo     RUNNING PROGRAM
echo ------------------------------

if "%USE_SYSTEM_PYTHON%"=="true" (
    echo === Running main.py using system Python %REQUIRED_VERSION% ===
    %PYTHON_BIN% main.py
) else (
    echo === Python 3.13.2 not available — running pyexec.py instead ===
    python pyexec.py
)

echo.
echo === Running pyexec.py ===
python pyexec.py

echo.
echo === Running Manim animation ===
manim mymanim.py MyManimClass -p -ql

echo.
echo === Done! ===
pause
