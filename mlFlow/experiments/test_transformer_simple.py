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
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    TrainingArguments, Trainer
)
from datasets import Dataset
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

if __name__ == "__main__":
    run_simple_transformer_test()
