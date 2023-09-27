console.log("Arrancando el Reproductor importado en .js");
let indiceReproduccionActual = 0;
let videoReproduciendo = "";
// let elementosPorArchivo = {}; // Lista que se va a sobreescribir cada vez que consulte getListaArchivos() Deprecado ya que ahora retorna un array y no un object
let elementos = [];
/*****************************
 * Importado del html a pelo
 **************************/
// Variables Globales
let ultimaFilaMarcada = null;
// Lista de detalles de archivos
let listaArchivos = [];
let idSeleccionado = 0;

const button = document.getElementById('toggleButton');
let darkModeEnabled = false;


//******************************
//         MOSTRAR POPUP
//******************************
function mostrarPopup(mensaje) {
    var popup = document.getElementById("popup");
    popup.innerText = mensaje;
    popup.style.display = "block";

    // Ocultar el mensaje emergente después de 3 segundos
    setTimeout(function() {
        popup.style.display = "none";
    }, 1500); // 3000 milisegundos = 3 segundos
}

/*
Agregar Eventos
*/
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

//*******************************
//ENVIAR DATOS PARA DESCARGAR VIDEO DE URL
//*******************************
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
    //fetch('http://localhost:8000/urlDownloader', {
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
* 
* Deshabilitado desde esta vista ya que no es cliente
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

/******************************** 
* reproducirVideo()
********************************/
function reproducirVideo(button) {
    // Limpio todas las classes seleccionada
    const tablaBody = document.getElementById('tabla-body');
    const filas = tablaBody.getElementsByTagName('tr');
    for (let i = 0; i < filas.length; i++) {
        filas[i].classList.remove('seleccionada');
    }
    //Cambio también la propiedad del anterior
    idAnterior = idSeleccionado;
    const filaValorActualizar = tablaBody.querySelector(`tr[data-id="${idAnterior}"]`);
        if (filaValorActualizar) {
            filaValorActualizar.style.backgroundColor = "";
            //filaValorActualizar.classList.add('seleccionado')
            //console.log("/listar_archivos - valor de filaValorActualizar:" + filaValorActualizar);
            filaValorActualizar.querySelector('button:nth-child(2)').disabled = false
        }

    // Obtener la fila seleccionada
    const fila = button.closest('tr');
    const idFila = fila.dataset.id;

    console.log(`Reproducir video con ID: ${idFila}`);

    // Buscar el archivo correspondiente en la lista de archivos
    const archivoSeleccionado = listaArchivos.find(archivo => archivo.id === Number(idFila));

    if (archivoSeleccionado) {
        const nombreArchivo = archivoSeleccionado.nombre;

        // Aquí puedes agregar el código para reproducir el video según el nombre del archivo
        // Datos que quieres enviar en formato JSON
        const datos = {
            accion: "reproducir",
            video: nombreArchivo // Utiliza el nombre del archivo en lugar de idVideo
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
            })
            .catch(error => {
                console.error('Error:', error);
            });

        // Marcar la fila en verde
        fila.classList.add('seleccionada');
        idSeleccionado = idFila
        console.log("Elemento (en reproducir) idSeleccionado: " + idSeleccionado);
        console.log("Lista: " + listaArchivos);

        // Actualizar el detalle de Reproduciendo
        spanReproduciendo = document.getElementById("reproduciendo")
        spanReproduciendo.innerHTML="Reproduciendo: "+ archivoSeleccionado.nombre;

        // Deshabilitar el botón de "Borrar"
        //
        const idBotonBorrar = `borrar-${idSeleccionado}`;
        const botonBorrar = document.getElementById(idBotonBorrar);
        if (botonBorrar) {
            botonBorrar.disabled = true;
        }
    }
}

