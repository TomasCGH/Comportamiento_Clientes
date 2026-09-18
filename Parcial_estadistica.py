
import pandas as pd
import numpy as np
import unicodedata

# =========================
# CONFIGURACIÓN BÁSICA
# =========================
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 40)

def imprimir_titulo(titulo):
    print("\n" + "="*80)
    print(titulo)
    print("="*80)

# =========================
# PUNTO 1 DEL PARCIAL
# VALIDAR QUE EL DATASET CUMPLE LOS REQUISITOS
# =========================
# El parcial exige al menos 20 variables combinadas entre categóricas y numéricas
# (sin contar identificadores) y al menos 1000 registros.

# =========================
# PUNTO 2 DEL PARCIAL
# DESCARGAR Y CARGAR DATASET
# =========================
file_path = "marketing_campaign.csv"
df = pd.read_csv(file_path, sep="\t")

imprimir_titulo("PUNTO 1 DEL PARCIAL - VALIDACIÓN DEL DATASET ESCOGIDO")

columnas_numericas_iniciales = df.select_dtypes(include=[np.number]).columns.tolist()
columnas_categoricas_iniciales = df.select_dtypes(include=["object"]).columns.tolist()

num_numericas_sin_id = len([c for c in columnas_numericas_iniciales if c.lower() != "id"])
num_categoricas = len(columnas_categoricas_iniciales)
total_variables_validas = num_numericas_sin_id + num_categoricas

print(f"Número de registros: {df.shape[0]}")
print(f"Número total de columnas: {df.shape[1]}")
print(f"Variables numéricas válidas (sin ID): {num_numericas_sin_id}")
print(f"Variables categóricas: {num_categoricas}")
print(f"Total de variables válidas para el parcial: {total_variables_validas}")

if df.shape[0] >= 1000 and total_variables_validas >= 20:
    print("Conclusión: el dataset SÍ cumple con los requisitos mínimos del parcial.")
else:
    print("Conclusión: el dataset NO cumple con los requisitos mínimos del parcial.")

# =========================
# PUNTO 3 DEL PARCIAL
# EXPLORACIÓN INICIAL
# =========================
imprimir_titulo("PUNTO 3 DEL PARCIAL - EXPLORACIÓN INICIAL")

print("\n" + "="*80)
print("PRIMERAS 5 FILAS DEL DATASET (FORMATO VERTICAL)")
print("="*80)
print(df.head().T.to_string())

print("\n" + "="*80)
print("DIMENSIONES DEL DATASET")
print("="*80)
print(f"Filas: {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")

print("\n" + "="*80)
print("COLUMNAS DEL DATASET")
print("="*80)
print(pd.DataFrame({"Columnas": df.columns}).to_string(index=False))

print("\n" + "="*80)
print("TIPOS DE DATOS")
print("="*80)
print(df.dtypes.reset_index().rename(columns={"index": "Variable", 0: "Tipo"}).to_string(index=False))

print("\n" + "="*80)
print("ESTRUCTURA GENERAL CON .info()")
print("="*80)
df.info()

print("\n" + "="*80)
print("VALORES NULOS POR COLUMNA")
print("="*80)
print(df.isnull().sum().reset_index().rename(columns={"index": "Variable", 0: "Nulos"}).to_string(index=False))

print("\n" + "="*80)
print("CANTIDAD DE DUPLICADOS EXACTOS EN EL DATASET ORIGINAL")
print("="*80)
print(df.duplicated().sum())

print("\n" + "="*80)
print("CANTIDAD DE VALORES ÚNICOS POR COLUMNA")
print("="*80)
print(df.nunique().reset_index().rename(columns={"index": "Variable", 0: "Valores únicos"}).to_string(index=False))

print("\n" + "="*80)
print("RESUMEN ESTADÍSTICO DE VARIABLES NUMÉRICAS")
print("="*80)
print(df.describe().T.to_string())

print("\n" + "="*80)
print("RESUMEN DE VARIABLES CATEGÓRICAS")
print("="*80)
print(df.describe(include=["object"]).T.to_string())

# =========================
# PUNTO 4 DEL PARCIAL
# MANEJO DE VALORES NULOS
# =========================
print("\n" + "="*80)
print("PUNTO 4 DEL PARCIAL - MANEJO DE VALORES NULOS")
print("="*80)

# =========================
# PASO 2: VALORES NULOS
# =========================
print("\n" + "="*80)
print("VALORES NULOS POR COLUMNA")
print("="*80)

