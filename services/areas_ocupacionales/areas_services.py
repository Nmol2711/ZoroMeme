import json
import logging
from groq import Groq
from services.areas_ocupacionales.areas_data import AREAS_OCUPACIONALES, CARPETAS_COMUNES
from services.configuracion_services.configuracion_services import ConfiguracionServices

logger = logging.getLogger(__name__)

class AreasServices:
    def __init__(self, config_service: ConfiguracionServices):
        self.config_service = config_service

    def obtener_areas_predefinidas(self):
        """Retorna el diccionario de áreas predefinidas."""
        return AREAS_OCUPACIONALES

    def obtener_diccionario_por_area(self, area_nombre):
        """
        Retorna un diccionario combinado de la área seleccionada y las comunes.
        """
        resultado = CARPETAS_COMUNES.copy()
        
        if area_nombre in AREAS_OCUPACIONALES:
            # Mezclar categorías específicas con las comunes
            # Si hay colisión de nombres, las de área ganan o se mezclan.
            # Aquí simplemente las añadimos.
            area_carpetas = AREAS_OCUPACIONALES[area_nombre]["carpetas"]
            for carpeta, keywords in area_carpetas.items():
                if carpeta in resultado:
                    # Mezclar keywords si ya existe
                    resultado[carpeta] = list(set(resultado[carpeta] + keywords))
                else:
                    resultado[carpeta] = keywords
        
        return resultado

    def generar_carpetas_con_ia(self, descripcion_trabajo, client: Groq):
        """
        Usa Groq para generar categorías y keywords personalizadas basadas en una descripción.
        """
        prompt = f"""
        Actúa como un experto en organización de archivos. 
        El usuario describe su trabajo como: "{descripcion_trabajo}"
        Genera un esquema de organización de carpetas (entre 5 y 8 carpetas).
        Para cada carpeta, proporciona entre 5 y 10 palabras clave que identifiquen los archivos que irían allí.
        Céntrate en términos técnicos, tipos de documentos o temas específicos de ese trabajo.
        
        Responde ESTRICTAMENTE con un objeto JSON donde las claves son los nombres de las carpetas 
        y los valores son listas de strings (las palabras clave).
        No incluyas explicaciones, solo el JSON.
        
        Ejemplo de formato:
        {{
            "Carpeta1": ["keyword1", "keyword2"],
            "Carpeta2": ["keyword3", "keyword4"]
        }}
        """

        try:
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            
            # Combinamos con las comunes para asegurar que siempre haya lo básico
            ia_result = json.loads(completion.choices[0].message.content)
            resultado = CARPETAS_COMUNES.copy()
            
            for carpeta, keywords in ia_result.items():
                # Sanitizar nombre de carpeta (quitar espacios, caracteres raros si los hay)
                nombre_limpio = carpeta.replace(" ", "_")
                if nombre_limpio in resultado:
                    resultado[nombre_limpio] = list(set(resultado[nombre_limpio] + keywords))
                else:
                    resultado[nombre_limpio] = keywords
                    
            return resultado
            
        except Exception as e:
            logger.error(f"Error al generar carpetas con IA: {e}")
            return CARPETAS_COMUNES # Fallback a las comunes si falla la IA

    def guardar_seleccion(self, nuevo_diccionario):
        """
        Guarda el diccionario final fusionándolo con el existente 
        para no borrar configuraciones manuales previas.
        """
        diccionario_actual = self.config_service.obtener_diccionario_palabras() or {}
        
        # Fusionar: El nuevo diccionario tiene prioridad en nombres de carpetas
        # pero mantenemos las carpetas que no están en el nuevo.
        resultado_fusión = diccionario_actual.copy()
        
        for carpeta, keywords in nuevo_diccionario.items():
            if carpeta in resultado_fusión:
                # Combinar keywords sin duplicados
                resultado_fusión[carpeta] = list(set(resultado_fusión[carpeta] + keywords))
            else:
                resultado_fusión[carpeta] = keywords
                
        return self.config_service.guardar_diccionario_palabras(resultado_fusión)
