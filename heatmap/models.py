#!/usr/bin/env python3
"""
All model definitions to be applied to questions in survey through `./heatmap/config_mapping.yml`

Column-model mapping requirements must adhere to `config_settings.json`,to include:
* 'status_category' <any except missing> for t-shirt size status, or
* 'status_numeric' <float between 0.0 and 1.0> for use with d3js template

Class:
    Config
    ModelMapping
    Model
    ... generic and custom mapping models
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from pathlib import Path
import json
import yaml




# Config classes
class Config:
    """TODO"""
    def __init__(self, filepath):
        testpath = Path(filepath)
        if testpath.is_file() and testpath.suffix == '.json':
            self.filepath = testpath
            self.categories = None
        else:
            raise TypeError
        
    def load(self):
        with open(self.filepath, 'r') as fh:
            self.categories = json.load(fh)
        return True
        
    
class ModelMapping:
    """TODO"""
    def __init__(self, filepath):
        testpath = Path(filepath)
        if testpath.is_file() and testpath.suffix == '.yml':
            self.filepath = testpath
            self.data = None
        else:
            raise TypeError
        
    def load(self):
        with open(self.filepath, 'r') as fh:
            data = yaml.safe_load(fh)
        self.data = {k:eval(v) for (k,v) in data.items()}
        return True







# Model classes
class Model:
    """Abstract for all question models."""
    def __init__(self, input_type, model_mapping):
        self.input_type = input_type
        self.model_mapping = model_mapping

    def run(self):
        pass


class Index(Model):
    """Model to apply to index columns.  This
    does not return anything."""
    def run(self, val):
        status_category = 'not_applicable'
        #return status_category
        return 'status_category', status_category


class TextContainsNo(Model):
    """Generic model to apply to text columns."""
    def run(self, val):
        val = str(val).lower()
        if 'no' in val:
            status_category = 'danger'
        else:
            status_category = 'safe'
        #return status_category
        return 'status_category', status_category


class Numeric(Model):
    """Generic model to apply to numeric columns
    with values 1 - 10."""
    def run(self, val):
        status_numeric = val / 10
        return 'status_numeric', status_numeric

class Binary(Model):
    """Generic model to apply to binary columns
    with values 0,1."""
    def run(self, val):
        status_numeric = val
        return 'status_numeric', status_numeric

class Likert(Model):
    """Generic model to apply to binary columns
    with values 0,1."""
    def run(self, val):
        scale = {'Strongly Disagree': 0.0,
                 'Somewhat disagree': 0.25,
                 'Neutral': 0.5,
                 'Somewhat agree': 0.75,
                 'Strongly Agree': 1.0
                 }
        status_numeric = scale[val]
        return 'status_numeric', status_numeric