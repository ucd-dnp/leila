# -*- coding: utf-8 -*-
from leila.datos_gov import DatosGov
import pandas as pd
import numpy as np
import scipy.stats as sstats
import warnings
import re
import math
import phik
import openpyxl
import requests
from difflib import SequenceMatcher
import datetime
from dateutil.parser import parse

class CalidadDatos:
    """
    Constructor por defecto de la clase leila.CalidadDatos. Esta clase se \
    encarga de manejar todas las funciones asociadas a la medición de la \
    calidad de los datos en una base de datos estructurada.

    Soporta la lectura directa de archivos con extensión `.xlsx` y \
    `.csv`, para otro tipo de formato (`.xls`, `xlsm`, `xlsb`, `odf`, \
    `ods` y `odt`) se recomienda hacer la conversión al formato `.csv`.

    **Nota:** Se recomienda cargar directamente los archivos con esta clase, \
    en lugar de utilizar pandas.

    :param datos: Se acepta cualquier ruta o path a archivos tipo `.xlsx` \
        o `.csv` (recomendado).\
        Si desea pasar un `DataFrame` de pandas, LEILA soporta este tipo \
        de entrada.
        LEILA también soporta como entrada objectos del tipo \
        `leila.DatosGov`. Para este tipo de entrada LEILA tendrá en el \
        futuro funcionalidades extendidas de calidad de datos con base \
        a los metadatos del conjunto de datos descargado del portal \
        datos.gov.co.
    :type datos: str, pandas.DataFrame, leila.DatosGov
    :param castDatos: Indica si se desean convertir las columnas al \
        mejor tipo de datos para cada columna según la función \
        `convert_dtypes` de Pandas. Por ejemplo si una columna es de \
        tipo `string`, pero sus datos son en su mayoría números, se \
        convierte a columna númerica. Valor por defecto: `True`.
    :type castDatos: bool, opcional
    :param diccionarioCast: Diccionario donde se especifican los tipos \
        de datos a los que se desean convertir las columnas dentro \
        del conjunto de datos. Por ejemplo, {'col1': 'booleano', \
        'edad':'numerico'}, donde `col1` y `edad` son columnas de la base \
        de datos. Los valores a los que se pueden convertir son: \
        ['string', 'numerico', 'booleano', 'fecha', 'categorico']. Valor \
        por defecto: `None`.
    :type diccionarioCast: dict , opcional
    :param errores: Indica qué hacer con las columnas cuyo tipo no se \
        puede cambiar al solicitado en `diccionarioCast`. Valor por \
        defecto: `"ignore"`.
    :type errores: {"ignore", "coerce", "raise"}, opcional
    :param formato_fecha: Formato string para el cast de las variables \
        tipo fecha. Para más información sobre las opciones de strings, \
        consulte: \
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior. \
        Valor por defecto: `"%d/%m/%Y"`.
    :type formato_fecha: str, optional
    :param ``**kwargs``: Parámetros adicionales que se le pueden pasar a la \
        función `pandas.read_csv()`. Para más información sobre estos \
        parámetros, consulte: \
        https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html.
    """

    def __init__(
        self,
        datos,
        castDatos=True,
        diccionarioCast=None,
        errores="ignore",
        formato_fecha="%d/%m/%Y",
        **kwargs,
    ):
        """
        Constructor por defecto de la clase leila.CalidadDatos. Esta clase se \
        encarga de manejar todas las funciones asociadas a la medición de la \
        calidad de los datos en una base de datos estructurada.        
        """
        self._dic_tipo = {
            "int": "Numérico",
            "float": "Numérico",
            "str": "Texto",
            "bool": "Booleano",
            "date": "Fecha",
            "object": "Otro",
        }
        self._metadatos = None
        self.__source = None
        self.__kwargs = kwargs
        self._castDatos = castDatos
        self._castdic = diccionarioCast
        self._errores = errores
        self._strdate = formato_fecha
        self.base = datos
        self._varCategoricas = []

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, datos):
        if not isinstance(self._castdic, (dict, type(None))):
            raise ValueError(
                "'diccionarioCast' debe ser de tipo diccionario (dict)."
            )

        if not isinstance(self._castDatos, bool):
            raise ValueError("'castDatos' debe ser de tipo booleano (bool).")

        self.__get_source(datos)
        if self.__source == "excel":
            self.__read_excel(datos, **self.__kwargs)
        elif self.__source == "csv":
            self.__read_csv(datos, **self.__kwargs)
        elif self.__source == "pandas":
            self._base = datos
        elif self.__source == "leila":
            self.__from_leila(datos)

        if self._castdic:
            for col, tipo in self._castdic.items():
                if tipo == "string":
                    self._base[col] = self._base[col].apply(lambda x: str(x))
                elif tipo == "numerico":
                    self._base[col] = pd.to_numeric(
                        self._base[col], errors=self._errores
                    )
                elif tipo == "booleano":
                    self._base[col] = self._base[col].astype("bool")
                elif tipo == "fecha":
                    self._base[col] = pd.to_datetime(
                        self._base[col],
                        format=self._strdate,
                        errors=self._errores,
                    )
                elif tipo == "categorico":
                    self._base[col] = pd.Categorical(self._base[col])
                else:
                    raise ValueError(
                        "Los valores de las llaves de 'diccionarioCast' "
                        "solo admiten: 'string', 'numerico', 'booleano', "
                        "'fecha' o 'categorico' "
                    )

        if self._castDatos:
            self._base = self._base.convert_dtypes()
        else:
            self._base = self._base.convert_dtypes(
                infer_objects=False,
                convert_string=True,
                convert_integer=False,
                convert_boolean=False,
                convert_floating=False,
            )

        # Tipo más común de cada columna
        tipo_mas_comun = [
            re.findall("'(.*)'", str(type(self._base[col][0])))[0]
            for col in self._base.columns
        ]

        # Tipo según 'dtypes'
        col_dtypes = list(self._base.dtypes.apply(str))
        self.lista_tipos_columnas = [
            list(self._base.columns),
            col_dtypes,
            tipo_mas_comun,
        ]

    # Tipos de las columnas
    def TipoColumnas(
        self, tipoGeneral=True, tipoGeneralPython=True, tipoEspecifico=True
    ):
        """
        Retorna el tipo de dato de cada columna del dataframe. \
        :ref:`Ver ejemplo <Tipos de cada columna>`

        :param tipoGeneral: (bool) {True, False}, valor por defecto: True. \
            Incluye el tipo general de cada columna. Los tipos son: numérico,\
            texto, booleano, otro.
        :param tipoGeneralPython: (bool) {True, False}, valor por defecto: \
            True. Incluye el tipo general de cada columna dado por el método\
            'pandas.dtypes' de Pandas
        :param tipoEspecifico: (bool) {True, False}, valor por defecto: True.\
            Incluye el porcentaje de los tres tipos más frecuentes de cada\
            columna. Se aplica la función nativa 'type' de Python para cada \
            observación.

        :return: Dataframe de pandas con los tipos de dato de cada columna.
        """
        if not isinstance(tipoGeneral, bool):
            raise ValueError("'tipoGeneral' debe ser booleano. {True, False}")

        if not isinstance(tipoGeneralPython, bool):
            raise ValueError(
                "'tipoGeneralPython' debe ser booleano. {True, False}"
            )

        if not isinstance(tipoEspecifico, bool):
            raise ValueError(
                "'tipoEspecifico' debe ser booleano. {True, False}"
            )

        if not (tipoGeneral or tipoGeneralPython or tipoEspecifico):
            raise ValueError(
                "Al menos uno de los párametros tipoGeneral, tipoGeneralPython"
                " o tipoEspecifico debe ser True"
            )

        lista_nombres = self.lista_tipos_columnas[0]
        tipos_dtypes = self.lista_tipos_columnas[1]
        tipo_datos = dict()

        # Tipo general en español
        if tipoGeneral:
            general = list(
                map(
                    self._dic_tipo.get,
                    [
                        re.findall("|".join(list(self._dic_tipo.keys())), k)[0]
                        for k in list(map(str.lower, tipos_dtypes))
                    ],
                )
            )
            tipo_datos["tipo_general"] = general

        # Tipo general de Python
        if tipoGeneralPython:
            tipo_datos["tipo_general_python"] = tipos_dtypes.copy()

        # Tipo específico Python
        if tipoEspecifico:
            temp_list = []
            for s in lista_nombres:
                tip = (
                    self.base[s]
                    .apply(type)
                    .value_counts(normalize=True, dropna=False)
                )

                nombre_tipo = [
                    re.findall("'(.*)'", x)[0]
                    for x in list(map(str, tip.index.tolist()))
                ]

                temp_dic = dict()
                for i, (nom, t) in enumerate(zip(nombre_tipo, tip)):
                    key = "tipo_especifico_" + str(i + 1)
                    temp_dic[key] = [f"'{nom}': {round(t*100,2)}%"]
                temp_list.append(temp_dic)

            max_keys = max(temp_list, key=len).keys()
            for d in temp_list:
                for key in max_keys:
                    if key not in d:
                        d[key] = [""]

                for k, v in d.items():
                    if k in tipo_datos:
                        tipo_datos[k].extend(v)
                    else:
                        tipo_datos[k] = v

        tips = pd.DataFrame.from_dict(
            tipo_datos, orient="index", columns=lista_nombres
        ).T

        return tips

    # valores únicos en cada columna
    # sin missing values
    def ValoresUnicos(self, faltantes=False):
        """
        Calcula la cantidad de valores únicos de cada columna del dataframe.

        :param faltantes: (bool) {True, False}, Valor por defecto: False. \
            Indica si desea tener en cuenta los valores faltantes en el \
            conteo de valores únicos.
        :return: Serie de pandas con la cantidad de valores únicos de cada \
            columna.
        """
        if not isinstance(faltantes, bool):
            raise ValueError("'faltantes' debe ser booleano. {True, False}.")

        if faltantes:
            unicos_columnas = self.base.apply(
                lambda x: len(x.value_counts(dropna=False)), axis=0
            )
        else:
            unicos_columnas = self.base.nunique()

        return unicos_columnas

    #  Valores faltantes (missing values)
    def ValoresFaltantes(self, numero=False):
        """
        Calcula el porcentaje/número de valores faltantes de cada columna \
        del dataframe. :ref:`Ver ejemplo <Datos faltantes>`

        :param numero: (bool) {True, False} Valor por defecto: False. Si el \
            valor es `False` el resultado se expresa como un cociente, si el \
            valor es `True` el valor se expresa como una cantidad de \
            registros (número entero).
        :return: Serie de pandas con la cantidad/cociente de valores \
            faltantes de cada columna.
        """

        if not isinstance(numero, bool):
            raise ValueError("'numero' debe ser booleano. {True, False}.")

        if numero:
            missing_columnas = pd.isnull(self.base).sum()
        else:
            missing_columnas = pd.isnull(self.base).sum() / len(self.base)

        return missing_columnas

    # Porcentaje y número de filas y columnas no únicas
    def CantidadDuplicados(self, eje=0, numero=False, numero_filas=30000):
        """
        Retorna el porcentaje/número de filas o columnas duplicadas \
        (repetidas) en el dataframe. \
        :ref:`Ver ejemplo <Datos duplicados>`

        :param eje: (int) {1, 0} Valor por defecto: 0. Si el valor \
            es `1` la validación se realiza por columnas. Si el valor es \
            `0` la validación se realiza por filas.
        :param numero: (bool) {True, False} Valor por defecto: False. Si el \
            valor es `False` el resultado se expresa como un cociente, si el \
            valor es `True` el valor se expresa como una cantidad de \
            registros (número entero).
        :param numero_filas: (int) Valor por defecto: 30000. Número de filas \
            que tendrá cada columna cuando se verifiquen los duplicados por \
            columna (cuando 'eje = 1'). Se utiliza para agilizar el proceso \
            de verificación de duplicados de columnas, el cual puede resultar \
            extremadamente lento para un conjunto de datos con muchas filas.
        :return: (int o float) Resultado de unicidad.
        """
        if not isinstance(numero, bool):
            raise ValueError("'numero' debe ser booleano. {True, False}.")
        if eje not in [0, 1]:
            raise ValueError("'eje' solo puede ser 0 o 1.")

        # Revisar si hay columnas con tipos diccionario o lista
        temp = np.array(self.lista_tipos_columnas)
        lista_columnas_dict = list(
            temp[0][(temp[2] == "dict") | (temp[2] == "list")]
        )

        # Proporcion (decimal) de columnas repetidas
        if eje == 1:
            if self.base.shape[0] <= numero_filas:
                if not len(lista_columnas_dict):
                    no_unic_columnas = self.base.T.duplicated()
                else:
                    subset = self.base.columns.difference(lista_columnas_dict)
                    no_unic_columnas = pd.concat(
                        [
                            self.base[subset],
                            self.base.loc[:, lista_columnas_dict].astype(str),
                        ],
                        axis=1,
                    ).T.duplicated()

            else:
                tercio = numero_filas // 3
                mitad = numero_filas // 2

                idx_mini = np.concatenate(
                    [
                        np.arange(tercio),
                        np.arange(mitad, mitad + tercio),
                        np.arange(numero_filas - tercio, numero_filas),
                    ]
                )
                if not len(lista_columnas_dict):
                    no_unic_columnas = self.base.iloc[idx_mini].T.duplicated()
                else:
                    subset = self.base.columns.difference(lista_columnas_dict)
                    no_unic_columnas = pd.concat(
                        [
                            self.base[subset].iloc[idx_mini],
                            self.base.loc[:, lista_columnas_dict]
                            .iloc[idx_mini]
                            .astype(str),
                        ],
                        axis=1,
                    ).T.duplicated()

            if numero:
                cols = no_unic_columnas.sum()
            else:
                cols = no_unic_columnas.sum() / self.base.shape[1]

        # Proporción de filas repetidas
        else:
            if not len(lista_columnas_dict):
                no_unic_filas = self.base.duplicated()
            else:
                subset = self.base.columns.difference(lista_columnas_dict)
                no_unic_filas = pd.concat(
                    [
                        self.base[subset],
                        self.base.loc[:, lista_columnas_dict].astype(str),
                    ],
                    axis=1,
                ).duplicated()
            if numero:
                cols = no_unic_filas.sum()
            else:
                cols = no_unic_filas.sum() / self.base.shape[0]

        return cols

    # Emparejamiento de columnas y filas no únicas
    def EmparejamientoDuplicados(self, col=False, limite_filas=30000):
        """
        Retorna las columnas o filas que presenten valores duplicados del \
        dataframe. \
        :ref:`Ver ejemplo <Emparejamiento de duplicados>`

        :param col: (bool) {True, False}, valor por defecto: False. Si el \
            valor es `True` la validación se realiza por columnas, en caso \
            contrario, la validación se hace por filas.
        :param numero_filas: (int), valor por defecto: 30000. Número de filas \
            que tendrá cada columna cuando se verifiquen los duplicados por \
            columna (cuando `eje=1`). Se utiliza para agilizar el proceso de \
            verificación de duplicados por columnas, el cual puede resultar \
            extremadamente lento para un conjunto de datos con muchas filas.
        :return: (Dataframe) Matriz que relaciona los índices de filas o \
            nombre de columnas que presentan valores duplicados.
        """

        if not isinstance(col, bool):
            raise ValueError("'col' debe ser booleano. {True, False}.")

        # Revisar si hay columnas con tipos diccionario o lista
        temp = np.array(self.lista_tipos_columnas)
        lista_columnas_dict = list(
            temp[0][(temp[2] == "dict") | (temp[2] == "list")]
        )

        # Proporcion (decimal) de columnas repetidas
        if col:
            if self.base.shape[0] <= limite_filas:
                if not len(lista_columnas_dict):
                    no_unic_columnas = self.base.T.duplicated(keep=False)
                else:
                    subset = self.base.columns.difference(lista_columnas_dict)
                    no_unic_columnas = pd.concat(
                        [
                            self.base[subset],
                            self.base.loc[:, lista_columnas_dict].astype(str),
                        ],
                        axis=1,
                    ).T.duplicated(keep=False)

            else:
                tercio = limite_filas // 3
                mitad = limite_filas // 2

                idx_mini = np.concatenate(
                    [
                        np.arange(tercio),
                        np.arange(mitad, mitad + tercio),
                        np.arange(limite_filas - tercio, limite_filas),
                    ]
                )

                if not len(lista_columnas_dict):
                    no_unic_columnas = self.base.iloc[idx_mini].T.duplicated(
                        keep=False
                    )
                else:
                    subset = self.base.columns.difference(lista_columnas_dict)
                    no_unic_columnas = pd.concat(
                        [
                            self.base[subset].iloc[idx_mini],
                            self.base.loc[:, lista_columnas_dict]
                            .iloc[idx_mini]
                            .astype(str),
                        ],
                        axis=1,
                    ).T.duplicated(keep=False)

            if not no_unic_columnas.sum():
                print("No hay columnas duplicadas")
                return

            if self.base.shape[0] <= limite_filas:
                subset1 = self.base.iloc[:, list(no_unic_columnas)]
            else:
                subset1 = self.base.iloc[idx_mini, list(no_unic_columnas)]

            d_duplicados = {}
            verificado = []
            for i, r1 in enumerate(subset1):
                indexs = []
                if r1 in verificado:
                    continue

                verificado.append(r1)
                indexs.append(r1)
                for r2 in subset1.iloc[:, i + 1 :]:
                    if r2 not in verificado:
                        comp = subset1[r1].equals(subset1[r2])
                        if comp:
                            indexs.append(r2)
                            verificado.append(r2)
                d_duplicados[str(r1)] = indexs
            d = pd.DataFrame.from_dict(d_duplicados, orient="index").T
            d.columns = [
                f"Columnas iguales {q + 1}" for q in range(d.shape[1])
            ]
        # Proporción de filas repetidas
        else:
            if not len(lista_columnas_dict):
                no_unic_filas = self.base.duplicated(keep=False)
            else:
                subset = self.base.columns.difference(lista_columnas_dict)
                no_unic_filas = pd.concat(
                    [
                        self.base[subset],
                        self.base.loc[:, lista_columnas_dict].astype(str),
                    ],
                    axis=1,
                ).duplicated(keep=False)

            if not no_unic_filas.sum():
                print("No hay filas duplicadas")
                return None

            subset1 = self.base.iloc[list(no_unic_filas)]

            d_duplicados = {}
            verificado = []

            n_rows = subset1.shape[0]
            for r1 in range(n_rows):
                indexs = []
                if r1 in verificado:
                    continue

                verificado.append(r1)
                indexs.append(subset1.index[r1])
                for r2 in range(r1 + 1, n_rows):
                    if r2 not in verificado:
                        comp = subset1.iloc[r1].equals(subset1.iloc[r2])
                        if comp:
                            indexs.append(subset1.index[r2])
                            verificado.append(r2)
                d_duplicados[str(r1)] = indexs

            d = pd.DataFrame.from_dict(d_duplicados, orient="index").T
            d.columns = [f"Filas iguales {q + 1}" for q in range(d.shape[1])]

        return d

    # Valores extremos
    def ValoresExtremos(self, extremos="ambos", numero=False, **kwargs):
        """
        Calcula el porcentaje o cantidad de valores extremos (outliers) de \
        cada columna numérica (las columnas con números en formato string se \
        intentarán transformar a columnas numéricas).

        :param extremos: {'superior', 'inferior', 'ambos'}. Si el valor es \
            `inferior` se tienen en cuenta los registros con valor menor al \
            límite inferior calculado por la metodología de valor atípico \
            por rango intercuartílico. Si el valor es `superior` se tienen \
            en cuenta los registros con valor \
            mayor al límite superior calculado por la metodología de valor \
            atípico por rango intercuartílico. Si el valor es `ambos` se \
            tienen en cuenta los registros con valor menor al límite inferior \
            calculado por la  metodología de valor atípico por rango \
            intercuartílico, y también aquellos con valor mayor al límite \
            superior calculado por la metodología de valor atípico por rango \
            intercuartílico. Valor por defecto "ambos"
        :type extremos: str, opcional.
        :param numero: Si `False` el resultado se expresa como una proporcion \
            (en decimales), si el valor es `True` el valor se expresa como \
            una cantidad de registros (número entero). Valor por defecto False
        :type numero: bool, opcional.
        :return: (pandas.Series) Serie de pandas con la cantidad/proporción \
            de valores extremos (outliers) de cada columna.
        """
        if not isinstance(numero, bool):
            raise ValueError("'numero' debe ser booleano. {True, False}.")
        if extremos not in ["superior", "inferior", "ambos"]:
            raise ValueError(
                "Valor  desconocido para  el parametro `extremos`. Este debe "
                "ser 'superior', 'inferior' o 'ambos'."
            )
        if "col_num" not in kwargs:
            # Revisar si hay columnas númericas
            col_num = self.base.select_dtypes(
                include=np.number
            ).columns.tolist()
            if not len(col_num):
                print("El conjunto de datos no tiene columnas numéricas")
                return
        else:
            col_num = kwargs.pop("col_num")

        # Calcular valores de columnas en percentiles 25 y 75
        percentiles_25 = (
            self.base[col_num]
            .astype(float)
            .apply(lambda x: np.nanpercentile(x, 25), axis=0)
        )
        percentiles_75 = (
            self.base[col_num]
            .astype(float)
            .apply(lambda x: np.nanpercentile(x, 75), axis=0)
        )

        # Calcular IQR
        iqr = percentiles_75 - percentiles_25
        iqr_upper = percentiles_75 + iqr * 1.5
        iqr_lower = percentiles_25 - iqr * 1.5

        # Calcular valores extremos
        dic_outliers = {}
        if extremos == "ambos":
            for i in range(0, len(iqr)):
                dic_outliers[self.base[col_num].columns[i]] = (
                    self.base[col_num].iloc[:, i] > iqr_upper[i]
                ) | (self.base[col_num].iloc[:, i] < iqr_lower[i])
        elif extremos == "superior":
            for i in range(0, len(iqr)):
                dic_outliers[self.base[col_num].columns[i]] = (
                    self.base[col_num].iloc[:, i] > iqr_upper[i]
                )
        else:  # extremos == "inferior":
            for i in range(0, len(iqr)):
                dic_outliers[self.base[col_num].columns[i]] = (
                    self.base[col_num].iloc[:, i] < iqr_lower[i]
                )

        base_outliers = pd.DataFrame(dic_outliers)

        cantidad_outliers = base_outliers.sum()
        if not numero:
            cantidad_outliers /= base_outliers.shape[0]

        return cantidad_outliers

    # Estadísticas descriptivas de columnas numéricas
    def DescripcionNumericas(self, variables=None):
        """
        Calcula estadísticas descriptivas de cada columna numérica. \
        Incluyen media, mediana, valores en distintos percentiles,\
        desviación estándar, valores extremos y porcentaje de valores \
        faltantes. :ref:`Ver ejemplo <Estadísticas descriptivas de variables numéricas>`

        :param variables: Por defecto None. lista de nombres de las \
            columnas númericas que se desea analizar. Si `None`, todas las \
            columnas númericas son seleccionadas.
        :type variables: list, opcional.
        :return: (pandas.DataFrame) Dataframe con las estadísticas \
            descriptivas de las columnas númericas.
        """

        # Revisar si hay columnas númericas
        col_num = self.base.select_dtypes(include=np.number).columns.tolist()
        if not len(col_num):
            print("El conjunto de datos no tiene columnas numéricas")
            return

        if isinstance(variables, list):
            col_num = [q for q in variables if q in col_num]
            if not len(col_num):
                raise ValueError(
                    "El parámetro `variables` no contiene ningún nombre "
                    "de columna númerica valido."
                )
        elif variables is None:
            pass
        else:
            raise ValueError("No se reconoce el parámetro `variables`.")

        # Calcular estadísticas descriptivas
        try:
            base_descripcion = self.base.loc[:, col_num].describe().T
        except Exception:
            base_descripcion = (
                self.base.loc[:, col_num].astype(np.float64).describe().T
            )
        base_descripcion["missing"] = pd.isnull(
            self.base.loc[:, col_num]
        ).sum() / len(self.base.loc[:, col_num])
        base_descripcion["outliers_total"] = self.ValoresExtremos(
            col_num=col_num
        )
        base_descripcion["outliers_altos"] = self.ValoresExtremos(
            extremos="superior", col_num=col_num
        )
        base_descripcion["outliers_bajos"] = self.ValoresExtremos(
            extremos="inferior", col_num=col_num
        )

        return base_descripcion

    # Varianza de columnas numéricas con el cálculo de percentiles
    def VarianzaEnPercentil(self, percentil_inferior=5, percentil_superior=95):
        """
        Retorna el nombre de las columnas numéricas cuyo `percentil_inferior` \
        sea igual a su `percentil_superior`.

        :param percentil_inferior: Percentil inferior de referencia en la \
            comparación. Valor por defecto 5.
        :type percentil_inferior: int, opcional.
        :param percentil_superior: Percentil superior de referencia en la \
            comparación. Valor por defecto 95.
        :type percentil_superior: int, opcional
        :return: (list) Lista de los nombres de las columnas cuyo percentil \
            inferior es igual al percentil superior.
        """

        # Revisar si hay columnas númericas
        col_num = self.base.select_dtypes(include=np.number).columns.tolist()
        if not len(col_num):
            print("El conjunto de datos no tiene columnas numéricas")
            return []

        # Calcular percentiles
        percentil_bajo = self.base[col_num].apply(
            lambda x: np.percentile(x.dropna(), 5), axis=0
        )
        percentil_alto = self.base[col_num].apply(
            lambda x: np.percentile(x.dropna(), 95), axis=0
        )

        percentiles_true = percentil_alto.index[
            percentil_alto == percentil_bajo
        ]

        if not len(percentiles_true):
            return []
        else:
            return list(percentiles_true)

    # tabla de valores únicos para cada variable de texto
    def DescripcionCategoricas(
        self,
        limite=0.5,
        categoriasMaximas=30,
        incluirNumericos=True,
        variables=None,
    ):
        """
        Genera una tabla con los primeros 10 valores más frecuentes de las \
        columnas categóricas del dataframe, además calcula su frecuencia y \
        porcentaje dentro del total de observaciones. Incluye los valores \
        faltantes. :ref:`Ver ejemplo <Estadísticas descriptivas de variables categóricas>`.

        :param limite: Valor de 0 a 1. Se utiliza para determinar si las \
            variables posiblemente son de tipo categóricas y ser incluidas \
            en el análisis. Si el número de valores únicos por columna es \
            mayor al número de registros limite, se considera que la \
            variable no es categórica. Por defecto `0.5`
        :type limite: float, opcional
        :param categoriasMaximas: Valor mayor a 1. Indica el máximo número \
            de categorías de una variable para que sea incluida en el \
            análisis. Por defecto `30`.
        :type categoriasMaximas: int, opcional
        :param incluirNumericos:  Determina si se desea considerar las \
            variables numéricas como categóricas e incluirlas en el \
            análisis. Si el valor es `True` se incluyen las variables \
            numéricas, solo si `variables` es igual a `None`. Por defecto \
            `True`.
        :type incluirNumericos: bool, opcional
        :param variables: Lista de nombres de las columnas separados \
            por comas. Permite escoger las columnas de interés. Si `variables`\
            es `None`, se considera todas las columnas del conjunto de datos. \
            Por defecto es `None`.
        :type variables: [type], opcional
        :return: (pandas.DataFrame) Dataframe con las estadísticas \
            descriptivas de las columnas identificadas de tipo categórica.
        """

        if not isinstance(incluirNumericos, bool):
            raise ValueError(
                "incluirNumericos debe ser booleano. {True, False}."
            )
        if isinstance(variables, list):
            not_in_cols = [
                v for v in variables if v not in self.lista_tipos_columnas[0]
            ]
            variables = [v for v in variables if v not in not_in_cols]
            if len(not_in_cols):
                cols = ", ".join(not_in_cols)
                warnings.warn(
                    f"Las variables {cols} no están en la base de datos"
                )

            if not len(variables):
                raise ValueError(
                    "El parámetro `variables` no contiene ningún nombre "
                    "de columna valido."
                )
        elif variables is None:
            variables = self.lista_tipos_columnas[0].copy()
            if not incluirNumericos:
                col_num = self.base.select_dtypes(
                    include=np.number
                ).columns.tolist()
                variables = [v for v in variables if v not in col_num]
        else:
            raise ValueError(
                "El parámetro `variables` debe ser una lista de nombres "
                "de variables en el conjunto de datos"
            )

        missing = self.base.columns[
            self.base.isnull().sum() == self.base.shape[0]
        ]
        if len(missing):
            variables = [v for v in variables if v not in missing]

        if not len(variables):
            warnings.warn(
                "No hay variables categóricas en el conjunto de datos."
            )
            return pd.DataFrame()

        # Detectar columnas de tipo object y transformar a string
        colObjs = list(
            self.base[variables].columns[
                self.base[variables].dtypes == "object"
            ]
        )
        if len(colObjs):
            tempData = self.base[colObjs].astype("str")
            variables = [v for v in variables if v not in colObjs]

        # Filtrar por el número de categorías únicas en cada variable
        if categoriasMaximas >= 2:
            if len(variables):
                categorias_unicas = self.base[variables].nunique()
                variables = list(
                    categorias_unicas.loc[
                        (categorias_unicas <= categoriasMaximas)
                        & (categorias_unicas >= 2)
                    ].index
                )
            if len(colObjs):
                categorias_unicas = tempData.nunique()
                colObjs = list(
                    categorias_unicas.loc[
                        (categorias_unicas <= categoriasMaximas)
                        & (categorias_unicas >= 2)
                    ].index
                )
        else:
            raise ValueError("`CategoriasMaximas` debe ser mayor o igual a 2.")

        # Calcular qué variables tipo object tienen valores únicos menores al
        # 50% (o valor de 'limite') del total de filas del conjunto de datos
        if len(variables):
            variables = list(
                self.base[variables].columns[
                    self.base[variables].nunique()
                    < (self.base.shape[0] * limite)
                ]
            )
        if len(colObjs):
            colObjs = list(
                tempData.columns[
                    tempData.nunique(dropna=False)
                    < (self.base.shape[0] * limite)
                ]
            )

        # Crear el dataframe con la información
        variables += colObjs
        if not len(variables):
            warnings.warn(
                "No hay variables categóricas en el conjunto de datos."
            )
            return pd.DataFrame()
        self._varCategoricas = variables
        lista_counts = []
        for s in variables:
            counts = (
                self.base[s]
                .astype(str)
                .value_counts()
                .drop("<NA>", errors="ignore")
            )
            if isinstance(counts.index[0], dict):
                continue

            # counts=list(counts)
            lista = counts[0:10]
            resto = sum(counts[10 : len(counts)])
            miss = pd.isnull(self.base[s]).sum()

            lista["Demás categorías"] = resto
            lista["Datos faltantes"] = miss

            lista[
                "Total categorías (incluye NA): {0}".format(
                    len(pd.unique(self.base[s]))
                )
            ] = np.nan

            lista = lista.to_frame()
            lista["Columna"] = s
            lista["Porcentaje del total de filas"] = lista[s] / len(self.base)

            resto = lista.iloc[:, 0].loc["Demás categorías"]

            if resto == 0:
                lista = lista.drop("Demás categorías", axis=0)

            lista = lista.reset_index()

            s = lista.columns.tolist()[1]
            colis = ["Columna", "index", s, "Porcentaje del total de filas"]
            lista = lista[colis]
            lista_cols = lista.columns.tolist()
            lista = lista.rename(
                columns={"index": "Valor", lista_cols[2]: "Frecuencia"}
            )
            lista_counts.append(lista)

        if not len(lista_counts):
            warnings.warn(
                "No hay variables categóricas en el conjunto de datos."
            )
            return pd.DataFrame()
        else:
            df_counts = pd.concat(lista_counts, axis=0)

        return df_counts

    # Tamaño del conjunto de datos en la memoria
    def Memoria(self, col=False, unidad="Mb"):
        """
        Calcula el tamaño del conjunto de datos en memoria (megabytes). \
        :ref:`Ver ejemplo <Peso de las variables en la memoria RAM>`

        :param col: Si `False` realiza el cálculo de memoria del Dataframe \
            completo, si `True` realiza el cálculo de memoria por \
            cada columna del Dataframe. Por defecto `False`.
        :type col: bool, opcional
        :param unidad: {"byte", "kb", "Mb", "Gb", "Tb"} Es la unidad de \
            medida de memoria con la que se desea ver la memoria que ocupa \
            en el computador del conjunto  de datos. Por defecto "Mb".
        :type unidad: str, opcional

        :return: (float | pandas.Series) Si `col = False` retorna el valor de \
            memoria ocupada por el conjunto de datos. Si `col = True`, retorna \
            la memoria ocupada por cada columna del conjunto de datos.
        """

        if not isinstance(col, bool):
            raise ValueError("'col' debe ser booleano. {True, False}.")
        if unidad not in ["b", "kb", "Mb", "Gb", "Tb"]:
            raise ValueError(
                "El parámetro 'unidad' debe ser uno de  estos "
                " valores : 'b', 'kb', 'Mb', 'Gb', 'Tb'"
            )

        if col:
            memoria_ = self.base.memory_usage(index=True)
        else:
            memoria_ = self.base.memory_usage(index=True).sum()

        if unidad == "b":
            pass
        elif unidad == "kb":
            memoria_ = memoria_ / (1024)
        elif unidad == "Mb":
            memoria_ = memoria_ / (1024 ** 2)
        elif unidad == "Gb":
            memoria_ = memoria_ / (1024 ** 3)
        elif unidad == "Tb":
            memoria_ = memoria_ / (1024 ** 4)

        return memoria_

    # tabla de resumen pequeña
    def Resumen(
        self,
        filas=True,
        columnas=True,
        colNumericas=True,
        colTexto=True,
        colBooleanas=True,
        colFecha=True,
        colOtro=True,
        filasRepetidas=True,
        columnasRepetidas=True,
        colFaltantes=True,
        colExtremos=True,
        memoriaTotal=True,
    ):
        """
        Retorna una tabla con información general el conjunto de datos.\
        Incluye número de filas y columnas, número de columnas de tipo \
        numéricas, de texto, booleanas, fecha y otros, número de filas y \
        columnas no únicas, número de columnas con más de la mitad de las \
        observaciones con datos faltantes, número de columnas con más del \
        10% de observaciones con datos extremos y el tamaño del conjunto de \
        datos en memoria. :ref:`Ver ejemplo <Tabla de resumen>`

        :param filas: Indica si se incluye el cálculo de número de filas \
            del conjunto de datos. Por defecto `True`.
        :type filas: bool, opcional
        :param columnas: Indica si se incluye el cálculo de número de \
            columnas del conjunto de datos. Por defecto `True`.
        :type columnas: bool, opcional
        :param colNumericas: Indica si se incluye el número de columnas de \
            tipo numéricas. Por defecto `True`.
        :type colNumericas: bool, opcional
        :param colTexto: Indica si se incluye el número de columnas de tipo \
            texto.Por defecto `True`.
        :type colTexto: bool, opcional
        :param colBooleanas:  Indica si se incluye el número de columnas de \
            tipo booleana. Por defecto `True`.
        :type colBooleanas: bool, opcional
        :param colFecha: Indica si se incluye el número de columnas de tipo \
            fecha. Por defecto `True`.
        :type colFecha: bool, opcional
        :param colOtro: Indica si se incluye el número de columnas de otro \
            tipo diferente a los anteriores. Por defecto `True`.
        :type colOtro: bool, opcional
        :param filasRepetidas: Indica si se incluye el número de filas \
            repetidas. Por defecto `True`.
        :type filasRepetidas: bool, opcional
        :param columnasRepetidas: Indica si se incluye el número de \
            columnas repetidas. Por defecto `True`.
        :type columnasRepetidas: bool, opcional
        :param colFaltantes: Indica si se incluye el número de columnas \
            con más de la mitad de las observaciones con datos faltantes. \
            Por defecto `True`.
        :type colFaltantes: bool, opcional
        :param colExtremos: Indica si se incluye el número de columnas con \
            más del 10% de observaciones con datos extremos. Por \
            defecto `True`.
        :type colExtremos: bool, opcional
        :param memoriaTotal: Indica si se incluye el uso del tamaño del \
            conjunto de datos en memoria.Por defecto `True`.
        :type memoriaTotal: bool, opcional
        :return: (pandas.Series) Serie de pandas con las estadísticas \
            descriptivas del conjunto de datos.
        """

        # Lista donde se guardarán resultados
        lista_resumen = [[], []]

        # Calcular tipo de columnas
        col_tipos = self.TipoColumnas(
            tipoGeneral=True, tipoGeneralPython=False, tipoEspecifico=False
        )

        # Agregar a lista, si se escoge que sea así

        # Número de filas
        if filas:
            calculo = self.base.shape[0]
            nombre = "Número de filas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Número de columnas
        if columnas:
            calculo = self.base.shape[1]
            nombre = "Número de columnas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Número de columnas numéricas
        if colNumericas:
            calculo = int((col_tipos == "Numérico").sum())
            nombre = "Columnas numéricas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Número de columnas de texto
        if colTexto:
            calculo = int((col_tipos == "Texto").sum())
            nombre = "Columnas de texto"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Número de columnas booleanas
        if colBooleanas:
            calculo = int((col_tipos == "Booleano").sum())
            nombre = "Columnas booleanas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Número de columnas de fecha
        if colFecha:
            calculo = int((col_tipos == "Fecha").sum())
            nombre = "Columnas de fecha"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Número de columnas de otro tipo
        if colOtro:
            calculo = int((col_tipos == "Otro").sum())
            nombre = "Otro tipo de columnas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Número de filas no únicas
        if filasRepetidas:
            calculo = self.CantidadDuplicados(eje=0, numero=True)
            nombre = "Número de filas repetidas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Número de columnas no únicas
        if columnasRepetidas:
            calculo = self.CantidadDuplicados(eje=1, numero=True)
            nombre = "Número de columnas repetidas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Porcentaje de columnas con más de la mitad de datos faltantes
        if colFaltantes:
            col_missing = self.ValoresFaltantes(numero=False)
            calculo = len(col_missing[col_missing > 0.5])
            nombre = "Columnas con más de la mitad de datos faltantes"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)

        # Columnas con más del 10% de datos como extremos
        if colExtremos:
            col_porc = self.ValoresExtremos(extremos="ambos", numero=False)
            try:
                calculo = len(col_porc[col_porc > 0.1])
                nombre = "Columnas con más del 10% de datos como extremos"
                lista_resumen[0].append(nombre)
                lista_resumen[1].append(calculo)
            except BaseException:
                pass

        # Tamaño del conjunto de datos en la memoria
        if memoriaTotal:
            memoria_tot = self.Memoria(unidad="b")
            name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(memoria_tot, 1024)))
            p = math.pow(1024, i)
            name = name[i]
            memoria_tot = round(memoria_tot / p, 2)
            nombre = f"Uso de memoria del conjunto de datos en {name} (aprox)"

            lista_resumen[0].append(nombre)
            lista_resumen[1].append(memoria_tot)

        tabla_resumen = pd.Series(
            data=lista_resumen[1], index=lista_resumen[0]
        ).astype(int)

        return tabla_resumen

    # Matrices de correlación para las variables numéricas
    def CorrelacionNumericas(self, metodo="pearson", variables=None):
        """
        Genera una matriz de correlación entre las variables de tipo numérico \
        :ref:`Ver ejemplo <Correlación entre variables numéricas>`.

        :param metodo: {'pearson', 'kendall', 'spearman'} Medida de \
            correlación. Por defecto "pearson".
        :type metodo: str, opcional
        :param variables: Lista de nombres de las columnas númericas \
            separados por comas. Permite seleccionar las columnas de interés. \
            Por defecto `None`.
        :type variables: [type], opcional
        :return: (pandas.DataFrame) Dataframe con las correlaciones de las \
            columnas de tipo numérico analizadas.
        """

        if metodo not in ["spearman", "kendall", "pearson"]:
            raise ValueError(
                "'metodo' es invalido. Seleccione 'spearman', "
                "'kendall' o 'pearson' en su lugar."
            )
        # Revisar si hay columnas numéricas.
        col_num = self.base.select_dtypes(include=np.number).columns.tolist()
        if not len(col_num):
            warnings.warn("El conjunto de datos no tiene columnas numéricas")
            return None

        # Crear lista de númericas filtradas por las variables escogidas
        if isinstance(variables, list):
            col_num = [q for q in variables if q in col_num]
            if not len(col_num):
                raise ValueError(
                    "El parámetro `variables` no contiene ningún nombre "
                    "de columna númerica valido."
                )

        # Crear la matriz de correlación dependiendo del método escogido
        if metodo == "pearson":
            correlacion_ = self.base[col_num].corr(method="pearson")
        elif metodo == "kendall":
            correlacion_ = self.base[col_num].corr(method="kendall")
        elif metodo == "spearman":
            correlacion_ = self.base[col_num].corr(method="spearman")

        return correlacion_

    # Matrices de correlación para variables categóricas
    def CorrelacionCategoricas(
        self, metodo="phik", limite=0.5, categoriasMaximas=30, variables=None
    ):
        """
        Genera una matriz de correlación entre las variables de tipo \
        categóricas. \
        :ref:`Ver ejemplo <Correlación de variables categóricas>`

        :param metodo: Medida de correlación a utilizar. \
            Por defecto  `phik`.
        :type metodo: str, opcional
        :param limite: (valor de 0 a 1) Límite de referencia, se \
            utiliza para determinar si las variables posiblemente son de tipo \
            categóricas y ser incluidas en el análisis. Si el número de \
            valores únicos por columna es mayor al número de registros \
            limite, se considera que la variable no es categórica. \
            Por defecto  `0.5`.
        :type limite: float, opcional
        :param categoriasMaximas: (valor mayor o igual a 2), indica el máximo \
            número de categorías de una variable para que sea incluida en el \
            análisis. Por defecto  `30`.
        :type categoriasMaximas: int, opcional
        :param variables: Lista de nombres de las columnas categóricas \
            separados por comas. Permite escoger las columnas de interés \
            dentro del conjunto de datos. Por defecto  `None`.
        :type variables: [type], opcional
        :return: (pandas.DataFrame) Dataframe con las correlaciones de las \
            columnas de tipo categóricas.
        """

        if metodo not in ["cramer", "phik"]:
            raise ValueError(
                "'metodo' no se reconoce. Seleccione 'cramer' "
                "o 'phik en su lugar."
            )

        _ = self.DescripcionCategoricas(
            categoriasMaximas=categoriasMaximas,
            variables=variables,
            limite=limite,
        )
        varCat = self._varCategoricas
        data = self.base[varCat].astype(str)
        # Hacer doble loop para crear matriz de correlation tipo Cramer V
        if metodo == "cramer":
            lista_matriz = [
                self.correlacion_cramerv(data[var1], data[var2])
                for var1 in varCat
                for var2 in varCat
            ]

            if len(lista_matriz) > 0:

                lista_matriz = [
                    lista_matriz[i : i + len(varCat)]
                    for i in range(0, len(lista_matriz), len(varCat))
                ]
                lista_matriz = pd.DataFrame(
                    lista_matriz, columns=varCat, index=varCat
                )
                correlacion_final = lista_matriz
            else:
                correlacion_final = pd.DataFrame()
        # Matriz de correlación con la metodología 'phik'
        else:  # "phik"
            correlacion_final = data.phik_matrix()

        return correlacion_final

    def correlacion_cramerv(self, x, y):
        """
        Función de soporte para calcular coeficiente de correlación Cramer V \
        (para usar en la función de las matrices de correlación entre \
        variables categóricas).

        :param x: Variable categorica 1.
        :type x: pandas.Series | list
        :param y: Variable categorica 2.
        :type y: pandas.Series | list
        :return: (float) Correlación de cramer V entre x y y
        """
        confusion_matrix = pd.crosstab(x, y)
        chi2 = sstats.chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum().sum()
        phi2 = chi2 / n
        r, k = confusion_matrix.shape
        phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
        rcorr = r - ((r - 1) ** 2) / (n - 1)
        kcorr = k - ((k - 1) ** 2) / (n - 1)
        return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

    def __read_excel(self, datos):
        warnings.warn(
            "Cargar archivos xlsx puede tomar demasiado tiempo, se aconseja "
            "fuertemente convertirlos a archivo csv, esto puede mejorar hasta "
            f"100x veces la velocidad de carga del archivo {datos}"
        )
        try:
            wb = openpyxl.load_workbook(
                datos,
                read_only=True,
                data_only=True,
                keep_links=False,
                keep_vba=False,
            )
        except Exception:
            raise NotImplementedError(
                "LEILA no soporta los archivos con el antiguo formato .xls, "
                "por favor convierta el archivo al formato xlsx o csv."
            )
        ws = wb.active
        data = ws.values
        cols = next(data)
        self._base = pd.DataFrame(list(data), columns=cols)

    def __read_csv(self, datos, **kwargs):
        kwtemp = kwargs.copy()
        kwtemp.pop("nrows", None)
        temp = pd.read_csv(datos, nrows=100, **kwtemp)
        # cols que pueden contener fecha
        col_objs = list(temp.select_dtypes(object))
        self._base = pd.read_csv(datos, parse_dates=col_objs, **kwargs)

    def __from_leila(self, datos):
        self._base = datos.datos
        self._metadatos = datos.metadatos()

    def __get_source(self, datos):
        if isinstance(datos, str):
            tipo = datos.split(".")[-1]
            if tipo == "csv":
                self.__source = "csv"
            elif tipo in ["xlsx", "xls", "xlsm"]:
                self.__source = "excel"
            else:
                raise NotImplementedError(
                    f"Los archivos con formato {tipo} no son soportados por "
                    "LEILA. Intente con archivos xlsx, xls, csv"
                )
        elif isinstance(datos, pd.DataFrame):
            self.__source = "pandas"
        elif isinstance(datos, DatosGov):
            self.__source = "leila"
        else:
            raise NotImplementedError(
                f"El tipo de datos {type(datos)} no está soportado por LEILA."
            )



