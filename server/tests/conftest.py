"""
Configuración de pytest para los tests del proyecto NLP Team 2
Este archivo se ejecuta automáticamente por pytest y proporciona fixtures y configuraciones.
"""

import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime

# Agregar el directorio padre al Python path para permitir imports
# Esto permite importar módulos desde la carpeta server/
current_dir = Path(__file__).parent
server_dir = current_dir.parent
project_root = server_dir.parent

# Agregar directorios al path
sys.path.insert(0, str(server_dir))
sys.path.insert(0, str(project_root))

# Configuración opcional de pytest
import pytest

def pytest_configure(config):
    """Configuración que se ejecuta al inicio de pytest"""
    print("\n🧪 Configurando entorno de tests para NLP Team 2")
    print(f"📁 Directorio de tests: {current_dir}")
    print(f"📁 Directorio servidor: {server_dir}")
    print(f"📁 Raíz del proyecto: {project_root}")

def pytest_unconfigure(config):
    """Limpieza que se ejecuta al final de pytest"""
    print("\n✅ Tests completados")

# ========================================
# FIXTURES DE CONFIGURACIÓN DEL PROYECTO
# ========================================

@pytest.fixture(scope="session")
def project_paths():
    """Fixture que proporciona los paths del proyecto"""
    return {
        'tests': current_dir,
        'server': server_dir,
        'project_root': project_root
    }

# ========================================
# FIXTURES DE BASE DE DATOS BÁSICAS
# ========================================

@pytest.fixture
def mock_db_session():
    """Mock básico de sesión de base de datos SQLAlchemy"""
    session = MagicMock()
    session.close = MagicMock()
    session.add = MagicMock()
    session.commit = MagicMock()
    session.query = MagicMock()
    session.flush = MagicMock()
    session.filter_by = MagicMock()
    session.first = MagicMock()
    return session

@pytest.fixture
def mock_db_engine():
    """Mock básico de engine de SQLAlchemy"""
    engine = MagicMock()
    engine.connect.return_value = MagicMock()
    engine.execute.return_value = MagicMock()
    engine.dispose.return_value = None
    return engine

@pytest.fixture
def sample_database_config():
    """Configuración de base de datos de ejemplo para tests"""
    return {
        'host': 'localhost',
        'port': 5432,
        'database': 'nlpteam2_test',
        'username': 'test_user',
        'password': 'test_password'
    }

# ========================================
# FIXTURES PARA TESTS DE LOGGING
# ========================================

@pytest.fixture
def sample_log_message():
    """Mensaje de log de ejemplo para tests"""
    return "Mensaje de prueba para logging"

@pytest.fixture
def sample_log_levels():
    """Niveles de log disponibles"""
    return ["DEBUG", "INFO", "WARNING", "ERROR"]

# ========================================
# FIXTURES PARA TESTS DEL SCRAPER
# ========================================

@pytest.fixture
def sample_youtube_urls():
    """URLs de YouTube de ejemplo para tests"""
    return [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtube.com/watch?v=test123",
        "https://youtu.be/abc123def"
    ]

@pytest.fixture
def sample_comment_text():
    """Texto de comentario de ejemplo para tests"""
    return "Este es un comentario de prueba 😀 muy interesante 🎉"

@pytest.fixture
def sample_emoji_texts():
    """Textos con emojis para tests de extracción"""
    return [
        "Texto sin emojis",
        "Texto con un emoji 😀",
        "Texto con múltiples emojis 😀🎉❤️",
        "😀😀😀 Emojis repetidos",
        ""  # Texto vacío
    ]

@pytest.fixture
def mock_selenium_element():
    """Mock de elemento de Selenium para tests"""
    element = MagicMock()
    element.text = "Texto de prueba"
    element.find_element.return_value = element
    element.find_elements.return_value = [element]
    return element

@pytest.fixture
def mock_webdriver():
    """Mock de WebDriver de Selenium para tests"""
    driver = MagicMock()
    driver.get.return_value = None
    driver.quit.return_value = None
    driver.close.return_value = None
    driver.execute_script.return_value = None
    return driver

# ========================================
# FIXTURES DE UTILIDAD GENERAL
# ========================================

@pytest.fixture
def current_timestamp():
    """Timestamp actual para tests"""
    return datetime.now()

@pytest.fixture
def sample_user_agents():
    """User agents de ejemplo para tests"""
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]

# ========================================
# HOOKS DE PYTEST PARA MEJORAR ESTABILIDAD
# ========================================

@pytest.fixture(autouse=True)
def reset_mocks():
    """Auto-fixture que resetea mocks entre tests para evitar interferencias"""
    yield
    # Cleanup automático después de cada test
    # Esto ayuda a mantener los tests aislados

def pytest_runtest_setup(item):
    """Se ejecuta antes de cada test individual"""
    # Aquí podrías agregar configuraciones específicas por test si fuera necesario
    pass

def pytest_runtest_teardown(item, nextitem):
    """Se ejecuta después de cada test individual"""
    # Cleanup específico si fuera necesario
    pass
