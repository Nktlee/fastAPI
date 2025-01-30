from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from exceptions import HotelNotFoundHTTPException, ObjectNotFoundException
from src.services.hotels import HotelService
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPatch


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение данных об отелях")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация отеля"),
    date_from: date = Query(example="2025-02-01"),
    date_to: date = Query(example="2025-02-07"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}", summary="Получение данных об отеле")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="Добавление данных об отеле")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Rich чето чето",
                    "location": "Сочи, ул. Мира 22",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Resort чето чето",
                    "location": "Дубай, ул. Дубайская 3",
                },
            },
        }
    ),
):
    hotel = HotelService(db).add_hotel(hotel_data)
    return {"status": "ok", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление данных об отеле")
async def delete_hotel(hotel_id: int, db: DBDep):
    HotelService(db).delete_hotel(hotel_id)
    return {"status": "ok"}


@router.put("/{hotel_id}", summary="Изменение данных об отеле")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    HotelService(db).put_hotel(hotel_id, hotel_data)
    return {"status": "ok"}


@router.patch("/{hotel_id}", summary="Частичное изменение данных об отеле")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    HotelService(db).patch_hotel(hotel_id, hotel_data)
    return {"status": "ok"}
