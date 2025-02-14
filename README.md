# Aula FastAPI

Este é um projeto de exemplo utilizando FastAPI.

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

