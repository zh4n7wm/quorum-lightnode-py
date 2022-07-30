import dataclasses
import json

from google.protobuf import message
from google.protobuf.json_format import MessageToDict


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, message.Message):
            return MessageToDict(o)
        return super().default(o)


def json_dump(  # pylint: disable=too-many-arguments
    obj, fp, cls=CustomJSONEncoder, indent=4, ensure_ascii=False, sort_keys=True
):
    return json.dump(
        obj, fp, cls=cls, indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys
    )


def json_dumps(  # pylint: disable=too-many-arguments
    obj, cls=CustomJSONEncoder, indent=4, ensure_ascii=False, sort_keys=True
):
    return json.dumps(
        obj, cls=cls, indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys
    )
