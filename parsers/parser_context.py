from abc import ABC, abstractmethod
from typing import Any


class ParseContext(ABC):
    @abstractmethod
    def _get_current_char(self) -> str:
        pass

    @abstractmethod
    def _get_next_char(self) -> str:
        pass

    @abstractmethod
    def _increment(self, n: int = 1) -> None:
        pass

    @abstractmethod
    def _get_index(self) -> int:
        pass

    @abstractmethod
    def _get_content(self) -> str:
        pass

    @abstractmethod
    def _peek_content(self, n: int) -> str:
        pass

    @abstractmethod
    def _slice_content(self, start: int, end: int) -> str:
        pass

    @abstractmethod
    def _parse_json(self) -> str | int | float | dict[str, str] | list[Any] | bool | None:
        pass
