# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 09:13:22 2019

@author: pabmontenegro
"""

import pandas as pd
import numpy as np
import datetime
from sodapy import Socrata


direccion_metatabla="https://dl.dropboxusercontent.com/s/84lt7ddrt73vzzu/tabla_final.txt?dl=0"

def sodapy_data(api_id,token=None):

    client = Socrata("www.datos.gov.co",
                     app_token=token)

    results = client.get(api_id,limit=1000000000)
    base_original = pd.DataFrame.from_records(results)
    return(base_original)

# OBTENER LA TABLA QUE TIENE DATOS ABIERTOS CON INFORMACIÓN DE LAS BASES DE DATOS
def asset_inventory(token=None):
    import pandas as pd
    from sodapy import Socrata
    client = Socrata("www.datos.gov.co",app_token=token)
    results = client.get("uzcf-b9dh",limit=1000000000)
    asset_inventory = pd.DataFrame.from_records(results)
    return(asset_inventory)

asset=asset_inventory(token="WnkJhtSI1mjrtpymw0gVNZEcl")


def asset_pretty(token=None):
    asset=asset_inventory(token=token)
    
    dic_rename={
         "uid":"No. identificación API",
         "name":"Nombre",
         "description":"Descripción",
         "owner":"Dueño",
         "type":"Tipo de datos",
         "category":"Categoría",
         "tags":"Términos clave",
         "url":"URL",
         "creation_date":"Fecha de creación",
         "last_data_updated_date":"Fecha de última actualización",
         "row_count":"Número de filas",
         "column_count":"Número de columnas",
         "contact_email":"Correo electrónico del contacto",
         "license":"Licencia",
         "attribution":"Entidad creadora de la base de datos",
         "attribution_link":"URL de entidad",
         "informacindelaentidad_sector":"Sector de la entidad",
         "informacindelaentidad_departamento":"Departamento de la entidad",
         "informacindelaentidad_orden":"Orden de la entidad",
         "informacindelaentidad_reaodependencia":"Dependencia de la entidad",
         "informacindelaentidad_municipio":"Municipio de la entidad",
         "informacindedatos_frecuenciadeactualizacin":"Frecuencia de actualización",
         "informacindedatos_idioma":"Idioma",
         "informacindedatos_coberturageogrfica":"Cobertura"     
         }
    
    lista_columnas=list(dic_rename.keys())
    asset=asset[lista_columnas].rename(columns=dic_rename)
    return(asset)

def meta_show(api_id,token=None):
    asset=asset_pretty(token=token)
    base_info=asset[asset["No. identificación API"]==api_id]
    base_info=pd.Series(base_info.iloc[0])
    base_info=base_info.replace("","CAMPO NO DILIGENCIADO").replace(np.nan,"CAMPO NO DILIGENCIADO")
    return(base_info)

############ METADATOS
# OBTENER INFORMACIÓN DE COLUMNAS DE LA BASE DE DATOS SEGÚN LA METADATA
def info_cols_meta(api_id):
    import pandas as pd  
    
    tabla_conj=pd.read_csv(direccion_metatabla)
    tabla_conj=tabla_conj.loc[tabla_conj.loc[:,"tipo"]=="Conjunto de Datos"]
    
    metas=tabla_conj[tabla_conj["api_id"]==api_id]

    dic_cols={}
    for s in ["col_nombres","col_des","col_tipo"]:
        col_nombres=metas['meta_columnas_nombre'].iloc[0].split(",")
        col_nombres=[q.replace("[","").replace("]","").replace(" ","") for q in col_nombres]
    
        col_des=metas['meta_columnas_descr'].iloc[0].split(",")
        col_des=[q.replace("[","").replace("]","").replace(" ","") for q in col_des]
    
        col_tipo=metas['meta_columnas_tipo'].iloc[0].split(",")
        col_tipo=[q.replace("[","").replace("]","").replace(" ","") for q in col_tipo]
    
        dic_cols["col_nombres"]=col_nombres
        dic_cols["col_des"]=col_des
        dic_cols["col_tipo"]=col_tipo

    cols_meta=pd.DataFrame(dic_cols)
    cols_meta=cols_meta.sort_values(by="col_nombres").reset_index(drop=True)
    return(cols_meta)
    
# COMPARAR LAS FILAS DE LOS METADATOS CON LA BASE DE DATOS MICRO
def compare_meta(api_id,token=None):
    import pandas as pd
    from sodapy import Socrata
    
    client=Socrata("www.datos.gov.co",app_token=token)
    results=client.get(api_id,limit=1000000000)
    base_original=pd.DataFrame.from_records(results)
    
    tabla_conj=pd.read_csv(direccion_metatabla)
    tabla_conj=tabla_conj.loc[tabla_conj.loc[:,"tipo"]=="Conjunto de Datos"]

    meta_fila=tabla_conj.loc[tabla_conj.loc[:,"api_id"]==api_id].loc[:,"meta_filas"].iloc[0]
    micro_fila=base_original.shape[0]

    meta_col=tabla_conj.loc[tabla_conj.loc[:,"api_id"]==api_id].loc[:,"meta_columnas"].iloc[0]
    micro_col=base_original.shape[1]

    comparacion=pd.Series(
        data=[meta_fila,micro_fila,meta_col,micro_col],
        index=["filas_metadatos","filas_datos","columnas_metadatos","columnas_datos"]
        )
    
    return(comparacion)

def rows_vs_meta(api_id,token=None):
    import pandas as pd
    from sodapy import Socrata
    
    client=Socrata("www.datos.gov.co",app_token=token)
    results=client.get(api_id,limit=1000000000)
    base_original=pd.DataFrame.from_records(results)
    
    tabla_conj=pd.read_csv(direccion_metatabla)
    tabla_conj=tabla_conj.loc[tabla_conj.loc[:,"tipo"]=="Conjunto de Datos"]
    
    meta_fila=tabla_conj.loc[tabla_conj.loc[:,"api_id"]==api_id].loc[:,"meta_filas"].iloc[0]
    micro_fila=base_original.shape[0]
    comparacion="Filas en metadatos: {0}. Filas en microdatos: {1}".format(meta_fila,micro_fila)
    return(comparacion)
    
# COMPARAR LAS COLUMNAS DE LOS METADATOS CON LA BASE DE DATOS MICRO
def cols_vs_meta(api_id,token=None):
    import pandas as pd
    from sodapy import Socrata
    
    client=Socrata("www.datos.gov.co",app_token=token)
    results=client.get(api_id,limit=1000000000)
    base_original=pd.DataFrame.from_records(results)
    
    tabla_conj=pd.read_csv(direccion_metatabla)
    tabla_conj=tabla_conj.loc[tabla_conj.loc[:,"tipo"]=="Conjunto de Datos"]
    
    meta_col=tabla_conj.loc[tabla_conj.loc[:,"api_id"]==api_id].loc[:,"meta_columnas"].iloc[0]
    micro_col=base_original.shape[1]
    comparacion="Columnas en metadatos: {0}. Columnas en microdatos: {1}".format(meta_col,micro_col)
    return(comparacion)
    

    
# OBTENER LA TABLA QUE SE SCRAPEÓ CON LA INFORMACIÓN DE LOS METADATOS DE DATOS ABIERTOS
def table_meta():
    import pandas as pd
    tabla_conj=pd.read_csv(direccion_metatabla)    
    return(tabla_conj)

#     
def table_search(columnas_valor,columnas_operacion):
    # base_filtro=tabla.copy()
    base_filtro=table_meta

    columnas=base_filtro.columns.tolist()
    
    lista_vocales=["a","e","i","o","u","a","e","i","o","u"]
    lista_tildes=["á","é","í","ó","ú","ä","ë","ï","ö","ü"]
    
    columnas_string=columnas_valor.copy()
    
    for s in ["meta_filas","meta_columnas","creacion","actualizacion_datos","actualizacion_metadatos"]:
        if s in columnas_string:del columnas_string[s]
    
    for s_key in columnas_string:
        if s_key not in columnas:
            return(print("No existe una columna con el nombre '{0}'".format(s_key)))
        lista=[]
        s_value=columnas_valor[s_key]
        
        for i_s in range(len(s_value)):
            for i in range(len(lista_vocales)):s_value[i_s]=s_value[i_s].lower().replace(lista_tildes[i],lista_vocales[i])
                    
        if columnas_operacion[s_key]=="contiene":
            for r in range(tabla.shape[0]):
                s_observacion=tabla.loc[:,s_key].astype(str).iloc[r].lower()
                for i in range(len(lista_vocales)):s_observacion=s_observacion.replace(lista_tildes[i],lista_vocales[i])
                
                if all(q in s_observacion for q in s_value):
                    lista.append(tabla.iloc[r])
            if len(lista)==0:
                return(print("Ninguna observación de la columna '{0}' contiene el texto '{1}'".format(s_key,s_value)))
        elif columnas_operacion[s_key]=="igual":
            if len(columnas_string[s_key])!=1:
                return("La lista con el valor buscado para la columna '{0}' tiene que tener una longitud de 1 porque se busca una coincidencia exacta".format(s_key))
                
            for r in range(tabla.shape[0]):
                s_observacion=tabla.loc[:,s_key].astype(str).iloc[r].lower()
                for i in range(len(lista_vocales)):s_observacion=s_observacion.replace(lista_tildes[i],lista_vocales[i])                                
                                
                if s_value[0]==s_observacion:
                    lista.append(tabla.iloc[r])   
            if len(lista)==0:
                return(print("Ninguna observación de la columna '{0}' es igual al texto '{1}'".format(s_key,s_value[0])))        
        else:
            return("Se introdujo una operación inválida para la columna '{0}'".format(s_key))
        base_filtro_pequeno=pd.DataFrame(lista)
        base_filtro=base_filtro.loc[base_filtro_pequeno.index].dropna(how="all")
    
    for s in ["meta_filas","meta_columnas"]:
        if s in columnas_valor: 
            col_op_metafil=columnas_operacion[s]
            col_val_metafil=columnas_valor[s]
            if col_op_metafil=="contiene":
                base_filtro=base_filtro[base_filtro[s].isin(columnas_valor[s])]
            elif col_op_metafil=="entre":
                entres=columnas_valor[s]
                if entres[0]>entres[1] or entres[0]<0 or entres[1]<0 or entres[0]==entres[1]:
                    return(print("El rango de la llave '{0}' del diccionario 'columnas_valor' no es válido"))
                else:
                    lista_entres=[q for q in range(entres[0],entres[1])]
                    base_filtro=base_filtro[base_filtro[s].isin(lista_entres)]
            elif col_op_metafil=="mayor":
                if len(col_val_metafil)!=1:
                    return(print("La lista de la llave '{0}' es inválida porque tiene una longitud distinta a 1".format(s)))
                else:
                    base_filtro=base_filtro[base_filtro[s]>col_val_metafil[0]]
            elif col_op_metafil=="menor":
                if len(col_val_metafil)!=1:
                    return(print("La lista de la llave '{0}' es inválida porque tiene una longitud distinta a 1".format(s)))
                else:
                    base_filtro=base_filtro[base_filtro[s]<col_val_metafil[0]]
            elif col_op_metafil=="mayor igual":
                if len(col_val_metafil)!=1:
                    return(print("La lista de la llave '{0}' es inválida porque tiene una longitud distinta a 1".format(s)))
                else:
                    base_filtro=base_filtro[base_filtro[s]>=col_val_metafil[0]]
            elif col_op_metafil=="menor igual":
                if len(col_val_metafil)!=1:
                    return(print("La lista de la llave '{0}' es inválida porque tiene una longitud distinta a 1".format(s)))
                else:
                    base_filtro=base_filtro[base_filtro[s]<=col_val_metafil[0]]
            else:
                return(print("El valor de la llave '{0}' del diccionario 'columnas_operacion' es distinto a 'contiene', 'entre', 'mayor', 'mayor igual', 'menor' o 'menor igual'".format(s)))    
    
    for s in ["creacion","actualizacion_datos","actualizacion_metadatos"]:
        if s in columnas_valor:
            if columnas_operacion[s]=="entre":
                fecha_inicio=datetime.datetime.strptime(columnas_valor[s][0],"%d/%m/%Y")
                fecha_fin=datetime.datetime.strptime(columnas_valor[s][1],"%d/%m/%Y")
                                
                base_filtro.loc[:,"{0}_fecha".format(s)]=base_filtro.loc[:,s].apply(lambda x:datetime.datetime.strptime(x,"%d/%m/%Y") if x!="nan" else np.nan)
                base_filtro=base_filtro[(base_filtro.loc[:,"{0}_fecha".format(s)]>=fecha_inicio) & (base_filtro.loc[:,"{0}_fecha".format(s)]<=fecha_fin)]
#                del base_filtro["{0}_fecha".format(s)]
            elif columnas_operacion[s]=="contiene":
                base_filtro=base_filtro[base_filtro[s].isin(columnas_valor[s])]
            else:
                return(print("El valor de la llave '{0}' del diccionario 'columnas_operacion' es distinto a 'contiene' o 'entre'".format(s)))
                
    return(base_filtro)


# VERIFICAR SI ACTUALIZACIONES DE DATOS Y METADATOS ESTÁN AL DÍA
def updated_data(api_id,tipo_dato="metadatos"):
    tabla_conj=pd.read_csv(direccion_metatabla)
    tabla_conj=tabla_conj.loc[tabla_conj.loc[:,"tipo"]=="Conjunto de Datos"]
    
    base_id=tabla_conj.loc[tabla_conj.loc[:,"api_id"]==api_id]
    fecha_creacion=base_id.loc[:,"creacion"].iloc[0]
    fecha_act_datos=base_id.loc[:,"actualizacion_datos"].iloc[0]
    fecha_act_metad=base_id.loc[:,"actualizacion_metadatos"].iloc[0]
    
    fecha_creacion=datetime.datetime.strptime(fecha_creacion,"%d/%m/%Y")
    fecha_act_datos=datetime.datetime.strptime(fecha_act_datos,"%d/%m/%Y")
    fecha_act_metad=datetime.datetime.strptime(fecha_act_metad,"%d/%m/%Y")

    rango_ano=366
    rango_semestral=rango_ano/2
    rango_mensual=366/12
    rango_trimestral=rango_ano/4
    rango_trienio=rango_ano*3
    rango_semanal=8
    rango_diario=1
    rango_quincenal=rango_mensual/2
    
    frecuencia_act=base_id.loc[:,"actualizacion_frec"].iloc[0]
    
#    hoy_menos_creacion=datetime.date.today()-fecha_creacion.date()    
    hoy_menos_act_datos=datetime.date.today()-fecha_act_datos.date()
    hoy_menos_act_metad=datetime.date.today()-fecha_act_metad.date()
    
    if tipo_dato=="datos":
        if frecuencia_act=="Anual":
            if hoy_menos_act_datos<=datetime.timedelta(rango_ano):
                return("La base de datos fue actualizada hace {0} días, por lo tanto sigue vigente para su período anual".format(hoy_menos_act_datos.days))
            else:
                return("La base de datos fue actualizada hace {0} días, por lo tanto ya superó su límite anual de actualización".format(hoy_menos_act_datos.days))
        elif frecuencia_act=="Semestral":
            if hoy_menos_act_datos<=datetime.timedelta(rango_semestral):
                return("La base de datos fue actualizada hace {0} días, por lo tanto sigue vigente para su período semestral".format(hoy_menos_act_datos.days))
            else:
                return("La base de datos fue actualizada hace {0} días, por lo tanto ya superó su límite semestral de actualización".format(hoy_menos_act_datos.days))
        elif frecuencia_act=="Mensual":
            if hoy_menos_act_datos<=datetime.timedelta(rango_mensual):
                return("La base de datos fue actualizada hace {0} días, por lo tanto sigue vigente para su período mensual".format(hoy_menos_act_datos.days))
            else:
                return("La base de datos fue actualizada hace {0} días, por lo tanto ya superó su límite mensual de actualización".format(hoy_menos_act_datos.days))
        elif frecuencia_act=="Trimestral":
            if hoy_menos_act_datos<=datetime.timedelta(rango_trimestral):
                return("La base de datos fue actualizada hace {0} días, por lo tanto sigue vigente para su período trimestral".format(hoy_menos_act_datos.days))
            else:
                return("La base de datos fue actualizada hace {0} días, por lo tanto ya superó su límite trimestral de actualización".format(hoy_menos_act_datos.days))
        elif frecuencia_act=="Trienio":
            if hoy_menos_act_datos<=datetime.timedelta(rango_trienio):
                return("La base de datos fue actualizada hace {0} días, por lo tanto sigue vigente para su período trianual".format(hoy_menos_act_datos.days))
            else:
                return("La base de datos fue actualizada hace {0} días, por lo tanto ya superó su límite trianual de actualización".format(hoy_menos_act_datos.days))
        elif frecuencia_act=="Diaria":
            if hoy_menos_act_datos<=datetime.timedelta(rango_diario):
                return("La base de datos fue actualizada hace {0} días, por lo tanto sigue vigente para su período diario".format(hoy_menos_act_datos.days))
            else:
                return("La base de datos fue actualizada hace {0} días, por lo tanto ya superó su límite diario de actualización".format(hoy_menos_act_datos.days))
        elif frecuencia_act=="Semanal":
            if hoy_menos_act_datos<=datetime.timedelta(rango_semanal):
                return("La base de datos fue actualizada hace {0} días, por lo tanto sigue vigente para su período semanal".format(hoy_menos_act_datos.days))
            else:
                return("La base de datos fue actualizada hace {0} días, por lo tanto ya superó su límite semanal de actualización".format(hoy_menos_act_datos.days))
        elif frecuencia_act=="Quincenal":
            if hoy_menos_act_datos<=datetime.timedelta(rango_quincenal):
                return("La base de datos fue actualizada hace {0} días, por lo tanto sigue vigente para su período quincenal".format(hoy_menos_act_datos.days))
            else:
                return("La base de datos fue actualizada hace {0} días, por lo tanto ya superó su límite quincenal de actualización".format(hoy_menos_act_datos.days))
        else:
            return("La información de La frecuencia de acualización no está disponible en los metadatos")
    elif tipo_dato=="metadatos":
        if frecuencia_act=="Anual":
            if hoy_menos_act_metad<=datetime.timedelta(rango_ano):
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto siguen vigentes para su período anual".format(hoy_menos_act_metad.days))
            else:
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto ya superaron su límite anual de actualización".format(hoy_menos_act_metad.days))
        elif frecuencia_act=="Semestral":
            if hoy_menos_act_metad<=datetime.timedelta(rango_semestral):
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto siguen vigentes para su período semestral".format(hoy_menos_act_metad.days))
            else:
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto ya superaron su límite semestral de actualización".format(hoy_menos_act_metad.days))
        elif frecuencia_act=="Mensual":
            if hoy_menos_act_metad<=datetime.timedelta(rango_mensual):
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto siguen vigentes para su período mensual".format(hoy_menos_act_metad.days))
            else:
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto ya superaron su límite mensual de actualización".format(hoy_menos_act_metad.days))
        elif frecuencia_act=="Trimestral":
            if hoy_menos_act_metad<=datetime.timedelta(rango_trimestral):
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto siguen vigentes para su período trimestral".format(hoy_menos_act_metad.days))
            else:
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto ya superaron su límite trimestral de actualización".format(hoy_menos_act_metad.days))
        elif frecuencia_act=="Trienio":
            if hoy_menos_act_metad<=datetime.timedelta(rango_trienio):
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto siguen vigentes para su período trianual".format(hoy_menos_act_metad.days))
            else:
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto ya superaron su límite trianual de actualización".format(hoy_menos_act_metad.days))
        elif frecuencia_act=="Diaria":
            if hoy_menos_act_metad<=datetime.timedelta(rango_diario):
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto siguen vigentes para su período diario".format(hoy_menos_act_metad.days))
            else:
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto ya superaron su límite diario de actualización".format(hoy_menos_act_metad.days))
        elif frecuencia_act=="Semanal":
            if hoy_menos_act_metad<=datetime.timedelta(rango_semanal):
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto siguen vigentes para su período semanal".format(hoy_menos_act_metad.days))
            else:
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto ya superaron su límite semanal de actualización".format(hoy_menos_act_metad.days))
        elif frecuencia_act=="Quincenal":
            if hoy_menos_act_metad<=datetime.timedelta(rango_quincenal):
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto siguen vigentes para su período quincenal".format(hoy_menos_act_metad.days))
            else:
                return("Los metadatos fueron actualizados hace {0} días, por lo tanto ya superaron su límite quincenal de actualización".format(hoy_menos_act_metad.days))
        else:
            return("La información de La frecuencia de acualización no está disponible en los metadatos")
        
    else:
        return("El segundo parámetro de la función 'actualización' (el tipo de dato) tiene que ser una de las siguientes palabras: 'datos' o 'metadatos'")





#def infos_cols_tabla(base):
#    tipo_columna=col_type(base)
#    valores_unicos=unique_col(base)
#    valores_unicos_missing=unique_col_missing(base)
#    porcentaje_missing=missing_perc(base)
#    
#    columnas=["Columna","Tipo de la columna","No. únicos","No. únicos con missing","% valores faltantes"]
#    
#    tabla_grande=pd.concat([tipo_columna,valores_unicos,valores_unicos_missing,porcentaje_missing],axis=1).reset_index()
#    tabla_grande.columns=columnas
#    return(tabla_grande)
    

























