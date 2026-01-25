import os
from utils.path_ultil import resource_path


class AppConfig:
    def __init__(self):
        self.tema = "dark"
        # Usar resource_path para compatibilidad con PyInstaller
        self.color_tema = resource_path(os.path.join('config', 'dark_blue.json'))
        self.titulo_ventana = "Sistema Organizador de Docuementos"
        self.icono = resource_path(os.path.join('resources', 'logo.ico'))
        # Tamaños recomendados de ventana para cada rango de pantalla
        self.tamano_ventana = {
            "pantalla_super_grande": (1200, 800),
            "pantalla_grande": (1100, 700),
            "pantalla_medio": (900, 650),
            "pantalla_pequeno": (800, 600),
            "pantalla_muy_pequeno": (700, 500),
            "pantalla_muy_muy_pequeno": (600, 400),
            "pantalla_muy_muy_muy_pequeno": (480, 320)
        }

    def evaluar_tamano_pantalla(self, ancho, alto):
        if ancho >= 1920 and alto >= 1080:
            return f"{self.tamano_ventana['pantalla_super_grande'][0]}x{self.tamano_ventana['pantalla_super_grande'][1]}"
        elif ancho >= 1600 and alto >= 900:
            return f"{self.tamano_ventana['pantalla_grande'][0]}x{self.tamano_ventana['pantalla_grande'][1]}"
        elif ancho >= 1366 and alto >= 768:
            return f"{self.tamano_ventana['pantalla_medio'][0]}x{self.tamano_ventana['pantalla_medio'][1]}"
        elif ancho >= 1280 and alto >= 720:
            return f"{self.tamano_ventana['pantalla_pequeno'][0]}x{self.tamano_ventana['pantalla_pequeno'][1]}"
        elif ancho >= 1024 and alto >= 768:
            return f"{self.tamano_ventana['pantalla_muy_pequeno'][0]}x{self.tamano_ventana['pantalla_muy_pequeno'][1]}"
        elif ancho >= 800 and alto >= 600:
            return f"{self.tamano_ventana['pantalla_muy_muy_pequeno'][0]}x{self.tamano_ventana['pantalla_muy_muy_pequeno'][1]}"
        else:
            return f"{self.tamano_ventana['pantalla_muy_muy_muy_pequeno'][0]}x{self.tamano_ventana['pantalla_muy_muy_muy_pequeno'][1]}"  
            
    
    def centrar_ventana(self, ventana, ancho, alto):
        ventana.update_idletasks()
        ancho_ventana = int(ancho)
        alto_ventana = int(alto)
        x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2) - 40  # Sube la ventana 40 píxeles
        if y < 0:
            y = 0  # Evita que la ventana se salga de la pantalla por arriba
        ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        return ventana        
    
    