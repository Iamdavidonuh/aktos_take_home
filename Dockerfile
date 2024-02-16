FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.7.0
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false


WORKDIR /app

COPY poetry.lock /app
COPY pyproject.toml /app
RUN poetry install --no-root

COPY . /app

CMD [ "python",  "manage.py",  "runserver",  "0.0.0.0:8000" ]