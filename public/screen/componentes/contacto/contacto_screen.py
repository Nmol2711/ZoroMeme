import customtkinter as ctk
from config.app_config import AppConfig
from public.auth.auth_confg import AuthCofig
from public.widget.mensaje_alerta import mensaje_alerta
from utils.config_componen_utils import *
from utils.path_ultil import *
from public.widget.entry import EntryWidget, EntryAnchoWidget
from utils.bind_mouse_wheel import bind_mouse_wheel
from config.settings import Settings

class ContactoScreen(ctk.CTkFrame):
    def __init__(self, master, parent, auth_config: AuthCofig, services):
        super().__init__(master)
        self.parent = parent
        self.auth_config = auth_config
        self.services = services
        self.contenido()

        self.boton_enviar = ctk.CTkButton(self, text="Enviar Sugerencia", fg_color=COLOR_BOTON_PRINCIPAL, hover_color=COLOR_BOTON_PRINCIPAL_HOVER, command=self.enviar_consulta)
        self.boton_enviar.pack(pady=(0,60), padx=20, anchor="e")


    def contenido(self):
        ctk.CTkLabel(self, text="Enviar Sugerencia", font=FONT_TITULO_PRINCIPAL, text_color=COLOR_TEXTO_TITULO, justify="left").pack(pady=(20,0), padx=20, anchor="w")

        self.frame_contenido_mostrar = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_contenido_mostrar.grid_columnconfigure(0, weight=1)
        self.frame_contenido_mostrar.grid_columnconfigure(1, weight=1)

        self.frame_contenido_mostrar.grid_rowconfigure(0, weight=0, minsize=10)
        self.frame_contenido_mostrar.grid_rowconfigure(1, weight=4)

        self.frame_contenido_mostrar.pack(fill="both", expand=True, padx=20, pady=20)

        freme_contenido_superios =ctk.CTkFrame(self.frame_contenido_mostrar, fg_color="transparent", border_color=BORDE_COLOR, border_width=2)
        freme_contenido_superios.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,10))

        self.nombre_usuario = EntryWidget(freme_contenido_superios,label_text="Ingresa tu nombre y apellido", placeholder_text="Nombre y Apellido:", width=300)
        self.nombre_usuario.pack(pady=20, padx=20, anchor="w")

        freme_contenido_inferior = ctk.CTkFrame(self.frame_contenido_mostrar, fg_color="transparent", border_color=BORDE_COLOR, border_width=2)
        freme_contenido_inferior.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10,0))

        self.contenido_email = EntryAnchoWidget(freme_contenido_inferior, label_text="Escribe tu sugerencia", width=600, height=200, max_length=300, expand=True)
        self.contenido_email.pack(pady=20, padx=20, anchor="w", fill="both", expand=True)

    def enviar_consulta(self):
        if self.nombre_usuario.get() and self.contenido_email.get():
            mensaje_alerta("Éxito", "Tu sugerencia ha sido enviada correctamente. ¡Gracias por contactarnos!", tipo='check')
            print("Nombre y Apellido:", self.nombre_usuario.get())
            print("Contenido de la Sugerencia:", self.contenido_email.get())
            self.nombre_usuario.set("")
            self.contenido_email.set("")
        else:
            mensaje_alerta("Error", "Por favor, completa todos los campos antes de enviar tu sugerencia.")
        #self.parent.dirijir_atomaticamente_opcion("inicio")