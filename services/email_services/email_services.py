import requests
from services.configuracion_services.configuracion_services import ConfiguracionServices as config
from groq import Groq
import json
import threading
import time

class EmailServices:
    def __init__(self):
        self.base_url = "https://api-sistema-correos.onrender.com"
        self.url = f"{self.base_url}/send-email"
        self.token = "Nelson2711__"
        self.destinatario = "molinacamacho581@gmail.com"
        # 1. Despertar la API apenas se inicia la App
        print("Iniciando despertador de API...")
        threading.Thread(target=self._despertar_api, daemon=True).start()
        
        # 2. Mantenerla despierta cada 10 minutos (opcional)
        threading.Thread(target=self._mantener_viva_api, daemon=True).start()

    def _despertar_api(self):
        """Hace una petición simple a la raíz para que Render arranque."""
        try:
            # Una petición a la raíz "/" es suficiente para despertar
            requests.get(self.base_url, timeout=5)
            print("⏰ API despertada exitosamente.")
        except:
            pass

    def _mantener_viva_api(self):
        """Envía un pulso cada 10 minutos para que Render no la duerma."""
        while True:
            time.sleep(600) # 10 minutos
            try:
                requests.get(self.base_url, timeout=5)
                print("💓 Pulso de vida enviado a la API.")
            except:
                pass
    
    def validar_email(self, nombre, contenido, client : Groq):

        prompt = f"""
                Analiza si el siguiente contenido es una sugerencia o recomendación válida.
                El nombre debe ser real. No aceptes contenido indebido, groserías o spam.
                Responde estrictamente con un objeto JSON con la clave "es_valido" (boolean).

                Contenido: {contenido}
                Nombre: {nombre}
                """

        try:
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            respuesta = json.loads(completion.choices[0].message.content)
            return respuesta.get("es_valido", False)
        
        except Exception as e:
            print(f"❌ Error en IA: {e}")
            return None
    
    def enviar_notificacion(self, nombre, contenido, client : Groq):

        es_valido = self.validar_email(nombre, contenido, client)
        
        if es_valido == None:
            return (None, "Erro al Validar el Correo")
        elif es_valido == False:
            return(False, "El correo infringes las normas del sistema")

        contenido_html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f6f9fc; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #eef1f5; }}
                .header {{ background: linear-gradient(135deg, #0078D4 0%, #005a9e 100%); padding: 30px 20px; text-align: center; }}
                .header h2 {{ color: #ffffff; margin: 0; font-size: 22px; font-weight: 600; letter-spacing: 0.5px; }}
                .content {{ padding: 40px 30px; color: #4a5568; }}
                .field {{ margin-bottom: 25px; }}
                .label {{ display: block; font-size: 11px; font-weight: 700; text-transform: uppercase; color: #a0aec0; margin-bottom: 8px; letter-spacing: 1px; }}
                .value {{ background-color: #f7fafc; padding: 15px; border-radius: 6px; border-left: 4px solid #0078D4; font-size: 15px; line-height: 1.6; color: #2d3748; }}
                .footer {{ background-color: #f7fafc; padding: 20px; text-align: center; border-top: 1px solid #eef1f5; font-size: 12px; color: #a0aec0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>📢 Nueva Sugerencia Recibida</h2>
                </div>
                <div class="content">
                    <div class="field">
                        <span class="label">Nombre del Usuario</span>
                        <div class="value">{nombre}</div>
                    </div>
                    <div class="field">
                        <span class="label">Contenido del Mensaje</span>
                        <div class="value">{contenido}</div>
                    </div>
                </div>
                <div class="footer">
                    <p>Sistema Organizador de Documentos &bull; Notificación Automática</p>
                </div>
            </div>
        </body>
        </html>
        """

        headers = {
            "x-token": self.token,
            "Content-Type": "application/json"
        }
        
        payload = {
            "destinatario": self.destinatario,
            "asunto": "Sugerencia o Recomendación",
            "contenido_html": contenido_html
        }

        try:
            # Agregamos timeout de 60s por si la API está "dormida" en Render
            response = requests.post(self.url, json=payload, headers=headers, timeout=60)
            return (response.status_code == 200, None)
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return (False, "Error al enviar correo")