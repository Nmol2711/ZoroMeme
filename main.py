import sys
import os
import warnings
import customtkinter as ctk
from public.main_window import MainWindow
from config.app_config import AppConfig
from utils.path_util import resource_path
from utils.logging_config import setup_logging

def main():
    # Configurar logging al inicio
    # Usar una ruta de log basada en el directorio del usuario si es posible
    log_file = os.path.join(os.path.expanduser("~"), ".zoromeme", "app.log")
    setup_logging(log_file)

    # Ignorar advertencias de 'Conditional Formatting' de openpyxl para una salida más limpia
    warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')

    color_thema = resource_path(AppConfig().color_tema)
    ctk.set_default_color_theme(color_thema)
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()