nulos = df.isnull().sum()
porcentaje_nulos = (df.isnull().sum() / len(df)) * 100

tabla_nulos = pd.DataFrame({
    "Variable": df.columns,
    "Nulos": nulos.values,
    "Porcentaje_nulos": porcentaje_nulos.values
}).sort_values(by="Porcentaje_nulos", ascending=False)

print(tabla_nulos.to_string(index=False))

# 1. ELIMINAR COLUMNAS CON MÁS DEL 50% DE NULOS
columnas_mas_50 = tabla_nulos[tabla_nulos["Porcentaje_nulos"] > 50]["Variable"].tolist()

print("\n" + "="*80)
print("COLUMNAS CON MÁS DEL 50% DE NULOS")
print("="*80)
print(columnas_mas_50 if len(columnas_mas_50)
       > 0 else "No hay columnas con más del 50% de nulos")

df_limpio = df.copy()
if len(columnas_mas_50) > 0:
    df_limpio = df_limpio.drop(columns=columnas_mas_50)

# 2. ANÁLISIS DE INCOME ANTES DE IMPUTAR
if "Income" in df_limpio.columns:
    print("\n" + "="*80)
    print("ANÁLISIS DE LA VARIABLE INCOME")
    print("="*80)

    income = df_limpio["Income"]

    media_income = income.mean()
    mediana_income = income.median()
    moda_income = income.mode().iloc[0] if not income.mode().empty else np.nan
    asimetria_income = income.skew()

    Q1 = income.quantile(0.25)
    Q3 = income.quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5 * IQR
    lim_sup = Q3 + 1.5 * IQR
    outliers_income = income[(income < lim_inf) | (income > lim_sup)].count()

    print(f"Nulos en Income: {income.isnull().sum()}")
    print(f"Media de Income: {media_income:.2f}")
    print(f"Mediana de Income: {mediana_income:.2f}")
    print(f"Moda de Income: {moda_income:.2f}")
    print(f"Asimetría de Income: {asimetria_income:.2f}")
    print(f"Cantidad de outliers en Income (IQR): {outliers_income}")

    print("\nJustificación de la decisión:")
    if abs(asimetria_income) > 1 or outliers_income > 0:
        print("- Income presenta asimetría y/o valores extremos.")
        print("- En estas condiciones, la media puede verse afectada por observaciones atípicas.")
        print("- Por ello se decide imputar con la mediana, ya que es una medida más robusta.")
    else:
        print("- Income no muestra una asimetría severa ni exceso de valores extremos.")
        print("- Aun así, se mantiene la mediana como criterio conservador en variables monetarias.")

    df_limpio["Income"] = df_limpio["Income"].fillna(mediana_income)

    print("\nResultado de la imputación:")
    print(f"Se imputó Income con la mediana: {mediana_income:.2f}")

# 3. RELLENAR CATEGÓRICAS CON 'desconocido' SI HAY NULOS
columnas_categoricas = df_limpio.select_dtypes(include=["object"]).columns

for col in columnas_categoricas:
    if df_limpio[col].isnull().sum() > 0:
        df_limpio[col] = df_limpio[col].fillna("desconocido")
        print(f"En la columna {col} los nulos se reemplazaron por 'desconocido'")

# 4. REVISIÓN FINAL DE NULOS
print("\n" + "="*80)
print("VALORES NULOS DESPUÉS DEL TRATAMIENTO")
print("="*80)

tabla_nulos_final = pd.DataFrame({
    "Variable": df_limpio.columns,
    "Nulos": df_limpio.isnull().sum().values,
    "Porcentaje_nulos": ((df_limpio.isnull().sum() / len(df_limpio)) * 100).values
}).sort_values(by="Porcentaje_nulos", ascending=False)

print(tabla_nulos_final.to_string(index=False))

# =========================
# PUNTO 5 DEL PARCIAL
# TRATAMIENTO DE DUPLICADOS
# =========================
print("\n" + "="*80)
print("PUNTO 5 DEL PARCIAL - TRATAMIENTO DE DUPLICADOS")
print("="*80)

# =========================
# PASO 3: DUPLICADOS
# =========================
print("\n" + "="*80)
print("REVISIÓN DE DUPLICADOS")
print("="*80)

duplicados_exactos = df_limpio.duplicated().sum()
print(f"Cantidad de filas duplicadas exactas: {duplicados_exactos}")

