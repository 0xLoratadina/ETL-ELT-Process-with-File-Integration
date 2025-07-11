import csv
import os
from datetime import datetime

# Get absolute path for the CSV file
current_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_path, 'Carreras.csv')

# Read the CSV file
carreras = []
with open(csv_path, 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    for idx, row in enumerate(reader):
        if len(row) >= 2:
            clave_carrera = row[0].strip().replace('\ufeff', '')
            nombre_carrera = row[1].strip()
            carreras.append((idx + 1, clave_carrera, nombre_carrera))  # CarreraId autoincremental simulado

# Generate the SQL INSERT statements
sql = "-- SQL script to insert careers\n"
sql += f"-- Automatically generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
sql += f"-- Total careers: {len(carreras)}\n\n"
sql += "-- Table: Carreras (CarreraId, ClaveCarrera, NombreCarrera)\n"
sql += "INSERT INTO Carreras (CarreraId, ClaveCarrera, NombreCarrera) VALUES\n"

values = []
for carrera_id, clave_carrera, nombre_carrera in carreras:
    clave_escaped = clave_carrera.replace("'", "''")
    nombre_escaped = nombre_carrera.replace("'", "''")
    values.append(f"({carrera_id}, '{clave_escaped}', '{nombre_escaped}')")

sql += ",\n".join(values) + ";\n\n"
sql += "-- End of script\n"

# Save to Mysql Queries
sql_path = os.path.join(current_path, '../Mysql Queries/Carreras.sql')
with open(sql_path, 'w', encoding='utf-8') as file:
    file.write(sql)

print("SQL query successfully generated in Mysql Queries/Carreras.sql")
print(f"Total careers processed: {len(carreras)}") 