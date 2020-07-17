# -*- coding: utf-8 -*-

# Created on Wed Sep 18 16:33:57 2019
# @author: pabmontenegro

import pandas as pd
import numpy as np
import phik
import scipy.stats as sstats
import warnings


class CalidadDatos:

    def __init__(self, _base,castFloat=False,diccionarioCast=None,errores="ignore",formato_fecha=None):
        """ Constructor por defecto de la clase CalidadDatos. Esta clase se \
        encarga de manejar todas las funciones asociadas a la medición de la \
        calidad de los datos en una base de datos 
        
        Parameters
        ----------
        base : pandas.DataFrame 
            Base de datos de tipo pandas.DataFrame que será
            analizada por la clase CalidadDatos.
        param castFloat: (bool) {True, False}. Valor por defecto: False \
            Indica si se desea convertir las columnas de tipos object y \
            bool a float, de ser posible
        param diccionarioCast: (dict) { {nombre_columna : tipo_columna} } \
            Diccionario donde se especifican los tipos a que se desean \
            convertir las columnas (string, numerico, booleano, fecha, \
            categorico)
        param errores: (string) {'ignore', 'coerce', 'raise'}\
            Valor por defecto: 'ignore'. Indica qué hacer con las columnas \
            cuyo tipo no se puede cambiar al solicitado en \
            'diccionarioCast'
        
        Returns
        -------
        CalidadDatos
            Objeto del tipo de la clase CalidadDatos
        """
        
        # Pasar los 'objects' a float, si posible
        if castFloat==True:
            tipos_columnas=_base.dtypes
            tipos_object=tipos_columnas[(tipos_columnas=="object")|(tipos_columnas=="bool")].index.to_list()
            _base[tipos_object]=_base[tipos_object].apply(lambda x:x.astype(float,errors="ignore"),axis=0)
        elif castFloat==False:
            pass
        else:
            raise ValueError('"castFloat" tiene que ser True o False')
        
        # Cambiar los tipos de las variables según el diccionario
        if type(diccionarioCast)==dict:
            for s in diccionarioCast:
        
                if diccionarioCast[s]=="string":
                    _base[s]=_base[s].apply(lambda x:str(x))
                elif diccionarioCast[s]=="numerico":
                    _base[s]=pd.to_numeric(_base[s],errors=errores)
                elif diccionarioCast[s]=="booleano":
                    _base[s]=_base[s].astype("bool")
                elif diccionarioCast[s]=="fecha":
                    _base[s]=pd.to_datetime(_base[s],format=formato_fecha,errors=errores)
                elif diccionarioCast[s]=="categorico":
                    _base[s]=pd.Categorical(_base[s])
                else:
                    raise ValueError('Las llaves de "diccionarioCast" tienen que ser "string", "numerico", "booleano", "fecha" o "categorico" ')
        elif diccionarioCast is None:
            pass
        else:
            raise ValueError('"diccionario" tiene que ser tipo "dict"')

        self.base = _base
        
    
    # Tipos de las columnas
    def TipoColumnas(self, detalle="bajo"):
        """ Retorna el tipo de dato de cada columna del dataframe, se \
            clasifican como de tipo numérico, texto, boolean u otro.
    
        :param detalle: (str) {'bajo', 'alto'}, valor por defecto: 'bajo'. \
            Indica el nivel de detalle en la descripción del tipo.
        :return: Serie de pandas con el tipo de dato de cada columna.
        """
    
        lista = [[], []]
        
        if detalle == "bajo":
            for s in self.base.columns:
                tipo_para_object = str(type(self.base[s].value_counts(dropna=True).index[0]))
                tipo_para_resto = str(self.base[s].dtype)
                
                lista[0].append(s)
                
                if "int" in tipo_para_resto or "float" in tipo_para_resto:
                    lista[1].append("Numérico")
                elif "str" in tipo_para_object:
                    lista[1].append("Texto")
                elif "bool" in tipo_para_resto:
                    lista[1].append("Boolean")
                # elif ""
                else:
                    lista[1].append("Otro")
                 
        elif detalle == "alto":
            for s in self.base.columns:
                tip = str(type(self.base[s].value_counts(dropna=True).index[0])).replace("<class ", "").replace(">", "").replace("'", "'")
                lista[0].append(s)
                lista[1].append(tip)
    
        else:
            raise ValueError('"detalle" tiene que ser "bajo" o "alto"')     
        
        tips = pd.DataFrame(lista).T.set_index(keys=0, drop=True).iloc[:, 0]
        return(tips)


    # valores únicos en cada columna
    # sin missing values
    def ValoresUnicos(self, faltantes=False):
        """ Calcula la cantidad de valores únicos de cada columna del dataframe.
    
        :param faltantes: (bool) {True, False}, valor por defecto: False. \
            Indica si desea tener en cuenta los valores faltantes en el \
                conteo de valores únicos.
        :return: serie de pandas con la cantidad de valores únicos de cada columna.
        """
    
        if faltantes==False:
            unicos_columnas = self.base.apply(lambda x: len(x.value_counts()), axis=0)
        elif faltantes==True:
            unicos_columnas = self.base.apply(lambda x: len(x.value_counts(dropna=False)), axis=0)
        else:
            raise ValueError('"faltantes" tiene que ser True o False')     

        return(unicos_columnas)


    #  Missing values
    def ValoresFaltantes(self, porc=True):
        """ Calcula el porcentaje/número de valores faltantes de cada columna \
            del dataframe.
    
        :param cociente: (bool) {True, False}, valor por defecto: True. Si el \
            valor es True el resultado se expresa como un cociente, si el \
                valor es False el valor se expresa como una cantidad de \
                    registros (número entero).
        :return: serie de pandas con la cantidad/cociente de valores \
            faltantes de cada columna.
        """
        base = self.base.copy()
        
        if porc==True:
            missing_columnas = pd.isnull(base).sum()/len(base)
        elif porc==False:
            missing_columnas = pd.isnull(base).sum()
        else:
            raise ValueError('"cociente" tiene que ser True o False')
            
        return(missing_columnas)

        
    # Porcentaje y número de filas y columnas no únicas
    def CantidadDuplicados(self, eje=0, porc=True):
        """ Retorna el porcentaje/número de \
            filas o columnas duplicadas (repetidas) en el dataframe.
    
        :param eje: (int) {1, 0}, valor por defecto: 0. Si el valor \
            es 1 la validación se realiza por columnas, si el valor es \
                0 la validación se realiza por filas.
        :param porc: (bool) {True, False}, valor por defecto: True. Si el \
            valor es True el resultado se expresa como un cociente, si el \
                valor es False el valor se expresa como una cantidad de \
                    registros (número entero).
        :return: (int o float) resultado de unicidad.
        """
        base=self.base.copy()
        
        # Revisar si hay columnas con tipos diccionario o lista para convertirlas a string
        tipo_columnas=self.TipoColumnas(detalle="alto")
        for s in tipo_columnas.index:
            if tipo_columnas[s]=="'dict'" or tipo_columnas[s]=="'list'":
                base[s]=base[s].apply(lambda x:str(x))
            else:
                pass
            
        # Porcentaje de columnas repetidas
        if eje==1 and porc==True:
            no_unic_columnas = base.T.duplicated(keep="first")
            cols = no_unic_columnas[no_unic_columnas].shape[0]/base.shape[1]
        
        # Número de columnas repetidas
        elif eje==1 and porc==False:
            no_unic_columnas = base.T.duplicated(keep="first")
            cols = no_unic_columnas[no_unic_columnas].shape[0]
        
        # Porcentaje de filas repetidas
        elif eje==0 and porc==True:
            no_unic_filas = base.duplicated(keep="first")
            cols = no_unic_filas[no_unic_filas].shape[0]/base.shape[0]
        
        # Número de filas repetidas
        elif eje==0 and porc==False:
            no_unic_filas = base.duplicated(keep="first")
            cols = no_unic_filas[no_unic_filas].shape[0]
            
        else:
            raise ValueError('"eje" tiene que ser 1 o 0 y "porc" tienen que ser True o False')
        
        return(cols)


    # Matching de columnas y filas no únicas
    def EmparejamientoDuplicados(self, col=False):
        """ Retorna las columnas o filas que presenten valores duplicados del \
            dataframe.
    
        :param col: (bool) {True, False}, valor por defecto: False. Si el valor \
            es True la validación se realiza por columnas, si el valor es \
                False la validación se realiza por filas.
        :return: matriz (dataframe) que relaciona las indices de filas/nombre \
            de columnas que presentan valores duplicados.
        """
        base=self.base.copy()
    
        # Revisar si hay columnas con tipos diccionario para convertirlas a string
        tipo_columnas=self.TipoColumnas(detalle="alto")
        for s in tipo_columnas.index:
            if tipo_columnas[s]=="'dict'" or tipo_columnas[s]=="'list'":
                base[s]=base[s].apply(lambda x:str(x))
            else:
                pass
        
        # Obtener todos los duplicados, sin hacer todavía el emparejamiento
        if col==True:
            dupli = base.T.duplicated(keep=False)
        elif col==False:
            dupli = base.duplicated(keep=False)
        else:
            raise ValueError('"col" tiene que ser True o False')
        
        dupli = dupli[dupli]
        if dupli.sum() == 0:
            print("No hay columnas duplicadas")
            return
        lista_duplicados = []
        for s in dupli.index:
            for ss in dupli.index:
                if col==True:
                    if base[s].equals(base[ss]) and s != ss:
                        lista_duplicados.append([s, ss])
                elif col==False:
                    if base.iloc[s].equals(base.iloc[ss]) and s != ss:
                        lista_duplicados.append([s, ss])
                else:
                    pass
    
        if col==False:
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
        
        if col==True:
            lista_listas = [q for q in dic.values()]
        else:
            lista_listas = [sorted(q) for q in dic.values()]
    
        for i in range(len(lista_listas)): 
            for ii in range(len(lista_listas[i])):
                lista_listas[i][ii] = str(lista_listas[i][ii])
        
        df = pd.DataFrame(lista_listas).drop_duplicates().reset_index(drop=True)
        
        df = df.T
        
        if col==True:
            lista_columnas_df = ["Columnas iguales {0}".format(q) for q in range(1, df.shape[1]+1)]
            df.columns = lista_columnas_df
        else:
            lista_columnas_df = ["Filas iguales {0}".format(q) for q in range(1, df.shape[1]+1)]
            df.columns = lista_columnas_df
        
        # Quitar los 'nan' del
        df=df.apply(lambda x:x.replace(np.nan,""))
        
        return(df)


    # CONSISTENCIA. Porcentaje de outliers
    def ValoresExtremos(self, extremos="ambos", porc=True):
        """ Calcula el porcentaje o cantidad de outliers de cada columna numérica \
            (las columnas con números en formato string se intentarán transformar \
            a columnas numéricas)
    
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
        :param porc: (bool) {True, False}, valor por defecto: True. Si el valor es \
            True el resultado se expresa como un porcentaje, si el valor es False el \ 
            valor se expresa como una cantidad de registros (número entero).
        :return: serie de pandas con la cantidad/porcentaje de valores outliers \
            de cada columna.
        """
    
        col_tipos = self.TipoColumnas()
        col_num = col_tipos[col_tipos == "Numérico"].index
        base_num = self.base[col_num]
        
        if base_num.shape[1] == 0:
            print("La base de datos no contiene columnas numéricas")
            return
        else:
            pass
        
        porcentiles_25 = base_num.apply(lambda x:np.nanpercentile(x,25),axis=0)
        porcentiles_75 = base_num.apply(lambda x:np.nanpercentile(x,75),axis=0)
        
        iqr = porcentiles_75-porcentiles_25
        iqr_upper = porcentiles_75+iqr*1.5
        iqr_lower = porcentiles_25-iqr*1.5
    
        dic_outliers = {}
        
        if extremos == "ambos":
            for i in range(0, len(iqr)):
                dic_outliers[base_num.columns[i]] = (base_num.iloc[:, i] > iqr_upper[i]) | (base_num.iloc[:, i] < iqr_lower[i])
        elif extremos == "superior":
            for i in range(0, len(iqr)):
                dic_outliers[base_num.columns[i]] = (base_num.iloc[:, i] > iqr_upper[i])
        elif extremos == "inferior":
            for i in range(0, len(iqr)):
                dic_outliers[base_num.columns[i]] = (base_num.iloc[:, i] < iqr_lower[i])
        else:
            raise ValueError('"extremos" tiene que ser "ambos", "superior" o "inferior"')
        
        base_outliers=pd.DataFrame(dic_outliers)
        
        if porc:
            base_outliers_porc = base_outliers.sum() / base_outliers.shape[0]
        elif not porc:
            base_outliers_porc = base_outliers.sum()
        else:
            raise ValueError('"porc" tiene que ser True o False')
    
        return(base_outliers_porc)


    # describe de columnas
    def DescripcionNumericas(self, variables=None):
        """ Calcula estadísticas descriptivas de cada columna numérica. \
            Incluyen media, mediana, valores en distintos percentiles,\
            desviación estándar, valores extremos y porcentaje de valores \
            faltantes.
        :param variables: (list) lista de nombres de las columnas separados \
            por comas. Permite escoger las columnas de interés de análisis \
            del dataframe
            
        :return: dataframe con las estadísticas descriptivas.
        """
        base = self.base.copy()
    
        # Filtrar la base por las variables escogidas en la opción 'variables'
        if type(variables) == list:
            base = base[variables]
        else:
            pass    
    
        col_tipos = self.TipoColumnas()
        col_num = col_tipos[(col_tipos == "Numérico") | (col_tipos == "Float")].index
        base_num = base[col_num]
        
        if len(col_num) == 0:
            print("La base de datos no tiene columnas numéricas")
            return
        else:
            pass
        
        base_descripcion = base.describe().T
        base_descripcion["missing"] = pd.isnull(base_num).sum() / len(base_num)
        base_descripcion["outliers_total"] = self.ValoresExtremos()
        base_descripcion["outliers_altos"] = self.ValoresExtremos(extremos="superior")
        base_descripcion["outliers_bajos"] = self.ValoresExtremos(extremos="inferior")
    
        return(base_descripcion)


    ###############
    def VarianzaEnPercentil(self, percentil_inferior=5, percentil_superior=95):
        """ Retorna las columnas numéricas cuyo percentil_inferior sea igual \
            a su percentil_superior.
    
        :param base: (dataframe) base de datos de interés a ser analizada.
        :param percentil_inferior: (float), valor por defecto: 5. Percentil \
            inferior de referencia en la comparación.
        :param percentil_superior: (float), valor por defecto: 95. Percentil \
            superior de referencia en la comparación.
        :return: indices de columnas cuyo percentil inferior es igual al \
            percentil superior.
        """
        base =self.base.copy()
    
        cols_tipos = base.dtypes
        lista_nums = []
        for i in range(len(cols_tipos)):
            if "int" in str(cols_tipos[i]) or "float" in str(cols_tipos[i]):
                lista_nums.append(cols_tipos.index[i])
        base_num = base[lista_nums]
        for c in base_num.columns:
            if base_num[c].isnull().sum() == base_num.shape[0]:
                del base_num[c]
            else:
                pass
            
        percentil_bajo = base_num.apply(lambda x: np.percentile(x.dropna(), 5), axis=0)
        percentil_alto = base_num.apply(lambda x: np.percentile(x.dropna(), 95), axis=0)
        
        percentiles = pd.concat([percentil_bajo, percentil_alto], axis=1)
        percentiles_true = (percentiles.iloc[:, 0] == percentiles.iloc[:, 1])
        percentiles_true = percentiles_true[percentiles_true  == True]
        
        if len(percentiles_true) == 0:
            print("No hay ninguna columna numérica que tenga el percentil {0} y el percentil {1} igual".format(percentil_inferior,percentil_superior))
            return
        else:
            return(percentiles_true.index)


    # tabla de valores únicos para cada variable de texto
    def DescripcionCategoricas(self, limite=0.5, categoriasMaximas=30, incluirNumericos=True, variables=None):
        """ Genera una tabla con los primeros 10 valores más frecuentes de las \
            columnas categóricas dataframe , además calcula su frecuencia \
            y porcentaje dentro del total de observaciones. Incluye los \
            valores faltantes.
    
        :param limite: (float) (valor de 0 a 1) límite de referencia, se \
            utiliza para determinar si las variables posiblemente son de tipo \
            categóricas y ser incluidas en el análisis. Si el número de \
            valores únicos por columna es mayor al número de registros \
            * limite*, se considera que la variable no es categórica.
        :param categoriasMaximas: (int) (valor mayor a 0), indica el máximo \
            número de categorías de una variable para que sea incluida en el \
            análisis
        :param incluirNumericos: (bool) {True, False}, determina si se desea \
            considerar las variables como categóricas e incluirlas en el \
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
        
        # Filtrar la base por las variables escogidas en la opción 'variables'
        if type(variables) == list:
            base = base[variables]
        else:
            pass
        
        # Filtrar por el número de categorías únicas en cada variable
        if categoriasMaximas>0:
            categorias_unicas=base.nunique()
            categorias_unicas=categorias_unicas.loc[categorias_unicas<=categoriasMaximas].index
            base=base[categorias_unicas]
        else:
            raise ValueError('"categoriasMaximas" tiene que un ´numero mayor a 0"')

        # Calcular qué variables tipo object tienen valores únicos menores al 50% (o valor de 'limite') del total de filas de la base original
        col_object = base.dtypes
        col_object = col_object[col_object == "object"]
        lista_object_unicos = []
        for s in col_object.index:
            unico = len(pd.unique(base[s]))
            if unico < base.shape[0]*limite:
                lista_object_unicos.append(s)
                
        # Si la opción 'transformar_nums' es True, incluir las variables numéricas con repeticiones menores al 50% (o el límite) del total de filas   
        if incluirNumericos==True:
            cols_types = base.dtypes
            col_nums = []
            for i in range(len(cols_types)):
                if "int" in str(cols_types[i]) or "float" in str(cols_types[i]):
                    col_nums.append(cols_types.index[i])
            for s in col_nums:
                unico = len(pd.unique(base[s]))
                if unico < base.shape[0]*limite:
                    lista_object_unicos.append(s)
        elif incluirNumericos==False:
            pass
        else:
            raise ValueError('"incluirNumericos" tiene que ser True o False')
        
        # Crear el dataframe con la información
        lista_counts = []
        for s in lista_object_unicos:
            counts = base[s].astype(str).value_counts().drop("nan", errors="ignore")
            if type(counts.index[0]) == dict:
                continue
            # counts=list(counts)
            lista = counts[0:10]
            resto = sum(counts[10:len(counts)])
            miss = pd.isnull(base[s]).sum()
    
            lista["Demás categorías"] = resto
            lista["Datos faltantes"] = miss
            # lista["Total de categorías (con NA)"]=len(pd.unique(base[s]))
    
            lista = lista.to_frame()
            lista["Columna"] = s
            lista["Porcentaje del total de filas"] = lista[s]/len(base)
                
            resto = lista.iloc[:, 0].loc["Demás categorías"]
            
            if resto == 0:
                lista = lista.drop("Demás categorías", axis=0)
    
            lista = lista.reset_index()
            
            s = lista.columns.tolist()[1]
            colis = ["Columna", "index", s, "Porcentaje del total de filas"]
            lista = lista[colis]
            lista_cols = lista.columns.tolist()
            lista = lista.rename(columns={"index": "Valor", lista_cols[2]: "Frecuencia"})
            lista_counts.append(lista)
        df_counts = pd.concat(lista_counts, axis=0)
        return(df_counts)


    # Tamaño de la base de datos en la memoria
    def Memoria(self, col=False):
        """ Calcula el tamaño de la base de datos en memoria (megabytes)
    
        :param col: (bool) {True, False}, valor por defecto: False. Si el \
            valor es False realiza el cálculo de memoria del dataframe \
            completo, si el valor es True realiza el cálculo de memoria por \
            cada columna del dataframe.
        :return: valor (float) del tamaño de la base de datos en megabytes \
            (si el parámetro col es False). Serie de pandas con el cálculo de \
            memoria en megabytes por cada columna del dataframe. (si el \
            parámetro col es True).
        """
        base = self.base.copy()
        if not col:
            memoria_ = base.memory_usage(index=True).sum()
        elif col:
            memoria_ = base.memory_usage(index=True)
        else:
            raise ValueError('"col" tiene que ser True o False')
        memoria_mb = memoria_/(1024**2)
        return(memoria_mb)


    # tabla de resumen pequeña
    def Resumen(self, filas=True, columnas=True, colNumericas=True, 
                colTexto=True, colBooleanas=True, colFecha=True, 
                colOtro=True, filasRepetidas=True, columnasRepetidas=False,
                colFaltantes=True, colExtremos=True, memoriaTotal=True):
        """ Retorna una tabla con información general de la base de datos.\
        Incluye número de filas y columnas, número de columnas de tipo \
        numéricas, de texto, booleanas, fecha y otros, número de filas y \
        columnas no únicas, número de columnas con más de la mitad de las \
        observaciones con datos faltantes, número de columnas con más del \
        10% de observaciones con datos extremos y el tamaño de la base de \
        datos en memoria.
    
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
            Indica si se incluye el cálculo del tamaño de la base de datos en memoria.
        :return: serie de pandas con las estadísticas descriptivas del dataframe.
        """
    
        # Lista donde se guardarán resultados, dependiendo de si se escoge o no ver el cálculo
        lista_resumen = [[], []]
        base = self.base.copy()
        # Calcular tipo de columnas
        col_tipos = self.TipoColumnas()
        
        # Agregar a lista, si se escoge que sea así
        
        # Número de filas
        if filas:
            calculo = base.shape[0]
            nombre = "Número de filas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass  
          
        # Número de columnas
        if columnas:
            calculo = base.shape[1]
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
            calculo = self.CantidadDuplicados(eje=0, porc=False)
            nombre = "Número de filas repetidas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass  
          
        # Número de columnas no únicas
        if columnasRepetidas:
            calculo = self.CantidadDuplicados(eje=1, porc=False)
            nombre = "Número de columnas repetidas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass        
    
        # Porcentaje de columnas con más de la mitad de datos faltantes
        if colFaltantes:
            col_missing = self.ValoresFaltantes(porc=True)
            calculo = len(col_missing[col_missing > 0.5])
            nombre = "Columnas con más de la mitad de datos faltantes"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass     
        
        # Columnas con más del 10% de datos como extremos
        if colExtremos:
            col_porc = self.ValoresExtremos(extremos="ambos", porc=True)
            calculo = len(col_porc[col_porc > 0.1])
            nombre = "Columnas con más del 10% de datos como extremos"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass         
        
        # Tamaño de la base en la memoria
        if memoriaTotal:
            memoria_tot = self.Memoria()
            if memoria_tot > 1024:
                memoria_tot = memoria_tot/1024
                nombre = "Tamaño de la base en gygabytes (redondeado)"
            else:
                nombre = "Tamaño de la base en megabytes (redondeado)"
            calculo = memoria_tot
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass         
        
        tabla_resumen = pd.Series(data=lista_resumen[1],index=lista_resumen[0]).astype(int)
        return(tabla_resumen)



    # Matrices de correlación para las variables numéricas
    def CorrelacionNumericas(self, metodo="pearson", variables=None):
        """ Genera una matriz de correlación entre las variables de tipo numérico
    
        :param metodo: (str) {'pearson', 'kendall', 'spearman'}, valor por \
            defecto: 'pearson'. Medida de correlación a utilizar.
        :param variables: (list) lista de nombres de las columnas separados \
            por comas. Permite escoger las columnas de interés de análisis \
            del dataframe
        :return: dataframe con las correlaciones de las columnas de tipo \
            numérico analizadas.
        """
        base = self.base.copy()
        
        # Filtrar la base por las variables escogidas en la opción 'variables'
        if type(variables) == list:
            base = base[variables]
        else:
            pass
        
        # Filtrar por columnas que sean numéricas
        col_tipos = self.TipoColumnas()
        col_num = col_tipos[col_tipos == "Numérico"].index
        base_num = base[col_num]
        
        # Crear la matriz de correlación dependiendo del método escogido
        if metodo == "pearson":
            correlacion_ = base_num.corr(method="pearson")
        elif metodo == "kendall":
            correlacion_ = base_num.corr(method="kendall")
        elif metodo == "spearman":
            correlacion_ = base_num.corr(method="spearman")
        else:
            raise ValueError('"metodo" tiene que ser "pearson", "kendall" o "spearman>"')
        
        return correlacion_
    

    # Matrices de correlación para variables categóricas
    def CorrelacionCategoricas(self,metodo='phik', limite=0.5, categoriasMaximas=30,variables=None):
        """ Genera una matriz de correlación entre las variables de tipo categóricas
    
        :param metodo: (str) {'phik', 'cramer'}, valor por \
            defecto: 'phik'. Medida de correlación a utilizar.   
        :param limite: (float) (valor de 0 a 1) límite de referencia, se \
            utiliza para determinar si las variables posiblemente son de tipo \
            categóricas y ser incluidas en el análisis. Si el número de \
            valores únicos por columna es mayor al número de registros \
            * limite*, se considera que la variable no es categórica.
        :param categoriasMaximas: (int) (valor mayor a 0), indica el máximo \
            número de categorías de una variable para que sea incluida en el \
            análisis            
        :param variables: (list) lista de nombres de las columnas separados \
            por comas. Permite escoger las columnas de interés de análisis \
            del dataframe
        :return: dataframe con las correlaciones de las columnas de tipo \
            categórica analizadas.
        """
        base=self.base.copy()
        
        # Filtrar la base por las variables escogidas en la opción 'variables'
        if type(variables) == list:
            base = base[variables]
        else:
            pass
        
        # Revisar si hay columnas con tipos diccionario o lista para convertirlas a string
        tipo_columnas=self.TipoColumnas(detalle="alto")
        for s in tipo_columnas.index:
            if tipo_columnas[s]=="'dict'" or tipo_columnas[s]=="'list'":
                base[s]=base[s].apply(lambda x:str(x))
            else:
                pass        
        
        # Filtrar por el número de categorías únicas en cada variable
        if categoriasMaximas>0:
            categorias_unicas=base.nunique()
            categorias_unicas=categorias_unicas.loc[categorias_unicas<=categoriasMaximas].index
            base=base[categorias_unicas]
        else:
            raise ValueError('"categoriasMaximas" tiene que un ´numero mayor a 0"')
                
        # Calcular qué variables tipo object tienen valores únicos menores al 50% (o valor de 'limite') del total de filas de la base original
        col_tipos = base.dtypes
        lista_tipos_unicos = []
        for s in col_tipos.index:
            unico = len(pd.unique(base[s]))
            if unico < base.shape[0]*limite:
                lista_tipos_unicos.append(s)
        
        # Filtrar la base con la lista de columnas categóricas deseadas
        base=base[lista_tipos_unicos]
        
        # Hacer doble loop para crear matriz de correlation tipo Cramer V
        if metodo=='cramer':
            lista_matriz=[]
            for c in lista_tipos_unicos:
                lista_fila=[]
                for cc in lista_tipos_unicos:
                    cramer=self.correlacion_cramerv(base[c],base[cc])
                    lista_fila.append(cramer)
                
                lista_matriz.append(lista_fila)
                
            lista_matriz=pd.DataFrame(lista_matriz)
            lista_matriz.columns=lista_tipos_unicos
            lista_matriz.index=lista_tipos_unicos
            
            correlacion_final=lista_matriz
            
            # Nombre de variables en 'correlacion_final' antes de filtro
            nombres_nofiltro=list(correlacion_final.columns)
            
            # Quitar las columnas y filas que son 'nan' 
            correlacion_final=correlacion_final.dropna(how="all",axis=1)
            correlacion_final=correlacion_final.dropna(how="all",axis=0)
            # Mencionar las variables 
            nombres_filtro=list(correlacion_final.columns)
            nombres_eliminados=nombres_nofiltro.copy()
            for s in nombres_filtro:
                nombres_eliminados.remove(s)
            for s in nombres_eliminados:
                warnings.warn("no se pudo calcular la correlación con la variable '{0}'".format(s))
                
        elif metodo=='phik':
            correlacion_final=base.phik_matrix()
        else:
            raise ValueError('"metodo" tiene que ser "phik" o "cramer"')
        
        return correlacion_final
      
    # Función de soporte para calcular coeficiente de correlación Cramer V 
    # (para usar en la función de las matrices de correlación entre variables categóricas)
    # poner privada.
    def correlacion_cramerv(self, x, y):
        confusion_matrix = pd.crosstab(x,y)
        chi2 = sstats.chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum().sum()
        phi2 = chi2/n
        r,k = confusion_matrix.shape
        phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
        rcorr = r-((r-1)**2)/(n-1)
        kcorr = k-((k-1)**2)/(n-1)
        return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))    

