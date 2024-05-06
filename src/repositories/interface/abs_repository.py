from abc import ABC, abstractmethod
from typing import List, Any


class AbstractRepository(ABC):
    """
    A base class representing an abstract repository that defines common database operations.

    This class provides a templates for repository classes which handle data transactions
    with a database for a specific entity or table. It enforces the implementation of
    basic CRUD operations along with additional retrieval methods. Each method is
    asynchronous, supporting asyncio for concurrent handling of database operations.

    Methods:
        create(data: dict):
            Asynchronously adds a new entry to the database.
            Parameters:
                data (dict): A dictionary containing the data to be added.

        update(unit_id: int, data: dict):
            Asynchronously updates an existing entry in the database.
            Parameters:
                unit_id (int): The identifier of the unit to be updated.
                data (dict): A dictionary containing the updated data.

        delete(unit_id: int):
            Asynchronously removes an entry from the database.
            Parameters:
                unit_id (int): The identifier of the unit to be deleted.

        get_list(limit: int = None, offset: int = None, **filter_by):
            Asynchronously retrieves a list of entries from the database.
            Parameters:
                limit (int, optional): The maximum number of entries to return.
                offset (int, optional): The offset from where to start retrieving entries.
                filter_by: Additional keyword arguments for filtering the results.

        get_scalar(unit_id: int):
            Asynchronously retrieves a single entry from the database.
            Parameters:
                unit_id (int): The identifier of the unit to retrieve.

    Usage:
        This class is intended to be subclassed with concrete implementations of the
        defined abstract methods. It should not be instantiated directly.
    """

    @abstractmethod
    async def create(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update(self, unit_id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, unit_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, unit_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_list(
        self,
        filter_conditions: List[Any],
        sorting_rule: str = "desc",
        limit: int = None,
        offset: int = None,
        *args,
        **kwargs
    ):
        raise NotImplementedError
