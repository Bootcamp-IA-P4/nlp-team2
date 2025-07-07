import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
import torch
import numpy as np
from datetime import datetime
from transformers import AutoTokenizer

class ToxicityPredictorFromBackup:
    def __init__(self, backup_folder=None):
        """Inicializar predictor desde backup local"""
        
        if backup_folder is None:
            backup_folder = self.find_latest_backup()
        
        print(f"🔄 Cargando modelo desde backup: {backup_folder}")
        
        try:
            self.load_from_backup(backup_folder)
            print(f"✅ Modelo cargado exitosamente")
            
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise
    
    def find_latest_backup(self):
        """Encontrar el backup más reciente"""
        models_dir = "models"
        if not os.path.exists(models_dir):
            raise Exception("No se encontró la carpeta models/")
        
        # Buscar carpetas de backup
        backup_folders = [
            f for f in os.listdir(models_dir) 
            if f.startswith('backup_distilbert_')
        ]
        
        if not backup_folders:
            raise Exception("No se encontraron backups de DistilBERT")
        
        # Usar el más reciente
        latest_backup = sorted(backup_folders)[-1]
        backup_path = os.path.join(models_dir, latest_backup)
        
        print(f"🎯 Backup más reciente encontrado: {latest_backup}")
        return backup_path
    
    def load_from_backup(self, backup_folder):
        """Cargar modelo desde backup"""
        
        # Cargar métricas para info
        metrics_path = os.path.join(backup_folder, "metrics.pkl")
        if os.path.exists(metrics_path):
            with open(metrics_path, 'rb') as f:
                self.metrics = pickle.load(f)
            
            print(f"   📊 Métricas del modelo:")
            print(f"      F1 Macro: {self.metrics.get('f1_macro', 'N/A'):.4f}")
            print(f"      Jaccard: {self.metrics.get('jaccard_score', 'N/A'):.4f}")
            print(f"      Hamming Loss: {self.metrics.get('hamming_loss', 'N/A'):.4f}")
        
        # Cargar modelo si está disponible
        model_path = os.path.join(backup_folder, "distilbert_model.pkl")
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model_pipeline = pickle.load(f)
                
                # Extraer componentes
                if hasattr(self.model_pipeline, 'model'):
                    self.model = self.model_pipeline.model
                    self.tokenizer = self.model_pipeline.tokenizer
                elif isinstance(self.model_pipeline, dict):
                    self.model = self.model_pipeline['model']
                    self.tokenizer = self.model_pipeline['tokenizer']
                else:
                    # Si es solo el modelo, crear tokenizer por separado
                    self.model = self.model_pipeline
                    self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
                
                print(f"   ✅ Modelo cargado desde backup")
                
            except Exception as e:
                print(f"   ⚠️ Error cargando modelo del backup: {e}")
                # Crear modelo base como fallback
                self.create_base_model()
        else:
            print(f"   ⚠️ No se encontró modelo en backup, creando modelo base")
            self.create_base_model()
        
        # Configurar dispositivo
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if hasattr(self.model, 'to'):
            self.model.to(self.device)
            self.model.eval()
    
    def create_base_model(self):
        """Crear modelo base como fallback"""
        from transformers import AutoModelForSequenceClassification
        
        print(f"   🔄 Creando modelo base DistilBERT...")
        
        self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = AutoModelForSequenceClassification.from_pretrained(
            'distilbert-base-uncased',
            num_labels=12,  # Número de etiquetas de toxicidad
            problem_type="multi_label_classification"
        )
        
        print(f"   ⚠️ NOTA: Usando modelo base sin entrenamiento específico")
    
    def predict_single_comment(self, text, show_details=True):
        """Predecir toxicidad para un solo comentario"""
        
        # Preprocesar texto básico
        cleaned_text = text.lower().strip()
        
        # Tokenizar
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
        
        # Umbral para clasificación binaria
        threshold = 0.5
        predictions = (probabilities > threshold).astype(int)
        
        # Definir etiquetas
        labels = [
            'IsToxic', 'IsAbusive', 'IsThreat', 'IsProvocative', 
            'IsObscene', 'IsHatespeech', 'IsRacist', 'IsNationalist',
            'IsSexist', 'IsHomophobic', 'IsReligiousHate', 'IsRadicalism'
        ]
        
        # Ajustar etiquetas si hay menos predicciones
        labels = labels[:len(probabilities)]
        
        # Crear resultado
        result = {
            'text_original': text,
            'text_cleaned': cleaned_text,
            'is_toxic_overall': bool(predictions[0]) if len(predictions) > 0 else False,
            'confidence_toxic': float(probabilities[0]) if len(probabilities) > 0 else 0.0,
            'categories': {},
            'all_predictions': {},
            'model_metrics': getattr(self, 'metrics', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        # Detalles por categoría
        for i, label in enumerate(labels):
            if i < len(predictions):
                result['all_predictions'][label] = {
                    'predicted': bool(predictions[i]),
                    'confidence': float(probabilities[i])
                }
                
                # Solo categorías detectadas como positivas
                if predictions[i] == 1:
                    result['categories'][label] = float(probabilities[i])
        
        if show_details:
            self.print_prediction_details(result)
        
        return result
    
    def print_prediction_details(self, result):
        """Mostrar detalles de predicción formateados"""
        print(f"\n{'='*60}")
        print(f"📝 ANÁLISIS DE COMENTARIO")
        print(f"{'='*60}")
        print(f"🔤 Original: {result['text_original']}")
        print(f"🧹 Limpio:   {result['text_cleaned']}")
        print(f"\n🎯 RESULTADO PRINCIPAL:")
        
        if result['is_toxic_overall']:
            print(f"   🚨 TÓXICO (confianza: {result['confidence_toxic']:.3f})")
        else:
            print(f"   ✅ NO TÓXICO (confianza: {1-result['confidence_toxic']:.3f})")
        
        if result['categories']:
            print(f"\n🏷️ CATEGORÍAS DETECTADAS:")
            for category, confidence in result['categories'].items():
                print(f"   🔸 {category}: {confidence:.3f}")
        else:
            print(f"\n🏷️ NO SE DETECTARON CATEGORÍAS ESPECÍFICAS")
        
        # Mostrar métricas del modelo
        if 'model_metrics' in result and result['model_metrics']:
            print(f"\n📊 INFORMACIÓN DEL MODELO:")
            metrics = result['model_metrics']
            print(f"   🎯 F1 Macro: {metrics.get('f1_macro', 'N/A')}")
            print(f"   🎯 Jaccard Score: {metrics.get('jaccard_score', 'N/A')}")
            print(f"   🎯 Hamming Loss: {metrics.get('hamming_loss', 'N/A')}")
        
        print(f"\n📊 TODAS LAS PREDICCIONES:")
        for label, pred_data in result['all_predictions'].items():
            status = "✅" if pred_data['predicted'] else "❌"
            print(f"   {status} {label}: {pred_data['confidence']:.3f}")

def test_model_with_examples():
    """Probar modelo con comentarios de ejemplo"""
    
    print("🧪 INICIANDO PRUEBAS DEL MODELO DE TOXICIDAD (DESDE BACKUP)")
    print("="*65)
    
    # Inicializar predictor
    try:
        predictor = ToxicityPredictorFromBackup()
    except Exception as e:
        print(f"❌ No se pudo cargar el modelo: {e}")
        return
    
    # Comentarios de prueba
    test_comments = [
        # Comentarios claramente NO tóxicos
        "This is a great video, thank you for sharing!",
        "I love this community, everyone is so helpful and kind.",
        "Amazing content, please keep it up!",
        
        # Comentarios claramente TÓXICOS
        "You are so stupid, I hate people like you",
        "This is the worst thing I've ever seen, complete garbage",
        "Go kill yourself, nobody likes you",
        
        # Comentarios ambiguos/borderline
        "I disagree with this opinion strongly",
        "This video is not very good in my opinion",
        "I don't think this is the right approach",
    ]
    
    print(f"\n🎯 Probando {len(test_comments)} comentarios de ejemplo...\n")
    
    # Estadísticas
    toxic_count = 0
    
    # Predecir individualmente con detalles
    for i, comment in enumerate(test_comments, 1):
        print(f"\n{'🧪 PRUEBA ' + str(i):-^60}")
        try:
            result = predictor.predict_single_comment(comment)
            if result['is_toxic_overall']:
                toxic_count += 1
        except Exception as e:
            print(f"❌ Error en predicción: {e}")
    
    # Resumen final
    print(f"\n{'📊 RESUMEN FINAL':-^60}")
    print(f"✅ Análisis completado para {len(test_comments)} comentarios")
    print(f"📈 Estadísticas:")
    print(f"   Total: {len(test_comments)}")
    print(f"   Tóxicos: {toxic_count}")
    print(f"   No tóxicos: {len(test_comments) - toxic_count}")
    print(f"   Tasa de toxicidad: {toxic_count/len(test_comments)*100:.1f}%")

def test_custom_comments():
    """Función para probar comentarios personalizados"""
    
    print("🎯 MODO PRUEBA PERSONALIZADA (DESDE BACKUP)")
    print("="*65)
    
    try:
        predictor = ToxicityPredictorFromBackup()
    except Exception as e:
        print(f"❌ No se pudo cargar el modelo: {e}")
        return
    
    print("💡 Escribe comentarios para analizar (escribe 'salir' para terminar)")
    print("-" * 60)
    
    while True:
        comment = input("\n📝 Ingresa un comentario: ").strip()
        
        if comment.lower() in ['salir', 'exit', 'quit', '']:
            print("👋 ¡Hasta luego!")
            break
        
        try:
            result = predictor.predict_single_comment(comment)
        except Exception as e:
            print(f"❌ Error en predicción: {e}")

if __name__ == "__main__":
    print("🚀 SELECTOR DE MODO DE PRUEBA (BACKUP MODEL)")
    print("="*50)
    print("1. 🧪 Probar con comentarios de ejemplo")
    print("2. 🎯 Probar con comentarios personalizados")
    print("3. ❌ Salir")
    
    while True:
        choice = input("\n👉 Selecciona una opción (1-3): ").strip()
        
        if choice == "1":
            test_model_with_examples()
            break
        elif choice == "2":
            test_custom_comments()
            break
        elif choice == "3":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Escribe 1, 2 o 3.")