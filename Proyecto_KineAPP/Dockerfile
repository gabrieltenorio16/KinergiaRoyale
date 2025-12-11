# 1. Imagen base
FROM python:3.12-slim

# 2. Variables para que Python no genere archivos intermedios y muestre logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiar requirements e instalar dependencias del sistema + Python
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
 && pip install --no-cache-dir -r requirements.txt \
 && apt-get purge -y gcc \
 && rm -rf /var/lib/apt/lists/*

# 5. Copiar todo el proyecto
COPY . /app/

# 6. Exponer el puerto del servidor de Django
EXPOSE 8000

# 7. Comando por defecto: servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
