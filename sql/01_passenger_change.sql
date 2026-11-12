-- Q1: passenger change, Mar-Aug 2026 vs same months of 2025
WITH w AS (
    SELECT b.brand, b.home_market, d.year,
           SUM(f.passengers) AS pax
    FROM fact_traffic f
    JOIN dim_brand b ON b.brand_id = f.brand_id
    JOIN dim_date  d ON d.month = f.month
    WHERE d.month_num BETWEEN 3 AND 8
      AND d.year IN (2025, 2026)
    GROUP BY b.brand, b.home_market, d.year
)
SELECT p25.brand, p25.home_market,
       p25.pax AS pax_2025,
       p26.pax AS pax_2026,
       ROUND((p26.pax - p25.pax) * 100.0 / p25.pax, 1) AS pct_change
FROM w p25
JOIN w p26 ON p26.brand = p25.brand AND p26.year = 2026
WHERE p25.year = 2025
ORDER BY pct_change;
