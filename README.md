# ToolGate

ToolGate is a local self-hosted control plane for agent tools and keys.

## Current features
- key storage
- tool registry
- tool execution
- remove / restore
- audit log
- untrusted output wrapping
- basic security classifier

## Stack
- FastAPI
- Postgres
- Docker

## Dev run

### 1. Start Postgres
docker compose up -d

### 2. Run API
cd services/api
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010

## API docs
- http://localhost:8010/docs
