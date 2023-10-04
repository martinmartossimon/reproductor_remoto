# Reproductor Remoto
<p align="center">
<img src="https://github.com/martinmartossimon/reproductor_remoto/blob/main/imagenes/screenshot.png" width="40%" height="40%">  <img src="https://github.com/martinmartossimon/reproductor_remoto/blob/main/imagenes/dark-theme.png" width="40%" height="40%">
<p>


Se trata de un aplicativo web donde se controla de manera remota los videos que los clientes reproducen en un navegador web tan sólo accediendo a una url desde el cliente(s). También tiene la opción para descargar videos directamente de plataformas como: youtube... los cuales aparecen listados en una lista de reproducción. Todas las labores de reproducción se realizan desde una web que se encarga de enviar los videos a reproducir a todos los clientes.
Los videos son reproucidos (y almacenados) desde el propio host de la aplicación, por lo que la latencia en la reproducción es mínima.


# Uso con contenedor.
Construimos la imagen con:  
```bash
docker build -t reproductor_remoto .
```

Lanzamos la instancia con:  
```bash
docker run -d --rm --name reproductor_remoto -p 8000:8000 -p 8001:8001 -v $(pwd)/contenido:/app/contenido reproductor_remoto

#Ejemplo para lanzar una instancia:
git clone "https://github.com/martinmartossimon/reproductor_remoto.git"
cd reproductor_remoto/
docker build -t reproductor_remoto . && docker run --rm --name reproductor_remoto -p 8000:8000 -p 8001:8001 -v $(pwd)/contenido:/app/contenido reproductor_remoto
```

# Uso de la aplicación:
En el host que va a dirigir la reproducción en los clientes abrir la url:   
`http://IP:8000/servidor`   


En los hosts clientes abrir la url:  
`http://IP:8000/viewer`


# Por implementa:
- ~~Control de reproducción. Play/Pause/+30/+60/-30/+30-~~
- ~~Lista de Clientes conectados.~~
- ~~Lista de Reproducción: Reproduciendo actualmente~~
- Archivar videos (a otra ubicación)
- ~~Agregar miniaturas de los videos~~
- Agregar Latencia de los clientes: {timeepoch: 1223445} - Backend sleep 1 segundos y devuelve el mismo JSON - Recibe JSON con epoch anterior, aunque quizás se podría hacer más fácil midiendo los tiempos en el fetch sabien que el fetch lo va a demorar exactamente 1 segundo.
- Recordar el progreso de visionado de un video. Cuando se produzca el evento de cambiar video, que recuerde el segundo del video actual y lo mande al backend. Cosa que luego se puede retomar la reproducción del video por donde se dejó.
- ~~Evitar lo videos duplicados en las descargas.~~
- Sincronizar video en los reproductores. (Ver si se puede usar el tema de la latencia para que la sincronización sea más fina)
- ~~Mejorar el mover del script de descarga para que no renombre los *,part sólo los *.mp4 y así poder tener descargas simultáneas (Ver posibilidad de leer el porcentaje de descarga para enviar al servidor de alguna manera)~~
- ~~Avanzar y Retroceder la reproducción en intervalos de 30 segundos (configurable). Sólo enviando al cliente un mensaje, sin considerar el segundo actual en el cliente (unidireccional, del backend al cliente)~~
- Visor de twitch. Stream a un archivo y enviar ese archivo a reproducir.
