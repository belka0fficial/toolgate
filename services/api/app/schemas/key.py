from pydantic import BaseModel

class KeyCreate(BaseModel):
    key_alias: str
    provider: str
    value: str
