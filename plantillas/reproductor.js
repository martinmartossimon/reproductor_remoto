console.log("Arrancando el Reproductor importado en .js");
console.log("Inicializando variables...");
// Variables Globales
let videoReproduciendo = ""; // identificador con el nombredelfichero.mp4
let elementos = []; // Array donde voy a guardar el resultado al consultar el listado de Archivos de /listar_archivos_detalle
let darkModeEnabled = false;


// Lista de detalles de archivos
let listaArchivos = [];
let idSeleccionado = 0;

// Elementos sobre los que vamos a tener eventos escuchando
const button = document.getElementById('toggleButton');
const buttonSiguiente = document.getElementById('siguiente');
const buttonAnterior = document.getElementById('anterior');
const buttonAtrasar30s = document.getElementById('atrasar30s');
const buttonAdelantar30s = document.getElementById('adelantar30s');
const buttonAtrasar60s = document.getElementById('atrasar60s');
const buttonAdelantar60s = document.getElementById('adelantar60s');

/******************
* MOSTRAR POPUP
*******************/
function mostrarPopup(mensaje) {
    var popup = document.getElementById("popup");
    popup.innerText = mensaje;
    popup.style.display = "block";

    // Ocultar el mensaje emergente después de 3 segundos
    setTimeout(function() {
        popup.style.display = "none";
    }, 1500); // 3000 milisegundos = 3 segundos
}

/******************
* agregarEvento() - Agrega entrada a la lista de eventos
******************/
function agregarEvento(texto) {
    const eventosDiv = document.getElementById("eventos");
    const eventoNuevo = document.createElement("div");
    eventoNuevo.textContent = texto;

    // Agregar una barra horizontal antes del eventoNuevo (si no es el primer evento)
    if (eventosDiv.firstChild !== null) {
        const hrElement = document.createElement("hr");
        eventosDiv.insertBefore(hrElement, eventosDiv.firstChild);
    }

    eventosDiv.insertBefore(eventoNuevo, eventosDiv.firstChild);

    // Limitar la cantidad de eventos mostrados (por ejemplo, a 100)
    const eventos = eventosDiv.getElementsByTagName("div");
    if (eventos.length > 100) {
        eventosDiv.removeChild(eventos[100]);
    }

    // Agregar la clase "highlight" al último div
    eventoNuevo.classList.add("highlight");

    // Usar setTimeout para quitar la clase después de 1 segundo
    setTimeout(function() {
        eventoNuevo.classList.remove("highlight");
    }, 4000); // 1000 milisegundos = 1 segundo
}

/******************
* ENVIAR DATOS PARA DESCARGAR VIDEO DE URL
******************/
function enviarDatos() {
    var host = window.location.host;
    var endpoint = '/urlDownloader';
    var url = 'http://' + host + endpoint;

    // Obtener el valor del input
    contenido = document.getElementById('url').value;

    // Crear un objeto JSON con el contenido
    const datos = { "url": contenido }
    console.log("Json enviado: " + JSON.stringify(datos));

    // Realizar la solicitud HTTP POST
    //fetch('http://host:8000/urlDownloader', {
    fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
    // Procesar la respuesta del endpoint
        console.log('Respuesta del endpoint:', data);
        document.getElementById('url').value="";
        contenido.placeholder="Siguiente URL...";
        // Aquí debería venir un mensaje emergente
        mostrarPopup("URL Añadida"); 
    })
    .catch(error => {
        console.error('Error al enviar los datos:', error);
    });
}

/******************************** 
* registrarCliente()
* !! Deshabilitado !! desde esta vista ya que no es cliente
********************************/
function registrarCliente(){
    console.log("Cliente Alive send")
    fetch('/addCliente', {
        method: 'GET', // Puedes ajustar el método según tu API
    })
    .then(response => response.json())
    .then(data => {
        // Actualiza el contenido en el elemento con ID "resultado"
        document.getElementById('estadoCliente').textContent = JSON.stringify(data);
    })
    .catch(error => {
        console.error('Error al consultar el endpoint:', error);
    });
}


