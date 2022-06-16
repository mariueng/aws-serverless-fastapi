# aws-serverless-fastapi
Serverless API that provides useful data on demand.

## Notes on pipenv

Pipenv can be successfully configured to used pyenv shims by creating new environments as such:

`pipenv install --python $(pyenv which python) -r requirements.txt`

where the `$(pyenv which python)` command evaluates to the currently selected python version in pyenv.