import customtkinter as ctk
from config.app_config import AppConfig
from public.auth.auth_confg import AuthCofig
from utils.config_componen_utils import *
from utils.path_ultil import *
from config.settings import Settings

class ScreenBase(ctk.CTkFrame):
    def __init__(self, master, auth_config: AuthCofig, services):
        super().__init__(master)
        self.auth_config = auth_config
        self.services = services
        self.opcion_actual = None

        self.update_idletasks()  # Asegúrate de que el frame esté renderizado
        
        # Configurar el layout con grid
        self.grid_columnconfigure(1, weight=1) # Columna para el cuerpo principal se expande
        self.grid_rowconfigure(1, weight=1)    # Fila para el cuerpo principal y sidebar se expande

        self.barra_superior()

        self.menu_lateral()

        self.cuerpo_principal = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SCREEN_PRINCIPAL)
        # Usamos grid en lugar de pack
        self.cuerpo_principal.grid(row=1, column=1, sticky="nsew")
        
    def barra_superior(self):

        icon_menu = leer_imagen(Settings().ruta_img["menu"], tamano=40)

        frameTopbar = ctk.CTkFrame(self, fg_color=COLOR_AZUL_PRINCIPAL, height=30, corner_radius=0)
        frameTopbar.grid(row=0, column=0, columnspan=2, sticky="ew")

        barra = ctk.CTkFrame(frameTopbar, fg_color="transparent", height=40)
        barra.pack(side="bottom", fill="x")

        titulo = ctk.CTkLabel( barra, text=" Dashboard Del Sistema", compound="left", font=("Roboto",18), text_color="white")
        titulo.pack(side=ctk.LEFT, padx=10)
        
        boton = ctk.CTkButton(barra, text="", image=icon_menu, width=32, fg_color="transparent", hover_color="white", command=self.ajustar_menu_lateral)
        boton.pack(side=ctk.LEFT, padx=15)

    def menu_lateral(self):
        self.menu_lateral = ctk.CTkFrame(self, fg_color=COLOR_FONDO_MENU_LATERAL)
        self.menu_lateral.grid(row=1, column=0, sticky="ns")
        
        opciones = [
            ("Inicio", self.inicio),
            ("Organizar Carpeta", self.organizar_carpeta),
            ("Historial De Movimiento", self.historial_movimiento),
            ("Configuración", self.configurar),
            ("Ayuda", self.mostrar_ayuda),
            ("Acerca De", self.acerca_de),
            ("Salir", self.salir)
        ]

        for opcion in opciones:
            esfera = leer_imagen(Settings().ruta_img["esfera1"],40)
            boton = ctk.CTkButton(self.menu_lateral, 
                                  text=opcion[0], 
                                  font=("Roboto", 18),
                                  image=esfera, 
                                  fg_color=COLOR_FONDO_MENU_LATERAL, 
                                  hover_color=COLOR_FONDO_SCREEN_PRINCIPAL, 
                                  text_color="white", 
                                  anchor="w",
                                  command=opcion[1]
                                  )
            
            boton.pack(fill="x", pady=10, padx=10)

    def ajustar_menu_lateral(self):
        """Alterna la visibilidad del sidebar"""
        if not hasattr(self, 'menu_lateral'):
            return

        if self.menu_lateral.winfo_ismapped():
            # Ocultar el sidebar
            self.menu_lateral.grid_forget()
        else:
            # Mostrar el sidebar
            self.menu_lateral.grid(row=1, column=0, sticky="ns")
            #self._ajustar_ancho_menu_lateral()
    
    def dirijir_atomaticamente_opcion(self, opcion):
        if self.opcion_actual == opcion:
            return
            
        if opcion == "inicio":
            self.inicio()
        elif opcion == "organizar_carpeta":
            self.organizar_carpeta()
        elif opcion == "historial_movimiento":
            self.historial_movimiento()
        elif opcion == "configurar":
            self.configurar()
        elif opcion == "ayuda":
            self.mostrar_ayuda()
        elif opcion == "salir":
            self.salir()


    def inicio(self):pass
    def organizar_carpeta(self):pass
    def historial_movimiento(self):pass
    def configurar(self):pass
    def mostrar_ayuda(self):pass
    def acerca_de(self):pass

    def salir(self):
        self.master.destroy()