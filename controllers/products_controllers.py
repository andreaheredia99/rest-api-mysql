import aiomysql as aio

# aiomysql: es una libreria para conectarse a MySQL de forma asíncrona

from fastapi import HTTPException

# para devolver errores HTTP (status code + mensaje)

from db.config import get_conexion

# función para conectarse a MySQL

from models.product_model import ProductCreate, Product

# importamos la funcion de crear producto para validar los datos

from core import functions as fn


# get_list_all()
async def get_list_all():
    try:
        # obtener el acceso a bbdd
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM 202509_shop.products WHERE products.status = 1"
            )
            data = await cursor.fetchall()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# get_by_id
async def get_by_id(id_product):

    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM 202509_shop.products WHERE id=%s", (id_product,)
            )
            data = await cursor.fetchone()
            if data:
                return data
            else:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# get_by_title
async def get_by_title(title):
    title_clean = fn.borrar_tildes(title)
    print(title_clean)
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM 202509_shop.products WHERE title LIKE %s AND status=1",
                (f"%{title_clean}%",),
            )
        data = await cursor.fetchall()
        if len(data) != 0:
            return data
        else:
            raise HTTPException(status_code=404, detail="No hay resultados")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# get_by_price
async def get_by_price(price_min, price_max):
    if price_min > price_max:
        raise HTTPException(
            status_code=400, detail="El precio mínimo no puede ser mayor que el máximo"
        )
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM 202509_shop.products WHERE price BETWEEN %s AND %s AND status=1",
                (price_min, price_max),
            )
            data = await cursor.fetchall()
            if len(data) == 0:
                raise HTTPException(status_code=404, detail="No hay productos")
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# get_by_quantity
async def get_by_quantity(quantity: int, compare: str):
    if quantity < 0:
        raise HTTPException(
            status_code=422, detail="Cantidad tiene que ser numerica y no negativa"
        )
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            if compare == "gt":
                query = "SELECT * FROM 202509_shop.products WHERE quantity>=%s AND status= 1"
            else:
                query = "SELECT * FROM 202509_shop.products WHERE quantity<=%s AND status= 1"
            await cursor.execute(query, (quantity,))
            data = await cursor.fetchall()
            if len(data) == 0:
                raise HTTPException(status_code=404, detail="No hay resultados")
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


async def get_title_strict(title):
    title_clean = fn.borrar_tildes(title)
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM 202509_shop.products WHERE title=%s", (title_clean,)
            )
        data = await cursor.fetchone()
        print(data)
        if data:
            return data
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# create_product
async def create_product(product: ProductCreate):
    exist = await get_title_strict(product.title)
    try:
        conn = await get_conexion()
        if not exist:
            async with conn.cursor(aio.DictCursor) as cursor:
                await cursor.execute(
                    "INSERT INTO 202509_shop.products (title, quantity, status, price) VALUES (%s,%s,%s,%s)",
                    (product.title, product.quantity, product.status, product.price),
                )
                await conn.commit()
                # recuperar el ultimo id
                nuevo_id = cursor.lastrowid
                product = await get_by_id(nuevo_id)
                return {"msg": "Producto insertado correctamente", "item": product}
        else:
            raise HTTPException(status_code=409, detail="Producto duplicado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# delete_product
async def delete_product(id_product: int):
    exist = await get_by_id(id_product)
    try:
        conn = await get_conexion()
        if exist:
            async with conn.cursor(aio.DictCursor) as cursor:
                await cursor.execute(
                    "DELETE FROM 202509_shop.products WHERE id=%s", (id_product,)
                )
                await conn.commit()
                return {
                    "msg": f"El producto con id {id_product} ha sido eliminado con exito",
                    "status": True,
                }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# update_product
async def update_product(id_product: int, product: Product):
    if id_product != product.id:
        raise HTTPException(status_code=400, detail="Los ID no coinciden")
    exist = await get_by_id(id_product)
    if exist is None:
        raise HTTPException(
            status_code=404, detail="El producto que intentas actualizar no existe."
        )
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "UPDATE 202509_shop.products SET title=%s, quantity=%s, status=%s, price=%s WHERE id=%s",
                (
                    product.title,
                    product.quantity,
                    product.status,
                    product.price,
                    product.id,
                ),
            )
            await conn.commit()
            # ya tenemos el id del producto y quiero responder con el producto actualizado.
            product = await get_by_id(id_product)
            return {"msg": "Producto actualizado correctamente", "item": product}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
