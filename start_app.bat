@echo off
echo =================================================
echo      Counselor Application - Starting Server
echo =================================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt

echo.
echo Checking Firebase credentials...
if not exist "firebase-service-account.json" (
    echo Warning: firebase-service-account.json not found
    echo Please add your Firebase service account key file
    echo.
)

echo.
echo Starting Flask application...
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
