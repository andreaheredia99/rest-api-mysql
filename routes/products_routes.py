from fastapi import APIRouter, Depends

# herramienta FastAPI para agrupar rutas

from models.product_model import Product, ProductCreate

# la ruta tiene que validar los datos, importamos model

from controllers import products_controllers

from core.dependencies import is_admin


router = APIRouter()
# creamos el router


# /products/
@router.get("/", status_code=200)
async def get_all():
    return await products_controllers.get_list_all()


# /products/{id}
@router.get("/{id_product}", status_code=200)
async def get_by_id(id_product: str):
    return await products_controllers.get_by_id(int(id_product))


#  /products/filter/name?title='lenovo'
@router.get("/filter/name", status_code=200)
async def get_by_title(title: str):
    return await products_controllers.get_by_title(title)


@router.get("/filter/price/{price_min}/{price_max}", status_code=200)
async def get_by_price(price_min: str, price_max: str):
    return await products_controllers.get_by_price(float(price_min), float(price_max))


#  /products/filter/quantity/10?compare='gt'
@router.get("/filter/quantity/{quantity}", status_code=200)
async def get_by_quantity(quantity: str, compare: str = "gt"):
    return await products_controllers.get_by_quantity(int(quantity), compare)


@router.post("/", status_code=201)
async def create_product(product: ProductCreate, user=Depends(is_admin)):
    return await products_controllers.create_product(product)


@router.delete("/{id_product}", status_code=200)
async def delete_product(id_product: str, user=Depends(is_admin)):
    return await products_controllers.delete_product(int(id_product))


@router.put("/{id_product}", status_code=200)
async def update_product(id_product: str, product: Product):
    return await products_controllers.update_product(int(id_product), product)
