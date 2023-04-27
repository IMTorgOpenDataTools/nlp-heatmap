# NLP Classification Heatmap

Create an interactive heatmap from tabular data for reporting.  Typical usage is with general surveys and questionnaires.  Questionnaire items may be in a variety of response formats, including unstructured text.




## Usage

Ensure the following:

* survey data is in the correct file format
* TODO: config file
* TODO: ques-model mapping

Run this: (remove optional --arg names)
```
python --input_file ./tests/data/survey.csv --output_dir ./tests/output/ --output_type html
```


![heatmap](/docs/heatmap.png 'Classification Heatmap')



## Tests

Open the d3 template (`heatmap/templates/index.html`) in the browser.  If the the data does not load, then you may have a CORS issue with the browser.  Verify this through the console.  Steps to fix the issue for FireFox, [here](https://stackoverflow.com/questions/51081754/cross-origin-request-blocked-when-loading-local-file).


## ToDo

* config file for settings and model mapping
```config.yml
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
* q* should contain:
  - input data type
  - model mapping
  - color mapping

* ~~create models.py for generic model classes~~
* ~~models_mapped.py for implemented models subclassed from models.py~~
* ~~provide models for different question response types~~
  - ~~numeric~~ q4
  - ~~binary~~ q5
  - ~~likert, ordered categories~~ q6
  - ~~unstructured text~~ q1,q2,q3
* frontend functions
  - sort
  - export table to excel