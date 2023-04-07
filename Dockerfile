FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH ./src

RUN  apt-get update && apt-get install -y netcat && pip install --upgrade pip  \
     && apt-get install -y postgresql-client --no-install-recommends

WORKDIR /opt/app

COPY --from=requirements-stage /tmp/requirements.txt /opt/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /opt/app/requirements.txt

COPY . .

CMD ["gunicorn", "--worker-class=gevent", "--workers=4", "-b", "0.0.0.0:5000", "app:app"]
