.. _instalacion:

Instalación
===========

En esta etapa de desarrollo de la librería aún no se cuenta con un procedimiento de instalación automática de las dependencias necesarias, dado lo anterior, se requiere que el usuario tenga acceso a los scripts de la librería y previamente tenga instalado las librerías de ``pandas``, ``numpy``, ``sodapy``, ``jinja2``. 

Para la instalación de los prerrequisitos de la librería se recomienda utilizar un gestor de paquetes como ``pip``, al igual que por buenas prácticas se sugiere crear un entorno virtual que permita aislar las librerías y evitar conflictos de versiones con el entorno de desarrollo base del computador.

Para instalar los requerimientos se recomienda utilizar el archivo requirements.txt, este archivo contiene un listado de las librerias o dependencias necesarias para el correcto funcionamiento de la libreria de calidad de datos.

    .. code-block:: console

        pip install -r requirements.txt

De manera alterna se pueden instalar las diferentes librerías de manera independiente, a manera de ejemplo se muestra como instalar la librería ``jinja2``.

    .. code-block:: console

        pip install Jinja2
