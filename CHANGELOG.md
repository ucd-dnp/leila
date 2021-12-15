# Changelog *LEILA*

Todos los cambios importantes de esta librería serán documentados en este archivo.

## 0.2.0 (2021-12-15)
### Agregado
- Se agrega sección ***Columnas en este conjunto de datos*** en reportes generados para conjuntos del portal de [Datos Abiertos Colombia ](https://www.datos.gov.co/) mediante la función [generar_reporte()](https://ucd-dnp.github.io/leila/versiones/master/funciones/reporte.html#reporte.generar_reporte) del módulo *reporte*.
- Se agregó la función [DatosGov.metadatos()](https://ucd-dnp.github.io/leila/versiones/master/funciones/datos_gov.html#datos_gov.DatosGov.metadatos) para consultar los metadatos del conjunto de datos de interés publicado en el portal de [Datos Abiertos Colombia ](https://www.datos.gov.co/).
- Se agregó la función [DatosGov.to_dataframe()](https://ucd-dnp.github.io/leila/versiones/master/funciones/datos_gov.html#datos_gov.DatosGov.to_dataframe) para retornar el conjunto de datos descargado del portal [Datos Abiertos Colombia ](https://www.datos.gov.co/) en formato pandas.DataFrame

### Cambiado
#### Código

* Se reestructuró el modulo [datos_gov](https://ucd-dnp.github.io/leila/versiones/master/funciones/datos_gov.html#) en la clase [DatosGov()](https://ucd-dnp.github.io/leila/versiones/master/funciones/datos_gov.html#datos_gov.DatosGov) 
* Se agregó parámetro *filtro* dentro de la función [tabla_inventario()](https://ucd-dnp.github.io/leila/versiones/master/funciones/datos_gov.html#datos_gov.DatosGov.tabla_inventario) del módulo [datos_gov](https://ucd-dnp.github.io/leila/versiones/master/funciones/datos_gov.html#) , que permite filtrar por palabras clave. 
* Se reemplazó el parámetro *df* por *datos* dentro de la función [generar_reporte()](https://ucd-dnp.github.io/leila/versiones/master/funciones/reporte.html#reporte.generar_reporte) 
* Se agregó soporte para lectura directa de archivos tipo '.xlsx', y '.csv' por parte de la clase [CalidadDatos()](https://ucd-dnp.github.io/leila/versiones/master/funciones/calidad_datos.html#calidad_datos.CalidadDatos) 
* Se agregó soporte para lectura directa de objetos tipo [leila.DatosGov()](https://ucd-dnp.github.io/leila/versiones/master/funciones/datos_gov.html#datos_gov.DatosGov) por parte de la clase [CalidadDatos()](https://ucd-dnp.github.io/leila/versiones/master/funciones/calidad_datos.html#calidad_datos.CalidadDatos) 
* Se agregó parámetro *especificas* dentro de la función [generar_reporte()](https://ucd-dnp.github.io/leila/versiones/master/funciones/reporte.html#reporte.generar_reporte), que permite personalizar el reporte automático.

- Se agregó el parámetro 'limite_filas' a los métodos 'CantidadDuplicados' y 'EmparejamientoDuplicados' de la clase 'CalidadDatos'. Este parámetro define el límite de filas que se tendrá en cuenta al calcular los duplicados por columnas (el valor por defecto es 30.000)
- Se ajustó el código de los siguientes métodos de la clase 'CalidadDatos', para no copiar el conjunto de datos de entrada y evitar problemas de memoria: CorrelacionCategoricas, DescripcionNumericas, DescripcionCategoricas, CantidadDuplicados, EmparejamientoDuplicados
- Se adecuó el código de la librería al estilo PEP-8
- Se ajustó el código del método 'TipoColumnas' de la clase CalidadDatos para mejorar los tiempos de ejecución
- Se adecuó el código de la clase CalidadDatos para que el tipo específico y el tipo general de las columnas se calculen cuando se crea la clase y no cuando se ejecutan los métodos que hacen uso de los tipos
- Los módulos "calidad_datos" y "reporte" tendrán el nuevo parámetro "castDatos", el cual indica si se desean convertir las columnas al mejor tipo de columna, según la función 'convert_dtypes' de la librería Pandas. Este parámetro remplazará a "castNumero", el cual será deprecado en un futuro

#### Repositorio
- Se redactó guía en GitHub en español para reportar issues en la librería 
- Se redactó guía en español para realizar colaboraciones y adiciones a la librería en GitHub
- Se añaden nuevos ejemplos de uso de la librería en la carpeta de [ejemplos](https://github.com/ucd-dnp/leila/tree/master/ejemplos)
- Se actualiza documentación de LEILA con respecto a los nuevos cambios.

#### Memoria y tiempo de ejecución

* Se mejoró los tiempos de ejecución para las funciones 'CantidadDuplicados' y 'EmparejamientoDuplicados' de  la clase 'CalidadDatos'

- Se redujeron los tiempos de ejecución generales y los requisitos de memoria. 
- Las funciones de la librería se pueden ejecutar para conjuntos de datos más grandes
- Las funciones generan resultados más rápidos para los mismos conjuntos de datos 

### Wiki de LEILA
El [Wiki de LEILA](https://github.com/ucd-dnp/leila/wiki) se encuentra en el repositorio web de GitHub y contiene la siguiente información: 

- Proceso de trabajo de los desarrolladores de LEILA
- Guía para hacer preguntas de uso, reportar errores y solicitar nuevas características para LEILA
- Guía para hacer contribuciones y pull-request a LEILA
- Reglas de comunidad

### Obsoleto

* Ya no es necesario el parámetro *token* dentro de las funciones [cargar_base()]() y en [generar_reporte()]() 

### Borrado

* Se eliminó función [filtrar_tabla()](https://ucd-dnp.github.io/leila/versiones/v0.1b/funciones/datos_gov.html#datos_gov.filtrar_tabla) del módulo [datos_gov()](https://ucd-dnp.github.io/leila/versiones/master/funciones/datos_gov.html#) 

### Arreglado
- Se corrigieron errores generados por conflictos de librerías de soporte al instalar la librería
