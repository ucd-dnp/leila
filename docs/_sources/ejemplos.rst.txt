.. _ejemplos:

Ejemplos
========

En esta sección se presentan ejemplos de uso de las diferentes funciones de la librería, el código usado y el resultado esperado de estas. Los datos utilizados para los ejemplos corresponden a una muestra de los **Casos positivos de COVID-19 en Colombia** disponibles en el portal de `Datos Abiertos de Colombia`_, se debe aclarar que los datos fueron modificados con el propósito de presentar el alcance de las diferentes funciones de la librería.

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

En caso que desee utilizar los datos utilizados en los ejemplos, puede descargarlos utilizando el siguiente link. :download:`Descargar datos (6.2 MB)<https://planeacionnacional-my.sharepoint.com/:x:/g/personal/ucd_dnp_gov_co/EcSDnonZAlBFqSFZ7N9MP1gBp50GlC_itwgNcLOm9CksyA?Download=1>`.


calidad_datos.CantidadDuplicados
--------------------------------
Retorna el porcentaje/número de filas o columnas duplicadas (repetidas) en el dataframe. Ver documentación :py:meth:`calidad_datos.CalidadDatos.CantidadDuplicados`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

    .. code-block:: python

        >>> # Numero de filas duplicadas
        >>> repetidos_col_prop = datos.CantidadDuplicados(eje=0, numero=True)
        >>> print(repetidos_col_prop)
        10

    .. code-block:: python

        >>> # Proporción de columnas duplicadas
        >>> repetidos_col_prop = datos.CantidadDuplicados(eje=1, numero=False)
        >>> print(repetidos_col_prop)
        0.0833

De acuerdo a los resultados obtenidos vemos que la base de datos de ejemplo presenta 10 filas duplicadas y el 8.3% (2 de 24) de las columnas duplicadas.


calidad_datos.CorrelacionCategoricas
------------------------------------
Genera una matriz de correlación entre las variables de tipo categóricas. Ver documentación :py:meth:`calidad_datos.CalidadDatos.CorrelacionCategoricas`

Procedemos a calcular la correlación de variables tipo categóricas, en este caso utilizaremos el método de cramer y limitaremos el cálculo a las variables 'Atención', 'Sexo', 'Tipo' y 'Estado'.

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para calcular la correlación de variables categóricas
        >>> matriz_cramer = datos.CorrelacionCategoricas(metodo='cramer', variables=['Atención', 'Sexo', 'Tipo', 'Estado'])
        >>> print(matriz_cramer)

    ========  ========  ========  ========  ========
    Index     Atención  Sexo      Tipo      Estado
    ========  ========  ========  ========  ========
    Atención  1.000000  0.018562  0.080947  0.812447
    Sexo      0.018562  1.000000  0.089351  0.022477
    Tipo      0.080947  0.089351  1.000000  0.141895
    Estado    0.812447  0.022477  0.141895  1.000000
    ========  ========  ========  ========  ========


calidad_datos.CorrelacionNumericas
----------------------------------
Genera una matriz de correlación entre las variables de tipo numérico. Ver documentación :py:meth:`calidad_datos.CalidadDatos.CorrelacionNumericas`

Procedemos a calcular la correlación de variables tipo numéricas, en este caso utilizaremos el método de spearman.

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para calcular la correlación de variables numéricas
        >>> corr_spearman = datos.CorrelacionNumericas(metodo="spearman")
        >>> print(corr_spearman)

    ==========  ========  ========  ==========
    Index       Edad      Edad 2    Edad meses
    ==========  ========  ========  ==========
    Edad        1.000000  1.000000  0.999849
    Edad 2      1.000000  1.000000  0.999849
    Edad meses  0.999849  0.999849  1.000000
    ==========  ========  ========  ==========


calidad_datos.DescripcionCategoricas
------------------------------------
Genera una tabla con los primeros 10 valores más frecuentes de las columnas categóricas del dataframe, además calcula su frecuencia y porcentaje dentro del total de observaciones. Incluye los valores faltantes. Ver documentación :py:meth:`calidad_datos.CalidadDatos.DescripcionCategoricas`

