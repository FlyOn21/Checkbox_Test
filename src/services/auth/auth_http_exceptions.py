import json
from fastapi import HTTPException, status


def user_not_found() -> HTTPException:
    return HTTPException(
        detail={
            "error": "User not found",
            "message": "User not found",
        },
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def password_incorrect() -> HTTPException:
    return HTTPException(
        detail={
            "error": "Password is incorrect",
            "message": "Password is incorrect",
        },
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def token_exception() -> HTTPException:
    return HTTPException(
        detail={
            "error": "Token has expired or is invalid",
            "message": "Please log in again",
        },
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def user_exists() -> HTTPException:
    return HTTPException(
        detail={
            "error": "User exists",
            "message": "User with this email already exists",
        },
        status_code=status.HTTP_409_CONFLICT,
    )


def user_is_not_active() -> HTTPException:
    return HTTPException(
        detail={
            "error": "User is not active",
            "message": "User is not active, please contact support",
        },
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
