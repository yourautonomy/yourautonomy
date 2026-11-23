from fastapi import FastAPI, Form                    # FastAPI y Form para leer formularios
from fastapi.responses import RedirectResponse       # para regresar al visitante a la página
from fastapi.staticfiles import StaticFiles          # para servir html, css e imágenes
from google.cloud import firestore                   # para guardar los mensajes

app = FastAPI()  # creamos la app


# ---------- Conexión a Firestore ----------
# Se conecta solo la primera vez que se necesita.
# Así la página carga aunque no haya credenciales (por ejemplo, en Docker local).
_db = None

def get_db():
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db


# ---------- Ruta de salud ----------
# Sirve para revisar rápido que el servidor está vivo: /health
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Formulario de contacto ----------
@app.post("/contacto")
def contacto(
    nombre: str = Form(..., max_length=100),
    correo: str = Form(..., max_length=150),
    mensaje: str = Form(..., max_length=2000),
    website: str = Form(""),  # trampa anti-spam: debe venir vacía
):
    # Si la trampa trae algo, es un bot: fingimos éxito y no guardamos nada
    if website:
        return RedirectResponse("/?enviado=ok#contacto", status_code=303)

    # Quitamos espacios al inicio y al final
    nombre = nombre.strip()
    correo = correo.strip()
    mensaje = mensaje.strip()

    # Validamos que no vengan vacíos y que el correo tenga @
    if not nombre or not mensaje or "@" not in correo:
        return RedirectResponse("/?enviado=error#contacto", status_code=303)

    # Guardamos en Firestore, en la colección "contactos"
    try:
        get_db().collection("contactos").add({
            "nombre": nombre,
            "correo": correo,
            "mensaje": mensaje,
            "fecha": firestore.SERVER_TIMESTAMP,  # la hora la pone Google
        })
        print("Mensaje guardado de:", correo)
    except Exception as e:
        print("Error guardando en Firestore:", e)
        return RedirectResponse("/?enviado=error#contacto", status_code=303)

    return RedirectResponse("/?enviado=ok#contacto", status_code=303)


# ---------- Archivos estáticos ----------
# SIEMPRE AL FINAL: todo lo que no sea una ruta de arriba se busca en la carpeta static
app.mount("/", StaticFiles(directory="static", html=True), name="static")