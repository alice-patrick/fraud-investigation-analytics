SELECT
    COUNT(*) AS total_transactions,
    SUM(alert) AS total_alerts,
    SUM(isFraud) AS total_frauds,
    SUM(CASE WHEN alert = 1 AND isFraud = 1 THEN 1 ELSE 0 END) AS true_positives,
    SUM(CASE WHEN alert = 1 AND isFraud = 0 THEN 1 ELSE 0 END) AS false_positives,
    SUM(CASE WHEN alert = 0 AND isFraud = 1 THEN 1 ELSE 0 END) AS missed_frauds,
    ROUND(
        CAST(SUM(CASE WHEN alert = 1 AND isFraud = 1 THEN 1 ELSE 0 END) AS FLOAT)
        / NULLIF(SUM(alert), 0),
        4
    ) AS alert_precision,
    ROUND(
        CAST(SUM(CASE WHEN alert = 1 AND isFraud = 1 THEN 1 ELSE 0 END) AS FLOAT)
        / NULLIF(SUM(isFraud), 0),
        4
    ) AS fraud_recall,
    ROUND(AVG(fraud_score), 4) AS avg_fraud_score,
    ROUND(SUM(expected_benefit), 2) AS total_expected_benefit
FROM thesis_decision_export;