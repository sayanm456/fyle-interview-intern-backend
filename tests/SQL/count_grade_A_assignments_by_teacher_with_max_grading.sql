-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherAssignmentCount AS (
    -- Count how many assignments each teacher has graded
    SELECT 
        teacher_id,
        COUNT(*) AS total_assignments
    FROM 
        assignments
    GROUP BY 
        teacher_id
), MaxTeacher AS (
    -- Find the teacher who graded the most assignments
    SELECT 
        teacher_id
    FROM 
        TeacherAssignmentCount
    ORDER BY 
        total_assignments DESC
    LIMIT 1
)
-- Count the number of A's given by that teacher
SELECT 
    COUNT(*) AS number_of_As
FROM 
    assignments
WHERE 
    teacher_id = (SELECT teacher_id FROM MaxTeacher)
    AND grade = 'A';