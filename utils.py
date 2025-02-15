from dotenv import load_dotenv
import os
from openai import OpenAI
import logging
from fastapi import HTTPException

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.deepseek.com")
client = OpenAI(api_key=os.getenv("API_KEY"))


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
    # response = client.chat.completions.create(
    #     model="deepseek-chat",
    #     messages=messages,
    #     stream=False,
    #     temperature=0
    # )
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18", messages=messages, stream=False, temperature=0
    )
    resposta = response.choices[0].message.content
    logger = obter_logger_e_configuracao()
    logger.info(f"Resposta LLM: {resposta}")
    return resposta


def extrair_json(texto):
    # Procura a primeira ocorrência de '{' ou '['
    pos_objeto = texto.find("{")
    pos_array = texto.find("[")

    # Se nenhum deles for encontrado, retorna None
    if pos_objeto == -1 and pos_array == -1:
        return None

    # Determina qual posição vem primeiro (a que for válida)
    if pos_objeto == -1:
        inicio = pos_array
    elif pos_array == -1:
        inicio = pos_objeto
    else:
        inicio = min(pos_objeto, pos_array)

    # Define os delimitadores de abertura e fechamento
    if texto[inicio] == "{":
        abertura = "{"
        fechamento = "}"
    elif texto[inicio] == "[":
        abertura = "["
        fechamento = "]"
    else:
        return None

    contador = 0
    for i in range(inicio, len(texto)):
        if texto[i] == abertura:
            contador += 1
        elif texto[i] == fechamento:
            contador -= 1
            # Quando o contador retorna a zero, encontramos o fechamento correspondente
            if contador == 0:
                return texto[inicio : i + 1]
    return None
