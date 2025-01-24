from datetime import date

from fastapi import HTTPException, Query, APIRouter, Body
from fastapi_cache.decorator import cache

from exceptions import ObjectNotFoundException
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
    per_page = pagination.per_page or 5

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/{hotel_id}", summary="Получение данных об отеле")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Отель не найден")


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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "ok", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление данных об отеле")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "ok"}


@router.put("/{hotel_id}", summary="Изменение данных об отеле")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "ok"}


@router.patch("/{hotel_id}", summary="Частичное изменение данных об отеле")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "ok"}
