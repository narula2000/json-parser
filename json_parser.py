from abc import ABC, abstractmethod
from typing import Any


class JsonException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


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


class SeperatorParser:
    def __init__(self, ctx: ParseContext) -> None:
        self.ctx = ctx

    def process_comma(self) -> None:
        pass
        if self.ctx._get_current_char() != ",":
            raise JsonException("JSON expected ','")
        self.ctx._increment()

    def process_colon(self) -> None:
        if self.ctx._get_current_char() != ":":
            raise JsonException("JSON expected ':'")
        self.ctx._increment()


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
        self.array_parser = ArraryParser(self)
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


class WhiteSpaceParser:
    def __init__(self, ctx: ParseContext) -> None:
        self.ctx = ctx
        self.white_spaces = [" ", "\t", "\n", "\r"]

    def _is_white_space(self, char: str) -> bool:
        return char in self.white_spaces

    def parse(self) -> None:
        while self.ctx._get_index() < len(self.ctx._get_content()) and self._is_white_space(
            self.ctx._get_current_char()
        ):
            self.ctx._increment()


class StringParser:
    def __init__(self, ctx: ParseContext) -> None:
        self.ctx = ctx
        self.white_space_parser = WhiteSpaceParser(ctx)
        self.valid_backslash_escape = ['"', "\\", "/", "b", "f", "n", "r", "t"]

    def _is_hexadecimal(self, char: str) -> bool:
        try:
            int(char, 16)
            return True
        except ValueError:
            return False

    def parse(self) -> str | None:
        parsed_string = None
        if self.ctx._get_current_char() == '"':
            parsed_string = ""
            self.ctx._increment()
            self.white_space_parser.parse()
            while self.ctx._get_current_char() != '"':
                if self.ctx._get_current_char() == "\\":  # Check for illegal backslash
                    next = self.ctx._get_next_char()
                    if next in self.valid_backslash_escape:
                        parsed_string += next
                        self.ctx._increment()
                    elif next == "u":
                        hex_digits = ""

                        for offset in range(2, 6):  # self.index+2 → self.index+5
                            adjusted_offset = self.ctx._get_index() + offset
                            char = self.ctx._peek_content(adjusted_offset)
                            if not self._is_hexadecimal(char):
                                raise JsonException("JSON illegal Unicode escape sequence")
                            hex_digits += char

                        parsed_string += chr(int(hex_digits, 16))
                        self.ctx._increment(5)
                    else:
                        raise JsonException("JSON illegal backslash")
                else:
                    if self.ctx._get_current_char() == "\t":
                        raise JsonException("JSON tab character in string")
                    elif self.ctx._get_current_char() == "\n":
                        raise JsonException("JSON new line character in string")
                    else:
                        parsed_string += self.ctx._get_current_char()
                self.ctx._increment()
            self.ctx._increment()
        return parsed_string


class NumberParser:
    def __init__(self, ctx: ParseContext) -> None:
        self.ctx = ctx

    def parse(self) -> int | float | None:
        start = self.ctx._get_index()

        if self.ctx._get_current_char() == "-":
            self.ctx._increment()

        if self.ctx._get_current_char() == "0":
            self.ctx._increment()
        elif self.ctx._get_current_char().isnumeric():
            self.ctx._increment()
            while self.ctx._get_current_char().isnumeric():
                self.ctx._increment()

        if self.ctx._get_current_char() == ".":
            self.ctx._increment()
            while self.ctx._get_current_char().isnumeric():
                self.ctx._increment()

        if self.ctx._get_current_char().lower() == "e":
            self.ctx._increment()
            if self.ctx._get_current_char() in ["-", "+"]:
                self.ctx._increment()
            while self.ctx._get_current_char().isnumeric():
                self.ctx._increment()

        if self.ctx._get_index() > start:
            number = self.ctx._slice_content(start=start, end=self.ctx._get_index())

            try:
                number = float(number)
            except ValueError:
                raise JsonException("JSON invlaid number")

            return int(number) if number % 1 == 0 else number


class KeywordParser:
    def __init__(self, ctx: ParseContext) -> None:
        self.ctx = ctx

    def parse(self, keyword: str, value: bool | None) -> bool | None:
        start = self.ctx._get_index()
        end = self.ctx._get_index() + len(keyword)
        to_check_keyword = self.ctx._slice_content(start=start, end=end)
        if to_check_keyword == keyword:
            self.ctx._increment(len(keyword))
            return value
        if keyword == "null":
            raise JsonException("JSON missing value")


class ArraryParser:
    def __init__(self, ctx: ParseContext) -> None:
        self.ctx = ctx
        self.white_space_parser = WhiteSpaceParser(ctx)
        self.seperator_parser = SeperatorParser(ctx)

    def parse(self) -> list[Any] | None:
        if self.ctx._get_current_char() == "[":
            self.ctx._increment()
            self.white_space_parser.parse()

            array = []
            init = True

            try:
                while self.ctx._get_current_char() != "]":
                    if not init:
                        self.seperator_parser.process_comma()
                        self.white_space_parser.parse()
                    value = self.ctx._parse_json()
                    self.white_space_parser.parse()
                    array.append(value)
                    init = False
            except IndexError:
                raise JsonException("JSON missing closing array")

            self.ctx._increment()

            return array


class ObjectParser:
    def __init__(self, ctx: ParseContext) -> None:
        self.ctx = ctx
        self.white_space_parser = WhiteSpaceParser(ctx)
        self.string_parser = StringParser(ctx)
        self.seperator_parser = SeperatorParser(ctx)

    def parse(self) -> dict[str, str] | None:
        if self.ctx._get_current_char() == "{":
            self.ctx._increment()
            self.white_space_parser.parse()

            parsed_object = {}
            init = True
            try:
                while self.ctx._get_current_char() != "}":
                    if not init:
                        self.white_space_parser.parse()
                        self.seperator_parser.process_comma()
                        self.white_space_parser.parse()

                    key = self.string_parser.parse()
                    self.white_space_parser.parse()
                    self.seperator_parser.process_colon()
                    self.white_space_parser.parse()
                    value = self.ctx._parse_json()
                    parsed_object[key] = value
                    self.white_space_parser.parse()
                    init = False
            except IndexError:
                raise JsonException("JSON missing closing object")
            self.ctx._increment()
            return parsed_object
