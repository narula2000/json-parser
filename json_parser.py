from typing import Any


WHITE_SPACES = [" ", "\t", "\n", "\r"]
VALID_BACKSLASH_ESCAPE = ['"', "\\", "/", "b", "f", "n", "r", "t"]


class JsonException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class JsonParser:
    def __init__(self, content: str | None) -> None:
        if not content:
            raise JsonException("No content provided")
        self.content: str = content
        self.index: int = 0
        self.white_space_parser = WhiteSpaceParser(self)
        self.string_parser = StringParser(self)

    def _get_current_char(self) -> str:
        if self.index < len(self.content):
            return self.content[self.index]
        raise IndexError

    def _get_next_char(self) -> str:
        if self.index < len(self.content):
            return self.content[self.index + 1]
        raise IndexError

    def _parse_number(self) -> int | float | None:
        start = self.index

        if self._get_current_char() == "-":
            self.index += 1

        if self._get_current_char() == "0":
            self.index += 1
        elif self._get_current_char().isnumeric():
            self.index += 1
            while self._get_current_char().isnumeric():
                self.index += 1

        if self._get_current_char() == ".":
            self.index += 1
            while self._get_current_char().isnumeric():
                self.index += 1

        if self._get_current_char().lower() == "e":
            self.index += 1
            if self._get_current_char() in ["-", "+"]:
                self.index += 1
            while self._get_current_char().isnumeric():
                self.index += 1

        if self.index > start:
            number = self.content[start : self.index]

            try:
                number = float(number)
            except ValueError:
                raise JsonException("JSON invlaid number")

            return int(number) if number % 1 == 0 else number

    def _process_comma(self) -> None:
        if self._get_current_char() != ",":
            raise JsonException("JSON expected ','")
        self.index += 1

    def _process_colon(self) -> None:
        if self._get_current_char() != ":":
            raise JsonException("JSON expected ':'")
        self.index += 1

    def _parse_object(self) -> dict[str, str] | None:
        if self._get_current_char() == "{":
            self.index += 1
            self.white_space_parser.parse()

            parsed_object = {}
            init = True
            try:
                while self._get_current_char() != "}":
                    if not init:
                        self.white_space_parser.parse()
                        self._process_comma()
                        self.white_space_parser.parse()

                    key = self.string_parser.parse()
                    self.white_space_parser.parse()
                    self._process_colon()
                    self.white_space_parser.parse()
                    value = self._parse_json()
                    parsed_object[key] = value
                    self.white_space_parser.parse()
                    init = False
            except IndexError:
                raise JsonException("JSON missing closing object")
            self.index += 1
            return parsed_object

    def _parse_array(self) -> list[Any] | None:
        if self._get_current_char() == "[":
            self.index += 1
            self.white_space_parser.parse()

            array = []
            init = True

            try:
                while self._get_current_char() != "]":
                    if not init:
                        self._process_comma()
                        self.white_space_parser.parse()
                    value = self._parse_json()
                    self.white_space_parser.parse()
                    array.append(value)
                    init = False
            except IndexError:
                raise JsonException("JSON missing closing array")

            self.index += 1

            return array

    def _parse_keyword(self, keyword: str, value: bool | None) -> bool | None:
        to_check_keyword = self.content[self.index : self.index + len(keyword)]
        if to_check_keyword == keyword:
            self.index += len(keyword)
            return value
        if keyword == "null":
            raise JsonException("JSON missing value")

    def _parse_json(self) -> str | int | float | dict[str, str] | list[Any] | bool | None:
        parsed_json = self.string_parser.parse()
        if parsed_json is None:
            parsed_json = self._parse_number()
        if parsed_json is None:
            parsed_json = self._parse_object()
        if parsed_json is None:
            parsed_json = self._parse_array()
        if parsed_json is None:
            parsed_json = self._parse_keyword(keyword="true", value=True)
        if parsed_json is None:
            parsed_json = self._parse_keyword(keyword="false", value=False)
        if parsed_json is None:
            parsed_json = self._parse_keyword(keyword="null", value=None)

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
    def __init__(self, json_parser: JsonParser) -> None:
        self.json_parser = json_parser

    def _is_white_space(self, char: str) -> bool:
        return char in WHITE_SPACES

    def parse(self) -> None:
        while self.json_parser.index < len(self.json_parser.content) and self._is_white_space(
            self.json_parser._get_current_char()
        ):
            self.json_parser.index += 1


class StringParser:
    def __init__(self, json_parser: JsonParser) -> None:
        self.json_parser = json_parser
        self.white_space_parser = WhiteSpaceParser(json_parser)

    def _is_hexadecimal(self, char: str) -> bool:
        try:
            int(char, 16)
            return True
        except ValueError:
            return False

    def parse(self) -> str | None:
        parsed_string = None
        if self.json_parser._get_current_char() == '"':
            parsed_string = ""
            self.json_parser.index += 1
            self.white_space_parser.parse()
            while self.json_parser._get_current_char() != '"':
                if self.json_parser._get_current_char() == "\\":  # Check for illegal backslash
                    next = self.json_parser._get_next_char()
                    if next in VALID_BACKSLASH_ESCAPE:
                        parsed_string += next
                        self.json_parser.index += 1
                    elif next == "u":
                        hex_digits = ""

                        for offset in range(2, 6):  # self.index+2 → self.index+5
                            char = self.json_parser.content[self.json_parser.index + offset]
                            if not self._is_hexadecimal(char):
                                raise JsonException("JSON illegal Unicode escape sequence")
                            hex_digits += char

                        parsed_string += chr(int(hex_digits, 16))
                        self.json_parser.index += 5
                    else:
                        raise JsonException("JSON illegal backslash")
                else:
                    if self.json_parser._get_current_char() == "\t":
                        raise JsonException("JSON tab character in string")
                    elif self.json_parser._get_current_char() == "\n":
                        raise JsonException("JSON new line character in string")
                    else:
                        parsed_string += self.json_parser._get_current_char()
                self.json_parser.index += 1
            self.json_parser.index += 1
        return parsed_string
