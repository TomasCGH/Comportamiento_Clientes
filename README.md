# Comportamiento de Clientes

## Descripción del proyecto

Este proyecto tiene como objetivo analizar el comportamiento de clientes en campañas de marketing y preparar los datos para tareas de predicción o segmentación. El análisis incluye validación del dataset, limpieza de registros, tratamiento de valores faltantes, normalización de variables categóricas, detección de valores atípicos, creación de variables derivadas y una comparación entre el dataset original y el dataset final listo para análisis.

La base principal del proyecto se encuentra en el archivo `marketing_campaign.csv`, donde se registran atributos demográficos, de ingreso, comportamiento de compra y respuesta del cliente a campañas promocionales.

## Objetivo principal

Comprender patrones de compra y comportamiento del cliente para apoyar decisiones de marketing, con énfasis en:

- Evaluar la calidad y consistencia del dataset.
- Preparar la información para análisis estadístico y modelado predictivo.
- Identificar variables relevantes del comportamiento del cliente.
- Crear indicadores útiles para segmentación y predicción de respuesta.

## Fuente de datos

La información utilizada para el análisis y la posible predicción proviene del archivo:

- `marketing_campaign.csv`

Este dataset incluye variables como:

- Identificación del cliente (`ID`)
- Año de nacimiento (`Year_Birth`)
- Nivel educativo (`Education`)
- Estado civil (`Marital_Status`)
- Ingreso (`Income`)
- Número de hijos en el hogar (`Kidhome`, `Teenhome`)
- Fecha de registro del cliente (`Dt_Customer`)
- Recencia de la última compra (`Recency`)
- Gastos por categoría de productos (`MntWines`, `MntFruits`, `MntMeatProducts`, `MntFishProducts`, `MntSweetProducts`, `MntGoldProds`)
- Número de compras por canal (`NumDealsPurchases`, `NumWebPurchases`, `NumCatalogPurchases`, `NumStorePurchases`)
- Visitas web mensuales (`NumWebVisitsMonth`)
- Respuestas a campañas promocionales (`AcceptedCmp1` a `AcceptedCmp5`, `Response`, `Complain`)

## Estructura del repositorio

```text
Comportamiento_Clientes/
├── marketing_campaign.csv        # Dataset principal con la información del cliente
├── Parcial_estadistica.py        # Script principal de análisis, limpieza y preparación
├── README.md                     # Documentación del proyecto
└── .gitignore                    # Archivos ignorados por Git (si aplica)
```

## Metodología aplicada

El script principal (`Parcial_estadistica.py`) realiza los siguientes procesos:

1. Validación del dataset
   - Verifica número de filas y columnas.
   - Confirma que el conjunto cumple con requisitos mínimos para análisis.

2. Exploración inicial
   - Revisión de tipos de datos.
   - Identificación de valores nulos y duplicados.
   - Resúmenes estadísticos generales.

3. Limpieza de datos
   - Tratamiento de valores faltantes.
   - Imputación por mediana para variables numéricas con sesgo o valores atípicos.
   - Relleno con valores estándar para variables categóricas.
   - Eliminación de duplicados.

4. Corrección de tipos de datos
   - Conversión de fechas.
   - Conversión de columnas numéricas a formato adecuado.

5. Normalización de texto
   - Estandarización de categorías como `Marital_Status`.
   - Reducción de inconsistencias y errores de escritura.

6. Detección y tratamiento de outliers
   - Uso de reglas IQR.
   - Eliminación de valores extremos en `Income` como criterio de robustez.

7. Validación de coherencia
   - Revisión de edades plausibles.
   - Verificación de valores negativos y valores binarios inválidos.

8. Variables derivadas
   - `MntTotal`: gasto total por categoría.
   - `NumTotalPurchases`: total de compras por canal.
   - `TotalChildren`: total de menores en el hogar.

9. Comparación final del dataset
   - Registro del impacto de la limpieza y preparación del dataset.

## Requisitos

Para ejecutar este proyecto, necesitas tener instalado Python 3.x junto con las librerías necesarias. Las principales son:

```bash
pip install pandas numpy
```

## Cómo ejecutar

Desde la raíz del repositorio:

```bash
python Parcial_estadistica.py
```

El script genera una serie de salidas por consola con:

- validación del dataset,
- análisis descriptivo,
- tratamiento de nulos,
- limpieza de duplicados,
- corrección de tipos,
- normalización de variables,
- gestión de outliers,
- variables derivadas,
- comparación final del dataset.

## Variables clave para la predicción

El proyecto se enfoca en variables relevantes para modelar el comportamiento del cliente, entre las más importantes se encuentran:

- `Income`: ingreso del cliente
- `Education`: nivel de educación
- `Marital_Status`: estado civil
- `Recency`: días desde la última compra
- `MntWines`, `MntFruits`, `MntMeatProducts`, `MntFishProducts`, `MntSweetProducts`, `MntGoldProds`: gasto por categoría
- `NumWebPurchases`, `NumCatalogPurchases`, `NumStorePurchases`: compras por canal
- `AcceptedCmp1` a `AcceptedCmp5`, `Response`: respuesta a campañas y conversión

## Resultado esperado

La preparación del dataset permite:

- realizar análisis exploratorio detallado,
- identificar patrones de compra,
- detectar clientes con mayor potencial de respuesta a campañas,
- preparar la información para modelos de clasificación o predicción.

## Consideraciones

Este proyecto se centra principalmente en la etapa de análisis y preparación de datos. La predicción final depende del uso posterior de las variables preparadas para entrenar modelos predictivos de clasificación o regresión.

## Autor

Proyecto desarrollado para análisis estadístico y exploratorio de comportamiento de clientes.

## Licencia

Este repositorio no especifica una licencia en el código actual. Si deseas reutilizarlo públicamente, se recomienda definir una licencia adecuada antes de compartirlo en producción.

---

Si quieres, también puedo dejarte una versión aún más refinada de este README en inglés, o una versión con más enfoque académico/profesional para entregar como proyecto universitario.
