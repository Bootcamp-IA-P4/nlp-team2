# Tests del Módulo print_dev - NLP Team 2 Server

## 📋 Descripción

Este directorio contiene tests unitarios usando **pytest** para el módulo `core/print_dev.py` del proyecto NLP Team 2 Server.

## 📁 Estructura

```
tests/
├── test_print_dev.py        # Tests del módulo core/print_dev.py (24 tests)
├── test_scrp.py            # Tests del módulo scraper/scrp.py (23 tests)
├── test_database.py        # Tests del módulo database/db_manager.py (18 tests)
├── run_tests_basico.py      # Script para ejecutar tests
├── run_tests.sh            # Script bash con entorno virtual automático
├── conftest.py             # Configuración y fixtures de pytest
├── pytest.ini              # Configuración de pytest
└── README.md               # Esta documentación
```

## 🧪 Tests Incluidos

### 🔧 TestPrintDev (core/print_dev.py) - 24 tests
- `TestColors`: Tests de la clase Colors (colores de consola)
- `TestSimpleLogger`: Tests de la clase SimpleLogger
- `TestGlobalFunctions`: Tests de funciones globales (is_running_local, printer_mensaje)
- `TestLogFunctions`: Tests de funciones de logging (log_debug, log_info, etc.)
- `TestGlobalLogger`: Tests del logger global
- `TestIntegration`: Tests de integración del módulo

### 🕷️ TestScraper (scraper/scrp.py) - 23 tests
- `TestYouTubeCommentScraperChrome`: Tests de la clase principal del scraper
- `TestScrapingMethods`: Tests de métodos de scraping (extract_comment_data, scroll_to_load_comments, etc.)
- `TestGlobalFunctions`: Tests de la función global scrape_youtube_comments
- `TestIntegration`: Tests de workflow completo del scraper

### 🗄️ TestDatabase (database/db_manager.py) - 18 tests
- `TestDatabaseConnection`: Tests de conexión a la base de datos
- `TestDatabaseSession`: Tests de creación y manejo de sesiones
- `TestDatabaseTables`: Tests de creación y manejo de tablas
- `TestDatabaseConnectivity`: Tests de conectividad general
- `TestDatabaseHealthCheck`: Tests de verificación de salud de la BD
- `TestIntegration`: Tests de workflow completo de base de datos

**Total: 65 tests unitarios y de integración** 🎯

## 🚀 Cómo Ejecutar

### Opción 1: Script Bash (automático con entorno virtual)
```bash
cd server/tests
./run_tests.sh
```
*Este script activa automáticamente el entorno virtual `.venv` y ejecuta todos los tests.*

### Opción 2: Script Python (requiere entorno virtual activado)
```bash
# Activar entorno virtual primero
source .venv/bin/activate
cd server/tests
python run_tests_basico.py
```

### Opción 3: pytest directo (requiere entorno virtual activado)
```bash
# Activar entorno virtual primero
source .venv/bin/activate
cd server/tests
python -m pytest test_print_dev.py -v
```

### Opción 4: pytest con más opciones
```bash
# Activar entorno virtual primero
source .venv/bin/activate
cd server/tests
python -m pytest test_print_dev.py -v --tb=short --color=yes
```

## 📊 Resultado Esperado

```
================= test session starts =================
test_print_dev.py::TestColors::test_colors_defined PASSED
test_print_dev.py::TestColors::test_colors_are_strings PASSED
test_print_dev.py::TestColors::test_colors_contain_escape_sequences PASSED
test_print_dev.py::TestSimpleLogger::test_logger_initialization PASSED
... (20 tests adicionales del módulo print_dev)

================= 24 passed in 0.82s =================
```

## 🛠️ Requisitos

- Python 3.6+
- pytest instalado (`pip install pytest`)

## 📈 Características

- **Tests unitarios**: Cada test es independiente
- **Sin dependencias externas**: Solo usan Python estándar
- **Cobertura básica**: Tests de funcionalidades fundamentales
- **Fácil ejecución**: Scripts simples para correr tests
- **Documentación clara**: Cada test tiene docstring explicativo

## 🎯 Propósito

Estos tests básicos sirven para:
1. Verificar que pytest está correctamente instalado
2. Demostrar la estructura básica de tests unitarios
3. Validar que el entorno Python funciona correctamente
4. Proporcionar una base para tests más complejos en el futuro

## ✅ Estado Actual del Sistema de Tests

### 📁 Archivos de Test
- `test_print_dev.py`: **24 tests unitarios** para el módulo `core/print_dev.py`
- `test_scrp.py`: **23 tests unitarios** para el módulo `scraper/scrp.py`
- `test_database.py`: **18 tests unitarios** para el módulo `database/db_manager.py`

### 🛠️ Archivos de Configuración
- `pytest.ini`: Configuración de pytest
- `conftest.py`: Configuración de pytest y helpers para imports

### 🚀 Scripts de Ejecución
- `run_tests.sh`: Script bash que activa automáticamente el entorno virtual
- `run_tests_basico.py`: Script Python para ejecutar tests (requiere venv activo)

### 📊 Cobertura de Tests
**Módulo core/print_dev.py:**
- ✅ Clase `Colors` (3 tests)
- ✅ Clase `SimpleLogger` (5 tests)  
- ✅ Funciones globales `is_running_local`, `printer_mensaje` (5 tests)
- ✅ Funciones de logging `log_debug`, `log_info`, etc. (4 tests)
- ✅ Logger global (2 tests)
- ✅ Tests de integración (3 tests)
- ✅ Test de importación del módulo (1 test)

**Módulo scraper/scrp.py:**
- ✅ Clase `YouTubeCommentScraperChrome` (12 tests)
- ✅ Métodos de scraping `scroll_to_load_comments`, `extract_comment_data`, etc. (4 tests)
- ✅ Función global `scrape_youtube_comments` (3 tests)
- ✅ Tests de integración (3 tests)
- ✅ Test de importación del módulo (1 test)

**Módulo database/db_manager.py:**
- ✅ Funciones de conexión `create_connection` (4 tests)
- ✅ Funciones de sesión `open_session` (3 tests)
- ✅ Funciones de tablas `create_tables` (3 tests)
- ✅ Tests de conectividad general (3 tests)
- ✅ Tests de health checks (2 tests)
- ✅ Tests de integración (2 tests)
- ✅ Test de importación del módulo (1 test)

**Total: 65 tests unitarios y de integración** ✨

---

*Tests creados para el proyecto NLP Team 2 - Server*
