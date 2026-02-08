# importar la libreria os (sistema operativo), para poder leer ficheros fisicos
import os
import aiomysql

# importar la ibreria que permita a python leer fichero .env
from dotenv import load_dotenv

load_dotenv()
# busca fichero .env dentro del entorno para cargarlo


async def get_conexion():
    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
    )
