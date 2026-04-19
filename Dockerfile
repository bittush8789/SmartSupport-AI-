# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV PYTHONPATH=.

EXPOSE 8000

CMD ["uvicorn", "smartsupport_ai.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
