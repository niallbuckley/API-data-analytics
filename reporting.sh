#! /bin/bash

# jupyter nbconvert --to notebook --execute --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=None analysis-API-endpoints.ipynb

python3 parse_jira.py
if [ $? -eq 0 ]; then
    echo "Parse jira executed successfully!"
else
    echo "Parse jira script failed with error code (429 error) $?"
    exit 1
fi
python3 create_master_csv.py
jupyter nbconvert --execute --to html --TemplateExporter.exclude_input=True automation_performance_analysis.ipynb
