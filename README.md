# SaaS Jurídico – Automação de Contestação

MVP com **FastAPI + OpenAI + HTML/Bootstrap** para gerar minutas de contestação jurídica.

## 1) Visão geral

O sistema inclui:
- Login básico de advogados (MVP demonstrativo)
- Geração automática de contestação
- Fluxo com agente jurídico (prompt estruturado)
- Segurança mínima de configuração (chave por variável de ambiente)

## 2) Arquitetura

- **Backend:** Python, FastAPI, OpenAI API
- **Frontend:** HTML + Bootstrap + JS
- **Infra recomendada:** Render/Railway/VPS com HTTPS

## 3) Passo a passo de execução

### 3.1 Pré-requisitos
- Python 3.10+

### 3.2 Configurar backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.3 Configurar chave OpenAI
```bash
cp .env.example .env
```
Edite o `.env` e preencha:
```env
OPENAI_API_KEY=sk-proj-sua-chave-real
OPENAI_MODEL=gpt-4.1-mini
```

### 3.4 Rodar API
```bash
uvicorn main:app --reload --port 8000
```

Acesse: `http://127.0.0.1:8000/docs`

### 3.5 Rodar frontend
Em outro terminal:
```bash
cd frontend
python -m http.server 5500
```
Abra: `http://127.0.0.1:5500`

## 4) Endpoints principais

- `GET /health` → status do serviço
- `POST /login` → login MVP
- `POST /gerar-contestacao` → gera contestação via OpenAI

Exemplo de payload para `/gerar-contestacao`:
```json
{
  "tipo_acao": "Ação de cobrança",
  "fatos": "O réu contesta o valor cobrado por ausência de prova documental suficiente.",
  "pedidos_autor": "Condenação ao pagamento integral + custas.",
  "nome_parte_autora": "Empresa XPTO",
  "nome_parte_re": "João da Silva"
}
```

## 5) Segurança e boas práticas

- Nunca versionar `.env` com chave real.
- Usar HTTPS em produção.
- Adicionar autenticação JWT e hash de senha (próximo passo).
- Implementar rate limit por usuário/chave.
- Não armazenar prompts com dados sensíveis sem anonimização.

## 6) Próximos passos recomendados

- Persistência em PostgreSQL (histórico de documentos)
- Geração em DOCX/PDF
- Controle de plano mensal por escritório
- Trilhas de auditoria e logs seguros
