Ejemplos - Datos gov
====================

datos_gov.tabla_inventario
--------------------------
Se conecta al API de Socrata y retorna la base de datos Asset Inventory descargada del Portal de Datos Abiertos como dataframe. Este conjunto de datos es un inventario de los recursos en el sitio. Ver documentación :py:meth:`datos_gov.tabla_inventario`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila import datos_gov

        >>> # Se invoca la función para descargar la base de datos Asset Inventory
        >>> inventario = datos_gov.tabla_inventario()
    
A continuación verificamos el tipo de objeto de la variable **inventario** y su tamaño, para asegurarnos de haber descargado los datos correctamente.

    .. code-block:: python

        >>> # Verificamos el tipo de objeto de 'inventario'
        >>> type(inventario)
        pandas.core.frame.DataFrame

    .. code-block:: python

        >>> # Verificamos el tamaño 'inventario'
        >>> inventario.shape
        (19729, 25)


datos_gov.filtrar_tabla
-----------------------
Permite filtrar la base de datos de tabla de inventario de acuerdo a diferentes términos de búsqueda. Como son fechas, textos y otros. Ver documentación :py:meth:`datos_gov.filtrar_tabla`

Para realizar el filtro de la base de datos de la tabla de inventario debemos tener en cuenta la información disponible, primero consultamos los campos de consulta que podemos usar.

    .. code-block:: python

        >>> # Consultamos las columnas de la base 'inventario'
        >>> list(inventario)
        ['numero_api',
         'nombre',
         'descripcion',
         'dueno',
         'tipo',
         'categoria',
         'terminos_clave',
         'url',
         'fecha_creacion',
         'fecha_actualizacion',
         'actualizacion_frecuencia',
         'filas',
         'columnas',
         'correo_contacto',
         'licencia',
         'entidad',
         'entidad_url',
         'entidad_sector',
         'entidad_departamento',
         'entidad_orden',
         'entidad_dependencia',
         'entidad_municipio',
         'idioma',
         'cobertura',
         'base_publica']

Una vez conocemos los campos de búsqueda que tenemos disponibles, procedemos con el filtro a la base *inventario*, en este caso filtraremos las bases de datos que contengan los términos 'SECOP' y 'contratos' en el nombre de la base de datos y cuya fecha de actualización sea posterior al 14 de Junio del 2020.

    .. code-block:: python
        
        >>> # Se importan las funciones de la librería
        >>> from leila import datos_gov

        >>> # Filtrar bases cuyo nombre incluyen el término 'SECOP' y 'contratos', y cuya fecha de actualización es posterior al 14 de junio de 2020
        >>> columnas_valor = {"nombre":["SECOP", "contratos"], "fecha_actualizacion":["2020-06-15","+"]}
        >>> tabla_filtrada = datos_gov.filtrar_tabla(columnas_valor)

Procedemos a consultar los resultamos obtenidos

    .. code-block:: python
        
        >>> # Consultamos el nombre, número api y fecha de actualización de las 5 primeras respuestas obtenidas
        >>> tabla_filtrada.head(5)[['nombre', 'numero_api', 'fecha_actualizacion']]

    =====  ================================================================== ========== ===================
    Index  nombre                                                             numero_api fecha_actualizacion
    =====  ================================================================== ========== ===================
    4299   SECOP II - Contratos+16KSMMLV                                      k9pc-rjkh  2020-07-30
    7134   SECOP II - Suma Contratos Por Proveedor                            iwpe-6gqp  2020-07-30
    11434  Vista SECOP Integrado Contratos FONTIC - Iniciativa Datos Abiertos bqww-w6pq  2020-07-30
    12946  SECOP II - Contratos Electrónicos                                  jbjy-vk9h  2020-07-30
    14357  SECOP I - Contratos+16KSMMLV                                       79ga-5jck  2020-07-30
    =====  ================================================================== ========== ===================

A continuación se presentan algunas variaciones que pueden utilizar al filtrar las bases de datos

    .. code-block:: python
        
        >>> # Filtrar bases con fechas anteriores a 2020-07-15
        >>> columnas_valor = {"fecha_creacion":["2020-07-15","-"]}

        >>> # Filtrar bases con fechas posteriores a 2020-07-15
        >>> columnas_valor = {"fecha_creacion":["2018-07-15","+"]}

        >>> # Filtrar bases con fecha inicial el 15 de Enero de 2020 y fecha final de 15 de Febrero de 2020
        >>> columnas_valor = {"fecha_creacion":["2020-01-15","2020-02-15"]}

        >>> # Filtrar bases cuya descripción incluya los términos 'economia' y 'ambiente'
        >>> columnas_valor = {"descripcion":["economia","ambiente"]}

        >>> # Filtrar bases que tengan entre 100 y 10000 filas y más de 10 columnas
        >>> columnas_valor = {"filas":[100,10000], "columnas":[10,"+"]}


datos_gov.cargar_base
---------------------
Se conecta al API de Socrata y retorna la base de datos descargada del Portal de Datos Abiertos como dataframe. Ver documentación :py:meth:`datos_gov.cargar_base`

Para la descarga de una base de datos del portal de datos abiertos, requerimos conocer con anterioridad su api_id, en este ejemplo bajaremos los primeros 1.000 registros de la base de datos denominada 'SECOP II - Contratos Electrónicos'

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila import datos_gov

        >>> # Se invoca la función para descargar la base de datos usando el api_id de interés
        >>> base_datos_abiertos = datos_gov.cargar_base("jbjy-vk9h", limite_filas=1000)

Procedemos a consultar los resultados obtenidos

    .. code-block:: python
        
        >>> # Consultados los datos de los 5 primeros registros obtenidos
        >>> base_datos_abiertos.head()


  =====  ===================================================================================== =========== ========================== ============ ========================================== =========== === 
  Index  nombre_entidad                                                                        nit_entidad departamento               ciudad       localizacion                               orden       ...
  =====  ===================================================================================== =========== ========================== ============ ========================================== =========== ===
  0      ESTABLECIMIENTO PENITENCIARIO DE MEDIANA SEGURIDAD Y CARCELARIO DE PENSILVANIA CALDAS 810001393   Caldas                     Pensilvania  Colombia, Caldas , Pensilvania, Manzanares Nacional    ...
  1      SUBRED INTEGRADA DE SERVICIOS DE SALUD SUR E.S.E                                      9009585649  Distrito Capital de Bogotá Bogotá       Colombia, Bogotá, Bogotá                   Territorial ...
  2      ESCUELA NAVAL DE SUBOFICIALES ARC BARRANQUILLA                                        800141653   Atlántico                  Barranquilla Colombia, Atlántico , Barranquilla         Nacional    ...
  3      INSTITUTO GEOGRÁFICO AGUSTÍN CODAZZI                                                  899999004   Distrito Capital de Bogotá No Definido  Colombia, Bogotá                           Nacional    ...
  4      E.S.E. HOSPITAL UNIVERSITARIO HERNANDO MONCALEANO PERDOMO DE NEIVA                    891180268   Huila                      Neiva        Colombia, Huila, Neiva                     Territorial ...
  =====  ===================================================================================== =========== ========================== ============ ========================================== =========== ===
