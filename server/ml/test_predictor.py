#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para probar la carga del modelo desde el predictor.
Este script verifica si el predictor puede cargar el modelo correctamente.
"""

import os
import sys
import time
import traceback
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Subir dos niveles para llegar a la raíz del proyecto
project_root = os.path.dirname(os.path.dirname(current_dir))

# Asegurar que el directorio del proyecto esté en el path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importar el predictor
from server.ml.predictor import ToxicityPredictor

def test_predictor():
    """Prueba la carga del modelo desde el predictor"""
    
    print("\n" + "="*70)
    print(" PRUEBA DE CARGA DEL MODELO DESDE EL PREDICTOR ".center(70))
    print("="*70 + "\n")
    
    try:
        print("🔄 Inicializando ToxicityPredictor...")
        start_time = time.time()
        
        # Inicializar el predictor (esto cargará el modelo en memoria)
        predictor = ToxicityPredictor()
        
        elapsed = time.time() - start_time
        print(f"✅ Predictor inicializado en {elapsed:.2f} segundos")
        
        # Verificar que el modelo se haya cargado correctamente
        model_info = predictor.get_model_info()
        print("\nInformación del modelo:")
        for key, value in model_info.items():
            if key != 'metrics':  # No imprimir las métricas completas
                print(f"  - {key}: {value}")
        
        # Probar el modelo con un texto de ejemplo
        print("\n🔄 Probando predicción con texto de ejemplo...")
        
        ejemplo = "Este es un texto de ejemplo para probar el modelo."
        resultado = predictor.predict_single(ejemplo)
        
        print("\nResultado de la predicción:")
        print(f"  - Texto: {resultado['text']}")
        print(f"  - Es tóxico: {resultado['is_toxic']}")
        print(f"  - Confianza: {resultado['toxicity_confidence']:.4f}")
        if resultado['categories_detected']:
            print(f"  - Categorías: {', '.join(resultado['categories_detected'])}")
        
        print("\n✅ Prueba completada exitosamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {str(e)}")
        print("\nDetalles del error:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Ejecutar la prueba
    success = test_predictor()
    # Salir con código adecuado
    sys.exit(0 if success else 1)
