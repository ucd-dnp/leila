Ejemplos - Calidad datos
========================


    .. code-block:: python

        >>> # Se importar la clase CalidadDatos del módulo calidad_datos
        >>> from leila.calidad_datos import CalidadDatos

        >>> # Se crea un objeto de la clase CalidadDatos con los datos de interés
        >>> ruta_covid = "dataset ejemplos.xlsx"
        >>> datos_covid = CalidadDatos(ruta_covid)


Tabla de resumen
----------------

El método :py:meth:`CalidadDatos.Resumen` calcula varias estadísticas que dan una primera impresión del conjunto de datos.

Estas métricas incluyen el número de filas y columnas; número de columnas de distintos tipos; número de filas y columnas repetidas (duplicadas); columnas con muchos datos faltantes o extremos; peso del conjunto de datos


    .. code-block:: python

        >>> # Calcular la tabla de resumen con el método "Resumen"
        >>> resumen = datos_covid.Resumen()

        >>> # Visualizar la tabla de resumen
        >>> resumen

        Número de filas                                       65616
        Número de columnas                                       25
        Columnas numéricas                                        3
        Columnas de texto                                        16
        Columnas booleanas                                        0
        Columnas de fecha                                         6
        Otro tipo de columnas                                     0
        Número de filas repetidas                                 1
        Número de columnas repetidas                              2
        Columnas con más de la mitad de datos faltantes           4
        Columnas con más del 10% de datos como extremos           0
        Uso de memoria del conjunto de datos en MB (aprox)       12
        dtype: int32


Tipos de cada columna
---------------------

El método :py:meth:`CalidadDatos.TipoColumnas` calcula el tipo de cada columna de tres maneras diferentes.

La primera es el tipo general de la columna en español. Indica si el tipo es numérico, texto, fecha, booleano u otro.

La segunda muestra el tipo general según el método dtypes de Python.

La tercera manera muestra los tipos de cada celda de cada columna. Es decir, muestra la distribución de tipos de cada columna. El tipo que más aparece en esa columna se muestra en la variable 'tipo_especifico_1' de la tabla de tipos y muestra el porcentaje. En caso de haber más de un tipo, se mostrará en las siguientes columnas 'tipo_especifico_#'

El ejemplo abajo muestra cómo el es código para generar los resultados de los tipos con el método 'TipoCOlumnas'. Los parámetros del método especifican qué tipo se quiere mostrar para las columnas (con las opciones True o False)


    .. code-block:: python

        >>> tipos = datos_covid.TipoColumnas(tipoGeneral=True, 
                                         tipoGeneralPython=True, 
                                         tipoEspecifico=True)
        >>> tipos


    ===========================     ============    ===================     =================================================       =================================================
    index                           tipo_general    tipo_general_python     tipo_especifico_1                                       tipo_especifico_2
    ===========================     ============    ===================     =================================================       =================================================
    ID de caso                      Texto           string                  'str': 100.0%   
    Fecha de notificación           Fecha           datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 10...   
    Código DIVIPOLA                 Texto           string                  'str': 100.0%   
    Ciudad de ubicación             Texto           string                  'str': 100.0%   
    Departamento o Distrito         Texto           string                  'str': 100.0%   
    Atención                        Texto           string                  'str': 99.71%                                           'pandas._libs.missing.NAType': 0.29%
    Edad                            Numérico        Int64                   'int': 100.0%   
    Edad 2                          Numérico        Int64                   'int': 100.0%   
    Edad meses                      Numérico        Int64                   'int': 100.0%   
    Sexo                            Texto           string                  'str': 100.0%   
    Tipo                            Texto           string                  'str': 100.0%   
    Estado                          Texto           string                  'str': 99.66%                                           'pandas._libs.missing.NAType': 0.34%
    País de procedencia             Texto           string                  'pandas._libs.missing.NAType': 98.58%                   'str': 1.42%
    Fecha de inicio de síntomas     Texto           string                  'str': 100.0%   
    Fecha de muerte                 Fecha           datetime64[ns]          'pandas._libs.tslibs.nattype.NaTType': 95.38%           'pandas._libs.tslibs.timestamps.Timestamp': 4.62%
    Fecha diagnostico               Fecha           datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 98...       'pandas._libs.tslibs.nattype.NaTType': 1.59%
    Fecha recuperado                Fecha           datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 91...       'pandas._libs.tslibs.nattype.NaTType': 8.67%
    Fecha reporte web               Fecha           datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 10...   
    Fecha de registro               Fecha           datetime64[ns]          'pandas._libs.tslibs.timestamps.Timestamp': 10...   
    Tipo recuperación               Texto           string                  'str': 91.33%                                           'pandas._libs.missing.NAType': 8.67%
    Codigo departamento             Texto           string                  'str': 100.0%   
    Codigo pais                     Texto           string                  'pandas._libs.missing.NAType': 98.65%                   'str': 1.35%
    Pertenencia etnica              Texto           string                  'str': 98.13%                                           'pandas._libs.missing.NAType': 1.87%
    Nombre grupo etnico             Texto           string                  'pandas._libs.missing.NAType': 97.97%                   'str': 2.03%
    Diccionario                     Texto           string                  'str': 100.0%
    ===========================     ============    ===================     =================================================       =================================================