/***************************************
* reproducirVideo()
* Envía un JSON con este formato al backend: JSON - {"accion":"reproducir","video":"T10x7Feijooenel.mp4"}
************************************/
function reproducirVideo(video) {
    const tablaBody = document.getElementById('tabla-body');
    tablaBody.innerHTML = ''; //Limpio el contenido de la tabla de reproduccion

    // Preparo la request al servidor
    const datos = {
        accion: "reproducir",
        video: video // Utiliza el nombre del archivo en lugar de idVideo
    };
    console.log("Datos: " + JSON.stringify(datos));
    // URL del endpoint al que deseas enviar los datos
    const endpointURL = '/reproducirVideo';
    // Opciones de la solicitud
    const opciones = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    };
    // Realiza la solicitud al servidor
    fetch(endpointURL, opciones)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error en la solicitud');
            }
        })
        .then(data => {
            console.log('Respuesta del servidor:', data);
            videoReproduciendo = video;
            console.log("videoReproduciendo="+videoReproduciendo)
            // Actualizo la lista
            getListaArchivos()
                .then(elementosPorArchivo => {
                    // Aquí puedes acceder a elementosPorArchivo
                    console.log("Contenido de elementosPorArchivo en funcion getListaArchivos:", elementosPorArchivo);
                    // Genero tabla a partir del listado de archivos
                    dibujarTablaReproduccion();
                    // Marco el video en reproduccion
                    marcarFilaReproduccion();
                })
                .catch(error => {
                    console.error('Error al obtener la lista de detalles:', error);
                });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    
    
}

/******************
* Función que dibuja la tabla con la lista de elementos de video reproducibles, con sus correspondientes botones
* Requiere que elementos[] tenga data para pintar
******************/
function dibujarTablaReproduccion() {
    if (elementos.length > 0) {
        console.log("Contenido de elementos en dibujarTablaReproduccion:", elementos);

        const tablaReproduccion = document.getElementById('tablaListaReproduccion');
        const tbody = tablaReproduccion.querySelector('tbody');
        tbody.innerHTML = '';

        elementos.forEach((elemento, index) => {
            const fila = document.createElement('tr');
            const id = index + 1;
            fila.dataset.id = id;

            const botones = document.createElement('td');
            botones.innerHTML = `<button id="reproducir-${id}" onclick="reproducirVideo('${elemento.archivo}')">&#x25B6;</button>
                                <button id="borrar-${id}" onclick="borrarVideo('${elemento.archivo}')">&#x1F5D1;</button>
            `;

            fila.innerHTML = `
                <td>${id}</td>                       
                <td>${elemento.archivo}</td>
                ${botones.outerHTML}
                <td>${elemento.archivo}</td>
                <td>${elemento.tamano}</td>
                <td>${elemento.Fecha_Creacion}</td>
                <td>${elemento.duracion_hms}</td>
            `;
            tbody.appendChild(fila);
        });
    }
    const fechaHora = new Date(); // Obtiene la fecha y hora actual
    const formatoFechaHora = fechaHora.toLocaleString(); // Convierte la fecha y hora a una cadena legible
    etiquetaUpdate = document.getElementById("ultimaActualizacion");
    etiquetaUpdate.innerHTML = "<p>Ultima actualizacion: " + formatoFechaHora + "</p>";
}

/***************************************
* marcarFilaReproduccion()
* Marco en funcion de reproduciendo. Busco en el array el índice del nombre del archivo y marco la fila: indice + 1 como seleccionada
************************************/
function marcarFilaReproduccion(){
    // Busco la fila
    const indiceDelReproduciendo = elementos.findIndex(elemento => elemento.archivo === videoReproduciendo);
    const indiceEntero = parseInt(indiceDelReproduciendo); // Convierte a entero

    indiceDeFila = indiceEntero + 1;
    if (!isNaN(indiceEntero) && indiceEntero !== -1) {
        console.log(`El video "${videoReproduciendo}" se encuentra en el índice ${indiceDelReproduciendo} del array elementos.`);
        console.log("Indice buscado en marcarFilaReproduccion: " + indiceDelReproduciendo + " Correspondiente al elemento de elementos[]: " + elementos[indiceDelReproduciendo] + " que en la tabla sería: " + indiceDeFila);

        // Aqui ya tengo indiceDeFila que es la fila que tengo que marcar.
        // Me posiciono en la fila de la tabla.
        filaSeleccionadaReproduciendo = document.querySelector(`tr[data-id="${indiceDeFila}"]`);
        // La añado a la clase seleccionada para que le aplique los estilos
        filaSeleccionadaReproduciendo.classList.add('seleccionada');

        //Compruebo la parte del tema oscuro para que también le añada la clase dark-theme
        if (darkModeEnabled) {
            filaSeleccionadaReproduciendo.classList.add('dark-theme');
        }

        // Deshabilito solo boton borrar
        const botonBorrar = filaSeleccionadaReproduciendo.querySelector('#borrar-' + indiceDeFila);
        botonBorrar.disabled = true;

        //Deshabilito los 2 o + botones:
        // Obtener los botones dentro de la fila
        //const botones = filaSeleccionadaReproduciendo.querySelectorAll('button');
        //// Deshabilitar los 2 botones
        //botones.forEach(boton => {
        //    boton.disabled = true;
        //});
    } else {
        console.log(`El video "${videoReproduciendo}" no se encontró en el array elementos.`);
    }
}

/******************************** 
* borrarVideo()
********************************/
function borrarVideo(idVideo) {
    console.log(`Borrar video con ID: ${idVideo}`);
    // Aquí puedes agregar el código para borrar el video según el ID proporcionado
    const nombreVideoABorrar = idVideo; // Cambia esto al nombre del video que deseas borrar

    const url = "/borrarVideo";

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre_video: nombreVideoABorrar }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        actualizarListaVideos();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

/******************************** 
* cargarClientes()
* Función para cargar la lista de clientes desde el backend
********************************/
function cargarClientes() {
    console.log("ejecuto cargarClientes()");
    // Obtén la dirección IP del host
    const hostIP = window.location.hostname;
    // Construye la URL completa del endpoint '/getClientes' con la dirección IP y el puerto 8001
    const url = `http://${hostIP}:8000/getClientes`;
    console.log("Obteniendo listado de clientes de: " + url);

    // Realiza una solicitud Fetch para obtener la lista de clientes
    fetch(url)
        .then(response => {
            console.log("Entro al response: ");
            if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error en la solicitud');
                }
        })
        .then(data => {
            console.log("Entro al data");
            // Obtén la tabla por su id
            const tablaClientes = document.getElementById("tablaClientes");
            console.log("Data recibida de getClientes: " + data.text);
            // Verifica si la tabla existe
            if (tablaClientes) {
                // Elimina todas las filas existentes en la tabla
                while (tablaClientes.rows.length > 1) {
                    tablaClientes.deleteRow(1);
                    console.log("Elimino fila previa a la carga de las nuevas.");
                }

                // Agrega una fila por cada cliente con su dirección IP
                //for (const cliente of JSON.parse(data)) {
                    for (const cliente of data) {    
                    const row = tablaClientes.insertRow();
                    //const clienteCell = row.insertCell(0);
                    //const direccionIPCell = row.insertCell(1);
                    console.log("Procesando Cliente: " + cliente);
                    const direccionIPCell = row.insertCell(0);
                    direccionIPCell.textContent = cliente.cliente;
                    direccionIPCell.textContent = cliente.cliente; // Supongo que la dirección IP está en la propiedad "cliente"
                }
            }
        })
        .catch(error => {
            console.log("Entro al error");
            console.error("Error al obtener la lista de clientes:", error);
        });
}

