-- Q3: recovery from the low point (YoY passenger change by month, Mar 2026 onwards)
WITH yoy AS (
    SELECT b.brand, d.month, d.month_name,
           ROUND((f26.passengers - f25.passengers) * 100.0 / f25.passengers, 1) AS yoy_pct
    FROM fact_traffic f26
    JOIN dim_date  d   ON d.month = f26.month AND d.year = 2026
    JOIN dim_brand b   ON b.brand_id = f26.brand_id
    JOIN dim_date  d25 ON d25.year = 2025 AND d25.month_num = d.month_num
    JOIN fact_traffic f25 ON f25.brand_id = f26.brand_id AND f25.month = d25.month
    WHERE d.month_num >= 3
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY brand ORDER BY yoy_pct ASC) AS low_rank,
           ROW_NUMBER() OVER (PARTITION BY brand ORDER BY month DESC)  AS latest_rank
    FROM yoy
)
SELECT lo.brand,
       lo.month_name AS low_month, lo.yoy_pct AS low_yoy,
       la.month_name AS latest_month, la.yoy_pct AS latest_yoy,
       ROUND(la.yoy_pct - lo.yoy_pct, 1) AS recovery_pts
FROM ranked lo
JOIN ranked la ON la.brand = lo.brand AND la.latest_rank = 1
WHERE lo.low_rank = 1
ORDER BY recovery_pts DESC;
