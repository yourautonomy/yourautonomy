# Imagen base con Python ligero
FROM python:3.12-slim

# Para que los print() salgan de inmediato en los logs de Cloud Run
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Primero solo las librerías (Docker reutiliza este paso si no cambian)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después todo tu código: main.py y la carpeta static
COPY . .

# Encender FastAPI en el puerto que Cloud Run indique (8080 por defecto)
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}