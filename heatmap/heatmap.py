#!/usr/bin/env python3
"""
Module for Status Heatmap Project.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import pandas as pd
import numpy as np


class HeatMapFormat:
    """Heatmap formatting based on conditions for each individual question.

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
        if 0 <= numeric <= 1.0:
            status_pairs = [(v['numeric'],k) for k,v in self.config.items() if v['numeric']!=None]
            pair = [p for p in status_pairs if p[0]>=numeric][0]
            status_category = pair[1]
        else:
            print('ERRROR')
        return status_category

    def convert_to_output_type(self, type, status):
        """Get the approprite output for the user-provided output_type."""
        if status['status_category']:
            val = status['status_category']
        elif status['status_numeric']:
            val = self.get_status_category_from_numeric(self, status['status_numeric'])
        else:
            print('ERROR')
        match type:
            case 'xlsx':
                rslt = f"background-color:{self.config[val]['bg']}; color:{self.config[val]['fc']}"
            case 'html':
                rslt = self.config[val]['numeric']
            case _:
                print('ERROR')
        return rslt

    #workflow
    def highlight_cells(self, row):
        """This is actually used with `.apply()`
        
        Each case refers to a column (question responses) that should be 
        mapped to a numeric value.
        """
        formats = []
        for key,val in zip(row.index, row):
            status = {'status_category':None, 'status_numeric':None}
            if pd.isna(val):
                status['status_category'] = 'missing'
            else:
                match key:
                    case 'Name': status['status_category'] = self.col_empty(val)
                    case 'Q1': status['status_category'] = self.col_Q1(val)
                    case 'Q2': status['status_category'] = self.col_Q1(val)
                    case 'Q3': status['status_category'] = self.col_Q1(val)
            rslt = self.convert_to_output_type(type='xlsx', val=status)
            formats.append(rslt)
        return formats

    def col_empty(self, val,):
        """Defined for empty columns"""
        status_category = 'not_applicable'
        return status_category 

    #column mapping definitions
    """
    Column mapping requirements, may provide:
    * 'status_category' <any except missing> for t-shirt size status, or
    * 'status_numeric' <float between 0.0 and 1.0> for use with d3js template

    """
    def col_Q1(self, val):
        val = str(val).lower()
        if 'no' in val:
            status_category  = 'danger'
        else:
            status_category  = 'not_applicable'
        return status_category 