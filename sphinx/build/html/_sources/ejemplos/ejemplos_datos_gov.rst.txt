Ejemplos - Datos gov
====================

Ejemplo tabla_inventario
------------------------


    .. code-block:: python

        >>> # Se importar la clase DatosGov del módulo datos_gov
        >>> from leila.datos_gov import DatosGov


Se importa la tabla de inventario de datos.gov.co. Esta tabla contiene todas las publicaciones del Portal (conjuntos de datos, enlaces externos, mapas, gráficos, etc.). Ver documentación :py:meth:`DatosGov.tabla_inventario`

    .. code-block:: python

        >>> inventario = DatosGov().tabla_inventario()


Las columnas de la tabla de inventario son las siguientes:

==============================  ==============
Columna                         Descripción
==============================  ==============
**numero_api**                  número API del conjunto de datos. Este es un carácter único de cada conjunto de datos del Portal que se usa como insumo para abrirlo desde código.
**nombre**                      nombre de la publicación
**descripcion**                 descripción de la publicación
**dueno**                       dueño de la publicación. 
**base_publica**                indica con un 'si' si la información del conjunto de datos es público y con un 'no' de lo contrario
**tipo**                        indica el tipo de la publicación, que puede ser uno de los siguientes: 'conjunto de datos', 'enlace externo', 'mapa', 'grafico', 'vista filtrada', 'archivo o documento', 'historia', 'visualizacion', 'lente de datos', 'formulario', 'calendario'.
**categoria**                   tema general del que trata la información publicada
**terminos_clave**              términos clave relacionados con la publicación
**url**                         enlace web de la publicación en el Portal de Datos Abiertos
**fecha_creacion**              fecha de creación de la publicación
**fecha_actualizacion**         última fecha de actualización de la publicación
**filas**                       número de filas del conjunto de datos, si aplica
**columnas**                    número de columnas del conjunto de datos, si aplica
**correo_contacto**             correo de contacto de la entidad dueña de los datos
**licencia**                    nombre de la licencia los datos
**entidad**                     nombre de la entidad dueña de los datos
**entidad_url**                 enlace web de la entidad dueña de los datos
**entidad_sector**              sector de la entidad
**entidad_departamento**        departamento de la entidad
**entidad_orden**               especifica si publicación es de orden territorial, nacional, departamental o internacional
**entidad_dependencia**         dependencia de la entidad dueña de los datos
**entidad_municipio**           municipio donde opera la entidad
**actualizacion_frecuencia**    frecuencia de actualización de los datos. Puede ser anual, semestral, mensual, trimestral, trianual, diaria, quinquenal, semanal, entre otros. También puede no aplicar
**idioma**                      idioma en el que se encuentra la información
**cobertura**                   alcance de la información. Puede ser nacional, departamental, municipal, centro poblado o internacional
==============================  ==============


Filtrar tabla inventario
++++++++++++++++++++++++

Búsqueda por términos clave
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para hacer la búsqueda por términos clave, se construye un diccionario de Python que contenga como llaves los nombres de las columnas de texto de la tabla de inventario sobre las cuales se desea hacer el filtro. Los valores de cada llave es una lista que contiene uno o más términos clave. Este diccionario se ingresa al método :py:meth:`DatosGov.tabla_inventario` dentro del parámetro 'filtro'.

Los términos que se ingresan al diccionario no tienen que tener tildes o mayúsculas que se encuentran en la columna original de la tabla de inventario. Por ejemplo, los resultados serán los mismos si se buscan las palabras 'Economía', 'economía', 'economia' o 'ECONOMÍA'.

