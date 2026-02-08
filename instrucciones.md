# API con MySQL

    0 - Crear entorno desarrollo
        python -m venv .venv
        source .venv/Scripts/activate

    1 - Instalar dependencias: 
        - "fastapi[standard]"
        - aiomysql
        -

    2 - Creamos el fichero requirements.txt
        - pip freeze > requirements.txt

# Crear base datos en MySQL
Vamos a crear api de usuarios y productos. Los usuarios van a ser de dos tipos, admin y user, el admin puede leer, crear, borrar y actualizar productos y usuarios. User solo podrá crear, borrar, visualizar y actualizar productos

    - Crear tabla users en una BBDD y llenarla con 10 registros
        - id: int
        - name: str
        - surname: str
        - age: int
        - mail: str
        - register_date: date => default instante en el que registramos
        - status: Boolean -> tinyint
        - password: str
        - rol: ENUM('admin', 'user') es una lista fija pero me permite añadir

# Crear los ficheros necesarios dentro de la carpeta routes, models, controllers para manejar la entidad users.
    - users_routes.py
        - GET users/id => obtener conectando a BBDD el usuario por id
    - users_controller.py
    - user_model.py