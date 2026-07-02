from pydantic import BaseModel

class KeyCreate(BaseModel):
    key_alias: str
    provider: str
    value: str

class KeyUpdate(BaseModel):
    provider: str | None = None
    value: str | None = None
