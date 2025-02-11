
from pydantic import BaseModel
from typing import List, Optional

class DadosMetar(BaseModel):
    metar: str
    
class Vento(BaseModel):
    direcao: str
    velocidade: str
    variacao: Optional[str] = None  # Pode ser None se não houver variaçã
    
class MetarData(BaseModel):
    tipo: str
    estacao: str
    data_hora: str
    vento: Vento
    visibilidade: str
    nuvens: List[str]
    temperatura: str
    ponto_de_orvalho: str
    pressao: str
    texto: str