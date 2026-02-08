# necesitamos las librerias de python => python-jose => criptografia, passlib => bcrypt
# pip install "python-jose[cryptography]"
# pip install "passlib[argon2]"
# os la necesitamos para cargar las variables del entorno

import os

# libreria de seguridad y encriptacion para crear y modificar contraseñas
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

# timedelta = transforma min en forma horaria


# cargar las variables de entorno
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALCORITHM")
ACCESS_TOKEN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# configurar bcrypt para poderlo usar dentro de este fichero para ello creamos un contexto. Activando bcrypt
pwd_context = CryptContext(
    schemes=["argon2"], deprecated="auto"
)  # auto, no o yes (actualizar sistema encriptacion si queda deprecado)


# crear una funcion que me permita convertir o codificar una contraseña con bcrypt
def hash_password(password: str):
    # hasheamos el password con bcrypt
    return pwd_context.hash(password)


# crear una funcion que me permita comparar el hash de mi contraseña con la almacenada en BBDD
def verify_password(plaintext_password: str, hashed_password: str):
    # verificar que una contraseña en texto plano no coincida con su hash
    return pwd_context.verify(plaintext_password, hashed_password)


# Crear el token (pulserita) para el usuario
# para crear el token del usuario vamos a necesitar el id_usuario, rol, fecha actual con el tiempo de expiracion vamos a obtener cuanto va a durar ese token, { id: user.id, rol: user.rol }
def create_token(data: dict):
    # crear el token con la libreria JWT con los datos del usuario que recibe de data
    datacopy_to_encode = data.copy()
    # necesito actualizar mi data copy con los datos de expiracion
    # { id: user.id, rol: user.rol, expire: tiempo}
    # Calcular el expire o tiempo de expiracion desde la fecha actual hasta los minutos del ACCESS_TOKEN
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN)
    # Actualizamos el objeto datacopy con la fecha de expiracion
    datacopy_to_encode.update({"expire": int(expire.timestamp)()})
    # timestamp, transforma en segundos una fecha
    # print(datacopy_to_encode)
    # codificar el token
    return jwt.encode(datacopy_to_encode, SECRET_KEY, algorithm=ALGORITHM)


# funcion para decodificar el token -> la usaremos para validar las opciones que esten protegidas por el uso de token(Depends)
def decode_token(token: str):
    # decodificar el token para recibir los datos del usuario. Son id, rol, fecha expiracion, y para ello usamos JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None
