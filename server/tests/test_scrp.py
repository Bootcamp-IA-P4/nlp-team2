"""
Tests unitarios para el módulo scraper/scrp.py
Estos tests verifican las funcionalidades del scraper de YouTube sin dependencias externas.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock, PropertyMock
from pathlib import Path
from collections import Counter

# Agregar el directorio padre al path para poder importar
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock de dependencias externas antes de importar
sys.modules['selenium'] = MagicMock()
sys.modules['selenium.webdriver'] = MagicMock()
sys.modules['selenium.webdriver.common'] = MagicMock()
sys.modules['selenium.webdriver.common.by'] = MagicMock()
sys.modules['selenium.webdriver.chrome'] = MagicMock()
sys.modules['selenium.webdriver.chrome.service'] = MagicMock()
sys.modules['selenium.webdriver.chrome.options'] = MagicMock()
sys.modules['selenium.webdriver.support'] = MagicMock()
sys.modules['selenium.webdriver.support.ui'] = MagicMock()
sys.modules['selenium.webdriver.support.expected_conditions'] = MagicMock()
sys.modules['webdriver_manager'] = MagicMock()
sys.modules['webdriver_manager.chrome'] = MagicMock()
sys.modules['emoji'] = MagicMock()

# Configurar mocks de constantes
emoji_mock = MagicMock()
emoji_mock.EMOJI_DATA = {'😀': 'grinning face', '🎉': 'party popper', '❤': 'red heart'}
sys.modules['emoji'] = emoji_mock

# Ahora importar el módulo a testear
from scraper.scrp import YouTubeCommentScraperChrome, scrape_youtube_comments


class TestYouTubeCommentScraperChrome:
    """Tests para la clase YouTubeCommentScraperChrome"""
    
    def test_scraper_initialization_default(self):
        """Test de inicialización del scraper con valores por defecto"""
        scraper = YouTubeCommentScraperChrome()
        
        assert scraper.driver is None
        assert scraper.headless is True
        assert scraper.comments_data == []
        assert isinstance(scraper.emoji_counter, Counter)
        assert len(scraper.emoji_counter) == 0
    
    def test_scraper_initialization_headless_false(self):
        """Test de inicialización del scraper con headless=False"""
        scraper = YouTubeCommentScraperChrome(headless=False)
        
        assert scraper.driver is None
        assert scraper.headless is False
        assert scraper.comments_data == []
        assert isinstance(scraper.emoji_counter, Counter)
    
    def test_scraper_initialization_attributes(self):
        """Test de verificación de todos los atributos del scraper"""
        scraper = YouTubeCommentScraperChrome()
        
        # Verificar que tiene todos los atributos esperados
        assert hasattr(scraper, 'driver')
        assert hasattr(scraper, 'headless')
        assert hasattr(scraper, 'comments_data')
        assert hasattr(scraper, 'emoji_counter')
    
    def test_extract_emojis_no_emojis(self):
        """Test de extracción de emojis con texto sin emojis"""
        scraper = YouTubeCommentScraperChrome()
        text = "Este es un texto normal sin emojis"
        
        result = scraper.extract_emojis(text)
        
        assert result == []
        assert len(scraper.emoji_counter) == 0
    
    def test_extract_emojis_with_emojis(self):
        """Test de extracción de emojis con texto que contiene emojis"""
        scraper = YouTubeCommentScraperChrome()
        text = "Hola 😀 esto es genial 🎉"
        
        result = scraper.extract_emojis(text)
        
        assert len(result) == 2
        assert '😀' in result
        assert '🎉' in result
        assert scraper.emoji_counter['😀'] == 1
        assert scraper.emoji_counter['🎉'] == 1
    
    def test_extract_emojis_repeated_emojis(self):
        """Test de extracción de emojis con emojis repetidos"""
        scraper = YouTubeCommentScraperChrome()
        text = "😀😀😀 tres veces el mismo emoji"
        
        result = scraper.extract_emojis(text)
        
        assert len(result) == 3
        assert all(emoji == '😀' for emoji in result)
        assert scraper.emoji_counter['😀'] == 3
    
    def test_extract_emojis_multiple_different_emojis(self):
        """Test de extracción de múltiples emojis diferentes"""
        scraper = YouTubeCommentScraperChrome()
        text = "Me gusta 😀 esta canción 🎉 es increíble ❤"
        
        result = scraper.extract_emojis(text)
        
        assert len(result) == 3
        assert scraper.emoji_counter['😀'] == 1
        assert scraper.emoji_counter['🎉'] == 1
        assert scraper.emoji_counter['❤'] == 1
    
    def test_extract_emojis_empty_string(self):
        """Test de extracción de emojis con string vacío"""
        scraper = YouTubeCommentScraperChrome()
        text = ""
        
        result = scraper.extract_emojis(text)
        
        assert result == []
        assert len(scraper.emoji_counter) == 0
    
    def test_extract_emojis_counter_accumulation(self):
        """Test de acumulación del contador de emojis en múltiples llamadas"""
        scraper = YouTubeCommentScraperChrome()
        
        # Primera llamada
        scraper.extract_emojis("Hola 😀")
        # Segunda llamada
        scraper.extract_emojis("Adiós 😀 hasta luego 🎉")
        
        assert scraper.emoji_counter['😀'] == 2
        assert scraper.emoji_counter['🎉'] == 1
    
    @patch('scraper.scrp.ChromeDriverManager')
    @patch('scraper.scrp.webdriver')
    @patch('scraper.scrp.Service')
    def test_setup_driver_success_with_manager(self, mock_service, mock_webdriver, mock_manager):
        """Test de configuración exitosa del driver con ChromeDriverManager"""
        # Configurar mocks
        mock_manager.return_value.install.return_value = "/path/to/chromedriver"
        mock_driver = MagicMock()
        mock_webdriver.Chrome.return_value = mock_driver
        
        scraper = YouTubeCommentScraperChrome()
        scraper.setup_driver()
        
        # Verificar que se configuró el driver
        assert scraper.driver == mock_driver
        mock_driver.execute_script.assert_called_once()
    
    @patch('scraper.scrp.ChromeDriverManager')
    @patch('scraper.scrp.webdriver')
    def test_setup_driver_fallback_to_system_chrome(self, mock_webdriver, mock_manager):
        """Test de fallback a Chrome del sistema cuando ChromeDriverManager falla"""
        # ChromeDriverManager falla
        mock_manager.return_value.install.side_effect = Exception("ChromeDriverManager failed")
        
        # Chrome del sistema funciona
        mock_driver = MagicMock()
        mock_webdriver.Chrome.return_value = mock_driver
        
        scraper = YouTubeCommentScraperChrome()
        scraper.setup_driver()
        
        # Verificar que se configuró el driver con Chrome del sistema
        assert scraper.driver == mock_driver
        mock_driver.execute_script.assert_called_once()
    
    @patch('scraper.scrp.ChromeDriverManager')
    @patch('scraper.scrp.webdriver')
    def test_setup_driver_complete_failure(self, mock_webdriver, mock_manager):
        """Test de fallo completo en configuración del driver"""
        # Ambos métodos fallan
        mock_manager.return_value.install.side_effect = Exception("ChromeDriverManager failed")
        mock_webdriver.Chrome.side_effect = Exception("Chrome failed")
        
        scraper = YouTubeCommentScraperChrome()
        
        with pytest.raises(Exception, match="No se pudo configurar Chrome en Docker"):
            scraper.setup_driver()


class TestScrapingMethods:
    """Tests para métodos de scraping que requieren driver activo"""
    
    def test_scroll_to_load_comments_setup(self):
        """Test de configuración inicial para scroll_to_load_comments"""
        scraper = YouTubeCommentScraperChrome()
        
        # Mock del driver
        mock_driver = MagicMock()
        scraper.driver = mock_driver
        
        # Configurar mocks para simular comportamiento de scroll
        mock_driver.execute_script.side_effect = [
            None,  # window.scrollTo(0, 800)
            1000,  # document.documentElement.scrollHeight (inicial)
            None,  # window.scrollTo(0, document.documentElement.scrollHeight)
            1000,  # document.documentElement.scrollHeight (después del scroll)
        ]
        
        # Mock para find_elements que retorna comentarios cargados
        mock_driver.find_elements.return_value = [MagicMock() for _ in range(5)]
        
        # Verificar que el método existe y es callable
        assert hasattr(scraper, 'scroll_to_load_comments')
        assert callable(scraper.scroll_to_load_comments)
    
    def test_extract_comment_data_method_exists(self):
        """Test de verificación de existencia del método extract_comment_data"""
        scraper = YouTubeCommentScraperChrome()
        
        assert hasattr(scraper, 'extract_comment_data')
        assert callable(scraper.extract_comment_data)
    
    def test_extract_reply_data_method_exists(self):
        """Test de verificación de existencia del método extract_reply_data"""
        scraper = YouTubeCommentScraperChrome()
        
        assert hasattr(scraper, 'extract_reply_data')
        assert callable(scraper.extract_reply_data)
    
    def test_scrape_video_comments_method_exists(self):
        """Test de verificación de existencia del método scrape_video_comments"""
        scraper = YouTubeCommentScraperChrome()
        
        assert hasattr(scraper, 'scrape_video_comments')
        assert callable(scraper.scrape_video_comments)


class TestGlobalFunctions:
    """Tests para funciones globales del módulo"""
    
    def test_scrape_youtube_comments_function_exists(self):
        """Test de verificación de existencia de la función global"""
        assert callable(scrape_youtube_comments)
    
    @patch('scraper.scrp.YouTubeCommentScraperChrome')
    @patch('scraper.scrp.os.getenv')
    def test_scrape_youtube_comments_with_defaults(self, mock_getenv, mock_scraper_class):
        """Test de función global con parámetros por defecto"""
        # Configurar mocks
        mock_getenv.side_effect = lambda key, default: {'MAX_COMMENTS': '500', 'ENTOR': 'Test'}.get(key, default)
        mock_scraper = MagicMock()
        mock_scraper_class.return_value = mock_scraper
        mock_scraper.scrape_video_comments.return_value = {
            'total_comments': 10,
            'total_threads': 5,
            'comments': []
        }
        
        # Ejecutar función
        scrape_youtube_comments("https://youtube.com/watch?v=test")
        
        # Verificar llamadas
        mock_scraper_class.assert_called_once_with(headless=True)
        mock_scraper.scrape_video_comments.assert_called_once()
    
    @patch('scraper.scrp.YouTubeCommentScraperChrome')
    @patch('scraper.scrp.os.getenv')
    def test_scrape_youtube_comments_with_custom_max_comments(self, mock_getenv, mock_scraper_class):
        """Test de función global con max_comments personalizado"""
        # Configurar mocks
        mock_getenv.side_effect = lambda key, default: {'MAX_COMMENTS': '1500', 'ENTOR': 'Test'}.get(key, default)
        mock_scraper = MagicMock()
        mock_scraper_class.return_value = mock_scraper
        mock_scraper.scrape_video_comments.return_value = None
        
        # Ejecutar función
        scrape_youtube_comments("https://youtube.com/watch?v=test", max_comments=2000)
        
        # Verificar llamadas
        mock_scraper_class.assert_called_once_with(headless=True)
        mock_scraper.scrape_video_comments.assert_called_once()


class TestIntegration:
    """Tests de integración del módulo scraper"""
    
    def test_scraper_workflow_initialization(self):
        """Test de workflow completo de inicialización del scraper"""
        # Crear scraper
        scraper = YouTubeCommentScraperChrome(headless=True)
        
        # Verificar estado inicial
        assert scraper.driver is None
        assert scraper.headless is True
        assert scraper.comments_data == []
        assert isinstance(scraper.emoji_counter, Counter)
        
        # Probar funcionalidad de emojis
        text_with_emojis = "Test 😀 con emojis 🎉"
        emojis = scraper.extract_emojis(text_with_emojis)
        
        assert len(emojis) == 2
        assert scraper.emoji_counter['😀'] == 1
        assert scraper.emoji_counter['🎉'] == 1
    
    def test_emoji_extraction_workflow(self):
        """Test de workflow completo de extracción de emojis"""
        scraper = YouTubeCommentScraperChrome()
        
        # Textos de prueba
        texts = [
            "Primer comentario 😀",
            "Segundo comentario 🎉 con múltiples emojis 😀",
            "Tercer comentario ❤",
            "Cuarto comentario sin emojis"
        ]
        
        all_emojis = []
        for text in texts:
            emojis = scraper.extract_emojis(text)
            all_emojis.extend(emojis)
        
        # Verificar resultados
        assert len(all_emojis) == 4  # 😀, 🎉, 😀, ❤
        assert scraper.emoji_counter['😀'] == 2
        assert scraper.emoji_counter['🎉'] == 1
        assert scraper.emoji_counter['❤'] == 1
    
    def test_all_methods_callable(self):
        """Test de verificación de que todos los métodos sean llamables"""
        scraper = YouTubeCommentScraperChrome()
        
        # Métodos que deben existir
        expected_methods = [
            'setup_driver',
            'extract_emojis',
            'scroll_to_load_comments',
            'extract_comment_data',
            'extract_reply_data',
            'scrape_video_comments'
        ]
        
        for method_name in expected_methods:
            assert hasattr(scraper, method_name), f"Método {method_name} no existe"
            assert callable(getattr(scraper, method_name)), f"Método {method_name} no es callable"


def test_module_import():
    """Test de importación correcta del módulo scrp"""
    # Verificar que se puede importar la clase principal
    from scraper.scrp import YouTubeCommentScraperChrome
    assert YouTubeCommentScraperChrome is not None
    
    # Verificar que se puede importar la función global
    from scraper.scrp import scrape_youtube_comments
    assert scrape_youtube_comments is not None
    
    # Verificar que se puede crear una instancia
    scraper = YouTubeCommentScraperChrome()
    assert scraper is not None
