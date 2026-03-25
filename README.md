# 📂 Organizador de Archivos Inteligente (IA)

¡Bienvenido! Este software utiliza Inteligencia Artificial para analizar el contenido de tus documentos y organizarlos automáticamente en carpetas temáticas. Olvídate de mover archivos uno por uno.

## 📋 Requisitos e Instalación

Para ejecutar este proyecto correctamente, asegúrate de tener instalado **Python 3.10** o superior en tu sistema.

### 1. Crear entorno virtual
Se recomienda utilizar un entorno virtual para gestionar las dependencias de forma aislada:

*   **Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
*   **Linux / macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 2. Instalar dependencias
Una vez activado el entorno virtual, instala las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt
```

## 1. 🔑 Cómo obtener tu Llave de API (Gratis)
Para que el programa "piense", necesita conectarse a la IA de Groq. Sigue estos pasos:

1. Ve a **Groq Cloud Console**.
2. Regístrate con tu correo (es gratis y rápido).
3. Haz clic en **"Create API Key"**.
4. Ponle un nombre (ej. "MiOrganizador") y copia la llave que empieza por `gsk_...`.

⚠️ **Guárdala bien**; el programa la pedirá la primera vez que lo abras.

## 2. 🚀 Cómo funciona
El organizador es "híbrido", lo que significa que es rápido y eficiente:

*   **Fase 1 (Rápida):** Busca palabras clave técnicas dentro de tus archivos. Si detecta términos claros (ej: Anatomía, Python, Factibilidad), los mueve al instante.
*   **Fase 2 (Inteligente):** Si no está seguro, le pregunta a la IA Llama 3 para que analice el contexto y decida la mejor categoría.
*   **Fase 3 (Seguridad):** Si el archivo ya existe en la carpeta de destino, el programa le añade un número al nombre para no sobrescribir ni borrar nada.

## 3. 📄 Formatos Compatibles
El programa puede "leer" el interior de:

*   📑 **PDF** (Documentos escaneados o digitales)
*   📝 **Word** (.docx)
*   📊 **Excel** (.xlsx)
*   🖼️ **PowerPoint** (.pptx)

Los demás archivos serán analizados por el modelo de IA

## 4. 📂 Registro y Configuración
*   **Logs:** ¿Quieres saber qué hizo el programa? Revisa el archivo `historial_orden.log` en tu carpeta de usuario.
*   **Ubicación de datos:** Tu configuración se guarda en `%AppData%\OrganizadorIA`. Si necesitas cambiar tu API Key, borra el archivo `config.json` en esa carpeta y el programa te pedirá la nueva.

## 💡 Tips de Uso
*   **Límites:** Las cuentas gratuitas de Groq permiten procesar cientos de archivos al día. Si procesas miles muy rápido, es posible que debas esperar un minuto para continuar.
*   **Orden:** El programa creará carpetas automáticamente (Anatomía, Programación, etc.) dentro de la ruta Documents.