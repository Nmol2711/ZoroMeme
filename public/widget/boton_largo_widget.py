import customtkinter as ctk
from config.settings import Settings
from utils.config_componen_utils import *
from utils.path_ultil import leer_imagen


class BotonLargoWidget(ctk.CTkFrame):
    def __init__(self, master, text, command=None, width=600, **kwargs):
        super().__init__(master, fg_color="transparent", width=width, **kwargs)
        img = leer_imagen(Settings().ruta_img["flecha"], tamano=20)

        boton_largo = ctk.CTkButton(
            self,
            text=f"  {text}", # Agregamos espacios para separar del borde izquierdo
            command=command,
            fg_color=COLOR_FUNDO_BOTON_LARGO,
            hover_color=COLOR_FUNDO_BOTON_LARGO_HOVER,
            width=width,
            height=40, # Reducimos la altura para que sea más delgado
            corner_radius=10,
            border_color=BORDE_COLOR,
            compound="right",   # <--- ESTO posiciona la imagen a la DERECHA del texto
            anchor="w",         # <--- Alinea el contenido a la izquierda
            **kwargs
        )

        boton_largo.pack(fill="x", expand=True)
        image_frame = ctk.CTkLabel(boton_largo, image=img, text="", fg_color="transparent")
        image_frame.place(relx=0.95, rely=0.5, anchor="center")  # Posiciona la imagen a la derecha del botón
    