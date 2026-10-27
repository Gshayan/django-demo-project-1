import pint
from pint.errors import UndefinedUnitError
from django.core.exceptions import ValidationError

def valid_units_check(value):
    ureg = pint.UnitRegistry()
    try:
        valid_unit = ureg(value)
    except UndefinedUnitError as e:
        raise ValidationError(f"{value} is not a valid unit of measure!")
    except:
        raise ValidationError(f"{value} is invalid!")