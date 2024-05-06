import json
from typing import List

from fastapi import HTTPException, status


def some_products_not_found(msg: str) -> HTTPException:
    return HTTPException(detail={"error": "Products not found", "message": msg}, status_code=status.HTTP_409_CONFLICT)


def product_conflicts(msg: List[str]) -> HTTPException:
    return HTTPException(
        detail={"error": "Create check conflict", "message": msg}, status_code=status.HTTP_409_CONFLICT
    )


def check_not_exist(msg: List[str]) -> HTTPException:
    return HTTPException(detail={"error": "Check not exists", "message": msg}, status_code=status.HTTP_404_NOT_FOUND)


def page_number_out_of_bounds(msg: List[str]) -> HTTPException:
    return HTTPException(detail={"error": "Out of bounds", "message": msg}, status_code=status.HTTP_409_CONFLICT)
