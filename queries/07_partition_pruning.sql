-- =============================================
-- 🎯 Partition Pruning: Cómo optimizar costos
-- =============================================
-- Este ejemplo muestra por qué las particiones
-- son importantes. Athena cobra por TB escaneado.
-- Si filtras por una partición, Athena SOLO lee
-- los archivos en esa carpeta, no toda la tabla.
--
-- 💡 Ejecuta ambas consultas y compara el
--    "Data scanned" en los resultados.
--
-- Nota: Con el CSV actual (50 registros) la
-- diferencia es mínima. Pero con millones de
-- registros y datos particionados en Parquet,
-- la diferencia puede ser 100x.
-- =============================================


-- CONSULTA A: Sin filtro de partición
-- Escanea TODOS los datos
SELECT
    COUNT(*) AS total_ordenes,
    ROUND(SUM(cantidad * precio_unitario), 2) AS total_ventas
FROM raw_ventas;


-- CONSULTA B: Con filtro (simula partition pruning)
-- En una tabla particionada por departamento,
-- esto SOLO leería la carpeta departamento=Lima/
SELECT
    COUNT(*) AS ordenes_lima,
    ROUND(SUM(cantidad * precio_unitario), 2) AS ventas_lima
FROM raw_ventas
WHERE departamento = 'Lima';

-- =============================================
-- 📊 Comparación de costos (ejemplo real):
--
-- Sin particiones (1 TB de datos):
--   Escanea: 1 TB → Costo: $5.00
--
-- Con particiones por departamento (Lima = 40%):
--   Escanea: 400 GB → Costo: $2.00
--
-- Con particiones + Parquet (75% compresión):
--   Escanea: 100 GB → Costo: $0.50
--
-- 💰 De $5.00 a $0.50 = 90% de ahorro
-- =============================================
