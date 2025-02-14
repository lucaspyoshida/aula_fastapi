# Aula FastAPI

A API "Auxílio Aeronáutico" desenvolvida com FastAPI é projetada para interpretar mensagens METAR, definir termos aeronáuticos e transcrever frases complexas em termos simples. Ela oferece endpoints para processar e decodificar mensagens METAR, fornecendo dados estruturados em formato JSON, além de permitir a busca por definições de termos aeronáuticos em diferentes contextos e a transcrição de frases técnicas para uma linguagem mais acessível. A API é útil para profissionais da aviação e entusiastas que precisam de assistência na interpretação de informações meteorológicas e terminologia aeronáutica.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/lucaspyoshida/aula_fastapi
    cd aula_fastapi
    ```

2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    ```

3. Ative o ambiente virtual:
    - No Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - No Linux/MacOS:
        ```bash
        source venv/bin/activate
        ```

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5. Preencha as keys conforme o exemplo em `.env.sample` e renomeie o arquivo para `.env`.

## Executando a API

1. Inicie o servidor FastAPI:
    ```bash
    fastapi run .\main.py
    ```

2. Acesse a documentação interativa da API:
    - Abra o navegador e vá para `http://127.0.0.1:8000/docs`

## Estrutura do Projeto

- `main.py`: Arquivo principal da aplicação FastAPI.
- `requirements.txt`: Arquivo com as dependências do projeto.
- `models.py`: Define os modelos de dados utilizados pela aplicação.
- `utils.py`: Funções utilitárias usadas na aplicação.
- `/routers/definir.py`: Função para definir termo aeronáutico
- `/routers/metar.py`: Função para interpretar METAR
- `/routers/frase.py`: Função para transcrever uma frase de termos complexos em termos simples

