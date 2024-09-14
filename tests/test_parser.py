# tests/test_parser.py

import pytest
from autoreason.parser import parse_formula

@pytest.mark.parametrize(
    "formula, expected",
    [
        ("A AND B", ("AND", ("VAR", "A"), ("VAR", "B"))),
        ("NOT A", ("NOT", ("VAR", "A"))),
        ("(A OR B) IMPLIES (C AND D)", 
         ("IMPLIES", ("OR", ("VAR", "A"), ("VAR", "B")), ("AND", ("VAR", "C"), ("VAR", "D")))),
        ("FORALL(x, A(x) IMPLIES B(x))", 
         ("FORALL", "x", ("IMPLIES", ("FUNC", "A", [("VAR", "x")]), ("FUNC", "B", [("VAR", "x")])))),
        ("EXISTS(y, NOT P(y))", ("EXISTS", "y", ("NOT", ("FUNC", "P", [("VAR", "y")])))),
        ("TRUE", "TRUE"),
        ("FALSE", "FALSE"),
        # Add more test cases as needed
    ]
)
def test_parse_formula(formula, expected):
    """
    Test the parse_formula function with different logical expressions.
    """
    result = parse_formula(formula)
    assert result == expected, f"Failed for formula: {formula}. Got {result}, expected {expected}."


@pytest.mark.parametrize(
    "formula",
    [
        "FORALL x, A(x) IMPLIES B(x)",  # Missing parentheses
        "A AND",  # Incomplete expression
        "NOT",  # Missing operand
        "(A OR B",  # Unmatched parentheses
        "FORALL(x, (A(x)) IMPLIES B(x))",  # Extra parentheses
    ]
)
def test_parse_formula_invalid(formula):
    """
    Test the parse_formula function with invalid logical expressions.
    """
    result = parse_formula(formula)
    assert result is None, f"Expected None for invalid formula: {formula}, but got {result}."
