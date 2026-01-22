from parsers.exceptions import JsonException
from parsers.parser_context import ParseContext


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
