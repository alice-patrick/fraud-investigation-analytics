SELECT
    severity,
    COUNT(*) AS alerts,
    SUM(isFraud) AS confirmed_frauds,
    ROUND(AVG(fraud_score), 4) AS avg_fraud_score,
    ROUND(SUM(expected_benefit), 2) AS total_expected_benefit
FROM thesis_decision_export
WHERE alert = 1
GROUP BY severity
ORDER BY total_expected_benefit DESC;