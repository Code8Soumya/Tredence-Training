USE worksphere;

-- PART A: Basic to Intermediate Analysis

-- 1. Workforce Engagement Analysis
SELECT 
    e.employee_id, 
    e.employee_name, 
    COUNT(ep.project_id) AS project_count
FROM worksphere.employees e
JOIN worksphere.employee_projects ep ON e.employee_id = ep.employee_id
GROUP BY e.employee_id, e.employee_name
HAVING COUNT(ep.project_id) > 2;


-- 2. Salary Benchmark Classification
SELECT 
    employee_id, 
    employee_name, 
    department,
    base_salary,
    CASE 
        WHEN base_salary > (SELECT AVG(base_salary) FROM worksphere.employees) THEN 'Above Average'
        ELSE 'Below Average'
    END AS salary_classification
FROM worksphere.employees;


-- 3. Employee Workload Assessment
SELECT 
    e.employee_id, 
    e.employee_name, 
    SUM(ep.hours_worked) AS total_hours_worked
FROM worksphere.employees e
JOIN worksphere.employee_projects ep ON e.employee_id = ep.employee_id
GROUP BY e.employee_id, e.employee_name
ORDER BY total_hours_worked DESC;

-- 4. Project Staffing Density
SELECT 
    p.project_id, 
    p.project_name, 
    p.department,
    COUNT(ep.employee_id) AS employee_count
FROM worksphere.projects p
JOIN worksphere.employee_projects ep ON p.project_id = ep.project_id
GROUP BY p.project_id, p.project_name, p.department
HAVING COUNT(ep.employee_id) > 3;



-- PART B: Intermediate to Advanced Analysis

-- 1. Department Revenue Performance
WITH DeptRevenue AS (
    SELECT 
        p.department, 
        SUM(mr.revenue_generated) AS total_dept_revenue
    FROM worksphere.projects p
    JOIN worksphere.monthly_revenue mr ON p.project_id = mr.project_id
    GROUP BY p.department
),
AvgDeptRevenue AS (
    SELECT AVG(total_dept_revenue) AS avg_revenue FROM DeptRevenue
)
SELECT 
    dr.department, 
    dr.total_dept_revenue,
    CASE 
        WHEN dr.total_dept_revenue > adr.avg_revenue THEN 'Exceeds Average'
        ELSE 'Below Average'
    END AS performance_status
FROM DeptRevenue dr
CROSS JOIN AvgDeptRevenue adr;

-- 2. Employee Revenue Ranking
WITH ProjectTotals AS (
    SELECT 
        p.project_id, 
        SUM(ep.hours_worked) AS total_project_hours,
        (SELECT SUM(revenue_generated) FROM worksphere.monthly_revenue mr WHERE mr.project_id = p.project_id) AS total_project_revenue
    FROM worksphere.projects p
    JOIN worksphere.employee_projects ep ON p.project_id = ep.project_id
    GROUP BY p.project_id
),
EmployeeTotalRevenue AS (
    SELECT 
        e.employee_id, 
        e.employee_name, 
        e.department, 
        e.base_salary,
        SUM((ep.hours_worked * 1.0 / pt.total_project_hours) * pt.total_project_revenue) AS total_revenue_contribution,
        SUM(ep.hours_worked) AS total_hours_worked
    FROM worksphere.employee_projects ep
    JOIN worksphere.employees e ON ep.employee_id = e.employee_id
    JOIN ProjectTotals pt ON ep.project_id = pt.project_id
    GROUP BY e.employee_id, e.employee_name, e.department, e.base_salary
)
SELECT 
    department, 
    employee_id, 
    employee_name, 
    ROUND(total_revenue_contribution, 2) AS total_revenue_contribution,
    RANK() OVER(PARTITION BY department ORDER BY total_revenue_contribution DESC) as dept_rank
FROM EmployeeTotalRevenue;

