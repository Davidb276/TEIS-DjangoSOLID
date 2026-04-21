# 1. Usamos una imagen base oficial de Python ligera (Slim es ideal para producción/dev)
FROM python:3.11-slim

# 2. Evitamos que Python escriba archivos .pyc y aseguramos que los logs se vean en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Establecemos el directorio de trabajo dentro del contenedor (el "quirófano")
WORKDIR /app

# 4. Instalamos dependencias del sistema operativo necesarias para Postgres y MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiamos los requerimientos e instalamos dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el resto del código fuente del proyecto
COPY . /app/

# 7. Exponemos el puerto 8000
EXPOSE 8000

# 8. Comando por defecto al iniciar el contenedor (será sobreescrito por docker-compose)
# Importante: Este comando es reemplazado por el 'command' en docker-compose.yml
CMD ["gunicorn", "Tienda.wsgi:application", "--bind", "0.0.0.0:8000"]