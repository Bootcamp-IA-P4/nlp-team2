"""
Configuración de pytest para los tests del proyecto NLP Team 2
Este archivo se ejecuta automáticamente por pytest y proporciona fixtures y configuraciones.
"""

import sys
import os
from pathlib import Path

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

@pytest.fixture(scope="session")
def project_paths():
    """Fixture que proporciona los paths del proyecto"""
    return {
        'tests': current_dir,
        'server': server_dir,
        'project_root': project_root
    }

# Fixtures para tests comunes
@pytest.fixture
def sample_log_message():
    """Mensaje de log de ejemplo para tests"""
    return "Mensaje de prueba para logging"

@pytest.fixture
def sample_log_levels():
    """Niveles de log disponibles"""
    return ["DEBUG", "INFO", "WARNING", "ERROR"]

# Fixtures específicas para tests del scraper
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
    from unittest.mock import MagicMock
    element = MagicMock()
    element.text = "Texto de prueba"
    element.find_element.return_value = element
    return element

# Fixtures específicas para tests de base de datos
@pytest.fixture
def sample_database_urls():
    """URLs de base de datos de ejemplo para tests"""
    return [
        "postgresql://user:password@localhost:5432/nlpteam2",
        "postgresql://test:test@testdb:5432/test_db",
        "sqlite:///test.db"
    ]

@pytest.fixture
def mock_database_engine():
    """Mock de engine de SQLAlchemy para tests"""
    from unittest.mock import MagicMock
    engine = MagicMock()
    engine.connect.return_value = MagicMock()
    engine.execute.return_value = MagicMock()
    return engine

@pytest.fixture
def mock_database_session():
    """Mock de sesión de base de datos para tests"""
    from unittest.mock import MagicMock
    session = MagicMock()
    session.query.return_value = session
    session.filter_by.return_value = session
    session.first.return_value = None
    session.add.return_value = None
    session.commit.return_value = None
    session.close.return_value = None
    return session

@pytest.fixture
def sample_database_config():
    """Configuración de base de datos de ejemplo para tests"""
    return {
        'host': 'localhost',
        'port': 5432,
        'database': 'nlpteam2',
        'username': 'test_user',
        'password': 'test_password'
    }
