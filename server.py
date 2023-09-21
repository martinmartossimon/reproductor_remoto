#!/usr/bin/python3

import http.server
import socketserver
import json
import os
import threading
import subprocess
import urllib.parse
import time

directorio = "./contenido"
mensajes = []


def listar_archivos():
    print("Entro a listar_archivos()")
    try:
        #archivos = os.listdir(directorio)
        #archivos = [nombre for nombre in os.listdir(directorio) if not nombre.startswith('.')]
        archivos = [nombre for nombre in os.listdir(directorio) if nombre.endswith('.mp4')]
        print("Listado de archivos leidos: " + str(archivos))
        return archivos
    except Exception as e:
        return str(e)


def descargarVideoYoutube(url):
    print("Entrando al método descargarVideoYoutube con url: '" + url + "'")
    #urlLimpia = urllib.parse.quote(url)
    urlLimpia = urllib.parse.unquote(url)
    #script_path = os.path.abspath('./descargadorYtb-dlp')
    script_path = os.path.abspath('/home/tincho/Scripts/reproductor_remoto/descargadorYtb-dlp')
    #script_path = os.path.abspath('/home/tincho/Scripts/reproductor_remoto/testScript.sh')

    try:
        #Funciona
        #subprocess.run(["sh", script_path, urlLimpia, "&"], check=True)
        #print("El script se ejecutó exitosamente.")
        
        #NO FUNCIONA EN PROCESOS HIJOS:
        #proceso = subprocess.Popen(["sh", script_path, urlLimpia, "&"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, start_new_session=True)
        #proceso = subprocess.Popen(["sh", script_path, urlLimpia], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, start_new_session=False)
        #proceso = subprocess.run(["sh", script_path, urlLimpia], check=True)
        proceso = subprocess.Popen(f"sh {script_path} {urlLimpia} &", shell=True)
        pid = proceso.pid
        print("PID del proceso:", pid)
        # Imprimir la salida estándar y de error del proceso (opcional)
        #salida_estandar, error_estandar = proceso.communicate()
        #print("Salida estándar del script:", salida_estandar.decode())
        #print("Error estándar del script:", error_estandar.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el script: {e}")
    except FileNotFoundError:
        print("No se encontró el archivo del script.")



    #Espero a que termine el proceso
    #proceso.wait()
    #if proceso.returncode != 0:
    #    print("Error durante la ejecución del script.")
    #    print("Código de salida:", proceso.returncode)
    # Imprimir un mensaje cuando el proceso ha terminado
    #print("El proceso ha terminado")

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
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode())

# Configurar el servidor para escuchar en el puerto 8000
#with socketserver.TCPServer(("", 8000), RequestHandler) as httpd:
#    print("Servidor en el puerto 8000")
#    httpd.serve_forever()

def iniciar_servidor():
    PORT = 8000
    with http.server.ThreadingHTTPServer(("", PORT), RequestHandler) as httpd:
        print(f"Servidor en el puerto {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Iniciar el servidor en un hilo separado
    servidor_thread = threading.Thread(target=iniciar_servidor)
    servidor_thread.start()