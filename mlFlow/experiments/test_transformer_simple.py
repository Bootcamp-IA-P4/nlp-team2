"""
Script simple para probar modelos transformer con el dataset de toxicidad
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mlflow
import mlflow.transformers
import pandas as pd
import numpy as np
import torch
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import hamming_loss, jaccard_score, f1_score
import warnings
warnings.filterwarnings('ignore')

def prepare_simple_dataset(texts, labels, tokenizer, max_length=128):
    """Preparar dataset simple para transformers"""
    
    # Tokenizar textos con longitud reducida
    encodings = tokenizer(
        list(texts), 
        truncation=True, 
        padding=True, 
        max_length=max_length,
        return_tensors='pt'
    )
    
    # Crear dataset
    dataset = Dataset.from_dict({
        'input_ids': encodings['input_ids'],
        'attention_mask': encodings['attention_mask'],
        'labels': torch.tensor(labels, dtype=torch.float)
    })
    
    return dataset

def compute_metrics(eval_pred):
    """Calcular métricas para evaluación"""
    predictions, labels = eval_pred
    
    # Convertir probabilidades a predicciones binarias
    predictions = torch.sigmoid(torch.tensor(predictions))
    predictions = (predictions > 0.5).float().numpy()
    
    # Calcular métricas
    hamming = hamming_loss(labels, predictions)
    jaccard = jaccard_score(labels, predictions, average='macro', zero_division=0)
    f1_macro = f1_score(labels, predictions, average='macro', zero_division=0)
    f1_micro = f1_score(labels, predictions, average='micro', zero_division=0)
    
    return {
        'hamming_loss': hamming,
        'jaccard_score': jaccard,
        'f1_macro': f1_macro,
        'f1_micro': f1_micro
    }

def run_simple_transformer_test():
    """Ejecutar prueba simple con DistilBERT"""
    
    # Importar funciones de preprocesamiento
    from src.data_preprocessing import load_and_preprocess_data, prepare_train_test_split
    
    print("🚀 INICIANDO PRUEBA SIMPLE TRANSFORMER")
    print("="*50)
    
    # Configurar MLflow
    mlflow.set_experiment("transformer-simple-test")
    
    # Cargar datos
    print("📊 Cargando datos...")
    df, toxicity_columns = load_and_preprocess_data('data/raw/youtoxic_english_1000.csv')
    X_train, X_test, y_train, y_test = prepare_train_test_split(df, toxicity_columns)
    
    print(f"   ✅ Datos cargados: {len(X_train)} train, {len(X_test)} test")
    print(f"   ✅ Columnas de toxicidad: {len(toxicity_columns)} -> {toxicity_columns}")
    
    # Usar solo un subset pequeño para la prueba
    subset_size = 100
    X_train_small = X_train[:subset_size]
    y_train_small = y_train[:subset_size]
    X_test_small = X_test[:50]
    y_test_small = y_test[:50]
    
    print(f"   🔄 Usando subset reducido: {len(X_train_small)} train, {len(X_test_small)} test")
    
    # Configurar dispositivo
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"   🔧 Dispositivo: {device}")
    
    with mlflow.start_run(run_name="distilbert_simple_test"):
        
        # Log de parámetros
        mlflow.log_param("model_name", "distilbert-base-uncased")
        mlflow.log_param("num_epochs", 1)
        mlflow.log_param("batch_size", 8)
        mlflow.log_param("learning_rate", 2e-5)
        mlflow.log_param("train_samples", len(X_train_small))
        mlflow.log_param("test_samples", len(X_test_small))
        mlflow.log_param("num_labels", y_train_small.shape[1])
        mlflow.log_param("max_length", 128)
        
        # Cargar tokenizer y modelo
        print("📝 Cargando DistilBERT...")
        model_name = "distilbert-base-uncased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=y_train_small.shape[1],
            problem_type="multi_label_classification"
        )
        model.to(device)
        
        # Preparar datasets
        print("📊 Preparando datasets...")
        train_dataset = prepare_simple_dataset(X_train_small, y_train_small, tokenizer)
        test_dataset = prepare_simple_dataset(X_test_small, y_test_small, tokenizer)
        
        # Configurar entrenamiento (muy simple)
        training_args = TrainingArguments(
            output_dir='./results_simple_test',
            num_train_epochs=1,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            learning_rate=2e-5,
            logging_steps=10,
            eval_strategy="epoch",  # Cambiado de evaluation_strategy
            save_strategy="no",  # No guardar checkpoints
            report_to=None,  # Desactivar wandb/tensorboard
            dataloader_num_workers=0,  # Evitar problemas de multiprocessing
            remove_unused_columns=False
        )
        
        # Crear trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
            compute_metrics=compute_metrics
        )
        
        # Entrenar
        print("🏃‍♂️ Entrenando modelo...")
        trainer.train()
        
        # Evaluación final
        print("📊 Evaluación final...")
        eval_results = trainer.evaluate()
        
        # Log de métricas finales
        for key, value in eval_results.items():
            if key.startswith('eval_'):
                metric_name = key.replace('eval_', '')
                mlflow.log_metric(metric_name, value)
        
        # Guardar modelo
        mlflow.transformers.log_model(
            transformers_model={
                "model": model,
                "tokenizer": tokenizer
            },
            artifact_path="distilbert_model"
        )
        
        print("\n✅ PRUEBA COMPLETADA!")
        print("="*50)
        print(f"F1 Macro: {eval_results.get('eval_f1_macro', 0):.4f}")
        print(f"F1 Micro: {eval_results.get('eval_f1_micro', 0):.4f}")
        print(f"Jaccard Score: {eval_results.get('eval_jaccard_score', 0):.4f}")
        print(f"Hamming Loss: {eval_results.get('eval_hamming_loss', 0):.4f}")
        
        return eval_results

class ToxicityPredictor:
    def __init__(self, model_uri=None):
        """Inicializar predictor con el mejor modelo"""
        mlflow.set_tracking_uri("file:mlruns")
        
        if model_uri is None:
            model_uri = self.find_best_model()
        
        print(f"🔄 Cargando modelo desde: {model_uri}")
        
        try:
            # MÉTODO CORREGIDO: Cargar modelo manualmente
            self.run_id = model_uri.split('/')[1]
            self.load_model_manually()
            
            print(f"✅ Modelo cargado exitosamente en {self.device}")
            
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise
    
    def load_model_manually(self):
        """Cargar modelo manualmente desde artifacts"""
        # Configurar dispositivo
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Obtener información del run
        client = mlflow.tracking.MlflowClient()
        run = client.get_run(self.run_id)
        
        # Obtener parámetros del modelo
        model_name = run.data.params.get('model_name', 'distilbert-base-uncased')
        num_labels = int(run.data.params.get('num_labels', 12))
        
        print(f"   📝 Cargando {model_name} con {num_labels} etiquetas...")
        
        # Cargar tokenizer y modelo desde HuggingFace
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels,
            problem_type="multi_label_classification"
        )
        
        # Intentar cargar los pesos entrenados
        try:
            # Buscar el archivo del modelo en artifacts
            artifacts_uri = f"runs:/{self.run_id}/transformer_model"
            local_path = mlflow.artifacts.download_artifacts(artifacts_uri)
            
            # Buscar archivos .bin o .safetensors
            import glob
            model_files = glob.glob(os.path.join(local_path, "*.bin")) + \
                         glob.glob(os.path.join(local_path, "*.safetensors"))
            
            if model_files:
                print(f"   🔄 Cargando pesos entrenados desde: {model_files[0]}")
                # Cargar los pesos del modelo entrenado
                if model_files[0].endswith('.bin'):
                    state_dict = torch.load(model_files[0], map_location='cpu')
                    self.model.load_state_dict(state_dict)
                
                print(f"   ✅ Pesos entrenados cargados exitosamente")
            else:
                print(f"   ⚠️ No se encontraron pesos entrenados, usando modelo base")
                
        except Exception as e:
            print(f"   ⚠️ No se pudieron cargar pesos entrenados: {e}")
            print(f"   📝 Usando modelo base de HuggingFace")
        
        # Mover al dispositivo y configurar para evaluación
        self.model.to(self.device)
        self.model.eval()
    
    def find_best_model(self):
        """Encontrar el mejor modelo registrado"""
        try:
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
            raise
    
    def predict_single_comment(self, text, show_details=True):
        """Predecir toxicidad para un solo comentario"""
        
        # Preprocesar texto (mismo que en entrenamiento)
        try:
            from src.data_preprocessing import clean_text
            cleaned_text = clean_text(text)
        except:
            # Fallback: limpieza básica
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
        
        # Definir etiquetas (orden estándar)
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
    ]
    
    print(f"\n🎯 Probando {len(test_comments)} comentarios de ejemplo...\n")
    
    # Predecir individualmente con detalles
    for i, comment in enumerate(test_comments, 1):
        print(f"\n{'🧪 PRUEBA ' + str(i):-^60}")
        try:
            result = predictor.predict_single_comment(comment)
        except Exception as e:
            print(f"❌ Error en predicción: {e}")
    
    print(f"\n{'📊 RESUMEN FINAL':-^60}")
    print(f"✅ Análisis completado")

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
        
        try:
            result = predictor.predict_single_comment(comment)
        except Exception as e:
            print(f"❌ Error en predicción: {e}")

if __name__ == "__main__":
    run_simple_transformer_test()
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