function reproducirVideo_new(video) {
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
            botones.innerHTML = `<button id="reproducir-${id}" onclick="reproducirVideo(this)">&#x25B6;</button>
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
}

/*
Marco en funcion de reproduciendo. Busco en el array el índice del nombre del archivo y marco la fila: indice + 1 como seleccionada
*/
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
    } else {
        console.log(`El video "${videoReproduciendo}" no se encontró en el array elementos.`);
    }

}

/******************************** 
* borrarVideo()
********************************/
function borrarVideo(idVideo, boton) {
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
        //actualizarListado();
        //actualizarListado_Detalle();
        actualizarListado_Detalle_Externo()
        //boton.disabled = true;
        //var fila = boton.closest('tr');
        //if (fila) {
            // Elimina la fila de la tabla
        //    fila.remove();
        //}
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

/******************************** 
* cargarClientes()
********************************/
// Función para cargar la lista de clientes desde el servidor
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



/* 
* Listeners 
*/
document.getElementById('enviar').addEventListener('click', enviarDatos);
document.addEventListener("DOMContentLoaded", function() {
    //setInterval(actualizarListado, 15000); // 5000 milisegundos = 5 segundos
    //setInterval(actualizarListado_Detalle, 15000); // 5000 milisegundos = 5 segundos
    setInterval(actualizarListado_Detalle_Externo, 15000); // 5000 milisegundos = 5 segundos
    setInterval(cargarClientes, 15000); // 5000 milisegundos = 5 segundos
    //setInterval(registrarCliente, 2000);
    //actualizarListado();
    //actualizarListado_Detalle();
    actualizarListado_Detalle_Externo();
    //registrarCliente();
});
/*
* Listener de cambio de tema
*/
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
    }
});

/***************************************
* Manejador de mensajes con el backend
***************************************/
var host = window.location.hostname;
var endpoint = '/eventosServidor';
var url = 'http://' + host + ":8001" + endpoint;
const eventSource = new EventSource(url);
//const eventSource = new EventSource('http://localhost:8001/eventos');

// Maneja eventos recibidos del servidor
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    //console.log("Recibido mensaje!: " + data);
    console.log("Recibido mensaje del backend:", JSON.stringify(data, null, 2));

    agregarEvento(data.fecha + " - " + data.mensaje);
};




/* Fin del importado del html */


/******************************** 
* actualizarListado_Detalle()
* Recibe: [{"archivo": "13COMANDOSRAROS.mp4", "tamano": "939.55 MB", "Fecha_Creacion": "20/09/2023 13:38", "duracion_segundos": 991.747483, "duracion_hms": "00:16:31"}, {"archivo": "ConcordeJustKis.mp4", "tamano": "6.37 MB", "Fecha_Creacion": "20/09/2023 21:32", "duracion_segundos": 300.721633, "duracion_hms": "00:05:00"}]

Pendiente: el reproducir en lugar de mandar this debe mandar el id del video
********************************/
function actualizarListado_Detalle_Externo() {
    console.log("*********************Actualizando el listado de detalles (Funcion dentro del JS)...");

    fetch('/listar_archivos_detalle')
        .then(response => response.json()) // Parsear la respuesta JSON
        .then(data => {
            console.log("Data recibida: " + data);
            // Obtén la tabla existente
            const tablaReproduccion = document.getElementById('tablaListaReproduccion');
            const tbody = tablaReproduccion.querySelector('tbody');
            tbody.innerHTML = '';
        
            // Iterar sobre la lista de detalles y construir las filas
            data.forEach((detalle, index) => {


                const fila = document.createElement('tr');
                const id = index + 1;
                //fila.dataset.id = id;
                fila.dataset.id = index + 1;

                // Agregar detalles a la lista
                listaArchivos.push({ id, nombre: detalle.archivo });

                // Botones de Reproducción y Borrar
                const botones = document.createElement('td');
                botones.innerHTML = `
                    <button id="reproducir-${id}" onclick="reproducirVideo(this)">&#x25B6;</button>
                    <button id="borrar-${id}" onclick="borrarVideo('${detalle.archivo}', this)">&#x1F5D1;</button>
                `;

                fila.innerHTML = `
                    <td>${id}</td>                       
                    <td>${detalle.archivo}</td>
                    ${botones.outerHTML}
                    <td>${detalle.archivo}</td>
                    <td>${detalle.tamano}</td>
                    <td>${detalle.Fecha_Creacion}</td>
                    <td>${detalle.duracion_hms}</td>
                `;

                tbody.appendChild(fila);

                // Pinto la fila de reproduciendo y deshabilito el boton
                const filaValorActualizar = tbody.querySelector(`tr[data-id="${idSeleccionado}"]`);
                if (filaValorActualizar) {
                    filaValorActualizar.style.backgroundColor = "lime";
                    filaValorActualizar.classList.add('seleccionado')
                    console.log("/listar_archivos - valor de filaValorActualizar:" + filaValorActualizar);
                    const botonBorrar = filaValorActualizar.querySelector('button:nth-child(2)'); // Suponiendo que el botón de "Borrar" es el segundo botón en la fila
                    if (botonBorrar) {
                        botonBorrar.disabled = true;
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error al obtener la lista de detalles:', error);
        });
        const fechaHora = new Date(); // Obtiene la fecha y hora actual
        const formatoFechaHora = fechaHora.toLocaleString(); // Convierte la fecha y hora a una cadena legible
        etiquetaUpdate = document.getElementById("ultimaActualizacion");
        etiquetaUpdate.innerHTML = "Ultima actualizacion: " + formatoFechaHora;
}

// Retorna una promesa
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