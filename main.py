
from fastapi import FastAPI, Depends
from utils import commom_verificacao_api_token
from routers import metar,definir



app = FastAPI(
 title="Aula",
 description="description",
 summary="API desenvolvida durante a aula de Construção de APIs para IA",
 version="0.1",
 terms_of_service="http://example.com/terms/",
 contact={
 "name": "Lucas Pacheco Yoshida",
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