class indice_calidad:
    """
    Constructor por defecto de la clase leila.indice_calidad. Esta clase se \
    encarga de generar el índice de calidad de conjuntos de datos del Portal \
    de Datos Abiertos de Colombia y sus subindicadores. 

    El insumo principal para generar el índice de calidad de un conjunto de datos \
    es su código API del Portal de Datos Abiertos. 

    :param api_id: código API del conjunto de datos del Portal de Datos Abiertos. Es \
        un string de nueve caracteres único para cada conjunto
    :type api_id: str
    :param numero_filas: es el número de filas que se utilizan para calcular los \
        duplicados de columnas en el método 'duplicados_columnas'
    :type numero_filas: int

    """ 

    def __init__(
            self,
            api_id = "",
            numero_filas = 30000
            ):
        self.numero_filas = numero_filas
        dominio = "https://www.datos.gov.co/"
        # Datos
        try:
            url = dominio + "resource/{0}.csv".format(api_id)
            self.base = pd.read_csv(url)
            
        except:
            self.base = None
            print("No es posible descargar los datos del conjunto de datos con número API {0}".format(api_id))            
        try:
            url = dominio + "api/views/" + api_id + ".json"
            self.metadatos = dict(requests.get(url).json())
        except:
            self.metadatos = None
            print("No es posible extraer los metadatos del conjunto de datos con número API {0}".format(api_id))
        
    ## Valores faltantes
    # Valores faltantes de todo el dataframe
    def faltantes(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Calcula \
        el porcentaje de celdas faltantes dentro del conjunto de datos y lo divide por el total de celdas y \
        resta el resultado al número 1
        :return: (float) Subindicador de calidad de datos faltantes
        """
        if self.base.shape[0] == 0 or self.base.shape[1] == 0:
            indicador = 0
        else:
            indicador = 1 - (pd.isnull(self.base).sum().sum() / (self.base.shape[0] * self.base.shape[1]))
        return indicador
    
    # Tamaño de las filas
    def tamano_filas(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        el conjunto de datos tiene una cantidad mínima de filas. Revisa si el número de filas del conjunto de \
        datos es menor o no a 50 y, en caso de ser 50 o más, el índice será 1. En caso de ser menor a 50, el \
        subindicador será el número de filas del conjunto dividio por 50
        
        :return: (float) Subindicador de calidad del tamaño de las filas
        """
        if self.base.shape[0] < 50:
            indicador = self.base.shape[0] / 50 
        else:
            indicador = 1
        return indicador
    
    # Tamaño de las columnas
    def tamano_columnas(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica \
        que el conjunto de datos tenga una cantidad mínima de columnas. En caso de tener 3 o más columnas, el \
        subindicador será igual a 1. En caso de tener menos de 3 columnas, será el número de columnas divido \
        por 3

        :return: (float) Subindicador del tamaño de las columnas
        """        
        if self.base.shape[1] < 3:
            indicador = self.base.shape[1] / 3
        else:
            indicador = 1
        return indicador
    
    # Duplicados de filas
    def duplicados_filas(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Calcula \
        la cantidad de filas duplicadas, las divide por el total de filas y luego resta este porcentaje al \
        número 1

        :return: (float) Subindicador de duplicados de filas
        """
        if self.base.shape[0] == 0 or self.base.shape[1] == 0:
            indicador = 0
        else:
            indicador = 1 - (self.base.applymap(str).duplicated(keep = "first").sum() / self.base.shape[0])
        return indicador
    
    # Duplicados de columnas (REVISAR DAVID)
    def duplicados_columnas(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Calcula \
        el número de columnas duplicadas, lo divide por el total de columnas y luego resta este porcentaje \
        al número 1. En caso de tener un valor mayor o igual al parámetro 'numero_filas' (por defecto es 30.000), \
        el algoritmo utiliza únicamente el número de filas igual a 'numero_filas' en los cálculos de duplicados

        :return: (float) Subindicador de duplicados columnas     
        """
        if self.base.shape[0] == 0 or self.base.shape[1] == 0:
            indicador = 0
        elif self.base.shape[0] > 0 and self.base.shape[1] > 0 and self.numero_filas < 30000:
            indicador = 1 - (self.base.applymap(str).T.duplicated(keep = "first").sum() / self.base.shape[1])
        else:
            numero_filas_tercio = self.numero_filas // 3
            base_mitad = self.base.shape[0] // 2
            mini_base = pd.concat([self.base.iloc[0: numero_filas_tercio], self.base.iloc[base_mitad: base_mitad + numero_filas_tercio], self.base.iloc[-numero_filas_tercio:]])
            indicador = 1 - (mini_base.applymap(str).T.duplicated(keep = "first").sum() / self.base.shape[1])
        return indicador
    
    # Más de un valor único por columna
    def valores_unicos(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        hay columnas que contienen el mismo valor en todos sus campos. El subindicador es igual al número 1 restado \
        por el porcentaje de columnas que contienen el mismo valor en cada celda

        :return: (float) Subindicador valores únicos en columnas
        """
        if self.base.shape[0] == 0:
            indicador = 0
        else:
            unicos = self.base.applymap(str).nunique()
            indicador = 1 - (len(unicos[unicos == 1]) / self.base.shape[1])
        return indicador
    
    # Tipos de observaciones en cada columna
    def tipos_columnas_unicos(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica \
        si hay columnas que contienen tipos de datos distintos, que no deberían estar en la misma columna. Por \
        ejemplo, si una columna contiene al mismo tiempo valores string y numéricos. El subindicador es igual \
        al número 1 restado por el porcentaje de columnas con más de 1 valor en sus celdas

        :return: (float) Subindicador tipos de celdas únicos en columnas
        """
        if self.base.shape[1] == 0:
            indicador = 0
        else:
            tipos_mal = []
            for s in self.base.columns:  
                tip = self.base[s].fillna("nan").apply(
                    lambda x: x if x == "nan" else type(x)).value_counts(
                    normalize=True, dropna=False).drop("nan", errors = "ignore")
                if len(tip) > 1:
                    tipos_mal.append(tip)
                else:
                    pass
                indicador = 1 - (len(tipos_mal) / self.base.shape[1])
        return indicador
    
    # Actualización de conjunto de datos
    def retardo_actualizacion(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si 
        el conjunto de datos se encuentra actualizado o no según la información de los metadatos. El valor es 1 \
        si está actualizado y 0 de lo contrario

        :return: (float) Subindicador de actualización de conjunto de datos
        """
        # Freuencia de actualización
        try:
            frecuencia_actualizacion = self.metadatos["metadata"]["custom_fields"]["Información de Datos"]["Frecuencia de Actualización"].lower()
        except:
            frecuencia_actualizacion = None
        
        dic_frecuencias = {
            "diaria": 1,
            "semanal": 7,
            "quincenal": 15, 
            "mensual": 31, 
            "trimestral": 92, 
            "cuatrimestral": 31 * 4,
            "semestral": 182, 
            "anual": 366,
            "trieno": 365 * 3, 
            }
        
        if frecuencia_actualizacion == "no aplica" or frecuencia_actualizacion == "nunca":
            return 1
        
        if frecuencia_actualizacion not in dic_frecuencias:
            print("No se puede calcular la actualización del conjunto de datos porque no está disponible la frecuencia de actualización")
            return 0
     
        dias = dic_frecuencias[frecuencia_actualizacion]

        fecha_act_num = self.metadatos["rowsUpdatedAt"]
        fecha_hoy_num = datetime.datetime.now().timestamp()
        
        # diferencia_fechas = (fecha_hoy_num - fecha_act_num) / 60 / 60 / 24
        diferencia_fechas = (datetime.datetime.fromtimestamp(fecha_hoy_num) - datetime.datetime.fromtimestamp(fecha_act_num)).days
    
        # Fecha de actualización
        try:
            fecha_actualizacion = datetime.datetime.fromtimestamp(self.metadatos["rowsUpdatedAt"])
        except:
            fecha_actualizacion = None
        
        if diferencia_fechas >= dias:
            print("El conjunto de datos no se encuentra actualizado porque la última actualización fue el {0} y debe ser actualizado de manera {1}".format(fecha_actualizacion, frecuencia_actualizacion))        
            indicador = 0
        else:
            print("El conjunto de datos se encuentra actualizado")
            indicador = 1
        
        return indicador
    
    # Trazabilidad_creacion
    def trazabilidad_creacion(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        se encuentran los campos de la fecha de creación y la fecha de publicación del conjunto de datos en los \
        metadatos

        :return: (float) Subindicador de trazabilidad de creación 
        """
        # Definir variables
        try:
            fecha_creacion = datetime.datetime.fromtimestamp(self.metadatos["createdAt"])
        except:
            fecha_creacion = None   
        try:
            fecha_publicacion = datetime.datetime.fromtimestamp(self.metadatos["publicationDate"])
        except:
            fecha_publicacion = None

        indicador = 0
        
        if fecha_creacion is not None:
            indicador = indicador + 0.5
        else: 
            pass
            
        if fecha_publicacion is not None:
            indicador = indicador + 0.5
        else:
            pass
        
        return indicador
    
    # Trazabilidad publicacion
    def trazabilidad_actualizacion(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        se encuentran los campos de la frecuencia de actualización y la fecha de la última actualización en los \
        metadatos

        :return: (float) Subindicador de trazabilidad de actualización 
        """
        # Definir variables
        try:
            fecha_actualizacion = datetime.datetime.fromtimestamp(self.metadatos["rowsUpdatedAt"])
        except:
            fecha_actualizacion = None
        
        # Freuencia de actualización
        try:
            frecuencia_actualizacion = self.metadatos["metadata"]["custom_fields"]["Información de Datos"]["Frecuencia de Actualización"]
        except:
            frecuencia_actualizacion = None
            
        indicador = 0
        if fecha_actualizacion is not None:
            indicador = indicador + 0.5
        else: 
            pass
            
        if frecuencia_actualizacion is not None:
            indicador = indicador + 0.5
        else:
            pass
        
        return indicador
    
    # Trazabilidad_contacto
    def trazabilidad_contacto(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        se encuentra el campo del nombre del dueño del conjunto de datos en los metadatos

        :return: (float) Subindicador de trazabilidad de contacto 
        """
        # Definir variables
        submitador = self.metadatos["approvals"][0]["submitter"]
        try: 
            nombre_contacto = submitador["displayName"]
        except:
            nombre_contacto = None

        indicador = 0
        if nombre_contacto is not None:
            indicador = indicador + 1
        else:
            pass

        return indicador
    
    # Trazabilidad título y descripción
    def trazabilidad_descripcion(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        se encuentran los campos del título y la descripción en los metadatos. Adicionalmente, castiga los metadatos \
        que contienen el título y descripción muy similares, que no contengan un mínimo de caracteres adecuado y que \
        no contengan letras

        :return: (float) Subindicador de trazabilidad de descripción 
        """
        # Definir variables
        try:
            titulo = self.metadatos["name"]
        except:
            titulo = None
        try:
            descripcion = self.metadatos["description"]
        except:
            descripcion = None
                    
        # Calcular similitud con SequenceMatcher
        try:
            similitud = SequenceMatcher(None, titulo.lower(), descripcion.lower()).ratio()
        except:
            similitud = 0
        
        # Revisar si hay al menos una letra en el título
        if titulo is not None:
            if any(c.isalpha() for c in titulo):
               titulo_letra = True
            else:
                titulo_letra = False
        else:
            titulo_letra = False
                
        # Revisar si hay al menos una letra en la descripción
        if descripcion is not None:
            if any(c.isalpha() for c in descripcion):
               descripcion_letra = True
            else:
                descripcion_letra = False
        else:
            descripcion_letra = False

        indicador = 0
        if titulo is not None and titulo_letra == True and len(titulo) > 20:
            indicador = indicador + 0.5
        else:
            pass
        if descripcion is not None and descripcion_letra == True and similitud < 0.5 and len(descripcion) > 60:
            indicador = indicador + 0.5
        else:
            pass
        
        return indicador    

    # Nombres de las columnas
    def nombres_columnas(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        el nombre de cada columna aparece en los metadatos

        :return: (float) Subindicador de nombres de columnas 
        """
        lista_nombres_cols = [q["name"] for q in self.metadatos["columns"]]
        indicador = 0
        for s in lista_nombres_cols:
            if s == "":
                pass
            else:
                indicador = indicador + 1
        return indicador / len(self.metadatos["columns"])    

    # Descripción de las columnas
    # Verificar si lo que está escrito está en español y tiene sentido (no puntuación)
    def descripcion_columnas(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        cada columna tiene su descripción en los metadatos

        :return: (float) Subindicador de descripción de columnas
        """
        try:
            lista_descr_cols = [q["description"] for q in self.metadatos["columns"]]
        except:
            return 0
        indicador = 0
        for s in lista_descr_cols:
            if s == "":
                pass
            else:
                indicador = indicador + 1
        return indicador / len(self.metadatos["columns"])

    # Tipos de columnas
    def tipos_columnas_meta(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        existe el campo que indica el tipo de cada columna en los metadatos

        :return: (float) Subindicador tipos de columnas
        """
        # Definir variables
        lista_tipos_meta = [q["renderTypeName"] for q in self.metadatos["columns"]]
        
        indicador = 0
        for s in lista_tipos_meta:
            if s == "":
                pass
            else:
                indicador = indicador + 1
        return indicador / len(self.metadatos["columns"])

    # Tamaño de conjunto igual en metadatos y en datos
    def tamano_comparacion(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        el número de filas y columnas del conjunto de datos es igual al número de filas y columnas reportado en los \
        metadatos

        :return: (float) Subindicador comparación de tamaño en datos y metadatos
        """
        # Defnición de variables
        try:
            cached_contents = self.metadatos["columns"][0]["cachedContents"]
        except:
            pass
        try:
            numero_filas = int(cached_contents["non_null"]) + int(cached_contents["null"])
        except:
            numero_filas = None
        try:
            numero_columnas = len(self.metadatos["columns"])
        except:
            numero_columnas = None


        fil_datos = self.base.shape[0]
        col_datos = self.base.shape[1]
        
        indicador = 0
        
        if fil_datos == numero_filas:
            indicador = indicador + 0.5
        else:
            pass
        
        if col_datos == numero_columnas:
            indicador = indicador + 0.5
        else:
            pass
        
        return indicador

    # Tipos de columnas son los que son
    def verificar_meta_cols(self):
        """
        Subindicador que varía entre 0 y 1, donde 1 representa la mejor calidad y 0 la peor calidad. Verifica si \
        cada columna del conjunto de datos tiene el mismo tipo indicado en los metadatos

        :return: (float) Subindicador de verificación de tipos de columnas
        """
        if self.base.shape[1] == 0:
            resultado = 0
        else:
            lista_tipos_meta = [q["renderTypeName"] for q in self.metadatos["columns"]]
            lista_tipos_datos = self.base.columns
            
            if len(lista_tipos_datos) != len(lista_tipos_meta):
                resultado = 0
            else:
                indicador = 0
                
                for i in range(len(lista_tipos_meta)):
                    columna = lista_tipos_datos[i]
                    m = self.base[columna].mode().iloc[0]
                            
                    if lista_tipos_meta[i] == "number":
                        try:
                            int(m)
                            indicador = indicador + 1
                        except:
                            try:
                                float(m)
                                indicador = indicador + 1
                            except:
                                pass
                    elif lista_tipos_meta[i] == "calendar_date":
                        try:
                            parse(m, fuzzy = False)
                            indicador = indicador + 1
                        except:
                                pass
                    elif lista_tipos_meta[i] == "checkbox":
                        if str(m) == "True" or str(m) == "False":
                            indicador = indicador + 1
                        else:
                            pass
                    elif lista_tipos_meta[i] == "text":
                        if isinstance(m, str) == True:
                            indicador = indicador + 1
                        else:
                            pass
                    else:
                        pass
                    
                resultado = indicador / len(lista_tipos_meta)
        
        return resultado
    
    def indice(self, datos = True, meta = True, subindicadores = False, numero_filas = 30000, dic_pesos_meta = None, dic_pesos_datos = None):
        """
        Método para calcular el índice de calidad y sus subindicadores para un conjunto de datos del Portal de Datos Abiertos. 

        :param datos: si es True incluye información de la calidad de los datos en los resultados. De lo contrario no calcula \
            la calidad de los datos y sí de los metadatos. Al menos uno de los parámetros, 'datos' o 'meta', tiene que tener el valor True \
            para poder generar resultados
        :type datos: bool
        :param meta: si es True incluye información de la calidad de los metadatos en los resultados. De lo contrario no calcula \
            la calidad de los metadatos y sí de los datos. Al menos uno de los parámetros, 'datos' o 'meta', tiene que tener el valor True \
            para poder generar resultados
        :type meta: bool
        :param subindicadores: si es True se calculan todos los subindicadores de los indicadores de datos y metadatos
        :type subindicadores: bool
        :numero_filas: es el número de filas que se utilizan para calcular los \
            duplicados de columnas en el método 'duplicados_columnas'
        :type numero_filas:int
        :dic_pesos_meta: diccionario de Python opcional donde un usuario define los pesos que desea para cada subindicador de \
            los metadatos. Las llaves del diccionario son los números de 1 a 10, representan cada subindicador, y los valores \
            son los pesos de cada subindicador, los cuales ttienen que sumar 1. 
        :type dic_pesos_meta: dict
        :dic_pesos_datos: diccionario de Python opcional donde un usuario define los pesos que desea para cada subindicador de \
            los datos. Las llaves del diccionario son los números de 1 a 7, representan cada subindicador, y los valores \
            son los pesos de cada subindicador, los cuales ttienen que sumar 1. 
        :type dic_pesos_datos: dict 
        :return: (dict) con índice y subíndices de calidad, si el parámetro 'subindicadores' es False.
                 (tuple) con diccionarios de índices y subíndices y de subindicadores si el parámetro 'subindicadores' es True
        """
        if meta == True:
            if self.metadatos is not None and dic_pesos_meta is None:
                dic_meta = {
                    1: self.trazabilidad_descripcion(),
                    2: self.descripcion_columnas(),
                    3: self.nombres_columnas(),
                    4: self.retardo_actualizacion(),
                    5: self.trazabilidad_actualizacion(),
                    6: self.tipos_columnas_meta(),
                    7: self.verificar_meta_cols(),
                    8: self.trazabilidad_creacion(), 
                    9: self.trazabilidad_contacto(),
                    10: self.tamano_comparacion()
                    }
                print(dic_meta)
            elif self.metadatos is None and dic_pesos_meta is None:
                dic_meta = {
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0,
                    6: 0,
                    7: 0,
                    8: 0,
                    9: 0, 
                    10: 0,
                    }  
            
            else:
                dic_meta = {
                    1: self.trazabilidad_descripcion(),
                    2: self.descripcion_columnas(),
                    3: self.nombres_columnas(),
                    4: self.retardo_actualizacion(),
                    5: self.trazabilidad_actualizacion(),
                    6: self.tipos_columnas_meta(),
                    7: self.verificar_meta_cols(),
                    8: self.trazabilidad_creacion(), 
                    9: self.trazabilidad_contacto(),
                    10: self.tamano_comparacion()
                    }
                
                pesos_meta = dic_pesos_meta.copy()
                indice_meta = 0
                for i in range(1, len(pesos_meta) + 1):
                # print(dic_meta[i], pesos_meta[i - 1])
                    indice_meta = indice_meta + dic_meta[i] * pesos_meta[i]      
                
            #### Índice de calidad estándar para metadatos
            if dic_pesos_meta is None:
                n_meta = len(dic_meta)
    
                ##### Suma reciprocal para metadatos
                jota_meta = sum([1 / q for q in range(1, n_meta +1)])
                
                # metadatos
                pesos_meta = []
                for i in range(1, n_meta + 1):
                    peso = (1 / i) / (jota_meta)
                    pesos_meta.append(peso)
    
                # Índice de calidad metadatos
                indice_meta = 0
                for i in range(1, n_meta + 1):
                # print(dic_meta[i], pesos_meta[i - 1])
                    indice_meta = indice_meta + dic_meta[i] * pesos_meta[i - 1]
                ##
                lista_nombres_meta = ['trazabilidad_descripcion', 'descripcion_columnas', 
                                      'nombres_columnas', 'retardo_actualizacion', 
                                      'trazabilidad_actualizacion', 
                                      'tipos_columnas_meta', 'verificar_meta_cols', 
                                      'trazabilidad_creacion', 'trazabilidad_contacto', 
                                      'tamano_comparacion']
    
                for i in range(1, n_meta + 1):
                    s = lista_nombres_meta[i - 1]
                    dic_meta[s] = dic_meta.pop(i)
                    
            else:
                lista_nombres_meta = ['trazabilidad_descripcion', 'descripcion_columnas', 
                        'nombres_columnas', 'retardo_actualizacion', 
                        'trazabilidad_actualizacion', 
                        'tipos_columnas_meta', 'verificar_meta_cols', 
                        'trazabilidad_creacion', 'trazabilidad_contacto', 
                        'tamano_comparacion']
    
                for i in range(1, len(dic_meta) + 1):
                    s = lista_nombres_meta[i - 1]
                    dic_meta[s] = dic_meta.pop(i)
        else:
            pass
                        
        ##
        if datos == True:
            if self.base is not None and dic_pesos_datos is None:
                dic_datos = {
                    1: self.faltantes(),
                    2: self.tamano_columnas(),
                    3: self.tamano_filas(),
                    4: self.duplicados_filas(),
                    5: self.duplicados_columnas(),                    
                    6: self.tipos_columnas_unicos(),
                    7: self.valores_unicos()
                    }
            elif self.base is None and dic_pesos_datos is None:
                dic_datos = {
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0,
                    6: 0,
                    7: 0
                    }
                
            else:
                dic_datos = {
                        1: self.faltantes(),
                        2: self.tamano_columnas(),
                        3: self.tamano_filas(),
                        4: self.duplicados_filas(),
                        5: self.duplicados_columnas(),
                        6: self.tipos_columnas_unicos(),
                        7: self.valores_unicos()
                        }
                pesos_datos = dic_pesos_datos.copy()
                indice_datos = 0
                for i in range(1, len(pesos_datos) + 1):
                    indice_datos = indice_datos + dic_datos[i] * pesos_datos[i]     
                       
            #### Índice de calidad estándar para datos 
            if dic_pesos_datos is None:
                n_datos = len(dic_datos)
    
                ##### Suma ranking para métricas de datos
                jota_datos = sum([q for q in range(1, n_datos +1)])
                           
                # datos
                pesos_datos = []
                for i in range(1, n_datos + 1):
                    peso = (n_datos + 1 - i) / (jota_datos)
                    pesos_datos.append(peso)
                    
                #### ïndices de calidad
                # Índice de calidad datos
                indice_datos = 0
                for i in range(1, n_datos + 1):
                    indice_datos = indice_datos + dic_datos[i] * pesos_datos[i - 1]
                
                lista_nombres_datos = ['faltantes', 'tamano_columnas', 'tamano_filas', 
                                       'duplicados_filas', 'duplicados_columnas', 
                                       'tipos_columnas_unicos', 'valores_unicos']
                
                for i in range(1, n_datos + 1):
                    s = lista_nombres_datos[i - 1]
                    dic_datos[s] = dic_datos.pop(i)
        
            else:
                lista_nombres_datos = ['faltantes', 'tamano_columnas', 'tamano_filas', 
                                       'duplicados_filas', 'duplicados_columnas', 
                                       'tipos_columnas_unicos', 'valores_unicos']
    
                for i in range(1, len(dic_datos) + 1):
                    s = lista_nombres_datos[i - 1]
                    dic_datos[s] = dic_datos.pop(i)
        else:
            pass

        ####
        if datos == True and meta == True:
            indice_final = 0.5 * indice_meta + 0.5 * indice_datos
        
            dic_indices = {"indice": indice_final,
                    "indice_metadatos": indice_meta, 
                    "indice_datos": indice_datos
                    }
            if subindicadores:
                return dic_indices, dic_meta, dic_datos
            else:
                return dic_indices
    
        elif datos == True and meta == False:
            indice_final = indice_datos
            dic_indices = {"indice": indice_final,
                    "indice_datos": indice_datos
                    }
            if subindicadores:
                return dic_indices, dic_datos
            else:
                return dic_indices
        
        elif datos == False and meta == True:
            indice_final = indice_meta
            dic_indices = {"indice": indice_final,
                    "indice_datos": indice_meta
                    }
            if subindicadores:
                return dic_indices, dic_meta
            else:
                return dic_indices
        
        else:
            print("Es necesario asignar el valor True a al menos uno de los siguientes parámetros: 'datos', 'meta'")