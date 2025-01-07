FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY ./app.py /app/app.py
COPY ./src /app/src/
COPY ./static /app/static
COPY ./templates /app/templates
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./schema.sql /app/schema.sql

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=0.0.0.0
ENV DATABASE_PATH=/app/db/flashcards.db

RUN chmod +x /app/entrypoint.sh

EXPOSE 5000

ENTRYPOINT [ "/app/entrypoint.sh" ]