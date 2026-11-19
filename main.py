from fastapi import FastAPI, Form #importamos la libreria de fastapi
from fastapi.staticfiles import StaticFiles # util para archivos estaticos como img,html y css
from fastapi.responses import RedirectResponse

app = FastAPI() #creamos la app y la declaramos

#parte donde se va a hacer el envio del form

@app.post("/contacto")
def contacto(
    nombre: str = Form(...),
    correo: str = Form(...),
    mensaje: str = Form(...)
):
    print("Nuevo mensaje:", nombre, correo, mensaje)
    return RedirectResponse("/?enviado=ok#contacto", status_code=303)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
