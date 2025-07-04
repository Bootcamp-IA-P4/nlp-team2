from fastapi import FastAPI
import server.database.db_manager as database
import server.scraper.scrp as scrp
from app.core.config import setting



print   ("🟢 Iniciando la extracción de comentarios de YouTube..."  )
retorno = scrp.scrape_youtube_comments("https://www.youtube.com/watch?v=8kZMBVvK-gg")

database.insert_video_from_scrapper(retorno)

print("🟢 Extracción completada."  )


app = FastAPI(
    title=setting.title,
    version=setting.version,
    description=setting.description
    )


@app.get(f"/{setting.version}/prediction_request")
def read_root(data: dict):
    return {"mensaje": data["url"]}
