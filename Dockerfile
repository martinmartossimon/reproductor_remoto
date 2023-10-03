# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY server.py .
COPY plantillas/ plantillas/
COPY descargadorYtb-dlp .

# Instala las dependencias si es necesario
RUN pip install --upgrade pip && pip install yt-dlp 

#RUN apt-get update && apt-get install -y vim ffmpeg
RUN apt-get install -y ffmpeg
RUN apt-get clean


# Expón los puertos 8000 y 8001
EXPOSE 8000
EXPOSE 8001

# Comando para arrancar el servicio
CMD ["python", "server.py"]
