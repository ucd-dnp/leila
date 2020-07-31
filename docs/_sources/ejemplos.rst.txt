.. _ejemplos:

Ejemplos
========

En esta sección se presentan ejemplos de uso de las diferentes funciones de la librería, el código usado y el resultado esperado de estas. Los datos utilizados para los ejemplos corresponden a una muestra de los **Casos positivos de COVID-19 en Colombia** disponibles en el portal de `Datos Abiertos de Colombia`_, se debe aclarar que los datos fueron modificados con el proposito de presentar el alcance de las diferentes funciones de la librería.

.. _Datos Abiertos de Colombia: https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr


    .. code-block:: python

        >>> # Se importa la librería pandas para la lectura de datos
        >>> import pandas as pd
        
        >>> dtypes = {'ID de caso': object, 
        >>>           'Código DIVIPOLA': object,
        >>>           'Codigo departamento': object, 
        >>>           'Codigo pais':object}

        >>> # Lectura de archivo de datos como dataframe
        >>> df_datos = pd.read_excel('dataset ejemplos.xlsx', dtype=dtypes)

En caso que desee utilizar los datos utilizados en los ejemplos, puede descargarlos utilizando el siguiente link. :download:`Descargar datos (6.2 MB)<./_static/data/dataset ejemplos.xlsx>`.

reporte.generar_reporte
-----------------------
Crea un reporte de calidad de datos en formato HTML utilizando las funciones disponibles en los otros módulos de la librería.

Ver documentación :py:meth:`reporte.generar_reporte`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.reporte import generar_reporte

        >>> # Se invoca la función para generar el reporte de calidad de datos
        >>> generar_reporte(df=df_datos, 
        >>>                 titulo='Perfilamiento datos COVID-19 - Colombia', 
        >>>                 archivo='perfilamiento.html')

        --------------------------------------------------------------
        Se ha generado el reporte "perfilamiento.html"
        11:52:29 AM (01 min 4 seg)
        --------------------------------------------------------------


datos_gov.tabla_inventario
--------------------------
Se conecta al API de Socrata y retorna la base de datos Asset Inventory descargada del Portal de Datos Abiertos como dataframe. Este conjunto de datos es un inventario de los recursos en el sitio.

Ver documentación :py:meth:`datos_gov.tabla_inventario`

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
Permite filtrar la base de datos de tabla de inventario de acuerdo a diferentes términos de búsqueda. Como son fechas, textos y otros.

Ver documentación :py:meth:`datos_gov.filtrar_tabla`

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

    ================================================================== ========== ===================
    nombre                                                             numero_api fecha_actualizacion
    ================================================================== ========== ===================
    SECOP II - Contratos+16KSMMLV                                      k9pc-rjkh  2020-07-30
    SECOP II - Suma Contratos Por Proveedor                            iwpe-6gqp  2020-07-30
    Vista SECOP Integrado Contratos FONTIC - Iniciativa Datos Abiertos bqww-w6pq  2020-07-30
    SECOP II - Contratos Electrónicos                                  jbjy-vk9h  2020-07-30
    SECOP I - Contratos+16KSMMLV                                       79ga-5jck  2020-07-30
    ================================================================== ========== ===================

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
Se conecta al API de Socrata y retorna la base de datos descargada del Portal de Datos Abiertos como dataframe.

Ver documentación :py:meth:`datos_gov.cargar_base`

Para la descarga de una base de datos del portal de datos abiertos, requerimos conocer con anterioridad su api_id, en este ejemplo bajararemos los primeros 1.000 registros de la base de datos denominada 'SECOP II - Contratos Electrónicos'

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila import datos_gov

        >>> # Se invoca la función para descargar la base de datos usando el api_id de interes
        >>> base_datos_abiertos = datos_gov.cargar_base("jbjy-vk9h", limite_filas=1000)

Procedemos a consultar los resultados obtenidos

    .. code-block:: python
        
        >>> # Consultados los datos de los 5 primeros registros obtenidos
        >>> base_datos_abiertos.head()


    ===================================================================================== =========== ========================== ============ ========================================== =========== === 
    nombre_entidad                                                                        nit_entidad departamento               ciudad       localizacion                               orden       ...
    ===================================================================================== =========== ========================== ============ ========================================== =========== ===
    ESTABLECIMIENTO PENITENCIARIO DE MEDIANA SEGURIDAD Y CARCELARIO DE PENSILVANIA CALDAS 810001393   Caldas                     Pensilvania  Colombia, Caldas , Pensilvania, Manzanares Nacional    ...
    SUBRED INTEGRADA DE SERVICIOS DE SALUD SUR E.S.E                                      9009585649  Distrito Capital de Bogotá Bogotá       Colombia, Bogotá, Bogotá                   Territorial ...
    ESCUELA NAVAL DE SUBOFICIALES ARC BARRANQUILLA                                        800141653   Atlántico                  Barranquilla Colombia, Atlántico , Barranquilla         Nacional    ...
    INSTITUTO GEOGRÁFICO AGUSTÍN CODAZZI                                                  899999004   Distrito Capital de Bogotá No Definido  Colombia, Bogotá                           Nacional    ...
    E.S.E. HOSPITAL UNIVERSITARIO HERNANDO MONCALEANO PERDOMO DE NEIVA                    891180268   Huila                      Neiva        Colombia, Huila, Neiva                     Territorial ...
    ===================================================================================== =========== ========================== ============ ========================================== =========== ===


calidad_datos.CantidadDuplicados
--------------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.CantidadDuplicados`

Retorna el porcentaje/número de filas o columnas duplicadas (repetidas) en el dataframe.


calidad_datos.CorrelacionCategoricas
------------------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.CorrelacionCategoricas`

Genera una matriz de correlación entre las variables de tipo categóricas


calidad_datos.CorrelacionNumericas
----------------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.CorrelacionNumericas`

Genera una matriz de correlación entre las variables de tipo numérico


calidad_datos.DescripcionCategoricas
------------------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.DescripcionCategoricas`

Genera una tabla con los primeros 10 valores más frecuentes de las columnas categóricas dataframe , además calcula su frecuencia y porcentaje dentro del total de observaciones. Incluye los valores faltantes.


calidad_datos.DescripcionNumericas
----------------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.DescripcionNumericas`

Calcula estadísticas descriptivas de cada columna numérica.


calidad_datos.EmparejamientoDuplicados
--------------------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.EmparejamientoDuplicados`

Retorna las columnas o filas que presenten valores duplicados del dataframe.


calidad_datos.Memoria
---------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.Memoria`

Calcula el tamaño de la base de datos en memoria (megabytes)


calidad_datos.Resumen
---------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.Resumen`

Retorna una tabla con información general de la base de datos.


calidad_datos.TipoColumnas
--------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.TipoColumnas`

Retorna el tipo de dato de cada columna del dataframe.


calidad_datos.ValoresExtremos
-----------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.ValoresExtremos`

Calcula el porcentaje o cantidad de outliers de cada columna numérica (las columnas con números en formato string se intentarán transformar a columnas numéricas)


calidad_datos.ValoresFaltantes
------------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.ValoresFaltantes`

Calcula el porcentaje/número de valores faltantes de cada columna del dataframe.


calidad_datos.ValoresUnicos
---------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.ValoresUnicos`

Calcula la cantidad de valores únicos de cada columna del dataframe.


calidad_datos.VarianzaEnPercentil
---------------------------------
Ver documentación :py:meth:`calidad_datos.CalidadDatos.VarianzaEnPercentil`

Retorna las columnas numéricas cuyo percentil_inferior sea igual a su percentil_superior.
