from parsers.parser_context import ParseContext


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
