import csv
import os
from datetime import datetime

# Obtener la ruta absoluta del archivo CSV
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(ruta_actual, 'Carreras.csv')

# Leer el archivo CSV
carreras = []
with open(ruta_csv, 'r', encoding='utf-8-sig') as archivo:
    lector = csv.reader(archivo)
    for fila in lector:
        if len(fila) >= 2:
            clave_carrera = fila[0].strip().replace('\ufeff', '')  # Elimina BOM si existe
            nombre_carrera = fila[1].strip()
            carreras.append((clave_carrera, nombre_carrera))

# Generar el query SQL con solo los INSERT statements
sql = "-- Script SQL para insertar carreras\n"
sql += f"-- Generado automáticamente el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
sql += f"-- Total de carreras: {len(carreras)}\n\n"

sql += "-- Insertar datos de carreras\n"
sql += "INSERT INTO carreras (clave_carrera, nombre_carrera) VALUES\n"

valores = []
for clave_carrera, nombre_carrera in carreras:
    # Escapar comillas simples en los valores
    clave_escaped = clave_carrera.replace("'", "''")
    nombre_escaped = nombre_carrera.replace("'", "''")
    valores.append(f"('{clave_escaped}', '{nombre_escaped}')")

sql += ",\n".join(valores) + ";\n\n"
sql += "-- Fin del script\n"

# Guardar en Mysql Queries
ruta_sql = os.path.join(ruta_actual, '../Mysql Queries/insert_carreras.sql')
with open(ruta_sql, 'w', encoding='utf-8') as archivo:
    archivo.write(sql)

print("Query SQL generado exitosamente en Mysql Queries/insert_carreras.sql")
print(f"Total de carreras procesadas: {len(carreras)}") 