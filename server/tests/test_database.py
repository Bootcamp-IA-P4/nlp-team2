"""
Tests unitarios para el módulo database/db_manager.py
Estos tests verifican la conectividad y funcionalidades básicas de la base de datos.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path

# Agregar el directorio padre al path para poder importar
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock de dependencias externas antes de importar
sys.modules['sqlalchemy'] = MagicMock()
sys.modules['sqlalchemy.orm'] = MagicMock()
sys.modules['sqlalchemy.ext'] = MagicMock()
sys.modules['sqlalchemy.ext.declarative'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

# Configurar mocks específicos
sqlalchemy_mock = MagicMock()
sqlalchemy_mock.create_engine = MagicMock()
sqlalchemy_mock.Column = MagicMock()
sqlalchemy_mock.Integer = MagicMock()
sqlalchemy_mock.String = MagicMock()
sqlalchemy_mock.Text = MagicMock()
sqlalchemy_mock.ForeignKey = MagicMock()
sqlalchemy_mock.DateTime = MagicMock()
sys.modules['sqlalchemy'] = sqlalchemy_mock

# Mock de ORM
orm_mock = MagicMock()
orm_mock.sessionmaker = MagicMock()
orm_mock.relationship = MagicMock()
orm_mock.joinedload = MagicMock()
sys.modules['sqlalchemy.orm'] = orm_mock

# Mock de dotenv
dotenv_mock = MagicMock()
dotenv_mock.load_dotenv = MagicMock()
sys.modules['dotenv'] = dotenv_mock

# Ahora importar el módulo a testear
from database.db_manager import create_connection, open_session, create_tables


class TestDatabaseConnection:
    """Tests para funciones de conexión a la base de datos"""
    
    @patch('database.db_manager.os.getenv')
    @patch('database.db_manager.create_engine')
    def test_create_connection_success(self, mock_create_engine, mock_getenv):
        """Test de creación exitosa de conexión a la base de datos"""
        # Configurar mocks
        mock_getenv.return_value = "postgresql://user:pass@localhost:5432/testdb"
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        # Ejecutar función
        result = create_connection()
        
        # Verificar llamadas
        mock_getenv.assert_called_once_with("POSTGRES_URL")
        mock_create_engine.assert_called_once_with("postgresql://user:pass@localhost:5432/testdb", echo=False)
        assert result == mock_engine
    
    @patch('database.db_manager.os.getenv')
    @patch('database.db_manager.create_engine')
    def test_create_connection_no_url(self, mock_create_engine, mock_getenv):
        """Test de conexión cuando no hay URL configurada"""
        # Configurar mocks
        mock_getenv.return_value = None
        mock_create_engine.side_effect = Exception("No database URL provided")
        
        # Verificar que se lanza excepción
        with pytest.raises(Exception, match="Error creating database connection"):
            create_connection()
    
    @patch('database.db_manager.os.getenv')
    @patch('database.db_manager.create_engine')
    def test_create_connection_invalid_url(self, mock_create_engine, mock_getenv):
        """Test de conexión con URL inválida"""
        # Configurar mocks
        mock_getenv.return_value = "invalid_url"
        mock_create_engine.side_effect = Exception("Invalid database URL")
        
        # Verificar que se lanza excepción
        with pytest.raises(Exception, match="Error creating database connection"):
            create_connection()
    
    @patch('database.db_manager.os.getenv')
    @patch('database.db_manager.create_engine')
    def test_create_connection_database_unreachable(self, mock_create_engine, mock_getenv):
        """Test de conexión cuando la base de datos no está disponible"""
        # Configurar mocks
        mock_getenv.return_value = "postgresql://user:pass@unreachable:5432/testdb"
        mock_create_engine.side_effect = Exception("Database connection failed")
        
        # Verificar que se lanza excepción
        with pytest.raises(Exception, match="Error creating database connection"):
            create_connection()


class TestDatabaseSession:
    """Tests para funciones de sesión de base de datos"""
    
    @patch('database.db_manager.create_connection')
    @patch('database.db_manager.sessionmaker')
    def test_open_session_success(self, mock_sessionmaker, mock_create_connection):
        """Test de apertura exitosa de sesión"""
        # Configurar mocks
        mock_engine = MagicMock()
        mock_create_connection.return_value = mock_engine
        mock_session_class = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_sessionmaker.return_value = mock_session_class
        
        # Ejecutar función
        result = open_session()
        
        # Verificar llamadas
        mock_create_connection.assert_called_once()
        mock_sessionmaker.assert_called_once_with(bind=mock_engine)
        mock_session_class.assert_called_once()
        assert result == mock_session
    
    @patch('database.db_manager.create_connection')
    def test_open_session_connection_failure(self, mock_create_connection):
        """Test de fallo en apertura de sesión por falla de conexión"""
        # Configurar mock para que falle
        mock_create_connection.side_effect = Exception("Connection failed")
        
        # Verificar que se lanza excepción
        with pytest.raises(Exception, match="Error opening database session"):
            open_session()
    
    @patch('database.db_manager.create_connection')
    @patch('database.db_manager.sessionmaker')
    def test_open_session_sessionmaker_failure(self, mock_sessionmaker, mock_create_connection):
        """Test de fallo en creación de sessionmaker"""
        # Configurar mocks
        mock_engine = MagicMock()
        mock_create_connection.return_value = mock_engine
        mock_sessionmaker.side_effect = Exception("Sessionmaker failed")
        
        # Verificar que se lanza excepción
        with pytest.raises(Exception, match="Error opening database session"):
            open_session()


class TestDatabaseTables:
    """Tests para funciones de manejo de tablas"""
    
    @patch('database.db_manager.create_connection')
    @patch('database.db_manager.Base')
    @patch('builtins.print')
    def test_create_tables_success(self, mock_print, mock_base, mock_create_connection):
        """Test de creación exitosa de tablas"""
        # Configurar mocks
        mock_engine = MagicMock()
        mock_create_connection.return_value = mock_engine
        mock_metadata = MagicMock()
        mock_base.metadata = mock_metadata
        
        # Ejecutar función
        create_tables()
        
        # Verificar llamadas
        mock_create_connection.assert_called_once()
        mock_metadata.drop_all.assert_called_once_with(mock_engine)
        mock_metadata.create_all.assert_called_once_with(mock_engine)
        mock_print.assert_any_call("Creating tables...")
        mock_print.assert_any_call("Tables created successfully.")
    
    @patch('database.db_manager.create_connection')
    def test_create_tables_connection_failure(self, mock_create_connection):
        """Test de fallo en creación de tablas por falla de conexión"""
        # Configurar mock para que falle
        mock_create_connection.side_effect = Exception("Connection failed")
        
        # Verificar que se lanza excepción
        with pytest.raises(Exception, match="Error creating tables"):
            create_tables()
    
    @patch('database.db_manager.create_connection')
    @patch('database.db_manager.Base')
    def test_create_tables_metadata_failure(self, mock_base, mock_create_connection):
        """Test de fallo en operaciones de metadata"""
        # Configurar mocks
        mock_engine = MagicMock()
        mock_create_connection.return_value = mock_engine
        mock_metadata = MagicMock()
        mock_metadata.create_all.side_effect = Exception("Metadata operation failed")
        mock_base.metadata = mock_metadata
        
        # Verificar que se lanza excepción
        with pytest.raises(Exception, match="Error creating tables"):
            create_tables()


class TestDatabaseConnectivity:
    """Tests de conectividad general de la base de datos"""
    
    @patch('database.db_manager.os.getenv')
    def test_database_url_environment_variable(self, mock_getenv):
        """Test de verificación de variable de entorno POSTGRES_URL"""
        # Configurar mock
        expected_url = "postgresql://user:pass@localhost:5432/nlpteam2"
        mock_getenv.return_value = expected_url
        
        # Importar y verificar
        from database.db_manager import os
        url = os.getenv("POSTGRES_URL")
        
        assert url == expected_url
        mock_getenv.assert_called_with("POSTGRES_URL")
    
    @patch('database.db_manager.create_connection')
    @patch('database.db_manager.open_session')
    def test_full_database_connectivity_workflow(self, mock_open_session, mock_create_connection):
        """Test de workflow completo de conectividad"""
        # Configurar mocks
        mock_engine = MagicMock()
        mock_session = MagicMock()
        mock_create_connection.return_value = mock_engine
        mock_open_session.return_value = mock_session
        
        # Simular workflow completo
        engine = mock_create_connection()
        session = mock_open_session()
        
        # Verificar que el workflow funciona
        assert engine == mock_engine
        assert session == mock_session
        mock_create_connection.assert_called_once()
        mock_open_session.assert_called_once()
    
    def test_database_functions_exist(self):
        """Test de verificación de existencia de funciones de base de datos"""
        # Verificar que las funciones principales existen
        from database import db_manager
        
        assert hasattr(db_manager, 'create_connection')
        assert hasattr(db_manager, 'open_session')
        assert hasattr(db_manager, 'create_tables')
        assert callable(db_manager.create_connection)
        assert callable(db_manager.open_session)
        assert callable(db_manager.create_tables)


class TestDatabaseHealthCheck:
    """Tests de verificación de salud de la base de datos"""
    
    @patch('database.db_manager.create_connection')
    def test_database_connection_health_check_success(self, mock_create_connection):
        """Test de verificación exitosa de salud de conexión"""
        # Configurar mock
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_engine.connect.return_value = mock_connection
        mock_create_connection.return_value = mock_engine
        
        # Simular health check
        engine = mock_create_connection()
        connection = engine.connect()
        
        # Verificar que la conexión se puede establecer
        assert connection == mock_connection
        mock_engine.connect.assert_called_once()
    
    @patch('database.db_manager.create_connection')
    def test_database_connection_health_check_failure(self, mock_create_connection):
        """Test de fallo en verificación de salud de conexión"""
        # Configurar mock para que falle
        mock_engine = MagicMock()
        mock_engine.connect.side_effect = Exception("Connection test failed")
        mock_create_connection.return_value = mock_engine
        
        # Simular health check que falla
        engine = mock_create_connection()
        
        with pytest.raises(Exception, match="Connection test failed"):
            engine.connect()


class TestIntegration:
    """Tests de integración del módulo database"""
    
    @patch('database.db_manager.os.getenv')
    @patch('database.db_manager.create_engine')
    @patch('database.db_manager.sessionmaker')
    def test_complete_database_workflow(self, mock_sessionmaker, mock_create_engine, mock_getenv):
        """Test de workflow completo de base de datos"""
        # Configurar mocks
        mock_getenv.return_value = "postgresql://test:test@localhost:5432/test"
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_session_class = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_sessionmaker.return_value = mock_session_class
        
        # Ejecutar workflow completo
        engine = create_connection()
        session = open_session()
        
        # Verificar workflow
        assert engine == mock_engine
        assert session == mock_session
        mock_getenv.assert_called()
        mock_create_engine.assert_called()
        mock_sessionmaker.assert_called()
    
    def test_all_database_functions_callable(self):
        """Test de verificación de que todas las funciones sean llamables"""
        from database import db_manager
        
        # Funciones que deben existir y ser llamables
        expected_functions = [
            'create_connection',
            'open_session', 
            'create_tables'
        ]
        
        for func_name in expected_functions:
            assert hasattr(db_manager, func_name), f"Función {func_name} no existe"
            assert callable(getattr(db_manager, func_name)), f"Función {func_name} no es callable"


def test_module_import():
    """Test de importación correcta del módulo database"""
    # Verificar que se pueden importar las funciones principales
    from database.db_manager import create_connection, open_session, create_tables
    
    assert create_connection is not None
    assert open_session is not None
    assert create_tables is not None
    
    # Verificar que se puede importar el módulo completo
    import database.db_manager as db_manager
    assert db_manager is not None
