@echo off
echo Setting up Image Utilities...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found. Setting up virtual environment...
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created successfully
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)

echo ✓ Virtual environment activated
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements...
echo.

REM Install core requirements
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Warning: Failed to install some core requirements.
)

REM Install channel packer requirements
if exist "channels-packing\requirements.txt" (
    echo Installing channel packer requirements...
    pip install -r channels-packing\requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Warning: Failed to install some channel packer requirements.
    )
)

echo.
echo Setup complete!
echo.
echo Virtual environment has been created and all dependencies installed.
echo.
echo You can now run:
echo - run_utils.bat   (Unified UI with all tools)
echo.
echo Note: The scripts will automatically activate the virtual environment.
echo If you want to run manually, first activate with: venv\Scripts\activate.bat
echo.
pause
