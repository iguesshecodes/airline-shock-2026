-- Q2: capacity change vs load factor change, Mar-Aug 2026 vs same months of 2025
WITH w AS (
    SELECT b.brand, d.year,
           SUM(f.ask_k) AS ask, SUM(f.rpk_k) AS rpk
    FROM fact_traffic f
    JOIN dim_brand b ON b.brand_id = f.brand_id
    JOIN dim_date  d ON d.month = f.month
    WHERE d.month_num BETWEEN 3 AND 8
      AND d.year IN (2025, 2026)
    GROUP BY b.brand, d.year
)
SELECT p25.brand,
       ROUND((p26.ask - p25.ask) * 100.0 / p25.ask, 1) AS capacity_chg_pct,
       ROUND(p25.rpk * 100.0 / p25.ask, 1) AS lf_2025,
       ROUND(p26.rpk * 100.0 / p26.ask, 1) AS lf_2026,
       ROUND(p26.rpk * 100.0 / p26.ask - p25.rpk * 100.0 / p25.ask, 1) AS lf_chg_pts
FROM w p25
JOIN w p26 ON p26.brand = p25.brand AND p26.year = 2026
WHERE p25.year = 2025
ORDER BY capacity_chg_pct;
