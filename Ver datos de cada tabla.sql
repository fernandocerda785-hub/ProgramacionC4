-- Ver los primeros 3 registros de cada tabla
SELECT '=== DEPARTAMENTOS ===' AS titulo;
SELECT * FROM departamento LIMIT 3;

SELECT '=== ESTUDIANTES ===' AS titulo;
SELECT * FROM estudiante LIMIT 3;

SELECT '=== PROFESORES ===' AS titulo;
SELECT * FROM profesor LIMIT 3;

SELECT '=== CURSOS ===' AS titulo;
SELECT * FROM curso LIMIT 3;

SELECT '=== CLASES ===' AS titulo;
SELECT * FROM clase LIMIT 3;

SELECT '=== INSCRIPCIONES ===' AS titulo;
SELECT * FROM inscripcion LIMIT 3;

SELECT '=== CALIFICACIONES ===' AS titulo;
SELECT * FROM calificacion LIMIT 3;