# Proyecto de Análisis y Predicción de Riesgo Social en Población Infantil y Adolescente

## Objetivos del Negocio

Diseñar y validar un índice estadístico de riesgo social para población infantil y adolescente de Bogotá usando variables sociodemográficas, educativas y del entorno familiar, con el fin de identificar niveles de vulnerabilidad y generar resultados cuantitativos que sirvan como insumo para posteriores decisiones por parte de expertos del área social.

## Objetivos específicos.

Definir y operacionalizar indicadores en dimensiones demográfica, educativa y familiar/social.
Construir y validar un índice compuesto de riesgo mediante estandarización, ponderación y métricas de ajuste.
Ajustar un GLM (logístico binario) para estimar el efecto de variables sobre la vulnerabilidad y entregar resultados estadísticos y visuales.
Alcance. Se limita al análisis estadístico y modelado predictivo; la interpretación social y las estrategias quedan a cargo de expertos del sector.


---

## Evaluación de la Situación

### Recursos Disponibles
- Base de datos estructurada con 115 columnas de tipo sociodemográfico, de salud, educativo y territorial.  
- Variables potenciales: edad, nivel educativo, afiliación al sistema de salud, composición del hogar y alertas psicosociales. 
- Información georreferenciada (localidad, UPZ/UPR, barrio, manzana del cuidado).  

### Riesgos y Contingencias
- Calidad de datos: presencia de valores faltantes, duplicados o inconsistencias en codificación.  
- Aspectos legales y éticos: uso responsable y anonimizado de datos sensibles de menores de edad.  
- Posibles limitaciones alcance estadístico del trabajo sin validación en campo, en la actualización y periodicidad de los registros.  

### Alcancer del Trabajo
- El equipo estadístico se limita a la fase analítica y de modelado predictivo, entregando un conjunto de resultados cuantitativos y visuales (tablas, modelos, gráficos, métricas). La interpretación contextual y toma de decisiones corresponde a los profesionales del área social o institucional.

---

## Objetivos de la Minería de Datos
- Construcción del Índice de Riesgo Social (IRS): basado en tres dimensiones:
  
->Demográfica: edad y grupo etario.

->Educativa: nivel educativo y asistencia escolar.

->Familiar/Social: composición del hogar y alertas psicosociales.

- Modelado Predictivo: Construir un modelo de riesgo social que estime la probabilidad de que un menor presente condiciones de vulnerabilidad, explicando qué variables influyen más en esa probabilidad.Uso de un GLM binomial o ordinal para estimar la influencia de las variables en el nivel de riesgo, interpretando los betas como evidencia estadística.

- Validación: evaluación del ajuste del modelo e interpretación de resultados mediante indicadores estadísticos, sin emitir juicios de política o intervención.

---

## Plan del Proyecto

### Tecnologías y Herramientas
- Python: pandas, scikit-learn, statsmodels (GLM). 

### Fases
1. Preparación de datos: limpieza, estandarización de nombres de columnas y validación de calidad.  
2. Exploración inicial: análisis descriptivo de variables sociodemográficas, de salud y educativas.
3. Selección de variables por dimensión (edad, educación, hogar).
4. Construcción del índice compuesto de riesgo social (inicialmente GLM).  
6. Ajuste del modelo GLM e interpretación de coeficientes.
7. Presentación de resultados estadísticos y visuales.

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
- Técnicas: Accuracy, Precision, Recall, F1-score, AUC-ROC, pseudo R², significancia de los betas. 
- Interpretativas: magnitud y dirección de los coeficientes como evidencia del peso de cada dimensión.

---

## Aspectos Éticos
- Datos totalmente anonimizados.  
- Uso exclusivo con fines académicos.
- Cumplimiento de la Ley 1581 de 2012 (hábeas data) y la Ley 1098 de 2006 (protección de menores).

---

## Entregables
- Base de datos depurada y documentada.  
- Índice de Riesgo Social validado y reproducible.
- Modelo GLM ajustado con interpretación estadística de betas.
- visualizaciones.
- Informe técnico final con hallazgos y recomendaciones estadísticas.  
