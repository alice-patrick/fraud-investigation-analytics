SELECT
    destination_account,
    COUNT(*) AS total_incoming_transactions,
    COUNT(DISTINCT customer_id) AS unique_senders,
    SUM(alert_flag) AS total_alerts,
    SUM(fraud_label) AS confirmed_frauds,
    SUM(CASE WHEN alert_severity = 'HIGH' THEN 1 ELSE 0 END) AS high_severity_alerts,
    ROUND(AVG(fraud_score), 4) AS avg_fraud_score,
    ROUND(MAX(fraud_score), 4) AS max_fraud_score,
    ROUND(SUM(expected_loss), 2) AS total_expected_loss,
    ROUND(AVG(priority_score), 2) AS avg_priority_score
FROM fraud_investigation_dataset
GROUP BY destination_account
HAVING
    COUNT(*) >= 3
    OR SUM(alert_flag) >= 2
    OR SUM(fraud_label) > 0
ORDER BY
    confirmed_frauds DESC,
    high_severity_alerts DESC,
    total_alerts DESC,
    total_expected_loss DESC
LIMIT 50;