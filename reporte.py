# -*- coding: utf-8 -*-
import argparse
import datetime
import pandas as pd

from jinja2 import FileSystemLoader
from jinja2 import Environment

from datos import resumen_base
from datos import descriptivas
from datos import col_tipo
from datos import memoria
from datos import unicos
from datos import categorias
from datos import duplic
from datos import correlacion

from metadatos import sodapy_base
from metadatos import mostrar_metadatos

import os
import sys
import numpy as np

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#pd.set_option('max_colwidth', None)

# https://pandas.pydata.org/docs/user_guide/options.html

# pd.set_option('precision', 7)
# pd.reset_option('max_colwidth')
# pd.reset_option("display.max_columns")
# pd.reset_option("^display")

# pd.get_option('max_colwidth')
# pd.get_option('display.max_columns')
# pd.get_option('display.max_rows')

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_columns', 30)
# pd.set_option('max_colwidth',150)


# hablar con pablo
# try > catch | filas_nounicas




def df_as_html(base, id=None, classes=None):
    """ Transforma el dataframe de entrada en una tabla HTML, se asignan al tab table las clases 'table' y
    'table-condensed' utilizadas por `Bootstrap v3.4`_.

    .. _Bootstrap v3.4: https://getbootstrap.com/docs/3.4/

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


def generar_reporte(my_base=None, api_id=None, token=None, titulo='Reporte perfilamiento', archivo='perfilamiento.html'):
    """Genera un reporte de calidad de datos en formato HTML

    :param token:
    :param api_id:
    :param my_base: (dataframe) base de datos de insumo para la generación del reporte de calidad de datos.
    :param titulo: (str) valor por defecto: 'Reporte perfilamiento'. Título del reporte a generar.
    :param archivo: (str) valor por defecto: 'perfilamiento.html'. Ruta donde guardar el reporte.
    :return: archivo de reporte en formato HTML.
    """

    base = my_base
    link_datos_abiertos = None
    html_metadatos_00 = None
    html_metadatos_01 = None
    html_metadatos_02 = None

    if api_id is not None:
        metadatos_base = sodapy_base(api_id=api_id, token=token)
        base = metadatos_base

        serie_metadatos = mostrar_metadatos(api_id=api_id, token=token)
        link_datos_abiertos = serie_metadatos['URL']

        df_metadatos = serie_metadatos.to_frame().reset_index()
        df_metadatos.replace('\n', '@@@', regex=True, inplace=True)
        df_metadatos.columns = ['Categoría', 'Valor']
        html_metadatos_00 = df_as_html(df_metadatos, classes=['white_spaces'])
        html_metadatos_01 = df_as_html(df_metadatos[:3], classes=['white_spaces'])
        html_metadatos_02 = df_as_html(df_metadatos[-22:], classes=['white_spaces'])

        html_metadatos_00 = html_metadatos_00.replace('@@@', '<br>')
        html_metadatos_01 = html_metadatos_01.replace('@@@', '<br>')
        html_metadatos_02 = html_metadatos_02.replace('@@@', '<br>')

    print('------------------------------------------------------------------')

    timestamp = datetime.datetime.now()
    current_time = timestamp.strftime("%d-%m-%Y %I:%M:%S %p")

    # Estadísticas generales ----------------------------------------------------
    dataframe_summary = resumen_base(base, filas_nounicas=False).to_frame().reset_index()
    dataframe_summary.columns = ['Categoría', 'Valor']
    html_data_summary_00 = df_as_html(dataframe_summary)
    html_data_summary_01 = df_as_html(dataframe_summary[:6])
    html_data_summary_02 = df_as_html(dataframe_summary[-5:])

    # Muestra de datos ----------------------------------------------------------
    # Head
    html_dataframe_head = df_as_html(base.head(10))
    # Tail
    html_dataframe_tail = df_as_html(base.tail(10))
    # Shape
    df_shape = base.shape
    dataframe_shape = str(df_shape[0]) + ' filas x ' + str(df_shape[1]) + ' columnas'

    # Tab 1 ---------------------------------------------------------------------
    dataframe_descriptive_stats = descriptivas(base)
    header_list = None
    items = None
    if type(dataframe_descriptive_stats) != str:
        dataframe_descriptive_stats = dataframe_descriptive_stats.T
        header_list = list(dataframe_descriptive_stats)
        dataframe_descriptive_stats = dataframe_descriptive_stats.reset_index()
        items = dataframe_descriptive_stats.values.tolist()

    # Tab 2 ---------------------------------------------------------------------
    tipo_df_low = col_tipo(base, detalle="bajo").to_frame()
    tipo_df_high = col_tipo(base, detalle="alto").to_frame()
    dataframe_descriptive_stats_2 = pd.merge(tipo_df_low, tipo_df_high, left_index=True, right_index=True, how='outer')

    memoria_df = memoria(base, col=True).to_frame()
    memoria_df = memoria_df.loc[~memoria_df.index.isin(['Index'])]
    dataframe_descriptive_stats_2 = pd.merge(dataframe_descriptive_stats_2, memoria_df, left_index=True, right_index=True, how='outer')

    valores_unicos_df = unicos(base).to_frame()
    dataframe_descriptive_stats_2 = pd.merge(dataframe_descriptive_stats_2, valores_unicos_df, left_index=True, right_index=True, how='outer')

    dataframe_descriptive_stats_2.columns = ['Tipo', 'Tipo (específico)', 'Memoria', 'Valores únicos']
    dataframe_descriptive_stats_2['Memoria'] = dataframe_descriptive_stats_2['Memoria'].map('{:,.6f}'.format)
    dataframe_descriptive_stats_2 = dataframe_descriptive_stats_2.T
    header_list_2 = list(dataframe_descriptive_stats_2)
    dataframe_descriptive_stats_2 = dataframe_descriptive_stats_2.reset_index()
    items_2 = dataframe_descriptive_stats_2.values.tolist()

    # Tab 3 ---------------------------------------------------------------------
    dataframe_unique_text = categorias(base)
    html_dataframe_unique_text = df_as_html(dataframe_unique_text)
    variables_list_3 = dataframe_unique_text.Columna.unique()
    columnas_list_3 = list(dataframe_unique_text)
    items_3 = dataframe_unique_text.values.tolist()

    # Tab 4 ---------------------------------------------------------------------
    dataframe_duplic01 = duplic(base, col=False)
    html_dataframe_duplic01 = None
    html_dataframe_duplic02 = None
    if type(dataframe_duplic01) != str:
        html_dataframe_duplic01 = df_as_html(dataframe_duplic01)
        dataframe_duplic02 = duplic(base, col=True)
        html_dataframe_duplic02 = df_as_html(dataframe_duplic02)

    # Gráficos correlaciones ----------------------------------------------------
    # https://codepen.io/antoinerg/pen/NLboJw

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
    # Tab 1 - Pearson -----------------------------------------------------------
    df_corre_pearson = correlacion(base, metodo="pearson")
    #df_corre_pearson = correlacion(base, metodo="pearson", variables=['FechaCreacion', 'Alto', 'Largo', 'CapacidadPeso', 'Valor Total Local'])

    df_corre_pearson = df_corre_pearson.round(3).fillna('null')
    corre_pearson_headers = list(df_corre_pearson)
    corre_pearson_values = df_corre_pearson.values.tolist()

    # Tab 2 - Kendall -----------------------------------------------------------
    df_corre_kendall = correlacion(base, metodo="kendall")
    #df_corre_kendall = correlacion(base, metodo="kendall", variables=['FechaCreacion', 'Alto', 'Largo', 'CapacidadPeso', 'Valor Total Local'])

    df_corre_kendall = df_corre_kendall.round(3).fillna('null')
    corre_kendall_headers = list(df_corre_kendall)
    corre_kendall_values = df_corre_kendall.values.tolist()

    # Tab 3 - Pearson -----------------------------------------------------------
    df_corre_spearman = correlacion(base, metodo="spearman")
    #df_corre_spearman = correlacion(base, metodo="spearman", variables=['FechaCreacion', 'Alto', 'Largo', 'CapacidadPeso', 'Valor Total Local'])

    df_corre_spearman = df_corre_spearman.round(3).fillna('null')
    corre_spearman_headers = list(df_corre_spearman)
    corre_spearman_values = df_corre_spearman.values.tolist()

    # ----------------------------------------------------------------------------

    # Configure Jinja and ready the loader    
    env = Environment(loader=FileSystemLoader(searchpath='templates'))

    # Assemble the templates we'll use
    base_template = env.get_template('template_base.html')

    # Produce and write the report to file
    with open(archivo, "w", encoding='utf8') as HTML_file:
        output = base_template.render(
            title=titulo,
            current_time=current_time,
            link_datos_abiertos=link_datos_abiertos,
            html_metadatos_00=html_metadatos_00,
            html_metadatos_01=html_metadatos_01,
            html_metadatos_02=html_metadatos_02,
            html_data_summary_00=html_data_summary_00,
            html_data_summary_01=html_data_summary_01,
            html_data_summary_02=html_data_summary_02,
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
            html_dataframe_duplic01=html_dataframe_duplic01,
            html_dataframe_duplic02=html_dataframe_duplic02,
            heatmap_colorscale=heatmap_colorscale,
            corre_pearson_headers=corre_pearson_headers,
            corre_pearson_values=corre_pearson_values,
            corre_kendall_headers=corre_kendall_headers,
            corre_kendall_values=corre_kendall_values,
            corre_spearman_headers=corre_spearman_headers,
            corre_spearman_values=corre_spearman_values
        )
        HTML_file.write(output)
    print('-----------------------------------------------------------------------')
    print('Se ha generado el reporte "perfilamiento.html"')
    print('dataframe shape:' + str(base.shape))
    print(timestamp.strftime("%I:%M:%S %p"))
    print('-----------------------------------------------------------------------')


def main():
    # PyCharm > File > Settings > Inspections
    # https://docs.python.org/3/library/argparse.html

    #parser = argparse.ArgumentParser(description='Analiza la calidad del dataframe suministrado '
    #                                             'y genera un reporte HTML.')
    #parser.add_argument('dataframe', help='path del dataframe que desea analizar')
    # parser.add_argument('out', default=os.getcwd(), help='path donde desea guardar el reporte HTML '
    #                                                      '(default: el path actual)')
    #args = parser.parse_args()

    # print(args)
    #df = pd.read_excel(args.dataframe)
    #api_id = args.dataframe

    #generar_reporte(api_id="38wq-iims", my_base=pd.read_excel('x_test_data.xlsx'))
    generar_reporte(api_id="gt2j-8ykr", my_base=pd.read_excel('x_test_data.xlsx'))

    os.system('perfilamiento.html')


if __name__ == "__main__":
    main()
