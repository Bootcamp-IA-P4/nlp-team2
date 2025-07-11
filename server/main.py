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
from server.scraper.scrp_socket import scrape_youtube_comments_with_progress  # ✅ Usar versión síncrona con WebSocket

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
    allow_origins=["http://localhost:3000", "http://localhost:5173","https://nlp-team2-front.onrender.com"],
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
    """Endpoint mejorado que incluye información de toxicidad REAL"""
    try:
        requests_data = database.get_request_list()
        
        enriched_requests = []
        for request_data in requests_data:
            video_data = request_data.get('video', {})
            
            # 🎯 OBTENER DATOS DE TOXICIDAD REALES
            toxicity_summary = database.get_toxicity_summary_by_request(request_data['id'])
            
            request_dict = {
                "id": request_data['id'],
                "fk_video_id": request_data['fk_video_id'],
                "request_date": request_data['request_date'].isoformat() if request_data['request_date'] else None,
                "created_at": request_data['request_date'].isoformat() if request_data['request_date'] else None,
                
                # Información del video
                "video_title": video_data.get('title', "Sin título"),
                "video_url": video_data.get('video_url', ""),
                "video_author": video_data.get('author_name', "Desconocido"),
                "video_description": video_data.get('description', ""),
                
                # Estadísticas básicas
                "total_comments": video_data.get('total_comments', 0),
                "total_replies": video_data.get('total_threads', 0),
                "total_likes": video_data.get('total_likes', 0),
                "total_emojis": video_data.get('total_emojis', 0),
                
                # 🎯 INFORMACIÓN DE TOXICIDAD REAL DE LA BD
                "toxicity_rate": float(toxicity_summary.toxicity_rate) if toxicity_summary else 0.0,
                "categories_summary": toxicity_summary.categories_summary if toxicity_summary else {},
                "toxic_comments": toxicity_summary.toxic_comments if toxicity_summary else 0,
                "average_toxicity": float(toxicity_summary.average_toxicity) if toxicity_summary else 0.0,
                "analysis_completed": toxicity_summary.analysis_completed_at.isoformat() if toxicity_summary and toxicity_summary.analysis_completed_at else None,
                "has_toxicity_analysis": toxicity_summary is not None
            }
            
            enriched_requests.append(request_dict)
        
        return {
            "prediction_list": enriched_requests,
            "total_count": len(enriched_requests),
            "has_toxicity_analysis": any(req.get("has_toxicity_analysis", False) for req in enriched_requests)
        }
        
    except Exception as e:
        logger.error(f"Error en prediction_list: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

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
        
        # ✅ EJECUTAR TU SCRAPER
        loop = asyncio.get_event_loop()
        scrape_data = await loop.run_in_executor(
            None,
            scrape_youtube_comments_with_progress,
            video_url,
            max_comments,
            session_id
        )
        
        # ✅ VALIDAR scrape_data
        if not scrape_data or not isinstance(scrape_data, dict):
            await progress_manager.send_completion(session_id, False, error="Error en el scraping: datos inválidos")
            return
        
        if 'threads' not in scrape_data or not scrape_data['threads']:
            await progress_manager.send_completion(session_id, False, error="Error: No se encontraron comentarios para analizar")
            return
        
        logger.info(f"✅ Scraping exitoso: {scrape_data.get('total_comments', 0)} comentarios extraídos")
        
        # 2. Análisis de toxicidad con ML
        await progress_manager.send_progress(session_id, 80, "🤖 Analizando toxicidad con IA...")
        
        try:
            from server.ml.pipeline import ToxicityPipeline
            pipeline = ToxicityPipeline()
            
            logger.info("🤖 Pipeline de toxicidad inicializado correctamente")
            analysis = pipeline.analyze_youtube_comments(scrape_data)
            
            if analysis is None:
                raise Exception("El pipeline devolvió None")
                
            logger.info("✅ Análisis de toxicidad completado exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error en análisis de toxicidad: {e}")
            # Crear análisis de fallback
            analysis = {
                'total_comments': scrape_data.get('total_comments', 0),
                'total_replies': 0,
                'total_analyzed': scrape_data.get('total_comments', 0),
                'toxic_comments': 0,
                'toxic_replies': 0,
                'total_toxic': 0,
                'toxicity_rate': 0.0,
                'main_comments_toxicity_rate': 0.0,
                'replies_toxicity_rate': 0.0,
                'analysis_results': [],
                'main_comments_analysis': [],
                'replies_analysis': [],
                'enhanced_scraped_data': scrape_data,
                'summary': {
                    'categories_found': {},
                    'most_toxic_comment': None,
                    'most_toxic_reply': None,
                    'average_toxicity': 0.0,
                    'model_info': {
                        'model_type': 'Error - Fallback',
                        'version': '1.0.0',
                        'device': 'CPU',
                        'error': str(e)
                    }
                }
            }
        
        # 3. Guardar en base de datos (ACTUALIZADO)
        await progress_manager.send_progress(session_id, 95, "💾 Guardando resultados...")
        
        bd_success = False
        toxicity_bd_success = False
        request_id = None
        video_id = None
        
        try:
            # 🎯 GUARDAR DATOS DE SCRAPING
            enhanced_data = analysis.get('enhanced_scraped_data', scrape_data)
            database.insert_video_from_scrapper(enhanced_data)
            logger.info("✅ Datos de scraping guardados en base de datos")
            bd_success = True
            
            # 🎯 OBTENER IDs PARA GUARDAR TOXICIDAD
            # Buscar el request recién creado
            video_id_from_data = enhanced_data.get('video_id')
            if video_id_from_data:
                # Obtener el video por youtube_video_id
                session = database.open_session()
                from server.database.models import Video, Request
                
                video = session.query(Video).filter_by(youtube_video_id=video_id_from_data).first()
                if video:
                    video_id = video.id
                    # Obtener el request más reciente para este video
                    latest_request = session.query(Request).filter_by(fk_video_id=video_id).order_by(Request.request_date.desc()).first()
                    if latest_request:
                        request_id = latest_request.id
                
                session.close()
            
            # 🎯 GUARDAR ANÁLISIS DE TOXICIDAD
            if request_id and video_id and analysis.get('total_toxic', 0) >= 0:  # Guardar incluso si no hay toxicidad
                toxicity_bd_success = database.save_toxicity_analysis(analysis, request_id, video_id)
                if toxicity_bd_success:
                    logger.info("✅ Análisis de toxicidad guardado en base de datos")
                else:
                    logger.warning("⚠️ Error guardando análisis de toxicidad")
            else:
                logger.warning(f"⚠️ No se pudo guardar toxicidad - request_id: {request_id}, video_id: {video_id}")
                
        except Exception as e:
            logger.warning(f"⚠️ Error guardando en BD: {e}")
            import traceback
            traceback.print_exc()
        
        await asyncio.sleep(1)
        
        # 4. ✅ SIEMPRE ENVIAR RESULTADO AL FRONTEND
        result = {
            "video_url": video_url,
            "max_comments_requested": max_comments,
            "actual_comments_found": scrape_data.get('total_comments', 0),
            "actual_replies_found": scrape_data.get('total_threads', 0),
            
            # 🎯 ESTADÍSTICAS DETALLADAS
            "total_analyzed": analysis.get('total_analyzed', 0),
            "main_comments_analyzed": analysis.get('total_comments', 0),
            "replies_analyzed": analysis.get('total_replies', 0),
            "toxic_main_comments": analysis.get('toxic_comments', 0),
            "toxic_replies": analysis.get('toxic_replies', 0),
            "total_toxic": analysis.get('total_toxic', 0),
            
            "scraping_data": scrape_data,
            "analysis": analysis,
            "database_saved": bd_success,
            "toxicity_saved": toxicity_bd_success,  # 🎯 NUEVO
            "request_id": request_id,  # 🎯 NUEVO
            "video_id": video_id  # 🎯 NUEVO
        }
        
        logger.info(f"🎉 Análisis completado exitosamente para {video_url}")
        logger.info(f"📊 Resultado: {analysis.get('total_analyzed', 0)} textos analizados, {analysis.get('total_toxic', 0)} tóxicos ({analysis.get('toxicity_rate', 0)*100:.1f}%)")
        logger.info(f"💾 BD: scraping={bd_success}, toxicidad={toxicity_bd_success}")
        
        # ✅ ENVIAR SIEMPRE AL FRONTEND
        await progress_manager.send_completion(session_id, True, result)
        
    except Exception as e:
        logger.error(f"❌ Error en análisis de video: {e}")
        import traceback
        traceback.print_exc()
        await progress_manager.send_completion(session_id, False, error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)