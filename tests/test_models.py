#!/usr/bin/env python3
"""
Test Model classes.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import sys
from pathlib import Path
sys.path.append(Path('heatmap').absolute().as_posix())
from heatmap import models


def test_Config():
    filepath = './tests/data/config_settings.json'
    config = models.Config(filepath=filepath)
    test = config.load()
    msg = config.categories['missing']
    assert msg == {'numeric':None, 'bg':'gray', 'fc':'black'}

def test_Mapping():
    filepath = './tests/data/config_mapping.yml'
    mapping = models.ModelMapping(filepath=filepath)
    test = mapping.load()
    map = mapping.data
    assert map['Name'] == models.Index

def test_IndexModel():
    input_type = str
    model_mapping = 'TODO'
    val = 'GroupA'
    status_category = models.Index(input_type, model_mapping).run(val)
    assert status_category == 'not_applicable'

def testTextContainsNo():
    input_type = str
    model_mapping = 'TODO'
    val = 'There is NO way this will fail!'
    status_category = models.TextContainsNo(input_type, model_mapping).run(val)
    assert status_category == 'danger'