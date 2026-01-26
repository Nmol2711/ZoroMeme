from public.main_window import MainWindow
from config.app_config import AppConfig
import customtkinter as ctk
from utils.path_ultil import resource_path

def main():
    color_thema = resource_path(AppConfig().color_tema)
    ctk.set_default_color_theme(color_thema)
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()