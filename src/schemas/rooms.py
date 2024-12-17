from pydantic import BaseModel, Field, ConfigDict


class RoomRequestAdd(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
