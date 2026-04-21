import json
import datetime
import logging
import threading
import re
from pathlib import Path
from groq import Groq
from services.configuracion_services.configuracion_services import ConfiguracionServices
from services.gestion_archivos.leer_archivos import (
    extraer_texto_del_archivo, 
    es_extension_soportada, 
    encode_image,
    EXTENSIONES_IMAGEN
)
from services.gestion_archivos.mover_documento import mover_archivos_a_carpeta
from services.organizador_documentos.proceso_estado import ProcesoEstado

logger = logging.getLogger(__name__)

class OrganizarDocumentosServices(ConfiguracionServices):
    def __init__(self):
        super().__init__()
        self.api_key = self.obtener_api_key()
        self.diccionario_palabras = self.obtener_diccionario_palabras()
        self.estado = ProcesoEstado()
    
    def _construir_prompt_texto(self, lista_pendientes):
        materias = ", ".join(self.diccionario_palabras.keys())
        datos_ia = ""
        for nombre, texto in lista_pendientes:
            datos_ia += f"ARCHIVO: {nombre} | CONTENIDO: {texto[:500]}\n"

        return f"Clasifica los siguientes archivos en UNA de estas categorías: [{materias}, Otros]. Responde estrictamente con un objeto JSON donde las claves son los nombres de los archivos y los valores son las categorías.\n\n{datos_ia}"

    def clasificar_con_groq(self, lista_pendientes, client: Groq):
        try:
            prompt = self._construir_prompt_texto(lista_pendientes)
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error en IA (Texto): {e}")
            return {}

    def clasificar_imagen_con_groq(self, ruta_imagen, client: Groq):
        """Clasifica una imagen usando Groq Vision."""
        materias = ", ".join(self.diccionario_palabras.keys())
        base64_image = encode_image(ruta_imagen)
        
        prompt = f"¿A qué categoría pertenece esta imagen? Categorías disponibles: [{materias}, Otros]. Responde solo con el nombre de la categoría en formato JSON: {{\"categoria\": \"NOMBRE\"}}"
        
        try:
            completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                model="llama-3.2-90b-vision-preview",

                response_format={"type": "json_object"}
            )
            res = json.loads(completion.choices[0].message.content)
            return res.get("categoria", "Otros")
        except Exception as e:
            logger.error(f"Error en IA (Visión) para {ruta_imagen.name}: {e}")
            return "Otros"

    def organizar_hibrido(self, carpeta_ruta, client: Groq):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            carpeta_path = Path(carpeta_ruta)
            archivos = [f for f in carpeta_path.iterdir() if f.is_file() and not f.name.startswith('~$') and es_extension_soportada(f)]

            self.estado.iniciar(len(archivos), str(carpeta_path))
            self.guardar_archivo_log([(timestamp, f"Iniciando sesión en: {str(carpeta_path)}. Archivos: {len(archivos)}")])
            
            informe_resultados = {"archivos_analizados": len(archivos), "archivos_movidos": 0, "nombre_archivos_movidos": []}
            
            # Preparar sets de keywords para búsqueda O(1)
            diccionario_sets = {m: set(k.lower() for k in keywords) for m, keywords in self.diccionario_palabras.items()}
            
            pendientes_para_ia = []
            
            for ruta in archivos:
                try:
                    self.estado.actualizar(ruta.name, incremento=False)
                    
                    if ruta.suffix.lower() in EXTENSIONES_IMAGEN:
                        # Las imágenes van directo a IA o filtro por nombre
                        # Filtro por nombre primero
                        nombre_lower = ruta.name.lower()
                        clasificado = False
                        for materia, kw_set in diccionario_sets.items():
                            if any(k in nombre_lower for k in kw_set):
                                self._mover_y_registrar(ruta, materia, informe_resultados, timestamp, "KEYWORD_NAME")
                                clasificado = True
                                break
                        
                        if not clasificado:
                            categoria = self.clasificar_imagen_con_groq(ruta, client)
                            self._mover_y_registrar(ruta, categoria, informe_resultados, timestamp, "IA_VISION")
                        
                        self.estado.actualizar(ruta.name, mensaje=f"Procesada imagen: {ruta.name}")
                        continue

                    # Procesamiento de documentos de texto
                    texto = extraer_texto_del_archivo(ruta)
                    texto_words = set(re.findall(r'\w+', texto.lower()))
                    
                    clasificado_local = False
                    mejor_materia = None
                    max_coincidencias = 0

                    for materia, kw_set in diccionario_sets.items():
                        # Intersección de sets es muy rápida
                        coincidencias = len(kw_set.intersection(texto_words))
                        
                        # También buscamos por nombre de archivo
                        if any(k in ruta.name.lower() for k in kw_set):
                            coincidencias += 2 

                        if coincidencias > max_coincidencias:
                            max_coincidencias = coincidencias
                            mejor_materia = materia

                    # Umbral de confianza local
                    if mejor_materia and max_coincidencias >= 2:
                        self._mover_y_registrar(ruta, mejor_materia, informe_resultados, timestamp, "LOCAL")
                        clasificado_local = True
                        self.estado.actualizar(ruta.name, mensaje=f"Clasificado local: {ruta.name} -> {mejor_materia}")
                    
                    if not clasificado_local:
                        pendientes_para_ia.append((ruta.name, texto, ruta))
                        
                except Exception as e:
                    logger.error(f"Error procesando archivo {ruta.name}: {e}")
                    self.estado.actualizar(ruta.name, mensaje=f"Error en {ruta.name}: {e}")

            # Procesar pendientes por IA en lotes
            if pendientes_para_ia:
                tamano_lote = 5
                for i in range(0, len(pendientes_para_ia), tamano_lote):
                    lote = pendientes_para_ia[i:i + tamano_lote]
                    self.estado.actualizar("Consultando IA...", mensaje=f"Consultando IA para lote de {len(lote)} archivos...", incremento=False)
                    
                    resultados_ia = self.clasificar_con_groq([(n, t) for n, t, r in lote], client)

                    for nombre, texto, ruta in lote:
                        categoria = resultados_ia.get(nombre, "Otros")
                        if categoria not in self.diccionario_palabras: 
                            categoria = "Otros"
                        
                        self._mover_y_registrar(ruta, categoria, informe_resultados, timestamp, "IA_TEXT")
                        self.estado.actualizar(nombre, mensaje=f"Clasificado IA: {nombre} -> {categoria}")

            self.estado.finalizar(informe_resultados)
            return informe_resultados
            
        except Exception as e:
            logger.error(f"Error general en organización: {e}")
            self.estado.finalizar(None)
            return False

    def _mover_y_registrar(self, ruta, categoria, informe, timestamp, metodo):
        if mover_archivos_a_carpeta(ruta, categoria):
            informe["archivos_movidos"] += 1
            informe["nombre_archivos_movidos"].append((ruta.name, categoria))
            self.guardar_archivo_log([(timestamp, f"{metodo}: {ruta.name} movido a {categoria}")])

import re # Necesario para findall en la búsqueda local