-- 3. Above-Department-Average Contributors
WITH ProjectTotals AS (
    SELECT 
        p.project_id, 
        SUM(ep.hours_worked) AS total_project_hours,
        (SELECT SUM(revenue_generated) FROM worksphere.monthly_revenue mr WHERE mr.project_id = p.project_id) AS total_project_revenue
    FROM worksphere.projects p
    JOIN worksphere.employee_projects ep ON p.project_id = ep.project_id
    GROUP BY p.project_id
),
EmployeeTotalRevenue AS (
    SELECT 
        e.employee_id, 
        e.employee_name, 
        e.department, 
        e.base_salary,
        SUM((ep.hours_worked * 1.0 / pt.total_project_hours) * pt.total_project_revenue) AS total_revenue_contribution,
        SUM(ep.hours_worked) AS total_hours_worked
    FROM worksphere.employee_projects ep
    JOIN worksphere.employees e ON ep.employee_id = e.employee_id
    JOIN ProjectTotals pt ON ep.project_id = pt.project_id
    GROUP BY e.employee_id, e.employee_name, e.department, e.base_salary
),
DeptAvgRevenue AS (
    SELECT department, AVG(total_revenue_contribution) AS avg_dept_employee_revenue
    FROM EmployeeTotalRevenue
    GROUP BY department
)
SELECT 
    etr.employee_name, 
    etr.department, 
    ROUND(etr.total_revenue_contribution, 2) AS total_revenue_contribution,
    ROUND(dar.avg_dept_employee_revenue, 2) AS avg_dept_employee_revenue
FROM EmployeeTotalRevenue etr
JOIN DeptAvgRevenue dar ON etr.department = dar.department
WHERE etr.total_revenue_contribution > dar.avg_dept_employee_revenue;

-- 4. Revenue Per Hour & Performance Tier
WITH ProjectTotals AS (
    SELECT 
        p.project_id, 
        SUM(ep.hours_worked) AS total_project_hours,
        (SELECT SUM(revenue_generated) FROM worksphere.monthly_revenue mr WHERE mr.project_id = p.project_id) AS total_project_revenue
    FROM worksphere.projects p
    JOIN worksphere.employee_projects ep ON p.project_id = ep.project_id
    GROUP BY p.project_id
),
EmployeeTotalRevenue AS (
    SELECT 
        e.employee_id, 
        e.employee_name, 
        e.department, 
        e.base_salary,
        SUM((ep.hours_worked * 1.0 / pt.total_project_hours) * pt.total_project_revenue) AS total_revenue_contribution,
        SUM(ep.hours_worked) AS total_hours_worked
    FROM worksphere.employee_projects ep
    JOIN worksphere.employees e ON ep.employee_id = e.employee_id
    JOIN ProjectTotals pt ON ep.project_id = pt.project_id
    GROUP BY e.employee_id, e.employee_name, e.department, e.base_salary
),
RevPerHourCalc AS (
    SELECT 
        employee_id, 
        employee_name, 
        total_revenue_contribution / total_hours_worked AS revenue_per_hour
    FROM EmployeeTotalRevenue
),
CompanyAvg AS (
    SELECT AVG(revenue_per_hour) AS avg_rev_per_hour FROM RevPerHourCalc
)
SELECT 
    r.employee_name, 
    ROUND(r.revenue_per_hour, 2) AS revenue_per_hour,
    CASE 
        WHEN r.revenue_per_hour >= c.avg_rev_per_hour THEN 'High Performer'
        ELSE 'Standard Performer'
    END AS performance_tier
FROM RevPerHourCalc r
CROSS JOIN CompanyAvg c;

-- 5. Revenue Per Employee by Project
WITH ProjectStats AS (
    SELECT 
        p.project_id, 
        p.project_name, 
        COUNT(ep.employee_id) AS assigned_employees,
        (SELECT SUM(revenue_generated) FROM worksphere.monthly_revenue mr WHERE mr.project_id = p.project_id) AS project_total_revenue
    FROM worksphere.projects p
    JOIN worksphere.employee_projects ep ON p.project_id = ep.project_id
    GROUP BY p.project_id, p.project_name
),
ProjectRevPerEmp AS (
    SELECT 
        project_name, 
        project_total_revenue / assigned_employees AS rev_per_employee
    FROM ProjectStats
),
AvgRevPerEmp AS (
    SELECT AVG(rev_per_employee) AS overall_avg_rev_per_emp FROM ProjectRevPerEmp
)
SELECT 
    pr.project_name, 
    ROUND(pr.rev_per_employee, 2) AS rev_per_employee
