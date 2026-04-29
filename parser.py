#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Iterator, Any
from dataclasses import dataclass
from iter_tokens import iter_tokens, Token


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


class ExpressionParser:
    def expr(self) -> Node:
        res = self.term()
        while (op := next(self.tokens)).val in ("+", "-"):
            right = self.expr()
            if op == "+":
                res = AddOp(res, right)
            else:
                res = MinusOp(res, right)
        return res

    def term(self) -> Node:
        res = self.factor()
        while (op := next(self.tokens)).val in ("*", "/"):
            right = self.term()
            if op == "*":
                res = MulOp(res, right)
            else:
                res = DivOp(res, right)
        return res

    def factor(self) -> Node:
        tok = next(self.tokens)
        if tok.val == "LPAREN":
            res = self.expr()
            self.expect("RPAREN")
            return res
        else:
            return Number(tok.val)

    def parse(self, expr: str) -> Node:
        self.tokens: Iterator[Token] = iter_tokens(expr)
        return self.expr()
