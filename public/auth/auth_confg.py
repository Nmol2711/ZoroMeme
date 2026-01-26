from services.configuracion_services.configuracion_services import ConfiguracionServices
from groq import Groq

class AuthCofig:
    def __init__(self, configuracion_services : ConfiguracionServices):
        self.configuracion_services = configuracion_services
    
    def existe_api_key(self):
        resultado = self.configuracion_services.obtener_api_key()
        
        if resultado == None:
            return (False,"No se ha insertado la api key")
        elif resultado == False:
            return (False,"Ocurre un error para obtener la api key, insertar nuevamente la api key")
        elif resultado:
            return (True,"")
        else:
            return (False,"Error inesperado")
        
    def autenticar_api_key(self, api_key=None):
        #Esto solo se va usar si el metodo de existe_api_key retorna true
        if api_key is None:
            api_key = self.configuracion_services.obtener_api_key()
            
        if not api_key or len(api_key) < 10: # Validación básica inicial
            return False
        try:
            client = Groq(api_key=api_key)
            # Intentamos listar los modelos (es una petición rápida y ligera)
            client.models.list()
            return True
        except Exception as e:
            # Si el error es 401 (Unauthorized), la key está mal.
            print(f"Error de validación: {e}")
            return False
    
    def existe_diccionario_palabras(self):
        resultado = self.configuracion_services.obtener_diccionario_palabras()  
        if resultado == None:
            return (False,"No se ha insertado el nombre de los directorios destinos\nDirijase a la configuracion para insertar los directorios")
        elif resultado == False:
            return (False,"Ocurre un error para obtener los directorios\nDirijase a la configuracion para insertar nuevamente los directorios")
        elif resultado:
            return (True,"")
        else:
            return (False,"Error inesperado")
    
    def obtener_cliente_groq(self):
        return Groq(api_key=self.configuracion_services.obtener_api_key())
        