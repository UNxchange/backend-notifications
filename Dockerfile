# Dockerfile robusto para backend-notifications
FROM python:3.11-slim

# Configurar variables de entorno para pip
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y otras librerías
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requisitos primero para aprovechar el cache de Docker
COPY requirements.txt .

# Actualizar pip y herramientas básicas
RUN pip install --upgrade pip setuptools wheel

# Instalar dependencias por grupos para evitar conflictos
RUN pip install --no-cache-dir fastapi==0.115.6 uvicorn[standard]==0.32.0
RUN pip install --no-cache-dir sqlalchemy==2.0.36 psycopg2-binary==2.9.9
RUN pip install --no-cache-dir pydantic==2.11.9 pydantic[email] pydantic-settings==2.1.0
RUN pip install --no-cache-dir python-multipart>=0.0.7
RUN pip install --no-cache-dir strawberry-graphql[fastapi]>=0.280.0
RUN pip install --no-cache-dir python-jose==3.3.0 passlib==1.7.4 python-dotenv==1.0.0
RUN pip install --no-cache-dir punq==0.6.2 bcrypt==4.1.2 prometheus_client
RUN pip install --no-cache-dir pytest==7.4.4 pytest-asyncio==0.21.1 httpx==0.25.2 requests==2.31.0
RUN pip install --no-cache-dir graphql-core>=3.2.3

# Copiar el código de la aplicación
COPY . .

# Crear un usuario no-root para ejecutar la aplicación
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]