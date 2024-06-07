from datetime import date

from app.hotels.router import router
from app.hotels.rooms.service import RoomService


# TODO add pydantic schemas
@router.get("/id/{hotel_id}/rooms")
def get_rooms(hotel_id: int, date_from: date, date_to: date):
    # TODO finish service
    return RoomService.find_by_id()
