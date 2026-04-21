import customtkinter as ctk
from utils.config_componen_utils import *
from utils.bind_mouse_wheel import bind_mouse_wheel


class ResultadoOrganizarCarpetasScreen(ctk.CTkScrollableFrame):
    def __init__(self, master, parent_principal, resultados: dict):
        super().__init__(master, fg_color=COLOR_FONDO_SCREEN_SECUNDARIO)
        self.screen_padre = master  # Referencia directa al componente ScreenOrganizarCarpeta
        self.parent_principal = parent_principal
        self.resultados = resultados
        self.contenido()

    def volver_a_organizar(self):
        # Usar la referencia directa para evitar el problema de Master en CTkScrollableFrame
        self.screen_padre.finalizar_y_volver()

    def contenido(self):
        # --- Título Principal ---
        ctk.CTkLabel(self,
                    text="Resultados de la Organización", 
                    font=FONT_TITULO_PRINCIPAL, 
                    text_color=COLOR_TEXTO_TITULO, 
                    justify="left").pack(pady=20, padx=40, anchor="w")
        
        # --- Frame de Estadísticas ---
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(pady=(0, 20), padx=40, fill="x")
        
        cantidad_analizados = self.resultados.get("archivos_analizados", 0)
        archivos_movidos = self.resultados.get("nombre_archivos_movidos", [])
        cantidad_movidos = len(archivos_movidos)

        ctk.CTkLabel(stats_frame, text=f"Archivos Analizados: {cantidad_analizados}", font=FONT_NORMAL, text_color=COLOR_TEXTO_SUBTITULO).pack(side="left")
        ctk.CTkLabel(stats_frame, text=f"Archivos Movidos: {cantidad_movidos}", font=FONT_NORMAL, text_color=COLOR_TEXTO_POSITIVO).pack(side="left", padx=20)

        # --- Frame de la Tabla ---
        tabla_frame = ctk.CTkFrame(self, fg_color="transparent")
        tabla_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        tabla_frame.grid_columnconfigure(0, weight=3)  # Más espacio para el nombre del archivo
        tabla_frame.grid_columnconfigure(1, weight=1)  # Menos para la categoría

        # --- Encabezados de la Tabla ---
        header_bg = COLOR_FONDO_INPUT
        ctk.CTkLabel(tabla_frame, text="Nombre del Archivo", font=FONT_TITULO_SECUNDARIO, text_color=COLOR_TEXTO_TITULO, fg_color=header_bg, corner_radius=5, height=30).grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=2)
        ctk.CTkLabel(tabla_frame, text="Categoría Destino", font=FONT_TITULO_SECUNDARIO, text_color=COLOR_TEXTO_TITULO, fg_color=header_bg, corner_radius=5, height=30).grid(row=0, column=1, sticky="nsew", padx=(2, 0), pady=2)        
        
        # --- Contenido de la Tabla ---
        if not archivos_movidos:
            ctk.CTkLabel(tabla_frame, text="No se movió ningún archivo.", font=FONT_NORMAL, text_color=COLOR_TEXTO_SUBTITULO).grid(row=1, column=0, columnspan=2, pady=20)
        else:
            for i, (nombre, categoria) in enumerate(archivos_movidos, start=1):
                # Colores de fila alternados para mejor legibilidad
                row_color = COLOR_FONDO_INPUT if i % 2 != 0 else "transparent"
                ctk.CTkLabel(tabla_frame, text=nombre, font=FONT_NORMAL, text_color=COLOR_TEXTO_NORMAL, anchor="w", fg_color=row_color).grid(row=i, column=0, sticky="nsew", padx=(0,2), pady=1)
                ctk.CTkLabel(tabla_frame, text=categoria, font=FONT_NORMAL, text_color=COLOR_TEXTO_NORMAL, anchor="w", fg_color=row_color).grid(row=i, column=1, sticky="nsew", padx=(2,0), pady=1)

        # --- Botón para volver ---
        boton_volver = ctk.CTkButton(self, text="Finalizar", command=self.volver_a_organizar, 
                                     fg_color=COLOR_BOTON_GOKU, 
                                     hover_color=COLOR_BOTON_GOKU_HOVER, 
                                     height=40, 
                                     width=120,
                                     )
        boton_volver.pack(pady=20, padx=40, anchor="e")

        # Aplicar scroll para Linux de forma recursiva a todos los widgets internos
        bind_mouse_wheel(self, self)