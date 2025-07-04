import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mlflow
import mlflow.transformers
import pickle
from datetime import datetime
import pandas as pd

def save_current_best_model():
    """Guardar el modelo DistilBERT actual como backup"""
    
    print("💾 GUARDANDO MODELO DISTILBERT ACTUAL")
    print("="*50)
    
    # ✅ CORREGIR RUTA DE MLFLOW
    mlflow.set_tracking_uri("file:mlruns")  # Sin ../
    
    # BUSCAR EN TODOS LOS EXPERIMENTOS
    experiments = mlflow.search_experiments()
    print("🔍 Buscando experimentos...")
    
    distilbert_runs = []
    
    for exp in experiments:
        print(f"📊 Revisando experimento: '{exp.name}'")
        
        try:
            runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
            
            # Buscar runs con DistilBERT
            if 'params.model_name' in runs.columns:
                distilbert_in_exp = runs[runs['params.model_name'] == 'distilbert-base-uncased']
                if len(distilbert_in_exp) > 0:
                    print(f"   ✅ Encontrados {len(distilbert_in_exp)} runs de DistilBERT")
                    for _, run in distilbert_in_exp.iterrows():
                        run_data = run.to_dict()
                        run_data['experiment_name'] = exp.name
                        distilbert_runs.append(run_data)
                else:
                    print(f"   ➖ No hay DistilBERT en este experimento")
            else:
                print(f"   ➖ Sin información de modelo")
                
        except Exception as e:
            print(f"   ❌ Error leyendo experimento: {e}")
    
    if len(distilbert_runs) == 0:
        print("\n❌ NO SE ENCONTRARON RUNS DE DISTILBERT")
        return
    
    print(f"\n🎉 ENCONTRADOS {len(distilbert_runs)} RUNS DE DISTILBERT!")
    
    # Convertir a DataFrame y encontrar el mejor
    runs_df = pd.DataFrame(distilbert_runs)
    
    # Ordenar por Jaccard Score (o F1 Macro si no hay Jaccard)
    if 'metrics.jaccard_score' in runs_df.columns:
    # Ordenar por Jaccard Score para encontrar el mejor
        best_run = runs_df.loc[runs_df['metrics.jaccard_score'].idxmax()]
        best_metric = f"jaccard_score ({best_run['metrics.jaccard_score']:.4f})"
    elif 'metrics.f1_macro' in runs_df.columns:
        best_run = runs_df.loc[runs_df['metrics.f1_macro'].idxmax()]
        best_metric = 'f1_macro'
    else:
        best_run = runs_df.iloc[0]
        best_metric = 'latest'
    
    print(f"\n🎯 MEJOR RUN DE DISTILBERT ENCONTRADO:")
    print(f"   Experimento: {best_run['experiment_name']}")
    print(f"   Run ID: {best_run['run_id']}")
    print(f"   Criterio: {best_metric}")
    
    # Mostrar métricas disponibles
    for col in runs_df.columns:
        if col.startswith('metrics.') and pd.notna(best_run[col]):
            metric_name = col.replace('metrics.', '')
            print(f"   {metric_name}: {best_run[col]:.4f}")
    
    # Crear carpeta para backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"models/backup_distilbert_{timestamp}"  # Sin ../
    os.makedirs(backup_dir, exist_ok=True)
    
    run_id = best_run['run_id']
    
    try:
        # Buscar artefactos disponibles
        client = mlflow.tracking.MlflowClient()
        artifacts = client.list_artifacts(run_id)
        
        print(f"\n📁 Artefactos disponibles en el run:")
        for artifact in artifacts:
            print(f"   📄 {artifact.path}")
        
        # Intentar diferentes rutas de modelo
        model_paths_to_try = [
            f"runs:/{run_id}/transformer_model",
            f"runs:/{run_id}/model", 
            f"runs:/{run_id}/distilbert_model",
            f"runs:/{run_id}/pytorch_model"
        ]
        
        model_saved = False
        for model_uri in model_paths_to_try:
            try:
                print(f"\n🔄 Intentando cargar desde: {model_uri}")
                model = mlflow.transformers.load_model(model_uri)
                
                # Guardar como pickle
                model_path = f"{backup_dir}/distilbert_model.pkl"
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)
                
                print(f"✅ Modelo cargado y guardado exitosamente!")
                model_saved = True
                break
                
            except Exception as e:
                print(f"❌ Falló: {e}")
                continue
        
        if not model_saved:
            print("⚠️ No se pudo cargar el modelo, pero guardando métricas...")
        
        # Guardar métricas (siempre funciona)
        metrics = {}
        for col in runs_df.columns:
            if col.startswith('metrics.') and pd.notna(best_run[col]):
                metric_name = col.replace('metrics.', '')
                metrics[metric_name] = best_run[col]
        
        # Agregar info adicional
        metrics.update({
            "run_id": run_id,
            "experiment_name": best_run['experiment_name'],
            "timestamp": timestamp,
            "model_saved": model_saved
        })
        
        metrics_path = f"{backup_dir}/metrics.pkl"
        with open(metrics_path, 'wb') as f:
            pickle.dump(metrics, f)
        
        # Guardar resumen legible
        summary = f"""
MODELO DISTILBERT BACKUP - {timestamp}
=====================================
🎯 Información:
   Experimento: {best_run['experiment_name']}
   Run ID: {run_id}
   Modelo guardado: {"SÍ" if model_saved else "NO"}
   
📊 Métricas:
"""
        
        for metric_name, value in metrics.items():
            if isinstance(value, (int, float)) and metric_name not in ['run_id', 'timestamp']:
                summary += f"   {metric_name}: {value:.4f}\n"
        
        summary += f"""
🔧 Configuración:
   Epochs: {best_run.get('params.num_epochs', 'N/A')}
   Batch Size: {best_run.get('params.batch_size', 'N/A')}
   Learning Rate: {best_run.get('params.learning_rate', 'N/A')}

📁 Archivos:
   Modelo: {'distilbert_model.pkl' if model_saved else 'NO GUARDADO'}
   Métricas: metrics.pkl
"""
        
        with open(f"{backup_dir}/README.txt", 'w', encoding='utf-8') as f:
         f.write(summary)
        
        print(f"\n✅ BACKUP COMPLETADO:")
        print(f"📁 Carpeta: {backup_dir}")
        print(f"📄 Modelo: {'✅ Guardado' if model_saved else '❌ No disponible'}")
        print(f"📊 Métricas: ✅ Guardadas")
        print(f"📝 Resumen: ✅ Creado")
        
    except Exception as e:
        print(f"❌ Error durante el backup: {e}")
        print(f"💡 Run ID para debug: {run_id}")

if __name__ == "__main__":
    save_current_best_model()