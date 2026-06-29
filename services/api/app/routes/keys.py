from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.core.db import SessionLocal
from app.models.key import Key
from app.schemas.key import KeyCreate
from app.services.crypto import encrypt_value

router = APIRouter(prefix="/keys", tags=["keys"])

@router.post("")
def create_key(payload: KeyCreate):
    db = SessionLocal()
    try:
        row = Key(
            key_alias=payload.key_alias,
            provider=payload.provider,
            encrypted_value=encrypt_value(payload.value),
        )
        db.add(row)
        db.commit()
        return {"status": "ok", "key_alias": payload.key_alias}
    finally:
        db.close()

@router.get("")
def list_keys():
    db = SessionLocal()
    try:
        rows = db.execute(select(Key)).scalars().all()
        return [{"key_alias": k.key_alias, "provider": k.provider} for k in rows]
    finally:
        db.close()

@router.get("/{key_alias}")
def get_key(key_alias: str):
    db = SessionLocal()
    try:
        row = db.get(Key, key_alias)
        if not row:
            raise HTTPException(404, "Key not found")
        return {"key_alias": row.key_alias, "provider": row.provider}
    finally:
        db.close()
