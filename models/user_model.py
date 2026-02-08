from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    mail: str
    register_date: Optional[datetime] = None
    status: int
    password: str
    rol: str


# en el User lleva id para que luego se pueda autoincrementar solo y el UserCreate no lleva para que cada vez que agregemos un nuevo usuario no de fallo
class UserCreate(BaseModel):
    name: str
    surname: str
    age: int
    mail: str
    register_date: Optional[datetime] = None
    status: int
    password: str
    rol: str


class UserLogin(BaseModel):
    mail: str
    password: str
