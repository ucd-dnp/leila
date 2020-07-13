# -*- coding: utf-8 -*-

# Created on Wed Sep 18 16:33:57 2019
# @author: pabmontenegro

import pandas as pd
import numpy as np
import phik
import scipy.stats as sstats


class CalidadDatos:

    def __init__(self, _base):
        """ Constructor por defecto de la clase CalidadDatos. Esta clase se \
        encarga de manejar todas las funciones asociadas a la medición de la \
        calidad de los datos en una base de datos 
        
        Parameters
        ----------
        base : pandas.DataFrame 
            Base de datos de tipo pandas.DataFrame que será
            analizada por la clase CalidadDatos.
        Returns
        -------
        CalidadDatos
            Objeto del tipo de la clase CalidadDatos
        """
        self.base = _base
        
    
    # Tipos de las columnas
    def col_tipo(self, detalle="bajo"):
        """ Retorna el tipo de dato de cada columna del dataframe, se \
            clasifican como de tipo numérico, texto, boolean u otro.
    
        :param detalle: (str) {'bajo', 'alto'}, valor por defecto: 'bajo'. \
            Indica el nivel de detalle en la descripción del tipo.
        :return: Serie de pandas con el tipo de dato de cada columna.
        """
    
        lista = [[], []]
        
        if detalle == "bajo":
            for s in self.base.columns:
                tip = str(type(self.base[s].value_counts(dropna=True).index[0]))
                lista[0].append(s)
            
                if "int" in tip or "float" in tip:
                    lista[1].append("Numérico")
                elif "str" in tip:
                    lista[1].append("Texto")
                elif "bool" in tip:
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
            return("Se ha ingresado en la opción 'detalle' un valor distinto a 'bajo' o 'alto'")
        
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
    
        if not faltantes:
            unicos_columnas = self.base.apply(lambda x: len(x.value_counts()), axis=0)
        elif faltantes:
            unicos_columnas = self.base.apply(lambda x: len(x.value_counts(dropna=False)), axis=0)
        else:
            return "La opción 'missing' tiene un valor distinto a False o True"
        return(unicos_columnas)


    # COMPLETITUD. Missing
    def ValoresFaltantes(self, porc=True):
        """ Calcula el porcentaje/número de valores faltantes de cada columna \
            del dataframe.
    
        :param porc: (bool) {True, False}, valor por defecto: True. Si el \
            valor es True el resultado se expresa como un porcentaje, si el \
                valor es False el valor se expresa como una cantidad de \
                    registros (número entero).
        :return: serie de pandas con la cantidad/porcentaje de valores \
            faltantes de cada columna.
        """
        base = self.base.copy()
        if porc:
            missing_columnas = pd.isnull(base).sum()/len(base)
        elif not porc:
            missing_columnas = pd.isnull(base).sum()
        else:
            return("La opción 'porc' tiene un valor distinto a True o False")
        return(missing_columnas)

        
    # Unicidad. Porcentaje y número de filas y columnas no únicas
    def nounicos(self, col=True, porc=True):
        """ Valida la unicidad del dataframe, retorna el porcentaje/número de \
            filas o columnas no únicas en el dataframe.
    
        :param col: (bool) {True, False}, valor por defecto: True. Si el valor \
            es True la validación se realiza por columnas, si el valor es \
                False la validación se realiza por filas.
        :param porc: (bool) {True, False}, valor por defecto: True. Si el \
            valor es True el resultado se expresa como un porcentaje, si el \
                valor es False el valor se expresa como una cantidad de \
                    registros (número entero).
        :return: (int o float) resultado de unicidad.
        """
    
        if col and porc:
            no_unic_columnas = self.base.T.duplicated(keep=False)
            cols = no_unic_columnas[no_unic_columnas].shape[0]/self.base.shape[1]
            
        elif col and not porc:
            no_unic_columnas = self.base.T.duplicated(keep=False)
            cols = no_unic_columnas[no_unic_columnas].shape[0]
            
        elif not col and porc:
            no_unic_filas = self.base.duplicated(keep=False)
            cols = no_unic_filas[no_unic_filas].shape[0]/self.base.shape[0]
            
        elif not col and not porc:
            no_unic_filas = self.base.duplicated(keep=False)
            cols = no_unic_filas[no_unic_filas].shape[0]
        else:
            return("Las opciones 'col' y 'porc' tienen valores distintos a True y False")
        
        return(cols)


    # Matching de columnas y filas no únicas
    def ValoresDuplicados(self, col=True):
        """ Retorna las columnas o filas que presenten valores duplicados del \
            dataframe.
    
        :param col: (bool) {True, False}, valor por defecto: True. Si el valor \
            es True la validación se realiza por columnas, si el valor es \
                False la validación se realiza por filas.
        :return: matriz (dataframe) que relaciona las indices de filas/nombre \
            de columnas que presentan valores duplicados.
        """
    
        if col:
            dupli = self.base.T.duplicated(keep=False)
        elif not col:
            dupli = self.base.duplicated(keep=False)
        else:
            print("El parámetro 'col' tiene valores distintos a True o False")
        
        dupli = dupli[dupli]
        if dupli.sum() == 0:
            return("No hay columnas duplicadas")
        lista_duplicados = []
        for s in dupli.index:
            for ss in dupli.index:
                if col:
                    if self.base[s].equals(self.base[ss]) and s != ss:
                        lista_duplicados.append([s, ss])
                elif not col:
                    if self.base.iloc[s].equals(self.base.iloc[ss]) and s != ss:
                        lista_duplicados.append([s, ss])
                else:
                    pass
    
        if not col:
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
        
        if col:
            lista_listas = [q for q in dic.values()]
        else:
            lista_listas = [sorted(q) for q in dic.values()]
    
        for i in range(len(lista_listas)): 
            for ii in range(len(lista_listas[i])):
                lista_listas[i][ii] = str(lista_listas[i][ii])
        
        df = pd.DataFrame(lista_listas).drop_duplicates().reset_index(drop=True)
        
        df = df.T
        
        if col:
            lista_columnas_df = ["Columnas iguales {0}".format(q) for q in range(1, df.shape[1]+1)]
            df.columns = lista_columnas_df
        else:
            lista_columnas_df = ["Filas iguales {0}".format(q) for q in range(1, df.shape[1]+1)]
            df.columns = lista_columnas_df
            
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
    
        col_tipos = self.col_tipo()
        col_num = col_tipos[col_tipos == "Numérico"].index
        base_num = self.base[col_num]
        
        if base_num.shape[1] == 0:
            print("La base de datos no contiene columnas numéricas")
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
            return("La opción extremos tiene valores distintos a 'ambos', 'superior' o 'inferior")
        
        base_outliers=pd.DataFrame(dic_outliers)
        
        if porc:
            base_outliers_porc = base_outliers.sum() / base_outliers.shape[0]
        elif not porc:
            base_outliers_porc = base_outliers.sum()
        else:
            return("La opción 'porc' tiene valores distintos a True o False")
    
        return(base_outliers_porc)


    # describe de columnas
    def descriptivas(self, float_transformar=False):
        """ Calcula estadísticas descriptivas de cada columna numérica. \
            Incluyen media, mediana, valores en distintos percentiles,\
            desviación estándar, valores extremos y porcentaje de valores \
            faltantes.
    
        :param float_transformar: (bool) {True, False}, valor por defecto: \
            True. Si el valor es True se intenta realizar una transformación \
            de valores de texto a numérico (float) para ser incluidas en \
            el análisis, si el valor es False no se intenta realizar \
            la transformación.
        :return: dataframe con las estadísticas descriptivas.
        """
        base = self.base.copy()
        if float_transformar:
            base = base.apply(lambda x: x.astype(float, errors="ignore"), axis=0)
        elif not float_transformar:
            pass
        else:
            return("La opción 'float_transform' tiene valores distintos a True o False")
    
        col_tipos = self.col_tipo()
        col_num = col_tipos[(col_tipos == "Numérico") | (col_tipos == "Float")].index
        base_num = base[col_num]
        
        if len(col_num) == 0:
            return("La base de datos no tiene columnas numéricas")
        else:
            pass
        
        base_descripcion = base.describe().T
        base_descripcion["missing"] = pd.isnull(base_num).sum() / len(base_num)
        base_descripcion["outliers_total"] = self.ValoresExtremos()
        base_descripcion["outliers_altos"] = self.ValoresExtremos(extremos="superior")
        base_descripcion["outliers_bajos"] = self.ValoresExtremos(extremos="inferior")
    
        return(base_descripcion)


    ###############
    def varianza_percentil(self, percentil_inferior=5, percentil_superior=95, 
                           float_transform=False):
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
        if float_transform:
            base = base.apply(lambda x: x.astype(float,errors="ignore"), axis=0)
        elif not float_transform:
            pass
        else:
            return("La opción 'float_transform' tiene valores distintos a True o False")
    
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
            return("No hay ninguna columna numérica que tenga el percentil {0} y el percentil {1} igual".format(percentil_inferior,percentil_superior))
        else:
            return(percentiles_true.index)


    # tabla de valores únicos para cada variable de texto
    def categorias(self, limite=0.5, transformar_nums=False, variables=None):
        """ Genera una tabla con los primeros 10 valores más frecuentes de las \
            columnas de tipo texto del dataframe, además calcula su frecuencia \
            y porcentaje dentro del total de observaciones. Incluye los \
            valores faltantes.
    
        :param limite: (float) (valor de 0 a 1) límite de referencia, se \
            utiliza para determinar si las variables posiblemente son de tipo \
            categóricas y ser incluidas en el análisis. Si el número de \
            valores únicos por columna es mayor al número de registros \
                * limite*, se considera que la variable no es categórica.
        :param transformar_nums: (bool) {True, False}, determina si se desea \
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
        
        # Calcular qué variables tipo object tienen valores únicos menores al 50% (o valor de 'limite') del total de filas de la base original
        col_object = base.dtypes
        col_object = col_object[col_object == "object"]
        lista_object_unicos = []
        for s in col_object.index:
            unico = len(pd.unique(base[s]))
            if unico < base.shape[0]*limite:
                lista_object_unicos.append(s)
                
        # Si la opción 'transformar_nums' es True, incluir las variables numéricas con repeticiones menores al 50% (o el límite) del total de filas   
        if transformar_nums:
            cols_types = base.dtypes
            col_nums = []
            for i in range(len(cols_types)):
                if "int" in str(cols_types[i]) or "float" in str(cols_types[i]):
                    col_nums.append(cols_types.index[i])
            for s in col_nums:
                unico = len(pd.unique(base[s]))
                if unico < base.shape[0]*limite:
                    lista_object_unicos.append(s)
        elif not transformar_nums:
            pass
        else:
            return("La opción 'transformar_nums' tiene un valor distinto a True o False")
        
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
    def memoria(self, col=False):
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
            return("La opción 'col' tiene un valor distinto a True o False")
        memoria_mb = memoria_/(1024**2)
        return(memoria_mb)


    # tabla de resumen pequeña
    def resumen(self, filas=True, columnas=True, col_numericas=True, 
                col_texto=True, col_booleanas=True, col_fecha=True, 
                col_otro=True, filas_nounicas=True, columnas_nounicas=False,
                col_faltantes=True, col_extremos=True, memoria_total=True):
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
        :param col_numericas: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de tipo numéricas.
        :param col_texto: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de tipo texto.
        :param col_booleanas: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de tipo boolean.
        :param col_fecha: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de tipo fecha.
        :param col_otro: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas de otro tipo deferente \
            a los anteriores.
        :param filas_nounicas: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de filas no únicas.
        :param columnas_nounicas: (bool) {True, False}, valor por defecto: \
            False. Indica si se incluye el número de columnas no únicas.
        :param col_faltantes: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas con más de la mitad de \
            las observaciones con datos faltantes.
        :param col_extremos: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el número de columnas con más del 10% de \
                observaciones con datos extremos.
        :param memoria_total: (bool) {True, False}, valor por defecto: True. \
            Indica si se incluye el cálculo del tamaño de la base de datos en memoria.
        :return: serie de pandas con las estadísticas descriptivas del dataframe.
        """
    
        # Lista donde se guardarán resultados, dependiendo de si se escoge o no ver el cálculo
        lista_resumen = [[], []]
        base = self.base.copy()
        # Calcular tipo de columnas
        col_tipos = self.col_tipo()
        
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
        if col_numericas:
            calculo = len(col_tipos[col_tipos == "Numérico"])
            nombre = "Columnas numéricas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass 
           
        # Número de columnas de texto
        if col_texto:
            calculo = len(col_tipos[col_tipos == "Texto"])
            nombre = "Columnas de texto"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass   
         
        # Número de columnas booleanas
        if col_booleanas:
            calculo = len(col_tipos[col_tipos == "Boolean"])
            nombre = "Columnas booleanas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass        
    
        # Número de columnas de fecha
        if col_fecha:
            calculo = len(col_tipos[col_tipos == "Fecha"])
            nombre = "Columnas de fecha"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass 
           
        # Número de columnas de otro tipo
        if col_otro:
            calculo = len(col_tipos[col_tipos == "Otro"])
            nombre = "Otro tipo de columnas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass        
       
        # Número de filas no únicas
        if filas_nounicas:
            calculo = self.nounicos(col=False, porc=False)
            nombre = "Número de filas no únicas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass  
          
        # Número de columnas no únicas
        if columnas_nounicas:
            calculo = self.nounicos(col=True, porc=False)
            nombre = "Número de columnas no únicas"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass        
    
        # Porcentaje de columnas con más de la mitad de datos faltantes
        if col_faltantes:
            col_missing = self.ValoresFaltantes(porc=True)
            calculo = len(col_missing[col_missing > 0.5])
            nombre = "Columnas con más de la mitad de datos faltantes"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass     
        
        # Columnas con más del 10% de datos como extremos
        if col_extremos:
            col_porc = self.ValoresExtremos(extremos="ambos", porc=True)
            calculo = len(col_porc[col_porc > 0.1])
            nombre = "Columnas con más del 10% de datos como extremos"
            lista_resumen[0].append(nombre)
            lista_resumen[1].append(calculo)
        else:
            pass         
        
        # Tamaño de la base en la memoria
        if memoria_total:
            memoria_tot = self.memoria()
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
    def correlacion(self, metodo="pearson", variables=None):
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
        col_tipos = self.col_tipo()
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
            return("El parámetro 'metodo' tiene valores diferentes a 'pearson', 'kendall' o 'spearman")
        
        return correlacion_
    

    # Matrices de correlación para variables categóricas
    def correlacion_categoricas(self, categorias_maximas=30, limite=0.5, 
                                variables=None,tipo='cramer',
                                columnas_intervalo=None):
        """ Genera una matriz de correlación entre las variables de tipo categórico

        :param categorias_maximas:
        :param limite:
        :param variables:
        :param tipo:
        :param columnas_intervalo:
        :return:
        """
        
        base=self.base.copy()
        
        # Filtrar la base por las variables escogidas en la opción 'variables'
        if type(variables) == list:
            base = base[variables]
        else:
            pass
        
        # Filtrar por el número de categorías únicas en cada variable
        if categorias_maximas>0:
            categorias_unicas=base.nunique()
            categorias_unicas=categorias_unicas.loc[categorias_unicas<=categorias_maximas].index
            base=base[categorias_unicas]
        else:
            pass
                
        # Calcular qué variables tipo object tienen valores únicos menores al 50% (o valor de 'limite') del total de filas de la base original
        col_tipos = base.dtypes
        lista_tipos_unicos = []
        for s in col_tipos.index:
            unico = len(pd.unique(base[s]))
            if unico < base.shape[0]*limite:
                lista_tipos_unicos.append(s)
        
        # Filtrar la base con la lista de columnas categóricas deseadas
        lista_tipos_unicos=lista_tipos_unicos
        base=base[lista_tipos_unicos]
        
        # Hacer doble loop para crear matriz de correlation tipo Cramer V
        if tipo=='cramer':
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
        
        elif tipo=='phik':
            correlacion_final=base.phik_matrix(interval_cols=columnas_intervalo)
        
        return correlacion_final
        
    # Función de soporte para calcular coeficiente de correlación Cramer V 
    #(para usar en la función de las matrices de correlación entre variables categóricas)
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

    