FROM ProjectRevPerEmp pr
CROSS JOIN AvgRevPerEmp ar
WHERE pr.rev_per_employee > ar.overall_avg_rev_per_emp;

-- 6. Salary vs Revenue Efficiency Gap
WITH ProjectTotals AS (
    SELECT 
        p.project_id, 
        SUM(ep.hours_worked) AS total_project_hours,
        (SELECT SUM(revenue_generated) FROM worksphere.monthly_revenue mr WHERE mr.project_id = p.project_id) AS total_project_revenue
    FROM worksphere.projects p
    JOIN worksphere.employee_projects ep ON p.project_id = ep.project_id
    GROUP BY p.project_id
),
EmployeeTotalRevenue AS (
    SELECT 
        e.employee_id, 
        e.employee_name, 
        e.department, 
        e.base_salary,
        SUM((ep.hours_worked * 1.0 / pt.total_project_hours) * pt.total_project_revenue) AS total_revenue_contribution,
        SUM(ep.hours_worked) AS total_hours_worked
    FROM worksphere.employee_projects ep
    JOIN worksphere.employees e ON ep.employee_id = e.employee_id
    JOIN ProjectTotals pt ON ep.project_id = pt.project_id
    GROUP BY e.employee_id, e.employee_name, e.department, e.base_salary
),
DeptStats AS (
    SELECT department, AVG(total_revenue_contribution) AS avg_dept_revenue
    FROM EmployeeTotalRevenue 
    GROUP BY department
),
HighestPaidPerDept AS (
    SELECT 
        department, 
        employee_name, 
        base_salary, 
        total_revenue_contribution,
        RANK() OVER(PARTITION BY department ORDER BY base_salary DESC) as salary_rank
    FROM EmployeeTotalRevenue
)
SELECT 
    hp.department, 
    hp.employee_name AS highest_paid_employee, 
    hp.base_salary,
    ROUND(hp.total_revenue_contribution, 2) AS employee_revenue, 
    ROUND(ds.avg_dept_revenue, 2) AS avg_dept_revenue
FROM HighestPaidPerDept hp
JOIN DeptStats ds ON hp.department = ds.department
WHERE hp.salary_rank = 1 AND hp.total_revenue_contribution < ds.avg_dept_revenue;

-- 7. Cumulative Revenue Trend Analysis
WITH DeptMonthlyRev AS (
    SELECT 
        p.department, 
        mr.revenue_month, 
        SUM(mr.revenue_generated) AS monthly_revenue
    FROM worksphere.monthly_revenue mr
    JOIN worksphere.projects p ON mr.project_id = p.project_id
    GROUP BY p.department, mr.revenue_month
)
SELECT 
    department, 
    revenue_month, 
    monthly_revenue,
    SUM(monthly_revenue) OVER (PARTITION BY department ORDER BY revenue_month) AS cumulative_revenue
FROM DeptMonthlyRev
ORDER BY department, revenue_month;

-- 8. Revenue Concentration Risk
WITH ProjectRevenue AS (
    SELECT 
        p.department, 
        p.project_name, 
        SUM(mr.revenue_generated) AS project_revenue
    FROM worksphere.projects p
    JOIN worksphere.monthly_revenue mr ON p.project_id = mr.project_id
    GROUP BY p.department, p.project_name
),
DeptRevenue AS (
    SELECT department, SUM(project_revenue) AS dept_total_revenue
    FROM ProjectRevenue 
    GROUP BY department
),
RankedProjects AS (
    SELECT 
        pr.department, 
        pr.project_name, 
        pr.project_revenue,
        RANK() OVER(PARTITION BY pr.department ORDER BY pr.project_revenue DESC) as rnk
    FROM ProjectRevenue pr
)
SELECT 
    rp.department,
    rp.project_name AS top_project,
    rp.project_revenue,
    dr.dept_total_revenue,
    ROUND((rp.project_revenue / dr.dept_total_revenue) * 100, 2) AS percentage_contribution
FROM RankedProjects rp
JOIN DeptRevenue dr ON rp.department = dr.department
WHERE rp.rnk = 1;



















