FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

ENV FASTAPI_BASE_URL="http://127.0.0.1:8000"

CMD ["python", "app.py"]