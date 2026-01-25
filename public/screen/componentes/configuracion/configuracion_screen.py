import customtkinter as ctk 
from public.screen.componentes.configuracion.config_api_key_screen import ConfigApiKeyScreen
from public.screen.componentes.configuracion.config_directorios_destinos_screen import ConfigDirectoriosDestinosScreen
from services.configuracion_services.configuracion_services import ConfiguracionServices
from utils.config_componen_utils import *
from utils.path_ultil import *

class ConfiguracionScreen(ctk.CTkFrame):
    def __init__(self, master, parent, auth, configuracion_services: ConfiguracionServices):
        super().__init__(master)
        self.auth = auth
        self.configuacion_services = configuracion_services
        self.parent = parent
        self.contenido()

    def contenido(self):
        ctk.CTkLabel(self, text="Configuración", font=FONT_TITULO_PRINCIPAL, text_color=COLOR_TEXTO_TITULO, justify="left").pack(pady=(20,0), padx=20, anchor="w")


        self.frame_contenido_mostrar = ctk.CTkFrame(self, fg_color="transparent", border_color=BORDE_COLOR, border_width=2,)
        self.frame_contenido_mostrar.pack(expand=True, fill="both", padx=60, pady=60)

        self.frame_contenido_inicio = ctk.CTkFrame(self.frame_contenido_mostrar, fg_color="transparent")
        self.frame_contenido_inicio.pack(expand=True, fill="both")



        #frame para el contenido izquierdo
        frame_contenido_izquierdo = ctk.CTkFrame(self.frame_contenido_inicio, fg_color= COLOR_FONDO_SCREEN_SECUNDARIO, corner_radius=10)
        frame_contenido_izquierdo.pack(side="left", expand=True, fill="both", padx=20, pady=20)

        titulo_config_api_key = ctk.CTkLabel(frame_contenido_izquierdo, text="Configuración de API Key", font=FONT_MENU, text_color=COLOR_TEXTO_TITULO, justify="left")
        titulo_config_api_key.pack(pady=(20,0), padx=20, anchor="w")

        parrafo_info_api_key = ctk.CTkLabel(frame_contenido_izquierdo, 
                                            text="Conecta el sistema con la IA de Groq.\nEs esencial para analizar el contexto de los documentos desconocidos y clasificarlos inteligentemente.", 
                                            font=FONT_NORMAL, 
                                            text_color=COLOR_TEXTO_SUBTITULO, 
                                            justify="left",
                                            wraplength=280)
        parrafo_info_api_key.pack(pady=(10,0), padx=20, anchor="w")

        boton_config_api = ctk.CTkButton(frame_contenido_izquierdo, text="Configurar", 
                                         fg_color=COLOR_BOTON_PRINCIPAL, 
                                         hover_color=COLOR_BOTON_PRINCIPAL_HOVER, 
                                         command=self.abrir_config_api)
        boton_config_api.pack(side="bottom", anchor="e", padx=20, pady=20)

        #frame para el contenido derecho
        frame_contenido_derecho = ctk.CTkFrame(self.frame_contenido_inicio, fg_color= COLOR_FONDO_SCREEN_SECUNDARIO, corner_radius=10)
        frame_contenido_derecho.pack(side="left", expand=True, fill="both", padx=20, pady=20)

        titulo_config_direcorios = ctk.CTkLabel(frame_contenido_derecho, text="Configuración de Directorios con\nPalabras Claves", font=FONT_MENU, text_color=COLOR_TEXTO_TITULO, justify="left")
        titulo_config_direcorios.pack(pady=(20,0), padx=20, anchor="w")

        parrafo_info_directorios = ctk.CTkLabel(frame_contenido_derecho, 
                                                text="Crea reglas rápidas y precisas.\nSi un archivo contiene ciertas palabras clave, se moverá directo a la carpeta asignada sin consultar a la IA.", 
                                                font=FONT_NORMAL, 
                                                text_color=COLOR_TEXTO_SUBTITULO, 
                                                justify="left",
                                                wraplength=280)
        parrafo_info_directorios.pack(pady=(10,0), padx=20, anchor="w")

        boton_config_diccionario = ctk.CTkButton(frame_contenido_derecho, text="Configurar", 
                                                 fg_color=COLOR_BOTON_PRINCIPAL, 
                                                 hover_color=COLOR_BOTON_PRINCIPAL_HOVER, 
                                                 command=self.abrir_config_diccionario)
        boton_config_diccionario.pack(side="bottom", anchor="e", padx=20, pady=20)

    def abrir_config_api(self):
        #destruir la ventana los cuadros de informacion
        for widget in self.frame_contenido_mostrar.winfo_children():
            widget.destroy()

        screen_api_key = ConfigApiKeyScreen(self.frame_contenido_mostrar, self.parent,self.auth, self.configuacion_services)
        screen_api_key.pack(expand=True, fill="both", padx=60, pady=60)

    def abrir_config_diccionario(self): 
        #destruir la ventana los cuadros de informacion
        for widget in self.frame_contenido_mostrar.winfo_children():
            widget.destroy()

        screen_directorios = ConfigDirectoriosDestinosScreen(self.frame_contenido_mostrar, self.parent, self.configuacion_services)
        screen_directorios.pack(expand=True, fill="both")