import customtkinter as ctk
from public.auth.auth_confg import AuthCofig
from public.widget.enlaces import CTkHyperlink
from public.widget.entry import EntryWidget
from public.widget.mensaje_alerta import mensaje_alerta
from utils.config_componen_utils import *


from services.configuracion_services.configuracion_services import ConfiguracionServices

class ConfigApiKeyScreen(ctk.CTkFrame):
    def __init__(self, master, parent_principal, auth_config: AuthCofig, configuacion_services: ConfiguracionServices):
        super().__init__(master, fg_color="transparent")
        self.parent_principal = parent_principal
        self.auth_config = auth_config
        self.configuacion_services = configuacion_services
        self.paso_mostrar = self.paso1
        self.contenido()

    def contenido(self):
        self.frame_contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_contenido.pack(expand=True, fill="both", anchor = "w")
        self.paso1()

        self.boton_volver = ctk.CTkButton(self,
                                            text="volver", 
                                            fg_color=COLOR_BOTON_PRINCIPAL, 
                                            hover_color=COLOR_BOTON_PRINCIPAL_HOVER,
                                            command=self.volver_paso)
        self.boton_volver.pack(pady=20, padx=20, side="left", anchor="w")

        self.boton_siguiente = ctk.CTkButton(self,
                                            text="siguiente", 
                                            fg_color=COLOR_BOTON_PRINCIPAL, 
                                            hover_color=COLOR_BOTON_PRINCIPAL_HOVER,
                                            command=self.siguiente_paso)
        self.boton_siguiente.pack(pady=20, padx=20, side="right", anchor="e")

        

    def paso1(self):#indicarle al usuario como generar la API KEY
        self.frame_paso1 = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        self.frame_paso1.pack(expand=False, fill="x")

        ctk.CTkLabel(self.frame_paso1,
                    text="Obtén tu API Key de Groq (Gratis y rápido)", 
                    font=FONT_TITULO_PRINCIPAL, 
                    text_color=COLOR_TEXTO_TITULO, 
                    height=TAMANO_TITULO_PRINCIPAL, 
                    justify="left").pack(pady=20, padx=20, anchor="w")
        
        ctk.CTkLabel(self.frame_paso1,
                     text="1 dirigete a la siguiente pagina: ", 
                     font=FONT_NORMAL, 
                     text_color=COLOR_TEXTO_SUBTITULO, 
                     justify="left").pack(padx=20, anchor="w")
        
        CTkHyperlink(self.frame_paso1, text="console.grop.com/keys", url="https://console.groq.com/keys").pack(padx=30, anchor="w")

        ctk.CTkLabel(self.frame_paso1,
                     text="2 Crea una cuenta (puedes usar Google)", 
                     font=FONT_NORMAL, 
                     text_color=COLOR_TEXTO_SUBTITULO, 
                     justify="left").pack(padx=20, anchor="w")
        
        ctk.CTkLabel(self.frame_paso1,
                     text="3 Una vez logueado, busca la opción API Keys", 
                     font=FONT_NORMAL, 
                     text_color=COLOR_TEXTO_SUBTITULO, 
                     justify="left").pack(padx=20, anchor="w")
        
        ctk.CTkLabel(self.frame_paso1,
                     text="4 Haz clic en \"Create API Key\", ponle un nombre (ej. \"Organizador\").\nLuego copia y guarda la clave en un lugar seguro.",
                     font=FONT_NORMAL, 
                     text_color=COLOR_TEXTO_SUBTITULO, 
                     justify="left").pack(padx=20, anchor="w")
        

    def paso2(self):#introducir la llave y guardarla
        self.frame_paso2 = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        self.frame_paso2.pack(expand=False, fill="x")

        ctk.CTkLabel(self.frame_paso2,
                    text="Introduce tu API Key", 
                    font=FONT_TITULO_PRINCIPAL, 
                    text_color=COLOR_TEXTO_TITULO, 
                    height=TAMANO_TITULO_PRINCIPAL, 
                    justify="left").pack(pady=20, padx=20, anchor="w")

        self.api_key_entry = EntryWidget(self.frame_paso2,
                                        label_text="API Key:",
                                        placeholder_text="Ingresa tu API Key aquí")
        self.api_key_entry.pack(pady=10, padx=20, anchor="w")

    def cambiar_api_key(self):
        pass

    def guardar_api_key(self):
        api_key = self.api_key_entry.get()
        if not api_key:
            mensaje_alerta("Error", "Por favor, ingresa una API Key válida.")
            return
        
        elif self.auth_config.autenticar_api_key(api_key) is False:
            mensaje_alerta("Error", "La API Key ingresada no es válida. Verifícala e intenta nuevamente.")
            return
        
        if self.configuacion_services.guardar_api_key(api_key):
            mensaje_alerta("Éxito", "API Key guardada correctamente.", tipo="check", accion=self.retonar_configuracion_screen)
            return
        else:
            mensaje_alerta("Error", "Hubo un problema al guardar la API Key. Intenta nuevamente.")
            return

    def siguiente_paso(self):
        if self.paso_mostrar == self.paso1:
            self.frame_paso1.destroy()
            self.paso_mostrar = self.paso2
            self.paso2()
            self.boton_siguiente.configure(text="Guardar", command=self.guardar_api_key)
    
    def volver_paso(self):
        if self.paso_mostrar == self.paso2:
            self.frame_paso2.destroy()
            self.paso_mostrar = self.paso1
            self.paso1()
            self.boton_siguiente.configure(text="Siguiente", command=self.siguiente_paso)
        elif self.paso_mostrar == self.paso1:
            self.parent_principal.opcion_actual = None
            self.retonar_configuracion_screen()

    def retonar_configuracion_screen(self):
        # Forzamos la recarga reseteando la opción actual para que el sistema no crea que ya estamos ahí
        self.parent_principal.opcion_actual = None
        self.after(100, lambda: self.parent_principal.dirijir_atomaticamente_opcion("configurar"))
        