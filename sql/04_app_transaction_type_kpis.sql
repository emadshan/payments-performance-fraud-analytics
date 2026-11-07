-- Project: Razorpay Payments Intelligence & Business Optimization
-- Purpose: Identify high-failure combinations of payment app and transaction type.
-- Data: Synthetic dataset; not actual Razorpay internal data.

CREATE OR REPLACE VIEW analytics.v_app_transaction_type_kpis AS
SELECT
    payment_app,
    transaction_type,
    COUNT(*) AS total_attempts,
    COUNT(*) FILTER (WHERE status = 'Success') AS successful_attempts,
    COUNT(*) FILTER (WHERE status = 'Failed') AS failed_attempts,
    COUNT(*) FILTER (WHERE status = 'Pending') AS pending_attempts,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'Failed')
        / NULLIF(COUNT(*), 0), 2
    ) AS failure_rate_pct,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'Success')
        / NULLIF(COUNT(*), 0), 2
    ) AS success_rate_pct,
    ROUND(AVG(amount), 2) AS average_attempt_amount
FROM analytics.transactions
GROUP BY payment_app, transaction_type
HAVING COUNT(*) >= 50;
