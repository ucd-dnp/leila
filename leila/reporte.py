# -*- coding: utf-8 -*-

import os
import datetime
import pandas as pd
from jinja2 import Environment, PackageLoader

##### Quitar luego
import sys
sys.path.insert(0, "leila")
#####

from leila.calidad_datos import CalidadDatos
from leila.datos_gov import DatosGov

def df_as_html(base, id=None, classes=None):
    """ Transforma el dataframe de entrada en una tabla HTML, se asignan al tab table las clases 'table' y
    'table-condensed' utilizadas por `Bootstrap v3.4`_.

    .. _Bootstrap v3.4: https://getbootstrap.com/docs/3.4/

    :param base: (dataframe) dataframe de interés a ser transformado en tabla.
    :param id: (str) id que se le desea asignar a la tabla.
    :param classes: (list) lista de strings de las clases que se desean agregar a la tabla.
    :return: código de la tabla en formato HTML con los datos del dataframe.
    """
    # html = base.to_html(table_id='mi_tabla', index=False, classes=['table', 'table-condensed', 'table-hover']) \

    my_classes = ['table', 'table-condensed']
    if classes is not None:
        my_classes.extend(classes)

    html = base.to_html(index=False, table_id=id, classes=my_classes) \
        .replace('table border="1" class="dataframe ', 'table class="')
    return html


