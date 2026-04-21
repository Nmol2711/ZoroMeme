import os
from utils.path_util import resource_path
# Importamos el módulo de estilos y la función para actualizar fuentes
import utils.config_componen_utils as style
from utils.config_componen_utils import actualizar_fuentes_globales
import platform

class AppConfig:
    def __init__(self):
        self.tema = "dark"
        # Usar resource_path para compatibilidad con PyInstaller
        self.color_tema = resource_path(os.path.join('config', 'dark_blue.json'))
        self.titulo_ventana = "Sistema Organizador de Docuementos"
        self.icono = resource_path(os.path.join('resources', 'logo.ico'))

        # Obtener el sistema operativo
        self.sistema_operativo = platform.system()

        self.categoria = "super_grande"  # Valor por defecto
        # Tamaños recomendados de ventana para cada rango de pantalla
        # Se establece un tamaño mínimo seguro para evitar que la UI se rompa en resoluciones pequeñas.
        self.tamano_ventana = {
            "super_grande": (1200, 800),
            "grande": (1200, 680),
            "medio": (1024, 680),
            "pequeno": (980, 650), # Tamaño mínimo seguro para la UI actual
        }
        # Perfiles de tamaño de fuente para cada resolución
        self.perfiles_fuente = {
            "super_grande": {
                "titulo_principal": 32, "titulo_secundario": 24, "menu": 18, "normal": 16, "pequeno": 12
            },
            "grande": {
                "titulo_principal": 30, "titulo_secundario": 22, "menu": 17, "normal": 15, "pequeno": 11
            },
            "medio": {
                "titulo_principal": 28, "titulo_secundario": 20, "menu": 16, "normal": 14, "pequeno": 11
            },
            "pequeno": {
                "titulo_principal": 26, "titulo_secundario": 19, "menu": 15, "normal": 13, "pequeno": 10
            }
        }
        # Perfiles de tamaño de imagen para Goku
        self.perfiles_tamano_goku = {
            "super_grande": 650,
            "grande": 550,
            "medio": 450,
            "pequeno": 400
        }

        self.tamano_goku_actual = self.perfiles_tamano_goku["super_grande"]
        

    def _ajustar_fuentes(self, categoria):
        """Ajusta los tamaños de fuente globales según la categoría de pantalla."""
        perfil = self.perfiles_fuente.get(categoria, self.perfiles_fuente["pequeno"])

        # Modificamos las variables de tamaño en el módulo de estilos
        style.TAMANO_TITULO_PRINCIPAL = perfil["titulo_principal"]
        style.TAMANO_TITULO_SECUNDARIO = perfil["titulo_secundario"]
        style.TAMANO_TEXTO_MENU = perfil["menu"]
        style.TAMANO_TEXTO_NORMAL = perfil["normal"]
        style.TAMANO_TEXTO_PEQUENO = perfil["pequeno"]

        # Ajustamos también el tamaño de la imagen de Goku
        self.tamano_goku_actual = self.perfiles_tamano_goku.get(categoria, self.perfiles_tamano_goku["pequeno"])

        # Llamamos a la función para que las tuplas de fuentes (FONT_...) se actualicen
        actualizar_fuentes_globales()

    def evaluar_tamano_pantalla(self, ancho, alto):
        """
        Evalúa la resolución de la pantalla y asigna una categoría para adaptar la UI.
        Cubre las resoluciones más comunes, agrupándolas en categorías lógicas.
        """
        # Grupo 1 (Super Grande): Para anchos de 1600px o más (ej. 1920x1080, 1600x900)
        if ancho >= 1600:
            categoria = "super_grande"
        # Grupo 2 (Grande): Para anchos entre 1360px y 1599px (ej. 1440x900, 1366x768)
        elif ancho >= 1360:
            categoria = "grande"
        # Grupo 3 (Medio): Para anchos entre 1152px y 1359px (ej. 1280x800, 1280x720)
        elif ancho >= 1152:
            categoria = "medio"
        # Grupo 4 (Pequeño): Para anchos menores a 1152px (ej. 1024x768, 800x600)
        # Se usa la configuración 'pequeno' que define el tamaño mínimo seguro.
        else:
            categoria = "pequeno"
        
        # Ajustamos las fuentes y el tamaño de Goku según la categoría detectada
        self._ajustar_fuentes(categoria)
        self.categoria = categoria
        # Devolvemos la geometría de la ventana correspondiente a la categoría
        tamano = self.tamano_ventana.get(categoria, self.tamano_ventana["pequeno"])
        return f"{tamano[0]}x{tamano[1]}"
    
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

    
    