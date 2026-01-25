from services.configuracion_services.configuracion_services import ConfiguracionServices
from services.gestion_archivos.leer_archivos import extraer_texto_del_archivo
from services.gestion_archivos.mover_docuemnto import mover_archivos_a_carpeta
from groq import Groq
import json
import datetime
from pathlib import Path
class OrganizarDocumentosServices(ConfiguracionServices):
    def __init__(self):
        super().__init__()
        self.api_key = self.obtener_api_key()
        self.diccionario_palabras = self.obtener_diccionario_palabras()
        self.archivo_log = self.obtener_archivo_log()
    
    def clasificar_con_groq(self,lista_pendientes, client: Groq):
        materias = ", ".join(self.diccionario_palabras.keys())
        datos_ia = ""
        for nombre, texto in lista_pendientes:
            datos_ia += f"ARCHIVO: {nombre} | CONTENIDO: {texto[:400]}\n"

        prompt = f"Clasifica los siguientes archivos en: [{materias}, Otros]. Responde estrictamente con un objeto JSON donde las claves son los nombres de los archivos y los valores son las categorías.\n\n{datos_ia}"

        try:
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            print(f"❌ Error en IA: {e}")
            return {}
    
    def organizar_hibrido(self,carpeta_ruta, client: Groq, archivo_log):
        timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        try:
            carpeta_path = Path(carpeta_ruta)
            
            archivos = [f for f in carpeta_path.iterdir() if f.is_file() and not f.name.startswith('~$')]

            self.guardar_archivo_log([(timestamp, f"Iniciando sesión en: {str(carpeta_path)}. Archivos a analizar: {len(archivos)}")])
            
            pendientes_para_ia = []

            informe_resultados = {"archivos_analizados": len(archivos), "archivos_movidos": 0, "nombre_archivos_movidos": []}
            self.diccionario_palabras = self.obtener_diccionario_palabras()

            for ruta in archivos:
                texto = extraer_texto_del_archivo(ruta)
                texto_lower = texto.lower()
                clasificado_local = False

                for materia, keywords in self.diccionario_palabras.items():
                    coincidencias = sum(1 for k in keywords if k.lower() in texto_lower)
                    if coincidencias >= 2:
                        if mover_archivos_a_carpeta(ruta, materia):
                            informe_resultados["archivos_movidos"] += 1
                            informe_resultados["nombre_archivos_movidos"].append((ruta.name, materia))
                        self.guardar_archivo_log([(timestamp, f"KEYWORD: {ruta.name} movido a {materia}")])
                        clasificado_local = True
                        break
                
                if not clasificado_local:
                    pendientes_para_ia.append((ruta.name, texto, ruta))

            if pendientes_para_ia:
                print(f"\n🤖 Consultando a la IA...")
                resultados_ia = self.clasificar_con_groq([(n, t) for n, t, r in pendientes_para_ia], client)

                for nombre, texto, ruta in pendientes_para_ia:
                    categoria = resultados_ia.get(nombre, "Otros")
                    if categoria not in self.diccionario_palabras: categoria = "Otros"
                    if mover_archivos_a_carpeta(ruta, categoria):
                        informe_resultados["archivos_movidos"] += 1
                        informe_resultados["nombre_archivos_movidos"].append((nombre, categoria))
                    self.guardar_archivo_log([(timestamp, f"IA: {nombre} movido a {categoria}")])
            return informe_resultados
        except Exception as e:
            print(f"❌ Error en organización: {e}")
            self.guardar_archivo_log([(timestamp, f"Error en organización: {e}")])
            return False