SELECT
    system,
    alerts,
    frauds_caught,
    missed_frauds,
    false_positives,
    ROUND(precision, 4) AS precision,
    ROUND(recall, 4) AS recall,
    ROUND(missed_fraud_cost, 2) AS missed_fraud_cost,
    ROUND(fraud_loss_prevented, 2) AS fraud_loss_prevented,
    ROUND(investigation_cost_total, 2) AS investigation_cost_total,
    ROUND(total_operational_cost, 2) AS total_operational_cost,
    ROUND(queue_efficiency, 4) AS queue_efficiency,
    ROUND(false_positive_rate_in_queue, 4) AS false_positive_rate_in_queue,
    ROUND(cost_diff_vs_static, 2) AS cost_diff_vs_static,
    ROUND(recall_diff_vs_static, 4) AS recall_diff_vs_static
FROM thesis_operational_summary
ORDER BY total_operational_cost ASC;