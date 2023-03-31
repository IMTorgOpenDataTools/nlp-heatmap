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

* config file for settings
* models config for question-model mapping
* enable different response types
  - numeric
  - binary
  - likert
  - ordered categories
  - unstructured text
* frontend functions
  - sort
  - export table to excel