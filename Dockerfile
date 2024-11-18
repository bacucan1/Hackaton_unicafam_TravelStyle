# Usa una imagen base de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos locales al contenedor
COPY . /app

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

