from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.repositories.hotels import HotelsRepository


router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("", summary="Получение данных об отеле")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )
    
@router.post("", summary="Добавление данных об отеле")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Rich чето чето",
        "location": "Сочи, ул. Мира 22",
    }},
    "2" : {"summary": "Дубай", "value": {
        "title": "Отель Resort чето чето",
        "location": "Дубай, ул. Дубайская 3",
    }},
})):
    
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})) 
        await session.commit()

    return {"status": "ok", "data": hotel}

@router.delete("/{hotel_id}", summary="Удаление данных об отеле")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "ok"}

@router.put("/{hotel_id}", summary="Изменение данных об отеле")
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "ok"}

@router.patch("/{hotel_id}", summary="Частичное изменение данных об отеле")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels

    if hotel_data.title != "string":
        hotels[hotel_id - 1]["title"] = hotel_data.title
    if hotel_data.name != "string":
        hotels[hotel_id - 1]["name"] = hotel_data.name

    return {"status": "ok"}