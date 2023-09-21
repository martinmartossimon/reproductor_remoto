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
mensajes = []
clientes = []
clientes_eventos = []


def listar_archivos():
    try:
        archivos = [nombre for nombre in os.listdir(directorio) if nombre.endswith('.mp4')]
        # Ordena la lista de archivos por fecha de creación ascendente
        archivos_ordenados = sorted(archivos, key=lambda x: os.path.getctime(os.path.join(directorio, x)))
        return archivos_ordenados
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
        # Listar Videos
        elif self.path == '/listar_archivos':
            archivos = listar_archivos()
            if isinstance(archivos, list):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = json.dumps(archivos)
                self.wfile.write(response_data.encode())
        # Anadir Cliente
        elif self.path == '/addCliente':
            # Obtiene la dirección IP del remitente
            client_ip = self.client_address[0]
            print("IP del remitente recibida en /addCliente:", client_ip)
            if client_ip not in clientes:
                    clientes.append(client_ip)
                    print("Nueva IP agregada a la lista:", client_ip, " Lista -> ", str(clientes))
            
            # Prepara la respuesta JSON
            response_data = {"estado": "Alive"}
            response_json = json.dumps(response_data)
            # Envia la respuesta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_json.encode()) 
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode())

    def do_POST(self):
        if self.path == '/urlDownloader':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print("Tipo de post_data: " + str(type(post_data)))
            print("Tipo de dato de json.loads(post_data.decode()): " + str(type(json.loads(post_data.decode()))))
            try:
                #Esta linea se puede borrar, asi lo lee originalmente
                diccionario = json.loads(post_data.decode())
                #diccionario = json.loads(post_data)
        
                # Actualizar los datos con los recibidos en la solicitud POST
                #data.update(post_data)
                print("diccionario: " + str(diccionario) + " tipo de dato: " + str(type(diccionario)))
                url = diccionario["url"]
                print("Datos recibidos en la post: " + post_data.decode())
                print("Datos recibidos en la llamada: " + url)
                print("Ahora llamaría al descargador, si fuese posible en un hilo aparte")
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                print("Ejecutando el proceso de descarga")
                descargarVideoYoutube(url)

                #self.wfile.write(post_data.encode())
                self.wfile.write(post_data)
                #self.wfile.write("URL Recivida!! " + str(post_data))
                #self.wfile.write("Servidor")

            except json.JSONDecodeError:
                self.send_response(400)  # Devuelve un código de respuesta 400 si los datos no son JSON válidos
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Datos JSON no válidos".encode())
        # Funcion para reproducir el video en los clientes
        elif self.path == '/reproducirVideo':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode('utf-8'))
            accion = data.get('accion')
            video = data.get('video')

            if accion == 'reproducir':
                # Llama a la función para reproducir el video en los clientes registrados
                #reproducir_video(video)
                #Aqui vendria la accion de añadirlo a la cola de eventos
                print("Llamo a reproducir video con video: " + video)
                # Obtener la fecha y hora actual
                fecha_actual = datetime.datetime.now()
                # Formatear la fecha y hora como una cadena
                fecha_actual_str = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
                # Le añado el campo fecha al json
                data["fecha"] = fecha_actual_str

                # Agrego a la lista el mensaje
                mensajes.append(data)

                print("Contenido de la lista mensajes: " + str(mensajes))
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

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode())


# Clase para manejar las conexiones de eventos
class EventosHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/eventos':
            # Obtén la dirección IP de la interfaz en la que se está escuchando
            server_ip = socket.gethostbyname(socket.gethostname())

            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', f'http://{server_ip}:8000')  # Reemplaza 8000 por el puerto adecuado
            self.end_headers()
            
            # Agregar el cliente a la lista de clientes
            clientes_eventos.append(self)

            # Mantener la conexión abierta
            try:
                while True:
                    # Envía eventos a todos los clientes de eventos
                    if mensajes:
                        evento = mensajes.pop(0)
                        mensaje = f"data: {json.dumps(evento)}\n\n"
                        
                        # Envía el mensaje a todos los clientes de eventos
                        for cliente in clientes_eventos:
                            try:
                                cliente.wfile.write(mensaje.encode('utf-8'))
                            except Exception as e:
                                print("Error al enviar mensaje al cliente:", str(e))
                                # Elimina al cliente si hay un error
                                clientes_eventos.remove(cliente)
                    
                    # Simula un intervalo de tiempo (ajusta según tus necesidades)
                    time.sleep(1)
            except Exception as e:
                print("Cliente desconectado:", str(e))
                # Elimina al cliente de la lista cuando se desconecta
                clientes_eventos.remove(self)


#def iniciar_servidor():
#    PORT = 8000
#    with http.server.ThreadingHTTPServer(("", PORT), RequestHandler) as httpd:
#        print(f"Servidor en el puerto {PORT}")
#        httpd.serve_forever()

#if __name__ == "__main__":
    # Iniciar el servidor en un hilo separado
#    servidor_thread = threading.Thread(target=iniciar_servidor)
#    servidor_thread.start()

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
        
        # Iniciar el servidor web
        httpd.serve_forever()

if __name__ == "__main__":
    # Iniciar ambos servidores en hilos separados
    iniciar_servidores()