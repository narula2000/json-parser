from parsers.exceptions import JsonException
from parsers.parser_context import ParseContext


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
            except ValueError as err:
                raise JsonException("JSON invlaid number") from err

            return int(number) if number % 1 == 0 else number
