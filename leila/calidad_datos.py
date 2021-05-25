# -*- coding: utf-8 -*-

from numpy.core.fromnumeric import var
import pandas as pd
import numpy as np
import scipy.stats as sstats
import warnings
import re
import phik


class CalidadDatos:
    def __init__(
        self,
        datos,
        castNumero=False,
        castDatos=True,
        diccionarioCast=None,
        errores="ignore",
        formato_fecha="%d/%m/%Y",
    ):
        """
        Constructor por defecto de la clase CalidadDatos. Esta clase se \
        encarga de manejar todas las funciones asociadas a la medición de la \
        calidad de los datos en una base de datos estructurada.

        :param datos: (Dataframe) Base de datos de tipo pandas.DataFrame que \
            será analizada por la clase `CalidadDatos`.
        :param castNumero: (bool) {True, False}. Valor por defecto: False \
            Indica si se desea convertir las columnas de tipos object y \
            bool a float, de ser posible.
        :param castDatos: (bool) {True, False}. Valor por defecto: True. \
            Indica si se desean convertir las columnas al mejor tipo de datos \
            para cada columna según la función `convert_dtypes` de Pandas. \
            Por ejemplo si una columna es de tipo string, pero sus datos son \
            en su mayoría números, se convierte a columna númerica. \
            `castNumero` debe ser `False`.
        :param diccionarioCast: (dict) { {nombre_columna : tipo_columna} }. \
            Valor por defecto None. Diccionario donde se especifican los \
            tipos de datos a los que se desean convertir las columnas dentro \
            del diccionario, por ejemplo, {'col1': 'booleano', \
            'edad':'numerico'}, donde `col1` y `edad` son columnas de la base \
            de datos. Los valores a los que se pueden convertir son: \
            ['string', 'numerico', 'booleano', 'fecha', 'categorico'].
        :param errores: (string) {'ignore', 'coerce', 'raise'}\
            Valor por defecto: 'ignore'. Indica qué hacer con las columnas \
            cuyo tipo no se puede cambiar al solicitado en 'diccionarioCast'.
        :param formato_fecha: (string) Valor de defecto: "%d/%m/%Y". Formato \
            string para el cast de las variables tipo fecha.
            Para más informacion sobre las opciones de strings, consulte: \
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        :return: Objeto del tipo de la clase `CalidadDatos`.
        """
        self._dic_tipo = {
            "int": "Numérico",
            "float": "Numérico",
            "str": "Texto",
            "bool": "Booleano",
            "date": "Fecha",
            "object": "Otro",
        }
        self._castNum = castNumero
        self._castDatos = castDatos
        self._castdic = diccionarioCast
        self._errores = errores
        self._strdate = formato_fecha
        self.base = datos.copy()

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, datos):
        if not isinstance(self._castNum, bool):
            raise ValueError("'castNumero' debe ser de tipo booleano (bool).")
        if not isinstance(self._castdic, (dict, type(None))):
            raise ValueError(
                "'diccionarioCast' debe ser de tipo diccionario (dict)."
            )
        if not isinstance(self._castNum, bool):
            raise ValueError("'castDatos' debe ser de tipo booleano (bool).")

        if self._castNum:
            self._base = datos.fillna(np.nan).convert_dtypes(
                infer_objects=False,
                convert_boolean=False,
            )
            warnings.warn(
                "En futuras versiones, el párametro castNumero será "
                "eliminado. En su lugar use castDatos=True",
                FutureWarning,
            )
        elif self._castDatos:
            self._base = datos.fillna(np.nan).convert_dtypes()
        else:
            self._base = datos.fillna(np.nan).convert_dtypes(
                infer_objects=False,
                convert_string=True,
                convert_integer=False,
                convert_boolean=False,
                convert_floating=False,
            )

        if self._castdic:
            for col, tipo in self._castdic.items():
                if tipo == "string":
                    self._base[col] = self.base[col].apply(lambda x: str(x))
                elif tipo == "numerico":
                    self._base[col] = pd.to_numeric(
                        self._base[col], errors=self._errores
                    )
                elif tipo == "booleano":
                    self._base[col] = self.base[col].astype("bool")
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

        # Tipo más común de cada columna
        tipo_mas_comun = [
            re.findall("'(.*)'", str(type(datos[col][0])))[0]
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
        :ref:`Ver ejemplo <calidad_datos.TipoColumnas>`

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
        Calcula la cantidad de valores únicos de cada columna del dataframe. \
        :ref:`Ver ejemplo <calidad_datos.ValoresUnicos>`

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
        del dataframe. :ref:`Ver ejemplo <calidad_datos.ValoresFaltantes>`

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
        :ref:`Ver ejemplo <calidad_datos.CantidadDuplicados>`

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
            de verificación de duplicados de columans, el cual puede resultar \
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
        :ref:`Ver ejemplo <calidad_datos.EmparejamientoDuplicados>`

        :param col: (bool) {True, False}, valor por defecto: False. Si el \
            valor es `True` la validación se realiza por columnas, en caso \
            contrario, la validación se hace por filas.
        :param numero_filas: (int), valor por defecto: 30000. Número de filas \
            que tendrá cada columna cuando se verifiquen los duplicados por \
            columna (cuando `eje=1`). Se utiliza para agilizar el proceso de \
            verificación de duplicados por columnas, el cual puede resultar \
            extremadamente lento para un conjunto de datos con muchas filas.
        :return: (Dataframe) Matriz que relaciona los indices de filas o \
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
                indexs.append(subset1.index[r1])
                for r2 in subset1.iloc[:, i + 1 :]:
                    if r2 not in verificado:
                        comp = subset1[r1].equals(subset1[r2])
                        if comp:
                            indexs.append(subset1.index[r2])
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
                return

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
        intentarán transformar a columnas numéricas). \
        :ref:`Ver ejemplo <calidad_datos.ValoresExtremos>`

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
        faltantes. :ref:`Ver ejemplo <calidad_datos.DescripcionNumericas>`

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
        base_descripcion = self.base.loc[:, col_num].describe().T
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
        sea igual a su `percentil_superior`. \
        :ref:`Ver ejemplo <calidad_datos.VarianzaEnPercentil>`

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
        faltantes. :ref:`Ver ejemplo <calidad_datos.DescripcionCategoricas>`.

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
        :ref:`Ver ejemplo <calidad_datos.Memoria>`

        :param col: Si `False` realiza el cálculo de memoria del Dataframe \
            completo, si `True` realiza el cálculo de memoria por \
            cada columna del Dataframe. Por defecto `False`.
        :type col: bool, opcional
        :param unidad: {"byte", "kb", "Mb", "Gb", "Tb"} Es la unidad de \
            medida de memoria con la que se desea ver la memoria que ocupa \
            en el computador del conjunto  de datos. Por defecto "Mb".
        :type unidad: str, opcional

        :return: (float | pandas.Series) Si `col = False` retorna el valor de \
            memoria ocupada por el cojunto de datos. Si `col = True`, retorna \
            la memoria ocupada por cada columna del conjunto de datos.
        """

        if not isinstance(col, bool):
            raise ValueError("'col' debe ser booleano. {True, False}.")
        if unidad not in ["byte", "kb", "Mb", "Gb", "Tb"]:
            raise ValueError(
                "El parámetro 'unidad' debe ser uno de  estos "
                " valores : 'byte', 'kb', 'Mb', 'Gb', 'Tb'"
            )

        if col:
            memoria_ = self.base.memory_usage(index=True)
        else:
            memoria_ = self.base.memory_usage(index=True).sum()

        if unidad == "byte":
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
        """ Retorna una tabla con información general el conjunto de datos.\
        Incluye número de filas y columnas, número de columnas de tipo \
        numéricas, de texto, booleanas, fecha y otros, número de filas y \
        columnas no únicas, número de columnas con más de la mitad de las \
        observaciones con datos faltantes, número de columnas con más del \
        10% de observaciones con datos extremos y el tamaño del conjunto de \
        datos en memoria. :ref:`Ver ejemplo <calidad_datos.Resumen>`

        :param filas: (bool) {True, False}, valor por defecto: True. Indica \
            si se incluye el cálculo de número de filas del dataframe.
        :param columnas: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el cálculo de número de filas del dataframe.
        :param colNumericas: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de tipo numéricas.
        :param colTexto: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de tipo texto.
        :param colBooleanas: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de tipo boolean.
        :param colFecha: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de tipo fecha.
        :param colOtro: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de otro tipo deferente \
            a los anteriores.
        :param filasRepetidas: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de filas repetidas.
        :param columnasRepetidas: (bool) {True, False}, valor por defecto: \
            False. Indica si se incluye el número de columnas repetidas.
        :param colFaltantes: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas con más de la mitad de \
            las observaciones con datos faltantes.
        :param colExtremos: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas con más del 10% de \
                observaciones con datos extremos.
        :param memoriaTotal: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el cálculo del tamaño del conjunto de datos en memoria.
        :return: serie de pandas con las estadísticas descriptivas del dataframe.
        """

        # Lista donde se guardarán resultados
        lista_resumen = [[], []]

        # Calcular tipo de columnas
        col_tipos = self.TipoColumnas(
            tipoGeneral=True, tipoGeneralPython=False, tipoEspecifico=False
        ).iloc[:, 0]

        ## Agregar a lista, si se escoge que sea así

        # Número de filas
        if filas:
            calculo = self.base.shape[0]
            nombre = "Número de filas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        # Número de columnas
        if columnas:
            calculo = self.base.shape[1]
            nombre = "Número de columnas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        # Número de columnas numéricas
        if colNumericas:
            calculo = len(col_tipos[col_tipos == "Numérico"])
            nombre = "Columnas numéricas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        # Número de columnas de texto
        if colTexto:
            calculo = len(col_tipos[col_tipos == "Texto"])
            nombre = "Columnas de texto"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        # Número de columnas booleanas
        if colBooleanas:
            calculo = len(col_tipos[col_tipos == "Boolean"])
            nombre = "Columnas booleanas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        # Número de columnas de fecha
        if colFecha:
            calculo = len(col_tipos[col_tipos == "Fecha"])
            nombre = "Columnas de fecha"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        # Número de columnas de otro tipo
        if colOtro:
            calculo = len(col_tipos[col_tipos == "Otro"])
            nombre = "Otro tipo de columnas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        # Número de filas no únicas
        if filasRepetidas:
            calculo = self.CantidadDuplicados(eje=0, numero=True)
            nombre = "Número de filas repetidas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        # Número de columnas no únicas
        if columnasRepetidas:
            calculo = self.CantidadDuplicados(eje=1, numero=True)
            nombre = "Número de columnas repetidas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        # Porcentaje de columnas con más de la mitad de datos faltantes
        if colFaltantes:
            col_missing = self.ValoresFaltantes(numero=False)
            calculo = len(col_missing[col_missing > 0.5])
            nombre = "Columnas con más de la mitad de datos faltantes"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

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
        else:
            pass

        # Tamaño del conjunto de datos en la memoria
        if memoriaTotal:
            memoria_tot = self.Memoria()
            if memoria_tot > 1024:
                memoria_tot = memoria_tot / 1024
                nombre = "Uso en memoria del conjunto de datos en gygabytes (aproximado)"
            elif memoria_tot < (1 / 1024):
                memoria_tot = memoria_tot * 1024 * 1024
                nombre = "Uso en memoria del conjunto de datos en bytes (aproximado)"
            elif memoria_tot < 1:
                memoria_tot = memoria_tot * 1024
                nombre = "Uso en memoria del conjunto de datos en kylobytes (aproximado)"
            else:
                nombre = "Uso en memoria del conjunto de datos en megabytes (aproximado)"

            calculo = memoria_tot
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass

        tabla_resumen = pd.Series(
            data=lista_resumen[1], index=lista_resumen[0]
        ).astype(int)
        return tabla_resumen

    # Matrices de correlación para las variables numéricas
    def CorrelacionNumericas(self, metodo="pearson", variables=None):
        """ Genera una matriz de correlación entre las variables de tipo numérico \
            :ref:`Ver ejemplo <calidad_datos.CorrelacionNumericas>`

        :param metodo: (str) {'pearson', 'kendall', 'spearman'}, valor por \
            defecto: 'pearson'. Medida de correlación a utilizar.
        :param variables: (list) lista de nombres de las columnas separados \
            por comas. Permite escoger las columnas de interés de análisis \
            del dataframe
        :return: dataframe con las correlaciones de las columnas de tipo \
            numérico analizadas.
        """
        # Revisar si hay columnas numéricas. En caso de no haber, detener función
        col_num = [
            self.lista_tipos_columnas[0][i]
            for i in range(len(self.lista_tipos_columnas[0]))
            if "float" in self.lista_tipos_columnas[1][i]
            or "int" in self.lista_tipos_columnas[1][i]
        ]
        if len(col_num) == 0:
            print("El conjunto de datos no tiene columnas numéricas")
            return
        else:
            pass

        # Crear lista de númericas filtradas por las variables escogidas en la opción 'variables'
        if isinstance(variables, list):
            columnas_filtro = [q for q in variables if q in list(col_num)]
            col_num = columnas_filtro
            del columnas_filtro
        else:
            pass

        # Crear la matriz de correlación dependiendo del método escogido
        if metodo == "pearson":
            correlacion_ = self.base[col_num].corr(method="pearson")
        elif metodo == "kendall":
            correlacion_ = self.base[col_num].corr(method="kendall")
        elif metodo == "spearman":
            correlacion_ = self.base[col_num].corr(method="spearman")
        else:
            raise ValueError(
                '"metodo" tiene que ser "pearson", "kendall" o "spearman>"'
            )

        return correlacion_

    # Matrices de correlación para variables categóricas
    def CorrelacionCategoricas(
        self, metodo="phik", limite=0.5, categoriasMaximas=30, variables=None
    ):
        """ Genera una matriz de correlación entre las variables de tipo categóricas. \
            :ref:`Ver ejemplo <calidad_datos.CorrelacionCategoricas>`

        :param metodo: (str) {'phik', 'cramer'}, valor por \
            defecto: 'phik'. Medida de correlación a utilizar.
        :param limite: (float) (valor de 0 a 1) límite de referencia, se \
            utiliza para determinar si las variables posiblemente son de tipo \
            categóricas y ser incluidas en el análisis. Si el número de \
            valores únicos por columna es mayor al número de registros \
            limite, se considera que la variable no es categórica.
        :param categoriasMaximas: (int) (valor mayor a 0), indica el máximo \
            número de categorías de una variable para que sea incluida en el \
            análisis
        :param variables: (list) lista de nombres de las columnas separados \
            por comas. Permite escoger las columnas de interés de análisis \
            del dataframe
        :return: dataframe con las correlaciones de las columnas de tipo \
            categórica analizadas.
        """
        # verificar si las variables escogidas del filtro se encuentran en el conjunto de datos
        if isinstance(variables, list):
            for v in variables:
                if v in self.lista_tipos_columnas[0]:
                    pass
                else:
                    raise ValueError(
                        '"{0}" no es una columna del conjunto de datos'.format(
                            v
                        )
                    )
        else:
            variables = self.lista_tipos_columnas[0].copy()

        # Revisar si hay columnas con tipos diccionario o lista
        lista_columnas_dict = []
        for i in range(len(self.lista_tipos_columnas[0])):
            col_nombre = self.lista_tipos_columnas[0][i]
            tip = self.lista_tipos_columnas[2][i]

            if tip == "dict" or tip == "list":
                lista_columnas_dict.append(col_nombre)
            else:
                pass

        # Filtrar por el número de categorías únicas en cada variable
        if categoriasMaximas > 0:
            categorias_unicas = pd.concat(
                [
                    self.base.drop(columns=lista_columnas_dict),
                    self.base.loc[:, lista_columnas_dict].astype(str),
                ],
                axis=1,
            ).nunique()
            categorias_unicas = categorias_unicas.loc[
                categorias_unicas <= categoriasMaximas
            ].index
            variables = [q for q in variables if q in categorias_unicas]
        else:
            raise ValueError(
                '"categoriasMaximas" tiene que un ´numero mayor a 0"'
            )

        # Calcular qué variables tipo object tienen valores únicos menores al
        # 50% (o valor de 'limite') del total de filas del conjunto de datos original
        col_object = self.base.loc[:, variables].dtypes
        col_object = col_object[col_object == "object"]
        lista_object_unicos = []
        for s in col_object.index:
            unico = len(pd.unique(self.base[s]))
            if unico < self.base.shape[0] * limite:
                lista_object_unicos.append(s)

        # Hacer doble loop para crear matriz de correlation tipo Cramer V
        if metodo == "cramer":
            lista_matriz = []
            for c in lista_object_unicos:
                lista_fila = []
                for cc in lista_object_unicos:
                    try:
                        if (
                            c not in lista_columnas_dict
                            or cc not in lista_columnas_dict
                        ):
                            cramer = self.correlacion_cramerv(
                                self.base[c], self.base[cc]
                            )
                        elif (
                            c in lista_columnas_dict
                            or cc not in lista_columnas_dict
                        ):
                            cramer = self.correlacion_cramerv(
                                self.base[c].astype(str), self.base[cc]
                            )
                        elif (
                            c not in lista_columnas_dict
                            or cc in lista_columnas_dict
                        ):
                            cramer = self.correlacion_cramerv(
                                self.base[c], self.base[cc].astype(str)
                            )
                        else:
                            cramer = self.correlacion_cramerv(
                                self.base[c].astype(str),
                                self.base[cc].astype(str),
                            )

                        lista_fila.append(cramer)
                    except BaseException:
                        lista_fila.append(np.nan)

                lista_matriz.append(lista_fila)

            # Convertir a dataframe
            lista_matriz = pd.DataFrame(lista_matriz)
            lista_matriz.columns = lista_object_unicos
            lista_matriz.index = lista_object_unicos

            correlacion_final = lista_matriz

            # Nombre de variables en 'correlacion_final' antes de filtro
            nombres_nofiltro = list(correlacion_final.columns)

            # Quitar las columnas y filas que son 'nan'
            correlacion_final = correlacion_final.dropna(how="all", axis=1)
            correlacion_final = correlacion_final.dropna(how="all", axis=0)

            # Mencionar las variables cuya correlación no se pudo calcular
            nombres_filtro = list(correlacion_final.columns)
            nombres_eliminados = nombres_nofiltro.copy()
            for s in nombres_filtro:
                nombres_eliminados.remove(s)
            for s in nombres_eliminados:
                warnings.warn(
                    "no se pudo calcular la correlación con la variable '{0}'".format(
                        s
                    )
                )

        # Matriz de correlación con la metodología 'phik'
        elif metodo == "phik":
            correlacion_final = self.base.loc[
                :, lista_object_unicos
            ].phik_matrix()
        else:
            raise ValueError('"metodo" tiene que ser "phik" o "cramer"')

        return correlacion_final

    def correlacion_cramerv(self, x, y):
        """ Función de soporte para calcular coeficiente de correlación Cramer V \
        (para usar en la función de las matrices de correlación entre variables categóricas)

        :param x:
        :param y:
        :return:
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
