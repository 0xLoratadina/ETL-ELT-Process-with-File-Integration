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
                        # Validar que la fila tenga al menos 6 columnas y que ninguna sea None
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
                        # Validar CCT
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
        print(f"Error al procesar el PDF: {e}")
    return planteles

def generar_insert_sql(planteles: List[Dict], archivo_salida: str):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("INSERT INTO planteles (cct, entidad, municipio, localidad, nombre_plantel, subsistema) VALUES\n")
        valores = []
        for plantel in planteles:
            cct = plantel['cct'].replace("'", "''")
            entidad = plantel['entidad'].replace("'", "''")
            municipio = plantel['municipio'].replace("'", "''")
            localidad = plantel['localidad'].replace("'", "''")
            nombre_plantel = plantel['nombre_plantel'].replace("'", "''")
            subsistema = plantel['subsistema'].replace("'", "''")
            valor = f"('{cct}', '{entidad}', '{municipio}', '{localidad}', '{nombre_plantel}', '{subsistema}')"
            valores.append(valor)
        f.write(',\n'.join(valores))
        f.write(';')

def main():
    ruta_pdf = r"C:\Users\Daniel\Desktop\BD\Catalogo\Catalogo_Escuelas_MediaSuperior.pdf"
    ruta_sql = r"C:\Users\Daniel\Desktop\BD\Mysql Queries\insert_planteles.sql"
    print("Iniciando extracción de datos del PDF...")
    planteles = extraer_datos_pdf(ruta_pdf)
    if planteles:
        print(f"Se encontraron {len(planteles)} planteles en el PDF")
        generar_insert_sql(planteles, ruta_sql)
        print(f"Archivo SQL generado exitosamente: {ruta_sql}")
        print("\nEjemplos de planteles encontrados:")
        for i, plantel in enumerate(planteles[:5]):
            print(f"{i+1}. CCT: {plantel['cct']} - {plantel['nombre_plantel']}")
    else:
        print("No se encontraron datos de planteles en el PDF")
        print("Es posible que necesites ajustar el patrón de extracción según la estructura específica del PDF")

if __name__ == "__main__":
    main() 