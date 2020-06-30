# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:33:57 2019

@author: pabmontenegro
"""
import pandas as pd
import numpy as np

## Tipos de las columnas
def col_tipo(base,detalle="bajo"):
    lista=[[],[]]
    
    if detalle=="bajo":
        
        for s in base.columns:
            tip=str(type(base[s].value_counts(dropna=True).index[0]))
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
             
    elif detalle=="alto":
        
        for s in base.columns:
            tip=str(type(base[s].value_counts(dropna=True).index[0])).replace("<class ","").replace(">","").replace("'","'")
            lista[0].append(s)
            lista[1].append(tip)

    else:
        return("Se ha ingresado en la opción 'detalle' un valor distinto a 'bajo' o 'alto'")
    
    tips=pd.DataFrame(lista).T.set_index(keys=0,drop=True).iloc[:,0]
            
    return(tips)

########## valores únicos en cada columna
# sin missing values
def unicos(base,faltantes=False):
    if faltantes==False:
        unicos_columnas=base.apply(lambda x:len(x.value_counts()),axis=0)
    elif faltantes==True:
        unicos_columnas=base.apply(lambda x:len(x.value_counts(dropna=False)),axis=0)
    else:
        return("La opción 'missing' tiene un valor distinto a False o True")
    return(unicos_columnas)
    
########## COMPLETITUD. Missing 
def faltantes(base,porc=True):
    if porc==True:
        missing_columnas=pd.isnull(base).sum()/len(base)
    elif porc==False:
        missing_columnas=pd.isnull(base).sum()
    else:
        return("La opción 'porc' tiene un valor distinto a True o False")
    return(missing_columnas)

        
########## Unicidad. Porcentaje y número de filas y columnas no únicas
def nounicos(base,col=True,porc=True):
    if col==True and porc==True:
        no_unic_columnas=base.T.duplicated(keep=False)
        cols=no_unic_columnas[no_unic_columnas==True].shape[0]/base.shape[1]
        
    elif col==True and porc==False:
        no_unic_columnas=base.T.duplicated(keep=False)
        cols=no_unic_columnas[no_unic_columnas==True].shape[0]
        
    elif col==False and porc==True:
        no_unic_filas=base.duplicated(keep=False)
        cols=no_unic_filas[no_unic_filas==True].shape[0]/base.shape[0]   
        
    elif col==False and porc==False:
        no_unic_filas=base.duplicated(keep=False)
        cols=no_unic_filas[no_unic_filas==True].shape[0]
    else:
        return("Las opciones 'col' y 'porc' tienen valores distintos a True y False")
    
    return(cols)
    
########## MATCHING DE COLUMNAS Y FILAS NO ÚNICAS
def duplic(base,col=True):
        
    if col==True:
        dupli=base.T.duplicated(keep=False)
    elif col==False:
        dupli=base.duplicated(keep=False)
    else:
        print("El parámetro 'col' tiene valores distintos a True o False")
    
    dupli=dupli[dupli==True]
    if dupli.sum()==0:
        return("No hay columnas duplicadas")
    lista_duplicados=[]
    for s in dupli.index:
        for ss in dupli.index:
            if col==True:
                if base[s].equals(base[ss]) and s!=ss:
                    lista_duplicados.append([s,ss])
            elif col==False:
                if base.iloc[s].equals(base.iloc[ss]) and s!=ss:
                    lista_duplicados.append([s,ss])
            else:
                pass

    if col==False:
        lista_duplicados=sorted(lista_duplicados)
    else:
        pass
                
    dic={}
    for s in dupli.index:
        dic[s]=[]
    for s in dupli.index:
        for i in range(len(lista_duplicados)):
            if s in lista_duplicados[i]:
                dic[s].append(lista_duplicados[i])
    for s in dic:
        lista=[q for l in dic[s] for q in l]
        dic[s]=list(set(lista))
    
    if col==True:            
        lista_listas=[q for q in dic.values()]
    else:
        lista_listas=[sorted(q) for q in dic.values()]

    for i in range(len(lista_listas)): 
        for ii in range(len(lista_listas[i])):
            lista_listas[i][ii]=str(lista_listas[i][ii])
    
    df=pd.DataFrame(lista_listas).drop_duplicates().reset_index(drop=True)
    
    df=df.T
    
    if col==True:
        lista_columnas_df=["Columnas iguales {0}".format(q) for q in range(1,df.shape[1]+1)]        
        df.columns=lista_columnas_df
    else:
        lista_columnas_df=["Filas iguales {0}".format(q) for q in range(1,df.shape[1]+1)]        
        df.columns=lista_columnas_df
        
    return(df)

########## CONSISTENCIA. Porcentaje de outliers
def extremos(base,extremos="ambos",porc=True):
    col_tipos=col_tipo(base,detalle="bajo")
    col_num=col_tipos[col_tipos=="Numérico"].index
    base_num=base[col_num]
    
    if base_num.shape[1]==0:
        print("La base de datos no contiene columnas numéricas")
    else:
        pass
    
    porcentiles_25=base_num.apply(lambda x:np.nanpercentile(x,25),axis=0)
    porcentiles_75=base_num.apply(lambda x:np.nanpercentile(x,75),axis=0)
    
    iqr=porcentiles_75-porcentiles_25
    iqr_upper=porcentiles_75+iqr*1.5
    iqr_lower=porcentiles_25-iqr*1.5

    dic_outliers={}
    
    if extremos=="ambos":
        for i in range(0,len(iqr)):
            dic_outliers[base_num.columns[i]]=(base_num.iloc[:,i]>iqr_upper[i])|(base_num.iloc[:,i]<iqr_lower[i])
    elif extremos=="superior":
        for i in range(0,len(iqr)):
            dic_outliers[base_num.columns[i]]=(base_num.iloc[:,i]>iqr_upper[i])
    elif extremos=="inferior":
        for i in range(0,len(iqr)):
            dic_outliers[base_num.columns[i]]=(base_num.iloc[:,i]<iqr_lower[i])
    else:
        return("La opción extremos tiene valores distintos a 'ambos', 'superior' o 'inferior")
    
    base_outliers=pd.DataFrame(dic_outliers)
    
    if porc==True:
        base_outliers_porc=base_outliers.sum()/base_outliers.shape[0]
    elif porc==False:
        base_outliers_porc=base_outliers.sum()
    else:
        return("La opción 'porc' tiene valores distintos a True o False")

    return(base_outliers_porc)        
    
############## describe de columnas
def descriptivas(base,float_transformar=False):
    
    if float_transformar==True:
        base=base.apply(lambda x:x.astype(float,errors="ignore"),axis=0)
    elif float_transformar==False:
        pass
    else:
        return("La opción 'float_transform' tiene valores distintos a True o False")

    col_tipos=col_tipo(base,detalle="bajo")
    col_num=col_tipos[(col_tipos=="Numérico")|(col_tipos=="Float")].index
    base_num=base[col_num] 
    
    if len(col_num)==0:
        return("La base de datos no tiene columnas numéricas")
    else:
        pass
    
    base_descripcion=base.describe().T
    base_descripcion["missing"]=pd.isnull(base_num).sum()/len(base_num)
    base_descripcion["outliers_total"]=extremos(base)
    base_descripcion["outliers_altos"]=extremos(base,extremos="superior")
    base_descripcion["outliers_bajos"]=extremos(base,extremos="inferior")
    
    
    return(base_descripcion)

###############
def varianza_percentil(base,percentil_inferior=5,percentil_superior=95,float_transform=False):
    
    if float_transform==True:
        base=base.apply(lambda x:x.astype(float,errors="ignore"),axis=0)
    elif float_transform==False:
        pass
    else:
        return("La opción 'float_transform' tiene valores distintos a True o False")

    cols_tipos=base.dtypes
    lista_nums=[]
    for i in range(len(cols_tipos)):
        if "int" in str(cols_tipos[i]) or "float" in str(cols_tipos[i]):
            lista_nums.append(cols_tipos.index[i])
    base_num=base[lista_nums]
    for c in base_num.columns:
        if base_num[c].isnull().sum()==base_num.shape[0]:
            del base_num[c]
        else:
            pass
        
    percentil_bajo=base_num.apply(lambda x:np.percentile(x.dropna(),5),axis=0)
    percentil_alto=base_num.apply(lambda x:np.percentile(x.dropna(),95),axis=0)
    
    percentiles=pd.concat([percentil_bajo,percentil_alto],axis=1)
    percentiles_true=(percentiles.iloc[:,0]==percentiles.iloc[:,1])
    percentiles_true=percentiles_true[percentiles_true==True]
    
    if len(percentiles_true)==0:
        return("No hay ninguna columna numérica que tenga el percentil {0} y el percentil {1} igual".format(percentil_inferior,percentil_superior))
    else:
        return percentiles_true.index
    
############### tabla de valores únicos para cada variable de texto
def categorias(base,limite=0.5,transformar_nums=False,variables=None):
    # Filtrar la base por las variables escogidas en la opción 'variables'
    if type(variables)==list:
        base=base[variables]
    else:
        pass
    
    # Calcular qué variables tipo object tienen valores únicos menores al 50% (o valor de 'limite') del total de filas de la base original
    col_object=base.dtypes
    col_object=col_object[col_object=="object"]
    lista_object_unicos=[]
    for s in col_object.index:
        unico=len(pd.unique(base[s]))
        if unico<base.shape[0]*limite:
            lista_object_unicos.append(s)
            
    # Si la opción 'transformar_nums' es True, incluir las variables numéricas con repeticiones menores al 50% (o el límite) del total de filas   
    if transformar_nums==True:
        cols_types=base.dtypes
        col_nums=[]
        for i in range(len(cols_types)):
            if "int" in str(cols_types[i]) or "float" in str(cols_types[i]):
                col_nums.append(cols_types.index[i])
        for s in col_nums:
            unico=len(pd.unique(base[s]))
            if unico<base.shape[0]*limite:
                lista_object_unicos.append(s)
    elif transformar_nums==False:
        pass
    else:
        return("La opción 'transformar_nums' tiene un valor distinto a True o False")
    
    # Crear el dataframe con la información
    lista_counts=[]
    for s in lista_object_unicos:
        counts=base[s].astype(str).value_counts().drop("nan",errors="ignore")
        if type(counts.index[0])==dict:
            continue
        # counts=list(counts)
        lista=counts[0:10]
        resto=sum(counts[10:len(counts)])
        miss=pd.isnull(base[s]).sum()

        lista["Demás categorías"]=resto
        lista["Datos faltantes"]=miss
        # lista["Total de categorías (con NA)"]=len(pd.unique(base[s]))

        lista=lista.to_frame()
        lista["Columna"]=s
        lista["Porcentaje del total de filas"]=lista[s]/len(base)
            
        resto=lista.iloc[:,0].loc["Demás categorías"]
        
        if resto==0:
            lista=lista.drop("Demás categorías",axis=0)

        lista=lista.reset_index()
        
        s=lista.columns.tolist()[1]
        colis=["Columna","index",s,"Porcentaje del total de filas"]
        lista=lista[colis]
        lista_cols=lista.columns.tolist()
        lista=lista.rename(columns={"index":"Valor",lista_cols[2]:"Frecuencia"})
        lista_counts.append(lista)
    df_counts=pd.concat(lista_counts,axis=0)
    return(df_counts)
    
########## Tamaño de la base de datos en la memoria
def memoria(base,col=False):
    if col==False:
        memoria=base.memory_usage(index=True).sum()
    elif col==True:   
        memoria=base.memory_usage(index=True)
    else:
        return("La opción 'col' tiene un valor distinto a True o False")
    memoria_mb=memoria/(1024**2)
    return memoria_mb
    
########## tabla de resumen pequeña
def resumen_base(base,filas=True,columnas=True,col_numericas=True,col_texto=True,
                 col_booleanas=True,col_fecha=True,col_otro=True,filas_nounicas=True,columnas_nounicas=False,
                 col_faltantes=True,col_extremos=True,memoria_total=True):
    # Lista donde se guardarán resultados, dependiendo de si se escoge o no ver el cálculo
    lista_resumen=[[],[]]
    
    # Calcular tipo de columnas
    col_tipos=col_tipo(base,detalle="bajo")
    
    ## Agregar a lista, si se escoge que sea así
    
    # Número de filas
    if filas==True:
        calculo=base.shape[0]
        nombre="Número de filas"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass  
      
    # Número de columnas
    if columnas==True:
        calculo=base.shape[1]
        nombre="Número de columnas"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass  
      
    # Número de columnas numéricas
    if col_numericas==True:
        calculo=len(col_tipos[col_tipos=="Numérico"])
        nombre="Columnas numéricas"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass 
       
    # Número de columnas de texto
    if col_texto==True:
        calculo=len(col_tipos[col_tipos=="Texto"])
        nombre="Columnas de texto"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass   
     
    # Número de columnas booleanas
    if col_booleanas==True:
        calculo=len(col_tipos[col_tipos=="Boolean"])
        nombre="Columnas booleanas"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass        

    # Número de columnas de fecha
    if col_fecha==True:
        calculo=len(col_tipos[col_tipos=="Fecha"])
        nombre="Columnas de fecha"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass 
       
    # Número de columnas de otro tipo
    if col_otro==True:
        calculo=len(col_tipos[col_tipos=="Otro"])
        nombre="Otro tipo de columnas"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass        
   
    # Número de filas no únicas
    if filas_nounicas==True:
        calculo=nounicos(base,col=False,porc=False)
        nombre="Número de filas no únicas"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass  
      
    # Número de columnas no únicas
    if columnas_nounicas==True:
        calculo=nounicos(base,col=True,porc=False)
        nombre="Número de columnas no únicas"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass        

    # Porcentaje de columnas con más de la mitad de datos faltantes
    if col_faltantes==True:
        col_missing=faltantes(base,porc=True)
        calculo=len(col_missing[col_missing>0.5])
        nombre="Columnas con más de la mitad de datos faltantes"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass     
    
    # Columnas con más del 10% de datos como extremos
    if col_extremos==True:
        col_porc=extremos(base,extremos="ambos",porc=True)
        calculo=len(col_porc[col_porc>0.1])
        nombre="Columnas con más del 10% de datos como extremos"
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass         
    
    # Tamaño de la base en la memoria
    if memoria_total==True:
        
        memoria_tot=memoria(base)
        if memoria_tot>1024:
            memoria_tot=memoria_tot/1024
            nombre="Tamaño de la base en gygabytes (redondeado)"
        else:
            nombre="Tamaño de la base en megabytes (redondeado)"
        calculo=memoria_tot
        lista_resumen[0].append(nombre)
        lista_resumen[1].append(calculo)
    else:
        pass         
    
    tabla_resumen=pd.Series(data=lista_resumen[1],index=lista_resumen[0]).astype(int)
    
    return(tabla_resumen)
 
########### Matrices de correlación para las variables numéricas
def correlacion(base,metodo="pearson",variables=None):
    
    # Filtrar la base por las variables escogidas en la opción 'variables'
    if type(variables)==list:
        base=base[variables]
    else:
        pass
    
    # Filtrar por columnas que sean numéricas
    col_tipos=col_tipo(base,detalle="bajo")
    col_num=col_tipos[col_tipos=="Numérico"].index
    base_num=base[col_num]
    
    # Crear la matriz de correlación dependiendo del método escogido
    if metodo=="pearson":
        correlacion=base_num.corr(method="pearson")
    elif metodo=="kendall":
        correlacion=base_num.corr(method="kendall")
    elif metodo=="spearman":
        correlacion=base_num.corr(method="spearman")
    else:
        return("El parámetro 'metodo' tiene valores diferentes a 'pearson', 'kendall' o 'spearman")
    
    return correlacion

#from distutils.sysconfig import get_python_lib
#print(get_python_lib())
#





