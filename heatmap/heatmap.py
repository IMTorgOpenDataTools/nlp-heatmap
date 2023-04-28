#!/usr/bin/env python3
"""
Module for Status Heatmap Project.

Class:
    HeatMapFormat
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from heatmap import models
from heatmap.models import Config

import pandas as pd
import numpy as np


class HeatMapFormat:
    """Formatting for heatmap output based on conditions for each
    individual question.

    Usage:
    >>> import heatmap_format as hf
    >>> config = models.Config(filepath=filepath)
    >>> mapping = models.ModelMapping(filepath=filepath)
    >>> config.load(); mapping.load()
    >>> hmformat = hf.HeatMapFormatting(config, mapping)
    >>> writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    >>> df.style.apply(hmformat.highlight_cells,
                        axis=1
                        ).to_excel(writer,
                                    sheet_name='Heatmap',
                                    engine='openpyxl'
                                    )
    """

    def __init__(self, config, mapping):
        """Create an object of type HeatMapFormat.  Depends on 
        configuration data.
        
        :param config(dict) - contains mapping of question values to 
        category's numeric value with colors
        :return None
        """
        if type(config).__name__=='Config' and type(mapping).__name__=='ModelMapping':
            self.config = config
            self.mapping = mapping
        else:
            raise TypeError

    #config attrs
    output_types = ['xlsx', 'html']


    #support methods
    def get_status_category_from_numeric(self, numeric):
        """Covert the numeric value to the config's status category.

        :param numeric(float) - numeric value matched to config settings's numeric
        :return status_category(str) - key value in config
        """
        if 0 <= numeric <= 1.0:
            status_pairs = [(v['numeric'],k) for k,v in self.config.categories.items() if v['numeric']!=None]
            pair = [p for p in status_pairs if p[0]>=numeric][0]
            status_category = pair[1]
        else:
            raise TypeError
        return status_category

    def convert_to_output_type(self, output_type, status):
        """Get the approprite output for the user-provided output_type."""
        if status['status_category']:
            val = status['status_category']
        elif status['status_numeric']>=0:
            val = self.get_status_category_from_numeric(status['status_numeric'])
        else:
            raise TypeError
        match output_type:
            case 'xlsx':
                rslt = f"background-color:{self.config.categories[val]['bg']}; color:{self.config.categories[val]['fc']}"
            case 'html':
                rslt = self.config.categories[val]['numeric']
            case _:
                raise TypeError
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
                mdl_class = self.mapping.data[col]
                mdl = mdl_class(input_type=type(val),model_mapping='')
                k,v = mdl.run(val)
                status[k] = v
            rslt = self.convert_to_output_type(output_type=output_type, status=status)
            if output_type=='xlsx': 
                formats.append(rslt)
            elif output_type=='html':
                new_key = col+'num'
                formats[new_key] = rslt
        return formats