import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = [
    "jinja2>=3.1.0",
    "openpyxl>=3.1.0",
    "pandas>=2.0.0",
    "phik>=0.12.0",
    "requests>=2.31.0",
    "scipy>=1.10.0",
    "unidecode>=1.3.0",
    "xlrd>=2.0.1",
    "numpy>=1.24.0",
]
PACKAGE_NAME = "leila"

setuptools.setup(
    name=PACKAGE_NAME,
    version="0.2",
    author="Departamento Nacional de Planeación - DNP",
    author_email="ucd@dnp.gov.co",
    maintainer="Unidad de Científicos de Datos - UCD",
    maintainer_email="ucd@dnp.gov.co",
    description=(
        "Librería para medir la calidad de los datos en conjuntos "
        "de datos estructurados"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=[
        "Python",
        "Calidad de datos",
        "UCD",
        "DNP",
    ],
    url="https://github.com/ucd-dnp/leila",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    project_urls={
        "Documentación": "https://ucd-dnp.github.io/leila/",
        "Seguimiento de fallas": "https://github.com/ucd-dnp/leila/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
