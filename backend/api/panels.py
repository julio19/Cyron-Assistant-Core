"""Ticket Panel CRUD API — /guilds/{guild_id}/panels"""

import uuid
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_session
from backend.dependencies import require_guild_admin
from backend.models.ticket_panel import TicketPanel

router = APIRouter(prefix="/guilds/{guild_id}/panels", tags=["panels"])


class PanelIn(BaseModel):
    name: str
    bot_id: int | None = None
    ticket_category_name: str = "Tickets"
    button_text: str = "Open Ticket"
    button_emoji: str | None = None
    welcome_message: str | None = None
    ai_context_id: uuid.UUID | None = None


class PanelOut(BaseModel):
    id: uuid.UUID
    guild_id: int
    name: str
    bot_id: int | None
    ticket_category_name: str
    button_text: str
    button_emoji: str | None
    welcome_message: str | None
    ai_context_id: uuid.UUID | None


async def _get_panel(session: AsyncSession, panel_id: uuid.UUID, guild_id: int) -> TicketPanel | None:
    result = await session.execute(
        select(TicketPanel).where(TicketPanel.id == panel_id, TicketPanel.guild_id == guild_id)
    )
    return result.scalar_one_or_none()


@router.get("", response_model=list[PanelOut])
async def list_panels(
    guild_id: int = Depends(require_guild_admin),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(TicketPanel).where(TicketPanel.guild_id == guild_id).order_by(TicketPanel.created_at)
    )
    return list(result.scalars().all())


@router.post("", response_model=PanelOut, status_code=201)
async def create_panel(
    body: PanelIn = Body(...),
    guild_id: int = Depends(require_guild_admin),
    session: AsyncSession = Depends(get_session),
):
    panel = TicketPanel(guild_id=guild_id, **body.model_dump())
    session.add(panel)
    await session.flush()
    return panel


@router.get("/{panel_id}", response_model=PanelOut)
async def get_panel(
    panel_id: uuid.UUID,
    guild_id: int = Depends(require_guild_admin),
    session: AsyncSession = Depends(get_session),
):
    panel = await _get_panel(session, panel_id, guild_id)
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    return panel


@router.put("/{panel_id}", response_model=PanelOut)
async def update_panel(
    panel_id: uuid.UUID,
    body: PanelIn = Body(...),
    guild_id: int = Depends(require_guild_admin),
    session: AsyncSession = Depends(get_session),
):
    panel = await _get_panel(session, panel_id, guild_id)
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    for k, v in body.model_dump().items():
        setattr(panel, k, v)
    await session.flush()
    return panel


@router.delete("/{panel_id}", status_code=204)
async def delete_panel(
    panel_id: uuid.UUID,
    guild_id: int = Depends(require_guild_admin),
    session: AsyncSession = Depends(get_session),
):
    panel = await _get_panel(session, panel_id, guild_id)
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    await session.delete(panel)
