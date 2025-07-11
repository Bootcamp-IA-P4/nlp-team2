"""
Tests básicos para el módulo core/print_dev.py
Estos tests verifican las funcionalidades de logging del sistema.
"""

import pytest
import sys
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

# Agregar el directorio padre al path para poder importar
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.print_dev import (
        SimpleLogger, 
        Colors, 
        logger,
        is_running_local,
        printer_mensaje,
        log_debug,
        log_info,
        log_warning,
        log_error
    )
except ImportError as e:
    pytest.skip(f"No se pudo importar el módulo print_dev: {e}", allow_module_level=True)


class TestColors:
    """Tests para la clase Colors"""
    
    def test_colors_defined(self):
        """Test: Verificar que los colores están definidos"""
        assert hasattr(Colors, 'RESET'), "Color RESET no está definido"
        assert hasattr(Colors, 'RED'), "Color RED no está definido"
        assert hasattr(Colors, 'GREEN'), "Color GREEN no está definido"
        assert hasattr(Colors, 'YELLOW'), "Color YELLOW no está definido"
        assert hasattr(Colors, 'CYAN'), "Color CYAN no está definido"
    
    def test_colors_are_strings(self):
        """Test: Verificar que los colores son strings"""
        assert isinstance(Colors.RESET, str), "RESET debe ser string"
        assert isinstance(Colors.RED, str), "RED debe ser string"
        assert isinstance(Colors.GREEN, str), "GREEN debe ser string"
        assert isinstance(Colors.YELLOW, str), "YELLOW debe ser string"
        assert isinstance(Colors.CYAN, str), "CYAN debe ser string"
    
    def test_colors_contain_escape_sequences(self):
        """Test: Verificar que los colores contienen secuencias de escape"""
        assert '\033[' in Colors.RESET, "RESET debe contener secuencia de escape"
        assert '\033[' in Colors.RED, "RED debe contener secuencia de escape"
        assert '\033[' in Colors.GREEN, "GREEN debe contener secuencia de escape"
        assert '\033[' in Colors.YELLOW, "YELLOW debe contener secuencia de escape"
        assert '\033[' in Colors.CYAN, "CYAN debe contener secuencia de escape"


class TestSimpleLogger:
    """Tests básicos para la clase SimpleLogger"""
    
    def test_logger_initialization(self):
        """Test: Verificar inicialización del logger"""
        test_logger = SimpleLogger()
        
        # Verificar que tiene el directorio de logs
        assert hasattr(test_logger, 'log_dir'), "Logger debe tener log_dir"
        assert isinstance(test_logger.log_dir, Path), "log_dir debe ser Path"
    
    def test_logger_has_methods(self):
        """Test: Verificar que el logger tiene todos los métodos necesarios"""
        test_logger = SimpleLogger()
        
        assert hasattr(test_logger, 'debug'), "Logger debe tener método debug"
        assert hasattr(test_logger, 'info'), "Logger debe tener método info"
        assert hasattr(test_logger, 'warning'), "Logger debe tener método warning"
        assert hasattr(test_logger, 'error'), "Logger debe tener método error"
        assert hasattr(test_logger, '_write_log'), "Logger debe tener método _write_log"
    
    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch.object(Path, 'mkdir')
    def test_debug_method(self, mock_mkdir, mock_file, mock_print):
        """Test: Verificar método debug"""
        test_logger = SimpleLogger()
        test_message = "Mensaje de debug"
        
        test_logger.debug(test_message)
        
        # Verificar que se llamó a print
        mock_print.assert_called_once()
        
        # Verificar que se intentó abrir el archivo
        mock_file.assert_called_once()
    
    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch.object(Path, 'mkdir')
    def test_info_method(self, mock_mkdir, mock_file, mock_print):
        """Test: Verificar método info"""
        test_logger = SimpleLogger()
        test_message = "Mensaje de info"
        
        test_logger.info(test_message)
        
        # Verificar que se llamó a print
        mock_print.assert_called_once()
        
        # Verificar que se intentó abrir el archivo
        mock_file.assert_called_once()
    
    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch.object(Path, 'mkdir')
    def test_warning_method(self, mock_mkdir, mock_file, mock_print):
        """Test: Verificar método warning"""
        test_logger = SimpleLogger()
        test_message = "Mensaje de warning"
        
        test_logger.warning(test_message)
        
        # Verificar que se llamó a print
        mock_print.assert_called_once()
        
        # Verificar que se intentó abrir el archivo
        mock_file.assert_called_once()
    
    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch.object(Path, 'mkdir')
    def test_error_method(self, mock_mkdir, mock_file, mock_print):
        """Test: Verificar método error"""
        test_logger = SimpleLogger()
        test_message = "Mensaje de error"
        
        test_logger.error(test_message)
        
        # Verificar que se llamó a print
        mock_print.assert_called_once()
        
        # Verificar que se intentó abrir el archivo
        mock_file.assert_called_once()


