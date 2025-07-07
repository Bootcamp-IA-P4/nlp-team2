import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mlflow
import mlflow.transformers
import pandas as pd
import numpy as np
import torch
from datetime import datetime

class ToxicityPredictor:
    def __init__(self, model_uri=None):
        """Inicializar predictor con el mejor modelo"""
        mlflow.set_tracking_uri("file:mlruns")
        
        if model_uri is None:
            # Buscar el mejor modelo automáticamente
            model_uri = self.find_best_model()
        
        print(f"🔄 Cargando modelo desde: {model_uri}")
        
        try:
            # Cargar modelo completo desde MLflow
            self.model_pipeline = mlflow.transformers.load_model(model_uri)
            self.tokenizer = self.model_pipeline['tokenizer']
            self.model = self.model_pipeline['model']
            
            # Configurar dispositivo
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            self.model.eval()
            
            print(f"✅ Modelo cargado exitosamente en {self.device}")
            
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise
    
    def find_best_model(self):
        """Encontrar el mejor modelo registrado"""
        try:
            # Buscar el mejor run por Jaccard Score
            runs = mlflow.search_runs(
                experiment_ids=[mlflow.get_experiment_by_name("toxicity-transformer-experiments").experiment_id],
                order_by=["metrics.jaccard_score DESC"],
                max_results=1
            )
            
            if len(runs) > 0:
                best_run_id = runs.iloc[0].run_id
                model_uri = f"runs:/{best_run_id}/transformer_model"
                print(f"🏆 Mejor modelo encontrado: {best_run_id}")
                print(f"   Jaccard Score: {runs.iloc[0]['metrics.jaccard_score']:.4f}")
                return model_uri
            else:
                raise Exception("No se encontraron modelos entrenados")
                
        except Exception as e:
            print(f"❌ Error buscando modelo: {e}")
            # Fallback: usar un run específico si sabes el ID
            return "runs:/YOUR_RUN_ID/transformer_model"
    
    def predict_single_comment(self, text, show_details=True):
        """Predecir toxicidad para un solo comentario"""
        
        # Preprocesar texto (mismo que en entrenamiento)
        from src.data_preprocessing import clean_text
        cleaned_text = clean_text(text)
        
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
        
        # Definir etiquetas (mismo orden que en entrenamiento)
        labels = [
            'IsToxic', 'IsAbusive', 'IsThreat', 'IsProvocative', 
            'IsObscene', 'IsHatespeech', 'IsRacist', 'IsNationalist',
            'IsSexist', 'IsHomophobic', 'IsReligiousHate', 'IsRadicalism'
        ]
        
        # Crear resultado
        result = {
            'text_original': text,
            'text_cleaned': cleaned_text,
            'is_toxic_overall': bool(predictions[0]),  # IsToxic
            'confidence_toxic': float(probabilities[0]),
            'categories': {},
            'all_predictions': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Detalles por categoría
        for i, label in enumerate(labels):
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
        
        print(f"\n📊 TODAS LAS PREDICCIONES:")
        for label, pred_data in result['all_predictions'].items():
            status = "✅" if pred_data['predicted'] else "❌"
            print(f"   {status} {label}: {pred_data['confidence']:.3f}")

def test_model_with_examples():
    """Probar modelo con comentarios de ejemplo"""
    
    print("🧪 INICIANDO PRUEBAS DEL MODELO DE TOXICIDAD")
    print("="*60)
    
    # Inicializar predictor
    try:
        predictor = ToxicityPredictor()
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
        
        # Comentarios con lenguaje técnico
        "The algorithm used here has some flaws",
        "Your analysis lacks proper statistical support",
        "This methodology is questionable"
    ]
    
    print(f"\n🎯 Probando {len(test_comments)} comentarios de ejemplo...\n")
    
    # Predecir individualmente con detalles
    for i, comment in enumerate(test_comments, 1):
        print(f"\n{'🧪 PRUEBA ' + str(i):-^60}")
        result = predictor.predict_single_comment(comment)
    
    # Resumen final simple
    print(f"\n{'📊 RESUMEN FINAL':-^60}")
    print(f"✅ Análisis completado para {len(test_comments)} comentarios")
    print(f"📝 Revisa los resultados detallados arriba")
    
    # Conteo rápido
    toxic_count = 0
    for comment in test_comments:
        result = predictor.predict_single_comment(comment, show_details=False)
        if result['is_toxic_overall']:
            toxic_count += 1
    
    print(f"\n📈 ESTADÍSTICAS RÁPIDAS:")
    print(f"   Total comentarios: {len(test_comments)}")
    print(f"   Comentarios tóxicos: {toxic_count}")
    print(f"   Comentarios no tóxicos: {len(test_comments) - toxic_count}")
    print(f"   Tasa de toxicidad: {toxic_count/len(test_comments)*100:.1f}%")

def test_custom_comments():
    """Función para probar comentarios personalizados"""
    
    print("🎯 MODO PRUEBA PERSONALIZADA")
    print("="*60)
    
    try:
        predictor = ToxicityPredictor()
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
        
        # Analizar comentario
        result = predictor.predict_single_comment(comment)

if __name__ == "__main__":
    print("🚀 SELECTOR DE MODO DE PRUEBA")
    print("="*40)
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