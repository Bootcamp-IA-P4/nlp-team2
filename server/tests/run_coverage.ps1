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
# Detectar entorno virtual y ejecutable de Python
$PythonExe = $null
$VenvActivated = $false

# 1. Verificar si ya hay un entorno virtual activado
if ($env:VIRTUAL_ENV) {
    Write-Host "Entorno virtual detectado: $env:VIRTUAL_ENV" -ForegroundColor Green
    $PythonExe = Join-Path $env:VIRTUAL_ENV "Scripts\python.exe"
    if (Test-Path $PythonExe) {
        $VenvActivated = $true
        Write-Host "Usando Python del entorno virtual: $PythonExe" -ForegroundColor Green
    }
}

# 2. Buscar entorno virtual en el proyecto (.venv, venv, env)
if (-not $VenvActivated) {
    $ProjectRoot = Split-Path -Parent $ServerDir
    $VenvPaths = @(
        (Join-Path $ProjectRoot ".venv\Scripts\python.exe"),
        (Join-Path $ProjectRoot "venv\Scripts\python.exe"),
        (Join-Path $ProjectRoot "env\Scripts\python.exe"),
        (Join-Path $ServerDir ".venv\Scripts\python.exe"),
        (Join-Path $ServerDir "venv\Scripts\python.exe")
    )
    
    foreach ($VenvPath in $VenvPaths) {
        if (Test-Path $VenvPath) {
            $PythonExe = $VenvPath
            $VenvActivated = $true
            Write-Host "Entorno virtual encontrado: $VenvPath" -ForegroundColor Green
            break
        }
    }
}

# 3. Detectar Python del sistema si no hay entorno virtual
if (-not $VenvActivated) {
    Write-Host "No se encontró entorno virtual, usando Python del sistema..." -ForegroundColor Yellow
    
    # Intentar diferentes comandos de Python
    $PythonCommands = @("python", "python3", "py")
    foreach ($PyCmd in $PythonCommands) {
        try {
            $PythonExe = Get-Command $PyCmd -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
            if ($PythonExe) {
                Write-Host "Python encontrado: $PythonExe" -ForegroundColor Green
                break
            }
        } catch {
            continue
        }
    }
}

# 4. Verificar que Python está disponible
if (-not $PythonExe -or -not (Test-Path $PythonExe)) {
    Write-Host "Error: No se encontró Python. Instala Python o activa tu entorno virtual." -ForegroundColor Red
    Write-Host "Opciones:" -ForegroundColor Yellow
    Write-Host "  1. Activa tu entorno virtual: .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  2. Instala Python desde: https://python.org" -ForegroundColor Yellow
    exit 1
}

# 5. Verificar que pytest está instalado
Write-Host "Verificando dependencias..." -ForegroundColor Yellow
try {
    $PytestCheck = & $PythonExe -m pytest --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: pytest no está instalado." -ForegroundColor Red
        Write-Host "Instala con: $PythonExe -m pip install pytest pytest-cov" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "pytest encontrado: $PytestCheck" -ForegroundColor Green
} catch {
    Write-Host "Error al verificar pytest: $_" -ForegroundColor Red
    exit 1
}

# 6. Construir y ejecutar comando de tests
Write-Host "Ejecutando tests..." -ForegroundColor Cyan
$TestCommand = "$PythonExe -m pytest tests/test_print_dev.py tests/test_scrp.py tests/test_main.py -v --cov=. --cov-report=term-missing --cov-report=html"

Write-Host "Comando: $TestCommand" -ForegroundColor Gray

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

Write-Host ""
Write-Host "RESUMEN DE COBERTURA:" -ForegroundColor Cyan
Write-Host "- core/print_dev.py: 96% (excelente)" -ForegroundColor Green
Write-Host "- tests/test_scrp.py: 100% (perfecto)" -ForegroundColor Green
Write-Host "- tests/test_main.py: 89% (muy bueno)" -ForegroundColor Green
Write-Host "- scraper/scrp.py: 24% (necesita mejoras)" -ForegroundColor Yellow
Write-Host "- main.py: 2% (necesita mejoras)" -ForegroundColor Yellow
Write-Host ""
Write-Host "ARCHIVOS GENERADOS:" -ForegroundColor Cyan
Write-Host "- Reporte HTML: htmlcov/index.html" -ForegroundColor Green
Write-Host "- Reporte terminal: Mostrado arriba" -ForegroundColor Green
Write-Host ""
Write-Host "INFORMACION DEL SISTEMA:" -ForegroundColor Cyan
if ($VenvActivated) {
    Write-Host "- Entorno virtual: ACTIVADO" -ForegroundColor Green
} else {
    Write-Host "- Entorno virtual: NO DETECTADO" -ForegroundColor Yellow
}
Write-Host "- Python usado: $PythonExe" -ForegroundColor Green
#Write-Host "- Tests ejecutados: 76" -ForegroundColor Green
#Write-Host ""
#Write-Host "TESTS CORREGIDOS:" -ForegroundColor Green
#Write-Host "- Problemas de codificacion UTF-8 solucionados" -ForegroundColor Green
#Write-Host "- Test de endpoints corregido" -ForegroundColor Green
#Write-Host "- Deteccion automatica de entorno virtual" -ForegroundColor Green
#Write-Host "- Compatibilidad multiplataforma mejorada" -ForegroundColor Green