Datos faltantes
---------------

El método :py:meth:`CalidadDatos.ValoresFaltantes` permite calcular el número o porcentaje de valores faltantes de un conjunto de datos. Si el parámetro 'numero' tiene asignado el valor True, se calcula el número de valores faltantes de cada columna. De lo contrario, si es False, se calcula el porcentaje.

El ejemplo a continuación presenta los porcentajes de datos faltantes de cada columna del conjunto de datos de COVID-19


    .. code-block:: python

        >>> faltantes = datos_covid.ValoresFaltantes(numero = False)
        >>> faltantes

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
        Diccionario                    0.000000
        dtype: float64


Datos duplicados
----------------

El método :py:meth:`CalidadDatos.CantidadDuplicados` calcula el número o porcentaje de duplicados en el conjunto de datos.

El ejemplo abajo calcula el número de duplicados para filas y columnas del conjunto de datos de COVID-19.

    .. code-block:: python

        >>> # Número de filas duplicadas. 
        >>> # Se escribe el parámetro eje = 0, para especificar fila
        >>> # Se escribe el parámetro numero = True, para especificar el número de duplicados (si es False se calcula el porcentaje)
        >>> filas_duplicadas = datos_covid.CantidadDuplicados(eje = 0, numero = True)

        >>> # Número de columnas duplicadas. 
        >>> # Se escribe el parámetro eje = 1, para especificar columna
        >>> # Se escribe el parámetro numero = False, para especificar el porcentaje de duplicados
        >>> columnas_duplicadas = datos_covid.CantidadDuplicados(eje = 1, numero = True)

        >>> print("Filas duplicadas: ", filas_duplicadas)
        >>> print("Columnas duplicadas: ", columnas_duplicadas)

        Filas duplicadas:  1        
        Columnas duplicadas:  2



Emparejamiento de duplicados
----------------------------

El método :py:meth:`CalidadDatos.EmparejamientoDuplicados` permite mostrar los nombres de filas o columnas que son exactamente iguales. El parámetro 'col' especifica si se quieren emparejar los duplicados de filas al asignarlo a False. Para emparejar las columnas se escribe True.

EL ejemplo abajo muestra los nombres de las filas duplicadas en cada columna de la tabla. Por ejemplo, la columna de la tabla 'Filas iguales 1' muestra que las filas 1 y 2 son duplicadas.

    .. code-block:: python

        >>> emparejamiento_dupli_filas = datos_covid.EmparejamientoDuplicados(col = False)
        >>> emparejamiento_dupli_filas

    =====   ===============
    index   Filas iguales 1
    =====   ===============
    0       267
    1       269
    =====   ===============


