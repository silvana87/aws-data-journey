-- =============================================
-- 🛒 ¿Cuáles son los Top 5 productos?
-- =============================================
-- Pregunta de negocio: ¿Qué productos generan
-- más ingresos? ¿Deberíamos ampliar el stock?
--
-- Insight esperado: Los productos de tecnología
-- (laptops, monitores) dominan por precio alto,
-- aunque no sean los más vendidos en unidades.
-- =============================================

SELECT
    producto,
    categoria,
    SUM(cantidad) AS unidades_vendidas,
    ROUND(SUM(cantidad * precio_unitario), 2) AS ingresos_totales
FROM raw_ventas
GROUP BY producto, categoria
ORDER BY ingresos_totales DESC
LIMIT 5;
