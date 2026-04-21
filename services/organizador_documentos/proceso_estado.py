import threading

class ProcesoEstado:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ProcesoEstado, cls).__new__(cls)
                cls._instance._inicializar()
            return cls._instance

    def _inicializar(self):
        self.en_ejecucion = False
        self.archivo_actual = ""
        self.total_archivos = 0
        self.procesados = 0
        self.log_en_vivo = []
        self.resultado_final = None
        self.callbacks = []
        self.ruta_carpeta_actual = None

    def reset(self):
        with self._lock:
            self.en_ejecucion = False
            self.archivo_actual = ""
            self.total_archivos = 0
            self.procesados = 0
            self.log_en_vivo = []
            self.resultado_final = None
            self.ruta_carpeta_actual = None
            self._notificar()

    def iniciar(self, total, ruta):
        with self._lock:
            self.en_ejecucion = True
            self.total_archivos = total
            self.procesados = 0
            self.archivo_actual = "Iniciando..."
            self.log_en_vivo = [f"Iniciando análisis en: {ruta}"]
            self.resultado_final = None
            self.ruta_carpeta_actual = ruta
            self._notificar()

    def actualizar(self, archivo, mensaje=None, incremento=True):
        with self._lock:
            if incremento:
                self.procesados += 1
            self.archivo_actual = archivo
            if mensaje:
                self.log_en_vivo.append(mensaje)
            self._notificar()

    def finalizar(self, resultado):
        with self._lock:
            self.en_ejecucion = False
            self.resultado_final = resultado
            self._notificar()

    def registrar_callback(self, callback):
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def eliminar_callback(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def _notificar(self):
        for cb in self.callbacks:
            try:
                cb()
            except Exception as e:
                print(f"Error en callback de estado: {e}")

    def get_progreso(self):
        if self.total_archivos == 0:
            return 0
        return self.procesados / self.total_archivos

    def get_texto_progreso(self):
        return f"Procesado: {self.procesados} de {self.total_archivos} archivos"
