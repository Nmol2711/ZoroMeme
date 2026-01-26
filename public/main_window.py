import customtkinter as ctk
import ctypes
from tkinterdnd2 import TkinterDnD
from config.app_config import AppConfig
from PIL import Image, ImageTk

#importar serices
from services.configuracion_services.configuracion_services import ConfiguracionServices

#importar auth
from public.auth.auth_confg import AuthCofig

# --- VENTANA PRINCIPAL ---
from public.screen.screen_principal import ScreenPrincipal
from services.organizador_documentos.organizador_documentos import OrganizarDocumentosServices

class MainWindow(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        # Desactivar el escalado automático y forzar DPI Awareness en Windows
        ctk.deactivate_automatic_dpi_awareness()
        ctk.set_window_scaling(1.0)
        ctk.set_widget_scaling(1.0)
        
        if AppConfig().sistema_operativo == "Windows":
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()

        super().__init__()

        self.TkdndVersion = TkinterDnD._require(self)

        #Configuaracion de la ventana principal

        self.app_config = AppConfig()
        self.title(self.app_config.titulo_ventana)
        
        # Configuración del icono según el sistema operativo
        if self.app_config.sistema_operativo == "Windows":
            self.iconbitmap(self.app_config.icono)
        else:
            # En Linux/macOS usamos wm_iconphoto con la imagen cargada por PIL
            self.wm_iconphoto(False, ImageTk.PhotoImage(Image.open(self.app_config.icono)))
         
        #Configuracion del tamano de la ventana
        ancho_pantalla = self.winfo_screenwidth()  
        alto_pantalla = self.winfo_screenheight()
        self.tamano_ventana  = self.app_config.evaluar_tamano_pantalla(ancho_pantalla, alto_pantalla)  # Evaluamos el tamaño de la pantalla
        print("Tamaño de la ventana: ",self.tamano_ventana)
        width, height = map(int, self.tamano_ventana.split("x"))
        self.app_config.centrar_ventana(self, width, height)
        self.minsize(width, height)
        self.resizable(True, True)
        # Iniciar la ventana maximizada (habilita el "cuadrito" de pantalla completa)
        if self.app_config.sistema_operativo == "Windows":
            self.state('zoomed')
        elif self.app_config.sistema_operativo == "Linux":
            self.attributes('-zoomed', True)
        #configuracion de tema y colores
        ctk.set_appearance_mode(self.app_config.tema)

        #autenticiones
        self.auth_config = AuthCofig(ConfiguracionServices())

        self.services = {
            "configuracion_services": ConfiguracionServices(),
            "organizador_documentos_services": OrganizarDocumentosServices()
        }


        self.vista_actual = None # Declaramos una variable para la vista actual

        self.mostrar_vista_principal()
    
    def mostrar_vista_principal(self):
        if self.vista_actual is None or not isinstance(self.vista_actual, ScreenPrincipal):
            self.vista_actual = ScreenPrincipal(self, self.auth_config, self.services)
            self.vista_actual.pack(fill="both", expand=True)
        


        
        
