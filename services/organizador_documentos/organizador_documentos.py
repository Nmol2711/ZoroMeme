from services.configuracion_services.configuracion_services import ConfiguracionServices
from services.gestion_archivos.leer_archivos import extraer_texto_del_archivo
from services.gestion_archivos.mover_docuemnto import mover_archivos_a_carpeta
from groq import Groq
import json
import datetime
from pathlib import Path

DOCUMENTOS_PERMITIDOS = ['.pdf', '.docx', '.txt', '.xlsx', '.pptx']

class OrganizarDocumentosServices(ConfiguracionServices):
    def __init__(self):
        super().__init__()
        self.api_key = self.obtener_api_key()
        self.diccionario_palabras = self.obtener_diccionario_palabras()
    
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
    
    def organizar_hibrido(self,carpeta_ruta, client: Groq):
        timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        try:
            carpeta_path = Path(carpeta_ruta)
            
            archivos = [f for f in carpeta_path.iterdir() if f.is_file() and not f.name.startswith('~$') and f.suffix.lower() in DOCUMENTOS_PERMITIDOS]

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
                    umbral = 1 if len(keywords) == 1 else 2
                    if coincidencias >= umbral:
                        if mover_archivos_a_carpeta(ruta, materia):
                            informe_resultados["archivos_movidos"] += 1
                            informe_resultados["nombre_archivos_movidos"].append((ruta.name, materia))
                        self.guardar_archivo_log([(timestamp, f"KEYWORD: {ruta.name} movido a {materia}")])
                        clasificado_local = True
                        break
                
                if not clasificado_local:
                    pendientes_para_ia.append((ruta.name, texto, ruta))

            if pendientes_para_ia:
                # Procesar en lotes para evitar error 413 (Rate Limit)
                tamano_lote = 5
                for i in range(0, len(pendientes_para_ia), tamano_lote):
                    lote = pendientes_para_ia[i:i + tamano_lote]
                    resultados_ia = self.clasificar_con_groq([(n, t) for n, t, r in lote], client)

                    for nombre, texto, ruta in lote:
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