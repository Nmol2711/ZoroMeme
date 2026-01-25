import customtkinter as ctk 
import threading
from public.auth.auth_confg import AuthCofig
from public.screen.componentes.organizar_carpeta.resultado_organizar_carpetas_screen import ResultadoOrganizarCarpetasScreen
from public.widget.arrastrar_soltar import ArrastrarSoltar
from services.organizador_documentos.organizador_documentos import OrganizarDocumentosServices
from utils.config_componen_utils import *
from utils.path_ultil import *
from public.widget.mensaje_alerta import mensaje_alerta


class ScreenOrganizarCarpeta(ctk.CTkFrame):
    def __init__(self, master, parent, auth_config : AuthCofig, services : OrganizarDocumentosServices):
        super().__init__(master)
        self.parent = parent
        self.auth_config = auth_config
        self.services = services
        self.ruta_carpeta = None

        self.contenido()

    def contenido(self):
        try:
            frame_titulo = ctk.CTkFrame(self, fg_color="transparent")
            frame_titulo.pack(expand=False, fill="x")

            ctk.CTkLabel(frame_titulo,
                        text="Organizador de carpetas", 
                        font=FONT_TITULO_PRINCIPAL, 
                        text_color=COLOR_TEXTO_TITULO, 
                        height=TAMANO_TITULO_PRINCIPAL, 
                        justify="left").pack(pady=20, padx=20, anchor="w")
            
            ctk.CTkLabel(frame_titulo,
                        text="Arastre la carpeta que desea Analizar o seleconela cen el boton Examinar", 
                        font=FONT_NORMAL, 
                        text_color=COLOR_TEXTO_SUBTITULO, 
                        justify="left").pack(padx=20, anchor="w")
                        
            self.boton_examinar = ctk.CTkButton(self, text="Examinar", command=self.examinar_ruta, 
                                            fg_color=COLOR_BOTON_GOKU, 
                                            hover_color=COLOR_BOTON_GOKU_HOVER, 
                                            height=40, 
                                            width=120,
                                            )
            self.boton_examinar.pack(anchor="e", padx=40)
            

            self.frame_arrastrar_soltar = ctk.CTkFrame(self, width=20, height=20, border_width=2, border_color="#0078D4")
            self.frame_arrastrar_soltar.pack(pady=20, padx=40, expand=False, fill="x")

            # --- Frame para progreso ---
            self.frame_progreso = ctk.CTkFrame(self, fg_color="transparent")
            self.frame_progreso.pack(pady=10, padx=40, fill="x")

            self.label_progreso = ctk.CTkLabel(self.frame_progreso, text="", font=FONT_NORMAL)
            self.label_progreso.pack(anchor="w")

            self.progressbar = ctk.CTkProgressBar(self.frame_progreso, mode='indeterminate')
            self.progressbar.pack(fill="x", pady=5)
            self.frame_progreso.pack_forget() # Ocultar al inicio

            #TODO: Esto solo va a funcionar en windows, hay que buscar una solucion para linux y macOS
            self.widget_arrastrar_soltar = ArrastrarSoltar(self.frame_arrastrar_soltar, self.guardar_ruta)
            self.widget_arrastrar_soltar.pack(fill="x")

            frame_inferior = ctk.CTkFrame(self, fg_color="transparent")
            frame_inferior.pack(expand=False, fill="x")

            frame_inferior_izquierda = ctk.CTkFrame(frame_inferior, fg_color="transparent")
            frame_inferior_izquierda.pack(pady=20, padx=20, anchor="w", side="left")

            frame_inferior_derecha = ctk.CTkFrame(frame_inferior, fg_color="transparent")
            frame_inferior_derecha.pack(pady=20, padx=40, anchor="w", side="right")

            

            self.label_ruta_seleccionada = ctk.CTkLabel(frame_inferior_izquierda, text="NO HAY RUTA SELECCIONADA", 
                                                        font=FONT_PEQUENO, 
                                                        text_color=COLOR_TEXTO_NEGATIVO,
                                                        justify="left",

                                                        )
            
            self.label_ruta_seleccionada.pack(pady=20, padx=20, anchor="w", side="left")

            self.boton_eliminar_ruta = ctk.CTkButton(frame_inferior_izquierda, 
                                                text="Eliminar", 
                                                fg_color=COLOR_BOTON_GOKU, 
                                                hover_color=COLOR_BOTON_GOKU_HOVER, 
                                                height=40, 
                                                width=120,
                                                command=self.eliminar_ruta,
                                                state="disabled"
                                            )
            
            self.boton_eliminar_ruta.pack(pady=20, padx=20, anchor="w", side="left")  


            self.boton_continuar = ctk.CTkButton(frame_inferior_derecha, 
                                                text="Comenzar", 
                                                fg_color=COLOR_BOTON_PRINCIPAL, 
                                                hover_color=COLOR_BOTON_PRINCIPAL_HOVER, 
                                                height=40, 
                                                width=120,
                                                command=self.continuar,
                                                state="disabled"
                                            )
            
            self.boton_continuar.pack(pady=20, padx=40, anchor="w", side="right")

        except Exception as e:
            print(f"Error en contenido: {e}")
    
    def guardar_ruta(self, ruta_carpeta = None):
        self.ruta_carpeta = ruta_carpeta
        if ruta_carpeta:
            self.label_ruta_seleccionada.configure(text=f"Ruta seleccionada:\n{self.ruta_carpeta}", text_color=COLOR_TEXTO_POSITIVO)
            self.boton_eliminar_ruta.configure(state="normal")
            self.boton_examinar.configure(state="disabled")
            self.widget_arrastrar_soltar.desabilitar()
            self.boton_continuar.configure(state="normal")
    
    def continuar(self):
        if self.ruta_carpeta:
            # Deshabilitar botones y mostrar progreso
            self.boton_continuar.configure(state="disabled")
            self.boton_examinar.configure(state="disabled")
            self.boton_eliminar_ruta.configure(state="disabled")
            
            self.label_progreso.configure(text="Organizando archivos, por favor espere...")
            self.frame_progreso.pack(pady=10, padx=40, fill="x") # Mostrar el frame de progreso
            self.progressbar.start()

            # Crear y empezar el hilo para no congelar la UI
            thread = threading.Thread(target=self.proceso_organizar)
            thread.start()

    def proceso_organizar(self):
        # Esta es la función que se ejecuta en el hilo secundario
        informe = self.services.organizar_hibrido(
            self.ruta_carpeta, 
            self.auth_config.obtener_cliente_groq(), 
            self.services.archivo_log
        )
        # Cuando el hilo termina, programamos la actualización de la UI en el hilo principal
        self.after(0, self.finalizar_proceso, informe)

    def finalizar_proceso(self, informe):
        # Detener y ocultar la barra de progreso
        self.progressbar.stop()
        self.frame_progreso.pack_forget()

        # Mostrar resultado
        if informe:
            self.mostrar_resultado(informe)
        else:
            mensaje_alerta("Error", "Ocurrió un error durante la organización. Revisa los logs para más detalles.")
            # Si hubo un error, reseteamos la UI para que el usuario pueda intentarlo de nuevo.
            self.eliminar_ruta()

    def examinar_ruta(self):
        ruta = seleccionar_carpeta()
        if ruta:
            self.ruta_carpeta = ruta
            self.label_ruta_seleccionada.configure(text=f"Ruta seleccionada:\n{self.ruta_carpeta}",text_color=COLOR_TEXTO_POSITIVO)
            self.boton_eliminar_ruta.configure(state="normal")
            self.boton_examinar.configure(state="disabled")
            self.widget_arrastrar_soltar.desabilitar()
            self.boton_continuar.configure(state="normal")
            self
        else:
            print("No se seleccionó ninguna carpeta")
    
    def eliminar_ruta(self):
        self.ruta_carpeta = None
        self.label_ruta_seleccionada.configure(text="NO HAY RUTA SELECCIONADA", text_color=COLOR_TEXTO_NEGATIVO)
        self.boton_eliminar_ruta.configure(state="disabled")
        self.boton_examinar.configure(state="normal")
        self.widget_arrastrar_soltar.habilitar()
        self.boton_continuar.configure(state="disabled")

    def mostrar_resultado(self, resultados: dict):
        # Limpiar el cuerpo principal
        for widget in self.winfo_children():
            widget.destroy()

        ResultadoOrganizarCarpetasScreen(self, self.parent, resultados).pack(fill="both", expand=True)