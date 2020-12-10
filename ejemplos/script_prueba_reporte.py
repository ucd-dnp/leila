from leila.datos_gov import Inventario, Datos
from leila.reporte import generar_reporte


# Abrir la base de datos original con los metadatos (asset inventory)
# del Portal de Datos Abiertos
inventario = Inventario()
inventario.inventario._base

# Buscar bases cuyo nombre incluye temas de SECOP
columnas_valor = {"nombre": ["SECOP"]}
tabla_filtrada = inventario.filtrar_tabla(columnas_valor)

# Cargar una base de datos de interes
# cargando la prmera base de datos que aparece en la tabla filtrada por
# la palabra "SECOP"
tabla_id = tabla_filtrada.iloc[1].numero_api
datos = Datos(tabla_id)

# Generar reporte con el modulo reporte
generar_reporte(df=datos)
