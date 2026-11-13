FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# REQUISITO: Declarar a porta TCP única para detecção do portal
EXPOSE 8080

# REQUISITO: O processo principal deve escutar em 0.0.0.0 e rodar em primeiro plano
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "360", "app:app"]