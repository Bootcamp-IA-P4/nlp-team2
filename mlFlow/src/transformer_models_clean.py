import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mlflow
import mlflow.transformers
import mlflow.pytorch
import pandas as pd
import numpy as np
import torch
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    TrainingArguments, Trainer, EarlyStoppingCallback
)
from datasets import Dataset
from sklearn.metrics import hamming_loss, jaccard_score, f1_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')

class TransformerToxicityTracker:
    """Tracker para modelos transformer con MLflow"""
    
    def __init__(self, experiment_name="toxicity-transformer-experiments"):
        mlflow.set_experiment(experiment_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"🔧 Usando dispositivo: {self.device}")
    
    def prepare_dataset(self, texts, labels, tokenizer, max_length=512):
        """Preparar dataset para transformers"""
        
        # Tokenizar textos
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
    
    def compute_metrics(self, eval_pred):
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
    
    def train_transformer_model(self, X_train, X_test, y_train, y_test, 
                               model_name="distilbert-base-uncased",
                               num_epochs=3, batch_size=16, learning_rate=2e-5):
        """Entrenar modelo transformer con tracking en MLflow"""
        
        run_name = f"{model_name.split('/')[-1]}_epochs{num_epochs}_lr{learning_rate}"
        
        with mlflow.start_run(run_name=run_name):
            try:
                print(f"🚀 Entrenando {model_name}...")
                
                # Log de parámetros
                mlflow.log_param("model_name", model_name)
                mlflow.log_param("num_epochs", num_epochs)
                mlflow.log_param("batch_size", batch_size)
                mlflow.log_param("learning_rate", learning_rate)
                mlflow.log_param("train_samples", len(X_train))
                mlflow.log_param("test_samples", len(X_test))
                mlflow.log_param("num_labels", y_train.shape[1])
                mlflow.log_param("device", str(self.device))
                
                # Cargar tokenizer y modelo
                print(f"   📝 Cargando tokenizer...")
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                
                print(f"   🧠 Cargando modelo...")
                model = AutoModelForSequenceClassification.from_pretrained(
                    model_name,
                    num_labels=y_train.shape[1],
                    problem_type="multi_label_classification"
                )
                model.to(self.device)
                
                # Preparar datasets
                print(f"   📊 Preparando datasets...")
                train_dataset = self.prepare_dataset(X_train, y_train, tokenizer)
                test_dataset = self.prepare_dataset(X_test, y_test, tokenizer)
                
                # Configurar entrenamiento - CORREGIDO
                training_args = TrainingArguments(
                    output_dir=f'./results_{model_name.split("/")[-1]}',
                    num_train_epochs=num_epochs,
                    per_device_train_batch_size=batch_size,
                    per_device_eval_batch_size=batch_size,
                    learning_rate=learning_rate,
                    warmup_steps=100,  # Reducido para dataset pequeño
                    weight_decay=0.01,
                    logging_dir='./logs',
                    logging_steps=10,
                    eval_strategy="epoch",  # CORREGIDO: era evaluation_strategy
                    save_strategy="epoch",
                    load_best_model_at_end=True,
                    metric_for_best_model="f1_macro",
                    greater_is_better=True,
                    report_to=None,  # Desactivar wandb/tensorboard
                    dataloader_num_workers=0,  # Evitar problemas de multiprocessing
                    save_total_limit=2,  # Solo guardar los 2 mejores checkpoints
                    remove_unused_columns=False  # Mantener columnas originales
                )
                
                # Crear trainer
                trainer = Trainer(
                    model=model,
                    args=training_args,
                    train_dataset=train_dataset,
                    eval_dataset=test_dataset,
                    compute_metrics=self.compute_metrics,
                    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
                )
                
                # Entrenar
                print(f"   🏃‍♂️ Iniciando entrenamiento...")
                trainer.train()
                
                # Evaluación final
                print(f"   📊 Evaluación final...")
                eval_results = trainer.evaluate()
                
                # Log de métricas finales
                for key, value in eval_results.items():
                    if key.startswith('eval_'):
                        metric_name = key.replace('eval_', '')
                        mlflow.log_metric(metric_name, value)
                
                # Guardar modelo en MLflow
                print(f"   💾 Guardando modelo en MLflow...")
                mlflow.transformers.log_model(
                    transformers_model={
                        "model": model,
                        "tokenizer": tokenizer
                    },
                    artifact_path="transformer_model",
                    registered_model_name=f"toxicity_{model_name.split('/')[-1]}"
                )
                
                print(f"   ✅ Entrenamiento completado!")
                print(f"      F1 Macro: {eval_results.get('eval_f1_macro', 0):.4f}")
                print(f"      Jaccard Score: {eval_results.get('eval_jaccard_score', 0):.4f}")
                print(f"      Hamming Loss: {eval_results.get('eval_hamming_loss', 0):.4f}")
                
                return model, tokenizer, eval_results
                
            except Exception as e:
                print(f"   ❌ Error en entrenamiento: {str(e)}")
                mlflow.log_param("error", str(e))
                mlflow.log_metric("training_success", 0)
                raise e

