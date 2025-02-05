from dotenv import load_dotenv
from openai import OpenAI
import os
from pydantic import BaseModel
from typing import List, Optional
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("api_key"), base_url="https://api.deepseek.com")

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
  response = client.chat.completions.create(
      model="deepseek-chat",
      messages=[
          {"role": "system", "content": orientacoes},
          {"role":"assistant","content":exemplo},
          {"role": "user", "content": "Analise a mensagem a seguir: " + metar},
      ],
      stream=False,
      temperature=0
  )
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

  resposta = response.choices[0].message.content

  try:
      data = json.loads(resposta)
      metar_data = MetarData(**data)
      return metar_data.model_dump_json(indent=2)
  except Exception as e:
      return "Erro de validação:", e



# metarteste = "METAR SBBR 052000Z 05008KT 360V100 9999 SCT030 FEW045TCU SCT070 29/15 Q1015="

# print(lermetar(metarteste))
