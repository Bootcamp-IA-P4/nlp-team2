import pandas as pd
import numpy as np
import re
import emoji
import string
from sklearn.model_selection import train_test_split

def clean_text(text):
    """Función de limpieza de texto"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    text = emoji.demojize(text, delimiters=(" ", " "))
    text = re.sub(r'[^\w\s.!?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def load_and_preprocess_data(file_path):
    """Cargar y preprocesar datos"""
    df = pd.read_csv(file_path)
    df['Text_Clean'] = df['Text'].apply(clean_text)
    
    # Definir TODAS las columnas de toxicidad
    all_toxicity_columns = [
        'IsToxic', 'IsAbusive', 'IsThreat', 'IsProvocative', 
        'IsObscene', 'IsHatespeech', 'IsRacist', 'IsNationalist', 
        'IsSexist', 'IsHomophobic', 'IsReligiousHate', 'IsRadicalism'
    ]
    
    # Filtrar columnas que tienen suficientes ejemplos (al menos 10 casos positivos y negativos)
    valid_toxicity_columns = []
    
    print("🔍 Analizando distribución de clases...")
    for col in all_toxicity_columns:
        if col in df.columns:
            positive_count = df[col].sum()
            negative_count = len(df) - positive_count
            
            if positive_count >= 10 and negative_count >= 10:
                valid_toxicity_columns.append(col)
                print(f"  ✅ {col}: {positive_count} positivos, {negative_count} negativos")
            else:
                print(f"  ❌ {col}: {positive_count} positivos, {negative_count} negativos (EXCLUIDO)")
    
    print(f"\n📊 Columnas válidas para ML: {len(valid_toxicity_columns)}")
    print(f"   {valid_toxicity_columns}")
    
    return df, valid_toxicity_columns

def prepare_train_test_split(df, toxicity_columns, test_size=0.2):
    """Preparar división de datos"""
    X = df['Text_Clean'].values
    y = df[toxicity_columns].values.astype(float)
    
    # Verificar que no hay columnas problemáticas
    print(f"\n🎯 Verificación final de datos:")
    print(f"   Forma de X: {X.shape}")
    print(f"   Forma de y: {y.shape}")
    print(f"   Rango de y: {y.min()} - {y.max()}")
    
    # Verificar que cada columna tiene al menos 2 clases
    for i, col in enumerate(toxicity_columns):
        unique_values = np.unique(y[:, i])
        print(f"   {col}: {len(unique_values)} clases únicas: {unique_values}")
    
    return train_test_split(X, y, test_size=test_size, random_state=42, stratify=y[:, 0])