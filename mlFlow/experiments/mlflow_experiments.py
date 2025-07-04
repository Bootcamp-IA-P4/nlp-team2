import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_preprocessing import load_and_preprocess_data, prepare_train_test_split
import mlflow
import mlflow.sklearn
import mlflow.pytorch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import hamming_loss, jaccard_score, classification_report, f1_score
import numpy as np

class MLflowModelTracker:
    def __init__(self, experiment_name="toxicity-detection"):
        mlflow.set_experiment(experiment_name)
        
    def train_sklearn_model(self, X_train, X_test, y_train, y_test, 
                           model_type="logistic", **model_params):
        """Entrenar modelo de sklearn con tracking"""
        
        with mlflow.start_run(run_name=f"{model_type}_model"):
            try:
                # Vectorización TF-IDF
                print(f"   🔤 Vectorizando texto...")
                vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
                X_train_vec = vectorizer.fit_transform(X_train)
                X_test_vec = vectorizer.transform(X_test)
                
                print(f"   📊 Forma de vectorización: {X_train_vec.shape}")
                
                # Seleccionar modelo base
                if model_type == "logistic":
                    base_model = LogisticRegression(random_state=42, **model_params)
                elif model_type == "random_forest":
                    base_model = RandomForestClassifier(random_state=42, **model_params)
                elif model_type == "svm":
                    base_model = SVC(probability=True, random_state=42, **model_params)
                
                # Modelo multi-output
                print(f"   🤖 Entrenando modelo {model_type}...")
                model = MultiOutputClassifier(base_model)
                
                # Entrenar
                model.fit(X_train_vec, y_train)
                
                # Predicciones
                print(f"   🎯 Realizando predicciones...")
                y_pred_probs = model.predict_proba(X_test_vec)
                
                # Para multi-output, necesitamos extraer las probabilidades de clase positiva
                y_pred_probs_positive = np.array([pred[:, 1] for pred in y_pred_probs]).T
                y_pred = (y_pred_probs_positive > 0.5).astype(int)
                
                # Métricas
                hamming = hamming_loss(y_test, y_pred)
                jaccard = jaccard_score(y_test, y_pred, average='macro', zero_division=0)
                f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
                f1_micro = f1_score(y_test, y_pred, average='micro', zero_division=0)
                
                # Log de parámetros y métricas
                mlflow.log_params(model_params)
                mlflow.log_param("model_type", model_type)
                mlflow.log_param("vectorizer_max_features", 10000)
                mlflow.log_param("train_samples", len(X_train))
                mlflow.log_param("test_samples", len(X_test))
                mlflow.log_param("num_features", X_train_vec.shape[1])
                mlflow.log_param("num_labels", y_train.shape[1])
                
                mlflow.log_metric("hamming_loss", hamming)
                mlflow.log_metric("jaccard_score", jaccard)
                mlflow.log_metric("f1_macro", f1_macro)
                mlflow.log_metric("f1_micro", f1_micro)
                
                # Guardar modelo
                mlflow.sklearn.log_model(model, "model")
                mlflow.sklearn.log_model(vectorizer, "vectorizer")
                
                print(f"   ✅ {model_type} completado!")
                print(f"      Hamming Loss: {hamming:.4f}")
                print(f"      Jaccard Score: {jaccard:.4f}")
                print(f"      F1 Macro: {f1_macro:.4f}")
                
                return model, vectorizer, {
                    "hamming_loss": hamming, 
                    "jaccard_score": jaccard,
                    "f1_macro": f1_macro,
                    "f1_micro": f1_micro
                }
                
            except Exception as e:
                print(f"   ❌ Error en {model_type}: {str(e)}")
                mlflow.log_param("error", str(e))
                mlflow.log_metric("training_success", 0)
                raise e

