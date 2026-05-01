import pytest
from parser import ExpressionParser, Number, AddOp, MinusOp, MulOp, DivOp


# --- Helpers ---------------------------------------------------------------


def unwrap_number(node):
    assert isinstance(node, Number)
    return node.val


# --- Basic parsing ---------------------------------------------------------


def test_single_number():
    parser = ExpressionParser()
    res = parser.parse("42")

    assert isinstance(res, Number)
    assert res.val == 42


def test_simple_addition():
    parser = ExpressionParser()
    res = parser.parse("2 + 3")

    assert isinstance(res, AddOp)
    assert unwrap_number(res.left) == 2
    assert unwrap_number(res.right) == 3


def test_simple_subtraction():
    parser = ExpressionParser()
    res = parser.parse("5 - 1")

    assert isinstance(res, MinusOp)
    assert unwrap_number(res.left) == 5
    assert unwrap_number(res.right) == 1


# --- Operator precedence ---------------------------------------------------


def test_multiplication_precedence():
    parser = ExpressionParser()
    res = parser.parse("2 + 3 * 4")

    # Expected: 2 + (3 * 4)
    assert isinstance(res, AddOp)
    assert unwrap_number(res.left) == 2

    assert isinstance(res.right, MulOp)
    assert unwrap_number(res.right.left) == 3
    assert unwrap_number(res.right.right) == 4


def test_division_precedence():
    parser = ExpressionParser()
    res = parser.parse("8 / 2 + 1")

    # Expected: (8 / 2) + 1
    assert isinstance(res, AddOp)

    assert isinstance(res.left, DivOp)
    assert unwrap_number(res.left.left) == 8
    assert unwrap_number(res.left.right) == 2

    assert unwrap_number(res.right) == 1


# --- Parentheses -----------------------------------------------------------


def test_parentheses_override_precedence():
    parser = ExpressionParser()
    res = parser.parse("(2 + 3) * 4")

    assert isinstance(res, MulOp)
    assert unwrap_number(res.right) == 4

    assert isinstance(res.left, AddOp)
    assert unwrap_number(res.left.left) == 2
    assert unwrap_number(res.left.right) == 3


# --- Nested expressions ----------------------------------------------------


def test_nested_expression():
    parser = ExpressionParser()
    res = parser.parse("(1 + (2 * 3))")

    assert isinstance(res, AddOp)
    assert unwrap_number(res.left) == 1

    inner = res.right
    assert isinstance(inner, MulOp)
    assert unwrap_number(inner.left) == 2
    assert unwrap_number(inner.right) == 3


# --- Error handling --------------------------------------------------------


def test_missing_closing_parenthesis():
    parser = ExpressionParser()

    with pytest.raises(SyntaxError):
        parser.parse("(2 + 3")


def test_unexpected_token():
    parser = ExpressionParser()

    with pytest.raises(SyntaxError):
        parser.parse("2 + )")


# --- Internal mechanics ----------------------------------------------------


def test_advance_returns_none_at_end():
    parser = ExpressionParser()
    parser.tokens = iter([])

    result = parser.advance()
    assert result is None


# --- Logging side-effect (visible with -s) ---------------------------------


def test_logging_side_effect(caplog):
    parser = ExpressionParser()

    with caplog.at_level("INFO"):
        parser.parse("1 + 2")

    # Ensure trace decorator actually logs something
    assert any("Starting expr" in message for message in caplog.text.splitlines())
