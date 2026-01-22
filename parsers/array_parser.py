from typing import Any

from parsers.exceptions import JsonException
from parsers.parser_context import ParseContext
from parsers.seperator_parser import SeperatorParser
from parsers.white_space_parser import WhiteSpaceParser


class ArrayParser:
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
            except IndexError as err:
                raise JsonException("JSON missing closing array") from err

            self.ctx._increment()

            return array
