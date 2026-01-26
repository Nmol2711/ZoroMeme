import sys
import os
from public.main_window import MainWindow
from config.app_config import AppConfig
import warnings
import customtkinter as ctk
from utils.path_ultil import resource_path

def main():
    # Ignorar advertencias de 'Conditional Formatting' de openpyxl para una salida más limpia
    warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')

    color_thema = resource_path(AppConfig().color_tema)
    ctk.set_default_color_theme(color_thema)
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()