if duplicados_exactos > 0:
    print("\nSe encontraron duplicados exactos.")
    print("Decisión: eliminarlos, porque representan la misma observación repetida y pueden sesgar el análisis.")
    df_limpio = df_limpio.drop_duplicates()
    print(f"Filas después de eliminar duplicados exactos: {df_limpio.shape[0]}")
else:
    print("\nNo se encontraron duplicados exactos.")
    print("Decisión: no se elimina ninguna fila por este criterio.")

if "ID" in df_limpio.columns:
    duplicados_id = df_limpio["ID"].duplicated().sum()

    print("\n" + "="*80)
    print("REVISIÓN DE ID REPETIDOS")
    print("="*80)
    print(f"Cantidad de IDs repetidos: {duplicados_id}")

    if duplicados_id > 0:
        print("Se encontraron IDs repetidos.")
        print("Decisión: no eliminarlos automáticamente sin revisar, porque podrían no ser duplicados exactos.")
        print("Registros con ID repetido:")
        print(df_limpio[df_limpio["ID"].duplicated(keep=False)].sort_values("ID").T.to_string())
    else:
        print("No se encontraron IDs repetidos.")

# =========================
# PUNTO 6 DEL PARCIAL
# CORRECCIÓN DE TIPOS DE DATOS
# =========================
print("\n" + "="*80)
print("PUNTO 6 DEL PARCIAL - CORRECCIÓN DE TIPOS DE DATOS")
print("="*80)

# =========================
# PASO 4: CORRECCIÓN DE TIPOS DE DATOS
# =========================
print("\n" + "="*80)
print("TIPOS DE DATOS ANTES DE LA CORRECCIÓN")
print("="*80)
print(df_limpio.dtypes.reset_index().rename
      (columns={"index": "Variable", 0: "Tipo"}).to_string(index=False))

if "Dt_Customer" in df_limpio.columns:
    df_limpio["Dt_Customer"] = pd.to_datetime(
        df_limpio["Dt_Customer"],
        format="%d-%m-%Y",
        errors="coerce"
    )

columnas_numericas = [
    "Year_Birth", "Income", "Kidhome", "Teenhome", "Recency",
    "MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts",
    "MntSweetProducts", "MntGoldProds", "NumDealsPurchases",
    "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases",
    "NumWebVisitsMonth", "AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
    "AcceptedCmp4", "AcceptedCmp5", "Complain", "Z_CostContact",
    "Z_Revenue", "Response"
]

for col in columnas_numericas:
    if col in df_limpio.columns:
        df_limpio[col] = pd.to_numeric(df_limpio[col], errors="coerce")

print("\n" + "="*80)
print("TIPOS DE DATOS DESPUÉS DE LA CORRECCIÓN")
print("="*80)
print(df_limpio.dtypes.reset_index().rename(columns={"index": "Variable", 0: "Tipo"}).to_string(index=False))

print("\n" + "="*80)
print("NULOS DESPUÉS DE CORREGIR TIPOS")
print("="*80)
print(df_limpio.isnull().sum().reset_index().rename(columns={"index": "Variable", 0: "Nulos"}).to_string(index=False))

# =========================
# REVISIÓN DE MARITAL_STATUS
# =========================
print("\n" + "="*80)
print("FRECUENCIAS DE MARITAL_STATUS")
print("="*80)

frecuencia_marital = df_limpio["Marital_Status"].value_counts(dropna=False)
porcentaje_marital = df_limpio["Marital_Status"].value_counts(normalize=True, dropna=False) * 100

tabla_marital = pd.DataFrame({
    "Frecuencia": frecuencia_marital,
    "Porcentaje": porcentaje_marital
})

print(tabla_marital.to_string())

print("\n" + "="*80)
print("FRECUENCIA ESPECÍFICA DE 'Absurd' Y 'YOLO'")
print("="*80)
print("Absurd:", (df_limpio["Marital_Status"] == "Absurd").sum())
print("YOLO:", (df_limpio["Marital_Status"] == "YOLO").sum())

# =========================
# PUNTO 7 DEL PARCIAL
# NORMALIZACIÓN DE VALORES CATEGÓRICOS
# =========================
print("\n" + "="*80)
print("PUNTO 7 DEL PARCIAL - NORMALIZACIÓN DE VALORES CATEGÓRICOS")
print("="*80)