EL ejemplo abajo muestra los nombres de las columnas duplicadas en cada columna de la tabla. Por ejemplo, la columna de la tabla 'Columnas iguales 1' muestra que las columnas 'Edad' y 'Edad 2' son duplicadas.

    .. code-block:: python

        >>> emparejamiento_dupli_cols = datos_covid.EmparejamientoDuplicados(col = True)
        >>> emparejamiento_dupli_cols

    =====  ==================   ==================
    index  Columnas iguales 1   Columnas iguales 2
    =====  ==================   ==================
    0      Edad                 Fecha reporte web
    1      Edad 2               Fecha de registro
    =====  ==================   ==================


Estadísticas descriptivas de variables numéricas
------------------------------------------------

El método :py:meth:`CalidadDatos.DescripcionNumericas` permite calcular estadísticas descriptivas para variables numéricas tales como el promedio, la desviación estándar, el mínimo, máximo, mediana (percentil 50), valores faltantes y extremos.

El objetivo de estos cálculos es verificar si las variables del conjunto de datos contienen los valores esperados o si existen errores en la digitación de los valores

El ejemplo abajo muestra las estadísticas descriptivas para las variables 'Edad', 'Edad_2' y 'Edad meses'

    .. code-block:: python

        >>> descr_numericas = datos_covid.DescripcionNumericas()
        >>> descr_numericas

    ==========  =======     ==========      ==========      ===     =====   =====   =====   ======  =======     ==============      ==============      ==============  
    index       count       mean            std             min     25%     50%     75%     max     missing     outliers_total      outliers_altos      outliers_bajos
    ==========  =======     ==========      ==========      ===     =====   =====   =====   ======  =======     ==============      ==============      ==============  
    Edad        65616.0     39.175536       18.661339       0.0     26.0    36.0    52.0    104.0   0.0         0.002865            0.002865            0.0
    Edad 2      65616.0     39.175536       18.661339       0.0     26.0    36.0    52.0    104.0   0.0         0.002865            0.002865            0.0
    Edad meses  65616.0     476.099625      223.962309      1.0     318.0   443.0   626.0   1250.0  0.0         0.004054            0.004054            0.0
    ==========  =======     ==========      ==========      ===     =====   =====   =====   ======  =======     ==============      ==============      ==============  

Es posible calcular las estadísticas descriptivas para algunas variables únicamente. Esto se hace al asignar una lista con las variables de interés al parámetro 'variables', como se muestra a continuación

    .. code-block:: python

        >>> descr_numericas = datos_covid.DescripcionNumericas(variables = ["Edad", "Edad meses"])
        >>> descr_numericas

    ==========  =======     ==========  ==========  ===     =====   =====   =====   ======  =======     ==============      ==============      ==============
    index       count       mean        std         min     25%     50%     75%     max     missing     outliers_total      outliers_altos      outliers_bajos
    ==========  =======     ==========  ==========  ===     =====   =====   =====   ======  =======     ==============      ==============      ==============
    Edad        65616.0     39.175536   18.661339   0.0     26.0    36.0    52.0    104.0   0.0         0.002865            0.002865            0.0
    Edad meses  65616.0     476.099625  223.962309  1.0     318.0   443.0   626.0   1250.0  0.0         0.004054            0.004054            0.0
    ==========  =======     ==========  ==========  ===     =====   =====   =====   ======  =======     ==============      ==============      ==============


Estadísticas descriptivas de variables categóricas
--------------------------------------------------

El método :py:meth:`CalidadDatos.DescripcionCategoricas` calcula la frecuencia, tanto en número como en porcentaje del total de filas, de los valores de las variables que se consideran numéricas.

Las variables se consideran categóricas si contienen valores limitados. Por defecto, el máximo número de categorías es 30 y las categorías no pueden representar más del 50% del total de filas de la columna. Estos valores se pueden modificar en los parámetros 'limite' y 'categoriasMaximas' del método 'DescripcionCategoricas'.

Es posible también especificar si las variables numéricas con pocos valores se quieren incluir en el análisis. Por ejemplo, variables que contienen únicamente los números 1 y 2. Para agregar las variables al análisis, se asigna el valor True al parámetro incluirNumericas (el cual está por defecto) y False si no se desean incluir.

