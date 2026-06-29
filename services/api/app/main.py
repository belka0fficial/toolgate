from fastapi import FastAPI
from app.core.db import Base, engine
from app.routes.tools import router as tools_router
from app.routes.keys import router as keys_router
from app.routes.audit import router as audit_router
from app.models import tool, key, audit

app = FastAPI(title="ToolGate")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(tools_router)
app.include_router(keys_router)

app.include_router(audit_router)
