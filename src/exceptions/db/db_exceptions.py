from sqlalchemy.exc import SQLAlchemyError


class TransactionException(SQLAlchemyError):
    def __init__(self, message):
        super().__init__(message)
