from fastapi import FastAPI
import server.database.db_manager as database
import server.scraper.scrp as scrp
from server.core.config import setting



# print   ("🟢 Iniciando la extracción de comentarios de YouTube..."  )
# retorno = scrp.scrape_youtube_comments("https://www.youtube.com/watch?v=8kZMBVvK-gg")

# database.insert_video_from_scrapper(retorno)

# print("🟢 Extracción completada."  )


app = FastAPI(
    title=setting.title,
    version=setting.version,
    description=setting.description
    )

@app.get("/")
def read_root():
    return {
        "Título": setting.title,
        "Version": setting.version,
        "Descripcion": setting.description,
        "Autores": setting.authors
        }

@app.post("/"+setting.version+"/prediction_request")
async def read_root(data: dict):
    scrape_data = scrp.scrape_youtube_comments(data["url"])
    database.insert_video_from_scrapper(scrape_data)
    return {
        "prediction_request": ""
        }

@app.get("/"+setting.version+"/prediction_list")
async def read_root():
    return {
        "prediction_list": database.get_request_list(),
    }

@app.get("/"+setting.version+"/prediction_detail/{id}")
async def read_root(id: int):
    return {
        "prediction": database.get_request(id),
    }