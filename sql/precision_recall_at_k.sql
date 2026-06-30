WITH ranked_alerts AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            ORDER BY rank_score DESC
        ) AS alert_rank
    FROM thesis_decision_export
    WHERE alert = 1
),

totals AS (
    SELECT
        COUNT(*) AS total_frauds
    FROM thesis_decision_export
    WHERE isFraud = 1
)

SELECT
    k_value,
    alerts_reviewed,
    frauds_found,

    ROUND(
        CAST(frauds_found AS FLOAT)
        / alerts_reviewed,
        4
    ) AS precision_at_k,

    ROUND(
        CAST(frauds_found AS FLOAT)
        / total_frauds,
        4
    ) AS recall_at_k

FROM (

    SELECT
        50 AS k_value,
        50 AS alerts_reviewed,
        SUM(isFraud) AS frauds_found
    FROM ranked_alerts
    WHERE alert_rank <= 50

    UNION ALL

    SELECT
        100,
        100,
        SUM(isFraud)
    FROM ranked_alerts
    WHERE alert_rank <= 100

    UNION ALL

    SELECT
        250,
        250,
        SUM(isFraud)
    FROM ranked_alerts
    WHERE alert_rank <= 250

) metrics

CROSS JOIN totals;