-- Ver cuántos registros hay en cada tabla
SELECT 
    'departamento' AS tabla, 
    COUNT(*) AS cantidad 
FROM departamento
UNION ALL
SELECT 'estudiante', COUNT(*) FROM estudiante
UNION ALL
SELECT 'profesor', COUNT(*) FROM profesor
UNION ALL
SELECT 'curso', COUNT(*) FROM curso
UNION ALL
SELECT 'clase', COUNT(*) FROM clase
UNION ALL
SELECT 'inscripcion', COUNT(*) FROM inscripcion
UNION ALL
SELECT 'calificacion', COUNT(*) FROM calificacion;