from typing import Any

from sqlalchemy import Engine, Connection
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

__all__ = ['Base', 'create_tables', 'BusinessObject']


class Base(DeclarativeBase):
    pass


def create_tables(engine: Engine | Connection | MockConnection) -> None:
    Base.metadata.create_all(engine)


class BusinessObject:
    """ Must be extended in conjunction with Base """
    id: Mapped[int] = mapped_column(primary_key=True)

    def __init__(self, *args: Any, **kwargs: Any):
        # Mostly empty constructor to silence type hinters when calling the
        # default constructor via businessobject.Registry
        super().__init__(*args, **kwargs)

    def to_dictionary(self) -> dict[Any, Any]:
        """ Must be used in conjunction with an object from sqlalchemy for the internal '__table__' field """
        obj_as_dict = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns  # type: ignore[attr-defined]
        }

        # relations
        for propertyName in [propertyName for propertyName in dir(self) if not propertyName.startswith('__')]:
            if isinstance(getattr(self, propertyName), BusinessObject):
                obj_as_dict[propertyName] = getattr(self, propertyName).to_dictionary()

        return obj_as_dict
