import json
from fastapi import HTTPException, status


def user_not_found() -> HTTPException:
    return HTTPException(detail=json.dumps(["User not found"]), status_code=status.HTTP_401_UNAUTHORIZED)


def password_incorrect() -> HTTPException:
    return HTTPException(detail=json.dumps(["Password is incorrect"]), status_code=status.HTTP_401_UNAUTHORIZED)


def token_exception() -> HTTPException:
    return HTTPException(
        detail=json.dumps(["Token has expired or is invalid. Please log in again."]),
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def user_exists() -> HTTPException:
    return HTTPException(
        detail=json.dumps(["User with this email already exists"]), status_code=status.HTTP_409_CONFLICT
    )


def user_is_not_active() -> HTTPException:
    return HTTPException(
        detail=json.dumps(["User deactivate, please contact support"]), status_code=status.HTTP_401_UNAUTHORIZED
    )
