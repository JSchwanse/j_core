from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from j_core.businessobject import BusinessObject
from j_core.config import DatabaseConnection


class Datasource:
    def __init__(self, conn: DatabaseConnection):
        self.db_connection = conn
        self.engine = create_engine(conn.get_connection_string())

    def initialize(self):
        # activate schema...
        schema = self.db_connection.get_schema() if self.db_connection.get_schema() is not None else 'public'
        with self.engine.begin() as exec_connection:
            exec_connection.execute(text('SET search_path TO ' + schema))

        # ... and generate tables
        BusinessObject.create_tables(self.engine)


class Runtime:
    Datasource: Datasource
    Session: sessionmaker


def initialize(conn: DatabaseConnection):
    datasource = Datasource(conn)
    datasource.initialize()

    Runtime.Datasource = datasource
    Runtime.Session = sessionmaker(bind=datasource.engine)