/* actualizarListaVideos = getListaArchivos + dibujarTablaReproduccion +  marcarFilaReproduccion*/
function actualizarListaVideos(){
    getListaArchivos();
    dibujarTablaReproduccion();
    marcarFilaReproduccion();
}


/* getListaArchivos() 
* Recive: [{"archivo": "13COMANDOSRAROS.mp4", "tamano": "939.55 MB", "Fecha_Creacion": "20/09/2023 13:38", "duracion_segundos": 991.747483, "duracion_hms": "00:16:31"}, {"archivo": "ConcordeJustKis.mp4", "tamano": "6.37 MB", "Fecha_Creacion": "20/09/2023 21:32", "duracion_segundos": 300.721633, "duracion_hms": "00:05:00"}]
* Retorna una promesa.
*/
function getListaArchivos() {
    return new Promise((resolve, reject) => {
        fetch('/listar_archivos_detalle')
            .then(response => response.json()) // Parsear la respuesta JSON
            .then(data => {
                // Crea un array para almacenar los elementos
                elementos = [];

                // Itera a través de los elementos y guárdalos en el array
                data.forEach(elemento => {
                    elementos.push(elemento);
                });

                // Resuelve la promesa con el array de elementos
                resolve(elementos);
            })
            .catch(error => {
                reject(error); // Rechaza la promesa en caso de error
            });
    });
}

