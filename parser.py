#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Iterator, Any, Optional
from dataclasses import dataclass
from functools import wraps
import logging
from iter_tokens import iter_tokens, Token, test_str


@dataclass
class Node:
    val: Any


@dataclass
class Number(Node):
    val: int


@dataclass
class UnaryOp(Node):
    child: Node


@dataclass
class BinaryOp(Node):
    left: Node
    right: Node


@dataclass
class AddOp(BinaryOp):
    pass


@dataclass
class MinusOp(BinaryOp):
    pass


@dataclass
class MulOp(BinaryOp):
    pass


@dataclass
class DivOp(BinaryOp):
    pass


def trace_when_called(trace_it=True):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if trace_it:
                logging.getLogger(__name__).info(f"Starting {func.__name__} ...")
            res = func(*args, **kwargs)
            if trace_it and not (res is None):
                logging.getLogger(__name__).info(f"{func.__name__} returned {res!r}")
            return res

        return wrapper

    return deco


logging.basicConfig(level=logging.DEBUG, filename="./.parser.log", filemode="w")


@dataclass
class ExpressionParser:
    tok: Optional[Token] = None
    token: Optional[Token] = None
    tokens: Optional[Iterator[Token]] = None

    @trace_when_called()
    def expr(self) -> Node:
        res = self.term()
        while (op := self.advance()).val in ("+", "-"):
            right = self.term()
            if op == "+":
                res = AddOp(res, right)
            else:
                res = MinusOp(res, right)
        return res

    @trace_when_called()
    def term(self) -> Node:
        res = self.factor()
        while (op := self.advance()).val in ("*", "/"):
            right = self.factor()
            if op == "*":
                res = MulOp(res, right)
            else:
                res = DivOp(res, right)
        return res

    @trace_when_called()
    def consume(self):
        self.token = self.tok
        self.tok = None

    @trace_when_called()
    def advance(self) -> Token:
        self.token = self.tok
        self.tok = next(self.tokens)
        return self.tok

    @trace_when_called(False)
    def expect(self, expected: str):
        if self.tok.val != expected:
            raise SyntaxError(f"Expected {expected!r}, got {self.tok.val!r}")
        self.advance()

    @trace_when_called()
    def factor(self) -> Node:
        # tok = self.advance()
        if self.tok.val == "(":
            self.advance()
            res = self.expr()
            self.expect(")")
            return res
        else:
            return Number(self.tok.val)

    @trace_when_called()
    def parse(self, expr: str) -> Node:
        self.tokens: Iterator[Token] = iter_tokens(expr)
        self.advance()
        return self.expr()


if __name__ == "__main__":
    parser = ExpressionParser()
    res = parser.parse(test_str)
    print(res)
