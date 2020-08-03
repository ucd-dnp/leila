# LEILA - Librería de calidad de datos

![screenshot](docs/_static/image/LEILA.jpg "LEILA")

## Descripción

La librería de calidad de datos tiene como objetivo principal ser una herramienta que facilite la verificación de contenido de bases de datos y dé métricas de calidad para que usuarios puedan decidir si sus bases de datos necesitan modificarse para ser utilizadas en los proyectos. La librería fue escrita en el lenguaje de programación de <em>Python</em> y puede analizar bases de datos estructurados que se conviertan en objetos dataframe. Contiene tres módulos principales, el módulo <strong>Calidad Datos</strong> para analizar cualquier base de datos, el módulo <strong>Datos gov</strong> para conectarse con los metadatos del Portal de [Datos Abiertos de Colombia](https://www.datos.gov.co/) y utilizar sus bases de datos, y por último el módulo <strong>Reporte</strong> el cual permite generar un reporte de calidad utilizando los módulos anteriores.

La librería surge como resultado de un proyecto relacionado con realizar análisis descriptivos de la calidad de la información cargada al portal de Datos Abiertos de Colombia, durante el desarrollo del proyecto se identifica el interés por parte de diferentes actores en el proyecto al igual que el beneficio potencial de tener a la mano una librería que facilite describir la calidad de una base de datos, lo cual motivó a realizar la implementación de la librería.

- A continuación podrá consultar la siguiente información:
  - [Ejemplo](#ejemplo)
  - [Documentación](#documentaci%C3%B3n)  
  - [Instalación](#instalaci%C3%B3n)
  - [Contribuciones](#contribuciones)
  - [Licencia](#licencia)
  - [Contacto](#contacto)

## Ejemplo

![screenshot](docs/_static/image/vista_reporte.jpg "Reporte")


La librería permite generar un reporte de calidad de datos el cual contiene información descriptiva del dataframe analizado, a continuación se presenta el código requerido para generar un reporte a partir de un archivo en excel en formato .xlsx.

```
import pandas as pd
from leila.reporte import generar_reporte

generar_reporte(df=pd.read_excel('datosDeInteres.xlsx'))
```

## Documentación

La librería cuenta con una documentación que detalla las funciones que la conforman, al igual que ejemplos de uso y demás información de interes relacionada con esta, para acceder a la documentación siga el siguiente link:

[Documentación - LEILA - Librería de calidad de datos.](https://ucd-dnp.github.io/leila/)

## Instalación

Para la instalación de la librería se debe utilizar el gestor de paquetes ``pip``, por buenas prácticas se sugiere antes de la instalación crear un entorno virtual que permita aislar las librerías y evitar conflictos de versiones con el entorno de desarrollo base del computador.

```
pip install leila
```

## Contribuciones

Para sugerir mejoras, cambios en la librería o seguir el avance de la solución de errores reportados, debe acceder a la sección de [Issues](https://github.com/ucd-dnp/calidad_datos/issues) del repositorio.

## Licencia

La librería LEILA - Calidad de datos se encuentra publicada bajo la licensia MIT <br />
Copyright (c) 2020 Departamento Nacional de Planeación - DNP Colombia

Para mayor información puede consultar el archivo de [Licencia](https://github.com/ucd-dnp/calidad_datos/blob/master/LICENSE)

## Contacto

Para comunicarse con la Unidad de Científicos de Datos (UCD) de la Dirección de Desarrollo Digital (DDD) del DNP, lo puede hacer mediante el correo electróncio ucd@dnp.gov.co
