from sqlalchemy import String, Text, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class Tool(Base):
    __tablename__ = "tools"

    tool_id: Mapped[str] = mapped_column(String, primary_key=True)
    provider: Mapped[str] = mapped_column(String)
    action: Mapped[str] = mapped_column(String)
    source_type: Mapped[str] = mapped_column(String)   # api | mcp | local
    executor_type: Mapped[str] = mapped_column(String) # http | mcp | function
    key_alias: Mapped[str | None] = mapped_column(String, nullable=True)
    config_json: Mapped[str] = mapped_column(Text, default="{}")
    input_schema_json: Mapped[str] = mapped_column(Text, default="{}")
    output_schema_json: Mapped[str] = mapped_column(Text, default="{}")
    failure_count: Mapped[int] = mapped_column(default=0)
    last_success_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_failure_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_removed: Mapped[bool] = mapped_column(Boolean, default=False)
    remove_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    removed_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
