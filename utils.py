from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.deepseek.com")


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
  response = client.chat.completions.create(
      model="deepseek-chat",
      messages=messages,
      stream=False,
      temperature=0
  )
  resposta = response.choices[0].message.content
  return resposta
    