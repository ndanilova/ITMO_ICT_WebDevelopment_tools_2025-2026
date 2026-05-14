FROM python:3.11-slim

WORKDIR /srv

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir -r /srv/requirements.txt

COPY core /srv/core
COPY parser_service /srv/parser_service

ENV PYTHONPATH=/srv

EXPOSE 8001

CMD ["uvicorn", "parser_service.parser_api:app", "--host", "0.0.0.0", "--port", "8001"]
