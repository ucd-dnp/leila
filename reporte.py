# -*- coding: utf-8 -*-
import argparse
import datetime
import pandas as pd

from jinja2 import FileSystemLoader
from jinja2 import Environment

from datos import data_summary
from datos import descriptive_stats
from datos import col_type
from datos import memoria
from datos import unique_col
from datos import unique_text

import os
import sys
import numpy as np

# Configure Jinja and ready the loader
env = Environment(loader=FileSystemLoader(searchpath='templates'))

# Assemble the templates we'll use
base_template = env.get_template('template_base.html')


def df_as_html(dataframe):
    # html = dataframe.to_html(table_id='mi_tabla', index=False, classes=['table', 'table-condensed', 'table-hover']) \
    html = dataframe.to_html(index=False, classes=['table', 'table-condensed', 'table-hover']) \
        .replace('table border="1" class="dataframe ', 'table class="')
    return html


def generar_reporte(dataframe):

    title = 'Reporte perfilamiento'
    timestamp = datetime.datetime.now()
    current_time = timestamp.strftime("%d-%m-%Y %I:%M:%S %p")

    # Estadísticas generales ----------------------------------------------------
    dataframe_summary = data_summary(dataframe).to_frame().reset_index()
    dataframe_summary.columns = ['Categoria', 'Valor']
    html_data_summary_00 = df_as_html(dataframe_summary)
    html_data_summary_01 = df_as_html(dataframe_summary[:6])
    html_data_summary_02 = df_as_html(dataframe_summary[-5:])

    # Tab 1 ---------------------------------------------------------------------
    dataframe_descriptive_stats = descriptive_stats(dataframe)
    dataframe_descriptive_stats = dataframe_descriptive_stats.T
    header_list = list(dataframe_descriptive_stats)
    dataframe_descriptive_stats = dataframe_descriptive_stats.reset_index()
    items = dataframe_descriptive_stats.values.tolist()

    # Tab 2 ---------------------------------------------------------------------
    tipo_df_low = col_type(dataframe, detail="low").to_frame()
    tipo_df_high = col_type(dataframe, detail="high").to_frame()
    dataframe_descriptive_stats_2 = pd.merge(tipo_df_low, tipo_df_high, left_index=True, right_index=True, how='outer')

    memoria_df = memoria(dataframe, col=True).to_frame()
    memoria_df = memoria_df.loc[~memoria_df.index.isin(['Index'])]
    dataframe_descriptive_stats_2 = pd.merge(dataframe_descriptive_stats_2, memoria_df, left_index=True, right_index=True, how='outer')

    valores_unicos_df = unique_col(dataframe).to_frame()
    dataframe_descriptive_stats_2 = pd.merge(dataframe_descriptive_stats_2, valores_unicos_df, left_index=True, right_index=True, how='outer')

    dataframe_descriptive_stats_2.columns = ['Tipo', 'Tipo (específico)', 'Memoria', 'Valores únicos']
    dataframe_descriptive_stats_2['Memoria'] = dataframe_descriptive_stats_2['Memoria'].map('{:,.6f}'.format)
    dataframe_descriptive_stats_2 = dataframe_descriptive_stats_2.T
    header_list_2 = list(dataframe_descriptive_stats_2)
    dataframe_descriptive_stats_2 = dataframe_descriptive_stats_2.reset_index()
    items_2 = dataframe_descriptive_stats_2.values.tolist()

    # Tab 3 ---------------------------------------------------------------------
    dataframe_unique_text = unique_text(dataframe)
    html_dataframe_unique_text = df_as_html(dataframe_unique_text)
    # ----------------------------------------------------------------------------

    # Produce and write the report to file
    with open("perfilamiento.html", "w", encoding='utf8') as HTML_file:
        output = base_template.render(
            title=title,
            current_time=current_time,
            html_data_summary_00=html_data_summary_00,
            html_data_summary_01=html_data_summary_01,
            html_data_summary_02=html_data_summary_02,
            header_list=header_list,
            items=items,
            header_list_2=header_list_2,
            items_2=items_2,
            html_dataframe_unique_text=html_dataframe_unique_text,
        )
        HTML_file.write(output)
    print('-----------------------------------------------------------------------')
    print('Se ha generado el reporte "perfilamiento.html"')
    print('dataframe shape:' + str(dataframe.shape))
    print(timestamp.strftime("%I:%M:%S %p"))
    print('-----------------------------------------------------------------------')


def main():
    # PyCharm > File > Settings > Inspections
    # https://docs.python.org/3/library/argparse.html

    parser = argparse.ArgumentParser(description='Analiza la calidad del dataframe suministrado '
                                                 'y genera un reporte HTML.')
    parser.add_argument('dataframe', help='path del dataframe que desea analizar')
    # parser.add_argument('out', default=os.getcwd(), help='path donde desea guardar el reporte HTML '
    #                                                      '(default: el path actual)')
    args = parser.parse_args()

    # print(args)
    df = pd.read_excel(args.dataframe)
    generar_reporte(dataframe=df)

    os.system('perfilamiento.html')


if __name__ == "__main__":
    main()