Procedemos a generar la tabla descriptiva de variables tipo categóricas, en este caso limitaremos el cálculo a las variables 'Atención' y 'Pertenencia etnica'.

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para generar la tabla descriptiva de variables categóricas
        >>> descripcion_categoricas = datos.DescripcionCategoricas(variables=['Atención', 'Pertenencia etnica'])
        >>> print(descripcion_categoricas)

    =====  ==================  ================================  ==========  =============================
    Index  Columna             Valor                             Frecuencia  Porcentaje del total de filas
    =====  ==================  ================================  ==========  =============================
    0      Atención            Recuperado                        59927.0     0.913299
    1      Atención            Fallecido                         2914.0      0.044410
    2      Atención            Hospital                          2138.0      0.032584
    3      Atención            Hospital UCI                      438.0       0.006675
    4      Atención            Casa                              6.0         0.000091
    5      Atención            Datos faltantes                   193.0       0.002941
    6      Atención            Total categorías (incluye NA): 6  NaN         NaN
    0      Pertenencia etnica  Otro                              57670.0     0.878901
    1      Pertenencia etnica  Negro                             5003.0      0.076247
    2      Pertenencia etnica  Indígena                          1333.0      0.020315
    3      Pertenencia etnica  Rom                               293.0       0.004465
    4      Pertenencia etnica  Raizal                            72.0        0.001097
    5      Pertenencia etnica  Palenquero                        15.0        0.000229
    6      Pertenencia etnica  Datos faltantes                   1230.0      0.018745
    7      Pertenencia etnica  Total categorías (incluye NA): 7  NaN         NaN
    =====  ==================  ================================  ==========  =============================


calidad_datos.DescripcionNumericas
----------------------------------
Calcula estadísticas descriptivas de cada columna numérica. Ver documentación :py:meth:`calidad_datos.CalidadDatos.DescripcionNumericas`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para generar la tabla descriptiva de variables numéricas
        >>> descripcion_numericas = datos.DescripcionNumericas()
        >>> print(descripcion_numericas)

    ==========  =======  ==========  ==========  ===  =====  =====  =====  ======  =======  ==============  ==============  ==============
    Index       count    mean        std         min  25%    50%    75%    max     missing  outliers_total  outliers_altos  outliers_bajos
    ==========  =======  ==========  ==========  ===  =====  =====  =====  ======  =======  ==============  ==============  ==============
    Edad        65616.0  39.175536   18.661339   0.0  26.0   36.0   52.0   104.0   0.0      0.002865        0.002865        0.0
    Edad 2      65616.0  39.175536   18.661339   0.0  26.0   36.0   52.0   104.0   0.0      0.002865        0.002865        0.0
    Edad meses  65616.0  476.099625  223.962309  1.0  318.0  443.0  626.0  1250.0  0.0      0.004054        0.004054        0.0
    ==========  =======  ==========  ==========  ===  =====  =====  =====  ======  =======  ==============  ==============  ==============


calidad_datos.EmparejamientoDuplicados
--------------------------------------
Retorna las columnas o filas que presenten valores duplicados del dataframe. Ver documentación :py:meth:`calidad_datos.CalidadDatos.EmparejamientoDuplicados`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

    .. code-block:: python

        >>> # Se invoca la función para identificar las columnas duplicadas
        >>> duplicados_col = datos.EmparejamientoDuplicados(col=True)
        >>> print(duplicados_col)

    =====  ==================  ==================
    Index  Columnas iguales 1  Columnas iguales 2
    =====  ==================  ==================
    0      Edad                Fecha reporte web
    1      Edad 2              Fecha de registro
    =====  ==================  ==================

    .. code-block:: python

        >>> # Se invoca la función para identificar las filas duplicadas
        >>> duplicados_fil = datos.EmparejamientoDuplicados(col=False)
        >>> print(duplicados_fil)

    =====  ===============  ===============  ===============  ===============  ===============  ===============  ===============  ===============  ===============
    Index  Filas iguales 1  Filas iguales 2  Filas iguales 3  Filas iguales 4  Filas iguales 5  Filas iguales 6  Filas iguales 7  Filas iguales 8  Filas iguales 9
    =====  ===============  ===============  ===============  ===============  ===============  ===============  ===============  ===============  ===============
    0      1                224              267              21571            48235            48237            60173            60175            64994
    1      2                225              268              21572            48236            48238            60174            60176            64995
    2                                        269                   
    =====  ===============  ===============  ===============  ===============  ===============  ===============  ===============  ===============  ===============

  
