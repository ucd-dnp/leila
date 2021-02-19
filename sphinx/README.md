# Generación de documentación con Sphinx

Este documento pretende ilustrar los pasos necesarios para generar la documentación de una librería utilizando [Sphinx](https://www.sphinx-doc.org/en/master/), no contempla la generación de multiples versiones.

Los pasos presentados a continuación se utilizaron con las siguientes librerías.

| Libreria            |versión|
|---------------------|-------|
| Sphinx              |3.5.1  |
| sphinx_copybutton   |0.3.1  |
| sphinx_rtd_theme    |0.5.1  |

Adicionalmente, se tomó como código fuente la librería [LEILA](https://github.com/ucd-dnp/leila) y se tiene en cuenta la siguiente estructura base de carpetas:

```
[Proyecto]               # carpeta principal
|
|--- [leila]             # carpeta que contiene el código fuente
| |--- [templates]
| |--- __init__.py
| |--- calidad_datos.py
| |--- datos_gov.py
| |--- reporte.py
```

Vale la pena mencionar que la librería [LEILA](https://github.com/ucd-dnp/leila) y los archivos usados en su documentación utilizan el lenguaje ReStructuredText. Para mayor información puede consultar los siguientes links:

* [ReStructuredText en Wikipedia](https://es.wikipedia.org/wiki/ReStructuredText)
* [Sphinx - reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)

***
#### 1. Cree un entorno virtual, actívelo y proceda a instalar las siguientes librerías.

```console
pip install leila
pip install -U sphinx
pip install sphinx_copybutton
pip install sphinx_rtd_theme
```

***
#### 2. Cree una carpeta 'doc' y dentro de esta corra el siguiente comando

```console
sphinx-quickstart
```

* Responda las preguntas en consola, a continuación se presenta un modelo:

```console
Separate source and build directories (y/n) [n]: y
Project name: LEILA
Author name(s): UCD-DNP
Project release []: v0.1
Project language [en]: es
Finished: An initial directory structure has been created.
```

Una vez finalizada la ejecución inicial deberá tener una estructura de archivos como la siguiente:

```
[Proyecto]               # carpeta principal
|
|--- [doc]
| |--- [build]           # carpeta de resultados de la documentación
| |--- [source]          # carpeta de archivos de configuración de sphinx
|   |--- [_static]       # carpeta de archivos estáticos como imágenes, .css y otros
|   |--- [_templates]    # carpeta de templates - se utiliza con sphinx-multiversion
|   |--- conf.py         # archivo principal de configuración de sphinx
|   |--- index.rst
|
| |--- make.bat          # archivo ejecutable - le permitirá generar la documentación
| |--- Makefile          # archivo ejecutable - le permitirá generar la documentación
|
|
|--- [leila]             # carpeta que contiene el código fuente
| |--- [templates]
| |--- __init__.py
| |--- calidad_datos.py
| |--- datos_gov.py
| |--- reporte.py
```

***
#### 3. Procedemos a hacer ajustes de configuración en el archivo doc/source/conf.py

#### 3.1 Se deben incluir las siguientes líneas para indicar la ubicación de los archivos de código fuente de la librería a documentar.

```python
import os
import sys
sys.path.insert(0, os.path.abspath('../../leila'))
```

***
#### 3.2 Se procede a modificar la variable *extensions* para agregar las extensiones que utilizaremos. El resultado final debe verse así:

```python
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosectionlabel', 'sphinx_copybutton']
```

* La extensión **'sphinx.ext.autodoc'** se utiliza para generar los archivos .rst base automáticamente de acuerdo a la estructura de la librería a documentar.

* La extensión **'sphinx.ext.autosectionlabel'** permite hacer referencias o enlaces entre las páginas de la documentación.

***
#### 3.3 Para cambiar el theme de los archivso html, se debe cambiar la variable html_theme con el nombre del theme (opcional)

```python
html_theme = 'sphinx_rtd_theme'
```

* si se usa el theme **'sphinx_rtd_theme'**, agregar en el archivo conf.py la siguiente línea para quitar el link 'View page source'

```python
html_show_sourcelink = False
```

***
#### 3.4 La extensión **'sphinx_copybutton'** habilita la función de copiar el código mediante un botón en la esquina superior derecha de las casillas identificadas como código.

```python
copybutton_prompt_text = ">>> "
```

La variable *copybutton_prompt_text* define una marca para saber cuales líneas se deben copiar.Teniendo en cuenta lo anterior, en el siguiente ejemplo no se copiaría la primera línea.

```python
# Se importan las funciones de la librería
>>> from leila.reporte import generar_reporte
```

***
#### 3.5 Se pueden agregar variables adicionales como son:

```python
# agrega la referencia de un archivo .css en la carpeta definida en la variable html_static_path.
html_css_files = ['css/custom.css']             

# permite agregar un logo a la documentación
html_logo  = '_static/image/logo_400.png'       

# permite agregar un favicon
html_favicon = '_static/image/favicon.ico'      
```
***Nota:*** No olvide agregar los archivos estáticos en las carpetas respectivas.

***
#### 4. Ejecutar la función de generación de archivos .rst

* Los archivos .rst son el insumo para la generación de los archivos html, se indica como argumento la ubicación de los archivos .rst y la ubicación de los archivos de código a documentar.

```python
# ubicados en la carpeta doc/source correr:
sphinx-apidoc -f -o . ../..
```

* Al finalizar la ejecución se generan dos archivos nuevos *leila.rst* y *modules.rst*

***
#### 5. Modificación del archivo doc/source/index.rst

* El archivo index.rst hace referencia a la página principal de la documentación. Debemos modificar este archivo para agregar el nuevo contenido (la documentación generada a partir del código fuente). Para esto agregamos 'modules' en el toctree.

    * El contenido del archivo *index.rst* debería quedar así:

```python
Welcome to LEILA's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

***Nota 1:*** solo se agrega la referencia al archivo *modules.rst* porque internamente este llama al archivo *leila.rst*

***Nota 2:*** tener cuidado con la indentación en los archivos *.rst*.

***Nota 3:*** los archivos *.rst* utilizan reStructuredText, para mayor información puede consultar el enlace [Sphinx - reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)

***
#### 6. Generación de documentación

#### 6.1 Generación de documentación - versión web

En este momento ya se puede generar una primera versión de la documentación.

```python
# ubicados en la carpeta doc (misma ubicación que el archivo make.bat) correr:
make clean              # borra los archivos en la carpeta build
make html               # inicia el proceso de generación de la documentación en formato html
```

***Nota:*** durante la generación de la documentación se presentarán varios warnings. estos no indican un error en el proceso, corresponden a unos labels duplicados presentes en la documentación.

Una vez finalizado el proceso podrá consultar los resultaos en la siguiente ruta: ***doc/build/html/index.html***

#### El resultado obtenido difiere mucho de la [documentación de LEILA](https://ucd-dnp.github.io/leila/) ya que la última versión incluye muchos ajustes de estilo, referencia y diseño en los archivos *.rst*. Puede consultar los archivos finales de la documentación de LEILA en este [enlace](https://github.com/ucd-dnp/leila/tree/master/sphinx/source)

***
#### 6.2 Generación de documentación - versión PDF

Para la generación de la documentación en formato PDF se requiere primero generar la documentación en formato latex.

```python
# ubicados en la carpeta doc (misma ubicación que el archivo make.bat) correr:
make latex              # inicia el proceso de generación de la documentación en formato latex
```

Una vez finalice la ejecución ejecute el siguiente comando.
```python
# ubicados en la carpeta doc/build/latex correr:
pdflatex leila.tex      # inicia el proceso de generación de la documentación en formato PDF
```

Se generará el archivo *leila.pdf* y lo podrá encontrar en la ruta ***doc/build/latex/leila.pdf***

***Nota:*** si no se reconoce el comando **pdflatex** seguramente no se tienen instaladas las dependencias de *latex*. Puede descargarlas desde https://miktex.org/download
