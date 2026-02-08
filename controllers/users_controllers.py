import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException
from models.user_model import UserCreate, User


async def get_user_id(user_id: int):
    try:
        # obtener acceso a la bbdd de forma asincrona a traves del get_conexion
        conn = await get_conexion()
        # voy abrir un sql para poder lanzar consultas de mysql
        async with conn.cursor(aio.DictCursor) as cursor:
            # lanzamos la consulta de datos
            await cursor.execute(
                "SELECT * FROM 202509_shop.users WHERE id=%s", (user_id,)
            )
            user = await cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


async def get_all():
    try:
        conn = await get_conexion()
        # donde hacemos la conexion
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM 202509_shop.users")
            # convertir la peticion en un array de json
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error:{str(e)}")

    finally:
        conn.close()


async def get_by_age(agemin, agemax):
    if agemin > agemax:
        raise HTTPException(
            status_code=400, detail="La edad minima no puede ser mayor que la maxima"
        )
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM 202509_shop.users WHERE users.age BETWEEN %s AND %s",
                (agemin, agemax),
            )
            userList = await cursor.fetchall()
            if len(userList) != 0:
                return userList
            else:
                raise HTTPException(status_code=404, detail="No hay resultados")
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


async def register(user: UserCreate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # TODO : hashear el password para mi yo del futuro
            # insertamos usuario en la bbdd
            await cursor.execute(
                "INSERT INTO users (name, surname, age,mail,status,password,rol) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                (
                    user.name,
                    user.surname,
                    user.age,
                    user.mail,
                    user.status,
                    user.password,
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


async def delete_by_id(user_id: int):
    user = await get_user_id(user_id)
    if user is not None:
        # podemos borrar el usuario que existe
        try:
            conn = await get_conexion()
            async with conn.cursor(aio.DictCursor) as cursor:
                await cursor.execute(
                    "DELETE FROM 202509_shop.users WHERE id=%s", (user_id,)
                )
                await conn.commit()
                return {"mag": f"Usuario con id{user_id} ha sido eliminado con exito"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error:{str(e)}")
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=404, detail="Usuario que intentas borrar no existe"
        )


async def update_by_id(user_id: int, user: User):
    if user_id != user.id:
        # comprobamos que id que tu mandas y el id de la lista coninciden
        raise HTTPException(status_code=400, detail="El ID no coincide")
    user_check = await get_user_id(user_id)
    # comprobar si existe en la base de datos
    if user is None:
        raise HTTPException(
            status_code=404, detail="El usuario que intentas actualizar no existe"
        )
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "UPDATE 202509_shop.users SET name=%s, age=%s, surname=%s, mail= %s,status=%s,password=%s, rol=%s WHERE id=%s",
                (
                    user.name,
                    user.age,
                    user.surname,
                    user.mail,
                    user.status,
                    user.password,
                    user.rol,
                    user.id,
                ),
            )
            await conn.commit()
            user = await get_user_id(user_id)
            return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error")
    finally:
        conn.close()
