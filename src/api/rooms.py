from fastapi import Query, APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomPatch, RoomRequestAdd, RoomRequestPatch
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Получение данных о номерах")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
    
@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение данных об одном номере")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
    
@router.post("/{hotel_id}/rooms", summary="Добавление данных о номере")
async def create_room(hotel_id: int, room_data: RoomRequestAdd = Body(openapi_examples={
    "1": {"summary": "Одноместные номера", "value": {
        "title": "123",
        "description": "Одноместные номера",
        "price": 1000,
        "quantity": 10
    }},
    "2": {"summary": "Двухместные номера", "value": {
        "title": "123",
        "description": "Двухместные номера",
        "price": 2000,
        "quantity": 10
    }},
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})) 
        await session.commit()

    return {"status": "ok", "data": room}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление данных о номере")
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "ok"}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение данных о номере")
async def put_hotel(hotel_id: int, room_id: int, room_data: RoomRequestAdd):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "ok"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных о номере")
async def patch_hotel(hotel_id: int, room_id: int, room_data: RoomRequestPatch):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "ok"}
