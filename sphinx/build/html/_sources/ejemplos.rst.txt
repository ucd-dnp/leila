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
Ver documentación :py:meth:`reporte.generar_reporte`

Crea un reporte de calidad de datos en formato HTML utilizando las funciones disponibles en los otros módulos de la librería.

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.reporte import generar_reporte

        >>> # Se invoca la función para generar el reporte de calidad de datos
        >>> generar_reporte(df=df_datos, 
        >>>                 titulo='Perfilamiento datos COVID-19 - Colombia', 
        >>>                 archivo='perfilamiento.html')


datos_gov.tabla_inventario
--------------------------
Ver documentación :py:meth:`datos_gov.tabla_inventario`

Se conecta al API de Socrata y retorna la base de datos Asset Inventory descargada del Portal de Datos Abiertos como dataframe. Este conjunto de datos es un inventario de los recursos en el sitio.


datos_gov.filtrar_tabla
-----------------------
Ver documentación :py:meth:`datos_gov.filtrar_tabla`

Permite filtrar la base de datos de tabla de inventario de acuerdo a diferentes términos de búsqueda. Como son fechas, textos y otros.


datos_gov.cargar_base
---------------------
Ver documentación :py:meth:`datos_gov.cargar_base`

Se conecta al API de Socrata y retorna la base de datos descargada del Portal de Datos Abiertos como dataframe.


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
