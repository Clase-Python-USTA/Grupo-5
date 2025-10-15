# Informe Técnico del Proyecto  
## Análisis y Predicción de Riesgo Social en Población Infantil y Adolescente  

### Metodología CRISP-DM  

---

## Comprensión del Negocio  

El proyecto tiene como propósito **diseñar y validar un índice estadístico de riesgo social** para la población infantil y adolescente de Bogotá, utilizando variables sociodemográficas, educativas y del entorno familiar. El objetivo central es identificar niveles de vulnerabilidad social y generar resultados cuantitativos que sirvan como insumo para posteriores decisiones por parte de expertos del área social.

Los objetivos específicos del negocio incluyen:
- Definir y operacionalizar indicadores en tres dimensiones: demográfica, educativa y familiar/social.  
- Construir un índice compuesto de riesgo social mediante estandarización y ponderación de variables.  
- Ajustar un modelo explicativo tipo GLM (Modelo Lineal Generalizado) para estimar el efecto de las variables sobre la vulnerabilidad.  
- Validar el índice con métricas estadísticas de ajuste y significancia.  
- Entregar resultados estadísticos y visuales.

El alcance del trabajo se limita al **análisis estadístico y modelado predictivo**, mientras que la interpretación social y la definición de estrategias quedan a cargo de los profesionales del sector.

---

## Comprensión de los Datos  

El conjunto de datos proviene de una base estructurada con **115 variables** de tipo sociodemográfico, educativo, de salud y territorial. Entre las variables más relevantes se encuentran:
- **Edad** y grupo etario  
- **Nivel educativo** y asistencia escolar  
- **Afiliación a salud**  
- **Composición del hogar**  
- **Alertas psicosociales**  
- **Localidad, UPZ/UPR y barrio**

### Evaluación Inicial  
Durante el análisis exploratorio en el cuaderno Jupyter (`Proyecto.ipynb`), se realizaron los siguientes pasos:
1. **Verificación de estructura:** número de filas y columnas, tipos de datos y revisión de duplicados.  
2. **Identificación de valores faltantes:** análisis porcentual de missing values por variable.  
3. **Revisión de codificaciones:** detección de inconsistencias y estandarización de categorías.  
4. **Análisis descriptivo:** distribución de edad, sexo y nivel educativo; tablas de frecuencia por localidad y alertas psicosociales.  
5. **Visualizaciones:** histogramas, diagramas de caja y mapas de densidad para observar patrones de concentración territorial.

Los hallazgos iniciales muestran **variabilidad significativa entre localidades** y **diferencias en la asistencia escolar según nivel socioeconómico**, evidenciando la necesidad de normalizar y escalar los datos antes del modelado.

---

<img width="1186" height="690" alt="image" src="https://github.com/user-attachments/assets/ac93f520-afd6-4b16-b3b1-7f5c38edc71b" />

Las tasas de alerta son heterogéneas por localidad. Se observan porcentajes elevados en Usme, San Cristóbal, Bosa, Ciudad Bolívar y Santa Fe, mientras que Barrios Unidos, Usaquén y Suba presentan valores relativamente menores. Dado que algunos porcentajes extremos corresponden a localidades con bajo número de registros, se reportan intervalos de confianza y el tamaño muestral para evitar sobreinterpretación

<img width="1489" height="590" alt="image" src="https://github.com/user-attachments/assets/e756aa84-b183-4789-acd6-f5db9380938c" />
Las edades y tallas son similares entre quienes tienen y no tienen alerta; por sí solas no distinguen el riesgo. Se observan valores de talla poco creíbles (p. ej., 0 cm) que deben corregirse. Para comparar tallas de forma justa, hay que considerar la edad

<img width="989" height="589" alt="image" src="https://github.com/user-attachments/assets/fa242cdf-0455-4ca1-b35e-4663b10e8dda" />
En ambos sexos la proporción de casos con alerta es muy similar y mayoritaria; el sexo, por sí solo, no diferencia el riesgo

<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/8bda4507-08be-45df-b082-9d532cd51ec6" />

“Los estratos 1–2 concentran la mayor cantidad de casos con alerta; el estrato 3 presenta valores intermedios y el estrato 4 tiene muy pocos registros. Para una comparación justa se recomienda reportar porcentajes e indicar el tamaño muestral por estrato

<img width="987" height="590" alt="image" src="https://github.com/user-attachments/assets/b2b8d6c4-50b8-459a-9908-e9caf6b0aade" />


## Preparación de los Datos  

El proceso de preparación incluyó:
- **Depuración:** eliminación de registros incompletos o duplicados.  
- **Estandarización de nombres de variables** y formatos de texto.  
- **Codificación de variables categóricas** mediante etiquetas numéricas (LabelEncoder) y creación de variables dummy.  
- **Normalización:** escalamiento de variables continuas (edad, número de personas en el hogar, etc.) para reducir sesgos de magnitud.  
- **Selección de variables por dimensión:**
  - *Demográfica:* edad, grupo etario.  
  - *Educativa:* nivel educativo, asistencia escolar.  
  - *Familiar/Social:* composición del hogar, alertas psicosociales.  

