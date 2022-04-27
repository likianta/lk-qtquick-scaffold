"""
fix typehint of Signal and Slot.
"""
from typing import Union

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtQml import QJSValue

# hold some objects globally (elevate their refcount), to prevent python gc.
__global_life_cycle = []


def slot(*argtypes: Union[type, str], name='',
         result: Union[str, type, None] = None):
    """
    args:
        argtypes: see also `def _reformat_argtypes`.
    """
    if result not in (None, str) and type(result) is not str:
        result = 'QVariant'
    
    argtypes = _reformat_argtypes(argtypes)
    
    def decorator(func):
        nonlocal argtypes, name, result
        __global_life_cycle.append(
            Slot(*argtypes, name=(name or func.__name__), result=result)(func)
        )
        return func
    
    return decorator


def _reformat_argtypes(argtypes: tuple) -> tuple:
    """
    args:
        argtypes: tuple[union[type, str alias], ...]
            type_alias: to reduce additionally imports for some un-basic types,
                we support using their alias. the alias will be converted to
                corresponding types here:
                    'qobject'   ->  QObject
                    'item'      ->  QObject
                    'any'       ->  QJSValue
                    'pyobject'  ->  QJSValue
                    'object'    ->  QJSValue
    """
    new_argtypes = []
    for t in argtypes:
        if t in ('qobject', 'item'):
            t = QObject
        elif t in ('any', 'pyobject', 'object'):
            t = QJSValue
        elif t not in (bool, bytes, float, int, str, QObject):
            t = QJSValue
        new_argtypes.append(t)
    return tuple(new_argtypes)


# -----------------------------------------------------------------------------

class SignalTypeHint:
    
    def __call__(self, *argtypes: type):
        pass
    
    def connect(self, func):
        pass
    
    def emit(self, *args):
        pass


signal: SignalTypeHint


def __init__():
    global signal
    signal = Signal


__init__()
