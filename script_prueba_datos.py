# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 08:30:57 2020

@author: pabmontenegro
"""

import pandas as pd

#importación libreria calidad de datos
from leila.calidad_datos import CalidadDatos

#Cargando base de datos de prueba
base = pd.read_excel("../../../1_Insumos/Bases_de_datos/Reporte DFI 2019 Julio v4 DNP.xlsx")

#creado objeto de la clase CalidadDatos, similar a pandas DataFrame

datos = CalidadDatos(base)

############ RESUMEN DE BASE DE DATOS
resumen=datos.resumen()
print(resumen)

############ VARIANZA DE DATOS
var_perc=datos.varianza_percentil(float_transform=True)

############ Tipos de columnas
# Detalles bajo
tipos_bajo=datos.col_tipo(detalle="bajo")
print(tipos_bajo)

# Detalles alto
tipos_alto=datos.col_tipo(detalle="alto")
print(tipos_alto)

############ Valores únicos en cada columna
# Sin faltantes
unicos_nofaltantes=datos.ValoresUnicos(faltantes=False)
print(unicos_nofaltantes)

# Con faltantes
unicos_sifaltantes=datos.ValoresUnicos(faltantes=True)
print(unicos_sifaltantes)

############ Valores faltantes por columna
# En porcentaje
faltantes_porc=datos.ValoresFaltantes(porc=True)
print(faltantes_porc)

# En número
faltantes_num=datos.ValoresFaltantes(porc=False)
print(faltantes_num)

############ Número y porcentaje de filas y columnas no únicas
# Porcentaje de columnas que no son únicas
nounic_col_porc=datos.nounicos(col=True,porc=True)
print(nounic_col_porc)

# Número de columnas que no son únicas
nounic_col_num=datos.nounicos(col=True,porc=False)
print(nounic_col_num)

# Porcentaje de filas que no son únicas
nounic_fil_porc=datos.nounicos(col=False,porc=True)
print(nounic_fil_porc)

# Número de filas que no son únicas
nounic_fil_num=datos.nounicos(col=False,porc=False)
print(nounic_fil_num)

############ Emparejamiento de columnas y filas duplicadas
# Columnas duplicadas
duplicados_col=datos.ValoresDuplicados(col=True)
print(duplicados_col)

# Filas duplicadas
duplicados_fil=datos.ValoresDuplicados(col=False)
print(duplicados_fil)

############ Valores extremos de cada columna
# Extremos altos y bajos en porcentaje
extremos_ambos_porc=datos.ValoresExtremos(extremos="ambos",porc=True)
print(extremos_ambos_porc)

# Extremos altos y bajos en número
extremos_ambos_num=datos.ValoresExtremos(extremos="ambos",porc=False)
print(extremos_ambos_num)

# Extremos altos porcentaje
extremos_sup_porc=datos.ValoresExtremos(extremos="superior",porc=True)
print(extremos_sup_porc)

# Extremos altos en número
extremos_sup_num=datos.ValoresExtremos(extremos="superior",porc=False)
print(extremos_sup_num)

# Extremos bajos porcentaje
extremos_inf_porc=datos.ValoresExtremos(extremos="inferior",porc=True)
print(extremos_inf_porc)

# Extremos bajos en número
extremos_inf_num=datos.ValoresExtremos(extremos="inferior",porc=False)
print(extremos_inf_num)

############ Estadísticas descriptivas
# No convertir las columnas numéricas a float
est_descrip_nofloat=datos.descriptivas(float_transformar=False)
print(est_descrip_nofloat)

# Convertir las columnas numéricas a float
est_descrip_float=datos.descriptivas(float_transformar=True)
print(est_descrip_float)

############ Matrices de correlación para columnas numéricas
# Correlación Pearson
corr_pearson=datos.correlacion(metodo="pearson")
print(corr_pearson)

# Correlación Kendall
corr_kendall=datos.correlacion(metodo="kendall")
print(corr_kendall)

# Correlación Spearman
corr_spearman=datos.correlacion(metodo="spearman")
print(corr_spearman)

############ Primeras frecuencias de variables categóricas
# No transformar números
categoricas_no_transformar=datos.categorias(limite=0.5,transformar_nums=False,variables=None)
print(categoricas_no_transformar)

# No transformar números
categoricas_transformar=datos.categorias(limite=0.5,transformar_nums=True,variables=None)
print(categoricas_transformar)

########### Peso en la memoria de la base en mega bytes
# Peso total
peso_base=datos.memoria(col=False)
print(peso_base)

# Peso total por columna
peso_base_cols=datos.memoria(col=True)
print(peso_base_cols)

########### Matrices de correlación para columnas categóricas
# Cramer V
matriz_cramer = datos.correlacion_categoricas(categorias_maximas=30, limite=0.5, variables=None,tipo='cramer',columnas_intervalo=None)
# Phik
matriz_phik = datos.correlacion_categoricas(categorias_maximas=30, limite=0.5, variables=None,tipo='phik')






