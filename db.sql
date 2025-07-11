-- =====================================================
-- SCRIPT PARA CREAR LA BASE DE DATOS
-- =====================================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS dataset;
USE dataset;

-- =====================================================
-- TABLA: CARRERAS
-- =====================================================
CREATE TABLE Carreras (
    CarreraId INT AUTO_INCREMENT PRIMARY KEY,
    ClaveCarrera VARCHAR(20) NOT NULL,
    NombreCarrera VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_clave_carrera (ClaveCarrera)
);

-- =====================================================
-- TABLA: PLANTELES
-- =====================================================
CREATE TABLE Planteles (
    PlantelId INT AUTO_INCREMENT PRIMARY KEY,
    Cct VARCHAR(20) NOT NULL,
    Entidad VARCHAR(100),
    Municipio VARCHAR(100),
    Localidad VARCHAR(100),
    NombrePlantel VARCHAR(255),
    Subsistema VARCHAR(100),
    UNIQUE KEY unique_cct (Cct)
);

-- =====================================================
-- TABLA: ESTUDIANTES
-- =====================================================
CREATE TABLE Estudiantes (
    EstudianteId INT AUTO_INCREMENT PRIMARY KEY,
    Curp VARCHAR(18) NOT NULL,
    Sexo VARCHAR(20),
    Edad INT,
    FechaNacimiento VARCHAR(10),
    Promedio DECIMAL(4,2),
    CarreraId INT,
    PlantelId INT,
    Entidad VARCHAR(100),
    Municipio VARCHAR(100),
    UNIQUE KEY unique_curp (Curp),
    FOREIGN KEY (CarreraId) REFERENCES Carreras(CarreraId),
    FOREIGN KEY (PlantelId) REFERENCES Planteles(PlantelId)
);

-- =====================================================
-- ÍNDICES ADICIONALES PARA OPTIMIZAR CONSULTAS
-- =====================================================
CREATE INDEX idx_estudiantes_sexo ON Estudiantes(Sexo);
CREATE INDEX idx_estudiantes_edad ON Estudiantes(Edad);
CREATE INDEX idx_estudiantes_entidad ON Estudiantes(Entidad);
CREATE INDEX idx_estudiantes_municipio ON Estudiantes(Municipio);
CREATE INDEX idx_estudiantes_promedio ON Estudiantes(Promedio);

-- =====================================================
-- COMENTARIOS DE LA ESTRUCTURA
-- =====================================================
/*
ESTRUCTURA DE LA BASE DE DATOS:

1. CARRERAS: Almacena información de las carreras disponibles
   - CarreraId: Identificador único autoincremental
   - ClaveCarrera: Código de la carrera
   - NombreCarrera: Nombre completo de la carrera

2. PLANTELES: Almacena información de las escuelas/planteles
   - PlantelId: Identificador único autoincremental
   - Cct: Clave del Centro de Trabajo
   - Entidad: Estado donde se ubica el plantel
   - Municipio: Municipio del plantel
   - Localidad: Localidad específica
   - NombrePlantel: Nombre del plantel
   - Subsistema: Tipo de subsistema educativo

3. ESTUDIANTES: Almacena información de los estudiantes
   - EstudianteId: Identificador único autoincremental
   - Curp: Clave Única de Registro de Población
   - Sexo: Masculino/Femenino
   - Edad: Edad calculada automáticamente
   - FechaNacimiento: Fecha en formato DD/MM/AAAA
   - Promedio: Promedio académico
   - CarreraId: Relación con la tabla Carreras
   - PlantelId: Relación con la tabla Planteles
   - Entidad: Estado (copiado del plantel)
   - Municipio: Municipio (copiado del plantel)

RELACIONES:
- Un estudiante pertenece a una carrera (CarreraId)
- Un estudiante pertenece a un plantel (PlantelId)
- Los datos de Entidad y Municipio se copian del plantel para facilitar consultas
*/