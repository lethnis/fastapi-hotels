from sqlalchemy import select, Select

from app.service.base import BaseService
from app.hotels.models import Hotels
from app.database import async_session


class HotelService(BaseService):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str):
        async with async_session() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.location.icontains(location))
            result = await session.execute(query)
            return result.mappings().all()
