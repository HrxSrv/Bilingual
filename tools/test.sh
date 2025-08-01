#!/bash/sh


APP_ENV=staging PYTHONPATH=$(pwd) poetry run pytest -p no:warnings
