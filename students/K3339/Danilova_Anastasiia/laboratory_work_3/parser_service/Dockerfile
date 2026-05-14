FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ../core ./core

# Запускаем FastAPI-обертку парсера (Подзадача 1)
CMD ["uvicorn", "parser_api:app", "--host", "0.0.0.0", "--port", "8001"]