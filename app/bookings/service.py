from datetime import date
from sqlalchemy import select, insert, and_, or_, func

from app.service.base import BaseService
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):

        async with async_session() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            (Bookings.date_from >= date_from) & (Bookings.date_from <= date_to),
                            (Bookings.date_from <= date_from) & (Bookings.date_to > date_from),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            rooms_left = (
                select((Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"))
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            rooms_left = await session.execute(rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                return None
