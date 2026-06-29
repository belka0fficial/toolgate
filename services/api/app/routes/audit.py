from fastapi import APIRouter
from sqlalchemy import select
from app.core.db import SessionLocal
from app.models.audit import AuditLog

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("")
def list_audit():
    db = SessionLocal()
    try:
        rows = db.execute(
            select(AuditLog).order_by(AuditLog.created_at.desc())
        ).scalars().all()

        return [
            {
                "id": row.id,
                "caller_id": row.caller_id,
                "tool_id": row.tool_id,
                "request_json": row.request_json,
                "result_status": row.result_status,
                "reason": row.reason,
                "security_flags_json": row.security_flags_json,
                "created_at": row.created_at,
            }
            for row in rows
        ]
    finally:
        db.close()
