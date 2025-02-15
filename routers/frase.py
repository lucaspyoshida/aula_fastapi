# import sys
# import os

# # Adiciona o diretório pai ao sys.path para que o Python possa encontrar o módulo utils.py
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import chamar_llm, obter_logger_e_configuracao, extrair_json
from models import ResFrase, DadosFrase
from fastapi import APIRouter
import json
from fastapi import HTTPException

router = APIRouter()
logger = obter_logger_e_configuracao()


@router.post(
    "/frase/v1",
    response_model=ResFrase,
    summary="Transcreve uma frase com termos aeronáutico em termos simples",
    description="Transcreve em termos simples frases com termos complexos.",
    tags=["Definições"],
)
def frase(dados: DadosFrase):
    """
    Transcreve em termos simples frases com termos complexos.

    Args:
      frase (DadosFrase): Frase a ser transcrita.

    Returns:
      str: Transcrição da frase em termos simples.
    """
    logger.info(f"Frase solicitada: {dados.frase}")
    res = transcrever(dados.frase)
    return res


orientacoes = """
Você é um especialista aeronáutico com profundo conhecimento técnico e experiência prática no setor da aviação. Você domina a terminologia e os múltiplos contextos nos quais termos e siglas podem ser aplicados, como meteorologia, operações e aeródromos.

- **Características e Estilo de Resposta:**
  - **Clareza e Precisão:** Você sempre fornece definições objetivas, concisas e tecnicamente corretas.
  - **Formato Estrito:** Você responde exclusivamente em JSON, obedecendo à estrutura:

    { "contexto": "xxxx", "transcrito": "xxxx" }

  - **Contexto:** Cada objeto que você retorna possui o campo "contexto", que deve ser formado por **apenas uma palavra**, representando a área de aplicação do termo (por exemplo: "meteorologia","aerodromo","operacoes","navegacao", "manutencao","seguranca","comunicacoes","regulamentacao").

- **Propósito:**
  Ao receber uma frase com termos aeronáuticos complexos ou siglas, você interpreta a frase e retorna a mesma em palavras mais simples, compreensível para um leigo, garantindo que o usuário obtenha uma compreensão completa e segmentada da terminologia.

Orientação mais importante: retorne apenas o JSON, não coloque nenhuma informação antes ou após o JSON de retorno. O retorno deve iniciar com "{" e terminar com "}"

Caso a frase fornecida não possa ser transcrita em termos simples, retornar um objeto vazio "{}".

"""


def transcrever(frase):
    """
    Define o significado de um termo fornecido.
    Args:
      termo (str): O termo que se deseja definir.
    Returns:
      dict: Um dicionário contendo as definições do termo.
    """
    messages = [
        {"role": "system", "content": orientacoes},
        {"role": "user", "content": "Transcreva a frase: " + frase},
    ]

    resposta = chamar_llm(messages)
    try:
        resposta = extrair_json(resposta)
        data = json.loads(resposta)
        if "contexto" not in data or "transcrito" not in data:
            raise HTTPException(
                status_code=400,
                detail="Erro ao processar a resposta do LLM. Verifique o formato informado.",
            )
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Erro ao processar a resposta do LLM. Verifique o formato informado.",
        )
    return data
