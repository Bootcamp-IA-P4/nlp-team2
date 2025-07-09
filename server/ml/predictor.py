import os
import pickle
import torch
import requests
import tempfile
import numpy as np
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging
from datetime import datetime

class ToxicityPredictor:
    """Predictor de toxicidad optimizado para producción, con descarga remota del modelo"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        base_url = os.getenv("MODEL_BASE_URL", "https://www.juancarlosmacias.es/models/distilbert_model.pkl")
        
        if model_path is None:
            model_file = "distilbert_model.pkl"
            self.model_path = base_url + model_file
        else:
            # Si no empieza con http, asumimos que es solo el nombre del archivo
            if not model_path.startswith("http"):
                self.model_path = base_url + model_path
            else:
                self.model_path = model_path
        
        self.metrics_path = None  # Asumimos que no hay métricas remotas
        
        self.temp_model_file = None
        
        self._load_model()
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if hasattr(self.model, 'to'):
            self.model.to(self.device)
            self.model.eval()
        
        self.logger.info(f"ToxicityPredictor inicializado en {self.device}")
    
    def _download_model(self, url: str) -> str:
        """Descarga el archivo modelo y devuelve la ruta local temporal"""
        self.logger.info(f"Descargando modelo desde {url}")
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f"No se pudo descargar el modelo. Código HTTP: {response.status_code}")
        
        # Guardar en archivo temporal
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pkl")
        tmp_file.write(response.content)
        tmp_file.close()
        self.logger.info(f"Modelo descargado a archivo temporal {tmp_file.name}")
        return tmp_file.name
    
    def _load_model(self):
        """Cargar modelo y tokenizer"""
        try:
            # Detectar si model_path es URL o ruta local
            if self.model_path.startswith("http"):
                # Descargar modelo
                self.temp_model_file = self._download_model(self.model_path)
                load_path = self.temp_model_file
            else:
                load_path = self.model_path
            
            # Cargar modelo desde archivo local
            if os.path.exists(load_path):
                with open(load_path, 'rb') as f:
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
                self.logger.warning(f"No existe el archivo modelo: {load_path}")
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
        
        cleaned_text = text.strip().lower()
        
        inputs = self.tokenizer(
            cleaned_text,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.sigmoid(outputs.logits).cpu().numpy()[0]
        
        threshold = 0.5
        predictions = (probabilities > threshold).astype(int)
        
        labels = [
            'IsToxic', 'IsAbusive', 'IsThreat', 'IsProvocative', 
            'IsObscene', 'IsHatespeech', 'IsRacist', 'IsNationalist',
            'IsSexist', 'IsHomophobic', 'IsReligiousHate', 'IsRadicalism'
        ]
        
        labels = labels[:len(probabilities)]
        
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
        return {
            'model_type': 'DistilBERT',
            'version': '1.0.0',
            'device': str(self.device),
            'metrics': getattr(self, 'model_metrics', {}),
            'model_loaded': getattr(self, 'model', None) is not None,
            'tokenizer_loaded': getattr(self, 'tokenizer', None) is not None
        }
