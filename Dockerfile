FROM python:3.11-slim

# рабочая директория внутри контейнера
WORKDIR /app

# чтобы Docker мог кэшировать слой установки пакетов
COPY requirements.txt .

# устанавливаем зависимости проекта
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# копируем код ML-сервиса и ML-пайплайна
COPY app.py .
COPY ml_pipeline.py .

# по умолчанию версия модели v1.0.0
ENV MODEL_VERSION=v1.0.0

# открываем порт FastAPI-приложения
EXPOSE 8000

# запускаем FastAPI через uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
