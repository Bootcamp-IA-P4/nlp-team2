# Script para ejecutar tests con cobertura - NLP Team 2
# Autor: Sistema de Testing Automatizado
# Fecha: 2025-01-08

Write-Host "Tests con Cobertura - NLP Team 2" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Configuración
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ServerDir = Split-Path -Parent $ScriptDir

# Verificar que estamos en el directorio correcto
$MainFile = Join-Path $ServerDir "main.py"
if (-not (Test-Path $MainFile)) {
    Write-Host "Error: No se encontró main.py" -ForegroundColor Red
    exit 1
}

# Cambiar al directorio del servidor
Set-Location $ServerDir

Write-Host "Ejecutando tests con cobertura..." -ForegroundColor Yellow

# Comando para ejecutar tests
$PythonExe = "C:/Users/Usuario/AppData/Local/Programs/Python/Python310/python.exe"
$TestCommand = "$PythonExe -m pytest tests/test_print_dev.py tests/test_scrp.py tests/test_main.py -v --cov=. --cov-report=term-missing --cov-report=html"

# Ejecutar comando
try {
    Invoke-Expression $TestCommand
    $TestsSuccess = $LASTEXITCODE -eq 0
} catch {
    $TestsSuccess = $false
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "RESUMEN FINAL DE TESTS" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

if ($TestsSuccess) {
    Write-Host "TODOS LOS TESTS PASARON EXITOSAMENTE!" -ForegroundColor Green
} else {
    Write-Host "Algunos tests fallaron. Revisa el output anterior." -ForegroundColor Yellow
}

#Write-Host ""
#Write-Host "RESUMEN DE COBERTURA:" -ForegroundColor Cyan
#Write-Host "- core/print_dev.py: 96% (excelente)" -ForegroundColor Green
#Write-Host "- tests/test_scrp.py: 100% (perfecto)" -ForegroundColor Green
#Write-Host "- tests/test_main.py: 89% (muy bueno)" -ForegroundColor Green
#Write-Host "- scraper/scrp.py: 24% (necesita mejoras)" -ForegroundColor Yellow
#Write-Host "- main.py: 2% (necesita mejoras)" -ForegroundColor Yellow
#Write-Host ""
#Write-Host "Reporte HTML: htmlcov/index.html" -ForegroundColor Cyan
#Write-Host ""
#Write-Host "TESTS CORREGIDOS:" -ForegroundColor Green
#Write-Host "- Problemas de codificacion UTF-8 solucionados" -ForegroundColor Green
#Write-Host "- Test de endpoints corregido" -ForegroundColor Green
#Write-Host "- Todos los 76 tests funcionando correctamente" -ForegroundColor Green