calidad_datos.Memoria
---------------------
Calcula el tamaño de la base de datos en memoria (megabytes). Ver documentación :py:meth:`calidad_datos.CalidadDatos.Memoria`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para realizar el cálculo de uso en memoria en megabytes
        >>> peso_base = datos.Memoria(col=False, unidad='megabyte')
        >>> print(peso_base)
        12.01


calidad_datos.Resumen
---------------------
Retorna una tabla con información general de la base de datos. Ver documentación :py:meth:`calidad_datos.CalidadDatos.Resumen`
    
    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para generar la tabla de información general de la base de datos
        >>> resumen = datos.Resumen(columnasRepetidas=True)
        >>> print(resumen)

    ===================================================  =====
    Index                                                Valor
    ===================================================  =====
    Número de filas                                      65616
    Número de columnas                                      24
    Columnas numéricas                                       3
    Columnas de texto                                       15
    Columnas booleanas                                       0
    Columnas de fecha                                        6
    Otro tipo de columnas                                    0
    Número de filas repetidas                               10
    Número de columnas repetidas                             2
    Columnas con más de la mitad de datos faltantes          4
    Columnas con más del 10% de datos como extremos          0
    Uso en memoria de la base en megabytes (aproximado)     12
    ===================================================  =====

calidad_datos.TipoColumnas
--------------------------
Retorna el tipo de dato de cada columna del dataframe. Ver documentación :py:meth:`calidad_datos.CalidadDatos.TipoColumnas`


    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para generar la tabla de descripción
        >>> tipos_columnas = datos.TipoColumnas()
        >>> print(tipos_columnas)

    ==============================  ======================  ======================  ======================================================  ==================================================
    Index                           tipo_general            tipo_general_python     tipo_especifico_1                                       tipo_especifico_2
    ==============================  ======================  ======================  ======================================================  ==================================================
    ID de caso                      Texto                   object                  'str': 100.0%   
    Fecha de notificación           Fecha                   datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 100.0%  
    Código DIVIPOLA                 Texto                   object                  'str': 100.0%   
    Ciudad de ubicación             Texto                   object                  'str': 100.0%   
    Departamento o Distrito         Texto                   object                  'str': 100.0%   
    Atención                        Texto                   object                  'str': 99.71%                                           nan: 0.29%
    Edad                            Numérico                int64                   'int': 100.0%   
    Edad 2                          Numérico                int64                   'int': 100.0%   
    Edad meses                      Numérico                int64                   'int': 100.0%   
    Sexo                            Texto                   object                  'str': 100.0%   
    Tipo                            Texto                   object                  'str': 100.0%   
    Estado                          Texto                   object                  'str': 99.66%                                           nan: 0.34%
    País de procedencia Texto       Texto                   object                  nan: 98.58%                                             'str': 1.42%
    Fecha de inicio de síntomas     Texto                   object                  'str': 100.0%   
    Fecha de muerte                 Fecha                   datetime64[ns]          nan: 95.38%                                             'pandas._libs.tslibs.timestamps.Timestamp': 4.62%
    Fecha diagnostico               Fecha                   datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 98.41%      nan: 1.59%
    Fecha recuperado                Fecha                   datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 91.33%      nan: 8.67%
    Fecha reporte web               Fecha                   datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 100.0%  
    Fecha de registro               Fecha                   datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 100.0%  
    Tipo recuperación               Texto                   object                  'str': 91.33%                                           nan: 8.67%
    Codigo departamento             Texto                   object                  'str': 100.0%   
    Codigo pais Texto               texto                   object                  nan: 98.65%                                             'str': 1.35%
    Pertenencia etnica              Texto                   object                  'str': 98.13%                                           nan: 1.87%
    Nombre grupo etnico             Texto                   object                  nan: 97.97%                                             'str': 2.03%
    ==============================  ======================  ======================  ======================================================  ==================================================


