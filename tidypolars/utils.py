import polars as pl
from operator import not_
from itertools import chain

__all__ = []

def _list_flatten(l):
    l = [x if isinstance(x, list) else [x] for x in l]
    return list(chain.from_iterable(l))

def _as_list(x):
    if type(x) == type:
        return [x]
    elif _safe_len(x) == 0:
        return []
    elif _is_tuple(x):
        # Helpful to convert args to a list
        x = [val.to_list() if _is_series(val) else val for val in x]
        x = _list_flatten(x)
        return x
    else:
        return [*x]

# Convert kwargs to col() expressions with alias
def _kwargs_as_exprs(kwargs):
    return [expr.alias(key) for key, expr in kwargs.items()]

def _safe_len(x):
    if x == None:
        return 0
    else:
        return len(x)

def _uses_by(by):
    if _is_expr(by) | _is_string(by):
        return True
    elif isinstance(by, list):
        # Allow passing an empty list to `by`
        if _safe_len(by) == 0:
            return False
        else:
            return True
    else:
        return False

def _is_list(x):
    return isinstance(x, list)

def _is_series(x):
    return isinstance(x, pl.Series)

def _is_expr(x):
    return isinstance(x, pl.Expr)

def _is_string(x):
    return isinstance(x, str)

def _is_type(x):
    return type(x) == type

def _is_tuple(x):
    return isinstance(x, tuple)

#  Wrap all str inputs in col()  
def _col_exprs(x):
    if _is_list(x) | _is_series(x):
        return [_col_expr(val) for val in x]
    else:
        return [_col_expr(x)]

def _col_expr(x):
    if _is_expr(x) | _is_series(x):
        return x
    elif _is_string(x) | _is_type(x):
        return pl.col(x)
    else:
       raise ValueError("Invalid input for column selection") 

def _repeat(x, times):
    if not_(_is_list(x)):
        x = [x]
    return x * times