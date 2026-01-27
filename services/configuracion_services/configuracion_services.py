from pathlib import Path
import os
import json
from datetime import datetime
from config.app_config import AppConfig


class ConfiguracionServices:
    def __init__(self):
        self.api_key = None
        self.archivo_log = None
        self.diccionario_palabras : dict[str, list[str]] = None
        
        # --- Lógica multiplataforma para rutas de configuración ---
        system = AppConfig().sistema_operativo
        if system == "Windows":
            # %APPDATA%\OrganizadorIA
            self.ruta_app_data = Path(os.getenv('APPDATA')) / "OrganizadorIA"
        elif system == "Linux":
            # ~/.config/OrganizadorIA (estándar XDG)
            self.ruta_app_data = Path.home() / ".config" / "OrganizadorIA"
        elif system == "Darwin": # macOS
            # ~/Library/Application Support/OrganizadorIA
            self.ruta_app_data = Path.home() / "Library" / "Application Support" / "OrganizadorIA"
        else: # Fallback para otros sistemas
            self.ruta_app_data = Path.home() / ".OrganizadorIA"

        self.ruta_config = self.ruta_app_data / "config"
        self.ruta_log = self.ruta_app_data / "log"

        # Crear las carpetas necesarias
        self.ruta_app_data.mkdir(exist_ok=True)
        self.ruta_config.mkdir(parents=True, exist_ok=True)
        self.ruta_log.mkdir(parents=True, exist_ok=True)

        # Inicializar archivos si no existen para evitar errores de lectura
        if not (self.ruta_config / "config.json").exists():
            with open(self.ruta_config / "config.json", "w") as f:
                json.dump({}, f)

        if not (self.ruta_config / "diccionario_palabras.json").exists():
            with open(self.ruta_config / "diccionario_palabras.json", "w") as f:
                json.dump({}, f)
        
        if not (self.ruta_log / "historial_orden.log").exists():
            with open(self.ruta_log / "historial_orden.log", "w") as f:
                pass

    def obtener_api_key(self):
        try:
            archivo_config = self.ruta_config / "config.json"
            if not archivo_config.exists():
                return None
            with open(archivo_config, "r") as f:
                return json.load(f).get("api_key")
        except Exception as e:
            print(f"Error al obtener la API key: {e}")
            return False
    
    def obtener_archivo_log(self, fecha_inicio: str = None, fecha_fin: str = None, filtro_texto: str = None):
        try:
            archivo_log = self.ruta_log / "historial_orden.log"
            if not archivo_log.exists():
                return [] if (fecha_inicio or fecha_fin or filtro_texto) else None

            if not fecha_inicio and not fecha_fin and not filtro_texto:
                return archivo_log

            registros = []
            dt_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
            dt_fin = datetime.strptime(fecha_fin, "%Y-%m-%d") if fecha_fin else None

            with open(archivo_log, "r", encoding="utf-8", errors="replace") as f:
                for linea in f:
                    try:
                        # Filtro de texto (nombre de carpeta, archivo, etc.)
                        if filtro_texto and filtro_texto.lower() not in linea.lower():
                            continue

                        # Formato esperado: "YYYY-MM-DD HH:MM:SS: mensaje"
                        fecha_linea = datetime.strptime(linea[:19], "%Y-%m-%d %H:%M:%S")
                        
                        if dt_inicio and fecha_linea < dt_inicio:
                            continue
                        if dt_fin and fecha_linea.date() > dt_fin.date():
                            continue
                        registros.append(linea.strip())
                    except (ValueError, IndexError):
                        continue
            return registros

        except Exception as e:
            print(f"Error al obtener el archivo de log: {e}")
            return [] if (fecha_inicio or fecha_fin or filtro_texto) else False
        
    def obtener_carpetas_analizadas_archivos_movidos(self, fecha_inicio: str = None, fecha_fin: str = None) -> tuple[int, int]:
        try:
            archivo_log = self.ruta_log / "historial_orden.log"
            if not archivo_log.exists():
                return (0, 0)

            carpetas_analizadas = 0
            archivos_movidos = 0
            dt_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
            dt_fin = datetime.strptime(fecha_fin, "%Y-%m-%d") if fecha_fin else None

            with open(archivo_log, "r", encoding="utf-8", errors="replace") as f:
                for linea in f:
                    try:
                        fecha_linea = datetime.strptime(linea[:19], "%Y-%m-%d %H:%M:%S")
                        
                        if dt_inicio and fecha_linea < dt_inicio:
                            continue
                        if dt_fin and fecha_linea.date() > dt_fin.date():
                            continue

                        mensaje = linea[21:].strip()
                        if "Iniciando sesión en:" in mensaje:
                            carpetas_analizadas += 1
                        elif "movido a" in mensaje:
                            archivos_movidos += 1
                    except (ValueError, IndexError):
                        continue
            return (carpetas_analizadas, archivos_movidos)

        except Exception as e:
            print(f"Error al obtener estadísticas del log: {e}")
            return (0, 0)
    
    def obtener_diccionario_palabras(self):
        try:
            archivo_diccionario = self.ruta_config / "diccionario_palabras.json"
            if not archivo_diccionario.exists():
                return None
            with open(archivo_diccionario, "r") as f:
                diccionario = json.load(f)
            return diccionario
        except Exception as e:
            print(f"Error al obtener el diccionario de palabras: {e}")
            return False
        
    def guardar_api_key(self, nueva_key):
        try:
            self.ruta_config.mkdir(parents=True, exist_ok=True)
            archivo_config = self.ruta_config / "config.json"

            config = {}
            if archivo_config.exists():
                with open(archivo_config, "r") as f:
                    try:
                        config = json.load(f)
                    except json.JSONDecodeError:
                        pass
            
            config["api_key"] = nueva_key
            with open(archivo_config, "w") as f:
                json.dump(config, f)
            
            self.api_key = nueva_key
            return True
        except Exception as e:
            print(f"Error al guardar la API key: {e}")
            return False
    
    def guardar_diccionario_palabras(self, nuevo_diccionario: dict[str, list[str]]):
        try:
            archivo_diccionario = self.ruta_config / "diccionario_palabras.json"
            with open(archivo_diccionario, "w") as f:
                json.dump(nuevo_diccionario, f)
            
            self.diccionario_palabras = nuevo_diccionario
            return True
        except Exception as e:
            print(f"Error al guardar el diccionario de palabras: {e}")
            return False
    
    def guardar_archivo_log(self, movimientos: list[tuple[str, str]]): # espera resivir una lista de tuplas (fecha, operacion realizada)
        try:
            archivo_log = self.ruta_log / "historial_orden.log"
            with open(archivo_log, "a", encoding="utf-8") as f:
                for fecha, operacion in movimientos:
                    f.write(f"{fecha}: {operacion}\n")
            
            self.archivo_log = archivo_log
            return True
        except Exception as e:
            print(f"Error al guardar el archivo de log: {e}")
            return False





        
