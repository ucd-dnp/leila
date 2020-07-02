# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 08:51:18 2020

@author: pabmontenegro
"""

import os
os.chdir(r"D:\Departamento Nacional de Planeacion\Unidad de Cientificos de Datos - Repositorio UCD\Proyectos UCD\2019\Datos abiertos Colombia\2_Codigo\1_Source\calidad_datos")
import metadatos

########### Abrir la base de datos original con los metadatos (asset inventory) del Portal de Datos Abiertos
asset=metadatos.asset_inventory()

########### Abrir la base de datos de los metadatos del Portal con menos columnas y traducidas a español
asset_bonita=metadatos.asset_inventory_espanol()

########## Mostrar los metadatos de una sola base
base_metadatos=metadatos.mostrar_metadatos("gydr-jtkd")

########## Abrir página web de base de datos
metadatos.pagina_metadatos("b62i-c8mw")

########## Búsqueda dentro de la tabla de asset inventory

# Buscar bases cuyo nombre incluye temas de SECOP
columnas_valor={
        "nombre":["SECOP"],
        }
tabla_filtrada=metadatos.filtrar_asset(columnas_valor)

# Buscar bases cuya descripción incluya 
columnas_valor={
        "descripcion":["economia","ambient"]
        }
tabla_filtrada=metadatos.filtrar_asset(columnas_valor)

# Buscar bases que tengan entre 100 y 10000 filas y más de 10 columnas
columnas_valor={
        "filas":[100,10000],
        "columnas":[10,"+"],
        }

tabla_filtrada=metadatos.filtrar_asset(columnas_valor)

# Buscar bases con fecha de creación en 2019
columnas_valor={
        "fecha_creacion":["2019-01-01","2019-12-31"]
        }
tabla_filtrada=metadatos.filtrar_asset(columnas_valor)

# Buscar bases con fecha de 2019 o más antiguas
columnas_valor={
        "fecha_creacion":["2018-12-31","-"]
        }
tabla_filtrada=metadatos.filtrar_asset(columnas_valor)





