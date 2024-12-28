FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
ENV FLASK_RUN_HOST=0.0.0.0
ENV DATABASE_PATH=/app/flashcards.db

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000

ENTRYPOINT [ "/entrypoint.sh" ]