calidad_datos.ValoresExtremos
-----------------------------
Calcula el porcentaje o cantidad de outliers de cada columna numérica (las columnas con números en formato string se intentarán transformar a columnas numéricas). Ver documentación :py:meth:`calidad_datos.CalidadDatos.ValoresExtremos`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para realizar el cálculo de valores extremos
        >>> extremos_ambos_prop = datos.ValoresExtremos(extremos="ambos", numero=True)
        >>> print(extremos_ambos_prop)

    ============  ========
    Index         Valor
    ============  ========
    Edad          188
    Edad 2        188
    Edad meses    266
    ============  ========


calidad_datos.ValoresFaltantes
------------------------------
Calcula el porcentaje/número de valores faltantes de cada columna del dataframe. Ver documentación :py:meth:`calidad_datos.CalidadDatos.ValoresFaltantes`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para realizar el cálculo de proporción de valores faltantes
        >>> faltantes_prop = datos.ValoresFaltantes(numero=False)
        >>> print(faltantes_prop)

    =============================  ========
    Index                          Valor
    =============================  ========
    ID de caso                     0.000000
    Fecha de notificación          0.000000
    Código DIVIPOLA                0.000000
    Ciudad de ubicación            0.000000
    Departamento o Distrito        0.000000
    Atención                       0.002941
    Edad                           0.000000
    Edad 2                         0.000000
    Edad meses                     0.000000
    Sexo                           0.000000
    Tipo                           0.000000
    Estado                         0.003414
    País de procedencia            0.985766
    Fecha de inicio de síntomas    0.000000
    Fecha de muerte                0.953837
    Fecha diagnostico              0.015941
    Fecha recuperado               0.086701
    Fecha reporte web              0.000000
    Fecha de registro              0.000000
    Tipo recuperación              0.086701
    Codigo departamento            0.000000
    Codigo pais                    0.986512
    Pertenencia etnica             0.018745
    Nombre grupo etnico            0.979685
    =============================  ========


calidad_datos.ValoresUnicos
---------------------------
Calcula la cantidad de valores únicos de cada columna del dataframe. Ver documentación :py:meth:`calidad_datos.CalidadDatos.ValoresUnicos`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para realizar el cálculo de valores únicos
        >>> unicos = datos.ValoresUnicos(faltantes=True)
        >>> print(unicos)

    =============================  =====
    Index                          Valor
    =============================  =====
    ID de caso                     65606
    Fecha de notificación            119
    Código DIVIPOLA                  578
    Ciudad de ubicación              559
    Departamento o Distrito           37
    Atención                           6
    Edad                             105
    Edad 2                           105
    Edad meses                      1082
    Sexo                               4
    Tipo                               3
    Estado                             6
    País de procedencia               43
    Fecha de inicio de síntomas      128
    Fecha de muerte                  127
    Fecha diagnostico                114
    Fecha recuperado                 134
    Fecha reporte web                104
    Fecha de registro                104
    Tipo recuperación                  3
    Codigo departamento               36
    Codigo pais                       40
    Pertenencia etnica                 7
    Nombre grupo etnico               49
    =============================  =====


calidad_datos.VarianzaEnPercentil
---------------------------------
Retorna las columnas numéricas cuyo percentil_inferior sea igual a su percentil_superior. Ver documentación :py:meth:`calidad_datos.CalidadDatos.VarianzaEnPercentil`

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Creamos un objeto tipo CalidadDatos con el dataframe de datos de interés
        >>> datos = CalidadDatos(df_datos)

        >>> # Se invoca la función para realizar el cálculo de varianza
        >>> varianza_perc = datos.VarianzaEnPercentil()
        >>> print(varianza_perc)
        No hay ninguna columna numérica que tenga el percentil 5 y el percentil 95 igual


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


reporte.generar_reporte
-----------------------
Crea un reporte de calidad de datos en formato HTML utilizando las funciones disponibles en los otros módulos de la librería. Ver documentación :py:meth:`reporte.generar_reporte`

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

