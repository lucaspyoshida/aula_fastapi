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
