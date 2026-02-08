from fastapi import APIRouter, Depends
from controllers import users_controllers
from models.user_model import User
from core.dependencies import is_admin_or_owner

router = APIRouter()


@router.get("/{user_id}", status_code=200)
async def get_user_id(user_id: str, user=Depends(is_admin_or_owner)):
    return await users_controllers.get_user_id(int(user_id))


# TODO: Intentar la ruta de obtener todos los usuarios, debe devolver una lista con todos los usuarios de la BBDD fetchone => fetchall
@router.get("/", status_code=200)
async def get_all():
    return await users_controllers.get_all()


# TODO: obtener la ruta que me permita extraer todos los usuarios de entre 20 y 40 años
@router.get("/age/{agemin}/{agemax}", status_code=200)
async def get_by_age(agemin: str, agemax: str):
    return await users_controllers.get_by_age(int(agemin), int(agemax))


# borrar un usuario por id
@router.delete("/{user_id}", status_code=200)
async def delete_by_id(user_id: str):
    return await users_controllers.delete_by_id(int(user_id))


# actualizar un usuario por id
@router.put("/{user_id}", status_code=201)
async def update_by_id(user_id: str, user: User):
    return await users_controllers.update_by_id(int(user_id), user)
