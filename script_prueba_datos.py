# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 08:30:57 2020

@author: pabmontenegro
"""

import os
import pandas as pd

os.chdir(r"D:\Departamento Nacional de Planeacion\Unidad de Cientificos de Datos - Repositorio UCD\Proyectos UCD\2019\Datos abiertos Colombia\2_Codigo\1_Source\calidad_datos")

import datos

base=pd.read_excel(r"D:\Departamento Nacional de Planeacion\Unidad de Cientificos de Datos - Repositorio UCD\Proyectos UCD\2019\Datos abiertos Colombia\1_Insumos\Bases_de_datos\Reporte DFI 2019 Julio v4 DNP.xlsx")

############ RESUMEN DE BASE DE DATOS
resumen=datos.resumen_base(base)

############ VARIANZA DE DATOS
var_perc=datos.varianza_percentil(base,float_transform=True)

############ Tipos de columnas
# Detalles bajo
tipos_bajo=datos.col_tipo(base,detalle="bajo")
# Detalles alto
tipos_alto=datos.col_tipo(base,detalle="alto")

############ Valores únicos en cada columna
# Sin faltantes
unicos_nofaltantes=datos.unicos(base,faltantes=False)
# Con faltantes
unicos_sifaltantes=datos.unicos(base,faltantes=True)

############ Valores faltantes por columna
# En porcentaje
faltantes_porc=datos.faltantes(base,porc=True)
# En número
faltantes_num=datos.faltantes(base,porc=False)

############ Número y porcentaje de filas y columnas no únicas
# Porcentaje de columnas que no son únicas
nounic_col_porc=datos.nounicos(base,col=True,porc=True)
# Número de columnas que no son únicas
nounic_col_num=datos.nounicos(base,col=True,porc=False)
# Porcentaje de filas que no son únicas
nounic_fil_porc=datos.nounicos(base,col=False,porc=True)
# Número de filas que no son únicas
nounic_fil_num=datos.nounicos(base,col=False,porc=False)

############ Emparejamiento de columnas y filas duplicadas
# Columnas duplicadas
duplicados_col=datos.duplic(base,col=True)
# Filas duplicadas
duplicados_fil=datos.duplic(base,col=False)

############ Valores extremos de cada columna
# Extremos altos y bajos en porcentaje
extremos_ambos_porc=datos.extremos(base,extremos="ambos",porc=True)
# Extremos altos y bajos en número
extremos_ambos_num=datos.extremos(base,extremos="ambos",porc=False)

# Extremos altos porcentaje
extremos_sup_porc=datos.extremos(base,extremos="superior",porc=True)
# Extremos altos en número
extremos_sup_num=datos.extremos(base,extremos="superior",porc=False)

# Extremos bajos porcentaje
extremos_inf_porc=datos.extremos(base,extremos="inferior",porc=True)
# Extremos bajos en número
extremos_inf_num=datos.extremos(base,extremos="inferior",porc=False)

############ Estadísticas descriptivas
# No convertir las columnas numéricas a float
est_descrip_nofloat=datos.descriptivas(base,float_transformar=False)
# Convertir las columnas numéricas a float
est_descrip_float=datos.descriptivas(base,float_transformar=True)

############ Matrices de correlación para columnas numéricas
# Correlación Pearson
corr_pearson=datos.correlacion(base,metodo="pearson")
# Correlación Kendall
corr_kendall=datos.correlacion(base,metodo="kendall")
# Correlación Spearman
corr_spearman=datos.correlacion(base,metodo="spearman")

############ Primeras frecuencias de variables categóricas
# No transformar números
categoricas_no_transformar=datos.categorias(base,limite=0.5,transformar_nums=False,variables=None)
# No transformar números
categoricas_transformar=datos.categorias(base,limite=0.5,transformar_nums=True,variables=None)

########### Peso en la memoria de la base en mega bytes
# Peso total
peso_base=datos.memoria(base,col=False)
# Peso total por columna
peso_base_cols=datos.memoria(base,col=True)





















