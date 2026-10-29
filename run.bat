@echo off
TITLE Signova - AI-Based Sign Language Recognition System
echo ======================================================================
echo           SIGNOVA: AI-BASED SIGN LANGUAGE RECOGNITION
echo               3rd-Year CSE Mini Project Launcher
echo ======================================================================
echo.

cd /d "%~dp0"

IF EXIST "%~dp0venv\Scripts\python.exe" (
    SET "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
) ELSE (
    SET "PYTHON_EXE=python"
)

echo [+] Testing system diagnostics...
"%PYTHON_EXE%" test_cam.py
echo.

echo [+] Launching Signova Streamlit Web Application...
echo [+] Opening browser at http://localhost:8501
echo.
"%PYTHON_EXE%" -m streamlit run app.py

pause
