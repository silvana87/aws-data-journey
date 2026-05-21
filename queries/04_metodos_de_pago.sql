-- =============================================
-- 💳 ¿Cómo prefieren pagar nuestros clientes?
-- =============================================
-- Pregunta de negocio: ¿Qué métodos de pago
-- debemos priorizar? ¿Vale la pena invertir
-- en integraciones con billeteras digitales?
--
-- Insight esperado: Yape y Plin juntos
-- representan ~40% de las transacciones.
-- Los pagos digitales están dominando.
-- =============================================

SELECT
    metodo_pago,
    COUNT(*) AS num_transacciones,
    ROUND(SUM(cantidad * precio_unitario), 2) AS total,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM raw_ventas),
        1
    ) AS porcentaje
FROM raw_ventas
GROUP BY metodo_pago
ORDER BY num_transacciones DESC;
