import customtkinter as ctk
from utils.config_componen_utils import *
from public.widget.boton_largo_widget import BotonLargoWidget
from services.configuracion_services.configuracion_services import ConfiguracionServices

REPUESTAJE_PREGUNTAS_FRECUENTES = {
    "Como puedo organizar mis carpetas?": "Para organizar tus carpetas, ve a la sección 'Organizar Carpeta' en el menú lateral. Allí podrás seleccionar la carpeta que deseas organizar y aplicar las reglas de organización configuradas.",
    
    "Como puedo conseguir mi api key?": "Dirijete al sitio ofical de grop, puede encontrar las indicacion en la seccion de 'Configuración' dentro del menú lateral de la aplicación.",
    
    "Como puedo cambiar mi api key?": "Para cambiar tu API Key, dirígete a la sección 'Configuración' en el menú lateral. Allí encontrarás una opción para configurar tu API Key.",
    
    "Como puedo configurar las carpetas donde se va a organizar?": """En la sección 'Configuración', puedes especificar las carpetas que deseas organizar. Añade el nombre de la carpeta en la seccion de configuración de carpetas, y agregale las palabras clave por las cuales se seleccionaran los archivos a mover.""",
    
    "Como crear un prompt para que me ayude a organizar mis carpetas?": """Prompt para la IA
        Actúa como un experto en estructuración de datos. Necesito que analices un listado de carpetas y generes palabras clave técnicas relacionadas con cada una, enfocadas en [Menciona aquí tu área, ej: Medicina Veterinaria y Programación].

        Instrucciones de formato:

        Genera una tabla con dos columnas: "Nombre Carpeta" y "Palabras Clave".

        En la columna de "Palabras Clave", pon al menos 6 términos técnicos por carpeta.

        IMPORTANTE: No uses comillas, ni símbolos especiales. Separa las palabras clave únicamente por comas.

        Entrega el resultado en texto plano (Markdown).

        Lista de carpetas: PEGA AQUI EL NOMBRE DE LAS CARPETAS DE DESTINO""",
    
    "Como puedo consultar el historial de movimientos?": "Puedes consultar el historial de movimientos en la sección 'Historial De Movimiento' del menú lateral. Allí podrás ver un registro detallado de todas las acciones realizadas por el sistema."
}

class AyudaScreen(ctk.CTkFrame):
    def __init__(self, master, parent, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = parent

        ctk.CTkLabel(self, 
                     text="Ayuda Para el Usuario", 
                     font=FONT_TITULO_PRINCIPAL, 
                     text_color=COLOR_TEXTO_TITULO,
                     fg_color="transparent",
                     height=TAMANO_TITULO_PRINCIPAL, 
                     justify="left").pack(pady=(20, 0), padx=20, anchor="w")
        
        self.contenido_ayuda()
    
    def contenido_ayuda(self):
        self.frame_contenido_mostrar = ctk.CTkFrame(self, fg_color="transparent", border_color=BORDE_COLOR, border_width=2,)
        self.frame_contenido_mostrar.pack(expand=True, fill="both", padx=60, pady=60, anchor="center")
        
        # Frame para listar las preguntas (Visible por defecto)
        self.frame_preguntas = ctk.CTkFrame(self.frame_contenido_mostrar, fg_color="transparent")
        self.frame_preguntas.pack(fill="both", expand=True)

        # Frame para mostrar la respuesta (Oculto por defecto)
        self.frame_respuesta = ctk.CTkFrame(self.frame_contenido_mostrar, fg_color="transparent")

        ctk.CTkLabel(self.frame_preguntas, 
                     text="Preguntas Frecuentes", 
                     font=FONT_TITULO_SECUNDARIO, 
                     text_color=COLOR_TEXTO_TITULO,
                     fg_color="transparent",
                     height=TAMANO_TITULO_SECUNDARIO, 
                     justify="left").pack(pady=(20, 0), padx=20, anchor="center")
        
        # Generar botones dinámicamente desde el diccionario para asignarles el comando correcto
        for pregunta in REPUESTAJE_PREGUNTAS_FRECUENTES.keys():
            BotonLargoWidget(self.frame_preguntas, text=pregunta,
                             command=lambda p=pregunta: self.mostrar_respuesta_pregunta(p)).pack(pady=10, padx=20, fill="x")

        self.boton_volver_preguntas = ctk.CTkButton(self.frame_contenido_mostrar, 
                                                text="← Volver a las preguntas frecuentes", 
                                                command=self.volver_preguntas_frecuentes,
                                                fg_color=COLOR_BOTON_PRINCIPAL,  
                                                hover_color=COLOR_BOTON_PRINCIPAL_HOVER)
        
    def volver_preguntas_frecuentes(self):
        self.frame_respuesta.pack_forget()
        self.boton_volver_preguntas.pack_forget()
        self.frame_preguntas.pack(fill="both", expand=True)

    def mostrar_respuesta_pregunta(self, pregunta):
        self.frame_preguntas.pack_forget()
        
        # Primero mostramos el botón de volver al inicio del contenedor para que sea accesible
        self.boton_volver_preguntas.pack(pady=10, padx=20, side="top", anchor="w")

        # Limpiar respuesta anterior
        for widget in self.frame_respuesta.winfo_children():
            widget.destroy()
            
        self.frame_respuesta.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        respuesta = REPUESTAJE_PREGUNTAS_FRECUENTES.get(pregunta, "Respuesta no encontrada")
        
        # Título de la pregunta
        ctk.CTkLabel(self.frame_respuesta, text=pregunta, font=FONT_TITULO_SECUNDARIO, text_color=COLOR_TEXTO_TITULO, wraplength=700, justify="left").pack(pady=(0, 10), anchor="w")

        # Contenido de la respuesta
        textbox = ctk.CTkTextbox(self.frame_respuesta, font=FONT_NORMAL, text_color=COLOR_TEXTO_NORMAL, wrap="word")
        
        if pregunta == "Como crear un prompt para que me ayude a organizar mis carpetas?":
            textbox.configure(fg_color=COLOR_FONDO_INPUT, text_color=COLOR_TEXTO_INPUT)
            # Altura fija para prompts largos pero permitiendo scroll
            textbox.configure(height=350)
        else:
            textbox.configure(fg_color="transparent", height=200)

        textbox.pack(pady=10, fill="both", expand=True)
        textbox.insert("1.0", respuesta)
        textbox.configure(state="disabled")