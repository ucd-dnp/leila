# -*- coding: utf-8 -*-

import warnings
import pandas as pd
import requests
from unidecode import unidecode
import re
import datetime


class DatosGov:
    """
    Clase para cargar conjuntos de datos del portal de `datos.gov.co` y \
    descargar los metadatos de dichos conjuntos.
    """

    def __init__(self):
        self._dominio = "https://www.datos.gov.co/resource/"
        self._meta = "https://www.datos.gov.co/api/views/"
        self.__metadatos = None
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
        :ref:`Ver ejemplo <Cargar conjunto de datos con número API>`.

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
        :return: (DatosGov) Objeto del tipo DatosGov, que contiene la \
            información del conjunto de datos. Para obtener el DataFrame \
            revise la función to_dataframe().
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
        self.__metadatos = dict(query.json())
        if "cachedContents" in self.__metadatos["columns"][0] and "count" in self.__metadatos["columns"][0]["cachedContents"]:
            self.__metadatos["n_rows"] = int(
                self.__metadatos["columns"][0]["cachedContents"]["count"]
            )
        else:
            self.__metadatos["n_rows"] = "NA"
        if "columns" in self.__metadatos:
            self.__metadatos["n_cols"] = len(self.__metadatos["columns"])
        else:
            self.__metadatos["n_cols"] = "NA"
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
        return self.__renombrar_metadatos()

    def tabla_inventario(self, filtro=None, limite_filas=10000000000):
        """
        Función que se conecta con el API de Socrata para el portal de \
        datos.gov.co y retorna el inventario de datos disponible. \
        :ref:`Ver ejemplo <Ejemplo tabla_inventario>`

        :param filtro: Permite filtar la tabla de inventario de datos \
            tomando como referencia las columnas presentes en la tabla, \
            mediante un diccionario de datos del tipo {'nombre_columna': \
            ['valor buscado1', 'valor buscado 2']}. Para mayor información \
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

    def __renombrar_metadatos(self):
        # Crear diccionario para renombrar algunos metadatos
        dic_rename = {
            'id': 'numero_api',
            'name': 'nombre',
            'description': 'descripcion',
            'assetType': 'tipo',
            'attributionLink': 'url',
            'category': 'categoria',
            'createdAt': 'fecha_creacion', 
            'viewCount': 'numero_vistas',
            'downloadCount': 'numero_descargas', 
            'licenseId': 'licencia',
            'publicationDate': 'fecha_publicacion', 
            'publicationStage': 'base_publica',
            'rowsUpdatedAt': 'fecha_actualizacion',  
            'n_rows': 'numero_filas',
            'n_cols': 'numero_columnas'
        }

        # Crear nuevo diccionario con algunos valores renombrados de metadatos
        dic_metadatos = {}
        dic_metadatos = {v: self.__metadatos[k] if k in list(self.__metadatos.keys()) else "NA" for (k, v) in dic_rename.items()}
        
        # Crear valores de fecha (a partir de integers)
        dic_metadatos['fecha_creacion'] = datetime.datetime.fromtimestamp(dic_metadatos['fecha_creacion']).strftime('%Y-%m-%d')
        dic_metadatos['fecha_publicacion'] = datetime.datetime.fromtimestamp(dic_metadatos['fecha_publicacion']).strftime('%Y-%m-%d')
        dic_metadatos['fecha_actualizacion'] = datetime.datetime.fromtimestamp(dic_metadatos['fecha_actualizacion']).strftime('%Y-%m-%d')

        # Agregar licencias
        if 'license' in self.__metadatos and 'name' in self.__metadatos['license']['name']:
            dic_metadatos['licencia'] = self.__metadatos['license']['name']
        else:
            dic_metadatos['licencia'] = "NA"
        
        if 'license' in self.__metadatos and 'termsLink' in self.__metadatos['license']:
            dic_metadatos['licencia_url'] = self.__metadatos['license']['termsLink']
        else:
            dic_metadatos['licencia_url'] = "NA"

        # # Agregar filas y columnas
        # dic_metadatos["filas"] = self.__metadatos['n_rows']
        # dic_metadatos["columnas"] = self.__metadatos['n_cols']

        # Diccionario para renombrar metadatos de 'Información de la Entidad'
        entidad_info_nombres = {
            'entidad': 'Nombre de la Entidad', 
            'entidad_municipio': 'Municipio',
            'entidad_sector': 'Sector', 
            'entidad_departamento': 'Departamento', 
            'entidad_orden': 'Orden', 
            'entidad_dependencia': 'Área o dependencia', 
        }

        # Diccionario para renombrar metadatos de 'Información de Datos'
        entidad_datos_nombres = {
            'cobertura': 'Cobertura Geográfica', 
            'idioma': 'Idioma', 
            'frecuencia_actualizacion': 'Frecuencia de Actualización'
        }

        # Crear diccionarios reducidos de 'Información de la Entidad' e 'Información de Datos'
        dic_info_entidad = self.__metadatos['metadata']['custom_fields']['Información de la Entidad']
        dic_info_datos = self.__metadatos['metadata']['custom_fields']['Información de Datos']

        # Agregar información renombrada a diccionario de metadatos
        for k, v in entidad_info_nombres.items():
            if v in dic_info_entidad:
                dic_metadatos[k] = dic_info_entidad[v]
            else:
                dic_metadatos[k] = "NA"
            
        for k, v in entidad_datos_nombres.items():
            if v in dic_info_datos:
                dic_metadatos[k] = dic_info_datos[v]
            else:
                dic_metadatos[k] = "NA"


        # Agregar dueño
        if 'owner' in self.__metadatos and 'displayName' in self.__metadatos['owner']:
            dic_metadatos['dueno'] = self.__metadatos['owner']['displayName']
        else:
            dic_metadatos['dueno'] = "NA"

        # Diccionario de columnas
        dic_c = {}

        # Agregar cada columna renombrada al diccionario de columnas
        for c in self.__metadatos['columns']:
            name = c["name"]
            dic_c[name] = {
                'tipo': c['dataTypeName'], 
                'descripcion': c['description'], 
                'nombre_df': c['fieldName']      
            }

        # Agergar diccionario de columnas a diccionario de metadatos
        dic_metadatos["columnas"] = dic_c

        return dic_metadatos