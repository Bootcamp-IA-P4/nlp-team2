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
VENV_PATH="$PROJECT_ROOT/.venv"

# Verificar que estamos en el directorio correcto
if [ ! -f "$SERVER_DIR/main.py" ]; then
    echo "❌ Error: No se encontró main.py. ¿Estás en el directorio correcto?"
    exit 1
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source "$VENV_PATH/bin/activate"

# Cambiar al directorio del servidor
cd "$SERVER_DIR"

echo "📊 Ejecutando tests con cobertura..."
echo "---"

# Ejecutar tests con coverage usando pytest --cov (funciona mejor)
echo "🎯 Ejecutando tests principales con cobertura..."
python -m pytest tests/test_print_dev.py tests/test_scrp.py tests/test_database.py tests/test_main.py -v --cov=. --cov-report=term-missing --cov-report=html

#echo ""
#echo "📈 REPORTE ADICIONAL: Ejecutando TODOS los tests para comparar..."
#python -m pytest tests/ -q --cov=. --cov-report=term-missing | grep -E "(main.py|TOTAL|Name)"

#echo ""
#echo "🌐 Reporte HTML generado correctamente"

#echo ""
#echo "✅ Tests y cobertura completados!"
#echo "📁 Reporte HTML disponible en: htmlcov/index.html"
#echo ""
#echo "📋 RESUMEN DE COBERTURA DE MÓDULOS PRINCIPALES:"
#echo "- core/print_dev.py: 96% (muy buena cobertura)"
#echo "- core/config.py: 100% (excelente cobertura)"
#echo "- database/db_manager.py: 32% (necesita más tests)"
#echo "- scraper/scrp.py: 24% (necesita más tests)"
#echo "- main.py: 11% (mejorado - tests estructurales creados)"
#echo ""
#echo "💡 Tip: Para ver el reporte HTML, abre htmlcov/index.html en tu navegador"
