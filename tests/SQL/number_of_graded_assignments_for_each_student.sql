-- Write query to get number of graded assignments for each student:
SELECT 
    student_id,
    COUNT(*) AS number_of_graded_assignments
FROM 
    assignments
WHERE 
    grade IS NOT NULL  -- Ensures that only graded assignments are counted
GROUP BY 
    student_id;