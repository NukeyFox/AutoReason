from typing import Any, List, Tuple, Union
from lark import Lark, Transformer, v_args, Tree, Token

# Define the updated grammar for logical expressions
logic_grammar: str = """
    ?start: expr

    ?expr: expr "AND" expr     -> and_op
         | expr "OR" expr      -> or_op
         | "NOT" expr          -> not_op
         | expr "IMPLIES" expr -> implies_op
         | expr "IFF" expr     -> iff_op
         | "(" expr ")"
         | atom

    ?atom: VAR "(" args ")"    -> func_call  // Added support for function-like terms
         | VAR                 -> var
         | "TRUE"              -> true
         | "FALSE"             -> false
         | quantifier "(" VAR "," expr ")" -> quantified_expr

    args: expr ("," expr)*

    quantifier: "FORALL" | "EXISTS"

    VAR: /[a-zA-Z_][a-zA-Z0-9_]*/

    %import common.WS
    %ignore WS
"""

# Create the Lark parser
logic_parser: Lark = Lark(logic_grammar, start='start', parser='lalr')

# Define the type for the parsed formula
ParsedFormula = Union[
    Tuple[str, Any],  # Handles AND, OR, NOT, IMPLIES, IFF, FUNC, VAR, QUANTIFIER
    str,  # Handles TRUE, FALSE
]

# Transformer to convert parse tree to a more usable structure
@v_args(inline=True)
class LogicTransformer(Transformer):
    def and_op(self, left: Any, right: Any) -> ParsedFormula:
        return ("AND", left, right)
    
    def or_op(self, left: Any, right: Any) -> ParsedFormula:
        return ("OR", left, right)
    
    def not_op(self, expr: Any) -> ParsedFormula:
        return ("NOT", expr)
    
    def implies_op(self, left: Any, right: Any) -> ParsedFormula:
        return ("IMPLIES", left, right)
    
    def iff_op(self, left: Any, right: Any) -> ParsedFormula:
        return ("IFF", left, right)
    
    def var(self, name: Token) -> ParsedFormula:
        return ("VAR", str(name))
    
    def func_call(self, func_name: Token, *args: Any) -> ParsedFormula:
        return ("FUNC", str(func_name), list(args))  # Function-like term handling

    def true(self) -> ParsedFormula:
        return "TRUE"
    
    def false(self) -> ParsedFormula:
        return "FALSE"
    
    def quantified_expr(self, quantifier: Token, var: Token, expr: Any) -> ParsedFormula:
        return (str(quantifier).upper(), str(var), expr)

    def args(self, *args: Any) -> List[Any]:
        return list(args)

# Instantiate the transformer
transformer = LogicTransformer()

# Define a function to parse logical formulas
def parse_formula(formula: str) -> Union[ParsedFormula, None]:
    """
    Parse a logical formula and return a structured representation.

    :param formula: A string representing the logical formula to parse
    :return: A structured representation of the formula or None if parsing fails
    """
    try:
        # Parse the formula
        parse_tree: Tree = logic_parser.parse(formula)
        # Transform the parse tree to a more usable form
        result: ParsedFormula = transformer.transform(parse_tree)
        return result
    except Exception as e:
        print(f"Error parsing formula: {e}")
        return None

# Test the parser
if __name__ == "__main__":
    formulas: List[str] = [
        "A AND B",
        "NOT A",
        "(A OR B) IMPLIES (C AND D)",
        "FORALL(x, A(x) IMPLIES B(x))",
        "EXISTS(y, NOT P(y))"
    ]
    
    for formula in formulas:
        print(f"Formula: {formula}")
        parsed = parse_formula(formula)
        print(f"Parsed: {parsed}\n")
