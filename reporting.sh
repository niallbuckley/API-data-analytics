#! /bin/bash

# jupyter nbconvert --to notebook --execute --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=None analysis-API-endpoints.ipynb


# jupyter nbconvert --execute --to html --TemplateExporter.exclude_input=True analysis-API-endpoints.ipynb