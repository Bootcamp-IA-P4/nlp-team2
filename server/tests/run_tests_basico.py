#!/usr/bin/env python3
"""
Script simple para ejecutar tests de los módulos print_dev, scrp y database con pytest
"""

import subprocess
import sys
import os

def ejecutar_tests():
    """Ejecutar los tests usando pytest"""
    print("🧪 Tests de Módulos Server - NLP Team 2")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    required_files = ["test_print_dev.py", "test_scrp.py", "test_database.py"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Error: No se encuentran los archivos: {', '.join(missing_files)}")
        print("   Ejecutar desde el directorio tests/")
        return False
    
    try:
        # Ejecutar pytest con todos los archivos de test
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "-v", 
            "--tb=short",
            "--color=yes"
        ], capture_output=True, text=True)
        
        # Mostrar salida
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Verificar resultado
        if result.returncode == 0:
            print("\n✅ ¡Todos los tests pasaron exitosamente!")
            return True
        else:
            print(f"\n❌ Tests fallaron con código {result.returncode}")
            return False
            
    except FileNotFoundError:
        print("❌ Error: pytest no está instalado")
        print("   Instalar con: pip install pytest")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def mostrar_ayuda():
    """Mostrar ayuda de uso"""
    print("📋 Script de Tests - Módulos Server")
    print("=" * 40)
    print("Uso:")
    print("  python run_tests_basico.py")
    print("")
    print("Requisitos:")
    print("  - Python 3.6+")
    print("  - pytest instalado (pip install pytest)")
    print("")
    print("Tests incluidos:")
    print("  - Tests del módulo core/print_dev.py (24 tests)")
    print("    * Tests de la clase Colors")
    print("    * Tests de la clase SimpleLogger")
    print("    * Tests de funciones globales")
    print("    * Tests de integración")
    print("")
    print("  - Tests del módulo scraper/scrp.py (23 tests)")
    print("    * Tests de la clase YouTubeCommentScraperChrome")
    print("    * Tests de extracción de emojis")
    print("    * Tests de configuración del driver")
    print("    * Tests de métodos de scraping")
    print("    * Tests de función global scrape_youtube_comments")
    print("")
    print("  - Tests del módulo database/db_manager.py (18 tests)")
    print("    * Tests de conexión a base de datos")
    print("    * Tests de creación de sesiones")
    print("    * Tests de manejo de tablas")
    print("    * Tests de conectividad y health checks")
    print("    * Tests de workflow completo de BD")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        mostrar_ayuda()
    else:
        success = ejecutar_tests()
        sys.exit(0 if success else 1)
