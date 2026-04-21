import customtkinter as ctk
from utils.config_componen_utils import *

class BarraProgresoWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Label informativo (Archivo actual)
        self.label_archivo = ctk.CTkLabel(self, text="Esperando...", font=FONT_NORMAL, text_color=COLOR_TEXTO_PROGRESO)
        self.label_archivo.pack(anchor="w", pady=(0, 5))
        
        # Barra de progreso
        self.progressbar = ctk.CTkProgressBar(self, mode="determinate")
        self.progressbar.set(0)
        self.progressbar.pack(fill="x", pady=5)
        
        # Label de porcentaje/conteo
        self.label_conteo = ctk.CTkLabel(self, text="0 / 0", font=FONT_PEQUENO, text_color=COLOR_TEXTO_SUBTITULO)
        self.label_conteo.pack(anchor="e")
        
        # Consola de log (Opcional, se puede mostrar/ocultar)
        self.frame_log = ctk.CTkScrollableFrame(self, height=100, fg_color=COLOR_FONDO_INPUT, corner_radius=5)
        self.frame_log.pack(fill="x", pady=(10, 0))
        
    def actualizar(self, archivo, progreso_val, conteo_texto, mensaje_log=None):
        """Actualiza los elementos de la UI."""
        self.label_archivo.configure(text=f"Analizando: {archivo}")
        self.progressbar.set(progreso_val)
        self.label_conteo.configure(text=conteo_texto)
        
        if mensaje_log:
            log_item = ctk.CTkLabel(self.frame_log, text=mensaje_log, font=FONT_PEQUENO, 
                                    text_color=COLOR_TEXTO_NORMAL, anchor="w", justify="left")
            log_item.pack(fill="x", padx=5)
            # Auto-scroll al final
            self.after(10, lambda: self.frame_log._parent_canvas.yview_moveto(1.0))

    def reset(self):
        self.label_archivo.configure(text="Listo")
        self.progressbar.set(0)
        self.label_conteo.configure(text="0 / 0")
        for widget in self.frame_log.winfo_children():
            widget.destroy()
