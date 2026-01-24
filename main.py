import os
import json
import datetime
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path
from leer_archivos import extraer_texto_del_archivo
from mover_docuemnto import mover_archivos_a_carpeta

# --- DICCIONARIO ORGANIZADOR (Igual al tuyo) ---
ORGANIZADOR = {
    "Anatomia": ["miología", "osteología", "esplacnología", "foramen", "articulación coxofemoral", "planimetría"],
    "Patologia": ["histopatología", "patogenia", "etiología", "necropsia", "exudado", "isquemia", "hipertrofia"],
    "Fisiologia": ["potencial de acción", "sinapsis", "neurotransmisor", "osmosis", "nefrona", "hematosis"],
    "Farmacologia": ["farmacocinética", "farmacodinámica", "posología", "vía parenteral", "biodisponibilidad"],
    "Cirugia": ["hemostasia", "laparotomía", "asepsia", "antisepsia", "electro bisturí", "traumatología"],
    "Parasitologia": ["endoparásito", "ectoparásito", "nematodo", "cestodo", "ixodidae", "coprológico"],
    "Reproduccion": ["espermatogénesis", "cuerpo lúteo", "folículo", "distocia", "palpación rectal", "estro"],
    "Clinica_Animal": ["anamnesis", "semiología", "constantes fisiológicas", "auscultación", "canis familiaris", "felis catus"],
    "Matematicas": ["trinomio", "logaritmo", "ecuación diferencial", "vectorial", "asíntota", "polinomio"],
    "Estadistica": ["desviación estándar", "chi cuadrado", "intervalo de confianza", "p-valor", "correlación de pearson"],
    "Programacion": ["entorno virtual", "diccionario python", "variable booleana", "encapsulamiento", "framework", "repositorio git"],
    "Redes": ["máscara de subred", "modelo osi", "dirección mac", "puerta de enlace", "dns", "dhcp"],
    "Base_de_Datos": ["clave foránea", "normalización de datos", "store procedure", "inner join", "instrucción select", "primary key"],
    "Sistemas": ["microprocesador", "memoria ram", "firmware", "bios", "kernel", "virtualización"],
    "Proyectos": ["diagrama de gantt", "metodología ágil", "matriz foda", "estudio de factibilidad", "acta de constitución"],
}

# --- AYUDA ---
def mostrar_ayuda():
    print("\n" + "="*50)
    print("ℹ️  INFORMACIÓN DE USO Y LÍMITES")
    print("="*50)
    print("1. LLAVE (API KEY): Se guarda en AppData/OrganizadorIA.")
    print("2. LÍMITES: Las cuentas gratuitas de Groq suelen permitir")
    print("   miles de archivos diarios, pero tienen límite de velocidad.")
    print("3. SEGURIDAD: El programa solo lee los primeros párrafos")
    print("   para clasificar, no guarda copias de tus datos.")
    print("4. LOGS: Consulta 'historial_orden.log' para ver movimientos. Esta ubicado en AppData/OrganizadorIA")
    print("="*50 + "\n")

def obtener_configuracion():
    ruta_appdata = Path(os.getenv('APPDATA')) / "OrganizadorIA"
    ruta_appdata.mkdir(exist_ok=True)
    archivo_config = ruta_appdata / "config.json"
    archivo_log = ruta_appdata / "historial_orden.log"

    if archivo_config.exists():
        with open(archivo_config, "r") as f:
            config = json.load(f)
    else:
        print("🔑 Primera vez detectada.")
        nueva_key = input("Introduce tu GROQ_API_KEY: ")
        config = {"api_key": nueva_key}
        with open(archivo_config, "w") as f:
            json.dump(config, f)
            
    return config["api_key"], archivo_log

def escribir_log(archivo_log, mensaje):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(archivo_log, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {mensaje}\n")

def clasificar_con_groq(lista_pendientes, client: Groq):
    materias = ", ".join(ORGANIZADOR.keys())
    datos_ia = ""
    for nombre, texto in lista_pendientes:
        datos_ia += f"ARCHIVO: {nombre} | CONTENIDO: {texto[:400]}\n"

    prompt = f"Clasifica estos archivos en: [{materias}, Otros]. Responde solo JSON: {{'nombre': 'CAT'}}"

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

def organizar_hibrido(carpeta_ruta, client: Groq, archivo_log):
    print("--- 🚀 Iniciando Clasificación ---")
    escribir_log(archivo_log, f"Iniciando sesión en: {carpeta_ruta}")
    
    archivos = [f for f in carpeta_ruta.iterdir() if f.is_file() and not f.name.startswith('~$')]
    pendientes_para_ia = []

    for ruta in archivos:
        texto = extraer_texto_del_archivo(ruta)
        texto_lower = texto.lower()
        clasificado_local = False

        for materia, keywords in ORGANIZADOR.items():
            coincidencias = sum(1 for k in keywords if k.lower() in texto_lower)
            if coincidencias >= 2:
                print(f"📍 Keywords: {ruta.name} -> {materia}")
                mover_archivos_a_carpeta(ruta, materia)
                escribir_log(archivo_log, f"KEYWORD: {ruta.name} movido a {materia}")
                clasificado_local = True
                break
        
        if not clasificado_local:
            pendientes_para_ia.append((ruta.name, texto, ruta))

    if pendientes_para_ia:
        print(f"\n🤖 Consultando a la IA...")
        resultados_ia = clasificar_con_groq([(n, t) for n, t, r in pendientes_para_ia], client)

        for nombre, texto, ruta in pendientes_para_ia:
            categoria = resultados_ia.get(nombre, "Otros")
            if categoria not in ORGANIZADOR: categoria = "Otros"
            print(f"✨ IA: {nombre} -> {categoria}")
            mover_archivos_a_carpeta(ruta, categoria)
            escribir_log(archivo_log, f"IA: {nombre} movido a {categoria}")

if __name__ == "__main__":
    load_dotenv()
    try:
        api_key, archivo_log = obtener_configuracion()
        client = Groq(api_key=api_key)
        
        print("-" * 40)
        print("| ORGANIZADOR DE ARCHIVOS INTELIGENTE |")
        print("-" * 40)

        opcion = input("¿Deseas ver la guía de uso y límites? S para si: ")
        if opcion.lower() == 's':
            mostrar_ayuda()
        
        print("Introdusca la ruta de la carpeta donde estan los archivos que desea clasificar. Ej: C:\\Users\\cpustorevzla\\Documents\\Documenntos varios")
        while True:
            entrada = input("\nRuta de carpeta (o 'N' para salir): ")
            if entrada.lower() == 'n': 
                print("Saliendo...")
                break
            if not entrada:
                continue
            
            ruta = Path(entrada)
            if ruta.exists() and ruta.is_dir():
                organizar_hibrido(ruta, client, archivo_log)
                print("\n✅ Proceso terminado.")
            else:
                print("❌ Ruta inválida.")

            if input("¿Otra carpeta? (S/N): ").lower() == 'n': 
                print("Saliendo...")
                break
            
    except Exception as e:
        print(f"💥 Error crítico: {e}")
        input("Presione ENTER para cerrar...")