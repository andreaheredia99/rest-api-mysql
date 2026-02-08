from fastapi import FastAPI
from routes import users_routes, auth_routes, products_routes
from core.security import verify_password

# activamos la ruta

# from core.security import hash_password

# levantar el servidor y crear acceso a la ruta user.
app = FastAPI()

"""
hash = hash_password("12345")
print(hash)
"""
# hash = hash_password("123456")
"""
print(
    verify_password(
        "123456",
        "$argon2id$v=19$m=65536,t=3,p=4$N4YQQmiNMcY4J2SslXKOMQ$C7r6/L/ngpQGFdxTMmlYE2NJ6Fe0/prpPDcHIKzxyNE",
    )
)"""

app.include_router(users_routes.router, prefix="/users", tags=["Users"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(products_routes.router, prefix="/products", tags=["Products"])