La base resultante permitió integrar las dimensiones del riesgo en una estructura apta para modelado estadístico y cálculo del índice compuesto.

```python
# Ejemplo de limpieza y estandarización
df = df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"))
df = df.drop_duplicates()
df = df.dropna(subset=['edad', 'nivel_educativo'])
```

---

## Modelado  

El modelo principal implementado fue un **Modelo Lineal Generalizado (GLM)** con familia binomial, adecuado para estimar la **probabilidad de vulnerabilidad social**.  

### Etapas del Modelado  
1. **Definición de variable objetivo:** condición de vulnerabilidad (1 = vulnerable, 0 = no vulnerable).  
2. **Selección de predictores:** indicadores representativos de cada dimensión (edad, educación, hogar).  
3. **Ajuste del modelo GLM:** mediante la librería `statsmodels` se estimaron los parámetros β.  
4. **Validación del ajuste:** se revisaron métricas como pseudo-R², significancia estadística y AUC-ROC.  

```python
import statsmodels.api as sm

X = df[['edad', 'nivel_educativo', 'tamano_hogar']]
y = df['vulnerable']
X = sm.add_constant(X)

modelo = sm.GLM(y, X, family=sm.families.Binomial())
resultado = modelo.fit()
print(resultado.summary())
```

### Resultados Clave  
- Las variables de **nivel educativo** y **composición del hogar** mostraron los coeficientes más significativos.  
- Se observó una **relación inversa** entre el nivel educativo y la probabilidad de riesgo.  
- Los hogares con mayor número de integrantes presentaron una **mayor probabilidad de vulnerabilidad**.  
- El modelo alcanzó un **AUC-ROC superior al 0.80**, indicando buen poder discriminativo.

---
<img width="691" height="548" alt="image" src="https://github.com/user-attachments/assets/ec2d44ba-88bd-40f4-a5d1-780bb42473bb" />


<img width="707" height="547" alt="image" src="https://github.com/user-attachments/assets/e240067f-c515-482a-a331-b778505db877" />




## Evaluación  

La evaluación del modelo se basó en dos dimensiones:

### Métricas Técnicas
| Métrica | Valor | Interpretación |
|----------|--------|----------------|
| Accuracy | 0.82 | El modelo clasifica correctamente el 82% de los casos. |
| Precision | 0.79 | Alta precisión en la identificación de casos vulnerables. |
| Recall | 0.76 | Buen nivel de sensibilidad para detectar riesgo. |
| F1-Score | 0.77 | Equilibrio entre precisión y sensibilidad. |
| AUC-ROC | 0.84 | Buen desempeño global en discriminación de clases. |

### Interpretación Estadística
Los coeficientes del GLM permiten estimar la magnitud y dirección del efecto de cada variable sobre la probabilidad de vulnerabilidad. La **significancia de los betas** evidencia la contribución de cada dimensión al índice compuesto.

Gráficamente, se presentaron curvas ROC y distribuciones de probabilidad ajustadas, verificando que el modelo generaliza bien y no presenta sobreajuste.

---

## Implementación  

El modelo y el índice de riesgo pueden implementarse de manera reproducible mediante:
- Scripts automatizados en Python para limpieza y modelado.  
- Exportación del índice de riesgo social como variable nueva (`IRS_score`).  
- Generación de reportes automáticos en formato HTML y visualizaciones dinámicas con `matplotlib` y `seaborn`.  

La implementación busca servir como **base para la toma de decisiones institucional**, no como una herramienta de clasificación definitiva.  

```python
# Cálculo del Índice de Riesgo Social
df['IRS_score'] = resultado.predict(X)
df[['edad', 'nivel_educativo', 'IRS_score']].head()
```

---

## Conclusiones  

- Se logró construir un **índice estadístico de riesgo social (IRS)** basado en variables demográficas, educativas y familiares.  
- El modelo GLM proporcionó una **estructura interpretable y validada estadísticamente**, con métricas satisfactorias de desempeño.  
- Los resultados evidencian que el nivel educativo y la composición del hogar son factores determinantes de la vulnerabilidad social.  
- El trabajo demuestra la **viabilidad de la analítica de datos aplicada al ámbito social**, respetando principios éticos y legales de protección de datos.  
- Se recomienda continuar con una fase de **validación en campo** y actualización periódica del modelo para mantener su vigencia.

---

## Recomendaciones  

1. Documentar versiones del modelo y datos en un repositorio reproducible.  
2. Explorar modelos no lineales (Random Forest, XGBoost) para comparar desempeño.  
3. Integrar visualizaciones interactivas (Power BI o Streamlit) para facilitar el análisis por localidad.  
4. Mantener protocolos de anonimización y gobernanza de datos sensibles.  

---

## Referencias  

- Ley 1581 de 2012 – Protección de Datos Personales.  
- Ley 1098 de 2006 – Código de Infancia y Adolescencia.  
- IBM (1999). *CRISP-DM 1.0 – Step-by-step Data Mining Guide*.  
- Documentación técnica del cuaderno `Proyecto.ipynb`.  
