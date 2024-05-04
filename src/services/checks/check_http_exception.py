import json
from typing import List

from fastapi import HTTPException, status


def some_products_not_found(msg: str) -> HTTPException:
    return HTTPException(detail=json.dumps([msg]), status_code=status.HTTP_409_CONFLICT)


def product_conflicts(msg: List[str]) -> HTTPException:
    return HTTPException(detail=json.dumps(msg), status_code=status.HTTP_409_CONFLICT)
