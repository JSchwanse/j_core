from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def create_tables(engine):
    Base.metadata.create_all(engine)


class BusinessObject:
    """ Must be extended in conjunction with Base """
    id: Mapped[int] = mapped_column(primary_key=True)

    def to_dictionary(self):
        """ Must be used in conjunction with an object from sqlalchemy for the internal '__table__' field """
        obj_as_dict = {}

        # simple fields
        for column in self.__table__.columns:  # type: ignore[attr-defined]
            obj_as_dict[column.name] = getattr(self, column.name)

        # relations
        for propertyName in [propertyName for propertyName in dir(self) if not propertyName.startswith('__')]:
            if isinstance(getattr(self, propertyName), BusinessObject):
                obj_as_dict[propertyName] = getattr(self, propertyName).to_dictionary()

        return obj_as_dict
