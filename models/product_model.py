from pydantic import BaseModel

# Pydantic: librería de Python para validación y gestión de datos


class Product(BaseModel):
    id: int
    title: str
    price: float  # JSON no tiene tipo decimal, llega como float
    status: int
    quantity: int


class ProductCreate(BaseModel):
    title: str
    price: float
    status: int
    quantity: int
