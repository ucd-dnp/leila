# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from datetime import datetime
import requests


class DatosGov:
    """
    Clase para cargar conjutos de datos del portal de `datos.gov.co` y \
    descargar los metadatos de dichos conjuntos.
    """

    def __init__(self):
        self._dominio = "https://www.datos.gov.co/resource/"
        self._meta = "https://www.datos.gov.co/api/views/"
        self.metadatos = None
        self.datos = None
        self._DIC_RENAME = {
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
            "publication_stage": "base_publica",
        }

    def cargar_base(self, api_id, limite_filas=1000000000):
        """
        Se conecta al API de Socrata y retorna el conjunto de datos \
        del Portal de Datos Abiertos como DataFrame. \
        :ref:`Ver ejemplo <datos_gov.cargar_base>` (REVISAR).

        .. warning::
            Al descargar una base de datos utilizando el API de Socrata, \
            esta omitirá cualquier columna que no contenga registros, lo cual \
            puede generar inconsistencias con la información descrita en el \
            portal de datos abiertos.

        :param api_id: (str) Identificación de la base de datos asociado con \
            el API de Socrata.
        :param limite_filas: (int) (valor mayor a 0), indica el número \
            máximo de filas a descargar de la base de datos asociada al \
            `api_id`. El límite está pensado para bases de gran tamaño que \
            superen la capacidad del computador.
        :return: (DataFrame) conjunto de datos que se descargó del portal de \
            datos abiertos.
        """
        url = f"{self._dominio}{api_id}.csv?$limit={100}"
        # Solo se leen 100 filas para estimar tipo de datos
        temp = pd.read_csv(url)
        # cols que pueden contener fecha
        col_objs = list(temp.select_dtypes(object))
        url = f"{self._dominio}{api_id}.csv?$limit={limite_filas}"
        self.datos = pd.read_csv(url, parse_dates=col_objs)
        # Almacenar los metadatos
        query = requests.get(f"{self._meta}{api_id}.json")
        self.metadatos = dict(query.json())
        self.metadatos["n_rows"] = int(
            self.metadatos["columns"][0]["cachedContents"]["count"]
        )
        self.metadatos["n_cols"] = len(self.metadatos["columns"])
        query.close()
        return self

    def tabla_inventario(self, limite_filas=10000000000):
        """
        Función que se conecta con el API de Socrata para el portal de \
        datos.gov.co y retorna el inventario de datos disponible. \
        :ref:`Ver ejemplo <datos_gov.tabla_inventario>` (REVISAR)

        :param limite_filas: Limite de registros a descargar del inventario \
            de datos. Por defecto: `10000000000`.
        :type limite_filas: int, opcional
        :return: (pandas.DataFrame) Dataframe con la información de los datos \
            disponibles en el portal datos.gov.co. 
        """
        url = f"{self._dominio}uzcf-b9dh.csv?$limit={limite_filas}"
        tabla = pd.read_csv(
            url,
            usecols=list(self._DIC_RENAME.keys()),
            parse_dates=["last_data_updated_date", "creation_date"],
        )
        tabla.rename(columns=self._DIC_RENAME, inplace=True)
        tabla.replace(
            {
                "base_publica": {"published": "Si", "unpublished": "No"},
                "tipo": {
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
                    "invalid_datatype": "tipo_invalido",
                },
            },
            inplace=True,
        )
        return tabla


# METADATOS


def filtrar_tabla(columnas_valor, token=None):
    """ Permite filtrar la base de datos de *tabla de inventario* de acuerdo con\
        diferentes términos de búsqueda. Como son fechas, textos y otros. :ref:`Ver ejemplo <datos_gov.filtrar_tabla>`

    :param columnas_valor: (diccinario) {'nombre de columna':'valor a buscar o rangos'}. \
    Corresponde al nombre de la columna a consultar y el valor a buscar.
    :param token: (str) opcional - token de usuario de la API Socrata.
    :return: dataframe Asset Inventory filtrado con los términos de búsqueda).
    """
    # base_filtro=tabla.copy()
    asset = tabla_inventario(token)

    base_filtro = asset.copy()

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
                "No existe una columna con el nombre '{0}'".format(s_key)
            )
        else:
            pass

        s_value = columnas_valor[s_key]

        # Pasar los nombres de los términos a buscar a minúscula y quitar
        # tildes
        for i_s in range(len(s_value)):
            for i in range(len(lista_vocales)):
                s_value[i_s] = (
                    s_value[i_s]
                    .lower()
                    .replace(lista_tildes[i], lista_vocales[i])
                )

        # Pasar todo el texto de la columna donde se busca a minúscula
        asset_columna = (
            base_filtro.loc[:, s_key].astype(str).apply(lambda x: x.lower())
        )
        # Cambiar todas las tildes en el texto
        for i in range(len(lista_vocales)):
            asset_columna = asset_columna.apply(
                lambda x: x.replace(lista_tildes[i], lista_vocales[i])
            )

        # Crear columna que diga si se encuentra o no el ´termino en esa
        # observación
        asset_columna = pd.DataFrame(asset_columna)
        # Iterar para cada término que se quiere buscar
        asset_columna["true"] = 0
        asset_columna["true"] = asset_columna[s_key].apply(
            lambda x: 1 if all(q in x for q in s_value) else 0
        )
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
                base_filtro = base_filtro.loc[
                    (base_filtro[s] <= limite_superior)
                    & (base_filtro[s] >= limite_inferior),
                    :,
                ]

            elif type(limite_inferior) == int and limite_superior == "+":
                base_filtro = base_filtro.loc[
                    base_filtro[s] >= limite_inferior, :
                ]

            elif type(limite_inferior) == int and limite_superior == "-":
                base_filtro = base_filtro.loc[
                    base_filtro[s] <= limite_inferior, :
                ]

            else:
                return "Los parámetros de 'fila' y/o 'columna' tienen valores incorrectos"

    for s in ["fecha_creacion", "fecha_actualizacion"]:
        if s in columnas_valor:
            fecha_inicio = datetime.datetime.strptime(
                columnas_valor[s][0], "%Y-%m-%d"
            )

            # Crear columna con fecha en formato fecha
            base_filtro.loc[:, "{0}_fecha".format(s)] = base_filtro.loc[
                :, s
            ].apply(
                lambda x: datetime.datetime.strptime(x, "%Y-%m-%d")
                if x != "nan"
                else np.nan
            )

            if columnas_valor[s][1] == "+":
                base_filtro = base_filtro.loc[
                    base_filtro.loc[:, "{0}_fecha".format(s)] >= fecha_inicio,
                    :,
                ]

            elif columnas_valor[s][1] == "-":
                base_filtro = base_filtro.loc[
                    base_filtro.loc[:, "{0}_fecha".format(s)] <= fecha_inicio,
                    :,
                ]

            else:
                fecha_fin = datetime.datetime.strptime(
                    columnas_valor[s][1], "%Y-%m-%d"
                )
                base_filtro = base_filtro.loc[
                    (base_filtro.loc[:, "{0}_fecha".format(s)] >= fecha_inicio)
                    & (base_filtro.loc[:, "{0}_fecha".format(s)] <= fecha_fin),
                    :,
                ]

            del base_filtro["{0}_fecha".format(s)]

    return base_filtro
