from typing import List, Dict, Any
from .predictor import ToxicityPredictor
import logging

class ToxicityPipeline:
    """Pipeline completo para análisis de toxicidad"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.predictor = ToxicityPredictor()
        self.logger.info("ToxicityPipeline inicializado")
    
    def analyze_youtube_comments(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar comentarios de YouTube scraped"""
        
        # Extraer textos de comentarios
        comment_texts = []
        for thread in scraped_data.get("threads", []):
            if "comment" in thread and thread["comment"]:
                comment_texts.append(thread["comment"])
        
        if not comment_texts:
            return {
                'total_comments': 0,
                'toxic_comments': 0,
                'toxicity_rate': 0.0,
                'analysis_results': [],
                'summary': {
                    'categories_found': {},
                    'most_toxic_comment': None,
                    'average_toxicity': 0.0
                }
            }
        
        # Predecir toxicidad
        self.logger.info(f"Analizando {len(comment_texts)} comentarios")
        predictions = self.predictor.predict_batch(comment_texts)
        
        # Calcular estadísticas
        toxic_count = sum(1 for pred in predictions if pred['is_toxic'])
        toxicity_rate = toxic_count / len(predictions) if predictions else 0
        
        # Análisis de categorías
        categories_count = {}
        total_toxicity = 0
        most_toxic_comment = None
        max_toxicity = 0
        
        for pred in predictions:
            total_toxicity += pred['toxicity_confidence']
            
            # Buscar comentario más tóxico
            if pred['toxicity_confidence'] > max_toxicity:
                max_toxicity = pred['toxicity_confidence']
                most_toxic_comment = pred
            
            # Contar categorías
            for category in pred['categories_detected']:
                categories_count[category] = categories_count.get(category, 0) + 1
        
        # Agregar predicciones a datos originales
        for i, prediction in enumerate(predictions):
            if i < len(scraped_data["threads"]):
                scraped_data["threads"][i]["toxicity_analysis"] = prediction
        
        return {
            'total_comments': len(comment_texts),
            'toxic_comments': toxic_count,
            'toxicity_rate': toxicity_rate,
            'analysis_results': predictions,
            'enhanced_scraped_data': scraped_data,
            'summary': {
                'categories_found': categories_count,
                'most_toxic_comment': most_toxic_comment,
                'average_toxicity': total_toxicity / len(predictions) if predictions else 0,
                'model_info': self.predictor.get_model_info()
            }
        }
    
    def analyze_single_comment(self, comment: str) -> Dict[str, Any]:
        """Analizar un solo comentario"""
        return self.predictor.predict_single(comment)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Estado de salud del pipeline"""
        model_info = self.predictor.get_model_info()
        
        return {
            'status': 'healthy' if model_info['model_loaded'] else 'unhealthy',
            'model_info': model_info,
            'pipeline_version': '1.0.0'
        }