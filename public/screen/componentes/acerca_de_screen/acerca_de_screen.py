import customtkinter as ctk
from config.settings import Settings
from utils.config_componen_utils import *
from public.widget.enlaces import CTkHyperlink
from utils.path_ultil import leer_imagen
from utils.bind_mouse_wheel import bind_mouse_wheel


class AcercaDeScreen(ctk.CTkFrame):
    def __init__(self, master, parent, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = parent

        ctk.CTkLabel(self, 
                     text="Acerca De", 
                     font=FONT_TITULO_PRINCIPAL, 
                     text_color=COLOR_TEXTO_TITULO,
                     fg_color="transparent",
                     height=TAMANO_TITULO_PRINCIPAL, 
                     justify="left").pack(pady=(20, 0), padx=40, anchor="w")
        
        self.contenido()

    def contenido(self):
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Frame principal con layout de grid para separar texto e imagen
        main_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=3)  # Columna de texto (más ancha)
        main_frame.grid_columnconfigure(1, weight=1)  # Columna de imagen

        # --- Frame para el texto a la izquierda ---
        text_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        text_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # --- Frame para la imagen a la derecha ---
        image_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        image_frame.grid(row=0, column=1, sticky="ne", pady=10)

        img_goku = leer_imagen(Settings().ruta_img["goku_chico"], tamano=150)
        ctk.CTkLabel(image_frame, image=img_goku, text="").pack()
        
        # --- Info Principal ---
        ctk.CTkLabel(text_frame, text="ZoroMeme", font=("Roboto", 28, "bold"), text_color=COLOR_TEXTO_TITULO).pack(anchor="w", pady=(10,0))
        ctk.CTkLabel(text_frame, text="Versión 1.0.0 (RC)", font=FONT_NORMAL, text_color=COLOR_TEXTO_SUBTITULO).pack(anchor="w")

        # --- Desarrollador ---
        ctk.CTkLabel(text_frame, text="\nDesarrollado por:", font=FONT_TITULO_SECUNDARIO, text_color=COLOR_TEXTO_TITULO).pack(anchor="w", pady=(20, 5))
        ctk.CTkLabel(text_frame, text="Nelson Molina", font=FONT_NORMAL, text_color=COLOR_TEXTO_NORMAL).pack(anchor="w")
        
        # Contacto
        frame_contacto = ctk.CTkFrame(text_frame, fg_color="transparent")
        frame_contacto.pack(anchor="w", fill="x", pady=(5,0))
        ctk.CTkLabel(frame_contacto, text="Contacto: ", font=FONT_NORMAL, text_color=COLOR_TEXTO_NORMAL).pack(side="left")
        CTkHyperlink(frame_contacto, text="molinacamcho581@gmail.com", url="mailto:molinacamcho581@gmail.com").pack(side="left")

        # --- Descripción ---
        ctk.CTkLabel(text_frame, text="\nDescripción", font=FONT_TITULO_SECUNDARIO, text_color=COLOR_TEXTO_TITULO).pack(anchor="w", pady=(20, 5))
        descripcion_text = """Este software utiliza Inteligencia Artificial para analizar el contenido de tus documentos y organizarlos automáticamente en carpetas temáticas. Olvídate de mover archivos uno por uno.

El organizador es "híbrido", lo que significa que es rápido y eficiente:
  • Busca palabras clave técnicas dentro de tus archivos.
  • Si no está seguro, le pregunta a la IA (Llama 3) para que analice el contexto.
  • Si el archivo ya existe en la carpeta de destino, le añade un número al nombre para no sobrescribir nada."""
        ctk.CTkLabel(text_frame, text=descripcion_text, font=FONT_NORMAL, text_color=COLOR_TEXTO_NORMAL, wraplength=500, justify="left").pack(anchor="w")

        # --- Agradecimientos ---
        ctk.CTkLabel(text_frame, text="\nAgradecimientos", font=FONT_TITULO_SECUNDARIO, text_color=COLOR_TEXTO_TITULO).pack(anchor="w", pady=(20, 5))
        agradecimientos_text = """- A Groq Inc. por proporcionar acceso a su veloz API de inferencia.
- A la comunidad de código abierto por las librerías que hacen posible este proyecto, como CustomTkinter, PyMuPDF y python-docx."""
        ctk.CTkLabel(text_frame, text=agradecimientos_text, font=FONT_NORMAL, text_color=COLOR_TEXTO_NORMAL, wraplength=500, justify="left").pack(anchor="w")

        bind_mouse_wheel(scroll_frame, scroll_frame)