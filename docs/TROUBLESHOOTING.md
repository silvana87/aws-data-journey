# 🔧 Troubleshooting: Solución de Errores Comunes

## ❌ "Account is denied access" al crear o ejecutar el Crawler

**Causa más probable:** Lake Formation está controlando los permisos.

**Solución:**
1. Ve a **Lake Formation** → **Settings**
2. Marca ambas casillas:
   - ☑️ Use only IAM access control for new databases
   - ☑️ Use only IAM access control for new tables in new databases
3. Guarda
4. **Elimina** la base de datos en Glue y **créala de nuevo**
5. Crea el Crawler nuevamente

**¿Por qué funciona?** Las bases de datos creadas antes de cambiar estos settings heredan los permisos restrictivos de Lake Formation. Recrearlas aplica la nueva configuración.

---

## ❌ "Account verification is in progress"

**Causa:** Tu cuenta AWS es nueva y no ha sido verificada completamente.

**Solución:** Esperar hasta 48 horas. Revisa tu email por correos de verificación de AWS. Si necesitas acelerar, contacta AWS Support.

---

## ❌ "User does not have access to target s3://..."

**Causa:** La política IAM del Crawler no tiene acceso al bucket correcto.

**Solución:**
1. Ve a **IAM** → **Policies** → busca tu política
2. Click **Edit** → pestaña **JSON**
3. Verifica que el nombre del bucket en `Resource` coincida **exactamente** con tu bucket
4. Guarda y vuelve a ejecutar el Crawler

---

## ❌ "Table not found" en Athena

**Causa:** El Crawler no ha terminado o la base de datos seleccionada en Athena es incorrecta.

**Solución:**
1. Verifica que el Crawler tenga status **READY** y que en "Table changes" diga "1 table change"
2. En Athena, panel izquierdo, selecciona la base de datos correcta (`ecommerce-db`)
3. Si la tabla no aparece, click en el ícono de refrescar (🔄) junto a "Tables"

---

## ❌ "No output location provided" en Athena

**Causa:** Athena necesita un bucket donde guardar los resultados de las consultas.

**Solución:**
1. En Athena, click **Settings** → **Manage**
2. En "Query result location", pon: `s3://tu-bucket/athena-results/`
3. Click **Save**

---

## ❌ El Crawler se queda en "RUNNING" por más de 5 minutos

**Causa:** Permisos insuficientes o problemas de conectividad.

**Solución:**
1. Click **View CloudWatch logs** en la página del Crawler
2. Busca el error específico en los logs
3. Generalmente es un problema de permisos → revisa que el rol IAM tenga las políticas correctas

---

## ❌ Columnas aparecen con tipos incorrectos en Athena

**Causa:** El Crawler infirió tipos diferentes a los esperados (ej: precio como string en vez de double).

**Solución:**
1. Ve a **Glue** → **Tables** → selecciona tu tabla
2. Click **Edit schema**
3. Cambia los tipos manualmente
4. Guarda

---

## ❌ "Access Denied" al ejecutar un Glue Job (ETL)

**Causa:** El rol IAM no tiene permiso `lakeformation:GetDataAccess`.

**Solución:** Asegúrate de que tu política incluya:
```json
{
    "Effect": "Allow",
    "Action": "lakeformation:GetDataAccess",
    "Resource": "*"
}
```

---

## 💡 Tips Generales

- **Siempre verifica la región.** Si creaste el bucket en `us-east-1`, asegúrate de que estés viendo Glue y Athena en la misma región.
- **Los nombres de bucket son globales.** Si `e-commerce-datalake-demo` ya está tomado, agrega tu nombre: `e-commerce-datalake-demo-tunombre`.
- **Ejecuta Lake Formation Settings ANTES de crear bases de datos.** Es el error más común y más frustrante.
