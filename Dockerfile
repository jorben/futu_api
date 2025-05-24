FROM python:3.9.21-slim

WORKDIR /app

COPY . .

RUN pip install -e .

EXPOSE 15000

CMD ["gunicorn", "--bind", "0.0.0.0:15000", "--workers", "4", "--timeout", "120", "run:app"]
