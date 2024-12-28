FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_SECRET_KEY=${FLASK_SECRET_KEY}

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]