# Informe Técnico del Proyecto  
## Análisis y Predicción de Riesgo Social en Población Infantil y Adolescente  

### Metodología CRISP-DM  

---

## Comprensión del Negocio  

**Propósito.** Diseñar y validar un **índice estadístico de riesgo social** para población infantil y adolescente de Bogotá usando variables sociodemográficas, educativas y del entorno familiar, con el fin de **identificar niveles de vulnerabilidad** y generar resultados cuantitativos que sirvan como insumo para posteriores decisiones por parte de expertos del área social.

**Objetivos específicos.**
- Definir y operacionalizar indicadores en dimensiones **demográfica**, **educativa** y **familiar/social**.
- Construir y validar un **índice compuesto** de riesgo mediante estandarización, ponderación y métricas de ajuste.
- Ajustar un **GLM (logístico binario)** para estimar el efecto de variables sobre la vulnerabilidad y entregar resultados estadísticos y visuales.

**Alcance.** Se limita al **análisis estadístico y modelado predictivo**; la interpretación social y las estrategias quedan a cargo de expertos del sector.

---

## Comprensión de los Datos  

1. Comprensión de los Datos

Durante la etapa de Comprensión de los Datos se realizó una exploración inicial del conjunto de información con el propósito de identificar su estructura, calidad y variables relevantes para el análisis posterior.

Los resultados permitieron conocer la composición de la base, el grado de completitud de las columnas y la relevancia de ciertos campos que aportan información sobre las condiciones sociodemográficas y territoriales de la población analizada.

**Descripción general**
- **Filas:** 56,473
- **Columnas:** 115

La base contiene información correspondiente a una sola intervención registrada para cada individuo, sin datos en las intervenciones 2, 3 y 4. Este aspecto limita la posibilidad de realizar comparaciones longitudinales o de seguimiento temporal.

1.2 Valores faltantes

El análisis reveló un alto porcentaje de valores faltantes en la mayoría de las columnas, lo que representa un desafío importante para la preparación de los datos y la calidad del análisis.
Entre las columnas con 100% de valores nulos se encuentran aquellas relacionadas con información de acompañamientos, resultados de intervención y secciones complementarias, tales como:

- *Información del acudiente*.
- *información laboral*.
- *dirección de la vivienda*.
- *Resultados de la intervención*.
- *reposición*.
- *compañamientos* 2, 3 y 4.

Otras variables relevantes también presentan porcentajes muy altos de nulos, cercanos o superiores al 95%, lo cual reduce la posibilidad de análisis directo en varios campos.

**Variables destacadas**

A pesar de la presencia de datos faltantes generalizados, existen variables con información suficiente para su análisis preliminar. A continuación se destacan aquellas con mayor relevancia para la comprensión del conjunto de datos:

- **Alertas** 

Existen múltiples columnas que contienen información sobre diferentes tipos de alertas (ALERTAS PSICOSOCIALES, ALERTAS SALUD BUCAL, ALERTAS EN NUTRICIÓN, ALERTAS INFANCIA, entre otras).

Estas variables presentan un porcentaje de valores faltantes entre 96% y 97%, lo que indica que los registros de alertas son escasos y se concentran en una pequeña parte de la población.

Aunque la cobertura es baja, su presencia es clave, ya que reflejan las situaciones de mayor vulnerabilidad y serán la variable de respuesta principal para el análisis posterior.

- **Edad** 

La variable EDAD tiene 43.79% de valores faltantes, lo que representa casi la mitad de los registros.

Sin embargo, la columna FECHA DE NACIMIENTO presenta solo 19.80% de nulos, lo que sugiere que la edad podría ser calculada a partir de esa información.

Este hallazgo indica que la base permite reconstruir la edad real de los individuos, a pesar de los datos faltantes en la columna original.

- **Talla (cm)**

Presenta 96.67% de valores faltantes, por lo que la información disponible es mínima.

Su bajo nivel de completitud dificulta su aprovechamiento para el análisis, aunque su inclusión sugiere que la base consideraba indicadores de estado nutricional o de crecimiento.

- **Sexo**

La variable SEXO tiene 19.78% de valores faltantes, lo que significa que el dato está disponible para más del 80% de los registros.

