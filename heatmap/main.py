#!/usr/bin/env python3
"""
Module Docstring
Workflow:
* ...
* TODO
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from heatmap.heatmap import HeatMapFormat
from report import Report

import pandas as pd

import argparse
from pathlib import Path


def read_data(input_file):
    """Import data to dataframe.
    
    :param input_file(str) - path to input file
    :return df(pd.DataFrame) - df of input data
    """
    if input_file.suffix == '.csv':
        df = pd.read_csv(input_file)
    elif input_file.suffix == '.xlsx':
        sheets = pd.ExcelFile(input_file)
        df = pd.read_excel(input_file,
                            sheet_name=sheets.sheet_names[0],
                            skiprows=1
                            )
    else:
        print('ERRROR')
    return df

def create_excel_report(df, hmformat, writer):
    """Generate heatmap formatted excel file.
    
    :param df(pd.DataFrame) - df of input data
    :param hmformat(HeatMapFormat) - class for conditional formatting
    :param writer(pd.ExcelWriter) - excel writer class for output

    :return completed(bool) - whether function compeleted, correctly
    """
    df.style.apply(hmformat.highlight_cells,
                            axis=1
                            ).to_excel(writer,
                                        sheet_name='Heatmap',
                                        engine='openpyxl'
                                        )
    completed = True
    return completed

def create_index_report(output_dir, data):
    """Generate d3 html index file from template.
    
    :param output_dir(str) - filepath to output index.html
    :param data(pd.DataFrame) - df in long format 

    :return completed(bool) - whether function compeleted, correctly
    """
    template_path = './heatmap/templates'
    template = 'index.html'
    template_data = {'data': data.to_dict('records')}    #data.to_json(orient='records')}
    output_filepath = output_dir / template

    report = Report(template_path)
    html = report.create_report(template=template, 
                                template_args=template_data
                                )
    report.save_report(html, filepath=output_filepath)
    completed = True
    return completed


def main(args):
    """ Main entry point of the app """
    input_file = Path(args.input_file)
    output_dir = Path(args.output_dir)
    df = read_data(input_file)
    hmformat = HeatMapFormat()
    match args.output_type:
        case 'xlsx':
            output_file = output_dir / 'file.xlsx'
            writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
            create_excel_report(df, hmformat, writer)
        case 'html':
            df_num = pd.DataFrame(
                df.apply(func=hmformat.highlight_cells, 
                         axis=1, 
                         output_type='html'
                         ).to_list()
                )
            row_sums = df_num.sum(axis=1, skipna=True)
            scaled_row_sums = row_sums / row_sums.max()
            idx_for_sums_column = df.columns.to_list().index('Q1')
            df_orig = df.copy(deep=True)
            
            df_num.insert(idx_for_sums_column, 'RowSums', scaled_row_sums)
            df_num = pd.concat([pd.DataFrame(df['Name']), df_num.iloc[:,idx_for_sums_column:]], axis=1)
            df_num.sort_values(by='RowSums', inplace=True, ascending=False)
            df_num.set_index('Name', inplace=True)
            df_num_long = df_num.melt(ignore_index=False).reset_index()
            df_num_long.rename(columns={'Name':'NameNum','variable':'VarNum'}, inplace=True)

            df_orig.insert(idx_for_sums_column, 'RowSums', scaled_row_sums)
            df_orig.sort_values(by='RowSums', inplace=True, ascending=False)
            df_orig.set_index('Name', inplace=True)
            df_orig_long = df_orig.melt(ignore_index=False).reset_index()
            df_orig_long.rename(columns={'variable':'Question','value':'text'}, inplace=True)

            df_long = pd.concat([df_orig_long, df_num_long], axis=1)
            df_long.drop(columns=['NameNum','VarNum'], inplace=True)
            create_index_report(output_dir=output_dir, data=df_long)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("--input_file", help="Input file (.xlsx, .csv)")
    parser.add_argument("--output_dir", help="Output directory")
    parser.add_argument("--output_type", help="either: 'xlsx' or 'html'")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)