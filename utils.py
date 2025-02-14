from dotenv import load_dotenv
import os
from openai import OpenAI
import logging
from fastapi import HTTPException

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.deepseek.com")

def obter_logger_e_configuracao():
    """
    Configura o logger padrão para o nível de informação e formato especificado.

    Retorna:
        logging.Logger: Um objeto de logger com as configurações padrões.
    """
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
    )
    logger = logging.getLogger("fastapi")
    return logger

def commom_verificacao_api_token(api_token: str):
    """
    Verifica se o token da API fornecido é válido.

    Args:
        api_token (str): O token da API a ser verificado.

    Raises:
        HTTPException: Se o token da API for inválido, uma exceção HTTP 401 é levantada com a mensagem "Token inválido".
    """
    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    
def chamar_llm(messages):
    """
    Chama o modelo de linguagem (LLM) para gerar uma resposta com base nas mensagens fornecidas.

    Args:
        messages (list): Uma lista de mensagens para enviar ao modelo de linguagem.

    Returns:
        str: A resposta gerada pelo modelo de linguagem.
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False,
        temperature=0
    )
    resposta = response.choices[0].message.content
    return resposta
    