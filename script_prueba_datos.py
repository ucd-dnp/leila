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

datos = CalidadDatos(base,castFloat=False)

############ RESUMEN DE BASE DE DATOS
resumen=datos.Resumen()
print(resumen)

############ VARIANZA DE DATOS
varianza_perc=datos.VarianzaEnPercentil()

############ Tipos de columnas
# Detalles bajo
tipos_bajo=datos.TipoColumnas(detalle="bajo")
print(tipos_bajo)

# Detalles alto
tipos_alto=datos.TipoColumnas(detalle="alto")
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
repetidos_col_porc=datos.CantidadDuplicados(eje=1,porc=True)
print(repetidos_col_porc)

# Número de columnas que no son únicas
repetidos_col_num=datos.CantidadDuplicados(eje=1,porc=False)
print(repetidos_col_num)

# Porcentaje de filas que no son únicas
repetidos_fil_porc=datos.CantidadDuplicados(eje=0,porc=True)
print(repetidos_fil_porc)

# Número de filas que no son únicas
repetidos_fil_num=datos.CantidadDuplicados(eje=0,porc=False)
print(repetidos_fil_num)

############ Emparejamiento de columnas y filas duplicadas
# Columnas duplicadas
duplicados_col=datos.EmparejamientoDuplicados(col=True)
print(duplicados_col)

# Filas duplicadas
duplicados_fil=datos.EmparejamientoDuplicados(col=False)
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
estadisticas_descriptivas=datos.DescripcionNumericas()
print(estadisticas_descriptivas)

############ Matrices de correlación para columnas numéricas
# Correlación Pearson
corr_pearson=datos.CorrelacionNumericas(metodo="pearson")
print(corr_pearson)

# Correlación Kendall
corr_kendall=datos.CorrelacionNumericas(metodo="kendall")
print(corr_kendall)

# Correlación Spearman
corr_spearman=datos.CorrelacionNumericas(metodo="spearman")
print(corr_spearman)

############ Primeras frecuencias de variables categóricas
# No transformar números
categoricas_no_transformar=datos.DescripcionCategoricas(limite=0.5,incluirNumericos=False,variables=None)
print(categoricas_no_transformar)

# No transformar números
categoricas_transformar=datos.DescripcionCategoricas(limite=0.5,incluirNumericos=True,variables=None)
print(categoricas_transformar)

########### Peso en la memoria de la base en mega bytes
# Peso total
peso_base=datos.Memoria(col=False)
print(peso_base)

# Peso total por columna
peso_base_cols=datos.Memoria(col=True)
print(peso_base_cols)

########### Matrices de correlación para columnas categóricas
# Cramer V
matriz_cramer = datos.CorrelacionCategoricas(metodo='cramer',categoriasMaximas=30, limite=0.5, variables=None)
print(matriz_cramer)
# Phik
matriz_phik = datos.CorrelacionCategoricas(metodo='phik',categoriasMaximas=30, limite=0.5, variables=None)
print(matriz_phik)