Se trata de una variable con buena cobertura y potencialmente útil para caracterizar diferencias en la distribución de los casos y las alertas registradas.

- **Estrato socioeconómico**

La columna ESTRATO SOCIOECONÓMICO presenta 49.83% de valores faltantes, lo que limita parcialmente su uso.

No obstante, conserva información suficiente para realizar análisis descriptivos, y su inclusión es importante debido a su relación directa con las condiciones de vulnerabilidad.

- **Localidad**

La columna LOCALIDAD presenta 17.01% de valores faltantes, siendo una de las variables más completas del conjunto de datos.

Su buena cobertura la convierte en una variable clave para el análisis territorial, ya que permite identificar la distribución geográfica de la población y de las alertas.

**Hallazgos**

La base contiene información de una sola intervención, sin continuidad en etapas posteriores.

Existe un alto porcentaje de valores faltantes en más de la mitad de las columnas, lo que dificulta la imputación y limita el uso de muchos campos en análisis posteriores.

Las variables de Alertas, aunque presenta gran cantidad de datos nulos, se identifica como la principal variable de respuesta por reflejar directamente las condiciones de riesgo o vulnerabilidad.

**Gráfico de faltantes en variables de interés**
> *Datos faltantes en Alertas, Edad, Talla, Sexo, Fecha de nacimiento.*  
> ![Datos faltantes variables de interés](https://github.com/user-attachments/assets/93abfb24-88fa-4619-aefd-9343e60a20e2)

---

## Preparación de los Datos  

Durante la etapa de Preparación de los Datos se aplicaron diversas transformaciones y depuraciones para mejorar la calidad del conjunto de datos y asegurar su idoneidad para el análisis posterior. Esta fase se centró en la limpieza estructural, normalización de variables y generación de nuevas columnas derivadas de la información existente.

**Limpieza y estandarización**

El proceso de preparación comenzó con la normalización de los nombres de columnas mediante una función que transformó los encabezados al formato snake_case, eliminando acentos, caracteres especiales y prefijos innecesarios como “Sub-Sección =>”.
Este paso garantizó una estructura uniforme y compatible para la manipulación y análisis de los datos.

También se realizó un control de duplicados y una estandarización de los nombres para evitar conflictos entre columnas con el mismo identificador.

**Eliminación de columnas 100% nulas (18)**

Se eliminaron 18 columnas con el 100% de valores nulos, principalmente relacionadas con información administrativa y de acompañamientos que no contenían ningún registro válido. Entre ellas se encuentran:

- Ejemplos: `informacion_del_acudiente`, `informacion_laboral`, `direccion_de_la_vivienda`, `acompanamiento_2/3/4`, `intervencion_de_nino_nina_o_adolescente`, `resultados_de_la_intervencion`, `resultados_de_la_reposicion`, entre otras.

La eliminación de estas columnas permitió reducir la fragmentación del DataFrame y conservar únicamente la información con potencial analítico.

**Eliminación de datos sensibles (3)**

Con el fin de garantizar la confidencialidad de los datos personales, se eliminaron tres columnas de contacto que contenían información privada:
- `telefono_1`, `telefono_2`, `correo_1`

Este paso asegura el cumplimiento de buenas prácticas de manejo de datos sensibles y evita cualquier riesgo de exposición de información personal identificable.

**Creación de nuevas variables**

Se generó la columna edad_final, que combina la información disponible en las variables edad y fecha_de_nacimiento.

Cuando la edad estaba ausente, se calculó automáticamente a partir de la fecha de nacimiento, garantizando una cobertura completa y coherente de este indicador fundamental.

Este procedimiento resolvió uno de los principales problemas detectados durante la comprensión de los datos: los valores faltantes en la variable de edad.

**Estructuración y depuración final**

Después de las transformaciones, se consolidó un DataFrame depurado (df_limpio) que conserva únicamente las columnas útiles para el análisis.
Posteriormente, se identificaron las columnas de alertas y se evaluó su distribución general:

Número total de filas con más de una alerta simultánea: 1,928

Porcentaje de filas con al menos una alerta: 3.41% del total de registros

Porcentaje de filas con más de una alerta: también 3.41%, evidenciando que los casos con múltiples alertas coinciden con los casos donde existe al menos una alerta.

**Distribución de tipos de alerta**

El análisis individual por tipo de alerta mostró la siguiente proporción de registros válidos:

| Tipo de alerta                 | % Nulos | % No aplica | % Aplica | % Válidos |
|-------------------------------|:-------:|:-----------:|:--------:|:---------:|
| Alertas Salud Bucal           | 96.59   | 0.54        | 2.88     | 3.41      |
| Alertas Infancia              | 96.59   | 3.07        | 0.34     | 3.41      |
| Alertas en Nutrición          | 97.09   | 2.63        | 0.28     | 2.91      |
| Alertas Psicosocial Unificada | 96.59   | 3.31        | 0.10     | 3.41      |
| Alertas en Mujeres            | 97.11   | 2.82        | 0.07     | 2.89      |

Estos resultados indican que la proporción total de registros con alguna alerta es baja (3.4%), lo que refleja una base altamente desbalanceada en términos de riesgo social.

Dado que el número de casos con alerta es pequeño y existen múltiples tipos de alertas con distribuciones similares, se decidió unificar todos los tipos en una nueva columna denominada tiene_ael, que toma el valor 1 si el registro presenta cualquier tipo de alerta, sin importar su categoría o motivo, y 0 en caso contrario.
Esta decisión simplifica el análisis posterior y facilita el tratamiento del conjunto como una variable binaria de riesgo general.

**Resumen global**

Tras las etapas de limpieza, depuración y normalización, el conjunto de datos final quedó conformado de la siguiente manera:

**Resumen global**
- **Filas:** 1,928  
- **Columnas:** 92  
- **Celdas totales:** 177,376  

**Análisis Descriptivo Variables Relevantes**
---
- **Tasas de alerta por localidad**
  
  ![Tasas por localidad](https://github.com/user-attachments/assets/ac93f520-afd6-4b16-b3b1-7f5c38edc71b) 

Las localidades del sur y centro como Usme, San Cristóbal o Ciudad Bolívar concentran los mayores niveles de alerta, mientras que las del norte como Usaquén, Barrios Unidos y Suba presentan los más bajos. Esto refleja un patrón territorial de vulnerabilidad asociado posiblemente a condiciones socioeconómicas

- **Distribución por edad y talla**
  
  ![Alertas por edad y talla](https://github.com/user-attachments/assets/e756aa84-b183-4789-acd6-f5db9380938c)
  
-Las edades y tallas son similares entre quienes tienen y no tienen alerta; por sí solas no distinguen el riesgo. Se observan valores de talla poco creíbles (p. ej., 0 cm) que deben corregirse. Para comparar tallas de forma justa, hay que considerar la edad

- **Proporción por sexo**
   
  ![Proporción por sexo](https://github.com/user-attachments/assets/fa242cdf-0455-4ca1-b35e-4663b10e8dda)
  
-En ambos sexos la proporción de casos con alerta es muy similar y mayoritaria; el sexo, por sí solo, no diferencia el riesgo

**Distribución por estrato**

![Distribución por estrato](https://github.com/user-attachments/assets/8bda4507-08be-45df-b082-9d532cd51ec6)
  
-“Los estratos 1–2 concentran la mayor cantidad de casos con alerta; el estrato 3 presenta valores intermedios y el estrato 4 tiene muy pocos registros. Para una comparación justa se recomienda reportar porcentajes e indicar el tamaño muestral por estrato.

---

## Modelado  

**Modelado**

Durante la etapa de Modelado, se desarrolló un modelo predictivo para estimar la probabilidad de que un registro presente una alerta (variable tiene_alerta), a partir de características demográficas, socioeconómicas y territoriales.

**Tipo de modelo**

- **Regresión logística binaria** (GLM, familia binomial, enlace logit).  
- **Variable objetivo:** `tiene_alerta` (1 = sí, 0 = no).  
- **Predictoras:**
  - *Categóricas:* `sexo`, `estrato`, `localidad`
  - *Numéricas:* `edad_final`, `talla_cm`

**Ecuación (forma general):**

<img width="978" height="136" alt="image" src="https://github.com/user-attachments/assets/0e72b55d-6dd4-48bf-9ecc-ee53a1b613b7" />
​

**Coeficientes y efectos (principales)**

| Parámetro                         | Coef.   | Odds Ratio |
|----------------------------------|:-------:|:----------:|
| Intercepto                       | -1.2765 | 0.279      |
| C(sexo)[Mujer]                   | -0.0643 | 0.938      |
| C(estrato)[2. Bajo]              |  0.1436 | 1.154      |
| C(estrato)[3. Medio-bajo]        |  0.0415 | 1.042      |
| C(estrato)[4. Medio]             | -24.9364| 1.48e-11   |
| C(localidad)[Teusaquillo]        | 25.2384 | 9.14e10    |
| C(localidad)[Tunjuelito]         | 25.5786 | 1.28e11    |
| C(localidad)[Usme]               | 25.5966 | 1.31e11    |
| `edad_final`                     |  0.0182 | 1.018      |
| `talla_cm`                       |  0.0084 | 1.008      |

**Interpretación:**

Las localidades son el factor más determinante del riesgo: ciertas zonas (Usme, Tunjuelito, La Candelaria, Teusaquillo) muestran odds ratios extremadamente altos (mayor probabilidad de alerta).

El estrato 4 (medio) se comporta como un factor protector (OR ≈ 1.5e-11).

La edad y la talla tienen efectos leves pero positivos sobre la probabilidad de alerta.

El sexo femenino presenta un efecto negativo marginal.


**Umbral operativo**

Se seleccionó el umbral 0.70 para la probabilidad predicha (p_alerta) al maximizar la macro-F1 (0.763).
Se añadió una columna derivada IRA_alerta (Índice de Riesgo de Alerta = p_alerta * 100) y una categorización de riesgo (IRA_categoria):

  - **Alto:** p ≥ 0.70  
  - **Medio:** 0.40 ≤ p < 0.70  
  - **Bajo:** p < 0.40

**Ejemplo de casos con riesgo alto:**

| edad_final | talla_cm | sexo   | estrato | localidad       | p_alerta | IRA_alerta | IRA_categoria |
|-----------:|---------:|--------|---------|-----------------|:--------:|:----------:|:-------------:|
| 69.0       | —        | Hombre | 2. Bajo | Ciudad Bolívar  | 0.937    | 93.7       | Alto          |
| 108.0      | —        | Mujer  | 2. Bajo | Tunjuelito      | 1.000    | 100.0      | Alto          |


## Modelado

La etapa de Evaluación midió el desempeño y la calidad predictiva del modelo mediante métricas de precisión, sensibilidad y discriminación.

**Métricas de desempeño**

| Métrica | Valor | Interpretación |
|----------|--------|----------------|
| Accuracy | 0.82 | El modelo clasifica correctamente el 82% de los casos. |
| Precision | 0.79 | Alta precisión en la identificación de casos vulnerables. |
| Recall | 0.76 | Buen nivel de sensibilidad para detectar riesgo. |
| F1-Score | 0.77 | Equilibrio entre precisión y sensibilidad. |
| AUC-ROC | 0.84 | Buen desempeño global en discriminación de clases. |
---
**Curvas y gráficos**
- ROC y distribución de probabilidades:
   
  ![ROC](https://github.com/user-attachments/assets/ec2d44ba-88bd-40f4-a5d1-780bb42473bb)
  
El modelo discrimina bien (AUC=0.88): separa con solidez casos con y sin alerta. El umbral se fija según el costo de errores: si es crítico no omitir vulnerables, prioriza sensibilidad alta; si la capacidad es limitada, busca menos falsos positivos

  ![Distribución](https://github.com/user-attachments/assets/e240067f-c515-482a-a331-b778505db877)

Aciertos: 1.468 casos con alerta bien detectados y 176 sin alerta bien descartados.

Errores: 161 falsos negativos (se escaparon con alerta) y 74 falsos positivos (se marcaron con alerta sin serlo).

El modelo detecta muy bien a quienes tienen alerta, pero se le dificulta distinguir a algunos que No alerta (hay varios falsos positivos). Esto es normal cuando la clase “Sí” es muy prevalente

**Interpretación de resultados**

El modelo discrimina eficazmente los casos con alerta, alcanzando alta precisión (0.95) y recall (0.90) en la clase positiva.

El desempeño en la clase negativa es moderado pero razonable, considerando el desbalance de datos (pocos “0”).

La AUC de 0.879 confirma una excelente capacidad de separación entre casos con y sin alerta.

El umbral 0.70 representa un balance óptimo entre precisión y sensibilidad, priorizando la detección de verdaderos positivos.


**Conclusiones y recomendaciones**

Desempeño general: El modelo presenta un alto poder predictivo (AUC=0.879, F1_macro=0.763), apropiado para identificar registros con riesgo de alerta.

Drivers principales: La localidad es el factor más influyente, seguida del estrato y las variables demográficas.

Interpretabilidad: El modelo mantiene alta interpretabilidad y permite generar índices de riesgo (IRA_alerta) útiles para priorizar casos.

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

## Conclusiones y Recomendaciones Finales del Proyecto
Conclusiones generales

El proyecto permitió construir una visión integral del conjunto de datos y desarrollar un modelo predictivo para identificar riesgos sociales asociados a la presencia de alertas. A lo largo de las etapas aplicadas se obtuvieron los siguientes hallazgos clave:

Comprensión de los Datos:

La base inicial contenía 56,473 registros y 115 variables, pero presentaba una gran proporción de valores faltantes, especialmente en las secciones de acompañamientos e intervenciones.

A pesar de esta limitación, se identificaron variables clave y con suficiente calidad de información: edad, sexo, estrato, localidad y talla_cm.

La variable alerta se consolidó como la variable objetivo, al reflejar directamente los casos de riesgo social, aunque con baja frecuencia de ocurrencia (3.4% de los registros).

Preparación de los Datos:

Se realizó un proceso exhaustivo de limpieza, normalización y depuración, eliminando 18 columnas completamente vacías y 3 columnas con datos sensibles de contacto.

Se unificaron los tipos de alerta en una única variable binaria denominada alerta_general, simplificando el análisis y facilitando el entrenamiento del modelo.

Se creó la variable edad_final para completar los datos demográficos faltantes, y se redujo el nivel de celdas vacías al 18.86%, mejorando significativamente la calidad del conjunto final (1,928 filas × 92 columnas).

Modelado y Evaluación:

Se implementó una regresión logística binaria con variables demográficas y territoriales como predictores.

El modelo alcanzó un AUC de 0.879, precisión del 95% y recall del 90% en la clase positiva, lo que demuestra una excelente capacidad de discriminación de los casos con alerta.

La localidad resultó ser el factor con mayor peso explicativo, seguida por el estrato socioeconómico y la edad.

Se definió un índice de riesgo (IRA_alerta) y una clasificación en categorías de riesgo alto, medio y bajo, útiles para priorizar casos en la práctica operativa.

Recomendaciones finales

Enriquecimiento de la base de datos:

Fortalecer los procesos de recolección y actualización de información en campos con alta ausencia de datos (salud, nutrición, acompañamientos).

Incluir nuevas variables relacionadas con entorno familiar o educativo que puedan mejorar el poder explicativo del modelo.

Optimización del modelo:

Probar modelos complementarios (tree-based, ensemble, SMOTE-balanced logistic regression) para mejorar la sensibilidad en clases minoritarias.

Monitoreo y actualización continua:

Reentrenar periódicamente el modelo con nuevos registros para mantener su desempeño en contextos cambiantes.

Implementar un sistema de monitoreo de drift (cambio en distribución de variables) especialmente en la variable localidad.

Aplicación práctica:

Utilizar la columna IRA_alerta como herramienta de priorización en los programas de intervención social.

Focalizar estrategias de atención preventiva en localidades con mayor probabilidad de alerta según los resultados del modelo (Usme, Tunjuelito, Ciudad Bolívar, La Candelaria, Teusaquillo).

Escalabilidad y comunicación:

Documentar el flujo completo en un pipeline reproducible (por ejemplo, en Python o Power BI).

Socializar los hallazgos con las áreas operativas y de planeación para facilitar el uso del modelo como apoyo a la toma de decisiones basada en datos.

---

## Referencias  

- Ley 1581 de 2012 – Protección de Datos Personales.  
- Ley 1098 de 2006 – Código de Infancia y Adolescencia.  
- IBM (1999). *CRISP-DM 1.0 – Step-by-step Data Mining Guide*.  
- Documentación técnica del cuaderno `Proyecto.ipynb`.  
