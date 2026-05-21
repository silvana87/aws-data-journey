-- =============================================
-- 👀 Vista general: ¿Qué datos tenemos?
-- =============================================
-- Esta es la primera consulta que ejecutas cuando
-- quieres explorar un dataset nuevo.
-- Athena lee directamente desde S3 usando el
-- esquema que el Crawler detectó.
--
-- 💡 Fíjate en "Data scanned" abajo de los resultados.
--    Con CSV, escanea TODO el archivo (~4.73 KB).
--    Con Parquet, escanearía mucho menos.
-- =============================================

SELECT *
FROM raw_ventas
LIMIT 10;
