import fitz  # PyMuPDF
import docx
import openpyxl
from pptx import Presentation
from pathlib import Path
import zipfile
import re

def limpiar_xml(xml_content):
    """Elimina etiquetas XML para dejar solo texto."""
    return re.sub(r'<[^>]+>', ' ', xml_content)

def leer_docx_raw(ruta):
    try:
        with zipfile.ZipFile(ruta) as z:
            xml_content = z.read('word/document.xml').decode('utf-8')
            return limpiar_xml(xml_content)
    except Exception:
        return ""

def leer_pptx_raw(ruta):
    texto = ""
    try:
        with zipfile.ZipFile(ruta) as z:
            slides = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            for slide in slides:
                xml_content = z.read(slide).decode('utf-8')
                texto += limpiar_xml(xml_content) + " "
    except Exception:
        pass
    return texto

def extraer_texto_del_archivo(ruta : Path):
    extension = ruta.suffix.lower()
    texto_extraido = ""

    try:
        # --- Leer PDF ---
        if extension == '.pdf':
            with fitz.open(ruta) as doc:
                # Leemos solo las primeras páginas para eficiencia
                for pagina in doc.pages(0, 3): 
                    texto_extraido += pagina.get_text()

        # --- Leer WORD (.docx) ---
        elif extension == '.docx':
            try:
                doc = docx.Document(ruta)
                parrafos = [p.text for p in doc.paragraphs[:30]]
                texto_extraido = "\n".join(parrafos)
            except Exception:
                texto_extraido = leer_docx_raw(ruta)

        # --- Leer POWERPOINT (.pptx) ---
        elif extension == '.pptx':
            try:
                prs = Presentation(ruta)
                # Leemos solo las primeras 10 diapositivas para no saturar
                for i, slide in enumerate(prs.slides[:10]):
                    for shape in slide.shapes:
                        if hasattr(shape, "text"):
                            texto_extraido += shape.text + " "
            except Exception:
                texto_extraido = leer_pptx_raw(ruta)

        # --- Leer EXCEL (.xlsx) ---
        elif extension == '.xlsx':
            # data_only=True para leer el resultado de fórmulas, no la fórmula en sí
            wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
            sheet = wb.active # Leemos la hoja principal
            # Leemos las primeras 50 filas y 10 columnas
            for row in sheet.iter_rows(max_row=50, max_col=10, values_only=True):
                fila_texto = " ".join([str(cell) for cell in row if cell is not None])
                texto_extraido += fila_texto + " "

    except Exception as e:
        print(f"Error al leer {ruta.name}: {e}")

    return texto_extraido.lower().strip()