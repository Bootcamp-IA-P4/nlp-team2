# feature_engineering.py

import pandas as pd
import numpy as np
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from collections import Counter
import nltk
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Descargar recursos de NLTK si es necesario
try:
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

class ToxicityFeatureExtractor:
    """Extractor de características específico para detección de toxicidad"""
    
    def __init__(self, max_features=10000):
        self.max_features = max_features
        self.tfidf_vectorizer = None
        self.ngram_vectorizer = None
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.toxic_keywords = [
            'hate', 'stupid', 'idiot', 'moron', 'kill', 'die', 'fuck', 'shit', 
            'damn', 'hell', 'bitch', 'asshole', 'racist', 'sexist'
        ]
        
    def extract_all_features(self, df, fit_vectorizers=True):
        """Extraer todas las características de toxicidad"""
        features_df = df.copy()
        
        # 1. Features básicas de texto
        features_df = self.add_basic_text_features(features_df)
        
        # 2. Features de sentimiento
        features_df = self.add_sentiment_features(features_df)
        
        # 3. Features específicas de toxicidad
        features_df = self.add_toxicity_features(features_df)
        
        # 4. Features de TF-IDF
        tfidf_features = self.extract_tfidf_features(features_df['Text_Clean'], fit=fit_vectorizers)
        
        # 5. Features de n-gramas
        ngram_features = self.extract_ngram_features(features_df['Text_Clean'], fit=fit_vectorizers)
        
        # Combinar todo
        final_df = pd.concat([
            features_df.reset_index(drop=True),
            tfidf_features.reset_index(drop=True),
            ngram_features.reset_index(drop=True)
        ], axis=1)
        
        return final_df
    
    def add_basic_text_features(self, df):
        """Agregar características básicas del texto"""
        df = df.copy()
        
        # Longitud del texto
        df['text_length'] = df['Text_Clean'].str.len()
        df['word_count'] = df['Text_Clean'].str.split().str.len()
        df['avg_word_length'] = df['text_length'] / df['word_count']
        
        # Conteo de caracteres especiales
        df['exclamation_count'] = df['Text_Clean'].str.count('!')
        df['question_count'] = df['Text_Clean'].str.count(r'\?')
        df['caps_count'] = df['Text_Clean'].str.count(r'[A-Z]')
        df['caps_ratio'] = df['caps_count'] / df['text_length']
        
        # Conteo de números y caracteres especiales
        df['number_count'] = df['Text_Clean'].str.count(r'\d')
        df['special_char_count'] = df['Text_Clean'].apply(
            lambda x: sum(1 for c in str(x) if c in string.punctuation)
        )
        
        return df
    
    def add_sentiment_features(self, df):
        """Agregar características de sentimiento"""
        df = df.copy()
        
        sentiments = df['Text_Clean'].apply(
            lambda x: self.sentiment_analyzer.polarity_scores(str(x))
        )
        
        df['sentiment_compound'] = sentiments.apply(lambda x: x['compound'])
        df['sentiment_positive'] = sentiments.apply(lambda x: x['pos'])
        df['sentiment_negative'] = sentiments.apply(lambda x: x['neg'])
        df['sentiment_neutral'] = sentiments.apply(lambda x: x['neu'])
        
        return df
    
    def add_toxicity_features(self, df):
        """Agregar características específicas de toxicidad"""
        df = df.copy()
        
        # Asegurar que tenemos word_count
        if 'word_count' not in df.columns:
            df['word_count'] = df['Text_Clean'].str.split().str.len()
        
        # Conteo de palabras tóxicas
        df['toxic_word_count'] = df['Text_Clean'].apply(
            lambda x: sum(1 for word in str(x).lower().split() if word in self.toxic_keywords)
        )
        df['toxic_word_ratio'] = df['toxic_word_count'] / (df['word_count'] + 1)  # +1 para evitar división por 0
        
        # Palabras en mayúsculas (agresividad)
        df['all_caps_words'] = df['Text_Clean'].apply(
            lambda x: len([word for word in str(x).split() if word.isupper() and len(word) > 1])
        )
        
        # Repetición de caracteres (ej: "nooooo", "!!!")
        df['repeated_chars'] = df['Text_Clean'].apply(
            lambda x: len(re.findall(r'(.)\1{2,}', str(x)))
        )
        
        # Densidad de insultos por oración
        df['sentence_count'] = df['Text_Clean'].str.count(r'[.!?]+') + 1
        df['toxic_density'] = df['toxic_word_count'] / df['sentence_count']
        
        return df
    
    def extract_tfidf_features(self, texts, fit=True):
        """Extraer características TF-IDF"""
        if fit or self.tfidf_vectorizer is None:
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=min(self.max_features, 5000),
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95
            )
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        else:
            tfidf_matrix = self.tfidf_vectorizer.transform(texts)
        
        # Convertir a DataFrame
        feature_names = [f'tfidf_{name}' for name in self.tfidf_vectorizer.get_feature_names_out()]
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
        
        return tfidf_df
    
    def extract_ngram_features(self, texts, fit=True):
        """Extraer características de n-gramas de caracteres"""
        if fit or self.ngram_vectorizer is None:
            self.ngram_vectorizer = CountVectorizer(
                analyzer='char',
                ngram_range=(2, 4),
                max_features=min(self.max_features // 2, 1000),
                binary=True
            )
            ngram_matrix = self.ngram_vectorizer.fit_transform(texts)
        else:
            ngram_matrix = self.ngram_vectorizer.transform(texts)
        
        # Convertir a DataFrame
        feature_names = [f'ngram_{name}' for name in self.ngram_vectorizer.get_feature_names_out()]
        ngram_df = pd.DataFrame(ngram_matrix.toarray(), columns=feature_names)
        
        return ngram_df

# Funciones de compatibilidad con versión anterior
def extract_features(df):
    """Función de compatibilidad - usa el extractor avanzado"""
    extractor = ToxicityFeatureExtractor()
    return extractor.extract_all_features(df)

def add_length_features(df):
    """Función de compatibilidad - características de longitud"""
    extractor = ToxicityFeatureExtractor()
    return extractor.add_basic_text_features(df)

def add_sentiment_features(df, sentiment_analyzer=None):
    """Función de compatibilidad - características de sentimiento"""
    extractor = ToxicityFeatureExtractor()
    return extractor.add_sentiment_features(df)