# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:18:14 2020

@author: hinsuasti
"""

from leila import datos_gov
from leila.reporte import generar_reporte


# Abrir la base de datos original con los metadatos (asset inventory)
# del Portal de Datos Abiertos
inventario = datos_gov.tabla_inventario()

# Buscar bases cuyo nombre incluye temas de SECOP
columnas_valor = {"nombre":["SECOP"]}
tabla_filtrada = datos_gov.filtrar_tabla(columnas_valor)

# Cargar una base de datos de interes
#cargando la prmera base de datos que aparece en la tabla filtrada por
#la palabra "SECOP"
tabla_id = tabla_filtrada.iloc[1].numero_api
datos = datos_gov.cargar_base(tabla_id)

# Generar reporte con el modulo reporte
generar_reporte(df = datos, castFloat=True)
