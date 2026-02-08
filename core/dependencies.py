# archivo de dependencias me permite bloquear el acceso a ciertas rutas en función de cierta caracteristica, si un usuarios es valido y existe o si tipo rol de admin.
from datetime import datetime, timezone
from fastapi import HTTPException, Depends, Path
from fastapi.security import OAuth2PasswordBearer
from controllers.users_controllers import get_user_id
from core.security import decode_token

# a las depencias hay que indicarles donde y cuando se genero el token
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2)):
    # decodificar el token
    payload = decode_token(token)
    print(payload)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalido")
    expire = payload.get("expire")
    if not expire or expire < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=401, detail="Token expirado")
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    # obtener los datos del usuario logado
    user = await get_user_id(user_id)
    return user


# verificar si tengo rol de administrador o soy el usuario propietario del recurso.


async def is_admin_or_owner(user=Depends(get_current_user), user_id: int = Path(...)):
    # verificar si el usuario autenticado es admin o es el dueño del recurso. Si no se cumple esto lanzo una excepcion.
    # si es admin
    if user["rol"] == "admin":
        return user

    # si el propietario del recurso
    if user["id"] == user_id:
        return user

    # si no es admin y tampoco propietario del recurso no tienes acceso
    raise HTTPException(
        status_code=403, detail="No tienes permisos para realizar esta acción"
    )


async def is_admin(user=Depends(get_current_user)):
    if user["rol"] == "admin":
        return user
    # si no es admin y tampoco propietario del recurso no tienes acceso
    raise HTTPException(status_code=403, detail="No eres administrador")
