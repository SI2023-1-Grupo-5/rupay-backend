from fastapi import FastAPI

from app.database.init import engine
from app.database import models

from app.controllers.auth_controller import router as AuthController
from app.controllers.user_controller import router as UserController

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(AuthController)
app.include_router(UserController)

# TODO: Turn controllers into classes and inject db (?)
# TODO: Add a directory for custom exceptions (?)
# TODO: Create a DB class with methods implementing all sql basic operations (SELECT, INSERT, UPDATE and DELETE)
# TODO: Login system
# TODO: Authentication and Session system (JWT)