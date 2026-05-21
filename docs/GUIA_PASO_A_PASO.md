# 📘 Guía Paso a Paso: De CSV a Insight

Esta guía te lleva de la mano por todo el proceso. Si nunca has usado S3, Glue o Athena, empieza aquí.

---

## 🔧 Pre-requisitos

- [ ] Cuenta AWS activa y **verificada** (las cuentas nuevas pueden tardar hasta 48 horas en habilitarse)
- [ ] Acceso a la consola de AWS con permisos de administrador
- [ ] Este repositorio clonado o descargado

---

## Paso 1: Configurar Lake Formation (IMPORTANTE)

> ⚠️ **Hacé esto PRIMERO.** Si no, Glue no va a poder crear tablas y vas a ver errores de "Account is denied access".

1. Ve a **AWS Lake Formation** → **Settings** (menú lateral, sección Administration)
2. Marca ambas casillas:
   - ☑️ Use only IAM access control for new databases
   - ☑️ Use only IAM access control for new tables in new databases
3. Click **Save**

Esto le dice a AWS: "Para bases de datos nuevas, usá solo permisos IAM, no Lake Formation". Es más simple y evita conflictos de permisos.

---

## Paso 2: Crear el Bucket S3

1. Ve a **Amazon S3** → **Create bucket**
2. Nombre: `e-commerce-datalake-demo` (o el nombre que prefieras, debe ser único global)
3. Región: `us-east-1` (U.S. East - N. Virginia)
4. Deja todo lo demás por defecto → **Create bucket**

### Crear la estructura de carpetas

Dentro del bucket:
1. Click **Create folder** → nombre: `raw` → Create
2. Dentro de `raw/`, click **Create folder** → nombre: `ventas` → Create

### Subir el CSV

1. Navega a `raw/ventas/`
2. Click **Upload** → **Add files**
3. Selecciona `data/ventas_mayo_2026.csv` de este repositorio
4. Click **Upload**

Tu bucket debería verse así:

```
e-commerce-datalake-demo/
└── raw/
    └── ventas/
        └── ventas_mayo_2026.csv
```

---

## Paso 3: Crear la Política IAM

1. Ve a **IAM** → **Policies** → **Create policy**
2. Click en la pestaña **JSON**
3. Borra todo y pega el contenido de [`iam/policy_crawler.json`](../iam/policy_crawler.json)

> ⚠️ **Importante:** Si tu bucket tiene un nombre diferente, edita las líneas que dicen `e-commerce-datalake-demo` y pon el nombre de tu bucket.

4. Click **Next**
5. Nombre: `PolicyCrawlerDemo`
6. Click **Create policy**

### ¿Qué permisos tiene esta política?

| Permiso | ¿Para qué? |
|---------|-------------|
| `s3:GetObject`, `s3:PutObject`, `s3:ListBucket` | Leer y escribir en tu bucket |
| `glue:*` | Crear tablas, ejecutar crawlers, crear jobs |
| `lakeformation:GetDataAccess` | Permite que Glue acceda a datos (necesario aunque hayas desactivado Lake Formation) |
| `logs:CreateLogGroup`, `logs:PutLogEvents` | Escribir logs de ejecución en CloudWatch |

---

## Paso 4: Crear el Rol IAM

1. Ve a **IAM** → **Roles** → **Create role**
2. **Trusted entity type:** AWS Service
3. **Use case:** Glue (búscalo en el dropdown)
4. Click **Next**
5. Busca y marca: `PolicyCrawlerDemo`
6. Click **Next**
7. Role name: `RolCrawlerDemo`
8. Click **Create role**

### ¿Qué es un Rol?

Un Rol es como un "disfraz" que un servicio de AWS se pone para acceder a otros servicios. Glue se "disfraza" de `RolCrawlerDemo` para poder entrar a tu bucket S3 y escribir en el Data Catalog. Sin este rol, Glue no puede hacer nada.

---

## Paso 5: Crear la Base de Datos en Glue

1. Ve a **AWS Glue** → **Data Catalog** → **Databases**
2. Click **Add database**
3. Name: `ecommerce-db`
4. Click **Create database**

### ¿Qué es una base de datos en Glue?

No es una base de datos tradicional con datos adentro. Es solo un **contenedor lógico** que agrupa tablas. Piensa en ella como una carpeta que organiza las tablas que el Crawler va a crear.

---

## Paso 6: Crear y Ejecutar el Crawler

### Crear el Crawler

1. Ve a **AWS Glue** → **Crawlers** → **Create crawler**
2. **Name:** `crawler-ecommerce`
3. Click **Next**
4. **Data source:** Click **Add a data source**
   - Data store: S3
   - S3 path: `s3://e-commerce-datalake-demo/raw/ventas/`
   - Click **Add an S3 data source**
5. Click **Next**
6. **IAM role:** Selecciona `RolCrawlerDemo`
7. Click **Next**
8. **Target database:** `ecommerce-db`
9. **Table name prefix:** `raw_`
10. Click **Next** → **Create crawler**

### Ejecutar el Crawler

1. Selecciona `crawler-ecommerce`
2. Click **Run crawler**
3. Espera ~1 minuto (el estado cambia de RUNNING a READY)

### ¿Qué hizo el Crawler?

