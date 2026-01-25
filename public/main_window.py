import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from config.app_config import AppConfig

#importar serices
from services.configuracion_services.configuracion_services import ConfiguracionServices

#importar auth
from public.auth.auth_confg import AuthCofig

# --- VENTANA PRINCIPAL ---
from public.screen.screen_principal import ScreenPrincipal
from services.organizador_documentos.organizador_documentos import OrganizarDocumentosServices


class MainWindow(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        #Configuaracion de la ventana principal
        self.app_config = AppConfig()
        self.title(self.app_config.titulo_ventana)
        self.iconbitmap(self.app_config.icono)
         
        #Configuracion del tamano de la ventana
        ancho_pantalla = self.winfo_screenwidth()  
        alto_pantalla = self.winfo_screenheight()
        self.tamano_ventana  = AppConfig().evaluar_tamano_pantalla(ancho_pantalla, alto_pantalla)  # Evaluamos el tamaño de la pantalla
        self.app_config.centrar_ventana(self, self.tamano_ventana.split("x")[0], self.tamano_ventana.split("x")[1])
        self.geometry(self.tamano_ventana)
        self.resizable(False, False)

        #configuracion de tema y colores
        ctk.set_appearance_mode(self.app_config.tema)
        AppConfig().centrar_ventana(self, *self.tamano_ventana.split("x"))  # Centramos la ventana en la pantalla

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
        


        
        
