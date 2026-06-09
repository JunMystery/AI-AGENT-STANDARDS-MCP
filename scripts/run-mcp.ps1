param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $McpArgs
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SrcPath = Join-Path $RepoRoot "src"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (Test-Path -LiteralPath $VenvPython) {
    $Python = $VenvPython
} else {
    $Python = "python"
}

if ([string]::IsNullOrEmpty($env:PYTHONPATH)) {
    $env:PYTHONPATH = $SrcPath
} else {
    $env:PYTHONPATH = "$SrcPath;$env:PYTHONPATH"
}

& $Python -m ai_agent_standards_mcp @McpArgs
exit $LASTEXITCODE