def generar_reporte(datos=None, titulo='Reporte perfilamiento', archivo='perfilamiento_leila.html', 
                    secciones = {'generales':True, 'muestra_datos': True, 'correlaciones': True, 
                    'especificas': ['tipo', 'frecuencias', 'duplicados_columnas', 'descriptivas']}, **kwargs):
    """Genera un reporte de calidad de datos en formato HTML. :ref:`Ver ejemplo <reporte.generar_reporte>`

    :param df: (dataframe) base de datos de insumo para la generación del reporte de calidad de datos.
    :param api_id: (str) opcional - Identificación de la base de datos asociado con la API de Socrata (de Datos Abiertos).
    :param titulo: (str) valor por defecto: 'Reporte perfilamiento'. Título del reporte a generar.
    :param archivo: (str) valor por defecto: 'perfilamiento.html'. Ruta donde guardar el reporte.    
    :param secciones: (dic) Diccionario indicando cuales secciones incluir en el reporte. Las opciones son las siguientes: \
         |ul| 
         |li| 'generales': (bool) {True, False}. Valor por defecto: True. Indica si desea incluir la sección de 'Estadísticas generales' en el reporte. |/li| 
         |li| 'muestra_datos': (bool) {True, False}. Valor por defecto: True. Indica si desea incluir la sección 'Muestra de datos' en el reporte. |/li| 
         |li| 'especificas': (bool/list) {True, False, Lista}. Valor por defecto: True. Puede tomar un valor boolean indicando \
                si desea incluir la sección de 'Estadísticas específicas' en el reporte. O mediante una lista de strings indicar \
                cuál pestaña de la sección incluir. Valores posibles: 'tipo', 'frecuencias', 'duplicados', 'duplicados_filas', \
                'duplicados_columnas', 'descriptivas' |/li|
         |li| 'correlaciones': (bool/list) {True, False, Lista}. Valor por defecto: True. Puede tomar un valor boolean indicando \
                si desea incluir la sección de 'Correlaciones' en el reporte. O mediante una lista de strings indicar \
                cuál pestaña de la sección incluir. Valores posibles: 'pearson','kendall','spearman','cramer','phik' |/li| 
         |/ul| 
    """

    link_datos_abiertos = None
    html_descr_col_meta = None
    html_metadatos_full = None
    html_metadatos_head = None
    html_metadatos_tail = None

    # if api_id is not None:
    if isinstance(datos, str):
        if datos == '':
            raise ValueError(
                "El parámetro datos no puede ser vacío"
            )
        try:
            # verifica si el string datos tiene extensión, en caso que no se asume que corresponde a un api_id
            temp = datos.split(".")[1]
            
            tipo = datos.split(".")[-1]
            base = CalidadDatos(datos)

        except Exception as e:
            if (str(e) == 'list index out of range'):
                
                # FIXME: BORRAR **kwargs
                datos = DatosGov().cargar_base(api_id=datos, **kwargs)

                base = CalidadDatos(datos)
                df_metadatos = pd.DataFrame.from_dict(datos.metadatos(), orient='index')

                desc_col = pd.DataFrame.from_dict(df_metadatos.loc['columnas', 0], orient='index')
                desc_col = desc_col.reset_index()
                desc_col = desc_col.rename(columns={"index": "Variable", "tipo": "Tipo", "descripcion":"Descripción", "nombre_df":"Nombre variable"})
                desc_col = desc_col[['Variable', 'Nombre variable', 'Tipo', 'Descripción']]

                df_metadatos = df_metadatos.drop("columnas")
                
                df_metadatos.loc['numero_vistas', 0] = str('{:,.0f}'.format(df_metadatos.loc['numero_vistas', 0]))
                df_metadatos.loc['numero_descargas', 0] = str('{:,.0f}'.format(df_metadatos.loc['numero_descargas', 0]))
                df_metadatos.loc['numero_filas', 0] = str('{:,.0f}'.format(df_metadatos.loc['numero_filas', 0]))
                df_metadatos.loc['numero_columnas', 0] = str('{:,.0f}'.format(df_metadatos.loc['numero_columnas', 0]))

                df_metadatos = df_metadatos.T
                df_metadatos = df_metadatos.rename(
                    columns={
                        "numero_api": "Número API",
                        "nombre": "Nombre",
                        "descripcion":"Descripción",
                        "tipo":"Tipo",
                        "url":"URL",
                        "categoria":"Categoría",
                        "fecha_creacion":"Fecha de creación",
                        "numero_vistas":"Número de vistas",
                        "numero_descargas":"Número de descargas",
                        "licencia":"Licencia",
                        "fecha_publicacion":"Fecha de publicación",
                        "base_publica":"Base pública",
                        "fecha_actualizacion":"Fecha de actualización",
                        "numero_filas":"Número de filas",
                        "numero_columnas":"Número de columnas",
                        "licencia_url":"Licencia URL",
                        "entidad":"Entidad",
                        "entidad_municipio":"Entidad municipio",
                        "entidad_sector":"Entidad sector",
                        "entidad_departamento":"Entidad departamento",
                        "entidad_orden":"Entidad orden",
                        "entidad_dependencia":"Entidad dependencia",
                        "cobertura":"Cobertura",
                        "idioma":"Idioma",
                        "frecuencia_actualizacion":"Frecuencia de actualización",
                        "dueno":"Dueño",
                    })
                df_metadatos = df_metadatos.T

                df_metadatos = df_metadatos.reset_index()
                df_metadatos.columns = ['Atributo', 'Valor']

                link_datos_abiertos = df_metadatos[df_metadatos['Atributo'] == 'URL']['Valor'].item()

                df_metadatos.replace('\n', '@#$', regex=True, inplace=True)

                html_descr_col_meta = df_as_html(
                    desc_col, classes=['white_spaces'])

                html_metadatos_full = df_as_html(
                    df_metadatos, classes=['white_spaces'])

                html_metadatos_head = df_as_html(
                    df_metadatos[:3], classes=['white_spaces'])

                html_metadatos_tail = df_as_html(
                    df_metadatos[-(len(datos.metadatos().keys()) - 4):], classes=['white_spaces'])

                html_metadatos_full = html_metadatos_full.replace('@#$', '<br>')
                html_metadatos_head = html_metadatos_head.replace('@#$', '<br>')
                html_metadatos_tail = html_metadatos_tail.replace('@#$', '<br>')
                print('--------------------------------------------------------------------------------------------')

    elif (datos.__class__.__name__ == 'CalidadDatos'):
        base = datos

    else:
        base = CalidadDatos(datos)

    timestamp = datetime.datetime.now()
    current_time = timestamp.strftime("%d-%m-%Y %I:%M:%S %p")

    # ------------------------------------------------------------------------
    # Estadísticas generales -------------------------------------------------
    if secciones.get('generales')==True:
        dataframe_summary = base.Resumen().to_frame().reset_index()
        dataframe_summary.columns = ['Categoría', 'Valor']

        try:
            dataframe_summary['Valor'] = dataframe_summary['Valor'].apply(
                '{:,.0f}'.format)
        except BaseException:
            pass

        html_data_summary_full = df_as_html(dataframe_summary)
        html_data_summary_head = df_as_html(dataframe_summary[:6])
        html_data_summary_tail = df_as_html(dataframe_summary[-6:])
    else:
        html_data_summary_full=None
        html_data_summary_head=None
        html_data_summary_tail=None

    # ------------------------------------------------------------------------
    # Muestra de datos -------------------------------------------------------
    if secciones.get('muestra_datos')==True:
        # Head
        html_dataframe_head = df_as_html(base.base.head(10))
        # Tail
        html_dataframe_tail = df_as_html(base.base.tail(10))
        # Shape
        df_shape = base.base.shape
        dataframe_shape = str('{:,.0f}'.format(
            df_shape[0])) + ' filas x ' + str('{:,.0f}'.format(df_shape[1])) + ' columnas'
    else:
        html_dataframe_head = None
        html_dataframe_tail = None
        dataframe_shape = None

    # ------------------------------------------------------------------------
    # Estadísticas específicas
    s_especificas=secciones.get('especificas')    
    seccion_especificas=False
    especificas_active=None

    # ------------------------------------------------------------------------
    if (isinstance(s_especificas, list) and 'tipo' in s_especificas) or (s_especificas==True):
    
        especificas_tipo=True
        seccion_especificas=True
        if especificas_active==None: especificas_active='tipo' 
        
        # Tab 5 - Tipo de las columnas -------------------------------------------
        tipo_columnas_df = base.TipoColumnas()

        df_headers = list(tipo_columnas_df)
        df_headers = [w.replace('tipo_general', 'Tipo general')
                      .replace('_python', ' (Python)')
                      .replace('tipo_especifico_', 'Tipo especifico ') for w in df_headers]
        tipo_columnas_df.columns = df_headers

        header_list_2 = list(tipo_columnas_df)
        variables_list_2 = list(tipo_columnas_df.T)

        tipo_columnas_df = tipo_columnas_df.reset_index()
        items_2 = tipo_columnas_df.values.tolist()
    else:
        especificas_tipo=False
        header_list_2=None
        variables_list_2=None
        items_2=None
        
    # ------------------------------------------------------------------------
    if (isinstance(s_especificas, list) and 'frecuencias' in s_especificas) or (s_especificas==True):
        
        especificas_frecuencias=True
        seccion_especificas=True
        if especificas_active==None: especificas_active='frecuencias' 
        
        # Tab 3 - Frecuencia de categorías ---------------------------------------
        dataframe_unique_text = base.DescripcionCategoricas()
        try:
            dataframe_unique_text['Frecuencia'] = dataframe_unique_text['Frecuencia'].apply(
                '{:,.0f}'.format)
        except BaseException:
            pass

        try:
            dataframe_unique_text['Porcentaje del total de filas'] = dataframe_unique_text[
                'Porcentaje del total de filas'].apply(lambda x: str(format(x * 100, ',.2f')) + '%')
        except BaseException:
            pass

        variables_list_3 = dataframe_unique_text.Columna.unique()
        columnas_list_3 = list(dataframe_unique_text)
        items_3 = dataframe_unique_text.values.tolist()
    else:
        especificas_frecuencias=False
        variables_list_3=None
        columnas_list_3=None
        items_3=None

    # ------------------------------------------------------------------------
    # TODO: REVISAR - emparejamiento de filas dejarlo en FALSE por defecto
    # if (isinstance(s_especificas, list) and 'duplicados' in s_especificas) or (s_especificas==True):
    if (isinstance(s_especificas, list) and any(item in ['duplicados', 'duplicados_filas', 'duplicados_columnas'] for item in s_especificas)) or (s_especificas==True):

        mensaje_duplicados = '<br><i>'
        seccion_especificas=True
        if especificas_active==None: especificas_active='duplicados'

        # Tab 4 - Datos duplicados -----------------------------------------------
        especificas_duplicados_filas=False
        especificas_duplicados_columnas=False
        html_dataframe_duplic_filas = None
        html_dataframe_duplic_colum = None

        if (isinstance(s_especificas, list) and any(item in ['duplicados', 'duplicados_filas'] for item in s_especificas)) or (s_especificas==True):
            especificas_duplicados_filas=True
            dataframe_duplic_filas = base.EmparejamientoDuplicados(col=False)

            if dataframe_duplic_filas is not None:
                filas_duplicadas = dataframe_duplic_filas.nunique().sum()
                filas_numero = base.base.shape[0]
                porcentaje_duplicados = (filas_duplicadas / filas_numero)
                mensaje_duplicados += f'Filas duplicadas {format(filas_duplicadas, ",.0f")} de {format(filas_numero, ",.0f")} ({str(format(porcentaje_duplicados * 100, ",.2f")) + "%"}). '

                dataframe_duplic_filas.fillna('', inplace=True)
                html_dataframe_duplic_filas = df_as_html(dataframe_duplic_filas, classes=['highlight_column'])

        if (isinstance(s_especificas, list) and any(item in ['duplicados', 'duplicados_columnas'] for item in s_especificas)) or (s_especificas==True):
            especificas_duplicados_columnas=True
            dataframe_duplic_colum = base.EmparejamientoDuplicados(col=True)
            
            if dataframe_duplic_colum is not None:
                col_duplicadas = dataframe_duplic_colum.nunique().sum()
                col_numero = base.base.shape[1]
                porcentaje_duplicados = col_duplicadas / col_numero
                mensaje_duplicados += f'Columnas duplicadas {format(col_duplicadas, ",.0f")} de {format(col_numero, ",.0f")} ({str(format(porcentaje_duplicados * 100, ",.2f")) + "%"}). '

                dataframe_duplic_colum.fillna('', inplace=True)
                html_dataframe_duplic_colum = df_as_html(dataframe_duplic_colum, classes=['highlight_column'])
        
        mensaje_duplicados += '</i>'
    else:
        especificas_duplicados_filas=False
        especificas_duplicados_columnas=False
        html_dataframe_duplic_filas=None
        html_dataframe_duplic_colum=None
        mensaje_duplicados=''

    # ------------------------------------------------------------------------
    if (isinstance(s_especificas, list) and 'descriptivas' in s_especificas) or (s_especificas==True):
    
        especificas_descriptivas=True
        seccion_especificas=True
        if especificas_active==None: especificas_active='descriptivas' 
        
        # Tab 6 - Estadísticas descriptivas --------------------------------------
        dataframe_descriptive_stats = base.DescripcionNumericas()

        header_list = None
        items = None
        variables_list = None
        if dataframe_descriptive_stats is not None:
            for col in ['freq', 'count', 'unique']:
                try:
                    dataframe_descriptive_stats[col] = dataframe_descriptive_stats[
                        col].apply('{:,.0f}'.format)
                except BaseException:
                    pass

            for col in ['mean', 'std', 'min', '25%', '50%', '75%', 'max']:
                try:
                    dataframe_descriptive_stats[col] = dataframe_descriptive_stats[
                        col].apply('{:,.2f}'.format)
                except BaseException:
                    pass

            for col in ['missing', 'outliers_total',
                        'outliers_altos', 'outliers_bajos']:
                try:
                    dataframe_descriptive_stats[col] = dataframe_descriptive_stats[
                        col].apply(lambda x: str(format(x * 100, ',.2f')) + '%')
                except BaseException:
                    pass

            df_headers = list(dataframe_descriptive_stats)
            df_headers = [w.replace('count', 'Conteo')
                          .replace('unique', 'Valores únicos')
                          .replace('mean', 'Media')
                          .replace('std', 'Desviación estándar')
                          .replace('min', 'Valor mín')
                          .replace('max', 'Valor máx')
                          .replace('missing', 'Faltantes')
                          .replace('outliers_', 'Outliers ')
                          .replace('top', 'Valor más común')
                          .replace('freq', 'Frecuencia valor más común') for w in df_headers]
            dataframe_descriptive_stats.columns = df_headers

            header_list = list(dataframe_descriptive_stats)
            variables_list = list(dataframe_descriptive_stats.T)
            dataframe_descriptive_stats = dataframe_descriptive_stats.reset_index()
            items = dataframe_descriptive_stats.values.tolist()
    else:
        especificas_descriptivas=False
        header_list=None
        variables_list=None
        items=None
        
    # ------------------------------------------------------------------------
    # Gráficos correlaciones -------------------------------------------------
    s_correlaciones=secciones.get('correlaciones')    
    seccion_correlaciones=False
    correlaciones_active=None

    # Escala de colores del heatmap
    heatmap_colorscale = [
        ['0.000000000000', 'rgb(103,  0, 31)'],
        ['0.111111111111', 'rgb(178, 24, 43)'],
        ['0.222222222222', 'rgb(214, 96, 77)'],
        ['0.333333333333', 'rgb(244,165,130)'],
        ['0.444444444444', 'rgb(253,219,199)'],
        ['0.555555555556', 'rgb(209,229,240)'],
        ['0.666666666667', 'rgb(146,197,222)'],
        ['0.777777777778', 'rgb( 67,147,195)'],
        ['0.888888888889', 'rgb( 33,102,172)'],
        ['1.000000000000', 'rgb(  5, 48, 97)']
    ]

    # Tab 1 - numérica - Pearson ---------------------------------------------
    if (isinstance(s_correlaciones, list) and 'pearson' in s_correlaciones) or (s_correlaciones==True):
        seccion_correlaciones=True
        if correlaciones_active==None: correlaciones_active='pearson'

        df_corre_pearson = base.CorrelacionNumericas(metodo="pearson")
        if df_corre_pearson is not None:
            corre_pearson_headers = list(df_corre_pearson)

            df_corre_pearson = df_corre_pearson.round(3).fillna('null')
            corre_pearson_values = df_corre_pearson.values.tolist()
        else:
            corre_pearson_headers=None
            corre_pearson_values=None
    else:
        corre_pearson_headers=None
        corre_pearson_values=None

    # Tab 2 - numérica - Kendall ---------------------------------------------
    if (isinstance(s_correlaciones, list) and 'kendall' in s_correlaciones) or (s_correlaciones==True):
        seccion_correlaciones=True
        if correlaciones_active==None: correlaciones_active='kendall'

        df_corre_kendall = base.CorrelacionNumericas(metodo="kendall")
        if df_corre_kendall is not None:
            corre_kendall_headers = list(df_corre_kendall)

            df_corre_kendall = df_corre_kendall.round(3).fillna('null')
            corre_kendall_values = df_corre_kendall.values.tolist()
        else:
            corre_kendall_headers=None
            corre_kendall_values=None    
    else:
        corre_kendall_headers=None
        corre_kendall_values=None    
    
    # Tab 3 - numérica - Pearson ---------------------------------------------
    if (isinstance(s_correlaciones, list) and 'spearman' in s_correlaciones) or (s_correlaciones==True):
        seccion_correlaciones=True
        if correlaciones_active==None: correlaciones_active='spearman'

        df_corre_spearman = base.CorrelacionNumericas(metodo="spearman")
        if df_corre_spearman is not None:
            corre_spearman_headers = list(df_corre_spearman)

            df_corre_spearman = df_corre_spearman.round(3).fillna('null')
            corre_spearman_values = df_corre_spearman.values.tolist()
        else:
            corre_spearman_headers=None
            corre_spearman_values=None
    else:
        corre_spearman_headers=None
        corre_spearman_values=None

    # Tab 4 - categórica - Cramer --------------------------------------------
    if (isinstance(s_correlaciones, list) and 'cramer' in s_correlaciones) or (s_correlaciones==True):
        seccion_correlaciones=True
        if correlaciones_active==None: correlaciones_active='cramer'

        df_corre_cramer = base.CorrelacionCategoricas(metodo="cramer")
        corre_cramer_headers = list(df_corre_cramer)

        df_corre_cramer = df_corre_cramer.round(3).fillna('null')
        corre_cramer_values = df_corre_cramer.values.tolist()
    else:
        corre_cramer_headers=None
        corre_cramer_values=None

    # Tab 5 - categórica - Phik ----------------------------------------------
    if (isinstance(s_correlaciones, list) and 'phik' in s_correlaciones) or (s_correlaciones==True):
        seccion_correlaciones=True
        if correlaciones_active==None: correlaciones_active='phik'

        df_corre_phik = base.CorrelacionCategoricas(metodo="phik")
        corre_phik_headers = list(df_corre_phik)

        df_corre_phik = df_corre_phik.round(3).fillna('null')
        corre_phik_values = df_corre_phik.values.tolist()
    else:
        corre_phik_headers=None
        corre_phik_values=None

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------
    
    # Configuración inicial de Jinja
    env = Environment(loader=PackageLoader('leila'))

    # Carga el template a utilizar
    base_template = env.get_template('template.html')

    # Generación del reporte
    reporte_full_path = ''
    with open(archivo, "w", encoding='utf8') as HTML_file:
        output = base_template.render(
            title=titulo,
            current_time=current_time,
            link_datos_abiertos=link_datos_abiertos,
            html_descr_col_meta=html_descr_col_meta,
            html_metadatos_full=html_metadatos_full,
            html_metadatos_head=html_metadatos_head,
            html_metadatos_tail=html_metadatos_tail,
            html_data_summary_full=html_data_summary_full,
            html_data_summary_head=html_data_summary_head,
            html_data_summary_tail=html_data_summary_tail,
            header_list=header_list,
            variables_list=variables_list,
            items=items,
            header_list_2=header_list_2,
            variables_list_2=variables_list_2,
            items_2=items_2,
            html_dataframe_head=html_dataframe_head,
            html_dataframe_tail=html_dataframe_tail,
            dataframe_shape=dataframe_shape,
            variables_list_3=variables_list_3,
            columnas_list_3=columnas_list_3,
            items_3=items_3,
            html_dataframe_duplic_filas=html_dataframe_duplic_filas,
            html_dataframe_duplic_colum=html_dataframe_duplic_colum,            
            generales=secciones.get('generales'),
            muestra_datos=secciones.get('muestra_datos'),
            seccion_especificas=seccion_especificas,
            especificas_active=especificas_active,
            especificas_tipo=especificas_tipo,
            especificas_frecuencias=especificas_frecuencias,
            especificas_duplicados_filas=especificas_duplicados_filas,
            especificas_duplicados_columnas=especificas_duplicados_columnas,
            mensaje_duplicados=mensaje_duplicados,
            especificas_descriptivas=especificas_descriptivas,            
            seccion_correlaciones=seccion_correlaciones,
            correlaciones_active=correlaciones_active,
            heatmap_colorscale=heatmap_colorscale,
            corre_pearson_headers=corre_pearson_headers,
            corre_pearson_values=corre_pearson_values,
            corre_kendall_headers=corre_kendall_headers,
            corre_kendall_values=corre_kendall_values,
            corre_spearman_headers=corre_spearman_headers,
            corre_spearman_values=corre_spearman_values,
            corre_cramer_headers=corre_cramer_headers,
            corre_cramer_values=corre_cramer_values,
            corre_phik_headers=corre_phik_headers,
            corre_phik_values=corre_phik_values
        )
        try:
            HTML_file.write(output)
            print(
                '--------------------------------------------------------------------------------------------')

            if archivo == 'perfilamiento_leila.html':
                if os.name == 'nt':
                    reporte_full_path = os.getcwd() + "\\" + archivo
                else:
                    import pathlib
                    reporte_full_path = str(
                        pathlib.Path().absolute()) + '/' + archivo
            else:
                reporte_full_path = archivo

            print(f'Se ha generado el reporte "{reporte_full_path}"')
            t1 = timestamp.strftime("%I:%M:%S %p")
            t2 = datetime.datetime.now()
            tiempo = str(t2 - timestamp).split(":")
            print(f"{t1} ({tiempo[1]} min {int(float(tiempo[2]))} seg)")

        except ValueError:
            print("Se presentó un error guardando el reporte HTML")

    try:
        print('--------------------------------------------------------------------------------------------')
        if os.name == 'nt':
            os.system(f'{reporte_full_path}')
    except FileNotFoundError:
        print("No se encontró el archivo reporte para abrir")
