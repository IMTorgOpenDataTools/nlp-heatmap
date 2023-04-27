#!/usr/bin/env python3
"""
Test primary functionality.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import sys
from pathlib import Path
sys.path.append(Path('heatmap').absolute().as_posix())
from heatmap import main
from heatmap import models, heatmap

import pandas as pd


config = models.Config(filepath='./tests/data/config_settings.json')
mapping = models.ModelMapping(filepath='./tests/data/config_mapping.yml')
test, test = config.load(), mapping.load()
hmformat = heatmap.HeatMapFormat(config, mapping)

data = {'Name':'record1', 
        'Q1':'On the way to Malaysia...no internet access to Twit',
        'Q2':'i want to go to music tonight but i lost my voice.',
        'Q3':'I`d have responded, if I were going',
        'Q4':1,
        'Q5':1,
        'Q6':'Strongly Disagree',
        }


def test_HeatMapFormat_get_status_category_from_numeric():
    numeric = .75
    status_category = hmformat.get_status_category_from_numeric(numeric)
    assert status_category == 'danger'

def test_HeatMapFormat_convert_to_output_type():
    errors = []
    status = {}
    status['status_category'] = 'danger'
    output_type = hmformat.output_types[0]
    output = hmformat.convert_to_output_type(output_type, status)
    if output != "background-color:##ff2e1b; color:white": errors.append('cond1')
    output_type = hmformat.output_types[1]
    status['status_numeric'] = 0.75
    output = hmformat.convert_to_output_type(output_type, status)
    if output != 1.0: errors.append('cond2')
    assert not errors

def test_HeatMapFormat_highlight_cells():
    output_type = hmformat.output_types[1]
    row = pd.Series(data)
    output = hmformat.highlight_cells(row, output_type)
    assert output == {'Namenum': None, 'Q1num': 1.0, 'Q2num': 0, 'Q3num': 0, 'Q4num': 0.5, 'Q5num': 1.0, 'Q6num': 0}



class Args:
    input_file = './tests/data/survey.csv'
    output_dir = './tests/output/'
    output_type = 'html'

def test_main():
    args = Args()
    main.main(args)
    assert True == True