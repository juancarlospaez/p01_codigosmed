# 📦 Procesador de Códigos IUM

Este paquete permite la validación y clasificación de códigos IUM utilizando expresiones regulares y tablas paramétricas.

## 🚀 Instalación

Asegúrate de tener las dependencias necesarias instaladas:

```sh
pip install pandas numpy nltk unidecode
```

## 📂 Estructura del Proyecto

```
mi_paquete/
│── data/
│   ├── TPECUM.parquet
│   ├── TPECUM_SEC.parquet
│── main.py
│── requirements.txt
│── setup.py
│── README.md
```

## 🛠️ Uso

Ejemplo de ejecución:

```python
from mi_paquete import packIUMtotEXC, packIUMuno, packIUM, load_patterns, load_parametric_tables

# Cargar patrones y tablas paramétricas
patrones = load_patterns()
DICRE, lpatrones = load_parametric_tables()

# Texto de prueba
testor = '1K1027361000103,IUM_Ok|1K1027361200102,IUM_Ok|AA1234561234123,Err_IUM_4'

# Procesamiento de códigos IUM
print(packIUMtotEXC(testor, patrones, DICRE, lpatrones))
print(packIUMuno(testor, patrones, DICRE, lpatrones))
print(packIUM(testor, patrones, DICRE, lpatrones))
```

## 📌 Funciones Principales

### `packIUMtotEXC(text, patrones, DICRE, lpatrones)`

🔹 Devuelve una cadena con los códigos y sus respectivas clasificaciones separadas por `|`.

### `packIUMuno(text, patrones, DICRE, lpatrones)`

🔹 Retorna solo el primer código clasificado o `0, SIN_IUM` si no se encuentra ninguno.

### `packIUM(text, patrones, DICRE, lpatrones)`

🔹 Devuelve una lista de códigos y su clasificación basada en patrones paramétricos.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

