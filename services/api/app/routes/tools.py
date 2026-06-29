import json
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.core.db import SessionLocal
from app.models.tool import Tool
from app.models.key import Key
from app.models.audit import AuditLog
from app.schemas.tool import ToolCreate, ToolEdit, ToolExecute
from app.services.executor import execute_http_tool
from app.services.untrusted_wrapper import wrap_output
from app.services.security_classifier import classify_wrapped_output

router = APIRouter(prefix="/tools", tags=["tools"])

@router.post("")
def create_tool(payload: ToolCreate):
    db = SessionLocal()
    try:
        tool = Tool(
            tool_id=payload.tool_id,
            provider=payload.provider,
            action=payload.action,
            source_type=payload.source_type,
            executor_type=payload.executor_type,
            key_alias=payload.key_alias,
            config_json=json.dumps(payload.config_json),
            input_schema_json=json.dumps(payload.input_schema_json),
            output_schema_json=json.dumps(payload.output_schema_json),
        )
        db.add(tool)
        db.commit()
        return {"status": "ok", "tool_id": payload.tool_id}
    finally:
        db.close()

@router.get("")
def list_tools():
    db = SessionLocal()
    try:
        rows = db.execute(select(Tool).where(Tool.is_removed == False)).scalars().all()
        return [{"tool_id": t.tool_id, "provider": t.provider, "action": t.action, "source_type": t.source_type} for t in rows]
    finally:
        db.close()

@router.get("/removed")
def list_removed():
    db = SessionLocal()
    try:
        rows = db.execute(select(Tool).where(Tool.is_removed == True)).scalars().all()
        return [{"tool_id": t.tool_id, "remove_reason": t.remove_reason} for t in rows]
    finally:
        db.close()

@router.get("/{tool_id}")
def get_tool(tool_id: str):
    db = SessionLocal()
    try:
        tool = db.get(Tool, tool_id)
        if not tool:
            raise HTTPException(404, "Tool not found")
        return {
            "tool_id": tool.tool_id,
            "provider": tool.provider,
            "action": tool.action,
            "source_type": tool.source_type,
            "executor_type": tool.executor_type,
            "key_alias": tool.key_alias,
            "is_removed": tool.is_removed,
            "remove_reason": tool.remove_reason,
        }
    finally:
        db.close()

@router.patch("/{tool_id}")
def edit_tool(tool_id: str, payload: ToolEdit):
    db = SessionLocal()
    try:
        tool = db.get(Tool, tool_id)
        if not tool:
            raise HTTPException(404, "Tool not found")

        if payload.key_alias is not None:
            tool.key_alias = payload.key_alias
        if payload.config_json is not None:
            tool.config_json = json.dumps(payload.config_json)
        if payload.input_schema_json is not None:
            tool.input_schema_json = json.dumps(payload.input_schema_json)
        if payload.output_schema_json is not None:
            tool.output_schema_json = json.dumps(payload.output_schema_json)

        db.commit()
        return {"status": "ok", "tool_id": tool_id}
    finally:
        db.close()

@router.post("/{tool_id}/remove")
def remove_tool(tool_id: str):
    db = SessionLocal()
    try:
        tool = db.get(Tool, tool_id)
        if not tool:
            raise HTTPException(404, "Tool not found")
        tool.is_removed = True
        tool.remove_reason = "removed"
        db.commit()
        return {"status": "ok", "tool_id": tool_id}
    finally:
        db.close()

@router.post("/{tool_id}/restore")
def restore_tool(tool_id: str):
    db = SessionLocal()
    try:
        tool = db.get(Tool, tool_id)
        if not tool:
            raise HTTPException(404, "Tool not found")
        tool.is_removed = False
        tool.remove_reason = None
        db.commit()
        return {"status": "ok", "tool_id": tool_id}
    finally:
        db.close()

@router.post("/execute")
async def execute_tool(payload: ToolExecute):
    db = SessionLocal()
    try:
        tool = db.get(Tool, payload.tool_id)
        if not tool:
            raise HTTPException(404, "Tool not found")
        if tool.is_removed:
            raise HTTPException(400, "Tool is removed")

        key_record = db.get(Key, tool.key_alias) if tool.key_alias else None

        if tool.executor_type != "http":
            raise HTTPException(400, "Only http executor is implemented in v1")

        raw_output = await execute_http_tool(tool, key_record, payload.arguments)
        wrapped = wrap_output(tool.tool_id, raw_output)
        security = classify_wrapped_output(wrapped)

        db.add(AuditLog(
            caller_id=payload.caller_id,
            tool_id=tool.tool_id,
            request_json=json.dumps(payload.arguments),
            result_status="ok",
            reason=None,
            security_flags_json=json.dumps(security["flags"]),
        ))
        db.commit()

        return {
            "status": "ok",
            "tool_id": tool.tool_id,
            "raw_output": raw_output,
            "wrapped_output": wrapped,
            "security": security,
        }
    finally:
        db.close()
