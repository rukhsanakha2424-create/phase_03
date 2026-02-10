@echo off
echo Starting backend server on port 8000...

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    pip install -r requirements.txt
)

REM Start the server
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload