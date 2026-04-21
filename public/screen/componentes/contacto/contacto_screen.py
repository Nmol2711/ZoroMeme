import customtkinter as ctk
import threading
from config.app_config import AppConfig
from public.auth.auth_confg import AuthCofig
from public.widget.mensaje_alerta import mensaje_alerta
from services.email_services.email_services import EmailServices
from utils.config_componen_utils import *
from utils.path_util import *
from public.widget.entry import EntryWidget, EntryAnchoWidget
from utils.bind_mouse_wheel import bind_mouse_wheel
from config.settings import Settings

class ContactoScreen(ctk.CTkFrame):
    def __init__(self, master, parent, auth_config: AuthCofig, services: EmailServices):
        super().__init__(master)
        self.parent = parent
        self.auth_config = auth_config
        self.services = services
        self.contenido()

        # --- Frame de Carga (Oculto inicialmente) ---
        self.frame_loading = ctk.CTkFrame(self, fg_color="transparent")
        self.label_loading = ctk.CTkLabel(self.frame_loading, text="Enviando... (Esto puede tardar unos segundos)", font=FONT_PEQUENO, text_color=COLOR_TEXTO_SUBTITULO)
        self.label_loading.pack(side="left", padx=10)
        self.progress_bar = ctk.CTkProgressBar(self.frame_loading, mode="indeterminate", width=150)
        self.progress_bar.pack(side="left", padx=10)
        self.frame_loading.pack_forget()

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
            # 1. Bloquear UI y mostrar carga
            self.boton_enviar.configure(state="disabled")
            self.frame_loading.pack(pady=(0, 10), padx=20, anchor="e")
            self.progress_bar.start()

            # 2. Iniciar proceso en segundo plano
            threading.Thread(target=self._proceso_envio, daemon=True).start()
        else:
            mensaje_alerta("Error", "Por favor, completa todos los campos antes de enviar tu sugerencia.")

    def _proceso_envio(self):
        """Se ejecuta en un hilo secundario"""
        client = self.auth_config.obtener_cliente_groq()
        if not client:
            # Volver al hilo principal para mostrar error
            self.after(0, lambda: self._finalizar_envio(None, "Error al obtener configuración de IA"))
            return

        exito, mensaje = self.services.enviar_notificacion(
            self.nombre_usuario.get(), 
            self.contenido_email.get(), 
            client
        )
        self.after(0, lambda: self._finalizar_envio(exito, mensaje))

    def _finalizar_envio(self, exito, mensaje):
        """Se ejecuta en el hilo principal para actualizar la UI"""
        self.progress_bar.stop()
        self.frame_loading.pack_forget()
        self.boton_enviar.configure(state="normal")

        if exito is True:
            mensaje_alerta("Éxito", "Mensaje Enviado Correctamente", tipo="check")
            self.nombre_usuario.set("")
            self.contenido_email.set("")
        else:
            # Maneja tanto False como None
            mensaje_alerta("Error", mensaje if mensaje else "Ocurrió un error inesperado")
    