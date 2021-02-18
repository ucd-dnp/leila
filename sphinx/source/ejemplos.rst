.. _ejemplos:

Ejemplos
++++++++

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


.. include:: ejemplos/ejemplos_calidad_datos.rst
.. include:: ejemplos/ejemplos_datos_gov.rst
.. include:: ejemplos/ejemplos_reporte.rst
