from datetime import date

from fastapi import APIRouter, status
from app.hotels.service import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])


# TODO add pydantic schemas
@router.get("/{location}", status_code=status.HTTP_200_OK)
async def get_hotels(location: str):
    # TODO finish service
    print(location)
    response = await HotelService.find_all(location=location)
    print(response)
    return response


# TODO add pydantic schemas
@router.get("/id/{hotel_id}", status_code=status.HTTP_200_OK)
async def get_hotel_by_id(hotel_id: int):
    # TODO finish service
    return await HotelService.find_by_id(model_id=hotel_id)
