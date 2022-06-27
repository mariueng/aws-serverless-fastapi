# aws-serverless-fastapi
Serverless API that provides useful data on demand.

## Install dependencies

With pip

`pip install -r requirements.txt`

or with pipenv

`pipenv shell`

## Running application locally

`uvicorn app.main:app --reload`

## Testing

To run all tests:

`pytest`

or with coverage.py:

`coverage run -m pytest`

To get coverage report, subsequentially run:

`coverage report -m`

## Notes on pipenv

Pipenv can be successfully configured to used pyenv shims by creating new environments as such:

`pipenv install --python $(pyenv which python) -r requirements.txt`

where the `$(pyenv which python)` command evaluates to the currently selected python version in pyenv.

## Build and deploy

Zip all packages to a file (replace X with your python version for the environment):

`zip -r9 <path to project>/function.zip <path to virtual environment>/lib/python3.X/site-packages`

Add the code inside app-directory:

`zip -g ./function.zip -r app`

and upload the code to the lambda function.