import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="SaaS Jurídico - Automação de Contestação", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str
    senha: str


class ContestacaoRequest(BaseModel):
    tipo_acao: str = Field(..., min_length=3)
    fatos: str = Field(..., min_length=10)
    pedidos_autor: str = Field(..., min_length=5)
    nome_parte_autora: Optional[str] = None
    nome_parte_re: Optional[str] = None


class ContestacaoResponse(BaseModel):
    contestacao: str
    criado_em: datetime


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/login")
def login(payload: LoginRequest) -> dict[str, str]:
    if not payload.email or not payload.senha:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    return {
        "token": "demo-token",
        "tipo": "bearer",
        "mensagem": "MVP: substitua por autenticação JWT em produção.",
    }


def _build_prompt(payload: ContestacaoRequest) -> str:
    return f"""
Você é um advogado brasileiro especialista em contestações cíveis.

Regras obrigatórias:
- Não inventar jurisprudência nem fatos.
- Não alterar nomes ou dados das partes.
- Usar linguagem jurídica formal brasileira.
- Gerar uma peça estruturada com: síntese dos fatos, preliminares (se houver), mérito, pedidos e requerimentos finais.

Dados da ação:
- Tipo de ação: {payload.tipo_acao}
- Parte autora: {payload.nome_parte_autora or "Não informado"}
- Parte ré: {payload.nome_parte_re or "Não informado"}
- Fatos narrados pela ré: {payload.fatos}
- Pedidos da inicial: {payload.pedidos_autor}
""".strip()


@app.post("/gerar-contestacao", response_model=ContestacaoResponse)
def gerar_contestacao(payload: ContestacaoRequest) -> ContestacaoResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY não configurada. Defina no ambiente antes de chamar este endpoint.",
        )

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=[{"role": "user", "content": _build_prompt(payload)}],
            temperature=0.2,
        )
        output = response.output_text.strip()
        if not output:
            raise ValueError("Resposta vazia do modelo")

        return ContestacaoResponse(contestacao=output, criado_em=datetime.utcnow())
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Erro ao gerar contestação: {exc}") from exc
