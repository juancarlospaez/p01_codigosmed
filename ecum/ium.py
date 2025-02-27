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

    # Obtener la ruta absoluta de la carpeta donde se encuentra este script (ium.py)
    base_path = os.path.dirname(os.path.abspath(__file__))  

    # Subir un nivel y acceder a la carpeta donde está el archivo
    parent_path = os.path.abspath(os.path.join(base_path, "..", "data"))
    # Construir la ruta completa del archivo
    file_path = os.path.join(parent_path, "TPECUM.parquet")
    TPECUM = pd.read_parquet(file_path)
    DICRE = {j: TPECUM[TPECUM['CLASL'] == j][['RE', 'CLASLR']].to_numpy() for j in TPECUM['CLASL'].unique()}


    # Obtener la ruta absoluta de la carpeta donde se encuentra este script (ium.py)
    base_path = os.path.dirname(os.path.abspath(__file__))  
    # Subir un nivel y acceder a la carpeta donde está el archivo
    parent_path = os.path.abspath(os.path.join(base_path, "..", "data"))
    # Construir la ruta completa del archivo
    file_path = os.path.join(parent_path, "TPECUM_SEC.parquet")
    TPECUM_SEC = pd.read_parquet(file_path)
    lpatrones = TPECUM_SEC[['PATRON', 'cod_err']].to_numpy()
    return DICRE, lpatrones

def ClasTexARRAY(text):
    tokens = descripNorm(text)
    return np.array([(token, ClasToken(token)[1], i) for i, token in enumerate(tokens)], dtype=object)

def ClasToken(token):
    return next(((token, k) for j, k in patrones if re.match(j, token)), (token, 'ER'))

def descripNorm(text):
    return [word.upper() for word in wordpunct_tokenize(NormT1(text)) if word not in stopwords.words('spanish') and word != "."]

def NormT1(string):
    return " ".join(re.sub(r"[^a-zA-Z0-9]", " ", unidecode.unidecode(string).lower()).split())

def PATRONVAL(qw):
    return next((n for p, n in DICRE.get(qw[1], []) if re.match(p, qw[0])), 0)

def packIUM(text):
    tokens = ClasTexARRAY(text)
    resultado1 = [PATRONVAL((token[0], token[1])) for token in tokens]
    strVEC = "".join(["aaaa" if x == 0 else str(x) for x in resultado1])
    
    dfmatch = pd.DataFrame([(int(match.start() / 4), int(match.end() / 4), jpatr[1])
                             for jpatr in lpatrones for match in re.finditer(jpatr[0], strVEC)],
                            columns=['a', 'b', 'c']).drop_duplicates('a', keep='first')
    return [("".join(tokens[int(k1):int(k2), 0]), k3) for k1, k2, k3 in dfmatch.to_numpy()]

def packIUMuno(text):
    return next(iter(packIUM(text)), (0, "SIN_IUM"))

def packIUMtotEXC(text):
    return "|".join(f"{j[0]},{j[1]}" for j in packIUM(text)) or "0,SIN_IUM"



initialize()  # Se llama una sola vez para cargar los valores en memoria


if __name__ == "__main__":
    textor = '1K1027361000103,IUM_Ok|1K1027361200102,IUM_Ok|AA1234561234123,Err_IUM_4'
    print(packIUMtotEXC(textor))
    print(packIUMuno(textor))
    print(packIUM(textor))
