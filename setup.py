import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = [
    "jinja2>=3.0.3",
    "openpyxl>=3.0.9",
    "pandas>=1.1.5",
    "phik>=0.12.0",
    "requests>=2.26.0",
    "scipy>=1.5.4",
    "unidecode>=1.3.2",
    "xlrd>=2.0.1",
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6.2",
)
