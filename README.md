# 🚀 El Viaje de tus Datos en AWS: De la Ingesta al Análisis

> **Nivel:** 100-200 (Principiante) | **Servicios:** Amazon S3, AWS Glue, Amazon Athena  
> **Tiempo del demo:** ~15 minutos | **Costo estimado:** < $0.05 USD

## 🎯 ¿Qué es esto?

Un laboratorio práctico que simula un caso real de **e-commerce** en Perú. Vas a construir un pipeline de datos completo en AWS — desde un CSV con órdenes de venta hasta consultas SQL que generan insights de negocio — sin levantar un solo servidor.

```
📦 CSV de ventas  →  🪣 Amazon S3  →  🤖 Glue Crawler  →  🔍 Amazon Athena  →  📊 Insights
```

### La analogía que lo explica todo

Imagina que tus datos son mercadería que llega a un centro comercial:

| Servicio | Analogía | ¿Qué hace? |
|----------|----------|-------------|
| **Amazon S3** | 🏬 La Bodega | Almacena todo. Nunca se llena, nunca se pierde nada |
| **AWS Glue** | 🏷️ El Inventario | Escanea, clasifica y organiza cada caja |
| **Amazon Athena** | 🔍 El Buscador | "Necesito todos los zapatos talla 42 de marzo" → los encuentra en segundos |

---

## 📋 ¿Para quién es esto?

- Desarrolladores que quieren entender cómo funciona un data lake
- Personas de negocio curiosas sobre cómo AWS maneja datos
- Estudiantes que están empezando con servicios de analytics en AWS
- Cualquiera que haya pensado: *"subí un archivo a S3... ¿y ahora qué?"*

---

## 🏪 El Caso de Uso: E-commerce Analytics

Eres parte del equipo de datos de una tienda online. Cada día recibes un archivo CSV con las órdenes del día. El equipo de negocio necesita respuestas rápidas:

- 📍 *"¿En qué ciudades vendemos más?"*
- 🛒 *"¿Cuáles son los productos top?"*
- 💳 *"¿Cómo prefieren pagar nuestros clientes?"*
- 📈 *"¿Cómo va la tendencia de ventas esta semana?"*

Hoy vas a construir el pipeline que responde todas esas preguntas.

### ¿Cuándo usar esta arquitectura?

Esta solución es ideal cuando:

- ✅ Tienes archivos que llegan periódicamente (CSVs, JSONs, logs)
- ✅ Necesitas consultar datos sin mantener una base de datos 24/7
- ✅ Tu volumen de datos va de megabytes a terabytes
- ✅ Quieres pagar solo por lo que usas (sin costos fijos)
- ✅ No tienes un equipo grande de infraestructura

Ejemplos del mundo real:
- 📊 **Reportes de ventas** — CSVs diarios de tu ERP o plataforma de e-commerce
- 📱 **Logs de aplicaciones** — registros de actividad de usuarios
- 🏦 **Datos financieros** — transacciones, conciliaciones bancarias
- 🚚 **Logística** — tracking de envíos, tiempos de entrega
- 📋 **IoT** — datos de sensores almacenados periódicamente

---

## 🗂️ Estructura del Repositorio

```
aws-data-journey/
├── 📄 README.md                    ← Estás aquí
├── 📁 data/
│   └── ventas_mayo_2026.csv        ← Dataset de ejemplo (50 órdenes)
├── 📁 scripts/
│   └── glue_etl_job.py             ← Script ETL para transformar datos
├── 📁 queries/
│   ├── 01_vista_general.sql        ← SELECT * básico
│   ├── 02_ventas_por_departamento.sql
│   ├── 03_top_productos.sql
│   ├── 04_metodos_de_pago.sql
│   ├── 05_tendencia_diaria.sql
│   ├── 06_categorias_por_ciudad.sql
│   └── 07_partition_pruning.sql    ← Comparación de costos
├── 📁 iam/
│   └── policy_crawler.json         ← Política IAM para el Crawler
└── 📁 docs/
    ├── GUIA_PASO_A_PASO.md         ← Tutorial completo
    ├── TROUBLESHOOTING.md          ← Solución de errores comunes
    └── LIMPIEZA.md                 ← Cómo eliminar todo al terminar
```

---

## ⚡ Quick Start (5 minutos)

> **Pre-requisito:** Una cuenta AWS activa y verificada.

### Paso 1: Crear el bucket S3

```bash
aws s3 mb s3://tu-datalake-demo --region us-east-1
```

Sube el CSV:
```bash
aws s3 cp data/ventas_mayo_2026.csv s3://tu-datalake-demo/raw/ventas/
```

### Paso 2: Configurar IAM

Crea la política usando el archivo incluido (edita el nombre del bucket primero):
```bash
aws iam create-policy \
  --policy-name PolicyCrawlerDemo \
  --policy-document file://iam/policy_crawler.json
```

