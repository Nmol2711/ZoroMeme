import customtkinter as ctk 
import threading
import logging
from public.auth.auth_confg import AuthCofig
from public.screen.componentes.organizar_carpeta.resultado_organizar_carpetas_screen import ResultadoOrganizarCarpetasScreen
from public.widget.arrastrar_soltar import ArrastrarSoltar
from services.organizador_documentos.organizador_documentos import OrganizarDocumentosServices
from services.organizador_documentos.proceso_estado import ProcesoEstado
from public.widget.barra_progreso_widget import BarraProgresoWidget
from utils.config_componen_utils import *
from utils.path_util import *
from public.widget.mensaje_alerta import mensaje_alerta
from utils.existe_conexion import check_internet_socket

logger = logging.getLogger(__name__)

class ScreenOrganizarCarpeta(ctk.CTkFrame):
    def __init__(self, master, parent, auth_config : AuthCofig, services : OrganizarDocumentosServices):
        super().__init__(master, fg_color=COLOR_FONDO_SCREEN_PRINCIPAL)
        self.parent = parent
        self.auth_config = auth_config
        self.services = services
        self.estado = ProcesoEstado()
        self.ruta_carpeta = None

        self.contenido()
        
        # Suscribirse al estado y verificar si ya hay algo corriendo
        self.estado.registrar_callback(self._on_estado_update)
        self.after(100, self._verificar_estado_inicial)

    def _verificar_estado_inicial(self):
        if self.estado.en_ejecucion:
            self.mostrar_progreso_activo()
            # Cargar logs previos si existen
            for log in self.estado.log_en_vivo:
                self.barra_progreso.actualizar(self.estado.archivo_actual, self.estado.get_progreso(), self.estado.get_texto_progreso(), log)
        elif self.estado.resultado_final:
            self.mostrar_resultado(self.estado.resultado_final)

    def _on_estado_update(self):
        """Callback invocado por ProcesoEstado cuando algo cambia."""
        self.after(0, self._actualizar_ui_progreso)

    def _actualizar_ui_progreso(self):
        if not self.winfo_exists():
            return
            
        if self.estado.en_ejecucion:
            # Obtener el último log si hay nuevos
            ultimo_log = self.estado.log_en_vivo[-1] if self.estado.log_en_vivo else None
            self.barra_progreso.actualizar(
                self.estado.archivo_actual, 
                self.estado.get_progreso(), 
                self.estado.get_texto_progreso(),
                ultimo_log
            )
        
        elif self.estado.resultado_final:
            self.mostrar_resultado(self.estado.resultado_final)

    def contenido(self):
        try:
            self.frame_main = ctk.CTkFrame(self, fg_color="transparent")
            self.frame_main.pack(expand=True, fill="both")

            self.label_titulo = ctk.CTkLabel(self.frame_main,
                        text="Organizador de carpetas", 
                        font=FONT_TITULO_PRINCIPAL, 
                        text_color=COLOR_TEXTO_TITULO, 
                        justify="left")
            self.label_titulo.pack(pady=20, padx=20, anchor="w")
            
            self.label_subtitulo = ctk.CTkLabel(self.frame_main,
                        text="Arrastre la carpeta que desea analizar o selecciónela con el botón Examinar", 
                        font=FONT_NORMAL, 
                        text_color=COLOR_TEXTO_SUBTITULO, 
                        justify="left")
            self.label_subtitulo.pack(padx=20, anchor="w")
                        
            self.boton_examinar = ctk.CTkButton(self.frame_main, text="Examinar", command=self.examinar_ruta, 
                                            fg_color=COLOR_BOTON_GOKU, 
                                            hover_color=COLOR_BOTON_GOKU_HOVER, 
                                            height=40, 
                                            width=120)
            self.boton_examinar.pack(anchor="e", padx=40)
            

            self.frame_arrastrar_soltar = ctk.CTkFrame(self.frame_main, border_width=2, border_color=BORDE_COLOR)
            self.frame_arrastrar_soltar.pack(pady=20, padx=40, fill="x")

            # --- Widget de Progreso Avanzado ---
            self.frame_progreso_container = ctk.CTkFrame(self.frame_main, fg_color="transparent")
            self.frame_progreso_container.pack(pady=10, padx=40, fill="x")
            
            self.barra_progreso = BarraProgresoWidget(self.frame_progreso_container)
            self.barra_progreso.pack(fill="x")
            self.frame_progreso_container.pack_forget() # Ocultar al inicio

            self.widget_arrastrar_soltar = ArrastrarSoltar(self.frame_arrastrar_soltar, self.guardar_ruta)
            self.widget_arrastrar_soltar.pack(fill="x")

            frame_inferior = ctk.CTkFrame(self.frame_main, fg_color="transparent")
            frame_inferior.pack(fill="x")

            self.label_ruta_seleccionada = ctk.CTkLabel(frame_inferior, text="NO HAY RUTA SELECCIONADA", 
                                                        font=FONT_PEQUENO, 
                                                        text_color=COLOR_TEXTO_NEGATIVO,
                                                        justify="left")
            self.label_ruta_seleccionada.pack(pady=20, padx=40, anchor="w", side="left")

            self.boton_eliminar_ruta = ctk.CTkButton(frame_inferior, 
                                                text="Eliminar", 
                                                fg_color=COLOR_BOTON_GOKU, 
                                                hover_color=COLOR_BOTON_GOKU_HOVER, 
                                                height=40, 
                                                width=120,
                                                command=self.eliminar_ruta)
            self.boton_eliminar_ruta.pack(pady=20, padx=20, side="left")
            self.boton_eliminar_ruta.configure(state="disabled")

            self.boton_continuar = ctk.CTkButton(frame_inferior, 
                                                text="Comenzar", 
                                                fg_color=COLOR_BOTON_PRINCIPAL, 
                                                hover_color=COLOR_BOTON_PRINCIPAL_HOVER, 
                                                height=40, 
                                                width=120,
                                                command=self.continuar)
            self.boton_continuar.pack(pady=20, padx=40, side="right")
            self.boton_continuar.configure(state="disabled")

        except Exception as e:
            logger.error(f"Error en contenido: {e}")
    
    def guardar_ruta(self, ruta_carpeta = None):
        if self.estado.en_ejecucion: return
        self.ruta_carpeta = ruta_carpeta
        if ruta_carpeta:
            self.label_ruta_seleccionada.configure(text=f"Ruta seleccionada:\n{self.ruta_carpeta}", text_color=COLOR_TEXTO_POSITIVO)
            self.boton_eliminar_ruta.configure(state="normal")
            self.boton_examinar.configure(state="disabled")
            self.widget_arrastrar_soltar.desabilitar()
            self.boton_continuar.configure(state="normal")
    
    def continuar(self):
        if self.ruta_carpeta:
            self.mostrar_progreso_activo()
            
            # El proceso se encarga de actualizar el estado
            thread = threading.Thread(target=self.proceso_organizar)
            thread.daemon = True # Detener con la app
            thread.start()

    def mostrar_progreso_activo(self):
        """Configura la UI para mostrar que hay un proceso en marcha."""
        self.boton_continuar.configure(state="disabled")
        self.boton_examinar.configure(state="disabled")
        self.boton_eliminar_ruta.configure(state="disabled")
        
        self.frame_progreso_container.pack(pady=10, padx=40, fill="x")
        self.barra_progreso.actualizar("Iniciando...", self.estado.get_progreso(), "Preparando archivos...")

    def proceso_organizar(self):
        # Validaciones iniciales
        existe_api, mensaje_api = self.auth_config.existe_api_key()
        existe_dir, mensaje_dir = self.auth_config.existe_diccionario_palabras()
        
        if not existe_api:
            self.after(0, lambda: mensaje_alerta("API Key no configurada", mensaje_api))
            self.estado.reset()
            return
        
        if not check_internet_socket():
            self.after(0, lambda: mensaje_alerta("Sin conexión", "Verifique su conexión a Internet."))
            self.estado.reset()
            return
        
        if not existe_dir:
            self.after(0, lambda: mensaje_alerta("Configuración incompleta", mensaje_dir))
            self.estado.reset()
            return

        try:
            self.services.organizar_hibrido(self.ruta_carpeta, self.auth_config.obtener_cliente_groq())
        except Exception as e:
            logger.error(f"Error en hilo de organización: {e}")
            self.estado.finalizar(None)

    def examinar_ruta(self):
        ruta = seleccionar_carpeta()
        if ruta:
            self.guardar_ruta(ruta)

    def eliminar_ruta(self):
        self.ruta_carpeta = None
        self.label_ruta_seleccionada.configure(text="NO HAY RUTA SELECCIONADA", text_color=COLOR_TEXTO_NEGATIVO)
        self.boton_eliminar_ruta.configure(state="disabled")
        self.boton_examinar.configure(state="normal")
        self.widget_arrastrar_soltar.habilitar()
        self.boton_continuar.configure(state="disabled")

    def mostrar_resultado(self, resultados: dict):
        if not self.winfo_exists(): return
        
        # Ocultar controles principales y mostrar resultados
        self.frame_main.pack_forget()
        
        # Limpiar resultados previos si los hay
        if hasattr(self, 'frame_resultados'):
            self.frame_resultados.destroy()
            
        self.frame_resultados = ResultadoOrganizarCarpetasScreen(self, self.parent, resultados)
        self.frame_resultados.pack(fill="both", expand=True)

    def finalizar_y_volver(self):
        """Invocado por el botón de la pantalla de resultados."""
        self.estado.reset()
        
        # Limpieza agresiva: destruir cualquier widget que no sea el frame_main
        for widget in self.winfo_children():
            if widget != self.frame_main:
                widget.destroy()
        
        # Si por alguna razón frame_main se perdió, lo reconstruimos (fallback de seguridad)
        if not hasattr(self, 'frame_main') or not self.frame_main.winfo_exists():
            self.contenido()
        
        # Volver a mostrar el frame principal
        self.frame_main.pack(expand=True, fill="both")
        self.eliminar_ruta()
        
        if hasattr(self, 'frame_progreso_container'):
            self.frame_progreso_container.pack_forget()
        
        # Aseguramos que los controles de entrada vuelvan a estar activos
        self.boton_examinar.configure(state="normal")
        self.widget_arrastrar_soltar.habilitar()
        
        # Forzar redibujado para evitar "fantasmas" visuales
        self.update_idletasks()