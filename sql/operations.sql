-- The Python caller substitutes an allowlisted dimension for {dimension}.
-- The hourly rate is a bound parameter. All measures use the selected ticket population.
SELECT
    {dimension} AS segment,
    COUNT(*) AS tickets,
    ROUND(AVG(handle_min), 2) AS avg_handle_min,
    ROUND(AVG(first_reply_min), 2) AS avg_first_reply_min,
    ROUND(AVG(resolution_min) / 60.0, 2) AS avg_resolution_hours,
    SUM(first_reply_min <= sla_min) AS sla_met,
    ROUND(100.0 * AVG(first_reply_min <= sla_min), 2) AS sla_pct,
    SUM(resolved_7d) AS resolved_7d,
    ROUND(100.0 * AVG(resolved_7d), 2) AS resolution_pct,
    ROUND(100.0 * AVG(reopened_7d), 2) AS reopen_pct,
    ROUND(SUM(handle_min) / 60.0 * :hourly_rate, 2) AS labor_usd
FROM tickets
GROUP BY {dimension}
ORDER BY {ordering};

