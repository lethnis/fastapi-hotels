from fastapi import APIRouter
from sqlalchemy import select

from app.database import async_session
from app.bookings.models import Bookings

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings():
    async with async_session() as session:
        query = select(Bookings.__table__.columns)
        result = await session.execute(query)
        print(result.mappings().all())