/* 
* getListaArchivosSinPromesa() 
*/
function getListaArchivosSinPromesa() {
    fetch('/listar_archivos_detalle')
        .then(response => response.json()) // Parsear la respuesta JSON
        .then(data => {
            // Crea un array para almacenar los elementos
            elementos = [];

            // Itera a través de los elementos y guárdalos en el array
            data.forEach(elemento => {
                elementos.push(elemento);
            });
        })
        .catch(error => {
            reject(error); // Rechaza la promesa en caso de error
        });
}


/****************
 * siguiente()
 ****************/
function siguiente(){
    console.log("Entrando en siguiente()");
    // Busco la fila
    if(videoReproduciendo != "") {
        console.log("videoReproduciendo =" + videoReproduciendo);
        const indiceDelReproduciendo = elementos.findIndex(elemento => elemento.archivo === videoReproduciendo);
        const indiceEntero = parseInt(indiceDelReproduciendo); // Convierte a entero
    
        cantVideosEnElementos = elementos.length;
        console.log("cantVideosEnElementos=" + cantVideosEnElementos);
    
        indiceDeFila = indiceEntero + 1;

        if (indiceDeFila >= cantVideosEnElementos){
            console.log("Estoy al final de la lista paso al 0");
            indiceDeFila = 0;
            console.log("Ahora saltaría a reproducir: " + elementos[indiceDeFila].archivo);
            reproducirVideo(elementos[indiceDeFila].archivo);
        } else {
            console.log("Ahora saltaría a reproducir: " + elementos[indiceDeFila].archivo);
            reproducirVideo(elementos[indiceDeFila].archivo);
        }
    } else {
        console.log("No hay reproduciendo, luego reproduciría el primero - Indice 0");
        indiceDeFila = 0;
        console.log("Ahora saltaría a reproducir: " + elementos[indiceDeFila].archivo);
        reproducirVideo(elementos[indiceDeFila].archivo);
    }
}

/****************
 * anterior()
 ****************/
function anterior(){
    console.log("Entrando en anterior()");
    // Busco la fila
    if(videoReproduciendo != "") {
        console.log("videoReproduciendo =" + videoReproduciendo);
        const indiceDelReproduciendo = elementos.findIndex(elemento => elemento.archivo === videoReproduciendo);
        const indiceEntero = parseInt(indiceDelReproduciendo); // Convierte a entero
    
        cantVideosEnElementos = elementos.length;
        console.log("cantVideosEnElementos=" + cantVideosEnElementos);
    
        indiceDeFila = indiceEntero - 1;

        if (indiceDeFila <= 0){
            console.log("Estoy al inicio de la lista paso al ultimo");
            indiceDeFila = elementos.length - 1;
            console.log("Ahora saltaría a reproducir: " + elementos[indiceDeFila].archivo);
            reproducirVideo(elementos[indiceDeFila].archivo);
        } else {
            console.log("Ahora saltaría a reproducir: " + elementos[indiceDeFila].archivo);
            reproducirVideo(elementos[indiceDeFila].archivo);
        }
    } else {
        console.log("No hay reproduciendo, luego reproduciría el ultimo de la lista - Indice: " + elementos.length -1 );
        indiceDeFila = elementos.length - 1;
        console.log("Ahora saltaría a reproducir: " + elementos[indiceDeFila].archivo);
        reproducirVideo(elementos[indiceDeFila].archivo);
    }
}

