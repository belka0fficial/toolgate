from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.core.db import SessionLocal
from app.models.key import Key
from app.schemas.key import KeyCreate, KeyUpdate
from app.services.crypto import encrypt_value, decrypt_value

router = APIRouter(prefix="/keys", tags=["keys"])

@router.post("")
def create_key(payload: KeyCreate):
    db = SessionLocal()
    try:
        existing = db.get(Key, payload.key_alias)
        if existing:
            raise HTTPException(409, "Key already exists")

        rec = Key(
            key_alias=payload.key_alias,
            provider=payload.provider,
            encrypted_value=encrypt_value(payload.value),
        )
        db.add(rec)
        db.commit()
        return {"status": "ok", "key_alias": payload.key_alias}
    finally:
        db.close()

@router.patch("/{key_alias}")
def update_key(key_alias: str, payload: KeyUpdate):
    db = SessionLocal()
    try:
        rec = db.get(Key, key_alias)
        if not rec:
            raise HTTPException(404, "Key not found")

        if payload.provider is not None:
            rec.provider = payload.provider
        if payload.value is not None:
            rec.encrypted_value = encrypt_value(payload.value)

        db.commit()
        return {"status": "ok", "key_alias": key_alias}
    finally:
        db.close()

@router.get("")
def list_keys():
    db = SessionLocal()
    try:
        rows = db.execute(select(Key)).scalars().all()
        return [{"key_alias": r.key_alias, "provider": r.provider} for r in rows]
    finally:
        db.close()

@router.get("/{key_alias}")
def get_key(key_alias: str):
    db = SessionLocal()
    try:
        rec = db.get(Key, key_alias)
        if not rec:
            raise HTTPException(404, "Key not found")
        return {
            "key_alias": rec.key_alias,
            "provider": rec.provider,
            "value": decrypt_value(rec.encrypted_value),
        }
    finally:
        db.close()
