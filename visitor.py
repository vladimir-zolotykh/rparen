#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import parser as PR


class Visitor:
    def visit(self, node):
        self.method_name = "visit" + type(node).__name__
        method = getattr(self, self.method_name, self.visit_generic)
        return method(node)

    def visit_generic(self, node):
        raise ValueError(f"No method {self.method_name} of {self.__class__} found")


# class Number(Node): ...
# class UnaryOp(Node): ...
# class BinaryOp(Node): ...
# class AddOp(BinaryOp): ...
# class MinusOp(BinaryOp): ...
# class MulOp(BinaryOp): ...
# class DivOp(BinaryOp): ...


class VisitEvaluate(Visitor):
    def visitAddOp(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visitMinusOp(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visitMulOp(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visitDivOp(self, node):
        return self.visit(node.left) / self.visit(node.right)

    def visitNumber(self, node):
        return node.val


class VisitInfix(Visitor):
    def visitAddOp(self, node):
        return f"(+ {self.visit(node.left)} {self.visit(node.right)})"

    def visitMinuxOp(self, node):
        return f"(- {self.visit(node.left)} {self.visit(node.right)})"

    def visitMulOp(self, node):
        return f"(* {self.visit(node.left)} {self.visit(node.right)})"

    def visitDivOp(self, node):
        return f"(/ {self.visit(node.left)} {self.visit(node.right)})"

    def visitNumber(self, node):
        return str(node.val)


if __name__ == "__main__":
    parser = PR.ExpressionParser()
    node = parser.parse("2 + ( 3 + 4 ) * 5")
    print(VisitEvaluate().visit(node))
    print(VisitInfix().visit(node))
