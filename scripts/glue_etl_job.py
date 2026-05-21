"""
AWS Glue ETL Job: Transformación de ventas e-commerce
=====================================================

Este script lee los datos crudos (CSV) desde la zona raw/ de S3,
los limpia, transforma, y guarda como Parquet en la zona processed/.

¿Por qué hacer esto?
- CSV es texto plano → Parquet es columnar y comprimido
- Con Parquet, Athena lee solo las columnas que necesitas
- Particionado por departamento → Athena escanea solo lo necesario
- Resultado: consultas más rápidas y hasta 75% más baratas

Cómo ejecutarlo:
- Crear un Glue Job en la consola de AWS
- Copiar este script en el editor
- Seleccionar el rol IAM con permisos a S3 y Glue
- Ejecutar el job

Nota: Este script usa el Glue Data Catalog para leer la tabla
que el Crawler ya creó. Si prefieres, puedes leer directo de S3.
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, upper, initcap, round as spark_round, to_date, when, lit

# ============================================
# CONFIGURACIÓN
# ============================================
BUCKET = "e-commerce-datalake-demo"
DATABASE = "ecommerce-db"
TABLE = "raw_ventas"
OUTPUT_PATH = f"s3://{BUCKET}/processed/ventas/"

# ============================================
# INICIALIZACIÓN
# ============================================
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ============================================
# PASO 1: EXTRACT — Leer datos crudos
# ============================================
# Lee la tabla del Glue Data Catalog (creada por el Crawler)
print("=" * 60)
print("📥 EXTRACT: Leyendo datos crudos desde el catálogo...")
print("=" * 60)

datasource = glueContext.create_dynamic_frame.from_catalog(
    database=DATABASE,
    table_name=TABLE
)

df = datasource.toDF()

print(f"✅ Registros leídos: {df.count()}")
print(f"📊 Columnas: {df.columns}")
print(f"📋 Esquema:")
df.printSchema()

# Alternativa: leer directo desde S3 sin usar el catálogo
# df = spark.read.option("header", "true").option("inferSchema", "true") \
#     .csv(f"s3://{BUCKET}/raw/ventas/")

# ============================================
# PASO 2: TRANSFORM — Limpiar y enriquecer
# ============================================
print("=" * 60)
print("🔧 TRANSFORM: Limpiando y enriqueciendo datos...")
print("=" * 60)

# --- 2.1 Normalizar nombres de clientes ---
# "juan pérez" → "Juan Pérez"
df_limpio = df.withColumn("cliente", initcap(col("cliente")))

# --- 2.2 Normalizar departamentos ---
# Asegurar que estén en formato título
df_limpio = df_limpio.withColumn("departamento", initcap(col("departamento")))
df_limpio = df_limpio.withColumn("ciudad", initcap(col("ciudad")))

# --- 2.3 Calcular campo total_venta ---
# cantidad * precio_unitario = lo que pagó el cliente
df_limpio = df_limpio.withColumn(
    "total_venta",
    spark_round(col("cantidad") * col("precio_unitario"), 2)
)

# --- 2.4 Asegurar tipos de datos correctos ---
df_limpio = df_limpio.withColumn(
    "fecha", to_date(col("fecha"), "yyyy-MM-dd")
)

# --- 2.5 Manejar valores nulos ---
# Si precio_unitario es null, poner 0
df_limpio = df_limpio.withColumn(
    "precio_unitario",
    when(col("precio_unitario").isNull(), lit(0))
    .otherwise(col("precio_unitario"))
)

# --- 2.6 Eliminar duplicados ---
df_limpio = df_limpio.dropDuplicates(["order_id"])

# --- 2.7 Eliminar registros sin datos críticos ---
df_limpio = df_limpio.dropna(subset=["order_id", "producto", "precio_unitario"])

print(f"✅ Registros después de limpieza: {df_limpio.count()}")
print(f"📊 Nuevas columnas: {df_limpio.columns}")
print(f"\n📋 Muestra de datos limpios:")
df_limpio.show(5, truncate=False)

# ============================================
# PASO 3: LOAD — Guardar como Parquet
# ============================================
print("=" * 60)
print("💾 LOAD: Guardando como Parquet particionado...")
print("=" * 60)

df_limpio.write \
    .mode("overwrite") \
    .partitionBy("departamento") \
    .parquet(OUTPUT_PATH)

print(f"✅ ¡Datos guardados exitosamente!")
print(f"📂 Ubicación: {OUTPUT_PATH}")
print(f"📁 Particionado por: departamento")
print(f"")
print(f"Estructura resultante en S3:")
print(f"  processed/ventas/")
print(f"    ├── departamento=Arequipa/")
print(f"    │   └── part-00000.snappy.parquet")
print(f"    ├── departamento=Cusco/")
print(f"    │   └── part-00000.snappy.parquet")
print(f"    ├── departamento=La Libertad/")
print(f"    │   └── part-00000.snappy.parquet")
print(f"    ├── departamento=Lambayeque/")
print(f"    │   └── part-00000.snappy.parquet")
print(f"    ├── departamento=Lima/")
print(f"    │   └── part-00000.snappy.parquet")
print(f"    └── departamento=Piura/")
print(f"        └── part-00000.snappy.parquet")
print(f"")
print(f"🎯 Siguiente paso:")
print(f"   1. Ejecutar un nuevo Crawler apuntando a processed/ventas/")
print(f"   2. Consultar la nueva tabla en Athena")
print(f"   3. Comparar el 'Data scanned' entre CSV y Parquet")

job.commit()
