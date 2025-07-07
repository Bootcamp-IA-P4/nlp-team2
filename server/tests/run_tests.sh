#!/bin/bash
# Script para ejecutar tests con activación automática del entorno virtual

echo "🧪 Iniciando Tests - NLP Team 2"
echo "================================"

# Cambiar al directorio del proyecto
cd "$(dirname "$0")/../.."

# Verificar que existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo "❌ Error: No se encuentra el entorno virtual .venv"
    echo "   Crear con: python -m venv .venv"
    exit 1
fi

# Activar entorno virtual y ejecutar tests
echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

echo "📁 Cambiando a directorio de tests..."
cd server/tests

echo "🧪 Ejecutando tests..."
python run_tests_basico.py

# Capturar código de salida
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "🎉 ¡Tests completados exitosamente!"
else
    echo ""
    echo "❌ Tests fallaron"
fi

exit $exit_code
