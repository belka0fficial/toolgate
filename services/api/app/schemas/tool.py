from pydantic import BaseModel
from typing import Any

class ToolCreate(BaseModel):
    tool_id: str
    provider: str
    action: str
    source_type: str
    executor_type: str
    key_alias: str | None = None
    config_json: dict[str, Any] = {}
    input_schema_json: dict[str, Any] = {}
    output_schema_json: dict[str, Any] = {}

class ToolEdit(BaseModel):
    key_alias: str | None = None
    config_json: dict[str, Any] | None = None
    input_schema_json: dict[str, Any] | None = None
    output_schema_json: dict[str, Any] | None = None

class ToolExecute(BaseModel):
    caller_id: str
    tool_id: str
    arguments: dict[str, Any] = {}
