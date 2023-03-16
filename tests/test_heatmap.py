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


class Args:
    input_file = './tests/data/survey.csv'
    output_dir = './tests/output/'
    output_type = 'html'


def test_main():
    args = Args()
    main.main(args)
    assert True == True