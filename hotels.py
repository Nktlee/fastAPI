from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]

@router.get("", summary="Получение данных об отеле")
def get_hotels(
    id: int | None = Query(None, description="Айди отеля"),
    title: str | None = Query(None, description="Название отеля"), 
):
    hotels_ = []

    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_

@router.post("", summary="Добавление данных об отеле")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи чето чето",
        "name": "sochi cheto cheto",
    }},
    "2" : {"summary": "Дубай", "value": {
        "title": "Отель Дубай чето чето",
        "name": "dubai cheto cheto",
    }},
})):
    global hotels

    hotels.routerend({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })

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