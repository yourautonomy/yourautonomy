from fastapi import FastAPI, Form #importamos la libreria de fastapi
from fastapi.staticfiles import StaticFiles # util para archivos estaticos como img,html y css
from fastapi.responses import RedirectResponse

app = FastAPI() #creamos la app y la declaramos

#parte donde se va a hacer el envio del form

@app.post("/contacto")
def contacto(
    nombre: str = Form(...,max_length=100),
    correo: str = Form(...,max_length=150),
    mensaje: str = Form(...,max_length=200),
    website: str = Form("")
):
    if website:
        return  RedirectResponse("/?enviado=ok#contacto", status_code=303)
    nombre = nombre.strip()
    correo = correo.strip()
    mensaje = mensaje.strip()

    if not nombre or not mensaje or "@" not in correo:
        return RedirectResponse("/?enviado=error#contacto", status_code=303)
        print("Nuevo mensaje:", nombre, correo, mensaje)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
