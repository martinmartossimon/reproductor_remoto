console.log("Arrancando el Reproductor importado en .js");

// Define la clase para un nodo de la lista enlazada
class NodoLista {
    constructor(valor) {
        this.valor = valor;
        this.siguiente = null;
    }
}

// Define la clase para la lista enlazada circular
class ListaReproduccion {
    constructor(videos) {
        this.primero = null;
        this.ultimo = null;
        this.actual = null; // Puntero al elemento actual
        this.crearLista(videos);
    }

    // Método para crear la lista a partir de un array de videos
    crearLista(videos) {
        for (const video of videos) {
            this.agregarVideo(video.archivo);
        }
    }

    // Método para agregar un video a la lista
    agregarVideo(video) {
        const nuevoNodo = new NodoLista(video);
        if (!this.primero) {
            this.primero = nuevoNodo;
            this.ultimo = nuevoNodo;
            nuevoNodo.siguiente = this.primero; // Establece la referencia circular
            this.actual = this.primero; // El primer elemento es el actual al inicio
        } else {
            this.ultimo.siguiente = nuevoNodo;
            nuevoNodo.siguiente = this.primero; // Establece la referencia circular
            this.ultimo = nuevoNodo;
        }
    }

    // Método para obtener el video actual
    obtenerVideoActual() {
        return this.actual ? this.actual.valor : null;
    }

    // Método para avanzar al siguiente video
    siguienteVideo() {
        if (this.actual) {
            this.actual = this.actual.siguiente;
        }
    }

    // Método para retroceder al video anterior
    videoAnterior() {
        if (this.actual) {
            let nodoAnterior = this.primero;
            while (nodoAnterior.siguiente !== this.actual) {
                nodoAnterior = nodoAnterior.siguiente;
            }
            this.actual = nodoAnterior;
        }
    }
}

// Ejemplo de uso
const listaDeVideos = [
    {"archivo": "DEMONSCRESTSUPE.mp4", "tamano": "91.84 MB", "Fecha_Creacion": "25/09/2023 00:54"},
    {"archivo": "Informativomati.mp4", "tamano": "7.17 MB", "Fecha_Creacion": "25/09/2023 09:43"}
];

const listaReproduccion = new ListaReproduccion(listaDeVideos);

// Obtener el video actual
console.log("Video actual:", listaReproduccion.obtenerVideoActual());

// Avanzar al siguiente video
listaReproduccion.siguienteVideo();
console.log("Siguiente video:", listaReproduccion.obtenerVideoActual());

// Retroceder al video anterior
listaReproduccion.videoAnterior();
console.log("Video anterior:", listaReproduccion.obtenerVideoActual());