import argparse
import os
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any


class TokensEnum(Enum):
    ObjectOpen = "{"
    ObjectClose = "}"


@dataclass
class Token:
    token: Any
    value: str


def setup_parser(arguments=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar="FILE", default="", type=str, nargs="*")
    return parser.parse_args(arguments)


def tokenizer(bytes):
    tokens = []
    for char in bytes.decode():
        if char == TokensEnum.ObjectOpen.value:
            tokens.append(Token(TokensEnum.ObjectOpen, char))
        if char == TokensEnum.ObjectClose.value:
            tokens.append(Token(TokensEnum.ObjectClose, char))

    if len(tokens) < 2:  # Not enough tokens to be valid
        sys.exit(1)

    return tokens


def parser(tokens):
    objects = []
    for token in tokens:
        if token.token is TokensEnum.ObjectOpen:
            objects.append(token)
        elif token.token is TokensEnum.ObjectClose:
            try:
                objects.pop()
            except IndexError:
                sys.exit(1)

    if len(objects) != 0:  # Still have open object
        sys.exit(1)


def main(argv=None):
    arguments = setup_parser(argv)
    if arguments.files:
        file = arguments.files[0]
        if os.path.isfile(file):
            with open(file, "rb") as bytes:
                tokens = tokenizer(bytes.read())
                parser(tokens)
    sys.exit(0)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
