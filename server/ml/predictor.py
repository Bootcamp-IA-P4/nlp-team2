import os
import pickle
import torch
import numpy as np
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging
from datetime import datetime

class ToxicityPredictor:
    """Predictor de toxicidad optimizado para producción"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        # Configurar rutas
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "models", "distilbert_model.pkl")
        
        self.model_path = model_path
        self.metrics_path = os.path.join(os.path.dirname(model_path), "metrics.pkl")
        
        # Cargar modelo
        self._load_model()
        
        # Configurar dispositivo
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if hasattr(self.model, 'to'):
            self.model.to(self.device)
            self.model.eval()
        
        self.logger.info(f"ToxicityPredictor inicializado en {self.device}")
    
    def _load_model(self):
        """Cargar modelo y tokenizer"""
        try:
            # Cargar métricas
            if os.path.exists(self.metrics_path):
                with open(self.metrics_path, 'rb') as f:
                    self.model_metrics = pickle.load(f)
            else:
                self.model_metrics = {}
            
            # Cargar modelo
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                # Extraer componentes según el tipo de datos
                if hasattr(model_data, 'model'):
                    self.model = model_data.model
                    self.tokenizer = model_data.tokenizer
                elif isinstance(model_data, dict):
                    self.model = model_data.get('model')
                    self.tokenizer = model_data.get('tokenizer')
                else:
                    self.model = model_data
                    self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
                
                self.logger.info("Modelo cargado desde archivo local")
            else:
                # Fallback: modelo base
                self._load_base_model()
                
        except Exception as e:
            self.logger.error(f"Error cargando modelo: {e}")
            self._load_base_model()
    
    def _load_base_model(self):
        """Cargar modelo base como fallback"""
        self.logger.warning("Cargando modelo base DistilBERT")
        
        self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = AutoModelForSequenceClassification.from_pretrained(
            'distilbert-base-uncased',
            num_labels=12,
            problem_type="multi_label_classification"
        )
        self.model_metrics = {"model_type": "base", "trained": False}
    
    def predict_single(self, text: str) -> Dict[str, Any]:
        """Predecir toxicidad para un solo comentario"""
        
        # Preprocesamiento básico
        cleaned_text = text.strip().lower()
        
        # Tokenización
        inputs = self.tokenizer(
            cleaned_text,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Predicción
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.sigmoid(outputs.logits).cpu().numpy()[0]
        
        # Clasificación binaria
        threshold = 0.5
        predictions = (probabilities > threshold).astype(int)
        
        # Etiquetas
        labels = [
            'IsToxic', 'IsAbusive', 'IsThreat', 'IsProvocative', 
            'IsObscene', 'IsHatespeech', 'IsRacist', 'IsNationalist',
            'IsSexist', 'IsHomophobic', 'IsReligiousHate', 'IsRadicalism'
        ]
        
        # Ajustar etiquetas
        labels = labels[:len(probabilities)]
        
        # Resultado estructurado
        categories_detected = []
        category_scores = {}
        
        for i, label in enumerate(labels):
            if i < len(predictions) and predictions[i] == 1:
                categories_detected.append(label)
                category_scores[label] = float(probabilities[i])
        
        return {
            'text': text,
            'is_toxic': bool(predictions[0]) if len(predictions) > 0 else False,
            'toxicity_confidence': float(probabilities[0]) if len(probabilities) > 0 else 0.0,
            'categories_detected': categories_detected,
            'category_scores': category_scores,
            'processing_time': datetime.now().isoformat(),
            'model_version': self.get_model_info()['version']
        }
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Predecir toxicidad para múltiples comentarios"""
        results = []
        
        for text in texts:
            try:
                result = self.predict_single(text)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error procesando texto: {e}")
                results.append({
                    'text': text,
                    'is_toxic': False,
                    'toxicity_confidence': 0.0,
                    'categories_detected': [],
                    'category_scores': {},
                    'error': str(e),
                    'processing_time': datetime.now().isoformat()
                })
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """Información del modelo"""
        return {
            'model_type': 'DistilBERT',
            'version': '1.0.0',
            'device': str(self.device),
            'metrics': self.model_metrics,
            'model_loaded': self.model is not None,
            'tokenizer_loaded': self.tokenizer is not None
        }