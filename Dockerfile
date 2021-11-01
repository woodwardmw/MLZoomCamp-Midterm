FROM python:3.9-slim

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict_vowel.py", "vowel-model.bin", "./"]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "predict_vowel:app" ]