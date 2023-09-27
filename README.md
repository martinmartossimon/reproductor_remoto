# Reproductor Remoto
Se trata de un aplicativo web donde se controla de manera remota los videos que los clientes reproducen en un navegador web tan sólo accediendo a una url desde el cliente(s). También tiene la opción para descargar videos directamente de plataformas como: youtube... los cuales aparecen listados en una lista de reproducción. Todas las labores de reproducción se realizan desde una web que se encarga de enviar los videos a reproducir a todos los clientes.
Los videos son reproucidos (y almacenados) desde el propio host de la aplicación, por lo que la latencia en la reproducción es mínima.


# Por implementar:
- Control de reproducción. Play/Pause/Vol+/Vol-
- ~~Lista de Clientes conectados.~~
- Lista de Reproducción: Reproduciendo actualmente
- Archivar videos (a otra ubicación)
- Agregar miniaturas de los videos
- Agregar Latencia de los clientes: {timeepoch: 1223445} - Backend sleep 1 segundos y devuelve el mismo JSON - Recibe JSON con epoch anterior, aunque quizás se podría hacer más fácil midiendo los tiempos en el fetch sabien que el fetch lo va a demorar exactamente 1 segundo.
- Recordar el progreso de visionado de un video. Cuando se produzca el evento de cambiar video, que recuerde el segundo del video actual y lo mande al backend. Cosa que luego se puede retomar la reproducción del video por donde se dejó.
- Evitar lo videos duplicados en las descargas.
- Sincronizar video en los reproductores. (Ver si se puede usar el tema de la latencia para que la sincronización sea más fina)
- Mejorar el mover del script de descarga para que no renombre los *,part sólo los *.mp4 y así poder tener descargas simultáneas (Ver posibilidad de leer el porcentaje de descarga para enviar al servidor de alguna manera)
- Avanzar y Retroceder la reproducción en intervalos de 30 segundos (configurable). Sólo enviando al cliente un mensaje, sin considerar el segundo actual en el cliente (unidireccional, del backend al cliente)