#!/usr/bin/python3

import http.server
import socketserver
import json
import os


directorio = "./contenido"

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
        # Servicio del contenidos
        elif self.path.startswith('/contenido/'):
            # Sirve archivos estáticos desde la carpeta "contenido"
            try:
                with open('.' + self.path, 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'video/mp4')  # Ajusta el tipo de contenido según tus archivos
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
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode())

    #def do_POST(self):
    #    if self.path == '/servidor':
    #        content_length = int(self.headers['Content-Length'])
    #        post_data = self.rfile.read(content_length)
    #        post_data = json.loads(post_data.decode())
    #        
    #        # Actualizar los datos con los recibidos en la solicitud POST
    #        data.update(post_data)
    #        
    #        self.send_response(200)
    #        self.send_header('Content-type', 'text/plain')
    #        self.end_headers()
    #        #self.wfile.write("Datos actualizados".encode())
    #        self.wfile.write("Servidor")
    #    else:
    #        self.send_response(404)
    #        self.send_header('Content-type', 'text/plain')
    #        self.end_headers()
    #        self.wfile.write("Endpoint no encontrado".encode())

# Configurar el servidor para escuchar en el puerto 8000
with socketserver.TCPServer(("", 8000), RequestHandler) as httpd:
    print("Servidor en el puerto 8000")
    httpd.serve_forever()