def run_transformer_experiments():
    """Ejecutar experimentos con diferentes modelos transformer"""
    
    # Cargar datos
    print("📊 Cargando datos para transformers...")
    from src.data_preprocessing import load_and_preprocess_data, prepare_train_test_split
    
    df, toxicity_columns = load_and_preprocess_data('data/raw/hatespeech.csv')
    X_train, X_test, y_train, y_test = prepare_train_test_split(df, toxicity_columns)
    
    print(f"📈 Datos preparados para transformers:")
    print(f"   Entrenamiento: {len(X_train)} muestras")
    print(f"   Prueba: {len(X_test)} muestras")
    print(f"   Etiquetas: {len(toxicity_columns)} columnas")
    
    # Inicializar tracker
    tracker = TransformerToxicityTracker()
    
    # Configuraciones de modelos transformer (empezar con modelo más liviano)
    transformer_configs = [
        {
        "model_name": "distilbert-base-uncased",
        "num_epochs": 2,
        "batch_size": 8,
        "learning_rate": 2e-5
    },
    # NUEVAS CONFIGURACIONES OPTIMIZADAS
    {
        "model_name": "distilbert-base-uncased",
        "num_epochs": 4,  # Más epochs
        "batch_size": 8,
        "learning_rate": 3e-5  # Learning rate más alto
    },
    {
        "model_name": "distilbert-base-uncased", 
        "num_epochs": 3,
        "batch_size": 16,  # Batch más grande
        "learning_rate": 2e-5
    },
    # BERT BASE (más potente)
    {
        "model_name": "bert-base-uncased",
        "num_epochs": 3,
        "batch_size": 4,  # Batch pequeño por memoria
        "learning_rate": 2e-5
    },
    # RoBERTa (estado del arte)
    {
        "model_name": "roberta-base",
        "num_epochs": 3,
        "batch_size": 4,
        "learning_rate": 1e-5  # LR más conservador para RoBERTa
    }
]
    
    results = []
    successful_experiments = 0
    
    print(f"\n🚀 Iniciando {len(transformer_configs)} experimentos transformer...")
    
    for i, config in enumerate(transformer_configs, 1):
        print(f"\n--- Experimento Transformer {i}/{len(transformer_configs)} ---")
        print(f"Modelo: {config['model_name']}")
        print(f"Épocas: {config['num_epochs']}")
        print(f"Batch size: {config['batch_size']}")
        print(f"Learning rate: {config['learning_rate']}")
        
        try:
            model, tokenizer, metrics = tracker.train_transformer_model(
                X_train, X_test, y_train, y_test,
                **config
            )
            
            results.append({
                "config": config,
                "metrics": metrics,
                "success": True
            })
            successful_experiments += 1
            
        except Exception as e:
            print(f"   ❌ Experimento transformer {i} falló: {str(e)}")
            results.append({
                "config": config,
                "metrics": None,
                "success": False,
                "error": str(e)
            })
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN TRANSFORMERS ({successful_experiments}/{len(transformer_configs)} exitosos):")
    print("="*70)
    
    successful_results = [r for r in results if r["success"]]
    if successful_results:
        for i, result in enumerate(successful_results, 1):
            config = result["config"]
            metrics = result["metrics"]
            print(f"🤖 Transformer #{i}: {config['model_name']}")
            print(f"   F1 Macro: {metrics.get('eval_f1_macro', 0):.4f}")
            print(f"   Jaccard Score: {metrics.get('eval_jaccard_score', 0):.4f}")
            print(f"   Hamming Loss: {metrics.get('eval_hamming_loss', 0):.4f}")
            print()
    
    print(f"🔍 Revisa los resultados en MLflow UI: mlflow ui")

if __name__ == "__main__":
    # Verificar dependencias
    try:
        import transformers
        import datasets
        print("✅ Dependencias transformer disponibles")
        run_transformer_experiments()
    except ImportError as e:
        print(f"❌ Faltan dependencias: {e}")
        print("💡 Instala con: pip install transformers datasets torch")
