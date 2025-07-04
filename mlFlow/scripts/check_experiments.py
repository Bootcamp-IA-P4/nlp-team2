import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mlflow

# Configurar MLflow
mlflow.set_tracking_uri("file:../mlruns")

# Listar todos los experimentos
experiments = mlflow.search_experiments()
print("🔍 EXPERIMENTOS DISPONIBLES:")
print("="*50)

for exp in experiments:
    print(f"📊 Nombre: '{exp.name}' (ID: {exp.experiment_id})")
    
    # Ver runs en cada experimento
    runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
    print(f"   📈 Runs: {len(runs)}")
    
    if len(runs) > 0:
        # Ver tipos de modelos
        model_types = runs['params.model_name'].dropna().unique() if 'params.model_name' in runs.columns else []
        if len(model_types) > 0:
            print(f"   🤖 Modelos: {list(model_types)}")
    print()