import mlflow
import mlflow.sklearn
import mlflow.pytorch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import hamming_loss, jaccard_score, classification_report
import numpy as np

class MLflowModelTracker:
    def __init__(self, experiment_name="toxicity-detection"):
        mlflow.set_experiment(experiment_name)
        
    def train_sklearn_model(self, X_train, X_test, y_train, y_test, 
                           model_type="logistic", **model_params):
        """Entrenar modelo de sklearn con tracking"""
        
        with mlflow.start_run(run_name=f"{model_type}_model"):
            # Vectorización TF-IDF
            vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
            X_train_vec = vectorizer.fit_transform(X_train)
            X_test_vec = vectorizer.transform(X_test)
            
            # Seleccionar modelo base
            if model_type == "logistic":
                base_model = LogisticRegression(random_state=42, **model_params)
            elif model_type == "random_forest":
                base_model = RandomForestClassifier(random_state=42, **model_params)
            elif model_type == "svm":
                base_model = SVC(probability=True, random_state=42, **model_params)
            
            # Modelo multi-output
            model = MultiOutputClassifier(base_model)
            
            # Entrenar
            model.fit(X_train_vec, y_train)
            
            # Predicciones
            y_pred_probs = model.predict_proba(X_test_vec)
            # Para multi-output, necesitamos extraer las probabilidades de clase positiva
            y_pred_probs_positive = np.array([pred[:, 1] for pred in y_pred_probs]).T
            y_pred = (y_pred_probs_positive > 0.5).astype(int)
            
            # Métricas
            hamming = hamming_loss(y_test, y_pred)
            jaccard = jaccard_score(y_test, y_pred, average='macro')
            
            # Log de parámetros y métricas
            mlflow.log_params(model_params)
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("vectorizer_max_features", 10000)
            
            mlflow.log_metric("hamming_loss", hamming)
            mlflow.log_metric("jaccard_score", jaccard)
            
            # Guardar modelo
            mlflow.sklearn.log_model(model, "model")
            mlflow.sklearn.log_model(vectorizer, "vectorizer")
            
            print(f"✅ {model_type} - Hamming Loss: {hamming:.4f}, Jaccard Score: {jaccard:.4f}")
            
            return model, vectorizer, {"hamming_loss": hamming, "jaccard_score": jaccard}