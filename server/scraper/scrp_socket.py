import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import emoji
from collections import Counter
import json
from server.core.print_dev import log_info, log_error, log_warning, log_debug
import asyncio
from server.scraper.progress_manager import progress_manager

class YouTubeCommentScraperChrome:
    def __init__(self, headless=True, progress_callback=None, session_id=None):
        """
        Inicializa el scraper de comentarios de YouTube para Docker con Chrome
        
        Args:
            headless (bool): Si True, ejecuta el navegador en modo sin interfaz gráfica
            progress_callback (function): Función opcional para reportar progreso
            session_id (str): ID de sesión para WebSocket
        """
        self.driver = None
        self.headless = headless
        self.comments_data = []
        self.emoji_counter = Counter()
        self.progress_callback = progress_callback
        self.session_id = session_id
        
    async def emit_progress(self, percentage, message):
        """Emitir progreso tanto por callback como por WebSocket"""
        print(f"📊 [{percentage}%] {message}")  # Log en consola
        
        # Callback original
        if self.progress_callback:
            self.progress_callback(percentage, message)
        
        # WebSocket para frontend
        if self.session_id:
            try:
                await progress_manager.send_progress(self.session_id, percentage, message)
            except Exception as e:
                print(f"⚠️ Error enviando progreso por WebSocket: {e}")
    
    async def setup_driver(self):
        await self.emit_progress(5, "🐳 Configurando Chrome para Docker...")
        chrome_options = Options()
        
        # Configuraciones obligatorias para Docker
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-webgl")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        # User agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Configuraciones adicionales para estabilidad
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            print("🐳 Configurando Chrome para Docker...")
            
            # Intentar primero con ChromeDriverManager
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ ChromeDriver automático configurado en Docker")
                await self.emit_progress(15, "✅ ChromeDriver automático configurado")
                
                # Configurar script para evitar detección
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                return
                
            except Exception as e:
                log_error("❌ ChormeDriverManager falló: " + str(e))
            
            # Intentar con Chrome del sistema
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                print("✅ Chrome del sistema configurado en Docker")
                await self.emit_progress(15, "✅ Chrome del sistema configurado")
                
                # Configurar script para evitar detección
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                return
                
            except Exception as e:
                log_error("❌ Chrome del sistema falló: " + str(e))
            
            raise Exception("No se pudo configurar Chrome en Docker")
            
        except Exception as e:
            raise Exception(f"Error configurando Chrome en Docker: {e}")
    
    def extract_emojis(self, text):

        emojis_found = []
        for char in text:
            if char in emoji.EMOJI_DATA:
                emojis_found.append(char)
                self.emoji_counter[char] += 1
        return emojis_found
    
    async def scroll_to_load_comments(self, max_comments=100):
        print(f"📜 Cargando comentarios... (máximo {max_comments})")
        
        # ✅ SCROLL MÁS AGRESIVO Y DEBUG
        for i in range(5):
            scroll_position = 800 + (i * 400)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(2)
            print(f"🔄 Scroll {i+1}/5 a posición {scroll_position}")
        
        # ✅ BUSCAR COMENTARIOS CON MÚLTIPLES SELECTORES
        comment_selectors = [
            "ytd-comment-thread-renderer",
            ".ytd-comment-thread-renderer", 
            "#comments ytd-comment-thread-renderer",
            "ytd-comments #comments ytd-comment-thread-renderer",
            "[id*='comment-thread']",
            ".comment-thread",
            "#comment-section ytd-comment-thread-renderer"
        ]
        
        comments_found = 0
        working_selector = None
        
        for selector in comment_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"🔍 Selector '{selector}': encontró {len(elements)} elementos")
                if elements:
                    comments_found = len(elements)
                    working_selector = selector
                    print(f"✅ Usando selector: {selector}")
                    break
            except Exception as e:
                print(f"❌ Error con selector {selector}: {e}")
        
        # ✅ DEBUG ADICIONAL SI NO ENCUENTRA COMENTARIOS
        if comments_found == 0:
            print("⚠️ No se encontraron comentarios con ningún selector")
            
            # Verificar si la sección de comentarios existe
            try:
                comments_section = self.driver.find_element(By.CSS_SELECTOR, "#comments")
                print("📍 ✅ Sección de comentarios (#comments) encontrada")
            except:
                print("📍 ❌ Sección de comentarios (#comments) NO encontrada")
            
            try:
                ytd_comments = self.driver.find_element(By.CSS_SELECTOR, "ytd-comments")
                print("📍 ✅ Elemento ytd-comments encontrado")
            except:
                print("📍 ❌ Elemento ytd-comments NO encontrado")
            
            # Verificar si los comentarios están deshabilitados
            try:
                page_source = self.driver.page_source
    
                # ✅ VERIFICACIÓN MÁS ESPECÍFICA
                comments_disabled_phrases = [
                    "comments are turned off",
                    "comentarios están desactivados", 
                    "comments are disabled",
                    "comment section is disabled",
                    "commenting has been disabled",
                    "comments on this video have been disabled"
                ]
                
                # Verificar si REALMENTE están deshabilitados (verificación estricta)
                actually_disabled = False
                for phrase in comments_disabled_phrases:
                    if phrase in page_source.lower():
                        # Verificar que no sea parte de otro texto
                        context_start = max(0, page_source.lower().find(phrase) - 50)
                        context_end = min(len(page_source), page_source.lower().find(phrase) + len(phrase) + 50)
                        context = page_source[context_start:context_end].lower()
                        
                        # Si aparece en un contexto que indica que están realmente deshabilitados
                        if ("section" in context or "video" in context or "turn" in context):
                            actually_disabled = True
                            print(f"🚫 ❌ Los comentarios están REALMENTE DESHABILITADOS: '{phrase}'")
                            print(f"📄 Contexto: {context}")
                            break
                
                if not actually_disabled:
                    if "comment" in page_source.lower():
                        print("💭 ✅ La palabra 'comment' aparece en la página")
                        comment_count = page_source.lower().count("comment")
                        print(f"📊 'comment' aparece {comment_count} veces en el HTML")
                        
                        # ✅ INTENTAR FORZAR CARGA DE COMENTARIOS
                        print("🔄 Intentando forzar carga de comentarios...")
                        
                        # Scroll más agresivo a la sección de comentarios
                        try:
                            # Buscar la sección de comentarios y hacer scroll hasta ella
                            comments_section = self.driver.find_element(By.CSS_SELECTOR, "#comments")
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", comments_section)
                            time.sleep(3)
                            print("📍 ✅ Scroll hasta sección de comentarios")
                            
                            # Scroll adicional para cargar comentarios
                            for i in range(5):
                                scroll_position = 1000 + (i * 500)
                                self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                                time.sleep(2)
                                
                                # Verificar si aparecieron comentarios
                                new_comments = len(self.driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer"))
                                if new_comments > 0:
                                    print(f"🎉 ¡Comentarios encontrados después del scroll {i+1}! ({new_comments} comentarios)")
                                    comments_found = new_comments
                                    working_selector = "ytd-comment-thread-renderer"
                                    break
                                else:
                                    print(f"⏳ Scroll {i+1}/5 - Aún sin comentarios...")
                        
                        except Exception as e:
                            print(f"❌ Error en scroll forzado: {e}")
                else:
                    print("🚫 ❌ Los comentarios están DESHABILITADOS en este video")
            
            except Exception as e:
                print(f"❌ Error verificando HTML: {e}")
            
            # Intentar hacer screenshot para debug
            try:
                self.driver.save_screenshot("debug_no_comments.png")
                print("📸 Screenshot guardado como debug_no_comments.png")
            except Exception as e:
                print(f"❌ Error guardando screenshot: {e}")
            
            return  # Salir si no hay comentarios
        
        # ✅ CONTINUAR CON SCROLL SI ENCONTRAMOS COMENTARIOS
        print(f"🎯 Encontrados {comments_found} comentarios iniciales, continuando con scroll...")
        
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        comments_loaded = comments_found
        scroll_attempts = 0
        max_scroll_attempts = 5  # Reducir intentos
        
        while comments_loaded < max_comments and scroll_attempts < max_scroll_attempts:
            # Scroll hacia abajo
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(3)
            
            # Usar el selector que funcionó
            current_comments = len(self.driver.find_elements(By.CSS_SELECTOR, working_selector))
            
            if current_comments > comments_loaded:
                comments_loaded = current_comments
                progress = 60 + (10 * min(comments_loaded / max_comments, 1))
                await self.emit_progress(int(progress), f"📝 Comentarios cargados: {comments_loaded}")
                print(f"📝 Comentarios cargados: {comments_loaded}")
                scroll_attempts = 0
            else:
                scroll_attempts += 1
                print(f"⏳ Intento de scroll {scroll_attempts}/{max_scroll_attempts}")
            
            # Verificar si la página sigue creciendo
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height and comments_loaded >= 1:
                await self.emit_progress(70, f"🔚 Carga completada con {comments_loaded} comentarios")
                print(f"🔚 Altura de página estabilizada en {comments_loaded} comentarios")
                break
            last_height = new_height
            
            if comments_loaded >= max_comments:
                print(f"🎯 Objetivo alcanzado: {comments_loaded} comentarios")
                break
    
    def extract_comment_data(self, comment_element):

        try:
            # Autor del comentario
            author_selectors = [
                "#author-text",
                ".ytd-comment-renderer #author-text",
                "a#author-text",
                "[id*='author-text']"
            ]
            
            author = "Autor desconocido"
            for selector in author_selectors:
                try:
                    author_element = comment_element.find_element(By.CSS_SELECTOR, selector)
                    author = author_element.text.strip()
                    break
                except:
                    continue
            
            # Contenido del comentario
            content_selectors = [
                "#content-text",
                ".ytd-comment-renderer #content-text",
                "#comment-content #content-text",
                "[id*='content-text']"
            ]
            
            content = "Contenido no disponible"
            for selector in content_selectors:
                try:
                    content_element = comment_element.find_element(By.CSS_SELECTOR, selector)
                    content = content_element.text.strip()
                    break
                except:
                    continue
            
            # Likes del comentario
            likes = 0
            like_selectors = [
                "#vote-count-middle",
                ".ytd-comment-action-buttons-renderer #vote-count-middle",
                "[id*='vote-count']"
            ]
            
            for selector in like_selectors:
                try:
                    like_element = comment_element.find_element(By.CSS_SELECTOR, selector)
                    likes_text = like_element.text.strip()
                    
                    if likes_text == '':
                        likes = 0
                    elif 'K' in likes_text:
                        likes = int(float(likes_text.replace('K', '')) * 1000)
                    elif 'M' in likes_text:
                        likes = int(float(likes_text.replace('M', '')) * 1000000)
                    else:
                        likes = int(likes_text) if likes_text.isdigit() else 0
                    break
                except:
                    continue
            
            # Tiempo del comentario
            published_time = "Desconocido"
            time_selectors = [
                ".published-time-text",
                "[class*='published-time']",
                "a[href*='lc=']"
            ]
            
            for selector in time_selectors:
                try:
                    time_element = comment_element.find_element(By.CSS_SELECTOR, selector)
                    published_time = time_element.text.strip()
                    break
                except:
                    continue
            
            # Extraer emojis
            emojis = self.extract_emojis(content)
            
            # Verificar si los datos del comentario son válidos
            if (author == "Autor desconocido" or 
                content == "Contenido no disponible" or 
                content == "" or 
                author == ""):
                print(f"⚠️ Saltando comentario con datos inválidos: author='{author}', content='{content}'")
                return None
            
            # Verificar si tiene respuestas y extraerlas
            has_replies = False
            replies_count = 0
            replies_data = []
            
            # Buscar botón de respuestas con selectores optimizados para Chrome
            reply_selectors = [
                "#more-replies",
                "button[aria-label*='respuesta']",
                "button[aria-label*='reply']",
                "button[aria-label*='replies']",
                "ytd-button-renderer[is-paper-button] button",
                ".more-button",
                "#replies-button"
            ]
            
            for selector in reply_selectors:
                try:
                    replies_button = comment_element.find_element(By.CSS_SELECTOR, selector)
                    button_text = replies_button.text.strip()
                    aria_label = replies_button.get_attribute('aria-label') or ''
                    
                    # Verificar si es botón de respuestas
                    if (("respuesta" in button_text.lower() or "reply" in button_text.lower() or "replies" in button_text.lower()) or
                        ("respuesta" in aria_label.lower() or "reply" in aria_label.lower() or "replies" in aria_label.lower())):
                        
                        has_replies = True
                        
                        # Extraer número de respuestas del texto
                        numbers = re.findall(r'\d+', button_text + ' ' + aria_label)
                        if numbers:
                            replies_count = int(numbers[0])
                        
                        print(f"🔄 Encontrado botón de respuestas: '{button_text}' con {replies_count} respuestas")
                        
                        # Hacer clic para expandir respuestas
                        try:
                            # Scroll al elemento antes de hacer clic
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", replies_button)
                            time.sleep(1)
                            
                            # Hacer clic con JavaScript para mayor confiabilidad
                            self.driver.execute_script("arguments[0].click();", replies_button)
                            time.sleep(3)  # Esperar más tiempo para que se carguen las respuestas
                            
                            # Buscar respuestas con múltiples selectores más específicos
                            reply_container_selectors = [
                                "#replies",
                                "ytd-comment-replies-renderer",
                                ".ytd-comment-replies-renderer",
                                "#expander-contents"
                            ]
                            
                            reply_elements = []
                            for container_selector in reply_container_selectors:
                                try:
                                    container = comment_element.find_element(By.CSS_SELECTOR, container_selector)
                                    # Intentar múltiples selectores para encontrar respuestas individuales
                                    reply_selectors_inner = [
                                        "ytd-comment-view-model",
                                        ".ytd-comment-view-model", 
                                        "ytd-comment-renderer",
                                        ".ytd-comment-renderer",
                                        "#comment",
                                        ".comment"
                                    ]
                                    
                                    for reply_selector in reply_selectors_inner:
                                        reply_elements = container.find_elements(By.CSS_SELECTOR, reply_selector)
                                        if reply_elements:
                                            print(f"✅ Encontradas respuestas con selector: {container_selector} > {reply_selector}")
                                            break
                                    
                                    if reply_elements:
                                        break
                                except Exception as inner_e:
                                    print(f"Error con contenedor {container_selector}: {inner_e}")
                                    continue
                            
                            print(f"💬 Encontradas {len(reply_elements)} respuestas para procesar")
                            
                            valid_replies_count = 0
                            for reply_elem in reply_elements[:8]:  # Limitar a 8 respuestas por comentario
                                reply_data = self.extract_reply_data(reply_elem)
                                if reply_data:  # Solo agregar si los datos son válidos
                                    replies_data.append(reply_data)
                                    valid_replies_count += 1
                            
                            print(f"✅ Procesadas {valid_replies_count} respuestas válidas de {len(reply_elements[:8])} intentadas")
                            
                        except Exception as e:
                            print(f"⚠️ Error expandiendo respuestas: {e}")
                        
                        break
                        
                except Exception as e:
                    continue
            
            return {
                'author': author,
                'comment': content,
                'likes': likes,
                'published_time': published_time,
                'emojis': emojis,
                'emoji_count': len(emojis),
                'has_replies': has_replies,
                'replies_count': max(replies_count, len(replies_data)),  # Usar el mayor entre el conteo y las respuestas reales
                'replies': replies_data
            }
            
        except Exception as e:
            log_error("❌ Error extrayendo comentario: " + str(e))

            return None
    
    def extract_reply_data(self, reply_element):

        try:
            # Autor de la respuesta - selectores optimizados para Chrome
            author_selectors = [
                "#author-text",
                ".ytd-comment-renderer #author-text",
                "a#author-text",
                "[id*='author-text']",
                "a[href*='@']"
            ]
            
            author = "Autor desconocido"
            for selector in author_selectors:
                try:
                    author_element = reply_element.find_element(By.CSS_SELECTOR, selector)
                    author = author_element.text.strip()

                    break
                except:
                    continue
            
            # Contenido de la respuesta
            content_selectors = [
                "#content-text",
                ".ytd-comment-renderer #content-text",
                "#comment-content #content-text",
                "[id*='content-text']",
                ".comment-text"
            ]
            
            content = "Contenido no disponible"
            for selector in content_selectors:
                try:
                    content_element = reply_element.find_element(By.CSS_SELECTOR, selector)
                    content = content_element.text.strip()
                    break
                except:
                    continue
            
            # Likes de la respuesta
            likes = 0
            like_selectors = [
                "#vote-count-middle",
                ".ytd-comment-action-buttons-renderer #vote-count-middle",
                "[id*='vote-count']",
                ".vote-count-middle"
            ]
            
            for selector in like_selectors:
                try:
                    like_element = reply_element.find_element(By.CSS_SELECTOR, selector)
                    likes_text = like_element.text.strip()
                    
                    if likes_text == '':
                        likes = 0
                    elif 'K' in likes_text:
                        likes = int(float(likes_text.replace('K', '')) * 1000)
                    elif 'M' in likes_text:
                        likes = int(float(likes_text.replace('M', '')) * 1000000)
                    else:
                        likes = int(likes_text) if likes_text.isdigit() else 0
                    break
                except:
                    continue
            
            # Extraer emojis de la respuesta
            emojis = self.extract_emojis(content)
            
            # Verificar si los datos son válidos (no desconocidos/no disponibles)
            if (author == "Autor desconocido" or 
                content == "Contenido no disponible" or 
                content == "" or 
                author == ""):
                print(f"⚠️ Saltando respuesta con datos inválidos: author='{author}', content='{content}'")
                return None
            
            return {
                'author': author,
                'comment': content,
                'likes': likes,
                'emojis': emojis,
                'emoji_count': len(emojis)
            }
            
        except Exception as e:
            log_error("❌ Error extrayendo respuesta: " + str(e))
            return None
    
    async def scrape_video_comments(self, video_url, max_comments=50):
        """Scrape los comentarios de un video de YouTube"""
        try:
            await self.emit_progress(10, "🚀 Iniciando proceso de scraping...")
            await self.setup_driver()
            await self.emit_progress(20, f"🌐 Accediendo a: {video_url}")
            print(f"🌐 Accediendo a: {video_url}")
            
            # Cargar la página del video
            self.driver.get(video_url)
            await self.emit_progress(25, "📖 Página cargada, extrayendo metadatos...")
            
            # Esperar a que la página cargue
            wait = WebDriverWait(self.driver, 30)
            
            # Obtener título del video
            await self.emit_progress(30, "🎬 Extrayendo título del video...")
            video_title = "Título no disponible"
            title_selectors = [
                "h1.ytd-watch-metadata",
                "h1.ytd-video-primary-info-renderer", 
                "h1[class*='title']",
                "h1 yt-formatted-string",
                "#title h1"
            ]
            
            for selector in title_selectors:
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    video_title = self.driver.find_element(By.CSS_SELECTOR, selector).text
                    break
                except:
                    continue
            
            await self.emit_progress(35, f"✅ Título encontrado: {video_title[:50]}...")
            print(f"🎬 Video: {video_title}")
            
            # Extraer ID del video de la URL
            video_id = "ID no disponible"
            try:
                if "v=" in video_url:
                    video_id = video_url.split("v=")[1].split("&")[0]
                elif "youtu.be/" in video_url:
                    video_id = video_url.split("youtu.be/")[1].split("?")[0]
            except:
                pass
            
            # Obtener autor del video
            await self.emit_progress(40, "👤 Extrayendo información del autor...")
            video_author = "Autor no disponible"
            author_selectors = [
                "ytd-channel-name #text",
                "ytd-channel-name a",
                "#owner-text a",
                "#upload-info #owner-text a",
                ".ytd-video-owner-renderer a",
                "ytd-video-owner-renderer #text",
                "#channel-name #text"
            ]
            
            for selector in author_selectors:
                try:
                    author_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    video_author = author_element.text.strip()
                    if video_author and video_author != "":
                        print(f"👤 Autor encontrado con selector: {selector}")
                        break
                except:
                    continue
            
            await self.emit_progress(45, f"✅ Autor encontrado: {video_author}")
            print(f"🆔 Video ID: {video_id}")
            print(f"👤 Autor: {video_author}")
            
            # Obtener descripción del video
            await self.emit_progress(50, "📝 Extrayendo descripción del video...")
            video_description = "Descripción no disponible"
            
            # Scroll hacia la sección de descripción y esperar más tiempo
            self.driver.execute_script("window.scrollTo(0, 600);")
            time.sleep(3)
            
            # Intentar buscar y expandir cualquier botón de expandir descripción
            try:
                # Buscar todos los posibles botones de expandir
                expand_selectors = [
                    "tp-yt-paper-button#expand",
                    "button#expand", 
                    ".more-button",
                    "[aria-label*='Show more']",
                    "[aria-label*='más']", 
                    "button[aria-label*='more']",
                    "ytd-button-renderer[aria-label*='more']",
                    "button[class*='expand']"
                ]
                
                for selector in expand_selectors:
                    try:
                        buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                print(f"🔧 Haciendo clic en botón expandir: {selector}")
                                self.driver.execute_script("arguments[0].click();", button)
                                time.sleep(2)
                                break
                    except:
                        continue
            except:
                pass
            
            # Lista ampliada de selectores para encontrar la descripción
            description_selectors = [
                # Selectores más recientes de YouTube
                "ytd-text-inline-expander #content",
                "ytd-text-inline-expander yt-formatted-string",
                "#description-inline-expander #content",
                "#description-inline-expander yt-formatted-string",
                
                # Selectores de la estructura expandida
                "#description yt-formatted-string",
                "#description .content",
                "#description",
                
                # Selectores de metadatos
                "ytd-video-secondary-info-renderer #description",
                "ytd-video-secondary-info-renderer yt-formatted-string",
                ".ytd-expandable-video-description-body-renderer",
                "yt-formatted-string.ytd-expandable-video-description-body-renderer",
                
                # Selectores genéricos
                "#meta #description",
                "#description-text",
                ".description-text",
                "[id*='description']",
                
                # Selectores más específicos
                "ytd-watch-metadata #description",
                "ytd-video-primary-info-renderer #description"
            ]
            
            # Intentar con cada selector
            for selector in description_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        desc_text = element.text.strip()
                        if desc_text and len(desc_text) > 10:
                            video_description = desc_text
                            print(f"📝 Descripción encontrada con selector: {selector}")
                            break
                    if video_description != "Descripción no disponible":
                        break
                except Exception as e:
                    continue
            
            # Si aún no encontramos descripción, intentar con JavaScript
            if video_description == "Descripción no disponible":
                try:
                    js_description = self.driver.execute_script("""
                        // Buscar elementos que contengan descripción
                        var desc = '';
                        var selectors = [
                            'ytd-text-inline-expander',
                            '[id*="description"]',
                            '[class*="description"]',
                            'yt-formatted-string'
                        ];
                        
                        for (var i = 0; i < selectors.length; i++) {
                            var elements = document.querySelectorAll(selectors[i]);
                            for (var j = 0; j < elements.length; j++) {
                                var text = elements[j].textContent || elements[j].innerText;
                                if (text && text.length > 50 && text.length < 5000) {
                                    return text.trim();
                                }
                            }
                        }
                        return '';
                    """)
                    
                    if js_description and len(js_description) > 10:
                        video_description = js_description
                        print(f"📝 Descripción encontrada con JavaScript")
                except:
                    pass
            
            await self.emit_progress(55, f"✅ Descripción extraída: {len(video_description)} caracteres")
            print(f"📝 Descripción extraída: {len(video_description)} caracteres")
            
            # Cargar comentarios
            await self.emit_progress(60, f"📜 Cargando comentarios (máximo {max_comments})...")
            await self.scroll_to_load_comments(max_comments)
            
            # Extraer comentarios
            await self.emit_progress(75, "🔍 Procesando comentarios extraídos...")
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer")
            total_elements = min(len(comment_elements), max_comments)
            await self.emit_progress(80, f"📝 Encontrados {len(comment_elements)} comentarios, procesando {total_elements}...")
            print(f"🔍 Procesando {len(comment_elements)} comentarios...")
            
            for i, comment_element in enumerate(comment_elements[:max_comments]):
                comment_data = self.extract_comment_data(comment_element)
                if comment_data:
                    self.comments_data.append(comment_data)
                    
                if (i + 1) % 3 == 0:
                    print(f"✅ Procesados {i + 1} comentarios...")
                
                # Actualizar progreso cada 5 comentarios para la web
                if (i + 1) % 5 == 0 or i == total_elements - 1:
                    progress = 80 + (15 * (i + 1) / total_elements)
                    await self.emit_progress(int(progress), f"✅ Procesados {i + 1}/{total_elements} comentarios...")
            
            # Estadísticas
            await self.emit_progress(95, "📊 Calculando estadísticas finales...")
            total_comments = len(self.comments_data)
            total_replies = sum(len(comment['replies']) for comment in self.comments_data)
            total_emojis = sum(comment['emoji_count'] for comment in self.comments_data)
            total_likes = sum(comment['likes'] for comment in self.comments_data)
            
            # Emojis y likes de las respuestas
            reply_emojis = 0
            reply_likes = 0
            for comment in self.comments_data:
                for reply in comment['replies']:
                    reply_emojis += reply['emoji_count']
                    reply_likes += reply['likes']
            
            total_emojis += reply_emojis
            total_likes += reply_likes
            
            results = {
                'video_id': video_id,
                'video_url': video_url,
                'title': video_title,
                'description': video_description,
                'author': video_author,
                'total_likes': total_likes,
                'total_comments': total_comments,
                'emoji_stats': dict(self.emoji_counter),
                'total_emojis': total_emojis,
                'most_common_emojis': dict(self.emoji_counter.most_common(10)),
                'total_threads': total_replies,
                'threads': self.comments_data
            }
            
            await self.emit_progress(100, f"🎉 ¡Scraping completado! {total_comments} comentarios y {total_replies} respuestas extraídas")
            
            # Notificar finalización exitosa
            if self.session_id:
                await progress_manager.send_completion(self.session_id, True, results)
            
            return results
            
        except Exception as e:
            await self.emit_progress(-1, f"❌ Error durante el scraping: {e}")
            
            # Notificar error
            if self.session_id:
                await progress_manager.send_completion(self.session_id, False, error=str(e))
            
            return None

# Función wrapper async
async def scrape_youtube_comments_async(video_url, max_comments=50, session_id=None):
    """Función principal async para scraping con progreso"""
    try:
        scraper = YouTubeCommentScraperChrome(headless=True, session_id=session_id)
        return await scraper.scrape_video_comments(video_url, max_comments)
    except Exception as e:
        print(f"❌ Error en scrape_youtube_comments_async: {e}")
        import traceback
        traceback.print_exc()
        return None

