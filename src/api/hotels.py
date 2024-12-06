from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("", summary="Получение данных об отеле")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels

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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})) 
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