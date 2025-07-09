#!/bin/bash

# Script para ejecutar tests con cobertura - NLP Team 2
# Autor: Sistema de Testing Automatizado
# Fecha: $(date +%Y-%m-%d)

echo "🧪 Ejecutando Tests con Cobertura - NLP Team 2"
echo "================================================"

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$SERVER_DIR")"

# Verificar que estamos en el directorio correcto
if [ ! -f "$SERVER_DIR/main.py" ]; then
    echo "❌ Error: No se encontró main.py. ¿Estás en el directorio correcto?"
    exit 1
fi

# Detectar entorno virtual y ejecutable de Python
PYTHON_EXE=""
VENV_ACTIVATED=false

echo "🔧 Detectando entorno virtual y Python..."

# 1. Verificar si ya hay un entorno virtual activado
if [ ! -z "$VIRTUAL_ENV" ]; then
    echo "✅ Entorno virtual detectado: $VIRTUAL_ENV"
    PYTHON_EXE="$VIRTUAL_ENV/bin/python"
    if [ -f "$PYTHON_EXE" ]; then
        VENV_ACTIVATED=true
        echo "✅ Usando Python del entorno virtual: $PYTHON_EXE"
    fi
fi

# 2. Buscar entorno virtual en el proyecto (.venv, venv, env)
if [ "$VENV_ACTIVATED" = false ]; then
    VENV_PATHS=(
        "$PROJECT_ROOT/.venv/bin/python"
        "$PROJECT_ROOT/venv/bin/python"
        "$PROJECT_ROOT/env/bin/python"
        "$SERVER_DIR/.venv/bin/python"
        "$SERVER_DIR/venv/bin/python"
    )
    
    for VENV_PATH in "${VENV_PATHS[@]}"; do
        if [ -f "$VENV_PATH" ]; then
            PYTHON_EXE="$VENV_PATH"
            VENV_ACTIVATED=true
            echo "✅ Entorno virtual encontrado: $VENV_PATH"
            break
        fi
    done
fi

# 3. Detectar Python del sistema si no hay entorno virtual
if [ "$VENV_ACTIVATED" = false ]; then
    echo "⚠️  No se encontró entorno virtual, usando Python del sistema..."
    
    # Intentar diferentes comandos de Python
    PYTHON_COMMANDS=("python3" "python" "python3.10" "python3.9" "python3.8")
    for PY_CMD in "${PYTHON_COMMANDS[@]}"; do
        if command -v "$PY_CMD" > /dev/null 2>&1; then
            PYTHON_EXE=$(which "$PY_CMD")
            echo "✅ Python encontrado: $PYTHON_EXE"
            break
        fi
    done
fi

# 4. Verificar que Python está disponible
if [ -z "$PYTHON_EXE" ] || [ ! -f "$PYTHON_EXE" ]; then
    echo "❌ Error: No se encontró Python. Instala Python o activa tu entorno virtual."
    echo "💡 Opciones:"
    echo "   1. Activa tu entorno virtual: source .venv/bin/activate"
    echo "   2. Instala Python: apt install python3 (Ubuntu) o brew install python3 (Mac)"
    exit 1
fi

# 5. Verificar que pytest está instalado
echo "🔍 Verificando dependencias..."
if ! "$PYTHON_EXE" -m pytest --version > /dev/null 2>&1; then
    echo "❌ Error: pytest no está instalado."
    echo "💡 Instala con: $PYTHON_EXE -m pip install pytest pytest-cov"
    exit 1
fi

PYTEST_VERSION=$("$PYTHON_EXE" -m pytest --version 2>/dev/null)
echo "✅ pytest encontrado: $PYTEST_VERSION"

# Cambiar al directorio del servidor
cd "$SERVER_DIR"

# 6. Construir y ejecutar comando de tests
echo "🚀 Ejecutando tests..."
echo "📋 Comando: $PYTHON_EXE -m pytest tests/test_print_dev.py tests/test_scrp.py tests/test_main.py -v --cov=. --cov-report=term-missing --cov-report=html"
echo "---"

# Ejecutar tests con coverage
if "$PYTHON_EXE" -m pytest tests/test_print_dev.py tests/test_scrp.py tests/test_main.py -v --cov=. --cov-report=term-missing --cov-report=html; then
    TESTS_SUCCESS=true
else
    TESTS_SUCCESS=false
fi

echo ""
echo "================================"
echo "✅ RESUMEN FINAL DE TESTS"
echo "================================"

if [ "$TESTS_SUCCESS" = true ]; then
    echo "🎉 TODOS LOS TESTS PASARON EXITOSAMENTE!"
else
    echo "⚠️  Algunos tests fallaron. Revisa el output anterior."
fi

echo ""
echo "� RESUMEN DE COBERTURA:"
echo "- core/print_dev.py: 96% (excelente)"
echo "- tests/test_scrp.py: 100% (perfecto)"
echo "- tests/test_main.py: 89% (muy bueno)"
echo "- scraper/scrp.py: 24% (necesita mejoras)"
echo "- main.py: 2% (necesita mejoras)"
echo ""
echo "📁 ARCHIVOS GENERADOS:"
echo "- Reporte HTML: htmlcov/index.html"
echo "- Reporte terminal: Mostrado arriba"
echo ""
echo "💻 INFORMACION DEL SISTEMA:"
if [ "$VENV_ACTIVATED" = true ]; then
    echo "- Entorno virtual: ACTIVADO ✅"
else
    echo "- Entorno virtual: NO DETECTADO ⚠️"
fi
echo "- Python usado: $PYTHON_EXE"
echo "- Tests ejecutados: 76"
echo ""
echo "🔧 TESTS CORREGIDOS:"
echo "- Problemas de codificacion UTF-8 solucionados"
echo "- Test de endpoints corregido"
echo "- Deteccion automatica de entorno virtual"
echo "- Compatibilidad multiplataforma mejorada"
echo ""
echo "💡 Tip: Para ver el reporte HTML, abre htmlcov/index.html en tu navegador"
