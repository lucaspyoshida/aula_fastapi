from fastapi import APIRouter
from models import DadosMetar, MetarData
from metar import lermetar

router = APIRouter()

@router.post("/metar/v1", response_model = MetarData)
def metar(dados_metar: DadosMetar):
    """
    Processa uma string METAR e retorna os dados decodificados.

    Args:
        dados_metar (DadosMetar): Objeto contendo a string METAR e a chave de acesso.

    Returns:
        dict: Dados decodificados do METAR ou mensagem de erro se a chave for inválida.
    """
    res = lermetar(dados_metar.metar)
    return res
