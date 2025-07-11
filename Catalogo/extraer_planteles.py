import pdfplumber
import os
from typing import List, Dict

def extraer_datos_pdf(ruta_pdf: str) -> List[Dict]:
    planteles = []
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                tablas = pagina.extract_tables()
                for tabla in tablas:
                    for fila in tabla:
                        if not fila or len(fila) < 6:
                            continue
                        if fila[0] is None or 'ENTIDAD' in str(fila[0]):
                            continue
                        if any(c is None for c in fila[:6]):
                            continue
                        entidad = str(fila[0]).strip()
                        municipio = str(fila[1]).strip()
                        localidad = str(fila[2]).strip()
                        nombre_plantel = str(fila[3]).strip()
                        subsistema = str(fila[4]).strip()
                        cct = str(fila[5]).strip()
                        if len(cct) == 10:
                            planteles.append({
                                'cct': cct,
                                'entidad': entidad,
                                'municipio': municipio,
                                'localidad': localidad,
                                'nombre_plantel': nombre_plantel,
                                'subsistema': subsistema
                            })
    except Exception as e:
        print(f"Error processing PDF: {e}")
    return planteles

def generar_insert_sql(planteles: List[Dict], archivo_salida: str):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("-- SQL script to insert schools\n")
        from datetime import datetime
        f.write(f"-- Automatically generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total schools: {len(planteles)}\n\n")
        f.write("-- Table: Planteles (PlantelId, Cct, Entidad, Municipio, Localidad, NombrePlantel, Subsistema)\n")
        f.write("INSERT INTO Planteles (PlantelId, Cct, Entidad, Municipio, Localidad, NombrePlantel, Subsistema) VALUES\n")
        valores = []
        for idx, plantel in enumerate(planteles):
            plantel_id = idx + 1
            cct = plantel['cct'].replace("'", "''")
            entidad = plantel['entidad'].replace("'", "''")
            municipio = plantel['municipio'].replace("'", "''")
            localidad = plantel['localidad'].replace("'", "''")
            nombre_plantel = plantel['nombre_plantel'].replace("'", "''")
            subsistema = plantel['subsistema'].replace("'", "''")
            valor = f"({plantel_id}, '{cct}', '{entidad}', '{municipio}', '{localidad}', '{nombre_plantel}', '{subsistema}')"
            valores.append(valor)
        f.write(',\n'.join(valores))
        f.write(';\n\n-- End of script\n')

def main():
    ruta_pdf = r"C:\\Users\\Daniel\\Desktop\\BD\\Catalogo\\Catalogo_Escuelas_MediaSuperior.pdf"
    ruta_sql = r"C:\\Users\\Daniel\\Desktop\\BD\\Mysql Queries\\Planteles.sql"
    print("Starting extraction of data from PDF...")
    planteles = extraer_datos_pdf(ruta_pdf)
    if planteles:
        print(f"Found {len(planteles)} schools in the PDF")
        generar_insert_sql(planteles, ruta_sql)
        print(f"SQL file successfully generated: {ruta_sql}")
        print("\nSample of schools found:")
        for i, plantel in enumerate(planteles[:5]):
            print(f"{i+1}. CCT: {plantel['cct']} - {plantel['nombre_plantel']}")
    else:
        print("No school data found in the PDF")
        print("You may need to adjust the extraction pattern according to the specific PDF structure")

if __name__ == "__main__":
    main() 