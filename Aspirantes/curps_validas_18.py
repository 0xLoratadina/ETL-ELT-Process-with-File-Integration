import pandas as pd
import re
import json
from datetime import datetime, date
import os
import csv

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

def validar_fecha_curp(fecha_str):
    """Valida que la fecha de nacimiento en la CURP sea válida"""
    if not validar_numeros(fecha_str, 6):
        return False
    try:
        anio = int(fecha_str[:2])
        mes = int(fecha_str[2:4])
        dia = int(fecha_str[4:6])
        
        # Validar mes (1-12)
        if mes < 1 or mes > 12:
            return False
        
        # Validar día según el mes
        dias_por_mes = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if dia < 1 or dia > dias_por_mes[mes]:
            return False
        
        # Validar febrero en años bisiestos
        if mes == 2:
            siglo = 2000 if anio <= int(str(date.today().year)[2:]) else 1900
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

def validar_letras(texto, cantidad):
    return len(texto) == cantidad and texto.isalpha()

def validar_numeros(texto, cantidad):
    return len(texto) == cantidad and texto.isdigit()

def validar_sexo(sexo):
    return sexo in ['H', 'M', 'X']

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
    
    # Verificar formato completo: 4 letras + 6 números + H/M/X + 5 letras + 2 alfanuméricos
    if not re.match(r'^[A-Z]{4}[0-9]{6}[HMX][A-Z]{5}[0-9A-Z]{2}$', curp_limpia):
        return False
    
    # Extraer componentes para validación específica
    fecha = curp_limpia[4:10]
    sexo = curp_limpia[10]
    entidad = curp_limpia[11:13]
    
    # Validar fecha
    if not validar_fecha_curp(fecha):
        return False
    
    # Validar sexo
    if not validar_sexo(sexo):
        return False
    
    # Validar entidad
    if not validar_entidad(entidad):
        return False
    
    return True

def extraer_info_curp(curp):
    """Extrae sexo (Masculino/Femenino), fecha de nacimiento (DD/MM/AAAA) y edad de la CURP"""
    curp = curp.strip().upper()
    # Fecha de nacimiento
    fecha_raw = curp[4:10]  # AAMMDD
    anio = int(fecha_raw[:2])
    mes = int(fecha_raw[2:4])
    dia = int(fecha_raw[4:6])
    # Determinar siglo
    anio_completo = 2000 + anio if anio <= int(str(date.today().year)[2:]) else 1900 + anio
    fecha_nacimiento = f"{dia:02d}/{mes:02d}/{anio_completo}"
    # Edad
    hoy = date.today()
    edad = hoy.year - anio_completo - ((hoy.month, hoy.day) < (mes, dia))
    # Sexo
    sexo_curp = curp[10]
    sexo = "Masculino" if sexo_curp == 'H' else "Femenino"
    return sexo, fecha_nacimiento, edad

def cargar_diccionario_carreras():
    path = os.path.join('Mysql Queries', 'Carreras.sql')
    carreras = {}
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('('):
                    parts = line.strip('(),\n ').split(',')
                    if len(parts) >= 3:
                        carrera_id = int(parts[0])
                        clave = parts[1].strip().strip("'")
                        carreras[clave] = carrera_id
    return carreras

def cargar_diccionario_planteles():
    path = os.path.join('Mysql Queries', 'Planteles.sql')
    planteles = {}
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('('):
                    parts = line.strip('(),\n ').split(',')
                    if len(parts) >= 7:
                        plantel_id = int(parts[0])
                        cct = parts[1].strip().strip("'")
                        entidad = parts[2].strip().strip("'")
                        municipio = parts[3].strip().strip("'")
                        planteles[cct] = {
                            'PlantelId': plantel_id,
                            'Entidad': entidad,
                            'Municipio': municipio
                        }
    return planteles

