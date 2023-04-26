#!/usr/bin/env python3
"""
Module for creating HTML report by combining template with data.

Classes:
    Report
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"



from jinja2 import Environment, FileSystemLoader
from pathlib import Path


class Report:
    """Class for creating and saving reports in HTML format from
    combining a template with data.
    
    Usage::
    >>> report = Report(template_path)
    >>> html = report.create_report(template=template, 
                                template_args=template_data
                                )
    >>> report.save_report(html, filepath=output_filepath)
    """

    def __init__(self, template_path):
        """Create class.

        :param output_path - "./tests/output/my_new_file.html"
        :return None
        """
        template_path = Path(template_path)
        if template_path.is_dir():
            self.template_path = template_path
        else:
            raise TypeError
        
    def create_report(self, template, template_args, output_path=False):
        env = Environment(loader=FileSystemLoader(self.template_path))
        template = env.get_template(template)
        output_from_parsed_template = template.render(template_args)

        if output_path:
            with open(output_path, "w") as fh:
                fh.write(output_from_parsed_template)
            return None
        else:
            return output_from_parsed_template

    def save_report(self, html, filepath):
        with open(filepath, "w") as f:
            f.write(html)