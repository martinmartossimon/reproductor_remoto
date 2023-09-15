#!/usr/bin/python3

import http.server
import socketserver
import json
import os


directorio = "./contenido"
mensajes = []


def listar_archivos():
    print("Entro a listar_archivos()")
    try:
        archivos = os.listdir(directorio)
        print("Listado de archivos leidos: " + str(archivos))
        return archivos
    except Exception as e:
        return str(e)


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
        ######
        #elif self.path == '/sse':
        #    self.send_response(200)
        #    self.send_header('Content-Type', 'text/event-stream')
        #    self.send_header('Cache-Control', 'no-cache')
        #    self.send_header('Connection', 'keep-alive')
        #    self.end_headers()
        #    
            # Enviar mensajes almacenados como eventos SSE
        #    for mensaje in mensajes:
        #        self.wfile.write(f"data: {mensaje}\n\n".encode())
        #        self.wfile.flush()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode())

    def do_POST(self):
        if self.path == '/urlDownloader':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode())
       
            # Actualizar los datos con los recibidos en la solicitud POST
            #data.update(post_data)
            print("Datos recibidos en la llamada: " + post_data)
            print("Ahora llamaría al descargador, si fuese posible en un hilo aparte")
            
            mensajes.append(f"Acción ha finalizado: {post_data}")

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(post_data.encode())
            #self.wfile.write("URL Recivida!! " + str(post_data))
            #self.wfile.write("Servidor")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode())

# Configurar el servidor para escuchar en el puerto 8000
with socketserver.TCPServer(("", 8000), RequestHandler) as httpd:
    print("Servidor en el puerto 8000")
    httpd.serve_forever()
