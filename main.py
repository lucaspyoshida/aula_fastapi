from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from metar import lermetar



app = FastAPI(
 title="Aula",
 description="description",
 summary="API desenvolvida durante a aula de Construção de APIs para IA",
 version="0.1",
 terms_of_service="http://example.com/terms/",
 contact={
 "name": "Rogério Rodrigues Carvalho",
 "url": "http://github.com/rogerior/",
 "email": "rogerior@ufg.br",
 },
 license_info={
 "name": "Apache 2.0",
 "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
 },    
)

@app.get("/teste")
def read_root():
    return {"Hello": "World"}

@app.get(
 path="/soma/{numero1}/{numero2}",
 summary="Soma dois números inteiros",
 description="Recebe dois números inteiros e retorna a soma",
 tags=["Operações matemáticas"]      
)
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

@app.post(
 path="/soma/{numero1}/{numero2}",
 summary="Soma dois números inteiros",
 description="Recebe dois números inteiros e retorna a soma",
 tags=["Operações matemáticas"]        
)
def soma_formato3(numeros: Numeros):    
    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}

class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"

class OperacaoMatematica(BaseModel):
    numero1: int
    numero2: int
    operacao: TipoOperacao

 
    
@app.post("/operacao_matematica")
def operacao_matematica(operacao_dados: OperacaoMatematica):
    if operacao_dados.operacao == TipoOperacao.soma:
        resultado = operacao_dados.numero1 + operacao_dados.numero2
    elif operacao_dados.operacao == TipoOperacao.subtracao:
        resultado = operacao_dados.numero1 - operacao_dados.numero2
    elif operacao_dados.operacao == TipoOperacao.multiplicacao:
        resultado = operacao_dados.numero1 * operacao_dados.numero2
    elif operacao_dados.operacao == TipoOperacao.divisao:
        resultado = operacao_dados.numero1 / operacao_dados.numero2
    return {"resultado": resultado} 

class DadosMetar(BaseModel):
    metar:str
    key: str


key = "d005ff24-81ac-41ea-b89d-6a5a3e460aa5"

@app.post("/metar")
def metar(dados_metar: DadosMetar):
    if dados_metar.key == key:
        res = lermetar(dados_metar.metar)
        return res
    else:
        return {"error": "Chave de acesso inválida"}
