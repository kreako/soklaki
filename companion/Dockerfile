FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .env .
COPY src/ .

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app", "--reload" ]