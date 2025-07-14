from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from ml.pipeline import ToxicityPipeline

# Configurar router
router = APIRouter(prefix="/v1/toxicity", tags=["toxicity"])  # ← Quitar /api/
logger = logging.getLogger(__name__)

# Inicializar pipeline global
try:
    toxicity_pipeline = ToxicityPipeline()
    PIPELINE_AVAILABLE = True
    logger.info("Pipeline de toxicidad inicializado correctamente")
except Exception as e:
    logger.error(f"Error inicializando pipeline: {e}")
    PIPELINE_AVAILABLE = False

# Modelos Pydantic
class CommentRequest(BaseModel):
    comment: str

class CommentsRequest(BaseModel):
    comments: List[str]

class YouTubeAnalysisRequest(BaseModel):
    video_url: str
    scraped_data: Dict[str, Any]

@router.get("/health")
def get_health():
    """Estado de salud del sistema de toxicidad"""
    if not PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Pipeline no disponible")
    
    return toxicity_pipeline.get_health_status()

@router.post("/analyze-comment")
def analyze_single_comment(request: CommentRequest):
    """Analizar un solo comentario"""
    if not PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Pipeline no disponible")
    
    try:
        result = toxicity_pipeline.analyze_single_comment(request.comment)
        return {
            'success': True,
            'result': result
        }
    except Exception as e:
        logger.error(f"Error analizando comentario: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-comments")
def analyze_multiple_comments(request: CommentsRequest):
    """Analizar múltiples comentarios"""
    if not PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Pipeline no disponible")
    
    try:
        results = toxicity_pipeline.predictor.predict_batch(request.comments)
        
        # Estadísticas rápidas
        toxic_count = sum(1 for r in results if r.get('is_toxic', False))
        
        return {
            'success': True,
            'total_comments': len(results),
            'toxic_comments': toxic_count,
            'toxicity_rate': toxic_count / len(results) if results else 0,
            'results': results
        }
    except Exception as e:
        logger.error(f"Error analizando comentarios: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-youtube")
def analyze_youtube_data(request: YouTubeAnalysisRequest):
    """Analizar datos scraped de YouTube"""
    if not PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Pipeline no disponible")
    
    try:
        analysis = toxicity_pipeline.analyze_youtube_comments(request.scraped_data)
        
        return {
            'success': True,
            'video_url': request.video_url,
            'analysis': analysis
        }
    except Exception as e:
        logger.error(f"Error analizando YouTube: {e}")
        raise HTTPException(status_code=500, detail=str(e))