def generar_archivo_sql_estudiantes(datos_completos):
    os.makedirs('Mysql Queries', exist_ok=True)
    sql_path = os.path.join('Mysql Queries', 'Estudiantes.sql')
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write("-- SQL script to insert students\n")
        f.write(f"-- Automatically generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total students: {len(datos_completos)}\n\n")
        f.write("-- Table: Estudiantes (EstudianteId, Curp, Sexo, Edad, FechaNacimiento, Promedio, CarreraId, PlantelId, Entidad, Municipio)\n")
        f.write("INSERT INTO Estudiantes (EstudianteId, Curp, Sexo, Edad, FechaNacimiento, Promedio, CarreraId, PlantelId, Entidad, Municipio) VALUES\n")
        valores = []
        for idx, dato in enumerate(datos_completos):
            estudiante_id = idx + 1
            curp = dato.get('CURP', '').replace("'", "''")
            sexo = dato.get('Sexo', '').replace("'", "''")
            edad = dato.get('Edad', '')
            fecha_nacimiento = dato.get('FechaNacimiento', '')
            promedio = dato.get('Promedio', None)
            carrera_id = dato.get('CarreraId', 'NULL')
            plantel_id = dato.get('PlantelId', 'NULL')
            entidad = dato.get('Entidad', '').replace("'", "''")
            municipio = dato.get('Municipio', '').replace("'", "''")
            edad_str = str(edad) if edad not in [None, ''] else 'NULL'
            fecha_nac_str = f"'{fecha_nacimiento}'" if fecha_nacimiento else 'NULL'
            promedio_str = str(promedio) if promedio not in [None, ''] else 'NULL'
            valor = f"({estudiante_id}, '{curp}', '{sexo}', {edad_str}, {fecha_nac_str}, {promedio_str}, {carrera_id}, {plantel_id}, '{entidad}', '{municipio}')"
            valores.append(valor)
        f.write(',\n'.join(valores))
        f.write(';\n\n-- End of script\n')

def extraer_curps_validas_18():
    try:
        df = pd.read_excel('Aspirantes/Aspirantes.xlsx', sheet_name='Aspirantes')
        print(f"File read successfully. Total records: {len(df)}")
        carreras_dict = cargar_diccionario_carreras()
        planteles_dict = cargar_diccionario_planteles()
        datos_completos = []
        curps_validas = []
        
        for index, row in df.iterrows():
            curp = str(row['CURP'])
            if validar_curp_18(curp):
                curps_validas.append(curp.strip().upper())
                sexo, fecha_nacimiento, edad = extraer_info_curp(curp)
                
                curp_limpia = curp.strip().upper()
                numero_carrera = str(row.get('Carreras', ''))
                cct = str(row.get('CCT', ''))
                promedio = row.get('Promedio', '')
                
                carrera_id = carreras_dict.get(numero_carrera, 'NULL')
                plantel_info = planteles_dict.get(cct, {})
                plantel_id = plantel_info.get('PlantelId', 'NULL')
                entidad = plantel_info.get('Entidad', '')
                municipio = plantel_info.get('Municipio', '')
                
                datos_registro = {
                    'CURP': curp_limpia,
                    'Promedio': promedio,
                    'Sexo': sexo,
                    'FechaNacimiento': fecha_nacimiento,
                    'Edad': edad,
                    'CarreraId': carrera_id,
                    'PlantelId': plantel_id,
                    'Entidad': entidad,
                    'Municipio': municipio
                }
                datos_completos.append(datos_registro)
        
        print(f"\n=== VALID 18-CHAR CURPs ===")
        print(f"Total valid CURPs found: {len(curps_validas)}")
        print(f"Percentage of valid CURPs: {len(curps_validas)/len(df)*100:.1f}%")
        
        if curps_validas:
            print(f"\nValid CURPs found:")
            for curp in curps_validas:
                print(f"- {curp}")
            
            os.makedirs('DB Jsons', exist_ok=True)
            with open('DB Jsons/estudiantes.json', 'w', encoding='utf-8') as f:
                json.dump(datos_completos, f, ensure_ascii=False, indent=2)
            print(f"Student data saved in 'DB Jsons/estudiantes.json'")
            generar_archivo_sql_estudiantes(datos_completos)
            print(f"SQL file generated: 'Mysql Queries/Estudiantes.sql'")
            print(f"\nSample of saved data:")
            print(json.dumps(datos_completos[0], ensure_ascii=False, indent=2))
        else:
            print("No valid 18-character CURPs found.")
    except Exception as e:
        print(f"Error processing the file: {e}")

if __name__ == "__main__":
    extraer_curps_validas_18() 