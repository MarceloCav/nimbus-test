FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 5784

COPY entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
