FROM python:3.11-buster as builder
LABEL maintainer="flyon21 <zhogolevpv@gmail.com>"
ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . /app
# Set the correct starting directory and ensure the Python script is executable
RUN chmod +x /app/run.py

# Define the command to run the app
ENTRYPOINT ["python3", "/app/run.py"]
