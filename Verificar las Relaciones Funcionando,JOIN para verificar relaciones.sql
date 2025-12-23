-- Verificar relación Departamento → Profesor (1:M)
SELECT 
    d.nombre AS departamento,
    COUNT(p.id_profesor) AS cantidad_profesores
FROM departamento d
LEFT JOIN profesor p ON d.id_departamento = p.id_departamento
GROUP BY d.id_departamento
ORDER BY cantidad_profesores DESC;

-- Verificar relación Profesor → Curso (1:M)
SELECT 
    CONCAT(p.nombre, ' ', p.apellido) AS profesor,
    COUNT(c.id_curso) AS cursos_impartidos
FROM profesor p
LEFT JOIN curso c ON p.id_profesor = c.id_profesor
GROUP BY p.id_profesor
ORDER BY cursos_impartidos DESC;

-- Verificar relación Estudiante → Inscripción (1:M)
SELECT 
    CONCAT(e.nombre, ' ', e.apellido) AS estudiante,
    COUNT(i.id_inscripcion) AS inscripciones_activas
FROM estudiante e
LEFT JOIN inscripcion i ON e.id_estudiante = i.id_estudiante 
    AND i.estado = 'activa'
GROUP BY e.id_estudiante
ORDER BY inscripciones_activas DESC;