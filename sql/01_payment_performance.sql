-- Project: Razorpay Payments Intelligence & Business Optimization
-- Purpose: Analyze payment attempts, transaction value, and outcomes.
-- Data: Synthetic dataset; not actual Razorpay internal data.

CREATE OR REPLACE VIEW analytics.v_payment_performance AS
SELECT
    transaction_type,
    status,
    COUNT(*) AS payment_attempts,
    ROUND(SUM(amount), 2) AS attempted_payment_value,
    ROUND(AVG(amount), 2) AS average_attempt_amount
FROM analytics.transactions
GROUP BY transaction_type, status;
