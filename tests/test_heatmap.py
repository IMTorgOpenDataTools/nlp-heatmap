#!/usr/bin/env python3
"""
Test primary functionality.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from ..heatmap.main import main


class Args:
    input_file = '../tests/data/survey.csv'
    output_dir = '../tests/output/'
    output_type = 'html'


def test_main():
    args = Args()
    main(args)
    assert True == True