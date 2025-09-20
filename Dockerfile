# Usa una imagen oficial de Python como imagen base
FROM python:3.12-slim

# Establece variables de entorno para evitar que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Asegura que la salida de Python se muestre inmediatamente en la terminal del contenedor
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias al directorio de trabajo
COPY requirements.txt .
COPY requirements-dev.txt .

# Instala TODAS las dependencias (desarrollo y producción)
# Esto nos permite ejecutar herramientas de desarrollo dentro del contenedor
RUN pip install --no-cache-dir --upgrade -r requirements-dev.txt

# Copia el resto del código de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto 8000 para que la aplicación sea accesible desde fuera del contenedor
EXPOSE 8000

# El comando por defecto para ejecutar la aplicación, usando el patrón de módulo de Python
# para evitar problemas de PATH. Se usa 0.0.0.0 para que sea accesible desde fuera del contenedor.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
