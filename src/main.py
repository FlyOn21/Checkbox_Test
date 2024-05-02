from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse

from src.services.auth.auth import fastapi_users
from starlette.middleware.cors import CORSMiddleware
from src.services.auth.auth import auth_backend
from src.models.user_model import User
from src.services.auth.schemas.user_auth import UserRead, UserCreate, UserUpdate
from src.services.auth.auth import current_user

app = FastAPI(title="CheckBox")


@app.get("/")
def base_route_redirect():
    return RedirectResponse(url="/docs")


app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["Auth"])

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)



@app.get("/protected-route")
def protected_route(user: "User" = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
