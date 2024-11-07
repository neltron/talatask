# Utiliza una imagen base oficial de Python
FROM python:3.11-slim


ENV PYTHONFAULTHANDLER=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100


# Instala dependencias del sistema
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    bash \
    build-essential \
    gettext \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias a la imagen
COPY requirements.txt /app/

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Exponer el puerto 8000 para el servidor de desarrollo de Django
EXPOSE 8000

ENTRYPOINT ["sh", "/app/entrypoint.sh"]

# RUN python manage.py migrate --no-input

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# 
# RUN python manage.py collectstatic --no-input
# RUN python manage.py runserver
#RUN gunicorn --worker-tmp-dir /dev/shm --workers=2 --threads=4 --worker-class=gthread --preload --bind 0.0.0.0:8000 talatask.wsgi:application
