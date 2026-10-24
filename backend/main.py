import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL não configurada. Crie backend/.env a partir de .env.example."
    )

# Normaliza URLs PostgreSQL que podem ser fornecidas pelo provedor.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Contato(Base):
    __tablename__ = "contatos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    telefone: Mapped[str] = mapped_column(String(30), nullable=False)


class ContatoEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    telefone: str = Field(min_length=8, max_length=30)


class ContatoSaida(ContatoEntrada):
    id: int
    model_config = ConfigDict(from_attributes=True)


def get_db():
    with Session(engine) as db:
        yield db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API de Contatos",
    description="API REST para cadastrar, consultar, atualizar e excluir contatos.",
    version="1.0.0",
    lifespan=lifespan,
)

origens = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    origens.append(frontend_url.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def inicio():
    return {"mensagem": "API de Contatos funcionando!"}


@app.post(
    "/contatos/",
    response_model=ContatoSaida,
    status_code=status.HTTP_201_CREATED,
)
def criar_contato(dados: ContatoEntrada, db: Session = Depends(get_db)):
    contato = Contato(**dados.model_dump())
    db.add(contato)
    db.commit()
    db.refresh(contato)
    return contato


@app.get("/contatos/", response_model=list[ContatoSaida])
def listar_contatos(db: Session = Depends(get_db)):
    return db.scalars(select(Contato).order_by(Contato.id)).all()


@app.get("/contatos/{contato_id}", response_model=ContatoSaida)
def buscar_contato(contato_id: int, db: Session = Depends(get_db)):
    contato = db.get(Contato, contato_id)
    if contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return contato


@app.put("/contatos/{contato_id}", response_model=ContatoSaida)
def atualizar_contato(
    contato_id: int,
    dados: ContatoEntrada,
    db: Session = Depends(get_db),
):
    contato = db.get(Contato, contato_id)
    if contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")

    for campo, valor in dados.model_dump().items():
        setattr(contato, campo, valor)

    db.commit()
    db.refresh(contato)
    return contato


@app.delete("/contatos/{contato_id}")
def excluir_contato(contato_id: int, db: Session = Depends(get_db)):
    contato = db.get(Contato, contato_id)
    if contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")

    db.delete(contato)
    db.commit()
    return {"mensagem": "Contato excluído com sucesso"}
