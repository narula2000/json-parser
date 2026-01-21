import argparse
import os
import sys

from json_parser import JsonException, JsonParser


def setup_parser(arguments=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar="FILE", default="", type=str, nargs="*")
    return parser.parse_args(arguments)


def main(argv=None):
    arguments = setup_parser(argv)
    if arguments.files:
        for file in arguments.files:
            if not os.path.isfile(file):
                continue

            print(f"Prasing: {file}")
            content = None
            with open(file) as reader:
                content: str | None = reader.read()

            try:
                json_parser = JsonParser(content=content)
                parsed_json = json_parser.parse()
            except JsonException as e:
                print(e)
                sys.exit(1)

            print(parsed_json)
            print()

    sys.exit(0)


if __name__ == "__main__":
    import sys

    # This ensure we can parse high nested JSON
    sys.setrecursionlimit(1_000_000)
    main(sys.argv[1:])
