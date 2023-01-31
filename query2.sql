SELECT d.id id, d.department department, COUNT(e.id) hired
FROM departments d, employees e
WHERE d.id = e.department_id
GROUP BY d.id
HAVING COUNT(e.id) > (
    SELECT COUNT(e.id) / (
        SELECT COUNT(DISTINCT(d.id)) 
        FROM departments d)
    FROM employees e
    WHERE STRFTIME('%Y', e.datetime) == '2021')
ORDER BY 3 DESC;