/****************
 * avanzar30()
 ****************/
function avanzar30(){
    gestionDeFlujoReproduccion("+30");
    console.log("Avanzando 30 segundos");
}

/****************
 * retroceder30()
 ****************/
function retroceder30(){
    gestionDeFlujoReproduccion("-30");
    console.log("Retrocedo 30 segundos");
}

/****************
 * avanzar60()
 ****************/
 function avanzar60(){
    gestionDeFlujoReproduccion("+60");
    console.log("Avanzando 30 segundos");
}

/****************
 * retroceder60()
 ****************/
function retroceder60(){
    gestionDeFlujoReproduccion("-60");
    console.log("Retrocedo 30 segundos");
}

/****************
 * getReproduciendo()
 ****************/
// Define la función getReproduciendo como async para poder usar await
async function getReproduciendo() {
    try {
        const response = await fetch('/getVideoReproduciendo');
        const data = await response.json();
        const videoReproduciendo = data.video;
        console.log("Reproduciendo obtenido de /getVideoReproduciendo: " + videoReproduciendo);
        const fechaHoraActual = obtenerFechaYHora();
        agregarEvento(fechaHoraActual + " - Video Reproduciendo cargado de Backend: " + videoReproduciendo);
        return videoReproduciendo;
    } catch (error) {
        return "";
    }
}

/****************
 * obtenerFechaYHora()
 * Obtiene la fecha/hora para agregarEvento al visor de eventos
 ****************/
function obtenerFechaYHora() {
    const fecha = new Date();
  
    // Obtener año, mes y día
    const year = fecha.getFullYear();
    const month = String(fecha.getMonth() + 1).padStart(2, '0'); // El mes comienza en 0, así que agregamos 1 y formateamos con ceros a la izquierda si es necesario
    const day = String(fecha.getDate()).padStart(2, '0');
  
    // Obtener horas, minutos y segundos
    const hours = String(fecha.getHours()).padStart(2, '0');
    const minutes = String(fecha.getMinutes()).padStart(2, '0');
    const seconds = String(fecha.getSeconds()).padStart(2, '0');
  
    // Construir la cadena de fecha y hora en el formato deseado
    const fechaYHora = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  
    return fechaYHora;
  }

function gestionDeFlujoReproduccion(accion){
//accion pueden ser "+30", "-30", "+60", "-60"
    const datos = {control: accion};
    const jsonDatos = JSON.stringify(datos);
    console.log("JSON de control de flujo: " + jsonDatos);

    // Paso 3: Enviar la cadena JSON al servidor usando fetch
    const endpointURL = "/controlDeFlujo"; // Reemplaza esto con la URL de tu endpoint
    const opciones = {
    method: "POST", // Método HTTP (puede ser POST, GET, PUT, etc., según tu necesidad)
    headers: {
        "Content-Type": "application/json" // Tipo de contenido para indicar que estás enviando JSON
    },
    body: jsonDatos // Los datos JSON que deseas enviar
    };

    fetch(endpointURL, opciones)
    .then(response => {
        if (response.ok) {
        return response.json(); // Si la respuesta es exitosa, puedes parsear la respuesta JSON si es necesario
        } else {
        throw new Error("Error al enviar datos al servidor");
        }
    })
    .then(data => {
        // Aquí puedes manejar la respuesta del servidor si es necesario
        console.log("Respuesta del servidor:", data);
    })
    .catch(error => {
        // Manejar errores, por ejemplo, si la solicitud no pudo completarse
        console.error("Error:", error);
    });
}

