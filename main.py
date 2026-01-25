from public.main_window import MainWindow
from config.app_config import AppConfig
import customtkinter as ctk

def main():
    color_thema = AppConfig().color_tema
    ctk.set_default_color_theme(color_thema)
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()