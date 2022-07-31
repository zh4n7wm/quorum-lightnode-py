from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Image:
    mediaType: str
    name: str
    content: str


@dataclass_json
@dataclass
class Object:
    content: str
    id: Optional[str]
    name: Optional[str]
    image: Optional[Image]
    type: str = "Note"
