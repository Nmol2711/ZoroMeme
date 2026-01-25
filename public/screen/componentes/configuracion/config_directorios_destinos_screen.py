import customtkinter as ctk
from services.configuracion_services.configuracion_services import ConfiguracionServices
from utils.config_componen_utils import *
from public.widget.entry import EntryWidget, EntryAnchoWidget
from utils.path_ultil import *
from public.widget.mensaje_alerta import mensaje_alerta

class ConfigDirectoriosDestinosScreen(ctk.CTkFrame):
    def __init__(self, master, parent_principal, config_services: ConfiguracionServices):
        super().__init__(master)
        self.parent_principal = parent_principal
        self.config_services = config_services
        self.listado_directorios = []
        ctk.CTkLabel(self, text="Configuración de Directorios Destinos: Agregue la el nombre de la carpeta\n y la palabra clave asociada que sean extremadamente únicas para cada directorio.", font=FONT_NORMAL, text_color=COLOR_TEXTO_NORMAL, justify="left").pack( padx=20, anchor="w")

        self.boton_agregar_directorio = ctk.CTkButton(self,
                                            text="  Agregar  ", 
                                            fg_color=COLOR_BOTON_PRINCIPAL, 
                                            hover_color=COLOR_BOTON_PRINCIPAL_HOVER,
                                            command=self.agrega_directorio)
        self.boton_agregar_directorio.pack(anchor="e", padx=40)
        self.contenido()
        
        # Cargar los datos guardados al iniciar la pantalla
        self.cargar_datos_existentes()

        self.boton_volver = ctk.CTkButton(self,
                                            text="volver", 
                                            fg_color=COLOR_BOTON_PRINCIPAL, 
                                            hover_color=COLOR_BOTON_PRINCIPAL_HOVER,
                                            command=self.volver)
        self.boton_volver.pack(pady=20, padx=20, side="left", anchor="w")

        self.boton_guardar = ctk.CTkButton(self,
                                            text="Guardar Configuración", 
                                            fg_color=COLOR_BOTON_PRINCIPAL, 
                                            hover_color=COLOR_BOTON_PRINCIPAL_HOVER,
                                            command=self.extraer_directorio)
        self.boton_guardar.pack(pady=20, padx=20, side="right", anchor="e")
        

    def contenido(self):
        frame_contenido = ctk.CTkFrame(self, fg_color="transparent")
        frame_contenido.pack(expand=True, fill="both", anchor = "w")

        self.frame_contenido_mostrar = ctk.CTkScrollableFrame(frame_contenido, fg_color=COLOR_FONDO_SCREEN_SECUNDARIO, border_color=BORDE_COLOR, border_width=2,)
        self.frame_contenido_mostrar.pack(expand=True, fill="both", padx=60, pady=40)

        # Aquí iría la lógica para mostrar y configurar los directorios destinos
        ctk.CTkLabel(self.frame_contenido_mostrar, text="Aquí puedes configurar los directorios destinos basados en palabras clave.", font=FONT_NORMAL, text_color=COLOR_TEXTO_SUBTITULO, justify="left").pack(pady=20, padx=20, anchor="w")
        # Por ejemplo, una lista de reglas actuales
        
    def cargar_datos_existentes(self):
        datos = self.config_services.obtener_diccionario_palabras()
        # Verificamos que existan datos y sea un diccionario válido
        if datos and isinstance(datos, dict):
            for nombre_carpeta, lista_palabras in datos.items():
                # Reutilizamos la función agrega_directorio pasándole los valores
                self.agrega_directorio(nombre_existente=nombre_carpeta, palabras_existentes=lista_palabras)
        
    def agrega_directorio(self, nombre_existente=None, palabras_existentes=None):
        freme_agregar = ctk.CTkFrame(self.frame_contenido_mostrar, fg_color = "transparent")
        freme_agregar.pack(pady=10, padx=20, fill="x")
        entry_nombre_directorio = EntryWidget(freme_agregar, "Nombre directorio","Ej. Matemáticas", width=200)
        entry_nombre_directorio.pack(side="left", padx=10, anchor="n")
        
        if nombre_existente:
            entry_nombre_directorio.set(nombre_existente)
        
        # Usamos EntryAnchoWidget: width=200 (angosto para caber) y height=100 (largo hacia abajo)
        entry_palabra_clave = EntryAnchoWidget(freme_agregar, label_text="Palabras clave", width=200, height=100)
        entry_palabra_clave.pack(side="left", padx=10, anchor="n")
        
        if palabras_existentes:
            # Convertimos la lista ["a", "b"] a un string "a\nb" para que se vea bien en el textbox
            texto_palabras = "\n".join(palabras_existentes)
            entry_palabra_clave.set(texto_palabras)
        
        self.listado_directorios.append(freme_agregar)

        def eliminar_directorio():
            freme_agregar.destroy()
            self.listado_directorios.remove(freme_agregar)

        boton_eliminar = ctk.CTkButton(freme_agregar,
                                        text="Eliminar", 
                                        fg_color=COLOR_BOTON_GOKU, 
                                        hover_color=COLOR_BOTON_GOKU_HOVER,
                                        command=eliminar_directorio)
        boton_eliminar.pack(side="right", padx=10, anchor="n")


    
    def extraer_directorio(self):
        directorio_guardar = {}
        if not self.listado_directorios:
            mensaje_alerta("Advertencia", "No hay directorios para guardar. Por favor, agregue al menos uno.")
            return
        for frame in self.listado_directorios:
            entradas = frame.winfo_children()
            nombre_directorio = entradas[0].get().strip()
            palabras_clave = entradas[1].textbox.get("1.0", ctk.END).strip().splitlines()
            palabras_clave = [palabra for palabra in palabras_clave if palabra]  # Eliminar líneas vacías
            if nombre_directorio and palabras_clave:
                directorio_guardar[nombre_directorio] = palabras_clave
        self.guardar_directorios(directorio_guardar)
        
    def guardar_directorios(self, directorio_guardar: dict[str, list[str]]):

        exito = self.config_services.guardar_diccionario_palabras(directorio_guardar)
        if exito:
            mensaje_alerta("Éxito", "Los directorios y palabras clave se han guardado correctamente.",tipo="check")
        else:
            mensaje_alerta("Error", "Hubo un problema al guardar la configuración. Por favor, inténtelo de nuevo.")
    
    def volver(self):
        self.parent_principal.opcion_actual = None
        self.retonar_configuracion_screen()

    def retonar_configuracion_screen(self):
        # Forzamos la recarga reseteando la opción actual para que el sistema no crea que ya estamos ahí
        self.parent_principal.dirijir_atomaticamente_opcion("configurar")

        
    