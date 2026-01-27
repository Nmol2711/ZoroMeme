import customtkinter as ctk
from public.widget.entry import EntryWidget
from utils.config_componen_utils import *
from utils.bind_mouse_wheel import bind_mouse_wheel
from datetime import datetime, timedelta

from services.configuracion_services.configuracion_services import ConfiguracionServices

class HistorialMovimientoScreen(ctk.CTkFrame):
    def __init__(self, master, parent, configu_service: ConfiguracionServices, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = parent
        self.configu_service = configu_service
        
        ctk.CTkLabel(self, 
                     text="Historial de Movimiento", 
                     font=FONT_TITULO_PRINCIPAL, 
                     text_color=COLOR_TEXTO_TITULO,
                     fg_color="transparent",
                     height=TAMANO_TITULO_PRINCIPAL, 
                     justify="left").pack(pady=(20, 0), padx=20, anchor="w")

        self.contenido_historial_movimiento()
        self.cargar_historial_ultimos_siete_dias()

    def contenido_historial_movimiento(self):
        # Frame para los controles de búsqueda
        freme_controles = ctk.CTkFrame(self, fg_color="transparent")
        freme_controles.pack(fill="x", padx=10, pady=10)

        self.entry_buscar = EntryWidget(freme_controles, label_text="Buscar (Fecha o Carpeta)", placeholder_text="Ej. 2024-01-15 o Matemáticas")
        self.entry_buscar.pack(pady=10, padx=10, expand=False, side="left", anchor="nw")

        boton_buscar = ctk.CTkButton(freme_controles, text="Buscar", fg_color=COLOR_BOTON_PRINCIPAL, hover_color=COLOR_BOTON_PRINCIPAL_HOVER, command=self.buscar_historial)
        boton_buscar.pack(pady=(42,10), padx=10, side="left", anchor="nw")

        # Frame para la tabla de resultados
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=COLOR_FONDO_SCREEN_SECUNDARIO, border_width=0)
        self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.scrollable_frame.grid_columnconfigure(0, weight=1) # Columna para fecha
        self.scrollable_frame.grid_columnconfigure(1, weight=4) # Columna para mensaje

    def cargar_historial_ultimos_siete_dias(self):
        hoy = datetime.now()
        hace_siete_dias = hoy - timedelta(days=7)
        fecha_inicio_str = hace_siete_dias.strftime("%Y-%m-%d")
        
        historial = self.configu_service.obtener_archivo_log(fecha_inicio=fecha_inicio_str)
        self.mostrar_datos_en_tabla(historial)

    def buscar_historial(self):
        texto = self.entry_buscar.get().strip()
        if not texto:
            self.cargar_historial_ultimos_siete_dias()
            return

        try:
            # Intentamos buscar por fecha exacta primero
            datetime.strptime(texto, "%Y-%m-%d")
            historial = self.configu_service.obtener_archivo_log(fecha_inicio=texto, fecha_fin=texto)
        except ValueError:
            # Si no es fecha, buscamos por texto (nombre de carpeta, archivo, etc.)
            historial = self.configu_service.obtener_archivo_log(filtro_texto=texto)
        
        self.mostrar_datos_en_tabla(historial)

    def mostrar_datos_en_tabla(self, historial: list):
        # 1. Limpiar resultados anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # 2. Resetear el scroll a la posición inicial
        self.scrollable_frame._parent_canvas.yview_moveto(0)

        # --- CAMBIO CLAVE: Resetear el grid para que no mantenga filas viejas ---
        # Esto elimina cualquier configuración de peso de búsquedas anteriores
        for i in range(101): # MAX_ITEMS + 1
            self.scrollable_frame.grid_rowconfigure(i, weight=0)

        # 3. Encabezados
        ctk.CTkLabel(self.scrollable_frame, text="Fecha y Hora", font=FONT_MENU, text_color=COLOR_TEXTO_TITULO).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ctk.CTkLabel(self.scrollable_frame, text="Operación Realizada", font=FONT_MENU, text_color=COLOR_TEXTO_TITULO).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        if not historial:
            ctk.CTkLabel(self.scrollable_frame, text="No se encontraron registros...", font=FONT_NORMAL).grid(row=1, column=0, columnspan=2, pady=20)
            self.update_idletasks()
            # Forzar el tamaño al mínimo si no hay nada
            self.scrollable_frame._parent_canvas.configure(scrollregion=(0, 0, 0, 0))
            return

        # 4. Renderizado (Igual que antes)
        historial_invertido = historial[::-1]
        MAX_ITEMS = 100 
        datos_a_mostrar = historial_invertido[:MAX_ITEMS]

        for i, linea in enumerate(datos_a_mostrar, start=1):
            fecha_hora = linea[:19] if len(linea) >= 19 else ""
            mensaje = linea[21:] if len(linea) > 21 else linea
            row_color = COLOR_FONDO_INPUT if i % 2 != 0 else "transparent"

            ctk.CTkLabel(self.scrollable_frame, text=fecha_hora, font=FONT_NORMAL, anchor="w", fg_color=row_color).grid(row=i, column=0, sticky="nsew", padx=5, pady=2)
            ctk.CTkLabel(self.scrollable_frame, text=mensaje, font=FONT_NORMAL, anchor="w", justify="left", fg_color=row_color).grid(row=i, column=1, sticky="nsew", padx=5, pady=2)

        # 5. Label de aviso
        ultimo_indice = len(datos_a_mostrar) + 1
        if len(historial) > MAX_ITEMS:
            ctk.CTkLabel(self.scrollable_frame, text=f"... Total: {len(historial)} ...", font=FONT_NORMAL).grid(row=ultimo_indice, column=0, columnspan=2, pady=10)

        # --- LA PARTE MÁS IMPORTANTE PARA LINUX ---
        self.update_idletasks()
        
        # Obtenemos el tamaño real de lo que se acaba de dibujar
        # bbox("all") nos da (x1, y1, x2, y2)
        region = self.scrollable_frame._parent_canvas.bbox("all")
        
        # Obligamos al Canvas a que su área scrolleable sea exactamente ese recuadro
        self.scrollable_frame._parent_canvas.configure(scrollregion=region)
        
        # Aplicamos el bind del mouse
        bind_mouse_wheel(self.scrollable_frame, self.scrollable_frame)