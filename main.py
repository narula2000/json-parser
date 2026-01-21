import argparse
import os
import sys


def setup_parser(arguments=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar="FILE", default="", type=str, nargs="*")
    return parser.parse_args(arguments)


class JsonExpcetion(Exception):
    pass


class JsonParser:
    def __init__(self, content: str | None) -> None:
        self.content = content or None
        self.index = 0

    def parse(self):
        if not self.content:
            raise JsonExpcetion("No content provided")
        return 0


def main(argv=None):
    arguments = setup_parser(argv)
    if arguments.files:
        for file in arguments.files:
            if not os.path.isfile(file):
                continue
            content = None
            with open(file) as reader:
                content: str | None = reader.read()

            try:
                parsed_json = JsonParser(content=content)
            except JsonExpcetion as e:
                print(e)
                sys.exit(1)

            print(f"Prased: {file}")
            print(parsed_json)
            print()

    sys.exit(0)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
