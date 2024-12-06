from fastapi import Query, APIRouter, Body

from sqlalchemy import insert

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Питер", "name": "spb"},
]

@router.get("", summary="Получение данных об отеле")
def get_hotels(
    pagination: PaginationDep,
    hotel_id: int | None = Query(None, description="Айди отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []

    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        start_index = (pagination.page - 1) * pagination.per_page
        end_index = start_index + pagination.per_page
        hotels_ = hotels_[start_index:end_index]

    return hotels_

@router.post("", summary="Добавление данных об отеле")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи чето чето",
        "location": "cheto cheto",
    }},
    "2" : {"summary": "Дубай", "value": {
        "title": "Отель Дубай чето чето",
        "location": "cheto cheto",
    }},
})):
    
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "ok"}

@router.delete("/{hotel_id}", summary="Удаление данных об отеле")
def delete_hotel(hotel_id: int):
    global hotels

    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "ok"}

@router.put("/{hotel_id}", summary="Изменение данных об отеле")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels

    hotels[hotel_id - 1]["title"] = hotel_data.title
    hotels[hotel_id - 1]["name"] = hotel_data.name

    return {"status": "ok"}

@router.patch("/{hotel_id}", summary="Частичное изменение данных об отеле")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels

    if hotel_data.title != "string":
        hotels[hotel_id - 1]["title"] = hotel_data.title
    if hotel_data.name != "string":
        hotels[hotel_id - 1]["name"] = hotel_data.name

    return {"status": "ok"}