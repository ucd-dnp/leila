Ejemplos - Reporte
========================

Ejemplo generar_reporte
-----------------------

Crea un reporte de calidad de datos en formato HTML. Ver documentación :py:meth:`reporte.generar_reporte`

En este ejemplo generaremos el reporte a partir de un api_id, este caso corresponde a los casos positivos de COVID-19 reportados en Colombia en el Portal de Datos Abiertos.
        
Teniendo en cuenta que se trata de un conjunto de datos con muchos registros, usamos el argumento limite_filas para
limitar la descarga de información a solo los primeros 1.000 registros.
        
El título del reporte será 'Casos positivos de COVID-19 en Colombia (primeros 1000 registros)' y será guardado con el nombre reporte_calidad_COVID.html


    .. code-block:: python

        >>> # Se importa la función generar_reporte del módulo de reporte
        >>> from leila.reporte import generar_reporte

        >>> generar_reporte(datos="gt2j-8ykr", 
        >>>                 titulo='Casos positivos de COVID-19 en Colombia (primeros 1000 registros)', 
        >>>                 archivo='ejemplo_reporte__API_datos_abiertos.html',
        >>>                 limite_filas=1000)

        --------------------------------------------------------------------------------------------
        No hay columnas duplicadas
        --------------------------------------------------------------------------------------------
        Se ha generado el reporte "ejemplo_reporte__API_datos_abiertos.html"
        09:00:11 AM (00 min 6 seg)
        --------------------------------------------------------------------------------------------


Si desea excluir una sección del reporte lo puede hacer mediante el parámetro secciones.
En el siguiente ejemplo se excluyó del reporte la sección "correlaciones", y de la sección "Estadísticas específicas"
solo se incluyeron las pestañas "Tipo de las columnas" y "Frecuencia de categorías"


    .. code-block:: python

        >>> # Se importa la función generar_reporte del módulo de reporte
        >>> from leila.reporte import generar_reporte

        >>> generar_reporte(datos="bign-27m7", 
        >>>                 titulo="Reporte visas",
        >>>                 archivo='ejemplo_reporte__secciones.html',
        >>>                 secciones={'generales':True, 'muestra_datos': True, 'correlaciones': False,
        >>>                            'especificas': ['tipo', 'frecuencias']})

        --------------------------------------------------------------------------------------------
        El conjunto de datos no tiene columnas numéricas
        --------------------------------------------------------------------------------------------
        Se ha generado el reporte "ejemplo_reporte__secciones.html"
        09:00:20 AM (00 min 0 seg)
        --------------------------------------------------------------------------------------------


También se puede generar el reporte a partir de un dataframe o indicando la ruta de un archivo XLSX o CSV. Para esto solo se requiere cambiar el parámetro datos.


    .. code-block:: python

        >>> # Se importa la función generar_reporte del módulo de reporte
        >>> from leila.reporte import generar_reporte

        >>> # Se llama la función para generar el reporte
        >>> generar_reporte(datos="dataset ejemplos.xlsx", 
        >>>                 titulo='Reporte de prueba archivo XLSX', 
        >>>                 archivo='ejemplo_reporte__archivo_XLSX.html')

        --------------------------------------------------------------
        Se ha generado el reporte "ejemplo_reporte__archivo_XLSX.html"
        09:00:38 AM (00 min 20 seg)
        --------------------------------------------------------------


    .. code-block:: python

        >>> # Se importa la función generar_reporte del módulo de reporte
        >>> from leila.reporte import generar_reporte

        >>> # Se llama la función para generar el reporte
        >>> generar_reporte(datos=df_datos,
        >>>                 titulo='Perfilamiento datos COVID-19 - Colombia',
        >>>                 archivo='ejemplo_reporte__dataframe.html')

        --------------------------------------------------------------
        Se ha generado el reporte "ejemplo_reporte__dataframe.html"
        09:01:22 AM (00 min 22 seg)
        --------------------------------------------------------------


.. figure:: https://github.com/ucd-dnp/leila/blob/gh-pages/sphinx/source/_static/image/vista_reporte.gif?raw=true
    :align: center
    :alt: Ejemplo de reporte
    :figclass: align-center

    Ejemplo de reporte