/****************
 * init()
 ****************/
// Define una función async que contiene el evento DOMContentLoaded
async function init() {
    const reproduciendo = await getReproduciendo(); // Usa await dentro de una función async
    if (reproduciendo !== "") {
        videoReproduciendo = reproduciendo;
    }
    actualizarListaVideos();
    setInterval(actualizarListaVideos, 5000);
    setInterval(cargarClientes, 15000);
}

/************************************************** 
* Listeners 
**************************************************/
document.getElementById('enviar').addEventListener('click', enviarDatos);
document.addEventListener("DOMContentLoaded", init);

/** Listener de cambio de tema **/
button.addEventListener('click', () => {
    darkModeEnabled = !darkModeEnabled; // Alternar entre temas oscuro y claro
    const body = document.body;
    const eventos = document.getElementById

    if (darkModeEnabled) {
        document.body.style.backgroundColor = '#333'; // Cambia el fondo a un color oscuro
        document.body.style.color = '#fff'; // Cambia el color del texto a blanco

        body.classList.add('dark-theme'); // Agregar la clase 'dark-theme' al cuerpo
        document.getElementById("eventos").classList.add("dark-theme");
        console.log('Tema oscuro activado');
        button.innerHTML = '<span>&#x1F4A1;</span> Encender';

        // Aplicar tema oscuro a las tablas con identificadores específicos
        const tables = document.querySelectorAll('#tablaListaReproduccion, #tablaClientes');
        tables.forEach(table => {
            table.classList.add('dark-theme'); // Agregar clase 'dark-theme' a las tablas
        });

        const elementosSeleccionados = document.querySelectorAll('.seleccionada');
        elementosSeleccionados.forEach(elemento => {
            elemento.classList.add('dark-theme');
        });
    } else {
        document.body.style.backgroundColor = '#ffffff'; // Cambia el fondo a un color oscuro
        document.body.style.color = '#000000'; // Cambia el color del texto a blanco

        body.classList.remove('dark-theme'); // Eliminar la clase 'dark-theme' del cuerpo
        document.getElementById("eventos").classList.remove("dark-theme");
        console.log('Tema claro activado');
        button.innerHTML = '<span>&#x1F4A1;</span> Apagar';
        // Restaurar estilos anteriores del botón aquí si es necesario

        // Restaurar tema claro en las tablas con identificadores específicos
        const tables = document.querySelectorAll('#tablaListaReproduccion, #tablaClientes');
        tables.forEach(table => {
            table.classList.remove('dark-theme'); // Eliminar clase 'dark-theme' de las tablas
        });

        const elementosSeleccionados = document.querySelectorAll('.seleccionada');
        elementosSeleccionados.forEach(elemento => {
            elemento.classList.remove('dark-theme');
        });
    }
});

/** Listener de cambio de siguiente **/
buttonSiguiente.addEventListener('click', () => {
    siguiente();
}); 

/** Listener de cambio de anterior **/
buttonAnterior.addEventListener('click', () => {
    anterior();
}); 

/** Listener de cambio de anterior **/
buttonAdelantar30s.addEventListener('click', () => {
    avanzar30();
}); 

/** Listener de cambio de anterior **/
buttonAtrasar30s.addEventListener('click', () => {
    retroceder30();
});

/** Listener de cambio de anterior **/
buttonAdelantar60s.addEventListener('click', () => {
    avanzar60();
}); 

/** Listener de cambio de anterior **/
buttonAtrasar60s.addEventListener('click', () => {
    retroceder60();
});

/***************************************
* Manejador de mensajes con el backend
***************************************/
var host = window.location.hostname;
var endpoint = '/eventosServidor';
var url = 'http://' + host + ":8001" + endpoint;
const eventSource = new EventSource(url);

// Maneja eventos recibidos del servidor
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    //console.log("Recibido mensaje!: " + data);
    console.log("Recibido mensaje del backend:", JSON.stringify(data, null, 2));
    agregarEvento(data.fecha + " - " + data.mensaje);
};