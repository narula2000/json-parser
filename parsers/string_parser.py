from parsers.exceptions import JsonException
from parsers.parser_context import ParseContext
from parsers.white_space_parser import WhiteSpaceParser


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
