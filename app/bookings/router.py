from datetime import date
from fastapi import APIRouter, Depends, status

from app.exceptions import RoomCannotBeBookedException
from app.bookings.schemas import SBooking
from app.bookings.service import BookingService
from app.users.models import Users
from app.users.dependencies import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# TODO
@router.get("", response_model=list[SBooking])
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingService.find_all(user_id=user.id)


@router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):

    booking = await BookingService.add(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)

    if booking is None:
        raise RoomCannotBeBookedException

    return booking


# TODO
@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingService.delete_by_id()