Por último, es posible agregar una lista limitada de variables al análisis, asignando una lista de Python con las variables al parámetro 'variables'

El ejemplo abajo muestra cómo se calculan las frecuencias de categorías de variables categóricas con los parámetros del método DescripcionCategoricas por defecto


    .. code-block:: python

        >>> descr_categoricas = datos_covid.DescripcionCategoricas(limite=0.5, 
        >>>                                                        categoriasMaximas=30, 
        >>>                                                        incluirNumericos=True, 
        >>>                                                        variables=None)
        >>> descr_categoricas

    =====   ==================      ================================    ==========      =============================
    index   Columna                 Valor                               Frecuencia      Porcentaje del total de filas
    =====   ==================      ================================    ==========      =============================
    0       Atención                Recuperado                          59927.0         0.913299
    1       Atención                Fallecido                           2914.0          0.044410
    2       Atención                Hospital                            2138.0          0.032584
    3       Atención                Hospital UCI                        438.0           0.006675
    4       Atención                Casa                                6.0             0.000091
    5       Atención                Datos faltantes                     193.0           0.002941
    6       Atención                Total categorías (incluye NA): 6    NaN             NaN
    0       Sexo                    M                                   35552.0         0.541819
    1       Sexo                    F                                   30056.0         0.458059
    2       Sexo                    f                                   6.0             0.000091
    3       Sexo                    m                                   2.0             0.000030
    4       Sexo                    Datos faltantes                     0.0             0.000000
    5       Sexo                    Total categorías (incluye NA): 4    NaN             NaN
    0       Tipo                    En estudio                          50836.0         0.774750
    1       Tipo                    Relacionado                         13847.0         0.211031
    2       Tipo                    Importado                           933.0           0.014219
    3       Tipo                    Datos faltantes                     0.0             0.000000
    4       Tipo                    Total categorías (incluye NA): 3    NaN             NaN
    0       Estado                  Leve                                52084.0         0.793770
    1       Estado                  Asintomático                        6811.0          0.103801
    2       Estado                  Moderado                            3135.0          0.047778
    3       Estado                  Fallecido                           2914.0          0.044410
    4       Estado                  Grave                               448.0           0.006828
    5       Estado                  Datos faltantes                     224.0           0.003414
    6       Estado                  Total categorías (incluye NA): 6    NaN             NaN
    0       Tipo recuperación       PCR                                 35370.0         0.539045
    1       Tipo recuperación       Tiempo                              24557.0         0.374253
    2       Tipo recuperación       Datos faltantes                     5689.0          0.086701
    3       Tipo recuperación       Total categorías (incluye NA): 3    NaN             NaN
    0       Pertenencia etnica      Otro                                57670.0         0.878901
    1       Pertenencia etnica      Negro                               5003.0          0.076247
    2       Pertenencia etnica      Indígena                            1333.0          0.020315
    3       Pertenencia etnica      Rom                                 293.0           0.004465
    4       Pertenencia etnica      Raizal                              72.0            0.001097
    5       Pertenencia etnica      Palenquero                          15.0            0.000229
    6       Pertenencia etnica      Datos faltantes                     1230.0          0.018745
    7       Pertenencia etnica      Total categorías (incluye NA): 7    NaN             NaN
    0       Diccionario             {1}                                 32808.0         0.500000
    1       Diccionario             {2}                                 32808.0         0.500000
    2       Diccionario             Datos faltantes                     0.0             0.000000
    3       Diccionario             Total categorías (incluye NA): 2    NaN             NaN
    =====   ==================      ================================    ==========      =============================


Peso de las variables en la memoria RAM
---------------------------------------

