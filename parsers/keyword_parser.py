from parsers.exceptions import JsonException
from parsers.parser_context import ParseContext


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