Entró a `s3://e-commerce-datalake-demo/raw/ventas/`, leyó el CSV, detectó:
- 10 columnas: order_id, fecha, cliente, producto, categoria, cantidad, precio_unitario, ciudad, departamento, metodo_pago
- Tipos de datos: strings, doubles, bigints
- Formato: CSV

Y registró toda esa información como una tabla llamada `raw_ventas` en la base de datos `ecommerce-db` del Glue Data Catalog.

---

## Paso 7: Configurar Athena

1. Ve a **Amazon Athena** → **Query Editor**
2. Si es tu primera vez, te pedirá configurar dónde guardar resultados:
   - Click **Settings** → **Manage**
   - Query result location: `s3://e-commerce-datalake-demo/athena-results/`
   - Click **Save**
3. En el panel izquierdo:
   - **Data source:** AwsDataCatalog
   - **Database:** `ecommerce-db`
4. Deberías ver la tabla `raw_ventas` listada

---

## Paso 8: Ejecutar Consultas

Copia y pega las consultas del directorio `queries/` en el editor de Athena.

### Consulta 1: Vista general

```sql
SELECT * FROM raw_ventas LIMIT 10;
```

¿Ves los datos? 🎉 Acabas de consultar un CSV que está en S3 usando SQL, sin instalar nada.

### Consulta 2: Ventas por departamento

```sql
SELECT
    departamento,
    COUNT(*) AS num_ordenes,
    ROUND(SUM(cantidad * precio_unitario), 2) AS total_ventas,
    ROUND(AVG(cantidad * precio_unitario), 2) AS ticket_promedio
FROM raw_ventas
GROUP BY departamento
ORDER BY total_ventas DESC;
```

### Consulta 3: Top 5 productos

```sql
SELECT
    producto, categoria,
    SUM(cantidad) AS unidades_vendidas,
    ROUND(SUM(cantidad * precio_unitario), 2) AS ingresos
FROM raw_ventas
GROUP BY producto, categoria
ORDER BY ingresos DESC
LIMIT 5;
```

### Consulta 4: Métodos de pago

```sql
SELECT
    metodo_pago,
    COUNT(*) AS transacciones,
    ROUND(SUM(cantidad * precio_unitario), 2) AS total,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM raw_ventas), 1) AS porcentaje
FROM raw_ventas
GROUP BY metodo_pago
ORDER BY transacciones DESC;
```

> 💡 **Observa:** Yape y Plin juntos dominan las transacciones. Este insight le sirve al equipo de marketing para decidir qué integraciones de pago priorizar.

---

## Paso 9 (Opcional): ETL con Glue Job

Este paso transforma los datos de CSV a Parquet. No es necesario para consultar, pero optimiza rendimiento y costos.

### ¿Por qué hacerlo?

| | CSV | Parquet |
|-|-----|---------|
| **Formato** | Texto plano (filas) | Columnar (columnas) |
| **Compresión** | Ninguna | Hasta 75% más pequeño |
| **Consulta Athena** | Lee TODO el archivo | Lee solo columnas necesarias |
| **Costo** | $5/TB escaneado (todo) | ~$1.25/TB (solo lo necesario) |

### Crear el Glue Job

1. Ve a **AWS Glue** → **ETL Jobs** → **Script editor**
2. Engine: Spark
3. Pega el contenido de [`scripts/glue_etl_job.py`](../scripts/glue_etl_job.py)
4. En **Job details**:
   - Name: `etl-ventas-ecommerce`
   - IAM Role: `RolCrawlerDemo`
   - Type: Spark
   - Glue version: 4.0
   - Worker type: G.1X
   - Number of workers: 2
5. Click **Save** → **Run**

### ¿Qué hace el script?

1. **Extract:** Lee la tabla `raw_ventas` del Data Catalog
2. **Transform:**
   - Normaliza nombres (juan → Juan)
   - Calcula `total_venta` = cantidad × precio_unitario
   - Convierte fechas al tipo correcto
   - Maneja valores nulos
   - Elimina duplicados
3. **Load:** Guarda como Parquet particionado por departamento en `processed/ventas/`

### Después del ETL

1. Crea un **nuevo Crawler** apuntando a `s3://e-commerce-datalake-demo/processed/ventas/`
2. Ejecútalo
3. Consulta la nueva tabla en Athena
4. Compara el "Data scanned" entre la tabla CSV y la tabla Parquet

---

## 🎯 Resumen: Lo que construiste

```
ventas_mayo_2026.csv
        │
        ▼
   ┌─────────────┐
   │  Amazon S3   │  raw/ventas/
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Glue Crawler  │  Detecta esquema automáticamente
   └──────┬────────┘
          │
          ▼
   ┌──────────────┐
   │ Glue Catalog  │  Tabla: raw_ventas (10 columnas)
   └──────┬────────┘
          │
          ▼
   ┌──────────────┐
   │ Amazon Athena │  SQL directo sobre S3
   └──────┬────────┘
          │
          ▼
   📊 Insights:
      • Lima lidera ventas
      • Tecnología es la categoría top
      • Yape/Plin dominan pagos digitales
      • Tendencia diaria de ventas
```

Todo **serverless**. Sin bases de datos que administrar. Sin servidores que mantener. Pagando solo por lo que usas.
