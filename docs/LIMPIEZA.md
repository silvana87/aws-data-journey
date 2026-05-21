# 🧹 Limpieza: Cómo eliminar todo al terminar

> **Importante:** Sigue estos pasos para no dejar recursos que generen costos.

## Opción 1: Desde la Consola (más fácil)

### 1. Eliminar el Crawler
- **AWS Glue** → **Crawlers** → selecciona `crawler-ecommerce` → **Delete**

### 2. Eliminar las tablas
- **AWS Glue** → **Data Catalog** → **Tables** → selecciona todas → **Delete**

### 3. Eliminar la base de datos
- **AWS Glue** → **Data Catalog** → **Databases** → selecciona `ecommerce-db` → **Delete**

### 4. Eliminar el Glue Job (si lo creaste)
- **AWS Glue** → **ETL Jobs** → selecciona `etl-ventas-ecommerce` → **Delete**

### 5. Vaciar y eliminar el bucket S3
- **S3** → selecciona `e-commerce-datalake-demo`
- Click **Empty** → confirma escribiendo el texto → **Empty**
- Luego click **Delete** → confirma → **Delete bucket**

### 6. Eliminar el Rol y la Política IAM
- **IAM** → **Roles** → busca `RolCrawlerDemo` → **Delete**
- **IAM** → **Policies** → busca `PolicyCrawlerDemo` → **Delete**

---

## Opción 2: Desde la CLI (más rápido)

```bash
# 1. Eliminar Crawler
aws glue delete-crawler --name crawler-ecommerce

# 2. Eliminar tabla
aws glue delete-table --database-name ecommerce-db --name raw_ventas

# 3. Eliminar base de datos
aws glue delete-database --name ecommerce-db

# 4. Eliminar Glue Job (si existe)
aws glue delete-job --job-name etl-ventas-ecommerce

# 5. Vaciar y eliminar bucket
aws s3 rm s3://e-commerce-datalake-demo --recursive
aws s3 rb s3://e-commerce-datalake-demo

# 6. Desvincular política del rol
aws iam detach-role-policy \
  --role-name RolCrawlerDemo \
  --policy-arn arn:aws:iam::TU_ACCOUNT_ID:policy/PolicyCrawlerDemo

# 7. Eliminar rol
aws iam delete-role --name RolCrawlerDemo

# 8. Eliminar política
aws iam delete-policy \
  --policy-arn arn:aws:iam::TU_ACCOUNT_ID:policy/PolicyCrawlerDemo
```

---

## ✅ Checklist de verificación

Después de limpiar, verifica que no quede nada:

- [ ] S3: No hay bucket `e-commerce-datalake-demo`
- [ ] Glue: No hay crawlers, tablas ni bases de datos del demo
- [ ] IAM: No hay rol `RolCrawlerDemo` ni política `PolicyCrawlerDemo`
- [ ] Athena: Los resultados en `athena-results/` se eliminaron con el bucket

---

## 💰 ¿Qué pasa si no limpio?

| Recurso | Costo si lo dejas |
|---------|-------------------|
| Bucket S3 (con el CSV de 5KB) | ~$0.001/mes |
| Glue Crawler (sin ejecutar) | $0.00 |
| Glue Data Catalog (1 tabla) | $0.00 (primeros 1M objetos gratis) |
| Athena (sin consultas) | $0.00 |
| **Total** | **Casi nada, pero es buena práctica limpiar** |

El riesgo real no es el costo de estos recursos, sino que alguien ejecute el Crawler o Glue Jobs repetidamente sin darse cuenta.
