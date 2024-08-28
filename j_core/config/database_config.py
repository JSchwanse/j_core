from typing import Self
from xml.etree import ElementTree

from j_core.exceptions.exceptions import ElementNotFoundException

__all__ = ['DatabaseConnection', 'DatabaseConfiguration']


class DatabaseConnection:
    def __init__(self, connection_config: dict[str, str | None]):
        self.connection_config: dict[str, str | None] = connection_config

    def get_driver(self) -> str | None:
        return self.connection_config['driver'] if 'driver' in self.connection_config else None

    def get_user(self) -> str | None:
        return self.connection_config['user'] if 'user' in self.connection_config else None

    def get_password(self) -> str | None:
        return self.connection_config['password'] if 'password' in self.connection_config else None

    def get_database(self) -> str | None:
        return self.connection_config['dbName'] if 'dbName' in self.connection_config else None

    def get_host(self) -> str | None:
        return self.connection_config['host'] if 'host' in self.connection_config else None

    def get_port(self) -> str | None:
        return self.connection_config['port'] if 'port' in self.connection_config else None

    def get_dialect(self) -> str | None:
        return self.connection_config['dialect'] if 'dialect' in self.connection_config else None

    def get_schema(self) -> str | None:
        return self.connection_config['schema'] if 'schema' in self.connection_config else None

    def get_connection_string(self) -> str:
        return (f"{self.get_driver()}{f'+{self.get_dialect()}' if self.get_dialect() is not None else ''}://"
                f"{self.get_user()}:{self.get_password()}@{self.get_host()}:{self.get_port()}/{self.get_database()}")


class DatabaseConfiguration:
    def __init__(self, config_path: str | None = None):
        self.config_path: str | None = config_path
        self.connections: dict[str, DatabaseConnection] | None = None
        if self.config_path is not None:
            self.read()

    def read(self, config_path: str | None = None) -> Self:

        # handle path
        if (config_path is None) and (self.config_path is None):
            raise FileNotFoundError('DatabaseConfiguration config_path is missing!')

        if config_path is not None:
            self.config_path = config_path

        # reset connections
        self.connections = {}

        # ensure config_path
        if self.config_path is None:
            raise FileNotFoundError('DatabaseConfiguration config_path is missing!')

        # parse config
        root = ElementTree.parse(self.config_path)
        el_alias_list = root.findall('Alias')
        el_conn_list = root.findall('Connection')

        if len(el_alias_list) == 0:
            raise ElementNotFoundException('No Alias-element found in dbconfig.')

        for el_alias in el_alias_list:

            conf_name = el_alias.get('name')
            conn_name = el_alias.get('connection')

            if (conf_name is not None) and (conn_name is not None):
                connection_config: dict[str, str | None] = {}

                for el_connection in el_conn_list:
                    if el_connection.get('name') == conn_name:
                        connection_config['driver'] = el_connection.get('driver')
                        for elProperty in el_connection.findall('Property'):
                            name = elProperty.get('name')
                            if name is None:
                                continue
                            connection_config[name] = elProperty.get('value')

                self.connections[conf_name] = DatabaseConnection(connection_config)

        return self

    def get_connection(self, alias: str) -> DatabaseConnection | None:
        return self.connections.get(alias) if self.connections is not None else None
