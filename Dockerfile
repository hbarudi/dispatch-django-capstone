FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USE_SQLITE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements_docker.txt /app/
RUN python -m pip install --upgrade pip && pip install -r requirements_docker.txt

COPY . /app/

RUN python -m sphinx -b html docs/source docs/build/html

RUN python manage.py migrate && \
    python manage.py loaddata db_backup.json

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
