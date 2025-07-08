# Sistema de Tests - NLP Team 2

Este README describe exclusivamente el sistema de testing del proyecto: cómo funciona, cómo ejecutarlo y cómo interpretar los resultados.
Este conjunto de tests esta desarrollado con Copilot integramente utilizando 'Ingeniería de Pronts'.

## 📋 Tabla de Contenidos

- [Estructura de Tests](#estructura-de-tests)
- [Configuración](#configuración)
- [Ejecución de Tests](#ejecución-de-tests)
- [Cobertura de Código](#cobertura-de-código)
- [Tipos de Tests](#tipos-de-tests)
- [Interpretación de Resultados](#interpretación-de-resultados)
- [Solución de Problemas](#solución-de-problemas)

## 🧪 Estructura de Tests

```
server/tests/
├── README.md             # Este archivo
├── conftest.py           # Configuración y fixtures de pytest
├── pytest.ini            # Configuración de pytest
├── .coveragerc           # Configuración de cobertura
├── run_coverage.sh       # Script para ejecutar tests con cobertura
├── test_print_dev.py     # Tests del módulo de logging (24 tests)
├── test_scrp.py          # Tests del scraper (23 tests)
├── test_database.py      # Tests del gestor de base de datos (18 tests)
└── test_main.py          # Tests unificados del módulo principal (29 tests)
```

**Total de Tests**: 94 tests unitarios y de integración

## ⚙️ Configuración

### Dependencias
El sistema de tests utiliza:
- `pytest` - Framework principal de testing
- `pytest-cov` - Plugin para medición de cobertura
- `coverage` - Herramienta de análisis de cobertura
- `unittest.mock` - Para mocking y simulación

### Archivos de Configuración

#### `pytest.ini`
Configuración principal de pytest con opciones de ejecución y reportes.

#### `.coveragerc`
Configuración de cobertura que especifica:
- Archivos a incluir/excluir
- Directorios a analizar
- Formato de reportes

#### `conftest.py`
Contiene fixtures reutilizables y configuración global:
- Fixtures de base de datos mock
- Fixtures para logging
- Fixtures para scraper
- Configuración de paths del proyecto

## 🚀 Ejecución de Tests

### Método 1: Script de Cobertura (Recomendado)
```bash
# Desde la carpeta tests/
./run_coverage.sh
```

Este script ejecuta todos los tests y genera reportes de cobertura completos.

### Método 2: Comandos Directos

#### Ejecutar todos los tests
```bash
cd server/tests
python -m pytest -v
```

#### Ejecutar tests con cobertura
```bash
cd server/tests
python -m pytest --cov=../ --cov-report=html --cov-report=term -v
```

#### Ejecutar tests específicos
```bash
# Test de un módulo específico
python -m pytest test_print_dev.py -v

# Test de una función específica
python -m pytest test_main.py::test_create_app -v

# Tests por patrón
python -m pytest -k "database" -v
```

#### Ejecutar con diferentes niveles de verbosidad
```bash
# Básico
python -m pytest

# Verboso
python -m pytest -v

# Extra verboso
python -m pytest -vv

# Con salida en tiempo real
python -m pytest -s
```

## 📊 Cobertura de Código

### Generar Reporte de Cobertura
```bash
# Reporte en terminal y HTML
python -m pytest --cov=../ --cov-report=html --cov-report=term

# Solo reporte HTML
python -m pytest --cov=../ --cov-report=html

# Solo reporte en terminal
python -m pytest --cov=../ --cov-report=term
```

### Ver Reportes
- **Terminal**: Se muestra automáticamente tras la ejecución
- **HTML**: Abre `htmlcov/index.html` en tu navegador
- **Archivos específicos**: `htmlcov/[nombre_archivo].html`

### Estado Actual de Cobertura
- **core/config.py**: 100% (7 líneas)
- **core/print_dev.py**: 96% (57 líneas, 2 sin cubrir)
- **database/models.py**: 100% (41 líneas)
- **scraper/scrp.py**: 24% (359 líneas, 273 sin cubrir)
- **database/db_manager.py**: 32% (122 líneas, 83 sin cubrir)
- **main.py**: 11% (19 líneas, 17 sin cubrir)
- **test_print_dev.py**: 99% (147 líneas, 2 sin cubrir)
- **test_main.py**: 89% (474 líneas, 53 sin cubrir)
- **test_scrp.py**: 100% (195 líneas)
- **test_database.py**: 100% (200 líneas)
- **Total del proyecto**: 59% (2092 líneas, 851 sin cubrir)

## 🔬 Tipos de Tests

### Tests Unitarios
- **test_print_dev.py**: Funciones de logging y impresión (24 tests)
- **test_scrp.py**: Funciones del scraper de YouTube (23 tests)
- **test_database.py**: Operaciones de base de datos (18 tests)

### Tests de Integración
- **test_main.py**: Tests unificados del módulo principal (29 tests)
  - Tests de estructura y configuración
  - Tests de importación y dependencias
  - Tests de cobertura forzada
  - Tests de ejecución real con mocks
  - Tests avanzados para maximizar cobertura

### Tipos de Mocking
- **Mock de Base de Datos**: Simula conexiones SQLAlchemy
- **Mock de Selenium**: Simula navegador web para scraping
- **Mock de APIs**: Simula respuestas de servicios externos
- **Mock de Sistema**: Simula operaciones del sistema operativo

## 📈 Interpretación de Resultados

### Salida de Tests Exitosos
```
==================== test session starts ====================
collected 94 items

test_print_dev.py ........................               [ 25%]
test_scrp.py .............................               [ 50%]
test_database.py .........................               [ 69%]
test_main.py .............................               [100%]

==================== 94 passed in 12.73s ====================
```

### Salida de Cobertura
```
Name                      Stmts   Miss  Cover
-------------------------------------------------------
core/config.py                7      0   100%
core/print_dev.py            57      2    96%
database/models.py           41      0   100%
scraper/scrp.py             359    273    24%
database/db_manager.py      122     83    32%
main.py                      19     17    11%
test_print_dev.py           147      2    99%
test_main.py                474     53    89%
test_scrp.py                195      0   100%
test_database.py            200      0   100%
-------------------------------------------------------
TOTAL                      2092    851    59%
```

### Símbolos de Estado
- ✅ `.` = Test pasó
- ❌ `F` = Test falló
- ⚠️ `E` = Error en el test
- ⏭️ `s` = Test saltado
- ❓ `x` = Fallo esperado

### Resumen de Estado Actual
- **Total de Tests**: 94 tests unitarios y de integración
- **Tests Exitosos**: 94/94 (100% de éxito)
- **Tests Fallidos**: 0
- **Warnings**: 2 (deprecation de asyncio en Python 3.14)

## 🛠️ Solución de Problemas

### Errores Comunes

#### "ModuleNotFoundError"
```bash
# Ejecutar desde la carpeta correcta
cd server/tests
python -m pytest
```

#### "No tests ran matching the given pattern"
```bash
# Verificar nombres de archivos
ls test_*.py

# Verificar sintaxis de tests
python -m pytest --collect-only
```

#### "ImportError" en módulos del proyecto
El archivo `conftest.py` maneja automáticamente los imports. Si persiste:
```bash
# Verificar que estás en la carpeta correcta
pwd
# Debe mostrar: .../nlp-team2/server/tests
```

### Incompatibilidades Conocidas
- **Python 3.14 + FastAPI**: Error de pydantic que impide importación directa
- **Solución**: Los tests usan mocks y verificaciones estructurales

### Debug de Tests
```bash
# Ejecutar con debug
python -m pytest --pdb

# Ver output completo
python -m pytest -s -v

# Ejecutar test específico con debug
python -m pytest test_main.py::test_specific_function -s -v
```

### Limpiar Cache
```bash
# Limpiar cache de pytest
rm -rf .pytest_cache/

# Limpiar cache de Python
find . -name "__pycache__" -exec rm -rf {} +

# Limpiar reportes anteriores
rm -rf htmlcov/
```

## 📝 Configuración de Fixtures

### Fixtures Disponibles en conftest.py
- **Base de Datos**: `mock_db_session`, `mock_db_engine`, `sample_database_config`
- **Logging**: `sample_log_message`, `sample_log_levels`
- **Scraper**: `sample_youtube_urls`, `mock_selenium_element`, `mock_webdriver`
- **Utilidades**: `current_timestamp`, `sample_user_agents`, `project_paths`

### Estructura de Test Recomendada
```python
def test_function_name():
    # Arrange - Configurar datos de prueba
    setup_data = "test"
    
    # Act - Ejecutar la función a probar
    result = function_to_test(setup_data)
    
    # Assert - Verificar resultado
    assert result == expected_value
```

### Convenciones de Nomenclatura
- Archivos: `test_[módulo].py`
- Funciones: `test_[función_específica]()`
- Clases: `TestClassName`

## ⚡ Comandos Rápidos

```bash
# Ejecutar todos los tests con cobertura
./run_coverage.sh

# Tests rápidos sin cobertura
python -m pytest

# Ver solo tests fallidos
python -m pytest --lf

# Ejecutar tests específicos por palabra clave
python -m pytest -k "database"

# Modo verboso con detalles
python -m pytest -v

# Con salida en tiempo real
python -m pytest -s
```

## 🎯 Métricas de Calidad

### Objetivos de Cobertura
- **Módulos core**: >90% (✅ core/print_dev.py: 96%, core/config.py: 100%)
- **Módulos principales**: >70% (⚠️ pendiente)
- **Total del proyecto**: >80% (🔄 actual: 59%)

### Estado de Estabilidad
- **Tasa de éxito**: 100% (94/94 tests)
- **Tests confiables**: ✅ Implementados
- **Mocks centralizados**: ✅ Configurados
- **CI/CD ready**: ✅ Scripts preparados
- **Archivos optimizados**: ✅ Unificación completada
- **Cobertura total**: 59% (2092 líneas)

---

**Para más información sobre pytest**: [Documentación oficial](https://docs.pytest.org/)  
**Para más información sobre coverage**: [Documentación oficial](https://coverage.readthedocs.io/)
