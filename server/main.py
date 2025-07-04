import database.db_manager as database
import scraper.scrp as scrp

print   ("🟢 Iniciando la extracción de comentarios de YouTube..."  )
retorno = scrp.scrape_youtube_comments("https://www.youtube.com/watch?v=8kZMBVvK-gg")

database.insert_video_from_scrapper(retorno)

print("🟢 Extracción completada."  )
