from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


import time
import os
from selenium.webdriver.common.keys import Keys



# Configurar Selenium con Chrome en modo headless
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(os.getenv("GECKODRIVER_PATH"))  # Ruta de GeckoDriver para Firefox DOCKER
    return webdriver.Firefox(service=service, options=options)

def scroll_to_load_comments(driver, scroll_pause=2, max_scrolls=20):
    
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    for _ in range(max_scrolls):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scrape_youtube_comments(video_url):
    print(f"🔵 Extrayendo comentarios de: {video_url}")
    driver = get_driver()
    driver.get(video_url)
    print("🔵 Navegando a la URL de YouTube..." )


    try:
        # Esperar a que cargue la sección de comentarios
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#comments"))
        )
        # Extraer título del video
        video_title = driver.title

        # Extraer autor del video
        author_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-channel-name a"))
        )
        video_author = author_elem.text
        # Extraer descripción del video
        descri_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#attributed-snippet-text"))
        )
        descri_author = descri_elem.text.strip()

        scroll_to_load_comments(driver)
        
        comment_threads = []
        comment_elements = driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer")

        # 1. Scroll para asegurar carga
        for _ in range(10):
            driver.execute_script("window.scrollBy(0, 2500);")
            time.sleep(1)

        # 2. Clic en todos los botones "Ver respuestas"
        reply_buttons = driver.find_elements(By.CSS_SELECTOR, "ytd-button-renderer#more-replies")
        reply_buttons = driver.find_elements(By.CSS_SELECTOR, "ytd-button-renderer.style-scope.ytd-comment-replies-renderer button")
         
        for button in reply_buttons:
            try:
                driver.execute_script("arguments[0].click();", button)
                #print("🔵 Clic en botón 'Ver respuestas' realizado.", button)
                time.sleep(0.5)
            except Exception as e:
                print("Error al hacer clic:", e)

        # 3. Extraer comentarios y respuestas
        for thread_elem in comment_elements:
            try:
                main_comment = thread_elem.find_element(By.CSS_SELECTOR, "#content #content-text").text
                main_author = thread_elem.find_element(By.CSS_SELECTOR, "#author-text span").text.strip()
            except:
                continue

            # Buscar respuestas dentro del hilo
            replies = []
            try:
                replies_container = thread_elem.find_element(By.CSS_SELECTOR, "ytd-comment-replies-renderer")
                reply_elems = replies_container.find_elements(By.CSS_SELECTOR, "ytd-comment-renderer")
                #print(f"🔵 Respuestas encontradas: {len(reply_elems)}")
                for reply in reply_elems:
                    try:
                        reply_author = reply.find_element(By.CSS_SELECTOR, "#author-text span").text.strip()
                        reply_text_elem = reply.find_element(By.CSS_SELECTOR, "#content #content-text")
                        reply_text = reply_text_elem.text.strip()
                        if reply_text:
                            replies.append({
                                "author": reply_author,
                                "comment": reply_text
                            })
                    except NoSuchElementException:
                        continue
            except NoSuchElementException:
                pass

            comment_threads.append({
                "author": main_author,
                "comment": main_comment,
                "replies": replies
            })

        return {
            "video_id": video_url.split("v=")[-1],
            "video_url": video_url,
            "title": video_title,
            "description": descri_author,
            "author": video_author,
            "total_threads": len(comment_threads),
            "threads": comment_threads
        }
    except Exception as e:
        print(f"❌ Error al extraer datos de YouTube: {e}")
        return {"error": str(e)}
    finally:
        print("🔴 Cerrando el navegador...")
        driver.quit()

