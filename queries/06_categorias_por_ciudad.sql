-- =============================================
-- 🏙️ ¿Qué categoría domina en cada ciudad?
-- =============================================
-- Pregunta de negocio: ¿Deberíamos adaptar
-- el catálogo según la ciudad?
--
-- Insight: Permite personalizar ofertas
-- por región. Ej: si Cusco compra más Hogar,
-- podemos hacer campañas específicas.
-- =============================================

SELECT
    ciudad,
    categoria,
    COUNT(*) AS ordenes,
    ROUND(SUM(cantidad * precio_unitario), 2) AS total
FROM raw_ventas
GROUP BY ciudad, categoria
ORDER BY ciudad, total DESC;
