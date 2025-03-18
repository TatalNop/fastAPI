FROM python:3.9

WORKDIR /app

# Copy all necessary parts
COPY ./users_service/requirements.txt .
COPY ./users_service/ .
COPY ../config ./config
COPY ../database ./database

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
