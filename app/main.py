from typing import Annotated
from datetime import date, timedelta

from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, Depends

from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.hotels.rooms.router import router as hotels_router


app = FastAPI(title="Hotels")

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)


class HotelsSearchArgs:
    def __init__(
        self,
        location: Annotated[str, Query()],
        date_from: Annotated[date, Query(ge=date.today(), le=date.today() + timedelta(days=365))],
        date_to: Annotated[date, Query(ge=date.today(), le=date.today() + timedelta(days=365))],
        stars: Annotated[int, Query(ge=1, le=5)] = None,
        has_spa: Annotated[bool, Query()] = None,
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa
