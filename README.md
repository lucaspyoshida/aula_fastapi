# Aula FastAPI

Este é um projeto de exemplo utilizando FastAPI.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/aula_fastapi.git
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
    uvicorn main:app --reload
    ```

2. Acesse a documentação interativa da API:
    - Abra o navegador e vá para `http://127.0.0.1:8000/docs`

## Estrutura do Projeto

- `main.py`: Arquivo principal da aplicação FastAPI.
- `requirements.txt`: Arquivo com as dependências do projeto.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob os termos da licença MIT.