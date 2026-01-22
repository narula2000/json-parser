from typing import Any

from parsers.array_parser import ArrayParser
from parsers.exceptions import JsonException
from parsers.keyword_parser import KeywordParser
from parsers.number_parser import NumberParser
from parsers.object_parser import ObjectParser
from parsers.parser_context import ParseContext
from parsers.string_parser import StringParser
from parsers.white_space_parser import WhiteSpaceParser


class JsonParser(ParseContext):
    def __init__(self, content: str | None) -> None:
        if not content:
            raise JsonException("No content provided")
        self.content: str = content
        self.index: int = 0
        self.white_space_parser = WhiteSpaceParser(self)
        self.string_parser = StringParser(self)
        self.number_parser = NumberParser(self)
        self.keyword_parser = KeywordParser(self)
        self.array_parser = ArrayParser(self)
        self.object_parser = ObjectParser(self)

    def _get_current_char(self) -> str:
        if self.index < len(self.content):
            return self.content[self.index]
        raise IndexError

    def _get_next_char(self) -> str:
        if self.index < len(self.content):
            return self.content[self.index + 1]
        raise IndexError

    def _increment(self, n: int = 1) -> None:
        self.index += n

    def _get_index(self) -> int:
        return self.index

    def _get_content(self) -> str:
        return self.content

    def _peek_content(self, n: int) -> str:
        return self.content[n]

    def _slice_content(self, start: int, end: int) -> str:
        return self.content[start:end]

    def _parse_json(self) -> str | int | float | dict[str, str] | list[Any] | bool | None:
        parsed_json = self.string_parser.parse()
        if parsed_json is None:
            parsed_json = self.number_parser.parse()
        if parsed_json is None:
            parsed_json = self.object_parser.parse()
        if parsed_json is None:
            parsed_json = self.array_parser.parse()
        if parsed_json is None:
            parsed_json = self.keyword_parser.parse(keyword="true", value=True)
        if parsed_json is None:
            parsed_json = self.keyword_parser.parse(keyword="false", value=False)
        if parsed_json is None:
            parsed_json = self.keyword_parser.parse(keyword="null", value=None)

        return parsed_json

    def parse(self):
        if not self.content:
            raise JsonException("No content provided")

        self.white_space_parser.parse()
        if self._get_current_char() not in ["[", "{"]:
            raise JsonException("JSON need to start with array or object")

        parsed_json = self._parse_json()

        try:
            self.white_space_parser.parse()
            self._get_current_char()
            raise JsonException("JSON contains extra characters after closing")
        except IndexError:
            pass

        return parsed_json
