# Proyecto de Análisis y Predicción de Riesgo Social en Población Infantil y Adolescente

## Objetivos del Negocio

### Objetivo General  
Analizar la información sociodemográfica, educativa, de salud y territorial contenida en la base de datos de la Subred Integrada de Servicios de Salud de Bogotá para identificar condiciones de vulnerabilidad en población infantil y adolescente, y orientar la toma de decisiones en intervenciones sociales mediante la construcción de un modelo de predicción de riesgo social.

### Objetivos Específicos  
1. Caracterizar a la población menor de edad según variables como edad, sexo, etnia, nivel educativo, ocupación y composición del hogar, con el fin de establecer perfiles de riesgo.  
2. Identificar las condiciones de salud y nutrición de la población infantil y adolescente a partir de indicadores registrados en la base, tales como afiliación al SGSSS, clasificación nutricional, alertas psicosociales y enfermedades reportadas.   
3. Desarrollar un modelo de predicción de riesgo social que identifique y explique las variables que más influyen en la probabilidad de que un menor se encuentre en situación de vulnerabilidad, considerando de manera opcional el uso de Modelos Lineales Generalizados (GLM) estableciendo como meta una precisión mínima del 80% (Accuracy).

---

## Evaluación de la Situación

### Recursos Disponibles
- Base de datos estructurada con 115 columnas de tipo sociodemográfico, de salud, educativo y territorial.  
- Variables clave de seguimiento de intervenciones sociales y de alertas de riesgo.  
- Información georreferenciada (localidad, UPZ/UPR, barrio, manzana del cuidado).  

### Riesgos y Contingencias
- Calidad de datos: presencia de valores faltantes, duplicados o inconsistencias en codificación.  
- Aspectos legales y éticos: uso responsable y anonimizado de datos sensibles de menores de edad.  
- Posibles limitaciones en la actualización y periodicidad de los registros.  

### Análisis Costo-Beneficio
- Costos: tiempo y esfuerzo en limpieza de datos, construcción de modelos predictivos y validación de resultados.  
- Beneficios: focalización más eficiente de recursos sociales y de salud, priorización de zonas críticas y evaluación de la efectividad de intervenciones.  

---

## Objetivos de la Minería de Datos
- Clasificación de riesgo social: Agrupar a la población según perfiles construidos con variables sociodemográficas, de salud y educación.  
- Predicción: Construir un modelo de riesgo social que estime la probabilidad de que un menor presente condiciones de vulnerabilidad, explicando qué variables influyen más en esa probabilidad. Se contempla el uso de Modelos Lineales Generalizados (GLM) por su capacidad interpretativa en escenarios sociales.  
- Análisis territorial: Identificar zonas críticas a través de las variables de localidad, barrio, UPZ y manzana del cuidado.  
- Evaluación de impacto: Medir el efecto de intervenciones registradas (nutrición, psicosociales, educativas) sobre la reducción de alertas en la población.  

---

## Plan del Proyecto

### Tecnologías y Herramientas
- Python: pandas, scikit-learn, statsmodels (GLM). 

### Fases
1. Preparación de datos: limpieza, estandarización de nombres de columnas y validación de calidad.  
2. Exploración inicial: análisis descriptivo de variables sociodemográficas, de salud y educativas.  
3. Modelado: desarrollo de modelos predictivos de riesgo social (inicialmente GLM).  
4. Evaluación: análisis de métricas técnicas (precisión, recall, AUC-ROC) y comparación con criterios sociales definidos.  
5. Implementación: informes que faciliten la toma de decisiones.  

---

## Estructura del Proyecto
```
Grupo-5
 ┣ .venv
 ┃ ┣ lib
 ┃ ┣ Scripts
 ┣ 1.Comprensión empresarial
 ┣ 2. Entedimiento de la base
 ┣ data
 ┃ ┣ interim
 ┃ ┣ raw
 ┣ reports_auto
 ┃ ┣ figures
 ┃ ┣ groups
 ┣ origen.py
 ┗ requirements.txt
```

---

## Métricas de Evaluación
- Técnicas: Accuracy, Precision, Recall, F1-score, AUC-ROC.  
- Sociales: reducción de alertas psicosociales, cobertura de intervenciones, focalización territorial.  

---

## Aspectos Éticos
- Datos totalmente anonimizados.  
- Uso exclusivo con fines académicos.  
- Cumplimiento con normativa de hábeas data y protección de menores.  

---

## Entregables
- Base de datos depurada y documentada.  
- Modelo predictivo validado (GLM y alternativas).  
- visualizaciones.  
- Informe técnico final con hallazgos y recomendaciones.  
