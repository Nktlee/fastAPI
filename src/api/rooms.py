from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.services.rooms import RoomService
from src.schemas.rooms import RoomRequestAdd, RoomRequestPatch
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
    try:
        models = await RoomService(db).get_rooms(hotel_id, date_from, date_to)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    return models


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение данных об одном номере")
@cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


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
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Двухместные номера",
                "value": {
                    "title": "123",
                    "description": "Двухместные номера",
                    "price": 2000,
                    "quantity": 10,
                    "facilities_ids": [1, 2],
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "ok", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление данных о номере")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id, room_id)

    return {"status": "ok"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение данных о номере")
async def put_room(hotel_id: int, room_id: int, room_data: RoomRequestAdd, db: DBDep):
    await RoomService(db).put_room(hotel_id, room_id, room_data)

    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных о номере")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomRequestPatch, db: DBDep):
    await RoomService(db).patch_room(hotel_id, room_id, room_data)

    return {"status": "ok"}
