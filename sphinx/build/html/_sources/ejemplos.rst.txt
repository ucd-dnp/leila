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

En caso que desee utilizar los datos utilizados en los ejemplos, puede descargarlos utilizando el siguiente link. :download:`Descargar datos (5.8 MB)<_static/data/dataset ejemplos.xlsx>`.

reporte.generar_reporte
-----------------------
Ver documentación :py:meth:`reporte.generar_reporte`

La función crea un reporte de calidad de datos en formato HTML utilizando las funciones disponibles en los otros módulos de la librería.

    .. code-block:: python

        >>> # Se importan las funciones de la librería
        >>> from leila.reporte import generar_reporte

        >>> # Se invoca la función para generar el reporte de calidad de datos
        >>> generar_reporte(df=df_datos, 
        >>>                 titulo='Perfilamiento datos COVID-19 - Colombia', 
        >>>                 archivo='perfilamiento.html')
        