def run_experiments():
    """Ejecutar experimentos con diferentes modelos"""
    
    # Cargar datos
    print("📊 Cargando datos...")
    df, toxicity_columns = load_and_preprocess_data('data/raw/hatespeech.csv')
    X_train, X_test, y_train, y_test = prepare_train_test_split(df, toxicity_columns)
    
    print(f"\nDatos preparados:")
    print(f"  Entrenamiento: {len(X_train)} muestras")
    print(f"  Prueba: {len(X_test)} muestras")
    print(f"  Etiquetas: {len(toxicity_columns)} columnas")
    
    # Inicializar tracker
    tracker = MLflowModelTracker("toxicity-detection-experiments")
    
    # Configuraciones de modelos a probar (empezar con modelos más simples)
    model_configs = [
        {
            "model_type": "logistic",
            "params": {"max_iter": 1000, "C": 1.0, "solver": "liblinear"}
        },
        {
            "model_type": "logistic", 
            "params": {"max_iter": 1000, "C": 0.1, "solver": "liblinear"}
        },
        {
            "model_type": "random_forest",
            "params": {"n_estimators": 50, "max_depth": 10, "n_jobs": -1}
        },
        {
            "model_type": "random_forest",
            "params": {"n_estimators": 100, "max_depth": 15, "n_jobs": -1}
        }
    ]
    
    results = []
    successful_experiments = 0
    
    print(f"\n🚀 Iniciando {len(model_configs)} experimentos...")
    
    for i, config in enumerate(model_configs, 1):
        print(f"\n--- Experimento {i}/{len(model_configs)} ---")
        print(f"Modelo: {config['model_type']}")
        print(f"Parámetros: {config['params']}")
        
        try:
            model, vectorizer, metrics = tracker.train_sklearn_model(
                X_train, X_test, y_train, y_test,
                model_type=config["model_type"],
                **config["params"]
            )
            
            results.append({
                "config": config,
                "metrics": metrics,
                "success": True
            })
            successful_experiments += 1
            
        except Exception as e:
            print(f"   ❌ Experimento {i} falló: {str(e)}")
            results.append({
                "config": config,
                "metrics": None,
                "success": False,
                "error": str(e)
            })
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DE RESULTADOS ({successful_experiments}/{len(model_configs)} exitosos):")
    print("="*70)
    
    successful_results = [r for r in results if r["success"]]
    if successful_results:
        # Ordenar por jaccard score
        successful_results.sort(key=lambda x: x["metrics"]["jaccard_score"], reverse=True)
        
        for i, result in enumerate(successful_results, 1):
            config = result["config"]
            metrics = result["metrics"]
            print(f"🏆 Ranking #{i}: {config['model_type']}")
            print(f"   Jaccard Score: {metrics['jaccard_score']:.4f}")
            print(f"   Hamming Loss: {metrics['hamming_loss']:.4f}")
            print(f"   F1 Macro: {metrics['f1_macro']:.4f}")
            print(f"   Parámetros: {config['params']}")
            print()
    
    # Mostrar experimentos fallidos
    failed_results = [r for r in results if not r["success"]]
    if failed_results:
        print("❌ EXPERIMENTOS FALLIDOS:")
        for result in failed_results:
            config = result["config"]
            print(f"   {config['model_type']}: {result['error']}")
    
    print(f"\n🎯 CONCLUSIÓN:")
    print(f"   ✅ Experimentos exitosos: {successful_experiments}")
    print(f"   ❌ Experimentos fallidos: {len(failed_results)}")
    if successful_results:
        best = successful_results[0]
        print(f"   🏆 Mejor modelo: {best['config']['model_type']} (Jaccard: {best['metrics']['jaccard_score']:.4f})")
    
    print(f"\n🔍 Para ver detalles ejecuta: mlflow ui")

def run_all_experiments():
    """Ejecutar todos los tipos de experimentos"""
    
    print("🚀 INICIANDO EXPERIMENTOS COMPLETOS")
    print("="*50)
    
    # 1. Experimentos tradicionales
    print("\n1️⃣ Ejecutando experimentos tradicionales...")
    run_experiments()
    
    # 2. Experimentos transformer (si está disponible)
    try:
        from src.transformer_models import run_transformer_experiments
        print("\n2️⃣ Ejecutando experimentos transformer...")
        run_transformer_experiments()
    except ImportError as e:
        print(f"⚠️ Transformers no disponibles: {e}")
    except Exception as e:
        print(f"❌ Error en transformers: {e}")
    
    print("\n✅ TODOS LOS EXPERIMENTOS COMPLETADOS")
    print("🔍 Ejecuta 'mlflow ui' para ver los resultados")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        run_all_experiments()
    else:
        run_experiments()