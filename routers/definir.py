import sys
import os

# Adiciona o diretório pai ao sys.path para que o Python possa encontrar o módulo utils.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from utils import chamar_llm, obter_logger_e_configuracao, extrair_json
from models import ListaDefinicoes, DadosDefinir
from fastapi import APIRouter
import json
from fastapi import HTTPException

router = APIRouter()
logger = obter_logger_e_configuracao()


@router.post(
    "/definir/v1",
    response_model=ListaDefinicoes,
    summary="Definir termos aeronáuticos",
    description="Recebe um termo aeronáutico e retorna suas definições em diferentes contextos.",
    tags=["Definições"],
)
def definir(dados: DadosDefinir):
    """
    Define um termo solicitado.

    Args:
      dados (DadosDefinir): Objeto contendo o termo a ser definido.

    Returns:
      str: Definição do termo solicitado de acordo com um contexto.
    """
    logger.info(f"Termo solicitado: {dados.termo}")
    res = definirtermo(dados.termo)
    return res


orientacoes = """
Você é um especialista aeronáutico com profundo conhecimento técnico e experiência prática no setor da aviação. Você domina a terminologia e os múltiplos contextos nos quais termos e siglas podem ser aplicados, como meteorologia, operações e aeródromos.

- **Características e Estilo de Resposta:**
  - **Clareza e Precisão:** Você sempre fornece definições objetivas, concisas e tecnicamente corretas.
  - **Formato Estrito:** Você responde exclusivamente em JSON, obedecendo à estrutura:

    [
      { "contexto": "xxxx", "significado": "xxxx" },
      { "contexto": "xxxx", "significado": "xxxx" }
    ]

  - **Contexto:** Cada objeto que você retorna possui o campo "contexto", que deve ser formado por **apenas uma palavra**, representando a área de aplicação do termo (por exemplo:     "meteorologia","aerodromo","operacoes","navegacao", "manutencao","seguranca","comunicacoes","regulamentacao").
  - **Adaptabilidade:** Se um termo ou sigla tiver múltiplos significados em diferentes áreas, você retornará uma entrada para cada contexto relevante, mantendo a consistência e a clareza.

- **Propósito:**
  Ao receber uma palavra ou sigla, você interpreta o termo e retorna as definições associadas a cada contexto de uso dentro do universo aeronáutico, garantindo que o usuário obtenha uma compreensão completa e segmentada da terminologia.

Orientação mais importante: retorne apenas o JSON, não coloque nenhuma informação antes ou após o JSON de retorno.

"""


def definirtermo(termo):
    """
    Define o significado de um termo fornecido.
    Args:
      termo (str): O termo que se deseja definir.
    Returns:
      dict: Um dicionário contendo as definições do termo.
    """
    messages = [
        {"role": "system", "content": orientacoes},
        {"role": "user", "content": "Dê o significado de: " + termo},
    ]

    resposta = chamar_llm(messages)
    try:
        resposta = extrair_json(resposta)
        data = json.loads(resposta)
        print(len(data))
        if not isinstance(data, list) or not all(
            "contexto" in item and "significado" in item for item in data
        ):
            raise ValueError
        if len(data) == 0:
            raise HTTPException(status_code=400, detail="Nenhuma definição encontrada.")
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=400, detail="Definição não encontrada.")
    return {"definicoes": data}
