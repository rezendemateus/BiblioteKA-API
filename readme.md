# BiblioteKA

## Primeiros passos para usar a API

1. Crie seu ambiente virtual:

```bash
python -m venv venv
```

2. Ative seu venv:

```bash
# linux:
source venv/bin/activate

# windows:
.\venv\Scripts\activate
```

3. Instale os pacotes que estão no arquivo `requirements.txt`:

```bash
pip install -r requirements
```

4. Faça uma cópia do arquivo `.env.example` com o nome `.env` e preencha os valores das variáveis de ambiente. Devem ficar os 2 arquivos na raiz do projeto dessa forma:

```
BiblioteKA-API
├── .env
└── .env.example
```

5. Crie um banco de dados no postgreSQL com o mesmo nome que você adicionou no arquivo `.env`. Então persista as tabelas no banco de dados dessa forma:

```bash
python manage.py migrate
```

6. Agora é só rodar o servidor e começar a usar a API:

```bash
python manage.py runserver
```
