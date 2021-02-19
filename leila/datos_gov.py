import pandas as pd
import numpy as np
import datetime
from sodapy import Socrata

from datetime import datetime, timedelta

class Datos:


    """clase para cargar los conjuntos de datos de Socrata y almacenar en atributos los datos y la metadata"""

    def __init__(self, api_id: str, token=None, limite_filas=1000000000):
        
        self.dominio_datos_gov = "www.datos.gov.co"
        self.api_id = api_id
        self.token = token
        self.limite_filas = limite_filas
        self._base = None
        self.metadata = None
        
        self.cargar_base()

    def cargar_base(self):
        """ Se conecta al API de Socrata y retorna la base de datos descargada del Portal de Datos Abiertos
        como dataframe. :ref:`Ver ejemplo <datos_gov.cargarself._base>`
    
        .. warning::
            Al descargar una base de datos utilizando el API de Socrata, esta omitirá cualquier
            columna que no contenga registros, lo cual puede generar inconsistencias con la información
            descrita en el portal de datos abiertos.

        :param api_id: (str) Identificación de la base de datos asociado con la API de Socrata.
        :param token: (str) opcional - token de usuario de la API Socrata.
        :param limite_filas: (int) (valor mayor a 0), indica el número máximo de filas a descargar de la base de datos \
        asociada al api_id. El límite está pensado para bases de gran tamaño que superen la capacidad del computador.
        :return: base de datos en formato dataframe.
        """

        client = Socrata(self.dominio_datos_gov, app_token=self.token)
        results = client.get(self.api_id, limit=self.limite_filas)
        self._base = pd.DataFrame.from_records(results)
        self.metadata = client.get_metadata(self.api_id)

