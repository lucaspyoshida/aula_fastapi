
from fastapi import FastAPI, Depends
from utils import commom_verificacao_api_token
from routers import metar,definir



app = FastAPI(
 title="Auxílio Aeronáutico",
 description="API destinada a interpretação de METAR e busca por definições de termos aeronáuticos.",
 summary="API desenvolvida durante a aula de Construção de APIs para IA.",
 version="0.1",
 contact={
 "name": "Lucas Yoshida",
 "url": "http://github.com/lucaspyoshida/",
 "email": "lucaspyoshida@hotmail.com",
 },
 license_info={
 "name": "Apache 2.0",
 "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
 },    
 dependencies=[Depends(commom_verificacao_api_token)],
)


app.include_router(metar.router)

app.include_router(definir.router)