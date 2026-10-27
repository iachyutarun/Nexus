$ErrorActionPreference = 'SilentlyContinue'
$nexusRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) {
    Write-Host "Python not found in PATH. Please install Python 3.x."
    pause
    exit 1
}
$env:PYTHONPATH = $nexusRoot
& $python.Source (Join-Path $nexusRoot "nexus\app\bootstrap.py")
