📊 MÉTRICAS EN CLASIFICACIÓN MULTI-LABEL
🎯 1. HAMMING LOSS (Pérdida de Hamming)
¿Qué es?
Mide el porcentaje de etiquetas mal clasificadas
Se calcula: (predicciones incorrectas) / (total de predicciones)
¿Cómo interpretar?

0.0 = PERFECTO (0% de errores)
0.1 = BUENO (10% de errores)
0.2 = REGULAR (20% de errores)
0.3+ = MALO (30%+ de errores)

Ejemplo práctico: 

# Si tienes 8 etiquetas por muestra y 200 muestras de prueba
# Total predicciones = 8 × 200 = 1,600

# Hamming Loss = 0.15 significa:
# 1,600 × 0.15 = 240 predicciones incorrectas
# Es decir, 85% de precisión

🎯 2. JACCARD SCORE (Índice Jaccard)
¿Qué es?
Mide la similitud entre conjuntos
Se calcula: (etiquetas correctas) / (etiquetas predichas + etiquetas reales - etiquetas correctas)
¿Cómo interpretar?

0.0 = TERRIBLE (sin coincidencias)
0.3 = ACEPTABLE
0.5 = BUENO
0.7+ = EXCELENTE


Ejemplo práctico:

# Para un comentario:
# Etiquetas reales: [IsToxic=1, IsAbusive=1, IsRacist=0]
# Predicciones:     [IsToxic=1, IsAbusive=0, IsRacist=1]

# Intersección = 1 (solo IsToxic coincide)
# Unión = 3 (todas las etiquetas mencionadas)
# Jaccard = 1/3 = 0.33


🎯 3. F1-SCORE
F1-Macro (Promedio por clase):
Calcula F1 para cada etiqueta y promedia
Bueno para clases desbalanceadas
F1-Micro (Global):
Considera todas las predicciones juntas
Favorece clases mayoritarias
¿Cómo interpretar?

0.0-0.2 = MALO
0.2-0.4 = REGULAR  
0.4-0.6 = BUENO
0.6-0.8 = MUY BUENO
0.8+ = EXCELENTE

📈 ANÁLISIS DE TUS RESULTADOS
🤖 Transformer (DistilBERT):

Hamming Loss: 0.1525 (15.25% errores) ✅ BUENO
Jaccard Score: 0.0276 (2.76% similitud) ❌ MALO
F1 Macro: 0.045 (4.5%) ❌ MALO
F1 Micro: 0.147 (14.7%) ❌ MALO


🔍 ¿Por qué estos resultados?
✅ Hamming Loss bueno PERO F1/Jaccard malos:
Esto significa que el modelo:

Acierta en la mayoría de predicciones (85% correcto)
PERO tiene problemas específicos:
Muchos falsos negativos (no detecta toxicidad cuando sí existe)
Muchos falsos positivos (dice que es tóxico cuando no lo es)