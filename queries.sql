-- Employee Attrition Analytics — optional SQL practice
-- These queries are included to demonstrate how the same business questions
-- could be answered in SQL.

-- 1) Overall attrition KPI
SELECT
    COUNT(*) AS employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS attrition_rate_pct
FROM employee_attrition;

-- 2) Attrition by department
SELECT
    Department,
    COUNT(*) AS employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS attrition_rate_pct
FROM employee_attrition
GROUP BY Department
ORDER BY attrition_rate_pct DESC;

-- 3) Attrition by job role
SELECT
    JobRole,
    COUNT(*) AS employees,
    ROUND(
        100.0 * AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END),
        2
    ) AS attrition_rate_pct
FROM employee_attrition
GROUP BY JobRole
HAVING COUNT(*) >= 20
ORDER BY attrition_rate_pct DESC;

-- 4) Overtime comparison
SELECT
    OverTime,
    COUNT(*) AS employees,
    ROUND(
        100.0 * AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END),
        2
    ) AS attrition_rate_pct
FROM employee_attrition
GROUP BY OverTime
ORDER BY attrition_rate_pct DESC;

-- 5) Attrition by tenure band
SELECT
    CASE
        WHEN YearsAtCompany <= 1 THEN '0-1'
        WHEN YearsAtCompany = 2 THEN '2'
        WHEN YearsAtCompany BETWEEN 3 AND 5 THEN '3-5'
        WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10'
        ELSE '11+'
    END AS tenure_band,
    COUNT(*) AS employees,
    ROUND(
        100.0 * AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END),
        2
    ) AS attrition_rate_pct
FROM employee_attrition
GROUP BY tenure_band
ORDER BY
    CASE tenure_band
        WHEN '0-1' THEN 1 WHEN '2' THEN 2 WHEN '3-5' THEN 3
        WHEN '6-10' THEN 4 ELSE 5
    END;
