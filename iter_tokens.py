#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
from dataclasses import dataclass
import re


tokens_dict = {
    "ID": r"[a-zA-Z]+\d*",
    "NUMBER": r"\d+",
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "EQ": r"=",
    "PLUS": r"\+",
    "MINUS": r"-",
    "STAR": r"\*",
    "DIVIDE": r"/",
    "WS": r"\s+",
}

test_str = "2+(3+4)*5"


@dataclass
class Token:
    name: str
    value: str


def iter_tokens(s: str) -> Iterator[Token]:
    master_pat = "|".join(
        rf"(?P<{tok_key}>{tok_re})" for tok_key, tok_re in tokens_dict.items()
    )
    for match in re.finditer(master_pat, s):
        yield Token(match.lastgroup, match.group())


if __name__ == "__main__":
    for tok in iter_tokens(test_str):
        print(tok)
