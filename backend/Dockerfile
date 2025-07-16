# Usa una versión moderna de Python
FROM python:3.12.10-slim

# Evita el buffering para ver los logs en tiempo real
ENV PYTHONUNBUFFERED=1

# Crea y define el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y lo instala
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto de tu código al contenedor
COPY . .

# Expón el puerto en el que correrá uvicorn
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
