# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY server.py .
COPY plantillas/ plantillas/
COPY descargadorYtb-dlp .

# Instala las dependencias si es necesario
 RUN pip install yt-dlp 

# Expón los puertos 8000 y 8001
EXPOSE 8000
EXPOSE 8001

# Comando para arrancar el servicio
CMD ["python", "server.py"]
