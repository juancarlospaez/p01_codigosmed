import pandas as pd
import re
import unidecode
import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import numpy as np
import os

# Cargar las variables globalmente una sola vez
patrones = None
DICRE = None
lpatrones = None

def initialize():
    global patrones, DICRE, lpatrones
    if patrones is None or DICRE is None or lpatrones is None:
        patrones = load_patterns()
        DICRE, lpatrones = load_parametric_tables()

def load_patterns():
    return [
        (r'\A[0-9]+\Z', 'NE'),
        (r'\A[0-9.]+\Z', 'NP'),
        (r'\A[A-Z]+\Z', 'AE'),
        (r'\A[A-Z.]+\Z', 'AP'),
        (r'\A[A-Z0-9]+\Z', 'AN'),
        (r'\A[A-Z0-9.]+\Z', 'AQ')
    ]

def load_parametric_tables():
    # Obtener la ruta absoluta de la carpeta del paquete
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta correcta para acceder a la carpeta "data"
    data_path = os.path.join(base_path, "..", "data")

    # Construir rutas completas de los archivos parquet
    file_tpecum = os.path.join(data_path, "TPECUM.parquet")
    file_tpecum_sec = os.path.join(data_path, "TPECUM_SEC.parquet")

    # Verificar si los archivos existen antes de cargarlos
    if not os.path.exists(file_tpecum):
        raise FileNotFoundError(f"El archivo {file_tpecum} no existe. Verifica la ubicación.")

    if not os.path.exists(file_tpecum_sec):
        raise FileNotFoundError(f"El archivo {file_tpecum_sec} no existe. Verifica la ubicación.")

    # Cargar las tablas
    TPECUM = pd.read_parquet(file_tpecum)
    DICRE = {j: TPECUM[TPECUM['CLASL'] == j][['RE', 'CLASLR']].to_numpy() for j in TPECUM['CLASL'].unique()}

    TPECUM_SEC = pd.read_parquet(file_tpecum_sec)
    lpatrones = TPECUM_SEC[['PATRON', 'cod_err']].to_numpy()

    return DICRE, lpatrones


def ClasTexARRAY(text):
    tokens = descripNorm(text)
    return np.array([(token, ClasToken(token)[1], i) for i, token in enumerate(tokens)], dtype=object)

"""
def ClasToken(token):
    return next(((token, k) for j, k in patrones if re.match(j, token)), (token, 'ER'))
"""

def ClasToken(token):
    # Verificar que patrones exista y no sea None
    if patrones is not None:
        # Usar una lista por comprensión dentro del next()
        return next(((token, k) for j, k in patrones if re.match(j, token)), (token, 'ER'))
    else:
        # Si patrones es None o está vacío, devolver un valor por defecto
        return (token, 'ER')




def descripNorm(text):
    return [word.upper() for word in wordpunct_tokenize(NormT1(text)) if word not in stopwords.words('spanish') and word != "."]

def NormT1(string):
    return " ".join(re.sub(r"[^a-zA-Z0-9]", " ", unidecode.unidecode(string).lower()).split())

"""
def PATRONVAL(qw):
    return next((n for p, n in DICRE.get(qw[1], []) if re.match(p, qw[0])), 0)
"""

def PATRONVAL(qw):
    # Verificar que DICRE no sea None
    if DICRE is not None:
        # Continuar con la búsqueda usando .get()
        return next((n for p, n in DICRE.get(qw[1], []) if re.match(p, qw[0])), 0)
    else:
        # Si DICRE es None, devolver el valor por defecto
        return 0
"""
def packIUM(text):
    tokens = ClasTexARRAY(text)
    resultado1 = [PATRONVAL((token[0], token[1])) for token in tokens]
    strVEC = "".join(["aaaa" if x == 0 else str(x) for x in resultado1])
    
    dfmatch = pd.DataFrame([(int(match.start() / 4), int(match.end() / 4), jpatr[1])
                             for jpatr in lpatrones for match in re.finditer(jpatr[0], strVEC)],
                            columns=['a', 'b', 'c']).drop_duplicates('a', keep='first')
    return [("".join(tokens[int(k1):int(k2), 0]), k3) for k1, k2, k3 in dfmatch.to_numpy()]
"""

"""
def packIUM(text):
    tokens = ClasTexARRAY(text)
    resultado1 = [PATRONVAL((token[0], token[1])) for token in tokens]
    strVEC = "".join(["aaaa" if x == 0 else str(x) for x in resultado1])
    
    dfmatch = pd.DataFrame([(int(match.start() / 4), int(match.end() / 4), jpatr[1])
                             for jpatr in lpatrones for match in re.finditer(jpatr[0], strVEC)],
                            columns=['a', 'b', 'c']).drop_duplicates('a', keep='first')
    unique_results = set((("".join(tokens[int(k1):int(k2), 0])), k3) for k1, k2, k3 in dfmatch.to_numpy())
    return list(unique_results)
"""


def packIUM(text):
    tokens = ClasTexARRAY(text)
    resultado1 = [PATRONVAL((token[0], token[1])) for token in tokens]
    strVEC = "".join(["aaaa" if x == 0 else str(x) for x in resultado1])
    
    # Verificar si lpatrones existe y no es None
    if lpatrones is not None:
        dfmatch = pd.DataFrame([(int(match.start() / 4), int(match.end() / 4), jpatr[1])
                                for jpatr in lpatrones for match in re.finditer(jpatr[0], strVEC)],
                               columns=['a', 'b', 'c']).drop_duplicates('a', keep='first')
        
        # Verificar si dfmatch existe y tiene datos
        if not dfmatch.empty:
            # Crear conjunto de resultados únicos
            unique_results = set((("".join(tokens[int(k1):int(k2), 0])), k3) for k1, k2, k3 in dfmatch.to_numpy())
            return list(unique_results)
    
    # Si lpatrones es None o no hay coincidencias, devolver una lista vacía
    return []

"""
def packIUMuno(text):
    return next(iter(packIUM(text)), (0, "SIN_IUM"))
"""
def packIUMuno(text):
    # Obtenemos los resultados de packIUM y los convertimos a un conjunto para eliminar duplicados
    results = set(packIUM(text))
    # Tomamos el primer elemento o el valor por defecto
    return next(iter(results), (0, "SIN_IUM"))


#def packIUMtotEXC(text):
#    return "|".join(f"{j[0]},{j[1]}" for j in packIUM(text)) or "0,SIN_IUM"
 
def packIUMtotEXC(text):
    # Aplicamos set() para eliminar duplicados
    unique_results = set(f"{j[0]},{j[1]}" for j in packIUM(text))
    # Unimos los resultados con "|" o devolvemos el valor por defecto si no hay resultados
    return "|".join(unique_results) or "0,SIN_IUM"

initialize()  # Se llama una sola vez para cargar los valores en memoria

if __name__ == "__main__":
    textor = '1K1027361000103,IUM_Ok|1K1027361200102,IUM_Ok|AA1234561234123,Err_IUM_4|AA1234561234123,Err_IUM_4|AA1234561234123,Err_IUM_4|AA1234561234123,Err_IUM_4'
    print(packIUMtotEXC(textor))
    print(packIUMuno(textor))
    print(packIUM(textor))
