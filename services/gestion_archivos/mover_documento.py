import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def mover_archivos_a_carpeta(ruta_origen, nombre_destino):
    ruta_home = Path.home()

    # Verificar si existe "Documentos" (Linux en español) o usar "Documents" (Windows/Linux en inglés)
    if (ruta_home / "Documentos").exists():
        carpeta_base = ruta_home / "Documentos"
    else:
        carpeta_base = ruta_home / "Documents"

    carpeta_destino = carpeta_base / nombre_destino
    
    # Verificamos si el archivo ya está en la carpeta destino (comparando con el padre del archivo)
    if carpeta_destino.resolve() == ruta_origen.parent.resolve():
        return True  # No es un error, pero no se mueve
    try:
        if not carpeta_destino.exists():
            carpeta_destino.mkdir(parents=True, exist_ok=True)

        destino_final = carpeta_destino / ruta_origen.name

        # Si el archivo ya existe, agregar un contador (ej: archivo (1).txt)
        if destino_final.exists():
            contador = 1
            while destino_final.exists():
                # Usamos f-string con stem y suffix para mantener la extensión correcta
                nuevo_nombre = f"{ruta_origen.stem} ({contador}){ruta_origen.suffix}"
                destino_final = carpeta_destino / nuevo_nombre
                contador += 1

        shutil.move(str(ruta_origen), str(destino_final))
        logger.info(f"Archivo movido a: {destino_final}")
        return True
    except Exception as e:
        logger.error(f"Error al mover el archivo {ruta_origen}: {e}")
        return False
