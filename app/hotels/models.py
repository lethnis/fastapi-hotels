from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list | None] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int | None]


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    services: Mapped[list[str] | None] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int | None]
