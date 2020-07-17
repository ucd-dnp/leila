.. _instalacion:

Instalación
===========

En esta etapa de desarrollo de la librería aún no se cuenta con un procedimiento de instalación automática de las dependencias necesarias, dado lo anterior, se requiere que el usuario tenga acceso a los scripts de la librería y previamente tenga instalado las librerías de ``pandas``, ``numpy``, ``sodapy``, ``jinja2``. 

Para la instalación de las librerías se recomienda utilizar un gestor de paquetes como ``pip``, al igual que por buenas prácticas se sugiere crear un entorno virtual que permita aislar las librerías y evitar conflictos de versiones con el entorno de desarrollo base del computador.

A continuación se presentan los pasos a seguir para la creación del entorno virtual e instalación de librerías requeridas.

#. Creación del entorno virtual. Para esto se puede utilizar la librería ``virtualenv``.
    
    .. code-block:: console

        virtualenv env
        
#. Activación del entorno virtual
    
    En linux:

    .. code-block:: console

        source env/bin/activate

    En Windows:

    .. code-block:: console

        cd env/Scripts
        activate

#. Una vez se active el entorno virtual se pueden instalar los requerimientos utilizando el archivo de requirements.txt, este archivo contiene un listado de las librerias o dependencias necesarias para el correcto funcionamiento de la libreria de calidad de datos.

    .. code-block:: console

        pip install -r requirements.txt

#. De manera alterna se pueden instalar las diferentes librerías de manera independiente, a manera de ejemplo se muestra como instalar la librería ``jinja2``.

    .. code-block:: console

        pip install Jinja2

#. Para desactivar el entorno virtual usar el comando deactivate

    .. code-block:: console

        deactivate