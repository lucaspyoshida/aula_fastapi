import json
from utils import chamar_llm, obter_logger_e_configuracao
from fastapi import APIRouter
from models import DadosMetar, MetarData
from fastapi import HTTPException
import re

logger = obter_logger_e_configuracao()

router = APIRouter()

@router.post("/metar/v1", response_model = MetarData,
            summary="Processa uma mensagem METAR",
            description="Recebe uma string METAR, decodifica e retorna os dados estruturados em formato JSON.",
            tags=["Meteorologia"]
            )
def metar(dados_metar: DadosMetar):
  """
  Processa uma string METAR e retorna os dados decodificados.

  Args:
      dados_metar (DadosMetar): Objeto contendo a string METAR.

  Returns:
      dict: Dados decodificados do METAR e um texto interpretando a mensagem.
      
  Raises:
    HTTPException: Se a string fornecida não contiver a palavra 'METAR'.
    HTTPException: Se o formato do METAR for inválido (não começar com um identificador ICAO de 4 letras).      
    """
  logger.info(f"METAR enviado: {dados_metar.metar}")
  if "METAR" not in dados_metar.metar:
    raise HTTPException(status_code=400, detail="A string fornecida não contém a palavra 'METAR'.")

  padrao_icao = r"\s[A-Z]{4}\s"  # Quatro letras maiúsculas seguidas de espaço

  if not re.search(padrao_icao, dados_metar.metar):
      raise HTTPException(status_code=400, detail="Código ICAO não encontrado.")


  res = lermetar(dados_metar.metar)
  return res



orientacoes = """
Você é um assistente especialista em meteorologia e interpretação de mensagens METAR. Sua tarefa é analisar uma mensagem METAR, extrair os principais elementos e retornar os dados em formato JSON, com uma chave para cada informação.

Considere os seguintes campos e suas descrições:

- **tipo**: Indica se a mensagem é um METAR (ou SPECI, se aplicável).
- **estacao**: Código ICAO da estação meteorológica.
- **data_hora**: Data e hora da observação (formato: DDHHMMZ).
- **vento**: Informações sobre a direção e a velocidade do vento.
  - **direcao**: A direção do vento (em graus ou "VRB" se variável).
  - **velocidade**: Velocidade do vento (incluindo a unidade, por exemplo, "KT").
- **visibilidade**: Valor da visibilidade horizontal (em metros ou quilômetros).
- **nuvens**: Um array com as diferentes camadas de nuvens informadas, cada camada deve ser representada como string (por exemplo, "FEW049" ou "BKN080").
- **temperatura**: Temperatura do ar em °C.
- **ponto_de_orvalho**: Ponto de orvalho em °C.
- **pressao**: Pressão atmosférica (valor de QNH, em hPa).

Instruções:
1. Analise a mensagem METAR fornecida.
2. Extraia os dados correspondentes aos campos acima.
3. Retorne a resposta em formato JSON conforme o exemplo abaixo.
4. Caso um campo não esteja presente na mensagem, atribua o valor `null` ou uma indicação apropriada para aquele campo.
5. Retorne apenas o JSON, não coloque nenhuma informação antes ou após o JSON de retorno.
"""

exemplo = """
Exemplo de METAR:

METAR SBGR 052000Z 35006KT 9999 FEW049 BKN080 25/20 Q1014=

Saída esperada JSON:
{
  "tipo": "METAR",
  "estacao": "SBGR",
  "data_hora": "052000Z",
  "vento": {
    "direcao": "350",
    "velocidade": "06KT"
  },
  "visibilidade": "9999",
  "nuvens": ["FEW049", "BKN080"],
  "temperatura": "25",
  "ponto_de_orvalho": "20",
  "pressao": "1014",
  "texto": "Em SBGR, às 20:00Z do dia 05, vento de 350° a 06 nós, visibilidade acima de 10 km, algumas nuvens a 4.900 pés e céu parcialmente encoberto a 8.000 pés, temperatura de 25°C, ponto de orvalho a 20°C e pressão de 1014 hPa."
}
"""

def lermetar(metar):
  """
  Analisa uma mensagem METAR e retorna os dados estruturados.
  Args:
    metar (str): A mensagem METAR a ser analisada.
  Returns:
    MetarData: Um objeto contendo os dados estruturados da mensagem METAR.
    Em caso de erro de validação, retorna uma string com a mensagem de erro e a exceção.
  Exceções:
    Exception: Qualquer exceção que ocorra durante a análise da mensagem METAR.
  """
  messages=[
      {"role": "system", "content": orientacoes},
      {"role":"assistant","content":exemplo},
      {"role": "user", "content": "Analise a mensagem a seguir: " + metar},
  ]


  resposta = chamar_llm(messages)

  try:
      data = json.loads(resposta)
      metar_data = MetarData(**data)
      return metar_data
  except Exception as e:
      return "Erro de validação:", e
