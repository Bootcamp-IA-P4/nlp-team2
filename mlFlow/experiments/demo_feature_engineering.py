import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas as pd
from feature_engineering import ToxicityFeatureExtractor
from data_preprocessing import load_and_preprocess_data

def demo_feature_engineering():
    """Demostración del nuevo sistema de feature engineering"""
    
    print("🚀 DEMO: FEATURE ENGINEERING AVANZADO PARA TOXICIDAD")
    print("="*60)
    
    # 1. Cargar datos - RUTA CORREGIDA
    print("📊 1. Cargando datos...")
    df, toxicity_columns = load_and_preprocess_data('data/raw/youtoxic_english_1000.csv')
    print(f"   ✅ Datos cargados: {df.shape}")
    
    # 2. Crear extractor de características
    print("\n🔧 2. Inicializando extractor de características...")
    extractor = ToxicityFeatureExtractor(max_features=1000)  # Menos features para demo
    print("   ✅ Extractor inicializado")
    
    # 3. Usar una muestra pequeña para la demo
    sample_df = df.head(100).copy()
    print(f"\n📋 3. Usando muestra de {len(sample_df)} comentarios para demo...")
    
    # 4. Extraer características básicas
    print("\n📏 4. Extrayendo características básicas...")
    basic_features = extractor.add_basic_text_features(sample_df)
    basic_cols = ['text_length', 'word_count', 'avg_word_length', 'exclamation_count', 
                  'caps_ratio', 'special_char_count']
    print("   ✅ Características básicas:")
    print(basic_features[basic_cols].describe())
    
    # 5. Extraer características de sentimiento
    print("\n😊 5. Extrayendo características de sentimiento...")
    sentiment_features = extractor.add_sentiment_features(sample_df)
    sentiment_cols = ['sentiment_compound', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral']
    print("   ✅ Características de sentimiento:")
    print(sentiment_features[sentiment_cols].describe())
    
    # 6. Extraer características de toxicidad
    print("\n💀 6. Extrayendo características específicas de toxicidad...")
    toxicity_features = extractor.add_toxicity_features(sample_df)
    toxicity_cols = ['toxic_word_count', 'toxic_word_ratio', 'all_caps_words', 'toxic_density']
    print("   ✅ Características de toxicidad:")
    print(toxicity_features[toxicity_cols].describe())
    
    # 7. Extraer todas las características
    print("\n🎯 7. Extrayendo TODAS las características...")
    all_features = extractor.extract_all_features(sample_df)
    print(f"   ✅ Dataset final: {all_features.shape}")
    print(f"   📊 Características originales: {sample_df.shape[1]}")
    print(f"   🆕 Nuevas características: {all_features.shape[1] - sample_df.shape[1]}")
    
    # 8. Análisis de características más discriminativas
    print("\n🔍 8. Análisis de características discriminativas...")
    
    # Comparar comentarios tóxicos vs no tóxicos
    toxic_comments = all_features[all_features['IsToxic'] == True]
    non_toxic_comments = all_features[all_features['IsToxic'] == False]
    
    discriminative_features = {}
    for col in ['toxic_word_ratio', 'sentiment_negative', 'caps_ratio', 'exclamation_count']:
        if col in all_features.columns:
            toxic_mean = toxic_comments[col].mean()
            non_toxic_mean = non_toxic_comments[col].mean()
            difference = abs(toxic_mean - non_toxic_mean)
            discriminative_features[col] = {
                'toxic_mean': toxic_mean,
                'non_toxic_mean': non_toxic_mean,
                'difference': difference
            }
    
    print("   📈 Características más discriminativas:")
    for feature, stats in sorted(discriminative_features.items(), 
                                key=lambda x: x[1]['difference'], reverse=True):
        print(f"     🎯 {feature}:")
        print(f"        Tóxicos: {stats['toxic_mean']:.3f}")
        print(f"        No tóxicos: {stats['non_toxic_mean']:.3f}")
        print(f"        Diferencia: {stats['difference']:.3f}")
    
    # 9. Ejemplos de comentarios con características extremas
    print("\n📝 9. Ejemplos de comentarios con características extremas...")
    
    if 'toxic_word_ratio' in all_features.columns:
        # Comentario con más palabras tóxicas
        max_toxic_idx = all_features['toxic_word_ratio'].idxmax()
        max_toxic_comment = all_features.loc[max_toxic_idx]
        print(f"\n   🔥 Comentario con más palabras tóxicas ({max_toxic_comment['toxic_word_ratio']:.2%}):")
        print(f"      \"{max_toxic_comment['Text_Clean'][:100]}...\"")
        print(f"      Es tóxico: {max_toxic_comment['IsToxic']}")
    
    if 'sentiment_negative' in all_features.columns:
        # Comentario más negativo
        max_negative_idx = all_features['sentiment_negative'].idxmax()
        max_negative_comment = all_features.loc[max_negative_idx]
        print(f"\n   😢 Comentario más negativo ({max_negative_comment['sentiment_negative']:.3f}):")
        print(f"      \"{max_negative_comment['Text_Clean'][:100]}...\"")
        print(f"      Es tóxico: {max_negative_comment['IsToxic']}")
    
    print("\n✅ DEMO COMPLETADA")
    print("="*60)
    print("💡 El nuevo feature engineering incluye:")
    print("   🔤 Características básicas de texto (longitud, palabras, etc.)")
    print("   😊 Análisis de sentimiento (VADER)")
    print("   💀 Características específicas de toxicidad")
    print("   📊 TF-IDF vectorization")
    print("   🔤 N-gramas de caracteres")
    print(f"\n📈 Total de características generadas: {all_features.shape[1]}")
    
    return all_features

if __name__ == "__main__":
    demo_feature_engineering()
