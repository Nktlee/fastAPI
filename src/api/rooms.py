from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomPatch, RoomRequestAdd, RoomRequestPatch
from src.api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение данных о номерах")
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение данных об одном номере")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms", summary="Добавление данных о номере")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Одноместные номера",
                "value": {
                    "title": "123",
                    "description": "Одноместные номера",
                    "price": 1000,
                    "quantity": 10,
                },
            },
            "2": {
                "summary": "Двухместные номера",
                "value": {
                    "title": "123",
                    "description": "Двухместные номера",
                    "price": 2000,
                    "quantity": 10,
                },
            },
        }
    ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "ok", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление данных о номере")
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"status": "ok"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение данных о номере")
async def put_hotel(hotel_id: int, room_id: int, room_data: RoomRequestAdd, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных о номере")
async def patch_hotel(hotel_id: int, room_id: int, room_data: RoomRequestPatch, db: DBDep):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"status": "ok"}
