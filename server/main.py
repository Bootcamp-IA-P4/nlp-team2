from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Importar módulos existentes
import server.database.db_manager as database
import server.scraper.scrp as scrp
from server.core.config import setting

# Importar las rutas de toxicidad
from server.ml.api.toxicity_routes import router as toxicity_router

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=setting.title,
    version=setting.version,
    description=setting.description
)

# Configurar CORS para tu frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# ✅ INCLUIR LAS RUTAS DE TOXICIDAD
app.include_router(toxicity_router)

@app.get("/")
def read_root():
    return {
        "Título": setting.title,
        "Version": setting.version,
        "Descripcion": setting.description,
        "Autores": setting.authors,
        "endpoints": {
            "toxicity_health": "/api/v1/toxicity/health",
            "analyze_comment": "/api/v1/toxicity/analyze-comment",
            "analyze_youtube": "/api/v1/toxicity/analyze-youtube",
            "docs": "/docs"
        }
    }

@app.post("/"+setting.version+"/prediction_request")
async def read_root(data: dict):
    """Endpoint original de tu compañero"""
    scrape_data = scrp.scrape_youtube_comments(data["url"])
    database.insert_video_from_scrapper(scrape_data)
    return {
        "prediction_request": ""
    }

# ✅ NUEVO ENDPOINT INTEGRADO CON ML
@app.post("/"+setting.version+"/analyze_video_with_ml")
async def analyze_video_with_ml(data: dict):
    """Endpoint que combina scraping + análisis ML"""
    try:
        # 1. Scraping (código existente de tu compañero)
        scrape_data = scrp.scrape_youtube_comments(data["url"])
        
        # 2. Análisis de toxicidad con ML
        from server.ml.pipeline import ToxicityPipeline
        pipeline = ToxicityPipeline()
        analysis = pipeline.analyze_youtube_comments(scrape_data)
        
        # 3. Guardar en base de datos (código de tu compañero)
        database.insert_video_from_scrapper(analysis['enhanced_scraped_data'])
        
        return {
            "success": True,
            "video_url": data["url"],
            "scraping_data": scrape_data,
            "toxicity_analysis": analysis
        }
        
    except Exception as e:
        logger.error(f"Error en análisis completo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/"+setting.version+"/prediction_list")
async def read_root():
    return {
        "prediction_list": database.get_request_list(),
    }

@app.get("/"+setting.version+"/prediction_detail/{id}")
async def read_root(id: int):
    return {
        "prediction": database.get_request_by_id(id),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)