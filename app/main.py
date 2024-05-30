from typing import Annotated
from datetime import date, timedelta

from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, Depends

from app.bookings.router import router as booking_router


app = FastAPI(title="Hotels")

app.include_router(booking_router)


class SHotel(BaseModel):
    address: str
    name: str
    stars: int = Field(ge=1, le=5)


hotels = [{"address": "here", "name": "lazy", "stars": 5}]


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


@app.get("/hotels", response_model=list[SHotel])
async def get_hotels(search_args: HotelsSearchArgs = Depends()):
    return hotels


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
