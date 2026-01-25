import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from typing import Literal

def mensaje_alerta(titulo, mensaje, tipo: Literal["info", "warning", "check"] = "warning", accion = None):
    # Se crea la instancia del messagebox.
    msg = CTkMessagebox(title=titulo, message=mensaje, icon=tipo)
    msg.overrideredirect(True)
    
    # Función recursiva para desvincular eventos de movimiento
    def bloquear_movimiento(widget):
        if isinstance(widget, ctk.CTkButton):
            return
        try:
            widget.unbind("<B1-Motion>")
            widget.unbind("<Button-1>")
        except Exception: pass
        for child in widget.winfo_children():
            bloquear_movimiento(child)
    
    bloquear_movimiento(msg)

    # El método .get() muestra la ventana, espera a que el usuario presione un botón
    # y devuelve el texto de ese botón (ej: "OK"). Es una llamada "bloqueante".
    # La ejecución del código se detiene aquí hasta que se cierra el messagebox.
    msg.get()

    # Una vez que el usuario ha presionado "OK", el código continúa y se ejecuta la acción.
    if accion:
        accion()