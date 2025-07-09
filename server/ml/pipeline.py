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
        """Analizar comentarios de YouTube scraped - INCLUYENDO RESPUESTAS"""
        
        # Extraer textos de comentarios Y respuestas
        comment_texts = []
        comment_metadata = []  # Para rastrear origen (comentario vs respuesta)
        
        for thread_idx, thread in enumerate(scraped_data.get("threads", [])):
            # 🎯 ANALIZAR COMENTARIO PRINCIPAL
            if "comment" in thread and thread["comment"]:
                comment_texts.append(thread["comment"])
                comment_metadata.append({
                    'type': 'main_comment',
                    'thread_index': thread_idx,
                    'author': thread.get('author', 'Desconocido'),
                    'likes': thread.get('likes', 0)
                })
            
            # 🎯 ANALIZAR RESPUESTAS (NUEVO)
            if "replies" in thread and thread["replies"]:
                for reply_idx, reply in enumerate(thread["replies"]):
                    if reply and reply.get("comment"):
                        comment_texts.append(reply["comment"])
                        comment_metadata.append({
                            'type': 'reply',
                            'thread_index': thread_idx,
                            'reply_index': reply_idx,
                            'author': reply.get('author', 'Desconocido'),
                            'likes': reply.get('likes', 0),
                            'parent_author': thread.get('author', 'Desconocido')
                        })
        
        if not comment_texts:
            return {
                'total_comments': 0,
                'total_replies': 0,
                'toxic_comments': 0,
                'toxic_replies': 0,
                'toxicity_rate': 0.0,
                'analysis_results': [],
                'summary': {
                    'categories_found': {},
                    'most_toxic_comment': None,
                    'most_toxic_reply': None,
                    'average_toxicity': 0.0
                }
            }
        
        # Predecir toxicidad para TODOS los textos (comentarios + respuestas)
        self.logger.info(f"Analizando {len(comment_texts)} textos total (comentarios + respuestas)")
        predictions = self.predictor.predict_batch(comment_texts)
        
        # 🎯 SEPARAR RESULTADOS POR TIPO
        main_comments_analysis = []
        replies_analysis = []
        toxic_count = 0
        toxic_replies_count = 0
        toxic_main_comments_count = 0
        total_toxicity = 0
        categories_count = {}
        most_toxic_comment = None
        most_toxic_reply = None
        max_toxicity = 0
        max_reply_toxicity = 0
        
        for i, (prediction, metadata) in enumerate(zip(predictions, comment_metadata)):
            is_toxic = prediction.get('is_toxic', False)
            toxicity_confidence = prediction.get('toxicity_confidence', 0)
            total_toxicity += toxicity_confidence
            
            # Agregar metadata al resultado
            prediction['metadata'] = metadata
            
            if metadata['type'] == 'main_comment':
                main_comments_analysis.append(prediction)
                if is_toxic:
                    toxic_main_comments_count += 1
                    if toxicity_confidence > max_toxicity:
                        max_toxicity = toxicity_confidence
                        most_toxic_comment = prediction
            else:  # reply
                replies_analysis.append(prediction)
                if is_toxic:
                    toxic_replies_count += 1
                    if toxicity_confidence > max_reply_toxicity:
                        max_reply_toxicity = toxicity_confidence
                        most_toxic_reply = prediction
            
            if is_toxic:
                toxic_count += 1
                # Contar categorías
                for category in prediction.get('categories_detected', []):
                    categories_count[category] = categories_count.get(category, 0) + 1
        
        # Calcular estadísticas
        total_main_comments = len(main_comments_analysis)
        total_replies = len(replies_analysis)
        toxicity_rate = toxic_count / len(predictions) if predictions else 0
        
        # 🎯 AGREGAR ANÁLISIS A LOS DATOS ORIGINALES
        for thread_idx, thread in enumerate(scraped_data["threads"]):
            # Agregar análisis al comentario principal
            main_analysis = [p for p in main_comments_analysis 
                            if p['metadata']['thread_index'] == thread_idx]
            if main_analysis:
                thread["toxicity_analysis"] = main_analysis[0]
            
            # Agregar análisis a las respuestas
            if "replies" in thread and thread["replies"]:
                for reply_idx, reply in enumerate(thread["replies"]):
                    reply_analysis = [p for p in replies_analysis 
                                    if p['metadata']['thread_index'] == thread_idx 
                                    and p['metadata']['reply_index'] == reply_idx]
                    if reply_analysis:
                        reply["toxicity_analysis"] = reply_analysis[0]
        
        return {
            'total_comments': total_main_comments,
            'total_replies': total_replies,
            'total_analyzed': len(predictions),
            'toxic_comments': toxic_main_comments_count,
            'toxic_replies': toxic_replies_count,
            'total_toxic': toxic_count,
            'toxicity_rate': toxicity_rate,
            'main_comments_toxicity_rate': toxic_main_comments_count / total_main_comments if total_main_comments > 0 else 0,
            'replies_toxicity_rate': toxic_replies_count / total_replies if total_replies > 0 else 0,
            'analysis_results': predictions,
            'main_comments_analysis': main_comments_analysis,
            'replies_analysis': replies_analysis,
            'enhanced_scraped_data': scraped_data,
            'summary': {
                'categories_found': categories_count,
                'most_toxic_comment': most_toxic_comment,
                'most_toxic_reply': most_toxic_reply,
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