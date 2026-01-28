import customtkinter as ctk
from public.auth.auth_confg import AuthCofig
from public.screen.componentes.ayuda.ayuda_screen import AyudaScreen
from public.screen.componentes.acerca_de_screen.acerca_de_screen import AcercaDeScreen
from public.screen.componentes.configuracion.configuracion_screen import ConfiguracionScreen
from public.screen.componentes.contacto.contacto_screen import ContactoScreen
from public.screen.componentes.historial_movimiento.historial_movimiento_screen import HistorialMovimientoScreen
from public.screen_base import ScreenBase
from public.widget.mensaje_alerta import mensaje_alerta
from utils.path_ultil import *
from utils.config_componen_utils import *
from config.settings import Settings
from config.app_config import AppConfig
from datetime import datetime
# Importar las Screen de las opciones
from public.screen.componentes.organizar_carpeta.organizar_carpetas_screen import ScreenOrganizarCarpeta

class ScreenPrincipal(ScreenBase):
    def __init__(self, master, auth_config: AuthCofig, services):
        super().__init__(master, auth_config, services)
        
        self.inicio()
        # Esperamos 1 segundo (1000ms) para que se muestre el inicio antes de validar
        self.after(1000, self.validar_arranque)

    def validar_arranque(self):
        existe = self.auth_config.existe_api_key()
        if not existe[0]:
            mensaje_alerta("Advertencia", existe[1], accion=lambda: self.dirijir_atomaticamente_opcion("configurar"))
        else:
            autorizado = self.auth_config.autenticar_api_key()
            if not autorizado:
                mensaje_alerta("Error", "La API Key no es válida o ha expirado.", accion=lambda: self.dirijir_atomaticamente_opcion("configurar"))

    def inicio(self):
        # Limpiar el cuerpo principal
        if self.opcion_actual == "inicio":
            return
        self.opcion_actual = "inicio"

        for widget in self.cuerpo_principal.winfo_children():
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
        print("Tamaño de Goku en inicio:", tamano_goku)
        goku = leer_imagen(Settings().ruta_img["goku_inicio"], tamano=tamano_goku)
        goku_label = ctk.CTkLabel(frame_inicio, image=goku, text="")
        # rowspan=2 permite que la imagen ocupe tanto la fila del texto como la de las stats
        goku_label.grid(row=0, column=1, rowspan=2, sticky="nsew")

    def organizar_carpeta(self):

        if self.opcion_actual == "organizar_carpeta":
            return
        self.opcion_actual = "organizar_carpeta"

        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        screen_organizar_carpeta = ScreenOrganizarCarpeta(self.cuerpo_principal,self, self.auth_config, self.services["organizador_documentos_services"])
        screen_organizar_carpeta.pack(fill="both", expand=True)

    def historial_movimiento(self):

        if self.opcion_actual == "historial_movimiento":
            return
        self.opcion_actual = "historial_movimiento"
        
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        historial_movimiento = HistorialMovimientoScreen(self.cuerpo_principal, self, self.services["configuracion_services"])
        historial_movimiento.pack(fill="both", expand=True)

    def configurar(self):

        if self.opcion_actual == "configurar":
            return
        self.opcion_actual = "configurar"

        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        configurarScreen = ConfiguracionScreen(self.cuerpo_principal, self, self.auth_config, self.services["configuracion_services"])
        configurarScreen.pack(fill="both", expand=True)

    def mostrar_ayuda(self):

        if self.opcion_actual == "ayuda":
            return
        self.opcion_actual = "ayuda"

        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        ayuda_screen = AyudaScreen(self.cuerpo_principal, self)
        ayuda_screen.pack(fill="both", expand=True)

    def contacto(self):
        if self.opcion_actual == "ayuda":
            return
        self.opcion_actual = "ayuda"

        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        contacto_screen = ContactoScreen(self.cuerpo_principal, self, self.auth_config, self.services)
        contacto_screen.pack(fill="both", expand=True)

    def acerca_de(self):

        if self.opcion_actual == "acerca_de":
            return
        self.opcion_actual = "acerca_de"

        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        acerca_de_screen = AcercaDeScreen(self.cuerpo_principal, self)
        acerca_de_screen.pack(fill="both", expand=True)