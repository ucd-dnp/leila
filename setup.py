import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leila-ucd-dnp", # Replace with your own username
    version="0.0.1",
    author="Departamento Nacional de Planeación - DNP",
    author_email="ucd@dnp.gov.co",
    description="calidad de datos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ucd-dnp/calidad_datos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: WINDOWS",
    ],
    python_requires='>=3.6',
)