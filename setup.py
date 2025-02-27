from setuptools import setup, find_packages

# Leer las dependencias desde requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="p01_codigosmed",  # Nombre del paquete
    version="0.1.7",  # Versión inicial
    author="Juan Paez",
    author_email="jcpaez@gmail.com",
    description="Identificación de los códigos IUM de medicamentos",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/juancarlospaez/p01_codigosmed",  # URL del repositorio
    packages=find_packages(),  # Detecta automáticamente los paquetes
    install_requires=required,  # Usa las dependencias del archivo requirements.txt
    
    include_package_data=True,  # ✅ Permite incluir archivos no Python
    package_data={
        "ecum": ["../data/*.parquet"],  # ✅ Asegura que los archivos .parquet sean incluidos
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
