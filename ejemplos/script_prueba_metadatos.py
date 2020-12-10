from leila.datos_gov import Datos, Inventario

# Abrir la base de datos original con los metadatos (asset inventory)
# del Portal de Datos Abiertos
inventario = Inventario()

# Búsqueda dentro de la tabla de asset inventory

# Buscar bases cuyo nombre incluye temas de SECOP
columnas_valor = {"nombre": ["SECOP"]}
tabla_filtrada = inventario.filtrar_tabla(columnas_valor)

# Cargar una base de datos de interes
# cargando la pirmera base de datos que aparece en la tabla filtrada por
# la palabra "SECOP"
tabla_id = tabla_filtrada.iloc[0].numero_api
datos = Datos(tabla_id)

# Buscar bases cuya descripción incluya
columnas_valor = {"descripcion": ["economia", "ambiente"]}
tabla_filtrada = inventario.filtrar_tabla(columnas_valor)

# Buscar bases que tengan entre 100 y 10000 filas y más de 10 columnas
columnas_valor = {"filas": [100, 10000],
                  "columnas": [10, "+"]}

tabla_filtrada = inventario.filtrar_tabla(columnas_valor)

# Buscar bases con fecha de creación en 2019
columnas_valor = {"fecha_creacion": ["2019-01-01", "2019-12-31"]}
tabla_filtrada = inventario.filtrar_tabla(columnas_valor)

# Buscar bases con fecha de 2019 o más antiguas
columnas_valor = {"fecha_creacion": ["2018-12-31", "-"]}
tabla_filtrada = inventario.filtrar_tabla(columnas_valor)


# Cargar bases de datos con API id ya conocida
base = Datos("iwpe-6gqp")
base = Datos("k9pc-rjkh")
