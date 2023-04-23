from typing import Any, Hashable, Mapping


def get_in(m: Mapping, *keys: Hashable, default=None) -> Any:
    for key in keys:
        try:
            m = m[key]
        except (TypeError, KeyError, IndexError):
            return default
    return m
