#OJO esto solo funcionara para windows

import customtkinter as ctk
from tkinterdnd2 import DND_FILES

class ArrastrarSoltar(ctk.CTkFrame):
    def __init__(self, master, ruta_carpeta, **kwargs):
        super().__init__(master, width=400, height=250, border_width=2, border_color="#0078D4", **kwargs)
        self.habilitado = True
        self.contenido()
        self.ruta_carpeta = ruta_carpeta
    
    def contenido(self):
        self.label = ctk.CTkLabel(self, text="📁 Arrastra tu carpeta aquí")
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        
        try:
            # Registramos el widget como destino de archivos
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self.procesar_ruta)
        except Exception as e:
            print(f"Error al configurar D&D: {e}")
            self.label.configure(text="Error: Main no soporta D&D", text_color="red")

    def procesar_ruta(self, event):
        try:
            if not self.habilitado:
                return

            # tkinterdnd2 devuelve la ruta en event.data
            # Si la ruta tiene espacios, Windows la envuelve en corchetes {}
            ruta_seleccionada = event.data
            if ruta_seleccionada.startswith('{') and ruta_seleccionada.endswith('}'):
                ruta_seleccionada = ruta_seleccionada[1:-1]
            
            print(f"Carpeta recibida: {ruta_seleccionada}")
            self.label.configure(text=f"Seleccionado:\n{ruta_seleccionada}", text_color="#2ECC71")
            self.ruta_carpeta(ruta_seleccionada)
        except Exception as e:
            print(f"Error al procesar la ruta: {e}")
            self.label.configure(text="Error al procesar la ruta", text_color="red")
    
    def desabilitar(self):
        self.habilitado = False
        self.configure(border_color="gray")
        self.label.configure(text="🚫 Deshabilitado", text_color="gray")
    
    def habilitar(self):
        self.habilitado = True
        self.configure(border_color="#0078D4")
        self.label.configure(text="📁 Arrastra tu carpeta aquí")


    