from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    location: Mapped[str] = mapped_column()
    services: Mapped[list | None] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column()
    image_id: Mapped[int | None] = mapped_column()


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column()
    price: Mapped[int] = mapped_column()
    services: Mapped[list | None] = mapped_column(JSON)
    quantity: Mapped[int] = mapped_column()
    image_id: Mapped[int | None] = mapped_column()
