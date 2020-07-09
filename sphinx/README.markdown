::::::::::::::::::::::::::::::::::::::::::::::
::: Generación de documentación con Sphinx :::
::::::::::::::::::::::::::::::::::::::::::::::

Sphinx versión      3.1.0
rinohtype           0.4.0
sphinx_rtd_theme    0.4.3

- crear carpeta para la documentación 'doc'
- crear ambiente virtual con virtualenv y activar ambiente (opcional)
- instalar dependencias

pip install -U sphinx
pip install sphinx_rtd_theme		#opcional
pip install rinohtype               #opcional - para exportar en PDF

pip install pandas
pip install sodapy

- para crear estructura inicial de sphinx, ejecutar el siguiente comando
    cd doc
    sphinx-quickstart

- ajustes archivo conf.py
    * como se tienen los archivos del código en una ruta diferente a la carpeta 'docs' se debe indicar la ruta de los archivos del código fuente, en lineas 13,14,15

        import os
        import sys
        sys.path.insert(0, os.path.abspath('../..'))

    * se debe agregar la extension de autodoc para que generar los .rst automáticamente, adicionalmente se agrega la extensión rinoh para exportar la documentación en formato pdf.

        extensions = ['sphinx.ext.autodoc', 'rinoh.frontend.sphinx']

    * para generar la documentación en pdf agregar 
        rinoh_documents = [('index',                                      # top-level file (index.rst)
                            'Documentacion',                              # output (target.pdf)
                            'Documentacion librería calidad de datos',    # document title
                            'DNP - UCD')]                                 # document author   

    * para cambiar el theme de los html, se debe cambiar la variable html_theme con el nombre del theme (opcional)
        html_theme = 'sphinx_rtd_theme'

    * si se usa el theme 'sphinx_rtd_theme', agregar en el archivo conf.py la siguiente línea para quitar el link 'View page source'
        html_show_sourcelink = False

- ejecutar la función de generación de archivos .rst, insumo para la generación de los archivos html, se indica como argumento la ubicación de los archivos .rst y la ubicación de los archivos de código a documentar.

    (desde .source)
    sphinx-apidoc -f -o . ../..

- ajustes archivo index.rst
    agregar modules en el toctree (nombre de los archivos .rst sin la extensión), tener cuidado con la indentación 

- ejecutar la función de generación de archivos HTML / PDF
    (desde .doc - misma ubicación que make.bat, los archivos HTML quedan en la ruta build/html)

    make clean
    make html
    sphinx-build -b rinoh source build

(Publicación usando github pages)
add an empty file named .nojekyll to the folder where all the html files are created by sphinx

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

make clean & make html & sphinx-build -b rinoh source build
make clean & make html & "C:\Users\jairoruiz\Documents\GitHub\calidad_datos\doc\build\html\index.html"

add :exclude-members: main to a .rst file to exclude/ignore a function from the documentation

:: Download miktex
https://miktex.org/download


pilas pues
https://github.com/sphinx-doc/sphinx/issues/3807

make clean
make html
make latex
cd build
cd latex
pdflatex calidaddedatos.tex


## A Collection of Issues about the LaTeX Output in Sphinx and the Solutions
https://www.topbug.net/blog/2015/12/11/a-collection-of-issues-about-the-latex-output-in-sphinx-and-the-solutions/

## https://stackoverflow.com/questions/5422997/sphinx-docs-remove-blank-pages-from-generated-pdfs
https://stackoverflow.com/questions/5422997/sphinx-docs-remove-blank-pages-from-generated-pdfs
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: ver configuración PyCharm
https://www.youtube.com/watch?v=mV44dBi9qcQ

:: Tips and Tricks for Hacking Docutils (and Sphinx)
http://jack.rosenth.al/hacking-docutils.html#external-links-in-new-tabs

:: reStructuredText
https://es.wikipedia.org/wiki/ReStructuredText
https://sphinx-test-docs.readthedocs.io/en/latest/restructured/index.html

:: Documentación rinhohtype
https://github.com/brechtm/rinohtype
http://www.mos6581.org/rinohtype/

:: Documentación sphinx-rtd-theme
https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html

:: Configuración general de Sphinx
https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_logo

::::::::::::::::::::::::::::::::::::::::::::::::::
:: Ejemplos
https://www.sphinx-doc.org/en/master/examples.html

https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/index.html
http://www.mos6581.org/rinohtype/
https://sphinx-rtd-theme.readthedocs.io/en/stable/demo/api.html
https://virtualenv.pypa.io/en/latest/
https://scapy.readthedocs.io/en/latest/
https://doc.pypy.org/en/latest/



http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html#colored-boxes-note-seealso-todo-and-warnings