#!/usr/bin/env python3
"""
Module for Status Heatmap Project.

Class:
    HeatMapFormat
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import pandas as pd
import numpy as np


class HeatMapFormat:
    """Formatting for heatmap output based on conditions for each
    individual question.

    Usage:
    >>> import heatmap_format as hf
    >>> hmformat = hf.HeatMapFormatting()
    >>> writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    >>> df.style.apply(hmformat.highlight_cells,
                        axis=1
                        ).to_excel(writer,
                                    sheet_name='Heatmap',
                                    engine='openpyxl'
                                    )
    """

    def __init__(self, config=None):
        """Create an object of type HeatMapFormat.  Depends on 
        configuration data.
        
        :param config(dict) - contains mapping of question values to 
        category's numeric value with colors
        :return None
        """
        if config:
            self.config = config

    #config attrs
    output_types = ['xlsx', 'html']

    config = {
        'missing' : {'numeric':None, 'bg':'gray', 'fc':'black'},
        'not_applicable' : {'numeric':None, 'bg':'white', 'fc':'black'},
        'safe' : {'numeric':0, 'bg':'#58f931', 'fc':'black'},
        'neutral' : {'numeric':0.5, 'bg':'#FFEB51', 'fc':'black'},
        'danger' : {'numeric':1.0, 'bg':'##ff2e1b', 'fc':'white'}
    }

    #support methods
    def get_status_category_from_numeric(self, numeric):
        """Covert the numeric value to the config's status category.

        :param numeric(float) - numeric value matched to config's numeric
        :return status_category(str) - key value in config
        """
        if 0 <= numeric <= 1.0:
            status_pairs = [(v['numeric'],k) for k,v in self.config.items() if v['numeric']!=None]
            pair = [p for p in status_pairs if p[0]>=numeric][0]
            status_category = pair[1]
        else:
            print('ERRROR')
        return status_category

    def convert_to_output_type(self, output_type, status):
        """Get the approprite output for the user-provided output_type."""
        if status['status_category']:
            val = status['status_category']
        elif status['status_numeric']:
            val = self.get_status_category_from_numeric(self, status['status_numeric'])
        else:
            print('ERROR')
        match output_type:
            case 'xlsx':
                rslt = f"background-color:{self.config[val]['bg']}; color:{self.config[val]['fc']}"
            case 'html':
                rslt = self.config[val]['numeric']
            case _:
                print('ERROR')
        return rslt

    #workflow
    def highlight_cells(self, row, output_type):
        """This function implements question to model mapping for each row of
        a DF.

        :param output_type(str) - <'xlsx','html'>
        :return formats - list of dict depending on output_type

        Usage::
            >>> df_num = pd.DataFrame(
                    df.apply(func=hmformat.highlight_cells, 
                         axis=1, 
                         output_type='html'
                         ).to_list()
                )
        Each case refers to a column (question responses) that should be 
        mapped to a numeric value.
        """
        if output_type=='xlsx': formats = []
        elif output_type=='html': formats = {}
        for col,val in zip(row.index, row):
            status = {'status_category':None, 'status_numeric':None}
            if pd.isna(val):
                status['status_category'] = 'missing'
            else:
                match col:
                    case 'Name': status['status_category'] = self.col_empty(val)
                    case 'Q1': status['status_category'] = self.col_Q1(val)
                    case 'Q2': status['status_category'] = self.col_Q1(val)
                    case 'Q3': status['status_category'] = self.col_Q1(val)
            rslt = self.convert_to_output_type(output_type=output_type, status=status)
            if output_type=='xlsx': 
                formats.append(rslt)
            elif output_type=='html':
                new_key = col+'num'
                formats[new_key] = rslt
        return formats

    def col_empty(self, val,):
        """Defined for empty columns"""
        status_category = 'not_applicable'
        return status_category 

    #column mapping definitions
    """Column mapping requirements, may provide:
    * 'status_category' <any except missing> for t-shirt size status, or
    * 'status_numeric' <float between 0.0 and 1.0> for use with d3js template

    """
    def col_Q1(self, val):
        val = str(val).lower()
        if 'no' in val:
            status_category  = 'danger'
        else:
            status_category  = 'safe'
        return status_category 