# =========================
# PASO 5: NORMALIZACIÓN DE VALORES CATEGÓRICOS
# =========================
print("\n" + "="*80)
print("VALORES ÚNICOS ANTES DE NORMALIZAR")
print("="*80)

columnas_categoricas = df_limpio.select_dtypes(include=["object"]).columns

for col in columnas_categoricas:
    print(f"\n{col}:")
    print(sorted(df_limpio[col].dropna().unique()))

for col in columnas_categoricas:
    df_limpio[col] = (
        df_limpio[col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

if "Marital_Status" in df_limpio.columns:
    df_limpio["Marital_Status"] = df_limpio["Marital_Status"].replace({
        "alone": "single",
        "absurd": "other",
        "yolo": "other"
    })

print("\n" + "="*80)
print("VALORES ÚNICOS DESPUÉS DE NORMALIZAR")
print("="*80)

for col in columnas_categoricas:
    print(f"\n{col}:")
    print(sorted(df_limpio[col].dropna().unique()))

# =========================
# PUNTO 8 DEL PARCIAL
# ELIMINAR VALORES ATÍPICOS (OUTLIERS)
# =========================
print("\n" + "="*80)
print("PUNTO 8 DEL PARCIAL - ELIMINAR VALORES ATÍPICOS (OUTLIERS)")
print("="*80)

# =========================
# PASO 6: OUTLIERS CON IQR
# =========================
print("\n" + "="*80)
print("DETECCIÓN DE OUTLIERS CON MÉTODO IQR")
print("="*80)

excluir = ["ID", "Year_Birth", "Z_CostContact", "Z_Revenue"]
binarias = [
    "AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
    "AcceptedCmp4", "AcceptedCmp5", "Complain", "Response"
]

columnas_numericas_detectar = df_limpio.select_dtypes(include=[np.number]).columns.tolist()
columnas_outliers = [col for col in columnas_numericas_detectar if col not in excluir + binarias]

resumen_outliers = []

for col in columnas_outliers:
    Q1 = df_limpio[col].quantile(0.25)
    Q3 = df_limpio[col].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5 * IQR
    lim_sup = Q3 + 1.5 * IQR

    n_outliers = df_limpio[(df_limpio[col] < lim_inf) | (df_limpio[col] > lim_sup)].shape[0]

    resumen_outliers.append({
        "Variable": col,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "Límite_inferior": lim_inf,
        "Límite_superior": lim_sup,
        "Cantidad_outliers": n_outliers
    })

tabla_outliers = pd.DataFrame(resumen_outliers).sort_values(by="Cantidad_outliers", ascending=False)
print(tabla_outliers.to_string(index=False))

print("\n" + "="*80)
print("TRATAMIENTO DE OUTLIERS")
print("="*80)
print("Decisión: eliminar outliers únicamente en 'Income'.")
print("Justificación:")
print("- En 'Income', los valores extremos pueden sesgar medidas como la media y la desviación estándar.")
print("- 'Year_Birth' no se trata aquí, sino en coherencia de datos, porque allí interesa más la plausibilidad del dato.")
print("- No se eliminan outliers de variables de gasto, porque un valor alto puede representar un cliente real de alto consumo.")

filas_antes_outliers = df_limpio.shape[0]

if "Income" in df_limpio.columns:
    Q1_income = df_limpio["Income"].quantile(0.25)
    Q3_income = df_limpio["Income"].quantile(0.75)
    IQR_income = Q3_income - Q1_income
    lim_inf_income = Q1_income - 1.5 * IQR_income
    lim_sup_income = Q3_income + 1.5 * IQR_income

    df_limpio = df_limpio[
        (df_limpio["Income"] >= lim_inf_income) &
        (df_limpio["Income"] <= lim_sup_income)
    ].copy()

    print(f"\nLímite inferior de Income: {lim_inf_income:.2f}")
    print(f"Límite superior de Income: {lim_sup_income:.2f}")

filas_despues_outliers = df_limpio.shape[0]

print(f"\nFilas antes de eliminar outliers: {filas_antes_outliers}")
print(f"Filas después de eliminar outliers: {filas_despues_outliers}")
print(f"Filas eliminadas por outliers en Income: {filas_antes_outliers - filas_despues_outliers}")

# =========================
# PUNTO 9 DEL PARCIAL
# VALIDACIÓN DE COHERENCIA
# =========================
print("\n" + "="*80)
print("PUNTO 9 DEL PARCIAL - VALIDACIÓN DE LA COHERENCIA DE LOS DATOS")
print("="*80)

# =========================
# PASO 7: VALIDACIÓN DE COHERENCIA
# =========================
print("\n" + "="*80)
print("VALIDACIÓN DE COHERENCIA DE LOS DATOS")
print("="*80)

# Regla 1: Year_Birth no puede ser mayor al año máximo observado en Dt_Customer
anio_max_registro = df_limpio["Dt_Customer"].dt.year.max()
regla_nacimiento = df_limpio["Year_Birth"] <= anio_max_registro

# Regla 2: eliminar los valores de Year_Birth que generan edades no plausibles (>100)
regla_year_birth_plausible = df_limpio["Year_Birth"] >= (anio_max_registro - 100)

columnas_no_negativas = [
    "Income", "Kidhome", "Teenhome", "Recency",
    "MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts",
    "MntSweetProducts", "MntGoldProds", "NumDealsPurchases",
    "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases",
    "NumWebVisitsMonth"
]

for col in columnas_no_negativas:
    print(f"Valores negativos en {col}: {(df_limpio[col] < 0).sum()}")

columnas_binarias = [
    "AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
    "AcceptedCmp4", "AcceptedCmp5", "Complain", "Response"
]

for col in columnas_binarias:
    invalidos = (~df_limpio[col].isin([0, 1])).sum()
    print(f"Valores inválidos en {col}: {invalidos}")

print("\n" + "="*80)
print("INCUMPLIMIENTOS DE REGLAS LÓGICAS")
print("="*80)
print(f"Años de nacimiento posteriores al rango válido: {(~regla_nacimiento).sum()}")
print(f"Años de nacimiento no plausibles (más de 100 años antes del último registro): {(~regla_year_birth_plausible).sum()}")

print("\n" + "="*80)
print("VALORES MÍNIMOS Y MÁXIMOS DE VARIABLES NUMÉRICAS")
print("="*80)

resumen_rangos = pd.DataFrame({
    "Variable": df_limpio.select_dtypes(include=[np.number]).columns,
    "Minimo": df_limpio.select_dtypes(include=[np.number]).min().values,
    "Maximo": df_limpio.select_dtypes(include=[np.number]).max().values
})

print(resumen_rangos.to_string(index=False))

filas_antes_validacion = df_limpio.shape[0]

condicion_final = regla_nacimiento & regla_year_birth_plausible

for col in columnas_no_negativas:
    condicion_final = condicion_final & (df_limpio[col] >= 0)

for col in columnas_binarias:
    condicion_final = condicion_final & (df_limpio[col].isin([0, 1]))

df_limpio = df_limpio[condicion_final].copy()

filas_despues_validacion = df_limpio.shape[0]

print("\n" + "="*80)
print("RESULTADO DE LA VALIDACIÓN")
print("="*80)
print(f"Filas antes de validar coherencia: {filas_antes_validacion}")
print(f"Filas después de validar coherencia: {filas_despues_validacion}")
print(f"Filas eliminadas por incoherencia: {filas_antes_validacion - filas_despues_validacion}")

# =========================
# PUNTO 10 DEL PARCIAL
# VARIABLES DERIVADAS
# =========================
print("\n" + "="*80)
print("PUNTO 10 DEL PARCIAL - CREACIÓN DE VARIABLES DERIVADAS")
print("="*80)

# =========================
# PASO 8: VARIABLES DERIVADAS
# =========================
print("\n" + "="*80)
print("CREACIÓN DE VARIABLES DERIVADAS")
print("="*80)

df_limpio["MntTotal"] = (
    df_limpio["MntWines"] +
    df_limpio["MntFruits"] +
    df_limpio["MntMeatProducts"] +
    df_limpio["MntFishProducts"] +
    df_limpio["MntSweetProducts"] +
    df_limpio["MntGoldProds"]
)

print("\nVariable creada: MntTotal")
print("Significa: gasto total del cliente en todas las categorías de productos.")

df_limpio["NumTotalPurchases"] = (
    df_limpio["NumDealsPurchases"] +
    df_limpio["NumWebPurchases"] +
    df_limpio["NumCatalogPurchases"] +
    df_limpio["NumStorePurchases"]
)

print("\nVariable creada: NumTotalPurchases")
print("Significa: número total de compras realizadas por el cliente en todos los canales.")

df_limpio["TotalChildren"] = df_limpio["Kidhome"] + df_limpio["Teenhome"]

print("\nVariable creada: TotalChildren")
print("Significa: número total de hijos o menores en el hogar del cliente.")

print("\n" + "="*80)
print("PRIMERAS FILAS CON VARIABLES DERIVADAS")
print("="*80)

columnas_mostrar = ["ID", "MntTotal", "NumTotalPurchases", "TotalChildren"]
print(df_limpio[columnas_mostrar].head().to_string(index=False))

# =========================
# ENTREGA DEL PARCIAL
# COMPARACIÓN DATASET INICIAL VS FINAL
# =========================
print("\n" + "="*80)
print("COMPARACIÓN DEL DATASET INICIAL VS FINAL")
print("="*80)

filas_inicial, columnas_inicial = df.shape
filas_final, columnas_final = df_limpio.shape

nulos_inicial = df.isnull().sum().sum()
nulos_final = df_limpio.isnull().sum().sum()

duplicados_inicial = df.duplicated().sum()
duplicados_final = df_limpio.duplicated().sum()

variables_nuevas = [col for col in df_limpio.columns if col not in df.columns]
columnas_eliminadas_total = max(0, columnas_inicial - columnas_final)

comparacion = pd.DataFrame({
    "Indicador": [
        "Número de filas",
        "Número de columnas",
        "Total de valores nulos",
        "Filas duplicadas exactas"
    ],
    "Dataset inicial": [
        filas_inicial,
        columnas_inicial,
        nulos_inicial,
        duplicados_inicial
    ],
    "Dataset final": [
        filas_final,
        columnas_final,
        nulos_final,
        duplicados_final
    ]
})

print(comparacion.to_string(index=False))

print("\n" + "="*80)
print("CAMBIOS REALIZADOS")
print("="*80)
print(f"Filas eliminadas en total: {filas_inicial - filas_final}")
print(f"Columnas eliminadas en total: {columnas_eliminadas_total}")
print(f"Variables derivadas creadas: {variables_nuevas if len(variables_nuevas) > 0 else 'Ninguna'}")

print("\n" + "="*80)
print("COLUMNAS FINALES DEL DATASET")
print("="*80)
print(pd.DataFrame({"Columnas finales": df_limpio.columns}).to_string(index=False))

# =============================================================================
# BLOQUE FINAL ADICIONAL
# DEMOSTRACIONES DE PROCEDIMIENTOS QUE EL PARCIAL PIDE
# AUNQUE NO SE PRESENTEN EN EL DATASET REAL
# =============================================================================
imprimir_titulo("ANEXO DEMOSTRATIVO - PROCEDIMIENTOS EXIGIDOS POR EL PARCIAL QUE NO SE DIERON EN EL DATASET REAL")

print("Este bloque NO altera df_limpio.")
print("Se trabaja sobre una copia auxiliar para demostrar que los procedimientos sí fueron implementados.")

df_demo = df.copy()

# -------------------------------------------------------------------------
# DEMOSTRACIÓN 1: COLUMNA CON MÁS DEL 50% DE NULOS
# -------------------------------------------------------------------------
imprimir_titulo("ANEXO 1 - DEMOSTRACIÓN DE COLUMNA CON MÁS DEL 50% DE NULOS")

df_demo["Columna_50_nulos_demo"] = pd.Series([None] * len(df_demo), dtype="object")
idx_no_nulos = np.random.choice(df_demo.index, size=int(len(df_demo) * 0.30), replace=False)
df_demo.loc[idx_no_nulos, "Columna_50_nulos_demo"] = "valor_demo"

nulos_demo = df_demo.isnull().sum()
porcentaje_nulos_demo = (df_demo.isnull().sum() / len(df_demo)) * 100

tabla_nulos_demo = pd.DataFrame({
    "Variable": df_demo.columns,
    "Nulos": nulos_demo.values,
    "Porcentaje_nulos": porcentaje_nulos_demo.values
}).sort_values(by="Porcentaje_nulos", ascending=False)

print(tabla_nulos_demo.to_string(index=False))

columnas_mas_50_demo = tabla_nulos_demo[tabla_nulos_demo["Porcentaje_nulos"] > 50]["Variable"].tolist()

print("\nColumnas con más del 50% de nulos (demostración):")
print(columnas_mas_50_demo if len(columnas_mas_50_demo) > 0 else "No hay columnas con más del 50% de nulos")

df_demo_sin_50 = df_demo.copy()
if len(columnas_mas_50_demo) > 0:
    df_demo_sin_50 = df_demo_sin_50.drop(columns=columnas_mas_50_demo)
    print("Se aplicó correctamente el borrado de columnas con más del 50% de nulos.")

# -------------------------------------------------------------------------
# DEMOSTRACIÓN 2: ELIMINAR REGISTROS INCOMPLETOS
# -------------------------------------------------------------------------
imprimir_titulo("ANEXO 2 - DEMOSTRACIÓN DE ELIMINACIÓN DE REGISTROS INCOMPLETOS")

df_demo_dropna = df.copy()
idx_incompletos = np.random.choice(df_demo_dropna.index, size=6, replace=False)
df_demo_dropna.loc[idx_incompletos[:2], "Income"] = np.nan
df_demo_dropna.loc[idx_incompletos[2:4], "Education"] = np.nan
df_demo_dropna.loc[idx_incompletos[4:], "Marital_Status"] = np.nan

filas_antes_dropna = df_demo_dropna.shape[0]
df_demo_dropna_limpio = df_demo_dropna.dropna()
filas_despues_dropna = df_demo_dropna_limpio.shape[0]

print(f"Filas antes de eliminar registros incompletos: {filas_antes_dropna}")
print(f"Filas después de eliminar registros incompletos: {filas_despues_dropna}")
print(f"Filas eliminadas con dropna(): {filas_antes_dropna - filas_despues_dropna}")

# -------------------------------------------------------------------------
# DEMOSTRACIÓN 3: IMPUTAR CON MEDIA
# -------------------------------------------------------------------------
imprimir_titulo("ANEXO 3 - DEMOSTRACIÓN DE IMPUTACIÓN CON MEDIA")

df_demo_media = df.copy()
idx_media = np.random.choice(df_demo_media.index, size=5, replace=False)
df_demo_media.loc[idx_media, "Income"] = np.nan

print(f"Nulos en Income antes de imputar con media: {df_demo_media['Income'].isnull().sum()}")
media_demo = df_demo_media["Income"].mean()
df_demo_media["Income"] = df_demo_media["Income"].fillna(media_demo)
print(f"Media usada para imputar Income: {media_demo:.2f}")
print(f"Nulos en Income después de imputar con media: {df_demo_media['Income'].isnull().sum()}")

# -------------------------------------------------------------------------
# DEMOSTRACIÓN 4: IMPUTAR CON MODA
# -------------------------------------------------------------------------
imprimir_titulo("ANEXO 4 - DEMOSTRACIÓN DE IMPUTACIÓN CON MODA")

df_demo_moda = df.copy()
idx_moda = np.random.choice(df_demo_moda.index, size=5, replace=False)
df_demo_moda.loc[idx_moda, "Education"] = np.nan

print(f"Nulos en Education antes de imputar con moda: {df_demo_moda['Education'].isnull().sum()}")
moda_demo = df_demo_moda["Education"].mode().iloc[0]
df_demo_moda["Education"] = df_demo_moda["Education"].fillna(moda_demo)
print(f"Moda usada para imputar Education: {moda_demo}")
print(f"Nulos en Education después de imputar con moda: {df_demo_moda['Education'].isnull().sum()}")

# -------------------------------------------------------------------------
# DEMOSTRACIÓN 5: SUSTITUIR POR UN VALOR ESPECÍFICO
# -------------------------------------------------------------------------
imprimir_titulo("ANEXO 5 - DEMOSTRACIÓN DE SUSTITUCIÓN POR VALOR ESPECÍFICO")

df_demo_valor = df.copy()
idx_valor = np.random.choice(df_demo_valor.index, size=5, replace=False)
df_demo_valor.loc[idx_valor, "Marital_Status"] = np.nan

print(f"Nulos en Marital_Status antes: {df_demo_valor['Marital_Status'].isnull().sum()}")
df_demo_valor["Marital_Status"] = df_demo_valor["Marital_Status"].fillna("desconocido")
print("Se reemplazaron los nulos de Marital_Status por 'desconocido'.")
print(f"Nulos en Marital_Status después: {df_demo_valor['Marital_Status'].isnull().sum()}")

# -------------------------------------------------------------------------
# DEMOSTRACIÓN 6: CREAR Y ELIMINAR DUPLICADOS
# -------------------------------------------------------------------------
imprimir_titulo("ANEXO 6 - DEMOSTRACIÓN DE IDENTIFICACIÓN Y ELIMINACIÓN DE DUPLICADOS")

df_demo_dup = df.copy()
fila_duplicada = df_demo_dup.iloc[[0]].copy()
df_demo_dup = pd.concat([df_demo_dup, fila_duplicada], ignore_index=True)

duplicados_exactos_demo = df_demo_dup.duplicated().sum()
print(f"Cantidad de duplicados exactos creados en la demostración: {duplicados_exactos_demo}")

filas_antes_dup = df_demo_dup.shape[0]
df_demo_dup = df_demo_dup.drop_duplicates()
filas_despues_dup = df_demo_dup.shape[0]

print(f"Filas antes de eliminar duplicados: {filas_antes_dup}")
print(f"Filas después de eliminar duplicados: {filas_despues_dup}")
print(f"Duplicados eliminados: {filas_antes_dup - filas_despues_dup}")

# -------------------------------------------------------------------------
# DEMOSTRACIÓN 7: UNIFICAR FORMATOS DE FECHA
# -------------------------------------------------------------------------
imprimir_titulo("ANEXO 7 - DEMOSTRACIÓN DE UNIFICACIÓN DE FORMATOS DE FECHA")

df_demo_fecha = df.copy()
df_demo_fecha.loc[df_demo_fecha.index[0], "Dt_Customer"] = "2014/08/15"
df_demo_fecha.loc[df_demo_fecha.index[1], "Dt_Customer"] = "15-08-2014"

print("Valores de fecha antes de la conversión:")
print(df_demo_fecha.loc[[0, 1], ["Dt_Customer"]].to_string(index=False))

fechas_demo = pd.to_datetime(df_demo_fecha["Dt_Customer"], format="%d-%m-%Y", errors="coerce")
mask_na = fechas_demo.isna()
fechas_demo.loc[mask_na] = pd.to_datetime(df_demo_fecha.loc[mask_na, "Dt_Customer"], errors="coerce")
df_demo_fecha["Dt_Customer"] = fechas_demo

print("\nValores de fecha después de la conversión:")
print(df_demo_fecha.loc[[0, 1], ["Dt_Customer"]].to_string(index=False))

# -------------------------------------------------------------------------
# DEMOSTRACIÓN 8: CORREGIR CARACTERES ESPECIALES Y MALAS DIGITACIONES
# -------------------------------------------------------------------------
imprimir_titulo("ANEXO 8 - DEMOSTRACIÓN DE CORRECCIÓN DE TEXTO, TILDES Y MALAS DIGITACIONES")

def quitar_tildes(texto):
    if pd.isna(texto):
        return texto
    texto = str(texto)
    return ''.join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )

df_demo_texto = df.copy()
df_demo_texto.loc[df_demo_texto.index[0], "Marital_Status"] = " Single "
df_demo_texto.loc[df_demo_texto.index[1], "Marital_Status"] = "SINGLE"
df_demo_texto.loc[df_demo_texto.index[2], "Marital_Status"] = "singlé"
df_demo_texto.loc[df_demo_texto.index[3], "Marital_Status"] = "yol0"
df_demo_texto.loc[df_demo_texto.index[4], "Marital_Status"] = "Absürd"

print("Valores antes de normalizar:")
print(sorted(df_demo_texto["Marital_Status"].dropna().astype(str).unique()))

df_demo_texto["Marital_Status"] = (
    df_demo_texto["Marital_Status"]
    .astype(str)
    .str.strip()
    .str.lower()
    .apply(quitar_tildes)
)

df_demo_texto["Marital_Status"] = df_demo_texto["Marital_Status"].replace({
    "alone": "single",
    "absurd": "other",
    "yolo": "other",
    "yol0": "other",
    "single": "single"
})

print("\nValores después de normalizar:")
print(sorted(df_demo_texto["Marital_Status"].dropna().astype(str).unique()))

# -------------------------------------------------------------------------
# CIERRE
# -------------------------------------------------------------------------
imprimir_titulo("CIERRE METODOLÓGICO")
print("1. El bloque principal conserva tu código original y produce el dataset final real.")
print("2. El bloque final adicional demuestra procedimientos pedidos por el parcial")
print("   aunque no se presenten naturalmente en el dataset.")
print("3. Así puedes defender que implementaste todos los puntos solicitados sin alterar")
print("   la limpieza real del dataset.")