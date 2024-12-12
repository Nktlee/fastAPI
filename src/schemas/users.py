from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

class User(UserAdd):
    id: int
    email: EmailStr
