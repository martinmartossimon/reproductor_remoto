#!/usr/bin/python3
import http.server
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
import socketserver
import socket
import json
import os
import threading
import subprocess
import urllib.parse
import time
import datetime


directorio = "./contenido"
mensajes = [] # [{'accion': 'reproducir', 'video': 'FalsaPROPAGANDA.mp4', 'fecha': '2023-09-25 01:05:30'}]
clientes_eventos = [] #Lista de objetos EventosHandler
clientes = [] #Lista strings de IP de clientes


def listar_archivos():
    try:
        archivos = [nombre for nombre in os.listdir(directorio) if nombre.endswith('.mp4')]
        # Ordena la lista de archivos por fecha de creación ascendente
        archivos_ordenados = sorted(archivos, key=lambda x: os.path.getctime(os.path.join(directorio, x)))
        return archivos_ordenados
    except Exception as e:
        return str(e)

def obtener_duracion_video(ruta_archivo):
    try:
        # Utiliza el comando ffprobe para obtener la duración del video en segundos
        resultado = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", ruta_archivo],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        if resultado.returncode == 0:
            duracion_segundos = float(resultado.stdout.strip())

            # Convierte la duración en segundos a horas, minutos y segundos
            duracion_hora = int(duracion_segundos // 3600)
            duracion_minuto = int((duracion_segundos % 3600) // 60)
            duracion_segundo = int(duracion_segundos % 60)

            return {
                "segundos": duracion_segundos,
                "duracion": f"{duracion_hora:02d}:{duracion_minuto:02d}:{duracion_segundo:02d}"
            }
        else:
            return None
    except Exception as e:
        return None

# Genera un JSON similar a: [{"archivo": "DEMONSCRESTSUPE.mp4", "tamano": "91.84 MB", "Fecha_Creacion": "25/09/2023 00:54"}, {"archivo": "Informativomati.mp4", "tamano": "7.17 MB", "Fecha_Creacion": "25/09/2023 09:43"}]
def listar_archivos_detalle(): 
    try:
        archivos = [nombre for nombre in os.listdir(directorio) if nombre.endswith('.mp4')]
        archivos_con_info = []

        for nombre_archivo in archivos:
            archivo_info = {}
            ruta_completa = os.path.join(directorio, nombre_archivo)

            # Obtener el tamaño del archivo en MB o GB
            tamano = os.path.getsize(ruta_completa)
            if tamano >= 1024 ** 3:  # Si es mayor o igual a 1 GB
                tamano_str = f"{tamano / (1024 ** 3):.2f} GB"
            else:
                tamano_str = f"{tamano / (1024 ** 2):.2f} MB"

            # Obtener la fecha de creación en el formato deseado
            fecha_creacion_timestamp = os.path.getctime(ruta_completa)
            fecha_creacion = datetime.datetime.fromtimestamp(fecha_creacion_timestamp).strftime('%d/%m/%Y %H:%M')

            # Obtener la duración del video
            duracion = obtener_duracion_video(ruta_completa)

            archivo_info['archivo'] = nombre_archivo
            archivo_info['tamano'] = tamano_str
            archivo_info['Fecha_Creacion'] = fecha_creacion
            # Agregar la duración en segundos y en formato h:m:s
            archivo_info['duracion_segundos'] = duracion['segundos']
            archivo_info['duracion_hms'] = duracion['duracion']

            archivos_con_info.append(archivo_info)

        return json.dumps(archivos_con_info, ensure_ascii=False)
    except Exception as e:
        return str(e)

def descargarVideoYoutube(url):
    urlLimpia = urllib.parse.unquote(url)
    script_path = os.path.abspath('/home/tincho/Scripts/reproductor_remoto/descargadorYtb-dlp')
    try:
        proceso = subprocess.Popen(f"sh {script_path} {urlLimpia} &", shell=True)
        pid = proceso.pid
        print("PID del proceso:", pid)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el script: {e}")
    except FileNotFoundError:
        print("No se encontró el archivo del script.")

# Manda mensaje a viewers: {"fecha": "2023-09-25 02:37:23", "accion": "Ping"}
def queryClientesAlive():
    data = {}
    # Obtener la fecha y hora actual
    fecha_actual = datetime.datetime.now()
    # Formatear la fecha y hora como una cadena
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
    # Le añado el campo fecha al json
    data["fecha"] = fecha_actual_str
    data["accion"] = "Ping"
    mensajes.append(data)
    print("PING!!")
    for cliente in clientes:
        print("Cliente - ", cliente)
    for cliente_E in clientes_eventos:
        print("Cliente_E - ", cliente_E)


# Definir el manejador de solicitudes personalizado
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        template_path = '/plantillas/'
        #Servicio del html del cliente
        if self.path == '/cliente':
            try:
                # Abre el archivo HTML solicitado en modo lectura binaria
                with open('.' + template_path + self.path + ".html", 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #response_data = json.dumps(data)
                #response_data = content 
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                pathBuscado='Archivo no encontrado en: .' + template_path + "cliente.html"
                self.wfile.write(pathBuscado.encode())
        #Servicio del html del servidor
        elif self.path == '/servidor':
            try:
                # Abre el archivo HTML solicitado en modo lectura binaria
                with open('.' + template_path + self.path + ".html", 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #response_data = json.dumps(data)
                #response_data = content 
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                pathBuscado='Archivo no encontrado en: .' + template_path + "cliente.html"
                self.wfile.write(pathBuscado.encode())
        # Endpoint de url del visor
        elif self.path == '/viewer':
            try:
                # Abre el archivo HTML solicitado en modo lectura binaria
                with open('.' + template_path + self.path + ".html", 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                pathBuscado='Archivo no encontrado en: .' + template_path + "cliente.html"
                self.wfile.write(pathBuscado.encode())
        # Servicio del contenidos de manera progresiva.
        elif self.path.startswith('/contenido/'):
            # Sirve archivos de video desde la carpeta "contenido"
            try:
                with open('.' + self.path, 'rb') as file:
                    content = file.read()
                self.send_response(206)  # Código de respuesta parcial (206 Partial Content)
                self.send_header('Content-type', 'video/mp4')  # Ajusta el tipo de contenido según tus archivos
                self.send_header('Accept-Ranges', 'bytes')  # Indica que el servidor admite solicitudes parciales
                file_size = len(content)
                self.send_header('Content-Length', file_size)  # Indica el tamaño total del archivo
                self.send_header('Content-Range', f'bytes 0-{file_size-1}/{file_size}')  # Indica el rango de bytes enviado
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Archivo no encontrado".encode())
            except ConnectionResetError as e:
                # Captura la excepción ConnectionResetError
                print(f"Se produjo un error de conexión: {e}")
                # Imprime un mensaje personalizado
                print("La conexión se restableció abruptamente por el cliente por cambio de video.")
        # Listar Videos: Envia algo así: ["13COMANDOSRAROS.mp4", "ConcordeJustKis.mp4", "T10x4Debatokere.mp4"]
        elif self.path == '/listar_archivos':
            archivos = listar_archivos()
            if isinstance(archivos, list):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = json.dumps(archivos)
                #print("JSON de /listar_archivos: ", response_data)
                self.wfile.write(response_data.encode())
        # Genera un JSON con el siguiente detalle: [{"archivo": "DEMONSCRESTSUPE.mp4", "tamano": "91.84 MB", "Fecha_Creacion": "25/09/2023 00:54"}, {"archivo": "Informativomati.mp4", "tamano": "7.17 MB", "Fecha_Creacion": "25/09/2023 09:43"}]
        elif self.path == '/listar_archivos_detalle':
            resultado_json = listar_archivos_detalle()         
            print("Tipo de dato de resultado_json: ", type(resultado_json))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            print("Enviando JSON: ", resultado_json.encode())
            self.wfile.write(resultado_json.encode())
        # Anadir Cliente. Envia el siguiente json: {"estado": "Conectado"}
        elif self.path == '/addCliente':
            # Obtiene la dirección IP del remitente
            client_ip = self.client_address[0]
            if client_ip not in clientes:
                clientes.append(client_ip)
                print("Nueva IP agregada a la lista clientes desde  /addCliente:", client_ip, " Lista de strings de Clientes: -> ", str(clientes))
            # Prepara la respuesta JSON
            response_data = {"estado": "Conectado"}
            response_json = json.dumps(response_data)
            # Envia la respuesta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_json.encode()) 
        # Servicio que envía un JSON con el listado de clientes: [{"cliente": "192.168.18.101"}, {"cliente": "192.168.18.151"}]
        elif self.path == '/getClientes':
            # Retorna algo en este formato: [{"cliente": "192.168.18.101"}, {"cliente": "192.168.18.112"}]
            # Obtén la dirección IP de la interfaz en la que se está escuchando
            server_ip = socket.gethostbyname(socket.gethostname())
            # Defino cabeceras
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()            
            # Crea una lista de diccionarios con el formato deseado
            json_data = [{"cliente": ip} for ip in clientes]
            # Convierte la lista de diccionarios en una cadena JSON
            #json_string = json.dumps(json_data, indent=4)
            json_string = json.dumps(json_data)
            # Ahora puedes enviar 'json_string' al cliente
            print(json_string.encode('utf-8'))
            self.wfile.write(json_string.encode('utf-8'))
        # Endpoint no encontrado
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode())

    def do_POST(self):
        # Endpoint que descarga videos de youtube. Recive un JSON como el siguiente: {"url":"https://www.youtube.com/watch?v=2MjgGqOXA5s"}
        if self.path == '/urlDownloader':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                diccionario = json.loads(post_data.decode())        
                # Actualizar los datos con los recibidos en la solicitud POST
                url = diccionario["url"]
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                descargarVideoYoutube(url)

                self.wfile.write(post_data)

            except json.JSONDecodeError:
                self.send_response(400)  # Devuelve un código de respuesta 400 si los datos no son JSON válidos
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Datos JSON no válidos".encode())
        # Funcion para reproducir el video en los clientes. Recive un JSON: {"accion":"reproducir","video":"Estoseveentiend.mp4"}
        elif self.path == '/reproducirVideo':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode('utf-8'))
            accion = data.get('accion')
            video = data.get('video')

            if accion == 'reproducir':
                # Obtener la fecha y hora actual
                fecha_actual = datetime.datetime.now()
                # Formatear la fecha y hora como una cadena
                fecha_actual_str = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
                # Le añado el campo fecha al json
                data["fecha"] = fecha_actual_str
                # Agrego a la lista el mensaje: [{'accion': 'reproducir', 'video': 'FalsaPROPAGANDA.mp4', 'fecha': '2023-09-25 01:05:30'}]
                mensajes.append(data)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"mensaje": "Comando de reproducción enviado a los clientes"}).encode('utf-8'))
                return
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"mensaje": "Accion no reconocida"}).encode('utf-8'))
                return
        # Funcion para borrar un video del listado de videos. Recive: {'nombre_video': 'FalsaPROPAGANDA.mp4'} - Retorna: {mensaje: 'Video eliminado correctamente'}
        elif self.path == '/borrarVideo':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                # Decodifica el JSON recibido
                data = json.loads(post_data.decode())
                video_a_borrar = data.get('nombre_video')
                
                # Verifica que se proporcionó el nombre del video a borrar
                if video_a_borrar:
                    # Construye la ruta completa al video a borrar
                    video_path = os.path.join(directorio, video_a_borrar)
                    
                    # Verifica si el archivo existe y es un archivo regular (no un directorio)
                    if os.path.isfile(video_path):
                        # Elimina el video
                        os.remove(video_path)
                        print("!! - Archivo Borrado: ", video_path)
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"mensaje": "Video eliminado correctamente"}).encode('utf-8'))
                    else:
                        # Si el archivo no existe, devuelve un mensaje de error
                        self.send_response(404)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": "El video no existe"}).encode('utf-8'))
                else:
                    # Si no se proporcionó el nombre del video, devuelve un mensaje de error
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Debe proporcionar el nombre del video a borrar"}).encode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)  # Devuelve un código de respuesta 400 si los datos no son JSON válidos
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Datos JSON no válidos".encode())
        # Error de Endpoint no encontrado
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode())


