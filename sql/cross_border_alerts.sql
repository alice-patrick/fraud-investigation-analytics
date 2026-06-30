SELECT
    transaction_id,
    step,
    customer_id,
    destination_account,
    transaction_type,
    country,
    device_type,
    channel,
    amount,
    fraud_score,
    expected_loss,
    priority_score,
    alert_severity,
    investigation_status,
    alert_reason
FROM fraud_investigation_dataset
WHERE
    cross_border_flag = 1
    AND alert_flag = 1
ORDER BY
    priority_score DESC,
    expected_loss DESC,
    fraud_score DESC
LIMIT 100;