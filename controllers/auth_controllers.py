from fastapi import HTTPException
from db.config import get_conexion
from models.user_model import UserCreate, UserLogin
import aiomysql as aio
from core.security import hash_password, verify_password, create_token
from controllers.users_controllers import get_user_id


async def register(user: UserCreate):
    # el password del usuario viene sin hashear
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # TODO : hashear el password para mi yo del futuro
            hashed_pass = hash_password(user.password)
            # insertamos usuario en la bbdd
            await cursor.execute(
                "INSERT INTO users (name, surname, age,mail,status,password,rol) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                (
                    user.name,
                    user.surname,
                    user.age,
                    user.mail,
                    user.status,
                    hashed_pass,
                    user.rol,
                ),
            )
            await conn.commit()
            new_id = cursor.lastrowid
            # devuelve ultimo id registrado
            user = await get_user_id(new_id)
            return {"msg": "Usuario registrado correctamente", "item": user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


async def login(user_login: UserLogin):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM 202509_shop.users WHERE mail=%s", (user_login.mail)
            )
            user = await cursor.fetchone()
            if not user:
                raise HTTPException(
                    status_code=404, detail="Usuario o password incorrecto"
                )
            # verificar la contraseña
            if not verify_password(user_login.password, user["password"]):
                raise HTTPException(
                    status_code=404, detail="Usuario o password incorrecto"
                )
            # vamos a crear el token con los datos y la funcion que hemos trabajado en security
            token_data = {"id": user["id"], "rol": user["rol"]}
            token = create_token(token_data)
            # print(decode_token(token))
            return {"msg": "Usuario logado correctamente", "token": token}
        # TODO: Crear el token para validar la API, esto despues de vacas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