# Clase para manejar las conexiones de eventos
class EventosHandler(BaseHTTPRequestHandler):
    # Inicializo la propiedad ip
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ip = self.client_address[0]
        # Agrega la IP del cliente a la lista global 'clientes'
        clientes.append(self.ip)
    
    # Destructor: Borra el cliente de clientes[]
    def __del__(self):
        # Elimina la IP del cliente de la lista global 'clientes' cuando se destruye el objeto
        if self.ip in clientes:
            clientes.remove(self.ip)

    def do_GET(self):
        # Servicio para el intercambio de mensajes con los clientes
        if self.path == '/eventos':
            print("Llamada a /eventos - Contenido de clientes eventos: ", clientes_eventos)
            # Obtén la dirección IP de la interfaz en la que se está escuchando
            server_ip = socket.gethostbyname(socket.gethostname())
            client_ip = self.client_address[0]

            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', f'http://{server_ip}:8000')  # Reemplaza 8000 por el puerto adecuado
            self.end_headers()
            
            # Agregar el cliente a la lista de clientes
            if self not in clientes_eventos:
                print("!!!!!!!! Agrego cliente nuevo porque no existia: ", str(client_ip))
                clientes_eventos.append(self)
            print("No agrego ya que el cliente existia previamente: ", str(client_ip))
            try: # Mantener la conexión abierta
                while True:
                    # Envía eventos a todos los clientes de eventos
                    if mensajes:
                        evento = mensajes.pop(0)
                        mensaje = f"data: {json.dumps(evento)}\n\n"
                        
                        # Envía el mensaje a todos los clientes de eventos
                        for cliente in clientes_eventos:
                            try:
                                print("Mensaje de reproduccion enviado a cliente: ", str(cliente.client_address[0]))
                                cliente.wfile.write(mensaje.encode('utf-8'))
                            except Exception as e:
                                print("Error al enviar mensaje al cliente:", str(e))
                                # Elimina al cliente si hay un error
                                clientes_eventos.remove(cliente)
                                print("********************Cliente desconectado - Borrando de clientes también: ", str(cliente.client_address[0]))
                                clientes.remove(cliente.client_address[0])
                    
                    # Simula un intervalo de tiempo (ajusta según tus necesidades)
                    time.sleep(1)
            except Exception as e:
                print("********************Cliente desconectado:", str(e))
                # Elimina al cliente de la lista cuando se desconecta
                clientes.remove(client_ip)
                clientes_eventos.remove(self)       

def ping_clientes():
    while True:
        queryClientesAlive()
        time.sleep(10)

def iniciar_servidores():
    PORT = 8000
    eventos_port = 8001  # Puerto para el servidor de eventos
    # Crear el servidor web en un hilo
    with ThreadingHTTPServer(("", PORT), RequestHandler) as httpd:
        print(f"Servidor en el puerto {PORT}")
        
        # Crear el servidor de eventos en otro hilo
        eventos_server = ThreadingHTTPServer(("", eventos_port), EventosHandler)
        eventos_thread = threading.Thread(target=eventos_server.serve_forever)
        eventos_thread.start()

        hilo_ping_clientes = threading.Thread(target=ping_clientes)
        hilo_ping_clientes.start()
        
        # Iniciar el servidor web
        httpd.serve_forever()

if __name__ == "__main__":
    # Iniciar ambos servidores en hilos separados
    iniciar_servidores()