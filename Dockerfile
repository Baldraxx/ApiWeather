# Usamos una imagen base de Python 3.11
FROM python:3.11-slim

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos de la app al contenedor
COPY . .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto 5000 (puerto Flask por defecto)
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "run.py"]
