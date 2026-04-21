import customtkinter as ctk
from services.areas_ocupacionales.areas_services import AreasServices
from utils.config_componen_utils import *
from public.widget.mensaje_alerta import mensaje_alerta

class OnboardingScreen(ctk.CTkFrame):
    def __init__(self, master, parent, auth_config, services):
        super().__init__(master, fg_color=COLOR_FONDO_SCREEN_PRINCIPAL)
        self.master = master
        self.parent = parent
        self.auth_config = auth_config
        self.areas_services = AreasServices(services["configuracion_services"])
        self.selected_area = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.contenido()

    def contenido(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=40, pady=(40, 20))
        
        ctk.CTkLabel(header, text="Personaliza tu organizador", font=FONT_TITULO_PRINCIPAL, text_color=COLOR_TEXTO_TITULO).pack(anchor="w")
        ctk.CTkLabel(header, text="Selecciona tu área ocupacional para configurar carpetas inteligentes automáticas.", 
                     font=FONT_NORMAL, text_color=COLOR_TEXTO_SUBTITULO).pack(anchor="w", pady=(5, 0))

        # Grid de Áreas
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=30)
        
        # Configurar grid de 3 columnas para las tarjetas
        for i in range(3):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

        areas = self.areas_services.obtener_areas_predefinidas()
        self.cards = {}
        
        row, col = 0, 0
        for nombre, data in areas.items():
            card = self.crear_tarjeta_area(nombre, data["icon"], row, col)
            self.cards[nombre] = card
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Tarjeta Especial: Mi área no está aquí
        card_custom = self.crear_tarjeta_area("Mi área no está aquí 🔍", "", row, col, is_custom=True)
        self.cards["custom"] = card_custom

        # Footer con botón continuar
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=40, pady=30)
        
        self.btn_confirmar = ctk.CTkButton(footer, text="Confirmar y Empezar", 
                                           fg_color=COLOR_BOTON_PRINCIPAL, 
                                           hover_color=COLOR_BOTON_PRINCIPAL_HOVER,
                                           height=45, width=200, font=FONT_MENU,
                                           command=self.confirmar_seleccion,
                                           state="disabled")
        self.btn_confirmar.pack(side="right")
        
        self.btn_omitir = ctk.CTkButton(footer, text="Configurar manualmente", 
                                         fg_color="transparent", 
                                         hover_color=COLOR_FONDO_SCREEN_SECUNDARIO,
                                         height=45, font=FONT_NORMAL,
                                         command=self.finalizar)
        self.btn_omitir.pack(side="right", padx=20)

        # Frame para entrada personalizada (oculto por defecto)
        self.custom_input_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLOR_FONDO_SCREEN_SECUNDARIO, corner_radius=10)
        self.entry_custom = ctk.CTkEntry(self.custom_input_frame, placeholder_text="Describe tu trabajo (ej: Fotógrafo de bodas, Carpintero, Chef...)", 
                                         height=40, font=FONT_NORMAL)
        self.entry_custom.pack(fill="x", padx=20, pady=20)

    def crear_tarjeta_area(self, nombre, icono, row, col, is_custom=False):
        card = ctk.CTkFrame(self.scroll_frame, fg_color=COLOR_CATEGORIA_CARD, corner_radius=12, cursor="hand2")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Click event
        card.bind("<Button-1>", lambda e, n=nombre: self.seleccionar_area(n))
        
        label_icon = ctk.CTkLabel(card, text=icono, font=(FUENTE_BASE, 40))
        label_icon.pack(pady=(20, 5))
        label_icon.bind("<Button-1>", lambda e, n=nombre: self.seleccionar_area(n))
        
        label_name = ctk.CTkLabel(card, text=nombre, font=FONT_MENU, text_color=COLOR_TEXTO_TITULO, wraplength=180)
        label_name.pack(pady=(0, 20), padx=10)
        label_name.bind("<Button-1>", lambda e, n=nombre: self.seleccionar_area(n))
        
        return card

    def seleccionar_area(self, nombre):
        self.selected_area = nombre
        self.btn_confirmar.configure(state="normal")
        
        # Actualizar UI visual de selección
        for name, card in self.cards.items():
            if name == ("custom" if nombre == "Mi área no está aquí 🔍" else nombre):
                card.configure(fg_color=COLOR_CATEGORIA_CARD_SELECTED, border_width=2, border_color="white")
            else:
                card.configure(fg_color=COLOR_CATEGORIA_CARD, border_width=0)

        if nombre == "Mi área no está aquí 🔍":
            # Mostrar campo de texto
            self.custom_input_frame.grid(row=99, column=0, columnspan=3, sticky="ew", pady=20, padx=10)
            # Hacer scroll hacia abajo después de un breve delay para asegurar que el widget se ha renderizado
            self.after(50, lambda: self.scroll_frame._parent_canvas.yview_moveto(1.0))
        else:
            self.custom_input_frame.grid_forget()

    def confirmar_seleccion(self):
        if not self.selected_area:
            return

        diccionario_final = {}
        
        if self.selected_area == "Mi área no está aquí 🔍":
            descripcion = self.entry_custom.get().strip()
            if not descripcion:
                mensaje_alerta("Aviso", "Por favor describe tu trabajo o elige una opción predefinida.")
                return
            
            # Mostrar cargando
            self.btn_confirmar.configure(text="Generando carpetas con IA...", state="disabled")
            self.update()
            
            # Esto debería ser asíncrono para no congelar la UI, pero para simplificar lo hacemos así
            # con un pequeño delay visual
            diccionario_final = self.areas_services.generar_carpetas_con_ia(descripcion, self.auth_config.obtener_cliente_groq())
        else:
            diccionario_final = self.areas_services.obtener_diccionario_por_area(self.selected_area)

        # Guardar y finalizar
        self.areas_services.guardar_seleccion(diccionario_final)
        mensaje_alerta("Éxito", f"¡Configurado! Se han creado las reglas para tu perfil de {self.selected_area if self.selected_area != 'Mi área no está aquí 🔍' else 'Especialista'}.", tipo="check")
        self.finalizar()

    def finalizar(self):
        self.master.mostrar_vista_principal()
