FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 15000

CMD ["gunicorn", "--bind", "0.0.0.0:15000", "--workers", "4", "--timeout", "120", "run:app"]