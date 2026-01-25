import customtkinter as ctk
from utils.config_componen_utils import *

class EntryWidget(ctk.CTkFrame):
    def __init__(self, master, label_text: str, placeholder_text: str = "", show: str = None, width: int = 400):
        super().__init__(master, fg_color="transparent")
        self.label_text = label_text
        self.placeholder_text = placeholder_text
        self.show = show
        self.width = width
        self.contenido()

    def contenido(self):
        self.label = ctk.CTkLabel(self, 
                                  text=self.label_text, 
                                  font=FONT_NORMAL, 
                                  text_color=COLOR_TEXTO_SUBTITULO, 
                                  justify="left")
        self.label.pack(pady=(0, 5), padx=20, anchor="w")

        self.entry = ctk.CTkEntry(self, 
                                  placeholder_text=self.placeholder_text, 
                                  font=FONT_NORMAL, 
                                  fg_color=COLOR_FONDO_INPUT, 
                                  text_color=COLOR_TEXTO_INPUT,
                                  show=self.show,
                                  width=self.width)
        self.entry.pack(pady=(0, 10), padx=20, anchor="w")

    def get(self) -> str:
        return self.entry.get()
    
    def set(self, text: str):
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, text)
    

class EntryAnchoWidget(ctk.CTkFrame):
    def __init__(self, master, label_text: str, width: int = 400, height: int = 100):
        super().__init__(master, fg_color="transparent")
        self.label_text = label_text
        self.width = width
        self.height = height
        self.contenido()

    def contenido(self):
        self.label = ctk.CTkLabel(self, 
                                  text=self.label_text, 
                                  font=FONT_NORMAL, 
                                  text_color=COLOR_TEXTO_SUBTITULO, 
                                  justify="left")
        self.label.pack(pady=(0, 5), padx=20, anchor="w")

        self.textbox = ctk.CTkTextbox(self, 
                                      width=self.width, 
                                      height=self.height,
                                      font=FONT_NORMAL, 
                                      fg_color=COLOR_FONDO_INPUT, 
                                      text_color=COLOR_TEXTO_INPUT,
                                      wrap="word")
        self.textbox.pack(pady=(0, 10), padx=20, anchor="w")

    def get(self) -> str:
        return self.textbox.get("1.0", "end-1c")
    
    def set(self, text: str):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
