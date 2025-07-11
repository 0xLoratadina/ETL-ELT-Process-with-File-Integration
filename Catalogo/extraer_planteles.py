import pdfplumber
import re
import os
from typing import List, Dict

def extraer_datos_pdf(ruta_pdf: str) -> List[Dict]:
    planteles = []
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    lineas = texto.split('\n')
                    for linea in lineas:
                        datos = procesar_linea_plantel(linea)
                        if datos:
                            planteles.append(datos)
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
    return planteles

def procesar_linea_plantel(linea: str) -> Dict | None:
    linea = linea.strip()
    if not linea or len(linea) < 10:
        return None
    if linea.startswith('ENTIDAD MUNICIPIO LOCALIDAD'):
        return None
    cct_pattern = r'(\b\d{2}[A-Z]{3}\d{4}[A-Z]\b)$'
    cct_match = re.search(cct_pattern, linea)
    if cct_match:
        cct = cct_match.group(1)
        linea_sin_cct = linea[:cct_match.start()].strip()
        partes = linea_sin_cct.split()
        if len(partes) < 5:
            return None
        entidad = partes[0]
        municipio = partes[1]
        localidad = partes[2]
        if len(partes) == 5:
            nombre_plantel = partes[3]
            subsistema = partes[4]
        else:
            nombre_plantel = ' '.join(partes[3:-1])
            subsistema = partes[-1]
        return {
            'cct': cct,
            'entidad': entidad,
            'municipio': municipio,
            'localidad': localidad,
            'nombre_plantel': nombre_plantel,
            'subsistema': subsistema
        }
    return None

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