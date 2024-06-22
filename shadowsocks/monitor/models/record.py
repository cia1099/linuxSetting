from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Record:
    asctime: str
    new: str
    old: str
    detail: str

    @staticmethod
    def from_dict(obj: Any) -> "Record":
        assert isinstance(obj, dict)
        asctime = from_str(obj.get("asctime"))
        new = from_str(obj.get("new"))
        old = from_str(obj.get("old"))
        detail = from_str(obj.get("detail"))
        return Record(asctime, new, old, detail)

    def to_dict(self) -> dict:
        result: dict = {}
        result["asctime"] = from_str(self.asctime)
        result["new"] = from_str(self.new)
        result["old"] = from_str(self.old)
        result["detail"] = from_str(self.detail)
        return result


def record_from_dict(s: Any) -> Record:
    return Record.from_dict(s)


def record_to_dict(x: Record) -> Any:
    return to_class(Record, x)
