pyenv install 3.7.2
pyenv local 3.7.2
pipenv run python -m ipykernel install --user --name saltedge_python
pipenv sync --dev