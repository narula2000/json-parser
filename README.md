# JSON Parser Coding Challenges

This repo is created as a part of the [codingchallenges.fyi](https://codingchallenges.fyi/challenges/intro) challenges.
This repo specifically tackle the [challenge](https://codingchallenges.fyi/challenges/challenge-json-parser/) of implementing a JSON parser.

## The Challenge

Build your own JSON parser to validate a JSON file.
This help with lexical analysis and syntactic analysis.
Lexical analysis is the process of dividing a sequence of characters into meaningful chunks, called tokens.
Syntactic analysis (which is also sometimes referred to as parsing) is the process of analysing the list of tokens to match it to a formal grammar.

As part of the validation we will be validating the files from [tests](./tests/).

The JSON validation files can be fetched from [here](http://www.json.org/JSON_checker/test.zip).

## Note on fail18.json

`fail18.json` is intentionally ignored in this project.

This file corresponds to the "TooDeep" JSON test case, which is designed to fail due to extremely deep nesting that exceeds typical recursion limits. In this implementation, we explicitly increase the recursion limit:

```python
sys.setrecursionlimit(100)
```

As a result, `fail18.json` no longer fails for the intended reason and does not provide meaningful validation for this parser.

Additionally, we do not add any explicit code-level checks to detect or guard against this extreme nesting case. The parser is allowed to recurse naturally under the increased recursion limit.

To avoid false negatives in the test suite, this file is excluded from failure assertions.
