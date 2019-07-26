pyenv install 3.7.2
pyenv local 3.7.2
pip install pipenv
pipenv install --dev
pipenv run python -m ipykernel install --user --name saltedge_python
