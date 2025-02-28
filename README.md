# medkode

**medkode** es una librería en Python que permite extraer, validar y clasificar códigos de Identificación Única de Medicamentos (IUM) según la codificación adoptada por el Ministerio de Salud y Protección Social de Colombia.

## Instalación

Para instalar la librería, usa:
```bash
pip install medkode
```

## Uso

La librería proporciona tres funciones principales para la extracción y validación de códigos IUM en un texto.

### 1. `ium_pipe(texto: str) -> str`
Esta función recibe un texto y devuelve una cadena con los códigos IUM encontrados, clasificados y separados por `|`.

**Ejemplo:**
```python
from medkode import ium_pipe

texto = "El medicamento tiene código 1K1027361200102 y otro código AA1234561234123."
print(ium_pipe(texto))
```
**Salida:**
```
"1K1027361200102,IUM_Ok|AA1234561234123,Err_IUM_4"
```

### 2. `ium_unique(texto: str) -> tuple`
Esta función extrae el primer código IUM válido encontrado en el texto y lo devuelve como una tupla con su clasificación.

**Ejemplo:**
```python
from medkode import ium_unique

texto = "El código 1K1027361200102 es correcto."
print(ium_unique(texto))
```
**Salida:**
```
('1K1027361200102', 'IUM_Ok')
```

### 3. `ium_tuple(texto: str) -> list`
Esta función devuelve una lista de tuplas con todos los códigos IUM encontrados en el texto y su clasificación.

**Ejemplo:**
```python
from medkode import ium_tuple

texto = "Aquí hay dos códigos: 1K1027361200102 y AA1234561234123."
print(ium_tuple(texto))
```
**Salida:**
```
[('1K1027361200102', 'IUM_Ok'), ('AA1234561234123', 'Err_IUM_4')]
```

## Clasificación de códigos IUM

La estructura del código IUM es `NLNNNNNNNNNNNNN`, donde:
- `N` representa un número.
- `L` representa una letra.

### Reglas de validación

Los códigos se validan según las siguientes reglas:

| Expresión Regular | Ejemplo | Clasificación | Error |
|------------------|---------|---------------|---------|
| `\b[0-9][A-Z][0-9]{13}\b` | 1A1234561234123 | IUM_Ok | N1, N2 y N3 completos |
| `\b[0-9][A-Z][0-9]{10}\b` | 1A1234567890 | IUM_N1_N2 | N1, N2 completos |
| `\b[0-9][A-Z][0-9]{6}\b` | 1A123456 | IUM_N1 | N1 completo |
| `\b[0-9][A-Z][0-9]{11,}\b` | 1A12345612341 | Err_IUM_1 | N3 incompleto |
| `\b[A-Z]{2}[0-9]{13}\b` | AA1234561234123 | Err_IUM_4 | El primer dígito debe ser numérico |
| `\b[A-Z][0-9]{13}\b` | A1234561234123 | Err_IUM_8 | Falta primer dígito |


## Referencias oficiales

El Identificador Único de Medicamentos (IUM) es una codificación establecida por el **Ministerio de Salud y Protección Social de Colombia**. Para más información, consulta las siguientes fuentes oficiales:
- [Ministerio de Salud y Protección Social](https://www.minsalud.gov.co/)
- [Normativa sobre Identificación de Medicamentos](https://www.minsalud.gov.co/salud/Lists/Normativa/AllItems.aspx)

## Licencia

Este proyecto está bajo la licencia **MIT**.



