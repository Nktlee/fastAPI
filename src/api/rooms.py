from fastapi import Query, APIRouter, Body

from src.schemas.rooms import RoomAdd
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker


router = APIRouter(prefix="/rooms", tags=["Номера"])

@router.get("/{hotel_id}", summary="Получение данных о номере")
async def get_rooms(
    hotel_id: int,
    title: str | None = Query(None)
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
                title=title,
                hotel_id=hotel_id
            )
    
@router.post("/{hotel_id}", summary="Добавление данных о номере")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "Одноместные номера", "value": {
        "hotel_id": 9,
        "title": "123",
        "description": "Одноместные номера",
        "price": 1000,
        "quantity": 10
    }},
    "2": {"summary": "Двухместные номера", "value": {
        "hotel_id": 10,
        "title": "123",
        "description": "Двухместные номера",
        "price": 2000,
        "quantity": 10
    }},
})): 
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})) 
        await session.commit()

    return {"status": "ok", "data": room}

@router.delete("/{hotel_id}", summary="Удаление данных о номере")
async def delete_hotel(hotel_id: int, title: str):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, title=title)
        await session.commit()

    return {"status": "ok"}

# @router.put("/{hotel_id}", summary="Изменение данных о номере")
# async def put_hotel(hotel_id: int, hotel_data: HotelAdd):
#     async with async_session_maker() as session:
#         await RoomsRepository(session).edit(hotel_data, id=hotel_id)
#         await session.commit()

#     return {"status": "ok"}

# @router.patch("/{hotel_id}", summary="Частичное изменение данных о")
# async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
#     async with async_session_maker() as session:
#         await RoomsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
#         await session.commit()

#     return {"status": "ok"}
