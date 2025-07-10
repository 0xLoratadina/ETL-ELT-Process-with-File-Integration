-- Script SQL para insertar estudiantes con CURPs válidas
-- Generado automáticamente el: 2025-07-10 17:30:32
-- Total de registros: 9

-- Crear tabla si no existe
CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curp VARCHAR(18) NOT NULL UNIQUE,
    cct VARCHAR(20),
    carrera VARCHAR(10),
    promedio DECIMAL(4,2),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de estudiantes
INSERT INTO estudiantes (curp, cct, carrera, promedio) VALUES
    ('JOQG231213HCMZNH00', '30ECB0011R', '13', 73.0),
    ('VAKG721231HCHZTN51', '30ECB0007E', '7', 86.0),
    ('UIZA560704MCHTRF53', '30ETH0667Y', '8', 70.0),
    ('MUXO120526HNLKYM59', '30ECB0038Y', '9', 95.0),
    ('WIGY840317HNTQWG04', '30DPT0012K', '8', 95.0),
    ('PENU190104MTCJXX09', '30ECB0005G', '8', 70.0),
    ('OOUF220402HPLFPJ78', '30ETH1028I', '11', 72.0),
    ('CIZR631213HDGHBW69', '30ETH0887J', '18', 72.0),
    ('BEMX141106HTCMZY08', '30ECB0024V', '10', 90.0);

-- Fin del script
