FROM python:3

WORKDIR /app

COPY requirements.txt .
COPY .env .

RUN pip install -r requirements.txt

COPY src/ .

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app", "--reload" ]