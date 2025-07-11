import os
import pickle
import torch
import numpy as np
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from datetime import datetime
from server.core.print_dev import log_info, log_error, log_warning, log_debug

# Importar funciones optimizadas para carga de modelo
from server.ml.api import get_model_efficiently, suppress_torch_numpy_warnings


class ToxicityPredictor:
    """Predictor de toxicidad optimizado para producción"""
    
    def __init__(self):
        # Configurar rutas para las métricas
        self.metrics_path = os.path.join(os.path.dirname(__file__), "model", "metrics.pkl")
        
        # Cargar modelo
        self._load_model()
        
        # Configurar dispositivo
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if hasattr(self.model, 'to'):
            self.model.to(self.device)
            self.model.eval()
        
        log_info(f"ToxicityPredictor inicializado en {self.device}")
    
    def _load_model(self):
        """
        Cargar modelo y tokenizer directamente en memoria.
        No requiere archivos locales ya que utiliza get_model_efficiently
        para unir y deserializar el modelo directamente en memoria.
        """
        try:
            # Cargar métricas
            if os.path.exists(self.metrics_path):
                with open(self.metrics_path, 'rb') as f:
                    self.model_metrics = pickle.load(f)
            else:
                self.model_metrics = {}
                log_warning(f"No se encontraron métricas en: {self.metrics_path}")
            
            # Cargar modelo
            # Siempre intenta cargar el modelo unificado en memoria
            # Intentar cargar el modelo eficientemente desde memoria compartida o caché
            try:
                log_info("Intentando cargar el modelo eficientemente desde memoria...")
                # Usar el contexto para suprimir advertencias durante la carga
                with suppress_torch_numpy_warnings():
                    # get_model_efficiently ya devuelve el modelo deserializado, no bytes
                    model_data = get_model_efficiently()
                log_info(f"Modelo cargado eficientemente: {type(model_data)}")
            except Exception as e:
                log_warning(f"No se pudo cargar el modelo eficientemente: {e}")
                log_warning("Utilizando modelo base como fallback")
                self._load_base_model()
                return

            # Extraer componentes según el tipo de datos
            if model_data is None:
                raise ValueError("El modelo cargado es None")
                
            if hasattr(model_data, 'model'):
                self.model = model_data.model
                self.tokenizer = model_data.tokenizer
                log_info("Modelo cargado desde objeto con atributos 'model' y 'tokenizer'")
            elif isinstance(model_data, dict):
                self.model = model_data.get('model')
                self.tokenizer = model_data.get('tokenizer')
                log_info("Modelo cargado desde diccionario con claves 'model' y 'tokenizer'")
            else:
                self.model = model_data
                log_info("Cargando tokenizer desde pretrained...")
                self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
                log_info("Tokenizer cargado desde pretrained")
            
            log_info(f"Modelo cargado correctamente. Tipo: {type(self.model)}")
                
        except Exception as e:
            log_error(f"Error cargando modelo: {e}")
            log_error(f"Detalles del error: {str(e)}")
            self._load_base_model()
    
    def _load_base_model(self):
        """Cargar modelo base como fallback"""
        log_warning("Cargando modelo base DistilBERT")
        
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
                log_error(f"Error procesando texto: {e}")
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