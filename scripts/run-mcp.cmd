@echo off
setlocal

set "REPO_ROOT=%~dp0.."
set "SRC_PATH=%REPO_ROOT%\src"
set "VENV_PYTHON=%REPO_ROOT%\.venv\Scripts\python.exe"

if exist "%VENV_PYTHON%" (
    set "PYTHON=%VENV_PYTHON%"
) else (
    set "PYTHON=python"
)

if "%PYTHONPATH%"=="" (
    set "PYTHONPATH=%SRC_PATH%"
) else (
    set "PYTHONPATH=%SRC_PATH%;%PYTHONPATH%"
)

"%PYTHON%" -m ai_agent_standards_mcp %*
exit /b %ERRORLEVEL%
