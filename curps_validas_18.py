import pandas as pd
import re
import json
from datetime import datetime

# Diccionario completo de entidades federativas
ENTIDADES = {
    'AG': 'Aguascalientes', 'BC': 'Baja California', 'BS': 'Baja California Sur',
    'CC': 'Campeche', 'CL': 'Coahuila', 'CM': 'Colima', 'CS': 'Chiapas',
    'CH': 'Chihuahua', 'DF': 'Ciudad de México', 'DG': 'Durango', 'GT': 'Guanajuato',
    'GR': 'Guerrero', 'HG': 'Hidalgo', 'JC': 'Jalisco', 'MC': 'México',
    'MN': 'Michoacán', 'MS': 'Morelos', 'NT': 'Nayarit', 'NL': 'Nuevo León',
    'OC': 'Oaxaca', 'PL': 'Puebla', 'QT': 'Querétaro', 'QR': 'Quintana Roo',
    'SP': 'San Luis Potosí', 'SL': 'Sinaloa', 'SR': 'Sonora', 'TC': 'Tabasco',
    'TS': 'Tamaulipas', 'TL': 'Tlaxcala', 'VZ': 'Veracruz', 'YN': 'Yucatán',
    'ZS': 'Zacatecas', 'NE': 'Nacido en el Extranjero'
}

def validar_letras(texto, cantidad):
    return len(texto) == cantidad and texto.isalpha()

def validar_numeros(texto, cantidad):
    return len(texto) == cantidad and texto.isdigit()

def validar_fecha(fecha_str):
    if not validar_numeros(fecha_str, 6):
        return False
    try:
        anio = int(fecha_str[:2])
        mes = int(fecha_str[2:4])
        dia = int(fecha_str[4:6])
        if mes < 1 or mes > 12:
            return False
        if dia < 1 or dia > 31:
            return False
        if mes in [4, 6, 9, 11] and dia > 30:
            return False
        if mes == 2:
            siglo = 2000 if anio <= 24 else 1900
            anio_completo = siglo + anio
            if anio_completo % 4 == 0 and (anio_completo % 100 != 0 or anio_completo % 400 == 0):
                if dia > 29:
                    return False
            else:
                if dia > 28:
                    return False
        return True
    except ValueError:
        return False

def validar_sexo(sexo):
    return sexo in ['H', 'M']

def validar_entidad(entidad):
    return entidad in ENTIDADES

def validar_curp_18(curp):
    """Valida si una CURP tiene formato válido de 18 caracteres"""
    if not isinstance(curp, str):
        curp = str(curp)
    curp_limpia = curp.strip().upper()
    
    # Verificar longitud exacta de 18 caracteres
    if len(curp_limpia) != 18:
        return False
    
    # Verificar formato completo: 4 letras + 6 números + H/M + 5 letras + 2 alfanuméricos
    if not re.match(r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9A-Z]{2}$', curp_limpia):
        return False
    
    # Extraer componentes para validación específica
    fecha = curp_limpia[4:10]
    sexo = curp_limpia[10]
    entidad = curp_limpia[11:13]
    
    # Validar fecha
    if not validar_fecha(fecha):
        return False
    
    # Validar sexo
    if not validar_sexo(sexo):
        return False
    
    # Validar entidad
    if not validar_entidad(entidad):
        return False
    
    return True

def extraer_curps_validas_18():
    """Extrae solo las CURPs válidas de 18 caracteres con todos sus datos"""
    try:
        # Leer el archivo Excel
        df = pd.read_excel('Aspirantes.xlsx', sheet_name='Aspirantes')
        print(f"Archivo leído correctamente. Total de registros: {len(df)}")
        
        # Leer el archivo de carreras y crear diccionario de mapeo
        carreras_dict = {}
        try:
            df_carreras = pd.read_csv('Carreras.csv', header=None, names=['numero', 'nombre'])
            for _, row in df_carreras.iterrows():
                carreras_dict[str(row['numero'])] = row['nombre']
            print(f"Archivo de carreras leído. Total de carreras: {len(carreras_dict)}")
        except Exception as e:
            print(f"Error al leer archivo de carreras: {e}")
            carreras_dict = {}
        
        # Filtrar CURPs válidas de 18 caracteres con todos sus datos
        curps_validas = []
        datos_completos = []
        
        for index, row in df.iterrows():
            curp = str(row['CURP'])
            if validar_curp_18(curp):
                curp_limpia = curp.strip().upper()
                curps_validas.append(curp_limpia)
                
                # Obtener número de carrera
                numero_carrera = str(row.get('Carreras', ''))
                
                # Obtener todos los datos del registro
                datos_registro = {
                    'CURP': curp_limpia,
                    'CCT': str(row.get('CCT', '')),
                    'Carrera': numero_carrera,
                    'Promedio': str(row.get('Promedio', ''))
                }
                datos_completos.append(datos_registro)
        
        print(f"\n=== CURPs VÁLIDAS DE 18 CARACTERES ===")
        print(f"Total de CURPs válidas encontradas: {len(curps_validas)}")
        print(f"Porcentaje de CURPs válidas: {len(curps_validas)/len(df)*100:.1f}%")
        
        if curps_validas:
            print(f"\nCURPs válidas (en una fila):")
            print(", ".join(curps_validas))
            
            # Guardar solo CURPs en archivo de texto
            with open('curps_validas_18.txt', 'w', encoding='utf-8') as f:
                f.write(", ".join(curps_validas))
            print(f"CURPs válidas guardadas en 'curps_validas_18.txt'")
            
            # Guardar datos completos en JSON
            with open('curps_validas_18_datos.json', 'w', encoding='utf-8') as f:
                json.dump(datos_completos, f, ensure_ascii=False, indent=2)
            print(f"Datos completos guardados en 'curps_validas_18_datos.json'")
            
            # Mostrar ejemplo de los datos
            print(f"\nEjemplo de datos guardados:")
            if datos_completos:
                print(json.dumps(datos_completos[0], ensure_ascii=False, indent=2))
        else:
            print("No se encontraron CURPs válidas de 18 caracteres.")
            
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    extraer_curps_validas_18() 