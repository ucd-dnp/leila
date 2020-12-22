# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import phik
import scipy.stats as sstats
import warnings


class CalidadDatos:

    def __init__(self, _base, castNumero=False, diccionarioCast=None,
                 errores="ignore", formato_fecha=None):
        """ Constructor por defecto de la clase CalidadDatos. Esta clase se \
        encarga de manejar todas las funciones asociadas a la medición de la \
        calidad de los datos en una base de datos

        :param base: (dataframe) Base de datos de tipo pandas.DataFrame que será
            analizada por la clase CalidadDatos.
        :param castNumero: (bool) {True, False}. Valor por defecto: False \
            Indica si se desea convertir las columnas de tipos object y \
            bool a float, de ser posible
        :param diccionarioCast: (dict) { {nombre_columna : tipo_columna} } \
            Diccionario donde se especifican los tipos a que se desean \
            convertir las columnas (string, numerico, booleano, fecha, \
            categorico)
        :param errores: (string) {'ignore', 'coerce', 'raise'}\
            Valor por defecto: 'ignore'. Indica qué hacer con las columnas \
            cuyo tipo no se puede cambiar al solicitado en 'diccionarioCast'
        :param formato_fecha: (string). Formato a ser utilizado al hacer cast a variables de fecha.
        :return: Objeto del tipo de la clase CalidadDatos
        """

        self.base = _base.copy()

        # Calcular tipos de columnas con 'dtypes' para no volver a calcular en todo el script
        self.tipos_dtypes = self.base.dtypes

        # Pasar los 'objects' a float, si posible
        if castNumero == True:
            tipos_object = self.tipos_dtypes[(self.tipos_dtypes == "object") | (
                self.tipos_dtypes == "bool")].index.to_list()
            # Pasar las columnas que se puedan a integer
            self.base[tipos_object] = self.base[tipos_object].apply(
                lambda x: x.astype("int64", errors="ignore"), axis=0)
            # Pasar las columnas qeu se puedan a float
            tipos_object = self.tipos_dtypes[(self.tipos_dtypes == "object") | (
                self.tipos_dtypes == "bool")].index.to_list()
            self.base[tipos_object] = self.base[tipos_object].apply(
                lambda x: x.astype(float, errors="ignore"), axis=0)

        elif castNumero == False:
            pass
        else:
            raise ValueError('"castNumero" tiene que ser True o False')

        # Cambiar los tipos de las variables según el diccionario
        if isinstance(diccionarioCast, dict):
            for s in diccionarioCast:

                if diccionarioCast[s] == "string":
                    self.base[s] = self.base[s].apply(lambda x: str(x))
                elif diccionarioCast[s] == "numerico":
                    self.base[s] = pd.to_numeric(self.base[s], errors=errores)
                elif diccionarioCast[s] == "booleano":
                    self.base[s] = self.base[s].astype("bool")
                elif diccionarioCast[s] == "fecha":
                    self.base[s] = pd.to_datetime(
                        self.base[s], format=formato_fecha, errors=errores)
                elif diccionarioCast[s] == "categorico":
                    self.base[s] = pd.Categorical(self.base[s])
                else:
                    raise ValueError(
                        'Las llaves de "diccionarioCast" tienen que ser "string", "numerico", "booleano", "fecha" o "categorico" ')
        elif diccionarioCast is None:
            pass
        else:
            raise ValueError('"diccionario" tiene que ser tipo "dict"')

        # Tipo más común´de cada columna
        tipo_mas_comun = [str(type(self.base[q].mode()[0])).replace(
            "<class ", "").replace(">", "").replace("'", "") for q in self.base.columns]

        columnas_dtypes = [str(q) for q in self.tipos_dtypes]
        self.lista_tipos_columnas = [
            list(self.base.columns), columnas_dtypes, tipo_mas_comun]

        print(self.lista_tipos_columnas)

    # Tipos de las columnas
    def TipoColumnas(self, tipoGeneral=True,
                     tipoGeneralPython=True, tipoEspecifico=True):
        """ Retorna el tipo de dato de cada columna del dataframe. :ref:`Ver ejemplo <calidad_datos.TipoColumnas>`

        :param tipoGeneral: (bool) {True, False}, valor por defecto: True. \
            Incluye el tipo general de cada columna. Los tipos son: numérico,\
            texto, booleano, otro
        :param tipoGeneralPython: (bool) {True, False}, valor por defecto: \
            True. Incluye el tipo general de cada columna dado por el método\
            'dtypes' de Python
        :param tipoEspecifico: (bool) {True, False}, valor por defecto: True.\
            Incluye el porcentaje de los tres tipos más frecuentes de cada\
            columna. Se aplica la función 'type' de Python para cada \
            observación.

        :return: Dataframe de pandas con los tipos de dato de cada columna.
        """

        # Funciones generales
        # Tipos de columnas según función dtypes
        tipos_dtypes = self.tipos_dtypes.apply(str)
        # Lista de los nombres de las columnas
        lista_nombres = list(self.base.columns)
        #
        numero_columnas_base = self.base.shape[0]
        ##

        lista_total = []

        # lista_nombres.insert(0, "")

        lista_total.append([""] + lista_nombres)

        if tipoGeneral == True:
            lista_general = []
            for s in lista_nombres:
                # Si solo hay missing values, poner como 'Otro'
                if self.base[s].isnull().sum() == numero_columnas_base:
                    lista_general.append("Otro")
                else:

                    tipo_para_object = str(
                        type(
                            self.base[s].mode(
                                dropna=True)[0]))
                    tipo_para_resto = tipos_dtypes[s]

                    if "int" in tipo_para_resto or "float" in tipo_para_resto:
                        lista_general.append("Numérico")
                    elif "str" in tipo_para_object:
                        lista_general.append("Texto")
                    elif "bool" in tipo_para_resto:
                        lista_general.append("Booleano")
                    elif "date" in tipo_para_resto:
                        lista_general.append("Fecha")
                    else:
                        lista_general.append("Otro")
            lista_general.insert(0, "tipo_general")
            lista_total.append(lista_general)
        elif tipoGeneral == False:
            pass
        else:
            raise ValueError('"tipoGeneral" tiene que ser True o False')

        # TIpo general de Python
        if tipoGeneralPython == True:
            lista_python = list(tipos_dtypes.copy())
            lista_python.insert(0, "tipo_general_python")
            lista_total.append(lista_python)
        elif tipoGeneralPython == False:
            pass
        else:
            raise ValueError('"tipoGeneralPython" tiene que ser True o False')

        # Tipo específico Python
        if tipoEspecifico == True:
            lista_especifico_1 = []
            lista_especifico_2 = []
            lista_especifico_3 = []
            lista_especifico_4 = []
            lista_especifico_5 = []

            for s in lista_nombres:

                tip = self.base[s].fillna("nan").apply(
                    lambda x: x if x == "nan" else type(x)).value_counts(
                    normalize=True, dropna=False)

                tip_1 = "{1}: {0}%".format(round(float(tip.iloc[0] * 100), 2),
                                           str(tip.index[0]).replace("<class ", "").replace(">", ""))
                lista_especifico_1.append(tip_1)

                try:
                    tip_2 = "{1}: {0}%".format(round(float(tip.iloc[1] * 100), 2),
                                               str(tip.index[1]).replace("<class ", "").replace(">", ""))
                    lista_especifico_2.append(tip_2)
                except BaseException:
                    lista_especifico_2.append("")

                try:
                    tip_3 = "{1}: {0}%".format(round(float(tip.iloc[2] * 100), 2),
                                               str(tip.index[2]).replace("<class ", "").replace(">", ""))
                    lista_especifico_3.append(tip_3)
                except BaseException:
                    lista_especifico_3.append("")

                try:
                    tip_4 = "{1}: {0}%".format(round(float(tip.iloc[3] * 100), 2),
                                               str(tip.index[3]).replace("<class ", "").replace(">", ""))
                    lista_especifico_4.append(tip_4)
                except BaseException:
                    lista_especifico_4.append("")

                try:
                    tip_5 = "{1}: {0}%".format(round(float(tip.iloc[4] * 100), 2),
                                               str(tip.index[4]).replace("<class ", "").replace(">", ""))
                    lista_especifico_5.append(tip_5)
                except BaseException:
                    lista_especifico_5.append("")

            lista_especifico_1.insert(0, "tipo_especifico_1")
            lista_total.append(lista_especifico_1)

            if all(q == "" for q in lista_especifico_2):
                pass
            else:
                lista_especifico_2.insert(0, "tipo_especifico_2")
                lista_total.append(lista_especifico_2)

            if all(q == "" for q in lista_especifico_3):
                pass
            else:
                lista_especifico_3.insert(0, "tipo_especifico_3")
                lista_total.append(lista_especifico_3)

            if all(q == "" for q in lista_especifico_4):
                pass
            else:
                lista_especifico_4.insert(0, "tipo_especifico_4")
                lista_total.append(lista_especifico_4)

            if all(q == "" for q in lista_especifico_5):
                pass
            else:
                lista_especifico_5.insert(0, "tipo_especifico_5")
                lista_total.append(lista_especifico_5)

            del tip

        elif tipoEspecifico == False:
            pass
        else:
            raise ValueError('"tipoEspecifico" tiene que ser True o False')

        tips = pd.DataFrame(lista_total).T.set_index(keys=0, drop=True)
        columnas = list(tips.iloc[0])
        tips.columns = columnas
        tips = tips.drop(tips.index[0])

        return (tips)

    # valores únicos en cada columna
    # sin missing values
    def ValoresUnicos(self, faltantes=False):
        """ Calcula la cantidad de valores únicos de cada columna del dataframe.  \
            :ref:`Ver ejemplo <calidad_datos.ValoresUnicos>`

        :param faltantes: (bool) {True, False}, valor por defecto: False. \
            Indica si desea tener en cuenta los valores faltantes en el \
                conteo de valores únicos.
        :return: serie de pandas con la cantidad de valores únicos de cada columna.
        """

        if faltantes == False:
            unicos_columnas = self.base.nunique()

        elif faltantes == True:
            unicos_columnas = self.base.apply(
                lambda x: len(x.value_counts(dropna=False)), axis=0)
        else:
            raise ValueError('"faltantes" tiene que ser True o False')

        return (unicos_columnas)

    #  Missing values
    def ValoresFaltantes(self, numero=False):
        """ Calcula el porcentaje/número de valores faltantes de cada columna \
            del dataframe. :ref:`Ver ejemplo <calidad_datos.ValoresFaltantes>`

        :param numero: (bool) {True, False}, valor por defecto: False. Si el \
            valor es False el resultado se expresa como un cociente, si el \
            valor es True el valor se expresa como una cantidad de \
            registros (número entero).
        :return: serie de pandas con la cantidad/cociente de valores \
            faltantes de cada columna.
        """

        if numero == False:
            missing_columnas = pd.isnull(self.base).sum() / len(self.base)
        elif numero == True:
            missing_columnas = pd.isnull(self.base).sum()
        else:
            raise ValueError('"cociente" tiene que ser True o False')

        return (missing_columnas)

    # Porcentaje y número de filas y columnas no únicas
    def CantidadDuplicados(self, eje=0, numero=False):
        """ Retorna el porcentaje/número de \
            filas o columnas duplicadas (repetidas) en el dataframe. \
            :ref:`Ver ejemplo <calidad_datos.CantidadDuplicados>`

        :param eje: (int) {1, 0}, valor por defecto: 0. Si el valor \
            es 1 la validación se realiza por columnas, si el valor es \
                0 la validación se realiza por filas.
        :param numero: (bool) {True, False}, valor por defecto: False. Si el \
            valor es False el resultado se expresa como un cociente, si el \
            valor es True el valor se expresa como una cantidad de \
            registros (número entero).
        :return: (int o float) resultado de unicidad.
        """
        base = self.base.copy()

        # Revisar si hay columnas con tipos diccionario o lista para
        # convertirlas a string
        for s in base.columns:
            tip = str(type(self.base[s].mode(dropna=False))).replace(
                "<class ", "").replace(">", "").replace("'", "")

            if tip == "dict" or tip == "list":
                base[s] = base[s].apply(str)
            else:
                pass

        # Proporcion (decimal) de columnas repetidas
        if eje == 1 and numero == False:

            # Calcular los duplicados con una submuestra del conjunto de datos grande
            if base.shape[0] > 30000:
                mini_base = base.iloc[0:30000]
                no_unic_columnas = mini_base.T.duplicated(keep="first")
            else:
                no_unic_columnas = base.T.duplicated(keep="first")

            # Si no hay columnas duplicadas en la muestra pequeña del conjunto de datos,#
            # entonces el valor de 'cols' será cero
            if no_unic_columnas.sum() == 0:
                cols = 0.00
                del mini_base
            # Si sí hay columnas duplicadas
            else:
                no_unic_columnas = base.T.duplicated(keep="first")
                cols = no_unic_columnas[no_unic_columnas].shape[0] / \
                    base.shape[1]

        # Número de columnas repetidas
        elif eje == 1 and numero == True:

            # Calcular los duplicados con una submuestra del conjunto de datos grande
            if base.shape[0] > 30000:
                mini_base = base.iloc[0:30000]
                no_unic_columnas = mini_base.T.duplicated(keep="first")
            else:
                no_unic_columnas = base.T.duplicated(keep="first")

            # Si no hay columnas duplicadas en la muestra pequeña del conjunto de datos,#
            # entonces el valor de 'cols' será cero
            if no_unic_columnas.sum() == 0:
                cols = 0
                del mini_base
            # Si sí hay columnas duplicadas
            else:
                no_unic_columnas = base.T.duplicated(keep="first")
                cols = no_unic_columnas[no_unic_columnas].shape[0]

        # Proporción de filas repetidas
        elif eje == 0 and numero == False:
            no_unic_filas = base.duplicated(keep="first")
            cols = no_unic_filas[no_unic_filas].shape[0] / base.shape[0]

        # Número de filas repetidas
        elif eje == 0 and numero == True:
            no_unic_filas = base.duplicated(keep="first")
            cols = no_unic_filas[no_unic_filas].shape[0]

        else:
            raise ValueError(
                '"eje" tiene que ser 1 o 0 y "numero" tiene que ser True o False')

        return (cols)

    # Matching de columnas y filas no únicas
    def EmparejamientoDuplicados(self, col=False):
        """ Retorna las columnas o filas que presenten valores duplicados del \
            dataframe. :ref:`Ver ejemplo <calidad_datos.EmparejamientoDuplicados>`

        :param col: (bool) {True, False}, valor por defecto: False. Si el valor \
            es True la validación se realiza por columnas, si el valor es \
                False la validación se realiza por filas.
        :return: matriz (dataframe) que relaciona las indices de filas/nombre \
            de columnas que presentan valores duplicados.
        """
        base = self.base.copy()

        # Revisar si hay columnas con tipos diccionario o lista para
        # convertirlas a string
        for s in base.columns:
            tip = str(type(self.base[s].value_counts(dropna=False).index[0])).replace("<class ", "").replace(">",
                                                                                                             "").replace(
                "'", "")

            if tip == "dict" or tip == "list":
                base[s] = base[s].apply(str)
            else:
                pass

        # Obtener todos los duplicados, sin hacer todavía el emparejamiento
        if col == True:
            if base.shape[0] > 30000:
                mini_base = base.iloc[0:30000]
                dupli = mini_base.T.duplicated(keep=False)
            else:
                dupli = base.T.duplicated(keep=False)

            if dupli.sum() == 0:
                return("No hay columnas duplicadas")
            else:
                duplicados_mini = dupli[dupli == True].index
                dupli = base[duplicados_mini].T.duplicated(keep=False)

        elif col == False:
            dupli = base.duplicated(keep=False)
        else:
            raise ValueError('"col" tiene que ser True o False')

        # Revisar si hay duplicados o no. Parar si no hay
        dupli = dupli[dupli]
        if dupli.sum() == 0:
            if col == True:
                print("No hay columnas duplicadas")
                return
            elif col == False:
                print("No hay filas duplicadas")
                return
            else:
                raise ValueError('"col" tiene que ser True o False')
        else:
            pass

        lista_duplicados = []
        for s in dupli.index:
            for ss in dupli.index:
                if col == True:
                    if base[s].equals(base[ss]) and s != ss:
                        lista_duplicados.append([s, ss])
                elif col == False:
                    if base.iloc[s].equals(base.iloc[ss]) and s != ss:
                        lista_duplicados.append([s, ss])
                else:
                    pass

        if col == False:
            lista_duplicados = sorted(lista_duplicados)
        else:
            pass

        dic = {}
        for s in dupli.index:
            dic[s] = []
        for s in dupli.index:
            for i in range(len(lista_duplicados)):
                if s in lista_duplicados[i]:
                    dic[s].append(lista_duplicados[i])
        for s in dic:
            lista = [q for l in dic[s] for q in l]
            dic[s] = list(set(lista))

        if col == True:
            lista_listas = [q for q in dic.values()]
        else:
            lista_listas = [sorted(q) for q in dic.values()]

        for i in range(len(lista_listas)):
            for ii in range(len(lista_listas[i])):
                lista_listas[i][ii] = str(lista_listas[i][ii])

        df = pd.DataFrame(
            lista_listas).drop_duplicates().reset_index(drop=True)

        df = df.T

        if col == True:
            lista_columnas_df = [
                "Columnas iguales {0}".format(q) for q in range(
                    1, df.shape[1] + 1)]
            df.columns = lista_columnas_df
        else:
            lista_columnas_df = [
                "Filas iguales {0}".format(q) for q in range(
                    1, df.shape[1] + 1)]
            df.columns = lista_columnas_df

        # Quitar los 'nan' del
        df = df.apply(lambda x: x.replace(np.nan, ""))

        return (df)

    # Valores extremos
    def ValoresExtremos(self, extremos="ambos", numero=False):
        """ Calcula el porcentaje o cantidad de outliers de cada columna numérica \
            (las columnas con números en formato string se intentarán transformar \
            a columnas numéricas). :ref:`Ver ejemplo <calidad_datos.ValoresExtremos>`

        :param extremos: (str) {'superior', 'inferior', 'ambos'}, valor por \
            defecto: 'ambos'. Si el valor es '**inferior**' se tienen en cuenta los \
            registros con valor menor al límite inferior calculado por la \
            metodología de valor atípico por rango intercuartílico. Si el valor es \
            '**superior**' se tienen en cuenta los registros con valor mayor al\
            límite superior calculado por la metodología de valor atípico por rango \
            intercuartílico. Si el valor es '**ambos**' se tienen en cuenta los \
            registros con valor menor al límite inferior calculado por la  \
            metodología de valor atípico por rango intercuartílico, y también \
            aquellos con valor mayor al límite superior calculado por la \
            metodología de valor atípico por rango intercuartílico.
        :param numero: (bool) {True, False}, valor por defecto: False. Si el valor es \
            False el resultado se expresa como una proporcion (en decimales), si el valor es True el \
            valor se expresa como una cantidad de registros (número entero).
        :return: serie de pandas con la cantidad/proporcion de valores outliers \
            de cada columna.
        """
        # Revisar si hay columnas numéricas. En caso de no haber, detener función
        col_num = [self.lista_tipos_columnas[0][i] for i in range(len(
            self.lista_tipos_columnas[0])) if "float" in self.lista_tipos_columnas[1][i] or "int" in self.lista_tipos_columnas[1][i]]

        if len(col_num) == 0:
            print("El conjunto de datos no tiene columnas numéricas")
            return
        else:
            pass

        ###
        percentiles_25 = self.base[col_num].apply(
            lambda x: np.nanpercentile(x, 25), axis=0)
        percentiles_75 = self.base[col_num].apply(
            lambda x: np.nanpercentile(x, 75), axis=0)

        iqr = percentiles_75 - percentiles_25
        iqr_upper = percentiles_75 + iqr * 1.5
        iqr_lower = percentiles_25 - iqr * 1.5

        dic_outliers = {}

        if extremos == "ambos":
            for i in range(0, len(iqr)):
                dic_outliers[self.base[col_num].columns[i]] = (self.base[col_num].iloc[:, i] > iqr_upper[i]) | (
                    self.base[col_num].iloc[:, i] < iqr_lower[i])
        elif extremos == "superior":
            for i in range(0, len(iqr)):
                dic_outliers[self.base[col_num].columns[i]] = (
                    self.base[col_num].iloc[:, i] > iqr_upper[i])
        elif extremos == "inferior":
            for i in range(0, len(iqr)):
                dic_outliers[self.base[col_num].columns[i]] = (
                    self.base[col_num].iloc[:, i] < iqr_lower[i])
        else:
            raise ValueError(
                '"extremos" tiene que ser "ambos", "superior" o "inferior"')

        base_outliers = pd.DataFrame(dic_outliers)

        if numero == False:
            cantidad_outliers = base_outliers.sum() / base_outliers.shape[0]
        elif numero == True:
            cantidad_outliers = base_outliers.sum()
        else:
            raise ValueError('"numero" tiene que ser True o False')

        del base_outliers

        return (cantidad_outliers)

    # describe de columnas
    def DescripcionNumericas(self, variables=None):
        """ Calcula estadísticas descriptivas de cada columna numérica. \
            Incluyen media, mediana, valores en distintos percentiles,\
            desviación estándar, valores extremos y porcentaje de valores \
            faltantes. :ref:`Ver ejemplo <calidad_datos.DescripcionNumericas>`

        :param variables: (list) lista de nombres de las columnas separados \
            por comas. Permite escoger las columnas de interés de análisis \
            del dataframe

        :return: dataframe con las estadísticas descriptivas.
        """
        # Seleccionar columnas numéricas de 'self.lista_tipos_columnas'
        col_num = [self.lista_tipos_columnas[0][i] for i in range(len(
            self.lista_tipos_columnas[0])) if "float" in self.lista_tipos_columnas[2][i] or "int" in self.lista_tipos_columnas[2][i]]

        # Filtrar el conjunto de datos por las variables escogidas en la opción 'variables'
        if isinstance(variables, list):
            baseObjeto = CalidadDatos(
                self.base[variables].copy(), castNumero=False)
            # Seleccionar columnas numéricas que se encuentren dentro de 'variables'
            col_num = [q for q in variables if q in col_num]
        else:
            baseObjeto = CalidadDatos(self.base.copy(), castNumero=False)

        if len(col_num) == 0:
            print("El conjunto de datos no tiene columnas numéricas")
            return
        else:
            pass

        base_descripcion = self.base.loc[:, col_num].describe().T
        base_descripcion["missing"] = pd.isnull(self.base.loc[:, col_num]).sum() / len(self.base.loc[:, col_num])
        base_descripcion["outliers_total"] = baseObjeto.ValoresExtremos()
        base_descripcion["outliers_altos"] = baseObjeto.ValoresExtremos(
            extremos="superior")
        base_descripcion["outliers_bajos"] = baseObjeto.ValoresExtremos(
            extremos="inferior")

        return (base_descripcion)

    ###############
    def VarianzaEnPercentil(self, percentil_inferior=5, percentil_superior=95):
        """ Retorna las columnas numéricas cuyo percentil_inferior sea igual \
            a su percentil_superior. :ref:`Ver ejemplo <calidad_datos.VarianzaEnPercentil>`

        :param base: (dataframe) base de datos de interés a ser analizada.
        :param percentil_inferior: (float), valor por defecto: 5. Percentil \
            inferior de referencia en la comparación.
        :param percentil_superior: (float), valor por defecto: 95. Percentil \
            superior de referencia en la comparación.
        :return: indices de columnas cuyo percentil inferior es igual al \
            percentil superior.
        """

        # Revisar si hay columnas numéricas. En caso de no haber, detener función
        col_num = [self.lista_tipos_columnas[0][i] for i in range(len(
            self.lista_tipos_columnas[0])) if "float" in self.lista_tipos_columnas[1][i] or "int" in self.lista_tipos_columnas[1][i]]

        if len(col_num) == 0:
            print("El conjunto de datos no tiene columnas numéricas")
            return
        else:
            pass
                
        lista_nums = []
        for i in range(len(self.tipos_dtypes)):
            if "int" in str(self.tipos_dtypes[i]) or "float" in str(self.tipos_dtypes[i]):
                lista_nums.append(self.tipos_dtypes.index[i])
        # base_num = base[lista_nums]
        numero_filas = self.base.shape[0]
        for c in self.base[lista_nums].columns:
            if self.base[c].isnull().sum() == numero_filas:
                del self.base[c]
            else:
                pass

        percentil_bajo = self.base[lista_nums].apply(
            lambda x: np.percentile(
                x.dropna(), 5), axis=0)
        percentil_alto = self.base[lista_nums].apply(
            lambda x: np.percentile(
                x.dropna(), 95), axis=0)

        percentiles = pd.concat([percentil_bajo, percentil_alto], axis=1)
        percentiles_true = (percentiles.iloc[:, 0] == percentiles.iloc[:, 1])
        percentiles_true = percentiles_true[percentiles_true == True]

        if len(percentiles_true) == 0:
            print("No hay ninguna columna numérica que tenga el percentil {0} y el percentil {1} igual".format(
                percentil_inferior, percentil_superior))
            return
        else:
            return (percentiles_true.index)

    # tabla de valores únicos para cada variable de texto
    def DescripcionCategoricas(
            self, limite=0.5, categoriasMaximas=30, incluirNumericos=True, variables=None):
        """ Genera una tabla con los primeros 10 valores más frecuentes de las \
            columnas categóricas del dataframe, además calcula su frecuencia \
            y porcentaje dentro del total de observaciones. Incluye los \
            valores faltantes. :ref:`Ver ejemplo <calidad_datos.DescripcionCategoricas>`

        :param limite: (float) (valor de 0 a 1) límite de referencia, se \
            utiliza para determinar si las variables posiblemente son de tipo \
            categóricas y ser incluidas en el análisis. Si el número de \
            valores únicos por columna es mayor al número de registros \
            limite, se considera que la variable no es categórica.
        :param categoriasMaximas: (int) (valor mayor a 0), indica el máximo \
            número de categorías de una variable para que sea incluida en el \
            análisis
        :param incluirNumericos: (bool) {True, False}, determina si se desea \
            considerar las variables numéricas como categóricas e incluirlas en el \
            análisis. Si el valor es True se incluyen las variables numéricas \
            en el análisis, si el valor es False no se incluyen las variables \
            numéricas en el análisis.
        :param variables: (list) lista de nombres de las columnas separados \
            por comas. Permite escoger las columnas de interés de análisis \
            del dataframe
        :return: dataframe con las estadísticas descriptivas de las columnas \
            de tipo texto.
        """
        base = self.base.copy()

        # Filtrar El conjunto de datos por las variables escogidas en la opción 'variables'
        if isinstance(variables, list):
            base = base[variables]
        else:
            pass

        # Si una variable solo tiene missing values, quitar
        for s in base.columns:
            if base[s].isnull().sum() == base.shape[0]:
                del base[s]
                warnings.warn(
                    "La variable '{0}' se eliminó del análisis porque solo tiene valores faltantes".format(s))
            else:
                pass

        # Revisar si hay columnas con tipos diccionario o lista para
        # convertirlas a string
        for s in base.columns:
            tip = str(type(self.base[s].value_counts(dropna=False).index[0])).replace("<class ", "").replace(">",
                                                                                                             "").replace(
                "'", "")

            if tip == "dict" or tip == "list":
                base[s] = base[s].apply(str)
            else:
                pass

                # Filtrar por el número de categorías únicas en cada variable
        if categoriasMaximas > 0:
            categorias_unicas = base.nunique()
            categorias_unicas = categorias_unicas.loc[categorias_unicas <=
                                                      categoriasMaximas].index
            base = base[categorias_unicas]
        else:
            raise ValueError(
                '"categoriasMaximas" tiene que un ´numero mayor a 0"')

        # Calcular qué variables tipo object tienen valores únicos menores al
        # 50% (o valor de 'limite') del total de filas del conjunto de datos original
        col_object = base.dtypes
        col_object = col_object[col_object == "object"]
        lista_object_unicos = []
        for s in col_object.index:
            unico = len(pd.unique(base[s]))
            if unico < base.shape[0] * limite:
                lista_object_unicos.append(s)

        # Si la opción 'transformar_nums' es True, incluir las variables
        # numéricas con repeticiones menores al 50% (o el límite) del total de
        # filas
        if incluirNumericos == True:
            cols_types = base.dtypes
            col_nums = []
            for i in range(len(cols_types)):
                if "int" in str(cols_types[i]) or "float" in str(
                        cols_types[i]):
                    col_nums.append(cols_types.index[i])
            for s in col_nums:
                unico = len(pd.unique(base[s]))
                if unico < base.shape[0] * limite:
                    lista_object_unicos.append(s)
        elif incluirNumericos == False:
            pass
        else:
            raise ValueError('"incluirNumericos" tiene que ser True o False')

        # Crear el dataframe con la información
        lista_counts = []
        for s in lista_object_unicos:

            counts = base[s].astype(str).value_counts().drop(
                "nan", errors="ignore")
            if isinstance(counts.index[0], dict):
                continue
            # counts=list(counts)
            lista = counts[0:10]
            resto = sum(counts[10:len(counts)])
            miss = pd.isnull(base[s]).sum()

            lista["Demás categorías"] = resto
            lista["Datos faltantes"] = miss

            lista["Total categorías (incluye NA): {0}".format(
                len(pd.unique(base[s])))] = np.nan

            lista = lista.to_frame()
            lista["Columna"] = s
            lista["Porcentaje del total de filas"] = lista[s] / len(base)

            resto = lista.iloc[:, 0].loc["Demás categorías"]

            if resto == 0:
                lista = lista.drop("Demás categorías", axis=0)

            lista = lista.reset_index()

            s = lista.columns.tolist()[1]
            colis = ["Columna", "index", s, "Porcentaje del total de filas"]
            lista = lista[colis]
            lista_cols = lista.columns.tolist()
            lista = lista.rename(
                columns={
                    "index": "Valor",
                    lista_cols[2]: "Frecuencia"})
            lista_counts.append(lista)
        df_counts = pd.concat(lista_counts, axis=0)
        return (df_counts)

    # Tamaño del conjunto de datos en la memoria
    def Memoria(self, col=False, unidad="megabyte"):
        """ Calcula el tamaño del conjunto de datos en memoria (megabytes). :ref:`Ver ejemplo <calidad_datos.Memoria>`

        :param col: (bool) {True, False}, valor por defecto: False. Si el \
            valor es False realiza el cálculo de memoria del dataframe \
            completo, si el valor es True realiza el cálculo de memoria por \
            cada columna del dataframe.
        :param unidad: (str) {byte, kylobyte, megabyte, gygabyte, terabyte}, \
            valor por defecto: 'megabyte'. Es la unidad con la que se desea \
            ver la memoria del conjunto  de datos
        :return: valor (float) del tamaño del conjunto de datos en megabytes \
            (si el parámetro col es False). Serie de pandas con el cálculo de \
            memoria en megabytes por cada columna del dataframe. (si el \
            parámetro col es True).
        """
        if col == False:
            memoria_ = self.base.memory_usage(index=True).sum()
        elif col == True:
            memoria_ = self.base.memory_usage(index=True)
        else:
            raise ValueError('"col" tiene que ser True o False')

        if unidad == "byte":
            pass
        elif unidad == "kylobyte":
            memoria_ = memoria_ / (1024)
        elif unidad == "megabyte":
            memoria_ = memoria_ / (1024 ** 2)
        elif unidad == "gygabyte":
            memoria_ = memoria_ / (1024 ** 3)
        elif unidad == "terabyte":
            memoria_ = memoria_ / (1024 ** 4)
        else:
            raise ValueError(
                '"unidad" tiene que ser "byte", "kylobyte", "megabyte", "gygabyte" o "terabyte"')
        return (memoria_)

    # tabla de resumen pequeña
    def Resumen(self, filas=True, columnas=True, colNumericas=True,
                colTexto=True, colBooleanas=True, colFecha=True,
                colOtro=True, filasRepetidas=True, columnasRepetidas=False,
                colFaltantes=True, colExtremos=True, memoriaTotal=True):
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

        # Lista donde se guardarán resultados, dependiendo de si se escoge o no
        # ver el cálculo
        lista_resumen = [[], []]

        # Calcular tipo de columnas
        col_tipos = self.TipoColumnas(
            tipoGeneral=True, tipoGeneralPython=False, tipoEspecifico=False).iloc[:, 0]

        # Revisar si hay columnas numéricas. En caso de no haber, detener función
        col_num = [self.lista_tipos_columnas[0][i] for i in range(len(
            self.lista_tipos_columnas[0])) if "float" in self.lista_tipos_columnas[1][i] or "int" in self.lista_tipos_columnas[1][i]]

        if len(col_num) == 0:
            print("El conjunto de datos no tiene columnas numéricas")
            return
        else:
            pass

        # Agregar a lista, si se escoge que sea así

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
            data=lista_resumen[1],
            index=lista_resumen[0]).astype(int)
        return (tabla_resumen)

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
        col_num = [self.lista_tipos_columnas[0][i] for i in range(len(
            self.lista_tipos_columnas[0])) if "float" in self.lista_tipos_columnas[1][i] or "int" in self.lista_tipos_columnas[1][i]]

        if len(col_num) == 0:
            print("El conjunto de datos no tiene columnas numéricas")
            return
        else:
            pass

        # Crera lista de númericas filtradas por las variables escogidas en la opción 'variables'
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
                '"metodo" tiene que ser "pearson", "kendall" o "spearman>"')

        return correlacion_

    # Matrices de correlación para variables categóricas
    def CorrelacionCategoricas(
            self, metodo='phik', limite=0.5, categoriasMaximas=30, variables=None):
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

        base = self.base.copy()

        # Filtrar el conjunto de datos por las variables escogidas en la opción 'variables'
        if isinstance(variables, list):
            base = base[variables]
        else:
            pass

        # Revisar si hay columnas con tipos diccionario o lista para
        # convertirlas a string
        for s in base.columns:
            tip = str(type(self.base[s].value_counts(dropna=False).index[0])).replace("<class ", "").replace(">",
                                                                                                             "").replace(
                "'", "")

            if tip == "dict" or tip == "list":
                base[s] = base[s].apply(str)
            else:
                pass

                # Filtrar por el número de categorías únicas en cada variable
        if categoriasMaximas > 0:
            categorias_unicas = base.nunique()
            categorias_unicas = categorias_unicas.loc[categorias_unicas <=
                                                      categoriasMaximas].index
            base = base[categorias_unicas]
        else:
            raise ValueError(
                '"categoriasMaximas" tiene que un ´numero mayor a 0"')

        # Calcular qué variables tipo object tienen valores únicos menores al
        # 50% (o valor de 'limite') del total de filas del conjunto de datos original
        col_tipos = base.dtypes
        lista_tipos_unicos = []
        for s in col_tipos.index:
            unico = len(pd.unique(base[s]))
            if unico < base.shape[0] * limite:
                lista_tipos_unicos.append(s)

        # Filtrar el conjunto de datos con la lista de columnas categóricas deseadas
        base = base[lista_tipos_unicos]

        # Hacer doble loop para crear matriz de correlation tipo Cramer V
        if metodo == 'cramer':
            lista_matriz = []
            for c in lista_tipos_unicos:
                lista_fila = []
                for cc in lista_tipos_unicos:
                    try:
                        cramer = self.correlacion_cramerv(base[c], base[cc])
                        lista_fila.append(cramer)
                    except BaseException:
                        lista_fila.append(np.nan)

                lista_matriz.append(lista_fila)

            lista_matriz = pd.DataFrame(lista_matriz)
            lista_matriz.columns = lista_tipos_unicos
            lista_matriz.index = lista_tipos_unicos

            correlacion_final = lista_matriz

            # Nombre de variables en 'correlacion_final' antes de filtro
            nombres_nofiltro = list(correlacion_final.columns)

            # Quitar las columnas y filas que son 'nan'
            correlacion_final = correlacion_final.dropna(how="all", axis=1)
            correlacion_final = correlacion_final.dropna(how="all", axis=0)
            # Mencionar las variables
            nombres_filtro = list(correlacion_final.columns)
            nombres_eliminados = nombres_nofiltro.copy()
            for s in nombres_filtro:
                nombres_eliminados.remove(s)
            for s in nombres_eliminados:
                warnings.warn(
                    "no se pudo calcular la correlación con la variable '{0}'".format(s))

        elif metodo == 'phik':
            correlacion_final = base.phik_matrix()
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