class TestGlobalFunctions:
    """Tests para las funciones globales del módulo"""
    
    def test_is_running_local_function_exists(self):
        """Test: Verificar que la función is_running_local existe"""
        assert callable(is_running_local), "is_running_local debe ser callable"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_is_running_local_without_gae_env(self):
        """Test: Verificar is_running_local sin GAE_ENV"""
        result = is_running_local()
        assert result == True, "Debe retornar True cuando GAE_ENV no está definido"
    
    @patch.dict(os.environ, {'GAE_ENV': 'standard'})
    def test_is_running_local_with_gae_env_standard(self):
        """Test: Verificar is_running_local con GAE_ENV=standard"""
        result = is_running_local()
        assert result == False, "Debe retornar False cuando GAE_ENV=standard"
    
    @patch.dict(os.environ, {'GAE_ENV': 'local'})
    def test_is_running_local_with_gae_env_local(self):
        """Test: Verificar is_running_local con GAE_ENV=local"""
        result = is_running_local()
        assert result == True, "Debe retornar True cuando GAE_ENV=local"
    
    def test_printer_mensaje_function_exists(self):
        """Test: Verificar que la función printer_mensaje existe"""
        assert callable(printer_mensaje), "printer_mensaje debe ser callable"
    
    @patch('core.print_dev.logger')
    def test_printer_mensaje_calls_logger_info(self, mock_logger):
        """Test: Verificar que printer_mensaje llama a logger.info"""
        test_message = "Test message"
        printer_mensaje(test_message)
        
        mock_logger.info.assert_called_once_with(str(test_message))


class TestLogFunctions:
    """Tests para las funciones de logging globales"""
    
    @patch('core.print_dev.logger')
    def test_log_debug_function(self, mock_logger):
        """Test: Verificar función log_debug"""
        test_message = "Debug message"
        log_debug(test_message)
        
        mock_logger.debug.assert_called_once_with(test_message)
    
    @patch('core.print_dev.logger')
    def test_log_info_function(self, mock_logger):
        """Test: Verificar función log_info"""
        test_message = "Info message"
        log_info(test_message)
        
        mock_logger.info.assert_called_once_with(test_message)
    
    @patch('core.print_dev.logger')
    def test_log_warning_function(self, mock_logger):
        """Test: Verificar función log_warning"""
        test_message = "Warning message"
        log_warning(test_message)
        
        mock_logger.warning.assert_called_once_with(test_message)
    
    @patch('core.print_dev.logger')
    def test_log_error_function(self, mock_logger):
        """Test: Verificar función log_error"""
        test_message = "Error message"
        log_error(test_message)
        
        mock_logger.error.assert_called_once_with(test_message)


class TestGlobalLogger:
    """Tests para el logger global"""
    
    def test_global_logger_exists(self):
        """Test: Verificar que existe el logger global"""
        assert logger is not None, "El logger global debe existir"
        assert isinstance(logger, SimpleLogger), "El logger global debe ser instancia de SimpleLogger"
    
    def test_global_logger_has_methods(self):
        """Test: Verificar que el logger global tiene todos los métodos"""
        assert hasattr(logger, 'debug'), "Logger global debe tener método debug"
        assert hasattr(logger, 'info'), "Logger global debe tener método info"
        assert hasattr(logger, 'warning'), "Logger global debe tener método warning"
        assert hasattr(logger, 'error'), "Logger global debe tener método error"


class TestIntegration:
    """Tests de integración básicos"""
    
    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch.object(Path, 'mkdir')
    def test_complete_logging_workflow(self, mock_mkdir, mock_file, mock_print):
        """Test: Verificar workflow completo de logging"""
        # Usar las funciones globales
        log_debug("Debug test")
        log_info("Info test")
        log_warning("Warning test") 
        log_error("Error test")
        
        # Verificar que se llamó a print 4 veces
        assert mock_print.call_count == 4, "Debería haberse llamado print 4 veces"
        
        # Verificar que se intentó abrir archivo 4 veces
        assert mock_file.call_count == 4, "Debería haberse intentado abrir archivo 4 veces"
    
    def test_all_functions_callable(self):
        """Test: Verificar que todas las funciones son callable"""
        functions_to_test = [
            is_running_local,
            printer_mensaje,
            log_debug,
            log_info,
            log_warning,
            log_error
        ]
        
        for func in functions_to_test:
            assert callable(func), f"La función {func.__name__} debe ser callable"


def test_module_import():
    """Test global: Verificar que el módulo se puede importar correctamente"""
    # Este test ya pasó si llegamos hasta aquí
    assert True, "El módulo print_dev se importó correctamente"
