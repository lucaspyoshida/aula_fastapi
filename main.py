from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()

@app.get("/teste")
def read_root():
    return {"Hello": "World"}

@app.get("/soma/{numero1}/{numero2}")
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


@app.post("/soma_formato2")
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}

class Numeros(BaseModel):
    numero1: int
    numero2: int

@app.post("/soma_formato3")
def soma_formato3(numeros: Numeros):    
    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}