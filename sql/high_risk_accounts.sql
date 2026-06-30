SELECT
    customer_id,
    COUNT(*) AS total_transactions,
    SUM(alert_flag) AS total_alerts,
    SUM(fraud_label) AS confirmed_frauds,
    SUM(CASE WHEN alert_severity = 'HIGH' THEN 1 ELSE 0 END) AS high_severity_alerts,
    SUM(CASE WHEN alert_severity = 'MEDIUM' THEN 1 ELSE 0 END) AS medium_severity_alerts,
    ROUND(AVG(fraud_score), 4) AS avg_fraud_score,
    ROUND(MAX(fraud_score), 4) AS max_fraud_score,
    ROUND(SUM(expected_loss), 2) AS total_expected_loss,
    ROUND(AVG(priority_score), 2) AS avg_priority_score,
    SUM(repeated_destination_flag) AS repeated_destination_events,
    SUM(cross_border_flag) AS cross_border_transactions
FROM fraud_investigation_dataset
GROUP BY customer_id
HAVING SUM(alert_flag) > 0
ORDER BY
    high_severity_alerts DESC,
    confirmed_frauds DESC,
    total_expected_loss DESC,
    avg_priority_score DESC
LIMIT 50;