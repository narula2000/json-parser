from parsers.exceptions import JsonException
from parsers.parser_context import ParseContext
from parsers.seperator_parser import SeperatorParser
from parsers.string_parser import StringParser
from parsers.white_space_parser import WhiteSpaceParser


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
            except IndexError as err:
                raise JsonException("JSON missing closing object") from err
            self.ctx._increment()
            return parsed_object
