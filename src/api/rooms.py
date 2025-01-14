from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomRequestAdd, RoomRequestPatch
from src.api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение данных о номерах")
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-02-01"),
    date_to: date = Query(example="2025-02-07"),
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение данных об одном номере")
@cache(expire=10)
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
                    "facilities_ids": [1,2]
                },
            },
            "2": {
                "summary": "Двухместные номера",
                "value": {
                    "title": "123",
                    "description": "Двухместные номера",
                    "price": 2000,
                    "quantity": 10,
                    "facilities_ids": [1,2]
                },
            },
        }
    ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]

    await db.rooms_facilities.add_bulk(rooms_facilities_data)
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
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)

    await db.commit()

    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных о номере")
async def patch_hotel(
    hotel_id: int, room_id: int, room_data: RoomRequestPatch, db: DBDep
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
  

    await db.commit()

    return {"status": "ok"}
