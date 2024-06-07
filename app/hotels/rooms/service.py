from app.service.base import BaseService
from app.hotels.rooms.models import Rooms


class RoomService(BaseService):
    model = Rooms
