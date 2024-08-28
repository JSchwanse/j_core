from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from j_core.businessobject import BusinessObject
from j_core.config import DatabaseConnection

__all__ = ['Datasource', 'Runtime', 'initialize']


class Datasource:
    def __init__(self, conn: DatabaseConnection):
        self.db_connection = conn
        self.engine = create_engine(conn.get_connection_string())

    def initialize(self) -> None:
        # activate schema...
        schema = self.db_connection.get_schema() if self.db_connection.get_schema() is not None else 'public'
        with self.engine.begin() as exec_connection:
            exec_connection.execute(text(f'SET search_path TO {schema}'))

        # ... and generate tables
        BusinessObject.create_tables(self.engine)


class Runtime:
    Datasource: Datasource
    Session: sessionmaker[Session]


def initialize(conn: DatabaseConnection) -> None:
    datasource = Datasource(conn)
    datasource.initialize()

    Runtime.Datasource = datasource
    Runtime.Session = sessionmaker(bind=datasource.engine)
