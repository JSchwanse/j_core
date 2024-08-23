from .BusinessObject import BusinessObject

Registry: dict[str, type[BusinessObject]] = {}


def businessobject(name: str):
    def _businessobject(cls: type[BusinessObject]):
        Registry[name] = cls
        return cls

    return _businessobject
