SELECT
    customer_id,
    step,

    COUNT(*) AS transactions_in_step,

    SUM(alert_flag) AS alerts_in_step,

    SUM(fraud_label) AS confirmed_frauds_in_step,

    ROUND(SUM(amount), 2) AS total_amount,

    ROUND(AVG(fraud_score), 4) AS avg_fraud_score,

    ROUND(MAX(fraud_score), 4) AS max_fraud_score,

    ROUND(SUM(expected_loss), 2) AS total_expected_loss

FROM fraud_investigation_dataset

GROUP BY
    customer_id,
    step

HAVING
    COUNT(*) >= 2
    OR SUM(alert_flag) > 0
    OR SUM(fraud_label) > 0

ORDER BY
    confirmed_frauds_in_step DESC,
    alerts_in_step DESC,
    transactions_in_step DESC,
    total_expected_loss DESC

LIMIT 100;