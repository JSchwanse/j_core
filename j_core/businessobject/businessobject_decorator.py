from typing import Type, Callable

from .BusinessObject import BusinessObject

Registry: dict[str, type[BusinessObject]] = {}


def businessobject(name: str) -> Callable[[Type[BusinessObject]], Type[BusinessObject]]:
    def _businessobject(cls: Type[BusinessObject]) -> Type[BusinessObject]:
        Registry[name] = cls
        return cls

    return _businessobject
