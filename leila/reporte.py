# -*- coding: utf-8 -*-

import os
import datetime
import pandas as pd
from jinja2 import Environment, PackageLoader

# Se deben usar estos imports para que funcione correctamente Sphinx
# from calidad_datos import CalidadDatos
# from datos_gov import *

from leila.calidad_datos import CalidadDatos
from leila.datos_gov import Datos, Inventario

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


def generar_reporte(df=None, api_id=None, token=None, titulo='Reporte perfilamiento',
                    archivo='perfilamiento_leila.html', castNumero=False, 
                    muestra_datos=True, correlaciones=True, especificas=True):
    """Genera un reporte de calidad de datos en formato HTML. :ref:`Ver ejemplo <reporte.generar_reporte>`

    :param castNumero: (bool) {True, False}. Valor por defecto: False. \
            Indica si se desea convertir las columnas de tipos object y bool a float, de ser posible.
    :param df: (dataframe) base de datos de insumo para la generación del reporte de calidad de datos.
    :param api_id: (str) opcional - Identificación de la base de datos asociado con la API de Socrata (de Datos Abiertos).
    :param token: (str) opcional - Token de usuario de la API de Socrata (de Datos Abiertos).
    :param titulo: (str) valor por defecto: 'Reporte perfilamiento'. Título del reporte a generar.
    :param archivo: (str) valor por defecto: 'perfilamiento.html'. Ruta donde guardar el reporte.
    :param muestra_datos: (bool) {True, False}. Valor por defecto: True. \
            Indica si desea incluir la sección de 'Muestra de datos' en el reporte.
    :param correlaciones: (bool) {True, False}. Valor por defecto: True. \
            Indica si desea incluir la sección de correlaciones en el reporte.
    :param especificas: (bool) {True, False}. Valor por defecto: True.
            Indica si desea incluir la sección de 'Estadísticas específicas' en el reporte.
    :return: archivo de reporte en formato HTML.
    """

    link_datos_abiertos = None
    html_metadatos_full = None
    html_metadatos_head = None
    html_metadatos_tail = None

    if api_id is not None:
        datos = Datos(api_id=api_id, token=token)
        base = CalidadDatos(datos, castNumero=castNumero)

        inventario = Inventario(token=token)
        df_metadatos = inventario.inventario._base[inventario.inventario._base['numero_api'] == api_id]

        df_metadatos.columns = ['Id api', 'Nombre', 'Descripción', 'Propietario', 'Tipo', 'Categoría', 'Términos clave',
                                'Página web', 'Fecha de creación', 'Fecha de actualización',
                                'Frecuencia de actualización', 'Número de filas', 'Número de columnas',
                                'Correo de contacto', 'Licencia', 'Entidad', 'Página web de la entidad',
                                'Sector entidad', 'Departamento entidad', 'Orden entidad', 'Dependencia entidad',
                                'Municipio entidad', 'Idioma', 'Cobertura', '¿Es pública la base?']
        df_metadatos = df_metadatos[['Id api', 'Nombre', 'Descripción', 'Propietario', 'Tipo', 'Categoría',
                                     'Términos clave', 'Página web', 'Fecha de creación', 'Fecha de actualización',
                                     'Frecuencia de actualización', 'Número de filas', 'Número de columnas',
                                     'Entidad', 'Dependencia entidad', 'Sector entidad', 'Página web de la entidad',
                                     'Correo de contacto', 'Licencia', 'Departamento entidad', 'Municipio entidad',
                                     'Orden entidad', 'Idioma', 'Cobertura', '¿Es pública la base?']]
        df_metadatos = df_metadatos.T.reset_index()
        df_metadatos.columns = ['Atributo', 'Valor']
        try:
            df_metadatos['Valor'] = df_metadatos['Valor'].apply(
                '{:,.0f}'.format)
        except BaseException:
            pass

        link_datos_abiertos = df_metadatos[df_metadatos['Atributo']
                                           == 'Página web']['Valor'].item()

        df_metadatos.replace('\n', '@#$', regex=True, inplace=True)
        html_metadatos_full = df_as_html(
            df_metadatos, classes=['white_spaces'])
        html_metadatos_head = df_as_html(
            df_metadatos[:3], classes=['white_spaces'])
        html_metadatos_tail = df_as_html(
            df_metadatos[-22:], classes=['white_spaces'])

        html_metadatos_full = html_metadatos_full.replace('@#$', '<br>')
        html_metadatos_head = html_metadatos_head.replace('@#$', '<br>')
        html_metadatos_tail = html_metadatos_tail.replace('@#$', '<br>')
        print('--------------------------------------------------------------------------------------------')
    else:
        base = CalidadDatos(df, castNumero=castNumero)

    timestamp = datetime.datetime.now()
    current_time = timestamp.strftime("%d-%m-%Y %I:%M:%S %p")

    # ------------------------------------------------------------------------
    # Estadísticas generales -------------------------------------------------
    if base.Resumen() is None:
        return
    
    dataframe_summary = base.Resumen().to_frame().reset_index()
    dataframe_summary.columns = ['Categoría', 'Valor']

    try:
        dataframe_summary['Valor'] = dataframe_summary['Valor'].apply(
            '{:,.0f}'.format)
    except BaseException:
        pass

    html_data_summary_full = df_as_html(dataframe_summary)
    html_data_summary_head = df_as_html(dataframe_summary[:6])
    html_data_summary_tail = df_as_html(dataframe_summary[-5:])

    # ------------------------------------------------------------------------
    # Muestra de datos -------------------------------------------------------
    if muestra_datos:
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
    if especificas:
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

        # ------------------------------------------------------------------------
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

        # ------------------------------------------------------------------------
        # Tab 4 - Datos duplicados -----------------------------------------------
        html_dataframe_duplic_filas = None
        html_dataframe_duplic_colum = None

        dataframe_duplic_filas = base.EmparejamientoDuplicados(col=False)
        if dataframe_duplic_filas is not None:
            html_dataframe_duplic_filas = df_as_html(dataframe_duplic_filas)

        dataframe_duplic_colum = base.EmparejamientoDuplicados(col=True)
        if dataframe_duplic_colum is not None:
            html_dataframe_duplic_colum = df_as_html(dataframe_duplic_colum)

        # ------------------------------------------------------------------------
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
        header_list=None
        variables_list=None
        items=None
        header_list_2=None
        variables_list_2=None
        items_2=None
        html_dataframe_head=None
        html_dataframe_tail=None
        dataframe_shape=None
        variables_list_3=None
        columnas_list_3=None
        items_3=None
        html_dataframe_duplic_filas=None
        html_dataframe_duplic_colum=None

    # ------------------------------------------------------------------------
    # Gráficos correlaciones -------------------------------------------------
    if correlaciones:
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
        df_corre_pearson = base.CorrelacionNumericas(metodo="pearson")
        corre_pearson_headers = list(df_corre_pearson)

        df_corre_pearson = df_corre_pearson.round(3).fillna('null')
        corre_pearson_values = df_corre_pearson.values.tolist()

        # Tab 2 - numérica - Kendall ---------------------------------------------
        df_corre_kendall = base.CorrelacionNumericas(metodo="kendall")
        corre_kendall_headers = list(df_corre_kendall)

        df_corre_kendall = df_corre_kendall.round(3).fillna('null')
        corre_kendall_values = df_corre_kendall.values.tolist()

        # Tab 3 - numérica - Pearson ---------------------------------------------
        df_corre_spearman = base.CorrelacionNumericas(metodo="spearman")
        corre_spearman_headers = list(df_corre_spearman)

        df_corre_spearman = df_corre_spearman.round(3).fillna('null')
        corre_spearman_values = df_corre_spearman.values.tolist()

        # Tab 4 - categórica - Cramer --------------------------------------------
        df_corre_cramer = base.CorrelacionCategoricas(metodo="cramer")
        corre_cramer_headers = list(df_corre_cramer)

        df_corre_cramer = df_corre_cramer.round(3).fillna('null')
        corre_cramer_values = df_corre_cramer.values.tolist()

        # Tab 5 - categórica - Phik ----------------------------------------------
        df_corre_phik = base.CorrelacionCategoricas(metodo="phik")
        corre_phik_headers = list(df_corre_phik)

        df_corre_phik = df_corre_phik.round(3).fillna('null')
        corre_phik_values = df_corre_phik.values.tolist()

    else:
        heatmap_colorscale=None
        corre_pearson_headers=None
        corre_pearson_values=None
        corre_kendall_headers=None
        corre_kendall_values=None
        corre_spearman_headers=None
        corre_spearman_values=None
        corre_cramer_headers=None
        corre_cramer_values=None
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
            corre_phik_values=corre_phik_values,
            muestra_datos=muestra_datos,
            correlaciones=correlaciones,
            especificas=especificas
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