Para calcular cuál es el peso de cada variable, se utiliza el método :py:meth:`CalidadDatos.Memoria`, como se muestra en el ejemplo abajo. El parámetro 'unidad' indica que se quiere calcular en Mega Bytes ('Mb') y el parámetro 'col' indica que se calcula para cada variable. En caso de desear calcular el peso total del conjunto de datos, se asigna False al parámetro 'col'.

    .. code-block:: python

        >>> peso_memoria = datos_covid.Memoria(col=True, unidad="Mb")
        >>> peso_memoria

        Index                          0.000122
        ID de caso                     0.500610
        Fecha de notificación          0.500610
        Código DIVIPOLA                0.500610
        Ciudad de ubicación            0.500610
        Departamento o Distrito        0.500610
        Atención                       0.500610
        Edad                           0.563187
        Edad 2                         0.563187
        Edad meses                     0.563187
        Sexo                           0.500610
        Tipo                           0.500610
        Estado                         0.500610
        País de procedencia            0.500610
        Fecha de inicio de síntomas    0.500610
        Fecha de muerte                0.500610
        Fecha diagnostico              0.500610
        Fecha recuperado               0.500610
        Fecha reporte web              0.500610
        Fecha de registro              0.500610
        Tipo recuperación              0.500610
        Codigo departamento            0.500610
        Codigo pais                    0.500610
        Pertenencia etnica             0.500610
        Nombre grupo etnico            0.500610
        Diccionario                    0.500610
        dtype: float64


Correlación entre variables numéricas
-------------------------------------

El método :py:meth:`CalidadDatos.CorrelacionNumericas` calcula una matriz de correlación entre las variables numéricas del conjunto de datos. El parámetro 'metodo' especifica si se desea calcular las correlaciones con el método Pearson ('pearson'), Kendall ('kendall') o Spearman ('spearman').

El siguiente ejemplo presenta la matriz de correlación para variables numéricas del conjunto de datos de COVID-19.

    .. code-block:: python

        >>> corr_numericas = datos_covid.CorrelacionNumericas(metodo="pearson", variables=None)
        >>> corr_numericas

    ==========      ======  ======  ==========
    index           Edad    Edad 2  Edad meses
    ==========      ======  ======  ==========
    Edad            1.0000  1.0000  0.9999
    Edad 2          1.0000  1.0000  0.9999
    Edad meses      0.9999  0.9999  1.0000
    ==========      ======  ======  ==========


Correlación de variables categóricas
------------------------------------

El método :py:meth:`CalidadDatos.CorrelacionCategoricas` calcula una matriz de correlación para variables categóricas. Contiene los mismos parámetros que se explicaron en la Sección 'Estadísticas descriptivas de variables categóricas', para definir variables categóricas, pero incluye también el parámetro 'metodo'. Este especifica si se quiere calcular la matriz con el método Cramer ('cramer') o con la metodología Phik ('phik'), de la librería Phik de Python.

A continuación se calcula la matriz de correlación de variables categóricas para el conjunto de datos de COVID-19

    .. code-block:: python

        >>> corr_categoricas = datos_covid.CorrelacionCategoricas(metodo="phik")
        >>> corr_categoricas

    ======================  ========    ========    ========    ========    =================   ==================  ===========
    index                   Atención    Sexo        Tipo        Estado      Tipo recuperación   Pertenencia etnica  Diccionario
    ======================  ========    ========    ========    ========    =================   ==================  ===========
    Atención                1.000000    0.038193    0.195794    0.987038    0.941437            0.028540            0.000000
    Sexo                    0.038193    1.000000    0.094794    0.041878    0.025933            0.000000            0.000000
    Tipo                    0.195794    0.094794    1.000000    0.325888    0.320547            0.133658            0.000000
    Estado                  0.987038    0.041878    0.325888    1.000000    0.917328            0.067380            0.004040
    Tipo recuperación       0.941437    0.025933    0.320547    0.917328    1.000000            0.051298            0.000000
    Pertenencia etnica      0.028540    0.000000    0.133658    0.067380    0.051298            1.000000            0.002036
    Diccionario             0.000000    0.000000    0.000000    0.004040    0.000000            0.002036            1.000000
    ======================  ========    ========    ========    ========    =================   ==================  ===========

