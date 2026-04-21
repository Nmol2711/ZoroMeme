import customtkinter as ctk
from public.auth.auth_confg import AuthCofig
from public.screen.componentes.ayuda.ayuda_screen import AyudaScreen
from public.screen.componentes.acerca_de_screen.acerca_de_screen import AcercaDeScreen
from public.screen.componentes.configuracion.configuracion_screen import ConfiguracionScreen
from public.screen.componentes.contacto.contacto_screen import ContactoScreen
from public.screen.componentes.historial_movimiento.historial_movimiento_screen import HistorialMovimientoScreen
from public.screen_base import ScreenBase
from public.widget.mensaje_alerta import mensaje_alerta
from utils.path_util import *
from utils.config_componen_utils import *
from config.settings import Settings
from config.app_config import AppConfig
from datetime import datetime
# Importar las Screen de las opciones
from public.screen.componentes.organizar_carpeta.organizar_carpetas_screen import ScreenOrganizarCarpeta

class ScreenPrincipal(ScreenBase):
    def __init__(self, master, auth_config: AuthCofig, services):
        super().__init__(master, auth_config, services)
        self.vistas = {} # Cache de vistas para no perder estado
        
        self.inicio()
        # Esperamos 1 segundo (1000ms) para que se muestre el inicio antes de validar
        self.after(1000, self.validar_arranque)

    def _cambiar_vista(self, nombre_vista, clase_vista, *args, **kwargs):
        """Maneja el cambio de vista ocultando la actual y mostrando la nueva o cacheada."""
        if self.opcion_actual == nombre_vista:
            return
        
        # Ocultar vista anterior si existe
        if self.opcion_actual and self.opcion_actual in self.vistas:
            self.vistas[self.opcion_actual].pack_forget()
        else:
            # Limpieza inicial por si hay widgets manuales (como el inicio)
            for widget in self.cuerpo_principal.winfo_children():
                if widget not in self.vistas.values():
                    widget.destroy()

        self.opcion_actual = nombre_vista

        # Crear vista si no está en cache
        if nombre_vista not in self.vistas:
            self.vistas[nombre_vista] = clase_vista(self.cuerpo_principal, self, *args, **kwargs)
        
        # Mostrar vista
        self.vistas[nombre_vista].pack(fill="both", expand=True)
        
        # Actualizar sidebar si es necesario (ej: resaltar botón actual)
        # self.actualizar_resaltado_menu(nombre_vista)

    def validar_arranque(self):
        existe = self.auth_config.existe_api_key()
        if not existe[0]:
            mensaje_alerta("Advertencia", existe[1], accion=lambda: self.dirijir_atomaticamente_opcion("configurar"))
        else:
            autorizado = self.auth_config.autenticar_api_key()
            if not autorizado:
                mensaje_alerta("Error", "La API Key no es válida o ha expirado.", accion=lambda: self.dirijir_atomaticamente_opcion("configurar"))

    def inicio(self):
        # El inicio es un frame especial que se reconstruye para mostrar estadísticas actualizadas
        if self.opcion_actual == "inicio":
            return
        
        if self.opcion_actual and self.opcion_actual in self.vistas:
            self.vistas[self.opcion_actual].pack_forget()
        
        self.opcion_actual = "inicio"
        # Limpiar inicio anterior si existe
        for widget in self.cuerpo_principal.winfo_children():
            if widget not in self.vistas.values():
                widget.destroy()

        # Obtener estadísticas
        hoy = datetime.now().strftime("%Y-%m-%d")
        primero_dia_mes = hoy[:8] + "01"
        estadisticas = self.services["configuracion_services"].obtener_carpetas_analizadas_archivos_movidos(primero_dia_mes, hoy)

        frame_inicio = ctk.CTkFrame(self.cuerpo_principal, fg_color="transparent")
        frame_inicio.pack(fill="both", expand=True)

        # Configuración del Grid: Columna 0 (Info), Columna 1 (Imagen)
        frame_inicio.grid_columnconfigure(0, weight=1)
        frame_inicio.grid_columnconfigure(1, weight=1)
        frame_inicio.grid_rowconfigure(0, weight=1) # Espacio superior (Texto)
        frame_inicio.grid_rowconfigure(1, weight=0) # Espacio inferior (Estadísticas)

        # --- SECCIÓN IZQUIERDA SUPERIOR: Bienvenida ---
        frame_texto = ctk.CTkFrame(frame_inicio, fg_color="transparent")
        frame_texto.grid(row=0, column=0, sticky="nw", padx=40, pady=100)

        ctk.CTkLabel(frame_texto, text="Bienvenidos al inicio del \nsistema organizador", text_color="white", font=FONT_TITULO_PRINCIPAL, justify="left").pack(anchor="w")
        ctk.CTkLabel(frame_texto, text="Tu asistente inteligente para gestionar documentos.", text_color="gray", font=FONT_NORMAL).pack(anchor="w", pady=5)

        # --- SECCIÓN IZQUIERDA INFERIOR: Estadísticas ---
        frame_stats = ctk.CTkFrame(frame_inicio, fg_color="transparent")
        frame_stats.grid(row=1, column=0, sticky="sw", padx=40, pady=(0, 100))

        def crear_stat_box(titulo, valor):
            box = ctk.CTkFrame(frame_stats, fg_color=COLOR_AZUL_PRINCIPAL, corner_radius=8)
            box.pack(side="left", padx=(0, 15), ipadx=15, ipady=10)
            ctk.CTkLabel(box, text=valor, font=("Roboto", 24, "bold"), text_color="white").pack()
            ctk.CTkLabel(box, text=titulo, font=("Roboto", 12), text_color="white").pack()

        crear_stat_box("Capetas Analizadas\n(Este Mes)", str(estadisticas[0]))
        crear_stat_box("Archivos Movidos", str(estadisticas[1]))

        # --- SECCIÓN DERECHA: Imagen ---
        tamano_goku = AppConfig().tamano_goku_actual
        goku = leer_imagen(Settings().ruta_img["goku_inicio"], tamano=tamano_goku)
        goku_label = ctk.CTkLabel(frame_inicio, image=goku, text="")
        goku_label.grid(row=0, column=1, rowspan=2, sticky="nsew")

    def organizar_carpeta(self):
        # 1. Validar que la API Key existe (Local, rápido)
        existe, mensaje = self.auth_config.existe_api_key()
        if not existe:
            mensaje_alerta("API Key requerida", 
                          "Para usar el organizador es necesario configurar una API Key de Groq.\n\n" + mensaje,
                          accion=lambda: self.dirijir_atomaticamente_opcion("configurar"))
            return

        # 2. Cambiar de vista instantáneamente. 
        # La validación funcional se hace al arrancar o al presionar "Comenzar" dentro de la vista.
        self._cambiar_vista("organizar_carpeta", ScreenOrganizarCarpeta, self.auth_config, self.services["organizador_documentos_services"])

    def historial_movimiento(self):
        self._cambiar_vista("historial_movimiento", HistorialMovimientoScreen, self.services["configuracion_services"])

    def configurar(self):
        self._cambiar_vista("configurar", ConfiguracionScreen, self.auth_config, self.services["configuracion_services"])

    def mostrar_ayuda(self):
        self._cambiar_vista("ayuda", AyudaScreen)

    def contacto(self):
        self._cambiar_vista("contacto", ContactoScreen, self.auth_config, self.services["email_services"])

    def acerca_de(self):
        self._cambiar_vista("acerca_de", AcercaDeScreen)