class Inventario:
    
    def __init__(self, token=None, limite_filas=1000000000):
        self.token = token
        self.limite_filas = limite_filas
        self.archivo_inventario = "uzcf-b9dh"
        self.inventario = None
        self.DIC_RENAME = {
            "uid": "numero_api",
            "name": "nombre",
            "description": "descripcion",
            "owner": "dueno",
            "type": "tipo",
            "category": "categoria",
            "tags": "terminos_clave",
            "url": "url",
            "creation_date": "fecha_creacion",
            "last_data_updated_date": "fecha_actualizacion",
            "informacindedatos_frecuenciadeactualizacin": "actualizacion_frecuencia",
            "row_count": "filas",
            "column_count": "columnas",
            "contact_email": "correo_contacto",
            "license": "licencia",
            "attribution": "entidad",
            "attribution_link": "entidad_url",
            "informacindelaentidad_sector": "entidad_sector",
            "informacindelaentidad_departamento": "entidad_departamento",
            "informacindelaentidad_orden": "entidad_orden",
            "informacindelaentidad_reaodependencia": "entidad_dependencia",
            "informacindelaentidad_municipio": "entidad_municipio",
            "informacindedatos_idioma": "idioma",
            "informacindedatos_coberturageogrfica": "cobertura",
            "publication_stage": "base_publica"
        }
        
        self.cargar_inventario()

    def cargar_inventario(self):
        """ Se conecta al API de Socrata y retorna la base de datos *Asset Inventory* descargada del Portal de Datos Abiertos
        como dataframe. Este conjunto de datos es un inventario de los recursos en el sitio.  \
        :ref:`Ver ejemplo <datos_gov.tabla_inventario>`

        :param token: (str) *opcional* - token de usuario de la API Socrata.
        :param limite_filas: (int) (valor mayor a 0), indica el número máximo de filas a descargar de la base de datos \
        asociada al api_id. El límite está pensado para bases de gran tamaño que superen la capacidad del computador.
        :return: base de datos en formato dataframe.
        """
        self.inventario = Datos(api_id=self.archivo_inventario, token=self.token, limite_filas=self.limite_filas)
        self.inventario.cargar_base()
        self.__inventario_espanol()

    def __inventario_espanol(self):
        """ Renombra los encabezados del inventario de bases de datos de Datos \
            Abiertos Colombia a términos en español.

        :param asset: (pandas.DataFrame) - Tabla de inventario del portal de datos\
            abiertos Colombia (https://www.datos.gov.co).
        :return: base de datos en formato dataframe.
        """

        lista_columnas = list(self.DIC_RENAME.keys())
        self.inventario._base = self.inventario._base[lista_columnas].rename(columns=self.DIC_RENAME)
        self.inventario._base["fecha_creacion"] = self.inventario._base["fecha_creacion"].apply(lambda x: x[0:10])
        self.inventario._base["fecha_actualizacion"] = self.inventario._base["fecha_actualizacion"].apply(lambda x: x[0:10])
        self.inventario._base["filas"] = self.inventario._base["filas"].astype(float)
        self.inventario._base["columnas"] = self.inventario._base["columnas"].astype(float)
        self.inventario._base["base_publica"] = self.inventario._base["base_publica"].map({"published": "Si", "unpublished": "No"})
        self.inventario._base["tipo"] = self.inventario._base["tipo"].map({
            "dataset": "conjunto de datos",
            "federatet_href": "enlace externo",
            "href": "enlace externo",
            "map": "mapa",
            "chart": "grafico",
            "filter": "vista filtrada",
            "file": "archivo o documento",
            "visualization": "visualizacion",
            "story": "historia",
            "datalens": "lente de datos",
            "form": "formulario",
            "calendar": "calendario",
            "invalid_datatype": "tipo_invalido"})

    def filtrar_tabla(self, columnas_valor: dict):
        """ Permite filtrar la base de datos de *tabla de inventario* de acuerdo con diferentes términos de búsqueda. Como son fechas, textos y otros. :ref:`Ver ejemplo <datos_gov.filtrar_tabla>`

        :param columnas_valor: (diccinario) {'nombre de columna': 'valor a buscar o rangos'}. \
        Corresponde al nombre de la columna a consultar y el valor a buscar.
        :param token: (str) opcional - token de usuario de la API Socrata.
        :return: dataframe Asset Inventory filtrado con los términos de búsqueda).
        """

        base_filtro = self.inventario._base.copy()
        columnas = base_filtro.columns.tolist()
        lista_vocales = ["a", "e", "i", "o", "u", "a", "e", "i", "o", "u"]
        lista_tildes = ["á", "é", "í", "ó", "ú", "ä", "ë", "ï", "ö", "ü"]
        columnas_string = columnas_valor.copy()

        # Revisar si término clave está en columnas de string
        for s in ["filas", "columnas", "fecha_creacion", "fecha_actualizacion"]:
            if s in columnas_string:
                del columnas_string[s]

        for s_key in columnas_string:
            if s_key not in columnas:
                return print(
                    "No existe una columna con el nombre '{0}'".format(s_key))
            else:
                pass

            s_value = columnas_valor[s_key]

            # Pasar los nombres de los términos a buscar a minúscula y quitar
            # tildes
            for i_s in range(len(s_value)):
                for i in range(len(lista_vocales)):
                    s_value[i_s] = s_value[i_s].lower().replace(lista_tildes[i], lista_vocales[i])

            # Pasar todo el texto de la columna donde se busca a minúscula
            asset_columna = base_filtro.loc[:, s_key].astype(str).apply(lambda x: x.lower())
            # Cambiar todas las tildes en el texto
            for i in range(len(lista_vocales)):
                asset_columna = asset_columna.apply(lambda x: x.replace(lista_tildes[i], lista_vocales[i]))

            # Crear columna que diga si se encuentra o no el ´termino en esa
            # observación
            asset_columna = pd.DataFrame(asset_columna)
            # Iterar para cada término que se quiere buscar
            asset_columna["true"] = 0
            asset_columna["true"] = asset_columna[s_key].apply(lambda x: 1 if all(q in x for q in s_value) else 0)
            # Quedarse con las observaciones donde se encontró el término
            asset_columna = asset_columna[asset_columna["true"] == 1]
            # Filtrar la base original con el índice dela base con las
            # observaciones encontradas
            base_filtro = base_filtro.loc[asset_columna.index]

        for s in ["filas", "columnas"]:
            if s in columnas_valor:
                # Obtener los límites inferior y superior deseados
                limite_inferior = columnas_valor[s][0]
                limite_superior = columnas_valor[s][1]
                # Si los limites son numéricos, por lo tanto en un rango, escoger
                # rango
                if type(limite_inferior) == int and type(limite_superior) == int:
                    base_filtro = base_filtro.loc[(base_filtro[s] <= limite_superior) & (base_filtro[s] >= limite_inferior), :]

                elif type(limite_inferior) == int and limite_superior == "+":
                    base_filtro = base_filtro.loc[base_filtro[s] >= limite_inferior, :]

                elif type(limite_inferior) == int and limite_superior == "-":
                    base_filtro = base_filtro.loc[base_filtro[s] <= limite_inferior, :]

                else:
                    return "Los parámetros de 'fila' y/o 'columna' tienen valores incorrectos"

        for s in ["fecha_creacion", "fecha_actualizacion"]:
            if s in columnas_valor:
                fecha_inicio = datetime.datetime.strptime(
                    columnas_valor[s][0], "%Y-%m-%d")

                # Crear columna con fecha en formato fecha
                base_filtro.loc[:, "{0}_fecha".format(s)] = base_filtro.loc[:, s].apply(
                    lambda x: datetime.datetime.strptime(x, "%Y-%m-%d") if x != "nan" else np.nan)

                if columnas_valor[s][1] == "+":
                    base_filtro = base_filtro.loc[base_filtro.loc[:, "{0}_fecha".format(s)] >= fecha_inicio, :]

                elif columnas_valor[s][1] == "-":
                    base_filtro = base_filtro.loc[base_filtro.loc[:, "{0}_fecha".format(s)] <= fecha_inicio, :]

                else:
                    fecha_fin = datetime.datetime.strptime(columnas_valor[s][1], "%Y-%m-%d")
                    base_filtro = base_filtro.loc[(base_filtro.loc[:, "{0}_fecha".format(s)] >= fecha_inicio) & (base_filtro.loc[:, "{0}_fecha".format(s)] <= fecha_fin), :]

                del base_filtro["{0}_fecha".format(s)]

        return base_filtro