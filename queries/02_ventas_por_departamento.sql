-- =============================================
-- 📍 ¿En qué departamentos vendemos más?
-- =============================================
-- Pregunta de negocio: El gerente quiere saber
-- dónde concentrar los esfuerzos de marketing.
--
-- Insight esperado: Lima lidera en ventas totales,
-- pero el ticket promedio puede ser mayor en
-- departamentos con menos órdenes.
-- =============================================

SELECT
    departamento,
    COUNT(*) AS num_ordenes,
    ROUND(SUM(cantidad * precio_unitario), 2) AS total_ventas,
    ROUND(AVG(cantidad * precio_unitario), 2) AS ticket_promedio
FROM raw_ventas
GROUP BY departamento
ORDER BY total_ventas DESC;
