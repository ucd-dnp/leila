# -*- coding: utf-8 -*-
import os
import sys
import argparse
import datetime
import numpy as np
import pandas as pd

from jinja2 import FileSystemLoader
from jinja2 import Environment

from leila.calidad_datos import CalidadDatos
from leila import datos_gov


def df_as_html(base, id=None, classes=None):
    """ Transforma el dataframe de entrada en una tabla HTML, se asignan al tab table las clases 'table' y
    'table-condensed' utilizadas por `Bootstrap v3.4`_.

    .. _Bootstrap v3.4: https://getbootstrap.com/docs/3.4/

    :param id:
    :param classes:
    :param base: (dataframe) dataframe de interés a ser transformado en tabla.
    :return: código de tabla HTML con los datos del dataframe.
    """
    # html = base.to_html(table_id='mi_tabla', index=False, classes=['table', 'table-condensed', 'table-hover']) \

    my_classes = ['table', 'table-condensed']
    if classes is not None:
        my_classes.extend(classes)

    html = base.to_html(index=False, table_id=id, classes=my_classes) \
        .replace('table border="1" class="dataframe ', 'table class="')
    return html


def generar_reporte(df=None, api_id=None, token=None, titulo='Reporte perfilamiento',
                    archivo='perfilamiento_leila.html'):
    """Genera un reporte de calidad de datos en formato HTML

    :param token:
    :param api_id:
    :param df: (dataframe) base de datos de insumo para la generación del reporte de calidad de datos.
    :param titulo: (str) valor por defecto: 'Reporte perfilamiento'. Título del reporte a generar.
    :param archivo: (str) valor por defecto: 'perfilamiento.html'. Ruta donde guardar el reporte.
    :return: archivo de reporte en formato HTML.
    """

    base = CalidadDatos(df)
    link_datos_abiertos = None
    html_metadatos_full = None
    html_metadatos_head = None
    html_metadatos_tail = None

    if api_id is not None:
        datos = datos_gov.cargar_base(api_id=api_id)
        base = CalidadDatos(datos)

        inventario = datos_gov.tabla_inventario()
        df_metadatos = inventario[inventario['numero_api'] == api_id]
        df_metadatos = df_metadatos.T.reset_index()
        df_metadatos.columns = ['Atributo', 'Valor']

        link_datos_abiertos = df_metadatos[df_metadatos['Atributo'] == 'url']['Valor'].item()

        df_metadatos.replace('\n', '@#$', regex=True, inplace=True)
        html_metadatos_full = df_as_html(df_metadatos, classes=['white_spaces'])
        html_metadatos_head = df_as_html(df_metadatos[:3], classes=['white_spaces'])
        html_metadatos_tail = df_as_html(df_metadatos[-22:], classes=['white_spaces'])

        html_metadatos_full = html_metadatos_full.replace('@#$', '<br>')
        html_metadatos_head = html_metadatos_head.replace('@#$', '<br>')
        html_metadatos_tail = html_metadatos_tail.replace('@#$', '<br>')
        print('--------------------------------------------------------------------------------------------')

    timestamp = datetime.datetime.now()
    current_time = timestamp.strftime("%d-%m-%Y %I:%M:%S %p")

    # Estadísticas generales ----------------------------------------------------
    dataframe_summary = base.resumen(filas_nounicas=False).to_frame().reset_index()
    dataframe_summary.columns = ['Categoría', 'Valor']
    html_data_summary_full = df_as_html(dataframe_summary)
    html_data_summary_head = df_as_html(dataframe_summary[:5])
    html_data_summary_tail = df_as_html(dataframe_summary[-5:])

    # Muestra de datos ----------------------------------------------------------
    # Head
    html_dataframe_head = df_as_html(base.base.head(10))
    # Tail
    html_dataframe_tail = df_as_html(base.base.tail(10))
    # Shape
    df_shape = base.base.shape
    dataframe_shape = str(df_shape[0]) + ' filas x ' + str(df_shape[1]) + ' columnas'

    # Tab 1 - Información general -----------------------------------------------
    dataframe_descriptive_stats = base.descriptivas()

    header_list = None
    items = None
    if type(dataframe_descriptive_stats) != str:
        dataframe_descriptive_stats = dataframe_descriptive_stats.T
        header_list = list(dataframe_descriptive_stats)
        dataframe_descriptive_stats = dataframe_descriptive_stats.reset_index()
        items = dataframe_descriptive_stats.values.tolist()

    # Tab 2 - Estadísticas descriptivas -----------------------------------------
    tipo_df_low = base.col_tipo(detalle="bajo").to_frame()
    tipo_df_high = base.col_tipo(detalle="alto").to_frame()
    dataframe_descriptive_stats_2 = pd.merge(tipo_df_low, tipo_df_high, left_index=True, right_index=True, how='outer')

    memoria_df = base.memoria(col=True).to_frame()
    memoria_df = memoria_df.loc[~memoria_df.index.isin(['Index'])]
    dataframe_descriptive_stats_2 = pd.merge(dataframe_descriptive_stats_2, memoria_df, left_index=True,
                                             right_index=True, how='outer')

    valores_unicos_df = base.ValoresUnicos().to_frame()
    dataframe_descriptive_stats_2 = pd.merge(dataframe_descriptive_stats_2, valores_unicos_df, left_index=True,
                                             right_index=True, how='outer')

    dataframe_descriptive_stats_2.columns = ['Tipo', 'Tipo (específico)', 'Memoria', 'Valores únicos']
    dataframe_descriptive_stats_2['Memoria'] = dataframe_descriptive_stats_2['Memoria'].map('{:,.6f}'.format)
    dataframe_descriptive_stats_2 = dataframe_descriptive_stats_2.T
    header_list_2 = list(dataframe_descriptive_stats_2)
    dataframe_descriptive_stats_2 = dataframe_descriptive_stats_2.reset_index()
    items_2 = dataframe_descriptive_stats_2.values.tolist()

    # Tab 3 - Frecuencia de valores únicos --------------------------------------
    dataframe_unique_text = base.categorias()
    html_dataframe_unique_text = df_as_html(dataframe_unique_text)
    variables_list_3 = dataframe_unique_text.Columna.unique()
    columnas_list_3 = list(dataframe_unique_text)
    items_3 = dataframe_unique_text.values.tolist()

    # Tab 4 - Datos duplicados --------------------------------------------------
    html_dataframe_duplic_filas = None
    html_dataframe_duplic_colum = None

    dataframe_duplic_filas = base.ValoresDuplicados(col=False)
    if type(dataframe_duplic_filas) != str:
        html_dataframe_duplic_filas = df_as_html(dataframe_duplic_filas)

    dataframe_duplic_colum = base.ValoresDuplicados(col=True)
    if type(dataframe_duplic_colum) != str:
        html_dataframe_duplic_colum = df_as_html(dataframe_duplic_colum)

    # Gráficos correlaciones ----------------------------------------------------

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
    # Tab 1 - numérica - Pearson -----------------------------------------------------------
    df_corre_pearson = base.correlacion(metodo="pearson")
    corre_numericas_headers = list(df_corre_pearson)

    df_corre_pearson = df_corre_pearson.round(3).fillna('null')
    corre_pearson_values = df_corre_pearson.values.tolist()

    # Tab 2 - numérica - Kendall -----------------------------------------------------------
    df_corre_kendall = base.correlacion(metodo="kendall")
    df_corre_kendall = df_corre_kendall.round(3).fillna('null')
    corre_kendall_values = df_corre_kendall.values.tolist()

    # Tab 3 - numérica - Pearson -----------------------------------------------------------
    df_corre_spearman = base.correlacion(metodo="spearman")
    df_corre_spearman = df_corre_spearman.round(3).fillna('null')
    corre_spearman_values = df_corre_spearman.values.tolist()

    # Tab 4 - categórica - Cramer ----------------------------------------------------------
    # corre_categoricas_headers = None
    # corre_cramer_values = None

    df_corre_cramer = base.correlacion_categoricas(tipo="cramer")
    corre_cramer_headers = list(df_corre_cramer)

    df_corre_cramer = df_corre_cramer.round(3).fillna('null')
    corre_cramer_values = df_corre_cramer.values.tolist()

    # Tab 5 - categórica - Phik ------------------------------------------------------------
    df_corre_phik = base.correlacion_categoricas(tipo="phik")
    corre_phik_headers = list(df_corre_phik)

    df_corre_phik = df_corre_phik.round(3).fillna('null')
    corre_phik_values = df_corre_phik.values.tolist()
    # -----------------------------------------------__________-----------------------------

    # Configure Jinja and ready the loader    
    env = Environment(loader=FileSystemLoader(searchpath='.'))

    # Assemble the templates we'll use
    base_template = env.get_template('template_base_reporte.html')

    # Produce and write the report to file
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
            items=items,
            header_list_2=header_list_2,
            items_2=items_2,
            html_dataframe_unique_text=html_dataframe_unique_text,
            html_dataframe_head=html_dataframe_head,
            html_dataframe_tail=html_dataframe_tail,
            dataframe_shape=dataframe_shape,
            variables_list_3=variables_list_3,
            columnas_list_3=columnas_list_3,
            items_3=items_3,
            html_dataframe_duplic_filas=html_dataframe_duplic_filas,
            html_dataframe_duplic_colum=html_dataframe_duplic_colum,
            heatmap_colorscale=heatmap_colorscale,
            corre_numericas_headers=corre_numericas_headers,
            corre_pearson_values=corre_pearson_values,
            corre_kendall_values=corre_kendall_values,
            corre_spearman_values=corre_spearman_values,
            corre_cramer_headers=corre_cramer_headers,
            corre_cramer_values=corre_cramer_values,
            corre_phik_headers=corre_phik_headers,
            corre_phik_values=corre_phik_values
        )
        HTML_file.write(output)

    print('--------------------------------------------------------------------------------------------')
    print(f'Se ha generado el reporte "{ archivo }"')
    print(timestamp.strftime("%I:%M:%S %p"))
    print('--------------------------------------------------------------------------------------------')
    os.system(f'{ archivo }')


def main():
    # si se ingresan los parámetros api_id y df, el df correspondiente al api_id es utilizado y se ignora el df ingresado al invocar la función

    # covid-19
    generar_reporte(api_id="gt2j-8ykr", df=None)

    # generar_reporte(df=pd.read_excel('x_test_data.xlsx'))

    # generar_reporte(api_id="38wq-iims", df=pd.read_excel('x_test_data.xlsx'))
    # generar_reporte(df=pd.read_excel('error_test_1.xlsx'))
    # generar_reporte(df=pd.read_excel('error_test_2.xlsx'))

if __name__ == "__main__":
    main()
