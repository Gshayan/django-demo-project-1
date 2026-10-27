from fractions import Fraction
from typing import Any

def number_str_to_float(amount_str:str) -> tuple[Any, bool]:
    """
    Take in an amount string to return float (if possible).
    
    Valid string returns:
    Float
    Boolean -> True

    Invalid string Returns
    Original String
    Boolean -> False
    
    Examples:
    1 1/2 -> 1.5, True
    32 -> 32.0, True
    Abc -> Abc, False
    """
    try:
        text = str(amount_str).strip()

        if text is None:
            return amount_str, False
        
        number_as_float = float(sum(Fraction(s) for s in text.split()))
        return number_as_float, True
    except (ValueError, ZeroDivisionError):
        return amount_str, False
    