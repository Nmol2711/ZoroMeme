import customtkinter as ctk
import webbrowser

class CTkHyperlink(ctk.CTkLabel):
    def __init__(self, master, text, url, **kwargs):
        super().__init__(master, text=text, font=("Inter", 12, "underline"), 
                         text_color="#1f538d", cursor="hand2", **kwargs)
        self.url = url
        self.bind("<Button-1>", lambda e: webbrowser.open_new_tab(self.url))