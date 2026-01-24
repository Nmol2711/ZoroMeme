import shutil
from pathlib import Path

def mover_archivos_a_carpeta(ruta_origen, nombre_destino):
    ruta_home = Path.home()

    carpeta_destino = Path(ruta_home / "Documents" / nombre_destino)
    try:
        if not carpeta_destino.exists():
            carpeta_destino.mkdir(parents=True, exist_ok=True)

        destino_final = carpeta_destino / ruta_origen.name

        # Si el archivo ya existe, agregar un contador (ej: archivo (1).txt)
        if destino_final.exists():
            contador = 1
            while destino_final.exists():
                destino_final = carpeta_destino / f"{ruta_origen.stem} ({contador}){ruta_origen.suffix}"
                contador += 1

        shutil.move(str(ruta_origen), str(destino_final))
        print(f"Archivo movido a la carpeta: {nombre_destino} -> {destino_final.name}")
    except Exception as e:
        print(f"Error al mover el archivo: {e}")
