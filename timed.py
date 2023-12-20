from __future__ import annotations

import datetime
from typing import Any, Iterator, Iterable, Optional

T = bool | dict[Any, Any] | float | int | list[Any] | str


class Timed:
    def __init__(self, value: T, parent: Optional[Timed] = None) -> None:
        self._parent: Optional[Timed] = parent
        self._time: datetime.datetime = datetime.datetime.now()
        self._value: T = {k: Timed(v, self) for k, v in value.items()} if isinstance(value, dict) else value

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value
        self._set_time()

    def _set_time(self) -> None:
        self._time = datetime.datetime.now()

        if self._parent is not None:
            self._parent._set_time()

    def __contains__(self, item: Any) -> bool:
        if isinstance(self._value, dict | list | str):
            return self._value.__contains__(item)
        raise TypeError("not subscriptable")

    def __getitem__(self, item: Any) -> Any:
        if isinstance(self._value, dict | list | str):
            return self._value.__getitem__(item)
        raise TypeError("not subscriptable")

    def __iter__(self) -> Iterator[Any]:
        if isinstance(self._value, Iterable):
            return self._value.__iter__()
        raise TypeError("not iterable")

    def __getattr__(self, item: str) -> Any:
        if item in ["_parent", "_time", "_value"]:
            return self.__dict__[item]
        self._set_time()
        return getattr(self._value, item)

    def __setattr__(self, key: Any, value: Any) -> None:
        if key in ["_parent", "_time"]:
            self.__dict__[key] = value
        else:
            self._set_time()
            if key == "_value":
                self.__dict__[key] = value
            else:
                setattr(self._value, key, value)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"<T>{self._value}"

    def get_updated(self, time: datetime.datetime) -> Optional[T]:
        if self._time <= time:
            return None

        if isinstance(self._value, Timed):
            return self._value.get_updated(time)

        if isinstance(self._value, dict):
            return {k: value for k, v in self._value.items() if (value := v.get_updated(time)) is not None}

        return self._value
