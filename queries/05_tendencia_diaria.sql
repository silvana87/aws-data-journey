-- =============================================
-- 📈 ¿Cómo va la tendencia de ventas?
-- =============================================
-- Pregunta de negocio: ¿Estamos vendiendo más
-- o menos que los días anteriores?
--
-- Insight: Permite detectar patrones como
-- días fuertes (lunes post-pago) o caídas
-- que necesitan investigación.
-- =============================================

SELECT
    fecha,
    COUNT(*) AS ordenes_del_dia,
    ROUND(SUM(cantidad * precio_unitario), 2) AS ventas_del_dia
FROM raw_ventas
GROUP BY fecha
ORDER BY fecha;
