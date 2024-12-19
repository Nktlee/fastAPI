from pydantic import BaseModel, ConfigDict


class RoomRequestAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

class RoomRequestPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
