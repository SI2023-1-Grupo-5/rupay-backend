from fastapi import FastAPI

from app.database.init import engine
from app.database import models

from app.controllers.auth_controller import router as AuthController
from app.controllers.user_controller import router as UserController
from app.controllers.payment_controller import router as PaymentController
from app.controllers.comment_controller import router as CommentController
from app.middlewares.authentication_middleware import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(AuthController)
app.include_router(UserController)
app.include_router(PaymentController)
app.include_router(CommentController)


app.add_middleware(AuthenticationMiddleware)

origins = [
    "http://localhost",
    "http://localhost:3000",  # Add the client's origin here
    # Add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Turn controllers into classes and inject db (?)
# TODO: Add a directory for custom exceptions (?)
# TODO: Create a DB class with methods implementing all sql basic operations (SELECT, INSERT, UPDATE and DELETE)