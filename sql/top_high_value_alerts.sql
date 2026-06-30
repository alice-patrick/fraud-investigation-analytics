SELECT
    transaction_id,
    step,
    type,
    amount,
    fraud_score,
    rank_score,
    expected_benefit,
    severity,
    reason,
    isFraud
FROM thesis_decision_export
WHERE alert = 1
ORDER BY expected_benefit DESC
LIMIT 50;