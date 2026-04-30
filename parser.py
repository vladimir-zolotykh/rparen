#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Iterator, Any
from dataclasses import dataclass
from functools import wraps
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


def trace_when_called(trace_id=True):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if trace_id:
                print(f"{func.__name__} is called")
            res = func(*args, **kwargs)
            return res

        return wrapper

    return deco


class ExpressionParser:
    @trace_when_called()
    def expr(self) -> Node:
        res = self.term()
        while (op := next(self.tokens)).val in ("+", "-"):
            right = self.term()
            if op == "+":
                res = AddOp(res, right)
            else:
                res = MinusOp(res, right)
        return res

    @trace_when_called()
    def term(self) -> Node:
        res = self.factor()
        while (op := next(self.tokens)).val in ("*", "/"):
            right = self.factor()
            if op == "*":
                res = MulOp(res, right)
            else:
                res = DivOp(res, right)
        return res

    @trace_when_called(False)
    def expect(self, expected: str):
        tok: Token = next(self.tokens)
        if tok.val != expected:
            raise SyntaxError(f"Expected {expected!r}, got {tok.val!r}")

    @trace_when_called()
    def factor(self) -> Node:
        tok = next(self.tokens)
        if tok.val == "(":
            res = self.expr()
            self.expect(")")
            return res
        else:
            return Number(tok.val)

    @trace_when_called()
    def parse(self, expr: str) -> Node:
        self.tokens: Iterator[Token] = iter_tokens(expr)
        return self.expr()


if __name__ == "__main__":
    parser = ExpressionParser()
    res = parser.parse(test_str)
    print(res)
