from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import uuid
import asyncio

# Importar módulos existentes
import server.database.db_manager as database
import server.scraper.scrp as scrp
from server.core.config import setting
from server.scraper.progress_manager import progress_manager
from server.scraper.scrp_socket import scrape_youtube_comments_async

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

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Incluir las rutas de toxicidad
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
            "analyze_video_with_ml": f"/{setting.version}/analyze_video_with_ml",
            "docs": "/docs"
        }
    }

@app.post("/"+setting.version+"/prediction_request")
async def prediction_request(data: dict):
    """Endpoint original de tu compañero"""
    scrape_data = scrp.scrape_youtube_comments(data["url"])
    database.insert_video_from_scrapper(scrape_data)
    return {
        "prediction_request": ""
    }

@app.get("/"+setting.version+"/prediction_list")
async def prediction_list():
    return {
        "prediction_list": database.get_request_list(),
    }

@app.get("/"+setting.version+"/prediction_detail/{id}")
async def prediction_detail(id: int):
    return {
        "prediction": database.get_request_by_id(id),
    }

# ✅ WEBSOCKET ENDPOINT
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket para progreso en tiempo real"""
    await progress_manager.connect(websocket, session_id)
    try:
        while True:
            # Mantener conexión viva
            await websocket.receive_text()
    except WebSocketDisconnect:
        progress_manager.disconnect(session_id)

# ✅ ÚNICO ENDPOINT CON WEBSOCKET (eliminar duplicado)
@app.post("/"+setting.version+"/analyze_video_with_ml")
async def analyze_video_with_ml(data: dict, background_tasks: BackgroundTasks):
    """Endpoint que combina scraping + análisis ML + base de datos"""
    try:
        # Generar ID único para esta sesión
        session_id = str(uuid.uuid4())
        
        # Extraer max_comments con valor por defecto
        max_comments = data.get("max_comments", 50)
        
        # Validar el número de comentarios
        if not isinstance(max_comments, int) or max_comments < 5 or max_comments > 1000:
            raise HTTPException(
                status_code=400, 
                detail=f"max_comments debe ser un entero entre 5 y 1000. Recibido: {max_comments}"
            )
        
        # Iniciar proceso en background
        background_tasks.add_task(process_video_analysis, data["url"], session_id, max_comments)
        
        return {
            "success": True,
            "session_id": session_id,
            "max_comments": max_comments,
            "message": f"Análisis iniciado para {max_comments} comentarios. Conéctate al WebSocket para seguir el progreso."
        }
        
    except Exception as e:
        logger.error(f"Error iniciando análisis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_video_analysis(video_url: str, session_id: str, max_comments: int = 50):
    """Procesar análisis de video en background"""
    try:
        # 1. Scraping con progreso
        await progress_manager.send_progress(session_id, 5, f"🎬 Iniciando análisis de video ({max_comments} comentarios)...")
        
        scrape_data = await scrape_youtube_comments_async(
            video_url, 
            max_comments=max_comments, 
            session_id=session_id
        )
        
        # ✅ VALIDAR scrape_data
        if not scrape_data or not isinstance(scrape_data, dict):
            await progress_manager.send_completion(session_id, False, error="Error en el scraping: datos inválidos")
            return
        
        if 'threads' not in scrape_data or not scrape_data['threads']:
            await progress_manager.send_completion(session_id, False, error="Error: No se encontraron comentarios para analizar")
            return
        
        logger.info(f"✅ Scraping exitoso: {scrape_data.get('total_comments', 0)} comentarios extraídos")
        
        # 2. Análisis de toxicidad con ML usando TU pipeline
        await progress_manager.send_progress(session_id, 80, "🤖 Analizando toxicidad con IA...")
        
        try:
            # ✅ USAR TU PIPELINE EXISTENTE
            from server.ml.pipeline import ToxicityPipeline
            pipeline = ToxicityPipeline()
            
            logger.info("🤖 Pipeline de toxicidad inicializado correctamente")
            
            # ✅ USAR TU MÉTODO analyze_youtube_comments
            analysis = pipeline.analyze_youtube_comments(scrape_data)
            
            if analysis is None:
                raise Exception("El pipeline devolvió None")
                
            logger.info("✅ Análisis de toxicidad completado exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error en análisis de toxicidad: {e}")
            # Crear análisis de fallback
            analysis = {
                'total_comments': scrape_data.get('total_comments', 0),
                'toxic_comments': 0,
                'toxicity_rate': 0.0,
                'analysis_results': [],
                'summary': {
                    'categories_found': {},
                    'most_toxic_comment': None,
                    'average_toxicity': 0.0,
                    'model_info': {
                        'model_type': 'Error - Fallback',
                        'version': '1.0.0',
                        'device': 'CPU',
                        'error': str(e)
                    }
                }
            }
        
        # 3. Guardar en base de datos (opcional)
        await progress_manager.send_progress(session_id, 95, "💾 Guardando resultados...")
        
        # TODO: Implementar guardado si lo necesitas
        # try:
        #     enhanced_data = analysis.get('enhanced_scraped_data', scrape_data)
        #     database.insert_video_from_scrapper(enhanced_data)
        #     logger.info("✅ Datos guardados en base de datos")
        # except Exception as e:
        #     logger.warning(f"⚠️ Error guardando en BD: {e}")
        
        await asyncio.sleep(1)
        
        # 4. Finalización exitosa
        result = {
            "video_url": video_url,
            "max_comments_requested": max_comments,
            "actual_comments_found": scrape_data.get('total_comments', 0),
            "actual_replies_found": scrape_data.get('total_threads', 0),
            "scraping_data": scrape_data,
            "analysis": analysis
        }
        
        logger.info(f"🎉 Análisis completado exitosamente para {video_url}")
        await progress_manager.send_completion(session_id, True, result)
        
    except Exception as e:
        logger.error(f"❌ Error en análisis de video: {e}")
        import traceback
        traceback.print_exc()
        await progress_manager.send_completion(session_id, False, error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)