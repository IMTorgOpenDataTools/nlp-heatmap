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


import argparse
import pandas as pd
from heatmap import HeatMapFormat
from report import Report


def read_data(input_file):
    """TODO"""
    sheets = pd.ExcelFile(input_file)
    df = pd.read_excel(input_file,
                        sheet_name=sheets.sheet_names[0],
                        skiprows=1
                        )
    return df

def create_excel_report(df, hmformat, writer):
    """TODO"""
    df.style.apply(hmformat.highlight_cells,
                            axis=1
                            ).to_excel(writer,
                                        sheet_name='Heatmap',
                                        engine='openpyxl'
                                        )

def create_index_report(output_dir, docs):
    """TODO"""
    template_path = './doc_extract/templates'
    template = 'index.html'
    template_data = {'records': docs}
    output_filepath = output_dir / template

    report = Report(template_path)
    html = report.create_report(template=template, 
                                template_args=template_data
                                )
    report.save_report(html, filepath=output_filepath)

def main(args):
    """ Main entry point of the app """
    df = read_data(args.input_file)
    hmformat = HeatMapFormat()
    match args.type:
        case 'xlsx':
            output_file = args.output_dir
            writer = pd.ExcelWriter(args.output_file, engine='xlsxwriter')
            create_excel_report(df, hmformat, writer)
        case 'html':
            hmformat.XXXX
            row_sums = df.sum(axis=0)
            idx_for_sums_column = df.columns.to_list().index('Q1')
            df.insert(idx_for_sums_column, 'Row_sums', row_sums)
            
            df.set_index('Name', inplace=True)
            df_long = df.melt(ignore_index=False).reset_index()
            create_index_report(args.output_dir, docs)


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