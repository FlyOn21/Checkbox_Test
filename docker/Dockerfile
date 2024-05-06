FROM python:3.9.15
WORKDIR /app
LABEL maintainer="flyon21 <zhogolevpv@gmail.com>"
ENV PYTHONUNBUFFERED 1

COPY server server
COPY alembic.ini alembic.ini
COPY alembic alembic
COPY run.py run.py
COPY requirements.txt requirements.txt
COPY google-certificate.json google-certificate.json
RUN chmod 777 server/celery_tasks/entrypoint.sh
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir

CMD ["python3", "run.py"]