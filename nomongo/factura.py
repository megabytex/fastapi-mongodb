import json
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()
datos_diccio = []

# Objeto FACTURA
class factura(BaseModel):
    fecha:str
    codigovehiculo:str
    descripcionvehiculo:str
    valorvehiculo:str
    impuestos:str
    valortotal:str

@app.get("/select-factura")
def mostrar_factura():
    readDatosDiccio()
    return datos_diccio

@app.post("/insert-factura") 
async def guardar_factura(datos:factura):
    readDatosDiccio()
    encode_datos = jsonable_encoder(datos)
    datos_diccio.append(encode_datos)
    writeDatosDiccio()
    return {"Mensaje":"Registro almacenado"}

@app.put("/update-factura") 
def actualizar_factura(datos:factura):
    print(datos)
    readDatosDiccio()
    estado = False
    id = 0
    for item in datos_diccio:
        if item["cedula"] == datos.cedula:
            datos_diccio[id]["nombre"] = datos.nombre
            datos_diccio[id]["apellido"] = datos.apellido
            datos_diccio[id]["telefono"] = datos.telefono
            datos_diccio[id]["correo"] = datos.correo
            datos_diccio[id]["direccionenvio"] = datos.direccionenvio
            writeDatosDiccio()
            estado = True
            break 
        id += 1

    if estado == True:
        return {"Mensaje": "Registro de factura actualizado"}
    else:
        return {"Mensaje": "Registro de factura no encontrado"}

@app.delete("/delete-factura")
def eliminar_factura(datos:factura):
    print(datos)
    readDatosDiccio()
    id = 0
    estado = False
    for item in datos_diccio:
        if item["cedula"] == datos.cedula:
            datos_diccio.pop(id)
            estado = True
            writeDatosDiccio()
            break
        id += 1
    if estado==True:
        return {"Mensaje": "Registro de factura eliminado"}
    else:
        return {"Mensaje": "Registro de factura no encontrado"}

# abro archivo json y convierto en dicionario
def readDatosDiccio():
    fichero = open("factura.json", "r")
    global datos_diccio
    datos_diccio = json.loads(fichero.read())
    fichero.close()

def writeDatosDiccio():
    fichero = open("factura.json", "w")
    #convierto diccionario a archivo Json con identacion
    forWrite = json.dumps(datos_diccio, indent=2)
    fichero.write(forWrite)
    fichero.close()
