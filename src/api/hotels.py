from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("", summary="Получение данных об отеле")
async def get_hotels(
    pagination: PaginationDep,
    hotel_id: int | None = Query(None, description="Айди отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels

    # if pagination.page and pagination.per_page:
    #     start_index = (pagination.page - 1) * pagination.per_page
    #     end_index = start_index + pagination.per_page
    #     hotels_ = hotels_[start_index:end_index]

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