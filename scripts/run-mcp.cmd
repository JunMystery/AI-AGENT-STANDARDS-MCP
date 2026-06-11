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

:: Detect if the script was double-clicked from Windows Explorer
:: We check if stdin is a console (not redirected) using timeout, and if cmdcmdline indicates a /c launch
set "IS_EXPLORER=0"
timeout /t 0 >nul 2>nul
if %errorlevel% equ 0 (
    echo %cmdcmdline% | findstr /i /c:"/c" >nul
    if %errorlevel% equ 0 (
        echo %cmdcmdline% | findstr /i /c:"run-mcp.cmd" >nul
        if %errorlevel% equ 0 set "IS_EXPLORER=1"
    )
)

if "%IS_EXPLORER%"=="1" (
    if "%~1"=="" (
        echo [INFO] Detected launch from Windows Explorer.
        echo [INFO] Starting MCP server with Streamable HTTP transport...
        "%PYTHON%" -m ai_agent_standards_mcp --transport streamable-http
        echo.
        echo MCP server stopped.
        pause
        exit /b 0
    )
)

"%PYTHON%" -m ai_agent_standards_mcp %*
exit /b %ERRORLEVEL%
