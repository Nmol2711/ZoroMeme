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

        # Opciones del sistema:
        self.opciones = [
            ("Inicio", self.inicio),
            ("Organizar Carpeta", self.organizar_carpeta),
            ("Historial De Movimiento", self.historial_movimiento),
            ("Configuración", self.configurar),
            ("Ayuda", self.mostrar_ayuda),
            ("Acerca De", self.acerca_de),
            ("Salir", self.salir)
        ]

        self.update_idletasks()  # Asegúrate de que el frame esté renderizado
        
        # Configurar el layout con grid
        self.grid_columnconfigure(1, weight=1) # Columna para el cuerpo principal se expande
        self.grid_rowconfigure(1, weight=1)    # Fila para el cuerpo principal y sidebar se expande
        evaluar_tamano = AppConfig()
        evaluar_tamano.evaluar_tamano_pantalla(self.winfo_screenwidth(), self.winfo_screenheight())
        if not evaluar_tamano.categoria == "medio" and not evaluar_tamano.categoria == "pequeno":
            self.barra_superior()
            self.menu_lateral()
        else:
            self.menu_superior()

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

        for opcion in self.opciones:
            esfera = leer_imagen(Settings().ruta_img["esfera1"],40)
            boton = ctk.CTkButton(self.menu_lateral, 
                                  text=opcion[0], 
                                  font=FONT_MENU,
                                  image=esfera, 
                                  fg_color=COLOR_FONDO_MENU_LATERAL, 
                                  hover_color=COLOR_FONDO_SCREEN_PRINCIPAL, 
                                  text_color="white", 
                                  anchor="w",
                                  command=opcion[1]
                                  )
            
            boton.pack(fill="x", pady=10, padx=10)

    # este menu se va a ejecutar solo si la ventana es muy pequeña
    def menu_superior(self):
        frameTopbar = ctk.CTkFrame(self, fg_color=COLOR_AZUL_PRINCIPAL, height=60, corner_radius=0)
        frameTopbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        frameTopbar.grid_propagate(False) # Mantiene la altura fija para evitar deformaciones

        # Título a la izquierda
        titulo = ctk.CTkLabel(frameTopbar, text=" Dashboard Del Sistema", font=("Roboto", 18, "bold"), text_color="white")
        titulo.pack(side="left", padx=20)

        # Usamos un ScrollableFrame horizontal para los botones.
        # Esto asegura que si la ventana es pequeña, los botones no se corten y se pueda navegar.
        botones_frame = ctk.CTkScrollableFrame(frameTopbar, orientation="horizontal", fg_color=COLOR_AZUL_PRINCIPAL, height=40)
        botones_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        for opcion in self.opciones:
            boton = ctk.CTkButton(botones_frame, 
                                  text=opcion[0], 
                                  font=FONT_MENU,
                                  fg_color="transparent", 
                                  hover_color=COLOR_FONDO_SCREEN_PRINCIPAL, 
                                  text_color="white", 
                                  anchor="center",
                                  width=0, # Ancho dinámico: se ajusta al tamaño del texto
                                  height=35,
                                  command=opcion[1]
                                  )
            
            boton.pack(side="left", padx=5)


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