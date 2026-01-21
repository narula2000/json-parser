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

    def _is_white_space(self, char: str) -> bool:
        return char in [" ", "\t", "\n", "\r"]

    def _skip_white_spaces(self) -> None:
        while self.index < len(self.content) and self._is_white_space(self._get_current_char()):
            self.index += 1

    def _get_current_char(self) -> str:
        if self.index < len(self.content):
            return self.content[self.index]
        raise IndexError

    def _get_next_char(self) -> str:
        if self.index < len(self.content):
            return self.content[self.index + 1]
        raise IndexError

    def _is_hexadecimal(self, char: str) -> bool:
        try:
            int(char, 16)
            return True
        except ValueError:
            return False

    def _parse_string(self) -> str | None:
        parsed_json = None
        if self._get_current_char() == '"':
            parsed_json = ""
            self.index += 1
            self._skip_white_spaces()
            while self._get_current_char() != '"':
                if self._get_current_char() == "\\":
                    next = self._get_next_char()
                    if next in ['"', "\\", "/", "b", "f", "n", "r", "t"]:
                        parsed_json += next
                        self.index += 1
                    elif next == "u":  # Chcek of hexadecimal
                        hex_digits = ""

                        for offset in range(2, 6):  # self.i+2 → self.i+5
                            char = self.content[self.index + offset]
                            if not self._is_hexadecimal(char):
                                raise JsonException("JSON illegal Unicode escape sequence")
                            hex_digits += char

                        parsed_json += chr(int(hex_digits, 16))
                        self.index += 5
                else:
                    if self._get_current_char() == "\t":
                        raise JsonException("JSON tab character in string")
                    elif self._get_current_char() == "\n":
                        raise JsonException("JSON new line character in string")
                    else:
                        parsed_json += self._get_current_char()
                self.index += 1
            self.index += 1
        return parsed_json

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
            self._skip_white_spaces()

            parsed_json = {}
            init = True

            while self._get_current_char() != "}":
                if not init:
                    self._skip_white_spaces()
                    self._process_comma()
                    self._skip_white_spaces()

                key = self._parse_string()
                self._skip_white_spaces()
                self._process_colon()
                self._skip_white_spaces()
                value = self._parse_json()
                parsed_json[key] = value
                self._skip_white_spaces()
                init = False
            self.index += 1
            return parsed_json

    def _parse_keyword(self, keyword: str, value: bool | None) -> bool | None:
        to_check_keyword = self.content[self.index : self.index + len(keyword)]
        if to_check_keyword == keyword:
            self.index += len(keyword)
            return value
        if keyword == "null":
            raise JsonException("JSON missing value")

    def _parse_json(self) -> str | dict[str, str] | int | float | bool | None:
        parsed_json = self._parse_string()
        if parsed_json is None:
            parsed_json = self._parse_number()
        if parsed_json is None:
            parsed_json = self._parse_object()
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

        self._skip_white_spaces()
        if self._get_current_char() not in ["[", "{"]:
            raise JsonException("JSON need to start with array or object")

        parsed_json = self._parse_json()

        try:
            self._skip_white_spaces()
            self._get_current_char()
            raise JsonException("JSON contains extra characters after closing")
        except IndexError:
            pass

        return parsed_json
