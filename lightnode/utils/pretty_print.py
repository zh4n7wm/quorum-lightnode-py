from .json import json_dumps


def pretty_print(obj: bool | str | bytes | object) -> None:
    if isinstance(obj, (str, bytes, bool)):
        print(obj)
    else:
        print(json_dumps(obj))
