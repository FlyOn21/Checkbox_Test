from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.services.auth.schemas.user_auth import HTTPExceptionModel
from src.utils.logging.set_logging import set_logger

logger = set_logger()


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as http_exception:
            context = HTTPExceptionModel(detail=http_exception.detail).dict()
            return JSONResponse(
                status_code=http_exception.status_code,
                content=context,
            )
        except Exception as e:
            # logger.exception(e)
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error", "message": "An unexpected error occurred."},
            )
