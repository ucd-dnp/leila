# -*- coding: utf-8 -*-
import argparse
import datetime
import pandas as pd

from jinja2 import FileSystemLoader
from jinja2 import Environment

from datos import data_summary

import os
import sys
import numpy as np

# Configure Jinja and ready the loader
env = Environment(loader=FileSystemLoader(searchpath='templates'))

# Assemble the templates we'll use
base_template = env.get_template('template_base.html')


def generar_reporte(dataframe):
    title = 'Reporte perfilamiento'
    timestamp = datetime.datetime.now()
    current_time = timestamp.strftime("%d-%m-%Y %I:%M:%S %p")

    dataframe_summary = data_summary(dataframe).to_frame().reset_index()
    dataframe_summary.columns = ['categoria', 'valor']
    html_data_summary = dataframe_summary.to_html(table_id='mi_tabla', index=False) \
        .replace('table border="1" class="dataframe"', 'table border="1"')

    # Produce and write the report to file
    with open("perfilamiento.html", "w", encoding='utf8') as HTML_file:
        output = base_template.render(
            title=title,
            current_time=current_time,
            html_data_summary=html_data_summary
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


if __name__ == "__main__":
    main()
