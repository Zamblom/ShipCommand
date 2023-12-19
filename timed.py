from __future__ import annotations

import datetime
from typing import Any, Iterator, Optional, Sequence, TypeVar


class Timed:
    T = TypeVar("T")

    def __init__(self, value: T, parent: Optional[Timed] = None) -> None:
        self._parent: Optional[Timed] = parent
        self._time: datetime.datetime = datetime.datetime.now()
        self._value: Any = value

    def set_time(self, tab: int = 0) -> None:
        self._time = datetime.datetime.now()
        if self._parent is not None:
            self._parent.set_time(tab + 1)

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        if value != self._value:
            self._value = value
            self.set_time()

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"<T>{self._value}"


    def get_updated(self, time: datetime.datetime, tab: int = 0) -> Optional[T]:
        if self._time > time:
            if isinstance(self._value, Timed):
                return self._value.get_updated(time, tab + 1)
            else:
                return self._value

class TimedInt(Timed):
    T = int

    def __hash__(self) -> int:
        return hash(self._value)

class TimedBool(TimedInt):
    T = bool

class TimedFloat(Timed):
    T = float

class TimedSequence(Timed):
    T = Sequence

    def __getitem__(self, indices: Any) -> Any:
        return self._value.__getitem__(indices)


class TimedImmutableSequence(TimedSequence):
    def __hash__(self) -> int:
        return hash(self._value)

    def __iter__(self) -> Iterator:
        return self._value.__iter__()

    def __contains__(self, value: Any) -> bool:
        return value in self._value


class TimedStr(TimedImmutableSequence):
    T = str


class TimedMutableSequence(TimedSequence):
    T = Sequence

    def __setitem__(self, key: Any, value: Any) -> None:
        if key in self._value and self._value[key] == value:
            return
        self._value.__setitem__(key, value)
        self.set_time()


class TimedList(TimedMutableSequence):
    T = list

    def append(self, *args, **kwargs) -> None:
        if not isinstance(self._value, list):
            raise TypeError("Incompatible Value Type")
        self.set_time()
        self._value.append(*args, **kwargs)

    def remove(self, *args, **kwargs) -> None:
        if not isinstance(self._value, list):
            raise TypeError("Incompatible Value Type")
        self.set_time()
        self._value.remove(*args, **kwargs)


class TimedDict(TimedMutableSequence):
    T = dict

    def __init__(self, value: T, parent: Optional[Timed] = None):
        super().__init__({k: build_timed(v, self) for k, v in value.items()}, parent)

    def get_updated(self, time: datetime.datetime, tab: int = 0) -> Optional[T]:
        return {k: v.get_updated(time) for k, v in self._value.items()}

    def keys(self) -> list[Any]:
        return self._value.keys()

    def values(self) -> list[Timed]:
        return self._value.values()

    def items(self) -> list[tuple[Any, Timed]]:
        return self._value.items()


def build_timed(value: bool | dict | float | int | list | str | Timed, parent: Optional[Timed] = None):
    if isinstance(value, bool):
        return TimedBool(value, parent)
    elif isinstance(value, dict):
        return TimedDict(value, parent)
    elif isinstance(value, float):
        return TimedFloat(value, parent)
    elif isinstance(value, int):
        return TimedInt(value, parent)
    elif isinstance(value, list):
        return TimedList(value, parent)
    elif isinstance(value, str):
        return TimedStr(value, parent)
    elif isinstance(value, Timed):
        return Timed(value, parent)
    else:
        raise TypeError(f"Type of {type(value)} is not allowed")
