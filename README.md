# NLP Classification Heatmap

Create an interactive heatmap from tabular data for reporting.  Typical usage is with general surveys and questionnaires.  Questionnaire items may be in a variety of response formats, including unstructured text.




## Usage

Ensure the following:

* survey data is in the correct file format
  - each row (record) and question (column)
  - for example, see: `./tests/data/survey.csv`
* modify config settings file: `heatmap/config_settings.json` (default in `./tests/data/`)
  - this determines the output formatting
  - there are a default of five categories: two for null values and three for typical stop-light (red, amber, green) formatting
  - each top-level key is a category that will be assigned the associated numeric value and cell formatting
  - if the data type of a column is numeric, then it will be chosen by the numeric value, not by the category
* modify config model mapping file: `heatmap/config_mapping.yml` (default in `./tests/data/`)
  - this maps questions / columns to models (`./heatmap/models.py`) that transform them to categories
  - several generic models exist, but custom class models may need to be defined to reach expected output display
* custom models, if applicable, defined in `./heatmap/models.py`

Run this: (remove optional --arg names)
```
python --input_file ./tests/data/survey.csv --output_dir ./tests/output/ --output_type html
```


![heatmap](/docs/heatmap.png 'Classification Heatmap')



## Tests

Testing is performed using pytest.

```shell
pytest --collect-only
pytest
```

To view created index file, open the d3 template (`heatmap/templates/index.html`) in the browser.  If the the data does not load, then you may have a CORS issue with the browser.  Verify this through the console.  Steps to fix the issue for FireFox, [here](https://stackoverflow.com/questions/51081754/cross-origin-request-blocked-when-loading-local-file).



## ToDo

* additional options for model mapping
```config_mapping.yml
setting:
  option1: feature
  index_columns: [1,2,3]
  columns_to_add: [summary1, summary2]

questions:
  q1: model1
  q2:
    - model2
    - model3
  q3: model4
  summary1: model5
  summary2: model6
```
* frontend functions
  - improve color configuration, [ref](https://observablehq.com/@lemonnish/color-scale-using-multiple-colors)
  - sort columns, [ref](https://github.com/michael-oppermann/d3-learning-material/tree/main/d3-case-studies/d3-case-study_measles-and-vaccines)
  - export table to excel, [ref](https://github.com/gitbrent/xlsx-js-style) [ref](https://github.com/sharonchoong/svg-exportJS)