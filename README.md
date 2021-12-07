# LEILA - Librería de calidad de datos

![screenshot](https://raw.githubusercontent.com/ucd-dnp/leila/master/recursos/LEILA.jpg "LEILA")



[![PyPI version fury.io](https://badge.fury.io/py/leila.svg)](https://pypi.org/project/leila/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/leila.svg)](https://pypi.org/project/leila/)
 [![PyPI license](https://img.shields.io/pypi/l/leila.svg)](https://pypi.org/project/leila/) [![Downloads](https://pepy.tech/badge/leila)](https://pepy.tech/project/leila) [![GitHub forks](https://img.shields.io/github/forks/ucd-dnp/leila.svg?style=social&label=Fork&maxAge=2592000)](https://github.com/ucd-dnp/leila/)

## Descripción

La librería de calidad de datos tiene como objetivo principal ser una herramienta que facilite la verificación de contenido de bases de datos y dé métricas de calidad para que usuarios puedan decidir si sus bases de datos necesitan modificarse para ser utilizadas en los proyectos. La librería fue escrita en el lenguaje de programación de <em>Python</em> y puede analizar bases de datos estructurados que se conviertan en objetos tipo pandas.DataFrame. Contiene tres módulos principales, el módulo <strong>Calidad Datos</strong> para analizar cualquier base de datos, el módulo <strong>Datos gov</strong> para conectarse con los metadatos del Portal de [Datos Abiertos de Colombia](https://www.datos.gov.co/) y utilizar sus bases de datos, y por último el módulo <strong>Reporte</strong> el cual permite generar un reporte de calidad utilizando los módulos anteriores.

La librería surge como resultado de un proyecto relacionado con realizar análisis descriptivos de la calidad de la información cargada al portal de Datos Abiertos de Colombia, durante el desarrollo del proyecto se identifica el interés por parte de diferentes actores en el proyecto al igual que el beneficio potencial de tener a la mano una librería que facilite describir la calidad de una base de datos, lo cual motivó a realizar la implementación de la librería.

- A continuación podrá consultar la siguiente información:
  - [Ejemplo](#ejemplo)
  - [Documentación](#documentaci%C3%B3n)  
  - [Instalación](#instalaci%C3%B3n)
  - [Control de cambios](#controldecambios)
  - [Contribuciones](#contribuciones)
  - [Licencia](#licencia)
  - [Contacto](#contacto)

## Ejemplo

La librería permite generar un reporte de calidad de datos el cual contiene información descriptiva del dataframe analizado, a continuación se presenta el código requerido para generar un reporte a partir de un archivo en Excel en formato .xlsx.

``` python
from leila.reporte import generar_reporte

generar_reporte(datos='datosDeInteres.xlsx')
```

![screenshot](https://raw.githubusercontent.com/ucd-dnp/leila/master/recursos/vista_reporte.gif "Reporte")

## Documentación

La librería cuenta con una documentación que detalla las funciones que la conforman, al igual que ejemplos de uso y demás información de interés relacionada con esta, para acceder a la documentación siga el siguiente link:

[Documentación - LEILA - Librería de calidad de datos.](https://ucd-dnp.github.io/leila/)

## Instalación

Para la instalación de la librería se recomienda utilizar el gestor de paquetes ``pip``, por buenas prácticas se sugiere antes de la instalación crear un entorno virtual que permita aislar las librerías y evitar conflictos de versiones con el entorno de desarrollo base del computador.

``` linux
pip install leila
```

De manera alterna también puede utilizar el gestor de paquetes ``conda``.

```
conda install -c ucd-dnp leila
```
## Control de cambios

Para ver todos los cambios en las versiones de `LEILA` ver el archivo [changelog](https://github.com/ucd-dnp/leila/wiki/Changelog)
## Contribuciones a LEILA

Todas las contribuciones, reportes de errores, corrección de errores, las mejoras de la documentación y las ideas son bienvenidas.

Puede encontrar una descripción detallada de cómo contribuir en la [Wiki de LEILA](https://github.com/ucd-dnp/leila/wiki)

También lo invitamos a revisar el [:calendar: Tablero **TODO** de LEILA](https://github.com/users/ucd-dnp/projects/3), donde hay una serie de temas listados en los que el equipo UCD se encuentra trabajando.

## Licencia [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

### **MIT License** 

La librería LEILA - Calidad de datos se encuentra publicada bajo la licencia MIT <br />
Copyleft (c) 2020 Departamento Nacional de Planeación - DNP Colombia

Para mayor información puede consultar el archivo de [Licencia](https://github.com/ucd-dnp/leila/blob/master/LICENSE)

## Contacto

Para comunicarse con la Unidad de Científicos de Datos (UCD) de la Dirección de Desarrollo Digital (DDD) del DNP, lo puede hacer mediante el correo electrónico ucd@dnp.gov.co
