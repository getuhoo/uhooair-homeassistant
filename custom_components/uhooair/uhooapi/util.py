import json
from typing import Any


def json_pp(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, indent=2, separators=(",", ": "))