Abajo se encuentra un ejemplo donde se filtra la tabla de inventario por las columnas 'nombre' y 'tipo'. Dentro de la columna 'nombre' se busca si contiene los términos 'economia' o 'ambiente' y si la columna 'tipo' contiene el término 'conjunto de datos'. Es decir, se están buscando conjuntos de datos de temas de economía o ambiente.


    .. code-block:: python

        >>> # Se crea el diccionario con el filtro deseado
        >>> filtro = {
        >>>     'nombre': ['economia', 'ambiente'],
        >>>     'tipo': ['conjunto de datos']
        >>> }

        >>> # Se abre la tabla de inventario con el filtro deseado
        >>> inventario = DatosGov().tabla_inventario(filtro=filtro)


    .. code-block:: python

        >>> # Se imprime la tabla de inventario con el filtro aplicado en la celda anterior
        >>> inventario

    =====  ===========  =================================================  =================================================  =================================================  ============  =================  ================================  ==================================================  ================================================  ===================  ===  ==================================================  ==================================================  ==================================  ====================  =============  =================================================  =================  ========================  =======  =============
    index  numero_api   nombre                                             descripcion                                        dueno                                              base_publica  tipo               categoria                         terminos_clave                                      url                                               fecha_creacion       ...  entidad                                             entidad_url                                         entidad_sector                      entidad_departamento  entidad_orden  entidad_dependencia                                entidad_municipio  actualizacion_frecuencia  idioma   cobertura
    =====  ===========  =================================================  =================================================  =================================================  ============  =================  ================================  ==================================================  ================================================  ===================  ===  ==================================================  ==================================================  ==================================  ====================  =============  =================================================  =================  ========================  =======  =============
    4331   8w5c-54ny    Economía del municipio                             La principal base de la economía del Municipio...  Alcaldía Guatavita                                 Si            conjunto de datos  Economía y Finanzas               NaN                                                 https://www.datos.gov.co/d/8w5c-54ny              2018-09-28 20:35:26  ...  NaN                                                 NaN                                                 Agricultura y Desarrollo Rural      Cundinamarca          Territorial    Desarrollo económico                               Guatavita          No aplica                 Español  Municipal
    5839   j7br-6yvm    Contactos Sec. Ambiente                            Contactos en el departamento del Tolima para e...  Carlos Alberto Sanchez Alfonso                     Si            conjunto de datos  Ambiente y Desarrollo Sostenible  gobernacion,tolima,ambiente,contacto                https://www.datos.gov.co/d/j7br-6yvm              2016-12-12 16:42:03  ...  Gobernacion del Tolima                              NaN                                                 Ambiente y Desarrollo Sostenible    Tolima                Territorial    Secretaría del Ambiente y Gestión Riesgo del T...  Ibagué             Anual                     Español  Departamental
    9952   bgmv-gnda    AMBIENTE FÍSICO ANIMALES                           Caracterización de viviendas estrategia APS (a...  Alcaldia de Pereira Secretaria TIC                 Si            conjunto de datos  Salud y Protección Social         NaN                                                 https://www.datos.gov.co/d/bgmv-gnda              2019-12-03 13:28:54  ...  Alcaldia de Pereira                                 NaN                                                 Salud y Protección Social           Risaralda             Territorial    Secretaria de Salud                                Pereira            Anual                     Español  Municipal
    9982   8ffd-q6x9    AMBIENTE                                           La consolidación de temas ambientales en el mu...  ALCALDIADEPALESTINA                                Si            conjunto de datos  Ambiente y Desarrollo Sostenible  ambiente                                            https://www.datos.gov.co/d/8ffd-q6x9              2018-07-12 16:56:38  ...  NaN                                                 NaN                                                 Ambiente y Desarrollo Sostenible    Caldas                Territorial    PLANEACION                                         Palestina          Anual                     Español  Municipal
    17209  rm5b-5f33    AMBIENTE FISICO                                    Caracterización de viviendas estrategia APS (a...  Alcaldia de Pereira Secretaria TIC                 Si            conjunto de datos  Salud y Protección Social         NaN                                                 https://www.datos.gov.co/d/rm5b-5f33              2019-12-03 13:37:29  ...  Alcaldia de Pereira                                 NaN                                                 Salud y Protección Social           Risaralda             Territorial    Secretaria de Salud                                Pereira            Anual                     Español  Municipal
    22681  8ffd-q6x9:0  AMBIENTE                                           La consolidación de temas ambientales en el mu...  ALCALDIADEPALESTINA                                No            conjunto de datos  Ambiente y Desarrollo Sostenible  ambiente                                            https://www.datos.gov.co/d/8ffd-q6x9/revisions/0  2021-03-04 14:43:12  ...  NaN                                                 NaN                                                 Ambiente y Desarrollo Sostenible    Caldas                Territorial    PLANEACION                                         Palestina          Anual                     Español  Municipal
    33255  q282-rcj5    Sector Economía Solidaria                          Registros de entidades pertenecientes al secto...  Cámara de Comercio de Valledupar para el Valle...  Si            conjunto de datos  NaN                               economía solidaria                                  https://www.datos.gov.co/d/q282-rcj5              2020-11-04 16:01:05  ...  Cámara de Comercio de Valledupar para el Valle...   https://ccvalledupar.org.co/                        No Aplica                           Cesar                 Territorial    Registros Públicos                                 Valledupar         No aplica                 Español  Departamental
    34615  fwsu-jxw6    RELACION PROTOCOLOS DE BIOSEGURIDAD SECTORES D...  RELACION PROTOCOLOS DE BIOSEGURIDAD SECTORES D...  alcaldiarovira                                     Si            conjunto de datos  Salud y Protección Social         bioseguridad,rovira,protocolos                      https://www.datos.gov.co/d/fwsu-jxw6              2020-10-21 21:39:17  ...  ALCALDIA DE ROVIRA                                  NaN                                                 No Aplica                           Tolima                Territorial    SECRETARIA DE SALUD                                Rovira             Anual                     Español  Municipal
    34628  3bvi-vpkx    Indicadores de Economía y Productividad de Sab...  Conozca indicadores de economía y productivida...  Alcaldía de Sabaneta                               Si            conjunto de datos  Economía y Finanzas               mercado laboral,comercio,economia,industria,in...   https://www.datos.gov.co/d/3bvi-vpkx              2018-10-02 14:50:36  ...  Alcaldía de Sabaneta                                http://www.otsabaneta.org/economia-y-productiv...   No Aplica                           Antioquia             Territorial    Secretaría de Planeación y Desarrollo Territor...  Sabaneta           Anual                     Español  Municipal
    =====  ===========  =================================================  =================================================  =================================================  ============  =================  ================================  ==================================================  ================================================  ===================  ===  ==================================================  ==================================================  ==================================  ====================  =============  =================================================  =================  ========================  =======  =============


Búsqueda por rango de filas y columnas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para hacer el filtro de la tabla de inventario por el tamaño de un conjunto de datos, se tiene que incluir el nombre de las columnas 'filas' y 'columnas' en el diccionario. Los valores de estas llaves son listas con dos elementos cada una: el primer elemento es el valor mínimo de filas o columnas y el segundo el valor máximo.

A continuación se muestra un ejemplo de filtro, donde se seleccionan los conjuntos de datos con mínimo 50 filas y máximo 60 y con mínimo 8 columnas y máximo 10


    .. code-block:: python

        >>> # Se crea el diccionario con el filtro deseado
        >>> filtro = {
        >>>     'filas': [50, 60],
        >>>     'columnas': [8, 10]
        >>> }
        
        >>> # Se abre la tabla de inventario con el filtro deseado
        >>> inventario = DatosGov().tabla_inventario(filtro=filtro)


    .. code-block:: python

        >>> # Imprimir las columnas del código API, nombre, descripción, filas y columnas de la tabla de inventario filtrada
        >>> inventario[['numero_api', 'nombre', 'descripcion', 'filas', 'columnas']]


    =====   ==========  ==================================================  =================================================   =====   ========
    index   numero_api  nombre                                              descripcion                                         filas   columnas
    =====   ==========  ==================================================  =================================================   =====   ========
    55      igcu-56c4   CONTRATOS PRESTACION DE SERVICIOS 2018 MUNIC...     Lista contratos de prestación de servicio al...     57.0    10.0
    326     e9d5-9xvt   Instituciones Educativas Extintas del Municipi...   Información de las Instituciones Educativas qu...   58.0    10.0
    367     vxhy-86k4   Ejecución Presupuestal a Junio de 2017              Acumulado de la ejecución presupuestal de la U...   56.0    9.0
    421     hysn-yquu   Publicidad registro de vallas Municipio de Pa...    Registro de vallas publicitarias del Municipio...   53.0    8.0
    519     8qip-sek5   Corregidores y Auxiliares Corregidores del Mun...   Corregidores y Auxiliares o Ayudantes de Corre...   54.0    9.0
    ...     ...         ...                                                 ...                                                 ...     ...
    34281   svz2-ug32   Contratistas Alcaldía Mistrató 2021                 Contiene datos del contratista como nombres y ...   50.0    9.0
    34628   3bvi-vpkx   Indicadores de Economía y Productividad de Sab...   Conozca indicadores de economía y productivida...   57.0    10.0
    34739   symc-8gre   DOCENTES POR GENERO 2019-2                          Docentes de planta, contrato y catedráticos cl...   59.0    8.0
    34759   rubk-nymq   Correos Institucionales Alcaldía de Copacabana      Correos institucionales del municipio de Copac...   54.0    8.0
    34808   9m2f-pdxx   Licencias de Cannabis otorgadas por el Ministe...   Licencias de uso de semillas para siembra, de ...   56.0    10.0
    =====   ==========  ==================================================  =================================================   =====   ========


Búsqueda por  fecha
~~~~~~~~~~~~~~~~~~~

La tabla de inventario también puede filtrase por fecha. Para hacerlo, se ingresa el diccionario de filtro con una de las columnas de fecha y se especifican las fechas de inicio y de fin deseadas. El siguiente ejemplo muestra cómo obtener la tabla de inventario para publicaciones creadas entre el 1 de enero de 2020 y el 1 de febrero de 2020.

    .. code-block:: python

        >>> # Se crea el diccionario con el filtro deseado
        >>> filtro = {
        >>>     'fecha_creacion': ['2020-01-01', '2020-02-01'],
        >>> }

        >>> # Se abre la tabla de inventario con el filtro deseado
        >>> inventario = DatosGov().tabla_inventario(filtro=filtro)


    .. code-block:: python

        >>> # Se muestra la tabla filtrada por fecha
        >>> inventario



======  ===========     =================================================   =================================================   =================================================   ============    =================   ================================    =================================================   ================================================    ===================  ===  =================================================     =================================================   ================================    ====================    =============       =============================================   =================   ========================    =======     =============
index   numero_api      nombre                                              descripcion                                         dueno                                               base_publica    tipo                categoria                           terminos_clave                                      url                                                 fecha_creacion       ...  entidad                                               entidad_url                                         entidad_sector                      entidad_departamento    entidad_orden       entidad_dependencia                             entidad_municipio   actualizacion_frecuencia    idioma      cobertura
======  ===========     =================================================   =================================================   =================================================   ============    =================   ================================    =================================================   ================================================    ===================  ===  =================================================     =================================================   ================================    ====================    =============       =============================================   =================   ========================    =======     =============
104     k2sw-5j93:2     Atención al usuario año 2020 Instituto Municip...   El ejercicio de caracterización de los usuario...   IMETY                                               No              conjunto de datos   Educación                           NaN                                                 https://www.datos.gov.co/d/k2sw-5j93/revisions/2    2020-01-23 19:49:39  ...  Instituto Municipal de Educación para el Traba...     NaN                                                 Educación                           Valle del Cauca         Territorial         Matricula Academica                             Yumbo               Anual                       Español     Departamental
106     5ex4-dqe9       Población estudiantil posgrado por semestre y/...   Población estudiantil posgrado por semestre y/...   Universidad Colegio Mayor de Cundinamarca           Si              conjunto de datos   Educación                           programas académicos,posgrado,unicolmayor,univ...   https://www.datos.gov.co/d/5ex4-dqe9                2020-01-21 17:05:26  ...  Universidad Colegio Mayor de Cundinamarca             http://www.unicolmayor.edu.co/portal/index.php...   Educación                           Bogotá D.C.             Nacional            Oficina de Planeación, sistemas y desarrollo    Bogotá D.C.         Anual                       Español     Nacional
331     wu3s-8hsw       Población estudiantil pregrado por programa y ...   Población estudiantil por programa y semestre ...   Universidad Colegio Mayor de Cundinamarca           Si              conjunto de datos   Educación                           estudiantes matriculados,programas académicos,...   https://www.datos.gov.co/d/wu3s-8hsw                2020-01-21 15:35:30  ...  Universidad Colegio Mayor de Cundinamarca             http://www.unicolmayor.edu.co/portal/index.php...   Educación                           Bogotá D.C.             Nacional            Oficina de Planeación, sistemas y desarrollo    Bogotá D.C.         Anual                       Español     Nacional
498     6b2t-68uu:0     Entidades Públicas Municipio de El Hobo             NaN                                                 Alcaldía de Hobo                                    No              conjunto de datos   NaN                                 NaN                                                 https://www.datos.gov.co/d/6b2t-68uu/revisions/0    2020-01-03 15:55:41  ...  NaN                                                   NaN                                                 NaN                                 NaN                     NaN                 NaN                                             NaN                 NaN                         NaN         NaN
549     88ru-5pzs:0     MORBILIDAD 2019                                     NaN                                                 Capacitacion Mintic                                 No              conjunto de datos   NaN                                 NaN                                                 https://www.datos.gov.co/d/88ru-5pzs/revisions/0    2020-01-02 16:12:57  ...  NaN                                                   NaN                                                 NaN                                 NaN                     NaN                 NaN                                             NaN                 NaN                         NaN         NaN
...     ...             ...                                                 ...                                                 ...                                                 ...             ...                 ...                                 ...                                                 ...                                                 ...                  ...  ...                                                   ...                                                 ...                                 ...                     ...                 ...                                             ...                 ...                         ...         ...
33666   ir4d-mzgr       Publicaciones_E_Interacciones_Campaña_#Evoluci...   La campaña #EvoluciónTransparente buscó conoce...   urnadecristal                                       Si              conjunto de datos   Participación ciudadana             NaN                                                 https://www.datos.gov.co/d/ir4d-mzgr                2020-01-17 15:35:23  ...  Urna de Cristal                                       NaN                                                 No Aplica                           Bogotá D.C.             Nacional            Urna de Cristal                                 Bogotá D.C.         No aplica                   Español     Nacional
34634   9et2-bf5i       Entrega y Retoma                                    Entrega y Retoma                                    Ministerio TIC Oficina TI Gestión de Informacion    Si              conjunto de datos   Ciencia, Tecnología e Innovación    NaN                                                 https://www.datos.gov.co/d/9et2-bf5i                2020-01-27 21:17:01  ...  Ministerio de Tecnologías de la Información y ...     https://colombiatic.mintic.gov.co                   Ciencia, Tecnología e innovación    Bogotá D.C.             Nacional            Dirección Computadores para Educar              Bogotá D.C.         Mensual                     Español     Nacional
34660   fnir-e2zx       DISCONTINUIDAD                                      DISCONTINUIDAD SEPTIEMBRE 2020                      EMPRESA IBAGUEREÑA DE ACUEDUCTO Y ALCANTARILLA...   Si              conjunto de datos   Vivienda, Ciudad y Territorio       NaN                                                 https://www.datos.gov.co/d/fnir-e2zx                2020-01-29 20:39:14  ...  NaN                                                   NaN                                                 Vivienda Ciudad y Territorio        Tolima                  Territorial         GRUPO CALIDAD DE AGUA                           Ibagué              Mensual                     Español     Municipal
34690   syiu-8mvf       PARQUE AUTOMOTOR DEL MUNICIPIO DE BARBOSA ANT...    Contiene el inventario de vehículos registrad...    Alcaldía de Barbosa - Antioquia                     Si              conjunto de datos   Transporte                          vehiculos,parque automotor                          https://www.datos.gov.co/d/syiu-8mvf                2020-01-16 19:19:56  ...  NaN                                                   NaN                                                 Transporte                          Antioquia               Territorial         Secretaría de Movilidad                         Barbosa             Anual                       Español     Municipal
34780   etwv-wj8f       Pueblos indígenas a nivel Nacional 2020             Información de la ubicación de los pueblos ind...   Ministerio del Interior                             Si              conjunto de datos   NaN                                 indígenas,dairm,etnias,pueblos                      https://www.datos.gov.co/d/etwv-wj8f                2020-01-27 14:47:31  ...  Ministerio del Interior                               NaN                                                 Interior                            Bogotá D.C.             Nacional            Dirección de Asuntos Indígenas ROM y Minorías   Bogotá D.C.         Anual                       Español     Nacional
======  ===========     =================================================   =================================================   =================================================   ============    =================   ================================    =================================================   ================================================    ===================  ===  =================================================     =================================================   ================================    ====================    =============       =============================================   =================   ========================    =======     =============


Abrir un conjunto de datos del Portal de Datos Abiertos
-------------------------------------------------------

Para abrir un conjunto de datos.gov.co es necesario tener el código API de ese conjunto e ingresarlo al método :py:meth:`DatosGov.cargar_base`. Con esta función se crea un objeto que contiene el dataframe y el diccionario de metadatos del conjunto, los cuales se pueden obtener con los métodos 'to_dataframe' y 'metadatos'

A continuación está el código para cargar el conjunto de datos de 'Pueblos indígenas a nivel Nacional 2020', el cual se encuentra en el último filtro de la tabla de inventario.


Cargar conjunto de datos con número API
+++++++++++++++++++++++++++++++++++++++


    .. code-block:: python
        
        >>> # Se define la variable 'numero_api', que contiene el número API del conjunto 'Pueblos indígenas a nivel Nacional 2020'
        >>> numero_api = 'etwv-wj8f'

        >>> # Se descarga la información del conjunto de datos en la variable 'data' con el método 'cargar_base'. 
        >>> # Al parámetro 'api_id' se asigna el número API y 'limite_filas' especifica que únicamente se descargan 200 filas del conjunto
        >>> data = DatosGov().cargar_base(api_id = numero_api, limite_filas=200)


Obtener dataframe del conjunto de datos
+++++++++++++++++++++++++++++++++++++++


    .. code-block:: python
        
        >>> # Se obtiene el dataframe del conjunto de datos con el método 'to_dataframe'
        >>> datos = data.to_dataframe()

        >>> # Se visualiza una versión reducida del dataframe
        >>> datos


    =====   ==============  ===============     =================
    index   unnamed_column  departamento        pueblos_indigenas
    =====   ==============  ===============     =================
    0       NaN             AMAZONAS            KAWIYARI
    1       NaN             AMAZONAS            SIONA
    2       NaN             AMAZONAS            YAGUA
    3       NaN             AMAZONAS            BARASANO
    4       NaN             AMAZONAS            LETUAMA
    ...     ...             ...                 ...
    195     NaN             VALLE DEL CAUCA     EMBERA CHAMI
    196     NaN             VALLE DEL CAUCA     EPERARA SIAPIDARA
    197     NaN             VALLE DEL CAUCA     NASA
    198     NaN             VALLE DEL CAUCA     PASTO
    199     NaN             VALLE DEL CAUCA     WAUNANN
    =====   ==============  ===============     =================


Obtener diccionario de metadatos del conjunto de datos
++++++++++++++++++++++++++++++++++++++++++++++++++++++

    .. code-block:: python

        >>> # Los metadatos se obtienen con el método 'metadatos' y se asignan a la variable 'meta'
        >>> meta = data.metadatos()
        
        >>> # Se visualiza el diccionario de metadatos
        >>> meta

        {'numero_api': 'etwv-wj8f',
         'nombre': 'Pueblos indígenas a nivel Nacional 2020',
         'descripcion': 'Información de la ubicación de los pueblos indígenas por departamento y municipio a 31 de Diciembre de 2020.',
         'tipo': 'dataset',
         'url': 'NA',
         'categoria': 'NA',
         'fecha_creacion': '2020-01-27',
         'numero_vistas': 360,
         'numero_descargas': 60,
         'licencia': 'NA',
         'fecha_publicacion': '2020-01-27',
         'base_publica': 'published',
         'fecha_actualizacion': '2021-01-26',
         'numero_filas': 'NA',
         'numero_columnas': 3,
         'licencia_url': 'http://creativecommons.org/licenses/by-sa/4.0/legalcode',
         'entidad': 'Ministerio del Interior',
         'entidad_municipio': 'Bogotá D.C.',
         'entidad_sector': 'Interior',
         'entidad_departamento': 'Bogotá D.C.',
         'entidad_orden': 'Nacional',
         'entidad_dependencia': 'Dirección de Asuntos Indígenas ROM y Minorías',
         'cobertura': 'Nacional',
         'idioma': 'Español',
         'frecuencia_actualizacion': 'Anual',
         'dueno': 'Ministerio del Interior',
         'columnas': {'Unnamed Column': {'tipo': 'text',
           'descripcion': '',
           'nombre_df': 'unnamed_column'},
          'DEPARTAMENTO': {'tipo': 'text',
           'descripcion': '',
           'nombre_df': 'departamento'},
          'PUEBLOS INDIGENAS': {'tipo': 'text',
           'descripcion': '',
           'nombre_df': 'pueblos_indigenas'}}}
