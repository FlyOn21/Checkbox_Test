from abc import ABC, abstractmethod


class AbstractDbModel(ABC):

    @abstractmethod
    async def to_model_schema(self):
        raise NotImplementedError
