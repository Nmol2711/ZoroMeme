import platform

def bind_mouse_wheel(widget, scrollable_frame):
    def on_mouse_wheel(event):
        try:
            canvas = getattr(scrollable_frame, "_parent_canvas", getattr(scrollable_frame, "_canvas", None))
            if not canvas:
                return

            # --- VALIDACIÓN DE ALTURA ---
            # Obtenemos la altura del contenido (bbox) y la altura del frame (winfo_height)
            bbox = canvas.bbox("all")
            if bbox:
                altura_contenido = bbox[3] - bbox[1]
                altura_visible = canvas.winfo_height()

                # Si el contenido es más pequeño que lo que se ve, NO scrollear
                if altura_contenido <= altura_visible:
                    return
            # ----------------------------

            if platform.system() == "Linux":
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
            else:
                if event.delta:
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    if platform.system() == "Linux":
        widget.bind("<Button-4>", on_mouse_wheel, add="+")
        widget.bind("<Button-5>", on_mouse_wheel, add="+")
    else:
        widget.bind("<MouseWheel>", on_mouse_wheel, add="+")

    for child in widget.winfo_children():
        bind_mouse_wheel(child, scrollable_frame)