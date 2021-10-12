# -*- coding: utf-8 -*-

import warnings
import pandas as pd
import requests
from unidecode import unidecode
import re


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
        Permite descargar un conjunto de datos del portal de datos.gov.co \
        dado su identificador `api_id` en el portal. \
        :ref:`Ver ejemplo <datos_gov.cargar_base>` (REVISAR).

        .. warning::
            Al descargar una base de datos utilizando el API de Socrata, \
            esta omitirá cualquier columna que no contenga registros, lo cual \
            puede generar inconsistencias con la información descrita en el \
            portal de datos abiertos.

        :param api_id: Identificador único del conjunto de datos registrado \
            en el API de Socrata.
        :type api_id: str
        :param limite_filas: Número máximo de registros a descargar del \
            conjunto de datos. Valor por defecto: `1000000000`.
        :type limite_filas: int, opcional
        :return: (DatosGo) Objeto del tipo DatosGov, que contiene la \
            información del conjunto de datos. Para obtener el DataFrame \
            revise la función to_dataframe(). (REVISAR)
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

    def to_dataframe(self):
        """
        Retorna el conjunto de datos descargado del portal de datos \
        abiertos (datos.gov.co) en formato pandas.DataFrame.
        :return: (pandas.DataFrame) conjunto de datos en DataFrame.
        """
        return self.datos

    def metadatos(self):
        """
        Retorna los metadatos del conjunto de datos descargado del \
        portal de datos abiertos (datos.gov.co) en un diccionario de Python.

        :return: (dict) Diccionario con los metadados del conjunto de datos.
        """
        return self.metadatos

    def tabla_inventario(self, filtro=None, limite_filas=10000000000):
        """
        Función que se conecta con el API de Socrata para el portal de \
        datos.gov.co y retorna el inventario de datos disponible. \
        :ref:`Ver ejemplo <datos_gov.tabla_inventario>` (REVISAR)

        :param filtro: Permite filtar la tabla de inventario de datos \
            tomando como referencia las columnas presentes en la tabla, \
            mediante un diccionario de datos del tipo {"nombre_columna": \
            ["valor buscado1", "valor buscado 2"]}. Para mayor información \
            consulte: (REVISAR)
        :type filtro: dict, opcional.
        :param limite_filas: Limite de registros a descargar del inventario \
            de datos. Por defecto: `10000000000`.
        :type limite_filas: int, opcional.
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
                    "federated_href": "enlace externo",
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
        if filtro is not None:
            tabla = self.__filtrar_tabla(tabla, filtro)

        return tabla

    def __filtrar_tabla(self, data, filtros):
        # valores del filtro
        col_filtros = set(filtros.keys())
        str_cols = list(
            set(data.dtypes[data.dtypes == object].index.tolist())
            & col_filtros
        )
        num_cols = list(set(["filas", "columnas"]) & col_filtros)
        date_cols = list(
            set(["fecha_creacion", "fecha_actualizacion"]) & col_filtros
        )

        if not len(str_cols + num_cols + date_cols):
            raise KeyError(
                "La tabla de inventario no tiene columna(s) con el nombre "
                f"{list(filtros.keys())}. Las llaves del diccionario solo "
                f" pueden tomar los siguientes valores:{list(data.columns)}"
            )
        # Buscar en columnas string
        if len(str_cols) > 0:
            for c in str_cols:
                if not isinstance(filtros[c], list):
                    raise TypeError(
                        "Los valores buscados deben ser tipo lista. Por "
                        "ejemplo, para buscar 'moneda' en el nombre de los "
                        "conjuntos de datos debe pasar filtro = "
                        "{'nombre':['moneda']}"
                    )
                value = [self.__normalizar_string(v) for v in filtros[c]]
                p = r"\b(?:{})\b".format("|".join(map(re.escape, value)))
                temp = data[c].apply(self.__normalizar_string)
                data = data[temp.str.contains(p)]
                if not data.shape[0]:
                    warnings.warn(
                        "No se encontró ningun registro con los valores: "
                        f"{value} en la columna: {c}"
                    )
                    return data

        # buscar limites en columas/filas numericas
        if len(num_cols) > 0:
            for c in num_cols:
                if not isinstance(filtros[c], list) or len(filtros[c]) != 2:
                    raise TypeError(
                        f"Para filtrar la tabla de inventario por [{c}] debe "
                        "pasar una lista de dos posiciones que representan el "
                        f"valor mínimo y máximo de {c} [v_min, v_max] por el "
                        "que desea filtrar."
                    )
                limites = filtros[c]
                data = data[(data[c] >= limites[0]) & (data[c] <= limites[1])]
                if not data.shape[0]:
                    return data

        # buscar en columnas de fecha
        if len(date_cols) > 0:
            for c in date_cols:
                if not isinstance(filtros[c], list) or len(filtros[c]) != 2:
                    raise TypeError(
                        f"Para filtrar la tabla de inventario por [{c}] debe "
                        "pasar una lista de dos posiciones que representan el "
                        f"la fecha inicial y fecha final de consulta "
                        "[fecha_inicial, fecha_final]. Por ejemplo, filtro = "
                        "{'fecha_creacion': ['2019-01-01', '2020-02-20']} "
                    )

                limites = filtros[c]
                data = data[(data[c] >= limites[0]) & (data[c] <= limites[1])]
                if not data.shape[0]:
                    return data

        return data

    def __normalizar_string(self, texto):
        return unidecode(texto.lower())
