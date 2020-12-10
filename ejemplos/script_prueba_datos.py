import pandas as pd

# importación libreria calidad de datos
from leila.calidad_datos import CalidadDatos

# Cargando base de datos de prueba
base = pd.read_excel("../../../1_Insumos/Bases_de_datos/dataset ejemplos.xlsx")


# creado objeto de la clase CalidadDatos, similar a pandas DataFrame

datos = CalidadDatos(base, castNumero=True)

# RESUMEN DE BASE DE DATOS
resumen = datos.Resumen(columnasRepetidas=False)
print(resumen)

# VARIANZA DE DATOS
varianza_perc = datos.VarianzaEnPercentil()
print(varianza_perc)

# Tipos de columnas
tipos_columnas = datos.TipoColumnas(
    tipoGeneral=True,
    tipoGeneralPython=True,
    tipoEspecifico=True)

print(tipos_columnas)

# Valores únicos en cada columna
# Sin faltantes
unicos_nofaltantes = datos.ValoresUnicos(faltantes=False)
print(unicos_nofaltantes)

# Con faltantes
unicos_sifaltantes = datos.ValoresUnicos(faltantes=True)
print(unicos_sifaltantes)

# Valores faltantes por columna
# En porcentaje
faltantes_prop = datos.ValoresFaltantes(numero=False)
print(faltantes_prop)

# En número
faltantes_num = datos.ValoresFaltantes(numero=True)
print(faltantes_num)

# Número y proporción de filas y columnas no únicas
# Proporción de columnas que no son únicas
repetidos_col_prop = datos.CantidadDuplicados(eje=1, numero=False)
print(repetidos_col_prop)

# Número de columnas repetidas
repetidos_col_num = datos.CantidadDuplicados(eje=1, numero=True)
print(repetidos_col_num)

# Proporción de filas repetidas
repetidos_fil_prop = datos.CantidadDuplicados(eje=0, numero=False)
print(repetidos_fil_prop)

# Número de filas que no son únicas
repetidos_fil_num = datos.CantidadDuplicados(eje=0, numero=True)
print(repetidos_fil_num)

# Emparejamiento de columnas y filas duplicadas
# Columnas duplicadas
duplicados_col = datos.EmparejamientoDuplicados(col=True)
print(duplicados_col)

# Filas duplicadas
duplicados_fil = datos.EmparejamientoDuplicados(col=False)
print(duplicados_fil)

# Valores extremos de cada columna
# Proporción de extremos totales
extremos_ambos_prop = datos.ValoresExtremos(extremos="ambos", numero=False)
print(extremos_ambos_prop)

# Número de extremos totales
extremos_ambos_num = datos.ValoresExtremos(extremos="ambos", numero=True)
print(extremos_ambos_num)

# Extremos altos proporción
extremos_sup_prop = datos.ValoresExtremos(extremos="superior", numero=False)
print(extremos_sup_prop)

# Extremos altos en número
extremos_sup_num = datos.ValoresExtremos(extremos="superior", numero=True)
print(extremos_sup_num)

# Extremos bajos proporción
extremos_inf_prop = datos.ValoresExtremos(extremos="inferior", numero=False)
print(extremos_inf_prop)

# Extremos bajos en número
extremos_inf_num = datos.ValoresExtremos(extremos="inferior", numero=True)
print(extremos_inf_num)

# Estadísticas descriptivas
estadisticas_descriptivas = datos.DescripcionNumericas()
print(estadisticas_descriptivas)

# Matrices de correlación para columnas numéricas
# Correlación Pearson
corr_pearson = datos.CorrelacionNumericas(metodo="pearson")
print(corr_pearson)

# Correlación Kendall
corr_kendall = datos.CorrelacionNumericas(metodo="kendall")
print(corr_kendall)

# Correlación Spearman
corr_spearman = datos.CorrelacionNumericas(metodo="spearman")
print(corr_spearman)

# Primeras frecuencias de variables categóricas
# No transformar números
categoricas_no_transformar = datos.DescripcionCategoricas(
    limite=0.5, incluirNumericos=False, variables=None)
print(categoricas_no_transformar)

# No transformar números
categoricas_transformar = datos.DescripcionCategoricas(
    limite=0.5, incluirNumericos=True, variables=None)
print(categoricas_transformar)

# Peso en la memoria de la base en mega bytes
# Peso total
peso_base = datos.Memoria(col=False)
print(peso_base)

# Peso total por columna
peso_base_cols = datos.Memoria(col=True)
print(peso_base_cols)

# Matrices de correlación para columnas categóricas
# Cramer V
matriz_cramer = datos.CorrelacionCategoricas(
    metodo='cramer',
    categoriasMaximas=30,
    limite=0.5,
    variables=None)
print(matriz_cramer)
# Phik
matriz_phik = datos.CorrelacionCategoricas(
    metodo='phik',
    categoriasMaximas=30,
    limite=0.5,
    variables=None)
print(matriz_phik)
