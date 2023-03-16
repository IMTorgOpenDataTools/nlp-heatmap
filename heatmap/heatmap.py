#!/usr/bin/env python3
"""
Module for Bank Status Heatmap Project.
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

    def __init__(self):
        #, config=None
        #if config:
        #    self.config = config
        pass

    output_types = ['xlsx', 'html']

    config = {
        'missing' : {'numeric':None, 'bg':'gray', 'fc':'black'},
        'not_applicable' : {'numeric':None, 'bg':'white', 'fc':'black'},
        'safe' : {'numeric':0, 'bg':'#58f931', 'fc':'black'},
        'neutral' : {'numeric':0.5, 'bg':'#FFEB51', 'fc':'black'},
        'danger' : {'numeric':1.0, 'bg':'##ff2e1b', 'fc':'white'}
    }

    def convert_to_output_type(self, type, val):
        """..."""
        if type == 'xlsx':
            rslt = f"background-color:{self.config[val]['bg']}; color:{self.config[val]['fc']}"
        elif type == 'html':
            rslt = self.config[val]['numeric']
        return rslt


    def highlight_cells(self, row):
        """This is actually used with `.apply()`
        
        Each case refers to a column (question responses) that should be 
        mapped to a numeric value.
        """
        formats = []
        for key,val in zip(row.index, row):
            match key:
                case 'Name': tmp = self.col_empty(val)
                case 'Q1': tmp = self.col_Q1(val)
                case 'Q2': tmp = self.col_Q1(val)
                case 'Q3': tmp = self.col_Q1(val)
            rslt = self.convert_to_output_type(type='xlsx', val=tmp)
            formats.append(rslt)
        return formats

    def col_empty(self, val):
        """For empty columns"""
        if pd.isna(val):
            return f"background-color:{self.config['missing']['bg']}; color:{self.config['missing']['fc']}"
        val = str(val).lower()
        return f"background-color: {self.config['not_applicable']['bg']}; color: {self.config['not_applicable']['fc']}"

    def col_Q1(self, val):
        """TODO"""
        if pd.isna(val):
            rslt = 'missing'
        else:
            val = str(val).lower()
            if 'no' in val:
                rslt = 'danger'
            else:
                rslt = 'not_applicable'
        return rslt