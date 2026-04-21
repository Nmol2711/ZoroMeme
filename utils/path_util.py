import sys
import os
import platform
from importlib import resources
from pathlib import Path
import customtkinter as ctk
from PIL import Image
from plyer import filechooser


def resource_path(relative_path):
    """Devuelve la ruta absoluta a un recurso, compatible con:
    - Desarrollo (ruta relativa al proyecto),
    - PyInstaller (sys._MEIPASS),
    - Nuitka standalone/onefile (carpeta junto al exe o <exe>.dist).
    """
    # 1) PyInstaller
    try:
        base_path = sys._MEIPASS
        candidate = os.path.join(base_path, relative_path)
        if os.path.exists(candidate):
            return candidate
    except Exception:
        pass

    # 2) Si estamos 'frozen' (Nuitka o similares), probar rutas junto al ejecutable
    if getattr(sys, 'frozen', False) or getattr(sys, 'frozen', None) is not None:
        exe_dir = os.path.dirname(sys.executable)
        candidate = os.path.join(exe_dir, relative_path)
        if os.path.exists(candidate):
            return candidate
        # En algunos layouts Nuitka crea <exe>.dist o coloca archivos en una carpeta con sufijo .dist
        dist_candidate = os.path.join(exe_dir, os.path.basename(exe_dir) + '.dist', relative_path)
        if os.path.exists(dist_candidate):
            return dist_candidate
        # Otro patrón: carpeta <exe>.dist al lado del exe
        alt_candidate = os.path.join(exe_dir + '.dist', relative_path)
        if os.path.exists(alt_candidate):
            return alt_candidate

    # 3) Desarrollo: relativo a la raíz del repo (cwd)
    candidate = os.path.abspath(relative_path)
    if os.path.exists(candidate):
        return candidate

    # 4) Intentar importlib.resources si el recurso está embebido como package data
    try:
        package, _, rest = relative_path.partition(os.sep)
        if rest and resources.is_resource(package, rest):
            with resources.path(package, rest) as p:
                return str(p)
    except Exception:
        pass

    # 5) Fallback: devolver la ruta tal cual (puede fallar al abrir)
    return relative_path

def leer_imagen(ruta, tamano=None):
        """
        Lee una imagen y la redimensiona.
        - Si tamano es una tupla (ancho, alto), redimensiona a ese tamaño (puede deformar).
        - Si tamano es un entero, lo usa como altura y calcula el ancho para mantener la proporción.
        """
        try:
            ruta_a_abrir = ruta
            if ruta and not os.path.isabs(ruta):
                posible = resource_path(ruta)
                if os.path.exists(posible):
                    ruta_a_abrir = posible

            imagen_pil = Image.open(ruta_a_abrir).convert("RGBA")

            # tamaño por defecto (tamaño original)
            tamano_final = imagen_pil.size

            if isinstance(tamano, int):
                # Redimensionar manteniendo la proporción basado en la altura
                altura_deseada = tamano
                proporcion = imagen_pil.width / imagen_pil.height
                ancho_calculado = int(altura_deseada * proporcion)
                tamano_final = (ancho_calculado, altura_deseada)
                imagen_pil = imagen_pil.resize(tamano_final, Image.Resampling.LANCZOS)

            elif isinstance(tamano, tuple):
                # Usar tamaño fijo (comportamiento anterior)
                tamano_final = tamano
                imagen_pil = imagen_pil.resize(tamano_final, Image.Resampling.LANCZOS)

            return ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=tamano_final)
        except Exception as e:
            print(f"Error al leer la imagen {ruta}: {e}")
            return None
    
def seleccionar_carpeta():
    # Detectar ruta de documentos (Inglés o Español)
    home = Path.home()
    initial_path = home
    
    if (home / "Documents").exists():
        initial_path = home / "Documents"
    elif (home / "Documentos").exists():
        initial_path = home / "Documentos"

    # Abre el explorador de archivos para elegir una carpeta
    if platform.system() == "Linux":
        ruta = filechooser.choose_dir(title="Selecciona la carpeta para organizar", path=str(initial_path))
        return ruta[0] if ruta else ""

    ruta = ctk.filedialog.askdirectory(
        title="Selecciona la carpeta que deseas organizar",
        initialdir=str(initial_path)
    )
    return ruta
