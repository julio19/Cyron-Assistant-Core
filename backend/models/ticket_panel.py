"""TicketPanel ORM model."""

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class TicketPanel(Base):
    __tablename__ = "ticket_panels"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guild_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("guilds.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="Default Panel")
    bot_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    ticket_category_name: Mapped[str] = mapped_column(String(255), nullable=False, default="Tickets")
    button_text: Mapped[str] = mapped_column(String(80), nullable=False, default="Open Ticket")
    button_emoji: Mapped[str | None] = mapped_column(String(32), nullable=True)
    welcome_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_context_id: Mapped[uuid.UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("ai_contexts.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
