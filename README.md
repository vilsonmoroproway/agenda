# Sistema de Contatos — FastAPI + PostgreSQL + HTML/JavaScript

Projeto didático com API REST em Python (FastAPI), persistência PostgreSQL e frontend em HTML, CSS e JavaScript puro.

## Estrutura

```text
sistema-contatos/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    └── index.html
```

## 1. Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL local (ou um banco PostgreSQL hospedado)
- Git, caso queira publicar no GitHub/Render

## 2. Configurar o backend local

Abra um terminal na pasta `backend`:

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `backend/.env` e configure `DATABASE_URL` para o seu PostgreSQL. Exemplo:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/contatos
FRONTEND_URL=http://127.0.0.1:5500
```

Crie previamente o banco `contatos` no PostgreSQL. Ajuste usuário, senha, host e porta conforme sua instalação.

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite `backend/.env` com a URL do PostgreSQL.

## 3. Executar a API

Ainda dentro da pasta `backend` e com o ambiente virtual ativado:

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000/
- Documentação interativa: http://127.0.0.1:8000/docs

A tabela `contatos` é criada automaticamente quando a API inicia, se ainda não existir.

## 4. Executar o frontend

Abra `frontend/index.html` usando a extensão Live Server do VS Code (porta padrão 5500). A constante `API_URL` no início do JavaScript deve apontar para `http://127.0.0.1:8000`.

Você também pode servir a pasta com Python:

```bash
python -m http.server 5500
```

Execute esse comando dentro de `frontend` e acesse http://127.0.0.1:5500.

## 5. Publicar no Render

### Banco PostgreSQL
1. Crie um PostgreSQL no painel do Render.
2. Copie a URL de conexão interna (Internal Database URL), se os serviços estiverem na mesma região.
3. Não publique credenciais no GitHub.

### API (Web Service)
1. Envie o projeto ao GitHub.
2. Crie um **Web Service** ligado ao repositório.
3. Configure `Root Directory` como `backend`.
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Adicione a variável `DATABASE_URL` com a URL do PostgreSQL.
7. Depois de publicar o frontend, configure `FRONTEND_URL` com a origem pública exata dele.

### Frontend (Static Site)
1. Crie um **Static Site** ligado ao mesmo repositório.
2. Configure `Root Directory` como `frontend`.
3. Deixe `Build Command` vazio.
4. Configure `Publish Directory` como `.`.
5. Em `frontend/index.html`, substitua `API_URL` pela URL pública real da API, sem barra final.
6. Faça commit e push dessa alteração. Confirme que `FRONTEND_URL` na API corresponde à URL pública do frontend.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/contatos/` | Lista contatos |
| GET | `/contatos/{id}` | Busca um contato |
| POST | `/contatos/` | Cadastra contato |
| PUT | `/contatos/{id}` | Atualiza contato |
| DELETE | `/contatos/{id}` | Exclui contato |

## Observações

- Este projeto é didático e não inclui autenticação/autorização.
- CORS não é um mecanismo de autenticação; restrinja a origem do frontend em produção.
- Para mudanças futuras no esquema do banco, prefira migrações com Alembic em vez de depender somente de `create_all()`.


