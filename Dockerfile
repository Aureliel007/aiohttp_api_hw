FROM python:3.11-slim

COPY ./app /app

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python3", "main.py"]