Crea el rol para Glue:
```bash
aws iam create-role \
  --role-name RolCrawlerDemo \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "glue.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name RolCrawlerDemo \
  --policy-arn arn:aws:iam::TU_ACCOUNT_ID:policy/PolicyCrawlerDemo
```

### Paso 3: Crear base de datos y Crawler

```bash
aws glue create-database \
  --database-input '{"Name": "ecommerce-db"}'

aws glue create-crawler \
  --name crawler-ecommerce \
  --role RolCrawlerDemo \
  --database-name ecommerce-db \
  --table-prefix raw_ \
  --targets '{"S3Targets": [{"Path": "s3://tu-datalake-demo/raw/ventas/"}]}'
```

### Paso 4: Ejecutar el Crawler

```bash
aws glue start-crawler --name crawler-ecommerce
```

Espera ~1 minuto. Verifica que terminó:
```bash
aws glue get-crawler --name crawler-ecommerce --query 'Crawler.State'
```

### Paso 5: Consultar con Athena

Configura el bucket de resultados en Athena y ejecuta:

```sql
SELECT * FROM raw_ventas LIMIT 10;
```

🎉 **¡Listo!** Estás consultando datos en S3 con SQL, sin servidores.

---

## 🔄 El Flujo Completo

```
                    ┌─────────────────────────────────────────────────────┐
                    │              EL VIAJE DE TUS DATOS                  │
                    └─────────────────────────────────────────────────────┘

    ┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐
    │  1. CSV  │         │ 2. S3   │         │ 3. Glue │         │4. Athena│
    │  ventas  │ ──────▶ │  raw/   │ ──────▶ │ Crawler │ ──────▶ │  SQL    │
    │  diarias │         │ ventas/ │         │  + ETL  │         │ queries │
    └─────────┘         └─────────┘         └─────────┘         └─────────┘
                                                 │
                                                 ▼
                                            ┌─────────┐
                                            │  Glue   │
                                            │ Catalog │
                                            │ (tabla) │
                                            └─────────┘
```

### Paso a paso:

1. **CSV llega a S3** — Cada día, el sistema de e-commerce exporta las ventas como CSV y las sube a `s3://bucket/raw/ventas/`

2. **Glue Crawler escanea** — Un robot automático lee el CSV, detecta que tiene 10 columnas (order_id, fecha, cliente...), infiere los tipos de datos, y registra todo en el **Glue Data Catalog** como una tabla llamada `raw_ventas`

3. **Athena consulta** — Sin instalar nada ni levantar servidores, escribes SQL directo sobre los datos en S3. Athena lee el catálogo de Glue para saber la estructura.

4. **(Opcional) Glue ETL transforma** — Un script Python convierte el CSV a formato **Parquet** (columnar, comprimido), lo particiona por departamento, y lo guarda en `processed/`. Esto hace que las consultas sean más rápidas y baratas.

---

## 📊 Las Consultas (queries/)

Cada archivo SQL responde una pregunta de negocio:

| Archivo | Pregunta | Insight |
|---------|----------|---------|
| `01_vista_general.sql` | ¿Qué datos tenemos? | Exploración inicial del dataset |
| `02_ventas_por_departamento.sql` | ¿Dónde vendemos más? | Lima lidera, Arequipa es segundo |
| `03_top_productos.sql` | ¿Qué se vende más? | Tecnología domina los ingresos |
| `04_metodos_de_pago.sql` | ¿Cómo pagan los clientes? | Yape y Plin ~40% de las transacciones |
| `05_tendencia_diaria.sql` | ¿Cómo va la semana? | Tendencia de ventas por día |
| `06_categorias_por_ciudad.sql` | ¿Qué vende cada ciudad? | Categoría dominante por ubicación |
| `07_partition_pruning.sql` | ¿Cómo optimizar costos? | Comparar scan con/sin filtro de partición |

---

## 💰 ¿Cuánto cuesta?

| Servicio | Precio | Este demo |
|----------|--------|-----------|
| **S3** | $0.023/GB/mes | < $0.01 |
| **Glue Crawler** | $0.44/DPU-hora | ~$0.01 |
| **Athena** | $5.00/TB escaneado | ~$0.00 |
| **Total** | | **< $0.05** |

> 💡 **Dato:** Con Parquet + particiones, una consulta que escanea 1GB en CSV escanearía ~250MB en Parquet. 4x más barato.

---

## 🧹 Limpieza

Para no dejar recursos corriendo, sigue la guía en [`docs/LIMPIEZA.md`](docs/LIMPIEZA.md).

---

## 📚 Recursos Adicionales

- [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/)
- [Amazon Athena User Guide](https://docs.aws.amazon.com/athena/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [Formato Apache Parquet](https://parquet.apache.org/)

---

## 🤝 Contribuir

¿Encontraste un error? ¿Tienes una mejora? Abre un Issue o Pull Request.

---

## 📝 Licencia

MIT — Usa este repositorio como quieras para aprender y enseñar.

---

> Creado para la charla **"El Viaje de tus Datos en AWS"** — AWS User Group Perú 🇵🇪
