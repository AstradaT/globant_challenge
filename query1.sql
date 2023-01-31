SELECT q1.d department, q1.j job, q1.q1 q1, q2.q2 q2, q3.q3 q3, q4.q4 q4 FROM (
    -- quarter 1
    SELECT d.department d, j.job j, IIF(STRFTIME('%m', e.datetime) IN ('01', '02', '03'), COUNT(e.name), 0) q1
    FROM departments d, jobs j, employees e
    WHERE STRFTIME('%Y', e.datetime) == '2021'
    AND d.id == e.department_id
    AND j.id == e.job_id
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
) q1
JOIN (
    -- quarter 2
    SELECT d.department d, j.job j, IIF(STRFTIME('%m', e.datetime) IN ('04', '05', '06'), COUNT(e.name), 0) q2
    FROM departments d, jobs j, employees e
    WHERE STRFTIME('%Y', e.datetime) == '2021'
    AND d.id == e.department_id
    AND j.id == e.job_id
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
) q2
ON q1.d = q2.d AND q1.j = q2.j
JOIN (
    -- quarter 3
    SELECT d.department d, j.job j, IIF(STRFTIME('%m', e.datetime) IN ('07', '08', '09'), COUNT(e.name), 0) q3
    FROM departments d, jobs j, employees e
    WHERE STRFTIME('%Y', e.datetime) == '2021'
    AND d.id == e.department_id
    AND j.id == e.job_id
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
) q3
ON q2.d = q3.d AND q2.j = q3.j
JOIN (
    -- quarter 4
    SELECT d.department d, j.job j, IIF(STRFTIME('%m', e.datetime) IN ('10', '11', '12'), COUNT(e.name), 0) q4
    FROM departments d, jobs j, employees e
    WHERE STRFTIME('%Y', e.datetime) == '2021'
    AND d.id == e.department_id
    AND j.id == e.job_id
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
) q4
ON q3.d = q4.d AND q3.j = q4.j;